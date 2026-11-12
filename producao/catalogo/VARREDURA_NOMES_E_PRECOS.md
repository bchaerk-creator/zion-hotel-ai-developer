# Varredura de nomes e preços antigos · Jornada do Desenvolvimento (R$ 970 em até 12x)

Data da varredura: 12/11/2026. Só leitura: nada foi editado, publicado ou enviado (Lovable, ClickMax e GitHub).
Tudo o que aparece como "sugestão" abaixo é **PROPOSTA**, a ser decidida por Bruno.

**Meta da proposta:** uma única jornada, **Jornada do Desenvolvimento** (Trilha 1 gravada + exercícios + ferramentas; o Marco Zero é só o primeiro módulo), R$ 970 em até 12x, pelo link Asaas `sd9u8uluy0urc2ye`.

**O que foi lido**
- Lovable "Zion Hospitality Platform": lista completa de arquivos (4 páginas de lista) e leitura de `hubPlans.ts`, `asaasHub.ts`, `checkouts.ts`, `links.ts`, `dossieOferta.ts`, `precosPaginaEstatica.ts`, `paginaEstatica.server.ts`, `schemaZion.ts`, `produtosProjects.ts`, `navegacao.ts`, `ecossistema.ts`, `llms.txt` e das rotas `hub`, `hub_.obrigado`, `consultoria.obrigado`, `pagamento-confirmado`, `metodo`, `metodo-zion`, `metodo-zion-360`, `club`, `clube`, `academy`, `land-bank`, `land-members`, `raio-x`, `sessao`, `projects`, `inscreva`, `OfertaLandBank`, `Header`. **Não li** (limite de tempo): `fundador`, `store*`, `oportunidades`, `parceiro`, `InscrevaPage`, `OfertaDossie`, `DiagnosticoPage`, `HotmartWidget`, `asaasHubWebhook.server.ts` e as rotas `livros/*`. Como o Lovable não tem busca de texto, vale pedir uma busca por "Trilha", "Fundadores", "270", "2.784", "302,09" nesses arquivos.
- Repositório: `docs/*.html` (e pastas), `docs/metodo`, `docs/lancamento`, `docs/previa`, `docs/teste`, `docs/reuniao`, `docs/raio-x`, `docs/trilha1`, `docs/clube`, `producao/clube`, `producao/mentoria-desenvolvimento-360`, `producao/catalogo`, `producao/jornada2`.
- ClickMax (só leitura): 47 produtos, 99 páginas, 9 funis, 123 templates do WhatsApp e 67 fluxos.

---

## 1. Mapa dos links Asaas encontrados

Preço e produto vêm do que o código do Lovable (`src/lib/asaasHub.ts`, `hubPlans.ts`, `dossieOferta.ts`) e os textos do site dizem. **Não consultei o Asaas**: o preço real de cada link precisa ser conferido lá.

