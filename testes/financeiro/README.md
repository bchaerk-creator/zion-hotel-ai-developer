# Testes financeiros · homologação T1 a T12

Comando 05C · 09/11/2026 · **Somente preparação de testes.** Nenhuma fórmula, ferramenta, plataforma ou crédito foi alterado ou consumido. Nenhum parâmetro foi homologado.

Transforma o `docs/academy/comando-05b/PLANO_TESTES_HOMOLOGACAO.md` (v0.2) em testes automatizados reproduzíveis, com os valores esperados do plano e as decisões do `DICIONARIO_FINANCEIRO.md` (v0.4).

## Estrutura (separada dos módulos de produção)

```
testes/financeiro/
├── run.js                 executor: roda os casos, classifica e grava o relatório
├── esperados.js           premissas e valores esperados copiados do plano (não alterar sem nova versão aprovada)
├── lib/
│   ├── base.js            tolerâncias, tipos de caso e status
│   ├── zaios.js           carrega o motor da ZAIOS a partir de uma cópia local (somente leitura)
│   ├── arsenal.js         executa o compute() de B06, B08 e A09 num contexto isolado (somente leitura)
│   ├── folha_j2.js        carrega a lógica da Folha Única J2 (somente leitura)
│   ├── f05.js + f05_recalc.py   recalcula uma CÓPIA da planilha EXEMPLO da F05 no LibreOffice
├── casos/
│   ├── _util.js           montagem dos cenários equivalentes
│   ├── t01_zbase.js … t12_parametros.js   um arquivo por teste do plano
└── resultados/
    ├── 2026-11-09-com-zaios/   execução de referência com o motor da ZAIOS
    ├── 2026-11-09-sem-zaios/   execução sem a ZAIOS (modo independente)
    └── ultima/                 saída padrão de novas execuções (ignorada pelo git)
```

## Rastreabilidade

Cada caso registra:
- **ID**: `T<teste>-<ferramenta>-<nº>`;
- **teste** do plano (T1 a T12);
- **ferramenta** (ZAIOS, B06, B08, A09, F05, Folha J2);
- **indicador**, com o nome do dicionário;
- **decisão metodológica** (v0, D1, D2-C, D3-A, D4, D7-C, D11-A, ou decisão pendente D5/D6/D8);
- **tipo de resultado**;
- **valor esperado e tolerância**, tirados de `esperados.js`, que cita o plano;
- **nota**, explicando a divergência quando houver.

## Tipos de resultado (instrução 4 do Comando 05C)

| Tipo no caso | O que significa | Status possíveis |
|---|---|---|
| `formula` | Fórmula deve estar **matematicamente correta** | `OK` · `FALHOU` |
| `divergencia` | **Divergência conhecida** em relação à metodologia aprovada (D1, D2-C, D3-A, D4, D7-C, D11-A). O caso testa a regra aprovada e **deve falhar** com o código atual | `DIVERGÊNCIA CONFIRMADA` · `DIVERGÊNCIA NÃO REPRODUZIDA (revisar)` |
| `limitacao` | Diferença conhecida ligada a uma decisão **ainda pendente** (D5, D6, D8) | `LIMITAÇÃO CONFIRMADA (decisão pendente)` · `LIMITAÇÃO NÃO REPRODUZIDA (revisar)` |
| `economico` | **Parâmetro pendente de validação econômica** (T12). Mostra o valor em uso hoje; não é aprovado nem reprovado | `PENDENTE DE VALIDAÇÃO ECONÔMICA` |

Também podem aparecer:
- `NÃO EXECUTADO (dependência ausente)`;
- `ERRO AO EXECUTAR`.

**Código de saída:** 1 se algum caso `formula` falhar ou der erro; 0 nos outros casos. Divergências confirmadas não reprovam a execução, porque são esperadas até a implementação aprovada.

**"Não reproduzida (revisar)"** quer dizer que uma divergência sumiu. Isso só deve acontecer depois de uma correção aprovada; se aparecer antes, é preciso investigar.

## Como executar

Requisitos:
- **Node 22.6 ou superior**, com suporte nativo a TypeScript: o Node 22.23 desta sessão funciona.
- **Python 3 + openpyxl + LibreOffice (`soffice`)**: só para os casos da F05.
- Nenhuma dependência npm. Nenhum acesso pago.

