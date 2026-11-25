# Correções do produto · Mini Mentoria de Estruturação Zion (lista priorizada, antes/depois)

ZION AUDITOR + CONVERSION/DATA · 25/11/2026 · **somente preparação para aprovação de Bruno.** Nada foi aplicado: `docs/` não foi alterado, nada foi mudado no ClickMax (turma, portal, lições, ofertas), Bela/Zaya intactas, nada enviado. Há compradores ativos.
Marcação: **[E]** evidência (arquivo lido ou teste rodado), **[NC]** não confirmado, **[H]** hipótese.
Base: `13-relatorios/VISTORIA_ENTREGAVEIS.md`, `05-funis/ONBOARDING_PROPOSTO.md`, `05-funis/REUNIAO_POS_MENTORIA.md`.
Regra de linguagem (Bruno, 25/11): em qualquer texto comercial usar só **"Acesso à plataforma digital"**, sem prazo de acesso, sem "vitalício", sem "ilimitado". Aplicada neste pacote; os acessos dos compradores existentes não são tocados por nenhum item.

Arquivos deste pacote: `patch/docs/trilha1/...` (arquivos novos, espelhando `docs/`), `patch/diffs/*.diff` (um por ficha), `testes/teste_fichas.js` e os resultados em `testes/RESULTADO_ANTES_DEPOIS.txt`, `gerar_patch.py` (regera o patch a partir de `docs/`), `PLANO_APLICACAO.md`.

## Resumo para decidir (uma tela)

| # | Item | Prioridade | Onde | Quem executa | Quando |
|---|---|---|---|---|---|
| P0-1 | 8 fichas "Faça agora": tirar Land Bank, envio automático e rastreador; texto honesto | P0 | GitHub Pages (`docs/trilha1/`) | Claude copia o patch, Bruno aprova o commit | **Antes de vender mais** |
| P0-2 | Vídeo de boas-vindas (Land Bank, parcerias, agenda): ocultar e pôr texto no lugar | P0 | ClickMax, lição `fcf20da1…` | Bruno (painel) ou Claude com "aprovado" | **Antes de vender mais** |
| P1-1 | Lição "Monte o seu dossiê inicial" e `/dossie/`: texto e envio | P1 | ClickMax + `docs/dossie/` | Bruno decide; depois Claude | Antes de vender (texto) / depois (página) |
| P1-2 | Descrições com Land Bank, reunião, agendar, simulador, mentor de IA | P1 | ClickMax (≈ 25 lições) | Claude com "aprovado" | Depois do P0 |
| P1-3 | Turma "(R$ 97)" renomeada | P1 | ClickMax, turma `087479a3…` | Bruno | Antes de vender |
| P1-4 | Anexar pptx, docx do Kit do Investidor e versões EXEMPLO | P1 | ClickMax, 3 lições | Claude com "aprovado" | Depois do P0 |
| P1-5 | E-books PDF com Land Bank, reunião | P1 | `docs/trilha1/materiais/` (fonte fora do repo) | Regeneração dos PDFs | **Por último** |
| P1-6 | Conferir os 17 vídeos do YouTube | P1 | YouTube (bloqueado no ambiente) | Bruno | Antes de anunciar "17 vídeo-aulas" |
| NF-1 | Descobertas novas desta sessão (rastreador, mentoria, mentor virtual) | P0/P1 | fichas | Bruno decide | Junto com o P0-1 |

---

## P0-1 · As 8 fichas "Faça agora" (arquivos do site)

**Fichas cobertas [E, grep + teste]:** `trilha1/marco-zero` (diagnóstico prévio), `aula1` (Pilar 1), `aula2` (Pilar 2), `aula3` (Pilar 3), `pilar4`, `pilar5`, `pilar6`, `pilar7` (Dossiê). As pastas `aula4`, `aula5`, `aula6` e `territorio` são versões antigas que não estão ligadas às lições; `aula4`, `aula5` e `aula6` têm `ZION_WEBHOOK_URL` vazia e não carregam `_landbank.js` [E]; `territorio` ainda tem um POST para o mesmo host (`DOSSIE_API`) [E] e ficou fora do patch por não estar nas 8 lições (ver "Fora do escopo" no fim).

