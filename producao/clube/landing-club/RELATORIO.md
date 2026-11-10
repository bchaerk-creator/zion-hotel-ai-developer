# Landing Zion Collection Club · relatório de homologação (10/11/2026)

Status: desenvolvida e testada em branch `claude/landing-club-dev`. **Não publicada.** Fonte: `producao/clube/landing-club/index.html`.

## 1. O que já existia
- ClickMax, projeto Infoprodutos Zion: produto "Zion Collection · Inscrição no clube (R$ 97)" (id 1847aa9f…), oferta 72924971… aprovada, checkout `https://payments.clickmax.io/v_4pU5zNYj`, Pix e cartão em até 2x, reembolso 7 dias. Entrega: área de membros, portal Zion Land Bank, turma "Zion Land Bank · Candidatos" (Panorama + Trilha 1, 70 aulas). Venda-teste de Bruno às 19h41 (Pix pendente).
- Área de membros: Trilha 1 completa (Marco Zero + 7 pilares), ferramentas ZAR, formulário do Land Bank dentro da trilha, masterclass às quintas 20h, link de agendamento da sessão na última aula.
- Fotos reais (docs/assets/store, docs/assets/operacoes), fontes Cormorant/Aventa, logo oficial.
- Meta Pixel 903918118859018 já usado nas páginas do site; SDK do ClickMax nas páginas de produto.
- Asaas: links antigos (R$ 270 / R$ 97 do kit) continuam intactos; não usados nesta página.
- Zaya: fluxo "Pagamento inscrição R$ 97 confirmado" existe, mas dispara pela tag do webhook do Asaas, não por venda do ClickMax.
- Landing anterior `docs/zion-collection/` (publicada como rascunho em 10/11) segue no ar; esta nova não a substitui até aprovação.

## 2. Reutilizado
Oferta e checkout do ClickMax, identidade visual, fotos reais, fontes, Pixel, texto da política de privacidade, entrega na turma Candidatos.

## 3. Criado
Página completa com os 11 blocos do prompt; variante B do hero por `?v=b`; UTMs da página repassadas ao checkout; eventos do Pixel (PageView, ViewContent, CTAClick custom, InitiateCheckout no clique); CTA fixo no celular após o hero; FAQ com as 10 perguntas; noindex enquanto em homologação.

## 4. Testes
- Playwright 390×844 e 1280×800: sem rolagem lateral, sem erro de JS; variante B troca o título; CTA fixo aparece após o hero; 6 CTAs apontam para o checkout com as UTMs anexadas.
- Todos os arquivos externos respondem 200 no GitHub Pages; imagens + fontes = 740 KB (hero 238 KB).
- Acessibilidade básica: títulos em ordem, alt nas fotos, foco visível, link "ir para a oferta", reduce-motion.

## 5. Radar ZAI
Não existe no repositório, no ClickMax nem no Lovable. O que existe é a inscrição do terreno no Land Bank (formulário da Trilha 1 → Airtable). O bloco 05 e o benefício 05 estão marcados "em homologação" e a FAQ diz que, enquanto não estiver operacional, o terreno é inscrito no Land Bank.

## 6. Benefícios: confirmados e pendentes
Confirmados: área de membros, Trilha 1 completa, planilhas e fichas, Dossiê, masterclass, inscrição no Land Bank, reembolso 7 dias.
Pendentes: (a) acesso por 12 meses: a venda do ClickMax cria acesso sem validade; configurar 365 dias (precisa "aprovado"); (b) sessão de 30 minutos: existe o agendamento pela última aula e o modelo de WhatsApp de 30 min, mas o aviso automático após venda do ClickMax ainda não existe; (c) Radar ZAI.

## 7. Rastreamento
Purchase não é disparado pela página (evita duplicidade); deve vir do ClickMax/servidor após pagamento confirmado. Pendente: confirmar no ClickMax o evento de compra para o Pixel.

## 8. Pós-compra (proposta, nada ativado)
Fluxo novo: gatilho "venda aprovada" da oferta 72924971… → tag LAND BANK | INSCRIÇÃO R$97 PAGA → WhatsApp "inscrição confirmada" (modelo zion_inscricao_ok) → aviso ao Bruno → Zaya acompanha agendamento. Depende de "aprovado".

## 9. Pendências para publicação
1. Aprovação de Bruno do texto e do visual.
2. Decidir destino: substituir `docs/zion-collection/` ou publicar em `docs/clube/` e, com aprovado, rota /clube no Lovable.
3. Validade de 365 dias no acesso.
4. Fluxo de pós-compra para venda ClickMax.
5. Radar ZAI: manter bloco em homologação ou trocar por "Land Bank".
6. Retirar `noindex` ao publicar.
