# RISCO DO REPOSITÓRIO PÚBLICO E DO HISTÓRICO · ZION AUDITOR · 25/11/2026

**Análise somente de leitura. Nada foi executado, apagado, reescrito ou tornado privado.** Este arquivo lista tipos, caminhos e commits; **não reproduz** nenhum dado sensível. Decisões de visibilidade e de reescrita de histórico são só de Bruno. Marcação: **[E]** verificado agora, **[H]** hipótese ou estimativa, **[NC]** não confirmado.

Limite: a API do GitHub para configurações (Pages, visibilidade) não é acessível daqui [E, 403 do proxy]; a visibilidade pública, o Pages ativo e o tamanho vêm de `repos/…` (consulta básica que passou) e da própria documentação do projeto.

## 1. O que o repositório e o histórico expõem

Repositório `bchaerk-creator/zion-hotel-ai-developer`: **público**, GitHub Pages ativo, cerca de 2,7 GB no GitHub (`.git` local 2,8 GB), 3.644 arquivos rastreados na `main`, 897 commits, **37 branches remotas** (todas públicas) [E].

| # | Categoria | Onde (tipo e caminho) | Commits/branches afetados | Gravidade |
|---|---|---|---|---|
| 1 | **Documentos jurídicos de terceiros** (contrato e acordo de prestação de serviço, recibos, checklist de regularização), com identificação fiscal de pessoas e empresas e valores | `docs/juridico/*.md/.docx/.pdf` | existem na branch remota `claude/contrato-prestacao-zeladoria-qc9p79` (commits como `4fe9e26`, `32d0e79`, `f38f21a`, `9b91574`, `3c7799c`, `f327f81`, `7120dac`, `08bbdc7`). Não estão na `main` atual [E] | **P0** (dado de terceiros; LGPD) |
| 2 | **Relatórios com valores reais** de campanhas, vendas e ofertas | `zion-sales-engine/13-relatorios/` (8 arquivos: G, H, I, J, HANDOFF, CONSOLIDADO, FINAL, README) | entraram no commit `7d10efb`, saíram do working tree em `ff74df0`; **continuam em `7d10efb` e na história da `main`** [E]. Contagem de valores em reais fora do catálogo de preços: dezenas (aprox. 16 só no relatório final) | **P0/P1** (regra do projeto: sem número real em repositório público) |
| 3 | **Produtos pagos baixáveis sem compra** | `docs/p/adbc67069af26ae0/*` (56 pastas, ~447 MB: planilhas, PDFs, guias, capas); `producao/**/dist/` e fontes dos produtos | `main` e Pages | **P1** (perda de receita; pirataria). O endereço é "discreto, não secreto" (`CLAUDE.md` §3); `Disallow: /p/` só orienta robôs educados |
| 4 | **E-mail pessoal do titular** | 1 ocorrência em `docs/zaios/ENTREGAS_VALIDACAO_ACADEMY.md:21` (histórico: `09a34e0`, `e7c7c4f`) e o mesmo e-mail como suporte da oferta no ClickMax (não é Git) | `main` | P2 |
| 5 | Telefone | só o WhatsApp de suporte da marca (público por desenho). Nenhum celular de cliente [E] | — | OK |
| 6 | E-mails de cliente/lead | nenhum encontrado na `main`; os demais são de exemplo (`exemplo.com`, `example.com`, `email.com`) ou institucionais [E]. Histórico: varredura por provedores comuns achou 13 commits, todos nos casos 1 e 4 e em skills/contratos [E] | — | OK com ressalva do item 1 |
| 7 | Segredos (token, chave, senha, chave privada) | **nenhum** no working tree nem no histórico pelo padrão de tokens da Meta, GitHub, Anthropic, AWS, Google, Slack e chaves privadas [E]; `.env` está no `.gitignore`; só `*.example` e `TOKEN_FALSO_DE_TESTE` | — | OK |
| 8 | Dados de comprador/lead (CSV de vendas, listas) | nenhum arquivo com esse nome ou conteúdo no histórico [E]; apenas `compras.csv.example` fictício. O `.gitignore` **não** cobre `compras.csv`/`*.enviados` (A11) | — | P2 (prevenção) |
| 9 | Ids de plataforma (oferta, página, campanha, pixel, conta de anúncio, portal, turma) | muitos, em `CLAUDE.md`, `producao/**/OFERTA.md`, `zion-sales-engine/**` | `main` | P2: não são segredo, mas mapeiam a operação; o próprio pixel é público no navegador |
| 10 | Estratégia comercial interna (modelo financeiro com parâmetros, plano de campanha, handoff) | `zion-sales-engine/**` | `main` | P2: concorrente vê a lógica de preço, teto e testes |
| 11 | Fornecedores e projetos de obra (RFQ, briefing) | `projects/zion-glamping-line/**` | branch remota `claude/zion-cocoon-zenith-design-68cw2z` e outras | P2 [NC: conteúdo não aberto a fundo] |
| 12 | Peso do repositório | `docs/` ~1,5 GB (vídeos, trilhas, anúncios) | — | P2: o Pages tem limite de tamanho publicado (cerca de 1 GB [H]); risco de falha de deploy |

