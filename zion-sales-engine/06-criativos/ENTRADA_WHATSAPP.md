# Entrada por WhatsApp · Vídeos 01 e 02 · ZION CREATIVE · 25/11/2026

Decisão de Bruno (25/11): pare tudo na Zion Collection; os Vídeos 01 (Terreno Capital) e 02 (Dono de Terreno), que captaram leads baratos, viram **só entrada de leads**. Não vendem nem prometem nada, dizem que queremos **conhecer o dono de terreno**, e o destino é o **WhatsApp direto** (anúncio com botão de WhatsApp, sem formulário, sem cobrança). A venda da Mini Mentoria de Estruturação Zion (R$ 47) acontece **dentro do WhatsApp**, pela equipe comercial/SDR/Bela, na janela de atendimento. Não se cobra nada na entrada; nenhum produto novo.

Este arquivo é o **delta** sobre `CAPTACAO_CORRIGIDA.md` (que tratava o destino como formulário gratuito; **substituído para os vídeos 01 e 02**). Marcação: [E] lido/executado, [H] hipótese, [NC] não confirmado. **Nada foi enviado ao Meta, ao ClickMax nem ao WhatsApp; nenhuma campanha foi ativada.**

## 0. Respostas diretas
1. **O áudio ORIGINAL pode ser mantido? NÃO.** A fala dos dois vídeos (lida por legenda queimada, ver `CAPTACAO_CORRIGIDA.md` §2.1 e §2.3) promete consultoria ("agende a tua sessão de consultoria"), "investimentos em destinos turísticos", "temos a solução", "viabilizar esse projeto", vende bubbles e traz número de mercado sem fonte ("setor que mais cresce"). Isso é exatamente o que a regra P0 proíbe, e a nova entrada nem tem consultoria para oferecer. Não dá para cortar só algumas frases sem deixar o vídeo sem sentido. **Recomendação: regravar a voz de Bruno** com os roteiros de 30 a 45 s da §3. Enquanto isso, as versões mudas com texto na tela da §4 servem.
2. **As versões mudas antigas (`capt-v01/v02-...-sem-audio.mp4`) servem?** Não como estão: falam em "cadastro gratuito", "conteúdos" e "R$47" na cartela, e o destino agora é o WhatsApp. **Gerei versões mudas novas** (§4), com o mesmo b-roll sem pessoas e cartela final nova.
3. **Há dois textos de anúncio por vídeo:** A (ordem literal de Bruno: só "queremos conhecer") e **B (recomendada)**: acrescenta uma frase dizendo que a equipe também apresenta uma formação digital paga, sem preço. Motivo: a regra "clareza antes do clique" ainda vale. Sem essa frase, quem clica espera uma conversa sobre o terreno e recebe uma oferta; com ela, o filtro acontece antes do clique e a conversa chega mais qualificada. **Bruno decide A ou B**; B não cita preço nem prometido algum.

## 1. Anúncio (igual para criativo mudo e para vídeo regravado)
Objetivo e posicionamento: campanha de **mensagens (clique para WhatsApp)**; destino = número de WhatsApp Business da Zion [NC: qual número/WABA; deve ser o mesmo que a equipe e a Bela atendem. Bruno confirma]. **Sem formulário. Sem URL de site.**

| Campo | Vídeo 02 · Dono de Terreno | Vídeo 01 · Terreno Capital |
|---|---|---|
| **Nome do anúncio** (padrão `PADRAO_UTM.md` §9.1: nome = id do criativo) | `entrada-wa-v02-dono-terreno` | `entrada-wa-v01-terreno-capital` |
| **Nome da campanha** | `entrada-whatsapp \| AAAA-MM-DD` | idem |
| **Título** (≤ 40; ~27 visíveis) | `Dono de terreno? Fale com a Zion` (32) | `Terreno parado? Converse com a Zion` (35) |
| **Descrição** (≤ 30; nem sempre aparece em anúncio de mensagem) | `Fale com a equipe no WhatsApp` (29) | idem |
| **CTA do botão** | **WhatsApp: Enviar mensagem** (`WHATSAPP_MESSAGE`; no Gerenciador, "Enviar mensagem") | idem |
| **Mensagem pré-preenchida** (a pessoa só aperta enviar) | `Olá, vi o vídeo e tenho um terreno.` (35) | `Olá, vi o vídeo e tenho um terreno parado.` (42) |
| **Perguntas rápidas** (ice breakers; até 3, ≤ 80 caracteres [H: limite do Gerenciador, conferir]) | `Tenho um terreno e quero conhecer a Zion` · `Tenho uma ideia de projeto` · `Quero entender como funciona` | idem |

