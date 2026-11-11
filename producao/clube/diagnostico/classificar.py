"""Classifica a resposta do formulário Meta "Adesão Terreno" / "Diagnóstico do terreno" em três níveis.
Regra fixa e explicável. Entrada: dict com as chaves usadas no ClickMax (customFields).
Saída: (nivel, pontos, motivos) com nivel em {"alto","ajustes","preparacao"}.
"""
import unicodedata

def _n(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).replace("r$ ", "r$")

def classificar(cf):
    p = 0; m = []
    doc = _n(cf.get("documentacao_meta"))
    if "escritura" in doc or "matricula" in doc: p += 2; m.append("documentação em dia")
    elif "contrato" in doc or "posse" in doc: p += 1; m.append("documentação a regularizar")
    else: m.append("sem documentação ainda")
    perfil = _n(cf.get("perfil_area"))
    if "turistica" in perfil or "empreendimento" in perfil or "pousada" in perfil or "desenvolvimento" in perfil:
        p += 2; m.append("área ou operação em região turística")
    elif "rural" in perfil or "natural" in perfil: p += 1; m.append("área natural, demanda a confirmar")
    area = _n(cf.get("area"))
    if area and "ate 5.000" not in area and "ate 5000" not in area: p += 1; m.append("área acima de 5.000 m²")
    inv = _n(cf.get("investimento"))
    if inv.startswith("acima") or inv.startswith("r$1 milhao"): p += 2; m.append("investimento previsto acima de R$ 1 milhão")
    elif inv.startswith("r$400"): p += 1; m.append("investimento previsto entre R$ 400 mil e R$ 1 milhão")
    val = _n(cf.get("valor_area_meta"))
    if val and not val.startswith("ate"): p += 1; m.append("área com valor acima de R$ 500 mil")
    nivel = "alto" if p >= 7 else "ajustes" if p >= 3 else "preparacao"
    return nivel, p, m

TAGS = {"alto": "c8867c45-e440-4e78-8d2c-c4933fc30cc8",
        "ajustes": "b12ab070-cb50-4f42-bd27-ba85d3d32b21",
        "preparacao": "8b65d297-158a-46e3-9f32-6264c5afd386"}
TITULO = {"alto": "potencial alto para o Land Bank",
          "ajustes": "potencial com ajustes",
          "preparacao": "projeto em preparação"}

if __name__ == "__main__":
    import json, sys
    cf = json.load(sys.stdin)
    n, p, m = classificar(cf)
    print(json.dumps({"nivel": n, "pontos": p, "motivos": m, "tagId": TAGS[n]}, ensure_ascii=False))
