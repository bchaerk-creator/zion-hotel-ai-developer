import sys; sys.path.insert(0, "producao/clube/diagnostico")
from brief_reuniao import brief
quente = {"b_situacao":"Terreno com infraestrutura","b_doc":"Escritura ou matrícula em dia","b_dif":"Um parceiro ou investidor","b_aprender":"Sim, agora","b_parceiro":"Quer ser parceiro Zion","b_infra":"Sim, entro com a infraestrutura","b_capital":"R$ 150 mil a R$ 400 mil","b_mentoria":"Sim","b_decisor":"Decide sozinho","b_clube":"Sim"}
b = brief(quente); assert (b["temperatura"], b["perfil"]) == ("QUENTE", "Parceiro pronto"), b
assert b["oferta_principal"].startswith("Mentoria") and "inscrição do terreno" in b["oferta_minima"]
descap = {"b_situacao":"Terreno sem infraestrutura","b_doc":"Só contrato ou posse","b_dif":"Capital para o projeto","b_aprender":"Sim, se entender o caminho","b_parceiro":"Quer entender a parceria","b_infra":"Não tenho como investir na infraestrutura","b_capital":"Ainda não","b_mentoria":"Agora não","b_decisor":"Decide junto com outra pessoa","b_clube":"Quer saber mais"}
b = brief(descap); assert b["perfil"] == "Descapitalizado com vontade" and b["temperatura"] in ("MORNO","FRIO"), b
nomes = [o[0] for o in b["objecoes"]]
assert any("dinheiro" in n for n in nomes) and any("sócio" in n for n in nomes) and any("escritura" in n for n in nomes), nomes
assert b["oferta_principal"].startswith("Clube")
fazer = {"b_situacao":"Terreno sem infraestrutura","b_doc":"Escritura ou matrícula em dia","b_dif":"Não sei por onde começar","b_aprender":"Não","b_parceiro":"Quer fazer sozinho","b_infra":"Não tenho como investir na infraestrutura","b_capital":"Ainda não","b_mentoria":"Agora não","b_decisor":"Decide sozinho","b_clube":"Não"}
b = brief(fazer); assert b["perfil"] == "Quer que façam por ele" and b["temperatura"] == "FRIO", b
assert "façam" in " ".join(o[0] for o in b["objecoes"]).lower()
sem = {"b_situacao":"Procurando terreno","b_doc":"Ainda não tenho","b_aprender":"Sim, agora","b_mentoria":"Sim"}
b = brief(sem); assert b["perfil"] == "Ainda sem terreno" and "inscrição do terreno" not in b["oferta_minima"], b
print("OK · 4 perfis")
