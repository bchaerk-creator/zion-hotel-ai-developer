# Sessão de Diagnóstico Estratégico · caminho da solicitação (após o Dossiê)

Agente: FUNNEL · 25/11/2026 · **somente rascunho e arquivos**. Nada publicado, ligado, enviado ou ativado. Marcação: **[E]** evidência, **[H]** hipótese, **[NC]** não confirmado.
Decisão de Bruno (25/11): depois de estruturar a mentoria (Dossiê concluído), o comprador **solicita** uma reunião gratuita com a equipe para apresentar a ideia, o projeto ou o terreno. Nome oficial: **Sessão de Diagnóstico Estratégico**. Entra na lista de entregáveis **com ressalva**. Prevalece sobre a regra antiga "sem reunião" (`REGRAS_REUNIAO_POS_MENTORIA.md`).

## 0. Redação padrão (usar sempre)
> Ao concluir o Dossiê, você pode solicitar a **Sessão de Diagnóstico Estratégico** com a nossa equipe para apresentar o seu projeto. É a sua oportunidade de buscar parceiros e investimentos para tirar o plano do papel*.
> *Gratuita para quem concluiu o Dossiê, mediante solicitação. Sujeita à análise e à agenda. Parceria e investimento não são garantidos.

**Não confundir** com a "Sessão de onboarding e estratégia" paga do Club (R$ 270): outro produto, outra oferta, outro fluxo. A Sessão de Diagnóstico Estratégico não é vendida, não substitui aquela e não usa a agenda pública antiga "Equipe Zion", a Zaya nem o playbook "Reunião Estratégica Zion Land Bank" (`c5a44e07…`), que ficam intocados.

## 1. O que a sessão entrega (para a promessa ser cumprível)
Uma sessão **única** de apresentação e leitura do projeto, com duração máxima de 30 minutos (parâmetro, ver 9). Entrega:
1. A equipe **ouve a apresentação** do projeto, a partir do Dossiê em PDF.
2. Uma **leitura de diagnóstico** do que está claro, do que falta e dos riscos visíveis no Dossiê (checklist da seção 7).
3. Um **resumo escrito curto** (até 10 linhas, por e-mail, em até 2 dias úteis [parâmetro]) com: o que está bem estruturado, o que falta, e o próximo passo possível.
4. Se, e só se, a equipe entender que há aderência: **dizer se há interesse em conversar mais**, sem prometer nada. Parceria e investimento seguem "possibilidade sujeita à análise".

**Não entrega:** consultoria contínua, acompanhamento, elaboração ou revisão do Dossiê, estudo de viabilidade, parecer jurídico ou financeiro, avaliação de valor do terreno, captação de investidor, garantia de parceria, de investimento, de ocupação, de renda ou de valorização. Uma sessão por comprador; nova sessão só por decisão da equipe.

## 2. Elegibilidade e verificação do "Dossiê concluído"
Elegível: comprador aprovado da oferta `0c71eeba…` (Mini Mentoria de Estruturação Zion, R$ 47), que concluiu o Dossiê, sem reembolso. Compradores da oferta antiga R$ 97 (`c298aaed`) recebem o mesmo conteúdo: tratar como elegíveis [H, decisão de Bruno].

| O que se quer provar | O que o ClickMax permite ver | Limite honesto |
|---|---|---|
| Comprou a Mini Mentoria | `leads_search` pelo e-mail + `leads_payments`/`transactions_list` (pagamento aprovado da oferta) e matrícula na turma `087479a3…` (`member_users_list_by_classroom`) [E, ferramentas existem] | Conferir e-mail da compra = e-mail do formulário. Divergência: a equipe pergunta, não presume |
| Progresso nas lições | `member_users_get_progress_by_lead` (por portal/turma/curso) e `member_users_get_progress` [E, ferramenta existe; [NC] o nível de detalhe real: nunca lido com um aluno real] | Mede "Concluir aula" clicado pelo aluno. As 70 lições são marcáveis, inclusive e-book e planilha: **marcar tudo não prova que o Dossiê foi montado** |
| Dossiê montado | **Nada.** As fichas "Faça agora" salvam no navegador do aluno (localStorage) e o PDF é gerado no aparelho. O ClickMax não recebe o Dossiê nem sabe se o PDF foi gerado [E, `VISTORIA_ENTREGAVEIS.md` §3] | Não é verificável por API. Falta de rastro: só a **ficha do Pilar 7 (Dossiê)** gera o PDF final |

