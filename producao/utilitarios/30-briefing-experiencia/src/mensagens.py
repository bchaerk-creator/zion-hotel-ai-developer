"""Fonte única dos campos e dos textos da Ferramenta 30 (Gerador de Briefing de Experiência).
Mesma mecânica da Ferramenta 11 (Kit de Mensagens). Segmentos:
  ("t", texto)            sempre entra; {campo} obrigatório vira [PREENCHA: rótulo] se estiver vazio
  ("o", texto)            opcional: só entra se TODOS os campos do texto estiverem preenchidos
  ("v", campo, texto)     só entra se o campo estiver VAZIO
"""

# (chave, rótulo, seção, obrigatório, ajuda, exemplo fictício). Seção H = a experiência (uma vez); R = esta saída.
CAMPOS = [
    ("exp", "Nome da experiência", "H", True, "Como o hóspede vai conhecer a experiência.", "Café da manhã na trilha do mirante"),
    ("assina", "Quem assina as mensagens", "H", True, "Seu nome ou o nome da equipe.", "Equipe Recanto Exemplo (fictícia)"),
    ("conduz", "Quem conduz", "H", True, "Nome de quem guia ou atende o grupo.", "Rafael, guia local (fictício)"),
    ("resumo", "O que acontece, em uma frase", "H", True, "Frase completa, com ponto final.", "Uma caminhada leve até o mirante, com café da manhã servido no alto da serra."),
    ("duracao", "Duração", "H", True, "Escreva como você fala. Ex.: 2h30.", "cerca de 3 horas"),
    ("ponto", "Ponto de encontro", "H", True, "Onde o grupo se encontra.", "recepção do Recanto Exemplo"),
    ("inclui", "O que está incluído", "H", True, "Lista curta, separada por vírgulas.", "guia, café da manhã completo, água e transporte até o início da trilha"),
    ("nao_inclui", "O que não está incluído", "H", False, "Opcional.", "bebidas alcoólicas e gorjeta"),
    ("levar", "O que levar", "H", True, "Lista curta, separada por vírgulas.", "tênis fechado, casaco leve, protetor solar e uma garrafa de água"),
    ("para_quem", "Para quem é", "H", True, "Exigência física e idade, se houver.", "pessoas que caminham 40 minutos em subida leve; crianças a partir de 8 anos, acompanhadas"),
    ("clima", "O que acontece com chuva ou mau tempo", "H", True, "Complete a frase: \"Com chuva ou mau tempo, ...\"", "a saída é remarcada sem custo ou o valor é devolvido"),
    ("minimo", "Mínimo de participantes para confirmar", "H", True, "Número. Use a Calculadora de Custos (Ferramenta 29) se quiser fazer a conta.", "4"),
    ("cancel", "Regra de cancelamento pelo cliente", "H", True, "Frase completa, com ponto final.", "Cancelamentos até 24 horas antes têm devolução integral."),
    ("preco", "Preço por pessoa", "H", False, "Opcional. Escreva como vai aparecer: R$ 180.", "R$ 180"),
    ("seguranca", "Orientação de segurança", "H", False, "Frase completa, com ponto final.", "Siga sempre o guia e não saia da trilha marcada."),
    ("contato", "Contato no dia", "H", True, "Telefone ou WhatsApp que responde no dia.", "(00) 90000-0000"),
    ("cliente", "Nome do cliente ou do grupo", "R", True, "Quem reservou.", "Paulo"),
    ("data", "Data da saída", "R", True, "Data.", "2026-12-12"),
    ("hora", "Horário de encontro", "R", True, "Ex.: 7h.", "7h"),
    ("pessoas", "Participantes confirmados", "R", True, "Número.", "5"),
    ("obs", "Restrições informadas pelo grupo", "R", False, "Alimentação, saúde, mobilidade. Opcional.", "uma pessoa não come glúten"),
]
DATAS = {"data"}

# (id, título, quando enviar, regra de data, segmentos). Regras: "logo", "data-2", "data-1", "data", "resposta"
MENSAGENS = [
    ("B01", "Descrição para anúncio ou cardápio", "Para publicar ou enviar a quem pergunta", "logo", [
        ("t", "{exp}. {resumo} Duração: {duracao}. Incluído: {inclui}."),
        ("o", " Não incluído: {nao_inclui}."),
        ("t", " Para quem é: {para_quem}. O que levar: {levar}."),
        ("o", " Valor: {preco} por pessoa."),
        ("t", " A saída é confirmada a partir de {minimo} participantes. Com chuva ou mau tempo, {clima}. {cancel}")]),
    ("B02", "Confirmação da reserva", "Logo depois que o cliente reservar", "logo", [
        ("t", "Olá, {cliente}! Sua reserva para {exp} está anotada: {data}, às {hora}, com encontro na {ponto}, para {pessoas} pessoa(s). "
              "A saída é confirmada a partir de {minimo} participantes; avisamos até dois dias antes. {cancel} Qualquer dúvida, é só responder aqui. {assina}.")]),
    ("B03", "Saída confirmada", "Dois dias antes, se o mínimo foi atingido", "data-2", [
        ("t", "Olá, {cliente}! A saída de {exp} em {data} está confirmada. Encontro às {hora}, na {ponto}. "
              "Na véspera mandamos o lembrete com o que levar. {assina}.")]),
    ("B04", "Saída não confirmada (abaixo do mínimo)", "Dois dias antes, se o mínimo não foi atingido", "data-2", [
        ("t", "Olá, {cliente}! A saída de {exp} em {data} não atingiu o mínimo de {minimo} participantes. "
              "Podemos remarcar para outra data ou devolver o valor pago, como você preferir. Qual opção é melhor para você? {assina}.")]),
    ("B05", "Lembrete da véspera", "Na véspera, à tarde", "data-1", [
        ("t", "Olá, {cliente}! Amanhã é dia de {exp}. Encontro às {hora}, na {ponto}; a experiência dura {duracao}. Leve {levar}."),
        ("o", " {seguranca}"),
        ("t", " Com chuva ou mau tempo, {clima}; se for o caso, avisamos cedo. No dia, fale com a gente pelo número {contato}. {assina}.")]),
    ("B06", "Briefing para quem conduz", "Na véspera, para o guia ou parceiro", "data-1", [
        ("t", "{conduz}, briefing de amanhã ({data}): {exp}, encontro às {hora} na {ponto}, {pessoas} participante(s), reserva em nome de {cliente}. "
              "Incluído: {inclui}. Duração prevista: {duracao}. Para quem é: {para_quem}."),
        ("o", " Restrições do grupo: {obs}."),
        ("v", "obs", " O grupo não informou restrições; confirme no encontro."),
        ("o", " Lembre o grupo: {seguranca}"),
        ("t", " Qualquer imprevisto, avise pelo número {contato}.")]),
    ("B07", "Resposta: mudança por clima", "Se o tempo obrigar a mudar", "resposta", [
        ("t", "Olá, {cliente}! A previsão para {exp} em {data} não está boa. Com chuva ou mau tempo, {clima}. "
              "Vamos combinar o melhor caminho para você? {assina}.")]),
    ("B08", "Agradecimento depois da experiência", "No fim do dia da saída", "data", [
        ("t", "{cliente}, obrigado por participar de {exp} hoje. Se puder, conte como foi para você; a sua opinião nos ajuda a melhorar a experiência. {assina}.")]),
]

def rotulo(k): return next(c[1] for c in CAMPOS if c[0] == k)
def obrig(k): return next(c[3] for c in CAMPOS if c[0] == k)
