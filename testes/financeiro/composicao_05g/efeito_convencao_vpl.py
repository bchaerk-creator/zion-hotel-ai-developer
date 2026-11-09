"""Comando 05G-B · P-O10a · efeito da convenção de desconto (independente, sem código da ZAIOS).
Compara o VPL atual (fluxo anual: ano 0 = -CAPEX inteiro; ano 1 = 1º ano de operação; anos 2-10 = regime; desconto no fim do ano)
com um VPL mensal (CAPEX pelo cronograma do P5 nos meses 2-9; operação a partir do mês 10; 10 anos completos de operação;
taxa mensal equivalente (1+i)^(1/12)-1; desconto no fim de cada mês). Mesmos dados do 05F (regra da ZAIOS, R2)."""
import json, pathlib, importlib.util, io, contextlib
AQUI = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r", AQUI.parent / "independente" / "composicao_05f_referencia.py")
with contextlib.redirect_stdout(io.StringIO()):
    M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
out = {}
for c in M.ENT["cenarios"]:
    e = M.estudo(c); i = 0.10; im = (1 + i) ** (1 / 12) - 1
    ab = M.MESES.index(c["mes_abertura"]); reg = M.regime(c, "bruta", "pct"); pri = M.primeiro_ano(c, "bruta", ab)
    linhas = {k: c["investimento"] * v for k, v in M.COM["linhas_capex_proporcao"].items()}; crono = M.cronograma(linhas)
    mes_proj = max(k + 1 for k, v in enumerate(crono) if v > 0) + 1
    ger = [m["ger"] for m in pri] + [reg[(ab + k) % 12]["ger"] for k in range(12, 120)]
    fl = []
    for mes in range(1, mes_proj + 120):
        v = -(crono[mes - 1] if mes <= len(crono) else 0); k = mes - mes_proj
        if 0 <= k < 120: v += ger[k]
        fl.append(v)
    vpl_m = sum(v / (1 + im) ** t for t, v in enumerate(fl, start=1))
    out[c["id"]] = {"vpl_anual_atual": e["vpl_sem"], "vpl_mensal_alternativo": vpl_m, "diferenca": vpl_m - e["vpl_sem"],
                    "diferenca_pct_do_capex": (vpl_m - e["vpl_sem"]) / e["capex"]}
(AQUI / "efeito_convencao_vpl.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out.items(): print(k, {a: round(b, 4) for a, b in v.items()})
