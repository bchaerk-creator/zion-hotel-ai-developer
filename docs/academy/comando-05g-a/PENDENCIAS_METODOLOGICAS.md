# Pendências metodológicas · Comando 05G-A

09/11/2026 · **Nenhuma destas pendências foi encerrada pela aprovação de O8 a O14.** As decisões abaixo são do Bruno. Nada aqui assume aprovação.

## 1. Pendências anteriores, preservadas

| Pendência | Situação | Registro de origem | Relação com O8 a O14 |
|---|---|---|---|
| **O6** · aluguel, gestão e marca em R$ na Folha J2 x % da receita no dicionário | Aberta | 05E | A O11 trata da base percentual na ZAIOS. A O6 (modalidade em R$ ou em %, e unidades) continua aberta para a Folha J2 e para a ZAIOS. Se o contrato puder ser em R$ fixo, a O11 precisa de uma terceira modalidade |
| **O7** · impostos como despesa variável na G2 | Aberta | 05E | Nenhuma direta. A O14 exige tributos sobre as receitas complementares no P6, não na G2 |
| **B08** · reserva no cálculo do equilíbrio (O3) | Aberta | 05D | Nenhuma |
| **A09** · gestão nas deduções (O2); 31 noites e 372 dias (D5) | Abertas | 05D/05E | A O11 define a base da gestão na ZAIOS, não no A09 |
| **B06** · regra de referência sem documento externo | Aberta | 05E | Nenhuma |
| **H4** · parâmetros e limites (taxa, múltiplo, 8/12 anos, colchão de 10%, cenários, rampa, prazos de giro) | Aberta | 05D | A O10 e a O12 dependem de limites e prazos que são H4 |
| **D5** · dias e fixos no A09 | Pendente | 05B | — |
| **D6** · base da contingência | Pendente | 05B | Contingência entra nos usos (O13) e na curva (O10) |
| **D8** · payback acima do horizonte (estender ou nulo) | Pendente | 05B | **Depende da O10:** com horizonte de 10 anos, decidir se o payback estendido continua |
| **D9** · custo variável por noite ou por estadia | Pendente | 05B | **Depende da O14:** as categorias A e B precisam de custo associado por noite, estadia ou consumo |
| **D10** · cenários de referência | Pendente | 05B | Cenários internos (−10%/−20%) afetam O14 (quais categorias variam) e O10 |
| **D12** · meses de fôlego x cobertura da reserva | Pendente | 05B | **Relacionada à O12** (prazo do giro) |
| **D13** · moeda em float x centavos | Pendente | 05B | Qualquer implementação nova (O9 a O14) precisa da mesma convenção |
| **D14** · taxa de limpeza e outras receitas | Pendente | 05B | **Depende da O14:** a taxa de limpeza pode virar categoria A. Alíquota por fonte de receita |
| **Integridade do código da ZAIOS** (hash na origem) | Aberta | 05E/05F | Pré-condição para homologar qualquer alteração |
| **Segunda transcrição da composição** | Aberta | 05F | Idem |
| **Pró-labore, reservas, quebra e contingência pela composição** | Abertos (sem teste) | 05F | A O12 cita "reservas específicas" como categoria distinta do giro |
| **Conferência externa** (contador ou analista) | Aberta | 05D | Recomendada antes da homologação das decisões implementadas |
| Divergências aprovadas e não implementadas (D1, D2-C, D3-A, D4, D7-C, D11-A) | Abertas | 05B/05D | **A O9 complementa a D7-C. A O8 complementa a D11-A.** A ordem de implementação precisa considerar as duas juntas |
| Reserva de 3–5% na ZAIOS x 3–6% aprovada (D2-C) | Aberta | 05C | Reserva de reposição ≠ capital de giro (O12) |

## 2. Novas definições necessárias para implementar O8 a O14 (decisão do Bruno)

| # | Pergunta | Decisão afetada | Bloqueia |
|---|---|---|---|
| P-O8 | Qual o rótulo da indicação preliminar do P6 (ex.: "Indicação inicial")? A régua de margem continua no P6? Quais indicadores entram no P6 (só antes ou também depois dos custos do modelo)? | O8 | Interface do P6 |
| P-O10a | Convenção de desconto no horizonte misto: mensal com taxa equivalente nos 36 meses e anual depois, ou tudo anual (agregando os meses)? | O10 | VPL, TIR, payback |
| P-O10b | Como modelar o atraso: deslocar a abertura em meses com o mesmo horizonte de calendário (a perda de receita aparece) ou estender o horizonte? | O10 | Teste O10-2 |
| P-O10c | O CAPEX e a contingência atrasam junto com a abertura, ou só a operação? | O10, D6 | Curva com atraso |
| P-O11 | Além de hospedagem e receita bruta, aceitar valor fixo em R$ (ligado à O6)? A base "receita bruta" inclui todas as categorias da O14? | O11, O6, O14 | Modelo de dados |
| P-O12 | Prazo ou método do componente de meses fixos do giro: manter 6 e 3, usar a curva de caixa (maior déficit acumulado) ou parametrizar por perfil (H4)? | O12, D12 | Cálculo do giro |
| P-O13 | O capital disponível é capital próprio destinado ao giro ou qualquer recurso do empreendedor? Ele entra na curva como saldo inicial? | O13 | Fontes e usos, curva |
| P-O14a | Lista de categorias e fatores por tipo de hospedagem (A: por noite ou por hóspede; B: ticket × adesão; C: valor anual ou mensal) | O14 | Interface e cálculo |
| P-O14b | A rampa do 1º ano e os cenários afetam as categorias B e C? | O14, D10 | Cálculo |
| P-O14c | Tributos por categoria (alíquota única ou por fonte) | O14, D14 | Cálculo |
| P-O14d | Migração: como converter o atual `outras_pct` (respostas já salvas) para a categoria A sem mudar resultados existentes sem aviso | O14 | Modelo de dados e dossiê |

**Sem resposta a estas perguntas, a implementação ficaria com premissas inventadas.** O plano marca cada uma como pré-requisito da etapa correspondente.
