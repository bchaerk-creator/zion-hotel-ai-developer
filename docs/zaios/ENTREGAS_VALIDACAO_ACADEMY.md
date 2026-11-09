# Três entregas para validação · Teste, revisão e currículo

Data: 08/11/2026 · Para: Bruno Chaerk · Status: proposta. Nada foi alterado, renomeado, produzido ou publicado, e nenhum crédito Lovable foi gasto.

---

# Entrega 1 · Roteiro de teste da ZAIOS (15 itens)

Onde: https://zaios.lovable.app · Quem: Bruno (admin) e, depois, 2 ou 3 membros.
Como registrar: em cada linha, marque **OK**, **Falhou** ou **Não testei**. Em "Falhou", escreva o que apareceu na tela (um print ajuda muito).
Tempo estimado: 40 a 60 minutos para o roteiro completo.

## Antes de começar
- Use o computador nos itens 1 a 13 e o celular no item 14.
- Tenha à mão um segundo e-mail seu (para os itens 2 e 11) e alguns dados de um empreendimento real ou inventado.

## Roteiro

| # | Teste | Passo a passo | Deve acontecer | Resultado | O que apareceu |
|---|---|---|---|---|---|
| 1 | Entrar | Abra o site, digite b.chaerk@gmail.com, clique em "Receber link de acesso" e abra o link do e-mail | O e-mail chega em poucos minutos e o link abre a ZAIOS (não a prévia) | | |
| 2 | Bloqueio | Peça o link com um e-mail que NÃO está liberado | Aparece "ainda não tem acesso" e nenhum e-mail chega | | |
| 3 | Aceite | No primeiro acesso, leia e aceite Termos e Privacidade | Só entra depois de aceitar | | |
| 4 | Cadastro | Crie um empreendimento preenchendo só o nome e o município | Salva e aparece no painel | | |
| 5 | Jornada Desenvolvimento | Escolha Desenvolvimento e faça Território, Mercado, Produto, CAPEX, Receitas e Viabilidade (pode ser com números inventados) | Cada pilar salva sozinho, volta de onde parou e mostra um veredito | | |
| 6 | Jornada Operação | Em outro empreendimento, escolha Operação e faça Raio-X, Posicionamento, Maturidade; lance 3 meses em Finanças e a ocupação em Indicadores | Os painéis mostram os números do mês e dos 12 meses | | |
| 7 | Conta certa | No Potencial de faturamento, use 3 unidades, 365 dias, diária R$ 680 e ocupação 38% | Receita do ano: R$ 282.948,00 | | |
| 8 | Recálculo | Mude o número de unidades no cadastro e volte a um exercício já feito | Aparece "Desatualizado" com o botão Recalcular | | |
| 9 | Plano | Abra o Plano de Melhoria (ou Plano de ação) e marque uma ação como feita | A pendência de origem também fica resolvida | | |
| 10 | Dossiê | Gere uma versão, baixe o PDF; mude um dado; gere outra versão | O PDF abre legível; a versão 1 continua igual; aparece a versão 2 | | |
| 11 | Privacidade entre membros | Libere seu segundo e-mail no Admin, entre com ele e tente abrir o endereço de um empreendimento do primeiro | Não vê nada do outro membro | | |
| 12 | Admin | Suspenda o segundo e-mail e tente usar a sessão dele; depois reative. Clique em "Exportar todos os dados" | Suspenso perde o acesso na hora; o arquivo de exportação baixa | | |
| 13 | Meus dados | Com o segundo e-mail: "Baixar meus dados"; depois "Excluir minha conta" | O arquivo tem os dados dele; a exclusão apaga tudo e ele não entra mais | | |
| 14 | Celular | No celular, repita os itens 4, 5 (um pilar) e 10 | Tudo cabe na tela, sem rolar para o lado, e os botões funcionam | | |
| 15 | Erros | Digite ocupação 150%, diária "500.50" e unidades "2,5" | Mensagens claras; a diária vira R$ 500,50; nada quebra | | |

