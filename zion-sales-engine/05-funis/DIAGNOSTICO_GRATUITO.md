# Diagnóstico gratuito de estágio do projeto · entrada por WhatsApp → Mini Mentoria de Estruturação Zion (R$ 47)

ZION FUNNEL + CREATIVE + DATA · 25/11/2026 · **PROPOSTA para aprovação de Bruno. Nada foi criado, enviado, ativado ou alterado** (nem Bela, Zaya, fluxos, etiquetas, campos, modelos, campanhas, Meta ou ClickMax). Repositório público: só exemplos **fictícios**, sem nomes, telefones, e-mails nem números reais.
Marcação: **[E]** evidência lida, **[H]** hipótese/parâmetro, **[NC]** não confirmado, **[APROVAÇÃO]** exige "aprovado" de Bruno (ou altera algo que já existe).
Código e testes: `diagnostico/score.py` e `diagnostico/tests/test_score.py` (`python3 -I`).

Ideia de Bruno (25/11): **dar valor antes da oferta**. A pessoa entra pelo anúncio (Vídeos 01/02) direto no WhatsApp, sem cobrança, e recebe um **diagnóstico gratuito do estágio do projeto**, com nota e parecer. O parecer mostra, com honestidade, o que já está claro e o que falta, e leva à **Mini Mentoria de Estruturação Zion (R$ 47)**, que já inclui a ficha de Pré-viabilidade e o Dossiê. **Sem produto novo. Sem reunião gratuita.**

Complementa (sem repetir): `VENDA_NO_WHATSAPP.md` (conversa, objeções, janela de 24 h, papéis, pipeline), `CRM_WHATSAPP_ENTRADA.md` (atribuição e medição), `FUNIL_P0_COERENTE.md`, `../08-checkouts/ENTREGAVEIS_VERIFICADOS.md` (o que pode ser dito sobre a entrega), `../09-tracking/PADRAO_UTM.md`.

## 0. Princípios (valem para todo o desenho)
1. **O diagnóstico mede ESTÁGIO DE ESTRUTURAÇÃO das informações enviadas.** Não mede valor do terreno, qualidade do investimento, viabilidade financeira ou jurídica, nem chance de receber investimento ou parceria.
2. **Clareza antes do clique:** o anúncio e a 1ª resposta dizem que o diagnóstico é gratuito **e** que, no fim, mostramos uma formação paga opcional (R$ 47). Ninguém é surpreendido.
3. **A nota nunca decide quem pode comprar nem o preço.** Todas as faixas recebem o mesmo convite, com o mesmo preço. A faixa só muda o que dizemos sobre o que falta.
4. **Linguagem de estágio, nunca de mérito:** "ideia inicial", "primeiros levantamentos", "projeto em montagem", "informações bem organizadas". Nada de "aprovado/reprovado", "bom/ruim", "viável/inviável".
5. **Pouco dado:** 6 perguntas de múltipla escolha. Sem texto livre, sem valor da área, sem capital, sem localização exata, sem documentos, sem CPF.

## 1. Fluxo completo
Anúncio (Vídeo 01/02, botão "Enviar mensagem") → mensagem pré-preenchida → **1ª resposta** (avisos + "Começar") → **6 perguntas** → cálculo da nota (regra fixa) → **parecer** (modelo por faixa) → botões "Quero saber como estruturar" / "Pedir revisão" / "Agora não" → **convite com preço e o que recebe** → link da landing v2 → checkout → compra → entrega.
Desfechos registrados por conversa: diagnóstico entregue · convite visto · clicou na landing · comprou · pediu revisão · pediu para parar · não concluiu.

## 2. O que coletar (6 perguntas, uma por mensagem)
Cada pergunta usa lista ou botões do WhatsApp (até 3 botões, ou lista com até 10 itens [NC: conferir limites no ClickMax/Gupshup]). Resposta é um **código**; texto livre não entra na regra.

| # | Pergunta (texto na conversa) | Opções (código → pontos) | Por que existe |
|---|---|---|---|
| 1 | "Qual é a sua situação hoje?" | `terreno` Tenho um terreno ou área · `ideia` Tenho uma ideia, ainda sem terreno · `hospedagem` Já tenho uma hospedagem e quero ampliar ou estruturar melhor · `aprender` Quero aprender sobre o assunto (sem pontos) | Define quais critérios se aplicam (quem não tem terreno não é penalizado) |
| 2 | "O que você já definiu sobre o empreendimento?" | `nao_definido` Ainda não defini (0) · `varias_ideias` Tenho várias ideias, sem escolha (7) · `tipo_escolhido` Já escolhi o tipo (cabanas, glamping, pousada...) (14) · `conceito_descrito` Tenho o conceito descrito: tipo, público e tamanho (20) | **Clareza do empreendimento** |
| 3 | "O que você já levantou sobre a área?" (só `terreno` e `hospedagem`) | `nada` Nada ainda (0) · `tamanho_localizacao` Só o tamanho e onde fica (7) · `acesso_entorno` Também o acesso e o que existe no entorno (14) · `levantamento_feito` Há medição ou planta da área (20) | **Informações levantadas sobre a área** |
| 4 | "Como estão os documentos da área?" (só `terreno` e `hospedagem`) | `nao_sei` Não sei como estão (0) · `alguns` Tenho alguns documentos (7) · `reunidos` Já reuni os documentos (15). Pergunta de **organização**, não de validade. | **Documentos da área reunidos** (não os analisamos, não pedimos cópia) |
| 5 | "Como estão os números do projeto?" | `nenhum` Nenhum cálculo (0) · `estimativa_de_cabeca` Só estimativa de cabeça (8) · `planilha_parcial` Planilha com parte dos custos ou receitas (17) · `planilha_completa` Planilha com custos e receitas (25) | **Números do projeto** |
| 6 | "Você tem algo para mostrar o projeto a outras pessoas?" | `nada` Nada (0) · `anotacoes_soltas` Anotações ou fotos soltas (7) · `resumo_simples` Um resumo ou apresentação simples (14) · `material_organizado` Material organizado (20) | **Material para mostrar o projeto** |

