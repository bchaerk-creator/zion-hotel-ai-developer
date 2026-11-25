# HANDOFF Fase 03 · ChatGPT estrutura a campanha de vendas da Mini Mentoria (R$ 47)

Agente: ZION TRAFFIC · 25/11/2026 (leitura Windsor às 05:59Z, cache). **Tudo aqui é PROPOSTA.** Nada foi criado, ligado, pausado ou editado no Meta; nenhuma ação de escrita no Windsor; nada no ClickMax. Este arquivo substitui o `HANDOFF_CHATGPT.md` anterior no que for tráfego; os fatos de produto e entrega continuam valendo.
Sem números reais de gasto, vendas, ROAS ou CAC (repositório público). A versão com os números reais fica fora do repositório. Marcação: **[E]** evidência lida, **[H]** hipótese, **[NC]** não confirmado, **[BRUNO]** só Bruno decide ou executa.

## 0. Regras que valem para quem assumir
- Gastar, ligar, pausar, editar campanha/conjunto/anúncio/público/orçamento: só com "aprovado" de Bruno, e sempre dentro do teto. **Campanhas nascem PAUSADAS.** Disparar mensagem a lead e ativar automação também exigem "aprovado".
- **Teto de teste: R$ 60/dia para a Mini Mentoria**, uma ou duas campanhas [BRUNO confirma se o teto é só da MM47 ou da conta toda; ver pergunta 1].
- Promessa-padrão: "Aprenda o passo a passo…". Sem promessa de renda, ocupação, investimento, parceria ou reunião. Parcerias e investimentos = "possibilidades, sujeitas à análise".
- Não concluir com amostra pequena; não otimizar por evento não provado; não escalar por CTR/CPC/pico de ROAS.
- Nada de senha, token, chave, e-mail, telefone ou nome de comprador/lead em arquivo ou chat.

## 1. Estado de partida (o que está no ar e o que NÃO duplicar)

Leitura Windsor, conta Zion Collection 2 (`1271873041294684`), somente `get_data` [E, cache, defasado]:

| Campanha | Id | Objetivo | Status lido | Orçamento configurado | Observação |
|---|---|---|---|---|---|
| **MM47 criada pelo ChatGPT** | `120250560823800016` | [NC] | **[NC] não apareceu** na leitura (consultada por id, janelas de 25/11 e 7 dias) | [NC] | Provavelmente criada depois do cache ou sem entrega. **O ChatGPT deve ler o estado no Gerenciador antes de qualquer coisa** e preencher a tabela da seção 1.2. |
| **Mini Mentoria [DESENVOLVIMENTO]** | `120250559484620016` | Tráfego (otimiza visualização da página) | **ACTIVE** (conjunto `120250559488770016` ACTIVE) | R$ 30/dia | Só o anúncio 03 PARTICIPAÇÃO (`120250559499010016`) apareceu com entrega; os outros 4 anúncios (01, 02, 04, 05) não aparecem [NC]. Copies antigos (ZC2-MM47-01 a 05) citam "possibilidade de parceria" e "apresentar a investidores": 03, 05 e o cartão 4 são os mais próximos de promessa (auditoria `06-criativos/AUDITORIA_CONTEUDO.md`). |
| Plataforma R$ 97 (venda direta) | `120250538576770016` | Vendas (otimiza início de checkout) | ACTIVE | R$ 50/dia (30 frio + 20 remarketing) | Destino /inscricao-47 (R$ 47) com vídeos "Vendas R$97", reprovados na auditoria; Audience Network consumia a maior parte do gasto [E, auditoria]. Conjunto de remarketing usa os públicos "IG 365 + vídeo + form 90d". |
| Form R$ 47 direto | `120250557420830016` | Leads | ACTIVE | R$ 30/dia | Usa "Vídeo 02 | Form 47", reprovado na auditoria. Lead nativo, outro caminho de conversão. |
| LT47 Parceiro Zion | `120250557994600016` | Vendas | PAUSED | R$ 30/dia | Não reativar (parceria/investidor). |
| Captação R$ 270; Land Bank; Curso Terreno; Urubici | vários | vários | PAUSED | n/a | Não reativar para a MM47. |

**Achado de orçamento [E]:** com as três campanhas ativas somam-se R$ 110/dia configurados (30 + 50 + 30), quase o dobro do teto de R$ 60/dia. Mesmo que o teto seja só da MM47, três campanhas de público parecido competem no mesmo leilão.

