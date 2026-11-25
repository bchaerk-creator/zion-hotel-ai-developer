# Funil híbrido (quente e frio) · Mini Mentoria de Estruturação Zion (R$ 47)

Agente: FUNNEL · 25/11/2026 · ordem de Bruno "funil híbrido". Marcação: **[E]** evidência lida agora no ClickMax, **[H]** hipótese, **[NC]** não confirmado.
Nada foi publicado, ativado ou enviado. O que foi criado no ClickMax (segmentos, fluxos, modelos, uma etiqueta) está em `SEGMENTACOES_HIB.md` e `FLUXOS_HIB.md`, com ids e reversão.
Sem dados pessoais, sem gasto real e sem resultado de campanha neste arquivo.

Princípio: clareza antes do clique, desejo antes da oferta, preço antes do checkout, pagamento aprovado antes de contar a venda, entrega fiel à promessa.

## 1. Os dois caminhos

- **A, quente:** anúncio de captação → formulário → CRM → educação → remarketing → landing → checkout → compra → entrega.
- **B, frio:** anúncio de venda direta → landing → checkout → compra → entrega.

Os dois terminam no mesmo produto (oferta `0c71eeba`, checkout `yhyiqUB9OF`) e na mesma entrega (turma `087479a3`). A diferença é só o que a pessoa sabe antes de chegar à landing.

## 2. Caminho A · funil quente, etapa por etapa