## No fim
- Quantos itens deram OK, quantos falharam.
- Três coisas que mais incomodaram (texto, visual ou caminho confuso).
- Se o e-mail de acesso chegou com texto estranho ou em inglês (ele ainda é o padrão).

Com isso eu separo o que é erro (corrigir antes de tudo) do que é melhoria (entra na fila).

---

# Entrega 2 · Lista de revisão dos 17 materiais já produzidos

Cada material é um **e-book HTML** (com PDF) e uma **aula de 40 slides**, publicados no site da Zion com `noindex` e guardados no ClickMax no curso arquivado "Biblioteca". Todos estão marcados "pronto para revisão": nenhum foi aprovado.

## Critérios de aprovação (valem para os 17)
Baseados no checklist de qualidade da escola (`.claude/skills/zion-learning-design`):
1. **Fidelidade:** frameworks com ™ e citações existem nas fontes Zion e estão escritos igual.
2. **Números:** vêm da fonte ou são exemplos marcados como fictícios; as contas estão certas.
3. **Promessa:** nenhuma promessa de renda, retorno, crédito, investidor ou aprovação.
4. **Linha de corte:** temas legais, ambientais e tributários mandam ao profissional habilitado.
5. **Duas jornadas:** cada capítulo serve para quem quer começar (Jornada A) e para quem quer crescer (Jornada B).
6. **Didática:** objetivo no início, pontos-chave, exemplo resolvido, exercício no fim de cada capítulo; aula com interação a cada 3 ou 4 slides.
7. **Linguagem Zion:** "ecossistema", "equipe Zion", "trilha", "membros"; sem consultoria, curso, comunidade ou mentoria; sem Airbnb nos textos de venda.
8. **Fatos da Zion:** só os aprovados (por exemplo, Urubici e Florianópolis desde 2020, os 20 anos de hotelaria do Bruno).
9. **Forma:** português correto, sem travessão, sem texto saindo de caixa, legível no celular.
10. **Decisões do produtor:** as premissas listadas na coluna "Para o Bruno decidir" foram aceitas ou corrigidas.

## Lista