**Regra proposta (verificação humana + autodeclaração com anexo):**
1. O aluno **declara** no formulário que concluiu o Dossiê e **cola o link do PDF** (Drive/Dropbox, permissão por link). O formulário não aceita upload de arquivo [E, tipos de campo], por isso link.
2. A equipe **abre o PDF** e confere o mínimo objetivo: capa + páginas 0 a 7 preenchidas (a vistoria viu PDF de 14 páginas completo; páginas não geradas saem em branco) e decisão final (avançar/ajustar/parar).
3. A equipe confere no ClickMax, como apoio e não como prova: compra aprovada e progresso na turma (ex.: Módulo 9, Pilar 7, concluído).
4. Critério de corte: PDF aberto, com ao menos o resumo e 5 das 8 páginas preenchidas [H, parâmetro]. Abaixo disso: resposta "ainda falta" com o que completar (mensagem 6.3), sem recusar para sempre.
Nunca pedir CPF, matrícula de imóvel, documentos pessoais ou bancários.

## 3. Formulário de solicitação (criado em rascunho)
- Formulário `aff270f4-0e83-4f4f-8b6f-f62ae00d1392`, nome `[RASCUNHO] MM47 · Solicitação da Sessão de Diagnóstico Estratégico`, projeto Infoprodutos Zion. **Status `draft`: não publicado, não ligado a página, funil, fluxo ativo ou anúncio** [E, `forms_get`/resposta do `forms_update`]. A URL pública do ClickMax existe tecnicamente (`publicUrl`) mas só passa a aceitar envios se for publicado (`status active`) [NC: comportamento exato do link em rascunho; não testar com envio real].
- Campos mínimos: nome; e-mail da compra; cidade e estado do terreno/projeto; estágio (5 opções); **link do PDF do Dossiê**; o que quer apresentar e objetivo (texto livre com aviso para não colocar CPF/endereço/dados bancários).
- Declarações obrigatórias: "concluí o Dossiê e o PDF é meu"; "entendi: sujeita à análise e à agenda, não é consultoria contínua, parceria e investimento não são garantidos".
- **Consentimentos opcionais e separados** (desmarcados, não obrigatórios; deixar desmarcado não afeta a análise): (a) contato comercial da Zion sobre outras formações e oportunidades; (b) uso dos dados de contato para personalizar anúncios. O aviso de privacidade aparece como texto (lgpdText) e **não** é condição: `lgpdRequired` falso.
- Texto de privacidade: usamos os dados só para conferir a compra, analisar o pedido e agendar a sessão; não pedimos documentos pessoais; opcionais separados; correção/exclusão pelo WhatsApp +55 48 6137-1061. [NC: base legal e prazo de retenção a validar com jurídico; o texto é proposta.]
- Mapeamento: só nome e e-mail vão aos campos nativos do contato; os demais ficam na submissão (não criei campos personalizados). Os dois opcionais **não** viram tag automática: quem trata é a equipe, registrando o consentimento na ficha ao analisar [H].
- `dedupRule merge` por e-mail; `allowIndexing` falso; mensagem de sucesso com o prazo "X dias úteis".
- **Como apagar:** `forms_delete` no id `aff270f4…`. Reverter qualquer edição: `forms_replace_schema`.
- **Como ligar (depende de aprovação de Bruno):** `forms_update status: active`, depois incluir o link na lição de Onboarding e na ficha final do Dossiê. Antes: teste com envio fictício do próprio Bruno e conferir que o fluxo continua em rascunho.
- Lacuna [NC]: não há campo de upload; se Bruno quiser anexo direto, só por link.

