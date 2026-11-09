# Plano de testes e homologação financeira · Academy e ZAIOS

Versão 0.1 · 09/11/2026 · Comando 05B · **Plano, não executado como homologação.** Os resultados abaixo vêm da auditoria de 09/11; a homologação formal depende do "aprovado" do Bruno.

## 1. Objetivo

Garantir que todas as ferramentas da Zion sigam o dicionário financeiro (`DICIONARIO_FINANCEIRO.md`):
- Em premissas iguais, dão o mesmo número quando o escopo é igual.
- Explicam a diferença quando o escopo é diferente.

A homologação da ZAIOS como referência central é a etapa 1: as outras ferramentas são conferidas contra ela.

## 2. Etapas

1. **Homologar a ZAIOS v0:**
   - Rodar os casos de referência abaixo.
   - O Bruno (com o contador, se quiser) confere premissas e resultados.
   - Aprovar como dicionário v1.0.
2. **Conferir cada ferramenta** contra os cenários equivalentes. Para cada uma: passa, diferença legítima (rotulada) ou erro (correção proposta).
3. **Aplicar as correções aprovadas, uma por vez.** Cada correção vem com:
   - teste novo que falha antes e passa depois;
   - relatório;
   - versão do dicionário.
4. **Regressão:** a cada mudança, os testes de todas as ferramentas rodam de novo.

## 3. Cenários de teste (dados fictícios)

### T1 · Z-base (premissas aceitas por todas as ferramentas de resultado)

- **Operação:** 3 unidades; diária R$ 680; ocupação 38%; 365 dias; sem sazonalidade, rampa ou reajuste.
- **Custos:** deduções 17%; variável R$ 80/noite; fixo R$ 6.000/mês; sem quebra, retirada ou reserva.
- **Investimento:** R$ 900.000 sem contingência; taxa 10%; 10 anos; sem saída.

| Resultado esperado | Valor | Tolerância |
|---|---|---|
| Receita bruta/ano | 282.948,00 | R$ 0,01 |
| Receita real | 234.846,84 | R$ 0,01 |
| Resultado operacional | 129.558,84 | R$ 0,01 |
| Ocupação de equilíbrio | 13,57% | 0,01 p.p. |
| VPL a 10% | −103.917,01 | R$ 0,01 |
| TIR | 7,24% | 0,01 p.p. |
| Payback simples | 6,95 anos | 0,01 ano |
| Payback descontado | não ocorre em 10 anos | — |
| Retorno anual | 14,40% | 0,01 p.p. |
| Retorno acumulado 10 anos | 43,95% | 0,01 p.p. |

**Resultado da auditoria de 09/11:**
- ZAIOS (regra) e B08: passam todos.
- A09: passa com 365 dias; o campo inteiro de noites por mês impede 365 (limitação D5).

### T2 · Z-completo (regras Zion completas)

T1 + quebra de 1% + reserva de reposição de 3% da receita bruta + rampa do 1º ano (40/50/75%), calendário real.

| Resultado esperado (ZAIOS) | Sem rampa | Com rampa |
|---|---|---|
| Resultado operacional (regime) | 126.729,36 | 126.729,36 |
| Geração de caixa (regime) | 118.240,92 | 118.240,92 |
| Geração do 1º ano | 118.240,92 | 42.405,16 |
| VPL a 10% | −173.460,73 | −242.402,34 |
| TIR | 5,30% | 3,71% |
| Payback simples | 7,61 | 8,25 |
| VPL com saída 6× EBITDA | +119.697,19 | +50.755,59 |

Aplica-se à ZAIOS e, depois das correções D2, D3 e D7, ao B08. A09 e Folha J2 só nas partes que tiverem.

### T3 · Casos de referência F01, F02 e F03 (já usados na ZAIOS)

| Caso | Esperado |
|---|---|
| F01 CAPEX | 1.237.400 (infra 250.000; projeto 70.000; obra 390.000; apoio 90.000; FF&E 195.000; OS&E 12%; pré-abertura 5% da base; contingência 25% da base) |
| F02 Receitas | 3 unidades, diária 680, ocupação 38%, deduções 17%, fixo 10.500/mês → receita real 234.846,84; resultado operacional 108.846,84; equilíbrio 223,25 noites (20,4%) |
| F03 Caso 1 | VPL −1.110.447,78; payback 38,6 anos; TIR com saída −8,4% → Redesenhar |
| F03 Caso 2 | Payback 5,75; descontado 8,82; VPL sem saída 92.549,78; com saída 624.599,52 |

### T4 · Orçamento (B06, F05, ZAIOS P5)

Escopo diferente, então não se espera o mesmo total. Testa-se a regra:
- contingência fora do capital de giro (B06 e ZAIOS);
- contingência e reserva explicadas no texto (F05);
- custo por unidade e custo por m² com as mesmas fórmulas.

Casos:
- Perfis oficiais do B06 (capex 449.500; intermediário 524.450; conservador 598.617,50).
- Exemplo da F05 (subtotal 197.040; reserva 19.704; total 216.744).
- F01 na ZAIOS.

### T5 · Folha Única J2 x ZAIOS G2/G3 (mês real)

Mesmo mês lançado nas duas. Devem coincidir:
- receita bruta, deduções, receita real;
- custos, resultado operacional;
- diária média, RevPAR, custo por noite.

Diferenças legítimas: meses de fôlego x cobertura da reserva (D12) e taxa de limpeza (D14).

### T6 · Limites e erros

- Ocupação 0% e 100%.
- Diária menor que o custo variável (sem equilíbrio).
- Fixo zero.
- Investimento zero.
- Fluxo sem troca de sinal (sem TIR).
- Fluxo com duas trocas (aviso de várias TIR).
- Payback acima de 10 anos (estendido x nulo).
- Campos "não sei".
- Diária "500.50" e unidades "2,5" (leitura de número).

## 4. Critérios de homologação

Uma ferramenta é homologada quando:
1. Passa T1 (ou declara a limitação com rótulo, como o A09).
2. Passa os cenários do seu escopo (T2 a T5).
3. Usa os nomes e rótulos do dicionário (seção 7 dele).
4. Mostra o tipo de cada valor (ilustrativo, referencial, comprovado, calculado).
5. Tem testes automáticos versionados no repositório.

**Situação em 09/11/2026:** nenhuma ferramenta está homologada. A ZAIOS v0 e o B08 passam T1. O A09 passa T1 com ressalva (D5). B06 e F05 têm testes próprios passando (59 de 59 e 33 de 33) e aguardam T4.

## 5. Responsáveis

| Ferramenta | Sessão | Testes existentes |
|---|---|---|
| ZAIOS | ZAIOS platform development | 396 testes (Vitest) no Lovable |
| B06, B08, A09 | Zion Arsenal | `producao/zion-arsenal/tests/profiles/*.json` + `tests/run.js` |
| F05 | Zion infoprodutos catálogo | `producao/utilitarios/05-orcamento-cabana/tests/test_planilha.py` |
| Folha Única J2 | Marketing da Zion install | `producao/jornada2/02-financas/tests/` |

Os cenários T1 a T6 devem virar arquivos de teste no formato de cada ferramenta, **depois do "aprovado"**.
