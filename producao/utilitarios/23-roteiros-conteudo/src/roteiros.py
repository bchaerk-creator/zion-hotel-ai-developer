"""Fonte única dos campos e dos roteiros da Ferramenta 23 (Kit de Roteiros de Conteúdo e Vídeos).
Mesma mecânica das Ferramentas 11 e 30. Segmentos:
  ("t", texto)            sempre entra; {campo} obrigatório vira [PREENCHA: rótulo] se estiver vazio
  ("o", texto)            opcional: só entra se TODOS os campos do texto estiverem preenchidos
  ("v", campo, texto)     só entra se o campo estiver VAZIO
"\n" dentro do texto vira quebra de linha na célula.
"""
# (chave, rótulo, seção, obrigatório, ajuda, exemplo fictício). H = a hospedagem (uma vez); C = calendário.
CAMPOS = [
    ("nome", "Nome da hospedagem", "H", True, "Como aparece no anúncio e no perfil.", "Refúgio do Vale (fictício)"),
    ("tipo", "Tipo de hospedagem", "H", True, "Chalé, apartamento, casa, pousada, glamping...", "chalé"),
    ("lugar", "Cidade ou região", "H", True, "Onde fica.", "Vale Exemplo (SC)"),
    ("hospede", "Para quem é", "H", True, "Complete: \"ideal para ...\".", "casais que querem descansar longe da cidade"),
    ("dif1", "Diferencial principal", "H", True, "O que o hóspede mais comenta.", "banheira com vista para o vale"),
    ("dif2", "Segundo diferencial", "H", False, "Opcional.", "lareira na sala"),
    ("manha", "Como é a manhã aí", "H", True, "Uma cena real, em poucas palavras.", "café na varanda com a neblina subindo"),
    ("perto", "O que fazer por perto", "H", False, "Opcional. Lista curta.", "duas cachoeiras e uma vinícola a 15 minutos"),
    ("pergunta", "Pergunta que mais chega", "H", True, "Como o hóspede escreve.", "Precisa de carro 4x4 para chegar?"),
    ("resposta", "Resposta para essa pergunta", "H", True, "Frase completa, verdadeira.", "Não. O acesso é por estrada de terra firme e qualquer carro chega."),
    ("cuidado", "Um cuidado que pouca gente vê", "H", True, "Algo que você faz em toda estadia.", "trocamos e passamos toda a roupa de cama antes de cada chegada"),
    ("nao", "Para quem não é", "H", True, "Seja honesto: ajuda a atrair o hóspede certo.", "quem procura agito e vida noturna"),
    ("reserva", "Como reservar", "H", True, "Onde a pessoa reserva.", "pelo link no perfil"),
    ("inicio", "Data do primeiro vídeo", "C", True, "Data.", "2026-12-01"),
    ("intervalo", "Dias entre um vídeo e outro", "C", True, "Número. Ex.: 3 = um vídeo a cada 3 dias.", 3),
]
DATAS = {"inicio"}

