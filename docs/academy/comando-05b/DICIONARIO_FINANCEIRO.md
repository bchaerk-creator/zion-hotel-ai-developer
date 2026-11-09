# Dicionário financeiro Zion · Academy e ZAIOS

**Versão 0.1 · proposta de 09/11/2026 · NÃO homologado.** Comando 05B. Nada foi alterado em ferramentas ou na ZAIOS.

## Regras do dicionário

1. **Fonte única.** Toda ferramenta da Zion (ZAIOS, mini mentorias, planilhas, Folha Única) usa estes nomes, definições e fórmulas. Ferramentas simplificadas podem **omitir** componentes, desde que digam qual omitiram ("resultado antes da sua retirada"). Nunca podem **redefinir** um nome.
2. **Tipos de valor.** Todo número mostrado ao aluno tem um tipo:
   - **Ilustrativo:** exemplo com dados fictícios, só para ensinar a conta.
   - **Referencial:** "Referência Zion", ponto de partida ajustável, com faixa e fonte; não é dado do aluno.
   - **Comprovado:** vem de documento do aluno (extrato, nota, cotação, contrato) ou de medição real; só o aluno ou a equipe marcam como comprovado.
   - **Calculado:** resultado de fórmula; herda o menor grau de confiança dos insumos.
3. **Versões.** Mudança de definição, fórmula ou referência sobe a versão:
   - **0.x:** proposta.
   - **1.0:** homologado pelo Bruno.
   - **1.x:** ajuste de referência.
   - **2.0:** mudança de fórmula.

   Cada resultado guarda a versão usada. Registro das mudanças no fim deste arquivo.
4. **Unidades.** Dinheiro em R$ (na ZAIOS, centavos inteiros; nas ferramentas simples, float com arredondamento só na tela, tolerância de R$ 0,01). Percentuais guardados como fração e mostrados em %. Tempo em anos ou meses, sempre dito.
5. **Status de cada item:**
   - **Proposto:** ainda não decidido.
   - **Decidido v0:** já decidido em `docs/zaios/PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md`.
   - **Divergente:** precisa de decisão; ver as divergências D1 a D14 em `AUDITORIA_COMERCIAL_FINANCEIRA.md`.

---

## 1. Operação

| Termo | Unidade | Definição | Fórmula | Referência / fonte | Status |
|---|---|---|---|---|---|
| Unidades | nº | Quartos, cabanas ou casas à venda | informado | — | Decidido v0 |
| Dias abertos | dias | Dias do calendário em que a unidade pode ser vendida | informado; ano = 365 (fev. 28), mês = dias reais | ZAIOS | Decidido v0 |
| Noites disponíveis | noites | Capacidade de venda | unidades × dias abertos | ZAIOS, CoStar/STR | Decidido v0 |
| Noites vendidas | noites | Noites efetivamente vendidas | informado, ou disponíveis × ocupação | ZAIOS | Decidido v0 |
| Ocupação | % | Parte da capacidade vendida | noites vendidas ÷ noites disponíveis | CoStar/STR | Decidido v0 |
| Estadia média | noites | Noites por reserva | noites vendidas ÷ estadias | J2, ZAIOS | Proposto (ref. 2 noites só como estimativa) |
| Sazonalidade | — | Ocupação e diária por temporada (alta, média, baixa) | por mês | ZAIOS P6 | Decidido v0 |
| Rampa | % | Ocupação do 1º ano em relação ao regime | 40% (meses 1–3), 50% (4–6), 75% (7–12) | ZAIOS P6 (F02) | Decidido v0; referencial |

## 2. Receita

| Termo | Unidade | Definição | Fórmula | Referência / fonte | Status |
|---|---|---|---|---|---|
| Diária média (ADR) | R$ | Receita de hospedagem por noite vendida | receita de hospedagem ÷ noites vendidas | CoStar/STR | Decidido v0 |
| Receita de hospedagem | R$ | Diárias brutas, antes de descontos, comissões e impostos; **sem a taxa de limpeza** | noites vendidas × diária média | ZAIOS, J2 | Decidido v0 |
| Outras receitas | R$ | Alimentação, experiências, extras; taxa de limpeza excedente (leitura J2) | informado ou % das diárias | ZAIOS, J2 | Proposto (D14) |
| Receita bruta | R$ | Hospedagem + outras receitas | soma | ZAIOS | Decidido v0 |
| RevPAR | R$ | Receita de hospedagem por noite disponível | receita de hospedagem ÷ noites disponíveis = ADR × ocupação | CoStar/STR | Decidido v0 |
| TRevPAR | R$ | Receita total por noite disponível | receita bruta ÷ noites disponíveis | CoStar/STR | Decidido v0 |

