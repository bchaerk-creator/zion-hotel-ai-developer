# Auditoria de conversão · Raio-X do Terreno e Zion Glamping Store

Data: 29/10/2026 · Páginas: `docs/raio-x/index.html` e `docs/store/index.html` (versão da `main`, commit `e45c74a`)
Método: skills `cro` (conversão da página) e `offers` (força da oferta).

---

## Resumo

As duas páginas já têm o que a maioria não tem: números próprios de operação (R$ 400 mil por cabana, 60% de ocupação, diária de R$ 1.571), notas públicas (Booking 9,6, Airbnb Superhost), um fundador com currículo verificável e avisos legais bem feitos. A base é boa.

O que mais trava a venda hoje:

1. **Quatro promessas que a página não cumpre** (botão de pagamento que vai para o WhatsApp, vídeo "em produção", botão sem link, link possivelmente quebrado). Isso derruba a confiança justamente no momento da compra.
2. **Na Store, o preço fica atrás de um formulário de 13 campos.** O texto diz "1 minuto", mas leva bem mais que isso.
3. **A oferta não tem reversão de risco nem bônus.** Só aparece a garantia do fabricante. A "condição exclusiva até 30/11" é real, mas não diz qual é a condição.
4. **Falta prova de cliente.** Todo o argumento é a operação da própria Zion. Não há nenhum comprador de Bubble nem aluno da Trilha 1 falando.

---

## 1. Correções urgentes (promessas quebradas)

> **Situação em 29/10:** 1.1 e 1.2 já estavam resolvidos na `main` (links do Asaas e trailer publicado). 1.3 e 1.5 foram corrigidos no commit `5d0f6fd`. Falta conferir 1.4 no site publicado.

| # | Página | Problema | Correção |
|---|---|---|---|
| 1.1 | Raio-X | `checkoutTrilha` e `checkoutCombo` estão vazios no `CONFIG`, então os botões "Trilha 1 · R$ 270" e "Pacote · R$ 890" abrem o WhatsApp. Logo abaixo, o texto diz **"Pagamento seguro. A Trilha 1 abre na hora"**. Quem clica para pagar cai numa conversa. | Colocar os links de pagamento no `CONFIG`. Enquanto não existirem, trocar o texto por "Você recebe o link de pagamento no WhatsApp". |
| 1.2 | Raio-X | O botão do topo "▶ Por que fazer o Raio-X · 1 min 40" abre uma caixa que diz **"O vídeo do Bruno entra aqui. Em produção"**. É o primeiro clique de muita gente. | Esconder o botão enquanto `CONFIG.video` estiver vazio. |
| 1.3 | Store | "Falar com a equipe Zion" (seção 27) tem `href="#"` e só ganha um link depois que o formulário é enviado. Antes disso, o clique abre uma aba nova da mesma página. | Definir um link padrão de WhatsApp no HTML. |
| 1.4 | Store | O link "veja o passo a passo…" aponta para `/aula-marco-zero`, uma rota que não existe neste repositório. A aula está em `docs/escola/marco-zero/`. | Conferir no site publicado e, se der erro, apontar para o caminho certo. |
| 1.5 | Raio-X | O texto do topo diz **"Você chegou pela Bubble"** para todo mundo, inclusive para quem vem do Método 360, do Instagram do Bruno ou de anúncio. | Usar o texto da Bubble só quando `utm_source` ou o referrer vierem da Store. Para os demais visitantes, usar "Em poucos minutos, o Raio-X mostra o modelo de hospedagem que combina com a sua região e o seu momento". |

---

## 2. Store · Diagnóstico

**Tipo:** página de produto de valor alto, com venda consultiva pelo WhatsApp (Zaya).
**Meta principal:** formulário de orçamento enviado.

### O que funciona
- O título da seção 04, **"Uma única cabana. Quase R$ 400 mil por ano."**, é o argumento mais forte do site.
- O bloco "O que a Bubble é / não é" filtra o cliente errado antes de ele chegar à Zaya.
- As objeções de calor, durabilidade, energia, limpeza e preservação estão todas respondidas, com dados concretos.
- O "exercício do pneu" e a calculadora de faturamento fazem o visitante usar os próprios números, o que gera compromisso.
- O prazo de 30/11 é real, com data.

