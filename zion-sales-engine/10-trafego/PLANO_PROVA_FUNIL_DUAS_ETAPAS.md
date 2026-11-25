# Plano de prova · Atração de leads + venda (quente e fria) · Mini Mentoria de Estruturação Zion (R$ 47)

Agente: ZION TRAFFIC, com apoio de DATA e FINANCE · 25/11/2026 · **PROPOSTA. Nada foi criado, ligado, pausado ou editado no Meta, no Windsor ou no ClickMax.** Só leitura e arquivos.
Marcação: **[E]** evidência lida, **[H]** hipótese, **[NC]** não confirmado, **[BRUNO]** só Bruno decide ou aprova. Repositório público: sem números reais de gasto, vendas, leads por etiqueta, ROAS ou CAC. Os números reais da leitura de 25/11 ficam fora do repositório. Todo valor em R$ abaixo é **parâmetro** (letra maiúscula), a ser preenchido por Bruno.
Base: ordem de Bruno de 25/11 (campanhas no ar = atração de lead; depois, venda com a narrativa correta) e o ajuste do mesmo dia (duas campanhas de venda, **quente** e **fria**). Regras comerciais: `REGRAS_P0_COERENCIA` (nenhum cliente chega ao checkout sem saber o que compra, quanto paga e o que recebe).

## Parâmetros (Bruno define; nada aqui é decisão)
| Símbolo | Significado | Quem define |
|---|---|---|
| `T` | teto diário vigente de gasto em anúncio (hoje, decisão de Bruno; teto de teste vigente para a MM47 consta em `HANDOFF_CHATGPT_FASE03.md`) | [BRUNO] |
| `G1` | orçamento diário da Etapa 1 (atração, já ligada com parte do orçamento) | [BRUNO] |
| `G2q`, `G2f` | orçamento diário da venda quente e da venda fria | [BRUNO] |
| `L` | líquido por venda: R$ 47 menos taxa fixa do gateway (R$ 44,51 no Pix [E]) menos impostos e custos variáveis (**sem valor definido**; use parâmetro `K`) | FINANCE + [BRUNO] |
| `P` | preço R$ 47 | fixo |
| Condição | `G1 + G2q + G2f <= T` em qualquer dia | regra |

---

## 1. Hipótese, enunciada para poder falhar

**H0 (a de Bruno) [H]:** Leads captados por anúncio de atração (vídeo + formulário), depois abordados por campanha de venda com a narrativa correta da Mini Mentoria, **compram a R$ 47 a um custo por comprador total menor** do que quem recebe a mesma oferta a frio, e **menor do que o líquido por venda `L`**.

Em termos mensuráveis, para a mesma janela de tempo:
- `CPC_quente = (gasto_atração_atribuído + gasto_venda_quente) ÷ compradores_quente`
- `CPC_fria = gasto_venda_fria ÷ compradores_fria`
- **H0 vale se** `CPC_quente < CPC_fria` **e** `CPC_quente < L` (com folga definida abaixo), com amostra mínima atingida (seção 3.4).

**O que REFUTA (definido antes de ligar):**
1. **Refutação forte:** com a amostra mínima atingida, `CPC_quente >= L` ou `CPC_quente >= CPC_fria`. Conclusão: atrair para depois vender a R$ 47 não paga; a atração não é etapa útil para este produto neste preço.
2. **Refutação do mecanismo:** a taxa lead→compra do grupo exposto à venda quente **não é maior** que a do grupo de controle (holdout, seção 3.5) além do intervalo de erro. Conclusão: os leads compram (ou não) igualmente com ou sem a campanha; o gasto de venda quente não causa a venda.
3. **Refutação por qualidade:** reembolso ou pedido de ajuda do grupo quente maior que o do frio em margem pré-definida (seção 3.3).
4. **Sem conclusão (não é prova nem refutação):** amostra abaixo do mínimo ao fim do prazo máximo. Nesse caso o relatório diz "inconclusivo", não "funcionou".

Pergunta que antecede tudo (leitura real já feita, resultado só fora do repositório, seção 4.5): **os leads que já existem na base compram?** Resposta preliminar [E, leitura de 25/11]: quase nenhum comprou alguma oferta, mas esses leads **nunca receberam a oferta correta de R$ 47** (a abertura atual cita R$ 97 e cadastro de área; seção 2.3). Portanto o dado não refuta H0: mostra o ponto de partida.

---

## 2. Desenho das duas etapas

### 2.1 Etapa 1 · Atração (já decidida por Bruno; no ar hoje)
| Item | Desenho |
|---|---|
| Objetivo | Leads (formulário nativo do Meta, "Direto low" e "form E" [NC: formulários do Meta não são legíveis por MCP; confirmar no Gerenciador]) |
| Criativos | Carrossel C (parte de `G1`) e Vídeos 01 e 02 (parte de `G1`) [E, informado por Bruno] |
| Público | atual da campanha [NC: conferir no Gerenciador] |
| Orçamento | `G1` (valor atual: Bruno) |
| Função | gerar a base de leads e os públicos de engajamento (formulário aberto, formulário enviado, vídeo 50% e ThruPlay) que alimentam a venda quente |

