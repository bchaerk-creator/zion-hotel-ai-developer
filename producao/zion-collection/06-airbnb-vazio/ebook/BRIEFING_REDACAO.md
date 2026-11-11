# Briefing de redação · E-book 06 · "Seu Airbnb Está Vazio? O Problema Pode Estar na Sua Oferta"

Produto da Zion Collection (Zion Hotel Group International), R$ 47. Guia prático de 60 páginas A4.
Você escreve o CONTEÚDO de capítulos em JSON. A diagramação é feita depois por script; não escreva HTML.

## Público
Donos e gestores de Airbnb, casas, apartamentos, chalés, pousadas pequenas e glampings, quase sempre iniciantes,
que olham o calendário com muitas datas livres e não sabem por onde começar. Leem no celular ou impresso.

## Regras inegociáveis
- Português brasileiro simples, voz "nós" (a Zion fala com o leitor: "você"). Frases curtas, contrastes diretos. Nada de jargão sem explicar.
- **Sem invenção:** nenhum número de mercado, estatística, estudo, depoimento, caso real de cliente, "pesquisa mostra". Toda conta ou exemplo numérico é marcado "(dados fictícios)" no título do exemplo.
- **Sem promessa** de reservas, ocupação, renda, lucro ou valorização. Use "aprenda o passo a passo para...", "aumentar a clareza", "tomar a decisão com evidência". O resultado depende do contexto e da execução.
- Não citar números da Zion Bubble (diária, EBITDA etc.). Pode dizer que o método "parte da rotina usada nas unidades da Zion" no máximo uma vez por capítulo e só quando fizer sentido.
- Não falar mal do Airbnb nem de concorrentes; não ensinar a burlar regras da plataforma; não inventar regras do algoritmo. Quando falar de plataforma, diga "confira a regra atual na central de ajuda da plataforma".
- Exemplos servem para Airbnb, casa, apartamento, pousada e glamping (varie; não só cabana).
- Nunca repetir o mesmo parágrafo genérico entre páginas. Cada página precisa ensinar algo novo e concreto.

## Método e lentes
- **ECROI** (só na abertura e no fechamento do capítulo, sem nomear a sigla no texto): Espelhamento (a situação concreta e a emoção do leitor) → Colapso de crença (a crença errada vs. a realidade) → Reenquadramento → Orientação (o caminho) → Implementação (o que fazer hoje).
- **Foco 20% · 4% · 0,8%** (lente de priorização da Zion, OP3LIF): de tudo que dá para melhorar, escolha os ~20% que mais pesam na decisão do hóspede; desses, a ação da semana (4%); dessa, o primeiro passo que cabe em menos de 1 hora hoje (0,8%). É uma heurística de foco, não uma promessa estatística. Use nos capítulos 8, 9 e 10 (e pode citar de leve nos outros).
- **As sete dimensões do Diagnóstico Zion de Oferta** (grafia exata): Fotos e apresentação; Título e descrição; Preço e posicionamento; Diferenciais e experiência; Avaliações e confiança; Atendimento e comunicação; Conforto e infraestrutura.
- **Ferramenta "Diagnóstico Zion de Oferta"** (incluída no produto): o leitor dá nota de 0 a 5 a cada dimensão, sempre com uma evidência (0 ausente, 1 muito fraco, 2 fraco, 3 parcial, 4 bom, 5 consistente e comprovado). Pontuação geral = soma das notas ÷ 35 × 100 (0 a 100), indicador orientativo, não previsão de faturamento. Faixas: 0–49 "lacunas relevantes"; 50–69 "ajustes prioritários"; 70–84 "boa base com pontos de melhoria"; 85–100 "oferta consistente: mantenha e acompanhe". A ferramenta mostra as 3 menores notas como prioridades (empate: vale a ordem das dimensões acima) e monta o plano com ação, responsável, prazo, custo estimado, indicador e status. Exporta PDF e CSV.
- Indicadores que podem ser usados (com definição): ocupação = noites vendidas ÷ noites disponíveis (bloqueadas não entram); diária média = receita de hospedagem ÷ noites vendidas; receita por noite disponível = receita ÷ noites disponíveis; taxa de consulta = consultas ÷ visualizações do anúncio; taxa de reserva = reservas ÷ consultas; tempo de primeira resposta. Diga que os nomes e onde achar os dados variam por plataforma.

## Formato de saída (JSON, UTF-8, um arquivo por capítulo: capNN.json)
{
  "num": 1,
  "titulo": "O problema não é só a ocupação",
  "deck": "frase curta em itálico, a ideia central (máx. 18 palavras)",
  "abertura": "ESPELHAMENTO + COLAPSO de crença em 2 parágrafos curtos (total 90 a 130 palavras), separados por \n\n",
  "aprender": ["3 a 4 itens 'Neste capítulo você vai...' (máx. 12 palavras cada)"],
  "paginas": [ 3 páginas de conteúdo, cada uma:
    { "titulo": "título da página",
      "blocos": [ ... 380 a 460 palavras no total por página ... ] }
  ],
  "exercicio": {
    "titulo": "Exercício: ...",
    "instrucao": "o que fazer, em 2 a 4 frases",
    "campos": [ {"rotulo": "pergunta para o leitor responder", "linhas": 2 a 4} ... 4 a 6 campos ],
    "checklist": ["4 a 6 itens verificáveis 'Pronto quando...'"],
    "fechamento": "ORIENTAÇÃO + IMPLEMENTAÇÃO: 2 a 3 frases que levam ao próximo capítulo e à ação de hoje"
  }
}
Tipos de bloco permitidos em "blocos":
- {"t":"p","txt":"parágrafo (40 a 110 palavras)"}
- {"t":"h","txt":"subtítulo curto"}
- {"t":"lista","itens":["..."]}  (3 a 6 itens)
- {"t":"passos","itens":["..."]}  (passo a passo numerado, 3 a 6)
- {"t":"caixa","titulo":"...","itens":["..."]}  (checklist ou regra prática; máx. 1 por página)
- {"t":"exemplo","titulo":"Exemplo (dados fictícios): ...","txt":"..."}  (máx. 1 por página)
- {"t":"quote","txt":"frase de efeito curta, máx. 20 palavras"} (máx. 1 por página)
- {"t":"tabela","cab":["col1","col2",...],"linhas":[["..",".."],...]} (máx. 4 colunas, 5 linhas)
- {"t":"diagrama","id":"<id da lista abaixo>"} (opcional, conta como ~120 palavras de espaço)
- {"t":"erro","txt":"Erro comum: ... → O que fazer: ..."}

