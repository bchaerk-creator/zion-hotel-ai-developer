# Relatório de integridade do código da ZAIOS usado nos testes

Comando 05E · 09/11/2026 · Auditoria somente leitura. Nenhum arquivo da ZAIOS foi alterado. Nenhum crédito Lovable foi consumido.

## 1. Conclusão

**A integridade não está comprovada. A ressalva continua aberta.**

As cópias usadas nos testes têm forte evidência de correspondência com o commit `ec21ad5`:
- três transcrições independentes dos 4 arquivos de cálculo são idênticas byte a byte;
- a cópia reproduz os resultados documentados nos testes da própria ZAIOS.

Mesmo assim, falta o que a instrução pede: comparar com um hash calculado **na origem**. A plataforma não fornece esse hash, e não existe repositório GitHub sincronizado com o projeto. Por isso, a correspondência exata não pode ser declarada.

## 2. Versão de referência

| Campo | Registro |
|---|---|
| Projeto | Lovable "Zaios" (id `51fa7ea5-6cb2-4867-9bf7-6e1cbb3e71dc`) |
| Commit | `ec21ad5606fd3d46f610f95d2efcbc3169386546` |
| Última edição registrada | 07/11/2026 19:55 UTC |
| Commit atual em 09/11/2026 | O mesmo `ec21ad5` (`get_project` → `latest_commit_sha`). Não houve edição depois da extração |
| Meio de leitura | `read_file` e `list_files` do conector Lovable, informando o commit. São leituras gratuitas, sem créditos e sem escrita |

## 3. Procedimento

1. **Busca de uma fonte com hash próprio.**
   - Repositórios acessíveis à sessão (`list_repos`): só `zion-hotel-ai-developer` (público) e `manus-github-test` (privado).
   - Nenhum dos dois está sincronizado com o projeto ZAIOS.
   - O conector Lovable devolve o texto do arquivo, mas não um hash nem o arquivo bruto. Não há como obter um hash calculado na origem.
2. **Três leituras independentes dos 4 arquivos de `src/calc`** (`tipos`, `capex`, `receitas`, `viabilidade`), todas do commit `ec21ad5`:
   - A: transcrição feita no Comando 05C;
   - B: nova transcrição, feita por um agente separado no Comando 05E, sem acesso à cópia A;
   - C: cópia feita junto com a leitura da camada de composição.
3. **SHA-256 local de cada cópia** e comparação entre elas.
4. **Prova funcional.**
   - A cópia reproduz os valores esperados escritos nos testes da própria ZAIOS (`src/test/viabilidade.test.ts`):
     - caso 1: VPL −1.110.447,78; payback 38,6; TIR com saída −8,4%;
     - caso 2: payback 5,75; descontado 8,82; VPL 92.549,78 e 624.599,52;
     - F02: 108.846,84.
   - Ela também reproduz os valores da ZAIOS na verificação independente do 05D e os 16 valores de composição do 05E.

## 4. Hashes (SHA-256, 16 primeiros caracteres)

### 4.1 Motor de cálculo (`src/calc`), três transcrições

| Arquivo | Cópia A (05C) | Cópia B (05E) | Cópia C (05E) | Resultado |
|---|---|---|---|---|
| `tipos.ts` | `a081b46e6d5bbf4a` | `a081b46e6d5bbf4a` | `a081b46e6d5bbf4a` | Idênticas |
| `capex.ts` | `cc3d8979b6c0da54` | `cc3d8979b6c0da54` | `cc3d8979b6c0da54` | Idênticas |
| `receitas.ts` | `2b1dde48d5cca080` | `2b1dde48d5cca080` | `2b1dde48d5cca080` | Idênticas |
| `viabilidade.ts` | `ab6075226cacd18a` | `ab6075226cacd18a` | `ab6075226cacd18a` | Idênticas |

### 4.2 Camada de composição e G2/G3, uma transcrição

| Arquivo | SHA-256 (16) | Uso nos testes |
|---|---|---|
| `src/exercicios/viabilidade-calculo.ts` | `2bcba2abb27a1e31` | Composição (1º ano, giro, captação, curva, colchão, régua) |
| `src/exercicios/receitas-calculo.ts` | `c36e73513e0a0402` | Composição |
| `src/exercicios/capex-calculo.ts` | `b728645b2a0ae834` | Composição (mapa do CAPEX) |
| `src/exercicios/financas-calculo.ts` | `420f36cad2929d47` | G2 e G3 |
| `src/exercicios/mercado-calculo.ts` | `595b6b20b4c948df` | Dependência |
| `src/calc/operacao.ts` | `016810f560aed332` | G2 e G3 (primitivas) |
| `src/calc/funcoes.ts` | `200075625ba50b02` | G3 (diária, ocupação, RevPAR) |
| `src/calc/convencoes.ts` | `038b6275bdb2fa61` | Dependência |
| `src/calc/formatar.ts` | `0a05b111e8d4e2ed` | Dependência (textos) |
| `src/calc/estatisticas.ts` | `93c8e3e964513406` | Dependência. Salvo sem quebra de linha final, o que pode mudar o hash, mas não o comportamento |

Também foram lidos, só como referência, `src/lib/operacao.ts` e os testes `src/test/{viabilidade,receitas,capex,financas-indicadores,operacao}.test.ts`.

Não foram lidos:
- `src/exercicios/tipos.ts`: só tipos, removidos na execução;
- o cliente Supabase;
- `src/lib/exercicios.ts`.

Nenhum deles entra nos cálculos testados.

## 5. Grau de evidência

| Evidência | Situação |
|---|---|
| Mesmo commit na leitura e no projeto atual | Confirmado |
| Três transcrições idênticas do motor (`src/calc`) | Confirmado |
| Duas ou mais transcrições da camada de composição e de G2/G3 | **Não feito.** Só uma transcrição |
| Reprodução dos valores escritos nos testes da própria ZAIOS | Confirmado nos casos citados |
| Execução dos testes da própria ZAIOS (vitest) sobre a cópia | **Não feito.** Os testes importam módulos não lidos (dossiê, definições dos exercícios, cliente Supabase) |
| Hash calculado na origem (exportação ou GitHub sincronizado) | **Indisponível** |

**Leitura:** se a transcrição tivesse um erro que mudasse um número, os testes funcionais teriam grande chance de mostrar a diferença. Isso não exclui diferenças em trechos não exercitados, como comentários, textos ou ramos não testados.

## 6. Como encerrar a ressalva (depende do Bruno)

1. **Conectar o projeto ZAIOS a um repositório GitHub privado** (função nativa do Lovable). A conexão grava o código no repositório e não altera o código nem as fórmulas.
   - Pode exigir uma ação no painel do Lovable. Verificar antes se consome créditos.
   - Exige autorização expressa, porque mexe na configuração do projeto.
2. Calcular o SHA-256 dos arquivos no repositório, no commit correspondente a `ec21ad5`, e comparar com a seção 4.
3. Se forem iguais, a ressalva é encerrada. Se forem diferentes, refazer a suíte da ZAIOS a partir do repositório.

Alternativa sem mudar a configuração: o Bruno baixa o código pelo painel do Lovable (exportação ou ZIP, se disponível) e envia os arquivos. O hash é calculado sobre esse download.

## 7. Onde a cópia fica

- A cópia fica só na área temporária da sessão, **fora do repositório público**. Ela some quando a sessão termina.
- Nenhum arquivo da ZAIOS foi publicado ou enviado para o Git.
- A decisão P3 continua com o Bruno: onde guardar uma cópia permanente, de preferência num repositório privado.
