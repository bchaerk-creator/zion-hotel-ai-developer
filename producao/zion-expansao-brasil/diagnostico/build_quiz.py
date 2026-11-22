"""Gera diagnostico/quiz.json: diagnóstico rápido das 7 frentes (lacunas), sem nota de viabilidade. Uso: python3 -I diagnostico/build_quiz.py"""
import json, pathlib
A = pathlib.Path(__file__).resolve().parent
OFFER = "037959a0-c602-4323-8e2f-e99902f377f4"
SEI, IDEIA, NAO = "Sei, e tenho dados", "Tenho uma ideia, mas sem dados", "Não sei"
P = [  # id, pergunta, título curto, lacuna, ok
 ("dem", "Você sabe qual é a demanda por hospedagem na sua região?", "Demanda da região",
  "Quantas pessoas procuram hospedagem na sua região, e de que perfil? Sem esse dado não dá para saber para quem o projeto é feito.",
  "Você já tem dados de demanda. Na sessão conferimos se eles sustentam o projeto."),
 ("saz", "Você sabe quais meses a região enche e quais esvazia (sazonalidade)?", "Sazonalidade",
  "Em quais meses a região enche e em quais esvazia? Isso define o caixa do ano inteiro, não só o da alta temporada.",
  "Você conhece a sazonalidade. Na sessão vemos como ela entra no seu caixa."),
 ("tkt", "Você sabe quanto o hóspede paga por diária na sua região e na sua categoria (ticket médio)?", "Ticket médio",
  "Quanto o hóspede paga por diária na sua região e na sua categoria? É a base de qualquer projeção de receita.",
  "Você tem uma referência de ticket médio. Na sessão conferimos se ela é realista."),
 ("ocu", "Você sabe quantas diárias do mês costumam ser vendidas por hospedagens parecidas (taxa de ocupação)?", "Taxa de ocupação",
  "Quantas diárias do mês costumam ser vendidas por hospedagens parecidas? Sem uma referência real, a receita vira chute.",
  "Você tem uma referência de ocupação. Na sessão confirmamos a fonte e o período."),
 ("orc", "Você sabe quanto custa implantar o projeto, etapa por etapa (orçamento)?", "Orçamento",
  "Quanto custa implantar o projeto, etapa por etapa? Parceiros e investidores costumam começar a conversa por aqui.",
  "Você tem um orçamento. Na sessão vemos se ele cobre todas as etapas."),
 ("ret", "Você sabe quanto o projeto precisa investir, quanto entra e em quanto tempo o investimento volta?", "Investimento e retorno",
  "Quanto investir, quanto entra, quanto sai e em quanto tempo volta? O número depende dos itens acima; sem eles só dá para trabalhar com hipóteses, e hipótese não é garantia.",
  "Você tem uma conta de investimento e retorno. Na sessão testamos as premissas."),
 ("jur", "Você conhece a estrutura jurídica do projeto (terreno, licenças e forma de sociedade ou parceria)?", "Estrutura jurídica",
  "Terreno, licenças e a forma de sociedade ou parceria estão resolvidos? Sem isso a conversa com parceiros costuma travar.",
  "Você conhece a estrutura jurídica. Na sessão revisamos o que falta documentar."),
]
steps = [{"id": "s_intro", "order": 0, "name": "Abertura", "blocks": [
  {"id": "b_intro_t", "type": "text", "align": "center", "body": "Diagnóstico rápido: o que você já sabe sobre o seu projeto de hospedagem?"},
  {"id": "b_intro_d", "type": "description", "align": "center", "body": "7 perguntas, 2 minutos, resultado na hora. É uma orientação automática, não uma avaliação técnica de viabilidade. A análise do seu caso acontece na sessão."},
  {"id": "b_intro_b", "type": "button", "label": "Começar", "action": "next", "variant": "solid"}]},
 {"id": "s_situ", "order": 1, "name": "Situação", "blocks": [{"id": "b_situ", "type": "options", "title": "Qual é a sua situação?", "required": True, "mapping": {"scope": "none"},
  "options": [{"id": f"o_situ_{i}", "label": t, "value": t} for i, t in enumerate(["Tenho terreno", "Tenho hospedagem", "Estou buscando terreno", "Ainda planejando"])]}]}]
for n, (k, q, *_r) in enumerate(P, start=2):
    steps.append({"id": f"s_{k}", "order": n, "name": q[:40], "blocks": [{"id": f"b_{k}", "type": "options", "title": q, "required": True, "mapping": {"scope": "none"},
      "options": [{"id": f"o_{k}_a", "label": SEI, "value": SEI, "score": 2}, {"id": f"o_{k}_b", "label": IDEIA, "value": IDEIA, "score": 1}, {"id": f"o_{k}_c", "label": NAO, "value": NAO, "score": 0}]}]})
steps.append({"id": "s_contato", "order": 9, "name": "Seus dados", "blocks": [{"id": "b_contato", "type": "capture", "title": "Para mostrar o seu resultado", "submitLabel": "Ver meu resultado", "fields": [
  {"id": "c_nome", "fieldType": "text", "label": "Seu nome", "required": True, "mapping": {"scope": "lead", "target": "name"}},
  {"id": "c_email", "fieldType": "email", "label": "E-mail", "required": True, "mapping": {"scope": "lead", "target": "email"}},
  {"id": "c_whats", "fieldType": "phone", "label": "WhatsApp", "required": True, "mapping": {"scope": "lead", "target": "phone"}},
  {"id": "c_local", "fieldType": "text", "label": "Cidade e estado do terreno ou da hospedagem", "required": True, "mapping": {"scope": "none"}},
  {"id": "c_mkt", "fieldType": "switch", "label": "Aceito receber conteúdos e novidades da Zion (opcional, separado do resultado)", "required": False, "mapping": {"scope": "none"}}]}]})
