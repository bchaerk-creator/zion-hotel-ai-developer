# AUDITORIA FASE 03 · ZION AUDITOR · 25/11/2026

Revisão independente das entregas de FUNNEL, CONVERSION, DATA, CREATIVE, FINANCE, MARKET e TRAFFIC (commits `380b1d2` a `802a09f`). Nada foi corrigido por este agente; só relato. Sem números reais de gasto, vendas ou resultado neste arquivo. Marcação: **[E]** verificado por mim agora (leitura/execução), **[L]** lido em documento de outro agente e não refeito, **[NC]** não confirmado.

## 1. Veredito

**APROVADO COM AJUSTES.** Os arquivos da Fase 03 estão limpos de segredo, e-mail, telefone e nome de cliente [E]. Os testes passam [E]. Nada novo foi publicado, ligado ou enviado [E]. Mas há **4 pontos P0** que não nasceram na Fase 03 e que o DIRECTOR deve levar a Bruno **antes** de qualquer outra coisa: campanhas ativas fora do teto e com peças reprovadas, gasto ligado sem compra de teste, página ao vivo com conteúdo incompatível recebendo tráfego pago, e exposição do repositório público (ver `RISCO_REPOSITORIO_PUBLICO.md`).

## 2. Método e o que eu executei [E]

| Verificação | Resultado |
|---|---|
| `git pull --rebase origin main` | atualizado |
| `node --test tests/*.test.js` em `09-tracking/capi-webhook` | 25 de 25 passam |
| `python3 08-financeiro/test_modelo.py` | todos os testes passam (recalcula no LibreOffice) |
| `python3 -I 11-testes-ab/test_amostra.py` | OK (3.841 por variante na referência do ClickMax; 8.158 na clássica) |
| `python3 test_conciliar.py` e `test_reenviar.py` | passam (7 e 11 testes), **mas só sem `-I`**; com `-I` falham (achado A11) |
| `persistir-utm.js` (`node --test`) | passa |
| `07-landing-pages/mini-mentoria/teste_local.js` (Playwright) | TUDO OK nas variantes A e B, celular e desktop; os builds reproduzem os `index.html` byte a byte |
| Ataque ao receptor CAPI (14 classificações, vazamento em log, segredo errado, duplicata, evento velho) | Pix gerado/expirado/unpaid ignorados; duplicata barrada; log sem e-mail, telefone, nome ou token; ver A05 |
| Varredura do working tree (e-mail, telefone, CPF/CNPJ, tokens, atribuições de segredo) | sem segredo; só o telefone de suporte da marca; e-mails de exemplo; 1 e-mail pessoal do titular em doc antigo (A12) |
| Varredura do histórico (e-mail, telefone, token) | sem token; ver `RISCO_REPOSITORIO_PUBLICO.md` |
| ClickMax (leitura): `pages_get` das 4 páginas, `flows_get` do pós-compra, `offers_get` da oferta canônica e de uma ferramenta, `portals_get`, `classrooms_details`, `sellers_status` | ver seção 6 |
| Windsor (leitura): estado das campanhas da conta Zion Collection 2 | ver A01 |

Limite: o checkout (`payments.clickmax.io`) e os painéis do Meta e da Ticto não são acessíveis daqui; Pix, cartão, CAPI, dataset e token continuam **[NC]**. Não li Bela/Zaya, Clube nem Land Bank (só confirmei que as campanhas R$ 270, Land Bank e LT47 seguem pausadas).

## 3. Achados

Severidade: **P0** bloqueia ou expõe risco grave agora; **P1** corrigir antes de ligar/publicar; **P2** melhoria. "Executa" = quem faz a correção.

### P0

**A01 · Campanhas ativas com peças reprovadas, destino divergente e fora do teto.** Windsor, 25/11: ficam `ACTIVE` a campanha "Plataforma R$97" (7 anúncios; destino `/inscricao-47` com vídeos reprovados pela auditoria), a "Form R$ 47 direto" (2 anúncios) e a "Mini Mentoria Tráfego" (`120250559484620016`, com a peça "03 PARTICIPAÇÃO", que o CREATIVE classificou como a mais próxima de promessa) [E]. O handoff soma orçamento configurado quase o dobro do teto de teste e registra, como hipótese, "faturamento por bubble" em formulário antigo (`10-trafego/HANDOFF_CHATGPT_FASE03.md:26,178`) [L]. O teto no `CLAUDE.md` (R$ 0) também não bate com o do modelo e do handoff (R$ 60/dia): três versões do teto.
- Por quê: promessa de renda e de parceria em anúncio vivo (política do Meta) e gasto acima do teto combinado.
- Correção: Bruno decide hoje pausar Plataforma R$97 e Form R$ 47 e definir um teto único por escrito; a Mini Mentoria Tráfego fica só se trocar a peça 03. Reversão: reativar a campanha pelo id. **Executa: Bruno (decisão e painel); ChatGPT prepara.** Nenhum agente da Fase 03 mexeu no Meta [E: estados batem com o handoff].

