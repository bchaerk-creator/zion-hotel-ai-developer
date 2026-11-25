# Order bump, upsell e downsell · estudo curto para a Mini Mentoria R$ 47

Agente: FUNNEL · 25/11/2026. **Estudo. Nada foi configurado, ativado ou testado em produção.** Marcação: **[E]** evidência (documentação do ClickMax e leitura de ofertas feita agora), **[H]** hipótese, **[NC]** não confirmado, **[BRUNO]** precisa de validação de Bruno.

## 1. O que o ClickMax permite (documentação lida)

| Recurso | Como funciona [E] | Aplicável ao nosso caso |
|---|---|---|
| **Order bump** | Aparece dentro do checkout, antes de pagar. Configurado no Editor de Checkout: selecionar o produto, ativar Order Bump, escolher o produto adicional, salvar. Só aparece se a oferta estiver aprovada e publicada. Existem as ferramentas `checkouts_set_order_bump` e `insights_order_bump_attach` | Possível em tese. **[NC]** se o bump aparece no checkout **embutido** (iframe `payments.clickmax.io/custom/<pageId>/<hash>`) de uma página de venda comum. Não consigo ver o checkout daqui (domínio bloqueado). Precisa de teste por Bruno |
| **Upsell** | Página extra do **funil**, exibida depois do pagamento aprovado, ligada como próxima etapa do checkout. A compra com um clique exige que a oferta principal use o checkout do ClickMax e que checkout e upsell estejam no mesmo domínio | A `/mini-mentoria` é página de venda com checkout embutido, **sem funil ligado** [NC: não confirmei se existe funil para ela]. Upsell exigiria montar um funil novo com checkout + upsell + obrigado |
| **Downsell** | Página do funil exibida quando o cliente recusa o upsell | Mesma condição do upsell |
| **Compra com um clique** | Vale para quem pagou com **cartão** no mesmo navegador; quem paga com Pix paga a oferta pelo formulário da página | **Maioria dos compradores paga por Pix** [H, é o padrão de baixo ticket]; o ganho de um clique se perde para eles |
| **Reembolso** | "O reembolso cancela a venda inteira, incluindo order bumps; não dá para reembolsar itens separadamente" | Se o comprador pedir reembolso da Mini Mentoria, perde também o bump. Aumenta o risco de reembolso se o complemento for percebido como empurrado |
| **Páginas pós-compra** | Devem ser protegidas contra acesso direto (Configurações do Funil → Redirecionamentos) | Obrigatório se houver página de upsell |
| **Gatilhos de página** | O mapa de gatilhos da `/mini-mentoria` lista `upsell_accepted`, `upsell_declined`, `downsell_accepted`, `downsell_declined` [E] | Confirma que o mecanismo existe no ClickMax, não que esta página o use |

Limite técnico direto: bump e upsell dependem de **checkout do ClickMax**. Aqui o gateway por trás é a Ticto, mas o checkout é o nativo embutido [E], então o requisito parece atendido; o comportamento no iframe é [NC] até o teste.

## 2. Alternativas viáveis (da mais simples para a mais complexa)

1. **E-mail de oferta complementar depois da compra aprovada** (e, se aprovado, WhatsApp). Não depende de checkout. O comprador já está dentro da plataforma, já pagou e já recebeu o acesso. Enviar **depois** do primeiro acesso ou de uma semana de uso, não no minuto da compra. Risco menor e mede-se por vendas do produto complementar. Ligar só com "aprovado" **[BRUNO]**.
2. **Bloco "Para continuar" dentro do portal** (aula ou material de fechamento no final do Pilar 7, com link para a página do produto complementar). Não é anúncio no meio do curso; aparece quando o aluno chegou ao ponto em que o complemento faz sentido. Edita-se conteúdo do portal (`lessons_*`/`content_*`): **mexe na turma, precisa de "aprovado"** **[BRUNO]**.
3. **Página de oferta pós-compra** (página nova em funil, depois da compra): exige funil novo e teste do caminho completo; só se o teste do bump (alternativa 4) for inconclusivo.
4. **Order bump no checkout**: testar primeiro em **oferta de teste** (não na `0c71eeba`). Precisa de um teste real de compra feito por Bruno com Pix e com cartão. Só depois decidir.
5. **Upsell/downsell em funil**: última opção; maior custo de montagem, e o ganho de um clique não vale para Pix.

Recomendação [H]: começar pela **alternativa 1** (e-mail pós-primeiro-acesso), medir, e só depois testar o bump.

## 3. Candidatos (somente produtos que já existem)

Critério de pertinência: o complemento resolve o problema **imediatamente seguinte** ao que a Mini Mentoria resolve, custa bem menos que o principal, não repete o que o aluno já recebeu e **não promete** o que as regras proíbem. Públicos: quem tem terreno e quer estruturar um empreendimento turístico.

