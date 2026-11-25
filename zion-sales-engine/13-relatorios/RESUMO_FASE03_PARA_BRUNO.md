# Resumo da Fase 03 para Bruno

25/11/2026 · ZION SALES DIRECTOR. Auditoria independente: **aprovado com ajustes**. Os ajustes de texto e código já foram corrigidos no repositório. Nada foi publicado, ligado, enviado ou gasto por nós nesta fase. Sem números reais neste resumo.

## 1. O que ficou pronto (12 entregas)

Caminhos dentro de `zion-sales-engine/`. **Liberado** = pode usar. **Ressalvas** = pode usar depois da condição. **Bloqueado** = não executar ainda.

| # | Entrega | Onde | Situação |
|---|---|---|---|
| 1 | Funil canônico, automações em rascunho, bump/upsell, relacionamento, textos de WhatsApp | `05-funis/` | Ressalvas: não ligar fluxo de recuperação sem a condição "já comprou" |
| 2 | Plano de consolidação do R$ 97 (só plano) | `05-funis/CONSOLIDACAO_OFERTA_97.md` | Ressalvas: travas de acesso incluídas; nenhum passo sem "aprovado" |
| 3 | Landing A e B da Mini Mentoria (rascunhos) | `07-landing-pages/mini-mentoria/` | Ressalvas: veja no celular; variante A precisa do seu "sim" |
| 4 | Obrigado, checkout enxuto e checklists | `07-landing-pages/mini-mentoria/obrigado/`, `08-checkouts/` | Ressalvas: texto já sem promessa de e-mail; publicar só depois da compra de teste |
| 5 | Plano do teste A/B | `11-testes-ab/` | Ressalvas: recomendamos **não executar** no teto atual |
| 6 | Plano de rastreamento e tutorial passo a passo | `09-tracking/PLANO_EXECUTAVEL.md`, `09-tracking/tutorial/` | Ressalvas: executar só com "aprovado"; padrão único de UTM já definido |
| 7 | Receptor da API de Conversões | `09-tracking/capi-webhook/` | Ressalvas: corrigido e testado; só ligar se a via nativa do ClickMax falhar |
| 8 | Recuperação das compras sem UTM, conciliação, snippet | `09-tracking/recuperacao/`, `conciliacao/`, `snippets/` | **Bloqueado** para envio real (passo 0, teste e base legal antes). Ferramentas e testes liberados |
| 9 | Criativos: conceitos, roteiro, 7 peças e copies | `06-criativos/`, `docs/ads/mm47-fase03/` | Ressalvas: só subir depois de corrigir o destino; copies já no padrão de UTM |
| 10 | Modelo financeiro | `08-financeiro/` | Ressalvas: faltam imposto, custos e tributos da veiculação |
| 11 | Mapa de produtos | `04-mercado/` | Liberado com ressalvas (amostrado) |
| 12 | Handoff de tráfego para o ChatGPT | `10-trafego/HANDOFF_CHATGPT_FASE03.md` | Ressalvas: depende das decisões abaixo |
| + | Segurança do repositório público | `13-relatorios/RISCO_REPOSITORIO_PUBLICO.md` | **Bloqueado** até a sua decisão |

Além disso: manual atualizado (`01-metodologia/MANUAL_MESTRE.md`, versão 2) e a lista completa de aprovações (`13-relatorios/MATRIZ_ALTERACOES_APROVACAO.md`).

## 2. O que você precisa decidir primeiro (em ordem)

1. **Qual é o teto de gasto?** Hoje há três versões. Escolha um valor por dia e eu atualizo o `CLAUDE.md`. (`aprovado: M01 teto R$ ___`)
2. **Pausar as campanhas "Plataforma R$97" e "Form R$ 47 direto"?** Estão ativas com peças que a auditoria reprovou. (`aprovado: M02`)
3. **Pausar ou ajustar a "Mini Mentoria Tráfego" até a página e o checkout estarem provados?** (`aprovado: M03`)
4. **Posso corrigir a página `/mini-mentoria` que está no ar?** Hoje o botão não mostra o preço e há tela e vídeo que falam de sócio e investimento. Eu faço o backup e publico a variante B (recomendada). Veja antes no celular. (`aprovado: M04 publicar variante B`)
5. **Você faz a compra de teste (Pix, depois cartão) e pede o reembolso?** É o que prova pagamento, acesso e rastreamento. (`aprovado: M05`)
6. **Posso fazer o espelho de segurança do repositório e levantar a lista de links de entrega?** É o primeiro passo para proteger os produtos pagos e os documentos de terceiros. (`aprovado: M06 espelho e inventário`)
7. **Quem ajusta o rastreamento no painel?** Compra só quando paga e tags de URL padrão nos anúncios. Eu preparo o passo a passo. (`aprovado: M07` e `aprovado: M08`)
8. **Depois dos itens acima, liga a campanha nova dentro do teto?** (`aprovado: M15 ativar com teto R$ ___ por dia`)

Prazo que corre: as compras reais sem UTM só podem ser reenviadas ao Meta até 7 dias depois do pagamento. Veja a data de cada uma no ClickMax e decida o `M10` com folga.

## 3. O caminho mais curto para vender

Teto (M01) → pausar o que está errado (M02, M03) → corrigir `/mini-mentoria` (M04) → compra de teste (M05) → rastreamento e tags de URL (M07, M08) → conferir e criar a campanha pausada (M09, M14) → ligar dentro do teto (M15) → publicar o obrigado (M18). Fluxos de e-mail, consolidação do R$ 97, teste A/B e repositório privado ficam para depois.

## 4. Avisos

- **Nada do que depende de painel foi visto por nós:** o checkout, o token e o dataset do Meta e a Ticto não são acessíveis daqui. Funcionamento do Pix, do cartão e da API de Conversões continua **não confirmado** até a compra de teste.
- **O repositório é público.** Há risco real de conteúdo de terceiros e de produtos pagos baixáveis sem compra. Não tornar privado sem migrar os links: quem já pagou perderia a entrega.
- **Ninguém mexe no acesso de quem já comprou.** O plano do R$ 97 só anda com retrato dos membros e confirmação por escrito do ClickMax.
- **Metodologias:** OP3D, Pareto em cascata, Método Zion 360° e Engenharia de Vendas Perpétuas estão só pelo nome. **Conteúdo detalhado pendente de Bruno.**
- **Imposto e custos** ainda sem valor: o ponto de equilíbrio do anúncio é uma estimativa até você informar.
- Silêncio não é "aprovado". Responda com a frase exata da matriz.