**A02 · Gasto ligado antes de provar compra e entrega.** O próprio handoff marca "BLOQUEIA" para checkout Pix/cartão nunca visto e entrega da oferta `0c71eeba` nunca provada (`HANDOFF_CHATGPT_FASE03.md:174-176`), mas a campanha da Mini Mentoria está `ACTIVE` [E]. Risco: comprador paga e não entra (reembolso e reputação).
- Correção: compra de teste de Bruno (Pix; depois cartão) com o roteiro `08-checkouts/CHECKLIST_ENTREGA_E_RECUPERACAO_MM47.md` itens 1 a 11; enquanto isso, pausar ou reduzir. **Executa: Bruno.**

**A03 · Página ao vivo `/mini-mentoria` incompatível com os anúncios que recebe.** `be23f04a` publicada em 25/11 03:51Z (`updatedAt` 03:50:57Z) [E]. Segundo CONVERSION (`07-landing-pages/mini-mentoria/README.md`, "Decisões 1 e 2") ela ainda usa a tela `mapa.jpg` (cita "sócio" e "Land Members") e um vídeo com quadros de "Land Bank" e "receber investimentos" [L]. Os botões ao vivo dizem "QUERO TRANSFORMAR MEU TERRENO", **sem preço** (`triggerMap`, [E]), contra a regra de CTA com preço. Os anúncios novos afirmam "parcerias e investimentos não fazem parte do produto".
- Correção: com "aprovado", publicar uma das variantes (B recomendada, ver A14) **depois** de `pages_clone` da ao vivo como backup, e conferir `lastPublishedAt`. Reversão: reimportar o backup. **Executa: CONVERSION com aprovação de Bruno.**

**A04 · Repositório público e histórico.** Resumo: documentos jurídicos de terceiros (com CPF/CNPJ e valores) numa branch pública, relatórios com valores reais no histórico do `main` (commit `7d10efb`, removido do working tree em `ff74df0` mas **não do histórico**), e os produtos pagos baixáveis sem compra. Detalhe, opções e plano: `RISCO_REPOSITORIO_PUBLICO.md`. **Executa: Bruno decide; Claude prepara.**

### P1

**A05 · Receptor CAPI: o que conta como "pago" é largo demais.** `src/config.js:31` define `paid,approved,completed,authorized,captured` como pagos. Cartão `authorized` (ainda não capturado) viraria `Purchase` [E: `{status:'authorized'}` → `purchase`]. Além disso `src/classify.js:26`: o nome `paid_pending` vira compra [E]. Viola R1 se o gateway usar esses termos.
- Correção: padrão `paid,approved`; ampliar só com evidência do payload real; acrescentar teste. **Executa: DATA/Claude.**

**A06 · Página de obrigado promete e-mail.** `07-landing-pages/mini-mentoria/obrigado/build.py:29`: "Se o e-mail não aparecer em alguns minutos, confira a caixa de spam". O fluxo de boas-vindas é rascunho (modo `draft`, [E]) e o ciclo compra→acesso nunca foi provado. O README do CONVERSION diz que não afirma "link por e-mail", mas a obrigado afirma.
- Correção: tirar a frase até o item 5 do checklist passar, ou ligar o fluxo só depois do teste. **Executa: CONVERSION.**