### 1.1 Recomendação: qual consolidar e qual manter (sem duplicar)
1. **Uma única campanha da MM47.** Ficar com a criada pelo ChatGPT (`120250560823800016`), **se** ela passar na conferência abaixo; se não passar, corrigir ela (com "aprovado") em vez de criar uma terceira. Nunca criar campanha nova enquanto houver uma MM47 não aproveitada.
2. **Conferência da `120250560823800016` (preencher e devolver a Bruno):** nasceu/está pausada? orçamento total ≤ R$ 60/dia? destino `/mini-mentoria` (sem `#pagar`) com `url_tags` padrão (seção 3)? só os criativos Fase 03 prontos (seção 3)? sem Audience Network? público sem exclusão faltante (seção 2.4)? botão "Saiba mais"? evento de otimização conforme a Fase 0 (seção 2.2)?
3. **`120250559484620016` (Mini Mentoria Tráfego, ativa):** recomendo **pausar** (não apagar) quando a `120250560823800016` estiver conferida e aprovada. Motivos: copies antigos com linguagem de parceria/investidor, 3 de 5 ressalvados, duplica a finalidade, sem UTM completo [NC]. Preservar para histórico e leitura. **Pausar exige "aprovado" de Bruno**, que ligou essa campanha em 25/11: a decisão é dele.
4. **Plataforma R$ 97 e Form R$ 47:** recomendo **pausar** com "aprovado": destino/criativos incompatíveis com a oferta e estouram o teto. Se Bruno quiser manter remarketing, os **públicos** do conjunto de remarketing podem ser reaproveitados na nova campanha, não o anúncio.
5. Resultado desejado: **1 campanha ativa (ou 2 no máximo: prospecção e remarketing separados)** somando ≤ R$ 60/dia.

### 1.2 Tabela a preencher pelo ChatGPT antes de agir (leitura no Gerenciador, sem editar)
| Campo | `120250560823800016` | `120250559484620016` |
|---|---|---|
| Status e orçamento | | |
| Objetivo e evento de otimização | | |
| Conjuntos, públicos, exclusões, posicionamentos | | |
| Anúncios (nome, arte, texto, URL e parâmetros) | | |
| Status de revisão/reprovações | | |

## 2. Estrutura recomendada

### 2.1 Princípio
A estrutura mínima que testa **uma hipótese por vez**: primeiro "qual criativo leva compra qualificada", com o mesmo destino e o mesmo público. Teste de landing A/B só depois (seção 3.4).

### 2.2 Objetivo e evento de otimização (o Purchase ainda não funciona)
Fatos [E, auditoria e `09-tracking/PLANO_EXECUTAVEL.md`]: o Meta registrou 0 compras mesmo com vendas reais; o início de checkout dispara no **carregamento** do iframe (≈ visualização de página); ViewContent desligado; as vendas reais de 24/11 vieram sem UTM; CAPI, dataset e token não são legíveis por MCP.

**Fase 0 · enquanto o Purchase não for provado (R1 a R6 do plano de rastreamento):**
- Objetivo **Tráfego**, otimização por **visualização da página de destino**, ou equivalente. É o único evento que o pixel entrega de forma reconhecível agora. **Não** otimizar por início de checkout (infla), nem por ViewContent (desligado), nem por Purchase (não chega: o Meta não aprenderia).
- Aceitar a limitação: otimizar por visualização atrai cliques baratos e **tráfego de servidor/bot** (cerca de 40% das visitas de 24/11 vieram de infraestrutura, sessão ≤ 3 s [E, auditoria]). Por isso a **decisão nunca usa a métrica do Meta**: usa **Pix gerado e venda paga no ClickMax por UTM** (seção 4).
- Duração curta e limitada a uma amostra definida (seção 5). Não é campanha de escala.

