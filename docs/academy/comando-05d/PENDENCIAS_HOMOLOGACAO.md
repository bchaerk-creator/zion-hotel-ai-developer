# Pendências da homologação financeira

Comando 05D · 09/11/2026 · Nada aqui foi executado. Cada item depende de aprovação do Bruno.

## 1. Para a homologação matemática definitiva (só testes, sem mudar ferramentas)

| # | Pendência | Afeta | Classe que fecha |
|---|---|---|---|
| T1 | Testar a camada de composição da ZAIOS (`src/exercicios/*-calculo.ts`): 1º ano com pró-labore, capital de giro A/B, captação, colchão, cenários, sensibilidade e estresse | ZAIOS | Amplia o alcance do H1 da ZAIOS para o que o membro usa |
| T2 | Testar os custos do modelo (aluguel, gestão, royalty) e o EBITDA | ZAIOS | EBITDA H2 → H1 |
| T3 | Testar G2/G3 (`src/calc/operacao.ts`) e confrontar com a Folha J2 (T5 completo) | ZAIOS, Folha J2 | Inclui Gestão na homologação |
| T4 | B08 com rampa linear, reajuste, extras, comissão separada e valor residual | B08 | VPL, TIR e payback H2 → H1 |
| T5 | A09 com contingência, extras em R$, gestão e cenários | A09 | Amplia o H1 |
| T6 | Perfis adicionais do B06 com cálculo independente e fórmula vinda da documentação, não do código | B06 | H2 → H1 |
| T7 | Indicadores, fôlego, equilíbrio e bloco de caixa da Folha J2; revisão dos 92 testes próprios | Folha J2 | H2 → H1 |
| T8 | Confirmar a cópia da ZAIOS por hash com exportação direta (GitHub sincronizado) | ZAIOS | Remove a ressalva de transcrição |
| T9 | Testes de tela (rótulos, veredito, sinal parcial), hoje verificados só pelo código-fonte | Todas | Evidência de exibição |

## 2. Divergências metodológicas confirmadas (aguardam implementação autorizada)

| Decisão | Divergências | Ferramentas |
|---|---|---|
| D1 · retorno anual x acumulado | 3 | ZAIOS (sem acumulado), B08 e A09 (rótulo "ROI") |
| D2-C · reserva de reposição | 5 | ZAIOS (3% e **faixa 3–5%**, aprovada 3–6%), Folha J2 (base receita real), B08 (dentro das deduções), A09 (ausente) |
| D3-A · quebra e perdas | 5 | ZAIOS (sem valor medido em R$), B08 e A09 (ausente) |
| D4 · pró-labore, distribuição, caixa (citada como "D4-C" no Comando 05D) | 4 | ZAIOS e Folha J2 (sem distribuição e caixa disponível), B08 e A09 (sem pró-labore) |
| D7-C · valor de saída | 4 | ZAIOS (só o múltiplo, sem valor líquido), B08 (residual em %) |
| D11-A · Régua Única | 4 | ZAIOS (veredito sem trava de homologação), B08 e A09 (sem contagem de critérios), A09 (metas misturadas) |

## 3. Decisões metodológicas ainda pendentes (Bruno)

| Decisão | Tema |
|---|---|
| D5 | A09: noites por mês inteiras (360 dias) e custo fixo sempre × 12 |
| D6 | Base da contingência nas ferramentas simples |
| D8 | Payback acima do horizonte: estender ou nulo |
| D9 | Custo variável por noite ou por estadia |
| D10 | Cenários de referência |
| D12 | Meses de fôlego x cobertura da reserva |
| D13 | Moeda em float x centavos |
| D14 | Taxa de limpeza e outras receitas |

## 4. Observações novas deste parecer (para classificar)

| # | Observação | Natureza |
|---|---|---|
| O1 | Faixa da reserva da ZAIOS 3–5% x aprovada 3–6% | Divergência D2-C (já registrada) |
| O2 | O A09 soma "gestão" às deduções; na ZAIOS gestão é custo do modelo (abaixo do resultado operacional) | Categoria; propor nova divergência (D15?) ou incluir na D9 |
| O3 | O B08 calcula o ponto de equilíbrio com a reserva dentro das deduções, o que eleva o equilíbrio | Consequência da D2-C no B08 |
| O4 | Convenção do payback (entrada uniforme no ano) diferente da do VPL (fim do ano) | Registrar no dicionário (texto), sem mudar fórmula |
| O5 | O nome da decisão D4 apareceu como "D4-C" no Comando 05D | Confirmar a nomenclatura |

## 5. Validação econômica (H4, fora do escopo matemático)

Os 15 parâmetros do T12 dependem de evidência por tipo de hospedagem, porte e perfil:
- deduções 17%;
- quebra 1%;
- reserva 4% (3–6%);
- R$ 40/hora;
- rampa 40/50/75%;
- OS&E 12%;
- pré-abertura 5%;
- contingências 20–25% e 10–15%;
- cenários conservador e otimista;
- múltiplo 6×;
- payback de 8 e 12 anos;
- colchão de 10%;
- 3 meses de fixo.

Também falta definir a meta da reserva de emergência e as referências de custos de venda e tributos do valor de saída (profissional habilitado).

## 6. Processo e governança

| # | Pendência | Responsável |
|---|---|---|
| P1 | Revisar e aprovar o parecer (classificação H1 a H4) | Bruno |
| P2 | Definir quem faz a conferência externa (contador, analista) | Bruno |
| P3 | Decidir onde guardar a cópia do código da ZAIOS usada nos testes (fora do repositório público) | Bruno |
| P4 | Definir a homologação econômica: fontes de evidência e calendário | Bruno + equipe |
| P5 | Autorizar a implementação, na sequência proposta (D11-A primeiro) | Bruno |
