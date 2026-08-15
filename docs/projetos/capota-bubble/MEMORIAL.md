# Capota Retrátil Bubble — ZG-CAP-01

Protótipo paramétrico de capota retrátil para Bubble de glamping.
Abra `index.html` no navegador (ou pelo GitHub Pages em `/projetos/capota-bubble/`).

Não é um desenho estático. É um modelo: você move os parâmetros e a geometria,
o molde de corte, os esforços e a lista de materiais recalculam ao vivo.

---

## O sistema escolhido

Arcos semicirculares aninhados girando sobre **um único eixo horizontal**,
posicionado no diâmetro da base da bolha.

Cada arco tem raio próprio, decrescente do fundo para a frente pelo passo de
aninhamento. É essa diferença que permite o encaixe telescópico: o arco maior
sempre passa por fora do menor, em qualquer ponto do curso, sem colisão.

- **Arco 1** — arco-mãe, maior raio, fixo na traseira.
- **Arcos 2 a N** — giram livres, cada um na sua pista de rolamento.
- **Arco N** — líder, menor raio, acionado.

## Por que não tem trilho no piso

O quadro de referência trazia "trilho em alumínio com carro deslizante". Não
fecha com a cinemática: se todos os arcos giram no mesmo eixo, os pés de cada
arco caem em `±R_i` sobre esse eixo, e não sobre uma pista perimetral.

A solução correta é um **eixo-tronco escalonado** em cada lado, curto (o
comprimento é apenas `(N−1) × passo`, cerca de 350 a 420 mm), com uma pista de
rolamento por arco. Como o menor raio já é maior que o raio da bolha, esse eixo
fica inteiramente **fora** da envoltória do Bubble.

Vantagem de produto: nenhum trilho circundando a bolha. O entorno fica limpo e
a leitura visual da esfera é preservada, que é o ativo do glamping.

## Os três números que governam o projeto

**1. Flecha do têxtil entre arcos.** O gomo é cortado sobre a esfera, mas sob
tensão tende à corda. A flecha resultante é `R·(1 − cos(δ/2))`. Acima de 60 mm
começa a empoçar no quadrante superior, onde a superfície é horizontal. É esse
critério, e não a estética, que define o número de arcos. Com Ø 6,00 m e
cobertura de 125°, sete arcos ficam em 60 mm e seis já passam de 80 mm.

**2. Momento gravitacional no ninho.** Com todos os arcos recolhidos na
traseira, os pesos param de se cancelar e somam no mesmo sentido. O conjunto
gera milhares de N·m no eixo. Sem **mola de torção pré-carregada em cada cubo**
o acionamento é inviável. Essa mola não é acessório, é item estrutural.
Com a compensação, o torque residual cai para a casa das centenas de N·m e o
acionamento vira um guincho de cabo comum.

**3. Momento de vento na posição fechada.** Supera o momento gravitacional. Não
pode passar pelo redutor. Vai para **pinos de travamento** que engatam arco a
arco na posição fechada, transferindo o esforço direto para as torres, mais
anemômetro com recolhimento automático a 45 km/h.

## Modelo geométrico

Os arcos são meridianos de uma esfera cujos polos ficam nas duas extremidades do
eixo. Isso dá fórmulas fechadas, e é por isso que as três vistas do protótipo
são projeções reais e não ilustrações:

| Grandeza | Fórmula |
|---|---|
| Área do gomo entre dois arcos | `2 · R² · δ` |
| Largura do gomo na estação θ | `w(θ) = R · δ · sen θ` |
| Comprimento desenvolvido do gomo | `π · R` |
| Folga mínima real capota↔bolha | `√(R_int² + h_eixo²) − R_bolha` |
| Corte transversal (vista no eixo) | leque de raios |
| Elevação (vista normal ao eixo) | semielipses `a = R`, `b = R·sen ψ` |
| Planta | semielipses `a = R`, `b = R·cos ψ` |

O molde de corte sai direto dessas fórmulas: uma lente simétrica, estações a
cada 15°, margem de costura de 25 mm e cordão keder nas duas bordas.

## Escopo e limites

Os esforços calculados são **pré-dimensionamento paramétrico**, para orientar
compra de perfil e escolha de acionamento. Antes de fabricar:

- verificação estrutural por engenheiro habilitado, com ART;
- vento pela NBR 6123 com a categoria de rugosidade e a altura reais do terreno;
- fundação das torres pela NBR 6118 / 8800 conforme o material adotado;
- protótipo físico de um par de arcos antes de calandrar a série completa.

## Próximos passos

1. Congelar o diâmetro real da bolha instalada em Vargem Pequena e medir em campo.
2. Rodar o protótipo com esse diâmetro e fechar N, passo e ângulo de cobertura.
3. Levar a lista de materiais a três serralherias de alumínio naval para cotação.
4. Fabricar um par de arcos e um gomo para validar aninhamento e tensão do têxtil.
5. Só então calandrar a série e costurar o jogo completo.