| Id do link | Produto (segundo o código/textos) | Preço mostrado | Onde aparece |
|---|---|---|---|
| `sd9u8uluy0urc2ye` | **Trilha 1 gravada**: tag "MÉTODO / COMPROU TRILHA 1" e só a turma da Trilha 1 (`ASAAS_TRILHA1_PAYMENT_LINKS`) | **R$ 970** (comentário no código). Texto do site: "à vista ou até 10x" | Lovable `asaasHub.ts` (libera acesso). Repo: só no slide interno de downsell em `docs/reuniao/index.html` (linha 86, "não mostrar antes"). **Nenhuma página pública vende esse link hoje.** |
| `zrhq4rk88iyta3id` | **Zion Land Members + Radar** ("link antes vendido como Trilha 1"; sem turma, sem Hub) | **R$ 270** (6x de R$ 45) | Lovable: `asaasHub.ts`, `dossieOferta.ts` (`OFERTA_LANDBANK`), `consultoria.obrigado.tsx` ("Quero a Jornada por R$ 270"). Repo: `docs/metodo/oferta` (4 botões), `docs/raio-x` (linhas 545 e 549), `docs/previa/land-members`, backups em `producao/clube/diagnostico/backup/`. ClickMax: template `zion_raiox_resultado` (aprovado), página 925b7055 (Planos Base R$ 270). **O mesmo link aparece com o rótulo "R$ 97" em `docs/raio-x` (linha 549): preço divergente.** |
| `axfglfadpsy91xna` | **Mentoria em Grupo, 12x** (plano base do Hub) | 12x de R$ 302,09 (total R$ 3.625,08) | Lovable `hubPlans.ts` (checkoutUrl12x) e página `/hub` |
| `fr2kwfgps0jpv9nf` | **Mentoria em Grupo, à vista** | R$ 2.784 (20% off sobre R$ 3.480) | Lovable `hubPlans.ts` (checkoutUrlAVista) e `/hub` |
| `z49647pi0e4gpgk3` | Aceito como "Método Zion/hub" no webhook; não aparece em nenhuma tela | não identificado | Lovable `asaasHub.ts` (lista `ASAAS_HUB_PAYMENT_LINKS`) |
| `5ktufm44l8dbiwt3` | Turma Fundadores (hub) | 6x de R$ 549 (R$ 3.294) | Lovable `asaasHub.ts`; repo `docs/lancamento/hub.html` (linha 551) e `docs/teste/hub.html` (linha 549) |
| `62zus3azyzd50jbw` | **Pacote** das 4 trilhas (3 turmas de trilha) | R$ 890 | Lovable `asaasHub.ts` (`pacote`); repo `docs/raio-x` (`checkoutCombo`, `precoPacote`) |
| `r053uykadfxvn2wo` | **Consultoria prévia** (só tag, sem turma) | R$ 490 (10x de R$ 49) | Lovable `asaasHub.ts`; repo `docs/metodo/oferta` (linha 263) |
| `meti39wznfh6lcbv` | **Aula 47** | R$ 47 | Lovable `asaasHub.ts` |
| `byaslf734y50uicg` | "Inscrição na Trilha 1" (prévia) | R$ 270 à vista ou 6x (texto da prévia) | Repo `docs/previa/trilha1` (linhas 58 e 99); ClickMax template `zion_trilha1_inscricao` (rascunho). **Não está na lista do Lovable: um pagamento por esse link não libera acesso.** |
| `ruo696qm7zcr705b` | Checkout antigo do Hub (R$ 790, até 10x) | R$ 790 | ClickMax: funil "Club · Diagnóstico → Hub → Adesão" (rascunho, descrição) |
| `1pbkdxksp3pw15xd` | Kit de Captação (versão anterior) | R$ 97 | Repo `producao/clube/kit-captacao/COPY.md` (linha 81) e backup |

Outros destinos de pagamento no Lovable: sete links Hotmart dos livros (`checkouts.ts`, `/academy`); `CHECKOUT_ZION_START` vazio (Zion Start R$ 970 sem checkout).

**Conclusão do mapa:** o link `sd9u8uluy0urc2ye` já está pronto no código para liberar a Trilha 1, mas **nenhum botão público leva a ele**. Os botões ativos apontam para `zrhq…` (R$ 270) e para os planos de mentoria (R$ 2.784 a R$ 12.375).

---

## 2. Tabela "onde aparece / texto antigo / sugestão do nome novo" (por prioridade)

Nome novo sugerido (**PROPOSTA**): **Jornada do Desenvolvimento**. "Trilha 1" fica só como nome interno; "Marco Zero" fica como primeiro módulo; "Land Members" fica como o clube, separado.

### Prioridade 1 · compra e dinheiro (preço/produto errado para quem paga)

