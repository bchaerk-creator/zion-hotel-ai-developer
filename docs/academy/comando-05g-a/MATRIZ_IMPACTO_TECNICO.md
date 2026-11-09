# Matriz de impacto técnico · O8 a O14

Comando 05G-A · 09/11/2026 · Levantamento por leitura do código da ZAIOS no commit `ec21ad5`. Nenhuma alteração foi feita.

- **Fonte dos caminhos e linhas:** cópia local, fora do repositório. Os arquivos de cálculo são os mesmos do 05E/05F. Os de interface, dossiê e dados foram lidos neste comando (`read_file` no commit `ec21ad5`).
- **Linhas citadas:** valem para esse commit.
- Nenhum trecho de código da ZAIOS é reproduzido além do mínimo necessário para identificar a fórmula.

## 0. Mapa dos módulos envolvidos

| Camada | Arquivo | Papel |
|---|---|---|
| Cálculo (primitivas) | `src/calc/receitas.ts` | Mês do P6 (`calcularMesP6`), rampa, `capitalGiro`, `pontoEquilibrio`, `reguaMargem`, constantes (`MESES_GIRO_A=6`, `MESES_GIRO_B=3`, `RESERVA_FAIXA`) |
| Cálculo (primitivas) | `src/calc/viabilidade.ts` | `fluxoProjeto` (10 anos), `valorSaida`, `comSaida`, `vpl`, `tir`, `paybackSimples` e `paybackDescontado`, `curvaCaixa` (`MESES_CURVA=36`), `ATRASO_ABERTURA=6`, passos da régua |
| Cálculo (primitivas) | `src/calc/capex.ts` | `capitalGiroMinimo` (`MESES_GIRO=6`), `necessidadeTotalCapital`, `cronogramaDesembolso` |
| Composição | `src/exercicios/receitas-calculo.ts` | `calcularReceitas`: monta os `ParametrosP6` (linhas 52–57), margem e régua (63, 72), giro (69–70, 77), **veredito do P6 (94–97)** |
| Composição | `src/exercicios/viabilidade-calculo.ts` | `calcularViabilidade`: saída (121), cenários e sensibilidade, captação (140), curva (142–146), atraso (148–150), passos, **veredito (172)** |
| Composição | `src/exercicios/capex-calculo.ts` | `calcularCapex`: giro mínimo do P5 (61) e necessidade total (71) |
| Campos (formulário) | `src/exercicios/receitas.ts` | Campos do P6: `outras_pct` (34), `custo_fixo` (41), `aluguel` (44), `gestao_pct` (45, rótulo "% da receita bruta"), `royalty_pct` (46, idem), `reserva_pct` (47, faixa 3–5%) |
| Campos | `src/exercicios/viabilidade.ts` | `taxa_desconto`, `multiplo_saida`, `mes_abertura_projeto` |
| Campos | `src/exercicios/capex.ts` | `custo_fixo` do P5 (49), "usado para calcular o capital de giro mínimo" |
| Interface | `src/components/zion/ResultadoPilar.tsx` | Mostra o **selo** (`SeloVeredito`) de qualquer pilar (linha 7) |
| Interface | `src/components/zion/ResultadoReceitas.tsx` | Demonstrativo do P6; margem e régua (34); giro A/B (65–68) |
| Interface | `src/components/zion/ResultadoViabilidade.tsx` | Caixa da decisão (44–48); valor de saída (59); estresse e atraso (78–82); curva de 36 meses (20, 88–93); colchão (93); passos (95–100); decisão (101) |
| Interface | `src/lib/viabilidade-texto.ts` | Formatação de payback, TIR, passos e cenários |
| Tipos | `src/exercicios/tipos.ts` | `Veredito.selo` = "Avançar" \| "Testar" \| "Ajustar" \| "Pausar" \| "Redesenhar" \| "Não se aplica" (linha 22); `ResultadoBase` (25) |
| Persistência | `src/lib/exercicios.ts` + tabela `respostas_exercicios` (migração 0001) | Uma linha por exercício: `respostas` (jsonb, com `valores`), `resultado` (jsonb = `paraSalvar`), `insumos_snapshot` (jsonb), `versao` |
| Relatórios | `src/lib/dossie.ts` | Seção do P6 (linhas 154–171), seção 7 do CAPEX (giro mínimo e necessidade total, 172–188), seção 10 de viabilidade e resumo com a decisão (189–214) |
| Relatórios | `src/lib/dossie-pdf.ts` | Monta o PDF a partir do objeto do dossiê. Sem lógica financeira própria (impacto indireto) |
| Integrações | — | Nenhuma integração externa (ClickMax, Asaas) usa estes cálculos. O impacto é interno à ZAIOS e ao banco de dados dela |