### O que está no ar hoje [E, `testes/RESULTADO_ANTES_DEPOIS.txt`, bloco ANTES]
1. **Envio automático ao baixar o PDF.** Nas 8 fichas, o clique em "Baixar PDF" dispara `enviarParaZion(...)`: um `POST` para `zion-dossie-aulas.lovable.app/api/dossie` com nome, e-mail e **todas as respostas**, e um registro do aluno como lead no ClickMax (formulário escondido `zx-lead`, chama `api.clickmax.io`). Acontece sem caixa de autorização.
2. **Rastreador do ClickMax em todas as 8 fichas**: `page_view` para `api.clickmax.io` já na abertura da página (GET), antes de qualquer clique.
3. **Botão "Enviar ao banco de áreas da Zion"** e o bloco "Banco de áreas da Zion" na tela do resultado (`_landbank.js`), com caixa de autorização; o clique faz o mesmo POST. Texto de apoio: "A Zion avalia cada caso".
4. **Frase "As respostas ficam só neste aparelho. Nada é enviado."** na tela inicial do diagnóstico (Marco Zero) e "Nada é enviado sem você pedir" nas demais: falsa pelos itens 1 a 3.
5. **Pilares 1 e 5**: bloco "Anexos do seu terreno" (`_anexos.js`): fotos, vídeos e documentos vão ao armazenamento da Zion "para a equipe Zion montar o seu estudo com você".
6. **Pilar 7**: bloco "Envie o seu Dossiê ao banco de áreas da Zion" (`_reuniao.js`: "envie as páginas do seu dossiê para a Zion conhecer o seu projeto") e três parágrafos sobre "o banco de áreas da Zion, uma lista de terrenos…" (tela e PDF).
7. **Pilares 1 e 2** (tela do resultado, quando a leitura é "avançar"): "pode entrar no banco de áreas da Zion, a vitrine de…".

### O que muda (antes → depois)
| Onde | Antes | Depois |
|---|---|---|
| `_landbank.js` | Botão + bloco "Banco de áreas da Zion", caixa de autorização, POST | Arquivo vazio (stub sem código); as 7 fichas deixam de carregá-lo (script removido) |
| 8 × `index.html` | `enviarParaZion(montarPayload(...))` no clique do PDF; `zionLead()`; `ZION_WEBHOOK_URL` apontando ao Lovable | Chamadas removidas; `zionLead` removida; `enviarParaZion` vira função vazia (só porque `window.ZionApp` a exporta); `ZION_WEBHOOK_URL = ""` |
| 8 × `index.html` | Formulário escondido `zx-lead` + iframe `zx-sink` | Removidos |
| 8 × `index.html` | SDK/rastreador ClickMax (`cxs('track','page_view')`, `<noscript>` com `api.clickmax.io`) | Removido (ver NF-1a: perde-se a contagem de visitas dessas fichas) |
| "Nada é enviado" (Marco Zero) / "Nada é enviado sem você pedir" (demais) | Falsa | **Fica como está**: passa a ser verdadeira; o teste prova que não há requisição de saída. A única exceção, o botão opcional "Pedir a leitura do mentor virtual", já avisa na própria seção que envia nome, e-mail, respostas e contas (ver NF-1c) |
| `_anexos.js` (Pilares 1 e 5) | Upload de arquivos + "equipe Zion montar o seu estudo com você" | Texto estático "Depois do Dossiê: solicite a Sessão de diagnóstico estratégico" (sem upload, sem rede) |
| `_reuniao.js` (Pilar 7) | "Envie o seu Dossiê ao banco de áreas da Zion" | Mesmo texto estático da Sessão (sem link; o formulário `aff270f4…` continua em rascunho) |
| Pilar 7, tela e PDF (2×) | "Nós, da Zion, organizamos o banco de áreas da Zion, uma lista de terrenos…" | "Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico com a nossa equipe para apresentar o seu projeto. A sessão é sujeita à análise e à agenda; não é consultoria contínua, e parceria e investimento não são garantidos." |
| Pilar 7, alerta "Conversar com a Zion" | "O banco de áreas da Zion … é um caminho possível" | Título "Sessão de diagnóstico estratégico" + frase curta da Sessão |
| Pilar 7, rodapé do PDF | "…ou entrada no banco de áreas da Zion. A Zion avalia cada caso." | "…venda ou parceria." |
| Pilares 1 e 2, "depois da leitura" | "pode entrar no banco de áreas da Zion…" | Frase curta da Sessão |

Texto-padrão usado (REGRAS_REUNIAO_POS_MENTORIA): "Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico com a nossa equipe para apresentar o seu projeto. Sujeita à análise e à agenda; parceria e investimento não são garantidos." Não há link nem telefone, porque o formulário ainda é rascunho e não pode ser divulgado antes de ser publicado com "aprovado".

### Mantido de propósito (o aluno vê igual)
Salvar no navegador, calcular, gerar PDF, o Dossiê reunindo as páginas salvas no mesmo aparelho, o botão do mentor virtual (clique do aluno, ver NF-1c).

### Risco para compradores ativos
- **Baixo no uso:** o aluno não perde nenhuma função de estudo (salvar, calcular, PDF). Perde o botão Land Bank e o upload de anexos do terreno (Pilares 1 e 5), que o produto não promete. **Quem já enviou algo ao Land Bank pelo botão não é desfeito** (ver LGPD no `PLANO_APLICACAO.md`).
- **Cache:** o navegador do aluno pode manter a versão antiga por algumas horas (GitHub Pages usa cache curto). Sem efeito colateral além de ver o botão antigo por mais um tempo.
- **Dossiê consolidado:** as chaves do `localStorage` não mudam; as respostas já salvas continuam lá [E, o patch não toca nas chaves `zion-t1-*`].
- **Quem estiver no meio de uma ficha:** a ficha recarrega com as respostas salvas; nada se perde.
- **Pedido de leitura do mentor:** o botão continua (NF-1c).