**A07 · Plano de consolidação do R$ 97: faltam travas de acesso.** `05-funis/CONSOLIDACAO_OFERTA_97.md`: nenhum passo remove acesso (bom) e a seção 2 proíbe isso [E], mas: (i) o Passo 1 (linhas 31 a 38) usa como "canário" compras de Bruno nas **mesmas ofertas** que têm os 2 compradores reais, e propõe arquivar `668391e7`, cujo efeito sobre o acesso é [NC]; (ii) o Passo 7 (linha 55) manda remover a entrega do portal antigo "nas ofertas que continuarem ativas" e renomear turmas, sem exigir antes um retrato dos membros; (iii) o Passo 6 (linha 53) arquiva `c298aaed`, a oferta dos compradores reais; (iv) a Opção B do e-mail (reembolso) cancela o acesso por natureza.
- Correção: acrescentar como condição de todo passo: (a) retrato antes/depois dos membros de **cada** turma dos dois portais (`member_users_list_by_classroom`) com comparação; (b) confirmação **por escrito do suporte do ClickMax** de que arquivar oferta não revoga acesso, antes de arquivar qualquer oferta com compradores; (c) não alterar entregas de `c298aaed` e `668391e7` em nenhuma hipótese; (d) o reembolso só a pedido do comprador. **Executa: FUNNEL (texto); Bruno (aprova).**

**A08 · Fluxos de recuperação sem a condição "já comprou".** `05-funis/AUTOMACOES_MM47.md` §4.2: a API recusou o passo; mitigação só por texto ("se já pagou, ignore"). Quem paga depois do Pix expirar receberia o e-mail de recuperação. Debounce de 3.600 s (§4.5) permite repetir. Já está no documento como pendência; eleva-se a **bloqueio de ativação**. **Executa: FUNNEL no editor; Bruno liga.**

**A09 · Padrão de UTM divergente entre documentos.** `utm_campaign`: `mm47` (`10-trafego/HANDOFF_CHATGPT_FASE03.md:111`, `COPIES.md`, plano A/B), `<campanha>` slug `mini-mentoria` (`09-tracking/PLANO_EXECUTAVEL.md:63`), `mini-mentoria` (`05-funis/CONSOLIDACAO_OFERTA_97.md:46`) e `<produto>` (`CLAUDE.md` §6). `COPIES.md` e `manifesto.json` trazem só `utm_source/medium/campaign/content/term`, enquanto o padrão definitivo exige também `sck`, `ad_id`, `campaign_id`, `adset_id` via `url_tags`: colar os dois produz parâmetro duplicado [H]. O plano A/B usa `utm_term=varA|varB`, o handoff usa `utm_content=<id>-varA` (divergência que o TRAFFIC já listou, não resolvida). Sem padrão único a conciliação (R7) e a atribuição (R5) quebram.
- Correção: um único padrão num único arquivo (sugestão: o do PLANO §1.7 com `utm_campaign=mm47`), `COPIES.md` com URL só de destino, e a escolha da marcação de variante. **Executa: DATA decide; CREATIVE e TRAFFIC alinham.**

**A10 · Dado real em repositório público.** A regra proíbe número de venda/resultado real. Ocorrências agregadas: contagem de compradores externos (`08-financeiro/build_modelo.py:107`, nota do parâmetro de reembolso), "vendas/compras reais de 24/11, R$ 97 cada, Pix" (`09-tracking/recuperacao/RECUPERACAO_COMPRAS_24-11.md`, primeiras linhas), proporção de tráfego de servidor num dia (`HANDOFF_CHATGPT_FASE03.md:179`), "0 compras contra 2 vendas reais" (`01-metodologia/MANUAL_MESTRE.md:203`). O exemplo de data e hora de pagamento em `RECUPERACAO_COMPRAS_24-11.md:34` pode ser a hora real de uma compra: [NC], trocar por exemplo fictício. Severidade baixa de sensibilidade (sem nome nem e-mail), mas descumpre a regra e fica no histórico.
- Correção: reescrever em faixas ("poucos") e trocar o exemplo. **Executa: cada agente dono; DIRECTOR confere.**

**A11 · Comandos de teste inconsistentes.** A regra do projeto manda `python3 -I`; `test_conciliar.py` e `test_reenviar.py` falham com `-I` (`ModuleNotFoundError`, [E]) e a documentação deles manda rodar sem `-I`. Também: `.gitignore` não cobre `compras.csv` nem `*.enviados`; o script recusa CSV dentro do repo (bom), mas a pasta de trabalho do Bruno pode ficar sob o repo. **Executa: DATA** (inserir `sys.path` como no `test_amostra.py`; acrescentar as entradas ao `.gitignore`).