**Deliberadamente fora:** valor estimado da área, capital disponível, investimento previsto, localização/cidade, tamanho em m², escritura/matrícula como "sim/não" jurídico, intenção de "buscar sócio", telefone/e-mail na regra. Esses campos existiam em `producao/marketing/scripts/qualificar_leads.py` (branch `claude/marketing-skills`) e medem **perfil comercial do lead**, o que não é o objetivo daqui (ver §3.3).
Dado opcional **fora da regra**: e-mail (só se a pessoa quiser o resumo por e-mail, com consentimento, §6).

## 3. SCORE explicável

### 3.1 Critérios e pesos (total 100)
| Critério | Peso | Aplica-se a |
|---|---|---|
| Clareza do empreendimento | 20 | todos |
| Informações levantadas sobre a área | 20 | `terreno`, `hospedagem` |
| Documentos da área reunidos | 15 | `terreno`, `hospedagem` |
| Números do projeto (custos e receitas) | 25 | todos |
| Material para mostrar o projeto a terceiros | 20 | todos |

**Cálculo:** `nota = round(100 × pontos obtidos ÷ pontos máximos aplicáveis)`. Quem não tem terreno é medido só pelos 3 critérios que se aplicam (máx. 65): ter o máximo neles dá 100, não 65. Por isso "sem terreno" não é "pior".
Por que esses pesos [H]: números pesam mais (25) porque são o que mais separa "ideia" de "projeto"; clareza, área e material pesam igual (20); documentos pesam menos (15) porque medem organização, não validade, e esse é o critério mais próximo do campo jurídico. Os pesos são parâmetros: Bruno pode ajustar em `score.py` (`CRITERIOS`); os testes garantem que somam 100.

### 3.2 Faixas
| Faixa | Nota | Nome (estágio) |
|---|---|---|
| F1 | 0 a 24 | Ideia inicial |
| F2 | 25 a 49 | Primeiros levantamentos |
| F3 | 50 a 74 | Projeto em montagem |
| F4 | 75 a 100 | Informações bem organizadas |
Cortes [H]; revisar com as primeiras 30 conversas para ver se as faixas separam estágios reais (não para "melhorar a conversão").

### 3.3 O que foi reaproveitado de `qualificar_leads.py` e o que foi descartado
| Do script atual (`seg`) | Aqui |
|---|---|
| Soma de pontos por resposta, nota, perfil (A a F) e temperatura (QUENTE/MORNO/FRIO) | **Mantida a ideia** de pontos por resposta e faixas |
| Pontua investimento previsto, valor da área, tamanho, escritura | **Descartado:** mede tamanho do negócio e potencial comercial, não estágio de estruturação |
| Perfis "Pronto para o Land Bank", "Terra estruturável", reunião com o Bruno | **Descartado:** Land Bank e reunião não fazem parte da oferta nem do produto |
| Temperatura (quente/morno/frio) | **Descartada:** vira faixa de estágio; "quente" sugeriria prioridade comercial por patrimônio |
| Mapa de objeções por resposta | **Aproveitado** só em `VENDA_NO_WHATSAPP.md` §6 (respostas sem R$ 270, reunião ou Land Bank) |

### 3.4 Como a pessoa pode ver o cálculo
`explicar()` em `score.py` devolve o texto: pontos por critério, o que ficou fora da conta, a frase de limite e o aviso de revisão. Se a pessoa perguntar "como foi calculado?" (botão no 1º contato e no parecer), enviamos esse texto.

## 4. Pareceres-modelo
Montados de peças fixas (nenhuma frase improvisada por IA): **abertura da faixa** + **o que já está claro** (critérios com ≥ 70 % dos pontos) + **o que ainda falta** (até 2 critérios mais baixos) + **próximo passo** + **onde se trabalha isso na Mini Mentoria** (só itens verificados em `ENTREGAVEIS_VERIFICADOS.md`) + frase de possibilidade + **frase de limite**. `{nome}` é preenchido pelo canal; o módulo nunca recebe nome.
Frase de limite (obrigatória, no fim de todo parecer): *"Este diagnóstico é um retrato do estágio das informações que você nos enviou, não é avaliação do terreno nem promessa de investimento."*
Frase de possibilidade (obrigatória): *"Qualquer parceria ou investimento é uma possibilidade, sujeita à análise de quem avalia o projeto, e este diagnóstico não promete nenhum."*