**Aviso sobre os criativos de atração:** os Vídeos 01 e 02 e o Carrossel C precisam estar com a promessa correta (sem reunião, sem "equipe entra em contato", sem investimento). O que foi aprovado como "atração de lead" não pode prometer o que o fluxo não entrega, ou a transição da seção 2.3 vira quebra de expectativa. [NC: verificar se as versões no ar são as v-P0 de `docs/ads/mm47-p0/` ou as antigas auditadas em `06-criativos/AUDITORIA_COERENCIA_P0.md`.]

### 2.2 O que acontece com o lead depois do formulário HOJE [E, leitura ClickMax 25/11]
1. **Formulário do Meta (lead nativo).** A tela de agradecimento é configurada no Meta [NC, não legível].
2. **Chegada ao ClickMax.** O lead entra com etiquetas de origem (por exemplo "FORMS FACEBOOK NATIVO", "META | FORM LAND BANK", "INSCRIÇÃO 270 | LEAD DO FORMULÁRIO"). Os nomes das etiquetas ainda trazem o modelo antigo (R$ 270, Land Bank).
3. **Fluxo `bc86b069` "Inscrição 270 · Abertura" (ativo).** Gatilho: aplicação da etiqueta "INSCRIÇÃO 270 | LEAD DO FORMULÁRIO". Envia o modelo de WhatsApp `clube_plataforma_d0` (vídeo + 2 botões). No máximo 1 vez a cada 30 dias por contato. Execuções lidas: todas bem-sucedidas, com entrega, abertura, 1 clique em botão e falhas (percentuais exatos no arquivo fora do repositório).
4. **O que o lead vê (texto do modelo, aprovado no Meta):** "Queremos te conhecer melhor... Você já tem o terreno. Nós temos o método... plataforma Zion Collection... cadastre a sua área no banco de áreas da Zion. **O acesso custa R$ 97**, em pagamento único... Parcerias e investimentos dependem da análise..." Botão "Acessar a plataforma" leva a `/inscricao` (não à `/mini-mentoria`) e botão "Não quero receber".
5. **Formulário "Direto low".** Não existe como formulário do ClickMax; é formulário do Meta [NC]. A etiqueta "TESTE B · AGENDAMENTO DIRETO (form Direto)" existe, sem leads. A informação de Bruno de que esse formulário não dispara mensagem é coerente com o que se vê: **só leads com a etiqueta "INSCRIÇÃO 270 | LEAD DO FORMULÁRIO" entram no fluxo**; leads que chegam só com "FORMS FACEBOOK NATIVO" não têm gatilho de mensagem [H, conferir se a integração aplica as duas etiquetas].
6. **Funil Zion (pipeline).** A descrição do pipeline ainda diz "Zaya qualifica e agenda a reunião estratégica sem custo... venda na reunião (Mentoria R$ 2.900...)". Há etapas de reunião e de "Janela aberta · responder agora". O pipeline de "Inscritos · Plataforma" (compradores de R$ 97) existe, desligado.
7. **Formulários do ClickMax** (quizzes e fichas): vários prometem "reunião estratégica sem custo" e "equipe Zion entra em contato". Não estão ligados aos anúncios de atração [NC], mas estão no mesmo CRM.

### 2.3 O fluxo atual é coerente com a regra nova? **Não. Conflitos (nenhum alterado):**
| # | Conflito | Regra violada | Onde |
|---|---|---|---|
| C1 | Modelo `clube_plataforma_d0` diz **R$ 97**, mas a oferta canônica é R$ 47 | preço claro e único | modelo aprovado no Meta, fluxo `bc86b069` |
| C2 | "Cadastre a sua área no banco de áreas" como parte do acesso | não vender cadastro; "avaliação" só como possibilidade | mesmo modelo |
| C3 | Botão leva a `/inscricao` (página antiga) e não à landing v2 com a Mini Mentoria | nenhum cliente chega ao checkout sem saber o que compra | mesmo modelo |
| C4 | Nome "Inscrição 270" em etiqueta, fluxo e meta; objetivo do fluxo cita outro modelo (`inscricao_novo_d0`) e se diz "RASCUNHO" com o fluxo ativo | confusão operacional; risco de ligar o fluxo errado | fluxo e etiquetas |
| C5 | Pipeline "Funil Zion" ainda conduz a reunião e a vendas de R$ 2.900, R$ 490, R$ 270 | produto único R$ 47, sem reunião | descrição e etapas |
| C6 | Leads de atração que não recebem mensagem (só "FORMS FACEBOOK NATIVO") ficam sem transição | quebra de expectativa silenciosa | gatilho do fluxo |
| C7 | O lead respondeu a um anúncio de atração que talvez prometa consultoria, inscrição ou avaliação | expectativa x produto | criativos de atração [NC] |

**Proposta de correção (precisa de aprovação, ninguém executa sem "aprovado"):** (a) **pausar** o fluxo `bc86b069` até existir modelo novo (não apagar); (b) criar modelo novo de WhatsApp no padrão P0 (R$ 47, sem banco de áreas, botão para a landing v2 com UTM do canal); enviar para aprovação do Meta é ação de Bruno; (c) a transição honesta da seção 6.4; (d) etiqueta nova de coorte por criativo/dia (seção 4.2), em vez de renomear as antigas.

### 2.4 Etapa 2 · Venda: duas campanhas

Ambas: objetivo e evento seguem o `HANDOFF_CHATGPT_FASE03.md` (Fase 0: tráfego por visualização da página, até o Purchase ser provado; Fase 1: Vendas por Purchase). **Decisão sempre por venda paga no ClickMax** (seção 4). Nascem **pausadas**. Posicionamentos manuais, sem Audience Network. Botão "Saiba mais". Destino com preço e CTA padrão **QUERO ACESSAR A PLATAFORMA POR R$47** na própria página.