## 4. Fluxo em rascunho
- Fluxo `ae20a311-4b82-47d8-8cd4-2f56d7a8d565`, `[RASCUNHO] MM47 · Solicitação da Sessão de Diagnóstico Estratégico`, **modo `draft`**, 0 execuções.
- Passos: gatilho "lead capturado" restrito ao formulário `aff270f4…` → e-mail de confirmação (passo `27ab9417…`, remetente `6a8925fb…`) → adicionar etiqueta `MM47 | SESSÃO DIAGNÓSTICO SOLICITADA` (passo `051c3445…`) → marcador de desenho `fc4d71de…` (aviso interno e cartão).
- `flows_validate` (25/11): `valid: true`, `hasEntryTrigger: true`, sem órfãos; único aviso `stepWithoutNext` no marcador (esperado).
- **Limite honesto:** o aviso interno e o cartão **não foram montados**: a API recusou o formato do passo `notifyOwner` (3 tentativas, "Expected union value") e o cartão exigiria `duplicateOpportunity`/`transferOpportunity` sobre um cartão existente do comprador [NC]. Ficam como **desenho** (marcador). Na ativação: montar no editor "Notificar a equipe" (para o responsável da análise) e "Duplicar oportunidade" para a etapa nova do quadro (seção 8), ou criar o cartão por `cards_create` à mão.
- Segurança de ativação: o gatilho filtra por formulário; este formulário nunca foi publicado, então o fluxo não dispara nem se ligado por engano. A confirmação é **e-mail transacional ao próprio solicitante** (não é disparo em massa).
- Apagar: `flows_delete` `ae20a311…`; modelo `email_templates_delete` `81b7bad1…`; etiqueta `tags_delete` `2fbcb654…`.

## 5. Mensagem de confirmação (e-mail em rascunho)
Modelo `81b7bad1-ed22-4685-a87b-7d474f40aaff` (biblioteca) e o mesmo HTML no passo do fluxo. Assunto: "Recebemos a sua solicitação da Sessão de Diagnóstico Estratégico". Texto: recebemos; conferimos compra e Dossiê; analisamos em **até X dias úteis** (X = parâmetro de Bruno); responderemos por e-mail com datas ou o motivo; sessão sujeita à análise e à agenda; não é consultoria contínua; **não é a Sessão de onboarding e estratégia paga do Club**; parceria e investimento não são garantidos; correção de dados por resposta ou WhatsApp. Sem urgência falsa, sem preço, sem promessa. O `{name}` e o rodapé de descadastro precisam ser conferidos no teste [NC: o HTML próprio pode não trazer link de descadastro; confirmar se o ClickMax acrescenta].

## 6. Mensagens de resposta (texto, a equipe envia à mão; nada automatizado)
**6.1 Positiva**
> Olá, {nome}. Analisamos o seu pedido e o seu Dossiê. Podemos fazer a Sessão de Diagnóstico Estratégico com você. Ela dura até 30 minutos, é gratuita e serve para você apresentar o projeto à equipe. Opções de dia e horário: [A], [B], [C]. Responda com a sua escolha. Depois da sessão enviamos um resumo curto por e-mail. Lembrando: não é consultoria contínua, e parceria e investimento não são garantidos.

**6.2 Negativa (honesta)**
> Olá, {nome}. Analisamos o seu pedido. Neste momento não vamos agendar a sessão. Motivo: [o motivo objetivo, ex.: o Dossiê ainda não tem as páginas 3 e 4 / o projeto está fora do que conseguimos avaliar]. Isso não é um julgamento do seu projeto. Você pode ajustar o Dossiê e pedir de novo. Obrigado por ter feito a formação.

**6.3 "Ainda falta"** (Dossiê incompleto): igual à negativa, com a lista do que completar e a frase "quando estiver pronto, peça de novo pelo mesmo formulário". Não promete resposta positiva.
Regra: nenhuma resposta cita investimento, parceria ou retorno como resultado.

## 7. Critérios de análise (propostos, transparentes)
Avaliados sobre o PDF e o formulário; a pessoa pode saber quais são (publicar na página da sessão ao ligar).
1. **Elegibilidade:** compra aprovada, sem reembolso, e-mail confere. (obrigatório)
2. **Dossiê concluído:** conforme seção 2. (obrigatório)
3. **Clareza do projeto:** dá para entender o que é, onde, para quem e em que estágio.
4. **Informação mínima:** localização, situação do terreno ou ponto de partida, números básicos preenchidos.
5. **Aderência à capacidade da equipe:** projeto de hospedagem/turismo dentro do que a equipe consegue ouvir e comentar (sem avaliar valor de terreno nem prometer nada).
6. **Ordem de chegada:** desempate dentro da capacidade semanal.
O que **não** conta: valor do terreno, tamanho do orçamento, ter investidor, nota do aluno em qualquer quiz.

