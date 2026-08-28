# Pilares Comerciais da Zion

> Fonte única da estrutura: [`src/config/pilares.py`](../src/config/pilares.py).
> Os agentes leem daqui — mudou o pilar no código, mudou em todo o sistema.
> Consulta rápida: `python -m src.main pilares`

---

## 1. As seis frentes

| Pilar | Oferta | Cliente | Como a Zion ganha |
|---|---|---|---|
| **Produto** | Venda de bubbles e cabanas | Quem já tem projeto definido | Receita por unidade entregue |
| **Desenvolvimento** | Escopo inteiro do desenvolvimento hoteleiro, como prestação de serviço | Dono de terreno ou projeto | Fee por etapa ou escopo fechado |
| **Capital** | Estruturação para apresentar a bancos, crédito e investidores | Projeto que precisa de capital | Fee de estruturação e êxito sobre o captado |
| **Conhecimento** | Mentoria para quem quer desenvolver o próprio projeto | Desenvolvedor iniciante | Formação, mentoria e recorrência |
| **Parceria** | Zion Joint Venture: entra com as bubbles e entra no equity, desenvolvendo o destino | Terrenista com terra boa e sem capital | Participação no equity e no resultado |
| **Sustentabilidade** | Selos ambientais, crédito de carbono e projetos fotovoltaicos | Destino em desenvolvimento e portfólio próprio | Crédito de carbono, economia de energia e valorização por selo |

---

## 2. A escada

Os pilares não são silos, nem linhas de negócio paralelas disputando atenção. São
degraus de uma mesma escada, e cada um alimenta o seguinte:

```
CONHECIMENTO  →  atrai e educa o mercado, gera demanda qualificada
      ↓
DESENVOLVIMENTO  →  estrutura o projeto de quem não quer fazer sozinho
      ↓
CAPITAL  →  viabiliza o projeto estruturado diante de banco e investidor
      ↓
PRODUTO  →  equipa o destino viabilizado com bubbles e cabanas
      ↓
PARCERIA  →  converte produto e método em equity quando a terra é boa e falta capital
      ↓
SUSTENTABILIDADE  →  valoriza o destino e monetiza a terra que não vira edificação
```

Ler a escada de baixo para cima também funciona, e explica a estratégia: **a Zion só
consegue entrar em equity (Parceria) porque domina o desenvolvimento; só domina o
desenvolvimento porque opera o próprio produto; e só é procurada porque educa o mercado.**

---

## 3. O perfil financeiro de cada pilar

Aqui está a decisão real. Os seis pilares têm ciclos de caixa incompatíveis entre si:

| Pilar | Ciclo até o caixa | Capital exigido | Escalabilidade | Risco principal |
|---|---|---|---|---|
| Produto | curto (venda e entrega) | médio (produção) | alta | estoque e capacidade de entrega |
| Desenvolvimento | curto a médio (por etapa) | baixo | limitada por equipe | depende de gente sênior, não escala sozinho |
| Capital | médio (fee) a longo (êxito) | baixo | média | êxito não depende só da Zion |
| Conhecimento | imediato | baixo | altíssima | exige mídia constante |
| Parceria | longo (anos) | alto | baixa por operação | imobiliza capital e método num único destino |
| Sustentabilidade | muito longo | alto | média | crédito só entra após verificação |

**A tensão a administrar:** Parceria e Sustentabilidade consomem caixa hoje e pagam anos
depois. Produto, Desenvolvimento e Conhecimento pagam agora. Empurrar os seis ao mesmo
tempo, com o mesmo peso, é o caminho mais curto para descasamento de caixa — o mesmo erro
que quebra projeto de carbono, na escala da empresa inteira.

**A regra que decorre disso:** os pilares de ciclo curto financiam os de ciclo longo.
Conhecimento, Produto e Desenvolvimento sustentam o caixa que permite à Zion entrar em
Parceria e Sustentabilidade sem depender de captação externa para sobreviver.

---

