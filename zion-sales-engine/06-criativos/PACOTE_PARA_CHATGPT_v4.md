# Pacote para o ChatGPT v4 · Nova estrutura (decisão de Bruno, 25/11) · Mini Mentoria de Estruturação Zion (R$ 47)

Substitui `PACOTE_PARA_CHATGPT_v3.md` (v3 vira histórico; o que ele diz sobre captação por **formulário** está **superado**). **Sem execução:** nada foi enviado ao Meta, ao ClickMax nem ao WhatsApp. **PARE TUDO na Zion Collection: nenhuma campanha ativa e nada a ativar.** Criar sempre **pausado**; subir ou ativar qualquer anúncio exige "aprovado" de Bruno; teto de gasto atual = R$ 0 até ele aprovar (CLAUDE.md). URLs públicas das artes abrem depois do deploy do GitHub Pages. Marcação: [E] lido/executado, [H] hipótese, [NC] a confirmar.

## 0. A nova estrutura em uma tabela
| Bloco | Peças | Promete/vende | Destino | Quem vende |
|---|---|---|---|---|
| **A · Entrada (WhatsApp)** | Vídeos 01 e 02 | **Nada.** Só "queremos conhecer o dono de terreno" | **WhatsApp direto** (botão Enviar mensagem, sem formulário, sem cobrança) | A equipe comercial/SDR/Bela vende a Mini Mentoria R$ 47 **dentro do WhatsApp**, na janela de atendimento |
| **B · Venda quente** | 6 anúncios (carrosséis e imagens) | Mini Mentoria R$ 47, com preço | Página `/mini-mentoria` (landing v2), depois checkout limpo | A página |
| **B · Venda fria** | 6 anúncios (carrosséis e imagens) | Mini Mentoria R$ 47, com preço | idem | A página |
| **C · Vídeos novos de venda de Bruno** | 3 vídeos (gravação hoje) | Mini Mentoria R$ 47, com preço | idem | A página. **Reservado, ver §5** |
Produto único: **Mini Mentoria de Estruturação Zion**, R$ 47, pagamento único, sem mensalidade, Pix ou cartão à vista, 12 meses, 9 módulos e 70 aulas e materiais, reembolso em 7 dias. Nome comercial único. Não criar produto novo.

## 1. BLOCO A · Entrada por WhatsApp (Vídeos 01 e 02) · detalhes completos em `ENTRADA_WHATSAPP.md`
- **Objetivo da campanha:** mensagens (clique para WhatsApp). **Sem formulário, sem site.** Nome da campanha `entrada-whatsapp | AAAA-MM-DD`; nome do anúncio = id do criativo.
- **Dois anúncios novos** (não editar os ativos; criativo e formulário antigos não são editáveis):
| id (nome do anúncio) | Vídeo | Título | Descrição | CTA do botão | Mensagem pré-preenchida |
|---|---|---|---|---|---|
| `entrada-wa-v02-dono-terreno` | Vídeo 02 Dono de Terreno | Dono de terreno? Fale com a Zion | Fale com a equipe no WhatsApp | **WhatsApp: Enviar mensagem** (`WHATSAPP_MESSAGE`) | Olá, vi o vídeo e tenho um terreno. |
| `entrada-wa-v01-terreno-capital` | Vídeo 01 Terreno Capital | Terreno parado? Converse com a Zion | Fale com a equipe no WhatsApp | idem | Olá, vi o vídeo e tenho um terreno parado. |
- **Texto primário e perguntas rápidas:** `ENTRADA_WHATSAPP.md` §1 (versões A e B; **B recomendada**; Bruno decide).
- **Vídeo (arquivo):** **o áudio original NÃO pode ser usado** (promete consultoria, investimento, bubbles). Usar **(1)** a versão **regravada por Bruno** (roteiros de 30 a 45 s em `ENTRADA_WHATSAPP.md` §3) ou **(2)** as versões **mudas novas** `entrada-wa-v0{1,2}-...-{A,B}-sem-audio.mp4` (fora do repositório, em `/tmp/claude-0/-home-user-zion-hotel-ai-developer/20b679d3-1387-56c1-a153-2b815cdf3664/scratchpad/cap/entrada/`; Bruno hospeda). Cartela final: "Queremos te conhecer · Converse com a equipe pelo WhatsApp". Sem preço, sem promessa.
- **Atribuição:** não há UTM no destino (é WhatsApp). Ligação anúncio → conversa pelo identificador do clique que o Meta entrega [H]; **testar antes de ligar** (`ENTRADA_WHATSAPP.md` §1 e §5). Link que a equipe envia na conversa (padrão de canal, `PADRAO_UTM.md` §5): `.../mini-mentoria?utm_source=whatsapp&utm_medium=sdr&utm_campaign=entrada-whatsapp&utm_content=<id do criativo>-oferta&src=whatsapp` [NC: o DATA acrescenta `entrada-whatsapp` ao padrão].
- **Antes de ligar [NC, dependem de Bruno]:** número de WhatsApp Business correto; **nenhuma automação do ClickMax dispara para conversa nova de WhatsApp com R$ 97/R$ 270** (o fluxo `bc86b069` e o modelo `clube_plataforma_d0` não podem rodar); prompts da Bela/Zaya sem R$ 97, R$ 270, consultoria, reunião, banco de áreas; quem atende e em que horário.