| # | Unidade | Título | Conteúdo (promessa) | Tamanho | Ferramenta associada | Para o Bruno decidir |
|---|---|---|---|---|---|---|
| 1 | Z00 | O Universo dos Negócios de Hospedagem | A diferença entre alugar e hospedar, e o mapa dos modelos de hospedagem | e-book + aula | Porta de entrada da ZAIOS | Texto de abertura com a trajetória do Bruno (Meliá, Barceló, Wyndham) está correto |
| 2 | Z01 | Da Propriedade ao Negócio de Hospedagem | Saber o que a propriedade comporta e decidir por escrito: seguir, ajustar ou parar | 142 pp | Diagnóstico de Potencial do Imóvel ou Terreno; ZAIOS P1; mini mentoria B05 | Faixas do Zion Score aplicadas à soma de 10 notas (0 a 100) |
| 3 | Z02 | Como Começar com os Recursos que Você Tem | Sair da paralisia sem apostar mais do que aguenta perder | 142 pp | Plano Inicial e Alternativas de Capital; B03, B04, B09 | Giro mínimo de 6 meses e regra da maior contingência |
| 4 | D00 | Marco Zero: A Jornada do Desenvolvedor | Saber onde está no desenvolvimento e o que é evidência ou opinião | 87 pp | Marco Zero do Desenvolvimento; ficha Marco Zero | "Dossiê de Desenvolvimento Zion" e escala de evidência 0 a 3 são criação do módulo |
| 5 | D01 | Território e Localização | Dizer com dado se existe negócio possível no lugar | 139 pp | Diagnóstico de Território; ZAIOS P1; ficha aula1 | Reserva legal só com percentual ilustrativo (nenhuma fonte cita lei) |
| 6 | D02 | Mercado e Demanda | Trocar "acho que tem demanda" por número com fonte e data | 136 pp | Estudo de Mercado; ZAIOS P2; ficha aula2 | Estrutura do Dossiê de Mercado do Volume 02 |
| 7 | D03 | Produto de Hospedagem e Diversificação | Produto decidido em número, tipo, tamanho, itens e custo de operar | 130 pp | Conceito de Produto; ZAIOS P3; ficha aula3; B07 | Briefing do arquiteto fica no D05 |
| 8 | D04 | Modelos de Negócio e Monetização | Quem opera, de onde vem cada real e como realizar o valor | 131 pp | Modelo de Negócio; ficha pilar4; B07 | Uso dos frameworks do Volume 04 (Quadrante, Cinco Receitas, Mapa de Saídas) |
| 9 | D05 | Conceito, Posicionamento e Masterplan | Frase própria, desenho do terreno inteiro e briefing do arquiteto | 135 pp | Conceito e Masterplan Faseado; ficha pilar5 | Score de Produto como soma 0 a 100; apoio de 15% a 25% da área |
| 10 | D06 | Estruturação Jurídica, Societária e Land Bank | Direito de uso verificado e estrutura explicável em uma página | 133 pp | Dossiê de Desenvolvimento Zion; ficha pilar7 | Zion Score de Estratégia e o "parecer" final |
| 11 | F00 | Marco Zero: A Jornada do Capital | Saber com número onde está no dinheiro antes de pedir capital | 96 pp | Marco Zero do Capital | Nenhum número de exemplo das fontes usado (erros documentados) |
| 12 | F01 | CAPEX e Necessidade de Capital | CAPEX linha por linha e quanto falta | 133 pp | Mapa do CAPEX; **ZAIOS P5**; Planilha 1; B06 | Números da personagem Marina reabertos (CAPEX R$ 1.237.400); faixas de OS&E, pré-abertura e contingência (as mesmas usadas na ZAIOS) |
| 13 | F02 | Receitas, Custos e Modelos de Rentabilidade | Quanto entra, sai e sobra em cada mês | 143 pp | Modelo de Receitas e Custos; **ZAIOS P6 Receitas**; A03 | Fator 0,82; retirada a R$ 40 por hora; cascata com reserva abaixo do EBITDA (a ZAIOS usa as mesmas regras) |
| 14 | F03 | Viabilidade e Análise de Investimentos | Decisão defensável diante de quem põe dinheiro | 135 pp | Estudo de Viabilidade; **ZAIOS P6 Viabilidade**; Planilha 2; A09; B08 | Taxa ilustrativa de 10%; múltiplo de saída 6 vezes; regra de decisão em 5 passos (a ZAIOS usa as mesmas regras) |
| 15 | F04 | Planejamento Financeiro, KPIs e Valuation | Plano conferido todo mês e o valor do negócio | 139 pp | Plano Financeiro e Painel de Indicadores; **ZAIOS G2 e G3** | Fonte nova usada (e-book Finanças Zion 360, Volume 5) |
| 16 | F05 | Crédito, Bancabilidade e Garantias | Quanto o projeto aguenta dever e o que fica em risco | e-book + aula | Mapa de Crédito e Garantias | Lacunas de fonte (taxas, amortização, documentos do banco); aula marcada como desativada |
| 17 | F06 | Sócios, Fundos e Captação | Pasta pronta e piso decidido antes da conversa de capital | e-book + aula | Estrutura de Capital e Uso dos Recursos; Kit do Investidor; B01, B02, B10 | Harmonização com o F05 (tetos de dívida das personagens) |

Endereços: `https://bchaerk-creator.github.io/zion-hotel-ai-developer/escola/<unidade>/` (e-book) e `.../escola/<unidade>/apresentacao/` (aula).

## Sugestão de ordem de revisão
1. **F01, F02, F03** primeiro: a ZAIOS já usa as regras deles. Aprovar ou corrigir aqui valida também os cálculos da plataforma.
2. **Z00, Z01, D00**: a porta de entrada.
3. **D01 a D06**: a Trilha 1 completa.
4. **F00, F04, F05, F06**: capital.

