# Formulário nativo NOVO da captação · textos de tela (RASCUNHO) · ZION CREATIVE · 25/11/2026

**Só texto em arquivo.** Nenhum formulário foi criado no Meta. Formulários do Meta **não são editáveis** (só arquivar): para corrigir, cria-se um novo. Texto jurídico em linguagem simples, **a validar por advogado** (LGPD, consentimento e política). Alinhado aos blocos 4.1 e 4.2 de `10-trafego/LGPD_BASE_LEGAL_E_PUBLICOS.md` (MARKET); se divergirem, vale o que o advogado aprovar. Referência de campos: leitura do Windsor `facebook_leads` e `get_fields` ([E], 25/11/2026) e o esquema de `create_lead_form` (usado só como referência: ele aceita `questions`, `context_card`, `privacy_policy_url`, `follow_up_action_url`, **não** tem campo de caixa de consentimento).
Limites de caracteres do Meta para introdução e tela final: [NC], conferir no Gerenciador; os textos abaixo são curtos de propósito.

## 1. Dados do formulário
| Campo | Proposta |
|---|---|
| Nome interno | `Captação gratuita · Educação Zion · nov/2026` |
| Tipo | Mais volume (padrão). **Não usar "Maior intenção"** com revisão que sugira pagamento; o cadastro é gratuito |
| Idioma | Português (BR) |
| Política de privacidade | `{URL_POLITICA_PRIVACIDADE}` (pendência M20 de Bruno; **obrigatória**); texto do link: "Política de privacidade da Zion" |
| Destino do botão final | `https://infoprodutos-zion.clickmax.space/mini-mentoria?utm_source=meta&utm_medium=paid&utm_campaign=captacao&utm_content=form-cadastro-gratuito` (página com preço, **não** o checkout) |

## 2. Tela de abertura (introdução)
**Título:** Cadastro gratuito Zion
**Lista (cada item é uma linha curta):**
- Cadastro gratuito, sem obrigação de compra.
- Você recebe conteúdos da Zion para estruturar um projeto turístico.
- Há formações pagas, como a Mini Mentoria Zion (R$ 47). Só compra quem quiser.
- Sem reunião, consultoria ou avaliação do terreno. Sem promessa de investimento.

## 3. Perguntas (mínimas)
| # | Pergunta | Tipo | Por que existe | Por que não pedimos mais |
|---|---|---|---|---|
| 1 | Nome completo | padrão Meta (pré-preenchido) | Identificar o cadastro | n/a |
| 2 | E-mail | padrão Meta | Enviar o conteúdo prometido e, com consentimento, a sequência | n/a |
| 3 | Telefone (WhatsApp) | padrão Meta | **Decisão de Bruno e do advogado.** Só é necessário se a Zion for enviar WhatsApp. Se o WhatsApp **não** for usado, **retirar** este campo (dado desnecessário). Se for usado: o telefone não é consentimento; só recebe WhatsApp quem marcar a caixa 2 | Padrão não pode ser marcado como opcional [NC] |
| 4 | **Qual a sua situação hoje?** | múltipla escolha (uma resposta) | Segmentar o conteúdo | Substitui "localização do terreno" e "objetivo", que induziam avaliação do terreno |
Opções da pergunta 4: "Tenho um terreno em destino turístico" · "Tenho uma ideia de empreendimento turístico (sem terreno)" · "Já tenho uma hospedagem e quero estruturar melhor" · "Quero aprender sobre o assunto".
**Removidos em relação aos formulários antigos:** localização do terreno (texto livre), "está disposto a pagar taxa de inscrição", "preencher formulários para nos apresentar", capital disponível, documentação, parceria, aporte, garantia de crédito, valor da área. Nenhum deles é necessário para um cadastro de educação, e vários sugerem análise de viabilidade, parceria ou investimento.

## 4. Consentimentos (DOIS, separados, caixa desmarcada, **não obrigatórios** para concluir o cadastro)
O Meta permite "aviso personalizado" com caixas de seleção; marcar cada caixa como **não obrigatória** é [NC] (testar no Gerenciador). Se não for possível, coletar as duas caixas na página de agradecimento ou no primeiro e-mail e tratar o lead como "cadastro gratuito, sem consentimento comercial" até lá (ver `MARKET`, 4.1).

**Caixa 1 · Comunicação comercial (e-mail e WhatsApp)**
> ☐ Quero receber conteúdos e ofertas da Zion por **e-mail** e por **WhatsApp**, como a Mini Mentoria de Estruturação Zion (R$ 47). Opcional: o cadastro gratuito vale sem marcar. Posso sair quando quiser: link de saída nos e-mails e resposta "Não quero receber" no WhatsApp.
(Se o Meta permitir mais de uma caixa de comunicação, separar em duas, uma por canal; consentimento é por canal.)

**Caixa 2 · Personalização de publicidade**
> ☐ Autorizo a Zion a usar meu e-mail e telefone, em formato protegido (hash), para criar públicos de anúncio no Facebook e no Instagram: para me mostrar anúncios da Zion e para não me mostrar anúncio de um produto que eu já comprei. Opcional e **separado** do cadastro. Esse uso envolve compartilhar dados protegidos com o Meta. Posso retirar a autorização pelo e-mail de suporte da Zion.

**Texto explicativo curto (abaixo das caixas, junto do link de privacidade):**
> Controlador: {RAZAO_SOCIAL_E_CNPJ_ZION}. Usamos seus dados para (a) enviar o conteúdo do cadastro gratuito e (b) só se você marcar as caixas acima, mensagens comerciais e públicos de anúncio. Você pode pedir acesso, correção ou exclusão dos dados e retirar qualquer autorização em {EMAIL_SUPORTE_DOMINIO_ZION}. Política de privacidade: {URL_POLITICA_PRIVACIDADE}.
Pendências de Bruno: razão social, CNPJ, URL da política (M20) e e-mail de suporte de domínio da empresa (hoje é e-mail pessoal) [NC].

## 5. Tela de conclusão
**Título:** Cadastro feito. Obrigado!
**Descrição:** Você vai receber os primeiros conteúdos da Zion. O cadastro foi gratuito e não obriga a nenhuma compra. Se quiser conhecer a Mini Mentoria de Estruturação Zion (R$ 47, pagamento único), veja a página com o conteúdo e o preço.
**Botão:** Ver a Mini Mentoria  → URL do quadro 1.
Cuidados: não escrever "nossa equipe entrará em contato", "vamos agendar" nem "avaliaremos seu terreno"; o botão leva à página de venda com preço, **não** ao pagamento.

## 6. Checagem
| Pergunta | Resposta |
|---|---|
| O cadastro diz que é gratuito? | Sim: introdução, conclusão e consentimento |
| Diz que há formação paga e o preço? | Sim: Mini Mentoria R$ 47 na introdução e na conclusão |
| Há promessa de reunião, consultoria, avaliação, investimento ou parceria? | Não; há negação explícita |
| Dado desnecessário? | Retirados localização, capital, documentação e parceria; telefone depende da decisão do item 3 |
| Consentimentos separados e opcionais? | Sim (2 caixas); formato exato [NC] no Meta |
| Quem recebe WhatsApp? | Só quem marcar a caixa 1 e se o telefone for coletado |
