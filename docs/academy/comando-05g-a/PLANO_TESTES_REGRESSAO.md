# Plano de testes de regressão e aceite · O8 a O14

Comando 05G-A · 09/11/2026 · **Testes preparados, não homologados.** Os esperados foram calculados de forma independente, a partir das decisões aprovadas, sem usar código da ZAIOS:
- script: `testes/financeiro/aceite_05g/aceite_05g_referencia.py`;
- esperados: `esperados_aceite_05g.json`.

Os testes usam os cenários do 05F (entradas em `testes/financeiro/composicao_05f/cenarios_05f.json`).

## 1. O que foi executado neste comando e o que não foi

| Item | Situação |
|---|---|
| Cálculo independente dos esperados (20 testes + 1 de integração) | **Executado** |
| Linha de base contra a ZAIOS atual (`aceite_05g/linha_base_05g.js`, cópia local, commit `ec21ad5`) | **Executada:** 11 verificações, 10 FALHA e 1 PASSA. **FALHA é o resultado esperado antes da implementação** |
| Testes de aceite sobre a implementação | **Pendentes** (não há implementação) |
| Regressão completa depois da implementação | **Pendente** |
| Homologação | **Não concedida** |

Evidência: `testes/financeiro/resultados/2026-11-09-05g-a-linha-base/` (`LINHA_BASE_05G.md`, `linha_base_05g.json`).

## 2. Testes de aceite por decisão

Tolerâncias, as mesmas do 05F:
- R$ 0,01;
- 0,000001 para frações, anos e meses;
- igualdade exata para textos e estados.

| Teste | O que verifica | Esperado (independente) | Linha de base (ZAIOS atual) |
|---|---|---|---|
| O8-1 | P6 nunca apresenta selo de aprovação definitiva | Nenhum dos selos proibidos (Avançar, Ajustar, Redesenhar, Aprovado, Viável) no P6; texto "indicação inicial, subordinada à análise financeira completa" | FALHA |
| O8-2 | Contradição entre P6 e viabilidade é explicitada | Indicação do P6 positiva (margem 45,40%) e decisão da viabilidade "Redesenhar" → aviso de conflito explícito; prevalece a análise completa | FALHA |
| O8-3 | Margem antes e depois dos custos do modelo aparecem com nomes distintos | Margem operacional (antes dos custos do modelo) 19,9332% e margem EBITDA -8,9409%, com nomes distintos | FALHA |
| O9-1 | EBITDA negativo não gera valor de saída negativo | Saída R$ 0,00; VPL com saída = VPL sem saída = R$ -891.343,30; TIR com saída inexistente | FALHA |
| O9-2 | EBITDA positivo: valor de saída inalterado | Saída R$ 3.312.531,36; VPL com saída R$ 2.225.674,45; TIR com saída 24,1441% | PASSA |
| O9-3 | Borda: EBITDA = 0 gera saída 0 | EBITDA 0 → saída R$ 0,00 | não executado (exige a implementação ou uma decisão pendente) |
| O10-1 | Necessidade de caixa depois do mês 36 aparece na análise (36 primeiros meses positivos) | Menor saldo em 36 meses R$ 22.704,75 (positivo); 1º mês negativo 54 (ano 5); menor saldo em 120 meses R$ -85.232,63; capital adicional R$ 85.232,63 | FALHA |
| O10-2 | Atraso de 6 meses não pode parecer melhorar o projeto | Saldo em 120 meses: base R$ 4.850.461,78, com atraso R$ 4.593.922,63 (perda R$ 256.539,15); decomposição exibida. Condicional: convenção de desconto (P-O10a/b) | FALHA |
| O10-3 | Saldos de fim de ano 1 a 10 (visão anual) | Saldos de fim de ano 1 a 10: R$ 139.935,70; R$ 433.753,30; R$ 985.841,86; R$ 1.537.930,42; R$ 2.090.018,98; R$ 2.642.107,54; R$ 3.194.196,10; R$ 3.746.284,66; R$ 4.298.373,22; R$ 4.850.461,78 | não executado (exige a implementação ou uma decisão pendente) |
| O11-1 | Gestão e royalties com bases diferentes e independentes | EBITDA por combinação (gestão/royalties): hospedagem/hospedagem R$ 571.888,56; hospedagem/bruta R$ 564.688,56; bruta/hospedagem R$ 559.288,56; bruta/bruta R$ 552.088,56 | FALHA |
| O11-2 | Sem base contratual definida: premissa marcada como hipótese | Sem base contratual: rótulo "hipótese", base e percentual exibidos | não executado (exige a implementação ou uma decisão pendente) |
| O12-1 | Aluguel entra na base mensal do capital de giro uma única vez | Base mensal com aluguel (uma vez): C1 R$ 12.000; C2 R$ 36.000; C3 R$ 125.000 | FALHA |
| O12-2 | Giro B com a base nova (déficit e sazonalidade já incluem o aluguel pela geração; o componente de meses fixos usa a base com aluguel) | Giro B com a base nova: R$ 118.095,26. Condicional: prazo de 3 meses só para conferência | não executado (exige a implementação ou uma decisão pendente) |
| O12-3 | Sem duplicidade: aluguel digitado também dentro do custo fixo deve gerar alerta, não soma dupla | Aluguel digitado também no custo fixo → alerta de duplicidade, sem soma dupla | não executado (exige a implementação ou uma decisão pendente) |
| O13-1 | Disponível menor que o necessário gera déficit e necessidade de captação, sem duplicidade | Necessário R$ 109.095,26; disponível R$ 45.000,00; déficit R$ 64.095,26; usos R$ 859.095,26; captação adicional para giro R$ 64.095,26 | FALHA |
| O13-2 | Déficit em C2 e C3 | C2: déficit R$ 48.000,00; C3: déficit R$ 150.000,00 | não executado (exige a implementação ou uma decisão pendente) |
| O13-3 | Excedente | C2 com disponível R$ 200.000: excedente R$ 32.000,00; usos sem mudança R$ 2.268.000,00 | não executado (exige a implementação ou uma decisão pendente) |
| O13-4 | Disponível não substitui o necessário na curva de caixa | Curva técnica com o necessário: menor saldo R$ 22.704,75; não usar o disponível (R$ -41.390,51) | não executado (exige a implementação ou uma decisão pendente) |
| O14-1 | Receita independente da ocupação não cai quando a ocupação cai | C3 → C3E: categoria C R$ 480.000,00 → R$ 480.000,00 (sem queda); A R$ 181.040,00 → R$ 144.832,00 (-20,00%); B R$ 132.008,33 → R$ 105.606,67 (-20,00%) | FALHA |
| O14-2 | Sem duplicidade: a receita de hospedagem não muda ao incluir complementares | Receita de hospedagem do C3 continua R$ 4.299.700,00 ao incluir complementares | não executado (exige a implementação ou uma decisão pendente) |
| INT-1 | Integração no C1: gestão sobre hospedagem, royalty sobre bruta (iguais em C1, sem complementares), saída MAX(0), giro necessário x disponível, horizonte de 10 anos | C1 com as sete decisões: EBITDA R$ -15.419,63; saída R$ 0,00; déficit de giro R$ 64.095,26; 1º mês negativo 54; capital adicional R$ 85.232,63; P6 preliminar com conflito sinalizado | não executado (exige a implementação ou uma decisão pendente) |

