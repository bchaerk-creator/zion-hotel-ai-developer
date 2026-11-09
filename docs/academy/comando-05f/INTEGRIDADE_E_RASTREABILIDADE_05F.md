# Integridade e rastreabilidade · Comando 05F

09/11/2026 · **A ressalva de integridade continua aberta.** Nada aqui comprova que a cópia testada é idêntica ao código hospedado na ZAIOS.

## 1. Origem do código testado

| Item | Registro |
|---|---|
| Projeto | Lovable "Zaios", id `51fa7ea5-6cb2-4867-9bf7-6e1cbb3e71dc` |
| Commit de referência | `ec21ad5606fd3d46f610f95d2efcbc3169386546` |
| Commit atual do projeto em 09/11/2026 (consulta do 05F) | O mesmo `ec21ad5`. Última edição em 07/11/2026 19:55:28 UTC (`get_project`). **Não houve edição depois da extração** |
| Cópia usada | Transcrição feita no 05E por leitura (`read_file` no commit `ec21ad5`), guardada só na área temporária da sessão, **fora do repositório** |
| Transcrições | Motor `src/calc` (4 arquivos): três transcrições idênticas byte a byte (05E). Camada de composição (`src/exercicios`): **uma** transcrição |
| Hash calculado na origem | **Indisponível.** O conector não fornece hash nem arquivo bruto, e não há repositório GitHub sincronizado. **Por instrução do 05F, a ZAIOS não foi conectada ao GitHub** |
| Execução | Node 22, que remove os tipos do TypeScript, sobre uma cópia temporária com os imports ajustados (`lib/zaios_comp.js`). As fórmulas não são alteradas |

## 2. Hashes SHA-256 das cópias usadas nesta execução

| Arquivo | SHA-256 (16 primeiros) | Igual ao 05E? |
|---|---|---|
| `src/exercicios/capex-calculo.ts` | `b728645b2a0ae834` | Sim |
| `src/exercicios/receitas-calculo.ts` | `c36e73513e0a0402` | Sim |
| `src/exercicios/viabilidade-calculo.ts` | `2bcba2abb27a1e31` | Sim |
| `src/exercicios/mercado-calculo.ts` | `595b6b20b4c948df` | Sim |
| `src/calc/receitas.ts` | `2b1dde48d5cca080` | Sim |
| `src/calc/capex.ts` | `cc3d8979b6c0da54` | Sim |
| `src/calc/viabilidade.ts` | `ab6075226cacd18a` | Sim |
| `src/calc/tipos.ts` | `a081b46e6d5bbf4a` | Sim |
| `src/calc/formatar.ts` | `0a05b111e8d4e2ed` | Sim |

Os hashes completos dos 3 módulos de composição carregados estão em `resultado_05f.json` (`fontesZaios`).

## 3. Escopo efetivamente coberto

- **Coberto:**
  - `calcularCapex` → `lerMapaCapex` → `calcularReceitas` → `calcularViabilidade`, em 4 execuções (C1, C2, C3, C3E), com 72 campos cada, 288 no total;
  - receita, deduções, custos, custos do modelo, EBITDA, 1º ano, giro A/B, captação, curva, colchão, retorno, payback, VPL, TIR, cenários, sensibilidade, estresse interno, atraso, régua e selos.
- **Não coberto:**
  - pró-labore, reserva de reposição, quebra e contingência maiores que zero passando pela composição (contingência de 25% só no 05E);
  - outras taxas de desconto e múltiplos;
  - telas (rótulos e selos exibidos);
  - G2/G3 (não fazem parte desta composição);
  - testes da própria ZAIOS (vitest), que dependem de módulos não lidos.

## 4. Limitações da origem

1. Sem hash da origem, a identidade com o código hospedado **não está comprovada**.
2. A camada de composição tem uma só transcrição. Um erro de transcrição em trecho não exercitado não seria detectado.
3. O que se comprova é que **esta cópia** calcula, nos cenários testados, o que a regra documentada diz.

## 5. Créditos Lovable e chamadas feitas

| Chamada | Tipo | Efeito |
|---|---|---|
| `get_project` (Zaios) | Leitura de metadados | Nenhum: o commit e a data de edição continuaram os mesmos |
| `list_workspaces`, `get_workspace` | Leitura de metadados | Nenhum |
| `read_file` | Não usado no 05F (a cópia é a do 05E) | — |
| `send_message`, `create_project`, `deploy_project` e qualquer escrita | **Não usados** | — |

**Sobre créditos:**
- O conector não mostra o saldo de créditos, e `get_workspace` só devolve nome, plano e número de projetos. **Não é possível verificar o saldo antes e depois.**
- A evidência disponível:
  - só foram chamadas operações de leitura, que pela descrição do conector não acionam o agente do Lovable;
  - o projeto continua no mesmo commit, sem edição desde 07/11.
