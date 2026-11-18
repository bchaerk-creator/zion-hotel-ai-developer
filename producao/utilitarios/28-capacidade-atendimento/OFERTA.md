# Ferramenta 28 · Planner de Capacidade e Atendimento

Status: arquivos prontos e testados. **Oferta enviada para aprovação em 18/11/2026** na rodada diária automática. A página fica em rascunho até a oferta estar ativa.

**ClickMax:**
- produto `0cf14c74-2d04-449c-ba9c-ddf689359d9b`;
- oferta `2f851e16-746d-44e6-8448-a33c4cba92ae` (R$ 19, checkout `rcTdhslLRC`), com status `pending` desde 18/11 às 04h56 UTC e sem erro de sincronização;
- página `4a1b7c4c-6c59-4d30-bb15-726754360ae9` em `/capacidade-atendimento` (rascunho).

Entrega: 4 arquivos e a página de acesso, em `docs/p/adbc67069af26ae0/capacidade-28/`, ligados à oferta.

**Por que a 28 nesta rodada:** 01, 21 e E08 aguardam decisão de Bruno, e E05 e E06 aguardam os PDFs A01 a A10. A 28 é a próxima ferramenta "A fazer" da lista.

**Sobreposição verificada:**
- A Ferramenta 29 calcula custo, preço e o mínimo de participantes em dinheiro. A 28 recebe o mínimo como regra pronta e cita a 29 como produto separado.
- A Ferramenta 30 escreve o briefing da experiência. A 28 cuida de capacidade, equipe e agenda.

Não há alegação de que o planner vem da rotina das unidades da Zion. Nenhuma regra de segurança ou proporção de condutores é apresentada como fato: quem define é o comprador.

## 1. Tarefa concreta
Planejar cada saída de uma experiência com horário marcado (trilha, passeio, aula, café especial): se cabe, se há condutores suficientes, se atingiu o mínimo, até quando decidir e o que fazer com a lista de espera.
- **Evidência:** item 28 do Catálogo. Nenhuma pesquisa de mercado e nenhum número externo.

## 2. Promessa
"Aprenda o passo a passo para planejar as saídas das suas experiências: quantas pessoas cabem, quantos condutores escalar, quando confirmar ou cancelar e o que fazer com a lista de espera."
- Tempo para começar: cerca de 20 minutos para cadastrar as experiências e duas semanas de saídas.
- Procura e reservas não dependem da planilha.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Capacidade-Atendimento-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Experiências (20), Saídas (200, só quantidades, sem dados pessoais) e Painel |
| `Capacidade-Atendimento-Zion-EXEMPLO.xlsx` | 4 experiências e 11 saídas fictícias, hoje = 20/11. Aparecem as situações: lotada com espera, falta condutor, decida, abaixo do mínimo, acima da capacidade, confirmada, lotada e já passou, mais 2 saídas com problema. Nos próximos 7 dias: 50 pessoas e 10 condutores |
| `Ficha-de-Saida.pdf` | Uma página: dados da saída, checklist antes de sair, participantes pelo código da reserva, contagem na saída e na volta, ocorrências |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist e limitações |
| `demonstracao/` | Telas de Saídas e Painel |
| `Ferramenta28-Capacidade-Atendimento-Zion.zip` | Pacote completo |

### Regras da planilha
**Cálculos:**
- condutores necessários = reservadas ÷ pessoas por condutor, arredondado para cima;
- vagas = capacidade − reservadas;
- ocupação = reservadas ÷ capacidade;
- decidir até = data − dias de antecedência.

**Situação da experiência**, na ordem em que a planilha confere:
1. Confira a capacidade (inteiro ≥ 1)
2. Confira pessoas por condutor (inteiro ≥ 1)
3. Confira o mínimo (inteiro ≥ 0 e ≤ capacidade; vazio = 0)
4. Confira a antecedência (inteiro ≥ 0; vazio = 0)
5. Pronta

