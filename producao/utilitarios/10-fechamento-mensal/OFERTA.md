# Ferramenta 10 · Fechamento Mensal por Imóvel

Status: arquivos prontos e testados. **Oferta enviada para aprovação em 19/11/2026** na rodada diária automática. **Oferta aprovada e página publicada em 20/11/2026.**

**ClickMax:**
- produto `2446ba99-5aea-4202-945f-1db04c8ced80`;
- oferta `2e335c78-25a4-411d-8f81-380b692f5648` (R$ 19, checkout `2BpmmqQLeG`), com status `pending` desde 19/11 às 04h55 UTC e sem erro de sincronização;
- página `e150beeb-37a2-4527-833f-140c2c5c7711` em `/fechamento-mensal` (publicada em 20/11).

Entrega: 4 arquivos e a página de acesso, em `docs/p/adbc67069af26ae0/financeiro-10/`, ligados à oferta.

**Por que a 10 nesta rodada:**
- 01, 21 e E08 aguardam decisão de Bruno, e E05 e E06 aguardam os PDFs A01 a A10.
- 25, 26 e 27 (projeto, públicos A e C) se sobrepõem ao que já existe: as planilhas do Clube (abas Premissas e Viabilidade), o Kit de Captação, o kit do investidor (one-pager e apresentação), a ZAIOS F01 a F03 e a Linha B (B08). Por isso foram para a decisão de Bruno, como a 01.
- A 10 é do público B. O catálogo já diz o que ela precisa trazer além da Ferramenta 01: categorias, fechamento, conciliação e vários imóveis.

**Sobreposição verificada:**
- A Ferramenta 01 calcula a diária mínima e tem um resumo de reservas de um imóvel.
- A 19 controla as compras contra o orçamento.
- A 10 fecha o mês de vários imóveis: receitas por canal, despesas por categoria, despesas comuns divididas, conferência com o extrato e resultado mês a mês.

As duas outras ferramentas são citadas como produtos separados. Não há alegação de que a planilha vem da rotina das unidades da Zion, e nenhuma regra fiscal é apresentada como fato.

## 1. Tarefa concreta
Fechar o mês de cada imóvel: lançar o que entrou e saiu, dividir as despesas comuns, conferir tudo com o extrato e ver o resultado de cada imóvel e de cada mês.
- **Evidência:** item 10 do Catálogo. Nenhuma pesquisa de mercado e nenhum número externo.

## 2. Promessa
"Aprenda o passo a passo para fechar o mês de cada imóvel: o que entrou por canal, o que saiu por categoria, as despesas divididas entre os imóveis e o que ainda falta conferir no extrato."
- Tempo para começar: cerca de 30 minutos para lançar o mês passado com o extrato em mãos.
- Resultado do mês não é lucro, e a planilha não substitui o contador.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Fechamento-Mensal-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Cadastros (10 imóveis, 10 categorias prontas e até 20, 4 canais fixos), Lançamentos (500), Fechamento e Ano |
| `Fechamento-Mensal-Zion-EXEMPLO.xlsx` | 3 imóveis e 17 lançamentos fictícios, fechamento de outubro de 2026 (detalhado abaixo) |
| `Folha-de-Fechamento.pdf` | Roteiro do fechamento, resultado de cada imóvel e anotações (1 página) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist e limitações |
| `demonstracao/` | Telas de Lançamentos e Fechamento |
| `Ferramenta10-Fechamento-Mensal-Zion.zip` | Pacote completo |

**Exemplo, outubro de 2026:**

| Imóvel | Receitas | Despesas | Parte das divididas | Resultado |
|---|---|---|---|---|
| Apto | R$ 3.000 | R$ 1.140 | R$ 250 | R$ 1.610 |
| Casa | R$ 3.200 | R$ 1.150 | R$ 250 | R$ 1.800 |
| Chalé | R$ 2.380 | R$ 2.200 | R$ 250 | −R$ 70 |
| **Total** | | | | **R$ 3.340** |

As despesas divididas somam R$ 750. Há 2 lançamentos a conferir no extrato e 2 com problema: categoria "Jardinagem" não cadastrada e um valor escrito por extenso.