| # | Onde aparece | Texto antigo | Sugestão (PROPOSTA) |
|---|---|---|---|
| 1 | Lovable `/hub` (`src/routes/hub.tsx` + `src/lib/hubPlans.ts`) | Três planos: "Mentoria em Grupo" 12x de R$ 302,09 / R$ 2.784, "Mentoria com Acompanhamento" 12x de R$ 510,43, "Mentoria Premium" 12x de R$ 1.031,27; selo "Método Zion para Desenvolvimento de Hospedagem · assinatura anual"; "Os três planos são a mesma mentoria de 12 meses" | Trocar por um único plano "Jornada do Desenvolvimento", R$ 970 em até 12x, botão para `sd9u8uluy0urc2ye`. Decidir se `/hub` sai do ar ou é reescrita |
| 2 | Lovable `/hub`, trecho "Quanto pesa no seu projeto" | "Método Zion à vista custa R$ 2.784: 1,86%"; "parcela de R$ 302,09 é cerca de 0,2%"; projeto de exemplo de R$ 150 mil | Recalcular com R$ 970 ou remover; manter "valor ilustrativo, dados fictícios" |
| 3 | Lovable `/hub`, hero e FAQ | "12x de R$ 302,09 no cartão · ou R$ 2.784 à vista (20% off)"; FAQ "Posso parcelar? ... à vista com 20% de desconto" | "12x" calculado sobre R$ 970 (conferir a parcela no Asaas). Não prometer desconto à vista se não existir |
| 4 | Lovable `/consultoria/obrigado` (`consultoria.obrigado.tsx`) | "Acrescente a Jornada do passo a passo por R$ 270 ... Quero a Jornada por R$ 270" (link `zrhq…`) | "Jornada do Desenvolvimento por R$ 970 em até 12x", link `sd9u8uluy0urc2ye` |
| 5 | Lovable `/hub/obrigado` (`hub_.obrigado.tsx`) | "Bem-vindo ao Método Zion para Desenvolvimento de Hospedagem"; "Sua mentoria começa agora"; "sessão estratégica com o Bruno" | "Bem-vindo à Jornada do Desenvolvimento"; remover a sessão com o Bruno se ela não fizer parte dos R$ 970 |
| 6 | Lovable `src/lib/asaasHub.ts` (comentários e nomes) | `ASAAS_TRILHA1_PAYMENT_LINKS`, tag "MÉTODO / COMPROU TRILHA 1"; `ASAAS_LANDBANK` com "reuses the link formerly sold as Trilha 1" | Funciona como está. Só renomear rótulos internos se Bruno quiser. **Não mexer nos ids** |
| 7 | `docs/raio-x/index.html` (linhas 545–552) | `inscricao:{preco:'R$ 97' ... link zrhq…}` (o link vende R$ 270); `precoTrilha:'R$ 97'`; `precoPacote:'R$ 890'`; texto do WhatsApp "pacote com as 4 trilhas (R$ 890)" | Corrigir o rótulo ou o link; retirar "pacote 4 trilhas"; usar o link `sd9u…` para a Jornada. É a página que o Lovable serve em `/raio-x` |
| 8 | `docs/metodo/index.html` (linha 265) e `docs/metodo/oferta/index.html` (linhas 165, 251, 262, 312, 319) | "Curso online: Trilha 1 ... 6x de R$ 45 ou R$ 270 à vista, por trilha"; "6x de R$ 45 / R$ 270 no total. Menos de 1% de uma unidade"; degrau 1 "Inscrição Zion Land Members" R$ 270 | "Jornada do Desenvolvimento, R$ 970 em até 12x". Atenção: o Lovable reescreve preços por regex (`precosPaginaEstatica.ts`) só para "R$ 270 em até 12x" → "6x de R$ 45"; esse filtro vira inútil ou perigoso depois da troca |
| 9 | Lovable `src/lib/precosPaginaEstatica.ts` | Regex que troca "R$ 270 ... em até 12x" por "6x de R$ 45 ou R$ 270 à vista" em toda página servida do GitHub | Remover ou atualizar junto com a página de origem, para não reescrever o novo preço |
| 10 | ClickMax funil "Club · Diagnóstico → Hub → Adesão" (13073b82, rascunho) | "oferta R$ 790 ... checkout `ruo696qm7zcr705b` (R$ 790, até 10x)" | Não publicar assim. Atualizar ou arquivar |
| 11 | ClickMax produto "Trilha 1 · Desenvolvimento · Transforme seu terreno…" (046301c3) | Oferta com status `incomplete` | Decidir se a venda fica só no Asaas (como no Lovable) ou se a oferta do ClickMax é completada |

### Prioridade 2 · textos que dizem "mentoria", "Fundadores", "trilha" para o comprador