Forma de revisar sem ler 2.000 páginas: abrir a aula de 40 slides de cada unidade (cerca de 15 minutos), conferir a coluna "Para o Bruno decidir" e ler só os capítulos em que algo incomodar.

---

# Entrega 3 · Proposta curricular dos quatro primeiros módulos de Gestão e Operação

Legenda: **Existe** (reaproveitar como está), **Adaptar** (existe, precisa de ajuste), **Novo** (produzir).
Padrão de cada módulo: 5 aulas, e-book da unidade do Método 360°, aula de 40 slides, ferramenta na ZAIOS ou utilitário, POPs, exercício e avaliação. Narrativa ECROI só na abertura e no fechamento do e-book e nos materiais de venda.

## Módulo 1 · Gestão financeira da operação
Unidade 360°: **G04 Fechamento Financeiro e Gestão Financeira** (com base em F02 e F04). Pilar ZAIOS: **G2 Finanças** (e G3).
Público: quem já hospeda (aluguel por temporada, cabana, glamping, pequena pousada).

Objetivos: separar a conta da hospedagem da conta pessoal; lançar receitas e despesas por categoria; fechar o mês; ler resultado gerencial, margem e pior mês sem confundir com caixa ou lucro contábil; montar a reserva de caixa.

| Aula | Conteúdo | Exercício |
|---|---|---|
| 1 · As três contas | Caixa da operação, reserva e retirada do dono | Separar 10 lançamentos fictícios nas três contas (Novo, curto) |
| 2 · Lançar o mês | Categorias de receita e despesa; fixa ou variável; comissão como linha própria | Lançar um mês no **G2** (Existe) |
| 3 · Fechar o mês | Conferir repasses das plataformas, extrato e lançamentos | Fechamento guiado de um mês fictício (Novo) |
| 4 · Ler o resultado | Receita bruta, receita líquida, resultado gerencial, margem, pior mês | **Calculadora de Custos e Rentabilidade A03** (Existe) |
| 5 · Proteger o caixa | Reserva, quantos meses ela cobre, o que fazer no mês fraco | Reserva no **G2** (Existe) |

| Material | Situação | Observação |
|---|---|---|
| E-book G04 | **Novo** | Reaproveitar F02 (Cap. 1 e Cap. 7, "Quem já opera") e F04 (plano mensal), sem repetir |
| Aula de 40 slides G04 | **Novo** | Fábrica de aulas |
| Vídeo tutorial A03 | **Existe** | zar-a03-tutorial.mp4 |
| Vídeo tutorial do G2 na ZAIOS | **Novo** | Gerador de tutoriais |
| Planilha Diária Mínima (abas Reservas e Resumo do mês) | **Existe** | Ferramenta 01 |
| "Planilha financeira por imóvel" (catálogo 10) | **Não produzir** | O G2 da ZAIOS já cobre |
| POP de fechamento mensal | **Novo** | 1 página |
| POP de conferência dos repasses das plataformas | **Novo** | 1 página |
| Entregável: Painel Financeiro Mensal + rotina de fechamento | **Existe** (G2 e Dossiê) + POP novo | |

Novos neste módulo: 1 e-book, 1 aula, 1 tutorial, 2 POPs, 2 exercícios curtos.

## Módulo 2 · Governança, limpeza e lavanderia
Unidade 360°: **O03 Limpeza, Arrumação e Lavanderia**. Pilar ZAIOS: O5 Rotinas (ainda não construído).

Objetivos: definir o padrão de limpeza por ambiente; separar arrumação de saída e de permanência; inspecionar e liberar a unidade; controlar enxoval (estoque mínimo e giro) e lavanderia; saber o tempo e o custo de cada unidade limpa.