| # | Etapa | Contrato de expectativa (o que a pessoa sabe antes) | Sistema | Estado atual | O que falta | Métrica |
|---|---|---|---|---|---|---|
| A1 | Anúncio de captação | Vai se cadastrar **de graça** para receber conteúdo sobre a metodologia Zion e estruturação de projetos turísticos; existem formações **pagas** (inclusive a Mini Mentoria de R$ 47); cadastro não garante reunião, investimento nem parceria | Meta Ads (execução do ChatGPT com aprovação de Bruno) | [E] a campanha de captação "Form inscrição R$270" foi religada com os criativos antigos (estado dito na ordem; não relido aqui). Os leads de 23 a 25/11 vieram de textos que falam em inscrição e R$ 270 [E, utm_campaign do segmento 02] | Criativos e textos corrigidos (arte, legenda, narração), com "cadastro gratuito" e "formações pagas" visíveis; UTM padrão | CPL, CTR, custo por lead qualificado (e-mail válido) |
| A2 | Formulário | Lê, antes de enviar: cadastro gratuito, o que receberá (e-mails de conteúdo), que há formações pagas; consentimentos opcionais **separados** | Formulário nativo do Meta (lead ads) e/ou ClickMax | [E] origem dos leads chega com `utm_medium` `formulario_meta` / `lead_ads`; o campo de origem do ClickMax **não** marca `MetaLeadAds` (0 leads) [E]. [NC] texto atual do formulário e do consentimento | Texto do formulário (propostas de consentimento na seção 6); conferir se o formulário atual condiciona o envio a consentimento opcional | Taxa de conclusão do formulário, % com e-mail válido |
| A3 | CRM | Nada novo para a pessoa; o lead entra com origem, campanha e criativo registrados | ClickMax (lead + UTM + etiqueta de entrada) | [E] etiqueta `INSCRIÇÃO 270 \| LEAD DO FORMULÁRIO` aplicada ao lead novo; 80 leads com ela; UTM gravada nos leads (campanha, criativo) [E]. Segmentos `[HIB]` criados (ver `SEGMENTACOES_HIB.md`) | Etiqueta nova `HIB \| EDUCAÇÃO · INÍCIO` (criada, sem uso) aplicada na entrada do lead de captação corrigida; reconciliação lead × comprador por e-mail normalizado | Leads por origem, campanha, criativo e coorte |
| A4 | Educação | Recebe 4 e-mails curtos em 7 dias; sabe que o cadastro é gratuito e que a formação paga é opcional | ClickMax, fluxo `[RASCUNHO] HIB · Educação do funil quente` | [E] rascunho com 4 e-mails e atrasos de 48 h, 48 h e 72 h, `flows_validate` válido; 0 execuções | Aprovação de Bruno; condição "já comprou" no editor (a API recusa, ver `FLUXOS_HIB.md` seção 4); link da landing v2 publicada; teste com contato de teste | Abertura e clique por e-mail, descadastro, reclamação, lead → visita à landing |
| A5 | Remarketing | Vê anúncio da Mini Mentoria **só** se é lead elegível e não comprou; o anúncio diz preço e o que é | Meta (público personalizado a partir do segmento `[HIB] 14`) | [E] segmento `[HIB] 14` existe (lead sem comprador). [NC] se o Windsor cria público personalizado (leitura/escrita de públicos não testada); consentimento de personalização de anúncio [NC] | Base legal e texto de consentimento de publicidade (seção 6); subir o público pelo Gerenciador de Anúncios (e excluir `[HIB] 13`); campanha de venda quente criada **pausada** | Custo por visita qualificada, CPA quente |
| A6 | Landing v2 | Entende o produto, vê a plataforma por dentro, o preço (R$ 47), o que não está incluso | ClickMax, variante B v2 (rascunho, com construção de desejo antes do CTA) | [E] duas variantes v2 em rascunho (ids no LOG do CONVERSION); `/mini-mentoria` no ar ainda é a versão antiga. [NC] qual id é a variante B | Publicar a v2 com "aprovado"; botões "QUERO ACESSAR A PLATAFORMA POR R$47"; eventos separados (visita, oferta, clique com preço) | Visita → clique qualificado → checkout efetivo |
| A7 | Checkout | Vê o nome do produto igual ao anúncio e à página, R$ 47, pagamento único, Pix e cartão, garantia de 7 dias | Checkout nativo ClickMax (Ticto), embutido | [E] oferta `approved`; `initiate_checkout` dispara no carregamento do iframe [E, fatos-chave]. Checkout nunca visto daqui (domínio bloqueado) | Checkout limpo (CONVERSION); evento de início efetivo | Checkout efetivo → Pix gerado → pago |
| A8 | Compra | Pagou R$ 47 uma vez; sabe que receberá e-mail de acesso | Ticto → ClickMax (`checkout.transaction.paid.v1`) | [E] 0 compras da oferta `0c71eeba` até 25/11 (segmento 11 vazio). Fluxo Pós-compra em rascunho | Compra de teste de Bruno; ligar Pós-compra (aprovado) | Compras aprovadas, tempo até a compra desde o cadastro |
| A9 | Entrega | Recebe e-mail de acesso, entra com o e-mail da compra, vê por onde começar | Portal `zion-plataforma`, turma `087479a3` | [E] entrega ligada. Onboarding **incoerente** com a oferta (vídeo com "Land Bank", lição que manda "enviar à Zion"); texto novo em `ONBOARDING_PROPOSTO.md` | Aprovação para trocar o texto; regravar a aula 1; teste ponta a ponta | % que entra em 24 h, uso do Dossiê, reembolso |

## 3. Caminho B · funil frio, etapa por etapa

| # | Etapa | Contrato de expectativa | Sistema | Estado atual | O que falta | Métrica |
|---|---|---|---|---|---|---|
| B1 | Anúncio de venda direta | Sabe o nome (Mini Mentoria de Estruturação Zion), que é formação digital autônoma, o preço (R$ 47) e que o clique leva a uma página que explica antes do pagamento | Meta Ads | [E] campanhas de venda (R$ 97 e Mini Mentoria Tráfego) pausadas segundo a ordem; a `Form R$47 direto` é de captação, não de venda direta [H] | Criativos do pacote P0 (CREATIVE) com preço; UTM padrão; destino = landing v2, nunca `/inscricao-47#pagar` | CTR, custo por clique, custo por visita |
| B2 | Landing v2 | Igual a A6 | ClickMax | Igual a A6 | Igual a A6 | Visita → clique qualificado |
| B3 | Checkout | Igual a A7 | ClickMax | Igual a A7 | Igual a A7 | Checkout efetivo → pago |
| B4 | Compra | Igual a A8 | Ticto → ClickMax | Igual a A8 | Igual a A8 | CPA frio, compra sem origem = "não atribuída" |
| B5 | Entrega | Igual a A9 | Portal | Igual a A9 | Igual a A9 | Igual a A9 |