Exemplos **fictícios** (gerados por `score.py`; "Maria" é fictícia):

**F1 · Ideia inicial · dados fictícios** (terreno, tudo "ainda não"; nota 0)
> Olá, Maria! Vimos que as informações que você tem ainda são muito preliminares. Isso é normal no começo, e é por aí que se começa. O que já está claro: você deu o primeiro passo ao nos contar sobre o seu projeto. O que ainda falta: definir com mais clareza o que será o empreendimento (tipo, público e tamanho); levantar mais informações sobre a área (tamanho, acesso, entorno e o que limita o uso). Antes de apresentar o seu projeto a potenciais parceiros e investidores, recomendamos que você estruture melhor a ideia, o projeto e a área. Fazemos isso passo a passo na Mini Mentoria de Estruturação Zion. Na Mini Mentoria você trabalha isso em: as fichas 'Faça agora' e o Dossiê. Qualquer parceria ou investimento é uma possibilidade, sujeita à análise de quem avalia o projeto, e este diagnóstico não promete nenhum. Este diagnóstico é um retrato do estágio das informações que você nos enviou, não é avaliação do terreno nem promessa de investimento.

**F2 · Primeiros levantamentos · dados fictícios** (terreno, tipo escolhido, números só de cabeça; nota 43)
> Olá, Maria! Vimos que você já fez os primeiros levantamentos, mas ainda faltam informações importantes. O que já está claro: o tipo de empreendimento já está bem definido. O que ainda falta: montar os números do projeto: quanto custa abrir, quanto entra e quanto sobra; levantar mais informações sobre a área (tamanho, acesso, entorno e o que limita o uso). Antes de apresentar o seu projeto a potenciais parceiros e investidores, o caminho é completar o que falta e juntar tudo num só lugar. Fazemos isso passo a passo na Mini Mentoria de Estruturação Zion. Na Mini Mentoria você trabalha isso em: as 2 planilhas em branco e a ficha de Pré-viabilidade (Pilar 6); as fichas 'Faça agora' e o Dossiê. [+ frases de possibilidade e de limite]

**F3 · Projeto em montagem · dados fictícios** (hospedagem existente, só os números parciais; nota 74)
> Olá, Maria! Vimos que o seu projeto já está em montagem: várias peças existem, outras ainda estão soltas. O que já está claro: o tipo de empreendimento já está bem definido; você já levantou boas informações sobre a área; você já reuniu os documentos da área (não os analisamos); você já tem um material para mostrar o projeto. O que ainda falta: montar os números do projeto: quanto custa abrir, quanto entra e quanto sobra. Você já tem boa parte do caminho. Falta amarrar as peças num projeto único. A Mini Mentoria de Estruturação Zion organiza isso nas fichas e no Dossiê. Na Mini Mentoria você trabalha isso em: as 2 planilhas em branco e a ficha de Pré-viabilidade (Pilar 6). [+ possibilidade e limite]

**F4 · Informações bem organizadas · dados fictícios** (tudo no máximo; nota 100)
> Olá, Maria! Vimos que as suas informações já estão bem organizadas. Pode faltar só acabamento. O que já está claro: (os cinco critérios). O que ainda falta: nenhum ponto grande nas perguntas que fizemos. Você pode não precisar de tudo. Se quiser, a Mini Mentoria de Estruturação Zion serve para conferir o que já fez e acertar o formato (Dossiê e Kit do Investidor). A decisão é sua. [+ possibilidade e limite]

**Sem terreno (F1) · dados fictícios:** "...recomendamos que você estruture melhor a ideia e o projeto." (a palavra "área" sai quando não há terreno; coberto por teste).
Honestidade da F4: o convite diz que a pessoa pode não precisar de tudo. Isso reduz venda no curto prazo e protege contra reembolso por expectativa errada.

**Proibido nos pareceres (testado em todas as 1.664 combinações de resposta):** "você receberá investimento", "seremos sócios", "garantimos", "garantido", "reunião", "viabilidade financeira", "viável/inviável", "laudo", "aprovado/reprovado", "valor do seu terreno", "vai render", "retorno garantido".

## 5. O convite à Mini Mentoria (preço e o que recebe **antes** do link)
Enviado só depois que a pessoa toca "Quero saber como estruturar" (ou 2 h depois, se o parecer foi lido e não houve resposta, dentro da janela de 24 h). Complementa `VENDA_NO_WHATSAPP.md` §5; a lista de entregáveis é a verificada.