## 2. BLOCO B · VENDA QUENTE (remarketing: visitantes da página e quem já conversou, **excluídos compradores**). 6 anúncios
Público: quem visitou a página ou a oferta; quem conversou no WhatsApp **se** o público de mensagens puder ser usado [NC]; **não subir lista de leads antigos** sem base legal e consentimento (`10-trafego/LGPD_BASE_LEGAL_E_PUBLICOS.md`). Excluir compradores quando tecnicamente possível.
| # | id (= `utm_content`) | Formato / cartões | Arquivos | Título | Primeira linha do texto primário | Descrição |
|---|---|---|---|---|---|---|
| Q1 | `mm47f3-c02-plataforma-por-dentro` | **Carrossel 5** | `docs/ads/mm47-fase03/c02-plataforma-1..5.png` | Veja por dentro da plataforma | R$ 47 · Veja por dentro da plataforma: capturas reais das telas da Mini Mentoria de Estruturação. | Mini Mentoria Zion · R$ 47 |
| Q2 | `mm47p0-n02-dossie-passeio` | **Carrossel 4** | `docs/ads/mm47-p0/n02-dossie-passeio-1..4.jpg` | Veja a plataforma por dentro | Acesse a plataforma por R$ 47 · Cada ficha vira uma página do seu Dossiê. Veja em três telas reais. | idem |
| Q3 | `mm47f3-c08-oferta-47` | Imagem | `docs/ads/mm47-fase03/c08-oferta-47.png` | Mini Mentoria por R$ 47 | R$ 47 · Mini Mentoria de Estruturação: aprenda o passo a passo para estruturar o seu empreendimento turístico. | idem |
| Q4 | `mm47p0-n06-entregaveis-numeros` | Imagem | `docs/ads/mm47-p0/n06-entregaveis-numeros.jpg` | O que vem dentro, em números | Acesse a plataforma por R$ 47 · 9 módulos, 70 aulas e materiais, 12 meses de acesso e o Dossiê em PDF. | idem |
| Q5 | `mm47p0-n07-para-quem-e` | Imagem | `docs/ads/mm47-p0/n07-para-quem-e.jpg` | É para você? | Acesse a plataforma por R$ 47 · É para você? Quem tem terreno ou ideia, quer entender custo e topa estudar. Não é reunião nem garantia de resultado. | idem |
| Q6 | `mm47f3-c09-objecoes` | Imagem | `docs/ads/mm47-fase03/c09-objecoes.png` | Quatro perguntas honestas | R$ 47 · É reunião? Preciso de capital? E se eu não gostar? Garante parceria? Respostas diretas. | idem |
**Reserva (não entra nas 6):** `mm47p0-n03-exemplo-ficticio` (exemplo com dados fictícios; o botão da arte diz "FAÇA A SUA CONTA", que pode ser lido como "criar conta": trocar o texto do botão antes de usar [NC, a arte é minha: ajusto se Bruno quiser]).
**Mudança em relação à v3:** entrou Q1 (carrossel de 5 cartões com telas reais; não usa as telas proibidas) no lugar de `n03`, para a quente ter dois carrosséis de verdade.