**Texto primário.** Meta mostra ~125 caracteres antes de "ver mais": a primeira frase carrega o gancho.
- **A (literal de Bruno), Vídeo 02, 210 caracteres:**
  "Você tem um terreno e ainda não sabe por onde começar? A Zion opera hospedagens em Urubici e Florianópolis e quer conhecer donos de terreno. Toque em Enviar mensagem e converse com a nossa equipe pelo WhatsApp."
- **B (recomendada), Vídeo 02, 289 caracteres:** o texto A **mais** "A equipe também apresenta a formação digital da Zion, se você quiser conhecer."
- **A, Vídeo 01, 261 caracteres:**
  "Terreno parado há tanto tempo, sem saber por onde começar? Você não precisa começar construindo um hotel. A Zion opera hospedagens em Urubici e Florianópolis e quer conhecer donos de terreno. Toque em Enviar mensagem e converse com a nossa equipe pelo WhatsApp."
- **B, Vídeo 01:** o texto A **mais** a mesma frase final de B.

Os números de caracteres foram contados com `len()` em Python [E]. Os limites (125 visíveis, 40 de título, 30 de descrição) são as recomendações usuais do Meta [H]: o Gerenciador é quem confirma.

**Pré-preenchida e identificação do vídeo.** A mensagem não leva código. O Meta informa o anúncio de origem quando a pessoa manda a primeira mensagem, e a documentação do ClickMax diz que ele registra o clique no contato sem UTM nem página [E, lida pelo FUNNEL em `05-funis/CRM_WHATSAPP_ENTRADA.md` §1]; **que apareça por anúncio no contato é [NC] até o teste**. Teste antes de ligar: abrir o anúncio de teste pelo celular de um colega e conferir no ClickMax/Bela se o contato aparece com a origem. **Plano B se não aparecer:** acrescentar ao fim da pré-preenchida um sufixo curto (`(v02)` / `(v01)`) e etiquetar o contato por esse sufixo.

## 2. Revisão do que já foi lido (fala, legenda, texto) e o que sai de cada vídeo
Base: leitura de 25/11 (`CAPTACAO_CORRIGIDA.md` §1 e §2). Só o delta:

| Item lido | Estado hoje | Nesta entrada |
|---|---|---|
| Fala de Bruno/narração (Vídeo 01 em câmera; Vídeo 02 em locução com b-roll) | Consultoria, investimento, bubbles, "setor que mais cresce" | **Sai inteira.** Regravar (§3) ou usar mudo (§4) |
| Legenda queimada | Repete a fala | Refazer pela fala nova |
| Cena da piscina com mulher (Vídeo 02, 0:00 a 0:03) | Pessoa não autorizada | Cortada em todas as versões |
| Hook | "Ei, você, dono de terreno!" / "Você aí, dono de terreno" | **Mantido como pergunta:** "Ei, dono de terreno! Você tem um terreno e ainda não sabe por onde começar?" (ver risco de política abaixo) |
| Cartela final antiga | "Glamping Collection" / "Cadastro gratuito · Formação paga a partir de R$47" | **Nova:** "Queremos te conhecer" + "Converse com a equipe pelo WhatsApp" |
| Texto, título, botão, formulário do anúncio | R$ 270, sessão de 45 min, "possibilidade de parcerias e investimentos", Cadastre-se/Saiba mais | Textos da §1; botão Enviar mensagem; sem formulário |
| "Queremos te conhecer" | Estava na lista de termos proibidos de `CAPTACAO_CORRIGIDA` (sugeria avaliação) | **Liberado por ordem de Bruno (25/11)**, **só** com o que segue: não prometer avaliação do terreno, reunião, consultoria, investimento, parceria |

