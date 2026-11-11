# Auditoria · Zion Collection (20 produtos) × ClickMax "Infoprodutos Zion"

Feita em 11/11/2026, só leitura no ClickMax (nada foi alterado na auditoria). Workspace Bruno's Workspace, projeto **Infoprodutos Zion** (`8d1152a4`).

## 1. O que já existe no ClickMax

| Item | Situação em 11/11 |
|---|---|
| **Conta de vendedor** | `sellerStatus: pending` (KYC enviado em 06/11), conta bancária `approved`, gateway Ticto. **Enquanto o vendedor estiver pendente, nenhum checkout vende de verdade.** |
| **Produtos** | 44 no workspace (34 no projeto Infoprodutos, 10 no "Projeto de Bruno", a maioria arquivada). |
| **Erro de sincronização** | 36 ofertas com `providerSyncError: "Não autorizado. Token inválido ou ausente."` (quase todas as criadas antes de 10/11). Precisa do suporte ClickMax. |
| **Páginas** | 43 no projeto: 9 páginas de ferramentas de R$ 19, 19 landings das mini mentorias A/B (R$ 27), Club, Parceiro, vitrine e a `/academy-01`. |
| **Funis** | 2 (Club Collection e Parceiros Club), ambos ligados ao Club. |
| **Fluxos** | 8, todos em rascunho (devolutivas do diagnóstico, carrinho abandonado e Pix do Club, pós-compra do Club). Nenhum para infoprodutos de R$ 47. |
| **Área de membros** | 2 portais: Zion Hospitality Business (`mentoria-zion`, 10 turmas, 11 membros) e Zion Land Bank (7 membros). |
| **Order bump** | Nenhuma oferta do projeto usa bump hoje. A ferramenta `checkouts_set_order_bump` existe. |
| **Rastreamento** | `setup.confirmedWebhook: false` no projeto; sem domínio próprio. Pixel/eventos não aparecem configurados para infoprodutos. |

## 2. Sobreposição que precisa de decisão sua: Produto 06

O Produto 06 do kit tem **exatamente o mesmo título** de um produto que já existe:

| | Já existe (Arsenal Interativo 01) | Kit Zion Collection 06 |
|---|---|---|
| Título | Seu Airbnb Está Vazio? O Problema Pode Estar na Sua Oferta — Zion Hotel Academy Vol. 01 | Seu Airbnb Está Vazio? O Problema Pode Estar na Sua Oferta |
| Preço | R$ 27 (oferta `1ff56fea`, checkout `ySAkZG38VS`, `incomplete` por erro de sincronização) | R$ 47 + bump R$ 19 |
| Entrega | App de 40 telas, 7 pilares, dossiê PDF (`p/adbc67069af26ae0/arsenal-01/`) | E-book 60 p., aula, videoaula, Diagnóstico Zion de Oferta, plano |
| Página | `/academy-01` (rascunho) | nova |

Também existe, arquivado no "Projeto de Bruno", "Como Criar um Airbnb de Sucesso" a R$ 47.

**O que fizemos:** o Produto 06 foi criado **novo e separado** (nada do Arsenal 01 foi tocado). Antes de qualquer campanha, você decide uma das opções:
- **A (recomendada):** o 06 de R$ 47 passa a ser a oferta principal do tema; o Arsenal 01 sai de venda (arquivar a oferta de R$ 27) ou vira bônus/upsell interativo do 06.
- **B:** manter os dois, com nomes diferentes (ex.: Arsenal 01 vira "Arsenal Interativo · 7 Pilares").
- Vender os dois com o mesmo título confunde o comprador e o anúncio.

## 3. O que pode ser reutilizado

| Ativo | Onde | Uso no 06 |
|---|---|---|
| Molde de app interativo (salvamento local, feedback, PDF com jsPDF, testes Node e Playwright) | `producao/academy01/arsenal/` | base técnica do Diagnóstico Zion de Oferta |
| Molde de planilha (openpyxl, aba "Comece aqui", amarelo/verde, teste no LibreOffice) | `producao/low-ticket/01-diaria-minima/`, `producao/utilitarios/*` | planilha do diagnóstico e calendário do bump |
| Molde de landing (sete bandas, fotos por URL pública) e de capa/página de acesso | `producao/academy01/landing/`, `producao/utilitarios/build_entrega.py` | landing e página de acesso do 06 |
| Fotos reais da Zion sem pessoas, logo oficial, fontes | `docs/assets/`, `docs/brand/` | e-book, slides, criativos (sempre com legenda de origem) |
| Ferramentas de R$ 19 já aprovadas | 17, 11, 13, 14, 29, 18, 20, 30 | futuras opções de bump/upsell de outros produtos do kit |
| Hospedagem discreta dos entregáveis | `docs/p/adbc67069af26ae0/` | entrega do 06 |

