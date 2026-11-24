# Prompt para o Claude Code · Aula 1 · Marco Zero em 7 vídeos de até 7:00

Este arquivo é seguido pelo Claude Code a partir do COMECE-AQUI.md, na raiz do kit. Para rodar só esta aula, abra o Claude Code nesta pasta e cole tudo a partir da linha "INÍCIO DO PROMPT".

## Antes de colar
1. **O PDF da aula** já está nesta pasta: `slides.pdf`, 51 páginas.
2. **(Opcional) A sua voz clonada no ElevenLabs** ou **o seu avatar no HeyGen.** Crie a variável `ELEVENLABS_API_KEY` ou `HEYGEN_API_KEY` no terminal. A chave nunca vai no prompt nem numa conversa.
3. **O e-book** também está nesta pasta (`ebook.pdf`), quando a aula tem e-book. Ele não entra nos vídeos: vai como material da aula no ClickMax.

Observação: o Claude Code precisa de Node 18 ou mais novo.

---

INÍCIO DO PROMPT

Você vai montar 7 vídeos curtos e narrados, em português do Brasil, a partir dos slides de uma aula. Trabalhe só nesta pasta. Não publique nada na internet, não envie arquivos para lugar nenhum e não apague arquivos que você não criou.

## O que existe na pasta
- `slides.pdf`: 51 páginas, uma por slide, em 16:9.
- Talvez a variável de ambiente `ELEVENLABS_API_KEY` ou `HEYGEN_API_KEY`.

## Regra principal: nenhum vídeo passa de 7 minutos
Os vídeos foram divididos para ficar abaixo de 7:00. Se algum passar depois de montado, não corte o texto nem acelere a voz: pare e me diga qual vídeo e quanto passou.

## O que você vai entregar
1. `saida/videos/V01-....mp4` a `V07-....mp4`: um arquivo por vídeo, com número e título no nome. 1920×1080, 30 fps, H.264, áudio AAC 48 kHz.
2. `saida/verticais/`: a mesma série em 1080×1920, com o slide centralizado e fundo verde-escuro #16261C, para Reels e Stories.
3. `saida/legendas/V01.srt` em diante: legenda em português com o texto exato da narração.
4. `saida/relatorio.txt`: a duração de cada slide e de cada vídeo, e qualquer problema encontrado.

## Passo a passo
1. **Ferramentas.** Verifique se existem `ffmpeg`, `ffprobe` e `pdftoppm` (poppler). Se faltar algum, me diga o comando para instalar no meu sistema e espere eu confirmar.
2. **Imagens.** Converta o PDF em PNG, uma imagem por página, em 1920×1080: `pdftoppm -png -r 150 -scale-to-x 1920 -scale-to-y 1080 slides.pdf slides/p`. Confira que saíram 51 imagens. Se não saíram, pare e me avise.
3. **Narração.** Use o ROTEIRO abaixo. Cada item é uma página do PDF. Grave um áudio por página em `audio/NN.mp3`.
   - **Opção A, a minha voz (ElevenLabs).** Se a chave existir, me pergunte o ID da voz e use o modelo multilíngue, com estabilidade em torno de 0,5 e similaridade em torno de 0,8. Gere primeiro a página 01 e me mostre antes de gerar o resto.
   - **Opção B, voz gratuita.** Sem chave, instale o `edge-tts` (peça antes) e use a voz `pt-BR-AntonioNeural`, com velocidade `-5%`.
   - **Opção C, o meu avatar (HeyGen).** Se a chave existir, me pergunte o ID do avatar e o da voz. Gere um vídeo do avatar por página, com fundo verde ou transparente, em 1080×1080. Teste a página 01 e me mostre antes. Na montagem, o avatar entra num círculo de 360 px no canto inferior direito, a 64 px das bordas. Nas aberturas de bloco e nas páginas marcadas com [FOTO], fica só a voz.
   - Não altere o texto. Não leia em voz alta números de página nem marcações entre colchetes.