| # | Onde aparece | Texto antigo | Sugestão (PROPOSTA) |
|---|---|---|---|
| 12 | `docs/lancamento/hub.html` (linhas 542, 551, 567, 587), `obrigado-aula.html` (77–93), `aula.html` (128, 181, 225, 230), `aula-ao-vivo.html` (98), `obrigado-mentoria.html` (7, 64) | "Turma Fundadores · 6 meses", "6x de R$ 549 (R$ 3.294)", "R$ 47 viram crédito", "Depois R$ 270/mês", marcadores `LINK_ASAAS_AULA_`, `LINK_ASAAS_TURMA_CREDITO` | Retirar do ar ou reescrever para a Jornada do Desenvolvimento. Preço "de" 6x R$ 549 e crédito de R$ 47 contradem a regra "sem preço de falso/bônus inventado" |
| 13 | `docs/teste/hub.html` (540–581) | Cópia de teste do mesmo Hub "Turma Fundadores" | Apagar ou manter com `noindex` |
| 14 | `docs/previa/trilha1`, `previa/clube`, `previa/land-members` | "R$ 270 à vista ou até 6x"; "Inscrição na Trilha 1"; MASTER 12x de R$ 81,67; PRO 12x de R$ 241,67; "R$ 2.900 à vista"; link `byaslf…` | Marcar como prévia/obsoleta ou atualizar. Planos Master/Pro e R$ 2.900 não existem na nova oferta |
| 15 | `docs/reuniao/index.html` (84–86) | "6x de R$ 549 ... Turma Fundadores"; downsell "Trilha 1 gravada, R$ 970 à vista ou até 10x" | Slide interno. Alinhar: a Jornada passa a ser a oferta principal, não o downsell; trocar "até 10x" por "até 12x" se o Asaas permitir |
| 16 | `docs/trilha1/aula4`, `aula5`, `aula6` e `marco-zero` | "A conta completa vem na Trilha 2"; "o próximo passo: a Trilha 2, Estruturação"; WhatsApp "quero saber da mentoria em grupo ou individual" | "Próximo passo: o módulo de viabilidade" / "Jornada de Gestão" (nome a decidir); trocar o convite de mentoria em grupo pelo texto da Jornada |
| 17 | `docs/metodo/index.html` (244, 266) e `metodo/oferta` (portas 02 a 04, esteira 3 e 4) | "mentoria em grupo", "Assessoria em grupo (6 meses)", "Assessoria individual", "Consultoria prévia R$ 490" | Decidir se continuam como degraus separados. Se for "uma única jornada", esconder |
| 18 | Lovable `/clube` (serve `docs/zion-collection/`) e `/land-members` (serve `docs/land-members/`) | Páginas do Club/Land Members com R$ 270/mês no clube | Manter separadas da Jornada; só garantir que não chamem o clube de "Trilha" |
| 19 | Lovable `/projects` (`produtosProjects.ts`) | **Zion Start · R$ 970** ("Diagnóstico estratégico do seu terreno"), botão sem checkout, leva a `/land-bank` | **Colisão de preço e de público:** outro produto de R$ 970. Decidir se o Zion Start continua |
| 20 | Lovable `src/lib/ecossistema.ts` e `llms.txt` | "Hotel Academy ... /academy", "Método Zion: método para transformar um terreno em projeto"; livros e "Club Zion Collection" | Acrescentar a Jornada do Desenvolvimento no `llms.txt` quando existir página própria |

### Prioridade 3 · WhatsApp, fluxos e templates