**Destino (comum às duas):**
- Hoje o destino possível é `https://infoprodutos-zion.clickmax.space/mini-mentoria` (no ar, v1) [E].
- A landing **v2** existe só como rascunho não publicado: A v2 `98ef3607…` (`/mini-mentoria-a-v2`) e B v2 `1dba4c0f…` (`/mini-mentoria-b-v2`) [E, `11-testes-ab/TESTE_AB_LANDING_MM47.md`]. O pedido de Bruno é usar a v2. **Para isso, precisa aprovar:** (1) publicar a v2 (Bruno ou executor autorizado; conferir `lastPublishedAt`); (2) escolher A v2 ou B v2 para o público de cada temperatura, ou manter o teste A/B de landing separado (não misturar variáveis: ver 5.4); (3) checkout limpo configurado conforme `08-checkouts/CHECKOUT_LIMPO_MM47.md` (nome, `checkoutTitle`, descrição, capa) e conferido no celular por Bruno (o domínio do checkout é bloqueado no ambiente).
- Enquanto a v2 não estiver publicada, o destino é `/mini-mentoria`. Nesse caso a página já tem preço e entregáveis, mas **não** segue o ECROI completo da v2; registrar essa limitação ao ler resultados.

#### Campanha A · VENDA QUENTE (tem relação anterior com a Zion)
| Item | Desenho |
|---|---|
| Estrutura | 1 campanha, 1 a 2 conjuntos (ABO): conjunto Q1 (engajou com formulário/lead) e conjunto Q2 (engajou com vídeo ou visitou a página, sem lead) se cada um tiver tamanho para entrega; senão, um conjunto único com os públicos somados |
| Públicos (inclusão) | (1) **Leads por etiqueta/lista do ClickMax** como público personalizado de clientes: etiquetas de origem de atração (lista de contatos exportada e carregada por quem Bruno designar; **exige base legal**, seção 6.1); (2) **Meta, abriu o formulário e não enviou** (público de engajamento com formulário de cadastro, "abriu mas não enviou"); (3) **Meta, enviou o formulário**; (4) **visitantes de `/mini-mentoria`** (e da v2 quando publicada), últimos 30 dias, via pixel [H: conferir se o pixel identifica visitantes fora do iframe, o ViewContent está desligado]; (5) **engajamento de vídeo** 50% ou ThruPlay dos Vídeos 01 e 02, últimos 30 dias |
| Exclusões | **compradores** da MM47, do R$ 97 legado e de qualquer oferta da turma; **leads de outras linhas** (Land Bank antigo, Bubble, Noite Mágica, base antiga do SDR, corretores/operadores, quem pediu "Não quero receber"); **equipe** e testes; e o **holdout** (seção 3.5) |
| Criativos | peças que **reconhecem que a pessoa já conheceu a Zion** e levam direto à oferta e à demonstração (seção 2.5) |
| Frequência | limitar a 3 a 4 impressões por pessoa por semana [H]; se passar, pausar o conjunto (público pequeno cansa rápido) |
| Orçamento | `G2q`: proposta inicial `G2q = 0,25 × (T − G1)` [H, ajustável]; o público quente é pequeno e não absorve muito; não aumentar para "gastar" |
| Janela de atribuição | leitura no ClickMax: compra em até 7 e 14 dias após o **primeiro contato da campanha** (impressão paga e clique); no Meta, 7 dias de clique e 1 dia de visualização; comparar sempre com 1 dia de clique |

#### Campanha B · VENDA FRIA (nunca conheceu a Zion, sem dados de leads)
| Item | Desenho |
|---|---|
| Estrutura | 1 campanha, 1 conjunto aberto (Brasil; Advantage+ aberto ou interesses amplos, escolha única e registrada; **sem usar nenhum dado de leads**) |
| Públicos | frio aberto: Brasil, adultos; sem públicos personalizados de inclusão |
| Exclusões | **compradores** (todas as ofertas da turma e R$ 97 legado); **todos os leads** (etiquetas de atração e as demais bases de leads, para a comparação ser limpa); quem engajou com os anúncios de atração (formulário e vídeo); equipe e testes. Usar a mesma lista de exclusão da campanha A, **mais** os públicos de inclusão da A (sobreposição zero) |
| Criativos | peças que **explicam o produto do zero** (seção 2.5) |
| Orçamento | `G2f`: proposta `G2f = 0,75 × (T − G1)` [H]. A venda fria precisa de volume para chegar a compras; mas respeite `G1 + G2q + G2f <= T` |
| Janela | igual à da quente, para comparação justa |

**Regra de justiça da comparação:** as duas campanhas rodam **no mesmo período**, com **os mesmos critérios de leitura**, a mesma landing/checkout e a mesma regra de UTM (seção 4.1). A diferença deve estar só em **temperatura do público e criativo da temperatura**; isso é a variável do experimento e fica registrada. Não trocar landing no meio.

### 2.5 Criativos por temperatura (fonte: `docs/ads/mm47-p0/manifesto.json` e `docs/ads/mm47-fase03/manifesto.json`)
Não editar a arte. Todo texto principal segue `COPIES_P0.md` / `COPIES.md`; só a **primeira linha** da quente é nova (propostas abaixo, sujeitas à revisão do CREATIVE e à regra "sem promessa").

