# Relatório · Fotos da propriedade no Dossiê (PDF)

Data: 28/11/2026. Sem commit e sem push.

## O que mudou
- O aluno anexa até 6 fotos do terreno na Ficha do Território (Pilar 1, `docs/trilha1/aula1/`). É a ficha que descreve o terreno.
- As fotos entram no PDF do Dossiê de Desenvolvimento (Pilar 7) numa página "Fotografias da propriedade", antes da página 7.
- Sem foto, o PDF fica igual: 14 páginas, sem página vazia.

## Arquivos
- Novo: `docs/trilha1/_fotos.js`. Módulo único, usado pela ficha e pelo Dossiê. Traz as regras (limites, redimensionamento), o salvamento e o bloco da tela.
- Editado: `docs/trilha1/aula1/index.html`. Uma linha: carrega o módulo com `data-montar="1"`.
- Editado: `docs/trilha1/pilar7/index.html`. Carrega o módulo, acrescenta a função `paginaFotosPDF` e uma chamada dela antes da página 7.
- Backups: `producao/zion-collection/sales-machine/backup/aula1-index.html.orig` e `pilar7-index.html.orig`. Ficaram fora de `docs/` para não ficarem públicos.
- Testes: `producao/zion-collection/sales-machine/tests-fotos/test_logic.js` e `e2e.js`.

## Regras aplicadas
- Só JPG, PNG e WEBP. Até 5 MB por arquivo e até 6 fotos.
- A foto é reduzida no navegador para no máximo 1200 px no lado maior e salva como JPEG com qualidade 0.8. Se a foto salva passar de 600 mil caracteres, a qualidade cai aos poucos até 0.45. O canvas descarta EXIF e geolocalização. PNG transparente fica com fundo branco.
- Cada foto tem legenda opcional (até 100 caracteres) e botão "Remover foto".
- As fotos ficam no `localStorage`, na chave `zion-t1-fotos`, separada das fichas. As respostas das fichas não foram mexidas.
- Nenhum envio: o módulo não tem fetch, upload nem formulário.
- Mensagens em português para arquivo inválido, acima de 5 MB, imagem corrompida e limite de 6 fotos.
- PDF: grade de 2 colunas, legenda abaixo, aviso "Fotos enviadas pelo próprio empreendedor, sem verificação da Zion." e nenhuma promessa. Usa as classes e cores que a página já tinha; fontes e paleta não foram trocadas.

## Testes (executados)
- `node test_logic.js`: 16 testes ok. Cobrem tipos, borda de 5 MB, limite de 6, dimensões, legenda, leitura de dados salvos corrompidos, ausência de rede e de promessa proibida no módulo.
- `node e2e.js`: 31 verificações ok, 0 falhas. Playwright no iPhone 13, jsPDF 2.5.1 do pacote npm servido localmente, servidor local de `docs/` na porta 8790. O que ele confirmou:
  - **Sem foto:** PDF de 14 páginas e 0 imagens.
  - **Com 2 fotos (PNG sintéticos, sem pessoas):** 15 páginas e 2 imagens.
  - **Com 6 fotos:** 15 páginas e 6 imagens.
  - **Página de fotos:** fica logo antes da página 7. Foi conferida com `pdftotext` (título, aviso, legenda) e com `pdftoppm` (imagem da página).
  - **Fotos na ficha:** reduzidas a 1200 px em JPEG, legenda salva, tudo continua após recarregar. Remover foto funciona e persiste.
  - **Arquivos recusados:** PDF, arquivo de mais de 5 MB e imagem corrompida, cada um com mensagem clara. Nenhum entrou na lista.
  - **Limite de 6:** ao escolher 5 fotos com 2 já salvas, entraram 4. A mensagem de limite apareceu e o botão ficou desativado.
  - **Rede:** nenhuma requisição além das fontes e do jsPDF da própria página, e nenhuma com corpo (POST).
  - **Tela e erros:** sem rolagem horizontal na ficha e sem erro de JavaScript.
- Capturas e PDFs de teste ficaram em `/tmp/claude-0/-home-user-zion-hotel-ai-developer/20b679d3-1387-56c1-a153-2b815cdf3664/scratchpad/saida/`, fora do repositório.
- Para rodar: `NODE_PATH=/opt/node22/lib/node_modules node e2e.js <pasta-saida> <jspdf.umd.min.js>`.

## Limitações
- As fotos ficam só no aparelho e no navegador onde foram anexadas. O Dossiê precisa ser gerado no mesmo aparelho.
- O armazenamento do navegador é de cerca de 5 MB. Se faltar espaço, a ficha avisa e a foto não é guardada.
- A foto que o aluno anexa **não** fica salva se ele limpar os dados do site. HEIC (foto direta do iPhone em alguns ajustes) não é aceito. O aluno precisa enviar JPG.
- Não testei o jsPDF vindo do cdnjs no navegador real do aluno, só o mesmo arquivo 2.5.1 servido localmente.
- Só a ficha do Território tem o upload. O Marco Zero e o Dossiê do Produto antigo (`aula6`) não mudaram.
- O bloco aparece abaixo de todas as telas da ficha, inclusive a de abertura. Não é uma pergunta do fluxo.
- O texto da landing que promete "anexe fotos e vídeos" continua sem corresponder ao produto: não há vídeo. Isso é decisão de texto, e não foi alterado aqui.
