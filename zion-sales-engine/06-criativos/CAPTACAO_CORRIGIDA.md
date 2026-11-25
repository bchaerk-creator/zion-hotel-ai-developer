# Captação corrigida · Caminho A (funil quente) · ZION CREATIVE · 25/11/2026

Ordem de Bruno (`REGRAS_FUNIL_HIBRIDO`): captar sem fazer a pessoa acreditar que receberá investimento, consultoria gratuita, reunião, avaliação do terreno ou parceria garantida e depois surpreendê-la com oferta paga. Este arquivo traz **só o delta** sobre `AUDITORIA_COERENCIA_P0.md` (não repete a auditoria). Marcação: [E] lido, [H] hipótese, [NC] não confirmado. **Nada foi enviado ao Meta nem alterado no Windsor, no ClickMax ou no WhatsApp.** Números de desempenho e dados de leads ficam fora do repositório (público).

Arquivos desta entrega: este arquivo (itens 1 e 5), `FORMULARIO_CAPTACAO_TEXTOS.md` (item 3), `MENSAGENS_TRANSICAO_E_EDUCACAO.md` (item 4), `docs/ads/captacao-p0/` (7 PNG, `COPIES.md`, `manifesto.json`), `build_cards_captacao.js`, `build_video_captacao.js`, `gera_manifesto_captacao.py`.

## 0. O que a captação passa a dizer (mensagem única, igual na arte, na fala, no texto e no formulário)
1. **Quem somos e o que fazemos:** a Zion ensina, em formação digital, a metodologia para estruturar e desenvolver projetos turísticos (território, mercado, orçamento, pré-viabilidade, Dossiê). A Zion opera hospedagens em Urubici e Florianópolis [E, CLAUDE.md].
2. **O cadastro é gratuito** e não obriga a nenhuma compra. A pessoa recebe conteúdos de educação (sequência em `MENSAGENS_TRANSICAO_E_EDUCACAO.md`; **só existe depois que Bruno aprovar e o FUNNEL montar**: ver dependência na seção 6).
3. **Existem formações pagas**, incluindo a **Mini Mentoria de Estruturação Zion, R$ 47**, pagamento único. Só compra quem quiser.
4. **Não há:** reunião, consultoria (gratuita ou paga), avaliação do terreno, sócio, parceria ou investimento garantidos. "Potenciais parceiros e investidores" aparece só como destino de apresentação do projeto, nunca como promessa (frase pendente de aprovação de Bruno, igual às peças P0).
5. **Preservado do que gerou interesse:** hook "Você aí, dono de terreno" / "Ei, você, dono de terreno!" e "tem terreno, mas não tem capital?"; ordem narrativa (dor, potencial não basta, equação, o que você já tem, autoridade, não precisa construir, convite); fotos reais da Zion sem pessoas; paleta musgo, preto, creme e dourado; Cormorant e Aventa.

## 1. Leitura nova (o que ainda não tinha sido lido) [E, Windsor `facebook_leads` e `facebook`, 25/11/2026, só leitura, sem dado pessoal]

### 1.1 Formulário nativo "Seu terreno pode ser o próximo destino da Zion.- inscrição" (campanha `[ZION COLLECTION][LEADS][FORM INSCRIÇÃO → LANDING → R$ 270] [22/11]`)
| Elemento | O que existe [E] | Problema |
|---|---|---|
| Nome do formulário | "Seu terreno pode ser o próximo destino da Zion.- inscrição" | Promete "a Zion" como destino do terreno; "inscrição" |
| Campos padrão | colunas de nome, e-mail e telefone existem no conector | O conector não mostra obrigatoriedade [NC] |
| Pergunta personalizada 1 | "Qual a localização do terreno ou projeto?" (texto livre; respostas variam de cidade a parágrafos sobre a propriedade) | Dado desnecessário para um cadastro de educação; induz "a Zion vai avaliar o meu terreno"; texto livre pode trazer dado pessoal |
| Pergunta personalizada 2 | "Qual o objetivo do projeto?" com 3 opções: desenvolver glamping, criar chalés ou cabanas, criar pousada ou hotel boutique | Útil para segmentar a educação (mantida, reescrita em "Qual a sua situação?") |
| Tela de abertura, tela final, botão final, URL de privacidade, URL de destino | **[NC]**: o Windsor `facebook_leads` não expõe esses campos | Bruno abre o formulário no Gerenciador e confere; o nome da campanha indica que o destino é a **landing de R$ 270** |
| Consentimentos | Nenhum campo de consentimento aparece [E] | Sem consentimento separado para comunicação comercial nem para personalização de anúncios |
| O que acontece depois | Lead entra no fluxo `bc86b069` (WhatsApp `clube_plataforma_d0`: "O acesso custa R$ 97", banco de áreas, botão `/inscricao`) [E, PLANO_PROVA_REAL] | Contradiz a captação nova (ver `MENSAGENS_TRANSICAO_E_EDUCACAO.md`) |

