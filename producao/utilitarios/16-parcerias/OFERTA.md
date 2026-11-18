# Ferramenta 16 · Kit Operacional de Parcerias

Status: arquivos prontos e testados. **Oferta enviada para aprovação em 17/11/2026** na rodada diária automática. **Oferta aprovada e página publicada em 18/11/2026.**

**ClickMax:**
- produto `f106fa17-e00d-4af9-81a6-afa170a2e67b`;
- oferta `eca8f010-c236-4c55-ab0e-5db125661687` (R$ 19, checkout `pAGdV-2yw1`), com status `pending` desde 17/11 às 04h55 UTC e sem erro de sincronização;
- página `ba973c0c-9dd5-4f47-b22d-3475d469000d` em `/kit-parcerias` (publicada em 18/11).

Entrega: 4 arquivos e a página de acesso, em `docs/p/adbc67069af26ae0/parcerias-16/`, ligados à oferta.

**Por que a 16 nesta rodada:** 01, 21 e E08 aguardam decisão de Bruno, e E05 e E06 aguardam os PDFs A01 a A10. A 16 é a próxima ferramenta "A fazer" da lista.

**Sobreposição verificada:** nenhum produto existente organiza parceiros locais, acordos e comissões. Não há alegação de que o kit vem da rotina das unidades da Zion. Nenhuma regra fiscal ou jurídica é apresentada como fato: a ficha não é contrato, e imposto é assunto do contador.

## 1. Tarefa concreta
Registrar com quais parceiros a hospedagem trabalha (restaurantes, guias, spas, transportes), o que foi combinado com cada um e as indicações feitas. Com isso, a planilha mostra o que falta confirmar, o que há para receber e quando um acordo precisa ser revisto.
- **Evidência:** item 16 do Catálogo. Nenhuma pesquisa de mercado e nenhum número externo.

## 2. Promessa
"Aprenda o passo a passo para organizar as parcerias da sua hospedagem: o que cada parceiro oferece, o que foi combinado, as indicações feitas e o que você tem a receber."
- Tempo para começar: cerca de 20 minutos para cadastrar os parceiros que você já indica.
- Os pagamentos dependem dos parceiros. O material é educativo: não substitui contrato nem contador.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Parcerias-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Parceiros (40), Indicações (300, pelo código da reserva, sem dados pessoais) e Painel |
| `Parcerias-Zion-EXEMPLO.xlsx` | 5 parceiros fictícios: 3 ativos, 1 sem acordo por escrito e 1 com revisão vencida. 10 indicações, das quais 8 são válidas e 2 têm problema. R$ 96 a receber e R$ 63 recebidos |
| `Ficha-de-Acordo-com-Parceiro.pdf` | Uma página para registrar o combinado com cada parceiro |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, exercícios, critérios, checklist e limitações |
| `demonstracao/` | Telas de Parceiros e Indicações |
| `Ferramenta16-Parcerias-Zion.zip` | Pacote completo |

### Regras da planilha
**Situação do parceiro**, na ordem em que a planilha confere:
1. Escolha o tipo
2. Escolha a contrapartida
3. Confira o valor da contrapartida (% entre 0 e 99, valor fixo maior que 0)
4. Sem acordo por escrito
5. Revisar o acordo (data de revisão igual ou anterior a hoje)
6. Ativa

**Comissão:** % × valor gasto, ou o valor fixo. Troca e nenhuma contrapartida não geram comissão.

**Situação da indicação**, na ordem em que a planilha confere:
1. Informe a data
2. Parceiro não cadastrado
3. Complete o cadastro do parceiro
4. Confira o valor gasto
5. Informe o valor gasto (quando a contrapartida é %)
6. Aguardando confirmação
7. Sem comissão
8. Recebido
9. A receber

O valor fica em texto fixo, sem TEXT() com "R$", para não depender do idioma da planilha.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **26 de 26**.
- **O que é comparado** com uma regra independente em Python: situação e totais de cada parceiro, comissão e situação de cada indicação, o Painel e a leitura "o que fazer agora".
- **Cenários:**
  - o exemplo e a versão em branco;
  - 8 cenários aleatórios com erros e 4 limpos;
  - casos de borda: revisão no dia exato, 99% versus 100%, tudo em dia, só cobrar, só confirmar, sem parceiros.
- Nenhuma célula com erro em 20 arquivos.
- Revisão visual do guia, da ficha, das telas, da capa e da página no celular (390 px, sem rolagem lateral).

**Não testado:** Excel e Google Sheets reais, celular de verdade e compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "Você indica. Mas quem lembra do combinado?"
- **Colapso de crença:** "parceria é só indicar". Parceria de boca some no mês seguinte.
- **Reencadramento:** de favor solto para acordo escrito, indicação registrada e cobrança mensal.
- **Inevitabilidade:** parceiro + acordo + indicação pelo código da reserva + conferência mensal = nada fica para depois.
- **Resultado educacional:** você aprende a registrar acordos, acompanhar indicações e conferir comissões.

Botão: "Quero o kit de parcerias" · R$ 19, pagamento único, reembolso em 7 dias.

## 6. Perguntas frequentes
- Não é preciso cobrar comissão: dá para marcar troca ou nenhuma contrapartida.
- A ficha não é contrato.
- Não anote o nome do hóspede, use o código da reserva.
- Imposto é com o contador.
- Funciona no celular.

## 7. Três anúncios
Formato 1080×1350, botão "Saiba mais", `utm_campaign=ferramenta16`.
1. **c16a · Combinado:** "Você indica. Mas quem lembra do combinado?" + tela de Parceiros (dados fictícios). Primeira linha: "Cada parceiro, cada acordo, num lugar só."
2. **c16b · A receber:** tela de Indicações. Primeira linha: "Comissão calculada pelo código da reserva."
3. **c16c · Ficha:** "Parceria de boca some no mês seguinte." Primeira linha: "Uma ficha de acordo para imprimir."

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
17/11/2026, rodada diária:
- os 4 arquivos e a página de acesso foram conferidos no ar (status 200) e ligados à oferta;
- `offers_get_incomplete_reason` voltou vazio;
- a oferta foi enviada para aprovação e está `pending`, sem erro de sincronização.

## Publicação (18/11/2026)
Oferta aprovada (`status` approved, sem erro de sincronização). Página publicada e conferida: status 200 com título, reembolso e capa em https://infoprodutos-zion.clickmax.space/kit-parcerias. O checkout é um iframe bloqueado neste ambiente, então a compra não foi testada.