**Quente (reconhece que já conheceu a Zion e vai direto à oferta e à prova do produto):**
| Peça | Por quê | Primeira linha proposta [H] |
|---|---|---|
| `mm47p0-n02-dossie-passeio` (carrossel 4) | demonstração real, quem já ouviu quer ver o produto | "Você já conheceu a Zion. Agora veja a plataforma por dentro." |
| `mm47f3-c02-plataforma-por-dentro` (carrossel 5) | telas reais | "Você viu o vídeo. Aqui estão as telas reais da Mini Mentoria." |
| `mm47p0-n06-entregaveis-numeros` | oferta em números | "R$ 47 · o que você recebe, sem surpresa." |
| `mm47f3-c09-objecoes` | quebra de objeções de quem hesitou (era a dúvida: reunião? parceria?) | "R$ 47 · Você tinha perguntas. Respostas diretas." |
| `mm47f3-c08-oferta-47` | oferta direta | "R$ 47 · A Mini Mentoria de Estruturação Zion é uma formação digital, sem reunião." |
Obrigatório em pelo menos uma peça quente: **dizer o que mudou** (seção 6.4): a oferta é uma formação digital autônoma, sem reunião, sem inscrição de área.

**Fria (explica do zero o produto, dor primeiro, ECROI):**
| Peça | Por quê |
|---|---|
| `mm47p0-vp0-a1-dor-direta` (carrossel 5) | campeão A1 v2 corrigido: espelhamento |
| `mm47p0-vp0-a3-saiba-o-custo` (carrossel 5) | campeão A3 v2 corrigido: custo escondido |
| `mm47p0-vp0-carrossel-c-narrativa` (carrossel 7) | campeão C: narrativa completa |
| `mm47f3-c03-custo-escondido`, `mm47f3-c06-obra-ultimo-passo` | dor específica e colapso de crença |
| `mm47p0-n04-tres-perguntas`, `mm47f3-c04-ordem-certa` (rodada 2) | tutorial prático |
| `mm47p0-n01-autoridade-operacao` | autoridade com bastidor documentado (sem pessoas/depoimentos inventados) |
Não usar: tudo da lista "O que NÃO usar" do `HANDOFF_CHATGPT_FASE03.md` (seção 3.3). Vídeos 01 e 02 de atração **não** entram na venda fria.

### 2.6 Cadência e leitura
- **Diária (5 min, anotar a hora; o cache do Windsor atrasa):** gasto × `T`; anúncio reprovado ou sem entrega; frequência da quente; vendas pagas e Pix gerados no ClickMax por `utm_campaign`/`utm_content`/etiqueta (seção 4); vendas sem UTM separadas.
- **A cada 3 a 4 dias:** sobreposição entre A e B (deve ser zero), entrega por anúncio, tamanho do público quente, tráfego de servidor.
- **Semanal:** relatório de decisão com amostra, intervalos e as comparações da seção 3.
- **Corte final:** só quando a amostra mínima for atingida ou no prazo máximo (3.4). Não interromper por vantagem temporária.

### 2.7 Critérios de escala e pausa (parâmetros; decisão de Bruno)
| Situação | Ação |
|---|---|
| Rastreamento da venda confiável (4.1 passou), amostra mínima atingida, `CPC_campanha <= L − M` (M = margem mínima definida por FINANCE/Bruno), reembolso dentro do limite | escalar em passos de no máximo 20% de orçamento a cada 3 dias [H], sempre `<= T` |
| Amostra incompleta, resultados bons | **não escalar**; esperar a amostra |
| `CPC_campanha > L` com amostra mínima | pausar a campanha (não apagar) |
| Frequência da quente acima do limite | pausar o conjunto, ou ampliar o público (nunca com público frio disfarçado) |
| Reprovação de anúncio ou queda de qualidade da conta | pausar e investigar |
| Venda sem UTM acima de limite `U` (parâmetro) | a campanha não pode ser julgada: corrigir rastreamento primeiro |
Escala nunca por CTR alto, CPC baixo ou pico isolado de ROAS (`02-agentes/traffic.md`).

### 2.8 O que bloqueia a ativação hoje (resumo; checklist completo na seção 5.2)
1. Landing v2 **não publicada** e checkout limpo não conferido no celular.
2. Modelo `clube_plataforma_d0` e fluxo `bc86b069` incoerentes com a oferta (C1 a C3).
3. Purchase não provado no Meta; vendas reais recentes sem UTM [E, HANDOFF]; o clique qualificado e o início de checkout efetivo ainda precisam estar em produção (`09-tracking/FUNIL_DE_EVENTOS_P0.md`).
4. Públicos personalizados não criados; base legal e política de privacidade a confirmar (6.1).
5. Orçamento: `G1 + G2q + G2f <= T` e valor de `T` e de `K`/`M` definidos por Bruno.
6. Criativos de atração no ar: verificar coerência (2.1).

---

## 3. COMO PROVAR (definido ANTES do teste)

