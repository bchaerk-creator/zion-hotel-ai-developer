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

## Correção A06 (auditoria da Fase 03, 25/11)
A página de obrigado dizia "Se o e-mail não aparecer em alguns minutos, confira a caixa de spam". Como o fluxo de boas-vindas ainda é rascunho (não envia e-mail) e o ciclo compra → acesso nunca foi provado, a frase foi **removida** do fonte (`obrigado/build.py`) e trocada por "Se não conseguir entrar, fale com a gente pelo WhatsApp no fim desta página". O texto continua dizendo só o que foi verificado (acesso liberado para o e-mail da compra, primeiro acesso sem criar senha). Os fontes das páginas A e B não prometem e-mail e não mudaram (os `index.html` seguem idênticos ao build).

**Registro de reimportação.** Reimportar numa página **rascunho** (nunca publicada) exige novo `pages_import_html_draft` na mesma `pageId`, com o `offerId` correto quando for página de vendas. Feito em 25/11 só no obrigado (`1a0aed43…`, sem oferta): `lastPublishedAt` conferido como nulo antes e depois. A (`f690b2c4…`) e B (`299947bf…`) não precisaram de reimportação (fonte inalterado). **Nunca** importar em `/mini-mentoria` (`be23f04a…`) sem "aprovado": a publicada é atualizada ao vivo.

## v2 · Correção P0 de coerência comercial (25/11/2026)
**Versões:** `variante-a/` e `variante-b/` (v1, geradas por `comum.py`) **foram mantidas sem alteração**. As novas ficam em `variante-a-v2/`, `variante-b-v2/` e `obrigado-v2/` (gerador `comum_v2.py`, que reaproveita o CSS e os helpers de `comum.py`). O obrigado v1 (`obrigado/`) também fica como histórico.

| Item | Id | Slug | Estado |
|---|---|---|---|
| A v2 (preço no topo, botão do topo só rola) | `98ef3607-d18b-4bff-924f-6a5e6897b570` | `/mini-mentoria-a-v2` | rascunho, `lastPublishedAt` null, `offerId 0c71eeba…` |
| B v2 (sem CTA no topo) | `1dba4c0f-61d4-43fa-99ec-0698dfad7a9d` | `/mini-mentoria-b-v2` | rascunho, `lastPublishedAt` null, `offerId 0c71eeba…` |
| Obrigado v2 | `1a0aed43-2f82-4b0a-826f-0424e2def674` (mesmo rascunho, reimportado) | `/obrigado-mini-mentoria` | rascunho, `lastPublishedAt` null |

**O que mudou:** CTA padrão `QUERO ACESSAR A PLATAFORMA POR R$47`; botões antes da oferta só rolam (`#demonstracao`, `#oferta`); bloco de oferta completo (Mini Mentoria de Estruturação Zion, R$47, pagamento único, sem mensalidade, 12 meses, 9 módulos, 70 aulas e materiais, garantia de 7 dias, formação digital autônoma, Pix e cartão à vista) antes do primeiro botão de pagamento; lista dos 9 módulos com número de itens; materiais com contagem verificada (`08-checkouts/ENTREGAVEIS_VERIFICADOS.md`); Dossiê página a página; telas reais seguras (`aula`, `diagnostico`, `previab`; sem `mapa`, sem `agendar`, sem vídeo demo); barra fixa só da oferta ao checkout. Removidos: cadastro do terreno e "possibilidade de parceria" como seção, "a Zion avalia cada caso" na oferta, qualquer menção a inscrição, reunião (só uma negação na FAQ), equipe entrará em contato, receber investimentos, sócio. Parceria/investimento aparece só como "apresentar a potenciais parceiros e investidores" e, na FAQ, como "não garantido".

**Testes:** `SHOTS=<pasta> NODE_PATH=$(npm root -g) node teste_local_v2.js` (390×844 e 1366×800).
**Regenerar:** `python3 -I variante-a-v2/build.py`, `variante-b-v2/build.py`, `obrigado-v2/build.py`. Reimportar só na página rascunho certa (nunca em `/mini-mentoria` `be23f04a…`).
**Reverter para a v1:** nada está publicado, então não há o que desfazer em produção. Para voltar ao material anterior basta usar as páginas `f690b2c4…` (A) e `299947bf…` (B), que não foram tocadas; o obrigado anterior volta com `python3 -I obrigado/build.py` e novo `pages_import_html_draft` em `1a0aed43…` (manifest `thank-you`). Para descartar a v2: apagar as páginas `98ef3607…` e `1dba4c0f…` (com "aprovado") e `git revert` do commit.
**Pendências:** não vi as páginas importadas renderizadas (rascunho devolve 404 por GET e o checkout é bloqueado aqui); Bruno confere por "Visualizar" no painel. Vídeo demo só depois de roteiro aprovado (o atual tem "Land Bank"/"receber investimentos").

## v3 · Sessão de Diagnóstico Estratégico e redação segura (25/11/2026)
**Versões:** v1 e v2 mantidas sem alteração (`variante-a/b`, `variante-a-v2/b-v2`, `obrigado`, `obrigado-v2`, `comum.py`, `comum_v2.py`). As novas ficam em `variante-a-v3/`, `variante-b-v3/`, `obrigado-v3/` (gerador `comum_v3.py`).

