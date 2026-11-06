"""Fonte única dos campos e das mensagens da Ferramenta 11 (Kit de Mensagens de Chegada e Saída).
Jornada e tom inspirados nos Scripts de Atendimento da Zion (Notion), generalizados.
Fora do kit por cautela: levar a conversa da plataforma para outro canal e pedir nota específica na avaliação.

Segmentos de cada mensagem:
  ("t", texto)            sempre entra; {campo} obrigatório vira [PREENCHA: rótulo] se estiver vazio
  ("o", texto)            opcional: só entra se TODOS os campos do texto estiverem preenchidos
  ("v", campo, texto)     só entra se o campo estiver VAZIO (alternativa ao opcional)
"""

# (chave, rótulo, seção, obrigatório, ajuda, exemplo fictício)
CAMPOS = [
    ("hosp", "Nome da hospedagem", "H", True, "Como o hóspede conhece o lugar.", "Recanto Exemplo"),
    ("anfit", "Quem assina as mensagens", "H", True, "Seu nome ou o nome da equipe.", "Marta (fictícia)"),
    ("end", "Endereço completo", "H", True, "Rua, número, bairro, cidade.", "Estrada Exemplo, km 4, Zona Rural, Cidade Exemplo (SC)"),
    ("mapa", "Link do mapa", "H", False, "Copie o link de compartilhamento do mapa.", "https://maps.example.com/recanto-exemplo"),
    ("chegar", "Referência para chegar", "H", False, "Um ponto de referência que evita erro no caminho.", "depois da ponte de madeira, entre na primeira estrada à direita"),
    ("estac", "Estacionamento", "H", False, "Onde o hóspede deixa o carro.", "há uma vaga coberta ao lado da unidade"),
    ("cin", "Check-in a partir de", "H", True, "Escreva como você fala. Ex.: 15h.", "15h"),
    ("climite", "Chegada até", "H", False, "Horário limite de chegada, se houver.", "21h"),
    ("cout", "Check-out até", "H", True, "Ex.: 11h.", "11h"),
    ("acesso", "Como é o acesso", "H", True, "Complete a frase: \"O acesso é por...\"", "fechadura com senha na porta principal"),
    ("wifi_rede", "Wi-Fi: nome da rede", "H", True, "", "RecantoExemplo"),
    ("wifi_senha", "Wi-Fi: senha", "H", True, "", "senha-ficticia-123"),
    ("regras", "Regras principais", "H", True, "Frases curtas, com ponto final.", "Não é permitido fumar dentro da unidade. Silêncio depois das 22h."),
    ("saida_inst", "O que fazer na saída", "H", True, "Complete a frase: \"Antes de sair, ...\"", "feche as janelas, deixe a louça na pia e deixe a chave na caixa ao lado da porta"),
    ("suporte", "Contato de suporte", "H", True, "Telefone ou WhatsApp que responde durante a estadia.", "(00) 90000-0000"),
    ("emerg", "Orientação de emergência", "H", False, "Frase completa, com ponto final.", "Em emergência, ligue 193 (Bombeiros) ou 192 (SAMU)."),
    ("avaliar", "Link para avaliação", "H", False, "Opcional. Só o link.", "https://example.com/avaliar-recanto"),
    ("dica", "Dica para a chegada", "H", False, "Frase completa, com ponto final.", "À noite a temperatura cai bastante, então vale trazer um agasalho."),
    ("nome", "Nome do hóspede", "R", True, "Como ele gosta de ser chamado.", "Paulo"),
    ("entrada", "Data de entrada", "R", True, "Data.", "2026-12-12"),
    ("saida", "Data de saída", "R", True, "Data.", "2026-12-14"),
    ("codigo", "Código de acesso desta reserva", "R", False, "Se a senha muda a cada reserva.", "4821"),
    ("hora_cheg", "Horário previsto de chegada", "R", False, "Preencha quando o hóspede responder.", ""),
]
DATAS = {"entrada", "saida"}

