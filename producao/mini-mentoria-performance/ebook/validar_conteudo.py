"""Valida ebook/conteudo/mod<N>.json. Uso: python3 -I ebook/validar_conteudo.py 1 [2 3 ...]  (sem argumentos: 1..7)"""
import json, re, sys, pathlib
A = pathlib.Path(__file__).resolve().parent.parent
FORM = json.load(open(A/"fontes/formularios.json", encoding="utf8"))["questions"]
PROIBIDAS = [r"garanti", r"aumente (suas|seu|sua)", r"dobre", r"\bvai (lotar|encher|lucrar|faturar)", r"resultado certo", r"sem risco", r"ZAIOS", r"Land ?Bank", r"\bClub\b", r"Collection", r"R\$ ?47", r"R\$ ?19"]
def n(s): return len(re.findall(r"\w+", s, flags=re.U))
def chk(errs, lbl, s, lo, hi):
    if not isinstance(s, str): errs.append(f"{lbl}: não é texto"); return
    w = n(s)
    if w < lo or w > hi: errs.append(f"{lbl}: {w} palavras (esperado {lo}-{hi})")
    for p in PROIBIDAS:
        if re.search(p, s, flags=re.I): errs.append(f"{lbl}: termo proibido /{p}/")
def valida(m):
    f = A/f"ebook/conteudo/mod{m}.json"; errs = []
    try: d = json.load(open(f, encoding="utf8"))
    except Exception as e: return [f"JSON inválido: {e}"]
    if d.get("modulo") != m: errs.append("campo modulo errado")
    for k in ("titulo", "subtitulo"): chk(errs, k, d.get(k, ""), 2, 20)
    a = d.get("abertura", {}); chk(errs, "abertura.para_que_serve", a.get("para_que_serve", ""), 80, 140); chk(errs, "abertura.como_trabalhar", a.get("como_trabalhar", ""), 50, 90)
    t = a.get("tenha_em_maos", []); 
    if not (4 <= len(t) <= 6): errs.append("tenha_em_maos: 4 a 6 itens")
    ids = [q["id"] for q in FORM if q["module"] == m]; ps = d.get("perguntas", [])
    if [p.get("id") for p in ps] != ids: errs.append(f"perguntas: ids devem ser {ids}")
    for p in ps:
        i = p.get("id", "?")
        chk(errs, f"{i}.por_que_importa", p.get("por_que_importa", ""), 50, 90)
        cc = p.get("como_coletar", [])
        if not (4 <= len(cc) <= 5): errs.append(f"{i}.como_coletar: 4 a 5 passos")
        for k, s in enumerate(cc): chk(errs, f"{i}.como_coletar[{k}]", s, 12, 40)
        e = p.get("exemplo", {}); chk(errs, f"{i}.exemplo.titulo", e.get("titulo", ""), 2, 16); chk(errs, f"{i}.exemplo.texto", e.get("texto", ""), 70, 130)
        if not str(e.get("texto", "")).startswith("Dados fictícios:"): errs.append(f"{i}.exemplo.texto: deve começar com 'Dados fictícios:'")
        chk(errs, f"{i}.erro_comum", p.get("erro_comum", ""), 25, 60)
        for k in ("ausente", "parcial", "comprovado"): chk(errs, f"{i}.como_ler.{k}", p.get("como_ler", {}).get(k, ""), 15, 40)
        chk(errs, f"{i}.verificacao", p.get("verificacao", ""), 30, 70)
    fc = d.get("fechamento", {}); chk(errs, "fechamento.resumo", fc.get("resumo", ""), 60, 110); chk(errs, "fechamento.limites", fc.get("limites", ""), 40, 90)
    g = fc.get("glossario", [])
    if not (4 <= len(g) <= 6): errs.append("glossario: 4 a 6 termos")
    for x in g: chk(errs, "glossario." + str(x.get("termo")), x.get("definicao", ""), 5, 40)
    return errs
if __name__ == "__main__":
    mods = [int(x) for x in sys.argv[1:]] or list(range(1, 8)); bad = 0
    for m in mods:
        e = valida(m); print(f"módulo {m}: " + ("ok" if not e else f"{len(e)} problemas")); [print("  -", x) for x in e[:25]]; bad += bool(e)
    sys.exit(1 if bad else 0)