# (id, formato, objetivo, regra de data, segmentos). Regra "post-N" = início + (N−1) × intervalo.
MENSAGENS = [
    ("V01", "Tour de 15 segundos", "Mostrar o lugar inteiro de uma vez", "post-1", [
        ("t", "GANCHO (0 a 3 s): \"15 segundos por dentro: {nome}\"\nCENAS: 1) chegada pela porta; 2) giro lento pela sala; 3) quarto; 4) {dif1}; 5) vista de fora.\nTEXTO NA TELA: {tipo} em {lugar}, ideal para {hospede}.\nLEGENDA: {nome}: {tipo} em {lugar}, feito para {hospede}. Do que você mais gostou?\nCHAMADA: Reserve {reserva}.")]),
    ("V02", "Diferencial em destaque", "Fazer o hóspede querer viver o diferencial", "post-2", [
        ("t", "GANCHO (0 a 3 s): \"Imagine terminar o dia assim.\"\nCENAS: 1) detalhe: {dif1}; 2) mão ou pés interagindo, sem mostrar rosto de hóspede; 3) plano aberto do lugar."),
        ("o", "\nCENA EXTRA: {dif2}."),
        ("t", "\nTEXTO NA TELA: {dif1}.\nLEGENDA: Em {nome}, o momento preferido de quem vem: {dif1}. Salve para a próxima viagem.\nCHAMADA: Reserve {reserva}.")]),
    ("V03", "Uma manhã aqui", "Vender a sensação, não só o quarto", "post-3", [
        ("t", "GANCHO (0 a 3 s): \"Como é acordar aqui: {nome}.\"\nCENAS: 1) cortina abrindo; 2) {manha}; 3) xícara ou detalhe da mesa; 4) plano aberto.\nTEXTO NA TELA: Uma manhã em {lugar}.\nLEGENDA: Aqui a manhã é assim: {manha}. Marque quem você traria.\nCHAMADA: Reserve {reserva}.")]),
    ("V04", "Pergunta que mais chega", "Tirar a dúvida que trava a reserva", "post-4", [
        ("t", "GANCHO (0 a 3 s): \"A pergunta que mais recebemos:\"\nCENAS: 1) texto da pergunta na tela; 2) imagem que mostra a resposta; 3) o lugar.\nTEXTO NA TELA: {pergunta}\nLEGENDA: {pergunta} {resposta} Ficou alguma dúvida? Pergunte nos comentários.\nCHAMADA: Reserve {reserva}.")]),
    ("V05", "Bastidores", "Mostrar o cuidado que gera confiança", "post-5", [
        ("t", "GANCHO (0 a 3 s): \"O que acontece antes de você chegar.\"\nCENAS: 1) mãos preparando o ambiente; 2) detalhe do cuidado; 3) o lugar pronto.\nTEXTO NA TELA: Antes de cada chegada.\nLEGENDA: Em {nome}, {cuidado}. É o que ninguém vê e todo mundo sente.\nCHAMADA: Reserve {reserva}.")]),
    ("V06", "Para quem é (e para quem não é)", "Atrair o hóspede certo", "post-6", [
        ("t", "GANCHO (0 a 3 s): \"Este lugar não é para todo mundo.\"\nCENAS: 1) plano aberto; 2) detalhe: {dif1}; 3) momento de calma.\nTEXTO NA TELA: É para {hospede}. Não é para {nao}.\nLEGENDA: {nome} é para {hospede}. Não é para {nao}, e tudo bem: queremos que você encontre o lugar certo.\nCHAMADA: Reserve {reserva}.")]),
    ("V07", "O que fazer por perto", "Dar motivo para a viagem", "post-7", [
        ("o", "GANCHO (0 a 3 s): \"Hospedado em {nome}, você fica perto de:\"\nCENAS: 1) o lugar; 2) os passeios: {perto}; 3) a volta para casa no fim do dia.\nTEXTO NA TELA: Perto de {nome}: {perto}.\nLEGENDA: De {nome} você chega a {perto}. Qual você faria primeiro?"),
        ("v", "perto", "GANCHO (0 a 3 s): \"Às vezes o melhor passeio é não sair.\"\nCENAS: 1) o lugar ao fim da tarde; 2) um momento de descanso; 3) a noite chegando.\nTEXTO NA TELA: Um fim de semana sem pressa.\nLEGENDA: Aqui dá para não fazer nada, e esse é o plano."),
        ("t", "\nCHAMADA: Reserve {reserva}.")]),
    ("V08", "Como reservar", "Facilitar o caminho até a reserva", "post-8", [
        ("t", "GANCHO (0 a 3 s): \"Quer passar uns dias em {nome}? É assim:\"\nCENAS: 1) o lugar; 2) tela mostrando onde reservar; 3) {dif1}.\nTEXTO NA TELA: Reserve {reserva}.\nLEGENDA: Para reservar {nome}, em {lugar}: {reserva}. Dúvidas? Responda aqui.\nCHAMADA: Reserve {reserva}.")]),
]

def rotulo(k): return next(c[1] for c in CAMPOS if c[0] == k)
def obrig(k): return next(c[3] for c in CAMPOS if c[0] == k)