### Reversão
`git revert <commit do patch>` na `main` do repositório devolve os arquivos antigos; o Pages republica em poucos minutos. Nenhum dado de aluno é gravado pelo patch.

### Quem executa e quando
Claude copia `patch/docs/.` para `docs/` e faz o commit **depois do "aprovado" de Bruno**; Bruno faz o teste manual (passo 4 do `PLANO_APLICACAO.md`). **Antes de vender mais.**

### Prova (resumo; saída completa em `testes/RESULTADO_ANTES_DEPOIS.txt`)
Seção "Resultado dos testes" no fim deste arquivo: ANTES 46 falhas (envio comprovado), DEPOIS aprovado, 0 requisições de saída.

---

## P0-2 · Vídeo de boas-vindas `fcf20da1-0475-4a04-b9fd-11553eb74d6a` (módulo 1, `plataforma-v02.mp4`)

**Problema [E, vistoria]:** o primeiro vídeo que o comprador vê mostra "Zion Land Bank", "Seu terreno pode ser uma dessas oportunidades", "Possíveis parcerias e investimentos", "Diagnóstico… você agenda com a equipe Zion" e "banco de áreas". Contradiz a oferta.

**Plano em duas etapas (reversível):**
1. **Ocultar agora.** `lessons_toggle_enabled` com `enabled=false`:
```json
{ "workspaceId": "e87e8ba9-37cf-4c54-9a97-3e4e1b01827a",
  "items": [ { "id": "fcf20da1-0475-4a04-b9fd-11553eb74d6a", "enabled": false } ] }
```
   O arquivo do vídeo não é apagado, a matrícula de ninguém muda. Reversão: o mesmo comando com `enabled=true`. Risco: alunos que já assistiram perdem o item da lista (o progresso salvo fica). [NC] se a lição desabilitada some do progresso percentual da turma; conferir na tela do aluno.
2. **No lugar, a lição de texto "Leia primeiro"** (primeira do módulo Onboarding), texto abaixo. Criar como **desabilitada** (`lessons_create` seguido de `lessons_toggle_enabled enabled=false`, ou criar e desabilitar na hora), revisar no painel, só então habilitar. Sem aviso de portal (aviso dispara e-mail em massa).

**Texto da lição "Leia primeiro" (revisado com a regra de acesso de 25/11):**

Título: **Leia primeiro: o que você comprou e por onde começar**

> **Você está na plataforma da Mini Mentoria de Estruturação Zion.**
> Esta é uma formação digital autônoma. Você estuda no seu ritmo e monta o Dossiê do seu projeto passo a passo. O seu acesso é à plataforma digital.
>
> **O que você tem aqui**
> 9 módulos e 70 conteúdos: aulas gravadas, fichas "Faça agora", e-books por pilar, 2 planilhas de cálculo em branco, o Kit do Investidor (modelos para você preencher), um kit de prompts e o Dossiê, que você gera em PDF no final.
>
> **O que não está incluído**
> Atendimento individual contínuo e consultoria. Calculadoras e simuladores também não fazem parte. Não prometemos investimento, parceria, ocupação, renda ou valorização: o que você leva é o conhecimento e o seu Dossiê.
>
> **Depois do Dossiê: Sessão de diagnóstico estratégico**
> Ao concluir o Dossiê, você pode **solicitar** a Sessão de diagnóstico estratégico com a nossa equipe para apresentar o seu projeto. É a sua oportunidade de buscar parceiros e investimentos para tirar o plano do papel*. Você pede por um formulário, informando o link do PDF do seu Dossiê; nós analisamos e respondemos por e-mail.
> *Gratuita para quem concluiu o Dossiê, sujeita à análise e à agenda. Dura até 30 minutos, é uma apresentação do seu projeto e não é consultoria contínua. Parceria e investimento não são garantidos. Não é a sessão paga do Club, que é outro produto.
>
> **Como você entra**
> Use sempre o **mesmo e-mail da compra**. No primeiro acesso você não precisa ter criado senha antes: siga as instruções da tela de entrada. Se o e-mail de acesso não chegar, olhe a caixa de spam e fale com o suporte. [NC: o passo exato do login nunca foi visto; confirmar na compra de teste de Bruno.]
>
> **Por onde começar, em 4 passos**
> 1. Abra o módulo "Marco Zero" e leia "Comece aqui · Como usar o curso".
> 2. Faça o seu diagnóstico de partida (ficha "Faça agora").
> 3. Siga os Pilares 1 a 7, na ordem. Em cada um: aula, material e a ficha "Faça agora".
> 4. No final, gere o seu Dossiê em PDF.
>
> **Seu Dossiê é seu**
> As fichas ficam salvas no seu aparelho. O Dossiê serve para você organizar o projeto e, se quiser, apresentá-lo a potenciais parceiros e investidores. Esta formação não envia as suas respostas para a Zion.
>
> **Ajuda e reembolso**
> Dúvida de acesso ou de uso? Use a aula "Suporte" ou o WhatsApp +55 48 6137-1061. Se a formação não for para você, peça o reembolso em até 7 dias da compra, pelo mesmo canal.