## 3. BLOCO B · VENDA FRIA (Brasil amplo, excluindo leads, conversas e compradores quando possível). 6 anúncios
| # | id (= `utm_content`) | Formato / cartões | Arquivos | Título | Primeira linha do texto primário | Descrição |
|---|---|---|---|---|---|---|
| F1 | `mm47p0-vp0-a3-saiba-o-custo` | **Carrossel 5** | `docs/ads/mm47-p0/vp0-a3-saiba-o-custo-1..5.jpg` | Saiba quanto custa o seu projeto | Acesse a plataforma por R$ 47 · Antes de falar com um investidor, saiba quanto custa o seu projeto. | Mini Mentoria Zion · R$ 47 |
| F2 | `mm47p0-vp0-a1-dor-direta` | **Carrossel 5** | `docs/ads/mm47-p0/vp0-a1-dor-direta-1..5.jpg` | Tem terreno? Estruture primeiro | Acesse a plataforma por R$ 47 · Tem terreno, mas não tem capital? Aprenda o passo a passo para estruturar o seu projeto. | idem |
| F3 | `mm47p0-vp0-carrossel-c-narrativa` | **Carrossel 7** | `docs/ads/mm47-p0/vp0-carrossel-c-narrativa-1..7.jpg` | Terreno + projeto = destino | Acesse a plataforma por R$ 47 · Você tem um terreno em um destino turístico, mas não tem capital para desenvolver? | idem |
| F4 | `mm47f3-c04-ordem-certa` | **Carrossel 6** | `docs/ads/mm47-fase03/c04-ordem-certa-1..6.png` | A ordem certa para estruturar | R$ 47 · A ordem certa para estruturar um empreendimento turístico, em sete pilares. | idem |
| F5 | `mm47f3-c03-custo-escondido` | Imagem | `docs/ads/mm47-fase03/c03-custo-escondido.png` | Quanto custa deixar tudo pronto? | R$ 47 · Você sabe o preço da cabana. Sabe quanto custa deixar tudo pronto? | idem |
| F6 | `mm47f3-c06-obra-ultimo-passo` | Imagem | `docs/ads/mm47-fase03/c06-obra-ultimo-passo.png` | Estruture antes de construir | R$ 47 · "Primeiro eu construo, depois eu vejo se dá certo." Começar pela obra é começar pelo último passo. | idem |
**Reserva:** `mm47f3-c10-obra-ou-estrutura` (substituída por F4; sobe se Bruno preferir imagem a carrossel); vídeo mudo `vp0-v02-passeio-mm47-sem-audio.mp4` (opcional; fora do repositório).
**Hoje a fria tem 4 carrosséis e 2 imagens; a quente, 2 carrosséis e 4 imagens.** Não faltou nenhuma peça para completar 6 por temperatura, então **não produzi arte nova** (a pasta `docs/ads/venda-carrossel/` não foi criada; só se criaria se uma delas fosse reprovada).

## 4. Para todas as peças de venda (B quente e fria)
- **Texto completo (texto primário inteiro, "o que você recebe", condições):** campo `texto` de `docs/ads/mm47-p0/manifesto.json` e `docs/ads/mm47-fase03/manifesto.json`, pelo `id`. Não reescrever; todas já passaram pela checagem P0 (preço na arte, "Aprenda o passo a passo", sem reunião/parceria/investimento garantidos, fotos sem pessoas, **sem texto sobre foto real**, rodapé de condições na arte).
- **Botão do Meta:** **Saiba mais**. **Chamada na arte:** "Aprenda o passo a passo · R$ 47" ou "Acesse a plataforma por R$ 47" (já está na arte). Em todo botão que leva ao checkout, na **página**, o texto é "QUERO ACESSAR A PLATAFORMA POR R$47".
- **Destino:** `https://infoprodutos-zion.clickmax.space/mini-mentoria` (sem `#pagar`, sem parâmetros na URL). Nunca `/inscricao`, `/inscricao-47`, `/inscricao-curta`, `/parceiro-zion`. Se o teste A/B de landing estiver ativo: `-a` / `-b` e sufixo no `utm_content` (`PADRAO_UTM.md` §3).
- **Descrição:** o manifesto traz "Mini Mentoria Zion · R$ 47 · pagamento único" (44 caracteres, acima dos ~30 recomendados [H]); usar **"Mini Mentoria Zion · R$ 47"** (26).
- **Tags de URL** (colar **uma vez**, no campo "Parâmetros de URL" do anúncio; `PADRAO_UTM.md` §9.1 vale sobre os manifestos antigos, que ainda trazem `utm_campaign=mm47`):
```
quente: utm_source=meta&utm_medium=paid&utm_campaign=venda-quente&utm_content=<id>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
fria  : utm_source=meta&utm_medium=paid&utm_campaign=venda-fria&utm_content=<id>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
```
  `<id>` = a coluna "id" das tabelas (sem espaço, maiúscula nem acento). Exemplo: `utm_content=mm47f3-c02-plataforma-por-dentro`.
