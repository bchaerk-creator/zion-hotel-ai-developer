import sys; sys.path.insert(0, "producao/clube/diagnostico")
from brief_reuniao import brief
quente = {"b_situacao":"Já opera hospedagem","b_infra":"Sim, entro com a infraestrutura","b_capital":"R$ 150 mil a R$ 400 mil","b_aprender":"Sim, agora","b_mentoria":"Sim","documentacao_meta":"escritura_ou_matrícula_em_dia"}
b = brief(quente); assert (b["temperatura"], b["perfil"], b["pontos"]) == ("QUENTE", "Parceiro pronto", 9), b
assert b["opera"] and b["oferta_principal"].startswith("Mentoria") and "inscrição do terreno" in b["oferta_minima"]
assert any("operação" in p for p in b["perguntas"])
sem_doc = dict(quente); sem_doc.pop("documentacao_meta"); assert brief(sem_doc)["perfil"].startswith("Parceiro pronto (confirmar")
descap = {"b_situacao":"Tem terreno, não opera","b_infra":"Não tenho como investir na infraestrutura","b_capital":"Ainda não","b_aprender":"Sim, se entender o caminho","b_mentoria":"Agora não","documentacao_meta":"só_contrato_ou_posse"}
b = brief(descap); assert b["perfil"] == "Descapitalizado com vontade" and b["temperatura"] == "FRIO", b
nomes = " ".join(o[0] for o in b["objecoes"]).lower()
assert "dinheiro" in nomes and "escritura" in nomes and "sócio" in nomes, nomes
assert b["oferta_principal"].startswith("Clube")
fazer = {"b_situacao":"Tem terreno, não opera","b_infra":"Não tenho como investir na infraestrutura","b_capital":"Ainda não","b_aprender":"Não","b_mentoria":"Agora não"}
b = brief(fazer); assert b["perfil"] == "Quer que façam por ele" and b["temperatura"] == "FRIO", b
sem = {"b_situacao":"Sem terreno","b_aprender":"Sim, agora","b_mentoria":"Sim"}
b = brief(sem); assert b["perfil"] == "Ainda sem terreno" and "inscrição do terreno" not in b["oferta_minima"], b
print("OK · 5 perfis")
