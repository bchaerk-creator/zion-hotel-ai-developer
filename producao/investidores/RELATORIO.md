# Zion Investors · relatório da sessão (28/11/2026)
**Nada publicado, nada enviado, nada alterado em produção, ClickMax, Lovable ou Meta.** Trabalho na branch `claude/zion-investors-page-redesign-er0n29`.

## Auditoria
- Lovable (projeto `dd227afd…`): a rota `src/routes/oportunidades.tsx` não tem conteúdo; ela busca `docs/investidores/index.html` no GitHub Pages (cache de 30 s) e injeta canonical e Meta Pixel (PageView). **Merge na `main` = página no ar.** Por isso não foi preciso mexer no Lovable.
- Página anterior preservada no git (`git log -- docs/investidores/index.html`); rollback = reverter o commit.
- Outras páginas, áreas privadas (`investidor.server.ts`) e integrações: intocadas.

## Entregue
| Item | Onde |
|---|---|
| Página mobile-first (wireframe do Master V2: hero, vídeo, luxo natural, modular, Urubici/Florianópolis, expansão, indicadores como temas, fundador, convite) | `docs/investidores/index.html` |
| Formulário de qualificação gratuito (9 perguntas, 3 dados + e-mail opcional, consentimento específico, sem CPF/capital) | idem (inline) |
| Carrossel adaptado + comparativo | `docs/ads/investidores-carrossel/` |
| Testes (40) | `producao/investidores/test_page.js` |
| Prints | `producao/investidores/prints/` (360, 390, 430, desktop; 4 telas do formulário) |
| Mapa das automações | `producao/investidores/MAPA_AUTOMACOES.md` |

## Testes (executados: 40 ok, 0 falhas)
Classificação (aderente, em maturação, apenas pesquisa, comprador de Bubble), normalização de telefone, ausência de rolagem horizontal em 360/390/430/1440, alvos de toque ≥ 44 px, imagens, validações do formulário, payload (id único, consentimento, sem dado sensível), honeypot, falha de servidor, comprador de Bubble redirecionado à loja, lead já cadastrado sem novo formulário, ausência de preço/checkout/promessa.
**Não testado:** integração real com ClickMax/WhatsApp (endpoint e números não configurados; webhooks, retries, idempotência no servidor, opt-out e fila ficam para depois da ligação), fontes Google (bloqueadas no ambiente de teste, aparece fonte reserva), áudio do vídeo institucional.

## Pendências
1. **WhatsApp 02** (número e responsável); WhatsApp 01 = final 1061 (confirmado). `ZION_CONFIG.WA01/WA02/ENDPOINT` ficam vazios até lá, e a página não mostra link de WhatsApp enquanto estiverem vazios.
2. Print do Instagram (cartão 04) e comprovação dos números.
3. Conferir o áudio do vídeo `video-zion.mp4` (vídeos antigos tinham falas de promessa).
4. Texto "Operações": a página diz que as oportunidades "podem envolver a expansão e também as operações atuais, caso a caso" (você informou que Urubici e Florianópolis também estão à venda/investimento). **Revisão jurídica.**
5. Pergunta 5 do Master V2 ("sede existente / nova / ambas"): interpretei como operações existentes / novas / ambas. Confirmar.
6. Aprovação comercial e jurídica antes de ativar campanha ou disparo.

## Atualização 28/11 (noite)
Decisões de Bruno aplicadas na página (WA01 1061, WA02 98872-9883, só expansão, vídeo sem URL até conferência de áudio) e no carrossel (só números documentados). 43 testes ok. Rascunhos criados no ClickMax: ver `MAPA_AUTOMACOES.md`, seção Atualização. Nada ativado.

## Separação plataforma × investidores (28/11)
Auditoria de 22 fluxos ativos, agentes, tags e sincronização Meta: ver `SEPARACAO_PLATAFORMA_INVESTIDORES.md` (8 pontos de contato e a regra para cada). Nada foi alterado no que já existe.

## 28/11 (noite, 2): publicada
Landing no ar em `/oportunidades` (merge autorizado por Bruno; rollback = reverter o merge `0d7da8f`). Formulário do Meta `1143109468438825` criado. Detalhes e pendências: `MAPA_AUTOMACOES.md`, última atualização.

## 28/11 · comando definitivo do formulário
Pacote de aprovação em `META_FORM_V3_PARA_APROVACAO.md` (spec, prévia mobile, classificação A+/A/B/C/D/T/BUBBLE/PENDENTE com 24 testes, política do Meta, argumentos conferidos: 266.388 seguidores confirmados). Nada criado no Meta nem ativado.
