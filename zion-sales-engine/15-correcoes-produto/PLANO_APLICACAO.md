# Plano de aplicação das correções do produto (para aprovação de Bruno)

ZION AUDITOR + CONVERSION/DATA · 25/11/2026 · **nada foi aplicado.** Este plano só vale depois do "aprovado" de Bruno, item por item. Detalhe de cada correção, antes/depois e risco: `CORRECOES_PRODUTO.md`. Há compradores ativos: nenhum passo remove acesso, matrícula ou conteúdo.
Regra de linguagem de Bruno (25/11): só "Acesso à plataforma digital"; sem prazo de acesso, sem "vitalício", sem "ilimitado". Mantidos: R$ 47, pagamento único, sem mensalidade, garantia de 7 dias.

## 0. Ordem e por quê

| Ordem | O quê | Onde | Quem | Reversão |
|---|---|---|---|---|
| 1 | Aprovar o patch das fichas e fazer o commit | GitHub (`docs/trilha1/`) | Bruno aprova, Claude executa | `git revert` |
| 2 | Teste manual de Bruno com a conta dele | navegador + celular | Bruno | (sem mudança) |
| 3 | Ocultar o vídeo de boas-vindas | ClickMax, lição `fcf20da1…` | Bruno (painel) ou Claude | reabilitar a lição |
| 4 | Criar a lição "Leia primeiro" **desabilitada**, revisar, habilitar | ClickMax, módulo Onboarding | Bruno (painel) | desabilitar/apagar a lição nova |
| 5 | Renomear a turma | ClickMax, turma `087479a3…` | Bruno (painel) | voltar o nome |
| 6 | Textos das lições e anexos (P1) | ClickMax | Claude com "aprovado" | repor o JSON salvo |
| 7 | Regenerar os e-books | repositório | Claude | `git revert` |

A lição "Leia primeiro" afirma "Esta formação não envia as suas respostas para a Zion". Essa frase só é verdadeira com o passo 1 aplicado; por isso o passo 4 vem depois do 1 e do 2.

## 1. Aplicar o patch das fichas (repositório)

Pré-condição: "aprovado" de Bruno para o P0-1. Quem executa: Claude.

1. `git pull --rebase origin main`.
2. Rodar de novo, para garantir que o patch parte do `docs/` atual: `python3 -I zion-sales-engine/15-correcoes-produto/gerar_patch.py` (aborta se alguma frase esperada mudou).
3. Rodar o teste: `NODE_PATH=$(npm root -g) node zion-sales-engine/15-correcoes-produto/testes/teste_fichas.js depois` (precisa dar **APROVADO**).
4. Copiar: `cp -r zion-sales-engine/15-correcoes-produto/patch/docs/. docs/` (muda 8 `index.html` e `_landbank.js`, `_anexos.js`, `_reuniao.js`, todos em `docs/trilha1/`; nada fora dessa pasta).
5. `git diff --stat docs/` deve listar exatamente esses 11 arquivos. Se aparecer outro, parar.
6. Commit curto em pt-BR, só desses arquivos (`git add docs/trilha1`), mensagem sugerida: "Fichas Faça agora: sem envio de dados, sem Land Bank, texto da Sessão de diagnóstico". Terminar com as duas linhas de atribuição do repositório. `git push origin main`.
7. **Aguardar o GitHub Pages** (costuma levar de 1 a 5 minutos; conferir em Actions o fim do "pages build and deployment").
8. Conferir no ar (de outra máquina, sem cache): `curl -s https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha1/marco-zero/ | grep -c "api.clickmax.io"` deve dar 0; idem `lovable.app` (nas fichas dos Pilares 1 a 7 ainda aparece 1 vez, a do mentor virtual, ver NF-1c) e `_landbank.js` (0).

**Reversão (a qualquer momento):** `git revert <hash>` e `git push`. Em 1 a 5 minutos as fichas voltam ao estado anterior.

