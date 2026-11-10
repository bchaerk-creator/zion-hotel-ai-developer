# Jornada 2 · Gestão · Módulo 6 · Compras, estoque e manutenção · Plano da lição (G06)

Status: plano de produção (10/11/2026). Entregável: **Matriz de Compras e Manutenção** (página 6 do Plano de Gestão): Matriz de Compras com os itens que mais pesam, três cotações, consumo por noite e por hóspede, contrato, estoque mínimo e ponto de pedido, e o calendário de manutenção preventiva de 12 meses com a reserva de manutenção. Não altera outros módulos nem ferramentas existentes; aponta, sem alterar, para as Ferramentas 13 (Controle de Enxoval e Reposição, `docs/p/adbc67069af26ae0/enxoval-13/`), 14 (Quadro de Ocorrências e Manutenção, `ocorrencias-14/`) e 18 (Planner de Manutenção Preventiva, `manutencao-18/`).

## 1. A lição em uma frase
Aprenda o passo a passo para listar o que você mais compra, comparar três cotações, saber o consumo por noite e por hóspede, definir o estoque mínimo e o ponto de pedido, e montar o calendário de manutenção preventiva de doze meses.

## 2. Públicos e jornadas
- Desenvolvedor (vai abrir): usa o consumo previsto e cotações reais da região; a Matriz vira a lista de compras de abertura e o calendário do primeiro ano. A ficha avisa.
- Gestor (dono que opera): público central; usa três meses de notas e a Folha Única do Mês (Módulo 2).
- Operador: monta a Matriz para propor ao dono (contratos e limite de compra são decisões do dono).
Jornada A (quero começar) e B (já opero) tratadas na abertura, como nos módulos anteriores.

## 3. Fontes Zion e convenções
- **Panorama, Trilha B, G5 Compras e Fornecedores**: "Compras não é detalhe administrativo. É onde a margem some sem fazer barulho."; pergunta central "O que se compra, de quem, e sob que contrato?"; passos 01 lista por valor ("Os cinco primeiros itens costumam responder pela maior parte do custo variável"), 02 três cotações, 03 contrato nos recorrentes, 04 consumo por hóspede ("amenities, enxoval, café, gás e energia por diária vendida"); na prática, três jogos por cama; erro comum, comprar sempre do mesmo fornecedor sem cotar. Entregável da fonte: "A Matriz de Compras com três cotações por item e a tabela de custo por hóspede."
- **Jornada do COMO · Etapa 09**: consumo = gasto de três meses ÷ diárias vendidas; amortização do enxoval e reposição por perda; reserva de manutenção de 3% a 6% da receita por mês (Passo 06).
- **Etapa 10**: compras e reposição (procedimento semanal) e manutenção preventiva (mensal, risco alto) na Ordem de Escrita; "Manutenção preventiva, com o calendário do ano"; critério de compra fora do previsto (exemplo da fonte: até R$ 300); "manutenção adiada que vira conserto".
- **Bíblia Operacional Zion (Notion)**: Controle de Estoque ("Atualizar toda segunda-feira. Quando item atingir o mínimo, acionar fornecedor imediatamente"; enxoval mínimo de 3 jogos; histórico de compras); Manual Gerencial (estoque diário e semanal, revisão mensal de fornecedores e custos); Manual Técnico e Manutenção (ronda técnica diária de 8 itens); Parceiros e Fornecedores (frequências de controle de pragas, dedetização); regra do projeto "trabalhar em baixa ocupação, preferencialmente segunda a quinta".
- Vocabulário para o membro: "custo variável por noite" e "noite vendida" (= diária vendida), "consumo por hóspede", "ponto de pedido", "reserva de manutenção". Sem siglas na tela. "DRE" só aparece no resumo, dentro da citação da fonte, com a explicação.
- Mapa de fontes completo fora do repositório (`scratchpad/fontes/MAPA_FONTES_compras.md`).

## 4. Objetivos (verbos observáveis)
1. Explicar por que compras é onde a margem some sem barulho e por que a lista se faz por valor (compreender).
2. Calcular o consumo por noite vendida e por hóspede de três meses de notas e conferir com o custo variável da Folha (aplicar).
3. Comparar três cotações por item e calcular a diferença na mesma quantidade, sem tratá-la como previsão (aplicar, avaliar).
4. Calcular o estoque mínimo e o ponto de pedido e decidir o pedido de hoje (aplicar).
5. Montar o calendário de manutenção preventiva de doze meses e conferir se a reserva de manutenção cobre o plano mês a mês (criar, avaliar).
6. Identificar a causa principal pelas regras da fonte e escrever um plano com prazo (avaliar, criar).

