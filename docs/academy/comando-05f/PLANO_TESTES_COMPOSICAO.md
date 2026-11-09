# Plano de testes da camada de composição

Comando 05F · 09/11/2026 · Escrito **antes** da execução, inclusive as tolerâncias. Somente leitura: nenhum arquivo da ZAIOS, fórmula ou parâmetro foi alterado.

## 1. Referências conferidas antes de começar

| Documento | Situação |
|---|---|
| `docs/academy/comando-05e/` (6 arquivos) | Existem, no commit `2135b2b` da main. Conteúdo relido. Hashes em `INTEGRIDADE_E_RASTREABILIDADE_05F.md` |
| `docs/academy/comando-05d/` (parecer, matriz, controle de versões, pendências) | Existem. Preservados sem alteração |
| `docs/academy/comando-05b/` (dicionário v0.4, decisões, plano de testes v0.2, auditoria) | Existem. Preservados sem alteração |
| Decisões pendentes D5, D6, D8, D9, D10, D12, D13, D14 | Registradas em `comando-05b/DECISOES_METODOLOGICAS.md` (seção 3) e `comando-05d/PENDENCIAS_HOMOLOGACAO.md` (seção 3) |

**Conferência dos números do 05E:**
- A composição tinha 17 casos: 16 de fórmula e 1 de divergência (veredito). Todos foram feitos num único cenário integrado.
- Os totais (98 casos complementares: 93 OK, 2 divergências, 3 limitações) batem com `testes/financeiro/resultados/2026-11-09-05e-com-zaios/resultado.json`.

## 2. Camada de composição (mapa)

Código lido do commit `ec21ad5`, cópia local fora do repositório.

| Função | Arquivo | Entradas | Saídas usadas |
|---|---|---|---|
| `calcularCapex(v)` | `src/exercicios/capex-calculo.ts` | 7 linhas de CAPEX, `contingencia_pct`, `perfil_risco`, `custo_fixo`, `unidades`, `terreno` | `mapa`: CAPEX, contingência, cronograma de desembolso, giro mínimo (6 × fixo), estresse |
| `lerMapaCapex(paraSalvar)` | idem | resultado salvo do P5 | mapa usado pela Viabilidade |
| `calcularReceitas(v, erros, contexto)` | `src/exercicios/receitas-calculo.ts` | unidades; temporadas (`meses_alta`, `meses_baixa`); diária e ocupação por temporada; `outras_pct`; `deducoes_pct`; `variavel_noite`; `custo_estadia`; `permanencia`; `quebra_pct`; `custo_fixo`; `horas_semana` × `custo_hora`; `aluguel`; `gestao_pct`; `royalty_pct`; `reserva_pct`; `mes_abertura` | `modeloP6`: ano de regime, 1º ano com rampa, margem operacional e régua, equilíbrio, déficit, capital de giro A/B, veredito |
| `calcularViabilidade(v, erros, contexto)` | `src/exercicios/viabilidade-calculo.ts` | `taxa_desconto`, `multiplo_saida`, `mes_abertura_projeto` (opcional) + contexto (mapa do P5, valores do P6, fixo do P5) | `estudoViabilidade`: captação, fluxo de 10 anos, retorno, payback simples e descontado, VPL e TIR com e sem saída, cenários, sensibilidade, estresse, curva de 36 meses, colchão, 5 passos, decisão, veredito |
| Primitivas | `src/calc/receitas.ts`, `capex.ts`, `viabilidade.ts` | — | mês a mês do P6, rampa, giro, equilíbrio, cronograma, VPL, TIR, payback, curva, régua |

**Dependências de G2 e G3:** nenhuma. A composição de viabilidade (P5 + P6) não importa `operacao.ts` nem `financas-calculo.ts`. G2/G3 são a gestão mensal real, um módulo separado, coberto no 05E. Os cenários do 05F não passam por G2/G3.