## 1. Matriz por decisão

### O8 · Avaliação preliminar do P6

| Item | Registro |
|---|---|
| Módulo | P6 Receitas (composição + interface + dossiê) |
| Arquivo e função | `receitas-calculo.ts` → `calcularReceitas` (veredito nas linhas 94–97; margem 63; régua 72); `ResultadoPilar.tsx` (selo, linha 7); `ResultadoReceitas.tsx` (margem e régua, 34); `dossie.ts` (margem e régua, 159) |
| Fórmula atual | Selo "Ajustar" se a margem operacional < 10% ou a folga do equilíbrio < 0; senão "Avançar". Margem operacional = resultado operacional ÷ receita bruta, **antes** de aluguel, gestão e royalties. Régua: ≥30% "boa", ≥20% "viável", ≥10% "apertada", <10% "não fecha" |
| Interface atual | O selo do P6 aparece no topo do pilar, com o mesmo componente dos outros pilares e o mesmo peso visual da decisão da viabilidade. Não há aviso de conflito com a viabilidade |
| Divergência | O selo "Avançar" funciona como aprovação. Não há subordinação à análise completa. No C3E: P6 "Avançar" x viabilidade "Redesenhar", sem aviso |
| Alteração proposta | (a) Trocar o veredito do P6 por um estado de **indicação preliminar**, sem os selos "Avançar", "Ajustar" e "Redesenhar". Exige um novo valor ou tipo em `Veredito` (`tipos.ts`, 22), ou um campo separado para a indicação. (b) Mostrar a margem antes **e** depois dos custos do modelo, com nomes distintos (ex.: "margem operacional" e "margem EBITDA"). (c) Na viabilidade e no dossiê, quando a indicação do P6 for positiva e a decisão for "Ajustar" ou "Redesenhar", mostrar um aviso de conflito explícito, com a viabilidade prevalecendo. (d) Texto fixo: "indicação inicial, subordinada à análise financeira completa" |
| Dependências | D11-A (veredito só após homologação) e o risco já registrado do veredito antecipado: as duas mudanças devem ser feitas juntas. P-O8 (rótulo). O plano de melhoria e as pendências podem consumir o veredito (verificar `plano-regras.ts` e `pendencias.ts` antes de implementar) |
| Risco de regressão | **Médio.** O tipo `Veredito` é compartilhado por todos os pilares. Mudar o enum pode afetar o selo de outros pilares, a jornada, o dossiê e as pendências geradas pelo selo "Ajustar" (linha 98) |
| Testes | O8-1, O8-2, O8-3 (`PLANO_TESTES_REGRESSAO.md`) + regressão visual dos outros pilares |
| Critério de aceite | Em nenhum cenário o P6 exibe "Avançar", "Ajustar", "Redesenhar", "Aprovado" ou "Viável". O C3E mostra o aviso de conflito. O C1 mostra a margem antes (19,93%) e depois (−8,94%) dos custos do modelo |

### O9 · Valor de saída com EBITDA negativo

| Item | Registro |
|---|---|
| Módulo | P6 Viabilidade (primitiva + composição + interface + dossiê) |
| Arquivo e função | `calc/viabilidade.ts` → `valorSaida` (linha 31); usado em `viabilidade-calculo.ts` (`estudoFluxo`, saída 121, cenários); `ResultadoViabilidade.tsx` (59); `dossie.ts` (206) |
| Fórmula atual | Valor de saída = múltiplo × EBITDA do regime (pode ser negativo). Somado ao ano 10 (`comSaida`) |
| Interface atual | Mostra "Valor de saída no ano 10 (múltiplo × EBITDA do regime)" com o sinal (ex.: −R$ 92.517,75) |
| Divergência | A diretriz exige MAX(0, EBITDA × múltiplo) e proíbe apresentar valor negativo como preço |
| Alteração proposta | `valorSaida` passa a devolver `max(0, múltiplo × EBITDA)` e um indicador de "EBITDA negativo: saída por múltiplo zerada". A interface e o dossiê mostram a nota. Dívidas e custos de encerramento ficam fora (não modelados hoje: registrar no texto) |
| Dependências | D7-C (três métodos e valor líquido): a O9 vale para o método 1 (múltiplo). Cenários (VPL com saída por cenário) e TIR com saída usam a mesma função |
| Risco de regressão | **Baixo.** Uma função pura. Muda só quando o EBITDA < 0. Os testes da ZAIOS (`viabilidade.test.ts`) não testam saída com EBITDA negativo, pela leitura do 05E |
| Testes | O9-1, O9-2, O9-3 |
| Critério de aceite | C1: saída = 0, VPL com saída = VPL sem saída = −R$ 891.343,30, TIR com saída inexistente. C2: saída = R$ 3.312.531,36 (sem mudança) |

