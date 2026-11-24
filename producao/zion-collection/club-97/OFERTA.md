# Zion Collection Club | Acesso à plataforma (R$ 97)

Criado em 24/11/2026. Tudo novo e separado; nada do que já existia foi alterado.

## ClickMax
- Produto: `072083e8-88c6-46bd-9e6c-5b851b6ac1c4` (projeto Infoprodutos Zion, classe Curso, categoria Negócios e Carreira).
- Oferta principal: `c298aaed-88ac-46dd-b6f3-f3c07ae08513`, R$ 97,00, pagamento único, Pix e cartão à vista (1x), sem boleto, checkout `1ApwIsdYSy`, `ZIONACADEMY`, suporte +55 48 6137-1061, reembolso em 7 dias.
- Turma nova no portal Zion Collection (`a8e2157a…`): "Zion Collection Club · Plataforma (R$ 97)" `69345987-7679-41e5-8e66-27281afa6892`, só com o conteúdo `fa9a6c54…` (sem o conteúdo de sessão `16f37c16…`).
- Entrega: área de membros (entregável `dbab19bc-4252-4c3f-a10f-fb71ba1a0538`).
- 24/11: `offers_get_incomplete_reason` voltou vazio e a oferta foi enviada para aprovação (resposta do envio: `pending`). Logo depois, `offers_get` mostrou `approved`: conferir no painel antes de contar com isso.
- Página (rascunho, não publicada): `d6b63999-3fdc-45f2-8fcc-af4d8e7e6d0b`, `/inscricao-97`, ligada à oferta nova. A página `/inscricao` (`77c286e6…`, R$ 270) não foi tocada.

## Promessa
Aprenda o passo a passo para estruturar o projeto de hospedagem do seu terreno. Sem promessa de investimento, parceria, renda ou valorização. Não inclui reunião individual.

## Página
- Fonte: `landing/build.py` → `landing/index.html`. Parte do esqueleto e do estilo da página `/inscricao` (cópia em `landing/inscricao-atual-270.html` e `.css`).
- Teste: `node landing/teste.js` (Playwright, celular 390×780 e desktop 1366×800).

## Pendências
- Vídeos "ZION-COLLECTION-PLATAFORMA-V02-CONVERSAO" e "QUEM SOMOS" não localizados (a galeria de telas ocupa o lugar).
- Imagem do produto (só pelo painel).
- Capturas da tela de login e do painel não existem.
- Prazo de 12 meses: está no texto, mas a turma nova não tem prazo de acesso configurado. Confirmar com o Bruno e ajustar.
- Troca da página no ar: só com a oferta aprovada e com o "aprovado" do Bruno.

## Registro · 24/11/2026 (troca aprovada por Bruno)

- Página `/inscricao` (`77c286e6-c3d2-4492-8fd9-8d5db7921ef8`) republicada às 01:01 UTC com a oferta `c298aaed-88ac-46dd-b6f3-f3c07ae08513` (R$ 97, checkout `1ApwIsdYSy`). Conferido no ar: preço, vídeo (8:36, toca), três botões, nenhum "270". Não conferido: o formulário de pagamento (o domínio de pagamento é bloqueado no ambiente de teste).
- Landing do site (`zionhotelgroup.com/inscricao`) reescrita para a oferta de R$ 97 e publicada.
- Bela: texto novo (venda direta, sem reunião, 12 meses) e uma base de 29 perguntas; as quatro bases de R$ 270 foram removidas.
- Turma `69345987-7679-41e5-8e66-27281afa6892`: acesso de 12 meses ao conteúdo `fa9a6c54-e40c-4ee0-99cc-ee6ec70e68fb`.
- Modelo de WhatsApp `clube_plataforma_d0` (`65598eac-57de-43d8-bc5e-fa24378d743c`): aprovado pelo Meta.
- Pendente: trocar o modelo no fluxo de abertura `bc86b069-5cb8-4620-b985-aaaeeeabd850` (ainda `inscricao_novo_d0`); fluxos de recuperação e de pagamento confirmado para a oferta nova; teste de compra real; imagem do produto; campanha de vendas (só pausada).
- 24/11 01:33 UTC: página `/inscricao` republicada com a frase de convite de Bruno no topo ("Faça a sua inscrição. Queremos te conhecer. Seja um parceiro Zion."); conferida no ar por curl. Mesma frase na landing do site e no convite oficial da Bela.
- 24/11 ~02:00 UTC: topo novo publicado em `/inscricao` e na landing do site: título "Faça a sua inscrição. Queremos te conhecer. Seja um parceiro Zion.", subtítulo "Transforme o seu terreno em destino turístico com a nossa plataforma.", botão "FAÇA A SUA INSCRIÇÃO" (texto aprovado por Bruno). Cartão 8 do carrossel preparado fora do repositório.
- 24/11 02:30 UTC: fluxo de abertura `bc86b069-5cb8-4620-b985-aaaeeeabd850` passou a enviar `clube_plataforma_d0` (vídeo da plataforma + botão para `/inscricao`), com "aprovado" de Bruno; 5 leads novos receberam (entregues). Lembretes de dia 2 e dia 5 ainda com texto antigo: segurar.
- 24/11: página `/inscricao` com o aviso "Avaliamos cada ideia, cada região e cada terreno…" e o bloco "O que você constrói na plataforma" (3 passos: vídeos, formulários, anexos; 5 itens; "Você constrói. A Zion conhece e avalia."). A capa da trilha saiu do bloco.
- 24/11 ~02:45 UTC: Meta (conta Zion Collection 2), tudo PAUSADO: campanha `120250538444300016` "[ZION COLLECTION][TRÁFEGO][PLATAFORMA R$97]" (tráfego, porque a página não tem pixel com compra utilizável), conjunto `120250538447120016` (R$ 30/dia provisório), anúncios `120250538459670016` (carrossel 10 A com preço), `120250538464160016` (carrossel 10 B sem preço), `120250538465770016` e `120250538466090016` (vídeo com texto novo; os dois usam o mesmo vídeo). Destino `/inscricao` com UTMs `utm_campaign=plataforma97`. Ativar só com "aprovado".
- 24/11: disparo "nova oportunidade" agendado para 24/11 09h30 (12:30Z), 32 leads de 22 e 23/11: fluxo `c84db4a6-8dd4-4ab6-9dea-b30b8f01815b`, execução `7f756892-7742-4c38-a99e-962aceabcbef`, modelo `clube_nova_oport_d1` (`a96cd456-8307-452b-8b90-6930a8038c0d`, em análise no Meta; conferência às 09h05).

