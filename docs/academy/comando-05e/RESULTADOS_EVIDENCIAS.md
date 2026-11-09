# Resultados e evidências dos testes complementares

Comando 05E · 09/11/2026 · Execução local, sem créditos Lovable e sem alterar produção.

## 1. Execuções

| Execução | Pasta | Casos | Resultado |
|---|---|---|---|
| Com a cópia da ZAIOS (`ZAIOS_CALC_DIR` e `ZAIOS_SRC_DIR`) | `testes/financeiro/resultados/2026-11-09-05e-com-zaios/` | 237 (139 do 05C/05D + 98 complementares) | 189 OK · 27 divergências confirmadas · 6 limitações · 15 pendentes de validação econômica · **0 falhas** |
| Sem a cópia da ZAIOS (reprodutível por qualquer pessoa com o repositório) | `testes/financeiro/resultados/2026-11-09-05e-sem-zaios/` | 237 | 84 OK · 18 divergências · 5 limitações · 15 pendentes · 115 não executados (dependem da ZAIOS) · **0 falhas** |

Os 139 casos anteriores (T1 a T12) deram exatamente o mesmo resultado do 05D. Nenhuma regressão.

**Comandos:**
```
python3 testes/financeiro/independente/complementares_referencia.py      # esperados independentes
ZAIOS_CALC_DIR=<cópia de src/calc> ZAIOS_SRC_DIR=<cópia da raiz com src/> node testes/financeiro/run.js --saida <pasta>
```

**Ambiente:** Node 22, que remove os tipos do TypeScript sem alterar o código; Python 3; LibreOffice headless para a F05.

## 2. Evidências por tipo

- **Fórmula (93 OK):** em todos os casos o valor obtido ficou dentro da tolerância. Nenhum caso precisou de tolerância maior que a registrada.
- **Divergências confirmadas (2):**
  - `C-ZAIOS-C-veredito`: a ZAIOS devolve o selo "Redesenhar" sem trava de homologação. É o risco já registrado (D11-A).
  - `C-B08-E-2`: o equilíbrio do B08 com reserva de 4% fica em 14,38%, contra 13,57% pela regra aprovada (O3, consequência da D2-C).
- **Limitações confirmadas (3):**
  - `C-A09-G-1`: gestão como dedução (O2).
  - `C-A09-D-1`: 31 noites × 12 = 372 dias (D5).
  - `C-G2-impostos`: impostos como despesa variável na G2 (nova observação O7).

**Falhas matemáticas x divergências metodológicas:** nenhum caso complementar falhou na matemática. Os 5 casos diferentes de OK reproduzem o cálculo que a ferramenta diz fazer. A diferença está na regra, que pertence às decisões D2-C, D5, D11-A e às observações O2 e O7.

## 3. Resultado caso a caso (98 casos)

Para os casos de fórmula, "obtido" é o valor devolvido pela ferramenta. Nos casos OK ele é mostrado igual ao esperado, porque o registro grava o valor dentro da tolerância.