## 5. As seis etapas
| Etapa | Peça | Duração |
|---|---|---|
| Diagnosticar | Abertura da ficha: situação e 4 perguntas (lista por valor? três cotações? mínimo escrito? calendário?) → nível 1 a 4 | 1 min |
| Compreender | Aula em vídeo (13 cenas, cerca de 6 min) + resumo em PDF (8 páginas) | 6 min + leitura |
| Observar | Tutorial da ficha com o exemplo "Cabanas do Vale" (continuação dos módulos 0, 2 e 3) | 4 min |
| Executar | Ficha "A minha Matriz de Compras e Manutenção" (5 telas) + planilha | 25 a 40 min |
| Validar | Resultado em cinco partes + critério de conclusão (selo) | 3 min |
| Entregar | PDF (página 6 do Plano) + plano de ação + próxima etapa (Módulo 7) + prompt de IA | 2 min |

## 6. Regras da ferramenta (testáveis, `src/logic.js`)
### 6.1 Entradas
Consumo: `mesesPeriodo` (1 a 12, padrão 3; aviso abaixo de 3), `noitesPeriodo` (inteiro ≥ 1), `hospedesPeriodo` (opcional), `unidades` (inteiro ≥ 1), `custoVariavelNoite` (opcional, aviso se faltar). Botão "Trazer os números da minha Folha Única" lê `zion-t2-financas` com a lógica do Módulo 2 (custo variável por noite, unidades, receita real), sem alterá-la.
Matriz (até 8 itens): nome, unidade, gasto no período, tipo (variável ou vendido à parte), preço de hoje, três cotações, contrato (tem, vou fechar, sem contrato); `prazoContratos` obrigatório se houver "vou fechar". Bloqueios: sem item, item sem nome, sem gasto ou sem tipo, número inválido, negativo, cotação sem preço de hoje. Avisos: menos de 5 itens; item com 1 ou 2 cotações.
Estoque (até 10 itens): nome, unidade, uso por mês, prazo de entrega, dias de segurança (padrão 7), estoque de hoje, intervalo de compra em dias (padrão 30); enxoval: camas e jogos (jogos obrigatórios se houver camas).
Manutenção: `ano` (2024 a 2099), `mesInicio`, `receitaReserva`, `reservaPct` (aviso fora de 3 a 6%), meses de casa cheia, tarefas (até 15: nome, frequência mensal/bimestral/trimestral/semestral/anual, primeiro mês, custo por vez, quem faz). Aviso com menos de 3 tarefas.
Rotina: dia da contagem, quem compra, limite de compra fora do previsto (R$), ronda diária (sim/não), registro de ocorrências (sim/não).

### 6.2 Cálculo
- Por noite = gasto ÷ noites do período; por hóspede = gasto ÷ hóspedes; peso = gasto ÷ total; posição por valor.
- Itens variáveis por noite = Σ gasto dos variáveis ÷ noites; cobertura = ÷ custo variável por noite da Folha; mês cheio = variáveis por noite × unidades × 30.
- Quantidade = gasto ÷ preço de hoje; diferença = quantidade × (preço de hoje − menor cotação), só se positiva; em doze meses = diferença × 12 ÷ meses (conta, não previsão).
- Estoque (definição-padrão, declarada): consumo por dia = uso do mês ÷ 30; mínimo = ⌈consumo por dia × segurança⌉; ponto de pedido = ⌈consumo por dia × (entrega + segurança)⌉; pedir quando estoque de hoje ≤ ponto de pedido; pedido = ⌈ponto de pedido sem arredondar + consumo por dia × intervalo − estoque de hoje⌉. Arredondamento protegido contra erro de ponto flutuante (100 ÷ 30 × 12 = 40).
- Enxoval: jogos ÷ camas; faltam = 3 × camas − jogos.
- Calendário: a tarefa cai no mês quando ((mês − primeiro mês) mod 12) mod passo = 0 (passo 1, 2, 3, 6, 12). Custo do mês = Σ custos; reserva do mês = receita × percentual; reserva e gasto acumulados mês a mês; "não cobre" quando o gasto acumulado passa da reserva acumulada; tarefa pesada (semestral ou anual) em mês de casa cheia.