> Pelo que você nos contou, o próximo passo é completar e juntar as informações do seu projeto num só lugar.
> Para isso existe a **Mini Mentoria de Estruturação Zion**: uma formação digital, gravada, em que você aprende o passo a passo para estruturar o seu projeto e prepará-lo para apresentar a potenciais parceiros e investidores. Ela já inclui a ficha de Pré-viabilidade e o Dossiê do seu projeto.
> **O que você recebe:** acesso à plataforma por 12 meses, 9 módulos, 70 aulas e materiais (aulas gravadas, fichas "Faça agora", e-books por pilar, 2 planilhas de cálculo em branco, modelos do Kit do Investidor, kit com 9 comandos prontos para IA e o Dossiê em PDF).
> **Valor: R$ 47, pagamento único**, Pix ou cartão à vista, sem mensalidade, com garantia de 7 dias.
> É formação autônoma: não é consultoria, não tem reunião nem atendimento individual, e não prometemos investimento nem parceria.
> Veja a plataforma por dentro e, se fizer sentido, finalize pela página: {link da landing v2}

Links: ver §10 (UTM). **Bloqueio:** sem a landing v2 e o checkout limpo publicados, **não enviar link de pagamento** (mesma regra de `VENDA_NO_WHATSAPP.md` §5). O link leva à landing, nunca direto ao checkout.

## 6. Sequência de 5 toques (tom de conversa, 1 ideia por toque)
Regra de canal: **WhatsApp só dentro da janela de 24 h** da última mensagem da pessoa (texto livre). Fora da janela, só modelo aprovado pelo Meta **e** com consentimento [APROVAÇÃO; não criado]. **E-mail só para quem informou o e-mail e marcou o consentimento** (caixa separada, desmarcada). Um único lembrete de WhatsApp por conversa (regra §7 de `VENDA_NO_WHATSAPP.md`). Quem compra sai da sequência; quem diz "pare/sair" sai de tudo na hora.

| Toque | Quando | Canal | Conteúdo |
|---|---|---|---|
| T1 | Ao fim das 6 perguntas | WhatsApp (janela) | Parecer da faixa (§4) + 3 botões: "Quero saber como estruturar" · "Pedir revisão" · "Agora não". Em seguida, **pergunta opcional**: "Quer receber o resumo por e-mail? Se sim, envie o e-mail. Só enviamos conteúdo se você marcar que aceita: [ ] e-mail." |
| T2 | Ao tocar o botão (ou 2 h depois, se leu e não respondeu) | WhatsApp (janela) | Convite com preço e o que recebe (§5) + link da landing v2 |
| T3 | ≈ 20 h depois do T2 **e só se a janela ainda estiver aberta e a pessoa não comprou nem pediu para parar** | WhatsApp (janela) | Lembrete curto e útil (texto abaixo) |
| T4 | Dia 2 | E-mail (só com consentimento) | Resumo do diagnóstico + o que a Mini Mentoria tem e **o que não tem** |
| T5 | Dia 5 | E-mail (só com consentimento) | Perguntas frequentes e fechamento, sem pressão |
Depois do T5 a sequência **termina**. Nova mensagem só com nova decisão e novo consentimento. Quem ficou no cadastro de e-mail pode entrar no fluxo de educação já em rascunho (`FLUXOS_HIB.md`, 4 e-mails) **só se o consentimento comercial cobrir isso**; o T4/T5 não duplicam esses e-mails (T4 usa o resumo do diagnóstico; T5 é o FAQ).

**T3 · lembrete (WhatsApp)**
> Oi, {nome}! Só um lembrete curto, sem pressa. No seu diagnóstico, o ponto que mais pede atenção é: {prioridade_1}. É esse o ponto que a Mini Mentoria ajuda a organizar ({onde}). Se ficou alguma dúvida, é só responder aqui. Se não for o momento, tudo bem.
(`{prioridade_1}` e `{onde}` vêm de `FALTA`/`ONDE` do `score.py`; sem desconto, sem prazo, sem escassez.)

**T4 · e-mail dia 2** · assunto: `O resumo do seu diagnóstico de estágio`
> Olá, {nome}. Você pediu o resumo do seu diagnóstico gratuito. Em uma frase: o seu projeto está na faixa "{faixa_nome}". Pontos que mais pedem atenção: {prioridades}. Como a nota foi calculada: {link ou texto do explicar()}.
> A Mini Mentoria de Estruturação Zion (R$ 47, pagamento único, 12 meses de acesso, garantia de 7 dias) é uma formação gravada com 9 módulos e 70 aulas e materiais. **Não inclui** reunião, atendimento individual, consultoria nem promessa de investimento ou parceria.
> [QUERO ACESSAR A PLATAFORMA POR R$47] → landing v2
> Este diagnóstico é um retrato do estágio das informações que você nos enviou, não é avaliação do terreno nem promessa de investimento. Para não receber mais e-mails: {link de descadastro}.

**T5 · e-mail dia 5** · assunto: `Dúvidas comuns sobre a Mini Mentoria (e o que ela não faz)`
> Olá, {nome}. Respondemos as dúvidas que mais aparecem: é reunião? (não, é formação gravada); preciso ter capital? (não para estudar; o curso ensina a montar os números); vocês garantem investimento ou parceria? (não); e se eu não gostar? (reembolso em até 7 dias). Se quiser conhecer, veja a página: {link}. Esta é a nossa última mensagem sobre isso. Para não receber mais e-mails: {link de descadastro}.

