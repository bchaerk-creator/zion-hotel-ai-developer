# ZG-CAP-02 — Capota chapéu retrátil para Bubble Glamping

**Projeto executivo preliminar para protótipo. Revisão P1. Não certificado estruturalmente.**

Casca rígida articulada em dois pivôs laterais, cobrindo somente a calota superior
da Bubble. A frente permanece transparente. Unidades: milímetros.

Abra `executivo.html` para o modelo paramétrico completo, com desenhos cotados,
cálculo do atuador, lista de materiais e lista de corte recalculados ao vivo.

---

## 1. O achado que definiu o projeto

O briefing pedia o eixo de rotação a **2.200 mm** do piso e curso de **90°**.
A verificação cinemática, feita antes de qualquer desenho, mostrou que os dois
não cabem juntos com uma casca rígida que acompanha a bolha.

### A regra

> Uma casca rígida só mantém folga constante contra uma esfera se o eixo de
> rotação passar pelo centro dessa esfera.

Quando o eixo passa pelo centro, a bolha é uma superfície de revolução em torno
desse eixo. O envelope, medido do eixo até a membrana, vale o raio da esfera em
qualquer ângulo. A folga não muda em nenhum ponto do curso.

Fora do centro, o envelope varia. Medido para a bolha de referência:

| Altura do eixo | Envelope mínimo | Envelope máximo | Variação |
|---|---|---|---|
| 600 mm (centro da esfera) | 3.000 | 3.000 | **0 mm** |
| 1.400 mm | 2.400 | 4.000 | 1.600 mm |
| 2.200 mm | 1.400 | 4.600 | 3.200 mm |

Com o eixo a 2.200 mm restariam duas saídas, ambas ruins: encostar na membrana,
ou afastar a casca até o maior valor do envelope, o que joga a capota mais de um
metro acima do ápice e transforma o chapéu em uma vela de 4,6 m de raio.

### A consequência

A altura do pivô não é uma escolha de projeto. É uma consequência da geometria
da bolha:

```
PIVOT_HEIGHT = BUBBLE_HEIGHT − BUBBLE_DIAMETER / 2
```

Para Ø 6.000 e altura 3.600, dá **600 mm**. Uma bolha mais esférica, de 5.200 mm
de altura com o mesmo diâmetro, colocaria o eixo exatamente nos 2.200 mm pedidos.
O pilar vira um pedestal baixo, o que também some melhor no deck.

### O curso

Com o eixo no centro, quem limita o curso é o piso, não o mecanismo. A borda
traseira desce enquanto gira:

```
ALPHA_MAX = 180° + asin((zc − folga_de_piso) / R_casca) − ε2
```

Para a configuração adotada dá **59,1°**, homologados em **55°** com 4° de reserva.
Os 90° pedidos colocariam a borda traseira 605 mm abaixo do piso. Para chegar
a 90° seria preciso reduzir a faixa coberta para cerca de 20°, o que não é mais
um chapéu, é uma pala.

Na abertura de 55° a casca vai para ε 95°–185°, ou seja, encosta atrás da bolha.
O céu fica livre de 0° a 95° de elevação: toda a frente e todo o topo.

### O ganho de bônus

Pressão de vento age normal à superfície. Numa casca esférica toda normal é
radial e passa pelo centro da esfera, que aqui é o próprio eixo. Momento de uma
força que corta o eixo é zero. **O vento praticamente não carrega o acionamento**:
vai direto para os dois mancais e para as fundações. Adotou-se 10% de parcela
residual, de atrito e imperfeição de forma, absorvida pelos batentes mecânicos.

---

## 2. Configuração adotada

| Parâmetro | Valor |
|---|---|
| BUBBLE_DIAMETER | 6.000 mm |
| BUBBLE_HEIGHT | 3.600 mm |
| Raio da esfera / centro | 3.000 mm / z 600 mm |
| CLEARANCE | 150 mm, constante em todo o curso |
| Raio da casca | 3.150 mm |
| PIVOT_HEIGHT | 600 mm (derivado) |
| Vão entre pivôs | 6.300 mm |
| Pedestais | x ± 3.400 mm, 461 mm fora da base da bolha |
| Faixa coberta ε1 → ε2 | 40° → 130° |
| CANOPY_WIDTH (tecido) | 5.800 mm |
| Arcos transversais | 5, tubo Ø 60 × 2,5 |
| Longarinas | 5, tubo Ø 32 × 2,0 |
| Curso homologado | 55,1° |
| Área de tecido | 28,7 m² |
| Massa da casca | ≈ 96 kg |
| Altura total fechada | 3.750 mm |

