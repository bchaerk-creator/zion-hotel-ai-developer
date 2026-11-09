# Ressalvas encerradas e abertas

Comando 05E · 09/11/2026 · Referência: pendências T1 a T9 e observações O1 a O5 do Comando 05D (`docs/academy/comando-05d/PENDENCIAS_HOMOLOGACAO.md`, preservado).

"Encerrada" quer dizer que a lacuna de **teste matemático** foi coberta. Não quer dizer que a metodologia foi aprovada nem que algo foi corrigido nas ferramentas.

## 1. Encerradas (propostas, para confirmação do Bruno)

| # | Ressalva do 05D | Como foi encerrada |
|---|---|---|
| T2 | ZAIOS · custos do modelo (aluguel, gestão, royalty) e EBITDA | 4 casos OK contra cálculo independente |
| T3 (parte G2/G3) | ZAIOS · G2/G3 sem teste | 16 casos OK contra os exemplos documentados |
| T4 | B08 com rampa, reajuste, extras, comissão separada e residual | 10 casos OK (VPL, TIR, payback simples, retorno acumulado) |
| T5 | A09 com contingência, extras em R$, gestão e cenários | 6 casos OK (payback e componentes) |
| T7 (parte cálculo) | Folha J2 · indicadores, fôlego, equilíbrio, bloco de caixa | 12 casos OK, incluindo os custos do modelo |
| — | ZAIOS · outras receitas, custo por estadia, sazonalidade | 5 casos OK |
| — | F05 · diferença entre verba e total, R$/m², versão em branco | 4 casos OK |

## 2. Parcialmente encerradas

| # | Ressalva | O que foi feito | O que falta |
|---|---|---|---|
| T1 | ZAIOS · camada de composição | 16 valores OK (1º ano, giro A/B, captação, curva, colchão, VPL, payback, cenário conservador, estresse, 5 passos, decisão) | Outros cenários: pró-labore, sazonalidade, outras receitas e abertura fora de janeiro passando pela composição. A sensibilidade não foi testada |
| T3 (parte cruzada) | Confrontar G2/G3 com a Folha J2 | As duas conferem com o dicionário, cada uma no seu exemplo | Um mesmo mês lançado nas duas, lado a lado |
| T6 | B06 · perfis adicionais | 3 perfis, 17 casos OK | A fórmula de referência vem do código. Falta um documento-fonte da regra do B06 para uma conferência totalmente independente |
| T8 | Integridade da cópia da ZAIOS | 3 transcrições idênticas do motor; prova funcional | Hash calculado na origem (GitHub sincronizado ou exportação). **Integridade não declarada** |

## 3. Abertas

| # | Ressalva | Tipo | Depende de |
|---|---|---|---|
| T7 (revisão) | 92 testes próprios da Folha J2 não revisados | Teste | Autorização para revisar |
| T9 | Testes de tela (rótulos, veredito, sinal parcial) | Teste | Acesso de visualização. Não exige créditos, mas exige definir o meio |
| — | Execução dos testes da própria ZAIOS (vitest) sobre a cópia | Teste | Ler os módulos que faltam (dossiê, definições), sem créditos |
| O1 | Faixa de reserva da ZAIOS 3–5% x aprovada 3–6% | Divergência D2-C | Implementação autorizada |
| O2 | A09 · gestão nas deduções | Classificação | Decisão do Bruno (nova D15 ou dentro da D9) |
| O3 | B08 · equilíbrio com reserva nas deduções | Consequência da D2-C | Implementação autorizada |
| O4 | Convenção do payback (entrada uniforme) diferente da do VPL (fim do ano) | Texto do dicionário | Revisão do dicionário |
| O5 | Nome "D4-C" x "D4" | Nomenclatura | Confirmação do Bruno |
| **O6 (nova)** | Folha J2: custos do modelo em R$ x dicionário em % da receita | Classificação | Decisão do Bruno |
| **O7 (nova)** | G2 da ZAIOS: impostos como despesa variável x dedução no dicionário | Classificação | Decisão do Bruno |
| **Correção** | Parecer do 05D: "no máximo 360 dias" no A09; o certo é até 372 | Documento | Próxima versão do parecer |
| D5, D6, D8, D9, D10, D12, D13, D14 | Decisões metodológicas pendentes | Metodologia | Bruno |
| ZAIOS | Veredito exibido antes da homologação | Divergência D11-A | Implementação autorizada (créditos Lovable) |
| D1, D2-C, D3-A, D4, D7-C, D11-A | Divergências confirmadas nas ferramentas | Metodologia aprovada, não implementada | Implementação autorizada |
| H4 | Parâmetros de referência e limites da régua | Econômica | Homologação econômica (P4) |
| P1 a P5 | Governança (aprovação do parecer, conferência externa, guarda da cópia, calendário econômico, autorização de implementação) | Processo | Bruno |
