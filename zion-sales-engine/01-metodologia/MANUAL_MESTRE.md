# MANUAL MESTRE · ZION SALES ENGINE

Versão 1 · 25/11/2026 · Responsável: Bruno Chaerk · Zion Hotel Group International.
Fonte: Comando Mestre ZION SALES ENGINE (25/11/2026), `CLAUDE.md` e a auditoria de 25/11 (`13-relatorios/`).

**Como ler este manual.** Onde o comando trouxe o texto, ele está aqui. Onde o texto detalhado ainda não foi entregue, está escrito **"detalhe a ser fornecido por Bruno"**. Nenhum agente deve preencher esse espaço por suposição. Marcação de evidência: [E] lido, [H] hipótese, [NC] não confirmado.

---

## 1. Missão

Atuar como **engenheiro de vendas digitais**, coordenando os agentes internos do ZION SALES ENGINE para desenhar, medir, testar e otimizar a venda de infoprodutos da Zion Hotel Academy, com decisões por evidência e aprovação final de Bruno.

Os agentes são internos e ficam descritos em `02-agentes/`. Não substituem nem interferem em Bela, Zaya e demais agentes de atendimento.

## 2. Metodologias obrigatórias

Todas devem orientar o trabalho. O conteúdo detalhado de cada uma **não foi entregue**: registra-se nome e papel.

| Metodologia | Papel no motor | Detalhe |
|---|---|---|
| **Low Ticket Raiz** | Base da oferta de entrada: produto de preço baixo, pagamento único, venda direta | Detalhe a ser fornecido por Bruno |
| **ECROI** | Estrutura de persuasão de copy, páginas e criativos: **E**spelhamento → **C**olapso de Crença → **R**econhecimento → **O**rientação → **I**mplementação | Os cinco nomes e a ordem vêm do comando. O significado de cada etapa: detalhe a ser fornecido por Bruno (existe também a skill `ecroi` no ambiente, mas ela não substitui o detalhe de Bruno) |
| **OP3D e Pareto em cascata** | Priorização do que mexer primeiro | Detalhe a ser fornecido por Bruno |
| **Método Zion 360°** | Metodologia da casa que ancora produto e linguagem | Detalhe a ser fornecido por Bruno |
| **Engenharia de Vendas Perpétuas de Resposta Direta** | Sistema de venda contínua, medido e otimizável, sem depender de reunião | Detalhe a ser fornecido por Bruno |

## 3. Os 7 pilares

### 3.1 Funis

- **Funil low ticket (sequência literal):** Anúncio → Landing page → Oferta com preço explícito → Checkout → Pagamento aprovado → Entrega automática → Relacionamento → Oferta complementar quando pertinente e aprovada.
- **Sem formulário de captação obrigatório.**
- **Sem reunião obrigatória.**
- **Não misturar venda direta com captação high ticket.**

### 3.2 Engenharia financeira

Fórmulas do comando:

- **CPA projetado** = custo por início efetivo de checkout ÷ taxa de conversão real do checkout.
- **Custo máximo por checkout** = CPA desejado × taxa de conversão do checkout.

"Início efetivo de checkout" é o início por intenção (ver 3.5), não o evento que dispara no carregamento do checkout (ver seção 8).

Indicadores financeiros a acompanhar. O comando traz uma lista própria, cujo texto literal **deve ser conferido com Bruno**. Os que já aparecem nos relatórios da auditoria e valem como base:

- preço, taxa do gateway e valor líquido por oferta;
- margem de contribuição = líquido − imposto − custos variáveis (imposto e custos sem valor definido ficam "indisponíveis", nunca zero);
- CPA máximo (ponto de equilíbrio por venda) e CAC real (só quando há atribuição);
- custo por visita, por checkout e por Pix gerado;
- resultado de mídia do período (venda líquida − gasto), com cenários rotulados como hipótese.

Faturamento não é lucro. Taxas só entram se comprovadas, com a origem do dado.

### 3.3 Criativos