### Geometria da casca

Os arcos são meridianos de uma esfera cujos polos ficam nas duas extremidades do
eixo. Cada arco é um semicírculo de raio 3.150 mm que vai de um pivô ao outro,
girado no plano de sua elevação ε. Todos convergem nos dois cubos, parando a 6°
do polo. As longarinas são os paralelos, arcos de raio `√(rc² − x²)` em cada
estação x.

Não é uma cúpula, não desce pela frente e não acompanha toda a superfície da
bolha. É uma faixa de 90° de abertura angular sobre a calota superior.

---

## 3. Por que o serralheiro consegue fabricar

- Todos os arcos têm o **mesmo raio de calandra**, 3.150 mm. Um gabarito só.
- As longarinas têm raios diferentes, mas todas são arcos simples com o raio na
  lista de corte.
- Os cubos são chapa cortada a laser com cinco encaixes radiais.
- Mancal, eixo, atuador e mola a gás são item de catálogo.
- Nada de usinagem além do eixo e da chaveta.

## 4. Pontos de atenção da fabricação

1. **Tolerância de locação dos pedestais: ±3 mm.** Fora disso o conjunto trava
   ou fica com folga desigual nos mancais.
2. **Calandrar sempre com a barra inteira**, conferindo o raio no gabarito de
   piso antes de cortar as pontas.
3. **Só apertar a estrutura depois de girar o curso inteiro**, medindo a folga
   contra a membrana em quatro pontos.
4. **Regular os batentes mecânicos antes dos fins de curso elétricos.** O fim de
   curso é redundância, nunca o único recurso.
5. **Isolar galvanicamente** todo contato alumínio–aço.

## 5. Drenagem

Os arcos correm de um pivô ao outro. As calhas naturais da flecha do pano correm
no mesmo sentido e drenam para as duas laterais, que estão 1,9 m abaixo da crista.
O ponto crítico é o ápice, onde a superfície é horizontal: quem decide empoçamento
é a flecha do pano entre arcos, `rc·(1 − cos(δε/2))`. Com 5 arcos dá 60 mm, no
limite. Com 6 arcos cai para 39 mm. O gotejamento sai 462 mm afastado da membrana,
pela pingadeira na longarina de bordo.

## 6. Acionamento

O momento gravitacional é quase nulo na posição fechada, porque a casca fica
simétrica sobre o eixo, e cresce até o máximo na posição aberta. Molas a gás nos
cubos compensam a maior parte; o resto vai para dois atuadores lineares de 24 V,
um por lado, com a central lendo corrente nos dois para garantir sincronismo.

Alternativa manual assistida: redutor sem-fim 1:100 com as mesmas molas a gás,
resultando em cerca de 47 N de força de mão numa manivela de 250 mm. É viável.

## 7. O que precisa de validação antes de fabricar

Não é projeto estrutural certificado e não substitui ART. Antes da fabricação
definitiva, verificar com engenheiro responsável:

- vento pela NBR 6123, com categoria de rugosidade, fator topográfico e altura
  reais do terreno;
- flambagem no plano e estabilidade fora do plano dos arcos;
- fundação e chumbadores pela NBR 6118;
- seleção final de mancais, eixo e soldas;
- compatibilidade galvânica alumínio / inox / chumbador;
- o admissível de 160 MPa adotado para a liga 6063-T6, a confirmar com o
  fornecedor da liga e do tratamento.

---

## Arquivos

```
executivo.html          modelo paramétrico completo, interativo
ZG-CAP-02.pdf           prancha técnica em A3 paisagem
cad/                    modelo OpenSCAD paramétrico
  parameters.scad         todas as variáveis, com assertivas de geometria
  bubble.scad             geometria de referência da bolha
  canopy.scad             arcos, longarinas e tecido
  mechanism.scad          pedestal, eixo, cubo, manivela, atuador, batentes
  assembly.scad           conjunto geral
  technical_views.scad    projeções 2D para exportar DXF/SVG
svg/                    18 desenhos exportados
  V-01..06                vistas ortográficas e isométrica
  P-01..05                posições de operação
  D-01..04                detalhes construtivos
  K-01                    diagrama do envelope
  M-01                    diagrama de movimento
  A-01                    curva de esforço do atuador
```

Os arquivos `.scad` foram escritos para OpenSCAD e não foram renderizados neste
ambiente, que não tem OpenSCAD instalado. A geometria que eles descrevem é a
mesma validada numericamente no `executivo.html`.