**A12 · LGPD e consentimento.** (i) O snippet `persistir-utm.js` grava origem no navegador por 30 dias e reescreve a URL (inclui `fbclid`) sem aviso de cookies/armazenamento documentado; (ii) a recuperação reenvia e-mail e telefone com hash ao Meta e o Handoff §7.3 sobe lista de compradores: a base legal e o aviso de privacidade são **[NC]** (o DATA registrou). (iii) E-mail pessoal do titular aparece em `docs/zaios/ENTREGAS_VALIDACAO_ACADEMY.md:21` e é o e-mail de suporte visível ao comprador na oferta (`supportEmail`), [E].
- Correção: texto de privacidade e cookies atualizado antes de instalar o snippet ou enviar lista/recuperação; usar e-mail de domínio da empresa como suporte. **Executa: Bruno com orientação jurídica; DATA redige o texto.**

**A13 · Campanha `120250560823800016` não verificada.** O handoff a chama de campanha "da MM47 criada pelo ChatGPT" e não a encontrou; minha leitura Windsor também não a lista [E]. Estado, destino e UTM: [NC]. **Executa: ChatGPT/Bruno** (ler no Gerenciador, itens 1.2 do handoff).

### P2

- **A14 · Ordem ECROI e posição do CTA.** Variante **B** segue a definição de Bruno (E→C→R→O→I→oferta→entregáveis→preço→CTA) [E, grep e teste]. Variante **A** põe CTA com preço no topo, antes da narrativa: é o teste pedido, mas foge da definição; Bruno deve dizer sim de forma explícita. Em B o primeiro CTA fica a cerca de 7.700 px no celular e a barra fixa só aparece na oferta: risco de perda de quem decide cedo. Os textos têm as cinco etapas, sem depoimento, sem urgência, sem preço "de/por" [E]. Palavras sensíveis só em negação ou em lista de conteúdo ("renda ou venda", "ocupação e demanda" nos cartões de entregáveis).
- **A15 · Bloco "Possibilidade de parceria".** `comum.py:169-172` cria uma seção própria com esse título dentro de uma página de R$ 47, com ressalva "possibilidade, sujeita à análise". Cumpre a regra, mas convida a expectativa e destoa da oferta ("não fazem parte do produto"). Sugestão: fundir à FAQ.
- **A16 · Anúncios: palavras de risco.** Todas as artes repetem no rodapé "Não promete renda, parceria ou investimento"; `c09` tem a pergunta "Garante parceria ou investimento?"; `c04` diz "como o projeto ganha dinheiro". São negações honestas, mas gatilham revisão de "oportunidade de negócio/financeiro" do Meta. Visualmente: sem texto sobre foto, sem pessoas, logo oficial, rodapé legível [E, 16 imagens vistas]. Texto das artes confere com a entrega real: 9 módulos, 70 aulas, "A sua Pré-viabilidade", "Planilha de pré-viabilidade", Kit do Investidor, cadastro do terreno [E, `classrooms_details`].
- **A17 · Nome da turma.** A turma da oferta canônica se chama "Plataforma de estruturação (R$ 97)" [E]: o comprador vê "R$ 97". Renomear exige "aprovado" e não altera acesso. O módulo "Comece aqui · Onboarding" existe, então os textos da obrigado e do e-mail estão corretos.
- **A18 · Receptor CAPI, endurecimento.** Segredo aceito por query string (fica em log de hospedagem); sem carimbo de tempo para impedir repetição; JSON inválido devolve 400 antes de checar o segredo; sem limite de taxa; `server.js` sem TLS próprio (depende do proxy). Nada disso vaza dado pessoal [E]. Defaults de `META_GRAPH_VERSION` [NC].
- **A19 · Finanças.** Reconferi as contas com fórmula independente (seção 5): batem. Lacunas: o gasto no Meta costuma ter tributos próprios sobre a veiculação que o modelo não tem como parâmetro [H, alíquota não verificada]; sugerir uma linha "custos da veiculação" a definir. Teto de mídia com três versões (A01).
- **A20 · Teste A/B de landing.** O plano está correto e honesto, mas com o teto vigente o tamanho de amostra não é alcançável em 28 dias (o próprio TRAFFIC diz isso, `HANDOFF:§3.4`). Recomendo registrar como **não executar** e decidir por leitura qualitativa, para ninguém declarar vencedora com poucos dados.
- **A21 · Cobertura de MARKET.** Amostrei preços e ranking contra o `CLAUDE.md` e o cálculo de CPA; bate. Não refiz linha a linha as 40 linhas de `mapa_produtos.csv` [NC].

## 4. Critérios solicitados, ponto a ponto