Diferenças em relação ao `ONBOARDING_PROPOSTO.md`: sai "durante 12 meses" (regra de 25/11); "70 aulas e materiais" vira "70 conteúdos" (vistoria §6); sai o passo "assista ao vídeo de boas-vindas" (vídeo oculto); "A Zion não recebe nem avalia o seu Dossiê" vira "Esta formação não envia as suas respostas para a Zion", frase que **só é verdadeira depois do P0-1 aplicado**. **Por isso a lição "Leia primeiro" só deve ser habilitada depois do P0-1** (e, se o `/dossie/` continuar enviando, ver P1-1).

**Substituto em vídeo (opcional, depois): roteiro de regravação de 60 a 90 s** (voz "nós", telas reais da plataforma em `docs/zion-collection/club/telas/`, sem texto sobre foto, sem pessoas como clientes, **sem** "Land Bank", "receber investimentos", sócio, banco de áreas, nem prazo de acesso):

| Tempo | Fala | Imagem |
|---|---|---|
| 0:00 a 0:10 | "Bem-vindo à Mini Mentoria de Estruturação Zion. Esta é uma formação digital: você estuda no seu ritmo, na plataforma." | Tela de entrada com os módulos |
| 0:10 a 0:30 | "Aqui você aprende o passo a passo para estruturar o seu projeto de hospedagem: aulas gravadas, fichas Faça agora, e-books, planilhas em branco, modelos e um kit de prompts." | Passeio pelos módulos; abrir uma ficha |
| 0:30 a 0:45 | "No final, cada ficha vira uma página do seu Dossiê, que você gera em PDF. O Dossiê é seu, para organizar o projeto e, se quiser, apresentar a potenciais parceiros e investidores." | Tela do Dossiê e do PDF |
| 0:45 a 1:00 | "Quando você concluir o Dossiê, pode solicitar a Sessão de diagnóstico estratégico com a nossa equipe, para apresentar o seu projeto. Ela é sujeita à análise e à agenda, e não garante parceria nem investimento." | Cartela simples, fundo musgo |
| 1:00 a 1:15 | "Comece pelo módulo Marco Zero. Depois siga os Pilares 1 a 7. Em caso de dúvida, use a aula Suporte. E o reembolso em até 7 dias está sempre disponível." | Marco Zero, depois a lista de pilares |

[NC] quem grava (voz humana ou narração de IA com aviso). Depois de gravado e aprovado: `lessons_update` na lição `fcf20da1…` com a nova `url` (ou criar lição nova e manter a antiga oculta), reabilitar. O vídeo antigo fica no host, oculto.

**Risco para compradores ativos:** baixo. Alunos novos deixam de ver o vídeo com Land Bank. **Quem já assistiu** segue com o que viu (não há como desfazer).
**Quem executa:** Bruno no painel ou Claude com "aprovado". **Quando:** antes de vender mais.

---

## P1-1 · Lição "Monte o seu dossiê inicial" `b12e98f3-07f0-4f23-ac28-02211d6dd992` e a página `/dossie/`

**Hoje [E]:** a lição abre `docs/dossie/` (questionário de 3 blocos). A página diz "O seu dossiê vai para a equipe Zion", "A equipe Zion lê o seu dossiê para conhecer o seu projeto", pede matrícula, fotos e documentos, e **envia tudo por POST** (`ENDPOINT`) quando o aluno toca em "Enviar", com caixa de autorização. Há um "agendar" na página (variável `AGENDAR`, aponta para `../agendar/`, a agenda pública antiga). A descrição da lição diz "envie as páginas do seu dossiê para a Zion".

**Atenção, achado desta sessão:** o texto de descrição proposto em `ONBOARDING_PROPOSTO.md` §3 diz "Esta lição não envia nada para a Zion". **Isso só é verdade se a página `/dossie/` deixar de enviar.** Hoje ela envia (com autorização do aluno). Duas saídas, Bruno escolhe:
- **(A) Recomendada:** trocar o link da lição para a ficha do Marco Zero (diagnóstico prévio, já corrigida no P0-1) ou tirar a lição do módulo; `/dossie/` fica fora da turma. Depois a descrição do §3 é verdadeira.
- **(B)** Manter `/dossie/` como envio voluntário ao time, mas **reescrever a página** (não é só trocar a descrição): sem "agendar", sem prometer que "a equipe conhece o seu projeto", dizendo claramente que o envio é opcional e não é a Sessão. Isso é redesenho de página, não preparado aqui.

**Texto da descrição para a opção A (sem prazo de acesso):**
> Responda ao diagnóstico, veja o resultado e guarde a página 0 do seu Dossiê. Tudo fica com você, no seu ritmo. Esta lição não envia nada para a Zion. Quando concluir o Dossiê completo (a ficha do Pilar 7 gera o PDF), você poderá solicitar a Sessão de diagnóstico estratégico, como explicado na lição "Leia primeiro". A sessão é gratuita para quem concluiu o Dossiê, mas é sujeita à análise e à agenda; parceria e investimento não são garantidos.

