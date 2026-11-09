# Linha de base dos testes de aceite O8 a O14

Gerado em 2026-11-09T22:39:05.101Z contra a cópia da ZAIOS (commit ec21ad5). **Antes da implementação, FALHA é o resultado esperado** onde a decisão ainda não existe no código. PASSA indica um comportamento que já atende à decisão.

| Teste | Verificação | Resultado atual | Evidência |
|---|---|---|---|
| O8-1 | P6 sem selo de aprovação (C2) | FALHA | selo do P6 = "Avançar" |
| O8-2 | Conflito P6 x viabilidade explicitado (C3E) | FALHA | P6 "Avançar" x viabilidade "Redesenhar"; alertas da viabilidade: 0 |
| O8-3 | Margem antes e depois dos custos do modelo com nomes distintos (C1) | FALHA | modelo do P6 expõe só margemOperacional = 0.199332 |
| O9-1 | Saída não negativa com EBITDA < 0 (C1) | FALHA | saída = R$ -92517.75; VPL com saída = R$ -927012.89 |
| O9-2 | Saída inalterada com EBITDA > 0 (C2) | PASSA | saída = R$ 3312531.36 |
| O10-1 | Necessidade de caixa no ano 5 aparece (C1) | FALHA | curva com 36 meses; menor saldo R$ 22704.75; esperado: 1º mês negativo 54 |
| O10-2 | Atraso não melhora o projeto sem explicação (C2) | FALHA | menor saldo com atraso R$ 148656.29 > sem atraso R$ 132524.00 |
| O11-1 | Bases de gestão e royalties configuráveis (C2) | FALHA | sem campo de base; EBITDA = R$ 552088.56 (= combinação bruta/bruta 552088.56) |
| O12-1 | Aluguel na base do giro (C1) | FALHA | giro A = R$ 54000.00 (6 × fixo sem aluguel) |
| O13-1 | Necessário x disponível com déficit (C1) | FALHA | sem campo de capital disponível; captação = R$ 859095.26 |
| O14-1 | Receita independente não cai com a ocupação (C3 → C3E, percentual mantido) | FALHA | outras no C3E com o mesmo percentual = R$ 345600.00 (esperado R$ 480.000,00 para a categoria C) |