| Aula | Conteúdo | Exercício |
|---|---|---|
| 1 · O padrão que o hóspede percebe | O que derruba avaliação; padrão por ambiente | Adaptar o modelo de 33 itens do **Checklist 17** (Existe) |
| 2 · Arrumação de saída e de permanência | Sequência, tempo, o que muda em cada uma | Cronometrar uma arrumação e registrar (Novo, curto) |
| 3 · Inspeção e liberação | Quem libera, o que bloqueia, pendências | Abas Troca, Pendências e Histórico do **Checklist 17** (Existe) |
| 4 · Enxoval e lavanderia | Jogos por unidade, mínimo, reposição, perdas | **Controle de Enxoval 13** (Existe) |
| 5 · Produtos, segurança e terceirizar ou não | Produtos de limpeza, cuidados, lavanderia própria ou terceirizada | Conta de tempo e custo por unidade limpa (Novo) |

| Material | Situação | Observação |
|---|---|---|
| E-book O03 | **Novo** | Fontes: Bíblia Operacional Zion (precisa do OK do Bruno para uso, sem nomes) |
| Aula de 40 slides O03 | **Novo** | |
| Checklist de Limpeza, Inspeção e Liberação (planilha + guia de 8 páginas) | **Existe** | Ferramenta 17 |
| Checklist interativo na ZAIOS | **Adaptar** | Versão do Checklist 17 dentro da plataforma (é o checklist do protótipo) |
| Controle de Enxoval (planilha + guia) | **Existe** | Ferramenta 13 |
| Vídeos tutoriais do Checklist 17 e do Enxoval 13 | **Novo** | Existem só imagens de demonstração |
| POPs: arrumação de saída; arrumação de permanência; inspeção e liberação; enxoval e lavanderia; produtos de limpeza (com remissão a profissional de segurança) | **Novo** | O Checklist 17 dá a base de 3 deles |
| Entregável: Manual de Governança da hospedagem (POPs + checklist + estoque mínimo) | **Novo** (montado com o que existe) | |

Novos neste módulo: 1 e-book, 1 aula, 2 tutoriais, 5 POPs, 2 exercícios curtos, 1 adaptação na ZAIOS.

## Módulo 3 · Recepção, reservas e atendimento
Unidade 360°: **O02 Recepção, Reservas e Atendimento** (com partes de L03 e L04). Pilar ZAIOS: O4 Padrão escrito e V7 (planejados); V1 já existe.

Objetivos: transformar consulta em reserva; preparar a chegada; fazer check-in e check-out sem atrito (presencial ou autônomo); recuperar o serviço quando algo dá errado; cuidar do pós-estadia e da avaliação.

| Aula | Conteúdo | Exercício |
|---|---|---|
| 1 · Da consulta à reserva | Tempo de resposta, perguntas certas, objeções | **Assistente de Conversão de Reservas A07** (Existe) |
| 2 · Pré-chegada | Mensagens antes da chegada, informações, regras | **Kit de Mensagens de Chegada e Saída 11** (Existe) |
| 3 · Check-in | Presencial e autônomo; o que conferir | Roteiro de check-in da própria hospedagem (Novo, curto) |
| 4 · Durante a estadia e recuperação de serviço | Reclamação, falha, compensação | Roteiro de recuperação de serviço (Novo) |
| 5 · Check-out e pós-estadia | Saída, avaliação, objetos esquecidos, recompra | **Auditor Inteligente da Experiência A06** (Existe, parcial) |

| Material | Situação | Observação |
|---|---|---|
| E-book O02 | **Novo** | |
| Aula de 40 slides O02 | **Novo** | |
| Vídeos tutoriais A07 e A06 | **Existe** | zar-a07 e zar-a06 |
| Vídeo tutorial do Kit 11 | **Novo** | Existe só o roteiro de demonstração |
| Kit de Mensagens (planilha com 10 textos + guia) | **Existe** | Ferramenta 11 |
| Playbook de Atendimento e Reservas | **Existe** | Entregável da mini mentoria A07 |
| POPs: reserva e confirmação; pré-chegada; check-in; check-out; recuperação de serviço; objetos esquecidos | **Novo** | O Kit 11 e o A07 dão a base de 4 deles |
| Entregável: POPs da recepção + Playbook de Atendimento | **Novo** (POPs) + **Existe** (Playbook) | |

