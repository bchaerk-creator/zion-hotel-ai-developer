# LOG de alterações · ZION SALES ENGINE

Formato: data · o que mudou · onde · ids · aprovado por · como reverter.
Só acrescentar entradas novas no topo. Ids de oferta e produto aparecem com 8 caracteres, como nos relatórios.

---

## 25/11/2026 · Fase 03 · DATA (rastreamento)

- Criados em `09-tracking/`: `PLANO_EXECUTAVEL.md`, `tutorial/` (HTML e PDF), `capi-webhook/` (receptor Node sem dependências, 25 testes automáticos com Graph simulado), `recuperacao/` (script `reenviar_compras.py` em dry-run por padrão, 11 testes, e o documento de opções), `conciliacao/` (script e 7 testes), `snippets/persistir-utm.js` (proposta testada localmente, não instalada).
- Autorizado por: Comando Mestre da Fase 03. **Sem alterações em produção** (nenhum pixel, CAPI, webhook, anúncio, página ou oferta foi alterado; nada foi enviado à Meta; nenhum token foi usado).
- Reverter: `git revert` do commit "Fase 03 DATA: rastreamento executável".

---

## 25/11/2026 · Fase 03 · ZION CONVERSION
- Criadas no ClickMax, **só em rascunho** (nada publicado, nada ligado, página ao vivo intocada): `/mini-mentoria-a` (`f690b2c4`), `/mini-mentoria-b` (`299947bf`), ambas com a oferta `0c71eeba`, e `/obrigado-mini-mentoria` (`1a0aed43`).
- Neste repositório: `07-landing-pages/mini-mentoria/` (geradores, HTML, testes Playwright, README), `11-testes-ab/TESTE_AB_LANDING_MM47.md` + `amostra.py` + `test_amostra.py`, `08-checkouts/CHECKOUT_E_AGRADECIMENTO_MM47.md` e `CHECKLIST_ENTREGA_E_RECUPERACAO_MM47.md`.
- Achado: a página ao vivo `/mini-mentoria` usa a tela `mapa` (cita "sócio" e "Zion Land Members") e o vídeo demo com quadros de Land Bank/investimento; correção exige 'aprovado'.
- Aprovado por: Fase 03 (rascunhos). Publicar, ligar redirecionamento e rodar o A/B exigem 'aprovado' de Bruno.
- Reverter: apagar as 3 páginas rascunho no painel; `git revert` do commit.

---

## 25/11/2026 · Fase 03 · ZION CREATIVE
- Criados em `zion-sales-engine/06-criativos/`: `AUDITORIA_CONTEUDO.md`, `CONCEITOS_DIFERENTES.md`, `ROTEIRO_VSL.md`, `PACOTE_PARA_CHATGPT.md` e os geradores. Criadas 16 imagens (7 peças) em `docs/ads/mm47-fase03/` com `COPIES.md` e `manifesto.json`.
- Sem alteração em produção, Meta ou ClickMax. Gravação do vídeo depende de Bruno ou de produção. Subir ao Meta exige 'aprovado'.
- Reverter: `git revert` do commit.

---

## 25/11/2026

### Fase 03 · FINANCE (25/11/2026)
- Criada `zion-sales-engine/08-financeiro/`: `modelo_financeiro.xlsx` (6 abas, molde sem dados reais), `MODELO_FINANCEIRO.md`, `build_modelo.py` e `test_modelo.py` (137 conferências contra conta independente, todas OK). Só leitura no ClickMax e no Windsor; nada alterado em produção. Reverter: apagar a pasta.

### Neste repositório
- Criada a estrutura `zion-sales-engine/` (15 pastas, README raiz, `MANUAL_MESTRE.md`, 9 agentes documentados, relatórios da auditoria sanitizados, especificação do dashboard) e as 9 definições executáveis `.claude/agents/zion-sales-director`, `-funnel`, `-finance`, `-creative`, `-market`, `-data`, `-conversion`, `-traffic`, `-auditor`.
- Autorizado por: Bruno Chaerk (Comando Mestre ZION SALES ENGINE, 25/11/2026).
- **Sem alterações em produção nesta etapa.** Apenas arquivos novos; `CLAUDE.md`, `docs/`, `producao/` e agentes anteriores intactos.
- Reverter: `git revert` do commit "Cria zion-sales-engine".

### Em produção durante o dia (registradas a partir dos relatórios e do handoff da auditoria)

| Hora | O que mudou | Onde | Ids | Aprovado por |
|---|---|---|---|---|
| 25/11 | Campanha Mini Mentoria **ligada**: objetivo Tráfego, otimiza visualização de página, conjunto de R$ 30/dia (Brasil 25–65), 5 anúncios | Meta, conta Zion Collection 2 | campanha `120250559484620016`; conjunto `120250559488770016`; anúncios `120250559495520016`, `120250559496680016`, `120250559499010016`, `120250559502270016`, `120250559503550016` | Bruno em 25/11 ("Aprovado, pode pausar a LT47 e ligar a Mini Mentoria") |
| 25/11 | Campanha LT47 **pausada** (otimizava ViewContent, que não dispara) | Meta | campanha `120250557994600016` | Aprovado por Bruno em 25/11 ("Aprovado, pode pausar a LT47 e ligar a Mini Mentoria") |
| 25/11 01:37Z | Bloco "O que você recebe em cada etapa" (entregáveis) publicado nas páginas `/inscricao-47`, `/inscricao-curta`, `/parceiro-zion` e `/mini-mentoria` | ClickMax, projeto Infoprodutos Zion | páginas dos paths indicados | Bruno (antes da ordem de congelar) |
| 25/11 | `/mini-mentoria`: foto real da bolha nítida no topo (sem texto sobre a foto) e barra fixa do botão | ClickMax | página `be23f04a` | Bruno |
| 25/11 | Criados o **produto** e a **oferta** Mini Mentoria de Estruturação (R$ 47, pagamento único, Pix e cartão à vista, reembolso 7 dias; entrega por portal, 9 módulos e 70 aulas) | ClickMax | produto `cbbb5fb1`; oferta `0c71eeba`; portal `3ef7a340`; turma `087479a3` | Bruno |