**Fase 1 · depois que Purchase for provado** (R1 a R4: só após pago, valor/moeda corretos, CAPI funcionando, deduplicação; Teste de eventos com Pix de teste de Bruno) **e a UTM estiver gravada em venda real (R5, R6):**
- **Nova campanha** de **Vendas** com evento de conversão **Purchase** (site, pixel `903918118859018`). Não trocar o objetivo da campanha antiga: criar nova, pausada, com os mesmos criativos vencedores.
- **Limite honesto [H]:** no teto de R$ 60/dia e com CPA máximo na casa do líquido, o volume esperado fica em ordem de unidades de compra por dia; o Meta costuma pedir dezenas de eventos por semana por conjunto para sair do aprendizado limitado. Esperar "aprendizado limitado" e **não mexer** no conjunto a cada dia (cada edição reinicia).
- Se, mesmo com Purchase correto, houver pouquíssimas compras: opção intermediária **[H]** é otimizar por um evento de meio de funil **corrigido** (início de checkout só quando o comprador clica ou gera o Pix, a definir com DATA), nunca pelo evento atual de carregamento.
- Uma campanha de e-book de julho, que otimizava Purchase com base própria, vendeu; é referência de método (Purchase + base própria), não de resultado para a MM47 [E, auditoria].

### 2.3 Conjuntos e orçamento (ABO, dentro de R$ 60/dia)
Orçamento por conjunto (controle manual, sem CBO, para ninguém passar do teto) [H, ajustável por Bruno]:

| Conjunto | Público | Orçamento/dia | Anúncios |
|---|---|---|---|
| **A · Prospecção fria** | Brasil, adultos, interesses (2.4), sem os públicos quentes | R$ 45 | Rodada 1: `mm47f3-c03`, `c06`, `c02`, `c09` (4 anúncios) |
| **B · Remarketing quente** | Públicos existentes (2.4), excluídos compradores | R$ 15 | `mm47f3-c08-oferta-47` (oferta direta) |

- Se o público de remarketing for pequeno demais para o Meta entregar (aviso "público pequeno"), **não ligar o B** e usar R$ 60 no A. Não preencher o B com público frio só para gastar.
- Rodada 2 (depois de amostra, seção 5): trocar os anúncios fracos por `c04-ordem-certa` e `c10-obra-ou-estrutura`. Vídeos (C09 jornada do Dossiê, C01 fundador) só quando existirem e Bruno aprovar.
- Um conjunto frio com 4 anúncios **não** distribui igual: o Meta concentra em poucos. Ler **por anúncio**, com cliques e visitas realmente recebidos, não por gasto. Para forçar comparação mais justa, a alternativa é um conjunto por criativo com orçamento igual, mas isso divide R$ 45 em fatias que ficam abaixo do que o leilão entrega bem [H]; preferir 4 anúncios no mesmo conjunto.

### 2.4 Públicos e exclusões
**Conjunto A (frio):**
- País Brasil; idade 25 a 65+ (ajustável, [H]); Advantage+ audience **desligado** na fase de teste para controlar a variável [H].
- Interesses [H, validar disponibilidade no seletor do Meta antes de fixar]: ligados a imóveis/investimento imobiliário, empreendedorismo, turismo rural e hospedagem alternativa. O conjunto antigo copiou comportamentos genéricos ("Frequent international travelers", "Recently Detected iPhone 14 Devices") e o interesse em espanhol "Inversiones inmobiliarias": **não replicar** os comportamentos de aparelho; evitar atributos pessoais (política do Meta).
- **Excluir:** (1) compradores da MM47 e de qualquer oferta da turma (lista de compradores ou público por visita à página de obrigado, seção 7); (2) compradores do R$ 97 legado (mesmo conteúdo); (3) **leads e base da Zion** (listas, "Público Zion 90", "Zion collection 365", "Público vídeo") e quem engajou com as campanhas de outras ofertas (R$ 270, Land Bank, Clube): essas pessoas vão para o conjunto B, não para o frio, para o teste frio ser limpo; (4) visitantes dos últimos 30 dias da página /mini-mentoria (vão para o B).
**Conjunto B (quente):** os públicos existentes acima + visitantes da página MM47 (30 dias) + quem iniciou checkout de verdade (quando o evento for corrigido), **menos** compradores. Conferir sobreposição entre A e B no Meta (ferramenta de sobreposição) antes de ligar.

### 2.5 Posicionamentos
- **Manual**, sem Audience Network, sem Messenger [E, o gasto em Audience Network foi o vazamento principal nas campanhas anteriores].
- As artes são **1080×1350 (4:5)** e o rodapé com condições faz parte da arte: **limitar a Feed do Facebook, Feed do Instagram e Explorar do Instagram**; **desligar Stories e Reels** até existir versão 9:16, para o Meta não cortar o rodapé [H, conferir pré-visualização de cada posicionamento]. O carrossel também em feed.

