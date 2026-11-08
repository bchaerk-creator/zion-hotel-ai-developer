# Marco Zero · O gestor e o diagnóstico · Roteiros de vídeo

Jornada 2 · Gestão. Dois vídeos: a aula (16:9, 1920×1080, narração sintética pt-BR, cenas geradas em `video/`) e o tutorial da ficha (1280×720, gravação real da ferramenta, `tutorial/`). Bruno pode regravar a aula com a própria voz usando este roteiro; as cenas ficam iguais.

Regras aplicadas: sem preço, sem promessa de renda ou resultado, sem números reais da Zion, exemplo marcado como fictício, citações literais das fontes Zion (Panorama, Etapa 09, Etapa 10).

## Aula em vídeo (cerca de 4 minutos, 11 cenas)

| # | Cena (tela) | Narração |
|---|---|---|
| 1 | Foto da operação · "A sua hospedagem funciona. Mas ela é gerida?" | Bem-vindo ao Marco Zero da Jornada 2, a jornada de Gestão. A sua hospedagem funciona: o hóspede chega, dorme, vai embora, e o dinheiro entra. A pergunta desta aula é outra: ela é gerida? Em uns quatro minutos, você vai entender o que é gerir, e de onde começar. |
| 2 | Citação do Panorama (três ofícios) | O Método Zion 360° separa a hospedagem em três ofícios. Desenvolver é escolher o que construir e onde. Administrar é fazer o que foi construído dar lucro. Operar é entregar a mesma coisa todo dia. A maior perda de tempo do setor é gente tentando resolver o problema da etapa errada. |
| 3 | Três caixas: Desenvolver, Gerir, Operar | Esta jornada é o ofício do meio. Desenvolver responde: o que dá para fazer aqui? Isso é a Jornada 1. Operar responde: como isso se entrega todo dia? Isso é a Jornada 3. Gerir responde a pergunta que fica no meio e que quase ninguém faz: como isso dá lucro? |
| 4 | "Casa cheia e não sobra dinheiro" + três lemas | O erro mais comum do setor é a casa cheia que não deixa dinheiro no fim do mês. Ocupação alta com diária baixa é trabalho sem lucro. Faturamento, lucro, caixa e margem são quatro coisas diferentes. Guarde três frases do método: movimento não é lucro. Estar presente não é gerir. E ocupação é vaidade, margem é sobrevivência. |
| 5 | A pergunta da saída da operação | Existe uma pergunta que separa um negócio de um emprego que você criou para si mesmo. Se você contratasse alguém para fazer exatamente o que você faz, pagasse o preço de mercado por isso, e saísse da operação, sobraria alguma coisa? Se a resposta for não, hoje a hospedagem paga o seu trabalho, e não o seu negócio. Isso não é um veredito. É o ponto de partida. |
| 6 | Lista: os cinco números do gestor | Gestão começa com cinco números do mês passado. Quanto entrou de verdade, depois de descontos e comissões. Quanto sobrou, que não é o saldo da conta. A ocupação: noites vendidas de quantas estavam disponíveis. A diária média real. E o custo por noite vendida: tudo o que saiu, dividido pelas noites que você realmente vendeu. Em mês de baixa, esse custo está no pico. |
| 7 | Lista: as oito áreas | E a gestão se organiza em oito áreas: planejamento e metas, finanças e fluxo de caixa, preço e reservas, marketing e vendas, pessoas, compras e estoque, limpeza e manutenção, e qualidade com indicadores. Para cada uma, só três respostas: não existe; funciona, mas só na minha cabeça; ou funciona com padrão e registro. O que está só na cabeça não dá para medir, delegar nem melhorar. |
| 8 | Exemplo didático · nota 50 | Um exemplo didático, com dados fictícios. As Cabanas do Vale têm quatro unidades e a dona opera sozinha. Ela sabe quanto entrou e a diária média, mas não sabe quanto sobrou nem o custo por noite. Metas e indicadores não existem. Finanças, preço e pessoas funcionam só na cabeça dela. A nota sai em cinquenta de cem: gestão em construção. A área mais frágil: planejamento e metas. |
| 9 | Tela da ficha no celular | Agora é a sua vez. Abra o Faça agora: o seu Diagnóstico de Gestão. São oito minutos. Você sai com a sua nota, a área mais frágil, uma ação de trinta dias com critério de verificação, e o módulo por onde começar. Tudo em PDF: é a página zero do seu Plano de Gestão. |
| 10 | Tela da planilha | Depois do diagnóstico, feche o mês passado em uma folha. A planilha Painel do Mês calcula os cinco números a partir do que você lança. Dez minutos por mês, sempre o mesmo painel, e a comparação certa é com o mesmo mês do ano anterior, nunca com o mês passado. |
| 11 | Regra de ouro | A regra de ouro desta jornada: comece pela área que está custando dinheiro hoje. Uma ação só, na área mais frágil, com prazo de trinta dias. Quando ela estiver feita e verificada, o Marco Zero está concluído, e a jornada aponta o seu próximo módulo. Nos vemos lá. |

Fontes das frases citadas: cena 2, Panorama ("O conceito"); cena 4, Panorama G6, G7 e estudo de caso da Trilha B; cena 5, Etapa 09, Passo 07; cena 6, Etapa 09, Passos 04 e 08; cena 10, Etapa 09, Passo 13; cena 11, Panorama, cap. 8.

## Tutorial da ficha (cerca de 3 minutos, 11 cenas)
Gravação real da ferramenta com cursor e destaques: abertura e dados, situação, quem cuida da gestão, as cinco perguntas, as oito áreas (duas telas), a rotina e a pergunta da saída, o resultado em cinco partes, ação e prazo, critério de conclusão, PDF. Roteiro completo em `tutorial/ficha-gestao-marco-zero.json`.

## Como regerar
```
cd producao/jornada2/00-marco-zero
node video/shots.js && node video/shot_xl.js            # telas da ficha e da planilha (servidor local de docs/ na porta 8790)
python3 video/make_video.py video/spec-g00.json ../../../docs/trilha2/videos/aula-marco-zero-gestao.mp4
cd ../../clube/tutoriais-video && python3 make.py ../../jornada2/00-marco-zero/tutorial/ficha-gestao-marco-zero.json ../../../docs/trilha2/videos/tutoriais/tutorial-ficha-gestao-marco-zero.mp4
```