### 3.1 Métricas e fórmulas
Todas por **comprador único** (não por transação), compras **pagas** (Pix pago ou cartão aprovado), sem compras de teste de Bruno e sem equipe.
| Métrica | Fórmula |
|---|---|
| Custo por lead (CPL) | `gasto Etapa 1 ÷ leads novos` (leads novos = contatos criados no ClickMax com a etiqueta de coorte, não formulário abertos) |
| Taxa de lead→compra em 7 e 14 dias | `compradores (pagos até 7 ou 14 dias depois da entrada do lead) ÷ leads da coorte`; 14 dias só lê coortes com 14 dias completos |
| Custo por comprador total (quente) | `CPC_quente = (gasto_atração_atribuído + gasto_venda_quente) ÷ compradores_quente`. `gasto_atração_atribuído = CPL × leads da coorte que entraram no público exposto`. Evita jogar todo o gasto de atração em quem nunca foi à venda |
| Custo por comprador (fria) | `CPC_fria = gasto_venda_fria ÷ compradores_fria` |
| Custo por comprador sem atração (só venda quente) | `gasto_venda_quente ÷ compradores_quente`: mostra quanto da vantagem vem de a atração ser "grátis" |
| Ponto de equilíbrio da taxa lead→compra | `r* = (CPL + gasto_venda_quente ÷ leads expostos) ÷ L`. Se a taxa observada ficar abaixo de `r*`, a etapa não paga |
| Receita líquida | `compradores × L` |
| Margem de contribuição | `receita líquida − gasto total da etapa`; ROAS = `receita ÷ gasto`; faturamento não é lucro |
| Comparação com a venda fria | `CPC_quente ÷ CPC_fria`; diferença de taxa de compra por visitante único da página entre as duas campanhas |
| Reembolso | `reembolsos em 7 dias ÷ compradores`, por grupo; só lê grupos com 7 dias completos após a compra |
| Qualidade do comprador | `% que fez o primeiro acesso à plataforma em 7 dias` e `% que concluiu o Marco Zero` (tabela de membros do ClickMax) por grupo; reembolso; pedido de ajuda |
| Cobertura de atribuição | `% das vendas do período com UTM ou etiqueta de coorte`; se menor que `1 − U`, resultado marcado como não confiável |

### 3.2 Regras de decisão pré-definidas
- **Refuta** (item 1 da seção 1): `CPC_quente >= L − M` ou `CPC_quente >= CPC_fria`, com amostra mínima.
- **Sustenta** H0: `CPC_quente < CPC_fria` e `CPC_quente <= L − M`, taxa lead→compra do exposto **maior** que a do holdout fora do intervalo de confiança (Wilson 95%), cobertura de atribuição aceitável, reembolso e qualidade sem piora.
- **Inconclusivo:** qualquer outro caso, ou amostra mínima não atingida. Dizer assim no relatório.
- Intervalo de Wilson 95% para toda taxa reportada. Para zero compras em `n` leads, o limite superior aproximado é `3 ÷ n` ("regra dos três").

### 3.3 Limites de qualidade (parâmetros)
Reembolso do grupo quente > reembolso do frio + `dq` (parâmetro, ex.: definido por Bruno) com amostra mínima de compradores: refuta por qualidade.

### 3.4 Amostra mínima e tempo (cálculo com parâmetros rotulados; sem taxas inventadas)
Ferramenta: `11-testes-ab/amostra.py` (duas proporções, bicaudal, alfa 5%, poder 80%). A taxa base real **não** está no repositório; use a medida no ClickMax. Cenários **hipotéticos** (saída de `python3 -I amostra.py --base <p> --efeito-relativo <e>`, rodada em 25/11):

| Taxa base `p` (hipotética) | Efeito relativo | n por grupo | compras esperadas no grupo base |
|---|---|---|---|
| 0,5% | +100% | 4.673 | 23,4 |
| 1% | +100% | 2.319 | 23,2 |
| 2% | +100% | 1.141 | 22,8 |
| 3% | +100% | 749 | 22,5 |
| 1% | +50% | 7.750 | 77,5 |
| 2% | +50% | 3.826 | 76,5 |

**Consequências honestas [H]:**
1. Para comparar duas **proporções** com efeito de +100% a 2% de base são ~1,1 mil pessoas por grupo. Se a base de leads for da ordem de centenas, **o holdout (grupo de controle dentro dos leads) não alcança poder estatístico**. Com holdout de 15% de uma base de poucas centenas, o grupo de controle terá algumas dezenas de pessoas: serve para **descrever**, não para **provar**.
2. Portanto o plano tem **duas camadas de evidência**:
   - **Confirmatória (campanha quente × campanha fria):** compara custo por comprador entre campanhas. Mínimo para qualquer afirmação: **`Nmin_compradores` compradores por campanha (sugestão: 30, parâmetro de Bruno/FINANCE)**; abaixo disso o custo por comprador tem erro enorme. Tempo estimado: `Nmin ÷ (compradores esperados por dia)`. Sem taxa medida, não há tempo estimável; **dizer que o prazo é desconhecido até haver 7 dias de taxa medida**, e fixar um **prazo máximo** de teste (`D`, parâmetro, sugestão 21 a 28 dias) ao fim do qual o resultado é lido como está (sustenta, refuta ou inconclusivo).
   - **Descritiva (holdout):** reportar a taxa do exposto e do holdout com intervalo de Wilson; só chamar de efeito se os intervalos não se sobrepuserem.
3. O tamanho do público quente limita o gasto útil. Se o Meta mostrar "público pequeno" ou frequência acima do limite, **a venda quente satura antes de dar amostra**; nesse caso o resultado é "público quente insuficiente para provar", não "venda quente falhou".
4. O volume de leads novos de atração por dia define quanto o público quente cresce. Medir **leads novos por dia nos primeiros 7 dias** antes de fixar `G2q`.