res = [{"id": "b_res_t", "type": "text", "align": "center", "body": "O seu diagnóstico, frente por frente"}]
for k, q, titulo, gap, ok in P:
    res.append({"id": f"b_ok_{k}", "type": "alert", "variant": "success", "title": titulo + ": coberto", "body": ok, "displayRule": {"when": [{"field": f"b_{k}", "op": "eq", "value": SEI}]}})
    res.append({"id": f"b_gap_{k}", "type": "alert", "variant": "warning", "title": titulo + ": falta definir", "body": gap, "displayRule": {"when": [{"field": f"b_{k}", "op": "in", "value": [IDEIA, NAO]}]}})
res += [
 {"id": "b_fecha", "type": "description", "align": "left", "body": "Quem tem um terreno ou uma hospedagem e quer buscar parceria ou investimento precisa de direcionamento antes de qualquer conversa. O ideal é fazer a sessão de 60 minutos com a nossa equipe e sair com o passo a passo de como começar."},
 {"id": "b_entregas", "type": "checklist", "title": "O que você recebe na sessão de R$ 270", "items": [{"id": f"e{i}", "text": t} for i, t in enumerate(["Sessão individual online de 60 minutos", "Diagnóstico preliminar personalizado", "Avaliação preliminar do projeto", "Estratégia de busca de recursos, sócios e investidores", "Argumentação comercial preliminar", "Dossiê personalizado em PDF", "Plano de ação de 30/60/90 dias", "Acesso ao Zion Land Bank, sem cobrança adicional (cadastro sujeito a avaliação)", "Área de membros Zion com documentos e conteúdos introdutórios"])]},
 {"id": "b_alert", "type": "alert", "variant": "info", "title": "Como funciona", "body": "Você paga, o calendário abre, escolhe o horário e recebe diagnóstico, dossiê em PDF e plano de ação de 30/60/90 dias. A Zion avalia cada caso."},
 {"id": "b_off", "type": "offer", "offerId": OFFER, "productName": "Sessão Zion 360°", "offerName": "Sessão de Diagnóstico e Estratégia Personalizada Zion 360°", "priceLabel": "R$ 270 · Pix ou cartão", "ctaLabel": "Contratar sessão e liberar calendário"}]
steps.append({"id": "s_result", "order": 10, "name": "Resultado", "blocks": res})
theme = {"headerBg": "#1B2117", "headerText": "#FEF5F0", "headerSubText": "#DED6BF", "logoBg": "#1B2117", "logoText": "#C9B37E", "pageBg": "#FEF5F0", "cardBg": "#FFFFFF", "cardBorder": "#DED6BF", "inputBg": "#FFFFFF", "inputBorder": "#CFC6BB", "labelColor": "#040605", "placeholder": "#8A8379", "btnBg": "#C9B37E", "btnText": "#1B2117", "cardR": "12px", "inputR": "8px", "btnR": "999px", "font": "Jost", "inputStyle": "bordered"}
settings = {"dedupRule": "merge", "dedupKey": "email_phone", "mergeStrategy": "incoming", "showLgpd": True, "lgpdRequired": True, "originTag": "DIAGNOSTICO RAPIDO 270",
 "completion": {"title": "Seu diagnóstico", "subtitle": "Esta nota mede o quanto você já sabe sobre o projeto, não a viabilidade do terreno.", "showScore": True, "scoreLabel": "Informações do projeto em mãos (máximo 14)",
  "scoreRanges": [
   {"id": "r_baixo", "min": 0, "max": 4, "badge": "Muito a mapear", "title": "Seu projeto ainda tem muito a ser mapeado", "message": "Você respondeu que ainda não tem a maior parte dos dados que parceiros e investidores costumam pedir. Isso é comum no começo. Esta nota mede só o que você já sabe, não o valor do seu terreno. Na sessão de 60 minutos organizamos o que falta e mostramos por onde começar."},
   {"id": "r_medio", "min": 5, "max": 9, "badge": "Parcialmente mapeado", "title": "Você já tem parte do caminho", "message": "Você tem algumas informações, mas ainda faltam dados para sustentar uma conversa com parceiros e investidores. Esta nota mede só o que você já sabe, não o valor do seu terreno. Na sessão avaliamos o seu caso e definimos os primeiros passos."},
   {"id": "r_alto", "min": 10, "max": 14, "badge": "Bem mapeado", "title": "Você já tem boa parte das informações", "message": "Você já reuniu muita informação. Esta nota mede só o que você já sabe, não a viabilidade do seu terreno. Na sessão validamos os números e preparamos a sua abordagem."}],
  "buttons": [{"label": "Contratar sessão e liberar calendário", "url": "https://payments.clickmax.io/W11sGasqD2?utm_source=meta&utm_medium=paid&utm_campaign=sessao-270&utm_content=diagnostico-resultado"}]},
 "lgpdText": "Aceito que a Zion use estas respostas para gerar o meu resultado e falar comigo sobre ele. O consentimento para receber conteúdos e novidades é separado e opcional."}
q = {"version": 1, "kind": "quiz", "name": "Diagnóstico rápido Zion · 7 frentes", "title": "O que você já sabe sobre o seu projeto de hospedagem?", "steps": steps, "theme": theme, "settings": settings}
(A / "quiz.json").write_text(json.dumps(q, ensure_ascii=False)); print(len(json.dumps(q, ensure_ascii=False)), "chars;", len(steps), "etapas;", len(res), "blocos no resultado")