Textos de e-mail seguem `FORMULARIO_CAPTACAO_TEXTOS.md` (consentimento) e o padrão do `CALENDARIO_EDUCACAO_7_DIAS.md`. Descadastro e remetente conforme `10-trafego/LGPD_BASE_LEGAL_E_PUBLICOS.md`.

## 7. Anúncio de entrada, mensagem pré-preenchida e primeira resposta (para o ChatGPT/Bruno)
Este bloco **substitui os textos de entrada** de `VENDA_NO_WHATSAPP.md` §2 e §3 **se Bruno aprovar o diagnóstico**; as demais seções daquele arquivo continuam valendo. Execução no Meta = ChatGPT, campanha **pausada**, Bruno aprova. Anúncio nativo "Enviar mensagem" (sem página-ponte), como decide `CRM_WHATSAPP_ENTRADA.md` §3. Nome do anúncio no padrão de `06-criativos/ENTRADA_WHATSAPP.md`: `entrada-wa-diag-v02-dono-terreno` e `entrada-wa-diag-v01-terreno-capital`; campanha `entrada-whatsapp-diag | AAAA-MM-DD`. Limites usuais do Meta [H, o Gerenciador confirma]: título ≤ 40, descrição ≤ 30, ~125 caracteres visíveis do texto antes de "ver mais" (nos textos acima a 1ª frase carrega o gancho e a palavra "gratuito" aparece antes do corte).

### 7.1 Ajuste dos Vídeos 01 e 02 (entrada)
Preservar a imagem e a narrativa de abertura (dor: "tenho terreno/ideia e não sei por onde começar"). **Trocar o final falado e escrito**: sai qualquer frase de investimento, parceiro, Land Bank, inscrição, "avaliar o terreno"; entra: *"Toque em Enviar mensagem e receba o diagnóstico gratuito do estágio do seu projeto."* O corte final mostra, em texto na tela: "Diagnóstico gratuito · ao final, formação paga opcional (R$ 47)". Detalhe de arte e legendas: `06-criativos/` (build_video_entrada_wa.js, outro agente; alinhar para não duplicar).

### 7.2 Texto do anúncio (3 variações; títulos até ~40 caracteres, texto curto na 1ª linha)
**A · Vídeo 02 (dono de terreno)**
- Texto: `Você tem um terreno e não sabe por onde começar? Receba, de graça, o diagnóstico do ESTÁGIO do seu projeto: 6 perguntas rápidas no WhatsApp e um parecer sobre o que já está claro e o que falta. Não é avaliação do terreno nem promessa de investimento. Ao final, mostramos uma formação paga opcional (R$ 47).`
- Título: `Diagnóstico gratuito do seu projeto`
- Descrição: `6 perguntas no WhatsApp`
**B · Vídeo 01**
- Texto: `Tem uma ideia de hospedagem e não sabe se ela já está bem estruturada? Faça o diagnóstico gratuito do estágio do seu projeto pelo WhatsApp. É um retrato do que você já definiu, sem consultoria e sem promessa de investimento. No final, apresentamos uma formação paga opcional (R$ 47).`
- Título: `Em que estágio está o seu projeto?`
- Descrição: `Gratuito, no WhatsApp`
**C · curta**
- Texto: `Diagnóstico gratuito do estágio do seu projeto de hospedagem. 6 perguntas no WhatsApp. Sem consultoria, sem promessa de investimento. Ao final, formação paga opcional (R$ 47).`
- Título: `Diagnóstico gratuito`
Botão: "Enviar mensagem" (formato de mensagens); se a lista for fixa, "Saiba mais" [NC: conferir no Gerenciador]. Proibido no texto/arte: "inscrição", "taxa", "investimento garantido", "parceiro/sócio", "reunião", "avaliação do terreno", "consultoria".

### 7.3 Mensagem pré-preenchida e respostas rápidas
- Vídeo 01 (62 caracteres): `Olá! Vi o vídeo e quero o diagnóstico gratuito do meu projeto.`
- Vídeo 02 (65 caracteres): `Olá! Vi o vídeo, tenho um terreno e quero o diagnóstico gratuito.`
- Respostas rápidas (até 3, ≤ 80 caracteres, mesmo limite [H] de `ENTRADA_WHATSAPP.md`): `Quero o diagnóstico gratuito` · `Como o diagnóstico é calculado?` · `Quanto custa a formação?`. "Falar com a equipe" fica fora (a equipe já responde; evita pedido de reunião).
- Boas-vindas do Meta: `Olá! Aqui é a equipe da Zion. Obrigado pelo interesse. Já respondemos por aqui.`
(Uma frase por vídeo continua servindo de marcador de origem, `CRM_WHATSAPP_ENTRADA.md` §3 camada B.)