### 3.5 Grupo de controle viável
- **Holdout aleatório (preferido) [H]:** dentro de cada coorte de leads, separar **10 a 20%** (parâmetro `h`) por regra reprodutível (por exemplo, último dígito do identificador do contato; **não** escolher a mão) e **excluir esses leads da campanha quente**. Eles continuam recebendo o fluxo orgânico (se existir). Compara taxa lead→compra exposto × holdout.
  - Viabilidade: só se `h × base` der grupo útil; se for pequeno demais, usar só como descrição (3.4).
  - Execução: a lista de exclusão é criada por quem Bruno designar (ChatGPT/Bruno); este plano não escreve em nenhum sistema.
- **Coorte por dia ou por semana (alternativa):** leads da semana 1 sem venda quente (só atração) × leads da semana 2 com venda quente. Mais fácil, mas **confunde com sazonalidade, mudança de criativo e dia da semana**; usar só se o holdout for impossível, rotulado como fraco.
- **Controle natural:** a campanha fria é o controle de "o que acontece sem atração" e **não** controle do mecanismo da quente; por isso as duas coisas se leem separadas.
- Não é viável, e não será feito: segmentar por "vontade de comprar" (viés de seleção).

---

## 4. COMO MEDIR SEM DEPENDER DO PIXEL

O ClickMax liga a compra ao lead (e-mail e telefone) e guarda a origem, UTMs e etiquetas. A fonte da verdade da **venda** é o ClickMax; o Meta serve para gasto, alcance e entrega.

### 4.1 Pré-requisitos (aceite antes de ligar a Etapa 2)
- Compra de teste de Bruno por link de anúncio de teste grava `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` e `sck` (`sales_get_utms`). Padrão em `09-tracking/PADRAO_UTM.md`.
- **UTM por campanha:** `utm_campaign=mm47` fixo; `utm_content=<id do criativo>`; incluir **a temperatura** no `utm_content` por sufixo (`-quente`, `-fria`), consistente com o padrão de sufixo de variante. [NC: confirmar com DATA que o sufixo extra não quebra o conciliador.] `sck={{campaign.id}}` já separa as campanhas.
- **Etiqueta de coorte:** cada lead de atração ganha etiqueta por **dia de entrada** e por **campanha de origem** (nova; criação é escrita no ClickMax e depende de "aprovado").

### 4.2 Consultas exatas (somente leitura)
| Objetivo | Chamada |
|---|---|
| Quantos leads por etiqueta | `tags_list` (campo `leadsCount`) ou `tags_get(tagId)` |
| Leads da coorte (por etiqueta e data) | `segments_preview_count` com `tagId = <coorte>` e `createdAt` (`greaterThanOrEqual`/`lessThan`); para listar, `leads_search` com os mesmos filtros |
| Quantos da coorte compraram | `segments_preview_count` com `tagId` **AND** `numberOfPurchases >= 1` (e/ou `lastPurchaseDate`, `productId`, `offerId`, `transactionStatus`) |
| Compraram a MM47 especificamente | filtro `offerId = 0c71eeba-2654-432c-9701-0a31e6113a08` ou `productId = cbbb5fb1-550f-4a8d-b269-5122c17b7780` |
| Origem e UTM do lead | `leads_search` com `utmSource`, `utmCampaign`, `utmContent`, `src`, `sck`; `leads_get(leadId)` para o detalhe |
| Compras de um lead | `leads_payments(leadId)` |
| UTM da **venda** | `sales_get_utms(saleId)` (ids vêm de `sales_get_details` ou `transactions_list`) |
| Detalhe da venda | `sales_get_details`, `transactions_get` |
| Série diária de vendas | `transactions_chart`, `analytics_sales_metrics`, `analytics_sales_pages` |
| Visitante → lead → compra | `visitors_attribution`, `visitors_lead_journey`, `visitors_conversion_funnel` |
| Acesso e progresso do aluno | `member_users_get_by_lead`, `member_users_get_progress_by_lead` |
| Reembolso | `transactions_list` (status de reembolso; é lista completa sem paginação: usar com cuidado) |
| Exportar para análise externa | `leads_export_csv` (dados pessoais: **não** gravar no repositório) |
| Engajamento do formulário | `forms_analytics` (formulários do ClickMax); formulário do Meta: só no Gerenciador |

**Cruzamento:** `compra × lead × etiqueta`: para cada comprador pago, ver se o lead tem a etiqueta de coorte e a data de entrada **antes** da compra; separar `entrou antes da campanha quente`, `entrou depois`, `sem etiqueta` (fria ou orgânico).

### 4.3 O que conferir em cada leitura
1. Venda com UTM da campanha fria **e** lead com etiqueta de atração: sobreposição (atribuir pela regra: **última** campanha paga com clique, `sck`).
2. Venda sem UTM e lead com etiqueta de coorte: atribuir à quente **apenas** se a compra ocorreu dentro da janela e o lead estava no público exposto; marcar como "atribuição por etiqueta".
3. Compras de teste e da equipe fora do cálculo.
4. Data do pagamento versus data da entrada do lead (janela 7 e 14 dias).
5. Reembolso depois da compra: remover da contagem de compradores líquidos.