### O10 · Horizonte de fluxo de caixa

| Item | Registro |
|---|---|
| Módulo | P6 Viabilidade (primitiva + composição + interface + dossiê) |
| Arquivo e função | `calc/viabilidade.ts` → `curvaCaixa` (123; `MESES_CURVA=36`, linha 5), `geracoesOperacao`, `fluxoProjeto` (19), `ATRASO_ABERTURA` (10); `viabilidade-calculo.ts` (curva 142–146 com 36 fixo na 144, atraso 148–150); `ResultadoViabilidade.tsx` (curva e escala fixa em 35 meses, linhas 15–31; textos 79–93) |
| Fórmula atual | Fluxo anual de 10 anos (ano 1 com rampa, anos 2 a 10 regime) para VPL, TIR e payback. Curva **mensal só de 36 meses** para o menor saldo e o colchão. Atraso: a mesma curva de 36 meses com a abertura 6 meses depois |
| Interface atual | Gráfico e tabela de 36 meses. O atraso mostra só o menor saldo e o saldo no mês 36 |
| Divergência | Não há visão dos anos 4 a 10 no caixa, nem alerta de caixa negativo depois do mês 36 (C1: negativo no mês 54). O atraso pode "melhorar" o menor saldo (C1, C2, C3E) sem explicação |
| Alteração proposta | (a) Curva de 120 meses: mensal nos meses 1 a 36 e agregada por ano do 4º ao 10º. (b) Alerta de cada período com saldo negativo e **capital adicional necessário** = −menor saldo em 120 meses. (c) Atraso medido no mesmo horizonte: perda de receita, despesas no período, investimento, financiamento (captação), saldo final e VPL. Proibir a leitura "melhora" sem a decomposição. (d) Indicadores (VPL, TIR, payback, colchão) declarados para o mesmo horizonte |
| Dependências | P-O10a, P-O10b, P-O10c (convenções); D8 (payback estendido); D6 (contingência); O13 (captação adicional = déficit + necessidade dos anos 4–10) |
| Risco de regressão | **Alto.** Mexe na curva, no colchão (passo 5 da régua), no atraso, no gráfico e no dossiê. Pode mudar a decisão de projetos existentes (ex.: o colchão passa a considerar 120 meses) |
| Testes | O10-1, O10-2, O10-3 + regressão da régua nos 5 cenários do 05E/05F |
| Critério de aceite | C1: menor saldo nos 36 meses = R$ 22.704,75 (positivo); 1º mês negativo = 54 (ano 5); capital adicional = R$ 85.232,63. C2: saldo em 120 meses com atraso < sem atraso (perda de R$ 256.539,15 no horizonte), com a decomposição exibida |

### O11 · Bases de gestão e royalties

| Item | Registro |
|---|---|
| Módulo | P6 Receitas (primitiva + composição + campos + interface + dossiê) |
| Arquivo e função | `calc/receitas.ts` → `calcularMesP6` (custos do modelo, linha 56) e `pontoEquilibrio` (97–104, que também usa receita bruta × (gestão + royalty)); `receitas-calculo.ts` (52–57); `receitas.ts` (45–46, rótulos já dizem "em percentual da receita bruta"); `ResultadoReceitas.tsx` (custos do modelo numa linha única); `dossie.ts` (158) |
| Fórmula atual | Custos do modelo = aluguel + receita bruta × (gestão + royalty). Mesma base fixa para as duas taxas |
| Interface atual | A base aparece no rótulo do campo ("% da receita bruta"), mas não é configurável. O demonstrativo mostra só o total dos custos do modelo |
| Divergência | Falta base configurável e independente para cada taxa. Falta o rótulo de hipótese quando o contrato não define a base. Gestão e royalties não aparecem separados nos relatórios |
| Alteração proposta | Novos campos `gestao_base` e `royalty_base` ("hospedagem" ou "bruta"), cada um com a indicação "contratual" ou "hipótese". `ParametrosP6` ganha as duas bases. `calcularMesP6` e `pontoEquilibrio` calculam cada taxa sobre a sua base. O demonstrativo e o dossiê mostram aluguel, gestão (base e %) e royalties (base e %) em linhas separadas |
| Dependências | O6 (modalidade em R$ x %, ainda aberta); O14 (o que entra em "receita bruta" com as categorias); P-O11. Cenários e sensibilidade herdam a base |
| Risco de regressão | **Médio.** O padrão precisa preservar o resultado atual (base = receita bruta) nas respostas já salvas, para não mudar números sem aviso |
| Testes | O11-1, O11-2 + regressão: base padrão = bruta reproduz os 288 campos do 05F |
| Critério de aceite | C2, as quatro combinações: EBITDA de R$ 571.888,56 (hosp/hosp), R$ 564.688,56 (hosp/bruta), R$ 559.288,56 (bruta/hosp) e R$ 552.088,56 (bruta/bruta, igual ao atual). Cada diferença = % × R$ 180.000 |