### 7.4 Primeira resposta (≤ 1 minuto; humana ou, se aprovada, da Bela)
> Oi! Aqui é da equipe Zion. Vamos fazer o seu diagnóstico gratuito do **estágio do projeto**: são 6 perguntas de múltipla escolha, uns 2 minutos.
> Antes de começar:
> • Não pedimos documentos, valores nem o endereço do terreno.
> • A nota é calculada de forma automática pelas suas respostas e mostra só o estágio das informações. Não é avaliação do terreno nem promessa de investimento.
> • Você pode pedir como foi calculada e a revisão por uma pessoa da equipe, quando quiser.
> • No final, vamos mostrar uma formação paga e opcional (a Mini Mentoria, R$ 47). Só compra quem quiser.
> Política de privacidade: {URL_POLITICA_PRIVACIDADE}. Podemos começar?
> [Começar] [Como é calculado?] [Agora não]
Se a pessoa já perguntou "quanto custa a formação?": responder o preço na hora (R$ 47, pagamento único, garantia de 7 dias) e oferecer o diagnóstico. Fora do horário: a resposta automática de `VENDA_NO_WHATSAPP.md` §3.

## 8. Quem faz o quê (descrição; **nenhuma alteração em Bela ou Zaya**)
Estado lido por outro agente [E, `VENDA_NO_WHATSAPP.md` §9]: Bela e Zaya estão ativas no mesmo número e falam R$ 97, `/inscricao`, reunião e "possível parceria". **Isso conflita com este fluxo.** Qualquer ajuste depende de aprovação e **não foi feito**.

| Etapa | Quem (proposta) | Observação |
|---|---|---|
| 1ª resposta e as 6 perguntas | **Fase 1: pessoa da equipe (SDR) com o roteiro acima.** Depois, Bela com roteiro novo [APROVAÇÃO] | A Bela só entra com novo prompt/conhecimento: diagnóstico gratuito, R$ 47, sem reunião, sem parceria |
| Cálculo da nota | **Regra fixa** (`score.py` ou tabela de pontos da §3 aplicada à mão; futuramente regra de pontuação do ClickMax [NC, não criada]). **Nem a Bela nem a SDR "decidem" a nota** | A IA não altera pontos nem improvisa o parecer; usa as peças da §4 |
| Parecer e convite | SDR ou Bela, **texto fixo** (§4 e §5) | Bela não adiciona promessa, prazo ou desconto |
| Dúvidas e objeções | Bela responde as básicas; **SDR humano** assume as demais (`VENDA_NO_WHATSAPP.md` §6 e §9) | Gatilhos de passagem a humano: pede humano, discorda da nota, fala de investimento/parceria, dúvida de pagamento ou acesso |
| **Pedido de revisão** | **Sempre humano**: confere as respostas, recalcula com a mesma regra e responde por escrito em até {1 dia útil} [H] | Direito a revisão (§9); se houve erro de digitação, corrige e reenvia |
| Comercial | Acompanha compra (pagamento aprovado) e acesso; **não oferece reunião, ligação nem avaliação do terreno** | Sem reunião gratuita |
| Zaya | Fora deste número/fluxo [APROVAÇÃO] | Promete reunião e parceria |

## 9. Salvaguardas obrigatórias (checklist antes de ligar qualquer coisa)
| # | Salvaguarda | Como está garantida |
|---|---|---|
| 1 | **Transparência do critério** | Aviso na 1ª resposta; botão "Como é calculado?"; `explicar()` mostra pontos por critério e o que ficou fora; pesos públicos neste arquivo |
| 2 | **Linguagem de estágio** | Nomes das faixas; pareceres montados de peças fixas; teste varre 1.664 combinações contra a lista de palavras proibidas |
| 3 | **Revisão humana (LGPD art. 20)** | A nota é tratamento automatizado de dados pessoais usado para formar um perfil. Mesmo sem decisão que negue algo (a nota não impede compra nem muda preço), oferecemos: informação clara sobre os critérios e o direito de pedir revisão por pessoa (aviso na 1ª resposta e no fim do parecer; revisão sempre humana). Parecer jurídico final: **advogado [NC]** |
| 4 | **Proibido parecer de viabilidade financeira ou jurídica** | A regra não usa valores nem documentos; o critério "documentos" mede só se estão reunidos; o parecer diz "não os analisamos"; palavras proibidas testadas |
| 5 | **Nada que pareça laudo** | Sem relatório formal, sem selo, sem PDF oficial, sem assinatura; só mensagem de conversa. Se algum dia houver PDF, a frase de limite entra no topo |
| 6 | **Frase de limite** | Obrigatória no fim de todo parecer (teste confere) |
| 7 | **Sem reunião gratuita** | Nenhum botão, texto ou resposta oferece reunião/ligação; o convite diz "não tem reunião" |
| 8 | **Clareza antes do clique** | Anúncio, 1ª resposta e convite dizem: gratuito, 6 perguntas, formação paga opcional de R$ 47 |
| 9 | **Minimização de dados** | 6 respostas por código; sem texto livre, sem valor da área, sem capital, sem documento; a regra recusa chaves desconhecidas (teste) |
| 10 | **Consentimentos separados** | Comunicação comercial (por canal) e personalização de anúncio são caixas separadas, opcionais, desmarcadas; o diagnóstico não depende delas; a pessoa que escreveu primeiro recebe resposta do atendimento, mas follow-up fora da janela exige consentimento e modelo aprovado |
| 11 | **A nota não bloqueia** | Todas as faixas recebem o mesmo convite e o mesmo preço; a nota não define acesso, preço nem prioridade de atendimento |
| 12 | **Parar quando pedir** | "pare/sair": encerra na hora e marca etiqueta `DIAG \| NAO QUER RECEBER` |