```bash
# Modo independente (sem a ZAIOS): roda B06, B08, A09, F05, Folha J2 e T12
node testes/financeiro/run.js

# Com o motor da ZAIOS (cópia local de src/calc: tipos.ts, capex.ts, receitas.ts, viabilidade.ts)
ZAIOS_CALC_DIR=/caminho/para/copia/src/calc node testes/financeiro/run.js

# Saída em outra pasta
node testes/financeiro/run.js --saida /tmp/resultado-financeiro
```

Saída: `RESULTADO.md` (tabela legível) e `resultado.json` (dados completos) em `resultados/ultima/`.

### Como obter a cópia local da ZAIOS sem gastar créditos

O código da ZAIOS **não é copiado para este repositório**, que é público. Para os casos da ZAIOS, copie os quatro arquivos de `src/calc/` do projeto Lovable "Zion Empreendimentos" para uma pasta local e aponte `ZAIOS_CALC_DIR` para ela. Há três formas, todas só de leitura:
- abrir os arquivos no editor do Lovable e copiar o conteúdo;
- usar a leitura de arquivos do Lovable por MCP, que não consome créditos;
- clonar o repositório GitHub sincronizado, se existir.

O carregador copia os arquivos para uma pasta temporária e só acrescenta `.ts` nos caminhos de `import` (exigência do Node). O conteúdo das fórmulas não é alterado.

## Execução de referência (09/11/2026)

**Com o motor da ZAIOS** (cópia lida do Lovable em 09/11/2026), em `resultados/2026-11-09-com-zaios/`:

| Status | Casos |
|---|---|
| OK | 96 |
| DIVERGÊNCIA CONFIRMADA | 25 |
| LIMITAÇÃO CONFIRMADA (decisão pendente) | 3 |
| PENDENTE DE VALIDAÇÃO ECONÔMICA | 15 |
| FALHOU / ERRO | **0** |
| **Total** | **139** |

**Sem a ZAIOS**, em `resultados/2026-11-09-sem-zaios/`:
- 72 não executados;
- 32 OK;
- 17 divergências e 3 limitações confirmadas;
- 15 pendentes.

## Mapa de cobertura por ferramenta (casos por teste)

| Teste | ZAIOS | B08 | A09 | B06 | F05 | Folha J2 |
|---|---|---|---|---|---|---|
| T1 Z-base | 9 OK · 1 div. | 10 OK | 6 OK · 1 lim. | — | — | — |
| T2 Z-completo | 14 OK | — (depende de D2/D3/D4) | — | — | — | — |
| T3 F01–F03 | 12 OK | — (não aceita fluxo direto) | — | — | — | — |
| T4 Orçamento | (coberto no T3, F01) | — | — | 4 OK · 1 lim. | 3 OK | — |
| T5 Mês real | 1 OK (com a Folha) | — | — | — | — | 4 OK |
| T6 Limites | 6 OK | 1 lim. | — | — | — | — |
| T7 Régua | 13 OK · 1 div. | 1 div. | 2 div. | — | — | — |
| T8 Omissões | — | 4 div. | 4 div. | — | — | — |
| T9 Reserva e quebra | 5 OK · 3 div. | 2 div. | 1 div. | — | — | 4 OK · 1 div. |
| T10 Pró-labore e caixa | 3 OK · 1 div. | (T8) | (T8) | — | — | 1 OK · 1 div. |
| T11 Saída | 1 OK · 2 div. | 1 div. | — | — | — | — |
| T12 Parâmetros | 15 pendentes (valores em uso na ZAIOS e na Folha J2) | | | | | |

## Testes que devem passar com as regras atuais (96)

Todos do tipo `formula`. Se algum falhar, é erro real de fórmula ou de ambiente.

- **T1 (25):**
  - ZAIOS 01 a 09: receita bruta, receita real, resultado, equilíbrio, VPL, TIR, payback simples e descontado, retorno anual.
  - B08 01 a 10.
  - A09 01 a 06: com 365 dias informados como 365/12 noites por mês.