### 1.2 Formulário "Seu terreno pode ser o próximo destino da Zion.- Direto low" (campanha `FORM R$ 47 DIRETO → PÁGINA R$ 47 [24/11]`, anúncio "VIDEO 02 | FORM 47" e "CARROSSEL C | FORM 47 | 9 CARTÕES", **ativos hoje**) [E]
| Elemento | O que existe | Problema |
|---|---|---|
| Pergunta 1 | "Para ter acesso à nossa plataforma, você precisa pagar uma **taxa de inscrição** de R$ 47 para estruturar o seu terreno, projeto, ideia ou empreendimento. Você está disposto?" (as 2 respostas lidas: "não") | "Taxa de inscrição"; compra disfarçada de pergunta; não explica o que é o produto |
| Pergunta 2 | "Dentro da nossa plataforma, você está disposto a preencher os formulários e criar a estruturação da sua ideia... **para nos apresentar**?" | Induz apresentação à Zion (avaliação, parceria) |
| Pergunta 3 | Localização do terreno ou projeto (texto livre) | Dado desnecessário |
| Texto do anúncio ativo | "A Zion está em plena expansão e quer te conhecer... nós avaliamos cada caso... inscreva-se (taxa de R$ 47)... **Receba o suporte da nossa equipe e vamos agendar uma conversa. A nossa equipe entrará em contato**" | Reunião, equipe, avaliação, taxa. **Reprovado**; recomendação: pausar com "aprovado" (decisão de Bruno; não executei) |
| Veredito | **Não reutilizar o formulário nem o texto.** Formulários do Meta não são editáveis | Criar formulário NOVO (`FORMULARIO_CAPTACAO_TEXTOS.md`) |

### 1.3 Texto dos 3 anúncios no ar hoje [E]
Os três (Vídeo 01 Terreno Capital, Vídeo 02 Dono Terreno, Carrossel C campeão) dizem: "A Zion quer conhecer sua oportunidade", "Inscreva o seu terreno na Zion Collection", "**A inscrição é única, de R$ 270, e inclui uma sessão estratégica individual de 45 minutos com Bruno Chaerk**", "com possibilidade de parcerias e investimentos" (Vídeo 02 e Carrossel C) ou "Por R$ 270, você faz a sua inscrição e participa de uma sessão estratégica individual de 45 minutos, com diagnóstico preliminar" (Vídeo 01), e "A Zion avalia cada caso". Botão: Saiba mais (vídeos) e Cadastre-se (carrossel). Título "Zion Glamping Collection" no carrossel. O próprio texto já cobra R$ 270 por reunião: **a captação atual não é gratuita** e vende reunião, portanto não pode simplesmente "ganhar um aviso de R$ 47".

### 1.4 Ligação anúncio ↔ vídeo [H]
Vídeo 02 Dono Terreno = arquivo "Dono de terras em destino turístico sem capital" (68 s); Vídeo 01 Terreno Capital = "Vídeo Collection 1 - inscrição" (82 s, Bruno em câmera). Ligação por nome e tema; o Windsor não traz o `video_id` e o host da mídia é bloqueado [NC]. **Bruno confirma no Gerenciador** (abrir cada anúncio e ver o vídeo).

## 2. Tabelas por criativo · trecho atual | problema | trecho novo