## 4. Outras sobreposições do kit com o que já existe (para os próximos 19)

| Kit | Já existe | Observação |
|---|---|---|
| 07 Pare de Cobrar a Diária Errada | A02 "Quanto Devo Cobrar pela Minha Diária?" (R$ 27), Ferramenta 01 Diária Mínima (R$ 19) | decidir posição |
| 08 Fatura, mas sobra dinheiro? | A03 "Sua Hospedagem Fatura, mas Dá Lucro?" | |
| 11 Limpeza 5 Estrelas | Ferramenta 17 Checklist de Limpeza (R$ 19, aprovada) | a 17 pode ser o bump do 11 |
| 12 Check-in que encanta | Ferramenta 11 Kit de Mensagens (aprovada) | idem |
| 13 Atendimento no WhatsApp | A07 "Você Está Perdendo Reservas no Atendimento?" | |
| 14 Sem surpresas de manutenção | Ferramentas 14 e 18 (aprovadas) | |
| 15 Operar sem fazer tudo sozinho | A10, Ferramenta 20 (aprovada) | |
| 16 Anúncio não converte | A04 "Seu Anúncio Está Afastando Hóspedes?" | |
| 17 Hospedagem como experiência | A05, Ferramentas 29 e 30 (aprovadas) | |
| 02 Quanto custa a primeira cabana | Ferramenta 05 Orçamento da Cabana, B06 | |
| 01, 03, 04, 05 (desenvolvimento) | B01–B10, Land Bank, Kit de Captação | linha B ainda em decisão (Comando 05B) |

## 5. Divergências dentro do próprio kit (resolvidas assim, revise)

| Tema | Kit diz | O que usamos |
|---|---|---|
| Cores | Guia visual: musgo `#10271E`, areia `#F3EEE3`, dourado `#C6A86C` | Paleta oficial do `CLAUDE.md` (`#1B2117`, `#FEF5F0`, `#DED6BF`, `#C9B37E`…), para não criar uma segunda identidade |
| Escala da ferramenta | Especificação: notas 0–5, 7 dimensões (inclui Conforto e infraestrutura), 0–100 | Especificação (é a mesma do e-book, da aula e da landing) |
| | Planilha de referência: notas 0–4, pesos, total 48, dimensões "Posicionamento" e "Conversão" | não usada como regra; conversão entra no capítulo 7 |
| Imagens | "12 imagens exclusivas geradas" | Regra do repositório: imagem gerada nunca como foto real. Usamos fotos reais da Zion **com legenda de origem**, desenhos e diagramas próprios. A imagem de referência do kit (com rosto de Bruno gerado e "Mais reservas") é só inspiração |
| Promessa | Imagem de referência: "Mais reservas e resultados" | Fora: sem promessa de reservas |
| Vídeo | "com Bruno Chaerk" | Sem rosto nem voz de Bruno; ver pendências |

## 6. Riscos

1. **Vendedor pendente**: o checkout não processa pagamento real; os testes de compra (aprovada, pendente, recusada, estorno, reembolso, webhooks) **não podem ser executados de verdade** até a conta ser liberada.
2. **Erro de sincronização do gateway** em 36 ofertas antigas; ofertas novas criadas depois de 10/11 vieram sem o erro.
3. **Mesmo título no ar duas vezes** (Seção 2).
4. **Repositório público**: os entregáveis em `docs/p/...` ficam acessíveis a quem tiver o link quando forem para a `main`.
5. **Pixel/CAPI**: não há pixel do Meta configurado para infoprodutos no ClickMax; sem ele não há Purchase deduplicado.

## 7. Permissões

| Ação | Status |
|---|---|
| Criar produto, oferta e página em rascunho, novos e separados | autorizado (CLAUDE.md) e pedido neste kit |
| Enviar oferta para aprovação do ClickMax | **segurado**: você pediu nada publicado sem aprovação |
| Publicar página, ativar campanha, disparar mensagens, ativar fluxo | exige "aprovado" |
| Alterar Arsenal 01 ou qualquer estrutura existente | exige "aprovado" |