- URL pública da arte: `https://bchaerk-creator.github.io/zion-hotel-ai-developer/<caminho a partir de docs/>`.
- **Coerência (5 respostas):** o anúncio promete a Mini Mentoria R$ 47 e o aprender do passo a passo; a página mostra produto, telas e preço; o cliente vê R$ 47 na arte, na página e no checkout; o checkout cobra R$ 47; o cliente recebe o acesso à turma (9 módulos, 70 aulas e materiais).

## 5. ESPAÇO RESERVADO · vídeos novos de venda de Bruno (gravação hoje; `ROTEIRO_GRAVACAO_HOJE.md`)
**Ainda não existem arquivos.** Quando Bruno enviar e eu editar, o ChatGPT recebe **uma atualização deste pacote (v4.1)** preenchendo a tabela:
| id (= `utm_content`) | Vídeo | Temperatura | Arquivo | Título | Primeira linha do texto primário | CTA | Status |
|---|---|---|---|---|---|---|---|
| `mm47-venda-v01-curto-vid` | Venda direta curta (50 a 60 s) | fria | _a preencher_ | _a definir (ex.: Aprenda a estruturar o seu projeto)_ | R$ 47 · _a definir_ | Saiba mais | aguardando gravação |
| `mm47-venda-v02-passeio-vid` | Passeio pelo Dossiê e pela plataforma (60 a 75 s) | quente (e fria como teste) | _a preencher_ | _a definir (ex.: Veja a plataforma por dentro)_ | R$ 47 · _a definir_ | Saiba mais | aguardando gravação |
| `mm47-venda-v03-objecoes-vid` | Objeções (55 a 65 s) | quente | _a preencher_ | _a definir (ex.: Quatro perguntas honestas)_ | R$ 47 · _a definir_ | Saiba mais | aguardando gravação |
**Não subir nenhum vídeo de venda sem preço dito em voz e na tela, nem antes de eu entregar a edição com a checagem de termos.**

## 6. O QUE NÃO USAR
- **Zion Collection e captação por formulário:** nenhuma campanha ativa; **não ativar nada**; **não** reaproveitar os 3 anúncios de R$ 270 no ar (Vídeo 01, Vídeo 02, Carrossel C originais), os 2 "FORM 47" nem os formulários "inscrição" e "Direto low".
- **`docs/ads/captacao-p0/` (Carrossel C v-captação, 7 cartões):** **NÃO serve para venda** (fala em "cadastro gratuito" e leva a formulário) **nem** para a entrada (não é vídeo, e a captação por formulário parou). Fica guardado, **sem uso**.
- **Os vídeos 01 e 02 com o áudio original** ("agende a tua sessão de consultoria", "investimentos em destinos turísticos", bubbles à venda, "setor que mais cresce"): proibidos. Também **não** usar as mudas antigas `capt-v01/v02-...-sem-audio.mp4` (cartela "Cadastro gratuito · Formação paga a partir de R$47" e "conteúdos" não valem mais).
- **Preço, formação paga ou produto citado nos anúncios de entrada** (ordem de Bruno): na entrada não há preço. (Na variante B, só "uma formação digital paga", sem nome e sem valor.)
- Fluxo `bc86b069` e modelo `clube_plataforma_d0` (R$ 97, banco de áreas, `/inscricao`): **não podem rodar para leads novos**; propor o substituto ao Meta é de `MENSAGENS_TRANSICAO_E_EDUCACAO.md` e depende de Bruno.
- Termos: R$ 97, R$ 270, taxa, inscrição, cadastro (como produto), agende, consultoria, reunião, sessão, avaliação do terreno, Land Bank, banco de áreas, sócio, investimento/parceria como promessa, calculadora/simulador, "sem capital" como afirmação, "faturar", "ganhar dinheiro", "20 anos".
- Telas da plataforma `agendar`, `mapa`, `raiox`, `implantacao`; aula 1 do Onboarding (Land Bank); mostrar dado de aluno.
- Fotos de banco sem conferência visual; qualquer pessoa na foto sem autorização; imagem gerada como foto real.
- Peças fora das listas: `n01` (autoridade; depende de Bruno confirmar fatos), `n04`, `n05`, `mm47f3-c10` (reserva), `n03` (reserva).