### 2.1 Vídeo 02 · Dono de Terreno (anúncio `120250521991370016`, ativo)
**Fala atual [E, legenda queimada lida por OCR; pode ter pequenos erros]** e conserto proposto. A fala original **não é reaproveitada** (vende sessão de consultoria e investimento).
| Trecho atual | Problema | Trecho novo |
|---|---|---|
| Cena 0:00-0:03: mulher na piscina | Pessoa não autorizada como cliente ou equipe | Cortar; começar no b-roll sem pessoas (palmeira e bubbles) |
| "Ei, você, dono de terreno! Achou que o teu caso não tinha solução, né?" | Mantém o interesse, mas "tinha solução" prepara a promessa seguinte | **Preservar** "Ei, você, dono de terreno!". Seguir com "Achou que o seu caso não tinha solução, né?" e logo reenquadrar para projeto |
| "Nós da Zion Bubble Collection estamos selecionando destinos paradisíacos por todo o Brasil, para implantar aqui as nossas majestosas Bubbles" | Vende bubbles/seleção de destinos; sugere que a Zion escolhe o terreno | "Antes do capital, vem o projeto. Estruturar é o primeiro passo, e não exige obra." |
| "Nós temos a solução e estamos abrindo a possibilidade de investimentos em destinos turísticos e queremos te conhecer" | Promessa de investimento; "queremos te conhecer" | "A Zion opera hospedagens em Urubici e Florianópolis e organiza esse conhecimento em formação digital." |
| "Agende aqui a tua sessão de consultoria e vamos viabilizar esse projeto" | Consultoria, reunião e promessa de viabilizar | "Cadastre-se de graça e receba conteúdos para começar. O cadastro é gratuito e não obriga a nada." |
| (sem menção) | Não diz que há produto pago | "Existem formações pagas, como a Mini Mentoria de Estruturação Zion, por R$ 47. Você só compra se quiser." |
| "O teu destino pode ser o próximo do setor" | Promessa implícita de destino/parceria | "Isto é educação: não é reunião, consultoria nem avaliação do terreno, e não prometemos investimento nem parceria." |
| Texto do anúncio (ver 1.3) | R$ 270, sessão de 45 min, "possibilidade de parcerias e investimentos" | Texto novo em `docs/ads/captacao-p0/COPIES.md` (capt-v02-dono-terreno) |
| Título "Inscreva o seu terreno na Zion Collection." | Inscrição, terreno como objeto de avaliação | "Dono de terreno? Comece pelo projeto" |
| Botão Saiba mais; destino formulário R$ 270 | Destino cobra | Cadastre-se; formulário novo e gratuito |
| Cartela final "Glamping Collection, mais do que uma hospedagem, uma experiência" | Marca de hospedagem, sem a oferta | Cartela "Cadastro gratuito · Formação paga a partir de R$47" |