## 10. CRM e etiquetas (**propostas, nada criado**; cada criação = [APROVAÇÃO])
**Campos personalizados do contato** (nomes sem acento, prefixo `diag_`; conferir antes se já existe algo equivalente com `custom_fields_list`):
| Campo | Tipo | Conteúdo |
|---|---|---|
| `diag_score` | número | nota 0 a 100 |
| `diag_faixa` | lista | F1, F2, F3, F4 |
| `diag_situacao` | lista | terreno, ideia, hospedagem, aprender |
| `diag_prioridades` | texto curto | até 2 códigos de critério (ex.: `numeros,local`) |
| `diag_versao` | texto curto | versão da regra (`v1-2026-11-25`) |
| `diag_data` | data | data da entrega do diagnóstico |
| `diag_revisao` | lista | nenhuma · pedida · concluída |
Não guardar as 6 respostas brutas em campo livre sem necessidade; se Bruno quiser auditoria da nota, guardar os códigos (sem texto livre). Ids de campo ficam fora do Git quando existirem.

**Etiquetas por faixa:** `DIAG | F1 IDEIA INICIAL`, `DIAG | F2 PRIMEIROS LEVANTAMENTOS`, `DIAG | F3 PROJETO EM MONTAGEM`, `DIAG | F4 INFORMACOES ORGANIZADAS`.
**Etiquetas de etapa:** `DIAG | ENTREGUE`, `DIAG | CONVITE VISTO`, `DIAG | CLICOU LANDING`, `DIAG | REVISAO PEDIDA`, `DIAG | NAO QUER RECEBER`. Convivem com as `WA | ...` de `VENDA_NO_WHATSAPP.md` §10 (não substituem).
**Segmentos (filtro apenas):** diagnóstico entregue por coorte semanal; por faixa; entregue e ainda não comprou; excluir sempre o segmento de compradores `[HIB] 13`.
**Link na conversa (UTM)**, alinhado a `CRM_WHATSAPP_ENTRADA.md` §5 e `PADRAO_UTM.md` §5: `https://infoprodutos-zion.clickmax.space/{landing v2}?utm_source=whatsapp&utm_medium=conversa&utm_campaign=mm47-wa&utm_content=video01-diag-f2&src=wa_video01` (`video01`/`video02` + `diag` + faixa em minúsculas; nunca dados da pessoa na URL). **Um ponto a alinhar com o outro agente [NC]:** o padrão de `utm_content` do WhatsApp (`video01|video02` puro) e o sufixo `-diag-<faixa>`.
Prioridade (`diag_prioridades`) é só para personalizar o T3/T4; **não** entra em público de anúncio.

## 11. Como medir (coortes, sem número real no Git)
Funil por **coorte de dia/semana de entrada** (não comparar lead novo com lead que já teve tempo de comprar). Uma linha por etapa; cada taxa = etapa ÷ etapa anterior e ÷ conversas iniciadas.

| Etapa | Fonte | Observação |
|---|---|---|
| Impressões → cliques → **conversa iniciada** | Meta/Windsor (leitura) e ClickMax | Custo por conversa iniciada |
| Aceitou começar (tocou "Começar") | etiqueta/etapa do ClickMax | Mede a clareza do aviso inicial |
| **Diagnóstico entregue** (concluiu as 6 perguntas) | `diag_data` preenchida / `DIAG \| ENTREGUE` | **Custo por diagnóstico entregue** = gasto ÷ entregues |
| Convite visto (tocou "Quero saber") | `DIAG \| CONVITE VISTO` | |
| **Clique na landing** | evento de clique no link (UTM) / visita à oferta (`FUNIL_DE_EVENTOS_P0.md`) | Clique qualificado, não carregamento de iframe |
| Início efetivo de checkout → Pix gerado | eventos P0 | |
| **Compra aprovada** | pagamento aprovado, conciliado por e-mail/telefone normalizado (`CRM_WHATSAPP_ENTRADA.md` §8) | Só pagamento aprovado conta |
| Reembolso em 7 dias | transação cancelada na oferta | Sinal de expectativa errada |
| Pedidos de revisão e descontentamento | `DIAG \| REVISAO PEDIDA`, mensagens | Qualidade do diagnóstico |

**Cortes de análise:** por faixa (F1 a F4), por criativo (Vídeo 01 × 02), por situação. Janelas de compra em D+1, D+7 e D+14 **por coorte de entrada**.
**Cuidados [H]:** (1) a faixa serve para ver se a conversa/convite funciona **por estágio**, não para escolher quem recebe oferta; (2) não declarar vencedor com amostra pequena; (3) comparar com a conversa **sem** diagnóstico (`VENDA_NO_WHATSAPP.md`) só em coortes simultâneas e do mesmo criativo; (4) CPA do caminho = gasto ÷ compradores conciliados, com o limite de `08-financeiro` (líquido Pix R$ 44,51 antes dos demais custos); (5) acompanhar reembolso e revisões: se muita gente pede revisão ou reembolso, o texto está prometendo mais do que entrega.
O dashboard (`12-dashboard`) precisa de uma seção "Diagnóstico" [NC, não alterado].