- **CTA com preço explícito.**
- **Matriz de 10 conceitos criativos.** Os dez conceitos: detalhe a ser fornecido por Bruno.
- Cada criativo 1080×1350 é um anúncio. Todos levam à landing com `utm_source=meta&utm_medium=paid&utm_campaign=<produto>&utm_content=<criativo>`.
- No Meta o botão vem de lista fixa ("Saiba mais"); a chamada personalizada vai na arte e na primeira linha do texto.
- Fotos reais da Zion, sem pessoas; texto não vai por cima da foto quando Bruno pedir foto nítida. Imagem gerada nunca é apresentada como foto real. Imagens de referência de terceiros ou de IA servem só de inspiração.

### 3.4 Inteligência de mercado

Entender público, dor, linguagem, concorrência e oferta antes de mexer. Sem números de mercado inventados: toda afirmação com fonte e data, ou marcada como hipótese.

### 3.5 Dados e rastreamento

**Jornada rastreável (sequência literal):** Impressão → Clique → Visita → Visualização da oferta → Início efetivo de checkout → Informação de pagamento → Pagamento pendente → Pagamento aprovado → Entrega → Reembolso.

Regras de eventos (alinhadas aos requisitos R1 a R8 do plano técnico, `13-relatorios/H_rastreamento.md`):

- **InitiateCheckout:** representa início efetivo, por intenção. Não pode disparar só porque o checkout carregou.
- **Purchase:** só depois do **pagamento aprovado**, com `value` e `currency` corretos.
- **Pix:** Pix gerado não é Pix pago. Pix gerado = informação de pagamento / pagamento pendente; Purchase só quando pago.
- **Deduplicação:** navegador e servidor (API de Conversões) com o mesmo `event_id`.
- **UTM:** persistente até a venda, com campanha, conjunto e anúncio (ids), para atribuir cada venda a um criativo.
- **Conciliação:** vendas do ClickMax × gateway × Meta com diferença de até 10% (critério R7 do plano).

### 3.6 Conversão

Página que explica o que a pessoa compra, o preço e o que recebe logo na primeira dobra, no celular, com CTA claro e checkout que funciona. Uma tag isolada não comprova pagamento nem entrega: verificar o caminho completo, do pagamento confirmado ao acesso.

### 3.7 Otimização e escala

- **Protocolo científico de testes:** hipótese, variável, métrica, duração e critério de decisão registrados antes do teste (`11-testes-ab/`). Detalhe do protocolo: **a ser fornecido por Bruno**.
- **Critérios antes de escalar:** o comando exige critérios; o texto literal **deve ser conferido com Bruno**. Pré-condições já provadas como necessárias pela auditoria:
  1. rastreamento provado (Purchase só após pago, value/currency, deduplicação, UTM com ids);
  2. conciliação dentro do limite do plano;
  3. compra real de teste concluída, com reembolso;
  4. oferta e entrega coerentes com a promessa da página.
- Só depois disso, escalar orçamento, e com "aprovado".

## 4. Governança e autorizações

**Pode, sem pedir "aprovado" a cada vez** (autorização permanente de Bruno, 06/11/2026, `CLAUDE.md`):
- produzir produtos do catálogo, um por vez, e criar produto, oferta e página no ClickMax;
- enviar a oferta para aprovação quando `offers_get_incomplete_reason` voltar vazio;
- publicar página de vendas quando a oferta estiver ativa (aprovada);
- ler dados (ClickMax, Windsor/Meta, GitHub, páginas públicas) e escrever documentação em `zion-sales-engine/`.

**Exige "aprovado" específico de Bruno:**
- gastar com anúncio; ligar, pausar ou alterar campanha, conjunto, anúncio ou orçamento (teto de gasto definido por Bruno; campanhas novas nascem pausadas);
- disparar mensagens para leads;
- ativar automações;
- mexer em qualquer coisa que já existe (produtos, páginas, funis, automações, checkouts, ofertas, pixel, CAPI, integrações, site `docs/`, Clube, Land Bank, Zion Collection);
- compra real de teste e reembolso;
- despublicar, arquivar ou consolidar páginas e ofertas.