### 2.2 Carrossel C campeão (anúncio `120250522199990016`, ativo; 7 cartões [E, lidos antes])
| Cartão | Trecho atual | Problema | Trecho novo (`capt-c-carrossel-c-N.png`) |
|---|---|---|---|
| 1 | "Você tem um terreno em um destino turístico, mas não tem capital para desenvolver?" | Nenhum; é o hook | **Preservado**; subtítulo "Existe um primeiro passo que não exige obra: estruturar o projeto." |
| 2 | "Seu terreno pode ter potencial turístico. Sozinho, isso não vira negócio." sobre colagem CABANAS/TENDAS/BUBBLES | Imagens que não são fotos Zion [H]; texto sobre foto | **Preservado** o texto; foto real op12 em bloco próprio, texto em painel |
| 3 | "Terreno + projeto = destino" | Nenhum | **Preservado**; marca "Zion · Educação"; texto mantém "potenciais parceiros e investidores" só como apresentação, com rodapé de não promessa |
| 4 | "Apresente o que você já tem" | "Apresente" sugere entrega à Zion | "Estruture o que você já tem" → "A metodologia Zion, em passos": território, mercado, orçamento, pré-viabilidade e Dossiê |
| 5 | "A Zion já opera hospedagens em Urubici e Florianópolis" + "Mais de 20 anos de experiência internacional" | "20 anos" sem prova [NC] | Mantém a operação (fato) e troca o resto por "E organiza esse conhecimento em formação digital..." |
| 6 | "Mais que uma hospedagem, uma experiência" (foto com pessoa); "Você não precisa começar construindo um hotel" | Foto com pessoa | Só "Você não precisa começar construindo um hotel" + foto real sem pessoa (op09) |
| 7 | "A Zion quer conhecer sua oportunidade. **Inscrição R$ 270.** Cadastre seu terreno ou projeto. Apresente seu projeto em uma sessão estratégica" | Cobra R$ 270 por sessão; "cadastre seu terreno" | **"Cadastro gratuito"**, "Receba conteúdos...", "Existem formações pagas, como a Mini Mentoria de Estruturação Zion (R$ 47, pagamento único). Só compra quem quiser." Faixa: **Cadastro gratuito · Formação paga a partir de R$47** |
| Texto | "Inscreva o seu terreno... A inscrição é única, de R$ 270, e inclui uma sessão estratégica individual de 45 minutos com Bruno Chaerk... possibilidade de parcerias e investimentos" | R$ 270, sessão, parceria | `COPIES.md` (capt-c-carrossel-c) |
| Título e botão | "Zion Glamping Collection"; Cadastre-se | Título genérico de hospedagem | "Cadastro gratuito: estruture o projeto"; Cadastre-se |
| Rodapé de todos | "Fotos reais... sem promessa..." (versão venda) | Falta dizer cadastro gratuito | "Cadastro gratuito, sem obrigação de compra · Formações pagas à parte, a partir de R$ 47 · Sem reunião, consultoria nem avaliação do terreno · Sem promessa de investimento, parceria ou renda" |

### 2.3 Vídeo 01 · Terreno Capital (anúncio `120250521979600016`, ativo)
| Trecho atual [E, legenda lida; vídeo com Bruno em câmera] | Problema | Trecho novo |
|---|---|---|
| "Você aí, dono de terreno, achou que o teu terreno não tinha solução. Esse teu terreno parado há tanto tempo, dando prejuízo." | Hook e dor: é o que gerou interesse | **Preservar** "Você aí, dono de terreno" e "terreno parado há tanto tempo"; tirar "dando prejuízo" (afirmação sobre a vida da pessoa) |
| "Nós temos a solução para esse teu terreno em destino turístico" | Promessa de solução | "Você não precisa começar construindo um hotel. Dá para estruturar o projeto no papel." |
| "Nós da Zion Glamping Collection abrimos a oportunidade de você adquirir as nossas majestosas bubbles... em um dia você instala... já pode receber o teu primeiro hóspede" | Vende bubbles; expectativa de compra de equipamento | Cortar inteiro. No lugar: "A Zion ensina a metodologia para estruturar antes de construir: território, mercado, orçamento e Dossiê." |
| "Pare de vender paredes... comece a vender experiência. O Glamping é o setor que mais cresce no Brasil... começar a faturar... ganhar dinheiro" | Número de mercado sem fonte; promessa de ganho | Cortar |
| "Agende a tua consultoria com a gente e nós vamos te dar o passo a passo, direcionar você e te oferecer os melhores produtos" | Consultoria, reunião, direcionamento individual | "Cadastre-se de graça e receba conteúdos para começar... Existem formações pagas, como a Mini Mentoria por R$ 47. Você só compra se quiser. Não é reunião nem consultoria." |
| Texto do anúncio (1.3): R$ 270, sessão de 45 min, "diagnóstico preliminar" | Reunião paga | `COPIES.md` (capt-v01-terreno-capital) |
| Título "Seu terreno pode ser o próximo destino da Zion." | Sugere que a Zion escolhe o terreno | "Terreno parado? Comece estruturando" |