### Regras da planilha
**Situação do lançamento**, na ordem em que a planilha confere:
1. Informe a data
2. Escolha o imóvel
3. Imóvel não cadastrado
4. Escolha o tipo
5. Receita precisa de um imóvel (receita com "Todos")
6. Escolha o canal
7. Categoria não cadastrada
8. Confira o valor (zero, negativo ou texto)
9. A conferir no extrato (entra nas contas)
10. OK

**Cálculos:**
- despesa "Todos (dividir igual)" = valor ÷ imóveis cadastrados;
- resultado = receitas − despesas do imóvel − parte das divididas.

**Situação do imóvel no mês:** Sem lançamentos próprios, Confira N no extrato, Resultado negativo ou Fechado.

**O que fazer agora**, na ordem:
1. Informe o mês
2. Cadastre os imóveis
3. Corrija os lançamentos com problema
4. Confira no extrato
5. Lance o mês
6. Resultado negativo em N imóvel(is)
7. Mês fechado

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **29 de 29**.
- **O que é comparado** com uma regra independente em Python: situação de cada lançamento; receitas, despesas, divididas, resultado, a conferir e situação de cada imóvel; totais; receitas por canal; despesas por categoria; os 12 meses da aba Ano de cada imóvel; a leitura "o que fazer agora".
- **Cenários:**
  - o exemplo e a versão em branco;
  - 8 cenários aleatórios com erros e 4 limpos (até 120 lançamentos, imóvel em branco no meio da lista);
  - casos de borda: divisão por três, virada de mês, tudo fechado, resultado negativo, receita com "Todos", categoria acrescentada, mês sem lançamentos, sem imóveis.
- Contas do exemplo conferidas à mão. Nenhuma célula com erro em 22 arquivos.
- **Falha real encontrada e corrigida:** a aba Ano não descontava as despesas divididas. A fórmula lia o número de imóveis numa célula vazia da própria aba. Agora lê o número da aba Fechamento, e os 12 cenários aleatórios passaram a bater.
- Revisão visual do guia, da folha, das telas, da capa e da página no celular (390 px, sem rolagem lateral).

**Não testado:** Excel e Google Sheets reais, celular de verdade e compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "Quanto cada imóvel deixou este mês?"
- **Colapso de crença:** "se sobrou dinheiro na conta, o mês foi bom". O dinheiro entra misturado e o mês fecha no chute.
- **Reencadramento:** de olhar o saldo para fechar imóvel por imóvel, conferido com o extrato.
- **Inevitabilidade:** lançar + dividir + conferir = resultado de cada imóvel, mês a mês.
- **Resultado educacional:** você aprende a organizar receitas e despesas por imóvel, dividir o que é comum e conciliar com o banco.

Botão: "Quero fechar o mês" · R$ 19, pagamento único, reembolso em 7 dias.

## 6. Perguntas frequentes
- Não substitui o contador.
- Resultado não é lucro.
- Serve para 1 a 10 imóveis.
- Não puxa dados de plataformas nem do banco.
- Funciona no celular.

## 7. Três anúncios
Formato 1080×1350, botão "Saiba mais", `utm_campaign=ferramenta10`.
1. **c10a · Quanto deixou:** "Quanto cada imóvel deixou este mês?" + tela do Fechamento (dados fictícios). Primeira linha: "Cada imóvel com a sua conta."
2. **c10b · Extrato:** tela de Lançamentos. Primeira linha: "A planilha que bate com o banco."
3. **c10c · Divididas:** "Internet, contador, ferramenta: de quem é essa conta?" Primeira linha: "Despesas comuns divididas entre os imóveis."

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
19/11/2026, rodada diária:
- os 4 arquivos e a página de acesso foram conferidos no ar (status 200) e ligados à oferta;
- `offers_get_incomplete_reason` voltou vazio;
- a oferta foi enviada para aprovação e está `pending`, sem erro de sincronização.

## Publicação (20/11/2026)
Oferta aprovada (`status` approved, sem erro de sincronização). Página publicada; 404 nos primeiros segundos (propagação), depois status 200 com título, reembolso e capa em https://infoprodutos-zion.clickmax.space/fechamento-mensal. O checkout é um iframe bloqueado neste ambiente, então a compra não foi testada.
