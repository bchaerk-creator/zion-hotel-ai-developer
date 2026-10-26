# Trilha 1 · Mentoria Zion · instruções para o Claude Code

Você vai produzir, a partir desta pasta, tudo o que falta da Trilha 1 "Transforme seu terreno em um destino turístico de sucesso", de Bruno Chaerk (Zion Hotel Group International): os vídeos animados de cada aula, as ferramentas da trilha e o pacote final para o Bruno subir no ClickMax. Fale sempre em português do Brasil, sem travessão.

## Regras que valem para tudo
- **Nada sai desta pasta sem aprovação expressa do Bruno.** Não publique, não suba para YouTube, Vimeo, ClickMax, Lovable ou qualquer hospedagem, não envie e-mail nem mensagem, não crie conta e não ligue domínio sem ele dizer "pode" naquela ação.
- Não altere os textos dos roteiros, dos e-books nem das apresentações. Se achar um erro, anote em `saida/PENDENCIAS.md` e siga.
- Chaves de API: só em variáveis de ambiente que o Bruno cria no terminal ou no serviço de hospedagem. Nunca peça a chave na conversa e nunca grave em arquivo.
- Nenhuma promessa de renda, retorno, ocupação, crédito ou sociedade em nada que você criar. A Zion "avalia".
- Antes de instalar qualquer coisa, diga o comando e espere o Bruno confirmar.

## Versão leve
Esta é a versão leve do kit: não tem os PDFs das apresentações nem os e-books. Eles não são necessários para os vídeos nem para as ferramentas. No passo 6 (pacote do ClickMax), peça ao Bruno para copiar para cada pasta de aula os arquivos `ebook.pdf` e `apresentacao.pdf` do zip completo.

## O que tem na pasta
| Pasta | O que é |
|---|---|
| `fotos/` | 18 fotos reais da Zion. São as únicas imagens que podem entrar nos vídeos |
| `00-marco-zero/` | apresentação em PDF e `roteiro-e-prompt-do-video.md` (9 vídeos) |
| `01-territorio-e-mercado/` a `06-dossie-final/` | por aula: e-book (PDF e HTML), apresentação em PDF e `roteiro-e-prompt-do-video.md` |
| `ferramentas/` | especificação das 5 ferramentas (`README.md`), as especificações antigas em JSON e as contas já programadas em TypeScript, com testes |
| `clickmax/estrutura-clickmax.md` | como o curso fica organizado no ClickMax: módulos, aulas, descrições e arquivos de cada aula |

Cada `roteiro-e-prompt-do-video.md` tem duas partes. A Parte 1 é o roteiro para o Bruno gravar. A Parte 2 é o prompt dos vídeos daquela aula, entre "INÍCIO DO PROMPT" e "FIM DO PROMPT". Siga a Parte 2 de cada aula como se o Bruno tivesse colado aquele prompt aqui.

## Ordem de trabalho

### 1. Combinar a voz, uma vez para tudo
Pergunte ao Bruno qual voz usar em todos os vídeos:
- **A, a voz dele:** ele grava cada bloco lendo a Parte 1 e salva em `<pasta da aula>/audio/V01.m4a`, `V02.m4a`… (um arquivo por vídeo, na ordem dos vídeos da Parte 2).
- **B, a voz clonada dele no ElevenLabs:** ele cria a variável `ELEVENLABS_API_KEY` e te passa o ID da voz.
- **C, voz gratuita** (`edge-tts`, `pt-BR-AntonioNeural`), só para aprovar ritmo e animação.
Ele pode começar com C para aprovar o visual e trocar depois para A ou B: nesse caso, guarde as composições para renderizar de novo só com o áudio novo.

### 2. Montar a base visual, uma vez
Monte um modelo de cena reutilizável (cores, fontes, selo do bloco, barra de progresso, cena de pausa, entrada de texto, foto com movimento, cartões, tabela que se monta, número grande, mapa da jornada com os marcos Marco Zero, 1 a 6). Todas as aulas usam esse modelo, para a trilha inteira ter a mesma cara.

### 3. Vídeos do Marco Zero primeiro
Siga a Parte 2 de `00-marco-zero/roteiro-e-prompt-do-video.md`. Faça só o V01, mostre 6 quadros ao Bruno e espere a aprovação. Depois faça o resto do Marco Zero.

### 4. Vídeos das Aulas 1 a 6
Uma aula por vez, na ordem, cada uma com a sua Parte 2. Ao terminar cada aula, mostre 3 quadros de cada vídeo e a tabela de durações, e siga para a próxima, a menos que o Bruno peça ajuste. Nenhum vídeo passa de 7 minutos. Saída por aula em `saida/<pasta da aula>/videos/`, `legendas/` e `verticais/`.

### 5. As ferramentas
Siga `ferramentas/README.md`. Primeiro rode os testes que já existem (dentro de `ferramentas/ts`: `npx tsx --test tests/*.test.ts`) e confirme que os 29 passam. Construa a versão 1 (sem IA, tudo no navegador do aluno, com o PDF do Dossiê) para as 5 rotas: `/1-1`, `/etapa-1`, `/etapa-2`, `/etapa-3` e `/dossie-final`. Rode no computador do Bruno (servidor local) e mostre cada página funcionando com o exemplo da Marina e com um caso cheio de "Não sei". A versão 2, com IA, e a publicação só depois que ele aprovar e disser onde hospedar.

### 6. O pacote para o ClickMax
Monte `saida/CLICKMAX/` seguindo `clickmax/estrutura-clickmax.md`: uma pasta por aula, com os vídeos numerados na ordem das aulas do ClickMax, as legendas, o e-book em PDF, a apresentação em PDF e um `descricao.txt` por aula (o texto da descrição, já com o link da ferramenta quando houver). No fim, um `CHECKLIST.md` com o que o Bruno faz, na ordem: subir os vídeos no YouTube como "não listado" (ou no Vimeo ou no Panda Video, que são os que o ClickMax aceita), colar cada link na aula, anexar os PDFs, trocar `[domínio do app]` pelo endereço das ferramentas e deixar as aulas desativadas até revisar.

### 7. Antes de dizer que terminou
Confira com `ffprobe` resolução, fps e duração de todos os vídeos; confira que todo `.srt` tem o texto exato da fala; liste em `saida/PENDENCIAS.md` tudo o que ficou para o Bruno decidir (links, fotos que faltam, casos marcados "confirmar com o Bruno", decisões das ferramentas).
