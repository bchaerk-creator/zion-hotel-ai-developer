# Guia visual de rastreamento (tutorial para Bruno)

- `index.html`: guia responsivo (celular primeiro), identidade Zion. Abra no navegador.
- `tutorial-rastreamento.pdf`: o mesmo guia em PDF (gerado com Playwright, sem dados pessoais, sem tokens e sem números de vendas).
- `build_tutorial.py` gera o HTML; `render_pdf.js` gera o PDF (`NODE_PATH=$(npm root -g) node render_pdf.js`).

Cobertura: E eventos do funil P0 (7 eventos, o que o ClickMax permite, roteiro de teste) · A ClickMax (pixel, API de Conversões, token, histórico de envio, aba Pixels, regras de Purchase/Pix e InitiateCheckout) · B Meta (Gerenciador de Eventos) · C Ticto · D roteiro da compra de teste e critérios R1 a R8 · lista de prints.
Selo **confirmado** = caminho citado na documentação oficial do ClickMax lida em 25/11/2026. Selo **NC** = não confirmado (painel e documentação da Meta e da Ticto não acessíveis nesta sessão); o texto diz o que procurar. As telas desenhadas são esquemas.