Os testes marcados como **condicional** dependem de uma definição pendente (`PENDENCIAS_METODOLOGICAS.md`, seção 2). O esperado mostra a premissa usada e deve ser recalculado quando o Bruno decidir.

## 3. Integração entre as decisões

| Combinação | Risco que o teste cobre | Teste |
|---|---|---|
| O9 + O10 | O valor de saída zerado precisa entrar no VPL do mesmo horizonte de 10 anos | INT-1 |
| O12 + O13 | O déficit usa o necessário calculado com a base nova, uma única vez | INT-1, O13-1 (recalcular com a base nova quando P-O12 for decidido) |
| O10 + O13 | O capital adicional dos anos 4 a 10 soma ao déficit de giro na necessidade de captação, sem contar duas vezes | INT-1 (esperado: déficit de giro R$ 64.095,26; capital adicional na curva de 120 meses R$ 85.232,63, medido **depois** de usar o necessário) |
| O11 + O14 | "Receita bruta" como base de gestão e royalties inclui as categorias A, B e C; "hospedagem" não inclui | O11-1 repetido com as categorias do O14-1 (preparar quando P-O11 e P-O14 forem decididos) |
| O8 + todas | A indicação preliminar do P6 nunca contradiz a decisão sem aviso, depois de qualquer mudança de cálculo | O8-2 rodado nos 5 cenários (C1, C2, C3, C3E, Z-base do 05E) |

## 4. Regressão obrigatória depois de cada etapa de implementação

| Suíte | Conteúdo | Situação hoje | Depois da implementação |
|---|---|---|---|
| `testes/financeiro/run.js` (T1 a T12 + complementares C) | 237 casos | 189 OK, 27 divergências, 6 limitações, 15 pendentes econômicos, 0 falhas | Os casos atingidos pelas decisões mudam de forma **prevista** (ex.: saída no C1, giro, outras receitas). Cada mudança precisa estar listada antes, com o novo esperado em versão nova do arquivo, **sem sobrescrever** o 05E |
| `composicao_05f/run_05f.js` | 288 campos | 249 OK, 32 metodológicas, 7 não aplicáveis, 0 matemáticas | Previsão: O9 muda `valor_saida`, `vpl_com` e `tir_com` do C1; O11 com base configurável elimina as divergências da base quando escolhida "hospedagem"; O12 e O13 mudam `giro`, `captacao` e a curva; O10 acrescenta campos de 120 meses; O14 muda as outras receitas do C3E |
| `aceite_05g/linha_base_05g.js` | 11 verificações | 10 FALHA, 1 PASSA | Todas PASSA |
| Testes da própria ZAIOS (`src/test/*.test.ts`, vitest) | 108 testes nos 5 arquivos lidos | Não executados nesta auditoria (dependem de módulos não lidos) | Rodar no ambiente da ZAIOS. Atualizar os que testam o selo do P6, a saída, o giro e as outras receitas |
| Visual (telas do P6, viabilidade e dossiê em PDF) | Rótulos, selos, alertas | Não testado | Roteiro manual com os 5 cenários; captura de tela antes e depois |
| Compatibilidade | Respostas e dossiês já salvos | Não testado | Abrir uma resposta antiga de cada pilar: o resultado anterior se mantém até o membro recalcular, e o dossiê antigo não muda |

## 5. Critério geral de aceite de uma etapa

1. Os testes de aceite da decisão passam.
2. Nenhum caso das suítes de regressão muda **fora** da lista de mudanças previstas.
3. Zero divergência matemática nas suítes 05E e 05F.
4. Os documentos de evidência são gerados em pasta nova, com data.
5. O Bruno aprova o resultado antes da etapa seguinte.