## 3. Deduções e receita real

| Termo | Unidade | Definição | Fórmula | Referência / fonte | Status |
|---|---|---|---|---|---|
| Deduções | R$ / % | O que sai antes de a receita chegar: descontos, comissões de canal, processamento, imposto sobre a receita, cancelamentos | soma dos componentes, ou receita bruta × % | **Referência Zion 17%** (15% comissões, processamento e impostos + 2% cancelamentos), ajustável por regime e canal | Decidido v0 |
| Receita real (líquida) | R$ | O que de fato chega | receita bruta − deduções | ZAIOS, J2 | Decidido v0 |

## 4. Custos e resultado

| Termo | Unidade | Definição | Fórmula | Referência / fonte | Status |
|---|---|---|---|---|---|
| Custo variável | R$ | Sai com cada noite ou estadia vendida | noites × custo por noite + estadias × custo por estadia + quebra | ZAIOS, J2 | Decidido v0 (D9: ferramentas simples podem ter um componente, com rótulo) |
| Quebra e perda | % | Itens quebrados ou perdidos | diárias × % (custo variável) | **Referência Zion 1%** | Decidido v0 (D3: faltando em B08/A09) |
| Margem de contribuição | R$ | O que sobra para pagar os fixos | receita real − custos variáveis | ZAIOS, J2 | Decidido v0 |
| Retirada do dono | R$/mês | O custo do trabalho do proprietário | horas por semana × valor da hora × 4,33 | **Referência Zion R$ 40/h** | Decidido v0 (D4: faltando em B08/A09) |
| Custos fixos | R$ | Saem com casa cheia ou vazia; incluem a retirada | soma | ZAIOS, J2 | Decidido v0 |
| Resultado operacional | R$ | O que sobra da operação ("quanto sobrou") | margem de contribuição − custos fixos | ZAIOS, J2 | Decidido v0 |
| Margem operacional | % | — | resultado operacional ÷ receita bruta | ZAIOS | Decidido v0 |
| Custos do modelo | R$ | Aluguel, taxa de gestão, royalty | aluguel + receita bruta × (gestão + royalty) | ZAIOS | Decidido v0 |
| EBITDA | R$ | Resultado antes de juros, impostos sobre o lucro, depreciação e amortização | resultado operacional − custos do modelo | ZAIOS | Decidido v0 |
| Reserva de reposição | R$ / % | Dinheiro guardado para trocar bens que se desgastam; **não é dedução** | receita bruta × % (abaixo do EBITDA) | Referência Zion **3%** (ZAIOS) ou **4%** (J2), faixa 3–6% | **Divergente (D2)** |
| Geração de caixa | R$ | O que fica no caixa da operação | EBITDA − reserva de reposição | ZAIOS | Decidido v0 |
| Equilíbrio (noites) | noites | Noites que empatam o resultado | (fixos + aluguel) ÷ contribuição por noite | ZAIOS | Decidido v0 |
| Ocupação de equilíbrio | % | — | equilíbrio ÷ noites disponíveis | ZAIOS | Decidido v0 |
| Meses de fôlego | meses | Quantos meses o caixa paga os fixos | (saldo + reservas separadas) ÷ fixo do mês | J2 | Proposto (D12, convive com "cobertura da reserva" da ZAIOS G2) |

## 5. Investimento

