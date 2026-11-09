# Parecer de homologação matemática condicionada

Comando 05D · 09/11/2026 · Responsável: Bruno Chaerk · Revisão técnica: Claude Code (sessão ZAIOS platform development) · **Status: parecer para revisão. Não é homologação definitiva. Implementação bloqueada.**

Documentos de apoio:
- `MATRIZ_EVIDENCIAS_TESTES.md`
- `CONTROLE_VERSOES_FINANCEIRAS.md`
- `PENDENCIAS_HOMOLOGACAO.md`
- `testes/financeiro/independente/RESULTADO_INDEPENDENTE.md`

---

## 1. Resumo executivo

1. **Suíte conferida:** os 139 casos da suíte T1–T12 estão íntegros. Os IDs são únicos, as categorias são mutuamente exclusivas e não há falha de fórmula nem erro.
   - 96 casos de fórmula correta.
   - 25 divergências da metodologia aprovada.
   - 3 diferenças ligadas a decisões pendentes.
   - 15 parâmetros econômicos.
2. **Os valores esperados não são cópia da lógica testada.** Uma implementação independente (Python, a partir do dicionário v0.4, sem ler o código das ferramentas, com TIR por método diferente) reproduz **79 de 79** valores numéricos. Ela confere tanto com o valor esperado do plano quanto com o valor obtido da ferramenta. Os outros 17 casos de fórmula conferem por definição.
3. **Nenhuma inconsistência matemática foi encontrada.** Nenhum grupo de cálculo ficou em H3.
4. **As diferenças entre as ferramentas são de metodologia ou de cobertura, não de matemática:**
   - 25 divergências de decisões aprovadas;
   - 3 de decisões pendentes;
   - lacunas de cobertura que levam alguns grupos a H2.
5. **Recomendação:** conceder **homologação matemática condicionada**:
   - em **H1**, aos grupos de cálculo indicados na seção 4, para as versões registradas;
   - em **H2**, aos demais, com as ressalvas listadas.

   **Não há homologação econômica nem financeira global.** Percentuais, limites da régua, múltiplos e tributos continuam H4.

## 2. Os quatro níveis de avaliação

| Nível | Pergunta | Este parecer |
|---|---|---|
| 1 · Correção matemática | A fórmula calcula certo com os insumos dados? | **Avaliado** (H1, H2, H3) |
| 2 · Conformidade metodológica | A ferramenta segue o dicionário e as decisões aprovadas? | **Registrado**, não homologado (as 25 divergências) |
| 3 · Validade econômica | Os parâmetros (17%, 1%, 4%, 6×, 8/12 anos…) são adequados? | **Fora do escopo** (H4) |
| 4 · Viabilidade de um empreendimento | Um projeto específico é viável? | **Fora do escopo.** Nenhuma ferramenta nem este parecer atestam isso |

Uma fórmula H1 pode, ao mesmo tempo, estar fora da metodologia aprovada. Exemplo: a reserva de 3% da ZAIOS calcula certo, mas a referência aprovada é 4%.

## 3. Metodologia de revisão

1. **Integridade da suíte:** contagem, unicidade de IDs, exclusividade de categorias, coerência entre tipo e status (seção 1 da matriz).
2. **Rastreio das versões:** commit e hash de cada módulo (controle de versões). Para a ZAIOS, o commit Lovable `ec21ad5` e a cópia local fora do repositório.
3. **Verificação independente:**
   - nova implementação, a partir das definições, em outra linguagem;
   - dados de entrada lidos sem executar o código das ferramentas: perfil do B06 em JSON, itens da F05 por leitura literal de `dados.py`, campos do exemplo da Folha J2;
   - TIR por secante, contra a bisseção das ferramentas;
   - payback, VPL, cascata e equilíbrio reescritos.
4. **Auditoria do código** de cada ferramenta nos 14 temas pedidos: bases, unidades, sinais, periodicidade, arredondamento, dupla contagem (seção 5).
5. **Classificação por grupo de cálculo** em H1 a H4 (seção 4).

**Limite de independência:** o plano, os valores esperados e a verificação independente foram produzidos pela mesma equipe técnica. São independentes do código, não da metodologia. Uma conferência externa (contador ou analista financeiro) é recomendada antes da homologação definitiva.

## 4. Resultados por ferramenta e grupo de cálculo