### 4.4 Limitações (dizer no relatório)
- **E-mail ou telefone diferente do lead:** a compra cria outro contato; o cruzamento por etiqueta **perde** essa venda. Mitigar com `leads_check_duplicates`/`leads_exists_by_email` e telefone; o resíduo é limite inferior da quente.
- **Compra sem UTM:** as vendas reais de 24/11 vieram sem UTM [E, HANDOFF]; sem UTM só dá para atribuir por etiqueta. Cobertura reportada em cada relatório.
- **Formulário do Meta não grava UTM de anúncio no lead** [NC]: a origem do lead pode ser só a etiqueta; **não dá para ligar lead ao criativo** sem etiqueta por campanha.
- **`numberOfPurchases`** pode contar compra não paga ou reembolsada [NC]: confirmar o campo com uma compra de teste e usar `transactionStatus`.
- O filtro de produto devolveu zero compradores da MM47 na leitura de 25/11 [E]; pode ser limitação do filtro ou ausência de vendas dessa oferta [NC]; conferir por `offerId`.
- Cache do Windsor atrasa; hora da leitura anotada.
- Compra por outro dispositivo e janela de visualização: o ClickMax **não** mede visualização de anúncio, só UTM de clique.

### 4.5 Primeiro dado de prova · "os leads existentes já compram?"
Leitura real feita em 25/11 (somente leitura, agregados; números e proporção **fora do repositório**, em `scratchpad/fase03/PLANO_PROVA_REAL.md`). O que dá para dizer aqui, sem número: a base de leads de formulário "inscrição" e "Land Bank" **existe em centenas**, e **quase nenhum desses leads comprou alguma oferta** até agora. Isso é o ponto de partida: eles ainda **não foram abordados pela oferta correta** (seção 2.3), portanto não refuta H0. Também define a escala do teste: com poucas centenas de leads, a prova confirmatória depende das campanhas, não do holdout (3.4).

---

## 5. Aprovação, execução e checklist

### 5.1 O que precisa de "aprovado" de Bruno e quem executa
| # | Ação | Aprova | Executa | Reversão |
|---|---|---|---|---|
| 1 | `T`, `G1`, `G2q`, `G2f`, `K`, `M`, `U`, `h`, `D`, `Nmin_compradores`, `dq` | Bruno | n/a | n/a |
| 2 | Publicar a landing v2 (ou manter `/mini-mentoria`) | Bruno | Bruno ou executor autorizado | despublicar |
| 3 | Aplicar o checkout limpo e conferir no celular | Bruno | Bruno (painel) | restaurar campos |
| 4 | Pausar fluxo `bc86b069`; novo modelo de WhatsApp P0 (aprovação no Meta) | Bruno | Bruno | reativar |
| 5 | Etiquetas de coorte e lista de exclusão/holdout no ClickMax | Bruno | executor designado | apagar etiqueta |
| 6 | Criar públicos no Meta (clientes por lista, engajamento de formulário e vídeo, visitantes) **e as 2 campanhas pausadas** | Bruno | **ChatGPT cria; nascem pausadas** | apagar campanha pausada |
| 7 | **Ativar** campanhas | **Bruno, com "aprovado"** | quem Bruno designar | pausar |
| 8 | Disparar qualquer mensagem aos leads | Bruno | Bruno | n/a |
| 9 | Texto de transição honesta (6.4) | Bruno (e CREATIVE) | Bruno | n/a |
Este agente **não** executa nada em produção.

### 5.2 Checklist pré-lançamento da Etapa 2
**Rastreamento**
- [ ] Compra de teste por link de anúncio grava os 6 campos de UTM na venda (`sales_get_utms`)
- [ ] Clique "QUERO ACESSAR A PLATAFORMA POR R$47" medido como clique qualificado; início de checkout efetivo (não carregamento) em produção; Pix gerado e pagamento aprovado distintos (`09-tracking/FUNIL_DE_EVENTOS_P0.md`)
- [ ] Sufixo de temperatura no `utm_content` aceito pelo conciliador
- [ ] Etiqueta de coorte criada e aplicada aos leads novos
- [ ] Plano de reenvio das vendas sem UTM ao Meta dentro do prazo (hora do pagamento + 7 dias)

**Página**
- [ ] Landing v2 publicada (`lastPublishedAt` preenchido) ou decisão de usar `/mini-mentoria`
- [ ] Todo botão de pagamento com CTA padrão e preço; botões anteriores só rolam
- [ ] Teste no celular

**Checkout**
- [ ] Nome igual ao anúncio e à página; resumo dos entregáveis; R$ 47; pagamento único; Pix e cartão; garantia 7 dias
- [ ] Sem cronômetro, sem formulário de captação antes da compra

**Entrega**
- [ ] Pagamento → confirmação → obrigado coerente (sem R$ 97, R$ 270, reunião) → e-mail de acesso → login → plataforma (`05-funis/JORNADA_ENTREGA_MM47.md`)
- [ ] Todo material anunciado existe (`08-checkouts/ENTREGAVEIS_VERIFICADOS.md`)

**Públicos e campanhas**
- [ ] Exclusões: compradores, leads de outras linhas, equipe, holdout; sobreposição A × B zero
- [ ] Tamanho do público quente suficiente para entrega (o Meta exige mínimo de pessoas correspondidas)
- [ ] Campanhas pausadas; soma dos orçamentos `<= T`; Audience Network desligado; "Saiba mais"
- [ ] Criativos de atração conferidos (2.1) e fluxo `bc86b069` tratado (2.3)