### O12 · Base do capital de giro

| Item | Registro |
|---|---|
| Módulo | P6 Receitas e P5 CAPEX (primitivas + composição + interface + dossiê) |
| Arquivo e função | `calc/receitas.ts` → `capitalGiro` (107–111; A = 6 × fixo sem retirada; B = déficit + meses negativos + 3 × fixo com retirada); `receitas-calculo.ts` (`fixoA` = fixo do P5 ou do P6, linhas 69–70, 77); `calc/capex.ts` → `capitalGiroMinimo` (42–47; 6 × fixo do P5) e `necessidadeTotalCapital` (49); `capex-calculo.ts` (61, 71); `ResultadoReceitas.tsx` (65–68); `dossie.ts` (168, 183–184) |
| Fórmula atual | Duas definições de giro: **P5:** "capital de giro mínimo" = 6 × custo fixo do P5, e "necessidade total" = CAPEX + esse giro. **P6:** recomendado = max(A, B). O aluguel não entra no A nem nos "3 × fixos" do B. No B, entra indiretamente pelo déficit e pelos meses negativos (via geração de caixa) |
| Interface atual | O P6 mostra A, B, sazonalidade e recomendado. O dossiê mostra o giro mínimo do P5 **e** o recomendado do P6 (dois números diferentes para o mesmo conceito) |
| Divergência | O aluguel e as obrigações fixas recorrentes não entram na base. Os 6 meses estão fixos (não aprovados como universais). Há duplicidade de conceitos (P5 x P6) |
| Alteração proposta | (a) Base mensal do giro = custos fixos operacionais + aluguel + outras obrigações fixas recorrentes (lista explícita), contando cada item uma vez. (b) Prazo ou método parametrizado (P-O12), em vez dos 6 e 3 fixos. (c) Uma única definição de "capital de giro necessário", usada no P5, no P6, na viabilidade e no dossiê. No P5, rotular como estimativa preliminar ou remover. (d) Alerta se o aluguel também foi digitado dentro do custo fixo |
| Dependências | P-O12 e D12 (fôlego); O13 (o necessário é a referência do déficit); O10 (método compatível com a curva de 120 meses); a reserva de reposição (D2-C) continua separada do giro |
| Risco de regressão | **Médio a alto.** Muda a captação, a curva, o colchão, a decisão e o dossiê do P5 e do P6 |
| Testes | O12-1, O12-2, O12-3 |
| Critério de aceite | A base mensal com aluguel = R$ 12.000 (C1), R$ 36.000 (C2) e R$ 125.000 (C3), cada um contado uma vez. Um único valor de giro necessário em todas as telas e no dossiê |

### O13 · Capital de giro necessário x disponível