- **T2 (14):** ZAIOS, com e sem rampa: resultado, geração, 1º ano, VPL, TIR, payback, VPL com saída.
- **T3 (12):** F01 (CAPEX 1.237.400), F02 (receita real, resultado, equilíbrio) e F03 casos 1 e 2.
- **T4 (7):**
  - B06 01 a 04: perfil oficial iniciante e contingência fora do giro.
  - F05 01 a 03: subtotal, reserva, total.
- **T5 (5):** cascata da Folha J2 fecha (4); pró-labore igual na Folha e na ZAIOS (1).
- **T6 (6):** ZAIOS: sem TIR, aviso de várias TIR, payback estendido, sem equilíbrio (2 casos), não se paga.
- **T7 (13):** ZAIOS: conservador, valor e VPL de saída, os 5 critérios, bordas e leitura.
- **T9 (9):**
  - ZAIOS 01 a 05: com reserva de 4% e quebra de 1% informadas, a cascata fecha sem dupla contagem.
  - Folha J2 01, 03, 04 e 05: referência 4% (3–6%), quebra de referência, quebra medida, deduções sem quebra.
- **T10 (4):** pró-labore na ZAIOS (3) e na Folha J2 (1).
- **T11 (1):** valor de saída 6× EBITDA na ZAIOS.

## Testes que devem falhar por divergências conhecidas (28)

**Metodologia aprovada, ainda não implementada (25):**

| ID | Ferramenta | Decisão | O que falta |
|---|---|---|---|
| T1-ZAIOS-10 | ZAIOS | D1 | Retorno acumulado em 10 anos |
| T8-B08-03, T8-A09-03 | B08, A09 | D1 | "ROI" sem qualificador |
| T9-ZAIOS-06 | ZAIOS | D2-C | Referência da reserva 3% → 4% |
| T9-ZAIOS-07 | ZAIOS | D2-C | Faixa da reserva 3–5% → 3–6% (**achado novo deste comando**) |
| T9-J2-02 | Folha J2 | D2-C | Base da reserva: receita real → receita bruta realizada |
| T9-B08-01 | B08 | D2-C | Reserva dentro das deduções |
| T8-A09-04 | A09 | D2-C | Sem reserva de reposição nem rótulo |
| T9-ZAIOS-08 | ZAIOS | D3-A | Quebra medida em R$ |
| T8-B08-01, T9-B08-02, T8-A09-01, T9-A09-01 | B08, A09 | D3-A | Sem quebra nem rótulo |
| T10-ZAIOS-04 | ZAIOS | D4 | Distribuição e caixa disponível |
| T10-J2-02 | Folha J2 | D4 | Distribuição sem nome próprio |
| T8-B08-02, T8-A09-02 | B08, A09 | D4 | Sem pró-labore nem rótulo |
| T11-ZAIOS-02, T11-ZAIOS-03 | ZAIOS | D7-C | Métodos 2 e 3 e valor líquido |
| T8-B08-04, T11-B08-01 | B08 | D7-C | Residual em % do investimento, sem método |
| T7-ZAIOS-14 | ZAIOS | D11-A | Veredito com menos de 5 critérios e sem trava de homologação |
| T7-B08-01, T7-A09-01 | B08, A09 | D11-A | Sem contagem de critérios |
| T7-A09-02 | A09 | D11-A | Metas do aluno misturadas à régua |

**Decisões ainda pendentes (3):**

| ID | Ferramenta | Decisão | Diferença |
|---|---|---|---|
| T1-A09-07 | A09 | D5 | Noites por mês inteiras: 360 dias no máximo |
| T4-B06-05 | B06 | D6 | Contingência sobre todo o CAPEX (263.725) x base da ZAIOS (182.500) |
| T6-B08-01 | B08 | D8 | Payback acima de 10 anos devolve nulo |

## Dependências que impedem a execução independente