### 2.6 Atribuição e janela
- Janela padrão do Meta (cliques 7 dias, visualizações 1 dia) para leitura de relatório; **sempre comparar com 1 dia de clique** [H].
- **Fonte da verdade da venda é o ClickMax por UTM** (seção 3.2). O Meta serve para custo, entrega e funil até a página. Divergência esperada enquanto Purchase não for provado: o Meta mostra menos compras que o ClickMax.

## 3. Criativos

### 3.1 Lista pronta (fonte: `docs/ads/mm47-fase03/manifesto.json` e `COPIES.md`; textos principais completos lá)
Todos: botão **Saiba mais**; descrição "Mini Mentoria de Estruturação · R$ 47"; preço na arte e na primeira linha; destino `https://infoprodutos-zion.clickmax.space/mini-mentoria`; nome do anúncio = o `id`. Arquivos em `https://bchaerk-creator.github.io/zion-hotel-ai-developer/ads/mm47-fase03/<arquivo>` (passam a abrir depois do deploy do GitHub Pages; conferir se abrem antes de subir).

| Rodada | id (`utm_content`) | Conceito ECROI | Formato | Headline | Primeira linha |
|---|---|---|---|---|---|
| 1 | `mm47f3-c03-custo-escondido` | E, O · dor específica | imagem 4:5 | Quanto custa deixar tudo pronto? | R$ 47 · Você sabe o preço da cabana. Sabe quanto custa deixar tudo pronto? |
| 1 | `mm47f3-c06-obra-ultimo-passo` | C, R · colapso de crença | imagem 4:5 | Estruture antes de construir | R$ 47 · "Primeiro eu construo, depois eu vejo se dá certo." Começar pela obra é começar pelo último passo. |
| 1 | `mm47f3-c02-plataforma-por-dentro` | I, O · demonstração real | carrossel 5 | Veja por dentro da plataforma | R$ 47 · Veja por dentro da plataforma: capturas reais das telas da Mini Mentoria de Estruturação. |
| 1 | `mm47f3-c09-objecoes` | R, C · quebra de objeções | imagem 4:5 | Quatro perguntas honestas | R$ 47 · É reunião? Preciso de capital? E se eu não gostar? Garante parceria? Respostas diretas. |
| remarketing | `mm47f3-c08-oferta-47` | O, I · oferta direta | imagem 4:5 | Mini Mentoria por R$ 47 | R$ 47 · Mini Mentoria de Estruturação: aprenda o passo a passo para estruturar o seu empreendimento turístico. |
| 2 | `mm47f3-c04-ordem-certa` | O, I · tutorial | carrossel 6 | A ordem certa para estruturar | R$ 47 · A ordem certa para estruturar um empreendimento turístico, em sete pilares. |
| 2 | `mm47f3-c10-obra-ou-estrutura` | R, O · comparação | imagem 4:5 | Obra primeiro ou estrutura primeiro? | R$ 47 · Obra primeiro ou estrutura primeiro? A Mini Mentoria ensina a segunda forma, em sete pilares. |
| depende de Bruno | C09 jornada do Dossiê (vídeo), C01 fundador (vídeo) | | 9:16 | a definir | não existem; ver `ROTEIRO_VSL.md` |

Arquivos: `c03-custo-escondido.png`, `c06-obra-ultimo-passo.png`, `c09-objecoes.png`, `c08-oferta-47.png`, `c10-obra-ou-estrutura.png`; carrosséis `c02-plataforma-1..5.png` e `c04-ordem-certa-1..6.png`. Não editar a arte (o rodapé com condições é parte da peça). Copy completa: copiar da seção do `id` em `COPIES.md`, sem reescrever.

### 3.2 URL de destino com UTM (padrão definitivo, `09-tracking/PLANO_EXECUTAVEL.md` §1.7)
Colar em **Parâmetros de URL** (nível do anúncio); o destino do anúncio é só `https://infoprodutos-zion.clickmax.space/mini-mentoria` (sem `#pagar`: o que vem depois do `#` não repassa a UTM):
```
utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content=<id do criativo>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
```
Colar as macros `{{ad.id}}` etc. exatamente assim (o Meta preenche). **Não** mudar `utm_campaign` entre variantes. **Aceite antes de ligar:** abrir o link de um anúncio de teste, fazer a compra de teste de Bruno e conferir que a venda grava `utm_*` e `sck` (`sales_get_utms`); sem isso, a venda não é atribuível e o CPA é só limite superior.