**Legenda:**
- **H1:** homologável.
- **H2:** homologável com ressalvas.
- **H3:** não homologável.
- **H4:** fora do escopo matemático.
- **N/I:** não implementado na ferramenta (divergência metodológica, não matemática).
- **—:** não se aplica.

| Grupo de cálculo | ZAIOS (`src/calc`, ec21ad5) | B08 | A09 | B06 | F05 | Folha J2 |
|---|---|---|---|---|---|---|
| Receita, ocupação, noites | **H1** | **H1** | **H2** (D5: no máximo 360 dias pela interface) | — | — | **H2** (só o exemplo) |
| Deduções e custos variáveis | **H1** | **H1** | **H1** (observação O2: gestão como dedução) | — | — | **H2** |
| Quebra e perdas | **H1** (percentual); valor em R$ N/I (D3-A) | N/I (D3-A) | N/I (D3-A) | — | — | **H2** (percentual e valor medido conferem) |
| Reserva de reposição (mecânica) | **H1** (base receita bruta) | **H2** (calcula como dedução; D2-C) | N/I (D2-C) | — | — | **H2** (base receita real; D2-C) |
| Pró-labore | **H1** | N/I (D4) | N/I (D4) | — | — | **H2** |
| Distribuição e caixa disponível | N/I (D4) | N/I | N/I | — | — | N/I (bloco de caixa não testado) |
| Resultado operacional | **H1** | **H1** | **H1** | — | — | **H2** |
| EBITDA | **H2** (custos do modelo não testados) | — | — | — | — | **H2** (custos do modelo zero no exemplo) |
| Retorno anual | **H1** | **H1** (rótulo "ROI": D1) | **H1** (rótulo "ROI": D1) | — | — | — |
| Retorno acumulado em 10 anos | N/I (D1) | **H1** (valor; rótulo D1) | — | — | — | — |
| VPL e TIR | **H1** | **H2** (só sem rampa, reajuste e residual) | — | — | — | — |
| Payback | **H1** (inclui estendido) | **H2** (nulo acima de 10 anos; D8) | **H2** (estático; rótulo de payback simplificado) | — | — | — |
| Ponto de equilíbrio | **H1** | **H2** (observação O3: reserva dentro da dedução) | **H1** | — | — | não testado |
| CAPEX e contingência | **H1** (F01) | — | — | **H2** (perfil oficial e regra; base D6; fórmula descrita a partir do próprio código) | **H1** (exemplo + suíte própria independente) | — |
| Valor de saída | **H1** (método 1: múltiplo × EBITDA); métodos 2 e 3 e valor líquido N/I (D7-C) | **H2** (residual em % do investimento; D7-C) | — | — | — | — |
| Régua Única: lógica dos 5 critérios e da leitura | **H1** (critérios, bordas, leitura) | N/I (D11-A) | N/I (D11-A) | — | — | — |
| Régua Única: limites (8 e 12 anos, colchão de 10%, 3 meses) | **H4** | — | — | — | — | — |
| Parâmetros de referência (17%, 1%, 4% e faixa, R$ 40/h, rampa, OS&E, pré-abertura, contingência, cenários, 6×) | **H4** | **H4** | **H4** | **H4** | **H4** | **H4** |

**Alcance da homologação da ZAIOS:** vale só para as **primitivas** de `src/calc` (`tipos`, `capex`, `receitas`, `viabilidade`) no commit `ec21ad5`.
- **Não cobre a camada que as compõe na aplicação** (`src/exercicios/*-calculo.ts`): por exemplo, como a viabilidade monta o 1º ano, o capital de giro, a captação e o colchão.
- **Não cobre G2/G3** (`operacao.ts`).

Essa camada é o que o membro realmente usa. Recomendo cobri-la antes de qualquer homologação definitiva.

## 5. Auditoria dos cálculos (os 14 temas)

