# Controle de versões das ferramentas financeiras

Comando 05D · extração e análise em 09/11/2026 · **A homologação matemática condicionada vale exclusivamente para as versões abaixo.** Qualquer mudança nesses arquivos exige nova execução da suíte e nova verificação dos componentes afetados.

Repositório: `bchaerk-creator/zion-hotel-ai-developer`.
- **Suíte:** commit `913968f` (09/11/2026).
- **Verificação independente:** commit deste comando.

Hashes SHA-256: os 16 primeiros caracteres.

## ZAIOS (motor de cálculo)

| Campo | Registro |
|---|---|
| Módulos | `src/calc/tipos.ts`, `capex.ts`, `receitas.ts`, `viabilidade.ts` |
| Origem | Projeto Lovable "Zaios" (id `51fa7ea5-6cb2-4867-9bf7-6e1cbb3e71dc`), **commit `ec21ad5606fd3d46f610f95d2efcbc3169386546`**, última edição em 07/11/2026 19:55 UTC |
| Extração | 09/11/2026, por leitura de arquivos (sem créditos), cópia local **fora do repositório** |
| Hashes da cópia | tipos.ts `a081b46e6d5bbf4a` · capex.ts `cc3d8979b6c0da54` · receitas.ts `2b1dde48d5cca080` · viabilidade.ts `ab6075226cacd18a` |
| Equivalência da cópia | A cópia foi transcrita a partir da leitura. Ela reproduz os resultados dos testes da própria ZAIOS (`src/test/viabilidade.test.ts`): caso 1 (VPL −1.110.447,78; payback 38,6; TIR com saída −8,4%), caso 2 (payback 5,75; descontado 8,82; VPL 92.549,78 e 624.599,52), bordas da régua e F02 (108.846,84). **Recomendação:** confirmar por hash com uma exportação direta (repositório GitHub sincronizado) antes da homologação definitiva |
| Cenários executados | T1, T2 (sem e com rampa), T3 (F01, F02, F03 casos 1 e 2), T5 (pró-labore), T6, T7, T9, T10, T11, T12 |
| Resultados | 63 fórmula OK (+1 caso cruzado com a Folha J2) · 8 divergências confirmadas · valores de T12 lidos |
| Tolerância | R$ 0,01; 0,01 p.p.; 0,01 ano (0,05 ano e 0,05 p.p. para valores do plano com uma casa) |
| Fora da cobertura | Exercícios que compõem as primitivas (`src/exercicios/*-calculo.ts`), G2/G3 (`src/calc/operacao.ts`), outras receitas, custo por estadia, sazonalidade alta/baixa, custos do modelo (aluguel, gestão, royalty), capital de giro A/B, curva de caixa e colchão com cenários próprios, cronograma, sensibilidade e estresse |

## Zion Arsenal · B06, B08, A09

| Campo | B06 · Calculadora de Implantação | B08 · Simulador de Viabilidade | A09 · Simulador de Viabilidade (cabana) |
|---|---|---|---|
| Módulo | `producao/zion-arsenal/app/products/B06.js` | `.../B08.js` | `.../A09.js` |
| Motor comum | `producao/zion-arsenal/app/engine.js`, commit `a60f075` (07/11), sha `667e67f9375f8a78` | idem | idem |
| Versão | commit `b1549d0` (07/11), sha `37229f03a0ded93d` | commit `b1549d0`, sha `76f3bf38af290049` | commit `b1549d0`, sha `c8fd2d7034742073` |
| Extração | 09/11/2026 (main `913968f`) | idem | idem |
| Execução | `compute()` em contexto isolado, com stub do motor (sem navegador) | idem | idem |
| Cenários | Perfil oficial "iniciante" (`tests/profiles/B06.json`, sha `028ef75b4748237a`); linhas do F01 com contingência de 25% | T1 Z-base; T6 investimento de 3.000.000; T9 com reserva de 4% | T1 com 365/12 e com 30 noites/mês |
| Resultados | 4 OK · 1 limitação (D6) | 10 OK · 8 divergências · 1 limitação (D8) | 6 OK · 7 divergências · 1 limitação (D5) |
| Tolerância | R$ 0,01 | R$ 0,01; 0,01 p.p.; 0,01 ano | idem |
| Fora da cobertura | Outros perfis (só por testes próprios), variação de custo, desembolso, gap de recursos, custo/m² | Rampa linear, reajuste, extras, comissão separada, valor residual, cenários com variação | Contingência, extras em R$, comissão e gestão, cenários, diária de equilíbrio |

## Ferramenta 05 · Orçamento da Cabana

| Campo | Registro |
|---|---|
| Módulos | `producao/utilitarios/05-orcamento-cabana/src/build_planilha.py` (sha `ecd8c9bf8de0efc0`), `src/dados.py` (sha `ba684cec810cc3d2`) |
| Planilha testada | `docs/p/adbc67069af26ae0/orcamento-05/Orcamento-Cabana-Zion-EXEMPLO.xlsx` (sha `3b7b291194cc2e31`) |
| Versão | commit `cfa48e5` (08/11/2026) |
| Execução | Cópia temporária recalculada no LibreOffice headless; original não alterado |
| Cenários | Exemplo fictício (subtotal, reserva de 10%, total) |
| Resultados | 3 OK |
| Tolerância | R$ 0,01 |
| Evidência adicional | Suíte própria `tests/test_planilha.py` (33 de 33 em 08/11), com regra independente em 29 arquivos |
| Fora da cobertura (nesta suíte) | Cronograma de 12 meses, diferença entre cotações, R$/m², "pago acima do orçado" |

## Folha Única do Mês · Jornada 2, Módulo 2

| Campo | Registro |
|---|---|
| Módulo | `producao/jornada2/02-financas/src/logic.js` |
| Versão | commit `7c8f041` (08/11/2026), sha `2ede7581ff8159d5` |
| Execução | `calcular(normalizar(EXEMPLO))` via Node |
| Cenários | Exemplo oficial; quebra medida de R$ 150 |
| Resultados | 9 OK · 2 divergências (D2-C, D4) |
| Tolerância | R$ 0,01 |
| Fora da cobertura | Meses de fôlego, ponto de equilíbrio, indicadores por noite, bloco de caixa, regras de leitura (a ferramenta tem 92 testes próprios, não revisados aqui) |

## Suíte e verificação

| Item | Versão |
|---|---|
| `testes/financeiro/` (suíte T1–T12) | commit `913968f` |
| `esperados.js` | igual ao plano v0.2; sem alterações desde a criação |
| `testes/financeiro/independente/verificacao_independente.py` | Comando 05D (Python 3, sem dependências além da biblioteca padrão) |
| Ambiente | Node 22.23.4; Python 3; LibreOffice headless |

## Regra de revalidação

| Mudança em… | Refazer |
|---|---|
| Qualquer arquivo de `src/calc` da ZAIOS | T1–T3, T5–T7, T9–T11 da ZAIOS + verificação independente |
| B06, B08, A09 ou `engine.js` | Casos da ferramenta + verificação independente |
| F05 (`build_planilha.py`, `dados.py` ou planilha publicada) | T4-F05 + suíte própria da F05 |
| Folha J2 (`logic.js`) | T5, T9-J2, T10-J2 |
| Dicionário ou decisões (D1…D11) | Revisar `esperados.js` só com nova versão do plano aprovada |