### Política Meta e limites de linguagem [H: política vigente conferida pelo Gerenciador, não por mim]
- **Atributos pessoais.** O Meta não permite o anúncio afirmar ou insinuar que conhece situação do usuário (finanças, dívida, condição). Por isso **o hook vira pergunta** ("Você tem um terreno...?") e saem "sem capital", "terreno dando prejuízo", "achou que o seu caso não tinha solução, né?" (afirma estado da pessoa). Se o anúncio for reprovado por "dono de terreno" como rótulo, trocar para "Tem um terreno?".
- **Sem promessa** de renda, investimento, parceria, resultado, "viabilizar"; sem número de mercado; sem "garantido".
- **Sem antes e depois, sem urgência falsa.** Fotos reais da Zion sem pessoas; nunca imagem gerada como foto real.
- **Sem preço e sem produto novo na entrada** (ordem de Bruno). Em B só aparece "uma formação digital paga", sem nome e sem valor.
- **Dados pessoais:** o anúncio não coleta nada; a coleta é na conversa (ver §5).
- Termos proibidos: R$ 97, R$ 270, taxa, inscrição, cadastro, "agende", consultoria (fora de negação), sessão, reunião, avaliação do terreno, Land Bank, banco de áreas, sócio, investimento/parceria como promessa, "faturar", "ganhar dinheiro", "setor que mais cresce", "20 anos".

## 3. Roteiros de voz revisados para Bruno regravar (30 a 45 s; nunca voz clonada ou sintética)
Duração estimada: 82 palavras, a 2,2 a 2,6 palavras por segundo, dá **32 a 38 s** [H: estimativa por contagem; mede-se na gravação].

### Vídeo 02 · Dono de Terreno (locução sobre o b-roll sem pessoas)
| Tempo | Fala | Texto na tela (painel) |
|---|---|---|
| 0 a 6 s | "Ei, dono de terreno! Você tem um terreno e ainda não sabe por onde começar?" | Ei, *dono de terreno!* |
| 6 a 13 s | "Antes do capital, vem o projeto. Estruturar no papel é o primeiro passo, e não exige obra." | Antes do capital, *vem o projeto.* |
| 13 a 21 s | "Aqui na Zion, a gente opera hospedagens em Urubici e Florianópolis. Conhecemos esse caminho por dentro." | A Zion opera hospedagens *em Urubici e Florianópolis.* |
| 21 a 30 s | "E a gente quer conhecer você, dono de terreno. Conta pra gente quem você é e o que você tem em mente." | Queremos *conhecer* você |
| 30 a 38 s | "Toque em Enviar mensagem e converse com a nossa equipe pelo WhatsApp." | Toque em *Enviar mensagem* |
| 38 a 46 s | (sem fala) | **Cartela final:** Queremos te conhecer · Converse com a equipe pelo WhatsApp |
Na versão **B**, a última fala acrescenta: "A equipe também apresenta uma formação digital da Zion, se você quiser conhecer."