| Tema | Achado |
|---|---|
| Receita bruta e realizada | ZAIOS: noites × diária + outras, por mês de calendário real (365 dias), em centavos. B08: noites/ano informadas (até 366). A09: noites/mês inteiras × meses (D5). Folha J2: valores do mês informados. Bases corretas |
| Ocupação e noites disponíveis | Unidades × dias; ocupação como fração. Correto em todas |
| Deduções e custos variáveis | Deduções sobre a receita bruta em todas. **O2:** o A09 soma "gestão" às deduções; na ZAIOS gestão é custo do modelo (abaixo do resultado operacional). O total do resultado do A09 equivale a um "EBITDA", não ao resultado operacional da ZAIOS. Diferença de categoria, não de conta |
| Quebra e perdas | ZAIOS e Folha J2: % das diárias como custo variável, fora das deduções (conferido de forma independente: 2.829,48). B08 e A09 não têm (D3-A) |
| Reserva de reposição | ZAIOS: % da receita bruta, abaixo do EBITDA, **3%, faixa 3–5%** (aprovado: 4%, 3–6%). Folha J2: 4% da **receita real** (aprovado: receita bruta realizada). B08: dentro das deduções. A09: não tem. Nenhuma conta duplica a reserva; o B08 a coloca no lugar errado |
| Pró-labore e distribuição | Pró-labore = horas × valor × 4,33, como custo fixo, igual na ZAIOS e na Folha (conferido: 3.464,00). Distribuição e caixa disponível não existem com esse nome em nenhuma ferramenta (D4) |
| Resultado operacional e fluxo | Cascata fecha em todas (testes T5 e T9, conferidos de forma independente). Fluxo: ano 0 = −investimento, anos 1–10 positivos ou negativos, sinais corretos |
| EBITDA | ZAIOS: resultado operacional − custos do modelo. Nos cenários testados os custos do modelo são zero, então EBITDA = resultado operacional. A subtração dos custos do modelo não foi exercitada (ressalva) |
| ROI anual e retorno acumulado | Valores corretos (14,40% ao ano; 43,95% em 10 anos). O nome "ROI" sem qualificador ainda aparece no B08 e no A09 (D1) |
| VPL e TIR | VPL com fluxos no fim do ano, ano 0 sem desconto. TIR por bisseção a partir da primeira troca de sinal, com aviso de várias TIR. Coincidência até o centavo com a implementação independente (secante) |
| Payback | Interpolação linear dentro do ano. **Ressalva de convenção:** o payback supõe entrada uniforme no ano, enquanto o VPL usa fim de ano. É prática comum, mas deve constar do dicionário. ZAIOS estende além de 10 anos; B08 devolve nulo (D8); A09 é estático |
| Contingência | ZAIOS: sobre infraestrutura + obra + apoio, arredondada ao centavo. B06: sobre todo o CAPEX, sem o giro. F05: sobre todos os itens. A09: sobre investimento + infraestrutura (D6 pendente) |
| Valor de saída | ZAIOS: múltiplo × EBITDA do regime, somado ao ano 10; VPL mostrado com e sem saída. B08: residual em % do investimento, até 100% (D7-C) |
| Régua Única Zion | Lógica dos 5 passos e da leitura correta, inclusive nas bordas (8,00; 12,00; 10%; 3 × fixo). **A ZAIOS mostra o veredito sem trava de homologação** (D11-A). Limites são H4 |
| Unidades e arredondamento | ZAIOS em centavos inteiros, frações para percentuais, arredondamento só na contingência, OS&E e pré-abertura e na tela. Ferramentas simples em float, com tolerância de R$ 0,01 |
| Dupla contagem | Nenhuma encontrada. Cada valor sai uma vez na cascata (T9 fecha: 115.411,44). **O3:** no B08, como a reserva está nas deduções, o ponto de equilíbrio passa a tratar a reserva como custo por noite e fica mais alto |

## 6. Divergências confirmadas

**Metodologia aprovada, ainda não implementada (25 casos):**
- D1 (3 casos).
- D2-C (5 casos), entre eles a **divergência da faixa da reserva na ZAIOS: atual 3% a 5%, aprovada 3% a 6%**.
- D3-A (5 casos).
- D4 (4 casos). No Comando 05D esta decisão foi citada como "D4-C"; é a mesma decisão registrada como D4 em 09/11.
- D7-C (4 casos).
- D11-A (4 casos).

**Decisões ainda pendentes (3 casos):** D5 (A09: 360 dias), D6 (B06: base da contingência), D8 (B08: payback acima de 10 anos).

**Pendentes sem caso de teste próprio:**
- D9: custo variável por noite ou por estadia.
- D10: cenários de referência.
- D12: meses de fôlego x cobertura da reserva.
- D13: moeda.
- D14: taxa de limpeza.

Lista completa por ID em `MATRIZ_EVIDENCIAS_TESTES.md` e em `testes/financeiro/README.md`. **Nenhuma foi corrigida.**

## 7. Evidências e limitações