## 8. Pipeline, etapas e etiquetas (proposta; nada criado)
**Onde:** no quadro **Alunos Zion** (`5f7000a7…`), que hoje tem 7 etapas (1 Comprou … 5 Concluiu o conteúdo, 6 Travado, 7 Pediu reembolso), 0 cartões, feito para a entrega da Mini Mentoria [E]. Não criar pipeline novo; **não usar** "Funil Zion" nem "Inscritos · Plataforma Zion Collection" (reunião/avaliação antigas). Etapas novas propostas, após "5 · Concluiu o conteúdo" (criar com `stages_create`, com aprovação):
- `5a · Sessão solicitada` → `5b · Sessão em análise` → `5c · Sessão agendada` → `5d · Sessão realizada` → `5e · Sem sessão (motivo registrado)`.
Reordenação com `stages_reorder` altera a ordem do quadro: confirmar antes que ninguém depende do número atual [NC].
**Etiquetas:** criada `MM47 | SESSÃO DIAGNÓSTICO SOLICITADA` (`2fbcb654…`, 0 leads). Propostas, **não criadas**: `... EM ANÁLISE`, `... AGENDADA`, `... REALIZADA`, `... NEGADA/AJUSTAR`, `... NO-SHOW`, `CONSENTIMENTO | CONTATO COMERCIAL`, `CONSENTIMENTO | PERSONALIZAÇÃO`. Não reutilizar as etiquetas `REUNIÃO | …` existentes (outros fluxos, 16+ leads).

## 9. Agenda nova, capacidade e SLA
**Agenda:** nunca a pública "Equipe Zion". Criar uma **agenda/playbook novo só para esse fim** (com aprovação de Bruno):
1. Agenda nova no ClickMax (Click Meeting), nome "Sessão de Diagnóstico Estratégico · MM47", **sem link público**: a equipe envia o link individual ao aprovado (`scheduled_calls_manage_link` ou criação manual por `scheduled_calls_create`), de 30 minutos, 1 pessoa, janelas fixas (ex.: 2 blocos por semana) [parâmetros].
2. Playbook novo "Sessão de Diagnóstico Estratégico" (escopo `meeting`) com o roteiro da seção 7/10; **não** reutilizar o playbook "Reunião Estratégica Zion Land Bank" (`c5a44e07…`, fala em R$ 97, mentoria e plano B de R$ 970). Não vinculá-lo a pipeline existente.
3. Quem conduz: pessoa(s) da equipe [NC: definir; Bruno decide].
**Capacidade e SLA (parâmetros para Bruno):** capacidade semanal = N sessões [ex.: 5]; resposta ao pedido em até X dias úteis [ex.: 5]; agendamento até 10 dias após aprovação; resumo em até 2 dias úteis após a sessão. Se a fila passar da capacidade, a mensagem de confirmação continua valendo ("sujeita à agenda") e o prazo é reajustado, sem culpar o aluno. Regra de proteção: se o volume de pedidos superar 2 semanas de capacidade, pausar a divulgação da sessão nas páginas até zerar [H].

## 10. Roteiro e checklist da sessão (apresentação do projeto; sem consultoria)
**Antes (10 min):** abrir o PDF; conferir compra; ler o objetivo; anotar 3 perguntas; abrir o checklist.
**Durante (30 min):** (1) 2 min: abertura e regras ("é uma apresentação; não é consultoria; parceria e investimento não são garantidos"); (2) 10 min: o aluno apresenta (ideia, local, estágio, números do Dossiê); (3) 12 min: perguntas da equipe e leitura do que está claro/falta (checklist abaixo); (4) 4 min: dizer o próximo passo possível (ajustar Dossiê, seguir sozinho, ou a equipe avalia conversar mais), sem prometer; (5) 2 min: encerramento.
**Checklist de leitura (marcar sim/não/parcial):** projeto definido; localização e situação do terreno; público e proposta; conceito de hospedagem; estimativa de investimento e retorno com premissas explícitas e marcadas como estimativa; modelo de operação; riscos listados; próximos 90 dias; o que a pessoa busca (sócio, capital, operador, só opinião).
**Depois:** enviar o resumo (até 10 linhas) em 2 dias úteis; mover o cartão para "5d · Sessão realizada"; registrar o desfecho; **não** prometer retorno; **não** acionar venda de outro produto na sessão (contato comercial só com o consentimento opcional marcado).