**Notas de confiança**
- Estado da campanha lido de volta no Meta: [NC] (cache do Windsor atrasa). Conferir antes de citar como estado atual.
- O horário exato de cada linha, exceto o bloco de entregáveis (01:37Z), não consta nos relatórios; só a data.
- A lista de ids foi tirada de `13-relatorios/HANDOFF_CHATGPT.md`, `RELATORIO_FINAL.md` e `I_inventario_ofertas.md`. Ids completos das ofertas e do produto estão no ClickMax.
- Como reverter cada item: no painel da própria plataforma (pausar campanha, despublicar página, arquivar oferta). Reverter via Git não desfaz produção. Qualquer desfazer em produção também exige 'aprovado' de Bruno.

- 25/11/2026 · ZION MARKET (Fase 03): criados `zion-sales-engine/04-mercado/MAPA_PRODUTOS.md` e `mapa_produtos.csv` (inventário, filtros, ranking, escada). Só arquivos novos e atualização da seção do agente; sem alteração em produção. Reverter: `git revert` do commit.
- 25/11/2026 · ZION FUNNEL (Fase 03): criados em `05-funis/` `FUNIL_CANONICO.md`, `CONSOLIDACAO_OFERTA_97.md` (só plano), `AUTOMACOES_MM47.md`, `BUMP_UPSELL_DOWNSELL.md`, `RELACIONAMENTO_BASE.md` e `MM47_WHATSAPP_TEXTOS_PROPOSTOS.md` (só texto). No ClickMax (aditivo, tudo rascunho, nada ativo): 3 fluxos `[RASCUNHO] MM47` (`50e32512`, `d98795db`, `845e3b70`), 3 modelos de e-mail (`97330e1d`, `0f78a232`, `95a66dbe`) e 3 tags `MM47 | ...`. Nada publicado, enviado ou alterado no que já existia. Reverter: `flows_delete`, `email_templates_delete` e `tags_delete` nos ids acima.
- 25/11/2026 · ZION TRAFFIC (Fase 03): criado `zion-sales-engine/10-trafego/HANDOFF_CHATGPT_FASE03.md` (handoff atualizado para o ChatGPT estruturar a campanha de vendas da MM47: estado de partida, consolidação, estrutura, criativos e UTM, critérios de escala/pausa, checklist, base de compradores, matriz de responsabilidades). Leitura Windsor somente; nada alterado no Meta, no Windsor nem no ClickMax. Reverter: `git revert` do commit.
- 25/11/2026 · ZION AUDITOR (Fase 03): criados `13-relatorios/AUDITORIA_FASE03.md` e `13-relatorios/RISCO_REPOSITORIO_PUBLICO.md`; atualizada a seção do agente. Leitura apenas no ClickMax e no Windsor; testes locais executados; nada alterado em produção, Meta ou ClickMax. Reverter: `git revert` do commit.
- 25/11/2026 · ZION SALES DIRECTOR (Fase 03, correções pós-auditoria): corrigidos no repositório A05 (receptor CAPI: pago só `paid`/`approved` por padrão, `paid_pending` nunca vira compra; 27 testes passam), A09 (padrão único em `09-tracking/PADRAO_UTM.md`, `utm_campaign=mm47`, variante como sufixo `-varA`/`-varB` no `utm_content`, URL de destino sem parâmetros; copies, manifesto, A/B, handoff, funis e tracking alinhados), A10 (dados reais agregados e exemplos de data/hora trocados por faixas e exemplos fictícios; `RECUPERACAO_COMPRAS_24-11.md` renomeado para `RECUPERACAO_COMPRAS_SEM_UTM.md`), A11 (testes de conciliação e recuperação rodam com `python3 -I`; `.gitignore` em `zion-sales-engine/`), A06 (obrigado sem promessa de e-mail), A12 (LGPD em 09-tracking e 05-funis), A07 (travas no plano do R$ 97), A08 (bloqueio de ativação dos fluxos de recuperação). **Produção:** reimportado só o rascunho do obrigado (`1a0aed43…`, `lastPublishedAt` nulo antes e depois); nada publicado, ligado ou enviado; `/mini-mentoria` intocada. Criados `13-relatorios/MATRIZ_ALTERACOES_APROVACAO.md` e `RESUMO_FASE03_PARA_BRUNO.md`; `MANUAL_MESTRE.md` na versão 2. Reverter: `git revert`; o rascunho do obrigado volta com novo import do fonte anterior.