## 3. Peças produzidas
### 3.1 Carrossel C v-captação [PRONTO, revisado visualmente]
`docs/ads/captacao-p0/capt-c-carrossel-c-1..7.png` (1080×1350, PNG). Ordem de 7 cartões preservada; foto real em bloco próprio e **nenhum texto sobre foto**; sem pessoas; cartão final com a faixa **"Cadastro gratuito · Formação paga a partir de R$47"**; rodapé de condições em todos os cartões. URL pública esperada: `https://bchaerk-creator.github.io/zion-hotel-ai-developer/ads/captacao-p0/capt-c-carrossel-c-<n>.png` (abre depois do deploy do GitHub Pages). Gerado por `build_cards_captacao.js`.
[NC] "a partir de R$47": o catálogo tem ferramentas de R$ 19 e o Arsenal de R$ 27 (CLAUDE.md). A frase só vale se "formação" significar a Mini Mentoria e linhas de formação semelhantes. **Bruno confirma o piso** ou trocar por "Formação paga: Mini Mentoria R$47".

### 3.2 Roteiro revisado · Vídeo 02 Dono de Terreno (para Bruno gravar, ~45 s; nunca voz clonada ou sintética)
| # | Tempo | Fala | Legenda queimada | Imagem |
|---|---|---|---|---|
| 1 | 0-6 s | "Ei, você, dono de terreno! Achou que o seu caso não tinha solução, né?" | igual à fala | b-roll bubbles/palmeira, sem pessoas |
| 2 | 6-12 s | "Você tem a área e a matrícula, mas não tem capital. Antes do capital, vem o projeto." | igual | b-roll |
| 3 | 12-18 s | "Estruturar o projeto no papel é o primeiro passo: território, mercado, orçamento e pré-viabilidade, sem começar pela obra." | igual | b-roll |
| 4 | 18-24 s | "A Zion opera hospedagens em Urubici e Florianópolis e organiza esse conhecimento em formação digital." | igual | b-roll |
| 5 | 24-30 s | "Cadastre-se de graça e receba conteúdos para começar. Sem obrigação de compra." | igual | b-roll |
| 6 | 30-37 s | "Existem formações pagas, como a Mini Mentoria de Estruturação Zion, por R$ 47, pagamento único. Você só compra se quiser." | igual | tela real da plataforma |
| 7 | 37-43 s | "Isto é educação: não é reunião, consultoria nem avaliação do terreno, e não prometemos investimento nem parceria." | igual | b-roll |
| 8 | 43-52 s | (sem fala ou só "Cadastre-se grátis") | **Cartela final:** Cadastro gratuito · Formação paga a partir de R$47; condições | cartela musgo |
Proibido na gravação: "agende", "consultoria" (fora da negação), "investimentos em destinos", "selecionando destinos", "queremos te conhecer", "viabilizar", bubbles à venda, "setor que mais cresce", "faturar", "ganhar dinheiro".

### 3.3 Roteiro revisado · Vídeo 01 Terreno Capital (Bruno em câmera, mesmo enquadramento e energia; ~45 s)
| # | Tempo | Fala | Legenda / cartela |
|---|---|---|---|
| 1 | 0-6 s | "Você aí, dono de terreno. Terreno parado há tanto tempo e sem saber por onde começar?" | igual (hook preservado) |
| 2 | 6-12 s | "Você não precisa começar construindo um hotel. Dá para estruturar o projeto no papel." | igual |
| 3 | 12-18 s | "Aqui na Zion a gente ensina a metodologia para estruturar antes de construir: território, mercado, orçamento e Dossiê." | igual |
| 4 | 18-24 s | "Cadastre-se de graça e receba conteúdos para começar. O cadastro não obriga a nada." | igual |
| 5 | 24-31 s | "Também temos formações pagas, como a Mini Mentoria de Estruturação Zion, por R$ 47. Você só compra se quiser." | igual, com tela real |
| 6 | 31-37 s | "Não é reunião nem consultoria, e a gente não promete investimento, parceria nem renda." | igual |
| 7 | 37-46 s | "Cadastre-se grátis." | **Cartela final:** Cadastro gratuito · Formação paga a partir de R$47 |
Se Bruno gravar, a legenda queimada segue o texto da fala (Jost, creme sobre barra musgo); se não gravar, usar a versão muda abaixo.

