# Estrutura nova de campanhas · Zion Collection · versão WhatsApp + venda direta

ZION TRAFFIC · 25/11/2026 · **PROPOSTA para aprovação de Bruno. Nada foi criado, ligado, pausado ou alterado no Meta (Windsor só leitura; nenhum `execute_action`).** Repositório público: sem gasto, vendas ou resultados reais; valores em R$ são **parâmetros** [H].
Marcação: **[E]** evidência, **[H]** hipótese/parâmetro, **[NC]** não confirmado, **[APROVAÇÃO]** só Bruno decide.
Decisão de Bruno (25/11): PARAR TUDO na Zion Collection (nenhuma campanha ativa) e reestruturar: (A) Vídeos 01 e 02 = só **entrada** de leads por **WhatsApp direto**; (B) **todos os carrosséis = venda direta** (quente e fria) com landing v2 e checkout limpo; (C) Bruno grava vídeos novos de venda hoje.
Substitui, no que for conflitante, a estrutura "captação por formulário + venda quente + venda fria" de `PLANO_PROVA_FUNIL_DUAS_ETAPAS.md` e `HANDOFF_CHATGPT_FASE03.md` (que permanecem como histórico). Processo comercial: `../05-funis/VENDA_NO_WHATSAPP.md`; CRM: `../05-funis/CRM_WHATSAPP_ENTRADA.md`.

## 0. Estado de leitura [E, Windsor facebook, 25/11]
- Conta Zion Collection 2: na leitura de conjuntos (30 dias), **todos os conjuntos aparecem pausados** (PAUSED ou CAMPAIGN_PAUSED), inclusive os da captação "inscrição" e do "Form R$47 direto". Coerente com a decisão de parar tudo. (Cache do Windsor pode atrasar algumas horas [NC]; confirmar no Gerenciador.)
- Existem conjuntos **antigos com destino WhatsApp** (otimização por conversas) na Página da Zion Collection; um deles aponta para um número que **não é** o número conectado ao ClickMax [E]. Detalhe em CRM §4.
- Pixel do site `903918118859018` (promovido em conjuntos de compra); o Purchase ainda não está provado (`../09-tracking/`). [E de auditoria anterior]

## 1. Ordem de implantação (tudo criado PAUSADO; ativar só com "aprovado")
| Ordem | Campanha | Papel | Criativos | Destino | Bloqueios principais |
|---|---|---|---|---|---|
| **C1** | Entrada WhatsApp | gerar conversa qualificável | Vídeos 01 e 02 (narrativa corrigida) | WhatsApp direto, número conectado ao ClickMax | número ↔ Página, boas-vindas, atendimento humano pronto, roteiro de venda |
| **C2** | Venda quente (carrosséis) | vender a quem já interagiu | todos os carrosséis | landing v2 → checkout limpo | landing v2 e checkout publicados, rastreamento, públicos e exclusões |
| **C3** | Venda fria (carrosséis) | vender a público novo | todos os carrosséis | landing v2 → checkout limpo | idem + exclusão de compradores/leads |
| **C4** | Reservada: vídeos novos de venda de Bruno | venda direta em vídeo | vídeos que Bruno gravar hoje | landing v2 → checkout limpo | vídeos prontos e revisados (copy P0), mesma trava de C2/C3 |
Ordem de risco/valor: C3 e C2 dependem de landing e checkout (mais bloqueios); C1 depende de pessoas e número. **Implantar C1 como primeiro teste pequeno**, em paralelo à publicação da landing v2; ativar C2/C3 só quando os bloqueios de §6 estiverem fechados. C4 nasce vazia (criada pausada, sem anúncio) para receber os vídeos.