4. **Montagem por página.** Cada página vira um clipe com a imagem parada e o áudio: duração = áudio + 0,8 s; nas páginas [PAUSA], segure mais 5 segundos em silêncio com o texto "pause e anote" no canto inferior esquerdo (sans-serif, cor #E0BE5E); zoom lento de 100% a 104% só nas páginas [FOTO]; fade de 0,4 s entre páginas.
5. **Cada vídeo.** Junte as páginas de cada vídeo, na ordem. No primeiro segundo, mostre no canto superior esquerdo o selo "Aula 1 · Marco Zero · N de 7" (sans-serif, 28 px, cor #E0BE5E, fundo #16261C com 80% de opacidade), saindo com fade aos 4 segundos. Nos últimos 2 segundos de cada vídeo, exceto o último, escreva no centro inferior "Próximo vídeo: [título do próximo]".
6. **Áudio.** Normalize a fala de cada vídeo para -16 LUFS integrado, com pico máximo de -1,5 dB. Sem música.
7. **Versão vertical.** 1080×1920, fundo #16261C, o vídeo horizontal com 1080 de largura no centro e a legenda queimada abaixo, em branco, até 2 linhas.
8. **Legenda.** Um `.srt` por vídeo, com os tempos reais, linhas de até 42 caracteres e no máximo 2 linhas.
9. **Conferência.** Antes de dizer que terminou: confirme com `ffprobe` resolução, fps e duração de cada arquivo, e que nenhum passa de 7:00. Extraia 3 quadros do começo de cada vídeo e me mostre. Escreva tudo no `relatorio.txt`.

## Regras do texto (já aplicadas no roteiro, não mude)
- Voz do Bruno Chaerk, primeira pessoa, conversa direta, sem jargão.
- Nenhuma promessa de renda, retorno, ocupação, crédito ou sociedade. A Zion "avalia".
- A Marina e os números marcados como ilustrativos são ditos como exemplo.

## ROTEIRO

### Vídeo 1 de 7 · Abertura (cerca de 6:31)

**Página 01 · capa** [FOTO]
Olá, aqui é o Bruno Chaerk, e esta é a Marco Zero da Trilha 1: transforme seu terreno em um destino turístico e um projeto de hospedagem de sucesso. Hoje eu vou te mostrar a visão macro de como a gente desenvolve um negócio de hospedagem, e você vai fazer comigo um diagnóstico prévio do seu terreno. Não é para só assistir: pega papel e caneta.

**Página 02 · proposito** 
Antes de começar, o propósito desta mentoria: conhecimento para abençoar, e para ser abençoado. Que cada pessoa prospere com o que já tem nas mãos, e use isso para abençoar outras.

**Página 03 · visaotempo** 
Antes de começarmos, quero trazer uma reflexão. Se você está aqui hoje, é porque existe uma visão dentro de você: transformar um terreno em um negócio, construir suas primeiras cabanas, desenvolver uma pousada. Um princípio que eu aprendi na Teologia do Empreendedorismo: em Eclesiastes 8, o coração do sábio conhece o tempo e o modo. Não basta ter uma boa ideia. São três perguntas. Visão: você sabe exatamente o que quer construir? Tempo: existe mercado, demanda e uma necessidade real para o que você quer oferecer? Modo: você tem conhecimento, estratégia e preparação para executar do jeito certo? Talvez o que esteja faltando entre o seu sonho e a realização não seja dinheiro nem oportunidade. Seja conhecimento para tomar as decisões certas. Ter uma visão é importante. Saber quando e como realizá-la é o que transforma um sonho em um projeto concreto. Das três, qual é a que mais falta para você hoje: visão, tempo ou modo?

**Página 04 · bloco-1** 
Bloco um. Abertura: quem está aqui, o setor e a promessa desta aula. Hoje você vai sair daqui com cinco respostas anotadas. É o diagnóstico prévio do seu projeto. E antes de falar de mim, quero falar de você.

**Página 05 · visao** [FOTO]
O fio desta aula: o que está parado não é a terra. É a visão. A terra não reclama de esperar. Quem fica parada é a visão: a ideia que você tem há anos para o seu terreno, sem plano, sem número, sem data. Eu vejo muita gente que fala do terreno com brilho no olho e não sabe dizer quanto custa a primeira cabana. Esta aula é sobre tirar a visão do lugar.

**Página 06 · preco** [FOTO]
Se você chegou até aqui, é porque o setor de hospedagem te interessa. Ou você tem um terreno, ou já está operando, ou está pesquisando para entrar no mercado. Alguns vieram saber o preço da Bubble ou de outra estrutura modular, e está tudo certo: é uma porta de entrada, não a única. Quem decide pelo produto antes de olhar o terreno e o mercado costuma gastar duas vezes. O produto é só um dos requisitos. O preço da estrutura é a última pergunta, não a primeira.

**Página 07 · setor** 
Muita gente conhece a Zion pela bolha, e ela é a nossa protagonista. Mas o setor de hospedagem é muito maior: domos, tendas, cabanas e chalés, casa de temporada, pousada boutique, hotel, resort, multipropriedade. Glamping não é regra, é uma opção. O método vale para todos. O produto certo é o que o seu mercado pede e o seu terreno permite. Qual desses você imagina no seu terreno?

**Página 08 · perfis** [PAUSA]
Qual é a sua situação? São seis. A: tenho a terra e o capital. B: tenho a terra, não o capital, e procuro sócio. C: já opero e quero crescer. D: tenho uma visão, ou uma casa de sítio. E: estou pesquisando para entrar no setor, olhando a Bubble, outra estrutura modular ou outro modelo. F: sou corretor. O B e o E são os que mais aparecem, e os dois precisam da mesma coisa: um plano antes do produto. Esta aula serve para os seis. Anote a sua letra, eu vou voltar nela.

**Página 09 · diag360** [PAUSA]
Antes de qualquer conta, a porta de entrada da escola: o Diagnóstico 360 graus do Empreendedor Hoteleiro. O primeiro ensinamento é conheça a si mesmo. Cinco perguntas, uma linha cada, sem pensar demais: o seu principal objetivo com a hospedagem; o problema do mercado que você atende; os recursos que você tem e os seus limites; a competência que você precisa desenvolver; e a primeira decisão concreta. Pare o vídeo: dois a três minutos, no papel. Não tem resposta certa. Tem a sua. A quinta resposta, a primeira decisão, você completa lá no fim.

**Página 10 · promessa** 
A promessa desta aula: você sai sabendo o que um investidor perguntaria sobre o seu terreno, e o que falta para você responder. É para você se tem uma terra, uma operação ou uma visão, se quer decidir com número e não com palpite, e se topa fazer a lição de casa. Não é para você se acha que basta ter a terra, se acha que basta ter o dinheiro, ou se quer ficar rico rápido. Só ter a terra não é a solução. Só ter o dinheiro também não. É ter o dinheiro ligado ao conhecimento e ao profissional certo. No final, eu abro as vagas da Turma Fundadores. Fica até o fim.

### Vídeo 2 de 7 · Provas (cerca de 2:23)

**Página 11 · bloco-2** 
Bloco dois. Quem fala. Agora você sabe quem está aqui. Deixa eu te contar de onde vem o que eu vou ensinar. O que a gente ensina, a gente opera. E também o que a gente errou.

**Página 12 · quem** [FOTO]
Uma apresentação curta. Eu sou o Bruno Chaerk: mais de vinte anos em hotelaria na Europa, e fundador da Zion Hotel Group International. A linha é Barcelona, Mallorca, Canárias, e o Brasil a partir de 2020: Urubici em 2020 e Florianópolis em 2024. Hoje também estou nas mesas onde se decide investimento em hotelaria: embaixador do Clube de Negócios Hotéis e Resorts, palestras, CNN e o Hotel Cast. O que a gente ensina, a gente opera. E é dessas mesas que eu trago o que o investidor pergunta.

**Página 13 · resorts** [FOTO]
Onde eu aprendi o que hoje eu ensino. O Rooftop Nine em Magaluf, a FlowRider do INNSiDE Wave, o Meliá Sitges, Jandía em Fuerteventura, e uma entrevista para a imprensa espanhola. As grandes redes estruturam tudo antes de construir. Eu vi de perto como os grandes fazem. Hoje eu trago isso para o tamanho do seu terreno.

**Página 14 · bolha** [FOTO]
A Zion trouxe as suítes bolha para o Brasil: Urubici em 2020, Florianópolis em 2024. Do terreno ao deck, da obra ao hóspede. O hóspede não paga por paredes, paga pelo momento: a banheira com vista. E as notas são o hóspede falando por nós: nove vírgula oito no Booking, quatro vírgula sete no Google, e cinco de cinco, Superhost no Airbnb. A gente não fala de teoria. Fala do que construiu, errou, corrigiu e opera hoje.

**Página 15 · errocaro** [FOTO]
A Zion também errou. Já operamos pousadas e hotéis tradicionais e construímos chalés: muita infraestrutura, pouco retorno. Com o glamping, gastamos menos, operamos mais e hospedamos mais. Errar não é perder. É ganhar conhecimento, só que custa caro. Aqui você aprende com o meu.

### Vídeo 3 de 7 · Colapso (cerca de 6:07)

**Página 16 · bloco-3** 
Bloco três. Os três erros: a pergunta do investidor, e os erros que deixam a visão parada. Agora eu vou fazer uma pergunta desconfortável. Pega a caneta.

**Página 17 · pergunta** [PAUSA]
Se você chegasse hoje na frente de um investidor, saberia dizer qual é o melhor produto para o seu terreno, quanto custa, quanto retorna, quanto de lucro dá e em quanto tempo? Nas mesas de investimento, quem chega com matrícula e sem essas cinco respostas não passa da primeira reunião. Não importa o produto, bolha, chalé ou resort. E se o investidor for você mesmo, quem precisa das cinco respostas primeiro é você. Anote: quantas das cinco você responde hoje, de zero a cinco?

**Página 18 · rendafixa** [PAUSA]
A pergunta que todo investidor faz em silêncio: o seu projeto é tão bom e tão competitivo que vale mais a pena investir nele do que deixar o dinheiro na renda fixa, no banco? E você conhece os parâmetros do mercado para afirmar que é um bom investimento? Diária, ocupação, custo por noite e prazo de retorno da sua região, com dado. Eu vejo gente que compara o projeto com o sonho, nunca com a alternativa segura. Se você não sabe responder isso, o investidor também não vai saber. E se o investidor for você, o seu dinheiro merece a mesma pergunta. Sim, não ou não sei? Anote. Isto é conteúdo educacional, não recomendação de investimento.

**Página 19 · erro1** 
O primeiro erro é achar que o problema é o dinheiro. Ninguém chega de helicóptero com uma mala de dinheiro para pôr na terra de um terceiro. O investidor não procura terra; procura projeto com parâmetro para avaliar. Nas mesas de investimento, tem gente querendo apostar em negócio novo e pouco projeto estruturado chegando. O que chega é matrícula sem plano. Dinheiro é energia. Ele vai para onde tem clareza. Você já ouviu um dia aparece um investidor na sua família?

**Página 20 · paredes** 
O segundo erro é escolher o produto antes do plano. A pergunta: você quer construir para você ou para o seu cliente? Eles vendem paredes. Do balcão para dentro é construir o que é mais fácil para você e entregar a chave. Do balcão para fora é construir o que o hóspede quer e hospedar de verdade. Eu vejo a mesma cabana de duas águas, com banheira e refletor verde, repetida dez vezes na mesma estrada. Quem aluga vende metro quadrado. Quem hospeda vende um momento. E você, hoje aluga ou hospeda?

**Página 21 · erro3** 
O terceiro erro é construir antes de medir a demanda. Dos que eu conheço, de cada dez, oito passaram perrengue com o construtor, porque só pensaram em construir. É observação minha em vinte anos de setor, não é pesquisa. Não sabe orçar: o orçamento é o do construtor. Não sabe quando volta: não existe conta, só esperança. Não sabe quem vem: nunca mediu a demanda. O caminho de sempre é terreno pelo preço, infraestrutura sem saber por onde começar, obra que estoura, anúncio mal feito, calendário vazio. Comprou barato, construiu caro e vai vender a pousada a preço de banana.

**Página 22 · inimigo** 
Não é culpa sua. No Brasil quase não existe a profissão que faz a ponte entre o dono da terra e o investidor. Lá fora ela tem nome: developer. E ela trabalha com método. Eu vejo corretor, arquiteto e construtor, cada um com uma peça, e ninguém montando o quebra-cabeça. Ninguém te mostrou a ordem. É aí que entra o Método Zion.

**Página 23 · calculadora** [PAUSA]
Exercício: o equalizador. Quanto a sua visão parada já custou? Aponte a câmera para o código na tela e suba e desça os controles: anos parada, unidades, diária, ocupação, margem e investimento. Quase todo mundo coloca a ocupação do mês mais cheio. Só fim de semana dá trinta e cinco a quarenta por cento na média do ano. Com feriados e datas festivas, cinquenta a sessenta. Sessenta e cinco a oitenta e cinco, só com procura extraordinária, comprovada pelo mercado. Quatro meses cheios não querem dizer o ano todo cheio. A regra de ouro: ocupação e diária médias do ano, nunca o mês mais cheio. É uma simulação educativa com os seus números, não promessa de renda, retorno ou ocupação. Pare o vídeo e anote quanto a espera já custou.

**Página 24 · implicacao** [PAUSA]
Pense um minuto antes de responder. Se daqui a noventa dias nada mudar, onde você vai estar? A mesma terra. A mesma visão. Mais um trimestre de imposto, de espera e de um dia eu faço. Não é para assustar. É para você olhar o custo real que já está pagando: o tempo, o imposto, a família cobrando.

### Vídeo 4 de 7 · O mecanismo (1 de 2) (cerca de 5:11)

**Página 25 · bloco-4** 
Bloco quatro. A Ordem Zion: o que fazer, em que ordem e por quê. Até aqui foi o problema. Daqui em diante é a solução. Agora eu vou te mostrar a ordem que ninguém te mostrou.

**Página 26 · tese** 
A tese da Zion. Não falta dinheiro. Faltam projetos bem estruturados, com parâmetros para captar esse dinheiro. Nas mesas de investimento que eu frequento, eu vejo mais investidor querendo apostar em negócio novo do que projeto bem estruturado chegando. A questão não é quanto você gasta. É como você gasta.

**Página 27 · nasceu** [FOTO]
Por que o método nasceu. Um terreno vazio em Urubici, na serra. Sem luz, sem água, sem internet. Só mata de araucárias e uma visão. A gente estruturou tudo do zero: energia, água, conectividade. Estudou território, mercado e produto, modelou o investimento, implantou e lançou. Quando a operação virou referência, as perguntas começaram a chegar: como vocês fizeram, por onde eu começo, quanto custou. O método foi escrito ao contrário: primeiro fizemos, depois documentamos. Cada régua aqui dentro já foi uma decisão com dinheiro de verdade.

**Página 28 · escada** 
Antes de te mostrar a ordem, quero te mostrar como cada aula funciona. Imagine uma árvore. Lá no alto está o sonho grande: o resort, as dez cabanas. Embaixo, os frutos que estão ao alcance da mão. Quem colhe os frutos baixos na ordem certa ajuda a pagar a escada até os altos. Primeiro validar, depois monetizar, só então escalar. Monetizar, aqui, é a fase pequena se pagar sozinha antes de crescer. Cada aula da trilha é um degrau, com quatro partes. Princípio: uma frase que muda o seu olhar. Experiência: uma história verdadeira, minha ou da Zion, ou um exemplo que eu digo que é exemplo. Ferramenta: o método em ordem, com a folha para você preencher onde costuma travar. E Ação: toda aula termina com um compromisso de sete dias, com prazo e com a prova de que você fez. A Escada é o jeito de ensinar. O caminho é a Ordem Zion, que eu vou te mostrar agora.

**Página 29 · ordem** 
A Ordem Zion em quatro etapas. Ler o terreno: o que dá para fazer aqui, e para quem. Desenhar o negócio: qual produto, qual modelo, a conta fecha. Estruturar o capital: de onde vem o dinheiro e quem é dono do quê. Lançar: implantar e vender antes de abrir. Embaixo de cada etapa estão os sete pilares do método. No fim da etapa três você tem o plano executivo: o projeto com parâmetros para captar. E a regra: nenhuma etapa avança sem a anterior concluída. Quase todo mundo começa pela etapa quatro, a obra. Ninguém define o produto antes de entender o mercado, e ninguém entende o mercado antes de ler o terreno. É essa ordem que ninguém te mostrou. Lembra do visão, tempo e modo? Visão é a etapa dois, tempo é a etapa um, e modo são as etapas três e quatro. Em qual etapa você começou?

**Página 30 · planoexec** 
Para não confundir: quando eu digo plano executivo, não é a planta nem o projeto de engenharia. O projeto mostra como construir. O plano executivo mostra se vale construir, o quê, por quanto e quando o dinheiro volta. O projeto vem dentro do plano, nunca o contrário. Eu vejo gente que paga o arquiteto primeiro e descobre depois que a conta não fecha. Antes do banquete, preparar a mesa. Todo mundo quer sentar na mesa do investidor sem ter feito a lição de casa. O plano executivo é a mesa posta.

**Página 31 · vitrine** [PAUSA]
Imagine uma vitrine com duas terras iguais, mesmo tamanho, mesmo lugar. A é a terra crua: uma matrícula e uma promessa, e quem compra faz toda a lição de casa. B é a terra com plano aprovado: mercado, viabilidade e aprovação prontos, e quem compra ganha tempo e reduz risco. A ou B? Qual vale mais, e por quê? Pense antes de seguir. Eu vejo incorporadoras, hoteleiras e entusiastas procurando exatamente a B, e quase ninguém oferecendo. Quem chega primeiro, governa. Quem prepara a terra antes define o preço e as condições.

### Vídeo 5 de 7 · O mecanismo (2 de 2) (cerca de 4:37)

**Página 32 · serra** [FOTO]
Um caso real, na Serra Catarinense. Um terreno comprado por seiscentos mil reais. Primeiro a visão, depois o plano executivo. Hoje, o terreno com o empreendimento vale cerca de seis milhões e meio, segundo o valuation do empreendimento e o balanço patrimonial. Esse valor inclui o que foi construído e investido. A lição: quem multiplicou não foi a terra sozinha. Foi a visão que virou plano, e o plano que virou negócio.

**Página 33 · joao** 
Agora um exemplo, para ilustrar o método: imagine o João. Um terreno de trezentos mil reais. Uns trinta a cinquenta mil em projetos e conhecimento. Uma SPE, a empresa criada só para aquele empreendimento, pronta para receber investidor. E o plano aprovado na prefeitura. Investimento pequeno perto do valor da terra. Ele transformou carvão em diamante: deixou de ter uma matrícula e passou a ter um negócio pronto para a mesa. Os valores variam por terreno e região.

**Página 34 · conta** 
Uma conta de padaria com dez cabanas, para mostrar que o mesmo terreno tem caminhos diferentes. É um exemplo ilustrativo. Renda, com diárias: com seiscentos e cinquenta reais de diária e de quarenta a sessenta e cinco por cento de ocupação média, dá de novecentos e quarenta e nove mil a um milhão e meio de receita por ano, e a margem que eu observo fica entre vinte e cinco e quarenta por cento. Venda por unidade: dez unidades de trezentos e cinquenta mil, três milhões e meio, e na planta só depois do registro da incorporação. Venda por cotas: cinquenta e uma cotas de trinta mil, um milhão quinhentos e trinta mil por unidade, mas vender cotas custa caro e tem regra. Não estou dizendo qual é o melhor. Estou dizendo que existe uma conta, e quem não faz a conta escolhe pelo que o vizinho fez. Qual é o melhor para o seu terreno depende do plano, e é isso que a etapa dois decide. Não é promessa de renda, retorno ou venda: converse com advogado e contador.

**Página 35 · landbank** [FOTO]
Ter a Zion como parceira é entrar no Land Bank Zion: um banco de áreas, com planos executivos estruturados que a Zion apresenta para um pool de investidores. Primeiro vêm o estudo de viabilidade e a due diligence dos documentos. Muitas vezes pedem garantia: o plano e, muitas vezes, a matrícula. Investidor não para o carro para matrícula sem plano. A Zion avalia. Nem todo plano entra. Não é oferta nem promessa de investimento, crédito ou sociedade.

**Página 36 · diagnostico** [PAUSA]
Exercício, seis minutos: em que etapa você está? Aponte a câmera para o código na tela. São vinte e um pontos: você marca onde está e descobre por onde começar. Pare o vídeo, faça, e anote a sua nota. Quem tirou menos de dez começa pela primeira etapa da Ordem, ler o terreno. Esse é o seu prêmio: saber por onde começar.

**Página 37 · ficha** [PAUSA]
Esse é o prêmio de todo mundo, com ou sem capital: o seu diagnóstico prévio. Cinco respostas que você foi anotando: a sua letra, quantas das cinco perguntas do investidor você responde, quanto a espera já custou, se a sua terra é A ou B, e em que etapa da Ordem você está, com o próximo passo. Quem tem capital sai sabendo onde gastar. Quem procura sócio sai sabendo o que o investidor pergunta. Quem quer vender sai sabendo que terra com plano vale mais. Escreva a sua ficha em uma linha, por exemplo: B, um de cinco, A, etapa um. O diagnóstico completo é o fechamento da Trilha 1.

### Vídeo 6 de 7 · Transição (cerca de 1:14)

**Página 38 · bloco-5** 
Bloco cinco. A transição: o ciclo completo, e a pergunta que fica.

**Página 39 · ciclo** 
E depois que abre? O desenvolvimento termina na abertura. A hospitalidade começa ali. O Método Zion tem três metodologias. Desenvolvimento, antes de abrir, que é a Ordem Zion e a Trilha 1. Gestão: quem conduz o negócio e com que régua. Uma boa gestão aumenta o valor do ativo. E Operação: como o padrão se entrega todo dia sem depender do dono. Uma boa operação mantém o hotel aberto. Muitos não quebram pelo terreno nem pelo produto; quebram porque tudo depende do dono. Uma operação que depende do dono não é vendável: é um emprego. Gestão e Operação são a Trilha 2, em lista de espera para quem já opera.

**Página 40 · transicao** 
Agora você já sabe o que precisa ser feito e por quê. A pergunta que fica é: como fazer isso na sua terra, com o seu dinheiro, no seu tempo?

### Vídeo 7 de 7 · A Trilha 1 (cerca de 6:21)

**Página 41 · bloco-6** 
Bloco seis. A Trilha 1: a Turma Fundadores, os bônus e as três portas. Eu prometi abrir as vagas no final. Chegou a hora.

**Página 42 · finalidades** 
Para que estruturar o seu projeto? Três finalidades, o mesmo método. Primeira: vou fazer sozinho, e quero saber onde gastar do jeito certo e na ordem certa. Segunda: tenho o terreno e não tenho o dinheiro, e quero atrair um sócio, um investidor ou até a Zion para o meu projeto. Terceira: quero fazer disso uma profissão. É o developer, e é o corretor de imóveis que capta áreas, desenvolve, prepara e faz a ponte entre o dono da terra e o investidor. E o investidor pode ser quem compra o terreno, uma incorporadora, uma empresa hoteleira, ou você mesmo. A Zion avalia cada projeto. Não é promessa de investimento, crédito ou sociedade. Qual das três é a sua finalidade?

**Página 43 · trilha1** 
Para quem está no começo, a Trilha 1: da visão parada ao plano executivo com a conta fechada, a nota de investimento e o plano de lançamento, em noventa dias. Doze encontros ao vivo comigo, toda semana, gravados. Mês um: ler o terreno e decidir o negócio. Mês dois: quando contratar arquiteto e engenheiro ambiental, se precisa mesmo, master plan e licenciamento. Mês três: fechar a conta, com custo, juros, retorno e riscos, captar e lançar. Muitas vezes contratamos profissional que não era necessário, e o que era necessário custava menos do que a gente imaginava. Você não vira arquiteto nem engenheiro. Aprende o que pedir, o que conferir e o que vai para a sua pasta.

**Página 44 · entregaveis** 
O que você recebe, e para quê. Encontros ao vivo para as dúvidas do seu plano. A sessão de boas-vindas, com o diagnóstico do seu terreno. Aulas e e-books, para rever quando precisar. As ferramentas do método, com o briefing e o checklist de cada profissional. A Zaya, a assistente de inteligência artificial para o dia a dia. O Dossiê, que é o seu plano executivo, com a nota de investimento. O plano de lançamento, para vender antes de abrir. A entrada do plano estruturado no Land Bank Zion, que a Zion avalia. E o certificado e a turma. Você não vira arquiteto. Aprende a dirigir quem faz.

**Página 45 · bonus** 
Um bônus para cada medo que eu ouço toda semana. Não tenho capital: a aula Capital sem Capital. Não sei se meu terreno serve: o diagnóstico revisado pela equipe Zion. Não tenho tempo: a Zaya e as ferramentas prontas. Minha família decide junto: uma cadeira para o sócio ou cônjuge. E a Bubble? Condição de aluno na Glamping Store, depois do plano. Vou conseguir? Revisão do Dossiê na semana doze. Quero ver como funciona por dentro: hospedagem na Zion, com trinta por cento na primeira noite e cinquenta na segunda. E quero gente do setor perto de mim: o Encontro presencial em Florianópolis, a cada seis meses, com certificado.

**Página 46 · ancoragem** 
Para comparar: quando a Zion cotou a estruturação de um empreendimento com uma consultoria de referência, a proposta chegou a cento e vinte mil reais. Uma hospedagem decente começa por volta de cento e cinquenta mil. No Pix, a Turma Fundadores é menos de dois por cento disso. Para gastar menos e errar menos.

**Página 47 · investimento** 
O investimento na Turma Fundadores: seis de quinhentos e quarenta e nove reais no cartão, ou dois mil seiscentos e noventa e sete reais à vista no Pix. Faz sentido para você?

**Página 48 · garantia** 
A garantia: o risco fica comigo. Sete dias para desistir por qualquer motivo, com cem por cento de volta. E mais: se você fizer as entregas e não terminar os noventa dias com o Dossiê pronto, continua na turma seguinte sem pagar nada. A garantia é sobre o plano, que depende do método. Nunca sobre capital, sócio ou renda.

**Página 49 · bonusdia** 
Para quem entrou no dia da aula ao vivo, até as vinte e três e cinquenta e nove, teve mais um bônus: o Diagnóstico do Terreno revisado pela equipe Zion, na primeira semana.

**Página 50 · caminhos** 
Daqui você tem três caminhos. Fazer sozinho, que é legítimo, mas paga em tempo e em erro que às vezes não tem volta. Ir juntando conselhos, que paga caro, e ninguém junta as peças. Ou seguir um método, que pede execução, e é o que a turma faz com você. Os três chegam. Um custa mais tempo, outro custa mais dinheiro, e o terceiro pede execução. Da visão nasce um plano. Do plano, um resultado.

**Página 51 · porta** 
Escolha a sua porta. Quem já decidiu entra agora, pelo link de inscrição da Turma Fundadores. Quem quer conversar antes preenche a aplicação, e a equipe fala com você sobre o seu terreno na Sessão Zero, de trinta a quarenta e cinco minutos. E quem já opera entra na lista de espera da Trilha 2, Gestão e Operação. Lembra do começo? Visão, tempo e modo. Agora você sabe qual dos três te falta. Da visão nasce um plano; do plano, um resultado. Se faz sentido para você, nós te aguardamos. Obrigado.

FIM DO PROMPT
