# Plano de implementação · O9 (valor de saída com EBITDA negativo)

Comando 05G-B · 09/11/2026 · **Plano. Não implementado.** A simulação abaixo foi feita numa **cópia descartável**, na área temporária da sessão. O código da ZAIOS e o Lovable não foram alterados.

**Regra aprovada (O9):** valor de saída por múltiplo = MAX(0, EBITDA × múltiplo). Dívidas, obrigações e custos de encerramento ficam separados. Hoje não são modelados na ZAIOS e continuam fora, com aviso no texto.

## 1. Arquivos e funções afetados (commit `ec21ad5`)

| Arquivo | Linha | O que faz hoje | Muda? |
|---|---|---|---|
| `src/calc/viabilidade.ts` | 31 | `valorSaida = múltiplo × EBITDA do regime` (pode ser negativo) | **Sim: é a única mudança de cálculo** |
| `src/calc/viabilidade.ts` | 33–35 | `comSaida` soma a saída ao último ano | Não (recebe a saída já limitada) |
| `src/exercicios/viabilidade-calculo.ts` | 118 | `estudoFluxo`: VPL com saída (cenário base, cenários e CAPEX +25%) | Não (herda) |
| `src/exercicios/viabilidade-calculo.ts` | 121–122 | Saída e fluxo com saída (TIR com saída) | Não (herda). Proposta: expor o sinal "saída zerada" no estudo |
| `src/calc/viabilidade.ts` | 155–158 | Passo 4 da régua usa o VPL com saída quando o VPL sem saída é negativo | Não (ver seção 4) |
| `src/components/zion/ResultadoViabilidade.tsx` | 59 | Rótulo "Valor de saída no ano 10 (múltiplo × EBITDA do regime)" | Sim: nota quando a saída for zerada |
| `src/lib/dossie.ts` | 206 | Frase "VPL com saída … (valor de saída …)" | Sim: mesma nota |
| `src/calc/FORMULAS.md` | — | Não documenta o valor de saída | Sim: acrescentar a regra |
| `src/test/viabilidade.test.ts` | 18, 29–31, 43 | Testa a saída só com EBITDA positivo | Acrescentar casos (EBITDA negativo e zero), sem mudar os existentes |

## 2. Comportamento atual

| Cenário | EBITDA | Saída hoje | VPL com saída hoje |
|---|---|---|---|
| C1 (05F) | −R$ 15.419,63 | −R$ 92.517,75 | −R$ 927.012,89 (pior que sem saída, −R$ 891.343,30) |
| B4 (05G-B) | −R$ 58.712,25 | −R$ 293.561,25 | −R$ 1.392.929,39 |

## 3. Alteração proposta

1. `valorSaida`: devolver `Math.max(0, múltiplo × EBITDA)`.
2. Expor no estudo um sinal `saidaZerada` (verdadeiro quando múltiplo × EBITDA < 0), para a tela e o dossiê.
3. Tela e dossiê: "EBITDA negativo: o valor de saída por múltiplo foi considerado zero. Dívidas, obrigações e custos de encerramento não estão incluídos."
4. `FORMULAS.md`: registrar a regra.
5. `viabilidade.test.ts`: acrescentar testes de EBITDA negativo, zero e positivo. **Os testes existentes não mudam.**

## 4. Impacto previsto (simulado na cópia descartável)

| Suíte | Campos | Mudaram | Quais |
|---|---|---|---|
| 05C/05D/05E (`run.js`) | 237 casos | **0** | Nenhum (nenhum caso tem EBITDA negativo) |
| 05F (`run_05f.js`) | 288 | **3** | C1: valor de saída (−92.517,75 → 0); VPL com saída (−927.012,89 → −891.343,30); VPL com saída do cenário conservador (−1.229.017,62 → −1.107.050,58) |
| 05G-B Teste B (`run_05g.js`) | 188 | **3** | B4: saída (−293.561,25 → 0); VPL com saída (−1.392.929,39 → −1.298.410,53); VPL com saída conservador (−1.636.932,91 → −1.483.134,49) |
| Aceite 05G-A | 11 | O9-1 passa a PASSA; O9-2 continua PASSA | — |

**Efeitos sobre os indicadores:**
- **VPL com saída:** passa a ser igual ao VPL sem saída quando o EBITDA é negativo.
- **TIR com saída:** igual à TIR sem saída. Nos dois cenários negativos continua não existindo, por falta de troca de sinal.
- **Payback simples e descontado:** **não mudam**, porque usam o fluxo sem saída.
- **Régua (passo 4):** não muda. Com EBITDA negativo, o VPL com saída já era negativo e continua negativo, então o passo segue "redesenhar".
- **Sensibilidade e estresse de receita:** não mudam (usam o VPL sem saída).

## 5. Testes

**Aceite** (esperados independentes, `aceite_05g/esperados_aceite_05g.json`):

| Teste | Critério |
|---|---|
| O9-1 | C1: saída = 0; VPL com saída = VPL sem saída = −R$ 891.343,30; TIR com saída inexistente |
| O9-2 | C2: saída = R$ 3.312.531,36 (sem mudança) |
| O9-3 | EBITDA = 0 → saída = 0 |
| Interface | O C1 mostra a nota de "saída zerada" na tela e no dossiê |

**Regressão:** as 4 suítes da tabela da seção 4. As únicas diferenças aceitas são as 6 listadas (3 no 05F e 3 no 05G-B). Os testes próprios da ZAIOS também precisam passar, ver `RESULTADOS_VITEST.md`.

## 6. Reversão

- **Pelo GitHub privado (se autorizado):** a mudança vai num commit isolado, revertido com `git revert`.
- **Pelo Lovable:** usar o histórico de versões do projeto para voltar ao commit anterior. A reversão também pode gastar créditos; confirmar no painel.
- Respostas e dossiês já salvos guardam o resultado antigo e só mudam quando o membro recalcula. Não há migração de dados.

## 7. Critérios para interromper a implementação

1. O projeto não estiver mais no commit `ec21ad5` no início, sem nova matriz de impacto.
2. Qualquer campo das suítes mudar fora das 6 diferenças previstas.
3. Qualquer teste próprio da ZAIOS existente falhar.
4. O diff da alteração tocar em mais arquivos que os da seção 1.
5. Houver consumo de créditos acima do autorizado.
6. Qualquer dúvida sobre dívidas e custos de encerramento exigir modelagem nova. Isso fica fora da O9.