## 12. Teste do módulo (executado)
`cd zion-sales-engine/05-funis/diagnostico && python3 -I tests/test_score.py` → **14 testes passam**, incluindo: pesos somam 100; faixas cobrem 0 a 100 sem buraco; nota por exemplo fictício de cada faixa conferida com **conta independente**; "sem terreno" não penaliza; nota nunca cai quando uma resposta melhora (monotonia); a regra **recusa** valor da área, capital, localização, nome, telefone, e-mail; respostas inválidas recusadas; **1.664 combinações** de resposta sem nenhuma palavra proibida e sempre com a frase de limite e a de possibilidade; explicação transparente; campos de CRM sem PII; resultado determinístico.
Uso: `python3 -I score.py respostas.json` imprime parecer e explicação. Exemplos **fictícios** em `tests/test_score.py` (`EX`).

## 13. O que depende de aprovação de Bruno
1. Adotar o diagnóstico no lugar das 3 perguntas de qualificação de `VENDA_NO_WHATSAPP.md` §4 (decisão de fluxo).
2. Criar campos, etiquetas, segmentos e (se houver) regra de pontuação no ClickMax.
3. Ajustar Bela (e tirar a Zaya do número): **não feito**.
4. Novos criativos de entrada (Vídeos 01/02 com o final novo), texto, mensagem pré-preenchida e respostas rápidas no Meta (ChatGPT, pausado).
5. Modelo de WhatsApp fora da janela (Meta) e fluxo de e-mail T4/T5 (ClickMax, rascunho; não ativar).
6. Publicar a landing v2 e o checkout limpo (sem isso, não há link de pagamento).
7. Advogado revisar: base legal, consentimentos, art. 20 e texto de privacidade ({URL_POLITICA_PRIVACIDADE}, {RAZAO_SOCIAL_E_CNPJ_ZION} e e-mail de suporte de domínio da empresa, pendências de Bruno [NC]).
8. Pesos e cortes (§3), revisados após as primeiras 30 conversas.

## 14. [NC]
- Limites de botões e listas do WhatsApp no ClickMax/Gupshup e se o ClickMax guarda as respostas de botão em campo.
- Se a regra de pontuação (`lead_score_rules`) do ClickMax aceita este cálculo ponderado; até lá, a nota é calculada pelo módulo ou à mão.
- Regra do Meta para janela/tarifa em conversa aberta por anúncio e opt-in de follow-up.
- Botão do anúncio de mensagens no Gerenciador.
- Parecer do advogado sobre art. 20 da LGPD no caso de nota automática.
- Se a Bela atual consegue conduzir perguntas com botões sem alterar o prompt (provavelmente não).

## 15. Coordenação com os outros agentes
Lido em 25/11 (releitura no fim): `VENDA_NO_WHATSAPP.md` (FUNNEL), `CRM_WHATSAPP_ENTRADA.md` (DATA) e `06-criativos/ENTRADA_WHATSAPP.md` (CREATIVE). Este arquivo **não repete** objeções, regras de conversa, janela de 24 h, pipeline, atribuição, arte e roteiro dos vídeos: remete a eles.
- **`ENTRADA_WHATSAPP.md` trata a entrada sem diagnóstico** (textos A "queremos conhecer" e B com "formação digital paga", mensagem pré-preenchida `Olá, vi o vídeo e tenho um terreno.`). **O §7 deste arquivo é a variante "com diagnóstico"**: usa a mesma estrutura (nome, título ≤ 40, descrição ≤ 30, botão Enviar mensagem, até 3 respostas rápidas) e **troca só o texto e a promessa** (diagnóstico gratuito do estágio + aviso da formação paga opcional). Bruno escolhe uma das duas; não rodar as duas no mesmo público ao mesmo tempo sem teste planejado. Se escolher o diagnóstico, o **final falado e a cartela final** dos vídeos mudos novos (`build_video_entrada_wa.js`) precisam de um ajuste ("Diagnóstico gratuito · ao final, formação paga opcional (R$ 47)"); isso é pedido ao CREATIVE, **não feito aqui**.
- **`VENDA_NO_WHATSAPP.md`:** se o diagnóstico for aprovado, mudam (a) mensagem pré-preenchida, respostas rápidas e 1ª resposta (§7); (b) as 3 perguntas de qualificação (§4 de lá) viram as 6 do diagnóstico (§2), sem cidade nem objetivo livre; (c) entre qualificação e oferta entra o parecer (§4); permanecem: objeções, regras de conversa, janela de 24 h, papéis, pipeline e etiquetas `WA | ...`, e a regra de **um lembrete** por conversa.
- **`CRM_WHATSAPP_ENTRADA.md`:** valem a atribuição (camadas A, B e C) e o teste obrigatório antes de qualquer gasto; os campos `diag_*` e as etiquetas `DIAG | ...` (§10) se somam às `WA | ...`. A mensagem pré-preenchida por vídeo continua sendo o marcador de origem.