- **Não declaro "zero créditos" como fato verificado.** Para confirmar, o Bruno pode comparar o saldo no painel do Lovable.

ClickMax, Asaas e outras plataformas: nenhuma chamada.

## 6. Repositório, branch e commits

| Item | Registro |
|---|---|
| Repositório | `bchaerk-creator/zion-hotel-ai-developer` (público) |
| Base da main no início do 05F | `15930006ece05e2271c8f756e856d474f4519b80` |
| Commit do 05E usado como referência | `2135b2b` (09/11/2026 06:21 UTC) |
| Árvore de trabalho | Limpa no início. Alterações preexistentes não relacionadas: nenhuma |
| Branch de trabalho | Worktree sincronizada com `origin/main`; o push vai para a `main`. Os documentos são copiados para `claude/zaios-planejamento`, depois de conferir que não há conflito |
| Código de produção no commit | Nenhum. Só testes, esperados, resultados e documentos. Nenhum arquivo da ZAIOS |

## 7. Documentos de referência conferidos (SHA-256, 16 primeiros)

| Documento | Hash |
|---|---|
| `comando-05e/ATUALIZACAO_RESSALVAS_H1_H2.md` | `0913f2847c20a257` |
| `comando-05e/MATRIZ_TESTES_COMPLEMENTARES.md` | `159e2b566b460cef` |
| `comando-05e/RECOMENDACAO_PROXIMA_ETAPA.md` | `9eab66ea1a106fa2` |
| `comando-05e/RELATORIO_INTEGRIDADE_ZAIOS.md` | `924ef45771033833` |
| `comando-05e/RESSALVAS_ENCERRADAS_ABERTAS.md` | `2a5540f2be67280b` |
| `comando-05e/RESULTADOS_EVIDENCIAS.md` | `9ebb3894835643a0` |
| `comando-05d/CONTROLE_VERSOES_FINANCEIRAS.md` | `d9310d7a77671270` |
| `comando-05d/MATRIZ_EVIDENCIAS_TESTES.md` | `b4c69f695c395fc3` |
| `comando-05d/PARECER_HOMOLOGACAO_MATEMATICA.md` | `22919eac1bcb3d21` |
| `comando-05d/PENDENCIAS_HOMOLOGACAO.md` | `ca0d5c9367007aa7` |
| `comando-05b/DECISOES_METODOLOGICAS.md` | `beee4523eda99a66` |
| `comando-05b/DICIONARIO_FINANCEIRO.md` | `ecd64df9c7bd665c` |

Os documentos do 05B, 05D e 05E não foram alterados neste comando.

## 8. Artefatos do 05F (SHA-256, 16 primeiros)

| Artefato | Hash |
|---|---|
| `testes/financeiro/composicao_05f/cenarios_05f.json` (entradas) | `84302e46101225a0` |
| `testes/financeiro/composicao_05f/run_05f.js` (executor) | `d159028189b2acd6` |
| `testes/financeiro/independente/composicao_05f_referencia.py` (cálculo independente) | `ec0c243bf2e9142b` |
| `testes/financeiro/independente/esperados_05f.json` | `0ac71978111d0b4f` |
| `testes/financeiro/lib/zaios_comp.js` (carregador, sem alteração desde o 05E) | `93775def3d016463` |
| `testes/financeiro/resultados/2026-11-09-05f/resultado_05f.json` | `3acd87be2de0a806` |
| `testes/financeiro/resultados/2026-11-09-05f/RESULTADO_05F.md` | `cecc40f72f2e22a6` |

O `resultado_05f.json` registra a data e hora da geração, então uma nova execução produz um hash diferente. Os valores comparados não mudam.

Os hashes dos documentos do 05F estão em `HASHES_05F.txt`, gerado no fechamento.

## 9. Comandos executados

```
# leitura de metadados (Lovable): get_project, list_workspaces, get_workspace
python3 testes/financeiro/independente/composicao_05f_referencia.py
ZAIOS_SRC_DIR=<cópia local> node testes/financeiro/composicao_05f/run_05f.js --saida testes/financeiro/resultados/2026-11-09-05f
# regressão da suíte anterior (sem gravar no repositório):
ZAIOS_CALC_DIR=<cópia> ZAIOS_SRC_DIR=<cópia> node testes/financeiro/run.js --saida <pasta temporária>
#   → 237 casos: 189 OK, 27 divergências, 6 limitações, 15 pendentes de validação econômica, 0 falhas (igual ao 05E)
sha256sum <arquivos acima>
```