| Candidato | Preço [E] | Entrega [E] | Pertinência | Risco de canibalização | Observações |
|---|---|---|---|---|---|
| **Ferramenta 05 · Orçamento da Cabana** (`a09778db`, `/orcamento-cabana`) | R$ 19 | Arquivo (planilha em branco, exemplo fictício, guia, ficha de cotação) + página de acesso | **Alta.** Próximo passo concreto de quem estrutura uma cabana: orçar. Descrição já é honesta ("não informa preços de mercado nem garante custo de obra") | Baixa a média: a Mini Mentoria já entrega "2 planilhas de cálculo em branco" [E]. Conferir se não é o mesmo conteúdo antes de oferecer | Entrega por arquivo e e-mail (independe de portal) |
| **E-book "Qual Cabana para o Meu Terreno?" + Kit** (`add69459`, `/ebook-qual-cabana`) | R$ 13 | Área de membros do portal **antigo** Zion Collection (turma `0fb67ceb`) | Média a alta: comparar modelos antes de decidir | Média: a Mini Mentoria tem "e-books por pilar" | **Atrito:** entrega em portal diferente do da Mini Mentoria (segundo acesso). Texto menciona "payback" no kit: conferir se não vira promessa |
| **E-book "Terreno Parado, Projeto com Sócio" + Kit** (`3852a88a`, `/ebook-terreno-parado-socio`) | R$ 13 | Portal antigo (turma `d3bdb859`) | Tema próximo (capital e sócio) | **Alta com o Pilar 7 (capital) e com o Kit do Investidor** da Mini Mentoria | **Risco de promessa:** a descrição diz "atrair um sócio, investidor ou parceiro... mesmo sem capital". Contraria "sem promessa de investimento e parceria". **Não usar sem revisar o texto** |
| **E-book "Do Terreno ao Airbnb" + Kit** (`/ebook-do-terreno-ao-airbnb`, oferta começa em `0afcefb4`) | [NC] não consegui ler a oferta com o id que usei (erro "não encontrada"); conferir o id pela página | [NC] | [NC] | [NC] | Conferir antes de qualquer decisão |
| **Ferramenta 29 · Calculadora de Custos de Experiências** (`a52ce33e`) | R$ 19 [E, CLAUDE.md] | Arquivo | Média, só para quem já pensa em experiências além da hospedagem | Baixa | Público mais "operador" que "terreno" [H] |
| **Produto "Você tem terra. Falta capital?" (terra-capital)** | R$ 47 (A) e R$ 67 (B) [E, CLAUDE.md] | Portal próprio, guia 60 p., 20 microaulas, 10 ferramentas | Tema muito próximo (capital) | **Alta:** repete o Pilar 7 da Mini Mentoria e custa o mesmo | **Não usar como complemento.** É produto concorrente, não complemento |
| **Zion Collection 06 · Seu Airbnb Está Vazio?** | R$ 47 [E] | Portal Zion Collection | Baixa: público é quem já opera hospedagem, não quem tem terreno | Baixa | Não pertinente |
| **Ferramentas R$ 19 de operação** (limpeza, mensagens, enxoval, manutenção, etc.) | R$ 19 | Arquivo | Baixa agora: servem a quem já tem hospedagem funcionando | Baixa | Podem entrar **mais tarde** na sequência, para quem avança para operar |

Escolha provisória [H, [BRUNO]]: **Ferramenta 05 (Orçamento da Cabana)** como primeiro complemento, por entrega simples (arquivo + página de acesso), preço baixo e pertinência alta; conferir antes a sobreposição com as planilhas em branco da Mini Mentoria. O e-book "Qual Cabana" é o segundo, depois de resolver o atrito do portal antigo.

## 4. Regras para qualquer complemento
- Sem "de/por" falso, sem bônus inventado, sem urgência falsa. Preço sempre visível.
- Não oferecer no mesmo e-mail do acesso. Primeiro entregar, depois oferecer.
- Quem pediu reembolso da Mini Mentoria **não recebe** oferta complementar.
- Cada oferta complementar leva UTM própria para medir (mesmo `utm_campaign=mm47` do padrão `09-tracking/PADRAO_UTM.md`, com `utm_content=complemento-<oferta>` para separar).
- Medir efeito real: ticket médio **e** número de pedidos, como recomenda a documentação do ClickMax. Se o bump derrubar a conversão da Mini Mentoria, desligar.

## 5. O que precisa de validação de Bruno
1. Teste de compra (Pix e cartão) para saber se o bump aparece no checkout embutido [NC].
2. Qual produto complementar (e se aceita o atrito do portal antigo para os e-books).
3. Revisão do texto do e-book "Terreno Parado..." antes de qualquer uso.
4. Permissão para editar conteúdo do portal (alternativa 2).
5. Permissão para ligar e-mail de oferta complementar após a compra.