## 2. C1 · Entrada WhatsApp (Vídeos 01 e 02)
- **Objetivo da campanha:** Engajamento/Mensagens (tipo "conversas"); **destino:** WhatsApp; **otimização:** **conversas iniciadas**. Não otimizar por Purchase nem por lead de formulário.
- **Botão:** "Enviar mensagem" (WhatsApp). **Sem formulário, sem página-ponte** (a ponte perde o `ctwa_clid`; CRM §3).
- **Mensagem pré-preenchida, respostas rápidas e boas-vindas:** `../05-funis/VENDA_NO_WHATSAPP.md` §2. Uma frase por vídeo (identifica o criativo).
- **Narrativa dos vídeos:** corrigida (sem "taxa de inscrição", reunião, parceria, investimento ou "cadastro" como produto); a promessa do anúncio é **conversar** e, na conversa, a formação paga de R$ 47 é apresentada com preço. Revisar fala e legenda (`../06-criativos/CAPTACAO_CORRIGIDA.md`, adaptando: o CTA passa de "cadastro" para "conversar"). [NC: o ZION CREATIVE precisa adaptar o texto do CTA dos vídeos 01/02 para WhatsApp; não alterei.]
- **Posicionamentos:** Instagram Feed, Reels, Stories e Facebook Feed/Reels **(vídeo vertical)**; **sem Audience Network** (consumia a maior parte do gasto em testes anteriores [E de auditoria]) e sem Messenger. Início manual por posicionamento, não Advantage+ de posicionamentos, para controlar o destino.
- **Público:** Brasil 25–65 aberto; **sem interesses** no início (o criativo qualifica); excluir **compradores** (lista de clientes, quando disponível, via painel) e contatos que já conversaram em C1 nos últimos 30 dias (público de engajamento de mensagens, [NC se disponível]). Mesmo desenho de C3, mas **objetivo diferente**.
- **Orçamento:** **PARÂMETRO** (§4). Orçamento por conjunto (ABO) ou por campanha (CBO, 2 vídeos no mesmo conjunto) [H: 1 conjunto, 2 anúncios].
- **Capacidade humana:** definir antes o **máximo de conversas/dia** que a equipe consegue atender em ≤ 5 min; o orçamento nasce dessa capacidade, não o contrário. [Bruno define.]
- **Métricas de leitura:** custo por conversa iniciada, taxa de resposta (`first_reply`), conversa qualificada, venda (CRM §7). Sem CPL de formulário.

## 3. C2 e C3 · Venda direta com carrosséis
- **Objetivo:** Vendas, **evento Purchase** (site, pixel) **quando o Purchase estiver provado**; antes disso, otimização por **visualização da página de destino** e métricas de clique qualificado (CTA com preço), como no handoff anterior. Nunca otimizar por início de checkout atual (dispara no carregamento).
- **Destino:** landing v2 (variante com desejo antes do CTA) → checkout limpo; CTA único "QUERO ACESSAR A PLATAFORMA POR R$47"; preço visível no criativo (carrossel já traz rodapé de condições).
- **C2 · quente:** públicos = engajamento (vídeo 50 %+, perfil/post Instagram 90–365 dias, **conversas iniciadas em C1** [se o Meta permitir esse público: NC]) e **leads elegíveis** da base existente (por base legal e consentimento; `LGPD_BASE_LEGAL_E_PUBLICOS.md`); **excluir compradores**. Sem lookalike agora.
- **C3 · fria:** Brasil aberto (Advantage+ público), 25–65; **excluir**: compradores, leads/contatos de WhatsApp de C1 (para não pagar duas vezes pela mesma pessoa) e público quente de C2. Exclusões só se tecnicamente aplicáveis (§6).
- **Orçamento:** PARÂMETRO (§4). Criativos: todos os carrosséis aprovados (`06-criativos/`), um carrossel por anúncio, sem repetir o mesmo criativo entre C2 e C3 sem anotar.
- **Mensagem do carrossel = promessa do checkout** (cinco respostas alinhadas, regra do AUDITOR).