## 2. Teste manual com a conta de Bruno (antes de mexer no ClickMax)

No celular (ou com a janela estreita) e em janela anônima, com a conta de aluno de Bruno:
1. Abrir uma ficha pela plataforma, ou direto pela URL pública, e conferir: não há botão "Enviar ao banco de áreas da Zion" nem caixa "Banco de áreas da Zion" na tela do resultado.
2. Abrir as ferramentas de desenvolvedor do navegador, aba Rede (Network), e **baixar o PDF**: não deve aparecer nenhuma chamada para `lovable.app` nem `clickmax.io`. (No celular: usar o computador com a mesma página.)
3. Fazer as 8 fichas em sequência no mesmo navegador (a vistoria pediu esse teste manual de ponta a ponta) e baixar o Dossiê do Pilar 7: conferir que reúne as páginas, que o texto fala da Sessão de diagnóstico estratégico (sem "banco de áreas") e que o PDF abre.
4. Nos Pilares 1 e 5, o bloco "Anexos do seu terreno" deve ter virado só o texto "Depois do Dossiê: solicite a Sessão…", sem botão de enviar arquivos.
5. Se algo falhar: avisar o Claude; o revert do passo 1 resolve.

## 3. O que Bruno executa no painel do ClickMax

Workspace Bruno's Workspace (`e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`). Antes de qualquer mudança, **anotar o estado atual** (print ou exportação) da turma e das lições, para poder desfazer.

### 3.1 Ocultar o vídeo de boas-vindas
Produtos → Mini Mentoria de Estruturação → Área de membros → Turma → módulo "Comece aqui · Onboarding" → lição de boas-vindas (`fcf20da1…`) → desligar o botão "Ativa/Habilitada". **Não apagar a lição e não trocar o arquivo.** Reverter: ligar de novo.
(Equivalente por API, se Bruno preferir que o Claude faça com "aprovado": `lessons_toggle_enabled` com `enabled=false`, payload em `CORRECOES_PRODUTO.md` P0-2.)

### 3.2 Criar a lição "Leia primeiro" em rascunho (desabilitada) primeiro
1. No módulo Onboarding, criar uma lição do tipo **texto**, título "Leia primeiro: o que você comprou e por onde começar", colar o texto do P0-2 (`CORRECOES_PRODUTO.md`).
2. **Deixar a lição desabilitada** ao salvar. **Não marcar "avisar os alunos"** (o aviso do portal envia e-mail a todos os membros, inclusive os antigos).
3. Colocar a lição na primeira posição do módulo.
4. Visualizar como aluno (modo de visualização ou a conta de teste) e conferir: texto sem prazo de acesso, sem "Land Bank", com a Sessão marcada como "sujeita à análise e à agenda".
5. Só depois do teste do item 2 deste plano, **habilitar**.
Reverter: desabilitar ou apagar a lição nova (nenhuma matrícula depende dela).

### 3.3 Renomear a turma
Turma `087479a3…`: de "Plataforma de estruturação (R$ 97)" para **Mini Mentoria de Estruturação Zion**. Editar só o nome; **não mexer em tempo de acesso, conteúdo ou membros.** Antes: conferir se algum fluxo, segmento ou relatório filtra pelo nome antigo [NC]. Reverter: voltar o nome.

### 3.4 (Depois do P0) textos das lições, anexos, link do dossiê inicial
Pedir ao Claude com "aprovado" (cada `lessons_update`). Antes de aplicar, o Claude guarda o JSON original de cada lição no scratchpad (fora do repositório público) para reverter.

## 4. Janela segura

