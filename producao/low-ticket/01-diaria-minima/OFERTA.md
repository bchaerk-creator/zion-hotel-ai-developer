# Ferramenta 01 · Diária Mínima e Controle do Mês

Status: protótipo funcional testado. Nada foi publicado, ativado ou anunciado.

## Público e situação de uso
- **Quem:** anfitriões de aluguel por temporada com uma a poucas unidades (Airbnb, Booking ou reserva direta).
- **Quando:**
  - ao definir ou revisar a diária;
  - antes de dar desconto na baixa temporada;
  - no fim do mês, ao olhar o extrato.

## Promessa
"Aprenda o passo a passo para descobrir a menor diária que cobre seus custos e taxas, e saiba quanto sobrou no mês."
- **Tempo para começar a usar:** cerca de 10 minutos.
- **Resultado externo:** vender mais ou a um preço melhor depende do mercado e da época. A planilha não promete isso.

## Entregáveis
1. `Diaria-Minima-Zion-EM-BRANCO.xlsx`, para os números do comprador.
2. `Diaria-Minima-Zion-EXEMPLO.xlsx`, preenchido com dados fictícios identificados como exemplo.
3. Aba "Comece aqui", com o passo a passo, a legenda de cores, os avisos e as limitações.
4. Funciona no Excel, no Google Sheets (importando o arquivo) e no LibreOffice.

## O que a planilha calcula (com a memória do cálculo à vista)
- Diária mínima para empatar e diária para atingir a meta de sobra do mês.
- Taxa da plataforma e impostos sobre diárias e limpeza cobrada; limpeza paga por estadia; custos por noite; custos fixos.
- Simulador de desconto: quantas noites a mais um desconto exige para manter a margem.
- Registro de reservas com taxa por canal (Airbnb, Booking ou reserva direta com taxa 0).
- Resumo do mês: ocupação, diária efetiva, margem e sobra, comparando a diária efetiva com a mínima.

## Como conferir o resultado
- A linha "Conferência" mostra "Confere com a meta" quando a memória do cálculo fecha exatamente na meta.
- A "Situação dos dados" bloqueia o cálculo quando:
  - falta algum campo;
  - há valor negativo;
  - taxa e impostos somam 100%;
  - as noites do mês são zero ou passam de 31;
  - a estadia média é maior que as noites do mês.

## Testes executados (21 de 21 passaram)
O arquivo foi recalculado no LibreOffice e cada resultado foi comparado com uma conta independente em Python (`test_planilha.py`):
- diária mínima, diária da meta e memória do cálculo;
- simulador de desconto;
- margem por reserva e canal direto sem taxa;
- resumo do mês (reservas, noites, ocupação e sobra);
- versão em branco;
- os 6 bloqueios de dados inválidos;
- desconto que zera a margem.

## Limitações e dependências
- Não prevê a demanda e não traz preços da região.
- A taxa da plataforma é informada pelo comprador. O Airbnb tem modelos diferentes, por isso a planilha manda conferir no extrato.
- O resumo conta cada reserva no mês da data de entrada.
- "Sobra no mês" não é lucro líquido.
- Manutenção baixa: revisar os textos se as plataformas mudarem a forma de cobrar.

## Preço inicial para teste: R$ 19
- **É o primeiro degrau da escada:** planilha R$ 19 → Arsenal 01 R$ 27 → Trilhas. Cada degrau entrega sozinho o que promete.
- **Concorrência:** modelos estrangeiros custam de US$ 12 a 24, em inglês e sem as particularidades do Brasil.
- **Atenção à conta:** num ticket de R$ 19, as taxas do checkout e os impostos pesam proporcionalmente mais, e o custo do anúncio por venda pode passar do preço. Faturamento não é lucro: acompanhe o custo por venda desde o primeiro dia.

## Custos variáveis e de manutenção conhecidos
- **Por venda:** taxa do checkout (ClickMax ou Hotmart), impostos e reembolsos (7 dias, pelo Código de Defesa do Consumidor).
- **Entrega:** arquivo anexado à oferta, sem servidor e sem custo de hospedagem.
- **Atendimento:** dúvidas sobre como importar no Google Sheets. A aba "Comece aqui" já explica.

## Copy da página (estrutura curta)
- **Título:** Qual é a menor diária que cobre os seus custos?
- **Subtítulo:** Uma planilha pronta para anfitriões. Você digita os seus custos e a taxa da plataforma, e ela mostra a diária mínima, a diária para a sua meta e quanto sobrou no mês.
- **Botão:** Quero a minha planilha.
- **O problema:** baixar a diária para encher o calendário pode fazer você trabalhar mais e ganhar menos. Sem a conta, cada desconto é um chute.
- **O que você recebe:** a calculadora de diária mínima, o simulador de desconto, o controle de reservas e o resumo do mês, nas versões em branco e com exemplo.
- **Demonstração:** vídeo de 20 segundos com os números sendo digitados e a diária aparecendo.
- **Para quem é:** quem anuncia uma ou poucas unidades. **Não é para:** quem procura previsão de demanda ou preço automático.
- **Preço:** R$ 19, pagamento único, acesso ao arquivo assim que o pagamento é confirmado. Sem preço "de".

## Perguntas frequentes
- **Funciona no celular?** Dá para consultar, mas preencher é mais confortável no computador. No celular, use o app do Google Sheets.
- **Preciso saber Excel?** Não. Você só preenche as células amarelas.
- **Serve para Booking?** Sim. Informe a taxa do canal em cada reserva.
- **Ela diz quanto cobrar?** Ela mostra o mínimo que cobre os seus custos e a diária para a sua meta. O preço final depende também do mercado.
- **É lucro?** Não. "Sobra no mês" não inclui depreciação, imposto de renda pessoal nem o seu tempo, a menos que você os inclua.

## Três conceitos de anúncio
1. **"Você sabe qual é a sua diária mínima?"** Tela da planilha, com os custos sendo digitados e a diária mínima em destaque. Botão: Saiba mais.
2. **"Antes de dar 15% de desconto, faça esta conta."** O simulador mostrando "17,1 noites para manter a margem" (exemplo fictício, identificado). Botão: Saiba mais.
3. **"Quanto sobrou da sua hospedagem este mês?"** O resumo do mês sendo preenchido pelas reservas. Botão: Saiba mais.

## Indicadores para acompanhar
- Custo por clique e taxa de clique por anúncio.
- Visitas na página → início de checkout → compras.
- Custo por venda comparado aos R$ 19 menos taxas e impostos.
- Pedidos de reembolso e dúvidas de uso.

## Entrega no ClickMax
1. Produto e oferta em rascunho, no projeto Infoprodutos Zion.
2. O comprador recebe os dois arquivos `.xlsx` anexados como entregável. O upload se faz no painel: Produtos → oferta → **Cadastrar E-Books, PDFs ou Arquivos Digitais** (aceita planilhas).
3. O ClickMax envia o acesso depois do pagamento confirmado.
4. Pendente: aprovação da conta de vendedor e da oferta, ambas pelo ClickMax. Alternativa: Hotmart, com o mesmo arquivo.
