# Decisões metodológicas financeiras · registro consolidado

Comando 05B · 09/11/2026 · Responsável: Bruno Chaerk · **Seis decisões aprovadas. Implementação não autorizada.**

Fonte de cada decisão: mensagens do Bruno nesta sessão, 09/11/2026. Dicionário correspondente: `DICIONARIO_FINANCEIRO.md` v0.4.

## 1. As seis decisões

| Decisão | O que foi aprovado | Efeito no dicionário |
|---|---|---|
| **D1 · Indicadores de retorno** | Separar o retorno anual sobre o investimento do retorno acumulado em 10 anos | "ROI" sem qualificador deixa de existir. **Retorno anual** = geração do regime ÷ investimento. **Retorno acumulado em 10 anos** = (Σ fluxos − investimento) ÷ investimento, com e sem saída |
| **D2-C · Reserva de reposição** | 4% provisórios sobre a receita bruta efetivamente realizada, faixa ajustável de 3% a 6% | Separada da **reserva de emergência**; sai uma única vez, depois do EBITDA; não é dedução nem custo; validar por tipo de hospedagem |
| **D3-A · Quebra e perdas** | Custo variável operacional sobre a receita efetivamente realizada com hospedagem, referência provisória ajustável de 1% | Prioridade para valores medidos; rótulo explícito quando a ferramenta não calcula; sem dupla contagem com deduções ou reservas |
| **D4 · Remuneração e caixa** | Diferenciar pró-labore, distribuição de resultados e caixa disponível | **Pró-labore** = custo fixo, antes do resultado. **Distribuição** = depois de custos e reservas, não é custo. **Caixa disponível** = saldo + geração − reserva de emergência − distribuição |
| **D7-C · Valor de saída** | Múltiplo do EBITDA, avaliação patrimonial e valor estimado informado | Método sempre identificado; cenário sem venda ao lado; valor líquido de custos, tributos e obrigações |
| **D11-A · Régua Única de Viabilidade** | Cinco critérios: geração de caixa operacional; resistência ao conservador; prazo de recuperação; criação de valor (VPL com e sem saída); segurança financeira e colchão | Ferramentas simples mostram "X de 5 critérios avaliados. Sinal parcial…". Avançar, Ajustar e Redesenhar só com os cinco critérios e após a homologação. Metas do A09 separadas. Limites provisórios, a validar por tipo, porte e perfil. Nenhuma classificação garante viabilidade, financiamento ou retorno |

**Correção de registro:** a D3 constava como "apresentada, sem decisão" no `docs/zaios/DECISOES.md`. O Bruno informou que a D3-A já estava aprovada. Correção documental feita em 09/11/2026.

---

## 2. Matriz de aderência de cada ferramenta

Situação **atual**, sem nenhuma alteração. Legenda:
- **Adere:** já segue a decisão.
- **Parcial:** segue em parte.
- **Não adere:** precisa mudar depois da homologação.
- **N/A:** a decisão não se aplica ao escopo.

| Decisão | ZAIOS (P5/P6, G2/G3) | Folha Única J2 | B08 | A09 | B06 | F05 |
|---|---|---|---|---|---|---|
| **D1** retorno anual x acumulado | **Parcial:** tem "retorno anual"; falta o acumulado em 10 anos | N/A (mensal) | **Não adere:** "ROI10" acumulado sem o retorno anual com o nome novo; rótulo "ROI" | **Não adere:** "ROI" anual sem qualificador | N/A | N/A |
| **D2-C** reserva 4% da receita bruta realizada, separada da emergência | **Não adere:** 3% da receita bruta | **Parcial:** 4% e faixa 3–6% certos, mas sobre a **receita real**; reserva de emergência separada nas "reservas separadas" | **Não adere:** reserva **dentro das deduções** | **Não adere:** não tem reserva | N/A | N/A |
| **D3-A** quebra como custo variável, 1%, medido primeiro | **Parcial:** 1% das diárias como custo variável; não aceita valor medido em R$ | **Adere:** prefere o valor medido; 1% só em branco | **Não adere:** não tem quebra nem rótulo | **Não adere:** não tem quebra nem rótulo | N/A | N/A |
| **D4** pró-labore, distribuição, caixa | **Parcial:** pró-labore como custo fixo ("retirada"); não separa distribuição nem caixa disponível | **Parcial:** pró-labore e bloco de caixa; "distribuição" não tem nome próprio | **Não adere:** sem pró-labore nem rótulo | **Não adere:** sem pró-labore nem rótulo | N/A | N/A |
| **D7-C** saída por 3 métodos, sem venda ao lado, valor líquido | **Parcial:** só o múltiplo × EBITDA; mostra com e sem saída; não desconta custos nem tributos | N/A | **Não adere:** residual em % do investimento (até 100%), sem método nem valor líquido | N/A (sem saída) | N/A | N/A |
| **D11-A** régua de 5 critérios, sinal parcial, veredito só após homologação | **Parcial:** calcula os 5 critérios, mas já mostra o veredito **antes da homologação** | N/A (gestão mensal) | **Não adere:** sinal só pelo VPL ≥ 0; sem contagem de critérios | **Não adere:** avisos por meta do usuário misturados; sem contagem de critérios | N/A (orçamento) | N/A (orçamento) |