No caminho B não há e-mail de educação: a pessoa é desconhecida até comprar. Quem **abre o checkout e não paga** entra nos fluxos de recuperação (Pix não pago, carrinho abandonado), sempre com a exclusão de compradores.

## 4. Segmentação, exclusão e conciliação (resumo)

- Segmentos `[HIB]` criados no ClickMax (filtros apenas, nada enviado): origem, campanha, criativo, coorte, interesse, visita (proxy), checkout (proxy), pagamento pendente, compra aprovada, reembolso (proxy), exclusão de compradores e "quente elegível". Ids, filtros, contagens e lacunas em `SEGMENTACOES_HIB.md`.
- **Conciliação lead × comprador:** chave = e-mail normalizado (minúsculas, sem espaços). O ClickMax já unifica por contato; se a compra vier com outro e-mail, o comprador aparece como contato novo e o lead antigo continua "quente elegível". Isso **não** é presumido como a mesma pessoa. Regra: tratar como "comprador não atribuído" e listar para revisão manual (telefone só como pista, nunca como prova).
- Atribuição: caminho A se o contato tem a etiqueta/UTM de captação **antes** da primeira compra; caminho B se a primeira UTM é de venda direta; sem UTM = "não atribuída". Nenhuma compra conta nos dois caminhos.

## 5. Conflitos do fluxo atual de abertura (só registro, nada alterado)

| # | O que existe [E] | Por que conflita | Proposta de substituição (precisa de "aprovado") |
|---|---|---|---|
| C1 | Modelo de WhatsApp `clube_plataforma_d0` (aprovado no Meta): diz "O acesso custa R$ 97", fala em cadastrar no banco de áreas e leva o botão para `/inscricao` | Preço errado (R$ 97, a oferta é R$ 47), promete banco de áreas, leva a página que cobra sem explicar | Modelo novo `hib_boas_vindas_d0` (texto proposto abaixo). Modelo de WhatsApp novo exige aprovação do Meta, feita por Bruno; nenhum foi criado ou submetido |
| C2 | Fluxo `bc86b069` "Inscrição 270 · Abertura" (**ativo**): gatilho = etiqueta `INSCRIÇÃO 270 \| LEAD DO FORMULÁRIO`; envia `clube_plataforma_d0`; debounce 30 dias; sem exclusão de compradores | Todo lead novo da captação religada recebe a mensagem do C1 | 1) Pausar `bc86b069` (`flows_close`, reversível) **antes** de a captação receber verba; 2) trocar o gatilho do novo fluxo para a etiqueta `HIB \| EDUCAÇÃO · INÍCIO`; 3) o WhatsApp novo só depois do Meta aprovar o modelo e só para quem autorizou WhatsApp |
| C3 | Fluxos de abertura e lembrete da linha R$ 270 (`Inscrição 270 · Lembrete dia 2`, `Lembrete dia 5`, `Recuperação de pagamento`, `Pagamento confirmado`) | Falam em R$ 270 e agendamento; [NC] o modo atual de cada um (a listagem trouxe versões ativas e pausadas com o mesmo nome) | Ler o modo de cada um antes de ligar a captação; pausar os que estiverem ativos e atingirem o gatilho da captação |
| C4 | Pipeline "Funil Zion": descrição fala em reunião estratégica sem custo e venda de R$ 2.900; etapas de reunião | A venda da Mini Mentoria não tem reunião; o lead da captação cairia num quadro que conduz a reunião | Lead da captação **não** entra no Funil Zion; vive na etiqueta e nos segmentos `[HIB]`; comprador vai ao quadro Alunos Zion (`AUTOMACOES_MM47.md`). Alterar a descrição do pipeline só com "aprovado" |
| C5 | Fluxo `a90448b6` "Club · Lead do formulário Meta → Zaya abre a conversa (menu) + lembrete em 48h" (ativo) | [NC] se o lead da captação corrigida também recebe a etiqueta que dispara a Zaya; a Zaya abre conversa com menu do Club | Conferir a etiqueta de gatilho antes de religar; não mexer na Zaya (regra da Fase 03) |