# (id, título, quando enviar (texto), regra de data, segmentos)
# regra de data: "logo", "entrada-2", "entrada", "entrada+1", "saida-1", "saida", "resposta"
MENSAGENS = [
    ("M01", "Confirmação da reserva", "Logo depois que a reserva for confirmada", "logo", [
        ("t", "Olá, {nome}! Sua reserva está confirmada: entrada em {entrada}, a partir das {cin}, e saída em {saida}, até as {cout}. "
              "Dois dias antes da chegada enviamos o endereço e as orientações de acesso. Qualquer dúvida, é só responder aqui. {anfit}, {hosp}.")]),
    ("M02", "Endereço e orientações de acesso", "Dois dias antes da entrada", "entrada-2", [
        ("t", "Olá, {nome}! Faltam poucos dias para a sua chegada. Endereço: {end}."),
        ("o", " Mapa: {mapa}"),
        ("o", " Para chegar: {chegar}."),
        ("o", " Estacionamento: {estac}."),
        ("t", " O check-in é a partir das {cin}"),
        ("o", " e a chegada deve ser até as {climite}"),
        ("t", ". O acesso é por {acesso}; no dia da entrada enviamos os detalhes."),
        ("o", " {dica}"),
        ("t", " Qual é o horário previsto da sua chegada? {anfit}, {hosp}.")]),
    ("M03", "Bom dia do dia da entrada", "No dia da entrada, pela manhã", "entrada", [
        ("t", "Bom dia, {nome}! Está tudo pronto para receber você hoje, a partir das {cin}."),
        ("o", " Anotamos sua chegada prevista para as {hora_cheg}; se mudar, é só avisar."),
        ("v", "hora_cheg", " Qual é o horário previsto da sua chegada?"),
        ("t", " {anfit}, {hosp}.")]),
    ("M04", "Boas-vindas com acesso e Wi-Fi", "Na chegada (ou pouco antes)", "entrada", [
        ("t", "{nome}, seja bem-vindo(a)! O acesso é por {acesso}."),
        ("o", " O código desta reserva é {codigo}."),
        ("t", " Wi-Fi: rede {wifi_rede}, senha {wifi_senha}. {regras} O check-out é até as {cout}. Se precisar de algo, fale com a gente pelo número {suporte}."),
        ("o", " {emerg}"),
        ("t", " {anfit}, {hosp}.")]),
    ("M05", "Apoio durante a estadia", "Na manhã seguinte à entrada (estadias de 2 noites ou mais)", "entrada+1", [
        ("t", "Bom dia, {nome}! Esperamos que a primeira noite tenha sido boa. "
              "Se precisar de alguma coisa ou de uma indicação na região, estamos por aqui no número {suporte}. {anfit}, {hosp}.")]),
    ("M06", "Lembrete da saída", "Na véspera da saída, à tarde ou à noite", "saida-1", [
        ("t", "Olá, {nome}! Um lembrete para amanhã: o check-out é até as {cout}. Antes de sair, {saida_inst}. "
              "Confira carregadores, documentos e itens pessoais. Se precisar de outro horário, pergunte que verificamos se é possível. {anfit}, {hosp}.")]),
    ("M07", "Dia da saída", "No dia da saída, pela manhã", "saida", [
        ("t", "Bom dia, {nome}! Hoje é o dia da saída, até as {cout}. Quando estiver pronto(a) para ir, nos avise por aqui. "
              "Obrigado pela estadia. {anfit}, {hosp}.")]),
    ("M08", "Agradecimento e pedido de avaliação", "Algumas horas depois da saída", "saida", [
        ("t", "{nome}, obrigado pela estadia. Se puder, deixe uma avaliação contando como foi a sua experiência; ela nos ajuda a melhorar."),
        ("o", " Link: {avaliar}"),
        ("t", " Esperamos receber você de novo. {anfit}, {hosp}.")]),
    ("M09", "Resposta: chegada fora do horário", "Quando o hóspede avisar que vai chegar fora do horário", "resposta", [
        ("t", "Obrigado por avisar, {nome}. Nosso check-in é a partir das {cin}"),
        ("o", " e a chegada combinada é até as {climite}"),
        ("t", ". Vamos verificar como receber você nesse horário e respondemos em seguida. {anfit}, {hosp}.")]),
    ("M10", "Resposta: problema durante a estadia", "Assim que o hóspede relatar um problema", "resposta", [
        ("t", "{nome}, obrigado por nos avisar. Já estamos verificando e retornamos em seguida com uma solução ou com o próximo passo. "
              "Se for urgente, fale com a gente pelo número {suporte}. {anfit}, {hosp}.")]),
]

def rotulo(k): return next(c[1] for c in CAMPOS if c[0] == k)
def obrig(k): return next(c[3] for c in CAMPOS if c[0] == k)