| Dependência | Afeta | Situação |
|---|---|---|
| **Cópia local do `src/calc` da ZAIOS** (`ZAIOS_CALC_DIR`) | 72 casos (T1 a T3, T5 cruzado, T6, T7, T9 a T11 da ZAIOS; valores da ZAIOS no T12) | **Principal dependência.** O código não está no repositório (público). Obter sem créditos, como descrito acima. Decisão do Bruno: manter fora ou guardar num repositório privado |
| LibreOffice + Python/openpyxl | 3 casos da F05 | Instalados nesta sessão; em outra máquina, sem eles, os casos ficam "não executados" |
| Node 22.6+ | casos da ZAIOS (TypeScript) | Node anterior não carrega `.ts` |
| Estrutura atual de B06, B08, A09 e Folha J2 | casos dessas ferramentas | Se os campos ou os nomes de saída mudarem numa correção aprovada, os casos de divergência devem ser revisados junto, sem mudar os valores esperados |

## Testes complementares (Comando 05E)

- `casos/c01_complementares.js`: B08 (rampa, reajuste, residual, equilíbrio), A09 (payback, gestão, 372 dias), B06 (3 perfis), F05 (diferença, R$/m², em branco), Folha J2 (indicadores, custos do modelo).
- `casos/c02_zaios_complementares.js`: ZAIOS (custos do modelo e EBITDA, outras receitas, estadia, sazonalidade, composição de `src/exercicios`, G2/G3).
- Esperados independentes: `independente/complementares_referencia.py` → `independente/esperados_complementares.json`.
- A composição precisa de uma cópia local da raiz do projeto ZAIOS (com `src/`), apontada por `ZAIOS_SRC_DIR`. O carregador `lib/zaios_comp.js` copia para uma pasta temporária e só ajusta os imports. O código não fica no repositório.

```
ZAIOS_CALC_DIR=<cópia de src/calc> ZAIOS_SRC_DIR=<cópia da raiz> node testes/financeiro/run.js --saida <pasta>
```

Execução de referência: `resultados/2026-11-09-05e-com-zaios/` (237 casos, 0 falhas) e `resultados/2026-11-09-05e-sem-zaios/`. Relatórios: `docs/academy/comando-05e/`.

## Composição da ZAIOS em 3 cenários (Comando 05F)

- Entradas: `composicao_05f/cenarios_05f.json`. Executor separado: `composicao_05f/run_05f.js` (não altera a suíte T1–T12 nem os casos C).
- Esperados independentes: `independente/composicao_05f_referencia.py` → `independente/esperados_05f.json`, em duas famílias: regra do comando (R1) e regra documentada da ZAIOS (R2).

```
python3 testes/financeiro/independente/composicao_05f_referencia.py
ZAIOS_SRC_DIR=<cópia da raiz> node testes/financeiro/composicao_05f/run_05f.js --saida <pasta>
```

Execução de referência: `resultados/2026-11-09-05f/` (288 campos: 249 OK, 32 divergências metodológicas, 7 não aplicáveis, 0 divergências matemáticas). Relatórios: `docs/academy/comando-05f/`.

## Limitações dos testes

1. **Interface não testada.** Os testes chamam o cálculo, não as telas. O que só aparece na tela é verificado pela presença de campos e textos no código-fonte das ferramentas (casos T7, T8, T11 de B08/A09): é um indicador, não prova de exibição. Isso inclui a seleção de veredito na ZAIOS, rótulos e leitura de números como "500.50".
2. **ZAIOS testada por cópia.** O resultado vale para a versão lida em 09/11/2026. Se o projeto Lovable mudar, a cópia precisa ser atualizada.
3. **Equivalência de cenário.** O A09 cobra custo variável por estadia: o cenário usa R$ 160 por estadia ÷ 2 noites = R$ 80 por noite. O B08 recebe as deduções como "imposto" (17%) com comissão zero. São premissas idênticas em valor, com nomes de campo diferentes.
4. **T2 usa a reserva v0 de 3%** porque os valores esperados do plano foram calculados assim. A reserva aprovada de 4% é testada no T9.
5. **T5** compara a cascata e o pró-labore. A igualdade completa de um mês entre Folha J2 e ZAIOS G2/G3 depende das decisões D12 e D14.
6. **T12 não aprova nem reprova.** Lista os valores em uso; a validação depende de evidências por tipo de hospedagem, porte e perfil.
7. **Nada é homologado por estes testes.** OK significa só que a fórmula reproduz o valor esperado do plano com a tolerância definida.