## Registro de 24/11/2026 (tarde) · teste de venda direta

- Página curta publicada: `/inscricao-curta` (id `1597b2cc-d4e8-4ced-9c4d-a23a1d6d7053`), oferta `c298aaed…` (checkout `1ApwIsdYSy`). Texto: "Queremos te conhecer. Faça a sua inscrição. Seja um parceiro Zion." + vídeo + plataforma de estruturação + checkout. A página longa `/inscricao` não foi alterada.
- Meta, conta Zion Collection 2, campanha de vendas `120250538576770016` (R$ 97, checkout direto, sem formulário):
  - conjunto interesses `120250538578280016` (R$ 30/dia): Vídeo 01 narrativa, Carrossel 10 A v2, Vídeo 02 longa (`120250554660270016`) e Vídeo 02 curta com `#pagar` (`120250554662510016`) ligados; Carrossel 10 B v2 pausado.
  - conjunto remarketing `120250555057580016` (R$ 20/dia, públicos Zion 90, Público video, Zion collection 365): Vídeo 01 (`120250555107730016`) e Vídeo 02 curta (`120250555108170016`) ligados. Vídeo 02 longa não criado no remarketing.
  - Carrossel C para site: não criado (faltam título e descrição dos 7 cartões do original).
- Aprovação de Bruno em 24/11: ligar os anúncios e subir a verba da campanha de vendas para R$ 50/dia (30 + 20). A campanha de formulário (R$ 270 / leads) segue como estava.
- Plano: R$ 97 hoje; se não converter, versão de R$ 47 (a preparar, pausada).

## Pós-compra R$ 97 (24/11/2026, noite) · tudo em rascunho/desligado
- Anúncios de venda direta PAUSADOS (campanha `120250538576770016`) até o teste de ponta a ponta. Campanha de formulário (leads) segue ligada.
- Duas compras reais de R$ 97 (Pix) em 24/11: o acesso foi criado sozinho nas duas turmas (nova e antiga) em poucos minutos. Cartões movidos à mão para "8 · Comprou" (Funil Zion) e criados no funil "Inscritos" (`8b4405c0-f50a-40ba-abfd-11ab80e1ec41`, etapa 1).
- Funil "Inscritos · Plataforma Zion Collection" criado (6 etapas), sem automação de entrada.
- Tags: CLUB 97 | COMPROU, FICHA PREENCHIDA, PIX NÃO PAGO, CHECKOUT ABANDONADO.
- Fluxo de compra aprovada `fcc14b4d-ff0f-433c-ad9e-655e76519cd1` (rascunho, desligado) e fluxos de recuperação `01b4967a…` e `deb2de62…` (só tag). Falta teste de execução e "aprovado" de Bruno para ligar.
- Formulário de pós-compra `75ee0a3a-b17b-4fcf-be66-8eb97f6064ad` (ativo, sem automação) e página de obrigado `/obrigado-plataforma` (`d7166fc3-4f27-483b-8d9e-ca636c7facf0`, publicada). O formulário não pôde ser embutido na página de obrigado (validação do ClickMax): abre em link separado.
- Pendências de Bruno no painel: redirecionar o checkout da oferta para `/obrigado-plataforma`; remover a entrega do portal antigo (`zion-collection`); decidir sobre "Acesso por 12 meses" na descrição da oferta.