Novos neste módulo: 1 e-book, 1 aula, 1 tutorial, 6 POPs, 2 exercícios curtos.

## Módulo 4 · Precificação e revenue management
Unidade 360°: **L05 Marketing Digital, Preço e Sazonalidade** (com base em D02, F02 e F04). Pilar ZAIOS: G3 Indicadores (existe), V6 Preço e canais (planejado), P2 Mercado (existe).

Objetivos: calcular a diária mínima; ler a faixa de preço do mercado; montar calendário de preço por temporada e dia da semana; definir mínimo de noites e cancelamento; conhecer o custo de cada canal; ler ocupação, diária média e RevPAR para ajustar.

| Aula | Conteúdo | Exercício |
|---|---|---|
| 1 · A diária mínima | O piso: custo por noite vendida e margem | **Planilha Diária Mínima** (Existe) |
| 2 · O preço do mercado | Concorrentes e faixas por temporada | **ZAIOS P2 Mercado** (Existe) |
| 3 · Calendário de preço | Temporadas, fim de semana, eventos, mínimo de noites | **Precificador Inteligente A02** (Existe) |
| 4 · Canais e custo de distribuição | Comissões, venda direta, dependência de plataforma | Custo por canal no **G2** (Existe, parcial) |
| 5 · Ler e ajustar | Ocupação, diária média, RevPAR, pior mês | **ZAIOS G3 Indicadores** (Existe) |

| Material | Situação | Observação |
|---|---|---|
| E-book L05 | **Novo** | Reaproveitar D02 (mercado), F02 (receita) e F04 (KPIs), sem repetir |
| Aula de 40 slides L05 | **Novo** | |
| Vídeos tutoriais A02 e A01 | **Existe** | zar-a02 e zar-a01 |
| Vídeo tutorial do G3 na ZAIOS | **Novo** | |
| Planilha Diária Mínima | **Existe** | Ferramenta 01 |
| Calendário de preço de 12 meses | **Adaptar** | O A02 já gera faixas; falta a planilha do calendário (pode virar o pilar V6 da ZAIOS) |
| POPs: revisão semanal de preço; regras de desconto, mínimo de noites e cancelamento | **Novo** | |
| Entregável: Plano de Preço de 12 meses + Painel de Indicadores (G3) | **Adaptar** + **Existe** | |

Novos neste módulo: 1 e-book, 1 aula, 1 tutorial, 2 POPs, 1 adaptação (calendário).

## Resumo do que os quatro módulos pedem de novo

| Tipo | Existe e entra como está | Novo a produzir |
|---|---|---|
| E-books | 0 (há capítulos reaproveitáveis em F02, F04, D02) | 4 (G04, O03, O02, L05) |
| Aulas de 40 slides | 0 | 4 |
| Ferramentas | 11 (G2, G3, P2, A02, A03, A06, A07, Diária Mínima, Kit 11, Checklist 17, Enxoval 13) | 2 adaptações (checklist interativo, calendário de preço) |
| Vídeos tutoriais | 5 (A01, A02, A03, A06, A07) | 5 (G2, G3, Checklist 17, Enxoval 13, Kit 11) |
| POPs | 0 | 15 |
| Exercícios curtos | vários dentro das ferramentas | 7 |

Todos os novos itens usam a fábrica existente (e-book, aula, tutorial e planilha). Nada é produzido antes da sua validação.

## Decisões para validar
1. O roteiro de teste (Entrega 1) está claro para você executar?
2. A ordem de revisão dos 17 materiais (Entrega 2), começando por F01, F02 e F03.
3. A estrutura de 5 aulas por módulo e a lista de materiais (Entrega 3).
4. Autorização para usar a Bíblia Operacional Zion como fonte dos módulos 2 e 3, sem nomes.
5. Não produzir a "Planilha financeira por imóvel" do catálogo, porque o G2 já cobre.