### Vídeo 01 · Terreno Capital (Bruno em câmera, mesmo enquadramento e energia)
| Tempo | Fala | Texto na tela |
|---|---|---|
| 0 a 7 s | "Terreno parado há tanto tempo, sem saber por onde começar? Calma: você não precisa começar construindo um hotel." | Terreno parado há tanto tempo, *sem saber por onde começar?* |
| 7 a 14 s | "Dá para estruturar o projeto no papel, antes da obra." | Dá para *estruturar o projeto no papel* |
| 14 a 22 s | "Eu sou o Bruno, e a Zion opera hospedagens em Urubici e Florianópolis. A gente conhece esse caminho por dentro." | A Zion opera hospedagens *em Urubici e Florianópolis* |
| 22 a 31 s | "E a gente quer conhecer você, dono de terreno. Conta pra gente quem você é e o que você tem em mente." | Queremos *conhecer* você |
| 31 a 38 s | "Toque em Enviar mensagem e converse com a nossa equipe pelo WhatsApp." | Toque em *Enviar mensagem* |
| 38 a 46 s | (sem fala) | **Cartela final** igual ao Vídeo 02 |
Versão **B**: mesma frase extra no fim. Proibido na gravação: tudo da lista de termos da §2 e improvisar "a gente vai avaliar o seu terreno", "vamos viabilizar", "pode virar sócio".

## 4. Versões mudas novas [PRONTAS, fora do repositório; os vídeos originais não foram tocados]
Pasta: `/tmp/claude-0/-home-user-zion-hotel-ai-developer/20b679d3-1387-56c1-a153-2b815cdf3664/scratchpad/cap/entrada/` [E: 4 arquivos, 1080×1920, 37,8 s, só vídeo, sem trilha de áudio, ~9 a 10 MB cada; abri 6 quadros de dois deles e conferi texto no painel (não sobre a foto), sem pessoas, cartela final correta].
| Arquivo | Texto |
|---|---|
| `entrada-wa-v02-dono-terreno-A-sem-audio.mp4` | Variante A (literal) |
| `entrada-wa-v02-dono-terreno-B-sem-audio.mp4` | Variante B (recomendada) |
| `entrada-wa-v01-terreno-capital-A-sem-audio.mp4` | Variante A |
| `entrada-wa-v01-terreno-capital-B-sem-audio.mp4` | Variante B |
Gerados por `build_video_entrada_wa.js <pasta _cenas de build_video_captacao> <saída>` (reaproveita o b-roll sem pessoas já gerado; não precisa do vídeo-fonte). Limite: mudo, com texto na tela; serve a Reels e Feed. O Vídeo 01 mudo **não usa a imagem de Bruno**; quem quer o rosto regrava o roteiro da §3. Hospedagem do arquivo para o Meta: Bruno decide (peso acima do que cabe bem no repositório).