| # | Onde aparece | Texto antigo | Sugestão (PROPOSTA) |
|---|---|---|---|
| 21 | Templates aprovados `zion_terreno_caminhos` e `zion_land_caminhos` | Botões "Jornada R$ 270", "Consultoria prévia", "Mentoria em grupo", "Mentoria individual", "A Zion faz por mim" | Novo template (Meta exige aprovação) com "Jornada do Desenvolvimento R$ 970". Não editar o aprovado |
| 22 | Template aprovado `zion_raiox_resultado` | "Zion Land Members ... São R$ 270 ou 6x de R$ 45, com garantia de 7 dias" (botão `zrhq…`) | Manter se o Land Members seguir vendendo; se não, criar novo |
| 23 | Templates `zion_inscricao_passos`, `zion_o_que_recebe` (aprovados) | "2x de R$ 48,50 ou R$ 97 à vista" (inscrição no clube) | Revisar para não confundir com a Jornada |
| 24 | Templates rascunho `zion_trilha1_inscricao` (link `byaslf…`), `zion_consultoria_paga` | "inscrição na Trilha 1"; "se você seguir para a mentoria, o valor da consultoria vira crédito" | Reescrever com o link `sd9u…` antes de enviar para aprovação |
| 25 | Fluxos ativos `Método Zion · Comprou Jornada → WhatsApp de acesso` (2c56ddfb) e `Método Zion · Comprou Trilha 1 ou Pacote → aviso + boas-vindas` (5cf1deeb) | Nome "Trilha 1 ou Pacote"; texto "acesso à Zion Land Members" no `zion_acesso_jornada` | Não mexer sem "aprovado" (automação ativa). Quando for trocar: o texto de acesso fala de Land Members, não de Jornada |
| 26 | Fluxos `Funil Terreno · 1 Clicou Jornada R$ 270` (fechado), `· 2 Clicou Consultoria prévia → link R$ 490`, `· 3 Mentorias e Premium`, `Raio-X · 1 Fez o Raio-X → oferta R$ 270`, `Raio-X · 2 Pagou R$ 270`, `Consultoria R$ 490`, `Método Zion · Pagamento Asaas (nativo) → aluno` ("liberar a Turma Fundadores") | Preços e nomes antigos nos nomes e textos | Rascunhos/fechados: arquivar ou reescrever depois da decisão |

### Prioridade 4 · produtos e páginas do ClickMax (rascunhos e arquivados)

| # | Onde aparece | Texto antigo | Sugestão (PROPOSTA) |
|---|---|---|---|
| 27 | Produtos arquivados: "Mentoria Zion 360° — Trilha A · Desenvolvimento" (50d6c664), "Trilha 2 · Gestão" (9c499405), "Trilha 3 · Operação" (305a5b3a), "Combo Mentoria Zion · As 3 trilhas" (1e6dd03c), "Estruturação Zion 360 — Dossiê" (13c09583), "Coleção Método Zion 360 — 7 volumes" (590541ec) | Nomes antigos | Já arquivados: deixar assim. Só garantir que nenhuma página ainda aponte para eles |
| 28 | Páginas "Lançamento · Hub Zion Turma Fundadores" (daa68392, "6x R$ 549"), "Lançamento · Boas-vindas Turma Fundadores" (abff747f), "Lançamento · Zion Glamping Store (Bubble)" (814e0f1e, "leva à mentoria") | Turma Fundadores, R$ 549 | Despublicar/arquivar após decisão |
| 29 | Páginas "Club · Hub (aula Marco Zero + adesão)" (0d7cedec, é a que o `/hub` do Lovable rastreia), "Aula · Marco Zero · 6 jornadas" (2d51262c) | "6 jornadas", Marco Zero como produto de entrada | Renomear para "Jornada do Desenvolvimento" |
| 30 | Páginas de checkout/inscrição R$ 97 e R$ 270: 5e0d2e63, ac57f756, 159794c5, 9614b777, 925b7055, 4cca189d | "Checkout R$ 97", "Base com link do Asaas de R$ 270. Provisória." | Pertencem ao Club/Land Bank. Não misturar com a Jornada |
| 31 | Página modelo "MODELO · Aplicação de Mentoria Premium" (1a9244d8) | "Mentoria Premium" | Modelo, sem uso. Apagar se não for usar |
| 32 | Funis em rascunho: "Aula de Sábado" (oferta da Coleção), "Ebooks Zion 360 · Venda", "Ebook Glamping Vol. 2 — R$47" | Coleção Método Zion 360 | Fora do escopo; só avisar |

---

## 3. O que precisa mudar, por lugar (tudo PROPOSTA, nada foi alterado)

### 3.1 Lovable (projeto dd227afd…)
Linhas aproximadas, pois o leitor do Lovable não numera linhas.