### 6.3 Leituras (regras das fontes, sem nota)
Peso por valor; consumo e conferência com a Folha (cobre, acima ou sem Folha); mês cheio; cotações (diferença ou já paga a menor); contratos; estoque no ponto de pedido; enxoval; calendário (tarefas, total, mês mais pesado); reserva (cobre ou não cobre, com o mês); casa cheia.

### 6.4 Causa principal e prioridades (até três, nesta ordem)
1 item sem três cotações → 2 compra recorrente sem contrato → 3 item no ponto de pedido → 4 menos de três jogos por cama → 5 manutenção pesada na casa cheia → 6 a reserva não cobre o plano → 7 sem ronda diária ou sem registro de ocorrências → 8 estoque sem dia de contagem ou compra sem limite. Nada dispara: "Compras e manutenção dentro das regras da fonte". A ordem segue os passos do G5 (cotar, contratar, consumir) e deixa manutenção e rotina para depois (elaboração declarada).

### 6.5 Critério de conclusão (selo)
Pelo menos três itens com preço de hoje e três cotações, pelo menos um item de estoque, calendário de 12 meses com pelo menos três tarefas, telas sem bloqueio; plano de ação com 10 letras ou mais e prazo; PDF baixado.

## 7. Telas da ficha
0 Abertura → 1 O período e o consumo → 2 A Matriz de Compras → 3 Estoque mínimo e ponto de pedido (e enxoval) → 4 O calendário de manutenção → 5 A rotina → Resultado (itens variáveis por noite em destaque; 1 a Matriz em cartões, estoque, enxoval, calendário; 2 significado; 3 atenção; 4 o que fazer; 5 como verificar; próxima etapa Módulo 7; complementos: planilha e Ferramentas 13, 14 e 18).

## 8. Planilha "Matriz de Compras e Manutenção" (em branco e exemplo)
Abas: Comece aqui · Matriz de Compras (período, 8 itens, resumo, situação) · Estoque (10 itens, enxoval) · Manutenção 12 meses (reserva, 15 tarefas, calendário com casa cheia, reserva acumulada, situação) · Rotina e checklist (rotina e 10 itens do mês) · Resumo (números da página 6, oito sinais e causa principal na ordem da ficha). Testada no LibreOffice contra conta independente em Python.

