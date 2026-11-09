# Matriz de evidências dos testes financeiros

Comando 05D · 09/11/2026 · Base: execução de referência da suíte `testes/financeiro/` com o motor da ZAIOS (`resultados/2026-11-09-com-zaios/`) e a verificação independente `testes/financeiro/independente/` (`RESULTADO_INDEPENDENTE.md`).

## Conferência dos 139 casos

| Verificação | Resultado |
|---|---|
| Casos na execução | 139, todos com ID único |
| Categorias mutuamente exclusivas | Sim: cada caso tem um único status, e o tipo sempre corresponde ao status (fórmula → OK; divergência → divergência confirmada; limitação → limitação confirmada; econômico → pendente) |
| Distribuição | 96 fórmula OK · 25 divergências confirmadas · 3 limitações de decisões pendentes · 15 parâmetros econômicos · 0 falhas · 0 erros |
| Casos de fórmula com conferência independente numérica | **79 de 79** numéricos conferem com o cálculo independente, tanto o valor esperado do plano quanto o valor obtido da ferramenta |
| Casos de fórmula conferidos por definição | 17 (nulos, alertas, bordas e leitura da régua) |

## Origem dos valores esperados e independência

| Evidência | Casos | Independência |
|---|---|---|
| Independente (Python, dicionário v0.4) | 51 | **Alta:** implementação própria, outra linguagem, sem ler o código testado. TIR por secante (as ferramentas usam bisseção) |
| Independente + caso de referência do Método (F01–F03) | 12 | **Alta:** valores das unidades F01–F03, recalculados |
| Independente: campos do exemplo + definição (Folha J2) | 9 | **Alta para a aritmética;** só o exemplo foi usado |
| Independente: itens de dados.py + definição (F05) | 3 | **Alta:** soma recalculada a partir dos itens; a F05 também tem suíte própria com regra independente (29 arquivos) |
| Independente: perfil + fórmula descrita na auditoria (B06) | 4 | **Parcial:** a fórmula do B06 foi descrita a partir da leitura do próprio código (Comando 05B) |
| Por definição (nulo, alerta, borda, leitura da régua) | 17 | **Alta:** decorre da definição no dicionário e na D11-A |
| Valor obtido da ferramenta x regra aprovada | 10 | Divergência metodológica; o esperado vem da decisão aprovada |
| Presença de campo ou texto no código | 18 | **Baixa:** indicador de que a funcionalidade não existe; não é prova de tela |
| Valor em uso lido do código (T12) | 15 | Não há evidência econômica; só registra o valor atual |

**Ponto de atenção sobre independência:** os valores esperados do plano e a implementação independente foram feitos pela mesma equipe técnica (esta sessão), a partir do dicionário. São independentes do **código** das ferramentas, mas não da **metodologia**. Uma revisão por outra pessoa (contador ou analista financeiro) fortaleceria a homologação.

## Classes usadas na coluna "Classe"

- **H1:** matematicamente homologável na versão examinada.
- **H2:** homologável com ressalvas (matemática consistente, cobertura ou evidência incompleta).
- **H3:** não homologável.
- **H4:** fora do escopo matemático (premissa econômica).
- **Metodologia:** divergência em relação à metodologia aprovada, que não é erro matemático.

A classe do caso é a do grupo de cálculo que ele sustenta (ver o parecer, seção 4).

## Os 139 casos

