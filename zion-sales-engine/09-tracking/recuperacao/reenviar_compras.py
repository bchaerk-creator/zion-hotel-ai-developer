#!/usr/bin/env python3
"""Reenvia compras reais ja pagas para a Conversions API da Meta (recuperacao).

SEGURANCA E REGRAS
- Padrao: --dry-run (nao toca a rede). So envia com --send.
- O CSV com dados dos compradores fica FORA do repositorio. O script RECUSA ler CSV de dentro do repo
  (use --allow-inside-repo apenas para o arquivo .example fictício).
- Pixel e token so por variaveis de ambiente: META_PIXEL_ID, META_ACCESS_TOKEN
  (opcionais: META_GRAPH_VERSION, META_TEST_EVENT_CODE, META_GRAPH_BASE).
- E-mail e telefone saem SO com SHA-256. Nada em texto puro vai ao Meta nem ao terminal.
- Meta aceita evento com ate 7 dias: linhas mais antigas sao bloqueadas.
- NUNCA atribui a anuncio sem dado: UTMs/fbc/fbp so vao se estiverem preenchidos no CSV.
- Idempotencia: arquivo de controle (so event_id) ao lado do CSV; linha ja enviada e pulada.

Uso:
  python3 reenviar_compras.py --csv /caminho/fora/do/repo/compras.csv            # dry-run
  META_TEST_EVENT_CODE=TESTxxxx META_PIXEL_ID=... META_ACCESS_TOKEN=... \
      python3 reenviar_compras.py --csv ... --send                                # envio de teste
  META_PIXEL_ID=... META_ACCESS_TOKEN=... python3 reenviar_compras.py --csv ... --send   # envio real
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MAX_AGE_DAYS = 7
MIN_VALUE, MAX_VALUE = 1.0, 2000.0
UTM_COLS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "src", "sck"]


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm_email(v):
    s = (v or "").strip().lower()
    return s if "@" in s else None


def norm_phone(v):
    d = re.sub(r"\D+", "", v or "").lstrip("0")
    if not d:
        return None
    if len(d) in (10, 11):
        d = "55" + d
    return d if len(d) >= 11 else None


def norm_name(v):
    s = (v or "").strip().lower()
    return s or None


def parse_time(v):
    s = (v or "").strip()
    if re.fullmatch(r"\d{10}", s):
        return int(s)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def build_event(row, now):
    """Devolve (evento, None) ou (None, motivo_do_bloqueio)."""
    event_id = (row.get("event_id") or "").strip()
    if not event_id:
        return None, "sem_event_id"
    try:
        value = round(float((row.get("value_brl") or "").replace(",", ".")), 2)
    except ValueError:
        return None, "valor_invalido"
    if not (MIN_VALUE <= value <= MAX_VALUE):
        return None, f"valor_fora_da_faixa:{value}"
    t = parse_time(row.get("paid_at"))
    if t is None:
        return None, "hora_invalida"
    if now - t > MAX_AGE_DAYS * 86400:
        return None, "mais_de_7_dias_o_meta_recusa"
    if t > now + 300:
        return None, "hora_no_futuro"
    ud = {}
    em, ph = norm_email(row.get("email")), norm_phone(row.get("phone"))
    if em:
        ud["em"] = [sha256(em)]
        ud["external_id"] = [sha256(em)]
    if ph:
        ud["ph"] = [sha256(ph)]
    nm = norm_name(row.get("fullname"))
    if nm:
        parts = nm.split()
        ud["fn"] = [sha256(parts[0])]
        if len(parts) > 1:
            ud["ln"] = [sha256(parts[-1])]
    if (row.get("fbc") or "").strip():
        ud["fbc"] = row["fbc"].strip()
    if (row.get("fbp") or "").strip():
        ud["fbp"] = row["fbp"].strip()
    if not (ud.get("em") or ud.get("ph") or ud.get("fbc") or ud.get("fbp")):
        return None, "sem_dado_para_correspondencia"
    currency = (row.get("currency") or "BRL").strip().upper()
    cd = {"value": value, "currency": currency, "order_id": event_id}
    for k in UTM_COLS:  # so o que existe no CSV; nada e inventado
        if (row.get(k) or "").strip():
            cd[k] = row[k].strip()
    ev = {
        "event_name": "Purchase",
        "event_time": t,
        "event_id": event_id,
        "action_source": "website",
        "user_data": ud,
        "custom_data": cd,
    }
    if (row.get("event_source_url") or "").strip():
        ev["event_source_url"] = row["event_source_url"].strip()
    return ev, None


def repo_root(start):
    p = Path(start).resolve()
    for cand in [p, *p.parents]:
        if (cand / ".git").exists():
            return cand
    return None


def inside_repo(csv_path):
    root = repo_root(Path(__file__).parent)
    if root is None:
        return False
    try:
        Path(csv_path).resolve().relative_to(root)
        return True
    except ValueError:
        return False


def load_ledger(path):
    if not path.exists():
        return set()
    return {ln.strip() for ln in path.read_text().splitlines() if ln.strip()}


def post_events(events, env, opener=urllib.request.urlopen):
    base = env.get("META_GRAPH_BASE") or "https://graph.facebook.com"
    ver = env.get("META_GRAPH_VERSION") or "v21.0"
    url = f"{base}/{ver}/{env['META_PIXEL_ID']}/events"
    payload = {"data": events, "access_token": env["META_ACCESS_TOKEN"]}
    if env.get("META_TEST_EVENT_CODE"):
        payload["test_event_code"] = env["META_TEST_EVENT_CODE"]
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"content-type": "application/json"}, method="POST")
    with opener(req, timeout=20) as r:
        return json.loads(r.read().decode())


def run(args, env=None, now=None, out=print, opener=urllib.request.urlopen):
    env = os.environ if env is None else env
    now = int(time.time()) if now is None else now
    if inside_repo(args.csv) and not args.allow_inside_repo:
        out("RECUSADO: o CSV esta dentro do repositorio. Dados de compradores ficam FORA dele.")
        return 2
    with open(args.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ledger_path = Path(args.ledger or (str(args.csv) + ".enviados"))
    done = load_ledger(ledger_path)
    ready, blocked = [], []
    for i, row in enumerate(rows, 1):
        eid = (row.get("event_id") or "").strip()
        if eid in done:
            out(f"linha {i} {eid}: JA ENVIADA (pulada)")
            continue
        ev, why = build_event(row, now)
        if why:
            blocked.append((i, eid, why))
            out(f"linha {i} {eid or '-'}: BLOQUEADA ({why})")
            continue
        age_h = (now - ev["event_time"]) / 3600
        out(f"linha {i} {eid}: OK value={ev['custom_data']['value']:.2f} {ev['custom_data']['currency']} "
            f"idade={age_h:.1f}h em={ev['user_data'].get('em', ['-'])[0][:8]}... ph={ev['user_data'].get('ph', ['-'])[0][:8]}... "
            f"utms={[k for k in UTM_COLS if k in ev['custom_data']] or 'nenhuma'}")
        ready.append((eid, ev))
    if not args.send:
        out(f"DRY-RUN: {len(ready)} pronta(s), {len(blocked)} bloqueada(s). Nada foi enviado. Use --send para enviar.")
        return 0
    missing = [k for k in ("META_PIXEL_ID", "META_ACCESS_TOKEN") if not env.get(k)]
    if missing:
        out(f"FALTAM variaveis de ambiente: {', '.join(missing)}")
        return 2
    if not ready:
        out("Nada para enviar.")
        return 0
    mode = "TESTE (aba Testar eventos, nao conta)" if env.get("META_TEST_EVENT_CODE") else "REAL (conta como Purchase)"
    out(f"Enviando {len(ready)} evento(s) em modo {mode}.")
    try:
        resp = post_events([e for _, e in ready], env, opener)
    except Exception as e:  # noqa: BLE001 - nao vazar token
        out(f"FALHA no envio: {type(e).__name__}")
        return 1
    received = resp.get("events_received", 0)
    out(f"Meta respondeu: events_received={received} fbtrace_id={resp.get('fbtrace_id')}")
    if received >= len(ready):
        if not env.get("META_TEST_EVENT_CODE"):  # envio de teste nao entra no controle
            with ledger_path.open("a") as f:
                for eid, _ in ready:
                    f.write(eid + "\n")
        return 0
    out("Meta nao confirmou todos os eventos. Controle NAO atualizado.")
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--send", action="store_true", help="envia de verdade (padrao e dry-run)")
    ap.add_argument("--ledger", help="arquivo de controle (padrao: <csv>.enviados)")
    ap.add_argument("--allow-inside-repo", action="store_true", help="so para o .csv.example ficticio")
    return run(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