| Caso | Ferramenta | Indicador | Tipo | Esperado | Obtido | Tolerância | Status |
|---|---|---|---|---|---|---|---|
| C-B08-R-fc1 | B08 | Fluxo do ano 1 (rampa 25%→40% em 3 anos, reajuste 5%, extras 10%) | formula | 43042.5 | 43042.5 | 0.01 | OK |
| C-B08-R-vpl | B08 | VPL a 12% | formula | -502004.793594 | -502004.793594 | 0.01 | OK |
| C-B08-R-tir | B08 | TIR | formula | 0.022371 | 0.022371 | 0.0001 | OK |
| C-B08-R-paybackS | B08 | Payback simples | formula | 9.053656 | 9.053656 | 0.01 | OK |
| C-B08-R-paybackD | B08 | Payback descontado (não ocorre em 10 anos) | formula | nulo | nulo | 0.01 | OK |
| C-B08-R-roi10 | B08 | Retorno acumulado em 10 anos (valor) | formula | 0.150318 | 0.150318 | 0.0001 | OK |
| C-B08-V-vpl | B08 | VPL a 12% com valor residual de 50% | formula | -308820.85164 | -308820.85164 | 0.01 | OK |
| C-B08-V-tir | B08 | TIR com valor residual | formula | 0.071789 | 0.071789 | 0.0001 | OK |
| C-B08-V-roi10 | B08 | Retorno acumulado com residual (valor) | formula | 0.650318 | 0.650318 | 0.0001 | OK |
| C-B08-V-paybackS | B08 | Payback simples (o residual não entra) | formula | 9.053656 | 9.053656 | 0.01 | OK |
| C-B08-E-1 | B08 | Ocupação de equilíbrio sem reserva | formula | 0.135742 | 0.135742 | 0.0001 | OK |
| C-B08-E-2 | B08 | Ocupação de equilíbrio com reserva de 4%, pela regra aprovada (reserva fora das deduções não muda o equilíbrio) | divergencia | 0.135742 | 0.143818 | 0.0001 | DIVERGÊNCIA CONFIRMADA |
| C-B08-E-3 | B08 | Ocupação de equilíbrio com reserva de 4% como dedução (conferência da conta atual) | formula | 0.143818 | 0.143818 | 0.0001 | OK |
| C-A09-P-1 | A09 | Investimento total com contingência de 10% | formula | 748000 | 748000 | 0.01 | OK |
| C-A09-P-recBruta | A09 | Receita bruta com extras de R$ 1.000/mês | formula | 190200 | 190200 | 0.01 | OK |
| C-A09-P-ded | A09 | Deduções (comissão 12% + imposto 6% + gestão 10%) | formula | 53256 | 53256 | 0.01 | OK |
| C-A09-P-resultado | A09 | Resultado do ano | formula | 21504 | 21504 | 0.01 | OK |
| C-A09-P-roi | A09 | Retorno anual (valor) | formula | 0.028749 | 0.028749 | 0.0001 | OK |
| C-A09-P-payback | A09 | Payback simplificado (34,8 anos, sem limite) | formula | 34.784226 | 34.784226 | 0.01 | OK |
| C-A09-G-1 | A09 | Resultado operacional antes da taxa de gestão (dicionário: gestão é custo do modelo) | limitacao | 40524 | 21504 | 0.01 | LIMITAÇÃO CONFIRMADA (decisão pendente) |
| C-A09-D-1 | A09 | Receita com o máximo do campo (31 noites × 12 = 372 dias) igual à de 365 dias | limitacao | 282948 | 288374.4 | 0.01 | LIMITAÇÃO CONFIRMADA (decisão pendente) |
| C-A09-D-2 | A09 | Conferência: 31 × 12 noites calculam como definido | formula | 288374.4 | 288374.4 | 0.01 | OK |
| C-B06-iniciante-capex | B06 | CAPEX · perfil iniciante | formula | 449500 | 449500 | 0.01 | OK |
| C-B06-iniciante-inter | B06 | Cenário intermediário (contingência fora do giro) · perfil iniciante | formula | 524450 | 524450 | 0.01 | OK |
| C-B06-iniciante-cons | B06 | Cenário conservador (variação × contingência) · perfil iniciante | formula | 598617.5 | 598617.5 | 0.01 | OK |
| C-B06-iniciante-giro | B06 | Capital de giro (fixo × meses) · perfil iniciante | formula | 30000 | 30000 | 0.01 | OK |
| C-B06-iniciante-desembMes | B06 | Desembolso mensal · perfil iniciante | formula | 61806.25 | 61806.25 | 0.01 | OK |
| C-B06-iniciante-m2 | B06 | Custo por m² da unidade · perfil iniciante | formula | 4000 | 4000 | 0.01 | OK |
| C-B06-intermediario-capex | B06 | CAPEX · perfil intermediario | formula | 722000 | 722000 | 0.01 | OK |
| C-B06-intermediario-inter | B06 | Cenário intermediário (contingência fora do giro) · perfil intermediario | formula | 844640 | 844640 | 0.01 | OK |
| C-B06-intermediario-cons | B06 | Cenário conservador (variação × contingência) · perfil intermediario | formula | 1006368 | 1006368 | 0.01 | OK |
| C-B06-intermediario-giro | B06 | Capital de giro (fixo × meses) · perfil intermediario | formula | 36000 | 36000 | 0.01 | OK |
| C-B06-intermediario-desembMes | B06 | Desembolso mensal · perfil intermediario | formula | 80864 | 80864 | 0.01 | OK |
| C-B06-intermediario-m2 | B06 | Custo por m² da unidade · perfil intermediario | formula | 3607.142857 | 3607.142857 | 0.01 | OK |
| C-B06-incompleto-extremo-capex | B06 | CAPEX · perfil incompleto-extremo | formula | 52000 | 52000 | 0.01 | OK |
| C-B06-incompleto-extremo-inter | B06 | Cenário intermediário (contingência fora do giro) · perfil incompleto-extremo | formula | 52000 | 52000 | 0.01 | OK |
| C-B06-incompleto-extremo-cons | B06 | Cenário conservador (variação × contingência) · perfil incompleto-extremo | formula | 52000 | 52000 | 0.01 | OK |
| C-B06-incompleto-extremo-giro | B06 | Capital de giro (fixo × meses) · perfil incompleto-extremo | formula | 0 | 0 | 0.01 | OK |
| C-B06-incompleto-extremo-desembMes | B06 | Desembolso mensal · perfil incompleto-extremo | formula | 52000 | 52000 | 0.01 | OK |
| C-F05-1 | F05 | Diferença verba − total (exemplo) | formula | -16744 | -16744 | 0.01 | OK |
| C-F05-2 | F05 | Custo por m² de área interna (exemplo) | formula | 7224.8 | 7224.8 | 0.01 | OK |
| C-F05-3 | F05 | Custo por m² de área total, interna + deck (exemplo) | formula | 5160.571429 | 5160.571429 | 0.01 | OK |
| C-F05-4 | F05 | Versão em branco: subtotal zero e leitura de espera | formula | [0, Ainda não há itens com cotação] | [0, Ainda não há itens com cotação] | nulo | OK |
| C-J2-I-noitesDisponiveis | Folha J2 | Noites disponíveis (4 × 31) | formula | 124 | 124 | 0.01 | OK |
| C-J2-I-ocupacao | Folha J2 | Ocupação | formula | 0.467742 | 0.467742 | 0.0001 | OK |
| C-J2-I-diariaMediaBruta | Folha J2 | Diária média bruta | formula | 280 | 280 | 0.01 | OK |
| C-J2-I-margemPorNoite | Folha J2 | Margem por noite | formula | 188.675862 | 188.675862 | 0.01 | OK |
| C-J2-I-pontoEquilibrioNoites | Folha J2 | Ponto de equilíbrio (noites) | formula | 35.372834 | 35.372834 | 0.01 | OK |
| C-J2-I-saldoFinal | Folha J2 | Saldo final do caixa | formula | 13620 | 13620 | 0.01 | OK |
| C-J2-I-mesesFolego | Folha J2 | Meses de fôlego | formula | 1.882776 | 1.882776 | 0.001 | OK |
| C-J2-M-custosModelo | Folha J2 | Custos do modelo (aluguel 800 + gestão 1.200 + marca 300) | formula | 2300 | 2300 | 0.01 | OK |
| C-J2-M-ebitda | Folha J2 | EBITDA com custos do modelo | formula | 1969.2 | 1969.2 | 0.01 | OK |
| C-J2-M-geracaoCaixa | Folha J2 | Geração de caixa com custos do modelo | formula | 1426.576 | 1426.576 | 0.01 | OK |
| C-J2-M-mesesFolego | Folha J2 | Meses de fôlego com custos do modelo | formula | 1.428571 | 1.428571 | 0.001 | OK |
| C-J2-M-pontoEquilibrioNoites | Folha J2 | Ponto de equilíbrio com custos do modelo | formula | 47.563053 | 47.563053 | 0.01 | OK |
| C-ZAIOS-M-custosModelo | ZAIOS | Custos do modelo (aluguel R$ 1.000/mês + gestão 10% + royalty 3%) | formula | 48783.24 | 48783.24 | 0.01 | OK |
| C-ZAIOS-M-ebitda | ZAIOS | EBITDA com custos do modelo | formula | 77946.12 | 77946.12 | 0.01 | OK |
| C-ZAIOS-M-geracaoCaixa | ZAIOS | Geração de caixa com custos do modelo e reserva de 4% | formula | 66628.2 | 66628.2 | 0.01 | OK |
| C-ZAIOS-M-resultadoOperacional | ZAIOS | Resultado operacional (antes dos custos do modelo) | formula | 126729.36 | 126729.36 | 0.01 | OK |
| C-ZAIOS-O-receitaBruta | ZAIOS | Receita bruta com outras receitas de 10% | formula | 311242.8 | 311242.8 | 0.01 | OK |
| C-ZAIOS-O-custosVariaveis | ZAIOS | Custos variáveis com custo por estadia (R$ 60, permanência 2,5) | formula | 43274.4 | 43274.4 | 0.01 | OK |
| C-ZAIOS-O-resultadoOperacional | ZAIOS | Resultado operacional com outras receitas e estadia | formula | 143057.124 | 143057.124 | 0.01 | OK |
| C-ZAIOS-S-1 | ZAIOS | Receita bruta com sazonalidade (alta dez–fev, baixa abr–jun) | formula | 315736.8 | 315736.8 | 0.01 | OK |
| C-ZAIOS-S-2 | ZAIOS | Resultado operacional com sazonalidade | formula | 155952.744 | 155952.744 | 0.01 | OK |
| C-ZAIOS-C-mesAberturaProjeto | ZAIOS (composição) | Mês de abertura sugerido pelo cronograma do P5 | formula | 10 | 10 | 0 | OK |
| C-ZAIOS-C-geracaoAno1 | ZAIOS (composição) | Geração do 1º ano (rampa a partir de janeiro) | formula | 15229.812 | 15229.812 | 0.01 | OK |
| C-ZAIOS-C-geracaoRegime | ZAIOS (composição) | Geração do ano de regime | formula | 108846.84 | 108846.84 | 0.01 | OK |
| C-ZAIOS-C-giro | ZAIOS (composição) | Capital de giro recomendado (o maior entre A = 6 × fixo e B) | formula | 63000 | 63000 | 0.01 | OK |
| C-ZAIOS-C-captacao | ZAIOS (composição) | Captação = CAPEX + capital de giro | formula | 1300400 | 1300400 | 0.01 | OK |
| C-ZAIOS-C-retorno | ZAIOS (composição) | Retorno anual sobre o investimento | formula | 0.087964 | 0.087964 | 0.0001 | OK |
| C-ZAIOS-C-vplSem | ZAIOS (composição) | VPL sem saída a 10% | formula | -653689.676467 | -653689.676467 | 0.01 | OK |
| C-ZAIOS-C-vplCom | ZAIOS (composição) | VPL com saída 6× EBITDA | formula | -401898.664041 | -401898.664041 | 0.01 | OK |
| C-ZAIOS-C-payback | ZAIOS (composição) | Payback simples (estendido) | formula | 12.228348 | 12.228348 | 0.01 | OK |
| C-ZAIOS-C-conservador | ZAIOS (composição) | Geração do regime no cenário conservador | formula | 43089.7248 | 43089.7248 | 0.01 | OK |
| C-ZAIOS-C-estresseReceita | ZAIOS (composição) | Estresse: geração com receita 30% menor | formula | 23962.44 | 23962.44 | 0.01 | OK |
| C-ZAIOS-C-capexMaior | ZAIOS (composição) | Estresse: CAPEX 25% maior | formula | 1546750 | 1546750 | 0.01 | OK |
| C-ZAIOS-C-menorSaldo | ZAIOS (composição) | Menor saldo da curva de caixa com a contingência usada | formula | 52438.404 | 52438.404 | 0.01 | OK |
| C-ZAIOS-C-colchao | ZAIOS (composição) | Colchão = menor saldo ÷ CAPEX | formula | 0.042378 | 0.042378 | 0.0001 | OK |
| C-ZAIOS-C-passos | ZAIOS (composição) | Resultado dos 5 passos | formula | [passa, passa, redesenhar, redesenhar, ajustar] | [passa, passa, redesenhar, redesenhar, ajustar] | 0 | OK |
| C-ZAIOS-C-decisao | ZAIOS (composição) | Decisão pela regra dos 5 passos | formula | Redesenhar | Redesenhar | 0 | OK |
| C-ZAIOS-C-veredito | ZAIOS (composição) | Veredito só após homologação (o selo hoje é exibido) | divergencia | sem selo antes da homologação | Redesenhar | nulo | DIVERGÊNCIA CONFIRMADA |
| C-G2-receitaBruta | ZAIOS (G2) | G2 · Receita bruta (centavos) | formula | 130000 | 130000 | 0.5 | OK |
| C-G2-comissoes | ZAIOS (G2) | G2 · Comissões (centavos) | formula | 13000 | 13000 | 0.5 | OK |
| C-G2-receitaLiquida | ZAIOS (G2) | G2 · Receita líquida de distribuição (centavos) | formula | 117000 | 117000 | 0.5 | OK |
| C-G2-fixas | ZAIOS (G2) | G2 · Despesas fixas (centavos) | formula | 30000 | 30000 | 0.5 | OK |
| C-G2-variaveis | ZAIOS (G2) | G2 · Despesas variáveis sem comissões (centavos) | formula | 7000 | 7000 | 0.5 | OK |
| C-G2-despesas | ZAIOS (G2) | G2 · Despesas totais (centavos) | formula | 50000 | 50000 | 0.5 | OK |
| C-G2-resultado | ZAIOS (G2) | G2 · Resultado gerencial (centavos) | formula | 80000 | 80000 | 0.5 | OK |
| C-G2-margem | ZAIOS (G2) | G2 · Margem gerencial (80.000 ÷ 130.000) | formula | 0.615385 | 0.615385 | 0 | OK |
| C-G2-cobertura | ZAIOS (G2) | G2 · Cobertura da reserva (90.000 ÷ média de 20.000, 30.000, 40.000) | formula | 3 | 3 | 0 | OK |
| C-G3-noitesDisponiveis | ZAIOS (G3) | G3 · Noites disponíveis (2 × 30) | formula | 60 | 60 | 0 | OK |
| C-G3-ocupacao | ZAIOS (G3) | G3 · Ocupação (20 ÷ 60) | formula | 0.333333 | 0.333333 | 0 | OK |
| C-G3-diariaMedia | ZAIOS (G3) | G3 · Diária média (hospedagem 100.000 ÷ 20, sem taxa de limpeza) | formula | 5000 | 5000 | 0.5 | OK |
| C-G3-revpar | ZAIOS (G3) | G3 · RevPAR (100.000 ÷ 60) | formula | 1666.666667 | 1666.666667 | 0.5 | OK |
| C-G3-trevpar | ZAIOS (G3) | G3 · TRevPAR (130.000 ÷ 60) | formula | 2166.666667 | 2166.666667 | 0.5 | OK |
| C-G3-despesaPorNoite | ZAIOS (G3) | G3 · Despesa por noite vendida (50.000 ÷ 20) | formula | 2500 | 2500 | 0.5 | OK |
| C-G3-bissexto | ZAIOS (G3) | Dias de fevereiro de 2028 (ano bissexto) | formula | 29 | 29 | nulo | OK |
| C-G2-impostos | ZAIOS (G2) | Impostos sobre a receita tratados como dedução (dicionário), não como despesa variável | limitacao | deducao | despesa variável | nulo | LIMITAÇÃO CONFIRMADA (decisão pendente) |

## 4. Limitações destes testes

1. **Cenário único na composição da ZAIOS.**
   - Os 16 valores de composição usam um só cenário integrado, que é o mesmo dos testes da própria ZAIOS: abertura em janeiro, sem pró-labore, sem sazonalidade, sem outras receitas.
   - As primitivas desses temas foram testadas separadamente, mas não passando pela composição.
2. **Independência parcial no B06 e no fluxo do B08 e do A09.** A regra de referência foi descrita a partir do código no Comando 05B. Os testes provam que o código faz o que diz, não que a regra está certa.
3. **Uma transcrição da composição e da G2/G3** (ver o relatório de integridade).
4. **Testes da própria ZAIOS (vitest) não executados.** Eles importam módulos que não foram lidos.
5. **Sem testes de tela.** Rótulos, veredito e sinal parcial foram verificados só pelo código (pendência T9 do 05D).
6. **G2/G3 com os exemplos do FORMULAS.md.** Lançamentos reais da operação não foram usados, por regra de dados.