### O que trava

**a) O formulário de orçamento (maior atrito).** São 13 campos obrigatórios: situação, nome, WhatsApp, e-mail, cidade, estado, modelo, unidades, terreno, infraestrutura, prazo, LGPD e uma mensagem opcional. A promessa é "Preencha em 1 minuto". Metade desses dados a Zaya consegue perguntar na conversa.
→ **Deixar só 5 campos:** nome, WhatsApp, cidade/estado, modelo e unidades, mais o aceite da LGPD. Os demais vão para a primeira mensagem da Zaya. A pergunta "situação" pode virar um campo opcional.

**b) O preço não aparece em lugar nenhum.** Quem não quer conversar com vendedor sai sem número. Como a página já traz os números de deck, FF&E (R$ 25.915) e piso, falta só a âncora da bolha.
→ **Testar "A partir de R$ X à vista até 30/11"** perto do botão. Se a decisão for não mostrar preço, ao menos dizer o que o orçamento inclui ("o valor da bolha + a estimativa do projeto completo"), o que já está no FAQ e pode subir para o lado do botão.

**c) A "condição exclusiva" não diz o que é.** "Preço especial à vista" não convence ninguém a agir antes de 30/11.
→ Escrever a condição: o desconto em %, o frete incluso, um bônus ou o que for real. Exemplo: "Até 30/11: X% à vista e a Trilha 1 de bônus".

**d) Excesso de saídas.** Ao longo da página, o visitante é chamado para o orçamento, o Raio-X, a Trilha 1, a Cápsula, a equipe Zion e a aula do Marco Zero. Na Store, o objetivo principal é o orçamento.
→ Manter o orçamento como botão dourado em todo lugar e deixar o Raio-X como link secundário ("Ainda não sabe se o terreno está pronto?"). Tirar a Trilha 1 da Store ou deixá-la só no fim.

**e) Nenhuma prova de cliente.** Todo o argumento é "nós operamos". O visitante pensa: "e quem comprou de vocês?".
→ 2 ou 3 depoimentos de compradores da Bubble, com nome, cidade, foto da bolha instalada e um número (meses até abrir, ocupação). Colocar logo antes do formulário.

---

## 3. Raio-X · Diagnóstico

**Tipo:** quiz de diagnóstico (isca de leads) que leva a uma escada de ofertas: Trilha 1 (R$ 270), Pacote 4 trilhas (R$ 890), mentoria em grupo, mentoria individual e estruturação pela Zion.
**Meta principal:** quiz concluído, com o lead enviado para `/api/public/raio-x-lead`.

### O que funciona
- O título **"Antes do preço, descubra o que o seu terreno pede."** é claro e posiciona a Zion como quem orienta, e não só vende.
- A opção "não sei" ("isso também é diagnóstico") reduz o medo de errar.
- A leitura do resultado muda conforme as respostas (5 leituras) e termina com "Por onde começar".
- A qualificação por investimento manda cada lead para a oferta do tamanho certo. É a melhor peça de vendas do site.
- "O Raio-X é a página zero do seu Dossiê" cria continuidade com a Trilha 1.

### O que trava

**a) O contato é pedido logo na pergunta 1.** O visitante ainda não recebeu nada e já precisa dar nome, WhatsApp e e-mail. É o ponto onde quizzes costumam perder mais gente.
→ **Teste A/B:** passar o contato para depois da pergunta 8 ("Para te mandar o seu Raio-X, onde enviamos?"). Quem já respondeu 8 perguntas raramente abandona na nona. O envio do lead já acontece só no resultado, então a mudança não perde nenhum dado.

**b) São 12 etapas no total** (9 perguntas mais 3 de qualificação). "Em poucos minutos" é verdade, mas a barra só mostra "de 9" e depois aparecem mais 3.
→ Mostrar "Pergunta X de 12" desde o começo, ou fundir `situacao` com `dor`, que se sobrepõem em parte.

**c) A oferta de R$ 270 não tem garantia nem bônus.** Pelo Código de Defesa do Consumidor (art. 49), toda compra online já tem 7 dias de arrependimento. A Zion pode transformar essa obrigação em argumento.
→ Escrever ao lado do botão: **"7 dias de garantia: se não for para você, devolvemos 100%."**
→ Bônus barato de entregar e coerente com o método, por exemplo um encontro ao vivo mensal de dúvidas com o Bruno ou a revisão por escrito da página do Raio-X no Dossiê.