## 2. O que a visibilidade pública sustenta hoje (e o que quebra se mudar)

Dependências do endereço `https://bchaerk-creator.github.io/zion-hotel-ai-developer/…`:

- **Entregas dos compradores.** Cada oferta de ferramenta tem arquivos (planilhas, PDFs) e uma página de acesso apontando para `p/adbc67069af26ae0/<produto>/` [E, `offers_get` da Ferramenta 17: 4 arquivos e 1 link por oferta]. O `CLAUDE.md` lista **23 pastas distintas** ligadas a ofertas e a Zion Collection 06 e o produto terra-capital usam mais. Estimativa [H]: **cerca de 23 a 26 ofertas e, nelas, de 100 a 130 URLs** (4 a 5 por oferta). A contagem exata exige `offers_get` em cada oferta (cerca de 30 chamadas de leitura), que não fiz.
- **Aulas do portal** da Zion Collection 06 apontam para `p/…/zc06-*` (documentado no `CLAUDE.md`).
- **Imagens do portal** `3ef7a340` (logo, capa, banner de login) e **das páginas de venda** (logo, fotos reais, telas da plataforma): 103 arquivos de `producao/` e `zion-sales-engine/` e 40 de `docs/` citam o endereço [E, contagem de arquivos].
- **Artes dos anúncios** (`docs/ads/mm47-fase03/` e anteriores) e o site institucional (`docs/`).
- **Rascunhos novos** A e B da landing: fotos e telas vêm do mesmo endereço.

No plano gratuito o Pages exige repositório público [dado do enunciado]. Tornar o repositório privado sem outra hospedagem: **as entregas dos compradores passam a dar 404, o portal perde as imagens, as páginas de venda perdem logo e fotos e os anúncios perdem as artes.** É perda de entrega para quem já pagou: **não fazer sem a migração dos links**.

## 3. Alternativas

| Opção | O que é | Prós | Contras | Custo [H, confirmar antes] | Tempo [H] | O que quebra |
|---|---|---|---|---|---|---|
| **A. Tornar privado e pagar o Pages** | plano pago do GitHub com Pages em repositório privado | menor esforço técnico; mantém endereços | custo mensal; **o endereço do Pages continua público** (só o código fica privado); o histórico passa a ser privado mas o que já foi copiado, indexado ou bifurcado fica | mensalidade do plano (consultar preço atual) | horas | nada, se o plano habilitar Pages privado; **[NC]** se mantém o mesmo endereço |
| **B. Repositório público mínimo + repositório privado novo** | `docs/` só com o que precisa ser público (logo, fotos, artes, páginas de acesso); `producao/`, `zion-sales-engine/`, `escola/`, `testes/`, `projects/` num repositório privado novo; o público passa a ser repositório novo "limpo" | resolve o código e o conteúdo interno; custo zero; histórico do público começa limpo | trabalho de separar e de reapontar links; o repositório antigo ainda existe até ser apagado ou privatizado | R$ 0 | 1 a 3 dias | links de entrega, se os caminhos mudarem |
| **C. Hospedar ativos em Cloudflare Pages ou Netlify** (planos gratuitos) | publicar só `docs/` (ou o mínimo) lá; o repositório vira privado | repositório privado sem custo; boa banda; domínio próprio possível | limites de arquivos e tamanho do plano gratuito [NC: conferir]; os endereços mudam, portanto **trocar todos os links**; o conteúdo continua aberto por URL | R$ 0 no plano gratuito | 1 a 2 dias + janela de troca | todos os links do item 2 até serem trocados |
| **D. Entregas dentro do ClickMax** (arquivo na oferta, drive ou área de membros) | `offers_add_file_delivery` com arquivo do armazenamento do ClickMax, ou lições na área de membros; o comprador baixa pelo ClickMax | **fecha o buraco de pirataria** (item 3); entrega presa à compra; some a dependência do Pages para o que é pago | `offers_add_file_delivery` hoje usa URL pública; upload de arquivo pelo painel (Bruno) ou pelo drive do ClickMax [NC: se gera link protegido]; esforço manual por produto; mexe em oferta existente | R$ 0 (limite de armazenamento do plano [NC]) | 2 a 5 dias para ~23 ofertas | nada, se feito oferta por oferta com teste |
| **E. Reescrever histórico (`git filter-repo`) e forçar push** | remove arquivos e valores de todos os commits e branches | elimina o conteúdo do histórico do repositório | **destrutivo e irreversível** para quem não tiver espelho; muda todos os hashes; invalida clones, branches e PRs; o GitHub guarda objetos em cache por um tempo (pedir limpeza ao suporte); não apaga o que já foi copiado, indexado ou bifurcado; exige coordenar as 37 branches | R$ 0 | 0,5 a 1 dia + conferência | todos os clones e referências a commits; **só Bruno decide** |