Diagramas disponíveis (o script desenha; use só os do seu capítulo, no máximo 1 por página):
- "ocupacao" (cap 1): calendário de 30 noites separando vendidas, livres e bloqueadas
- "jornada" (cap 2): busca → resultados → anúncio → consulta → reserva, com a pergunta do hóspede em cada etapa
- "atributo-beneficio" (cap 3): atributo → benefício → prova
- "primeira-foto" (cap 4): ordem sugerida das 10 primeiras fotos
- "preco-piso" (cap 5): custo variável por estadia + parte do custo fixo + margem = piso da diária
- "confianca" (cap 6): pilares da confiança (avaliações, transparência, informação, resposta)
- "funil" (cap 7): visualizações → consultas → reservas, com as duas taxas
- "radar" (cap 8): gráfico de radar das sete dimensões
- "gravidade-facilidade" (cap 8): matriz 2×2 gravidade × facilidade
- "foco" (cap 8 ou 9): 20% → 4% → 0,8%
- "semanas" (cap 9): linha do tempo das 4 semanas
- "ciclo" (cap 10): medir → decidir → executar → revisar

Grave os arquivos com a ferramenta Write em:
/home/user/zion-hotel-ai-developer/producao/zion-collection/06-airbnb-vazio/ebook/conteudo/capNN.json (NN com dois dígitos).
Depois valide com: python3 -I -c "import json,sys;[json.load(open(f)) for f in sys.argv[1:]]" <arquivos> e conte as palavras de cada página (alvo 380–460).
Responda só com: arquivos gravados, palavras por página e qualquer dúvida de conteúdo.

## Esqueleto dos 10 capítulos (subtemas que devem aparecer)
1. O problema não é só a ocupação — calendário vazio é sintoma; separar impressão de evidência; como calcular a ocupação (bloqueadas fora); o que a diária média esconde; definir meta realista e mensurável. Exercício: fotografia do negócio (últimos 90 dias).
2. Por que o hóspede não escolhe você — a jornada de comparação; escolher três concorrentes relevantes (mesma região, capacidade, padrão, datas); diferenciais que o hóspede percebe; localização: vantagem ou objeção; quando o preço vira desculpa. Exercício: matriz competitiva.
3. Sua hospedagem é um produto — definir o hóspede prioritário; transformar atributos em benefícios (com prova); a promessa de experiência; posicionamento em uma frase; o que eliminar da oferta. Exercício: proposta de valor.
4. O anúncio que desperta desejo — a primeira foto precisa explicar a oferta; sequência visual que responde dúvidas; título: clareza antes de adjetivos; descrição: benefícios e fatos; comodidades e regras sem surpresas. Exercício: auditoria do anúncio.
5. A diária certa para a oferta certa — preço não é palpite; custos variáveis e fixos; margem mínima e piso da diária; fins de semana e sazonalidade; descontos que não destroem margem. Exercício: cenário de tarifas (dados do leitor).
6. Como aumentar a confiança — avaliações: padrões e oportunidades; respostas públicas a críticas; transparência sobre limitações; informações que reduzem insegurança; velocidade e consistência no atendimento. Exercício: mapa de confiança.
7. Transforme visualizações em reservas — medir visitas e conversão; responder objeções antes da pergunta; mensagem que vende sem pressionar; facilitar a decisão; recuperar oportunidades com respeito. Exercício: roteiro comercial.
8. O Diagnóstico Zion — as sete dimensões; como pontuar com evidências (escala 0–5); separar gravidade de facilidade; identificar três prioridades (foco 20/4/0,8); construir hipóteses testáveis ("se ... então ... medido por ... até ..."). Exercício: preencher o diagnóstico (tabela das 7 dimensões com nota e evidência).
9. Plano de ação de 30 dias — semana 1 diagnóstico e fotos; semana 2 texto e posicionamento; semana 3 preço e confiança; semana 4 medição e ajustes; o que registrar diariamente (5 minutos). Exercício: cronograma de execução. (Pode mencionar que existe um "Calendário comercial de 30 dias" opcional vendido à parte, mas o capítulo precisa funcionar sozinho, sem ele.)
10. Seu novo posicionamento — comparar antes e depois (mesma base de datas); indicadores que importam; quando uma mudança não funciona (o que fazer); ciclo de melhoria contínua; próximos 90 dias. Exercício: compromisso de implementação.