## 4. Orçamento (PARÂMETRO; a hipótese R$ 30/15/15 precisa ser reconfirmada)
A hipótese anterior (teto R$ 60/dia: captação R$ 30, venda quente R$ 15, venda fria R$ 15) era para **formulário**. Com WhatsApp:
1. **O custo por conversa substitui o CPL**, e o gargalo passa a ser a **capacidade de atendimento** e a **conversa→venda**, não o custo do lead. O orçamento de C1 deve caber na equipe (§2).
2. **Parâmetros (não fixados):** `B_C1`, `B_C2`, `B_C3`, `B_C4` por dia; teto diário `T`; dias `D`; teto total `T × D`. O modelo v3 (`../08-financeiro/modelo_financeiro_v3.xlsx`, aba Funil Híbrido) já aceita parâmetros: acrescentar um caminho "WhatsApp" [NC: não alterei o modelo]. Valor inicial só **depois** que Bruno responder: (a) o teto vale para só Mini Mentoria ou para a conta toda (CLAUDE.md §1: teto atual R$ 0 de anúncio e campanhas só pausadas); (b) o teto diário total; (c) a divisão. **Sem número aprovado, nada é ligado.**
3. Sugestão de **forma** da divisão [H], sem valores: C1 pequena no início (aprendizado de custo por conversa); C2 menor que C3 porque o público quente é pequeno; C4 só ativa quando houver vídeo aprovado. Entre C1 e a venda direta, **comparar custo por comprador** (CPA de caminho) antes de reequilibrar.
4. A soma configurada ativa **não pode passar do teto aprovado**; conjuntos sem anúncio ativo contam como "configurado".

## 5. Teste de 14 dias e protocolo de validação, adaptados
Mantém o protocolo (`PROTOCOLO_VALIDACAO_14_DIAS.md`, apêndice "versão WhatsApp") e troca o caminho A (formulário) pelo caminho **W (WhatsApp)**:
- **Métricas:** custo por conversa iniciada; conversa qualificada; **conversa→venda em 7 e 14 dias**; **CPA por caminho**: W (gasto C1 ÷ compradores atribuídos a conversas), B-quente (C2), B-frio (C3) e C4 à parte; CPA global = investimento total ÷ compradores únicos; tempo até a compra; margem; reembolsos.
- **Coortes por dia de entrada da conversa** (D0 = dia da 1ª mensagem); não comparar conversa nova com antiga.
- **Teto do teste:** `T × 14` (parâmetro); o antigo R$ 840 só vale se Bruno reconfirmar.
- **Início do relógio:** somente após §6 e autorização; compras de teste internas fora da conta.
- **Não declarar vencedor** sem amostra suficiente; conversa→venda tem ruído grande no começo (poucas conversas).

## 6. O que bloqueia a ativação (todos precisam estar OK; registrar no LOG)
1. **Landing v2 publicada** (C2/C3/C4 e link da conversa) e **checkout limpo** (nome do produto igual, resumo, R$ 47, Pix/cartão, 7 dias). [Publicar = APROVAÇÃO.]
2. **Rastreamento** (`../09-tracking/`): eventos distintos (visita, oferta, clique CTA com preço, início efetivo de checkout, Pix gerado, compra aprovada); Purchase só com pagamento aprovado; UTM na venda; compra de teste interna provada.
3. **Base legal e LGPD** (`LGPD_BASE_LEGAL_E_PUBLICOS.md`): consentimentos separados; público quente só de quem pode.
4. **Número(s) de WhatsApp conectado(s) ao Meta/Página** corretos: o número que o anúncio abre é o **conectado ao ClickMax** (CRM §4). **[NC por leitura]** conferir no painel.
5. **Mensagem de boas-vindas, respostas rápidas e mensagem pré-preenchida** criadas no anúncio pelo ChatGPT, **pausadas**, conferidas por Bruno.
6. **Equipe pronta:** quem atende, horário, SLA, roteiro de `VENDA_NO_WHATSAPP.md` e (se aprovado) a Bela nova; Zaya e fluxos conflitantes tratados (§7).
7. **Exclusões e públicos** aplicáveis (§8).
8. **Teste do CRM** (CRM §6): conversa de teste cria contato, registra o clique do anúncio, mostra atribuição; o atendente vê o contato.
9. **Orçamento e teto** confirmados por escrito por Bruno.
10. **Vídeos 01/02 com narrativa corrigida** e CTA adaptado a WhatsApp.