Payload (a confirmar `moduleId` com `modules_list`, [NC] aqui):
```json
{ "workspaceId": "e87e8ba9-37cf-4c54-9a97-3e4e1b01827a", "id": "b12e98f3-07f0-4f23-ac28-02211d6dd992",
  "moduleId": "<módulo Onboarding>", "description": "<texto acima>", "url": "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha1/marco-zero/" }
```
**Risco:** baixo para a descrição; médio para trocar o link (o aluno que já abriu `/dossie/` e enviou continua com o que enviou). **Reversão:** repor descrição e `url` antigos (guardar o JSON atual da lição antes: `lessons_get`). **Quem:** Claude com "aprovado". **Quando:** o texto, junto com o P0-2; a página `/dossie/`, depois.

---

## P1-2 · Descrições com Land Bank, reunião, agendar, simulador, mentor de IA

Ids da vistoria (`§5` itens 4, 6, 8, 12). Cada linha é um `lessons_update` só de `description` (nenhum `url`, anexo ou matrícula muda). O texto novo de cada uma sai de `lessons_get` na hora de aplicar (não copiei o original aqui por não ter o `moduleId`). Regra de troca:

| Trecho que sai | Entra |
|---|---|
| "enviar ao banco de áreas da Zion", "cadastro no banco de áreas", "Land Bank" | (apagar a frase; se precisar de ponte) "No final, gere o seu Dossiê em PDF." |
| "para a equipe Zion montar o seu estudo com você", "análise pela equipe Zion" | "Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico (sujeita à análise e à agenda)." |
| "agendar", "reunião" (sem a decisão de 25/11) | "solicitar a Sessão de diagnóstico estratégico" |
| "simulador", "mentor virtual" | Só se a ferramenta existir na ficha e funcionar (Pilares 4 a 7 têm simulador na tela [E]; mentor virtual é botão opcional, NF-1c). Não anunciar como entregável nem como "atendimento" |
| qualquer prazo de acesso | "Acesso à plataforma digital" |

| Lição | Id (vistoria) | Item da vistoria |
|---|---|---|
| Comece aqui | `90ccd3db…` | §5.6 |
| Aulas interativas 1 a 8 | `49320a7a…`, `1bdba655…`, `1cdb4a5c…`, `d5255480…`, `9325cb47…`, `cb87b90f…`, `8df647ec…`, `423f4a95…` | §5.6 |
| Mapa de direcionamento | `b625a0e6…` ("…até o cadastro no banco de áreas da Zion") | §5.6 |
| Cadastro (Airtable) | `6a3d7c71…` | §5.6 |
| "Use o mesmo e-mail da inscrição… análise pela equipe Zion" | `e9274de1…` | §5.6 |
| Faça agora com "simulador"/"mentor" na descrição | `0481b040…` (Pilar 1), `d159ed5d…` (Pilar 3), `182d507a…` (Pilar 4), `9895ce66…` (Pilar 5), `b94b3b56…` (Pilar 6) | §5.12 |
| Vídeo 16 ("…ou conversar com a Zion. A Zion avalia cada caso.") | `73b47479…` | §5.8 |
| Dossiê prévio | `b12e98f3-07f0-4f23-ac28-02211d6dd992` | P1-1 |

Os ids de 8 caracteres precisam ser completados com `lessons_list` por módulo antes de aplicar [NC: a vistoria só os registra truncados]. Os 8 ids completos das lições "Faça agora" estão na vistoria §5.2.

**Risco:** baixo (só texto). **Reversão:** guardar o JSON de cada lição (`lessons_get`) antes e repor a `description`. **Quem:** Claude com "aprovado" (cada `lessons_update` é escrita em turma ativa). **Quando:** depois do P0 e do P1-1; fora da janela de pico.

---

## P1-3 · Turma "Plataforma de estruturação (R$ 97)" → "Mini Mentoria de Estruturação Zion"

Turma `087479a3-9d6f-4e1f-a542-c47b347bf5ed`. [NC] se o aluno vê o nome da turma (Bruno confere na tela de um aluno de teste). Payload (só o nome; **não** enviar `contentsAccessTime`, `contentsToAdd` nem `contentsIdsToRemove`, para não mexer em prazo nem em conteúdo):
```json
{ "workspaceId": "e87e8ba9-37cf-4c54-9a97-3e4e1b01827a",
  "id": "087479a3-9d6f-4e1f-a542-c47b347bf5ed",
  "name": "Mini Mentoria de Estruturação Zion" }
```
**O que muda:** o rótulo. **Risco:** nenhum acesso muda; os dois compradores de R$ 97 mantêm o acesso [E, regra de Bruno]. Referências por nome em automações [NC]: antes de renomear, conferir fluxos e segmentos que filtrem por nome da turma (os ids não mudam). **Reversão:** `classrooms_update` com o nome antigo. **Quem:** Bruno no painel (Turmas, editar nome) ou Claude com "aprovado". **Quando:** antes de vender.

---

