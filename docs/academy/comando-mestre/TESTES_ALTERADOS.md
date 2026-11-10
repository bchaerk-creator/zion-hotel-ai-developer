# Testes da ZAIOS alterados por decisão aprovada

Cada alteração troca a regra antiga pela regra aprovada. O valor antigo fica no comentário da linha. Nenhum teste foi removido.

| Arquivo | Teste | Antes | Depois | Decisão |
|---|---|---|---|---|
| receitas.test.ts | indicadores do ano e veredito | selo "Avançar" | selo "Indicação preliminar", motivo com "a operação se sustenta" | O8 |
| receitas.test.ts | contribuição zero não tem equilíbrio | selo "Ajustar" | "Indicação preliminar", indicação negativa, mesma pendência | O8 |
| receitas.test.ts | margem abaixo de 10% | selo "Ajustar" | indicação negativa | O8 |
| receitas.test.ts | giro A usa o custo fixo do P5 | recomendado = máximo entre A e B | recomendado = necessidade técnica + reserva operacional (A continua calculado e conferido) | O12 |
| viabilidade.test.ts | veredito e uma pendência por passo | colchão = 63.000 / CAPEX (giro A de 6 meses) | colchão = 31.500 / CAPEX (reserva de 3 meses); selo "Ajustar" mantido | O12 |
| viabilidade.test.ts | veredito e uma pendência por passo (caso "todos passam") | giro de 150 mil pela regra A (6 meses) | o mesmo giro de 150 mil pela reserva configurada em 6 meses; com o padrão de 3 meses o passo 5 pediria ajuste | O12 |