## 7. Conflitos com Bela, Zaya e fluxos existentes quando o lead chega por WhatsApp
Quando alguém clica no anúncio e manda a 1ª mensagem ao número "Zion Collection", o contato nasce no ClickMax e a conversa fica **aberta (janela de 24 h)**. O que já existe e pode responder:
| Item existente [E] | Conflito |
|---|---|
| **Bela** (`a8a076d4`, ativa, SDR inbound, WhatsApp Zion Collection) | atende conversa nova **dizendo R$ 97**, link de `/inscricao` e "a Zion avalia cada caso" → contradiz a oferta R$ 47 e a landing v2 |
| **Zaya** (`db450d9a`, ativa) | promete **reunião gratuita** e "possível parceria ou investimento", "nunca informa preço"; recebe respostas no mesmo número → contradiz a regra de zero reunião/promessa |
| Modelo `clube_plataforma_d0` e fluxo `bc86b069` ("Abertura") | disparado por **lead de formulário**, não por conversa de anúncio; **não** deve disparar para quem chegou por WhatsApp. **[NC]** se existe gatilho "contato criado/ mensagem recebida" em algum fluxo ativo (a leitura de fluxos não devolveu gatilhos de mensagem inbound; os ativos lidos são manuais ou de checkout/etiqueta) |
| Fluxo manual "Club 97 · Nova oportunidade" | disparo manual; só afeta se alguém o rodar sobre o contato novo |
| Pipeline "Funil Zion · Novo lead → Reunião → Venda" (ativo, playbook de reunião/Land Bank) | se o contato novo for jogado nele por automação ou à mão, herda linguagem de reunião |
| Tags/modelos de R$ 97/R$ 270/reunião | ver `../08-checkouts/`/`FUNIL_P0_COERENTE.md`: não usar |
| Lembretes de reunião (link fixo) | não relacionados, mas ativos |
**Efeito prático:** sem tratamento, a **primeira resposta automática da Bela** a um lead de C1 poderia anunciar R$ 97/inscrição, quebrando a coerência. **Mitigação sem alterar nada:** (a) **não ativar C1** até a Bela ser corrigida **ou** (b) operação 100 % humana com atendente ativo na conversa (atendente humano silencia a Bela [E: 8 conversas silenciadas]) [precisa estar ativo **antes** da 1ª mensagem, caso contrário a Bela responde] **ou** (c) desativar Bela/Zaya nesse número [APROVAÇÃO; não executado]. Proposta recomendada: **(a)+(b) na fase de teste e correção da Bela para R$ 47 em seguida**.

## 8. Exclusões e públicos: o que dá por leitura e o que só no Gerenciador
- **Windsor (facebook):** só leitura de campanha/conjunto/anúncio e métricas; **não cria públicos nem lê a lista de exclusão** com segurança [NC]; `execute_action` **não foi usado**. Verificar a exclusão em `adset_targeting` (campo legível) depois que o ChatGPT criar [E: campo existe no conector].
- **Só pelo Gerenciador (ChatGPT/Bruno):** criar público personalizado de clientes (lista de compradores: exige arquivo com dados pessoais, **fora do Git**), de engajamento, de conversas iniciadas; configurar exclusões; vincular número de WhatsApp à Página.

## 9. O que o ChatGPT cria × o que Bruno aprova
| ChatGPT executa (tudo **PAUSADO**) | Bruno aprova ("aprovado") |
|---|---|
| Campanhas C1, C2, C3, C4 (esqueleto), conjuntos, anúncios, textos copiados dos arquivos, mensagem pré-preenchida/boas-vindas/ice breakers | orçamento por campanha e teto; **ativar** cada campanha; qual número de WhatsApp; qual público quente; **publicar** landing v2/checkout; alterar Bela/Zaya; criar tags/pipeline; modelos de WhatsApp; devolver eventos ao Meta |
| Públicos e exclusões no Gerenciador, quando permitido | listas com dados pessoais (Bruno fornece ao painel; nunca no chat/Git) |
| Conferência de nomes/UTM/`url_tags` e relatório de leitura | decisão de pausar/escala após dados |
Nada é ligado sem "aprovado" (CLAUDE.md §1). O que já está pausado **permanece pausado**; não mexer nas campanhas da Zion Bubble.

## 10. [NC]
- Vínculo real número ↔ Página (painel).
- Se o ClickMax mostra o clique do anúncio no contato e em quais campos/MCP.
- Se o Meta permite público de "conversas iniciadas" e anúncio "Enviar mensagem" pré-visualizável para teste.
- Gatilhos de mensagem inbound em fluxos ativos (leitura completa de 93 fluxos não feita).
- Capacidade de atendimento e horário comercial definidos por Bruno.
- Regra vigente de janela/tarifa do Meta para conversa aberta por anúncio.