**d) O Pacote de R$ 890 vende trilhas que ainda não existem.** "As Trilhas 2, 3 e 4 entram conforme forem lançadas" soa como risco para o comprador.
→ Apresentar como **pré-venda com preço de fundador**, com um prazo real ("R$ 890 até a Trilha 2 abrir; depois, R$ X"). Assim a incerteza vira motivo para comprar agora, e sem urgência falsa.

**e) Nenhuma prova social.** A seção "Quem está por trás" é forte, mas fala só do Bruno.
→ Um depoimento de aluno ou mentorado perto do resultado ("Fiz o Raio-X, comecei pela Trilha 1 e hoje…") ou o número real de Raio-X já feitos.

---

## 4. A oferta pela equação de valor

Notas de 1 a 10. A nota mais baixa é a que mais limita a venda.

| Alavanca | Bubble (Store) | Trilha 1 (Raio-X) |
|---|---|---|
| Resultado sonhado | 9 · "R$ 400 mil por cabana" | 7 · "Dossiê para levar a banco, sócio ou à Zion" |
| Chance percebida de dar certo | 6 · prova só da Zion, nenhum cliente | 5 · nenhum aluno, nenhuma garantia |
| Tempo até o resultado | 7 · "até 90 dias com o deck pronto" | 6 · o tempo para concluir a trilha não é dito |
| Esforço do cliente | 5 · deck, luz, água, esgoto e móveis por conta dele | 7 · online, no ritmo dele |

**O gargalo nas duas é a chance percebida de dar certo.** A correção é a mesma: prova de cliente e garantia. Para a Bubble, também vale reduzir o esforço. Um "kit de implantação" (checklist do deck, lista de fornecedores parceiros, uma videochamada com a equipe antes da obra) como bônus da condição até 30/11 ataca o esforço sem mexer no preço.

---

## 5. Alternativas de texto

**Título da Store** (atual: "Transforme seu terreno em um destino turístico com os produtos da Zion.")
1. "A cabana que fatura quase R$ 400 mil por ano na Zion. Agora no seu terreno." · Começa pelo número mais forte, que hoje só aparece na seção 04.
2. "Hospede dentro da mata, onde uma casa não entraria. Operando em até 90 dias." · Destaca a vantagem única (área sem uso) e o prazo.
3. "As cabanas de glamping que a Zion opera há 5 anos, com nota 9,6 no Booking." · Começa pela prova, para o público que desconfia.

**Botão da Store** (atual: "Receber o valor e a condição")
1. "Ver o preço da minha Bubble no WhatsApp"
2. "Quero o valor e a condição até 30/11"

**Título do Raio-X** (atual: "Antes do preço, descubra o que o seu terreno pede.") · O atual é bom. Alternativa para testar:
1. "Descubra em 5 minutos se o seu terreno pode virar hospedagem, e por onde começar."

---

## 6. Ideias de teste A/B (em ordem)

1. **Raio-X:** contato na pergunta 1 contra contato no fim. Métrica: quizzes concluídos por visitante.
2. **Store:** formulário de 13 campos contra 5 campos. Métricas: formulários enviados e o percentual que a Zaya qualifica.
3. **Store:** sem preço contra "a partir de R$ X". Métricas: formulários enviados e taxa de fechamento (não só leads).
4. **Raio-X:** botão da Trilha 1 sem garantia contra "7 dias de garantia". Métrica: compras por resultado exibido.

O tráfego das duas páginas ainda é pequeno, então rode um teste por vez e por pelo menos duas semanas.

---

## 7. O que preciso de você para a próxima etapa

- O link de pagamento da Trilha 1 e do Pacote (item 1.1).
- Qual é, de fato, a condição até 30/11 (desconto, frete, bônus).
- Se existe o preço "a partir de" que pode aparecer na Store.
- 2 ou 3 clientes da Bubble e 1 ou 2 alunos ou mentorados que topem dar depoimento.
- Os números atuais, se houver: visitas, quizzes concluídos, formulários enviados e vendas.