## P1-4 · Anexar os arquivos que as descrições prometem

Os arquivos existem no host (HTTP 200 na vistoria). `lessons_update` com `lessonAttachmentsToCreate` (não substitui os anexos existentes):

| Lição | Id | Anexos a criar (URL pública) |
|---|---|---|
| Kit do Investidor | `78a3f24f-0392-4d48-94e8-6cae4b51c72b` | "Modelo de Pitch deck (pptx)": `https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha1/materiais/kit-investidor/Pitch-Deck-Zion-MODELO.pptx` · "Modelo de Teaser e One-pager (docx)": `…/trilha1/materiais/kit-investidor/Teaser-e-One-Pager-Zion-MODELO.docx` |
| Planilha 1 (Orçamento de Abertura) | `d3ae8d55-c339-4241-aa70-ec1dc4252894` | "Versão com exemplo (dados fictícios)": `…/trilha1/materiais/planilhas/Orcamento-de-Abertura-Zion-EXEMPLO.xlsx` |
| Planilha 2 (Estudo de Massas e Viabilidade) | `05c0bdc1-7d00-48f8-a8d3-58b6bb973576` | "Versão com exemplo (dados fictícios)": `…/trilha1/materiais/planilhas/Estudo-de-Massas-e-Viabilidade-Zion-EXEMPLO.xlsx` |

Exemplo de payload (Kit):
```json
{ "workspaceId": "e87e8ba9-37cf-4c54-9a97-3e4e1b01827a", "id": "78a3f24f-0392-4d48-94e8-6cae4b51c72b",
  "moduleId": "<módulo Pilar 7>",
  "lessonAttachmentsToCreate": [
    { "name": "Modelo de Pitch deck (pptx)", "url": "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha1/materiais/kit-investidor/Pitch-Deck-Zion-MODELO.pptx" },
    { "name": "Modelo de Teaser e One-pager (docx)", "url": "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha1/materiais/kit-investidor/Teaser-e-One-Pager-Zion-MODELO.docx" } ] }
```
Antes de anexar: abrir cada arquivo e conferir que não contém Land Bank, reunião, sócio garantido nem prazo de acesso [NC: esta sessão não abriu o conteúdo dos 4 arquivos; a vistoria só confirmou que existem]. O texto "dados fictícios" no nome da versão EXEMPLO está de acordo com a regra do repositório.
**Risco:** baixo (adiciona itens; nada é removido). **Reversão:** `lessonAttachmentsToDelete` com os ids criados. **Quem:** Claude com "aprovado". **Quando:** depois do P0 (e depois de conferir os 4 arquivos).

---

## P1-5 · E-books PDF com Land Bank e reunião (a regeneração é por último)

Fonte dos PDFs: `docs/trilha1/materiais/*-ebook.pdf` (publicados e anexados nas lições de e-book). Os arquivos de origem dos e-books (HTML/Markdown) [NC] não foram localizados nesta sessão; a regeneração parte deles. Mapa para o editor (a vistoria registra 6 menções no total, §5.7; esta sessão **não** reabriu os PDFs, então página e trecho exatos ficam por confirmar):

| E-book | Lição (id) | Trecho a trocar (vistoria) | Página [NC] |
|---|---|---|---|
| Marco Zero | `6063c501…` | citação do Land Bank Zion | extrair com `pdftotext` e `grep -n "Land Bank"` |
| Pilar 1 | `475d900d…` | idem | idem |
| Pilar 2 | `09e8eac4…` | idem | idem |
| Pilar 3 | `da5c67ec…` | idem | idem |
| Pilar 4 | `09ea86f8…` | idem | idem |
| Pilar 5 | `8abb60e2…` | idem | idem |
| Pilar 6 | `e620975e…` | idem | idem |
| Pilar 7 | `d2cc48fd…` | "A reunião e a lista do Land Bank Zion são caminhos possíveis, não promessas" e questão de quiz sobre estar na lista | idem |

Receita para listar página e trecho (comando para quem for editar, somente leitura):
`for f in docs/trilha1/materiais/*-ebook.pdf; do echo "== $f"; for p in $(seq 1 $(pdfinfo "$f" | awk '/Pages/{print $2}')); do pdftotext -f $p -l $p "$f" - | grep -inE "land bank|banco de áreas|reunião|equipe zion" | sed "s/^/p.$p: /"; done; done`

Também: e-books de aprofundamento `docs/escola/d01..d05` remetem a "D06 · Estruturação Jurídica, Societária e Land Bank" (vistoria §5.10); e o tutorial do Pilar 7 (mp4 `f3cdce4a…`) termina com "o cadastro no Zion Land Members" (§5.9); os dois ficam na lista de regravação/regeneração.
Substituição proposta: onde hoje se lê "reunião" ou "lista do Land Bank", "Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico (sujeita à análise e à agenda; parceria e investimento não são garantidos)". Quiz do Pilar 7: trocar a questão sobre "estar na lista" por uma sobre o que a Sessão é e não é.
**Risco para compradores ativos:** quem já baixou o PDF mantém a versão antiga; trocar o arquivo no host muda para quem baixar depois. Se a URL for a mesma, a lição não precisa de `lessons_update`. **Reversão:** `git revert`. **Quem:** produção dos e-books (Claude, com a fonte) + "aprovado". **Quando:** **por último**, depois de P0, P1-1 a P1-4 e do teste manual de Bruno.