Pontos comuns: (i) tornar privado ou limpar **não desfaz exposição que já ocorreu** (cópias, buscadores, Wayback, bifurcações, clones locais); trate o conteúdo dos itens 1 e 2 como já divulgado e avalie o dever de comunicação aos titulares dos dados do item 1 com orientação jurídica; (ii) não há segredo a rotacionar (item 7), então a emergência é de conteúdo e de receita, não de credencial.

## 4. Recomendação em fases (cada uma com reversão)

Princípio: **primeiro parar de piorar, depois proteger quem pagou, depois fechar o que foi exposto.**

**Fase 0 · Agora (sem tocar em nada que funciona).** [Executa: Bruno decide; Claude prepara]
1. Congelar: nenhum arquivo com dado sensível novo no repositório; os agentes seguem a regra atual.
2. Espelho de segurança: `git clone --mirror` do repositório (todas as branches) para um local privado do Bruno **antes** de qualquer mudança. Reversão: não há o que reverter (só cópia).
3. Inventário exato: ler `offers_get` de todas as ofertas e listar as URLs ligadas ao endereço do Pages (arquivo fora do repositório). Reversão: n/a (leitura).
4. Decidir o item 1: confirmar com orientação jurídica se os documentos de terceiros da branch `claude/contrato-prestacao-zeladoria-qc9p79` precisam de comunicação; remover a branch remota (`git push origin --delete`, só com "aprovado") e pedir ao suporte do GitHub a limpeza do cache de objetos. Reversão: o espelho da Fase 0 restaura a branch.

**Fase 1 · Proteger a receita e o conteúdo interno (1 a 3 dias).** [Executa: Claude monta, Bruno aprova]
1. Criar repositório **privado** novo e mover para ele `producao/`, `zion-sales-engine/`, `escola/`, `testes/`, `projects/`, `.claude/` e o histórico relevante. O repositório atual **não** é alterado nesta fase. Reversão: apagar o repositório novo.
2. No repositório público manter apenas `docs/` necessário ao ar. Ainda sem trocar links.

**Fase 2 · Tirar as entregas pagas do endereço aberto (2 a 5 dias).** [Executa: Bruno no painel; Claude confere por leitura]
1. Para cada oferta, subir os arquivos ao ClickMax (Produtos → oferta → entrega de arquivo) ou criar a lição na área de membros, **testar com a conta de teste**, e só então remover a entrega antiga (`offers_add_*` e remoção são ação em oferta existente: **"aprovado" a cada lote**). Começar por 1 oferta como piloto, depois lotes de 5.
2. Manter o endereço antigo no ar durante a transição; quem já comprou continua baixando. Reversão: religar a entrega antiga (a pasta no Pages segue intacta até a Fase 4).
3. Não remover acesso de nenhum comprador; a troca é de **origem do arquivo**, não de quem tem direito (regra do projeto).

**Fase 3 · Hospedar o que precisa ser público fora do repositório (1 a 2 dias).** [Executa: Claude prepara; Bruno cria a conta e o domínio]
1. Publicar logo, fotos reais, telas e artes dos anúncios em Cloudflare Pages ou Netlify (plano gratuito) ou no armazenamento de imagens do ClickMax. Conferir limites do plano antes.
2. Reapontar as imagens do portal `3ef7a340` e das páginas de venda, **página por página, em cópia/rascunho primeiro** (nunca importar sobre página publicada sem backup). Reversão: manter o endereço antigo até a Fase 4.

**Fase 4 · Fechar (só quando as Fases 2 e 3 estiverem provadas, e só com decisão de Bruno).**
- Opção leve: tornar o repositório privado (Pages sai do ar; as entregas e imagens já foram migradas).
- Opção forte: `git filter-repo` para remover do histórico os itens 1 e 2 e, se quiser, o item 3; **destrutiva**; fazer em cópia, coordenar as 37 branches, pedir ao GitHub a limpeza do cache. Reversão: só pelo espelho da Fase 0.
- Nunca antes de a contagem de links ligados ter chegado a zero.

**Gatilho de parada em qualquer fase:** comprador sem acesso, página de venda quebrada ou entrega com 404 → voltar ao estado anterior da fase (o endereço antigo continua válido até a Fase 4).

## 5. Perguntas a Bruno
1. Aprova a Fase 0 (espelho, inventário de links e consulta jurídica sobre os documentos de terceiros)?
2. Prefere o caminho B+D+C (custo zero, mais trabalho) ou A (custo mensal, menor esforço, mas o endereço continua público)?
3. Aceita adiar qualquer reescrita de histórico até depois das Fases 2 e 3?
4. Quem executa as entregas no painel do ClickMax: ele ou alguém designado?
