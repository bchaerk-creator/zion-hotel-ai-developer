# Registro da implementação · Comando Mestre

10/11/2026 · Ambiente isolado: repositório git local, privado, criado a partir da cópia auditada do commit `ec21ad5` (transcrição, sem hash da origem). **Nenhuma alteração na ZAIOS ativa, no Lovable, no ClickMax ou na produção.** O código da ZAIOS não está neste repositório público; aqui ficam só as regras, os testes independentes e os resultados.

Ciclo em cada decisão: versão anterior preservada no commit anterior → implementação → aceite → regressão (Vitest, suíte financeira de 237 casos, composição 05F e 05G, linha de base 05G-A) → registro → próxima. Interrupção prevista se aparecesse mudança fora do esperado: não apareceu.

## Sequência

| # | Commit local | Decisão | Arquivos de regra tocados | Testes novos | Regressão: o que mudou nas suítes antigas |
|---|---|---|---|---|---|
| 0 | `a6d0153`, `9a2554e` | Base | — | — | Vitest 134/135 (1 falha antiga: espaço não separável); 237 casos: 189 OK, 27 divergências, 6 limitações, 15 sem dependência; 05F e 05G sem divergência matemática |
| 1 | `18267df` | O9 | viabilidade (cálculo e composição), tela, dossiê, FORMULAS | 3 | Só os 6 campos previstos no 05G-B (C1 e B4: saída, VPL com saída, VPL com saída do conservador) |
| 2 | `9584802`, `1df7e66` | O8 | tipos, receitas (composição), tela, dossiê, viabilidade (alerta) | 4 | Selo do P6 nos 4 cenários; 3 asserções antigas trocadas (ver `TESTES_ALTERADOS.md`) |
| 3 | `68ea376` | O11 | receitas (cálculo, composição, campos), tela, dossiê | 8 | Nenhuma (sem os campos novos vale a regra anterior) |
| 4 | `4ffb03f` | O14 | receitas (cálculo, composição, campos), tela, dossiê | 7 | Nenhuma |
| 5 | `ea8998e`, `62b936a`, `b871107` | O12 | receitas (cálculo, composição, campos), P5 (texto), tela, dossiê | 5 | Giro, captação, curva e colchão em todos os cenários (efeito direto da regra); 3 asserções antigas trocadas |
| 6 | `cd68c64` | O13 | viabilidade (composição, campos), tela, dossiê | 3 | Nenhuma |
| 7 | `053d85e` | O10 | viabilidade (cálculo e composição), tela, dossiê | 5 | Curva e atraso passam a 120 meses; em C1 e B4 o caixa negativo depois do mês 36 aparece e o passo 5 pede redesenho |
| 8 | `4351132`, `966cbfe` | O7 | G2 (categorias e resumo), dossiê (coluna condicional), FORMULAS | 2 | O caso C-G2-impostos (limitação O7) deixa de se reproduzir |
| 9 | `9f4e339` | Compatibilidade | — | 2 | — |
| 10 | `8676e9e` | Diagnóstico NBSP | — | 2 | — |

Totais: 13 arquivos de regra, tela, dossiê e documentação de fórmulas; 12 arquivos de teste (10 novos, 2 com asserções trocadas). 659 linhas acrescentadas e 82 removidas.

## Arsenal (repositório público, branch `dev/mestre-arsenal`, fora da main)

| Commit | Ferramenta | Mudança |
|---|---|---|
| `4619380` | B08 | Equilíbrio operacional (sem reserva como dedução) e equilíbrio de caixa (com reserva); feedback novo |
| `4619380` | A09 | Calendário real (365/366); noites por mês opcionais e limitadas aos dias reais; ano de referência opcional |
| `4619380` | Suíte | C-B08-E-2 e C-A09-D-1 passam de divergência/limitação a fórmula; C-B08-E-3 lê o equilíbrio de caixa; C-A09-D-2 e D-3 conferem o calendário real e o ano bissexto |

A main publica o Arsenal no GitHub Pages; por isso as mudanças ficaram na branch de desenvolvimento.

## Compatibilidade com projetos salvos

- Respostas antigas (sem os campos novos), oito cenários: os **256** campos de regras não alteradas ficam idênticos à versão `ec21ad5` (DRE do regime e do primeiro ano, equilíbrio, fluxo, VPL sem saída, TIR, paybacks, cenários, sensibilidade). Mudam só os 52 campos previstos (selo, giro, captação, saída com EBITDA negativo, VPL com saída, curva, colchão, decisão).
- Resultados salvos no formato anterior abrem no dossiê novo sem recalcular, com os textos da regra anterior, sem "undefined" nem "NaN".
- Não há migração de banco: os campos novos cabem no JSON das respostas e dos resultados.