## 7. Ordem de execução e aprovação (ChatGPT executa só com "aprovado" de Bruno)
| # | Ação | Quem executa | Aprovação | Reversão |
|---|---|---|---|---|
| 1 | Bruno escolhe A ou B nos textos de entrada e regrava a voz (ou aprova o mudo) | Bruno | Bruno | n/a |
| 2 | Bruno grava os 3 vídeos de venda; eu edito (v4.1) | Bruno + CREATIVE | Bruno | n/a |
| 3 | Conferir número de WhatsApp, atendimento, automações e prompts da Bela (`ENTRADA_WHATSAPP.md` §5.6) | Bruno / responsável Bela | Bruno | n/a |
| 4 | Criar **pausadas**: campanha de entrada (2 anúncios), venda quente (6) e venda fria (6) | ChatGPT (Windsor) | Bruno | arquivar |
| 5 | Pausar de vez o que sobrou da captação por formulário e da Zion Collection | Bruno / ChatGPT | Bruno | reativar |
| 6 | Ativar | Bruno ("aprovado") | Bruno | pausar |
Orçamento: o teto de R$ 60/dia do funil híbrido tinha "captação" como um dos blocos; com esta decisão a composição muda (entrada WhatsApp, venda quente, venda fria). **Quem recompõe é FINANCE/TRAFFIC [NC]**; até lá, R$ 0.

## Teste (grep de termos proibidos)
Verificador `check_termos.py` (scratchpad `cap/`): procura por linha `R\$ ?97|R\$ ?270|inscri|taxa de|banco de áreas|Land Bank|agend|sócio|faturar|ganhar dinheiro|mais cresce|equipe entrar|avaliamos|selecionando destinos|viabilizar|majestosas` e, por sentença, `reunião|consultoria|avaliação|investimento|parceria|renda|garantia` **sem** negação.
Resultado, executado nesta sessão: ver linha "Resultado do teste" abaixo.
**Resultado do teste (executado em 25/11/2026):** `build_video_entrada_wa.js` (textos de cena e cartela): **2 achados, os dois da frase "queremos te conhecer"**, liberada por ordem de Bruno (25/11) e usada só como convite, sem promessa. `ENTRADA_WHATSAPP.md`, `ROTEIRO_GRAVACAO_HOJE.md` e este pacote: 39 linhas sinalizadas, **todas** em linhas que listam termos proibidos, descrevem o que foi removido, negam ("não é reunião nem consultoria", "Garante parceria? Não") ou citam a fala antiga reprovada; nenhuma está em texto de anúncio, de tela, de cartela ou de fala proposta. Os 12 anúncios de venda não foram alterados (já passaram pela checagem P0).
**Teste visual:** conferi a olho o contato dos 12 anúncios de venda (preço na arte, rodapé, sem pessoas, sem texto sobre foto) e 12 quadros dos vídeos mudos novos (texto no painel, cartela final correta).

## Criativos de venda a partir dos campeões originais (v5)
Ordem de Bruno (25/11): todo criativo parte do que já funciona, editando o arquivo ORIGINAL e trocando só os textos. As peças `vp0-carrossel-c-narrativa-1..7` e `vp0-a1-dor-direta-1..5` (`docs/ads/mm47-p0/`) estão **SUBSTITUÍDAS** por estas (reconstruíam os cartões com painéis novos).
| Peça | Pasta | Conteúdo |
|---|---|---|
| Carrossel C de venda (7 cartões 1080×1350) | `docs/ads/venda-carrossel-c/` | `carrossel-c-venda-1..7.png`, `painel-comparacao.jpg` (original × novo), `COPIES.md`, `manifesto.json`, `build.js`, `troca_fotos.py`. Mesmas imagens, blocos, fontes e ordem do campeão; cartões 4 e 7 com foto real sem pessoas |
| Curso Terreno A1 de venda (5 cartões) | `docs/ads/venda-a1/` | `carrossel-a1-venda-1..5.png`, `painel-comparacao.jpg`, `COPIES.md`, `manifesto.json`, `build.js` (mesmo gerador do A1 v2) |
Destino: `/mini-mentoria`; botão do Meta "Saiba mais"; arte do último cartão "QUERO ACESSAR A PLATAFORMA POR R$47"; UTM do PADRAO_UTM §9 (`venda-fria` ou `venda-quente`, `utm_content` = id do criativo). Nada enviado ao Meta; criar pausado e ativar só com "aprovado".
**Teste:** grep de termos proibidos (R$97, R$270, inscri*, taxa, banco de áreas, Land Bank, agend*, sócio, sessão, reunião, consultoria, garantido, 20 anos, equipe, renda) nos textos das artes e nos COPIES: limpo (as únicas ocorrências estão nas linhas "o que mudou", que citam o texto antigo). Texto primário 464 e 301 caracteres; título 25. Conferido a olho nos 12 cartões: sem texto vazando, legível no celular.
**Sinalização:** cartões 2 e 6 do Carrossel C mantêm imagens do campeão de origem não verificada (legenda "ilustrativa"); Bruno pode pedir troca por foto da biblioteca.