**Leitura:**
- Nenhuma ferramenta adere a tudo.
- A ZAIOS e a Folha Única J2 são as mais próximas.
- B08 e A09 concentram as mudanças.
- B06 e F05 só são afetados por decisões ainda pendentes (D6, contingência).

---

## 3. Pendências técnicas e metodológicas

**Metodológicas (decisão do Bruno):**
1. **Divergências ainda sem decisão:**
   - D5: dias e fixos no A09.
   - D6: base da contingência.
   - D8: payback além do horizonte.
   - D9: custo variável por noite ou por estadia.
   - D10: cenários de referência.
   - D12: meses de fôlego x cobertura da reserva.
   - D13: moeda.
   - D14: taxa de limpeza.
2. **Meta da reserva de emergência:** em meses de custo fixo.
3. **Validação das referências por tipo de hospedagem, porte e perfil** (glamping/bubble, cabana, chalé, pousada, apartamento):
   - reserva 4%, quebra 1%, deduções 17%;
   - limites da régua (8 e 12 anos, colchão de 10%, 3 meses);
   - rampa 40/50/75%;
   - cenários −10% e −20%;
   - múltiplo 6×.
4. **Quem homologa:** Bruno, com contador e, para tributos de saída, um advogado ou contador tributarista. Definir também quais evidências valem: dados reais da Zion Bubble, mercado, literatura.
5. **Tributos e custos de venda no valor de saída:** referências para corretagem, documentação e ganho de capital (exigem profissional habilitado).

**Técnicas:**
1. ZAIOS:
   - mudar a reserva de 3% para 4%;
   - aceitar quebra medida em R$;
   - separar distribuição e caixa disponível;
   - três métodos de saída e valor líquido;
   - retorno acumulado;
   - **ocultar o veredito até a homologação** (hoje aparece).

   **Exige créditos Lovable e autorização.**
2. B08: reserva fora das deduções; quebra; pró-labore; método de saída; rótulos D1; régua com contagem de critérios.
3. A09: reserva; quebra; pró-labore; rótulos D1; régua parcial; metas separadas; dias (D5).
4. Folha J2: base da reserva de receita real para receita bruta realizada.
5. Testes T1 a T12 escritos no formato de cada ferramenta.
6. Revisão de textos: aulas, e-books F02/F03, tutoriais e criativos que citem "ROI", reserva ou veredito.

---

## 4. Proposta de sequência de implementação (não executada)

Cada etapa só começa com autorização expressa do Bruno.

| Etapa | O que | Onde | Depende de | Custo |
|---|---|---|---|---|
| 0 | Teste fechado da ZAIOS (roteiro de 15 itens) | ZAIOS | Bruno | 0 |
| 1 | Escrever os testes T1 a T12 como arquivos, **sem mudar ferramentas** (os testes vão falhar onde há não aderência, e isso serve de prova) | Repositório (cada pasta) | Autorização para "preparação de testes" (já dada para documentar) | Tempo de sessão |
| 2 | Homologação **matemática** da ZAIOS v0 (casos F01, F02, F03, T1, T2) e do dicionário v0.4 → v1.0 nas fórmulas | Bruno + contador | Etapa 1 | 0 |
| 3 | ZAIOS: ocultar o veredito até a homologação (D11) e trocar os rótulos (D1) | Lovable | Etapa 2 + autorização | Créditos Lovable (estimativa baixa) |
| 4 | ZAIOS: reserva 4% (D2-C), quebra medida (D3-A), distribuição e caixa (D4), saída (D7-C) | Lovable | Etapa 3 | Créditos Lovable (estimativa média) |
| 5 | B08 e A09: D1, D2-C, D3-A, D4, D7-C, D11-A, um por vez, com teste antes e depois | Sessão Zion Arsenal | Etapa 2 | Tempo de sessão |
| 6 | Folha Única J2: base da reserva (D2-C) | Sessão Marketing da Zion install | Etapa 2 | Tempo de sessão |
| 7 | Decisões pendentes D5, D6, D8, D9, D10, D12–D14 → B06, F05 e ajustes finais | Sessões responsáveis | Decisões do Bruno | Tempo de sessão |
| 8 | Homologação **econômica** das referências por tipo de hospedagem (evidências) | Bruno + equipe | Dados reais e de mercado | Tempo da equipe |
| 9 | Revisão de textos (aulas, e-books, tutoriais, criativos) | Sessões de conteúdo | Etapas 3 a 7 | Tempo de sessão |
| 10 | Regressão final: todas as ferramentas passam T1 a T12 → dicionário v1.0 completo | Todas | Etapas 1 a 9 | — |
