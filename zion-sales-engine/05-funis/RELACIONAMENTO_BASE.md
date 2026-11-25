# Relacionamento e monetização da base de compradores · Mini Mentoria R$ 47

Agente: FUNNEL · 25/11/2026. **Plano. Nada foi ativado nem enviado.** Só o e-mail de boas-vindas existe, em rascunho (`AUTOMACOES_MM47.md`). Marcação: **[E]**, **[H]**, **[NC]**, **[BRUNO]**.

Princípio: primeiro o aluno **usa** o material; só depois vem pedido de depoimento, pesquisa e oferta complementar. Nada de promessa de resultado externo, reunião ou investimento. Mensagens por e-mail; WhatsApp só com modelo aprovado e consentimento.

## 1. Sequência por e-mail (proposta)

| Dia | Mensagem | Objetivo | Para quem | Estado |
|---|---|---|---|---|
| 0 (na compra) | Boas-vindas e acesso | Entrar, saber por onde começar, saber o suporte | Todos os compradores | **Rascunho pronto** (`97330e1d`) |
| 2 | Primeiro passo | "Já abriu o Onboarding? Comece pelo Marco Zero": 1 ação de 15 min | Só quem **não** fez o primeiro acesso | A criar [BRUNO aprova] |
| 5 | Dossiê: o que já está pronto | Mostrar que cada ficha "Faça agora" vira uma página do Dossiê | Quem acessou | A criar |
| 10 | Dica do Pilar em andamento | Um passo prático do pilar que o aluno está cursando | Quem está estudando | A criar; depende de dado de progresso |
| 21 | Gerar o PDF do Dossiê | Convidar a concluir e gerar o PDF no final | Quem avançou | A criar |
| 30 | Pedido de depoimento e pesquisa | Ver seção 3 | Quem usou o material | A criar |
| 45 | Oferta complementar (se pertinente) | Ver `BUMP_UPSELL_DOWNSELL.md` | Quem concluiu parte do conteúdo e não pediu reembolso | Só com aprovação |

Regras: no máximo 1 mensagem a cada 3 dias; cancelar a sequência de quem pediu reembolso; link de descadastro; nada de "últimas vagas" ou prazo inventado.

## 2. Onboarding e engajamento no Dossiê

O que se mede [E, quadro Alunos Zion]: comprou → acesso liberado → primeiro acesso → estudando → concluiu → travado → pediu reembolso.

Sinais de progresso disponíveis no ClickMax: `member_users_get_progress`, `member_users_get_course_progress`, `member_users_get_access_times` [E, ferramentas existentes]. **[NC]** se o progresso por aula e o uso do Dossiê aparecem de forma suficiente para segmentar; verificar com um aluno de teste.

Ações propostas (todas só com aprovação):
1. Mover o card entre as etapas de Alunos Zion com base no progresso (automação do quadro, desligada hoje).
2. Para "Travado · precisa de ajuda" (sem acesso em 7 dias ou parado em um módulo): e-mail de ajuda **sem** tarefa para a equipe individual (sem atendimento personalizado prometido). Dúvidas respondem por e-mail/WhatsApp de suporte como já informado na oferta.
3. Medir: % que faz o primeiro acesso em 24 h, % que preenche a primeira ficha, % que gera o PDF do Dossiê.

O Dossiê é o ativo que o aluno leva: cada ficha vira uma página, PDF no final [E, fatos-chave]. É o melhor gancho de engajamento (concluir o próprio documento), e **não** substitui avaliação da Zion nem garante parceria.

## 3. Depoimento REAL e pesquisa de satisfação

Regras (CLAUDE.md): nada de depoimento inventado; resultado só com documentação; "sem caso documentado" quando não houver.

1. **Pesquisa de satisfação (dia 30):** 3 perguntas curtas: "Conseguiu acessar sem dificuldade?", "O material ajudou você a organizar o seu projeto? (nota de 1 a 5)", "O que faltou?". Formulário do ClickMax (`forms_create`) ou resposta por e-mail. Os dados ficam no CRM, **nunca no repositório**.
2. **Pedido de depoimento:** só para quem respondeu nota alta **e** usou o material. Mensagem honesta: "Se quiser contar em poucas linhas o que achou, ótimo; só publicamos com a sua autorização por escrito."
3. **Consentimento:** texto de autorização com nome de exibição (pode ser só o primeiro nome), onde será usado (página, anúncio) e como retirar. Guardar a autorização fora do repositório público.
4. **Uso:** depoimento real, sem edição que mude o sentido, sem prometer que outro aluno terá o mesmo resultado. Rótulo "depoimento de aluno, resultado individual".
5. **Até haver depoimento autorizado:** a página usa a alternativa honesta (demonstração da plataforma com telas reais), sem prova social inventada.

## 4. Webinário educativo para alunos

**Estado [E]:** o módulo de webinars está **desligado** na conta (`webinars_list` devolve "Module disabled: webinars:read").

**O que é preciso ligar:** o módulo de webinars do ClickMax. Ligar é ação de conta (plano ou configuração do ClickMax), **[BRUNO]**; este agente não liga. Depois disso, a documentação do ClickMax descreve sala de controle, sessões, transmissão ao vivo pela câmera (ClickStream) e oferta na sala [E, docs.clickmax.io].

**Alternativas sem ligar o módulo:**
1. **Aula ao vivo por link** (Zoom, Google Meet ou YouTube Live), com o link enviado por e-mail aos alunos. Gravação depois postada como aula no portal (`lessons_create`, mexe na turma: **[BRUNO]**).
2. **Aula gravada de "perguntas e respostas"** montada a partir de dúvidas reais dos alunos, publicada no portal ou por e-mail.
3. **Encontro no calendário** (agenda do ClickMax `scheduled_calls_*` ou Calendly já conectado) só para o evento, **sem** transformar em reunião individual obrigatória.

**Cuidados de promessa:** o webinário é **aula coletiva educativa**. Não substitui "sem reunião e sem acompanhamento individual" da oferta; não vender parceria ou investimento na transmissão; não prometer que haverá novas edições (só anunciar a data marcada). Se a Mini Mentoria passar a incluir encontros ao vivo, a descrição da oferta e a página precisam mudar **antes** (decisão de Bruno e capacidade real da equipe).

**Primeira edição sugerida [H]:** "Como preencher o Dossiê, ficha por ficha", 40 minutos, para quem está nos Pilares 1 a 3; convite no dia 14 da sequência.

## 5. Monetização da base (sem inventar produto)
- Ordem: entrega → uso → satisfação → depoimento autorizado → oferta complementar pertinente (ferramenta de R$ 19 ou e-book) → ofertas das trilhas **só se existirem e forem aprovadas** [BRUNO].
- Escada de preços do CLAUDE.md: ferramentas R$ 19 → Arquivo R$ 27 → Trilhas. Cada degrau entrega sua própria promessa.
- Não vender captação high ticket (Land Bank, Club) para a base da Mini Mentoria por esta sequência; é outro funil.

## 6. Pendências
- Aprovação de Bruno para criar e ligar cada mensagem.
- Teste de compra para conferir progresso e quadro Alunos Zion.
- Decisão sobre ligar o módulo de webinars ou usar link externo.
- Modelo de consentimento para depoimento (texto final) e local seguro de guarda.
