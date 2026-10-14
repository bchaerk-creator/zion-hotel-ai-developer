# E-book Zion (~120 páginas)

Modelo aprovado: `docs/escola/z00/index.html` (Z00, edição completa, 129 páginas A4 com capa, sumário e glossário; ~30 mil palavras).

## Estrutura
1. Capa (verde musgo, numeral gigante, título com ênfase em itálico dourado, deck, assinatura "Da Ideia ao Negócio. Da Hospedagem ao Destino.").
2. Sumário clicável com tempo de leitura por capítulo.
3. Abertura: carta de Bruno (só fatos permitidos), objetivos do módulo, como usar o e-book, as duas jornadas, onde o módulo se encaixa.
4. Seis a oito capítulos de 2.900 a 5.000 palavras.
5. Capítulo final de aplicação: ferramenta interativa, caderno do módulo (respostas salvas só no navegador, com impressão em PDF), autoavaliação com respostas de referência, atividade aplicada com rubrica, checklist e próxima atividade.
6. Glossário, fontes, "o que conferir no seu caso" e aviso legal.

## Anatomia de cada capítulo
- Numeral gigante, tag, título com ênfase, deck, régua dourada.
- Caixa "Neste capítulo" (organizador prévio).
- Primeiro parágrafo com capitular.
- Seções curtas (h3), progressivas.
- Por capítulo: 2 a 4 diagramas SVG próprios, 2 a 4 tabelas, 2 a 4 citações de destaque literais das fontes, 3 ou mais caixas, 1 a 3 exemplos ilustrativos, 1 caixa "Aplicação" (Jornada A e Jornada B), "Pontos-chave" com 5 a 7 itens e exercício final com campos.

## Densidade
- No impresso A4, a média é de cerca de 235 palavras por página, com caixas e figuras. Para 120 páginas, mire em 27 a 30 mil palavras.
- Máximo de duas fotografias de página inteira por volume. Imagens geradas nunca aparecem como fotos reais da Zion.

## Técnica
- HTML e CSS num único arquivo, com fontes Playfair Display (Google Fonts) e Aventa (`docs/assets/fonts/aventa.woff2`). Use números alinhados (`font-variant-numeric: lining-nums`), porque o padrão do Playfair transforma "Z00" em "Zoo".
- Leitura em celular: diagramas dentro de `figure > .scroll` com largura mínima e a dica "Deslize".
- Impressão: `@page A4`, corpo em duas colunas e capítulos em nova página.
- Página com `noindex`. A hospedagem é feita em `docs/escola/<código>/` (GitHub Pages), e a aula entra no ClickMax como link externo desativado.