## 11. Medição
Funil: **comprador (compra aprovada) → Dossiê concluído (autodeclarado + PDF conferido) → solicitação → análise → sessão agendada → sessão realizada → desfecho** (sem parceria/investimento como "meta"; desfechos: seguiu sozinho, ajustou e voltou, interesse mútuo em conversar mais, sem aderência).
| Indicador | Fonte |
|---|---|
| Compradores | `transactions_list`/segmento de compradores MM47 |
| Concluíram lições do Pilar 7 | `member_users_get_progress_by_lead` (aproximação) |
| Solicitações | `forms_submissions_list` do formulário `aff270f4…` + etiqueta |
| % solicitaram / compradores | calculado, por coorte de compra |
| Tempo até responder (SLA) | data da submissão × data da resposta (ficha) |
| % aprovadas, % "ainda falta", % negadas | etapas do quadro |
| % sessões realizadas, no-show | `scheduled_calls_list` da agenda nova |
| Reembolso após sessão | segmento de reembolso |
Sem dados pessoais no repositório. Não declarar efeito da sessão sobre vendas sem coorte e amostra.

## 12. Ressalva: conteúdo antigo que contradiz esta etapa e a oferta (vistoria 25/11)
As fichas dos Pilares e o vídeo de boas-vindas **ainda** têm conteúdo antigo (Land Bank, "enviar à Zion", envio de dados ao baixar o PDF). Nada foi corrigido aqui. O **risco de privacidade** (item 3 da vistoria) é o mais grave: o texto diz "Nada é enviado" e o clique em "Baixar PDF" tenta POST a hosts externos, mesmo sem a caixa de autorização. Com a sessão, o aluno vai gerar o PDF e anexá-lo por link: **o fluxo de PDF precisa estar limpo antes de divulgar a sessão**.

**Ordem de correção proposta (tudo com "aprovado" de Bruno; a turma tem compradores ativos):**
1. **Privacidade das fichas:** parar o envio automático ao baixar o PDF e o botão "Enviar ao Land Bank" (`_landbank.js`, `enviarParaZion`) nas 8 fichas, ou corrigir o texto "Nada é enviado" para o que de fato acontece. Mexe em arquivos do site: ordem de Bruno. **Antes de ligar o formulário.**
2. **Vídeo de boas-vindas** `fcf20da1…`: ocultar (reversível com `lessons_toggle_enabled`) até regravar com o roteiro de `ONBOARDING_PROPOSTO.md` (incluindo a Sessão).
3. **Lições de Onboarding:** criar "Leia primeiro" e trocar a descrição de "Monte o seu dossiê inicial" (textos prontos neste arquivo e no onboarding).
4. **Textos "a equipe Zion monta o seu estudo com você"** (`_anexos.js`, Pilares 1 e 5) e "o dossiê vai para a equipe Zion" (`/dossie/`).
5. **Descrições** que citam "banco de áreas", "simulador" e "mentor de IA" (lições listadas na vistoria §5.6 e §5.12).
6. **E-books PDF** (Land Bank/reunião/quiz) e e-books de aprofundamento "D06": regerar com texto limpo; é o item mais caro, por último.
7. Renomear a turma "(R$ 97)"; anexar pptx/docx do Kit do Investidor; teste manual do Dossiê de ponta a ponta (pedido já registrado).

## 13. O que depende de aprovação de Bruno
Publicar o formulário; ligar o fluxo; criar etapas/etiquetas extras; criar agenda e playbook novos; definir X, capacidade, equipe e SLA; aplicar os textos no portal; corrigir fichas e vídeo; validar privacidade com jurídico; decidir sobre compradores de R$ 97; incluir a sessão na página de venda e no checkout (lista de entregáveis, **com a ressalva**).