**Texto proposto do WhatsApp de substituição** (não criado, não submetido; só para quem autorizou WhatsApp):
> Olá, {{1}}! Recebemos o seu cadastro gratuito na Zion Hotel Group. Ele não tem custo e não garante reunião, investimento nem parceria. Vamos enviar conteúdo sobre como estruturar um empreendimento de hospedagem. A Zion também tem formações pagas, como a Mini Mentoria de Estruturação Zion (R$ 47), mas você só compra se quiser. Posso enviar o primeiro conteúdo?
> Botões: "Pode enviar" · "Agora não"

## 6. Consentimento e LGPD (proposta; base legal a validar com o jurídico, [NC])

Dois textos opcionais, **separados** e **não marcados por padrão**; o cadastro não depende de nenhum deles:
1. Comunicação: "Quero receber e-mails e mensagens da Zion Hotel Group com conteúdo e ofertas de formações."
2. Publicidade: "Autorizo usar meu e-mail para me mostrar anúncios da Zion em redes como Instagram e Facebook."
Segmento `[HIB] 14` não filtra por consentimento hoje (a base ainda não tem o campo de forma confiável [NC]); antes de subir público ao Meta, filtrar por quem marcou o texto 2 e antes de enviar e-mail em massa, por quem marcou o texto 1 (campo `messagePreferencesAuthorized` do ClickMax existe para canais; para publicidade é preciso criar campo próprio).

## 7. Públicos no Meta: o que se faz onde

- **Pelo Windsor (conector `facebook`):** leitura de campanhas, conjuntos e anúncios; escrita de campanhas pausadas (já usada). [NC] criação de público personalizado e de exclusões: não foi testada nesta sessão, e a regra é nenhuma escrita no Windsor sem aprovação.
- **Só pelo Gerenciador (passo de Bruno ou do ChatGPT com aprovação):** subir o público a partir do segmento `[HIB] 14` (exportar o segmento e enviar lista com e-mail), aplicar a exclusão `[HIB] 13` e a exclusão de leads no conjunto frio, conferir Brasil amplo.

## 8. Financeiro e prova (resumo, números do briefing)

Base R$ 47; líquido Pix R$ 44,51; CPA máximo preliminar R$ 44,51 e desejado até R$ 31,16 (antes dos demais custos: cartão, imposto, reembolso, a confirmar). CPA quente = (captação + venda quente) ÷ compradores do funil quente; CPA frio = venda fria ÷ compradores do frio; CPA global = total ÷ compradores únicos. Medição em coortes de entrada (segmento 06 é a primeira; criar uma por semana). Protocolo de 14 dias e limites em `10-trafego/PLANO_PROVA_FUNIL_DUAS_ETAPAS.md`. Não declarar vencedor com amostra pequena.

## 9. Aprovações pedidas (nada disso foi feito)

1. Pausar `bc86b069` antes de a captação receber verba (reversível: `flows_activate`).
2. Condição "já comprou" nos fluxos de recuperação e de educação, pelo editor (tutorial em `FLUXOS_HIB.md`).
3. Aplicar `ONBOARDING_PROPOSTO.md` na turma (há compradores; acessos não mudam).
4. Ligar educação e recuperação (um fluxo por vez), depois de teste com contato de teste.
5. Modelo de WhatsApp `hib_boas_vindas_d0` para o Meta.
6. Subir público quente e exclusões no Gerenciador.
