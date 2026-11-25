# Jornada de entrega · Mini Mentoria de Estruturação Zion (R$ 47)

Agente: FUNNEL · 25/11/2026 · ordem P0 de coerência comercial. Verificação por leitura no ClickMax; escrita só em rascunhos criados pelo FUNNEL (seção 6). Marcação: **[E]** evidência lida, **[H]** hipótese, **[NC]** não confirmado. Sem dados de clientes neste arquivo.
Regra P0: ninguém deve chegar ao checkout sem saber o que compra, quanto paga e o que recebe depois. Esta jornada cobre o depois.
A verificação dos entregáveis (o que existe na turma) é do CONVERSION e não é repetida aqui: ver `08-checkouts/ENTREGAVEIS_VERIFICADOS.md` e `08-checkouts/CHECKLIST_ENTREGA_E_RECUPERACAO_MM47.md`.

## 1. A jornada, passo a passo

| # | Passo | O que o cliente vê | Sistema responsável | Estado | O que pode falhar | Verificação |
|---|---|---|---|---|---|---|
| 1 | Pagamento aprovado | Tela do checkout confirma (Pix pago ou cartão aprovado) | Ticto (gateway) dentro do checkout nativo ClickMax | [E] oferta `approved`, gateway Ticto, Pix e cartão 1x, sem erro de sincronização. [NC] o checkout renderizado nunca foi visto (domínio bloqueado) | Pix pago após expirar; cartão recusado | Compra de teste de Bruno (checklist B.3) |
| 2 | Confirmação da compra | E-mail "Pagamento aprovado" do ClickMax com produto, identificador da transação, subtotal, desconto e total, e recibo com período de acesso | ClickMax (e-mail automático, não editável; visual ClickMax) | [E] existe, por documentação (`docs.clickmax.io/features/messaging/platform-emails`). [NC] se chegou a algum comprador real; [NC] o que a Ticto envia por conta própria (não verificável por MCP) | Vai para spam; o nome do produto no e-mail é o nome da oferta ("Mini Mentoria de Estruturação", sem "Zion") | Compra de teste; ver caixa de entrada e spam |
| 3 | Obrigado | Hoje: página padrão do ClickMax (a auditoria registra que o campo "Página de obrigado" não está ligado). Preparada: `/obrigado-mini-mentoria` (rascunho `1a0aed43`, não publicada) | ClickMax, campo da oferta | [E] rascunho existe; [NC] valor atual do campo (a API da oferta não expõe); [NC] se o checkout embutido respeita o campo | Página não publicada: o redirecionamento falha | Publicar (aprovado), ligar o campo, compra de teste |
| 4 | E-mail de acesso | "Acesso à área liberado": nome da área ("Plataforma Zion Collection"), botão que abre a tela de login **com o e-mail já preenchido**, e-mail de suporte da área (ou o da conta, se a área não tem) | ClickMax, e-mail automático da área de membros (usa nome, logo e cor da área) | [E] regra documentada: sai quando a pessoa ganha acesso a uma área que ainda não tinha, por compra. [NC] remetente exato e assunto: a documentação só diz que, com até 500 pessoas, sai "pelo endereço de sempre" (o de e-mails automáticos); o endereço e o assunto não estão na documentação nem em nenhuma ferramenta. [NC] chegada real nesta oferta | Spam; e-mail digitado errado; vem do ClickMax e não da Zion (o comprador pode não reconhecer) | Compra de teste; `member_users_send_access_link` reenvia (com "aprovado") |
| 5 | Login | Tela de login do portal `zion-plataforma.clickmax.space` | ClickMax, portal `3ef7a340` | [E] `firstAccessWithoutPass` true e `allowSimplePass` true: o primeiro acesso é sem senha criada antes. O link do e-mail abre o login com o e-mail preenchido [E, documentação]. [NC] se o link entra direto, sem digitar nada, ou se pede um código/senha simples: o passo exato da tela não foi visto (login bloqueado aqui). Há ainda a rota de código de 6 dígitos por e-mail ("pedido de código de acesso") [E, doc] | Comprador usa outro e-mail; confunde com a área "Zion Collection" (Club) | Compra de teste, no celular |
| 6 | Orientação inicial | Primeiro módulo "Comece aqui · Onboarding": 3 itens (vídeo "Bem-vindo à plataforma Zion Collection", "Monte o seu dossiê inicial", "Suporte") | ClickMax, turma `087479a3` | [E] existe, mas **tem lacunas** (seção 3) | Ver seção 3 | Leitura das lições (feita) e teste de Bruno |
| 7 | Plataforma | 9 módulos e 70 conteúdos, todos habilitados; acesso à plataforma digital | ClickMax, conteúdo `79d3e792` | [E] 9 módulos, 70 itens, `defaultAccessDuration` 12 meses, liberação "dias após a compra" sem prazo configurado (tudo liberado) | Vídeo e links externos (GitHub Pages, YouTube, Airtable) fora do ClickMax | Percorrer 1 aula de cada tipo |