---

## P1-6 · Os 17 vídeos do YouTube

[NC]: `youtu.be` e `www.youtube.com` voltam 403 no proxy deste ambiente; nunca foram abertos pela vistoria. Quem confere é Bruno (ou outra máquina). Para cada um: abre? está **público ou não listado** (não privado)? duração? Depois preencher `duration` na lição (`lessons_update`, campo `duration`, formato texto). Os ids dos 17 itens `video` vêm de `lessons_list` por módulo (Marco Zero 2, Pilares 1 a 3 e 5 a 7: 2 cada, Pilar 4: 3, sendo 1 extra).
Tabela para Bruno preencher: `item | URL | abre (s/n) | visibilidade | duração | cita Land Bank, reunião ou prazo de acesso (s/n)`.
O terceiro vídeo do Pilar 4 (extra) e o Vídeo 16 (`73b47479…`, descrição "ou conversar com a Zion") merecem atenção. **Até conferir, não anunciar "17 vídeo-aulas"; usar "vídeo-aulas e tutoriais em vídeo"** (vistoria §9). **Quando:** antes de publicar o cartão "O que você recebe" com números.

---

## NF-1 · Descobertas novas desta sessão (não estavam na vistoria)

**a) Rastreador do ClickMax nas 8 fichas.** Cada ficha chamava `api.clickmax.io` (GET `page_view`) ao abrir, de um projeto de rastreamento de nome pessoal (`projeto-de-bruno-…`). O patch o remove, porque "nada é enviado" não seria verdadeiro com ele. **Custo:** perde-se a contagem de visitas dessas 8 fichas no ClickMax. **Decisão de Bruno:** aceitar a perda (recomendado: não há consentimento nem aviso ao aluno) ou, se quiser a métrica, trocar o texto por "não enviamos as suas respostas; contamos apenas as visitas à página" e manter o SDK (o patch teria de ser regerado com essa opção; `gerar_patch.py` tem a regra isolada e é fácil de ajustar).

**b) O diagnóstico do Marco Zero (resultado) vende outra coisa.** O bloco "Os seus próximos passos com a Zion" (tela e PDF) oferece "mentoria em grupo ou individual com o Bruno Chaerk" (botão do WhatsApp com o resumo das respostas pré-escrito), "O Bruno e a equipe Zion olham o seu caso de perto", "O seu Dossiê revisado pela equipe Zion", "Acompanhamento do Bruno sobre o seu terreno" e a venda da Bubble ("o valor e a condição exclusiva chegam no seu WhatsApp"). Isso contradiz "sem atendimento individual contínuo" e "sem consultoria" e leva o comprador a outra oferta dentro de um produto de R$ 47. **Não patcheado** (pode ser upsell desejado por Bruno): decisão dele entre (1) manter como está e declarar na oferta, (2) retirar o bloco, ou (3) trocar pelo texto da Sessão. Preparo a versão que ele escolher.

**c) "Mentor virtual".** Os Pilares 1 a 7 têm o botão "Pedir a leitura do mentor virtual" (cliente aperta; `POST` para `zion-dossie-aulas.lovable.app/api/feedback` com nome, e-mail, respostas e contas; a seção avisa disso antes do clique). Não é envio automático e não foi alterado. Mas é um envio de dado pessoal a um serviço externo (Lovable) e a descrição dos materiais diz "mentor de IA" (a vistoria pediu para não anunciar). **Decisão de Bruno:** (1) manter (opt-in, com aviso) e documentar na política de privacidade; (2) desligar: `FEEDBACK_URL = ""` em cada ficha faz a seção mostrar "Disponível em breve" (mudança de uma linha por arquivo; não incluída no patch para não decidir por ele). O teste mostra exatamente 1 POST e só depois do clique.

**d) "A Zion avalia cada caso" continua em 17 lugares** (rodapés e dicas dos Pilares 4 a 6 e do Marco Zero, `aula3` linha 724 "fale com a Zion", alertas do Pilar 7). Sem Land Bank, a frase deixa de ter objeto: é só um aviso genérico. Não é falsa, mas é ambígua. Sugestão: trocar por "Parceria e investimento não são garantidos" numa rodada de texto (P1, sem urgência). Não incluída no patch.

**e) Google Fonts e jsPDF (cdnjs) continuam sendo carregados** (GET sem dados do aluno; expõem o IP do aluno a Google e Cloudflare). Padrão da web, não é envio das respostas. Se Bruno quiser "zero terceiros", hospedar as fontes e o jsPDF em `docs/` (tarefa à parte).