- Aplicar o passo 1 (patch das fichas) e os passos 3.1 a 3.3 **de madrugada ou de manhã cedo, em dia de semana** [H: horário de menor uso; confirmar no ClickMax em Analytics, "visitantes por hora" e acessos dos membros dos últimos 14 dias, antes de escolher a hora; não consegui ler o uso da turma nesta sessão].
- Evitar horário de pico de compra (logo após ativar campanhas) e a hora em que um anúncio entra no ar.
- Fazer o P0 antes de ligar qualquer nova campanha de venda; é a condição para vender sem a quebra de expectativa.
- Um passo por vez, com 15 minutos de observação entre eles (checar suporte, WhatsApp e e-mails de aluno).

## 5. LGPD: o que já foi enviado antes (para Bruno decidir)

**Fato [E, leitura do código].** Até a correção, o clique em "Baixar PDF" nas fichas enviou ao host externo `zion-dossie-aulas.lovable.app` (um app Lovable) um pacote com nome, e-mail, cidade e **todas as respostas** da ficha; e registrou o aluno como lead no ClickMax (`api.clickmax.io`). Os Pilares 1 e 5 também permitiam enviar fotos, vídeos e documentos ao armazenamento da Zion. O botão Land Bank enviava a mesma coisa, com autorização marcada pelo aluno. O PDF disparava o envio **sem** pedir autorização. Esta sessão **não** inspecionou o conteúdo do que foi guardado, nem dados pessoais de ninguém (nenhum dado real foi lido; os testes usaram dados fictícios e nenhuma requisição saiu de verdade).

**O que não sabemos [NC] e Bruno precisa responder (por quem administra o Lovable e o ClickMax):**
1. O que o app do Lovable (`/api/dossie`, `/api/anexo`, `/api/feedback`) grava? Em qual banco, onde está hospedado, quem acessa, por quanto tempo fica, existe backup?
2. Quantos registros existem desde o início (só a contagem, sem abrir)? Desde quando o PDF dispara o envio sem autorização?
3. Esses registros vão para o Land Bank (Airtable) ou para outro lugar? Quem lê?
4. No ClickMax: o lead criado pela ficha entra em qual lista/tag? Já recebeu alguma mensagem por causa disso? (Não disparar nada para esses leads.)
5. O aviso de privacidade (`land-members/privacidade/`) cobre esse envio para os alunos da Mini Mentoria?

**Riscos:** envio de dado pessoal sem aviso e sem consentimento específico (princípios de transparência e finalidade da LGPD); possível pedido de apagamento de aluno; dependência de um terceiro. **Recomendações (todas dependem de Bruno):** (a) aplicar o patch (para o envio parar); (b) levantar o item acima; (c) decidir se mantém ou apaga os dados já recebidos e, se apagar, fazê-lo por quem administra o Lovable, sem copiar para outro lugar; (d) se houver dado pessoal, avaliar com assessoria jurídica se cabe comunicação aos titulares ("avise o aluno de que não precisa fazer nada" é texto a ser revisado por advogado; esta sessão não redigiu nem enviou nada); (e) atualizar o aviso de privacidade se mantiver o mentor virtual ou o envio voluntário do `/dossie/`.

## 6. O que depende de aprovação de Bruno (checklist)

- [ ] Aplicar o patch das fichas (P0-1) e aceitar a perda do contador de visitas das fichas (NF-1a).
- [ ] Decidir o bloco "próximos passos com a Zion" do Marco Zero (mentoria individual, Bubble): manter, retirar ou trocar (NF-1b).
- [ ] Decidir o botão do mentor virtual: manter ou desligar (NF-1c).
- [ ] Ocultar o vídeo de boas-vindas (P0-2) e habilitar "Leia primeiro" depois do teste manual.
- [ ] Renomear a turma (P1-3).
- [ ] Decidir sobre `/dossie/` e a lição "Monte o seu dossiê inicial": opção A (trocar o link) ou B (reescrever a página) (P1-1).
- [ ] Autorizar os `lessons_update` de P1-2 e P1-4.
- [ ] Conferir os 17 vídeos do YouTube (P1-6).
- [ ] Responder as perguntas da seção 5 (LGPD).
- [ ] Autorizar a regeneração dos e-books, por último (P1-5).