## 9. Exemplo didático (dados fictícios, conferido duas vezes: lógica e planilha)
Cabanas do Vale, 4 unidades, a mesma dos módulos 0, 2 e 3. Três meses de notas: **174 noites vendidas** (58 por mês, como na Folha de outubro), **150 hóspedes**. Custo variável por noite da Folha: **R$ 28,32**.
| # | Item | Período | Peso | Por noite | Por hóspede | Hoje → menor | Diferença | Contrato |
|---|---|---|---|---|---|---|---|---|
| 1 | Café da manhã e cestas (vendido à parte) | 1.260 | 32,3% | 7,24 | 8,40 | 28,00 → 25,50 (45 cestas) | 112,50 | vou fechar |
| 2 | Lavanderia do enxoval | 900 | 23,1% | 5,17 | 6,00 | 3,00 → 2,60 (300 kg) | 120,00 | tem |
| 3 | Amenidades | 780 | 20,0% | 4,48 | 5,20 | 10,40 → 8,90 (75 kits) | 112,50 | vou fechar |
| 4 | Gás do aquecimento da água | 720 | 18,5% | 4,14 | 4,80 | 120 → 112 (6 botijões) | 48,00 | sem contrato |
| 5 | Reposição de enxoval | 240 | 6,2% | 1,38 | 1,60 | 120 → 98 (2 jogos) | 44,00 | vou fechar |
Total **R$ 3.900**; variáveis R$ 2.640 → **R$ 15,17 por noite**, **53,6%** dos R$ 28,32 (resto R$ 13,15: limpeza por estadia 8,62, energia elétrica 1,72, quebra 2,80, todos da Folha). **Coerência com o Módulo 2:** a Matriz abre linhas da Folha de outubro: enxoval R$ 380 = lavanderia 300 + reposição 80; amenidades 260; energia variável R$ 340 = gás 240 + elétrica 100; café e cestas R$ 420 = custo das outras receitas. Mês cheio (4 × 30 noites): **R$ 1.820,69**. Diferença para a menor cotação: **R$ 437,00** no período, **R$ 1.748,00** em doze meses (conta, não previsão). Contratos a fechar até 31/03/2027.
Estoque (segurança 7 dias): kit de amenidades 25/mês, entrega 7, hoje 14 → mínimo 6, ponto 12, ok; papel higiênico 100/mês, entrega 5, hoje 30 → mínimo 24, ponto 40, **pedir 110**; botijão 2/mês, entrega 2, hoje 2 → 1/1, ok; café em pó 8/mês, entrega 3, hoje 6 → 2/3, ok. O uso por mês do kit (25) e do botijão (2) bate com as quantidades da Matriz (75 kits e 6 botijões em três meses). Enxoval: 10 jogos, 4 camas → **2,5 por cama**, faltam 2.
Manutenção 2027 (casa cheia: jun, jul, ago, dez): filtros do ar-condicionado trimestral (jan) R$ 0; controle de pragas trimestral (fev) 180; aquecedor a gás anual (mar) 280; revisão elétrica anual (abr) 350; calhas semestral (abr) 150; caixa d'água semestral (mai) 250; ar-condicionado por técnico anual (set) 480; extintores anual (out) 160; deck anual (nov) 900. Mês a mês: 0 / 180 / 280 / 500 / 430 / 0 / 0 / 180 / 480 / 310 / 1.330 / 0 → **17 tarefas, R$ 3.690**; mês mais pesado novembro (R$ 1.330, na baixa). Reserva de **3%** da receita real de R$ 13.565,60 (Folha) = **R$ 406,97 por mês, R$ 4.883,62 no ano**; cobre o plano em todos os meses; sobra **R$ 1.193,62**. Nenhuma tarefa pesada na casa cheia.
Rotina: contagem às segundas-feiras, compras com Ana (dona), limite de R$ 300, ronda e registro de ocorrências: sim.
Causa principal: **compra recorrente sem contrato** (gás). Prioridades: contrato, pedido (papel), enxoval. Diagnóstico: um sim (mínimo escrito) → nível 1 "Compra no susto".

## 10. Versão autônoma e acompanhada
Mesmo conteúdo; no acompanhamento a Matriz é revisada pela equipe Zion no marco da semana 6 (coerência das contas, cotações reais, calendário compatível com a casa cheia) e a prioridade 1 vira compromisso do encontro.

## 11. Lacunas das fontes e elaborações declaradas
- A fonte não define estoque mínimo nem ponto de pedido: a ficha usa a definição-padrão de gestão de estoque, dita como tal; dias de segurança e intervalo são decisões do membro (exemplo: 7 dias).
- A fonte não dá frequências de manutenção além da ronda diária da Bíblia e das frequências de pragas e dedetização da página de fornecedores: as do exemplo são didáticas, e a ficha manda seguir o manual do fabricante e o profissional responsável.
- O pilar O4 Manutenção e Ativos aparece só pelo nome no Panorama extraído (sem conteúdo): o calendário apoia-se na Etapa 10, na Etapa 09 e na Bíblia.
- A fonte não fixa prazo de contrato nem quantas cotações por período; a ficha exige data para os contratos marcados "vou fechar".
- A reserva de manutenção do exemplo é de 3% (mínimo da faixa da fonte, pedido para este módulo); a Folha do Módulo 2 usa 4% como reserva de reposição. Pendência para o Bruno (REGISTRO.md).
- Regra do calendário por frequência, conferência com a Folha, "mês cheio" e ordem dos oito sinais: elaborações desta lição.

## 12. Compatibilidade com o ZAIOS
Chave local `zion-t2-compras`; estado com `situacao`, `diag`, `mesesPeriodo`, `noitesPeriodo`, `hospedesPeriodo`, `unidades`, `custoVariavelNoite`, `itens[]`, `prazoContratos`, `estoque[]`, `camas`, `jogos`, `ano`, `mesInicio`, `receitaReserva`, `reservaPct`, `casaCheia[]`, `tarefas[]`, `diaContagem`, `quemCompra`, `alcada`, `ronda`, `ocorrencias`, `acao`, `prazo`, `pdf`. A lógica roda igual no Node.
