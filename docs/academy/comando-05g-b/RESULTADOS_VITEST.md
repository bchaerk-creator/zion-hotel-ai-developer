# Resultados dos testes próprios da ZAIOS (Teste C)

Comando 05G-B · 09/11/2026 · Execução local, numa cópia, sem alterar os testes nem o código.

## 1. O que foi possível executar

- A ZAIOS tem **19 arquivos de teste** em `src/test/` (mais `setup.ts` e `dossie-fixture.ts`), segundo o `list_files` do commit `ec21ad5`.
- Foram executados os **5 arquivos ligados aos cálculos financeiros**, que já estavam lidos: `capex`, `receitas`, `viabilidade`, `operacao` e `financas-indicadores`.
- Para isso, foram buscados 20 arquivos de dependência (definições dos exercícios, validação e base de exemplo do dossiê). Nenhum teste foi alterado.

| Arquivo | Testes | Passaram | Falharam |
|---|---|---|---|
| `capex.test.ts` | 17 | 17 | 0 |
| `receitas.test.ts` | 20 | 20 | 0 |
| `viabilidade.test.ts` | 27 | 27 | 0 |
| `operacao.test.ts` | 21 | 21 | 0 |
| `financas-indicadores.test.ts` | 50 | 49 | 1 |
| **Total** | **135** | **134** | **1** |

**A falha não é de cálculo.**
- **Teste:** "Dossiê de Operação G2 e G3 monta seções 8, 9 e 10 completas sem alterar a foto". A linha do mês tem os mesmos valores, mas o texto difere num caractere invisível:
  - esperado: `"R$ 1.300,00"` (com espaço comum);
  - obtido: `"R$ 1.300,00"` (espaço não separável, gerado por `toLocaleString("pt-BR")` em `fmtMoeda`).
- **Causa provável:** o arquivo original tem o espaço não separável e a leitura por texto o trocou por espaço comum (ver `TESTES_INTEGRIDADE.md`, seção 3).
- **Hipótese alternativa:** o teste também falha no ambiente da ZAIOS. Não dá para distinguir sem o arquivo original.
- **O teste não foi alterado.**

## 2. Cobertura (só dos 5 arquivos executados)

| Módulo | Linhas | Funções | Ramos |
|---|---|---|---|
| `calc/capex.ts` | 100% | 100% | 87,9% |
| `calc/receitas.ts` | 100% | 100% | 83,9% |
| `calc/viabilidade.ts` | 98,8% | 100% | 97,4% |
| `calc/operacao.ts` | 100% | 100% | 83,3% |
| `calc/tipos.ts`, `convencoes.ts` | 100% | 100% | 100% |
| `calc/estatisticas.ts` | 100% | 100% | 75% |
| `calc/funcoes.ts` | 41,4% | 31,8% | 46,4% |
| `calc/formatar.ts` | 22,2% | 42,9% | 18,2% |
| `exercicios/capex-calculo.ts` | 100% | 100% | 90,2% |
| `exercicios/receitas-calculo.ts` | 96,3% | 92,3% | 95,7% |
| `exercicios/viabilidade-calculo.ts` | 100% | 100% | 87,2% |
| `exercicios/financas-calculo.ts` | 96,9% | 93,9% | 89,6% |
| `exercicios/mercado-calculo.ts` | 100% | 95,5% | 84,7% |
| **Total (calc + composição, incluindo outros exercícios)** | **85,5%** | **85,9%** | **79,2%** |

- A cobertura baixa de `funcoes.ts` e `formatar.ts` se explica pelos testes não executados (`calc.test.ts`, `formatar.test.ts`).
- Os testes de auditoria (05C a 05G-B) cobrem o que os testes da ZAIOS deixam de fora nos cálculos financeiros.

## 3. Não executados

| Arquivo | Motivo |
|---|---|
| `calc.test.ts`, `formatar.test.ts`, `dossie.test.ts`, `exercicios.test.ts`, `territorio.test.ts`, `mercado-produto.test.ts`, `maturidade-plano.test.ts`, `acesso.test.ts`, `privacidade.test.ts` | Não lidos neste comando. Fora do núcleo financeiro do escopo; executáveis numa próxima leitura |
| `app-routing.test.tsx`, `exercicio-generico.test.tsx`, `exercicio-runner.test.tsx` | Testes de interface (React/jsdom). Exigem as dependências completas do projeto |
| `privacidade.integration.test.ts`, `seguranca.integration.test.ts` | Testes de integração. Dependem de serviço externo e credenciais. **Não executar** |

## 4. Adaptações do ambiente (documentadas, sem alterar testes)

- vitest 4.1.10, na faixa `^4.1.10` do `package.json` da ZAIOS. Instalado com `--legacy-peer-deps` por causa de um erro do npm 10.9 ("edgesOut").
- Ambiente `node` em vez de `jsdom`. O `setup.ts` original não foi lido nem usado.
- Componentes de interface e cliente Supabase substituídos por stubs. O stub do Supabase lança erro se for chamado, para que nenhuma dependência externa passe despercebida.
- Configuração e stubs: `testes/financeiro/vitest_harness/` (sem código da ZAIOS). Resumo: `testes/financeiro/resultados/2026-11-09-05g-b-vitest/resumo_vitest.json`.
