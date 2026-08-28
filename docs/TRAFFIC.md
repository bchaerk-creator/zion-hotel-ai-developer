# Zion Traffic & Acquisition Architect™

> Aquisição digital: do gate de campanha à receita atribuída.
> Código: [`src/traffic/`](../src/traffic/) · Uso: `python -m src.main traffic -i <conta.json>`

---

## 1. A métrica que manda

Custo por lead não é a métrica. Custo por cliente é melhor. Receita por real investido é a
verdadeira. E entre elas existe uma que quase nenhuma conta acompanha:

> **CPQO — custo por oportunidade qualificada.**

Mil leads baratos podem valer menos que dez oportunidades reais. O módulo calcula o CPQO com
o mesmo destaque que o CPL e usa ele, não o CPL, como critério de escala.

---

## 2. O gate — antes de qualquer campanha

Dez perguntas precisam de resposta antes de a campanha existir: o que vendemos, para quem,
qual problema, qual desejo, qual transformação, qual oferta, qual preço, qual funil, qual
evento de conversão, qual meta financeira.

Faltando qualquer uma, o veredito é literal: **NÃO CRIAR CAMPANHA AINDA.**

Não é burocracia. Cada pergunta sem resposta é uma decisão que será tomada por acaso depois,
com dinheiro rodando. O gate também checa a estrutura de medição — evento de conversão, UTM,
destino, meta de CAC ou CPQO, criativos com hook declarado. Sem UTM, a venda nunca volta
para a campanha que a gerou, e a conta inteira fica cega.

---

## 3. Diagnóstico: o gargalo é o primeiro ponto que quebra

A cadeia é percorrida em ordem:

```
público → criativo → clique → página → lead → qualificação → oferta → venda → receita
```

E o gargalo é o **primeiro** ponto que quebra, não o mais visível. Poucas vendas quase nunca
é problema de venda — é consequência de algo anterior.

| Sintoma | Causa provável |
|---|---|
| CTR abaixo da referência | Hook, criativo ou mensagem |
| CPC alto | Consequência do CTR, não causa própria |
| Muitos cliques, poucas conversões | Landing page ou oferta |
| Muitos leads, poucas oportunidades | Público ou promessa que atrai quem não tem ativo |
| Muitas oportunidades, poucas vendas | Oferta, comercial ou fechamento |

Os limiares são **referências de mercado, não benchmarks Zion** — servem para levantar
suspeita, não para provar nada, e devem ser recalibrados com o histórico da conta.

---

## 4. Nenhum threshold arbitrário

A regra do método diz para nunca aplicar limiar sem considerar volume estatístico. Isso virou
código de verdade:

**"Gastei e não converteu."** O módulo calcula a probabilidade de observar zero conversões se
a campanha fosse tão boa quanto a referência. Com 15 cliques e conversão esperada de 10%, a
chance de zero leads é 21% — ainda é ruído, e pausar seria decisão por impaciência. Com 500
cliques, a chance cai para menos de 0,1% — aí o zero é evidência, e a ação é verificar
rastreamento antes de pausar.

**Teste A/B.** Dois criativos com CTR diferente podem ser o mesmo criativo com sorte
diferente. `comparar_proporcoes` roda um teste z de duas proporções e só declara vencedor com
p < 0,05. Com 11% contra 9% em 100 impressões cada, a resposta é explícita: não declarar
vencedor ainda.

**Volume mínimo.** Antes de julgar qualquer coisa: 1.000 impressões, 100 cliques, 25 leads.
Abaixo disso a decisão é `aguardar_volume`, não um palpite com aparência de análise.

---

## 5. Escala

Nunca escalar só porque "está vendendo". A decisão `escalar` exige, cumulativamente: CAC
dentro da meta, pelo menos 10 vendas (abaixo disso o CAC observado não é estável), margem
cobrindo o investimento, cadeia sem gargalo e CPQO dentro da meta.

Há uma armadilha que o módulo bloqueia explicitamente: **CPL ótimo com CPQO ruim**. Lead
barato que não vira negócio — escalar ali só multiplica volume de lead errado.

E há o que nenhum dado de mídia mostra. O módulo sempre devolve, como bloqueio declarado:

> Confirmar fora do sistema: capacidade comercial de atender mais oportunidades e capacidade
> de entrega do produto vendido.

---

## 6. O loop com o CRM — a peça central

A plataforma de anúncios sabe quanto custou o lead. Só o CRM sabe se aquele lead virou
negócio. Cruzar os dois pela UTM responde a pergunta que o relatório de plataforma nunca
responde:

> **Qual campanha gerou os clientes — não qual gerou mais leads.**

Rodando na amostra deste repositório, o resultado é exatamente o caso que o método prevê:

- A campanha do **livro** lidera em volume de leads.
- A campanha de **desenvolvimento no Google** é a que gera receita: R$ 420.000 de um único
  cliente, contra R$ 4.900 da campanha do livro.

Otimizar por custo por lead teria escalado a campanha errada. O módulo marca a divergência de
ranking automaticamente e diz o que fazer com cada lado: lead barato que não converte não
escala; lead caro e bom é candidato a mais orçamento.

**Alerta de rastreamento.** Quando a plataforma reporta muito mais lead do que o CRM tem
atribuído, o módulo interrompe qualquer conclusão sobre qualidade: o problema é a passagem de
UTM, não a campanha. Julgar qualidade com metade dos dados faltando é pior que não julgar.

---

## 7. Como usar

```bash
# Só a conta de tráfego
python -m src.main traffic -i data/exemplo_conta_trafego.json

# Com atribuição real de receita via CRM
python -m src.main traffic -i data/exemplo_conta_trafego.json --crm data/exemplo_base_comercial.json

# Com relatório e leitura estratégica de IA
python -m src.main traffic -i data/exemplo_conta_trafego.json \
    --crm data/exemplo_base_comercial.json -o output/aquisicao.md --ia
```

```python
from src.agents.traffic_agent import TrafficAgent

agent = TrafficAgent()
relatorio, markdown = agent.analisar(dados, dados_crm)   # determinístico
agent.criar_copy(campanha)                               # ângulos de performance
agent.criar_campanha(briefing)                           # estratégia completa
```

Métricas, gate, diagnóstico, decisão e atribuição rodam sem chave de API. O LLM entra em
copy, criativo, estrutura e leitura estratégica — recebendo os números já calculados com
instrução de não recalculá-los.

---

## 8. Fronteiras com os outros módulos

Este módulo **não inventa** promessa, posicionamento, mecanismo, prova ou preço — isso vem da
oferta. **Não inventa** conceito, ferramenta ou case Zion — isso vem do
[Knowledge Engine](KNOWLEDGE_ENGINE.md), e se não houver case documentado, não se afirma
prova. E trabalha com o [CRM](CRM.md) para saber quais campanhas geram clientes.

Vale registrar o que a auditoria do Knowledge Engine já apontou: **não existe hoje nenhum
case com resultado documentado no sistema.** Enquanto isso não mudar, nenhuma campanha da
Zion deveria afirmar prova de resultado em criativo ou landing page.

---

## 9. Integração com plataformas

O módulo hoje lê JSON. Os campos de `MetricasCampanha` espelham o que Meta Ads e Google Ads
exportam — investimento, impressões, cliques, visitas, leads — e os campos de qualificação
vêm do CRM. A integração com API de plataforma é um adaptador de leitura.

Quando houver acesso de escrita a uma plataforma, vale a regra do método: nunca alterar
campanha crítica sem verificar os dados, e nunca executar alteração sem confirmação explícita
da mudança específica.