### 3.3 O que NÃO usar (lista da auditoria `06-criativos/AUDITORIA_CONTEUDO.md`)
- Todos os vídeos "Vendas R$97" 01, 02, remarketing e "Form 47 Vídeo 02": texto de agendar conversa, equipe entra em contato, parceria/investimento; o vídeo-fonte mostra "Land Bank" e "receber investimentos".
- Todas as peças **R$ 270** (vídeos e carrosséis A, B, C): preço e sessão individual com Bruno inexistentes. O carrossel campeão de leads preserva só a **estrutura narrativa**, não a peça.
- Vídeos Parceiro Zion 11/11, Land Bank/Diagnóstico → Reunião, Clube (2 min), Urubici/Floripa, Bubble, e-book "Glamping Lucrativo" (reunião, renda ou outro produto).
- MM47 03 "participação", MM47 05 "parceiro", LT47 03/04/05, o cartão 4 "A Zion pode ser a sua parceira"; MM47 04 (Airbnb) destoa do público. MM47 01/02 e LT47 01/02 só com aprovação expressa de Bruno da frase condicional de parceria.
- Telas `agendar` e `mapa` da plataforma em qualquer peça.
- Qualquer texto de renda, ocupação, faturamento, "garantido", "últimas vagas", preço "de/por", antes/depois, atributo pessoal ("você está endividado"). Preço diferente de R$ 47 (R$ 270, R$ 97 como preço).
- Botão personalizado: o do Meta é de lista fixa; usar **Saiba mais**; a chamada com preço fica na arte e na primeira linha.

### 3.4 Teste A/B de landing (destino por variante)
- **Destino atual: `/mini-mentoria` (no ar)** até Bruno aprovar publicar `/mini-mentoria-a` e `/mini-mentoria-b` (rascunhos `f690b2c4…` e `299947bf…`; plano em `11-testes-ab/TESTE_AB_LANDING_MM47.md`).
- **Não rodar o teste de landing junto do teste de criativo** (duas variáveis). O A/B de landing exige amostras na casa de milhares de visitantes únicos por variante em taxas baixas [E, tabela do plano]: no teto de R$ 60/dia provavelmente **não alcança** em 28 dias; se não alcançar, não rodar por compra e não declarar vencedora.
- Se Bruno aprovar mesmo assim, caminho preferido: divisão 50/50 no ClickMax (teste A/B de funil, uma URL no anúncio). Caminho alternativo: **anúncios separados por variante** com o mesmo criativo:
  - A: `…/mini-mentoria-a?` + parâmetros do 3.2 com `utm_content=<id>-varA`
  - B: `…/mini-mentoria-b?` + parâmetros do 3.2 com `utm_content=<id>-varB`
  - Mantém `utm_term={{ad.id}}` e `sck`. **Divergência a alinhar com DATA/CONVERSION:** o plano A/B cita `utm_term=varA|varB`; aqui a variante vai em `utm_content` para preservar o id do anúncio em `utm_term`. Escolher um dos dois e usar o mesmo nos dois anúncios. O Meta não garante 50/50 entre anúncios: analisar por **visitantes únicos recebidos por variante**.

## 4. Evento de conversão e cadência de leitura
- **Evento de decisão (hoje):** venda **paga** (Pix pago ou cartão aprovado) no ClickMax, atribuída por UTM; compras de teste de Bruno e reembolsadas excluídas. **Evento de acompanhamento:** Pix gerado (`pix_generated`). **Ruído conhecido:** início de checkout (dispara ao carregar), cliques no botão isolados, CTR, tempo na página.
- **Evento de otimização no Meta:** seção 2.2 (visualização da página na Fase 0; Purchase na Fase 1).
- **Cadência:**
  - **Diária (5 min, anotar a hora da leitura; o cache do Windsor atrasa):** gasto × teto; anúncios reprovados ou sem entrega; vendas pagas e Pix gerados no ClickMax por `utm_content`; vendas **sem UTM** (separar como "não atribuível"). Sem decisão de escala/pausa por mérito nesta leitura; só segurança (estouro de teto, reprovação, checkout fora do ar).
  - **A cada 3 a 4 dias:** conferir distribuição de entrega por anúncio, posicionamento (sem Audience Network), % de tráfego de servidor e sobreposição A/B.
  - **Semanal:** relatório de decisão com amostra, CPA contra a faixa do modelo, e proposta a Bruno (formato do agente: mapa, leitura por evento, problemas por prioridade, proposta com risco e reversão).
  - **Conciliação ClickMax × Ticto × Meta** diária enquanto R1 a R6 não passarem (`09-tracking/conciliacao/`); prazo para reenviar as vendas reais de 24/11 ao Meta: **01/12**.