**(a) Coerência anúncio × página × checkout × produto.** Promessa: "Aprenda o passo a passo" em todos [E]. Preço R$ 47: arte, primeira linha, A/B e oferta batem [E]; **a página ao vivo não mostra o preço no botão** (A03). Pix/cartão 1x, reembolso 7 dias, 12 meses, suporte: ads, páginas e oferta batem [E]. Entrega: o que os anúncios e as páginas citam existe na turma [E] (9 módulos, 70 aulas, fichas, e-books, planilhas, Kit do Investidor, Kit de prompts, cadastro opcional). UTM: divergente (A09). Checkout em si: [NC].

**(b) Segurança.** Sem segredo, e-mail de cliente, telefone de cliente ou nome em arquivos da Fase 03 [E]. Receptor: log sem PII e sem token [E], segredo comparado em tempo constante [E]. Histórico: ver `RISCO_REPOSITORIO_PUBLICO.md`.

**(c) Integridade de acessos.** Nenhuma ação proposta remove acesso explicitamente [E: leitura dos planos]; as travas faltantes estão em A07. Não existe, na Fase 03, chamada de `member_users_*` de escrita em nenhum documento.

**(d) Políticas das plataformas.** Sem antes/depois, sem atributo pessoal, sem renda garantida nas peças novas [E]. "Você tem o terreno" na landing e "Seu terreno está parado" (H1) pressupõem condição do leitor: risco baixo de atributo pessoal em anúncio; o anúncio em si não usa isso [E]. Pixel/CAPI/LGPD: A12.

**(e) Rastreamento R1–R8.** Código: R1 parcial (A05), R2 ok (centavos ÷ 100 uma vez, faixa 1 a 2.000, rejeita 0,47 e 4700 [E]), R3 [NC] sem token, R4 depende de desligar o Purchase nativo (documentado), R5/R6 dependem do snippet e de `url_tags` (não instalados), R7 `conciliar.py` testado, R8 Pix gerado/expirado ignorado e reembolso não vira `Purchase` [E]. Dedupe do receptor por `event_id` idempotente (memória por padrão; disco opcional). `Purchase` só com `value` > 0 e `currency` [E].

**(f) ECROI e termos proibidos.** Variantes A e B e obrigado: palavras "reunião", "atendimento individual", "investimento", "parceria" aparecem só em negação, em "possibilidade sujeita à análise" ou no nome "Kit do Investidor"; sem "sócio", "faturamento", "garantido", "Land Bank", "consultoria" (só na pergunta do anúncio c09 em negação) [E, grep do texto renderizado].

**(g) Viabilidade financeira.** Ver seção 5.

**(h) Reversibilidade.** Todos os itens têm reversão escrita: fluxos, modelos e tags (`*_delete`), páginas (`pages_delete`/despublicar), arquivos (`git revert`). A reversão de um `Purchase` enviado ao Meta **não existe** (o DATA avisa; o teste vem antes) [E].

**(i) Falsidades.** Nenhuma promessa falsa, urgência falsa, preço "de" ou depoimento inventado encontrado nas entregas novas [E]. O handoff e o relacionamento tratam depoimento só real e autorizado.

**(j) Preservação de ativos.** Seção 6.

**(k) Repositório público.** `RISCO_REPOSITORIO_PUBLICO.md`.

## 5. Reconferência financeira (fórmula independente) [E]
Líquido Pix: R$ 47 − 2,49 = **44,51**; R$ 97 com 2,49 + 6,99% = **87,73**; R$ 270 = **248,64**; R$ 19 = 16,51. CPA máximo (sem imposto e custos, ainda "a definir") = líquido. ROAS de equilíbrio = preço ÷ CPA máximo: R$ 47 → 1,06; R$ 97 → 1,11; R$ 270 → 1,09. Equilíbrio no teto de R$ 60/dia: 60 ÷ 44,51 = **1,35 vendas/dia**; com margem alvo de 30%: CPA desejado 31,16 e 1,93 vendas/dia; estresse com 6,99%: 41,22. R$ 19: taxa fixa = 13,1% do preço contra 5,3% em R$ 47; "63% menos por clique" confere (16,51 ÷ 44,51 = 0,371). Todas as linhas da aba "Outros produtos" que conferi batem. A regra de taxa por faixa de preço segue **[NC]**; o resultado financeiro de qualquer decisão depende de imposto, custos e tributos da veiculação, ainda sem valor (A19).

