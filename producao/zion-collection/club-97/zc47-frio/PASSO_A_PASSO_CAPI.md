# Passo a passo · ClickMax + Ticto + Meta (pixel e API de Conversões)

Para Bruno executar no painel. Nada disto foi feito por esta sessão. O token da Meta é colado só no painel do ClickMax, nunca no chat.

## Antes de começar
- A oferta de R$ 47 (`668391e7…`) usa o gateway **Ticto dentro do ClickMax**. A confirmação do pagamento chega ao ClickMax pela própria Ticto: **não há webhook para configurar na Ticto** nem no Asaas para esta oferta. O ClickMax é quem envia o Purchase à Meta.
- Escolha **um** conjunto de dados (pixel) para todas as ofertas da Zion Collection: o que estiver ligado à conta de anúncios Zion Collection 2 no Gerenciador de Eventos (ver `RASTREAMENTO_AUDITORIA.md`, pixels `1378530017570073` e `903918118859018`). Não crie pixel novo sem decidir.

## 1. Gerar o token da API de Conversões (Meta)
1. business.facebook.com › Gerenciador de Eventos › selecione o pixel escolhido.
2. Configurações › API de Conversões › "Gerar token de acesso".
3. Copie o token (não envie por mensagem).

## 2. Cadastrar o pixel no ClickMax
1. ClickMax › Marketing › Tráfego › **Pixel e trackeamento** › Adicionar pixel › Meta.
2. ID do pixel: o escolhido. Apelido: "Zion Collection · Meta".
3. Marque **Receber eventos que não acontecem numa tela** (opcional) e, se quiser, **Usar em tudo que eu criar a partir de agora**.
4. Eventos:
   - **Comprou (Purchase):** navegador **e** servidor; formas de pagamento **todas** (inclusive Pix).
   - **Abriu o checkout:** ligado, com **Só contar depois dos dados pessoais**.
   - **Escolheu a forma de pagamento (AddPaymentInfo):** ligado.
   - **Abriu uma página (PageView):** ligado (só navegador).
5. Bloco **API de Conversões da Meta:** cole o token › **Testar token**. Deixe o **Código de teste** preenchido só durante o passo 4.
6. Se aparecer "Eventos novos disponíveis", leia "Ver o que muda" antes de ativar: InitiateCheckout passa a chegar como **AddToCart**.

## 3. Ligar o pixel a cada checkout e página
1. Produtos › "Zion Collection Club | Acesso à plataforma" (`072083e8…`) › aba **Pixels** › marque o pixel (vale para os checkouts de R$ 47 e R$ 97).
2. Faça o mesmo nos produtos das demais ofertas da Zion Collection (Inscrição R$ 270, Mini Mentoria `cbbb5fb1…`, Sessão).
3. Páginas `/checkout-zion-47` e demais landings do ClickMax: aba de rastreamento › pixels › marque.
4. **Não** adicione Purchase por Google Tag Manager nem pelo site (duplicaria).

## 4. Teste controlado (com Código de teste ligado)
1. No Gerenciador de Eventos, aba **Testar eventos**, copie o código e cole em "Código de teste" no ClickMax.
2. Abra `zionhotelgroup.com/inscricao?utm_source=teste&utm_campaign=capi&fbclid=TESTE` › botão › checkout.
3. Gere um Pix e **não pague**: na aba de testes deve aparecer PageView/AddToCart/AddPaymentInfo, **sem Purchase**.
4. Pague um Pix de R$ 47: deve aparecer **1 Purchase**, valor **47,00 BRL**, recebido por "Navegador e servidor" (deduplicado) e com parâmetros de correspondência (e-mail, telefone, fbc).
5. No ClickMax, Tráfego › Pixel e trackeamento › Histórico de envio: Purchase **Enviado**.
6. Confira a venda em Minhas vendas: UTMs gravadas (utm_source teste, utm_campaign capi).
7. **Limpe o Código de teste** e reembolse a compra de teste.

## 5. Depois do teste
- Conjuntos de dados: compartilhe o pixel com a conta Zion Collection 2 (Configurações do negócio › Fontes de dados › Pixels › Contas de anúncio).
- Só então: proposta de campanha de Vendas (Compra), substituindo a de Tráfego.

---

# Histórico de compradores no Meta (análise, nada executado)

**O que dá para fazer**
1. **Exclusão de compradores** (recomendado já): público personalizado por lista de clientes (e-mails e telefones dos compradores pagos de R$ 47 e R$ 97), usado só como **exclusão** nas campanhas de aquisição. Baixo risco e evita pagar para alcançar quem já comprou.
2. **Público semelhante de compradores:** a Meta exige no mínimo 100 pessoas encontradas na lista; hoje a base de compradores pagos da Zion Collection é pequena (a de R$ 47 tem 1 venda paga real até 27/11, mais compras de teste). Fica para quando houver volume.
3. **Envio retroativo de compras pela API:** a Meta só aceita eventos de site com até **7 dias**; compras anteriores não reentram como conversão de site. Eventos "offline/sistema" aceitam janela maior, mas não ajudam a otimizar campanhas de site e têm de usar o mesmo `event_id` da venda para não duplicar.

**LGPD e consentimento**
- Base legal: legítimo interesse para marketing próprio, com transparência. A política de privacidade do site e do checkout precisa dizer que dados de clientes podem ser compartilhados de forma criptografada (hash) com a Meta para medição e exclusão de anúncios, com caminho de oposição.
- Só e-mail e telefone, com hash SHA-256 (a Meta faz o hash no upload pelo Gerenciador); nunca CPF.
- Remover quem pediu para não receber comunicações e quem pediu reembolso, se a política assim definir.
- Upload pelo próprio Bruno no Gerenciador de Públicos (lista de clientes); o Windsor não tem ação de envio de lista.

**Deduplicação:** a lista de clientes não conta conversão; só a API/pixel conta. Não reenviar compras antigas como Purchase de site.