**Fluxo:** AUDITOR valida → DIRECTOR consolida → Bruno aprova → execução → registro em `14-historico-alteracoes/LOG.md`.
Depois de toda alteração em produção, registrar. Nunca pedir senha ou credencial no chat; tokens entram só pelo painel, por Bruno.

## 5. Fases 01 a 08

O comando organiza o trabalho em oito fases. **Os nomes e o conteúdo literal das fases 01 a 08 não foram entregues a este documento: detalhe a ser fornecido por Bruno.** Nesse meio-tempo, a ordem de trabalho em vigor vem do plano da auditoria (`RELATORIO_CONSOLIDADO_FASE2.md`, seção 6): medição → correção da configuração de rastreamento → compra real de teste → limpeza de páginas e ofertas → reestruturação de campanhas → análise semanal e escala.

| Fase | Nome | Conteúdo |
|---|---|---|
| 01 | A fornecer | Detalhe a ser fornecido por Bruno |
| 02 | A fornecer | Detalhe a ser fornecido por Bruno |
| 03 | A fornecer | Detalhe a ser fornecido por Bruno |
| 04 | A fornecer | Detalhe a ser fornecido por Bruno |
| 05 | A fornecer | Detalhe a ser fornecido por Bruno |
| 06 | A fornecer | Detalhe a ser fornecido por Bruno |
| 07 | A fornecer | Detalhe a ser fornecido por Bruno |
| 08 | A fornecer | Detalhe a ser fornecido por Bruno |

## 6. Primeira entrega (15 itens)

O comando define uma primeira entrega de 15 itens. **A lista literal não foi entregue a este documento: detalhe a ser fornecido por Bruno.** Esta etapa de 25/11 entregou: estrutura `zion-sales-engine/` (15 pastas), este manual, os 9 agentes (documentação e definições executáveis), relatórios da auditoria sanitizados, log de alterações e especificação do dashboard.

| Item | Descrição | Situação |
|---|---|---|
| 1 a 15 | A fornecer | Detalhe a ser fornecido por Bruno |

## 7. Regras fixas do repositório (`CLAUDE.md`)

- **Sem invenção:** nada de números de mercado, depoimentos, resultados, garantias, preço "de" falso, bônus ou urgência falsa. Exemplos sempre marcados "dados fictícios".
- **Sem promessa** de reservas, ocupação, renda, investimento ou valorização. Promessa-padrão: **"Aprenda o passo a passo para ..."**. Diferenciar o tempo para começar a usar do resultado externo.
- **Teste de verdade** antes de dizer que funciona, mostrando o resultado. Nunca dizer que testou sem ter executado.
- **Dados pessoais e credenciais:** não pedir senha nem credencial no chat; não coletar dado desnecessário.
- **Não mexer no que já existe:** criar tudo novo e separado.
- **Identidade Zion:** preto `#040605`, verde musgo `#1B2117`, creme `#FEF5F0`, areia `#DED6BF`, terra `#8B714E`, dourado champanhe `#C9B37E`; Cormorant (títulos) e Aventa (texto), no ClickMax Cormorant Garamond e Jost; logo oficial em `docs/brand/`, sem criar outro.
- **Fotos reais** da Zion Bubble Glamping, sem apresentar pessoas como clientes ou equipe sem autorização; nunca imagem gerada como foto real.
- **Texto:** português brasileiro simples, voz "nós", pouco texto por tela, botões claros, celular primeiro.
- **Oferta padrão no ClickMax:** pagamento único, Pix e cartão à vista, sem boleto e sem recorrência, reembolso em 7 dias (Código de Defesa do Consumidor).
- **Gasto, mensagem a leads, automação e mexer no existente:** só com "aprovado" de Bruno.
- **Medição:** comparar custo por venda com o preço menos taxas e impostos.