### Fora do escopo desta entrega (listado para não se perder)
`docs/trilha1/territorio/` (Leitor de Território) ainda faz POST ao mesmo host e tem o botão Land Bank, mas não é uma das 8 lições [E]. `docs/trilha1/apresentacao/_motor/jornada.js`, `docs/zion-collection/`, `docs/ficha`, `docs/diagnostico`, `docs/jornada-desenvolvimento`, `docs/previa/landbank`, `docs/agendar`, `docs/reuniao-direta`, `docs/land-members`, `docs/parceiro-zion` e as páginas `lancamento/` referenciam `lovable`, `api.clickmax.io` ou Land Bank: são outros produtos/funis (Land Bank, Zion Collection, Clube), **regra do CLAUDE.md: não mexer**. Se alguma delas for aberta por alguém da turma da Mini Mentoria, tratar à parte.

---

## Resultado dos testes

Comando (da raiz do repositório): `NODE_PATH=$(npm root -g) node zion-sales-engine/15-correcoes-produto/testes/teste_fichas.js ambos`. Playwright em 390×844; jsPDF do pacote npm servido localmente; qualquer host que não seja `127.0.0.1` é interceptado e respondido localmente (nenhum dado saiu de verdade; respostas fictícias); as 8 fichas rodam em sequência no mesmo navegador (o Dossiê lê as páginas salvas). Saída completa em `testes/RESULTADO_ANTES_DEPOIS.txt` (rodada de 25/11/2026).

| Ficha | ANTES: bloco/botão Land Bank | ANTES: requisição de saída ao baixar o PDF | DEPOIS: Land Bank | DEPOIS: saída ao baixar o PDF | DEPOIS: PDF | Salvo no navegador |
|---|---|---|---|---|---|---|
| Marco Zero | 1/1 | POST lovable.app | 0/0 | 0 | 1 p. | sim |
| Pilar 1 | 1/1 | POST lovable.app | 0/0 | 0 | 4 p. | sim |
| Pilar 2 | 1/1 | POST lovable.app | 0/0 | 0 | 4 p. | sim |
| Pilar 3 | 1/1 | POST lovable.app | 0/0 | 0 | 4 p. | sim |
| Pilar 4 | 1/1 | POST lovable.app | 0/0 | 0 | 4 p. | sim |
| Pilar 5 | 1/1 | POST lovable.app | 0/0 | 0 | 6 p. | sim |
| Pilar 6 | 1/1 | POST lovable.app | 0/0 | 0 | 6 p. | sim |
| Pilar 7 (Dossiê) | 1/1 | POST lovable.app | 0/0 | 0 | 15 p. | sim |

**ANTES (arquivos originais): 46 falhas de critério, o que comprova o achado da vistoria.** Nas 8 fichas: o clique em "Baixar PDF" gera `POST` ao host do Lovable e, na abertura, `GET` a `api.clickmax.io` (rastreador); o botão "Enviar ao banco de áreas da Zion" também faz `POST` (testado nas 8); a tela do resultado tem "banco de áreas" e "Enviar ao"; Pilares 1 e 5 têm upload de anexos com "para a equipe Zion montar o seu estudo"; o código servido contém `lovable.app`, `api.clickmax.io`, `zx-lead`.

**DEPOIS (patch sobre `docs/`): APROVADO, 0 falhas.** Em todas as 8 fichas: carrega sem erro de JS, preenche e chega ao resultado, salva no navegador, gera PDF válido (`%PDF-`), **0 requisições de saída ao baixar o PDF e 0 na carga e no preenchimento** (só os GET estáticos permitidos de fonte e jsPDF, 16, que o teste serve localmente); nenhum bloco ou botão Land Bank; bloco de anexos sem campo de upload; a tela do resultado sem "Land Bank", "banco de áreas", "Enviar ao", "monta o seu estudo", "vai para a equipe"; o código servido de `_landbank.js`, `_anexos.js`, `_reuniao.js` e do Marco Zero sem nenhum termo antigo nem `fetch`. Frase "Nada é enviado" (Marco Zero) e "Nada é enviado sem você pedir" (demais): continuam e agora são verdadeiras para carga, preenchimento, salvar e PDF.

**Resíduo conhecido e declarado (não é falha do teste):** nos Pilares 1 a 7 o código ainda contém o `fetch POST` do botão opcional "Pedir a leitura do mentor virtual" (`FEEDBACK_URL`, `lovable.app/api/feedback`). O teste clica nele e registra **exatamente 1 POST por ficha, só depois do clique** (fica fora do critério de aprovação, ver NF-1c). As 7 "falhas" que apareceram na primeira rodada vinham dessa linha e o teste foi ajustado para listá-la à parte, e não para ignorá-la.

**Limites dos testes:** dados fictícios; o robô responde às perguntas de forma genérica (primeira opção, números como 100, 5 ou 1), então valida o fluxo, não a qualidade do texto do resultado. Não testei o ClickMax, a área de membros nem a lição vista pelo aluno. Um teste manual de Bruno continua necessário (`PLANO_APLICACAO.md` seção 2). Na rodada ANTES o navegador acumulou 1 chave extra de `localStorage` por ficha em relação ao DEPOIS; não identifiquei qual [NC].