**Situação da saída**, na ordem em que a planilha confere:
1. Informe a data
2. Experiência não cadastrada
3. Complete a experiência
4. Confira os reservados, Confira os condutores, Confira a lista de espera (inteiros ≥ 0)
5. Já passou (data anterior a hoje)
6. Acima da capacidade
7. Falta condutor
8. Abaixo do mínimo, que vira "Decida: confirmar ou cancelar" a partir da data de decisão
9. Lotada, com lista de espera, ou Lotada
10. Confirmada

**Painel:** a janela dos próximos 7 dias vai de hoje até hoje + 6. "Condutores necessários" soma as saídas.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **29 de 29**, todos já na primeira execução.
- **O que é comparado** com uma regra independente em Python: situação de cada experiência e saída, capacidade, vagas, condutores, ocupação, data de decisão, os totais por experiência, as 14 linhas do Painel e a leitura "o que fazer agora".
- **Cenários:**
  - o exemplo e a versão em branco;
  - 8 cenários aleatórios com erros e 4 limpos (até 80 saídas cada);
  - casos de borda: prazo no dia exato, condutor no limite, lotada e acima, hoje e ontem, limite dos 7 dias, tudo em dia, só experiências, sem experiências.
- **Contas do exemplo conferidas à mão:**
  - 50 pessoas = 12 + 14 + 2 + 3 + 8 + 11;
  - 10 condutores = 2 + 2 + 1 + 1 + 1 + 3;
  - café com 14 pessoas pede 2 condutores, barco com 11 pede 3.
- Nenhuma célula com erro em 22 arquivos.
- Revisão visual do guia, da ficha, das telas, da capa e da página no celular (390 px, sem rolagem lateral). Um ajuste feito: as etiquetas de situação esticavam na demonstração.

**Não testado:** Excel e Google Sheets reais, celular de verdade e compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "Lotou demais, faltou guia ou saiu com duas pessoas?"
- **Colapso de crença:** "a agenda cabe na cabeça", até o dia em que não cabe.
- **Reencadramento:** de resolver na hora para regras escritas uma vez e aplicadas em todas as saídas.
- **Inevitabilidade:** regras + saídas com números + situação de cada uma = nenhuma surpresa na véspera.
- **Resultado educacional:** você aprende a definir capacidade, equipe, mínimo e prazo, e a ler o que cada saída pede.

Botão: "Quero o planner" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho; cita a Ferramenta 29 como produto separado.

## 6. Perguntas frequentes
- A planilha não diz o que é seguro: quem define é você.
- Não calcula preço (veja a Ferramenta 29).
- Não use nomes de participantes, só quantidades.
- Não recebe reservas nem avisa participantes.
- Funciona no celular.

## 7. Três anúncios
Formato 1080×1350, botão "Saiba mais", `utm_campaign=ferramenta28`.
1. **c28a · Lotou:** "Lotou demais, faltou guia ou saiu com duas pessoas?" + tela de Saídas (dados fictícios). Primeira linha: "Cada saída no tamanho certo."
2. **c28b · Semana:** tela do Painel. Primeira linha: "Quantas pessoas e quantos condutores a semana pede."
3. **c28c · Decida:** "Confirmar ou cancelar? Decida no prazo." Primeira linha: "O mínimo e a data de decisão de cada saída."

## 8. Preço, custos e entrega
- **Preço:** R$ 19.
- **Custos por venda:** taxa do checkout, impostos e reembolsos.
- **Entrega:** 4 arquivos e a página de acesso. Manutenção baixa.
- **Indicadores:** visitas à página, conversão do checkout, reembolsos e custo por venda (quando houver anúncio aprovado).

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

## Envio para aprovação
18/11/2026, rodada diária:
- os 4 arquivos e a página de acesso foram conferidos no ar (status 200) e ligados à oferta;
- `offers_get_incomplete_reason` voltou vazio;
- a oferta foi enviada para aprovação e está `pending`, sem erro de sincronização.