## 8. Regras aprendidas na auditoria de 25/11

Fatos de `13-relatorios/`. Os itens marcados (*) foram informados no comando e não aparecem nos relatórios copiados; confirmar na próxima auditoria.

1. **O gateway é a Ticto, não o Asaas.** O Asaas só aparece em um fluxo rascunho sem execuções. [E]
2. **O evento "iniciou checkout" (`initiate_checkout`) dispara no carregamento do checkout embutido**, sem clique. Acompanha as visitas e não mede intenção. [E]
3. **Script colado em HTML é removido pelo ClickMax**(*): rastreamento não entra por script na página; usar a configuração nativa de pixel/CAPI do ClickMax.
4. **`pages_publish` pode devolver sucesso sem publicar**(*): conferir `lastPublishedAt` e abrir a URL pública depois de publicar.
5. **R$ 47 e R$ 97 entregam o mesmo conteúdo** (mesmo conteúdo, 9 módulos, 70 aulas). O de R$ 97 só ganha uma segunda porta de acesso. Não há diferença real de produto. [E]
6. **Nenhuma campanha otimizava para compra** e o Meta registrou 0 compras contra 2 vendas reais; as vendas vieram sem UTM. Não se atribui venda a anúncio sem UTM e ids. [E]
7. **A campanha otimizada para ViewContent não entregava aprendizado**: o ViewContent está desligado nas páginas. Conferir o evento de otimização antes de ligar. [E]
8. **O ClickMax só enxerga o que a Ticto repassa**: recusa, Pix expirado e abandono ficam invisíveis. Falta extrato do gateway. [E]
9. **Pix gerado × pago se distinguem no ClickMax** (pendente → pago em 51 a 91 segundos); falta garantir o mesmo no Meta. [E]
10. **Cerca de 40% das visitas de um dia eram tráfego de servidor** (sessão de até 3 s); filtrar na análise de conversão. [E/H]
11. **Audience Network concentrou a maior parte do gasto dos melhores vídeos**, com CPM muito alto; excluir nas campanhas novas (precisa de "aprovado"). [E/H]
12. **Rótulo e destino precisam bater:** a campanha rotulada "R$ 97" levava a página de R$ 47. Um preço, um nome, uma entrega por campanha. [E]
13. **Promessas que a oferta não entrega** (reunião, "entrará em contato", "receber investimentos", "parceiro/sócio") devem sair de anúncios e páginas. [E]
14. **O hash do checkout deve bater com a oferta** da página (conferido em 27 de 27 páginas publicadas com iframe). Conferir sempre. [E]
15. **Páginas ligadas a oferta arquivada ou com preço obsoleto não vendem** e podem estar recebendo tráfego: auditar o vínculo página → oferta. [E]
16. **Ofertas com erro de sincronização do gateway** (17 em 25/11, nenhuma ligada a página publicada) não devem receber página até resolver. [E]
17. **Pós-compra em rascunho:** compradores recebem o acesso, mas sem e-mail, tag, card ou tarefa; ativar só com "aprovado" e depois de testar. [E]
18. **Mensagens incoerentes entre si** (abertura, Bela, Zaya) com preço e promessa diferentes: unificar com a oferta vigente antes de disparar. [E]
19. **Checkout real ficou bloqueado no ambiente de auditoria** (domínio de pagamento retorna 403): campos, Pix na tela e e-mail de acesso exigem teste de Bruno. [E]

## 9. Pendências do próprio manual

Detalhe a ser fornecido por Bruno: texto de Low Ticket Raiz, significado de cada etapa do ECROI, OP3D e Pareto em cascata, Método Zion 360°, Engenharia de Vendas Perpétuas de Resposta Direta; lista literal de indicadores financeiros; os 10 conceitos criativos; protocolo científico de testes; critérios literais antes de escalar; fases 01 a 08; os 15 itens da primeira entrega; perguntas diárias do painel (`12-dashboard/README.md`).