### 3.4 Vídeos sem o áudio original [PRONTOS, fora do repositório; originais intactos]
- `/tmp/claude-0/-home-user-zion-hotel-ai-developer/20b679d3-1387-56c1-a153-2b815cdf3664/scratchpad/cap/video/capt-v02-dono-terreno-sem-audio.mp4` (51,8 s, 1080×1920, sem trilha de áudio, 12,6 MB).
- `/tmp/claude-0/-home-user-zion-hotel-ai-developer/20b679d3-1387-56c1-a153-2b815cdf3664/scratchpad/cap/video/capt-v01-terreno-capital-sem-audio.mp4` (45,8 s, 1080×1920, sem trilha de áudio, 10,1 MB).
- **Como foram feitos:** só imagem do vídeo "Dono de terras" (corte superior de 1080×1344, de 6 s em diante: sem a cena da piscina com pessoa e sem as legendas antigas), uma tela real da plataforma (Marco Zero e diagnóstico, sem os nomes "Club" nem Land Bank) e cartelas novas (Jost/Cormorant, paleta Zion). Gerados por `build_video_captacao.js <vídeo-fonte> <pasta>`; conferi um quadro de cada cena abrindo a imagem. O Vídeo 01 original (Bruno em câmera) **não foi usado**, porque a fala dele é a que precisa sair; esta versão muda reaproveita b-roll sem pessoas e preserva o hook em texto. Quem quer o rosto e a energia do Bruno regrava o roteiro 3.3.
- **Limite:** mudo, com texto na tela (serve a Reels e Feed com legenda). Hospedagem do arquivo para o Meta: Bruno decide (não vai ao repositório por tamanho).

### 3.5 Manifesto e copies
`docs/ads/captacao-p0/manifesto.json` (id, arquivo, URL pública esperada, texto principal, título, descrição, CTA, UTM) e `COPIES.md`. UTM: `utm_campaign=captacao`, `utm_content=<id>` (`capt-c-carrossel-c`, `capt-v02-dono-terreno`, `capt-v01-terreno-capital`), demais chaves do `09-tracking/PADRAO_UTM.md`. Obs.: o padrão fixa `utm_campaign=mm47` para anúncios de venda; `captacao` é a exceção pedida por Bruno e deve ser acrescentada ao padrão pelo DATA [NC].

## 4. Checagem de termos proibidos
Rodei `grep -n -i -E` (e o verificador por sentença) em `COPIES.md`, `manifesto.json` e nos textos dos cartões e das cenas (`build_cards_captacao.js`, `build_video_captacao.js`). Resultado e comando na seção "Teste" do final deste arquivo.

## 5. Criativos de VENDA (Caminho B frio e Caminho A quente): lista final enxuta
Base: `docs/ads/mm47-p0/manifesto.json` (10 peças), `docs/ads/mm47-fase03/` (7 peças), `PACOTE_PARA_CHATGPT_v2.md`. Critério: **fria** = pessoa não conhece a Zion: precisa de dor/curiosidade e preço claro na primeira linha; **quente** = pessoa já se cadastrou ou visitou: precisa de prova do produto, entregáveis, filtro de objeções e oferta direta. Todas já passaram pela checagem P0 (preço na arte, "Aprenda o passo a passo", sem reunião/parceria/investimento garantidos, fotos sem pessoas, destino `/mini-mentoria`).

| Temperatura | Lista final (≤ 6) | Por quê |
|---|---|---|
| **Fria (6)** | `mm47p0-vp0-a3-saiba-o-custo`; `mm47p0-vp0-a1-dor-direta`; `mm47f3-c03-custo-escondido`; `mm47f3-c06-obra-ultimo-passo`; `mm47p0-vp0-carrossel-c-narrativa`; `mm47f3-c10-obra-ou-estrutura` | Dor específica, colapso de crença e narrativa do campeão. A 1 e a 2 são os campeões do curso recuperados; a 5 é o Carrossel C na versão de venda com preço; todas abrem pela dor e mostram R$ 47 sem prometer resultado |
| **Quente (6)** | `mm47f3-c08-oferta-47`; `mm47p0-n02-dossie-passeio`; `mm47p0-n06-entregaveis-numeros`; `mm47p0-n07-para-quem-e`; `mm47p0-n03-exemplo-ficticio`; `mm47f3-c09-objecoes` | Oferta direta, passeio pela plataforma, entregáveis em números, filtro "para quem é", exemplo (dados fictícios) e objeções. Para quem já sabe quem somos |
**Fora das listas (não produzir mais):** `n01` (autoridade: depende de Bruno confirmar fatos, entra se aprovado), `n04`, `n05`, `mm47f3-c02`, `mm47f3-c04` (redundantes com as acima), o vídeo mudo `vp0-v02-passeio-mm47-sem-audio.mp4` (opcional como 7º da fria, só se Bruno quiser vídeo). Nenhuma peça nova foi produzida para venda; **o único material novo desta entrega é a captação**.
Regra de coerência quente × captação: o lead que veio da captação nova viu "cadastro gratuito" e "Mini Mentoria R$ 47". O anúncio quente mostra o mesmo nome e preço. Não usar para o quente nada que mencione R$ 97, R$ 270, "inscrição" ou "banco de áreas".

