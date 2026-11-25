# Landing /mini-mentoria · Fase 03 · variantes A e B (rascunhos)

Agente: ZION CONVERSION · 25/11/2026. **Nada foi publicado, nada foi ligado, a página ao vivo `/mini-mentoria` não foi tocada** (conferido por `pages_get`: `updatedAt` e `lastPublishedAt` da `be23f04a` são anteriores a esta sessão).

## Páginas rascunho no ClickMax (workspace `e87e8ba9…`, projeto Infoprodutos Zion)
| Item | Id | Slug | Estado |
|---|---|---|---|
| Variante A (CTA com preço desde o topo) | `f690b2c4-1c05-4887-92c1-ddefbf1a230d` | `/mini-mentoria-a` | rascunho, `lastPublishedAt` null, `offerId 0c71eeba…` |
| Variante B (CTA só depois da oferta) | `299947bf-cf4a-42a7-971e-b9e02850bb81` | `/mini-mentoria-b` | rascunho, `lastPublishedAt` null, `offerId 0c71eeba…` |
| Obrigado Mini Mentoria | `1a0aed43-2f82-4b0a-826f-0424e2def674` | `/obrigado-mini-mentoria` | rascunho, tipo `thankYou`, sem oferta ligada |

Os nomes internos das páginas A e B herdaram "(Copy)…" do clone; renomear no painel se quiser (não afeta nada).

## O que muda entre A e B (única variável principal: posição do primeiro CTA de compra)
- **A:** CTA `QUERO ACESSAR A MINI MENTORIA POR R$47` no topo (hero), na faixa das telas reais, na oferta, depois dos entregáveis, no bloco de checkout e na barra fixa do celular (barra visível desde o topo).
- **B:** sem CTA no hero (selo "Formação digital · acesso por 12 meses" e aviso de rolagem). Primeiro CTA vem depois de dor, colapso, reconhecimento, método, aplicação, telas reais, **oferta e entregáveis**; barra fixa só a partir da seção da oferta.
- Todo o resto é idêntico (mesmo `comum.py`). Todo CTA que leva ao pagamento traz o preço.

## Estrutura (ECROI, depois oferta)
Hero (foto real nítida, sem texto sobre a foto) → **E** "Você tem o terreno. Mas não sabe por onde começar." → **C** "Preciso ter todo o capital antes de começar." (capital é o último passo da conta) → **R** "Não é falta de sorte. É terreno sem projeto estruturado." → **O** Marco Zero e sete pilares ("Aprenda o passo a passo") → **I** quatro passos na plataforma (assista, preencha a ficha, monte a página do Dossiê, gere o PDF) + telas reais → oferta (preço, como o acesso chega) → "O que você recebe em cada etapa" (reaproveita `CARDS` de `producao/.../build_bloco.py`) → Dossiê/cadastro opcional/possibilidade de parceria → foto real do interior (origem do método) → checkout → FAQ (sem reunião nem atendimento individual; parceria/investimento = possibilidade sujeita à análise; reembolso 7 dias).

## Acesso (só o que foi verificado)
`portals_get 3ef7a340…` em 25/11: `firstAccessWithoutPass: true` [E]. Texto usado: "o acesso é liberado para o e-mail usado na compra. Você entra com esse e-mail; o primeiro acesso é sem criar senha". **Não** afirmo "link por e-mail" nem prazo de chegada: o ciclo compra → acesso da oferta de R$ 47 ainda precisa do teste real de Bruno [NC].

## Decisões que fogem do pedido literal (por segurança do conteúdo)
1. **Vídeo `plataforma-v02.mp4` NÃO foi embutido.** A auditoria do CREATIVE (`06-criativos/AUDITORIA_CONTEUDO.md`) registra quadros com "Zion Land Bank" e "receber investimentos na sua área". No lugar: slot "Veja em poucos minutos como funciona a Mini Mentoria" com 3 telas reais (`aula`, `diagnostico`, `previab`), texto do slot vindo de `06-criativos/ROTEIRO_VSL.md`. **Como encaixar o VSL depois:** gravar conforme o roteiro; hospedar (GitHub Pages `docs/p/...` ou Vturb) e trocar o bloco `<div class="telas">` do slot por `<video ... src=URL>` (ou `<div data-cx-vturb=...>`), validar com `pages_validate_html` e reimportar na **página rascunho** (nunca na ao vivo).
2. **Tela `mapa.jpg` não usada**: ela cita "sócio" e "Zion Land Members". **A página ao vivo `/mini-mentoria` ainda usa essa tela** (e o vídeo acima). É uma frase incompatível no ar; correção exige "aprovado" de Bruno (ver relatório).
3. Nome "Mini Mentoria" mantido (decisão de Bruno); a página diz "formação digital" e "sem reunião nem atendimento individual".

## Regenerar
```
python3 -I zion-sales-engine/07-landing-pages/mini-mentoria/variante-a/build.py   # gera variante-a/index.html
python3 -I zion-sales-engine/07-landing-pages/mini-mentoria/variante-b/build.py
python3 -I zion-sales-engine/07-landing-pages/mini-mentoria/obrigado/build.py
```
Depois: `pages_validate_html` e `pages_import_html_draft` (manifest `sales`; `thank-you` no obrigado) **na página rascunho certa**, com `offerId 0c71eeba-2654-432c-9701-0a31e6113a08` nas vendas. O HTML precisa ir inteiro na chamada (sem arquivo anexo).

## Testes (Playwright, local) · `teste_local.js`
`SHOTS=<pasta> NODE_PATH=$(npm root -g) node teste_local.js` — 390×844 e 1366×800, A e B: sem overflow horizontal, 0 `<span>`, 0 `<script>`, 1 `[data-cx-checkout]`, seções hero/problem/solution/offer/cta/social-proof/faq, todo CTA com "R$47", A com 1 CTA no hero e B com 0, 0 erros de página, textos proibidos ausentes (grep: sócio, "receber investimento", faturamento, consultoria, R$ 97, simulador, calculadora, rede de investidores; "reunião" e "atendimento individual" só em negação). Resultado em 25/11: **TUDO OK**. Revisão visual de topo (A) e oferta/entregáveis (B) no celular; um defeito achado (preço invisível sobre fundo creme) foi corrigido antes da importação.
**Preview das rascunhos:** o endereço público das páginas em rascunho devolve 404 (conferido por GET) e o checkout (`payments.clickmax.io`) é bloqueado no ambiente. **Não vi as páginas importadas renderizadas**; o teste vale para o HTML local, idêntico ao importado. Bruno confere com "Visualizar" no painel, no celular, antes de publicar. Também não foi possível verificar se o ClickMax mantém a barra fixa (`position:sticky`) no render final.

## Reverter
Nada a reverter em produção. Para descartar: apagar as 3 páginas rascunho no painel (ou `pages_delete` com "aprovado"). Arquivos: `git revert` do commit.