**Onde as parcelas se combinam** (mês a mês, em `calcularMesP6`):
1. noites vendidas = unidades × dias do mês × ocupação da temporada × fator de rampa;
2. diárias = noites × diária; outras = diárias × `outras_pct`; receita bruta = diárias + outras;
3. deduções = receita bruta × `deducoes_pct`; receita real = bruta − deduções;
4. custos variáveis = noites × `variavel_noite` + (noites ÷ permanência) × `custo_estadia` + diárias × `quebra_pct`;
5. resultado operacional = receita real − variáveis − (fixo + pró-labore);
6. custos do modelo = aluguel + **receita bruta** × (gestão + royalty);
7. EBITDA = resultado operacional − custos do modelo; geração = EBITDA − receita bruta × `reserva_pct`.

**Unidades:**
- dinheiro em centavos, sem arredondamento até a tela;
- percentuais como fração.

Os únicos arredondamentos são:
- o cronograma do P5, em centavos inteiros (o resto vai para o 1º mês da janela);
- a contingência, com `Math.round`.

Nos cenários abaixo, as linhas de CAPEX foram escolhidas divisíveis pelas janelas e a contingência é zero, então nenhum arredondamento interfere.

**Convenções temporais:**
- ano de 365 dias (meses de 28 a 31 dias), sem bissexto;
- rampa de 40%/50%/75% nos meses 1–3, 4–6 e 7–12 da operação;
- fluxo anual com ano 0 = −CAPEX (o capital de giro fica fora), ano 1 = 1º ano com rampa e anos 2 a 10 = regime;
- desconto no fim do ano;
- payback simples interpolado e estendido além do ano 10 pela geração do regime;
- payback descontado só dentro do horizonte;
- curva de 36 meses com a captação no mês 1 e a operação a partir do mês de abertura do projeto.

## 3. Método de comparação

Para cada campo há **dois esperados independentes**, calculados em Python por `testes/financeiro/independente/composicao_05f_referencia.py`. O script não importa nem executa código da ZAIOS.

| Família | Regra | Para que serve |
|---|---|---|
| **R1 · Regra do comando** | Como o Comando 05F descreve: gestão e royalties sobre a **receita de hospedagem**; outras receitas em R$ por ano; capital de giro **informado** | Mostra se a ZAIOS calcula o que o comando pede. Diferença com cálculo correto = **divergência metodológica** |
| **R2 · Regra documentada da ZAIOS** | Dicionário v0.4 e FORMULAS.md: gestão e royalties sobre a **receita bruta**; outras como % das diárias; capital de giro calculado (A = 6 × fixo; B = déficit da rampa + meses negativos + 3 × fixo) | Mostra se o código faz o que a documentação diz. Diferença = **divergência matemática** |

**Independência:**
- O Python foi escrito a partir das regras em texto, em outra linguagem, sem copiar nem chamar funções da ZAIOS.
- Limitação: quem escreveu o Python também leu o código da ZAIOS no 05E. A independência é de implementação e de fonte (texto), não de pessoa.
- A família R1 é independente da ZAIOS também na regra.

**Conversão das entradas para a ZAIOS:**
- outras receitas anuais em R$ viram `outras_pct` = outras ÷ diárias do ano de regime. Isso preserva o total anual do regime, mas distribui as outras pelos meses na proporção das diárias e aplica a rampa sobre elas.
- O comando não define como as outras receitas se comportam no 1º ano. Usamos a regra da ZAIOS e registramos isso como limitação.

## 4. Campos que o comando não informa (valores adotados, sem defaults silenciosos)

