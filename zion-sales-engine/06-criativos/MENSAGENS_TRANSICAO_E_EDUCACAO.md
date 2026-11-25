# Mensagem de transição, modelo de WhatsApp substituto e sequência de educação · ZION CREATIVE · 25/11/2026

**SOMENTE TEXTO PARA APROVAÇÃO.** Nenhum modelo foi criado, submetido ao Meta/Gupshup nem enviado; nenhum fluxo foi alterado, ativado ou pausado. Modelo de WhatsApp novo exige aprovação do Meta e "aprovado" de Bruno. Texto jurídico e de consentimento: **a validar por advogado**. Consentimentos: `FORMULARIO_CAPTACAO_TEXTOS.md` e `10-trafego/LGPD_BASE_LEGAL_E_PUBLICOS.md`.

## 1. O problema do modelo atual [E, leitura 25/11/2026, `PLANO_PROVA_REAL`]
`clube_plataforma_d0` (aprovado, categoria utilidade/marketing a conferir, fluxo `bc86b069` ativo, janela de 24 h) abre automaticamente para os leads do formulário "inscrição". O texto diz **"O acesso custa R$ 97"**, fala em cadastrar a área no **banco de áreas** e leva o botão para `/inscricao`. Contradiz: cadastro gratuito, Mini Mentoria R$ 47 e ausência de banco de áreas. Na leitura, abertura de 57,5% e 1 clique em botão nos 80 leads: o canal funciona, o texto é que está errado. **Não alterei.** Recomendação: **pausar `bc86b069` antes de ligar a captação nova** (decisão de Bruno) e usar o modelo abaixo.

## 2. Modelo de WhatsApp substituto (proposta)
- **Nome sugerido:** `zion_cadastro_gratuito_d0` (minúsculas, sem acento)
- **Categoria:** **Marketing** (apresenta formação paga)
- **Idioma:** pt_BR · **Variável:** `{{1}}` = primeiro nome
- **Para quem:** só quem marcou o consentimento de WhatsApp (caixa 1 do formulário) e informou o telefone. Telefone sem consentimento **não** recebe.
- **Corpo:**
> Olá, {{1}}! Seu cadastro gratuito na Zion foi recebido. Você vai receber conteúdos sobre como estruturar um projeto turístico, sem obrigação de compra.
>
> A Zion também tem formações pagas, como a Mini Mentoria de Estruturação Zion: R$ 47, pagamento único, 12 meses de acesso. Não é reunião nem consultoria, e não garantimos investimento nem parceria.
>
> Quer ver o que vem na formação? Toque no botão abaixo. Se preferir não receber mensagens, toque em "Não quero receber".
- **Rodapé (opcional):** Zion · Mensagem de marketing
- **Botões:** (1) **URL** "Ver a Mini Mentoria" → `https://infoprodutos-zion.clickmax.space/mini-mentoria?utm_source=whatsapp&utm_medium=template&utm_campaign=captacao&utm_content=d0-cadastro-gratuito&src=whatsapp` (página com preço, não o checkout); (2) **Resposta rápida** "Não quero receber".
- **Tratamento do "Não quero receber":** marcar etiqueta de não contatar e cortar WhatsApp e e-mail comercial em até 24 h (prazo interno [H]); só mensagens transacionais de compra seguem.
- **Remove:** R$ 97, banco de áreas, `/inscricao`, "inscreva-se", reunião, equipe, avaliação.
- Conferir no Gupshup: tamanho máximo do corpo e se o botão de URL aceita parâmetros [NC].

## 3. Mensagem de transição para quem já está na base (leads dos formulários antigos)
Quem recebeu `clube_plataforma_d0` ou se cadastrou com a promessa de R$ 270, reunião ou "avaliação" **não** deve receber a sequência nova como se nada tivesse mudado. O texto de transição (e-mail, uma vez, só com "aprovado" de Bruno e revisão jurídica) está em `LGPD_BASE_LEGAL_E_PUBLICOS.md` §4.3 (MARKET) e fica **como está**; aqui só a versão curta para a primeira linha de uma eventual mensagem aos 80 leads de "INSCRIÇÃO 270", **por e-mail e só se não pediram para sair**:
> **Assunto:** O que mudou na Zion
> Olá, {{nome}}. Você deixou seus dados em um formulário da Zion. Queremos ser claros sobre o que fazemos hoje: a Zion oferece formação digital para estruturar projetos turísticos, **sem reunião e sem atendimento individual**. A formação paga Mini Mentoria de Estruturação Zion custa R$ 47, em pagamento único. Você não precisa fazer nada. Se preferir não receber mais mensagens, [clique aqui para sair]({LINK_DESCADASTRO}).
Não enviar por WhatsApp (sem consentimento de canal) nem a leads de outras linhas (Bubble, SDR).