### Como o acesso é criado após a compra [E]
- A oferta `0c71eeba` tem 1 entrega `internal_membership` (portal `3ef7a340`, turma `087479a3`) [E, `offers_get`]. Pagamento aprovado cria o usuário de membro e o coloca na turma, sem fluxo e sem liberação manual (documentação do ClickMax, "Como entrego meu curso na área de membros", passo 3).
- Prova indireta de que o caminho funciona na prática: os compradores reais de 24/11 (oferta antiga de R$ 97, mesma turma) aparecem em `member_users_list_by_classroom` com `active` true e `lastLoginAt` preenchido, um deles minutos após a criação [E]. Isso prova criação do acesso e login para o R$ 97. Para a oferta de R$ 47 o ciclo **nunca foi percorrido**: 0 vendas [NC].
- Diferença que importa: a oferta antiga `668391e7` ("Zion Collection Club | Acesso à plataforma (R$ 47)") entrega em **duas** áreas (portal `zion-collection` e portal `zion-plataforma`) [E]. Quem comprou por ela tem dois acessos e, pela regra "uma vez por área", tende a receber dois e-mails de acesso [H]. A Mini Mentoria `0c71eeba` entrega em uma só.

### Respostas diretas às perguntas da ordem
1. **O cliente recebe e-mail de acesso automático do ClickMax ao comprar?** Sim, por documentação [E-doc]; chegada real nesta oferta [NC]. Remetente: nome "Plataforma Zion Collection" (nome da área) [E-doc]; endereço e assunto [NC].
2. **O link entra no portal sem senha?** O botão abre o login com o e-mail preenchido e o portal permite primeiro acesso sem senha [E]. Se entra sem nenhum clique extra [NC].
3. **O que ele vê ao entrar?** A turma "Plataforma de estruturação (R$ 97)" [E] com o título do conteúdo "Plataforma de estruturação Zion Collection", capa e módulos. O módulo 1 é o Onboarding. Se o nome da turma aparece ao aluno [NC] (CONVERSION já sinalizou).
4. **A orientação inicial existe e é clara?** Existe, mas **não é clara nem coerente com a oferta de R$ 47** (seção 3).

## 2. O que a Mini Mentoria promete versus o que o aluno encontra ao entrar

Leitura das 3 lições do Onboarding [E]:
| Lição | O que diz | Problema P0 |
|---|---|---|
| 1 · Bem-vindo à plataforma Zion Collection (vídeo `plataforma-v02.mp4`) | "você assiste aos vídeos, preenche os formulários e constrói o seu Dossiê de Desenvolvimento" | O vídeo é o mesmo apontado pelo CREATIVE e pelo CONVERSION como contendo quadros de "Land Bank" e "receber investimentos" [segundo `ENTREGAVEIS_VERIFICADOS.md`; o FUNNEL não assistiu ao vídeo, [NC]]. O nome "Zion Collection" não é o nome do produto comprado |
| 2 · Monte o seu dossiê inicial | "Preencha os formulários e **envie as páginas do seu dossiê para a Zion conhecer o seu projeto**. Responda ao diagnóstico, veja o resultado e leve a página 0" | Contradiz "sem reunião, sem atendimento individual, sem avaliação": o aluno entende que a Zion vai receber e avaliar o que ele enviar |
| 3 · Suporte · Tire suas dúvidas aqui | Chat de suporte (link do ClickMax) | Ok. [NC] se o chat é monitorado |