## 5. Critérios de escala, pausa e manutenção (ligados a `08-financeiro/MODELO_FINANCEIRO.md`)
Decisão final **sempre de Bruno**. Valores abaixo são fórmulas e parâmetros; o que depender de dado real é preenchido fora do repositório.

**Referências:** líquido Pix R$ 47 = **R$ 44,51** [E]. `CPA máximo = líquido − custos variáveis − reserva de reembolso (− imposto%·preço)`; hoje, com imposto, custos e reembolso **sem valor definido**, o teto superior é R$ 44,51 (não é lucro). `CPA desejado = CPA máximo × (1 − margem alvo)`, margem alvo 30% [H, Bruno]. `ROAS de equilíbrio = preço ÷ CPA máximo`. `CPA projetado = custo por checkout efetivo ÷ conversão real do checkout` (indisponível enquanto o início de checkout disparar ao carregar). `CPA real = gasto Meta ÷ vendas externas pagas atribuídas por UTM`.

**Amostra mínima (parâmetros do modelo, [H] ajustáveis):** 5 vendas pagas atribuídas **e** 100 checkouts efetivos; para ler criativo por clique, ≥ 100 cliques no link por anúncio. Abaixo disso: **NÃO DECIDIR**, manter o teto, coletar. Duração mínima 7 dias corridos para leitura de criativo (ciclo semanal) [H].

| Situação | Decisão | Regra |
|---|---|---|
| Sem amostra, sem UTM, sem Purchase provado | **MANTER** o teto de R$ 60/dia; corrigir rastreamento | nunca escalar |
| CPA real ≤ CPA desejado, amostra cumprida, R1 a R6 ok, estável em 2 leituras semanais | **ESCALAR em degrau** (proposta: ≤ 20% do orçamento por vez, com intervalo de 3 a 4 dias e "aprovado" a cada degrau) [H] | uma variável por vez; capacidade financeira e entrega confirmadas |
| CPA desejado < CPA real ≤ CPA máximo | **MANTER** | cobre a mídia sem a margem alvo; otimizar criativo, checkout e página |
| CPA real > CPA máximo, amostra cumprida | **PAUSAR** com "aprovado" e corrigir | cada venda perde dinheiro |
| Gasto acumulado ≥ k × CPA máximo com 0 venda externa atribuída | **PROPOR PAUSA ou revisão de rastreamento** | k = 3 sugerido [H]; antes, conferir se o rastreamento está registrando; Bruno decide |
| Falha técnica, reprovação de política, estouro de teto, reembolso fora do aceitável | **PAUSAR por segurança** (com "aprovado" de Bruno, ou aviso imediato) | critério de parada do plano A/B |

Não escalar por CTR alto, CPC baixo ou pico isolado. Escalar também exige: rastreamento confiável, compras reais, margem positiva, conversão do checkout estável, volume adequado, capacidade financeira (protocolo do `02-agentes/traffic.md`).
**Pontos de atenção financeiros [E/NC]:** a taxa fixa de R$ 2,49 pesa mais em ticket baixo; a regra por faixa de preço, a taxa do cartão e o prazo de recebimento são [NC] (extrato da Ticto); compras com cartão podem baixar o líquido real.

## 6. Checklist pré-lançamento (o que ainda bloqueia)
Legenda: OK = evidência lida; BLOQUEIA = impede ligar com gasto; ATENÇÃO = não impede o teste, mas limita a leitura.