## 5. O que acontece depois do clique (para a equipe comercial/SDR/Bela; não altero Bela, Zaya nem automações)
**Fonte da conversa completa:** `05-funis/VENDA_NO_WHATSAPP.md` e `05-funis/CRM_WHATSAPP_ENTRADA.md` (FUNNEL). O que segue é só o mínimo para o criativo ser coerente com elas; em caso de diferença, vale o do FUNNEL. **Conflito a decidir por Bruno:** `05-funis/DIAGNOSTICO_GRATUITO.md` §7 propõe textos de entrada para os mesmos Vídeos 01 e 02 que **prometem um "diagnóstico gratuito do estágio do projeto"**. A ordem de Bruno para este trabalho é que os vídeos **não prometam nem vendam nada** (só "queremos conhecer"); por isso os textos deste arquivo seguem essa ordem. Se Bruno aprovar o diagnóstico, valem os textos do §7 de lá e este arquivo fica como alternativa.
1. **Primeira resposta (humana ou Bela, dentro da janela de atendimento):** curta, sem preço ainda. Sugestão: "Olá! Aqui é a equipe da Zion, obrigado por falar com a gente. Conta pra nós: em que cidade fica o seu terreno e o que você pensa em fazer nele? (se preferir, pode pular)". Não pedir dado além disso.
2. **Oferta, com tudo claro antes do link:** "Pelo que você contou, o primeiro passo é estruturar o projeto. Temos a Mini Mentoria de Estruturação Zion: formação digital com 9 módulos, 70 conteúdos e acesso à plataforma digital, por R$ 47 em pagamento único (Pix ou cartão), com reembolso em 7 dias. Não é reunião nem consultoria, e não prometemos investimento nem parceria. Posso te mandar a página para você ver tudo antes de decidir?"
3. **Link:** a **página** (não o checkout): `https://infoprodutos-zion.clickmax.space/mini-mentoria?utm_source=whatsapp&utm_medium=sdr&utm_campaign=entrada-whatsapp&utm_content=<criativo>-oferta&src=whatsapp`, conforme o padrão de canal de `PADRAO_UTM.md` §5 e §8. `<criativo>` = `entrada-wa-v02-dono-terreno` ou `entrada-wa-v01-terreno-capital`. [NC] `utm_campaign=entrada-whatsapp` é valor novo: o DATA acrescenta ao padrão; a UTM de canal grava a origem do **canal**, não do anúncio (quem liga venda a anúncio é o identificador do clique, ver §1).
4. **Consentimento:** quem escreve primeiro pode ser respondido na janela. Para avisos futuros (modelo aprovado, remarketing, e-mail) pedir o aceite explícito na conversa: "Posso te avisar por aqui sobre novidades da Zion?" e registrar. Nunca reutilizar o modelo `clube_plataforma_d0` (R$ 97, banco de áreas).
5. **Janela:** a de atendimento padrão do WhatsApp é de 24 h a partir da mensagem da pessoa (ordem de Bruno); conversas que vêm de anúncio de clique para WhatsApp têm janela maior sem custo [H: 72 h, conferir no painel do WhatsApp]. Fora da janela só modelo aprovado pelo Meta.
6. **Pontos de atenção antes de ligar [NC]:**
   - Confirmar que **nenhuma automação do ClickMax dispare para conversa nova de WhatsApp** (por exemplo o fluxo `bc86b069`, que usa R$ 97) e que **os prompts da Bela/Zaya não citem** R$ 97, R$ 270, consultoria, reunião ou banco de áreas. Quem confere: Bruno / responsável pela Bela.
   - Tela do Meta que explica a conversa e política de privacidade do número comercial.
   - Quem atende, em que horário, e o que o anúncio diz se ninguém responde (o Meta pode penalizar demora [H]).

## 6. Medição (sem declarar vencedor por poucos dados)
Custo por conversa iniciada; taxa de resposta da pessoa à primeira mensagem; conversas com terreno informado; página enviada; checkout efetivo; **compra aprovada** (única venda que conta); custo por compra atribuída (clique → conversa → compra, com a conciliação do DATA); reembolso. Conversa iniciada barata **não é** resultado: o objetivo é comprador, não curioso. [NC] Evento de compra de volta ao Meta para mensagens exige identificador do clique no contato; combinar com o DATA.

## 7. Ordem de execução e aprovação
| # | Ação | Quem | Aprovação | Reversão |
|---|---|---|---|---|
| 1 | Escolher A ou B; Bruno regrava a voz (§3) ou aprova o mudo (§4) | Bruno | Bruno | n/a |
| 2 | Conferir número de WhatsApp, atendimento e automações (§5.6) | Bruno / responsável Bela | Bruno | n/a |
| 3 | Criar 2 anúncios de mensagem NOVOS (não editar os ativos), **pausados** | ChatGPT (Windsor) | Bruno | arquivar |
| 4 | Pausar de vez os 3 anúncios de R$ 270 e os "FORM 47" (decisão "pare tudo") | Bruno / ChatGPT | Bruno | reativar |
| 5 | Ativar | Bruno ("aprovado") | Bruno | pausar |
Orçamento: o teto atual é R$ 0 até Bruno aprovar (CLAUDE.md); a proposta de R$ 60/dia do funil híbrido muda de composição com esta decisão, e quem reescreve é FINANCE/TRAFFIC [NC].

## Teste
Rodei `grep -n -i -E` com os termos proibidos acima em `ENTRADA_WHATSAPP.md`, `build_video_entrada_wa.js` e nos textos de cena: achados só nas linhas que **listam** o que é proibido ou que **negam** ("não é reunião nem consultoria", tabela de termos). Detalhes na seção "Teste" do final de `PACOTE_PARA_CHATGPT_v4.md`.