Outras lições citam "enviar ao banco de áreas" e "mentor de IA" (CONVERSION, achados fora do texto de venda). Aqui só se acrescenta: **a lição 2 do Onboarding é a que mais quebra a expectativa**, porque é a primeira coisa que o aluno faz.

## 3. Lacunas da orientação inicial e a correção proposta

| # | Lacuna | Gravidade | Correção |
|---|---|---|---|
| L1 | Nenhuma lição diz **o que você comprou** nem **o que não está incluído** (sem reunião, sem atendimento individual, sem promessa de investimento ou parceria) | Alta | Aula-texto proposta A (abaixo) |
| L2 | Não há **ordem de uso** explícita no módulo 1 (a ordem está em "Comece aqui · Como usar o curso", dentro do Marco Zero, módulo 2) | Média | Aula-texto A traz os 4 passos |
| L3 | Lição 2 manda "enviar o dossiê para a Zion" | Alta | Reescrever a descrição (texto B) |
| L4 | O portal e o conteúdo chamam-se "Zion Collection"; o aluno comprou "Mini Mentoria de Estruturação Zion" | Média | Texto A abre dizendo "Você está na plataforma da Mini Mentoria de Estruturação Zion"; renomear portal/turma só com "aprovado" |
| L5 | Turma chama-se "(R$ 97)" | Média | Renomear (`classrooms_update`), com "aprovado" de Bruno; acessos permanecem |
| L6 | Não há como saber **quanto tempo leva** e **como pedir ajuda ou reembolso** | Média | Texto A traz: ritmo livre, suporte por WhatsApp, reembolso em 7 dias pelo mesmo canal |
| L7 | Não existe e-mail de boas-vindas ativo | Alta | Rascunho já criado e atualizado (seção 6), aguarda aprovação para ligar |

**Nada abaixo foi aplicado.** Há compradores ativos na turma: nunca alterar módulos, aulas ou turma sem "aprovado" de Bruno. Os textos ficam como proposta.

### Texto A · Aula-texto proposta, nova lição 0 do Onboarding ("Leia primeiro: o que você comprou e por onde começar")
> **Você está na plataforma da Mini Mentoria de Estruturação Zion.**
> Esta é uma formação digital autônoma: você estuda no seu ritmo e monta o seu Dossiê passo a passo.
>
> **O que você tem aqui:** 9 módulos e 70 conteúdos: aulas gravadas, aulas interativas, fichas "Faça agora", e-books por pilar, 2 planilhas de cálculo em branco, Kit do Investidor (modelos para você preencher), kit com 9 comandos de IA e o Dossiê, que você gera em PDF no final.
>
> **O que não está incluído:** reunião e atendimento individual. Não prometemos investimento, parceria, ocupação ou renda: o que você leva é o conhecimento e o seu Dossiê.
>
> **Por onde começar, em 4 passos:**
> 1. Assista ao vídeo de boas-vindas (aula seguinte).
> 2. Vá ao módulo "Marco Zero" e abra "Comece aqui · Como usar o curso".
> 3. Faça o seu diagnóstico prévio ("Faça agora").
> 4. Siga os Pilares 1 a 7, na ordem. Em cada um: aula, vídeo e a ficha "Faça agora".
>
> **Ajuda:** dúvida de acesso ou de uso? Use a aula "Suporte" ou o WhatsApp +55 48 6137-1061. Se achar que a formação não é para você, peça o reembolso em até 7 dias pelo mesmo canal.

### Texto B · Descrição proposta para a lição 2 do Onboarding ("Monte o seu dossiê inicial")
> Responda ao diagnóstico, veja o resultado e guarde a página 0 do seu Dossiê. Todo o material fica com você: o envio ao banco de áreas da Zion, mais adiante, é opcional e não garante análise, parceria nem investimento.

### Texto C · Aviso do portal (opcional, "Novo aviso publicado" também sai por e-mail em massa; preferir a lição A para não disparar e-mail)
Não usar aviso. Motivo: todo aviso publicado sai por e-mail em massa a todos os membros da área, inclusive aos compradores antigos [E-doc].