1. `src/lib/hubPlans.ts`, linhas ~26–95: o vetor `HUB_PLANOS` (3 mentorias, R$ 2.784 a R$ 12.375). Trocar por 1 plano "Jornada do Desenvolvimento" com `checkoutUrl12x` = `https://www.asaas.com/000/c/sd9u8uluy0urc2ye`. Atualizar também `HUB_COMPARATIVO` (~100–112) ou remover a tabela.
2. `src/routes/hub.tsx`: `DESC` (~linha 20), `<title>`/`og:title` (~27–33), hero "12x de R$ 302,09 · R$ 2.784" (~215), bloco "Quanto pesa no seu projeto" (~330–355), FAQ "Posso parcelar?", "Como é a sessão com o Bruno?" (~85–95), seção "Sessão estratégica" e "Rede Zion". Inclui promessas de acesso a "investidores" e "Rede Zion" (ver riscos).
3. `src/routes/hub_.obrigado.tsx` (~12–30): título, "mentoria", "sessão estratégica com o Bruno".
4. `src/routes/consultoria.obrigado.tsx` (~30–36): "Jornada ... por R$ 270" e link `zrhq…`.
5. `src/lib/precosPaginaEstatica.ts` (arquivo todo, 5 linhas) e `paginaEstatica.server.ts` (~1–3 e ~52): filtro de preço R$ 270 → 6x R$ 45.
6. `src/lib/asaasHub.ts`: sem erro. Só conferir que `sd9u8uluy0urc2ye` continua em `ASAAS_TRILHA1_PAYMENT_LINKS` (linha ~25). Opcional: renomear comentários. **Não alterar ids nem tags.**
7. `src/lib/dossieOferta.ts` (~15–27): `OFERTA_LANDBANK` R$ 270 = Land Members. Manter se o clube continua.
8. `src/lib/produtosProjects.ts` (~20–32): "Zion Start · R$ 970" (colisão de preço).
9. `public/llms.txt`, `public/sitemap.xml`: incluir a Jornada quando houver página.
10. `src/lib/checkouts.ts` (`CHECKOUT_ZION_START` ~linha 18): vazio, sem ação.
11. Ainda não lidos: ver a lista da introdução.

### 3.2 Repositório (`/home/user/zion-hotel-ai-developer`)
Páginas públicas do GitHub Pages que **ainda mostram nomes ou preços antigos** (ordenadas por risco; as marcadas com * o Lovable serve no domínio oficial):

| Página pública | O que mostra |
|---|---|
| `docs/raio-x/index.html` * (`/raio-x`) | "R$ 97" com link de R$ 270, pacote R$ 890, "4 trilhas" |
| `docs/metodo/index.html` * (`/metodo-zion`) | Trilha 1 "6x de R$ 45 ou R$ 270", "mentoria em grupo", "assessoria individual" |
| `docs/metodo/oferta/index.html` | R$ 270, R$ 490, "Assessoria em grupo/individual", âncora "mais de R$ 120.000" |
| `docs/lancamento/` (6 arquivos) | Turma Fundadores, 6x R$ 549, R$ 3.294, R$ 270/mês |
| `docs/previa/trilha1`, `previa/clube`, `previa/land-members` | R$ 270, Master/Pro, R$ 2.900 |
| `docs/teste/hub.html` | Cópia de teste da Turma Fundadores |
| `docs/reuniao/index.html` | Apresentação de reunião (slide interno com R$ 970 "até 10x") |
| `docs/trilha1/aula4`, `aula5`, `aula6`, `marco-zero` | "Trilha 2", convite a mentoria em grupo |
| `docs/store/comprar/index.html` | 12x de R$ 6.583 e R$ 7.083 (Bubble, outro produto; só avisar que não é da Jornada) |

Documentos internos (não públicos de venda, mas com nomes antigos): `producao/mentoria-desenvolvimento-360/INVENTARIO.md` (Trilha A, Trilha 2, Trilha 3, Combo, Turma Fundadores), `producao/clube/*` (OFERTA_CLUBE_ENTRADA, ESTRATEGIA_FUNIL_97, LANDING_GATILHO_47_97, ROTEIRO_REUNIAO, COPY do kit etc., com R$ 97, R$ 270, R$ 980, R$ 2.900), `producao/jornada2/*` (PLANOs e REGISTROS que citam preços e "Trilha"), `CLAUDE.md` (não cita a Jornada de R$ 970).

Não encontrei R$ 290, R$ 297 nem R$ 470 nas pastas varridas (fora de `producao/jornada2`, que tem números de exemplo; não confirmei um a um).