## 6. Preservação de ativos [E, leitura]
- `/mini-mentoria` (`be23f04a`): `updatedAt` 25/11 03:50:57Z, `lastPublishedAt` 03:51:24Z, **antes** dos clones da Fase 03 (05:42Z): não foi alterada pela sessão.
- Rascunhos novos: `/mini-mentoria-a` e `/mini-mentoria-b`: `lastPublishedAt` nulo, **não publicados**; ligados à oferta `0c71eeba` por `offerId` (necessário ao checkout; só valem quando publicados). `/obrigado-mini-mentoria`: tipo `thankYou`, nulo, sem oferta.
- Fluxo `[RASCUNHO] MM47 · Pós-compra`: modo `draft`, gatilho com escopo por `offerId`; não ativo.
- Oferta canônica: `approved`, R$ 47, Pix e cartão 1x, boleto off, entrega só na turma `087479a3`, reembolso 7 dias, gateway sem erro de sincronização; vendedor `pending`, `canSell` true (como o `CLAUDE.md` descreve).
- Ofertas antigas de ferramentas continuam com `providerSyncError` de token (já era conhecido).
- Campanhas Meta: R$ 270, Land Bank e LT47 seguem `PAUSED` [E]; as três ativas do A01 batem com o que o LOG diz que Bruno ligou. Não há registro de escrita no Windsor pelos agentes (nem teria como eu provar a ausência; a evidência é o LOG e a coerência de estados) [NC parcial].
- Clube, Land Bank, Bela, Zaya: não lidos, sem sinal de alteração.

## 7. Tabela final: liberado / liberado com ressalvas / bloqueado

| # | Entrega | Situação | Condição para sair da ressalva |
|---|---|---|---|
| 1 | FUNNEL · funil canônico, automações em rascunho, bump/upsell, relacionamento, textos de WhatsApp | **Liberado com ressalvas** | A08 antes de ligar qualquer fluxo; WhatsApp só texto, nada submetido |
| 1b | FUNNEL · plano de consolidação R$ 97 | **Liberado com ressalvas** (só plano) | Travas de A07 antes de qualquer passo; não executar Passos 1, 6 e 7 sem confirmação escrita do ClickMax |
| 2 | CONVERSION · landing A e B (rascunhos) | **Liberado com ressalvas** | Bruno confere no celular; A14 (A exige "sim" explícito); A15 sugerido |
| 3 | CONVERSION · obrigado, checkout enxuto, checklists | **Liberado com ressalvas** | A06 (frase do e-mail); não publicar antes da compra de teste |
| 4 | CONVERSION · plano A/B (11-testes-ab) | **Liberado com ressalvas** | A20: registrar como "não executar" no teto atual; A09 (variante) |
| 5 | DATA · plano executável e tutorial | **Liberado com ressalvas** | Executar fase 1 só com "aprovado"; resolver A09; texto de privacidade (A12) |
| 6 | DATA · receptor CAPI | **Liberado com ressalvas** | Corrigir A05 antes de qualquer uso; só ligar se a via nativa falhar; A18 opcional |
| 7 | DATA · recuperação 24/11, conciliação, snippet | **Bloqueado** (envio real) | Passo 0 (conferir se o Meta já tem as compras), envio de teste, base legal (A12), exemplo sem dado real (A10). Ferramentas e testes: liberados |
| 8 | CREATIVE · conceitos, roteiro, 7 peças e `COPIES.md` | **Liberado com ressalvas** | Não subir antes de A03 (destino) e A09 (UTM); A16; vídeo depende de Bruno |
| 9 | FINANCE · modelo e teste | **Liberado com ressalvas** | A10 (frase de compradores), A19 (tributos da veiculação), teto único |
| 10 | MARKET · mapa de produtos | **Liberado com ressalvas** | Amostrado (A21); faixas sem número real: ok |
| 11 | TRAFFIC · handoff para o ChatGPT | **Liberado com ressalvas** | A01, A02, A09, A13 resolvidos ou decididos por Bruno antes de ligar gasto; A10 (percentual de tráfego de servidor) |
| 12 | Segurança do repositório (público e histórico) | **Bloqueado** | Decisão de Bruno sobre o plano em fases de `RISCO_REPOSITORIO_PUBLICO.md`; até lá, nada sensível novo no repositório |

## 8. O que o DIRECTOR deve fazer antes de levar a Bruno
1. Pôr A01 a A04 no topo, com a pergunta de decisão em uma linha cada.
2. Mandar A05, A06, A09, A10, A11 aos agentes donos (correção pequena, sem produção).
3. Pedir ao FUNNEL as travas de A07 por escrito.
4. Registrar que a verificação do checkout, da CAPI e da entrega continua [NC] até a compra de teste.