## 4. O que pode falhar e como achar cedo
1. **E-mail de acesso não chega.** Diagnóstico em `CHECKLIST_ENTREGA_E_RECUPERACAO_MM47.md` seção C. O e-mail de boas-vindas da Zion (rascunho) existe justamente para não depender só do e-mail do sistema.
2. **O comprador não sabe quem é o remetente.** O e-mail de acesso sai com o nome da área ("Plataforma Zion Collection"). O e-mail da Zion cita o nome do produto e o botão "ENTRAR NA PLATAFORMA".
3. **Compra com e-mail diferente do que ele usa.** O texto manda usar o e-mail da compra. Suporte pelo WhatsApp.
4. **Três e-mails seguidos** (pagamento aprovado + acesso liberado + boas-vindas da Zion) podem confundir. Aceitável por serem de naturezas diferentes; se Bruno preferir enxugar, manter só os dois do sistema e a lição A (a boas-vindas da Zion é a única que pode ser desligada sem perder o acesso).
5. **Nome do produto diferente em cada ponto** (checkout, e-mail do sistema, portal). Ver `FUNIL_P0_COERENTE.md`, seção 3.

## 5. Verificação (roteiro que fecha os [NC])
Compra real de Bruno (já descrita em `CHECKLIST_ENTREGA_E_RECUPERACAO_MM47.md`), anotando só o que está abaixo, sem e-mail nem CPF no repositório:
| Conferir | Resultado |
|---|---|
| Assunto e remetente exatos do "Pagamento aprovado" e do "Acesso à área liberado" | |
| Minutos entre pagamento e e-mail de acesso | |
| O botão do e-mail entra sem senha? Pede código? | |
| Primeira tela vista após o login (qual turma, qual módulo) | |
| A turma mostra o nome com "R$ 97"? | |
| Texto das 3 lições do Onboarding no celular | |
| Chegou o e-mail de boas-vindas da Zion (só depois de ligar o fluxo) | |

## 6. O que foi criado ou alterado em rascunho (tudo não ativo, nada enviado)
| Item | Id | Alteração |
|---|---|---|
| Modelo `[RASCUNHO] MM47 · Boas-vindas e acesso` | `97330e1d-0975-4ef2-99e9-a836a7750465` | Reescrito no padrão P0: nome Zion, R$ 47, acesso à plataforma digital, o que comprou, como acessar, onde começar (Onboarding, Marco Zero, Pilares), suporte, garantia |
| Fluxo `[RASCUNHO] MM47 · Pós-compra`, passo de e-mail | fluxo `50e32512-e263-4074-ada4-8f3d3d347ed7`, passo `e2793276-c5c0-4a60-97ef-b5c1031f1089` | Mesmo conteúdo do modelo |
| Modelo **novo** `[RASCUNHO] MM47 · Confirmação da compra (o que você comprou)` | `ef272b75-47b2-4880-8c8a-4c48543a024d` | Biblioteca apenas, **não ligado a fluxo** (evita 4 e-mails seguidos). Usar no lugar da boas-vindas só se Bruno quiser separar confirmação e acesso |
| Modelo `[RASCUNHO] MM47 · Pix expirado` | `0f78a232-d2e3-490c-b848-6e8243fbad47` | Padrão P0 e botão "QUERO ACESSAR A PLATAFORMA POR R$47" |
| Fluxo `[RASCUNHO] MM47 · Pix não pago`, passo de e-mail | fluxo `d98795db-2653-4077-a0d0-ed8743259b89`, passo `4acc21ca-3a69-48cc-af5e-37f6cb5f5754` | Idem; debounce 3600 s para 604800 s (7 dias) |
| Modelo `[RASCUNHO] MM47 · Carrinho abandonado` | `95a66dbe-2bf4-4811-9efa-2e1ede11fa98` | Padrão P0 e botão com preço |
| Fluxo `[RASCUNHO] MM47 · Carrinho abandonado`, passo de e-mail | fluxo `845e3b70-ca71-4de9-923a-ee19f4cd7e73`, passo `d4bd357f-3c63-4535-ae59-d783cffb49ea` | Idem; debounce para 604800 s |

