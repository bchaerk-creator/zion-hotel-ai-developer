# Testes de composição complementar (Teste B)

Comando 05G-B · 09/11/2026 · Execução local da cópia da ZAIOS (commit `ec21ad5`), sem alterar nada.

**Hipóteses exclusivamente de teste:**
- reserva de reposição de 4% e quebra de 1%: servem só para exercitar as fórmulas e não são parâmetros aprovados para uso;
- taxas e múltiplos alternativos (8%, 10%, 12%; 5×, 6×, 8×) são H4.

## 1. Cenários

| Cenário | Base (05F) | Pró-labore | Reserva | Quebra | Contingência | Taxa | Múltiplo |
|---|---|---|---|---|---|---|---|
| B1 | C2 (intermediário, sazonal, outras receitas) | 40 h/sem × R$ 40/h | 4% | 1% | 20% | 10% | 6× |
| B2 | C2 | idem | 4% | 1% | 20% | 12% | 5× |
| B3 | C2 | idem | 4% | 1% | 20% | 8% | 8× |
| B4 | C1 (resultado negativo) | 20 h/sem × R$ 40/h | 4% | 1% | 25% | 12% | 5× |

- Entradas: `testes/financeiro/composicao_05g/cenarios_05g.json`, sobre os cenários do 05F.
- Esperados independentes: `composicao_05g_referencia.py` → `esperados_05g.json`. O script é escrito em Python e não usa código da ZAIOS.
- Executor: `run_05g.js`.

## 2. Resultado

| Cenário | Campos | OK | Divergência matemática | Não aplicável |
|---|---|---|---|---|
| B1 | 47 | 46 | 0 | 1 |
| B2 | 47 | 46 | 0 | 1 |
| B3 | 47 | 46 | 0 | 1 |
| B4 | 47 | 42 | 0 | 5 |
| **Total** | **188** | **180** | **0** | **8** |

- **Zero divergências matemáticas.** A maior diferença absoluta foi de 1.2e-09 (ruído de ponto flutuante). As tolerâncias são as do 05F.
- "Não aplicável" são indicadores que não existem no cenário e que a ZAIOS também não apresenta: payback descontado fora do horizonte em B1 a B3; payback e TIR no B4.

Evidência: `testes/financeiro/resultados/2026-11-09-05g-b-teste-b/` (`resultado_05g.json`, `RESULTADO_05G_TESTE_B.md`).

## 3. Valores principais (esperado independente = ZAIOS)

| Indicador | B1 (10%, 6×) | B2 (12%, 5×) | B3 (8%, 8×) | B4 (C1 negativo, 12%, 5×) |
|---|---|---|---|---|
| Pró-labore mensal (horas × R$/h × 4,33) | 692.800,00% | 692.800,00% | 692.800,00% | 346.400,00% |
| Custos variáveis (com quebra de 1%) | R$ 92.978,64 | R$ 92.978,64 | R$ 92.978,64 | R$ 18.012,75 |
| Custos fixos com pró-labore (ano) | R$ 419.136,00 | R$ 419.136,00 | R$ 419.136,00 | R$ 149.568,00 |
| EBITDA do regime | R$ 457.266,72 | R$ 457.266,72 | R$ 457.266,72 | R$ -58.712,25 |
| Reserva de reposição 4% (ano) | R$ 53.943,36 | R$ 53.943,36 | R$ 53.943,36 | R$ 6.898,50 |
| Geração de caixa do regime (EBITDA − reserva) | R$ 403.323,36 | R$ 403.323,36 | R$ 403.323,36 | R$ -65.610,75 |
| Contingência | R$ 302.400,00 | R$ 302.400,00 | R$ 302.400,00 | R$ 135.000,00 |
| CAPEX com contingência | R$ 2.402.400,00 | R$ 2.402.400,00 | R$ 2.402.400,00 | R$ 885.000,00 |
| Giro A (6 × fixo do P5, sem pró-labore) | R$ 168.000,00 | R$ 168.000,00 | R$ 168.000,00 | R$ 54.000,00 |
| Giro B (déficit + meses negativos + 3 × fixos com pró-labore) | R$ 175.209,50 | R$ 175.209,50 | R$ 175.209,50 | R$ 216.432,08 |
| Captação | R$ 2.577.609,50 | R$ 2.577.609,50 | R$ 2.577.609,50 | R$ 1.101.432,07 |
| Menor saldo sem usar a contingência | R$ 407.184,00 | R$ 407.184,00 | R$ 407.184,00 | R$ 155.578,50 |
| Menor saldo com a contingência toda usada | R$ 104.784,00 | R$ 104.784,00 | R$ 104.784,00 | R$ 20.578,50 |
| Colchão | 4,36% | 4,36% | 4,36% | 2,33% |
| Payback simples | 6,83 anos | 6,83 anos | 6,83 anos | não existe (nulo) |
| Valor de saída (múltiplo × EBITDA) | R$ 2.743.600,32 | R$ 2.286.333,60 | R$ 3.658.133,76 | R$ -293.561,25 |
| VPL sem saída | R$ -245.019,74 | R$ -438.670,48 | R$ -22.876,60 | R$ -1.298.410,53 |
| VPL com saída | R$ 812.756,95 | R$ 297.467,75 | R$ 1.671.547,14 | R$ -1.392.929,39 |
| TIR sem saída | 7,81% | 7,81% | 7,81% | não existe (nulo) |
| TIR com saída | 14,95% | 14,06% | 16,52% | não existe (nulo) |
| 5 passos | passa, passa, passa, ajustar, ajustar | passa, passa, passa, ajustar, ajustar | passa, passa, passa, ajustar, ajustar | redesenhar, redesenhar, redesenhar, redesenhar, ajustar |
| Decisão | Ajustar | Ajustar | Ajustar | Redesenhar |

## 4. Leitura

1. **Pró-labore:** entra nos custos fixos e no componente "3 × fixos" do giro B, mas **não entra no giro A**, que usa o fixo do P5 sem retirada. A conta está certa e segue a regra documentada. É mais um ponto para a O12 (a base do giro precisa ser única e explícita).
2. **Reserva de reposição:** reduz a geração de caixa, mas não o EBITDA. O valor de saída usa o EBITDA. É o comportamento documentado e está coerente com a D2-C (a reserva sai depois do EBITDA).
3. **Quebra:** incide sobre as diárias, como custo variável (D3-A). Confere.
4. **Contingência:**
   - entra no CAPEX (base = infraestrutura + obra + apoio) e é retirada da curva só nos meses de obra, na hipótese "contingência toda usada";
   - no B1, o menor saldo cai de R$ 407.184,00 para R$ 104.784,00 e o colchão vai a 4,36%.
5. **Taxas e múltiplos:** mudam só o VPL e a TIR com saída. O payback e a TIR sem saída não mudam entre B1, B2 e B3, como esperado. No B3 (8%, 8×), o VPL sem saída fica perto de zero (−R$ 22.876,60): é um exemplo de como a decisão depende de parâmetros H4.
6. **B4:** o valor de saída é negativo (−R$ 293.561,25), confirmando a necessidade da O9 também com pró-labore, reserva e contingência.

## 5. Limitações

- Usa a mesma cópia da composição dos comandos anteriores; o resultado da segunda transcrição está em `TESTES_INTEGRIDADE.md`.
- Um único perfil de pró-labore por cenário. A contingência foi testada em 20% e 25%.
- A reserva e a quebra foram testadas só com os percentuais de referência.