| Item | Registro |
|---|---|
| Módulo | P6 Viabilidade (composição + campos + interface + dossiê); possivelmente P5 |
| Arquivo e função | `viabilidade-calculo.ts` (giro 112, captação 140, curva 142–146); `viabilidade.ts` (campos); `ResultadoViabilidade.tsx` (texto da captação, 90); `dossie.ts` (resumo e seção 10) |
| Fórmula atual | Captação = CAPEX + giro recomendado. Não há campo de giro disponível. A curva começa com a captação completa no mês 1 |
| Interface atual | "Mês 1: entra a captação de R$ X (CAPEX + capital de giro recomendado)" |
| Divergência | Faltam o disponível, a diferença (déficit ou excedente) e o déficit na necessidade de captação |
| Alteração proposta | Novo campo `giro_disponivel` (moeda, informado). Saídas: `giroNecessario` (técnico), `giroDisponivel`, `diferenca`, `deficit`, `excedente`. Usos = CAPEX + necessário. Fontes = disponível + captação adicional (= déficit). A curva técnica usa o necessário. O disponível nunca o substitui e nunca é somado duas vezes |
| Dependências | O12 (definição do necessário); O10 (capital adicional dos anos 4–10 também entra na necessidade de captação); P-O13; D4 (caixa disponível: conceito diferente, cuidar dos nomes) |
| Risco de regressão | **Médio.** Novo campo opcional. Sem o campo preenchido, o resultado atual deve se manter |
| Testes | O13-1 a O13-4 |
| Critério de aceite | C1 com disponível de R$ 45.000: necessário R$ 109.095,26 (regra atual); déficit R$ 64.095,26; usos R$ 859.095,26; captação adicional para giro R$ 64.095,26; curva técnica com menor saldo de R$ 22.704,75 (não −R$ 41.390,51). C2 com R$ 200.000: excedente R$ 32.000 |

### O14 · Receitas complementares

| Item | Registro |
|---|---|
| Módulo | P6 Receitas (primitiva + composição + campos + interface + dossiê); Viabilidade (cenários e sensibilidade) |
| Arquivo e função | `calc/receitas.ts` → `calcularMesP6` (outras = diárias × `outrasPct`, linha 47) e `ParametrosP6`; `receitas-calculo.ts` (54); `receitas.ts` (34, "Outras receitas, em percentual das diárias"); `viabilidade-calculo.ts` → `cenarioP6` (ajusta só diária e ocupação; as outras acompanham por serem %); `dossie.ts` (158) |
| Fórmula atual | Uma única linha "outras" = % das diárias: acompanha ocupação, diária, rampa e cenários. Tributos sobre a receita bruta inteira (inclui outras). Nenhum custo associado específico |
| Interface atual | Um campo percentual. O demonstrativo não separa as outras receitas (só a receita bruta) |
| Divergência | Não há categorias A, B e C, nem fatores próprios, nem custos associados. Receitas independentes caem com a ocupação (C3E: R$ 345.600 em vez de R$ 480.000) |
| Alteração proposta | Lista de receitas complementares com categoria: **A** (por noite ou por hóspede × fator); **B** (estadias × adesão × ticket); **C** (valor mensal ou anual fixo, com sazonalidade própria opcional). Cada uma com custo associado (%) e alíquota (D14). Rampa e cenários aplicados por categoria (P-O14b). O demonstrativo e o dossiê mostram cada categoria. Migração do `outras_pct` atual para a categoria A (% das diárias), sem mudar resultados salvos sem aviso |
| Dependências | D9 (custo por noite ou estadia), D14 (taxa de limpeza, alíquotas), D10 (cenários), O11 (base "bruta"), P-O14a a P-O14d. G2/G3 (gestão mensal) têm categorias reais próprias: alinhar os nomes |
| Risco de regressão | **Alto.** Mudança no modelo de dados das respostas, no demonstrativo, nos cenários, na sensibilidade, no giro (meses negativos) e no dossiê |
| Testes | O14-1, O14-2 + migração (respostas antigas reproduzem o resultado atual) |
| Critério de aceite | C3 → C3E: a categoria C fica em R$ 480.000 (sem queda); a A cai 20% (R$ 181.040 → R$ 144.832); a B cai 20% pelas estadias (R$ 132.008,33 → R$ 105.606,67). A receita de hospedagem não muda ao incluir complementares |

## 2. Impactos separados por natureza

