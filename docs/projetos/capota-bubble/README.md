# Capota retrátil para Bubble Glamping Zion

Duas soluções desenvolvidas para o mesmo problema, com conceitos de produto
diferentes. Ambas paramétricas e recalculadas ao vivo no navegador.

| | ZG-CAP-01 | ZG-CAP-02 |
|---|---|---|
| Conceito | capota em arcos aninhados, cobertura total | chapéu rígido sobre a calota superior |
| Movimento | leque telescópico, arcos independentes | casca única girando em dois pivôs |
| Cobertura fechada | 125° de faixa, envolve a bolha | 90° de faixa, só o topo |
| Vista frontal | parcialmente coberta | totalmente livre |
| Eixo | centro da esfera | centro da esfera |
| Curso | 100° | 55° |
| Complexidade | alta, N cubos e N molas | baixa, 2 mancais e 2 atuadores |
| Arquivo | `index.html` | `executivo.html` |
| Memorial | `MEMORIAL.md` | `MEMORIAL-ZG-CAP-02.md` |

## Qual usar

**ZG-CAP-02** é o projeto executivo para protótipo. Menos peças, menos massa,
vento que não carrega o acionamento e a bolha continua transparente na frente,
que é o ativo do produto.

**ZG-CAP-01** continua válido para quem quiser sombra total, inclusive na frente,
aceitando um sistema bem mais caro de fabricar e manter.

## A regra geométrica comum aos dois

Uma casca rígida só mantém folga constante contra uma esfera se o eixo de rotação
passar pelo centro dessa esfera. Por isso, nos dois projetos:

```
PIVOT_HEIGHT = BUBBLE_HEIGHT − BUBBLE_DIAMETER / 2
```

Não é escolha de projeto, é consequência da geometria da bolha.

## Geometria da Bubble real

A partir do CAD do fabricante, o ZG-CAP-02 passou a usar as medidas reais:
Ø 5.000 mm no nível do deck e 2.292 mm de altura. Disso sai esfera de raio
2.509 mm com centro **217 mm abaixo do deck**, ou seja, os dois mancais ficam
num nível rebaixado ao lado do deck, não sobre ele.

## Estrutura

```
index.html                    ZG-CAP-01 · protótipo paramétrico
MEMORIAL.md                   ZG-CAP-01 · memorial
executivo.html                ZG-CAP-02 · projeto executivo paramétrico
MEMORIAL-ZG-CAP-02.md         ZG-CAP-02 · memorial, achados e ressalvas
ZG-CAP-02.pdf                 ZG-CAP-02 · prancha técnica A3
animacao.html                 ZG-CAP-02 · animação de abertura no navegador
ZG-CAP-02-animacao.mp4        ZG-CAP-02 · vídeo 16:9, 9 s em loop
ZG-CAP-02-animacao-quadrado.mp4  ZG-CAP-02 · vídeo 1:1 para redes
orcamento.html                ZG-CAP-02 · orçamento e fornecedores
ZG-CAP-02-cotacao.xlsx        ZG-CAP-02 · planilha de cotação para fornecedor
gerar_orcamento.py            gera a planilha e a página a partir da geometria
orcamento-template.html       template da página de orçamento
cad/                          ZG-CAP-02 · modelo OpenSCAD
svg/                          ZG-CAP-02 · 18 desenhos exportados
```

## Refazer o orçamento depois de mudar o projeto

```
python3 gerar_orcamento.py
```

Regera `ZG-CAP-02-cotacao.xlsx` e `orcamento.html` a partir da geometria. Se o
engenheiro responsável mudar seção de tubo, chapa ou fundação, altere as
constantes no topo do script e rode de novo.

Nenhum dos dois é projeto estrutural certificado. Cargas de vento, ancoragem e
dimensionamento final precisam de engenheiro responsável com ART antes da
fabricação definitiva.