| # | Item | Estado | Quem |
|---|---|---|---|
| R1 | Purchase só após pagamento aprovado (Pix gerado ≠ pago) | **BLOQUEIA** a Fase 1; a Fase 0 só roda com a decisão pelo ClickMax | Bruno (Testar eventos + Pix de teste); DATA |
| R2/R3/R4 | Valor/moeda, CAPI funcionando, deduplicação | **BLOQUEIA** a Fase 1 [NC: token e dataset ilegíveis] | Bruno (Gerenciador de Eventos) |
| R5/R6 | UTM e `sck` gravados em venda real (`sales_get_utms`) | **BLOQUEIA** a atribuição: sem isso o CPA é limite superior | Bruno (compra de teste pelo link do anúncio) |
| — | Início de checkout dispara ao carregar; ViewContent desligado | ATENÇÃO (ruído; não otimizar por eles) | DATA/Bruno |
| — | Página `/mini-mentoria` no ar (`be23f04a…`); tela `mapa.jpg` (cita "sócio" e "Land Members") e vídeo ainda na página ao vivo | ATENÇÃO: frase incompatível no ar; corrigir exige "aprovado" | CONVERSION/Bruno |
| — | Checkout Pix e cartão: pagamento Pix da oferta `0c71eeba` e o cartão nunca foram vistos/provados por ferramenta (domínio de pagamento bloqueado no ambiente) | **BLOQUEIA**: antes de gastar, Bruno faz uma compra de teste Pix e confere cartão | Bruno |
| — | Entrega ponta a ponta da oferta `0c71eeba` (portal `3ef7a340`, turma `087479a3`): comprovada só no R$ 97; para a oferta nova **não** provada | **BLOQUEIA** (comprador pago sem acesso = reembolso e reputação) | Bruno (teste) |
| — | Redirecionamento do checkout para a página de obrigado (rascunho `/obrigado-mini-mentoria`, `1a0aed43…`, não ligada) | ATENÇÃO | Bruno (painel) |
| — | Pós-compra, Pix não pago e carrinho abandonado: fluxos em **rascunho**, nada ativo | ATENÇÃO (sem recuperação nem boas-vindas além do acesso) | Bruno aprova ativar |
| — | Bela e Zaya: mensagens incoerentes com a oferta (R$ 97, reunião, R$ 270) | ATENÇÃO: lead que responder recebe promessa errada | Bruno/outro agente (não mexer) |
| — | Vendedor ClickMax "pending" (oferta aprovada, `canSell` true) | ATENÇÃO | Bruno |
| — | Pasta de anúncios no GitHub Pages abre (URLs públicas das artes) | conferir antes de subir | ChatGPT |
| — | Revisão de política do Meta (categoria de oportunidade de negócio/financeira; textos de investidor/parceria) | ATENÇÃO: se pedirem, tratar como infoproduto educacional | ChatGPT/Bruno |
| — | Formulários antigos citam "R$ 350 mil de faturamento por bubble" e rentabilidade [H: ainda em anúncio ativo] | promessa proibida; conferir e pausar | Bruno |
| — | Tráfego de servidor/bot (~40% das visitas num dia) | ATENÇÃO: filtrar na leitura | TRAFFIC/DATA |

**Regra de liberação:** com os itens BLOQUEIA ainda abertos, a campanha pode ser **criada pausada e conferida**, mas **ligar com gasto** só com "aprovado" de Bruno, ciente do que fica sem prova. Sugestão: ligar a Fase 0 apenas depois da compra de teste com UTM gravada e entrega confirmada.

## 7. Compradores da Mini Mentoria: consolidar a base (sem dados pessoais no repositório)
Objetivo: (a) **excluir** compradores de anúncios de venda; (b) formar o **público quente** por critério e (c) preparar **lookalike** futuro. Nenhum arquivo com e-mail, telefone ou nome vai ao Git ou ao chat; trabalhar pelos painéis.

1. **Fonte única: ClickMax.** A tag `MM47 | COMPROU` (`0366905f…`) e a lista/segmento de compradores já são o padrão do fluxo pós-compra (hoje em rascunho). Criar (ClickMax, com "aprovado") um **segmento** "Compradores Mini Mentoria" por produto/oferta paga (`0c71eeba`) **e** um segmento do R$ 97 legado (mesmo conteúdo, 2 compradores externos). Compras de teste de Bruno ficam **fora**, com tag própria `TESTE` [H, nome].
2. **Exclusão por evento (sem dado pessoal):** público personalizado do Meta por **visitantes da página de obrigado** (URL contém `/obrigado-mini-mentoria` e a antiga `/obrigado-plataforma`) quando a página estiver publicada e o checkout redirecionar para ela. Vantagem: automático, sem upload. Limite: só vale se o redirecionamento estiver configurado [BRUNO].
3. **Exclusão por lista:** exportar do ClickMax os compradores pagos e subir como **Lista de clientes** em Gerenciador de Públicos (o Meta faz o hash no envio). Feito por Bruno ou por quem ele designar, direto nos painéis; apagar o arquivo local após o envio. Atualizar a lista a cada nova leva de compradores (semanal enquanto o volume for baixo). Ter consentimento e base legal (LGPD) para esse uso; incluir no aviso de privacidade.
4. **Lookalike futuro:** só com **origem suficiente de compradores reais**. O Meta exige um mínimo de pessoas na origem e recomenda milhares para qualidade [H, conferir na conta]; hoje há muito poucos compradores externos, então **não criar lookalike agora**. Etapas: (1) acumular compradores pagos com Purchase provado; (2) criar origem "compradores MM47" (lista + evento Purchase com valor); (3) lookalike 1% do Brasil; (4) testar contra o frio por interesse, uma variável por vez.
5. **Segmentos de relacionamento** (para e-mail do `RELACIONAMENTO_BASE.md`, não para anúncio): estudando, concluiu, travado, pediu reembolso. **Reembolsados** saem do público de lookalike e da sequência.
6. **Higiene:** deduplicar por e-mail (`leads_check_duplicates`); nunca remover acessos; registrar a data da última atualização de cada público no LOG, sem contagem de pessoas se a contagem identificar alguém.

