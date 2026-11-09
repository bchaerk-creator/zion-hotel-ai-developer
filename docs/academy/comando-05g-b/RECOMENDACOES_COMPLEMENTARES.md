# Recomendações complementares P-O8 a P-O14

Comando 05G-B · 09/11/2026 · **Propostas, não decisões aprovadas.** As decisões O8 a O14 (05G-A) continuam como estavam. Estas recomendações só detalham como implementá-las e aguardam a aprovação do Bruno.

| # | Proposta | Verificação feita neste comando | Situação |
|---|---|---|---|
| **P-O8** | Rótulo "Indicação preliminar" no P6. Margens antes e depois dos custos do modelo. A régua de margem não funciona como selo de aprovação | Linha de base do 05G-A: O8-1, O8-2 e O8-3 falham hoje (o selo "Avançar" aparece; não há aviso de conflito; só existe a margem antes dos custos do modelo) | Proposta |
| **P-O10a** | Manter a convenção atual do VPL (fluxo anual, desconto no fim do ano) e documentar como os 36 meses mensais são agregados por ano | **Efeito medido de forma independente** (`composicao_05g/efeito_convencao_vpl.py`): diferença entre o VPL anual atual e um VPL mensal (CAPEX pelo cronograma, operação a partir do mês 10, taxa mensal equivalente). C1: +R$ 41.436 (+5,5% do CAPEX); C2: −R$ 562 (−0,03%); C3: +R$ 61.160 (+0,9%); C3E: +R$ 229.310 (+3,4%). **Nenhum sinal muda.** A convenção atual é a mais conservadora em 3 de 4 cenários | Proposta, com evidência |
| **P-O10b** | Simular atrasos em meses dentro do horizonte de 10 anos, com receita não realizada, custos mantidos e impacto em VPL, caixa e retorno | Teste O10-2 (05G-A): em C2, o atraso de 6 meses reduz o saldo em 10 anos em R$ 256.539,15, mas hoje "melhora" o menor saldo dos 36 meses. A proposta corrige a leitura | Proposta |
| **P-O10c** | Cenário conservador do atraso: só a operação atrasa; o CAPEX segue o cronograma original. Não é a única modalidade possível | É o comportamento atual da ZAIOS (a curva com atraso mantém o cronograma). Precisa ficar declarado na tela | Proposta |
| **P-O11** | Além de % sobre hospedagem ou receita bruta, modalidade em valor fixo (R$) para gestão, royalties e encargos, com unidade, periodicidade e base contratual. Compatível com a O6 | O aluguel já existe em R$/mês. Gestão e royalty hoje só aceitam % da receita bruta (`receitas.ts`, linhas 45–46). A O6 (Folha J2 em R$) fica resolvida se a ZAIOS aceitar as duas modalidades | Proposta |
| **P-O12** | Separar três números: (1) necessidade técnica pela curva de caixa; (2) reserva operacional de obrigações fixas recorrentes, com aluguel; (3) giro disponível. **Não somar automaticamente (1) e (2)** | **Verificado no código e nos testes:** o giro B atual já soma uma reserva (déficit da rampa + meses negativos + **3 × fixos com pró-labore**). O giro A (6 × fixo do P5, sem pró-labore e sem aluguel) é uma segunda reserva. Exemplo C1: B = 66.675,64 + 15.419,63 + 27.000 = 109.095,26. Somar uma reserva operacional nova ao B contaria duas vezes. O prazo de 3 meses continua pendente | Proposta; o prazo não está aprovado |
| **P-O13** | Capital próprio destinado ao giro é uma fonte. Não reduz a necessidade técnica. Mostrar necessidade, disponível e diferença | Teste O13-4 (05G-A): usar o disponível no lugar do necessário levaria a curva do C1 de +R$ 22.704,75 para −R$ 41.390,51. A proposta evita essa troca silenciosa | Proposta |
| **P-O14** | Categorias A (por noite ocupada), B (ticket × adesão × estadias ou consumidores), C (independentes, com projeção, sazonalidade e variação de demanda próprias). Verificar rampa, cenários e tributos por categoria. Compatibilidade do `outras_pct` sem migração agora | Hoje "outras" = % das diárias: acompanha ocupação, rampa e cenários (C3E: R$ 345.600 em vez de R$ 480.000). O `outras_pct` atual equivale à categoria A em % das diárias, o que permite manter os dados salvos | Proposta |

## Itens que continuam sem proposta fechada

- **Prazo da reserva operacional (P-O12):** 3 meses é proposta. 6 meses não está aprovado como regra universal (O12).
- **Alíquota por categoria de receita (P-O14 e D14):** a mesma alíquota é só padrão de teste.
- **Fatores de cada categoria por tipo de hospedagem (P-O14):** são H4.
- **Valor de saída por outros métodos e valor líquido (D7-C):** a O9 cobre só o múltiplo.