| Termo | Unidade | Definição | Fórmula | Referência / fonte | Status |
|---|---|---|---|---|---|
| CAPEX | R$ | Investimento para implantar: linhas de terreno e infraestrutura, projeto e licenças, obra, apoio e áreas comuns, FF&E, OS&E, pré-abertura + contingência | soma das linhas + contingência | ZAIOS P5 (F01) | Decidido v0 |
| OS&E | R$ | Enxoval, louça, utensílios | FF&E × % | Referência Zion 12% (faixa 10–15%) | Decidido v0 |
| Pré-abertura | R$ | Gastos antes de abrir | base × % | Referência Zion 5% (faixa 5–10%) | Decidido v0 |
| Contingência | R$ / % | Margem para imprevistos de obra | base (infraestrutura + obra + apoio) × %; **nunca sobre o capital de giro** | Referência Zion 20–25% (primeira obra), 10–15% (com experiência) | **Divergente (D6)**: ferramentas simples podem usar "total" com aviso |
| Capital de giro | R$ | Caixa para operar até a receita estabilizar | o maior entre 6 × fixo sem retirada e (déficit da rampa + sazonalidade + 3 × fixo com retirada) | ZAIOS | Decidido v0 |
| Necessidade total | R$ | Tudo o que o projeto precisa | CAPEX + capital de giro | ZAIOS | Decidido v0 |

## 6. Viabilidade

| Termo | Unidade | Definição | Fórmula | Referência / fonte | Status |
|---|---|---|---|---|---|
| Horizonte | anos | Período do fluxo | 10 anos | F03 | Decidido v0 |
| Fluxo do projeto | R$ | Ano 0 = −CAPEX; ano 1 = geração do 1º ano; anos 2–10 = geração do regime | — | ZAIOS | Decidido v0 |
| Taxa de desconto | % a.a. | Custo do dinheiro do aluno + prêmio de risco | **informada pelo aluno**, sem valor sugerido | Decisão 08/11 | Decidido v0 |
| VPL | R$ | Valor presente do fluxo | Σ fluxo_t ÷ (1 + taxa)^t, fluxos no fim do ano | F03 | Decidido v0 |
| TIR | % a.a. | Taxa que zera o VPL | bisseção; aviso se houver mais de uma troca de sinal | F03 | Decidido v0 |
| Payback simples | anos | Quando o acumulado vira positivo | acumulado com fração; **estendido** pelo regime além do horizonte e marcado | ZAIOS | Proposto como padrão (D8) |
| Payback descontado | anos | Idem com fluxos descontados | só dentro do horizonte | ZAIOS | Decidido v0 |
| Payback simplificado | anos | Atalho sem rampa | investimento ÷ resultado anual | A09 | Proposto (rótulo obrigatório) |
| Retorno anual | % a.a. | Resultado de um ano sobre o investimento | resultado (ou geração) do regime ÷ investimento | ZAIOS, A09 | **Proposto (D1)**: substitui "ROI" sem qualificador |
| Retorno acumulado em 10 anos | % | Ganho total sobre o investimento no horizonte | (Σ fluxos 1–10 + saída − investimento) ÷ investimento | B08 | **Proposto (D1)** |
| Valor de saída | R$ | Valor estimado de venda do ativo no fim do horizonte; **sempre mostrado à parte** | múltiplo × EBITDA do regime | Referência Zion 6× (ajustável) | **Divergente (D7)**: o B08 usa % do investimento |
| Cenários | — | Variações de diária e ocupação | conservador: diária −10%, ocupação −20%; otimista: +10%, +15% | ZAIOS | Proposto como referência (D10) |
| Regra de decisão Zion | — | 5 passos: geração ≥ 0; conservador aguenta até 3 meses de fixo; payback ≤ 8 (passa), ≤ 12 (ajustar); VPL sem saída ≥ 0; colchão ≥ 10% do CAPEX | — | F03, ZAIOS | Decidido v0 (D11: ferramentas simples mostram "sinal", não veredito) |

## 7. Rótulos obrigatórios em qualquer ferramenta

- **"Cenários, não promessas."** junto de qualquer projeção.
- **"Referência Zion (ajustável)"** junto de cada referência, com a versão do dicionário.
- **"Resultado antes da sua retirada"** quando a ferramenta não tiver retirada.
- **"Valor de saída: estimativa, mostrada à parte"** quando houver.
- **"Exemplo com dados fictícios"** em exemplos.
- Nunca "retorno garantido", "renda passiva", "captação assegurada", "acesso a investidores".

## Registro de versões

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 09/11/2026 | Proposta inicial (Comando 05B), a partir da ZAIOS v0, da Folha Única J2, de B06, B08, A09 e F05 |