### 5.3 O que ainda bloqueia
Itens 1 a 6 da seção 2.8. Enquanto isso, **nada de ligar a Etapa 2**. A Etapa 1 pode continuar, desde que a transição (2.3) deixe de prometer o que não existe.

### 5.4 Cuidado com a mistura de variáveis
O teste A/B de landing (`TESTE_AB_LANDING_MM47.md`) e este plano **não devem rodar juntos**: duas variáveis (landing e temperatura) invalidam as duas leituras. Este plano usa **uma landing única** nas duas campanhas.

---

## 6. Riscos

### 6.1 LGPD
- Os formulários coletam consentimento para "receber contato da equipe Zion sobre o meu projeto" [E, texto do formulário do ClickMax]. **Usar o dado do lead para formar público personalizado e anunciar para ele é finalidade diferente.** Exige base legal (consentimento específico ou legítimo interesse documentado, com teste de proporcionalidade) e aviso na política de privacidade [BRUNO + jurídico].
- Preferir, na primeira rodada, **públicos de engajamento do próprio Meta** (abriu/enviou formulário, vídeo, visitantes), que não exigem subir lista de contatos.
- Se subir lista de contatos: **só quem aceitou** e **só quem não pediu "Não quero receber"**; dados em hash; exclusão de quem pediu para sair; guardar o registro da base legal. Não subir a base antiga do SDR nem leads de outras linhas.
- Nenhum arquivo do repositório pode conter e-mail, telefone ou nome de lead.

### 6.2 Mínimo de público do Meta e entrega
Públicos personalizados abaixo do mínimo de pessoas correspondidas não entregam. O público quente será pequeno e a taxa de correspondência é menor que 100%; o resultado pode ser "não entrega". Plano: somar públicos de engajamento; se não bastar, **não** completar com frio (contaminaria a comparação).

### 6.3 Sobreposição, canibalização e contaminação
- Quente e fria no mesmo leilão com o mesmo criativo competem entre si: usar exclusões mútuas e criativos diferentes (2.5).
- A venda quente pode canibalizar vendas que aconteceriam organicamente (o lead compraria de qualquer jeito): é o que o holdout mede.
- Leads de atração expostos também à fria por falha de exclusão invalidam a leitura: conferir a sobreposição a cada 3 a 4 dias.
- Frequência alta em público pequeno cansa e pode gerar rejeição.

### 6.4 Quebra de expectativa nos leads que vieram com promessa de consultoria (mensagem de transição honesta)
Quem preencheu formulário vendo "reunião", "diagnóstico", "inscrição" ou "avaliação" não deve receber a oferta como se nada tivesse acontecido. Proposta de texto (sujeita a CREATIVE, Bruno e aprovação do Meta se for modelo de WhatsApp; **não enviar sem "aprovado"**):

> Olá, {{nome}}. Você deixou seus dados em um formulário da Zion. Queremos ser claros sobre o que oferecemos hoje: a Mini Mentoria de Estruturação Zion é uma formação digital, sem reunião e sem atendimento individual. Por R$ 47, em pagamento único, você tem acesso à plataforma digital com 9 módulos e 70 conteúdos para aprender o passo a passo de estruturar o seu projeto. Parcerias e investimentos não fazem parte da compra. Se preferir não receber mais mensagens, é só avisar.

Regras: não prometer reunião, contato de equipe, parceria, investimento ou avaliação; dizer o que mudou; oferecer saída ("Não quero receber"); preço e entregáveis na primeira mensagem.
Medir também a **taxa de saída e de reclamação** como risco de qualidade da conta.

### 6.5 Outros
- **Preço baixo × custo de atração:** com `L` da ordem de R$ 44,51 menos impostos e custos [E, taxa], a conta de atração + venda só fecha se a taxa lead→compra for alta o bastante; é a pergunta que o teste responde. Se `r*` for maior do que o plausível, a etapa de atração para vender a R$ 47 é negativa mesmo com vendas [H].
- **Purchase não provado:** a fase 0 otimiza por visualização, que atrai tráfego de servidor; a decisão não usa a métrica do Meta.
- **Conta e política:** campanhas de leads com promessa imprecisa podem gerar reprovação; atenção ao texto da atração.
- **Reembolso:** garantia de 7 dias; reembolso mais alto na quente pode indicar expectativa não corrigida.
- **Compradores do R$ 97:** manter o acesso (nunca remover); excluir dos públicos de venda.

---

## 7. Resumo para decisão
1. H0 é falseável e tem três formas de refutação (custo, mecanismo, qualidade). Resultado possível: sustenta, refuta ou inconclusivo.
2. Duas campanhas de venda, comparadas no mesmo período: quente (leads e engajamento, exclui compradores) e fria (aberta, exclui compradores e leads); orçamento por parâmetro dentro de `T`.
3. A prova depende do ClickMax (compra × lead × etiqueta), não do pixel; exige etiqueta de coorte e UTM por campanha.
4. Com a base de leads em centenas, o holdout só descreve; a prova real vem da comparação entre campanhas, com `Nmin_compradores` e prazo máximo `D`.
5. Bloqueios principais: landing v2 e checkout limpo, modelo de WhatsApp D0 incoerente (R$ 97), rastreamento de venda, públicos e base legal, parâmetros de orçamento.
