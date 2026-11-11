import json, sys, collections
sys.path.insert(0, "producao/clube/diagnostico")
from classificar import classificar
casos = [
 ({"documentacao_meta":"escritura ou matrícula em dia","perfil_area":"terreno em área turística","area":"mais de 50.000 m²","investimento":"r$1 milhão a r$3 milhões","valor_area_meta":"acima de r$ 5 milhões"}, "alto", 8),
 ({"documentacao_meta":"ainda não tenho","perfil_area":"área rural ou natural","area":"até 5.000 m²","investimento":"r$150 mil a r$400 mil","valor_area_meta":"até r$ 500 mil"}, "preparacao", 1),
 ({"documentacao_meta":"só contrato ou posse","perfil_area":"terreno em área turística","area":"5.000 m² a 20.000 m²","investimento":"r$150 mil a r$400 mil","valor_area_meta":"até r$ 500 mil"}, "ajustes", 4),
 ({"documentacao_meta":"escritura ou matrícula em dia","perfil_area":"hotel ou pousada que deseja expandir","area":"até 5.000 m²","investimento":"r$400 mil a r$1 milhão","valor_area_meta":"de r$ 500 mil a r$ 2 milhões"}, "ajustes", 6),
 ({}, "preparacao", 0),
]
for cf, esperado, pts in casos:
    n, p, m = classificar(cf); assert (n, p) == (esperado, pts), (cf, n, p, m)
# distribuição na base real de 74 leads
d = json.load(open("/tmp/claude-0/-home-user-zion-hotel-ai-developer/20b679d3-1387-56c1-a153-2b815cdf3664/scratchpad/ingest/payloads.json"))
c = collections.Counter(classificar(x["payload"].get("customFields") or {})[0] for x in d)
print("OK 5 casos ·", dict(c))
