# LOG de alterações · ZION SALES ENGINE

Formato: data · o que mudou · onde · ids · aprovado por · como reverter.
Só acrescentar entradas novas no topo. Ids de oferta e produto aparecem com 8 caracteres, como nos relatórios.

---

## 25/11/2026

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
