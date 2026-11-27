# Validação antes do lançamento · teste A/B (27/11)
Nada foi ativado nem substituído. Prévias: `videos.jpg` (V17C e V06) e `prev.jpg` (carrosséis 01 e 02).

1. **Prévias:** vídeos e carrosséis acima. O V06 mostra o cartão "Reunião estratégica" e a fala promete "reunião estratégica com a nossa equipe". A campanha B entrega um formulário, não uma reunião, então é preciso confirmar se a equipe vai mesmo fazer essas reuniões.
2. **Formulário 1959234188381295:** criado com introdução, 5 perguntas e "Maior intenção". A tela de agradecimento é a padrão do Meta (o conector não permite personalizar o texto), e o botão final abre `/inscricao?utm_source=meta&utm_medium=lead_form&utm_campaign=zc2-b-formulario&utm_content=form-obrigado`. O conector não lê o formulário de volta, então a conferência visual precisa ser feita no Gerenciador.
3. **Lead de teste:** NÃO executado. Só dá para fazer na ferramenta de teste de anúncios de cadastro do Meta (developers.facebook.com/tools/lead-ads-testing), com o login do Bruno. Depois, conferir o lead na Central de Leads da página.
4. **Preço:** o checkout cobra R$ 47 uma vez (pagamento único, Pix ou cartão à vista, sem recorrência). A landing diz "R$ 47, pagamento único" e "12 meses a partir da liberação". Os anúncios dizem "Adesão inicial R$ 47". **Há divergência:** "adesão inicial" sugere que haverá outra cobrança depois. Recomendação: "R$ 47 · pagamento único" nos anúncios, ou explicar na landing o que vem depois da adesão.
5. **Otimização:** A = visualização da página; B = cadastro (lead). Mantido.
6. **UTMs, públicos e exclusões:**
   - A1 `utm_content=a-v17c`; A2 `a-carrossel01` (+ c1…c5); `utm_campaign=zc2-a-venda-direta`, `utm_term=quente-remarketing`. A landing repassa utm_* ao checkout (testado em produção em 27/11).
   - A inclui 7 públicos quentes; B inclui LAL 1% + 2 públicos de formulário e exclui os 7 do A. Compradores não são excluídos (não existe público de compra).
7. **Limite de R$ 90 por campanha:** o Meta recusou o limite de gasto da campanha (mínimo R$ 300 em BRL). Alternativa: no lançamento, gravar uma data de fim de 72 h em cada conjunto (R$ 30/dia × 3 = R$ 90).
8. **Orçamento consolidado da conta (Windsor, 30 dias):** a única campanha ativa é a ZC47 Frio `120250595856880016` (R$ 30/dia, limite R$ 420, R$ 6,38 gastos). As outras 15 campanhas com gasto no período estão PAUSADAS. A e B estão pausadas (R$ 30/dia cada). Campanhas sem gasto em 30 dias não aparecem nessa leitura: a conferência de duplicidade com a outra conversa precisa ser feita pelos nomes no Gerenciador.
   - Hoje: R$ 30/dia. Com a substituição proposta (pausar a ZC47 e ligar A e B): **R$ 60/dia, R$ 180 em 72 h**.