**Evidências:**
- Execução de referência: `testes/financeiro/resultados/2026-11-09-com-zaios/`.
- Verificação independente: `testes/financeiro/independente/RESULTADO_INDEPENDENTE.md`.
- Hashes e commits: `CONTROLE_VERSOES_FINANCEIRAS.md`.

**Limitações:**
1. **Cópia da ZAIOS transcrita a partir de leitura.** A equivalência é evidenciada porque ela reproduz os testes da própria ZAIOS, mas a identidade **byte a byte** ainda não foi confirmada por hash de uma exportação direta.
2. **Camada de composição da ZAIOS** (exercícios) e G2/G3 não executadas.
3. **Telas não testadas.** Rótulos e campos de B08 e A09 foram verificados por presença no código-fonte.
4. **Cobertura parcial:**
   - B08: rampa, reajuste, extras e residual;
   - A09: contingência, extras, gestão e cenários;
   - B06: só um perfil;
   - Folha J2: só o exemplo.
5. **Independência metodológica limitada** (seção 3).
6. **B06:** a fórmula usada na verificação foi descrita a partir da leitura do próprio código.

## 8. Riscos

| Risco | Efeito | Mitigação |
|---|---|---|
| Homologar a ZAIOS sem cobrir a camada de exercícios | Primitivas certas compostas de forma errada passariam despercebidas | Testes da camada de composição antes da homologação definitiva |
| Ler "H1" como "metodologia aprovada" ou como "viável" | Decisão de negócio em cima de parâmetro não validado | Sempre citar os quatro níveis; H4 visível nas telas e nos materiais |
| Veredito da ZAIOS exibido antes da homologação (D11-A) | O membro lê "Avançar" como aprovação | Prioridade 1 da implementação, quando autorizada |
| Divergência entre a cópia e o projeto Lovable | Homologação de uma versão diferente da que está em uso | Conferência por hash e regra de revalidação |
| Faixa da reserva da ZAIOS (3–5%) diferente da aprovada (3–6%) | Valor aceito na metodologia pode ser marcado como fora da faixa | Correção na implementação D2-C |

## 9. Conclusão técnica

Com base na integridade da suíte, na conferência independente de 79 valores numéricos e 17 lógicos, e na auditoria do código, **não há inconsistência matemática** nas ferramentas examinadas.

**Proponho, para revisão do Bruno, a homologação matemática condicionada:**
- **H1**, nas versões registradas em `CONTROLE_VERSOES_FINANCEIRAS.md`:
  - **ZAIOS** (primitivas de `src/calc`, commit `ec21ad5`): receita, deduções, quebra percentual, reserva (mecânica), pró-labore, resultado operacional, retorno anual, VPL, TIR, payback, equilíbrio, CAPEX e contingência (F01), valor de saída por múltiplo e lógica da Régua Única;
  - **B08**: receita, deduções, resultado operacional, retorno anual e acumulado (valores);
  - **A09**: deduções, resultado operacional, retorno anual, equilíbrio;
  - **F05**: orçamento.
- **H2**, com as ressalvas da seção 4:
  - **ZAIOS**: EBITDA com custos do modelo;
  - **B08**: VPL, TIR e payback fora do cenário testado, reserva e equilíbrio;
  - **A09**: receita (360 dias) e payback;
  - **B06**: inteiro;
  - **Folha J2**: inteira.
- **H3:** nenhum grupo.
- **H4:** todos os parâmetros de referência e os limites da Régua Única.

Esta homologação **não** é metodológica, econômica nem financeira global. Vale só para as versões examinadas.

## 10. Recomendação para a próxima etapa

1. **Bruno revisa este parecer** e aprova (ou ajusta) a classificação H1 a H4.
2. **Fechar as ressalvas, só com testes** (sem mudar ferramentas):
   - camada de exercícios da ZAIOS;
   - custos do modelo;
   - G2/G3;
   - B08 com rampa, reajuste e residual;
   - A09 com contingência e gestão;
   - mais perfis do B06;
   - indicadores da Folha J2.
3. **Confirmar a cópia da ZAIOS por hash** com uma exportação direta, e decidir onde guardá-la (fora do repositório público).
4. **Conferência externa** por contador ou analista financeiro, recomendada.
5. Só depois, **iniciar a implementação autorizada**, na ordem já proposta. A primeira etapa é ocultar o veredito da ZAIOS até a homologação (D11-A).