| Campo exigido pela ferramenta | Valor adotado | Justificativa |
|---|---|---|
| 7 linhas do CAPEX | Investimento × 12% infra, 6% projeto, 52% obra, 8% apoio, 15% FF&E, 2% OS&E, 5% pré-abertura | A ferramenta só calcula com as 7 linhas. A proporção é uma hipótese de teste: valores redondos e divisíveis pelas janelas. OS&E e pré-abertura ficam dentro das faixas de referência |
| Contingência | 0% | O comando trata o investimento como total. Um percentual mudaria o investimento informado. Efeito: a curva "com contingência usada" é igual à "sem", e o passo 5 da régua testa o colchão sem contingência |
| Perfil de risco | "primeira obra" | Só gera alerta (contingência abaixo da faixa). Não muda cálculo |
| Terreno | 0 | Fora do escopo. O retorno com terreno fica nulo |
| Custo variável por noite e quebra | 0 | O comando informa só o custo por estadia. **A quebra de 1% (D3-A) não foi aplicada:** o teste não representa a metodologia aprovada |
| Reserva de reposição | 0% | O comando não informa. **A reserva de 4% (D2-C) não foi aplicada.** A ressalva da faixa de 3–5% da ZAIOS continua aberta |
| Pró-labore (horas × R$/hora) | 0 | Não informado |
| Comissões de canais | 0 (deduções = só tributos) | O comando informa só tributos sobre vendas. Na ZAIOS, `deducoes_pct` costuma somar comissões e tributos (referência de 17%, H4) |
| Taxa de desconto | 10% a.a. | A mesma dos testes da própria ZAIOS. Hipótese de teste (H4) |
| Múltiplo de saída | 6× EBITDA | Referência da ZAIOS (H4) |
| Custo fixo do P5 (base do giro A) | Igual ao custo fixo mensal do comando | O giro A usa o fixo do P5. Os dois foram mantidos iguais, inclusive no estresse |
| Mês de abertura (calendário) | C1 janeiro; C2 março; C3 outubro | O comando não informa. Meses diferentes testam a rampa com e sem sazonalidade |
| Mês do projeto em que a hospedagem abre | Não informado: a ferramenta usa o sugerido pelo cronograma (mês 10) | Valor derivado pela própria regra |
| Sazonalidade (C2) | Alta: jan, fev, jul, dez (121 dias) a 75%. Média: mar, ago, out, nov (123 dias) a 58%. Baixa: abr, mai, jun, set (121 dias) a 41%. Diária de R$ 690 em todas as temporadas | A ZAIOS trabalha com 3 temporadas (diária e ocupação por temporada), não com multiplicadores mensais. Média ponderada pelos dias: (121 × 0,75 + 123 × 0,58 + 121 × 0,41) ÷ 365 = 0,58. Diária constante para manter a diária média exata em R$ 690 |
| Estresse (C3E) | Ocupação 0,496; diária R$ 855; fixo R$ 109.250 (também no P5); estadia R$ 176; **outras mantidas em R$ 480.000** (o `outras_pct` foi recalculado) | "Manter os demais parâmetros constantes". Com o percentual antigo, as outras receitas cairiam junto com as diárias. Aluguel, gestão, royalty, tributos e investimento constantes |
| Capital de giro informado | Não há campo na ZAIOS | A ferramenta calcula o giro recomendado. O valor informado entra só na família R1 |

## 5. Tolerâncias (fixadas antes da execução)

| Grandeza | Tolerância | Motivo |
|---|---|---|
| Dinheiro | R$ 0,01 (absoluta) | Os dois lados usam precisão completa, sem arredondamento |
| Frações (ocupação, margem, retorno, TIR, colchão) | 0,000001 (absoluta) | Mais rigorosa que a do 05E (0,0001), porque não há arredondamento intermediário |
| Anos (payback) e noites | 0,000001 | idem |
| Textos, listas e indicadores nulos | Igualdade exata (nulo só é OK se os dois lados forem nulos) | — |

Diferenças de arredondamento (abaixo da tolerância) aparecem como OK, com a diferença registrada.

## 6. Classificação

- **OK:** confere com a regra de referência.
- **DIVERGÊNCIA MATEMÁTICA:** difere da regra documentada da ZAIOS (R2) além da tolerância.
- **DIVERGÊNCIA METODOLÓGICA:** confere com R2, mas difere da regra do comando (R1).
- **LIMITAÇÃO:** não dá para concluir por falta de definição.
- **NÃO APLICÁVEL:** o indicador não pode ser calculado legitimamente no cenário (por exemplo, TIR sem troca de sinal). Só é OK se a ZAIOS também não apresentar número.

Além disso, há uma **leitura econômica** de cada cenário: verificar se os números fazem sentido e se a apresentação não induz a conclusões indevidas.

## 7. Execução

```
python3 testes/financeiro/independente/composicao_05f_referencia.py
ZAIOS_SRC_DIR=<cópia local da raiz da ZAIOS> node testes/financeiro/composicao_05f/run_05f.js --saida testes/financeiro/resultados/2026-11-09-05f
```

Os resultados vão para uma pasta nova, sem sobrescrever o 05C, o 05D nem o 05E.