| ID | Teste | Ferramenta | Indicador | Decisão | Tipo | Esperado | Obtido | Status | Evidência | Classe |
|---|---|---|---|---|---|---|---|---|---|---|
| T1-ZAIOS-01 | T1 | ZAIOS | Receita bruta/ano | v0 | formula | 282948 | 282948 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-02 | T1 | ZAIOS | Receita real | v0 | formula | 234,846.84 | 234,846.84 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-03 | T1 | ZAIOS | Resultado operacional | v0 | formula | 129,558.84 | 129,558.84 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-04 | T1 | ZAIOS | Ocupação de equilíbrio | v0 | formula | 0.1357 | 0.135742 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-05 | T1 | ZAIOS | VPL a 10% | v0 | formula | -103,917.01 | -103,917.01 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-06 | T1 | ZAIOS | TIR | v0 | formula | 0.0724 | 0.0723896 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-07 | T1 | ZAIOS | Payback simples | v0 | formula | 6.95 | 6.95 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-08 | T1 | ZAIOS | Payback descontado (não ocorre em 10 anos) | v0 | formula | — | — | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T1-ZAIOS-09 | T1 | ZAIOS | Retorno anual sobre o investimento | D1 | formula | 0.144 | 0.143954 | OK | Independente (Python, dicionário v0.4) | H1 |
| T1-ZAIOS-10 | T1 | ZAIOS | Retorno acumulado em 10 anos | D1 | divergencia | 0.4395 | — | DIVERGÊNCIA CONFIRMADA | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T1-B08-01 | T1 | B08 | Receita bruta/ano | v0 | formula | 282948 | 282948 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-02 | T1 | B08 | Receita real | v0 | formula | 234,846.84 | 234,846.84 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-03 | T1 | B08 | Resultado operacional | v0 | formula | 129,558.84 | 129,558.84 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-04 | T1 | B08 | Ocupação de equilíbrio | v0 | formula | 0.1357 | 0.135742 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-05 | T1 | B08 | VPL a 10% | v0 | formula | -103,917.01 | -103,917.01 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-06 | T1 | B08 | TIR | v0 | formula | 0.0724 | 0.0723896 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-07 | T1 | B08 | Payback simples | v0 | formula | 6.95 | 6.95 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-08 | T1 | B08 | Payback descontado (não ocorre em 10 anos) | v0 | formula | — | — | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H2 |
| T1-B08-09 | T1 | B08 | Retorno anual (valor) | D1 | formula | 0.144 | 0.143954 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-B08-10 | T1 | B08 | Retorno acumulado em 10 anos (valor) | D1 | formula | 0.4395 | 0.439543 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-A09-01 | T1 | A09 | Receita bruta/ano (365 dias) | v0 | formula | 282948 | 282948 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-A09-02 | T1 | A09 | Receita real | v0 | formula | 234,846.84 | 234,846.84 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-A09-03 | T1 | A09 | Resultado operacional | v0 | formula | 129,558.84 | 129,558.84 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-A09-04 | T1 | A09 | Ocupação de equilíbrio | v0 | formula | 0.1357 | 0.135742 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-A09-05 | T1 | A09 | Payback (simplificado, sem rampa) | v0 | formula | 6.95 | 6.95 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-A09-06 | T1 | A09 | Retorno anual (valor) | D1 | formula | 0.144 | 0.143954 | OK | Independente (Python, dicionário v0.4) | H2 |
| T1-A09-07 | T1 | A09 | Receita bruta/ano com o campo como a interface permite (30 noites × 12) | D5 (pendente) | limitacao | 282948 | 279072 | LIMITAÇÃO CONFIRMADA (decisão pendente) | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T2-ZAIOS-S1 | T2 | ZAIOS | Resultado operacional (regime) (sem rampa) | v0 | formula | 126,729.36 | 126,729.36 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-S2 | T2 | ZAIOS | Geração de caixa (regime) (sem rampa) | v0 | formula | 118,240.92 | 118,240.92 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-S3 | T2 | ZAIOS | Geração do 1º ano (sem rampa) | v0 | formula | 118,240.92 | 118,240.92 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-S4 | T2 | ZAIOS | VPL a 10% (sem rampa) | v0 | formula | -173,460.73 | -173,460.73 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-S5 | T2 | ZAIOS | TIR (sem rampa) | v0 | formula | 0.053 | 0.0529696 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-S6 | T2 | ZAIOS | Payback simples (sem rampa) | v0 | formula | 7.61 | 7.61 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-S7 | T2 | ZAIOS | VPL com saída 6× EBITDA (sem rampa) | v0 | formula | 119,697.19 | 119,697.19 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-R1 | T2 | ZAIOS | Resultado operacional (regime) (com rampa) | v0 | formula | 126,729.36 | 126,729.36 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-R2 | T2 | ZAIOS | Geração de caixa (regime) (com rampa) | v0 | formula | 118,240.92 | 118,240.92 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-R3 | T2 | ZAIOS | Geração do 1º ano (com rampa) | v0 | formula | 42,405.16 | 42,405.16 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-R4 | T2 | ZAIOS | VPL a 10% (com rampa) | v0 | formula | -242,402.34 | -242,402.34 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-R5 | T2 | ZAIOS | TIR (com rampa) | v0 | formula | 0.0371 | 0.037082 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-R6 | T2 | ZAIOS | Payback simples (com rampa) | v0 | formula | 8.25 | 8.25 | OK | Independente (Python, dicionário v0.4) | H1 |
| T2-ZAIOS-R7 | T2 | ZAIOS | VPL com saída 6× EBITDA (com rampa) | v0 | formula | 50,755.59 | 50,755.59 | OK | Independente (Python, dicionário v0.4) | H1 |
| T3-F01-01 | T3 | ZAIOS | F01 · CAPEX com contingência de 25% da base | v0 | formula | 1237400 | 1237400 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F02-01 | T3 | ZAIOS | F02 · Receita real | v0 | formula | 234,846.84 | 234,846.84 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F02-02 | T3 | ZAIOS | F02 · Resultado operacional | v0 | formula | 108,846.84 | 108,846.84 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F02-03 | T3 | ZAIOS | F02 · Equilíbrio em noites | v0 | formula | 223.25 | 223.25 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F02-04 | T3 | ZAIOS | F02 · Ocupação de equilíbrio (20,4%) | v0 | formula | 0.204 | 0.203878 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F03-C1-1 | T3 | ZAIOS | F03 caso 1 · VPL a 10% | v0 | formula | -1,110,447.78 | -1,110,447.78 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F03-C1-2 | T3 | ZAIOS | F03 caso 1 · Payback simples estendido (38,6 anos) | v0 | formula | 38.60 | 38.57 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F03-C1-3 | T3 | ZAIOS | F03 caso 1 · TIR com saída 6× (−8,4%) | v0 | formula | -0.084 | -0.0844161 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F03-C2-1 | T3 | ZAIOS | F03 caso 2 · Payback simples | v0 | formula | 5.75 | 5.75 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F03-C2-2 | T3 | ZAIOS | F03 caso 2 · Payback descontado | v0 | formula | 8.82 | 8.82 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F03-C2-3 | T3 | ZAIOS | F03 caso 2 · VPL sem saída | v0 | formula | 92,549.78 | 92,549.78 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T3-F03-C2-4 | T3 | ZAIOS | F03 caso 2 · VPL com saída 6× | v0 | formula | 624,599.52 | 624,599.52 | OK | Independente (Python) + caso de referência do Método (F01–F03) | H1 |
| T4-B06-01 | T4 | B06 | CAPEX (perfil oficial iniciante) | v0 | formula | 449500 | 449500 | OK | Independente: dados do perfil + fórmula descrita na auditoria (independência parcial) | H2 |
| T4-B06-02 | T4 | B06 | Cenário intermediário (perfil iniciante) | v0 | formula | 524450 | 524450 | OK | Independente: dados do perfil + fórmula descrita na auditoria (independência parcial) | H2 |
| T4-B06-03 | T4 | B06 | Cenário conservador (perfil iniciante) | v0 | formula | 598,617.50 | 598,617.50 | OK | Independente: dados do perfil + fórmula descrita na auditoria (independência parcial) | H2 |
| T4-B06-04 | T4 | B06 | Contingência fora do capital de giro (intermediário − giro = CAPEX × (1 + contingência)) | v0 | formula | 0 | -5.82077e-11 | OK | Independente: dados do perfil + fórmula descrita na auditoria (independência parcial) | H2 |
| T4-B06-05 | T4 | B06 | Contingência sobre as linhas do F01 (base ZAIOS: infra + obra + apoio = 182.500) | D6 (pendente) | limitacao | 182500 | 263725 | LIMITAÇÃO CONFIRMADA (decisão pendente) | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T4-F05-01 | T4 | F05 | Subtotal do exemplo | v0 | formula | 197040 | 197040 | OK | Independente: itens de dados.py + definição (subtotal, reserva, total) | H1 |
| T4-F05-02 | T4 | F05 | Reserva para imprevistos (contingência) do exemplo | v0 | formula | 19704 | 19704 | OK | Independente: itens de dados.py + definição (subtotal, reserva, total) | H1 |
| T4-F05-03 | T4 | F05 | Total com reserva do exemplo | v0 | formula | 216744 | 216744 | OK | Independente: itens de dados.py + definição (subtotal, reserva, total) | H1 |
| T5-J2-01 | T5 | Folha J2 | Receita real − custos variáveis = margem de contribuição | v0 | formula | 0 | 0 | OK | Independente: campos do exemplo + definição | H2 |
| T5-J2-02 | T5 | Folha J2 | Margem de contribuição − fixos = resultado operacional | v0 | formula | 0 | 0 | OK | Independente: campos do exemplo + definição | H2 |
| T5-J2-03 | T5 | Folha J2 | Resultado operacional − custos do modelo = EBITDA | v0 | formula | 0 | 0 | OK | Independente: campos do exemplo + definição | H2 |
| T5-J2-04 | T5 | Folha J2 | EBITDA − reserva de reposição = geração de caixa | v0 | formula | 0 | 0 | OK | Independente: campos do exemplo + definição | H2 |
| T5-J2-05 | T5 | Folha J2 × ZAIOS | Pró-labore 20 h × R$ 40 × 4,33 igual nas duas | D4 | formula | 0 | 0 | OK | Independente: campos do exemplo + definição | H2 |
| T6-ZAIOS-01 | T6 | ZAIOS | TIR inexistente quando o fluxo não muda de sinal | v0 | formula | — | — | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T6-ZAIOS-02 | T6 | ZAIOS | Aviso de mais de uma TIR com duas trocas de sinal | v0 | formula | True | True | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T6-ZAIOS-03 | T6 | ZAIOS | Payback acima do horizonte marcado como estendido | v0 | formula | True | True | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T6-ZAIOS-04 | T6 | ZAIOS | Sem equilíbrio quando a diária é menor que o custo variável | v0 | formula | — | — | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T6-ZAIOS-05 | T6 | ZAIOS | Sem equilíbrio com ocupação 0% | v0 | formula | — | — | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T6-ZAIOS-06 | T6 | ZAIOS | Geração do regime negativa: não se paga | v0 | formula | — | — | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T6-B08-01 | T6 | B08 | Payback acima de 10 anos com valor estendido (padrão proposto) | D8 (pendente) | limitacao | número acima de 10 | — | LIMITAÇÃO CONFIRMADA (decisão pendente) | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T7-ZAIOS-01 | T7 | ZAIOS | Conservador · receita bruta (diária 612, ocupação 30,4%) | D11-A | formula | 203,722.56 | 203,722.56 | OK | Independente (Python, dicionário v0.4) | H1 |
| T7-ZAIOS-02 | T7 | ZAIOS | Conservador · geração de caixa | D11-A | formula | 70,459.32 | 70,459.32 | OK | Independente (Python, dicionário v0.4) | H1 |
| T7-ZAIOS-03 | T7 | ZAIOS | Valor de saída no ano 10 (6× EBITDA) | D11-A | formula | 777,353.04 | 777,353.04 | OK | Independente (Python, dicionário v0.4) | H1 |
| T7-ZAIOS-04 | T7 | ZAIOS | Valor presente da saída | D11-A | formula | 299,703.25 | 299,703.25 | OK | Independente (Python, dicionário v0.4) | H1 |
| T7-ZAIOS-05 | T7 | ZAIOS | VPL com saída | D11-A | formula | 195,786.24 | 195,786.23 | OK | Independente (Python, dicionário v0.4) | H1 |
| T7-ZAIOS-06 | T7 | ZAIOS | Resultado dos 5 critérios (o 5º não avaliável no T1) | D11-A | formula | ['passa', 'passa', 'passa', 'ajustar', 'nao_avaliado'] | ['passa', 'passa', 'passa', 'ajustar', 'nao_avaliado'] | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-07 | T7 | ZAIOS | Borda · payback de 8,00 anos passa | D11-A | formula | passa | passa | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-08 | T7 | ZAIOS | Borda · payback de 12,00 anos pede ajuste | D11-A | formula | ajustar | ajustar | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-09 | T7 | ZAIOS | Borda · payback acima de 12 pede redesenho | D11-A | formula | redesenhar | redesenhar | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-10 | T7 | ZAIOS | Borda · colchão de 10% passa | D11-A | formula | passa | passa | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-11 | T7 | ZAIOS | Borda · déficit igual a 3 × fixo pede ajuste | D11-A | formula | ajustar | ajustar | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-12 | T7 | ZAIOS | Borda · déficit acima de 3 × fixo pede redesenho | D11-A | formula | redesenhar | redesenhar | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-13 | T7 | ZAIOS | Leitura: um 'redesenhar' dá Redesenhar; só 'ajustar' dá Ajustar; tudo 'passa' dá Avançar | D11-A | formula | ['Redesenhar', 'Ajustar', 'Avançar'] | ['Redesenhar', 'Ajustar', 'Avançar'] | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H1 |
| T7-ZAIOS-14 | T7 | ZAIOS | Apresentação com 4 de 5 critérios: sinal parcial, sem veredito | D11-A | divergencia | 4 de 5 critérios avaliados. Sinal parcial, não representa aprovação do projeto. | Ajustar | DIVERGÊNCIA CONFIRMADA | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T7-B08-01 | T7 | B08 | Mostra 'X de 5 critérios avaliados. Sinal parcial…' | D11-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T7-A09-01 | T7 | A09 | Mostra 'X de 5 critérios avaliados. Sinal parcial…' | D11-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T7-A09-02 | T7 | A09 | Metas pessoais (prazo e retorno desejados) em bloco separado da Régua Zion | D11-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-B08-01 | T8 | B08 | Quebra e perdas: campo próprio ou rótulo 'Resultado antes de quebra e perdas' | D3-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-B08-02 | T8 | B08 | Pró-labore: campo próprio ou rótulo 'Resultado antes do seu pró-labore' | D4 | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-B08-03 | T8 | B08 | Sem 'ROI' sem qualificador (usa 'retorno anual' / 'retorno acumulado em 10 anos') | D1 | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-A09-01 | T8 | A09 | Quebra e perdas: campo próprio ou rótulo 'Resultado antes de quebra e perdas' | D3-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-A09-02 | T8 | A09 | Pró-labore: campo próprio ou rótulo 'Resultado antes do seu pró-labore' | D4 | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-A09-03 | T8 | A09 | Sem 'ROI' sem qualificador (usa 'retorno anual' / 'retorno acumulado em 10 anos') | D1 | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-A09-04 | T8 | A09 | Reserva de reposição: campo próprio ou rótulo 'Antes da reserva de reposição' | D2-C | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T8-B08-04 | T8 | B08 | Valor de saída com método identificado (múltiplo do EBITDA, avaliação patrimonial ou valor informado) | D7-C | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T9-ZAIOS-01 | T9 | ZAIOS | Deduções (17%) sem quebra nem reserva | v0 | formula | 48,101.16 | 48,101.16 | OK | Independente (Python, dicionário v0.4) | H1 |
| T9-ZAIOS-02 | T9 | ZAIOS | Quebra de 1% como custo variável | D3-A | formula | 2,829.48 | 2,829.48 | OK | Independente (Python, dicionário v0.4) | H1 |
| T9-ZAIOS-03 | T9 | ZAIOS | Resultado operacional com quebra | D3-A | formula | 126,729.36 | 126,729.36 | OK | Independente (Python, dicionário v0.4) | H1 |
| T9-ZAIOS-04 | T9 | ZAIOS | Reserva de 4% da receita bruta (informada) abaixo do EBITDA | D2-C | formula | 11,317.92 | 11,317.92 | OK | Independente (Python, dicionário v0.4) | H1 |
| T9-ZAIOS-05 | T9 | ZAIOS | Geração de caixa (a cascata fecha, reserva sai uma vez) | D2-C | formula | 115,411.44 | 115,411.44 | OK | Independente (Python, dicionário v0.4) | H1 |
| T9-ZAIOS-06 | T9 | ZAIOS | Referência da reserva de reposição = 4% | D2-C | divergencia | 0.04 | 0.03 | DIVERGÊNCIA CONFIRMADA | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T9-ZAIOS-07 | T9 | ZAIOS | Faixa da reserva de reposição = 3% a 6% | D2-C | divergencia | [0.03, 0.06] | [0.03, 0.05] | DIVERGÊNCIA CONFIRMADA | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T9-ZAIOS-08 | T9 | ZAIOS | Aceita quebra medida em R$ (prioridade ao valor real) | D3-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T9-J2-01 | T9 | Folha J2 | Referência da reserva = 4%, faixa 3% a 6% | D2-C | formula | [4, 3, 6] | [4, 3, 6] | OK | Por definição (nulo, alerta, borda ou leitura da régua) | H2 |
| T9-J2-02 | T9 | Folha J2 | Reserva = 4% da receita bruta realizada (exemplo: 4% × 17.220,00 = 688,80) | D2-C | divergencia | 688.80 | 542.62 | DIVERGÊNCIA CONFIRMADA | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T9-J2-03 | T9 | Folha J2 | Quebra sem medição = 1% da receita de hospedagem (162,40) | D3-A | formula | 162.40 | 162.40 | OK | Independente: campos do exemplo + definição | H2 |
| T9-J2-04 | T9 | Folha J2 | Quebra medida em R$ tem prioridade (informada 150,00) | D3-A | formula | 150 | 150 | OK | Independente: campos do exemplo + definição | H2 |
| T9-J2-05 | T9 | Folha J2 | Deduções não contêm quebra (650 + 18,5% × 16.240 = 3.654,40) | D3-A | formula | 3,654.40 | 3,654.40 | OK | Independente: campos do exemplo + definição | H2 |
| T9-B08-01 | T9 | B08 | Reserva de 4% fora das deduções (deduções continuam 48.101,16) | D2-C | divergencia | 48,101.16 | 59,419.08 | DIVERGÊNCIA CONFIRMADA | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T9-B08-02 | T9 | B08 | Quebra como custo variável disponível | D3-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T9-A09-01 | T9 | A09 | Quebra como custo variável disponível | D3-A | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T10-ZAIOS-01 | T10 | ZAIOS | Pró-labore 20 h × R$ 40 × 4,33 por mês | D4 | formula | 3464 | 3464 | OK | Independente (Python, dicionário v0.4) | H1 |
| T10-ZAIOS-02 | T10 | ZAIOS | Pró-labore por ano | D4 | formula | 41568 | 41568 | OK | Independente (Python, dicionário v0.4) | H1 |
| T10-ZAIOS-03 | T10 | ZAIOS | Resultado operacional do T1 com pró-labore como custo fixo | D4 | formula | 87,990.84 | 87,990.84 | OK | Independente (Python, dicionário v0.4) | H1 |
| T10-ZAIOS-04 | T10 | ZAIOS | Distribuição de resultados e caixa disponível separados do resultado | D4 | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T10-J2-01 | T10 | Folha J2 | Pró-labore do exemplo (20 h × R$ 40 × 4,33) | D4 | formula | 3464 | 3464 | OK | Independente: campos do exemplo + definição | H2 |
| T10-J2-02 | T10 | Folha J2 | Distribuição de resultados com nome próprio, fora do resultado | D4 | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T11-ZAIOS-01 | T11 | ZAIOS | Método 1 · 6× EBITDA de 129.558,84 | D7-C | formula | 777,353.04 | 777,353.04 | OK | Independente (Python, dicionário v0.4) | H1 |
| T11-ZAIOS-02 | T11 | ZAIOS | Métodos 2 e 3 (avaliação patrimonial, valor informado) e valor líquido de custos, tributos e obrigações | D7-C | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T11-ZAIOS-03 | T11 | ZAIOS | Valor líquido com custo de venda ilustrativo de 6% (antes de tributos) | D7-C | divergencia | 730,711.86 | — | DIVERGÊNCIA CONFIRMADA | Valor obtido da ferramenta x regra aprovada (dicionário v0.4) | Metodologia (não matemático) |
| T11-B08-01 | T11 | B08 | Saída aceita múltiplo do EBITDA (residual hoje em % do investimento, até 100%) | D7-C | divergencia | True | False | DIVERGÊNCIA CONFIRMADA | Presença de campo/texto no código (indicador, não prova de tela) | Metodologia (não matemático) |
| T12-01 | T12 | todas | Deduções sobre a receita | v0 | economico | 0.17 | ZAIOS: 0.17; Folha J2: 0.17 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-02 | T12 | todas | Quebra e perdas | D3-A | economico | 0.01 | ZAIOS: 0.01; Folha J2: 0.01 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-03 | T12 | todas | Reserva de reposição | D2-C | economico | 0.04 | ZAIOS: 0.03; Folha J2: 0.04 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-04 | T12 | todas | Valor da hora do pró-labore (R$) | D4 | economico | 40 | Folha J2 (exemplo): 40 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-05 | T12 | todas | Rampa do 1º ano (meses 1–3, 4–6, 7–12) | v0 | economico | [0.4, 0.5, 0.75] | ZAIOS: [0.4, 0.5, 0.75] | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-06 | T12 | todas | OS&E sobre FF&E | v0 | economico | 0.12 | ZAIOS: 0.12 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-07 | T12 | todas | Pré-abertura sobre a base | v0 | economico | 0.05 | ZAIOS: 0.05 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-08 | T12 | todas | Contingência primeira obra | v0 | economico | [0.2, 0.25] | ZAIOS: [0.2, 0.25] | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-09 | T12 | todas | Contingência com experiência | v0 | economico | [0.1, 0.15] | ZAIOS: [0.1, 0.15] | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-10 | T12 | todas | Cenário conservador (diária, ocupação) | D10 pendente | economico | [-0.1, -0.2] | ZAIOS: [-0.1, -0.2] | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-11 | T12 | todas | Cenário otimista (diária, ocupação) | D10 pendente | economico | [0.1, 0.15] | ZAIOS: [0.1, 0.15] | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-12 | T12 | todas | Múltiplo de saída (método 1) | D7-C | economico | 6 | ZAIOS: 6 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-13 | T12 | todas | Régua: payback passa / ajustar (anos) | D11-A | economico | [8, 12] | ZAIOS: [8, 12] | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-14 | T12 | todas | Régua: colchão mínimo sobre o CAPEX | D11-A | economico | 0.1 | ZAIOS: 0.1 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
| T12-15 | T12 | todas | Régua: déficit conservador aceito (meses de fixo) | D11-A | economico | 3 | ZAIOS: 3 | PENDENTE DE VALIDAÇÃO ECONÔMICA | Valor em uso lido do código; sem evidência econômica | H4 |