| Item | Id | Slug | Estado |
|---|---|---|---|
| A v3 (botão do topo só rola) | `cbbf0a50-826f-4978-94a0-583d9ddbc481` | `/mini-mentoria-a-v3` | rascunho novo (clone de `98ef3607…`), `lastPublishedAt` null, `offerId 0c71eeba…` |
| B v3 (sem botão no topo) | `e0933e71-255e-4edc-bfec-92ba6a0121ac` | `/mini-mentoria-b-v3` | rascunho novo (clone de `1dba4c0f…`), `lastPublishedAt` null, `offerId 0c71eeba…` |
| Obrigado v3 | `1a0aed43-2f82-4b0a-826f-0424e2def674` (mesmo rascunho, reimportado) | `/obrigado-mini-mentoria` | rascunho, `lastPublishedAt` null |

`/mini-mentoria` (`be23f04a…`) não foi tocada (`updatedAt` anterior a esta sessão, publicada em 25/11 03:51). A v2 (`98ef3607…`, `1dba4c0f…`) ficou como estava.

**O que mudou na v3**
1. **Reunião após a mentoria**, com o nome decidido por Bruno: **Sessão de Diagnóstico Estratégico**. Saiu "sem reunião e sem atendimento individual". Entrou: etapa 5 "Depois da mentoria: solicite uma Sessão de Diagnóstico Estratégico*" na seção de Implementação (ECROI: I), seção "Estruture o seu projeto e faça parte da nossa expansão" ("Faça a mentoria. Depois, nós queremos te conhecer."), item nos entregáveis e na oferta, FAQ ("Tem reunião?", "Como solicito...", "É a mesma coisa que a Sessão de onboarding e estratégia?" -> não, é de outro produto), e a nota padrão: "*Sessão sujeita à análise e à agenda. Parceria e investimento não são garantidos." (corpo, oferta, checkout, rodapé). Não há atendimento individual contínuo; nada de consultoria; sem link da agenda pública.
2. **Redação segura da vistoria:** "70 conteúdos" (entre vídeos, fichas, e-books, planilhas e kits), "vídeo-aulas + 8 tutoriais em vídeo" (sem número de vídeo-aulas: YouTube [NC]), "8 fichas interativas", "8 e-books em PDF", "2 planilhas de cálculo com fórmulas", Kit do Investidor "guia das 6 peças", "9 comandos de IA", "Dossiê para baixar em PDF". Removidos "70 aulas", "26", "10 fichas", "6 modelos", "9 aulas interativas" e "e-books/slides de aprofundamento". Cartões por etapa reescritos (sem "1 vídeo" no Onboarding: o vídeo de boas-vindas tem Land Bank e fica fora da conta).
3. **Faixa de transparência** no topo (A e B): "Formação paga · Mini Mentoria Zion · R$47". Efeito no teste A/B: o preço agora aparece no topo nas duas; a variável passa a ser o botão de rolagem no topo (A) e a posição do primeiro CTA de compra (A na oferta; B após os entregáveis).
4. CTA `QUERO ACESSAR A PLATAFORMA POR R$47` mantido; preço antes do primeiro botão de pagamento.

**Obrigado v3:** bloco "Sessão de Diagnóstico Estratégico" com o botão `SOLICITAR A SESSÃO (APÓS CONCLUIR O DOSSIÊ)` apontando para o marcador **`{{LINK_SOLICITACAO}}`**. **Pendência:** o FUNNEL cria o formulário de solicitação (rascunho) e informa a URL; só então trocar o marcador (reimportar na página rascunho) e **antes de publicar** a página. Enquanto o marcador existir, o botão não leva a lugar nenhum; não publicar assim.

**Testes:** `SHOTS=<pasta> NODE_PATH=$(npm root -g) node teste_local_v3.js` (390x844 e 1366x800). Resultado 25/11: **TUDO OK** (sem overflow, 0 `<span>`, 0 `<script>`, 1 checkout, todo botão de pagamento com "R$47", preço antes do primeiro botão de pagamento, faixa presente, etapa "Depois da mentoria" presente, grep sem "taxa de inscrição", "sócio garantido", "garantimos", "consultoria", "R$97", "R$270", "70 aulas", "26", "10 fichas", "6 modelos", "land bank", "agendar", "cadastr"; "reunião" só nas frases da regra nova). Revisão visual no celular do topo, da Implementação, da seção Depois da mentoria e dos cartões. Não vi as páginas importadas renderizadas (rascunho devolve 404 por GET; checkout bloqueado).
**Regenerar:** `python3 -I variante-a-v3/build.py`, `variante-b-v3/build.py`, `obrigado-v3/build.py`. Reimportar só na página rascunho certa, com `offerId 0c71eeba…` nas de venda; nunca em `/mini-mentoria`.
**Reverter para a v2:** nada está publicado; use `98ef3607…` (A v2) e `1dba4c0f…` (B v2); o obrigado v2 volta com `python3 -I obrigado-v2/build.py` e novo `pages_import_html_draft` (manifest `thank-you`) em `1a0aed43…`. Para descartar a v3: apagar `cbbf0a50…` e `e0933e71…` (com "aprovado") e `git revert`.
**Depende de "aprovado" de Bruno:** publicar qualquer v3; enviar o `offers_update` (payload v3 em `08-checkouts/CHECKOUT_LIMPO_MM47.md`, não enviado); publicar o obrigado e ligá-lo ao checkout.