`flows_validate` (25/11, depois das edições): os 3 fluxos `valid: true`, `hasEntryTrigger: true`, sem órfãos, sem `triggerWithoutOutput`; único aviso `stepWithoutNext` no e-mail final (esperado). `flows_list`: os 3 continuam `draft`, 0 execuções, 0 contatos [E]. Conferência de termos nos 4 textos (script local): nenhum contém R$ 97, 270, reunião, investimento (fora do nome "Kit do Investidor"), parceria, "equipe entrará em contato", "inscrição".
Os e-mails seguem sem urgência falsa. O link dos de recuperação vai para `/mini-mentoria` (página que explica e mostra o preço), nunca direto ao checkout.

## 7. Condição "já comprou" nos fluxos de Pix e de carrinho
Tentativas desta sessão, todas recusadas pela API [E]:
1. `flows_graph_apply` `add` conditional com `input.statements:[{type:'tagApplied', tagId, operator:'is-not'}]`, a partir de `flows_conditionals_catalog`: "Expected union value".
2. Mesmo, com `input.type:'conditional'`; com `input.conditions`; com `input.operator:'and'` e `statements` aninhados; com `input.type:'tags'`: mesma recusa (5 formatos no total).
3. Saída por evento: `flows_steps_triggers_set` `triggerExit` (pagamento aprovado da oferta): "triggerExit is read-only: the flow goal is configured via PUT /flows/:flowId/goal". O objetivo do fluxo (a "meta" que encerra a execução) não tem ferramenta no MCP.
4. Não há fluxo existente com condição para copiar o formato (`flows_list` com `types:['conditional']` vazio).
**Resultado: a condição continua pendente e bloqueia a ativação dos dois fluxos de recuperação** (A08). Tutorial para Bruno, no editor do ClickMax (nomes de menu conforme a documentação e o catálogo [NC: rótulos exatos podem variar]):

Opção 1 (preferida, mais simples): meta do fluxo
1. Automações → abrir `[RASCUNHO] MM47 · Pix não pago`.
2. Abrir as configurações do fluxo → **Meta** (objetivo do fluxo; o fluxo já está com "encerrar ao atingir a meta" ligado, `finishOnGoal` true).
3. Definir a meta como o evento **Compra aprovada** (`checkout.transaction.paid.v1`) com a restrição **Oferta = Mini Mentoria de Estruturação**. Salvar.
4. Repetir no `[RASCUNHO] MM47 · Carrinho abandonado`.
Efeito: quem paga durante a espera sai do fluxo e não recebe o e-mail.

Opção 2: passo Condição
1. No fluxo, passe o mouse sobre a linha entre **Espera** e **E-mail** → **+** → **Condição**.
2. Condição **Tag aplicada** → tag `MM47 | COMPROU` → operador **não está aplicada** (`is-not`).
3. Ligue a saída **Sim** ao e-mail e deixe a saída **Não** sem destino (fim).
4. Observação: a tag `MM47 | COMPROU` só é aplicada pelo fluxo de Pós-compra, que também está desligado. Para a Opção 2 funcionar, o Pós-compra precisa estar ligado antes. Por isso a Opção 1 é a preferida.

Teste de prova (obrigatório antes de ligar): gerar um Pix, deixar expirar, pagar um novo Pix antes da espera acabar, e confirmar em `flows_executions_list` que o fluxo saiu sem enviar. **Não executado** (exigiria compra real).

## 8. Aprovações pedidas
1. Compra de teste de Bruno e preenchimento da tabela 5.
2. Ligar o campo "Página de obrigado" e publicar `/obrigado-mini-mentoria` (CONVERSION).
3. Aplicar os textos A e B no portal (nova lição e descrição); renomear a turma "(R$ 97)".
4. Ligar o fluxo Pós-compra (depois do teste); recuperação só após a condição ou meta (seção 7).
Reverter o que o FUNNEL fez hoje: o texto antigo dos e-mails (versão com "Mini Mentoria de Estruturação" sem "Zion", sem botão de preço) está descrito em `AUTOMACOES_MM47.md`, seção 2, mas o HTML original não foi guardado; como são rascunhos sem uso, o caminho é reescrever, não restaurar. O modelo novo sai com `email_templates_delete` no id `ef272b75`.
