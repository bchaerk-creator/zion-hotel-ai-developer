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

## Estrutura

```
index.html                 ZG-CAP-01 · protótipo paramétrico
MEMORIAL.md                ZG-CAP-01 · memorial
executivo.html             ZG-CAP-02 · projeto executivo paramétrico
MEMORIAL-ZG-CAP-02.md      ZG-CAP-02 · memorial, achados e ressalvas
ZG-CAP-02.pdf              ZG-CAP-02 · prancha técnica A3
cad/                       ZG-CAP-02 · modelo OpenSCAD
svg/                       ZG-CAP-02 · 18 desenhos exportados
```

Nenhum dos dois é projeto estrutural certificado. Cargas de vento, ancoragem e
dimensionamento final precisam de engenheiro responsável com ART antes da
fabricação definitiva.
