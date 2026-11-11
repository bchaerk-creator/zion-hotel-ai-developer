"""Calendário comercial de 30 dias (order bump do Produto 06). Uma ação por dia, de 15 a 60 minutos.
Complementa o capítulo 9 do e-book (que funciona sozinho): aqui cada dia já vem escrito.
(dia, dimensão, ação, minutos, o que observar)"""
SEMANAS = {1: "Diagnóstico e fotos", 2: "Texto e posicionamento", 3: "Preço e confiança", 4: "Medição e ajustes", 5: "Fechamento do ciclo"}
ACOES = [
    (1, "Todas", "Preencha o Diagnóstico Zion de Oferta com evidência para cada nota. Anote a pontuação e as 3 prioridades.", 40, "Pontuação inicial e prioridades"),
    (2, "Todas", "Tire a 'foto' dos últimos 30 dias: noites disponíveis, vendidas, visualizações, consultas e reservas. É a sua linha de base.", 30, "Ocupação, taxa de consulta e taxa de reserva"),
    (3, "Fotos e apresentação", "Abra o anúncio no celular como se fosse hóspede. Anote as 3 dúvidas que as fotos não respondem.", 20, "Lista de dúvidas sem resposta visual"),
    (4, "Fotos e apresentação", "Arrume e limpe os ambientes para foto: tire objetos pessoais, abra cortinas, acenda luzes quentes.", 60, "Ambientes prontos"),
    (5, "Fotos e apresentação", "Fotografe na melhor luz do dia, na horizontal, na altura do peito. Faça a foto do diferencial com calma.", 60, "Fotos novas por ambiente"),
    (6, "Fotos e apresentação", "Escolha a nova primeira foto: a que explica a oferta. Reorganize as 10 primeiras na ordem das dúvidas.", 30, "Data da troca anotada"),
    (7, "Fotos e apresentação", "Escreva legendas curtas e verdadeiras nas fotos principais. Revisão da semana: o que mudou e quando.", 30, "Registro das mudanças da semana"),
    (8, "Título e descrição", "Escreva em uma frase para quem é a sua hospedagem e qual problema da viagem ela resolve.", 20, "Frase de posicionamento"),
    (9, "Título e descrição", "Liste 3 diferenciais e transforme cada um em benefício com prova (foto, detalhe, regra).", 30, "3 pares benefício + prova"),
    (10, "Título e descrição", "Escreva 3 opções de título com público + diferencial + lugar. Escolha a mais clara, não a mais bonita.", 30, "Título novo publicado e data"),
    (11, "Título e descrição", "Reescreva o primeiro parágrafo da descrição com os 3 fatos que o hóspede mais procura.", 40, "Primeiro parágrafo novo"),
    (12, "Título e descrição", "Revise comodidades: marque só o que existe e funciona. Explique o que pode surpreender (escada, acesso, barulho).", 30, "Comodidades conferidas"),
    (13, "Atendimento e comunicação", "Junte as 5 perguntas que mais chegam no chat e escreva a resposta-padrão de cada uma.", 40, "5 respostas-padrão salvas"),
    (14, "Diferenciais e experiência", "Revisão da semana: compare consultas por visualização com a linha de base, sem concluir antes do tempo.", 20, "Taxa de consulta da semana"),
    (15, "Preço e posicionamento", "Some seus custos variáveis por estadia (limpeza, lavanderia, amenidades) e os fixos do mês.", 40, "Custo variável e fixo"),
    (16, "Preço e posicionamento", "Calcule o piso da diária: (variável por noite + fixo por noite + margem) ÷ (1 − taxas e impostos).", 30, "Piso da diária"),
    (17, "Preço e posicionamento", "Compare com 3 anúncios realmente parecidos (região, capacidade, padrão) nas mesmas datas.", 40, "Tabela dos 3 concorrentes"),
    (18, "Preço e posicionamento", "Defina tarifas por tipo de dia (semana, fim de semana, feriado), sempre acima do piso. Confira as regras da plataforma.", 30, "Tarifas por tipo de dia"),
    (19, "Avaliações e confiança", "Leia as últimas avaliações e marque o que se repete, bom e ruim. Escolha 1 causa para corrigir.", 30, "Padrão de crítica escolhido"),
    (20, "Avaliações e confiança", "Responda com respeito às críticas sem resposta: agradeça, explique o que mudou, sem discutir.", 30, "Respostas publicadas"),
    (21, "Conforto e infraestrutura", "Faça a vistoria como hóspede: cama, banho, internet, tomadas, cheiro, ruído. Corrija o que aparece em reclamação.", 60, "Itens corrigidos"),
    (22, "Atendimento e comunicação", "Meça o tempo de primeira resposta da semana. Defina o seu prazo máximo e quem cobre quando você não pode.", 20, "Tempo de primeira resposta"),
    (23, "Atendimento e comunicação", "Escreva a mensagem de pré-chegada com acesso, horário, como chegar e contato, sem jargão.", 30, "Mensagem de pré-chegada"),
    (24, "Diferenciais e experiência", "Escolha um pequeno detalhe de boas-vindas coerente com o seu hóspede prioritário e o custo dele.", 30, "Detalhe escolhido e custo"),
    (25, "Todas", "Compare as 3 semanas com a linha de base: visualizações, consultas, reservas. Mesma base de datas.", 30, "Comparação antes × depois"),
    (26, "Todas", "Escolha 1 mudança que não mostrou efeito e decida: manter mais tempo, ajustar ou desfazer.", 20, "Decisão registrada"),
    (27, "Título e descrição", "Atualize título ou primeira foto só se os números pedirem. Uma mudança por vez, com data.", 30, "Mudança e data"),
    (28, "Todas", "Revisão da semana: o que funcionou, o que não funcionou, o que você não conseguiu fazer.", 20, "3 respostas escritas"),
    (29, "Todas", "Refaça o Diagnóstico Zion de Oferta com a mesma régua de evidências. Compare com o dia 1.", 40, "Pontuação nova × inicial"),
    (30, "Todas", "Escolha as prioridades do próximo ciclo de 30 dias e marque na agenda o próximo dia 1.", 20, "Próximo ciclo marcado"),
]
assert [a[0] for a in ACOES] == list(range(1, 31))
def semana(dia): return min((dia - 1) // 7 + 1, 5)