| Natureza | O8 | O9 | O10 | O11 | O12 | O13 | O14 |
|---|---|---|---|---|---|---|---|
| **Cálculo financeiro** | Margem EBITDA nova; lógica do estado preliminar | `valorSaida` | `curvaCaixa` 120 meses; atraso; capital adicional | `calcularMesP6`, `pontoEquilibrio` | `capitalGiro`, `capitalGiroMinimo` | Diferença, déficit, fontes e usos | `calcularMesP6`, `cenarioP6`, categorias |
| **Interface e experiência** | Fim do selo no P6; aviso de conflito | Nota "saída zerada" | Gráfico de 10 anos (36 meses + anos), alertas, decomposição do atraso | 2 campos de base + rótulo de hipótese; linhas separadas | Base do giro explícita; um só giro | Campo de giro disponível; déficit ou excedente | Lista de receitas por categoria |
| **Modelo de dados** | Tipo `Veredito` (TS); `resultado` salvo (JSON) | `resultado` salvo (JSON) | `resultado` salvo (estudo maior) | Novos valores nas respostas (JSON) | Possíveis novos valores (obrigações fixas, prazo) | Novo valor nas respostas | Estrutura de lista nas respostas + migração do `outras_pct` |
| **Relatórios e exportações** | `dossie.ts` (159, 197) | `dossie.ts` (206) | `dossie.ts` (209) | `dossie.ts` (158) | `dossie.ts` (168, 183–184) | `dossie.ts` (seção 10) | `dossie.ts` (158) |
| **Integrações** | Nenhuma externa | Nenhuma | Nenhuma | Nenhuma | Nenhuma | Nenhuma | Nenhuma |
| **Testes automatizados** | Novos + regressão de selos | Novos | Novos + régua | Novos + padrão = atual | Novos | Novos | Novos + migração |

**Modelo de dados (confirmado):**
- `drizzle/schema.ts` está vazio ("auto-generated and intentionally left blank"). A estrutura real está nas migrações SQL.
- A migração `0001_etapa2_respostas_custos_guarda_admin.sql` cria `respostas_exercicios` com `respostas jsonb`, `resultado jsonb`, `insumos_snapshot jsonb`, `versao integer` e chave única (empreendimento, slug).
- **Os novos campos de O11, O12, O13 e O14 cabem no JSON existente, sem migração de tabela e sem alteração de permissões (RLS).**
- O que exige cuidado é a compatibilidade:
  - respostas já salvas não têm os campos novos e precisam de valor padrão que preserve o resultado atual;
  - resultados (`resultado`) e versões de dossiê já gravados guardam o formato antigo;
  - as funções de leitura (`lerModeloP6`, `lerEstudoViabilidade`, `lerMapaCapex`) precisam aceitar os dois formatos.
- O nome da migração `0003_dossie_versoes_imutaveis` indica que versões antigas do dossiê não são alteradas. O conteúdo dessa migração não foi lido; conferir antes da implementação.

## 3. Rastreabilidade decisão → código → teste

| Decisão | Código afetado (arquivo: linhas em `ec21ad5`) | Teste de aceite |
|---|---|---|
| O8 | `receitas-calculo.ts`: 63, 72, 94–98 · `tipos.ts`: 22 · `ResultadoPilar.tsx`: 7 · `ResultadoReceitas.tsx`: 34 · `viabilidade-calculo.ts`: 172 · `dossie.ts`: 159, 197 | O8-1, O8-2, O8-3, INT-1 |
| O9 | `calc/viabilidade.ts`: 31–35 · `viabilidade-calculo.ts`: 116–121, cenários · `ResultadoViabilidade.tsx`: 59 · `dossie.ts`: 206 | O9-1, O9-2, O9-3, INT-1 |
| O10 | `calc/viabilidade.ts`: 5, 10, 19–21, 109–135 · `viabilidade-calculo.ts`: 140–150 · `ResultadoViabilidade.tsx`: 12–31, 77–93 · `dossie.ts`: 209 | O10-1, O10-2, O10-3, INT-1 |
| O11 | `calc/receitas.ts`: 27–31, 56, 97–104 · `receitas-calculo.ts`: 52–57 · `receitas.ts`: 45–46 · `ResultadoReceitas.tsx`: 27 · `dossie.ts`: 158 | O11-1, O11-2, INT-1 |
| O12 | `calc/receitas.ts`: 9–10, 107–111 · `receitas-calculo.ts`: 68–70, 77 · `calc/capex.ts`: 11, 42–51 · `capex-calculo.ts`: 61, 71 · `capex.ts`: 49 · `ResultadoReceitas.tsx`: 65–68 · `dossie.ts`: 168, 183–184 | O12-1, O12-2, O12-3 |
| O13 | `viabilidade-calculo.ts`: 112, 140–146 · `viabilidade.ts`: campos · `ResultadoViabilidade.tsx`: 90 · `dossie.ts`: seção 10 | O13-1 a O13-4, INT-1 |
| O14 | `calc/receitas.ts`: 27–31, 47–48 · `receitas-calculo.ts`: 54 · `receitas.ts`: 34 · `viabilidade-calculo.ts`: `cenarioP6` · `dossie.ts`: 158 | O14-1, O14-2 |

As linhas são do commit `ec21ad5`. Qualquer edição posterior na ZAIOS exige refazer este mapa.
