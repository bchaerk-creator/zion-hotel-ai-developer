# Zion CRM & Lead Intelligence™

> Qualificação, roteamento e inteligência comercial sobre a base de leads.
> Código: [`src/crm/`](../src/crm/) · Uso: `python -m src.main crm -i <base.json>`

---

## 1. A pergunta que o CRM existe para responder

Não é "quem está na base". É:

> **Quem devemos contactar, por quê, com qual oferta e qual é o próximo passo?**

Todo lead precisa ter contexto, classificação, estágio, potencial e próxima ação. Faltando
qualquer uma, o CRM está incompleto — e a auditoria de higiene aponta exatamente isso.

---

## 2. Zion Lead Score™

Oito dimensões, de 0 a 10, com pesos:

| Dimensão | Peso | O que mede |
|---|---:|---|
| FIT | 18% | O perfil combina com a Zion |
| ATIVO | 15% | Possui terreno, capital, operação, projeto, marca, experiência, rede |
| CAPITAL | 14% | Capacidade financeira |
| URGÊNCIA | 13% | Existe necessidade real e prazo |
| PROJETO | 12% | Existe projeto concreto e em que estágio |
| AUTORIDADE | 12% | Pode decidir |
| POTENCIAL | 11% | Tamanho da oportunidade |
| ENGAJAMENTO | **5%** | Está interagindo |

**Engajamento tem deliberadamente o menor peso.** Um lead pode curtir todo conteúdo e nunca
comprar; outro pode não interagir e ter um terreno de 150 ha com capital em caixa. Fit,
ativo, intenção, capacidade e momento valem mais — e o modelo é construído para que isso seja
verdade, não apenas uma frase.

### Score e confiança são coisas diferentes

Esta é a decisão de modelagem mais importante do módulo.

O score é calculado **apenas sobre as dimensões conhecidas**. Dimensão não levantada não vira
nota zero — ela reduz a **confiança**, que é reportada separadamente.

Por quê: um lead sem informação não é um lead ruim, é um lead **não qualificado**. O erro
clássico de CRM é enterrar lead bom por falta de dado. Aqui, confiança abaixo de 50% gera
alerta explícito recomendando qualificar, nunca descartar.

Cada dimensão reporta ainda se sua nota foi `informada` (dado explícito), `derivada`
(inferida de outro campo) ou `desconhecida`. O briefing mostra a composição inteira, então
ninguém precisa confiar no número sem ver de onde ele veio.

---

## 3. Temperatura

| | Critério |
|---|---|
| 🔥 **Oportunidade** | Projeto concreto **e** estágio em oferta, negociação ou decisão |
| 🟢 **Quente** | Score ≥ 7, confiança ≥ 50%, **e** autoridade, urgência e capital juntos |
| 🟡 **Morno** | Existe interesse e objetivo declarado, sem os elementos de decisão |
| 🔴 **Frio** | Pouca informação, sem urgência, sem objetivo |

Quente exige os cinco elementos simultâneos. Um lead com terreno enorme e capital, mas que
não é o decisor, **não é quente** — por mais alto que seja o score.

---

## 4. Roteamento e a regra de não empurrar venda

| Situação | Porta |
|---|---|
| Terreno + dúvida | Diagnóstico |
| Terreno + quer aprender | Mentoria |
| Terreno + quer delegar | Desenvolvimento |
| Projeto + precisa de capital | Capital |
| Capital + busca oportunidade | Investimento |
| Operação + quer melhorar | Management |
| Fit estratégico real | Parceria |
| Incerteza declarada | Diagnóstico |

O roteamento devolve também **o que não ofertar agora**, e isso é tão importante quanto a
porta:

- Se o lead ainda não sabe o que construir → não vender bubble.
- Se ainda não sabe se o terreno é viável → não vender desenvolvimento.
- Se não tem projeto → não vender captação.
- Se ainda não passou por qualificação → nenhuma proposta fechada.

Na base de exemplo, um lead chega pedindo preço de cinco bubbles, com capital e sem terreno
nem projeto. O sistema roteia para **Diagnóstico**, não para Produto, e registra por escrito:
*"vender unidade agora seria empurrar produto para um destino que não existe."*

---

## 5. Higiene da base

`LIMPAR CRM` detecta, por gravidade:

**Bloqueante** — lead sem canal de contato; lead aberto sem próxima ação; perda sem motivo registrado.

**Alta** — duplicidade por e-mail, telefone ou nome; lead sem perfil; follow-up vencido; lead
aberto parado há mais de 30 dias; negócio sem responsável.

**Média** — e-mail inválido; oportunidade sem valor potencial.

Duas regras merecem destaque, porque são as mais violadas na prática:

> **"Aguardando retorno" não é gestão.** Todo lead aberto precisa de ação, data e responsável.

> **"Perdido" sem motivo é proibido.** Perda sem explicação destrói a capacidade de aprender
> com o funil — e, na lista de reativação, o lead perdido sem motivo aparece com a observação
> de que, se ninguém sabe por que ele saiu, não há razão para ele não voltar.

---

## 6. Análise de funil

O gargalo é a maior queda percentual entre etapas consecutivas, e o diagnóstico depende de
**onde** ela acontece:

- Queda no topo → o problema é **qualificação**. Entram leads que não deveriam entrar.
- Queda no meio → o problema é **diagnóstico**. O lead conversa mas não enxerga valor.
- Queda no fim → o problema é **oferta ou preço**. O lead entende o valor e não fecha.

Nunca otimizar por achismo: se o volume for insuficiente para sustentar a conclusão, o
módulo diz que é insuficiente em vez de inventar um padrão.

---

## 7. Reativação

`ZION REACTIVATION LIST™` recupera leads parados há mais de 30 dias e perdas recuperáveis
(timing, adiou, não respondeu, sem decisão — e perdas sem motivo registrado), filtrando por
score mínimo. Para cada um: contexto, dias parado, provável problema, porta potencial e
abordagem recomendada.

O princípio: **silêncio não é desinteresse.** Pode ser falta de tempo, mensagem errada,
timing, canal inadequado, falta de confiança ou oferta errada. Antes de perder, requalificar.

---

## 8. Como usar

```bash
python -m src.main crm -i data/exemplo_base_comercial.json
python -m src.main crm -i data/exemplo_base_comercial.json --lead LD-007   # briefing de reunião
python -m src.main crm -i data/exemplo_base_comercial.json -o output/comercial.md
python -m src.main crm -i data/exemplo_base_comercial.json --ia            # leitura estratégica
```

```python
from src.agents.crm_agent import CRMAgent

agent = CRMAgent()
relatorio, markdown = agent.analisar(dados)     # determinístico
agent.qualificar_lead(lead)                     # score + roteamento
agent.preparar_reuniao(lead)                    # briefing completo
```

Tudo que é cálculo roda sem chave de API. O LLM entra apenas na leitura de padrão e na
abordagem comercial, e recebe os números já calculados com instrução explícita de não
recalculá-los.

---

## 9. Integração com o HubSpot

O módulo hoje lê JSON. O schema em [`src/crm/models.py`](../src/crm/models.py) foi desenhado
espelhando os campos recomendados para o HubSpot — dados, perfil, ativo, financeiro, projeto
e comercial — então a integração é um adaptador de leitura, não uma remodelagem.

Antes de conectar, vale usar a lista de higiene como especificação dos campos obrigatórios:
os achados bloqueantes são exatamente os campos que, ausentes, tornam a operação comercial
impossível.