### 3.3 ClickMax (workspace e87e8ba9…)
- **Produto:** completar ou deixar de lado a oferta "Trilha 1 · Desenvolvimento" (046301c3, `incomplete`). Se a venda for só pelo Asaas, não é preciso criar oferta nova.
- **Páginas a despublicar/arquivar/renomear:** Turma Fundadores (daa68392, abff747f), Hub (0d7cedec), "Aula · Marco Zero · 6 jornadas" (2d51262c), checkout R$ 97/R$ 270 (se saírem do funil), modelo "Mentoria Premium" (1a9244d8).
- **Funil:** "Club · Diagnóstico → Hub → Adesão" (R$ 790).
- **Templates WhatsApp:** criar novo em vez de editar os aprovados (item 21 a 24).
- **Fluxos ativos:** 2c56ddfb, 5cf1deeb, 08a59f14 (Pagamento R$ 97 confirmado). Não mexer sem "aprovado".

---

## 4. Riscos

1. **Preço divergente (alto):** a mesma frase "R$ 97" aponta para um link de R$ 270 em `docs/raio-x` (`zrhq…`). O Lovable serve essa página em `/raio-x`.
2. **Dois preços e um link no ar para a mesma "Jornada":** `/consultoria/obrigado` e `docs/metodo/oferta` vendem "a Jornada" por R$ 270 (link Land Members), enquanto o link da Trilha 1 de R$ 970 não aparece em nenhum botão público. Quem comprar R$ 270 recebe Land Members, **sem a turma da Trilha 1**.
3. **Webhook x link novo:** um link Asaas fora da lista de `asaasHub.ts` (como `byaslf734y50uicg`) não libera acesso. Só `sd9u8uluy0urc2ye` está ligado à turma da Trilha 1.
4. **Regex que reescreve preço (médio):** `precosPaginaEstatica.ts` altera o HTML do GitHub no momento de servir. Depois da troca para R$ 970, o filtro pode mascarar ou contradizer o texto novo.
5. **Preço "de" e âncoras (regra do CLAUDE.md):** `docs/lancamento` usa "6x de R$ 549" com crédito de R$ 47; `docs/metodo/oferta` usa "Consultoria completa: mais de R$ 120.000" (sem fonte); `/hub` usa "20% off" sobre R$ 3.480 e um projeto de exemplo de R$ 150 mil. Sem fonte ou sem marca de "dados fictícios", são risco.
6. **Promessas a revisar (não encontrei "garantia de renda/ocupação" explícita, mas há linguagem próxima):**
   - `/hub`: "Porta para investidores do setor", "Projetos estruturados ficam na vitrine ... vista pela rede de parceiros e investidores"; "Zion como parceira estratégica". Há avisos de "não é promessa", mas o título da seção sugere acesso a capital.
   - `/land-bank` (Lovable, texto do hero): "Estar nele abre a possibilidade de ser parceiro da Zion e de receber investimentos do setor". É mais forte que o FAQ ("não garante"). Sugestão de trocar por "...abre a possibilidade de conversa".
   - `/hub` FAQ e `docs/metodo/oferta`: "garantia de 7 dias" nos templates (aceitável, é o CDC); conferir se o Asaas oferece o mesmo.
   - `/hub`: "Menos de 2% do projeto para decidir o resto com método": comparação de preço com obra; mantém o aviso, mas é argumento de retorno implícito.
7. **Colisão de produto (médio):** "Zion Start R$ 970" na página `/projects` tem o mesmo preço da Jornada, com outro conteúdo.
8. **Mentoria e sessão com o Bruno:** `/hub`, `hub/obrigado` e vários templates prometem "sessão estratégica com o Bruno". Se a Jornada de R$ 970 é só gravada, isso precisa sair, para não vender o que não entrega.
9. **Escopo de leitura incompleto:** arquivos do Lovable não lidos (introdução) podem ter mais textos antigos. O mesmo vale para `docs/clube/kit-captacao` e `docs/zion-collection`, que tiveram 0 ocorrências pela busca simples (pode haver "R$&nbsp;97" ou espaços especiais).
10. **Parcelas:** "12x" no Asaas costuma ter juros por conta do cliente; o texto do site hoje diz isso no `/hub`. A nova página precisa repetir, e a parcela exibida precisa vir do próprio Asaas (não calculei aqui).

---

*Arquivo gerado por varredura de leitura. Nenhum commit, nenhuma publicação.*