## 4. Sequência curta de educação · 3 e-mails (da captação à Mini Mentoria, sem promessa)
Regras: remetente identificado; link de saída em um clique em todos; e-mail de suporte de domínio da Zion {EMAIL_SUPORTE_DOMINIO_ZION}; no máximo 1 mensagem a cada 3 dias; **E1 vai a todos que se cadastraram** (entrega do que o cadastro prometeu); **E2 e E3 só a quem marcou a caixa 1** (comunicação comercial); parar para quem comprou ou pediu para sair; sem urgência falsa, sem "últimas vagas", sem depoimento ou número de mercado. Exemplos numéricos só com "dados fictícios". UTM de canal (`PADRAO_UTM.md` §5): `utm_source=email&utm_medium=sequencia&utm_campaign=captacao&utm_content=<mensagem>&src=email`.

### E1 · Imediato · "Seu cadastro gratuito na Zion: por onde começar"
> Olá, {{nome}}! Seu cadastro gratuito foi recebido. Não há nada a pagar nem obrigação de compra.
>
> Para você começar hoje, quatro perguntas que organizam qualquer projeto turístico, com ou sem terreno:
> 1. **Onde?** O que existe no entorno: acesso, energia, água, esgoto e o que atrai o visitante.
> 2. **Para quem?** Quem você quer receber e o que essa pessoa procura.
> 3. **O quê?** Qual hospedagem ou experiência cabe no lugar e no seu momento.
> 4. **Quanto custa deixar tudo pronto?** Além da construção: estrada, energia, fossa, projeto, taxas, móveis e enxoval.
> Escreva uma resposta curta para cada uma, mesmo incompleta. Isso já é o começo do seu projeto no papel.
>
> A Zion tem formações pagas, mas você não precisa comprar nada. Se não quiser receber nossos e-mails, [clique aqui]({LINK_DESCADASTRO}).

### E2 · Dia 3 · "Obra primeiro ou estrutura primeiro?"
> Olá, {{nome}}. Muita gente sabe o preço da cabana, mas não sabe quanto custa deixar tudo pronto. Começar pela obra é começar pelo último passo.
>
> Um jeito simples de estruturar antes de construir: liste o que o projeto precisa em cinco grupos, território, mercado, produto, modelo de negócio e conta (orçamento e pré-viabilidade). Para cada grupo, escreva o que você já sabe e o que falta descobrir. O que falta é a sua lista de estudo.
>
> A Zion opera hospedagens em Urubici e Florianópolis e organiza esse passo a passo em formação digital. Na próxima mensagem mostramos como é, com preço e condições.
>
> Para sair, [clique aqui]({LINK_DESCADASTRO}).

### E3 · Dia 6 · "Conheça a Mini Mentoria de Estruturação Zion (R$ 47)"
> Olá, {{nome}}. Como prometemos, aqui está a formação paga, com tudo às claras.
>
> **Mini Mentoria de Estruturação Zion** · formação digital autônoma · **R$ 47, pagamento único**, sem mensalidade · Pix ou cartão à vista · **12 meses de acesso** · 9 módulos, 70 aulas e materiais: aulas gravadas, fichas "Faça agora", e-books por pilar, 2 planilhas de cálculo em branco, Kit do Investidor (modelos), kit de prompts e Dossiê em PDF · **reembolso em até 7 dias**.
>
> **O que não é:** reunião, atendimento individual ou consultoria. Não inclui avaliação do seu terreno nem promete reservas, renda, parceria ou investimento. Você aprende o passo a passo e aplica no seu projeto.
>
> Veja a página com o conteúdo e o preço: https://infoprodutos-zion.clickmax.space/mini-mentoria?utm_source=email&utm_medium=sequencia&utm_campaign=captacao&utm_content=e3-mini47&src=email
> Se não for para você, tudo bem: o cadastro gratuito continua valendo. Para sair, [clique aqui]({LINK_DESCADASTRO}).

Lista de entregáveis conferida com `08-checkouts/ENTREGAVEIS_VERIFICADOS.md`: nada de calculadoras ou simuladores, reunião ou comunidade. Rodapé jurídico completo: `LGPD_BASE_LEGAL_E_PUBLICOS.md` §4.4.

## 5. Dependências
| Item | Quem | Observação |
|---|---|---|
| Aprovar os textos | Bruno | Inclui a frase "formação paga a partir de R$47" (piso [NC]) |
| Revisão jurídica | Advogado | Consentimentos, política, transição |
| Submeter o modelo `zion_cadastro_gratuito_d0` no Gupshup | Bruno/ChatGPT | Meta aprova; só depois substituir o gatilho do fluxo |
| Montar a sequência em rascunho no ClickMax | FUNNEL | Com exclusão de compradores antes de qualquer e-mail de oferta; **não ativar** sem "aprovado" |
| Pausar `bc86b069` e os anúncios antigos | Bruno | Antes de ligar a captação nova |