## 8. Matriz: o que o ChatGPT executa × o que depende de Bruno
| Ação | ChatGPT | Bruno |
|---|---|---|
| Ler campanhas `120250560823800016` e `120250559484620016` no Gerenciador e preencher 1.2 | executa (leitura) | |
| Conferir a `120250560823800016` contra 1.1 e propor correções | executa (proposta) | aprova |
| Criar campanha/conjuntos/anúncios **pausados** conforme seções 2 e 3 | prepara e cria só com "aprovado" | aprova antes |
| Subir artes, textos e URLs com UTM padrão; checar pré-visualização por posicionamento | executa depois de aprovado | |
| Ligar qualquer campanha / gastar | não | **aprovado obrigatório** |
| Pausar `120250559484620016`, Plataforma R$ 97, Form R$ 47 | propõe | **decide e aprova** |
| Mudar orçamento, público, escalar, pausar por critério | propõe com hipótese, risco e reversão | **aprovado** |
| Teste de eventos (Pix de teste), token da CAPI, deduplicação, dataset | orienta passo a passo | **executa no painel** |
| Compra de teste com UTM e conferência de entrega | acompanha a leitura | **executa** |
| Configurar redirecionamento para a obrigado; publicar /mini-mentoria-a/b | não | **aprovado/painel** |
| Segmentos e tags de compradores no ClickMax; listas e públicos no Meta | desenha, orienta | **executa ou designa**; aprova |
| Leitura diária e relatório semanal por UTM (ClickMax × Meta) | executa (leitura) | decide |
| Vídeos novos (C09, C01); depoimento real; frase condicional de parceria | não | **depende de Bruno** |
| Extrato da Ticto (taxas, cartão, prazo); imposto e custos | não | **fornece** |
| Disparar mensagens a leads; ativar automações | não | **aprovado obrigatório** |

## 9. Perguntas de aprovação para Bruno
1. O teto de R$ 60/dia vale **só para a MM47** ou para **toda a conta**? Se for a conta toda, as campanhas Plataforma R$ 97 e Form R$ 47 precisam ser pausadas.
2. Aprova **pausar** a Mini Mentoria Tráfego (`120250559484620016`) depois de a `120250560823800016` ser conferida? E pausar Plataforma R$ 97 e Form R$ 47?
3. Aprova a **Fase 0** (Tráfego por visualização da página) por até 7 a 14 dias e no máximo o gasto-limite da seção 5, **só depois** da compra de teste com UTM gravada e da entrega confirmada? Ou prefere esperar o Purchase provado?
4. Aprova os conjuntos A (R$ 45) e B (R$ 15) e os posicionamentos só de feed?
5. Aprova subir os 4 criativos da rodada 1 e o de remarketing? (Os 5 antigos MM47 ficam fora.)
6. Aprova o A/B de landing agora ou só depois do teste de criativo?
7. Qual margem alvo e quais impostos/custos usar no CPA desejado (hoje 30% [H] e "a definir")?

## 10. Limites desta leitura
- A campanha `120250560823800016` **não foi lida** (Windsor/cache). Estado, orçamento, público e anúncios dela: [NC].
- Leitura da `120250559484620016` limitada a 1 anúncio com entrega; demais anúncios [NC].
- Plano de rastreamento (R1 a R8) pode mudar; usar sempre a versão atual de `09-tracking/PLANO_EXECUTAVEL.md`.
- Políticas do Meta, mínimos de lookalike e exigências de eventos por semana são [H] a conferir na conta. Nada foi executado.