## 6. Ordem de execução proposta e o que depende de aprovação
| # | Ação | Quem executa | Aprovação | Reversão |
|---|---|---|---|---|
| 1 | Revisar e aprovar peças e textos (frase "potenciais parceiros e investidores"; "a partir de R$47") | Bruno | Bruno | n/a |
| 2 | Revisão jurídica do formulário e dos consentimentos | Advogado | Bruno | n/a |
| 3 | Criar o formulário NOVO no Gerenciador (texto em `FORMULARIO_CAPTACAO_TEXTOS.md`). `create_lead_form` do Windsor não tem campo de consentimento: usar o Gerenciador | ChatGPT com Bruno | Bruno | `set_lead_form_status` arquivar |
| 4 | Criar 3 anúncios NOVOS (pausados) ligados ao formulário novo; não editar os ativos (criativo e formulário não são editáveis) | ChatGPT | Bruno | arquivar |
| 5 | Pausar os 3 anúncios de R$ 270 e os 2 "FORM 47" | Bruno / ChatGPT | Bruno | `enable_ad` |
| 6 | **Antes de ativar o item 4:** corrigir o gatilho do fluxo `bc86b069` (hoje envia R$ 97) e montar a sequência de educação | FUNNEL + Bruno | Bruno e Meta (modelo novo) | desativar fluxo |
| 7 | Ativar a captação | Bruno ("aprovado") | Bruno | pausar |
Dependência crítica: **não ligar a captação nova enquanto o fluxo `bc86b069` ainda envia "O acesso custa R$ 97"**. Sem o item 6, a pessoa lê "cadastro gratuito" no anúncio e recebe R$ 97 no WhatsApp.

## Teste (grep de termos proibidos)
Comando: `python3 -I check_termos.py <arquivos>` (verificador no scratchpad: procura por linha `R\$ ?97|R\$ ?270|inscri|taxa de|banco de áreas|Land Bank|agend|sócio|faturar|ganhar dinheiro|mais cresce|equipe entrar|queremos te conhecer|conhece e avalia|avaliamos|selecionando destinos|viabilizar|majestosas` e, por sentença, `reunião|consultoria|avaliação|investimento|parceria|renda|garantia` **sem** negação (sem, não, nem)).
- **Peças e copies** (`COPIES.md`, `manifesto.json`, `build_cards_captacao.js`, `build_video_captacao.js`, `gera_manifesto_captacao.py`): **0 achados**.
- **Formulário e mensagens** (`FORMULARIO_CAPTACAO_TEXTOS.md`, `MENSAGENS_TRANSICAO_E_EDUCACAO.md`): 10 ocorrências, **todas** em linhas que listam o que foi removido ou o que não se deve escrever ("Removidos em relação aos formulários antigos", "Remove: R$ 97, banco de áreas...", "Cuidados: não escrever...") ou na pergunta da checagem; nenhuma está no texto proposto de tela, de modelo ou de e-mail.
- Nota: o primeiro passe do verificador acusou "Aprenda" por conter "renda"; corrigido com limite de palavra e reexecutado.
- **Teste visual:** abri os 7 cartões (contato e o cartão 7 em tamanho real) e um quadro de cada cena dos dois vídeos [E]. Texto fora de foto, sem pessoas, faixa e rodapé legíveis. Duração e trilha conferidas com `ffprobe` (51,8 s e 45,8 s, só vídeo, sem áudio).