## 4. Por onde cada lead entra

A base de leads da Zion já está segmentada por perfil. Cada perfil tem um pilar de entrada
natural — e um caminho de subida na escada:

| Perfil do lead | Entra por | Sobe para |
|---|---|---|
| Terrenista sem capital | Conhecimento ou Parceria | Parceria |
| Terrenista com capital | Desenvolvimento | Produto e Sustentabilidade |
| Projeto inicial | Conhecimento | Desenvolvimento e Capital |
| Investidor | Capital | Parceria |
| Operador hoteleiro | Produto | Desenvolvimento |
| Airbnb host | Produto | Conhecimento |

Qualificar o lead é, na prática, identificar por qual pilar ele entra. Oferecer o pilar
errado para o perfil errado é o desperdício comercial mais caro que existe: consome o mesmo
esforço de venda e converte a uma fração da taxa.

---

## 5. O que não pode acontecer em cada pilar

| Pilar | O erro que destrói o pilar |
|---|---|
| Produto | Vender unidade para destino sem viabilidade — a unidade vira símbolo do fracasso do cliente |
| Desenvolvimento | Assumir escopo inteiro sem etapa 0 validada, e carregar projeto que não deveria existir |
| Capital | Levar a banco ou investidor um projeto com número frágil — queima a credibilidade para todos os projetos seguintes |
| Conhecimento | Ensinar o método sem operação real por trás — vira infoproduto genérico e mata a autoridade |
| Parceria | Entrar em equity por terra ruim, ou sem cláusula de saída — imobiliza capital e método por anos |
| Sustentabilidade | Prometer crédito de carbono como receita antes de contrato e verificação — vira passivo reputacional |

O padrão é o mesmo nos seis: **o erro nunca é vender pouco, é vender o pilar errado ou
vender antes da hora.**

---

## 6. Como os pilares aparecem no sistema

| Pilar | Módulo do Zion Hotel AI Developer |
|---|---|
| Produto | Etapa 3 — Product Designer |
| Desenvolvimento | Etapas 0 a 4 e 6 |
| Capital | Etapas 2, 4 e 5 |
| Conhecimento | Transversal a todas as etapas |
| Parceria | Etapas 0 a 4 e módulo 7 (Land Bank) |
| Sustentabilidade | Módulo 7 — Land Bank |

O bloco de pilares é injetado no system prompt base de todos os agentes, então qualquer
análise gerada pelo sistema já sai sabendo por qual frente a oportunidade entra.

```bash
python -m src.main pilares                  # visão geral e a escada
python -m src.main pilares --pilar PARCERIA # detalhe de um pilar
python -m src.main pilares --etapa 5        # pilares alimentados por uma etapa
```

```python
from src.config.pilares import listar_pilares, obter_pilar, pilares_da_etapa
```

---

## 7. Decisões em aberto

Estes pontos ficaram fora da estrutura porque dependem de decisão do fundador, não de
modelagem. Estão registrados aqui para não se perderem:

1. **Produto vende avulso?** Bubble e cabana são vendidas para qualquer comprador, ou só
   dentro de projeto desenvolvido pela Zion? A resposta muda o volume e muda o risco
   reputacional do pilar.
2. **Qual é a porta de entrada primária?** Toda a comunicação pode apontar para um pilar
   só, ou a marca sustenta seis ofertas simultâneas sem confundir o mercado?
3. **Qual o teto de Parceria?** Quantos destinos em equity a Zion suporta ao mesmo tempo,
   dado que cada um imobiliza produto, método e gente sênior por anos?
4. **Sustentabilidade é pilar ou atributo?** Hoje ela vende sozinha, ou funciona como
   diferencial dos outros cinco? O Land Bank mostra que o caixa de carbono é longo demais
   para sustentar uma frente comercial isolada no curto prazo.
5. **Preço e fee por pilar.** Nenhum dos seis tem faixa de preço registrada no sistema.
   Enquanto não tiver, o sistema não consegue estimar receita por frente.
