# 12 · Dashboard (especificação)

**Dono:** DATA. **Situação:** só especificação. O painel **não foi construído** (25/11/2026). Construir exige 'aprovado' de Bruno.

## Objetivo
Responder, todo dia e em um só lugar, se estamos vendendo, quanto custa vender e onde o funil perde, sem misturar o que foi medido com o que foi suposto.

## Perguntas diárias
A lista literal de perguntas diárias do Comando Mestre **deve ser conferida e colada aqui por Bruno ou pelo DIRECTOR**. Até lá, as perguntas abaixo derivam dos indicadores do comando e da auditoria:

1. Quanto foi gasto ontem, por campanha e no total?
2. Quantas vendas pagas houve (ClickMax e gateway), de qual oferta e por qual anúncio (UTM)?
3. Qual o custo por venda atribuída, comparado ao líquido da oferta?
4. Quantas visitas reais (sem tráfego de servidor), visualizações da oferta, inícios efetivos de checkout, Pix gerados e Pix pagos?
5. Onde está a maior perda entre uma etapa e a seguinte?
6. O Meta recebeu os mesmos Purchase que o ClickMax registrou? Qual a diferença em %?
7. Há reembolso, recusa ou Pix expirado no período?
8. Algum anúncio ou página ativa promete algo que a oferta não entrega?
9. Quais campanhas estão ligadas, com qual orçamento e qual evento de otimização?
10. O que mudou em produção desde ontem (conforme o LOG) e o que aguarda 'aprovado' de Bruno?

## Fontes de dados

| Fonte | O que traz | Limite conhecido |
|---|---|---|
| ClickMax (MCP) | Visitantes, vendas, UTMs, funil, ofertas, páginas, entrega | Só vê o que o gateway repassa (sem recusa, Pix expirado, abandono) |
| Ticto (extrato, por Bruno) | Todos os status de pagamento | Depende de Bruno exportar |
| Meta via Windsor | Gasto, impressões, cliques, eventos do pixel | Cache atrasa; guardar a hora da leitura |
| Gerenciador de Eventos (Bruno) | Eventos recebidos, deduplicação, qualidade | Só pelo painel |
| `14-historico-alteracoes/LOG.md` | Mudanças em produção | Só o que foi registrado |

## Classificação obrigatória de cada número

Todo valor no painel carrega um destes selos:

| Selo | Significa | Exemplo |
|---|---|---|
| **Real** | Lido na fonte, com data e hora | Vendas pagas no ClickMax |
| **Estimado** | Calculado a partir de real com regra declarada | Visitas sem tráfego de servidor |
| **Hipótese** | Cenário ou suposição, rotulado | CAC se todas as vendas viessem da campanha X |
| **Indisponível** | Não há como medir hoje, com dono e prazo | Recusa no checkout da Ticto |

Número sem selo não aparece. Indisponível nunca vira zero.

## Estrutura sugerida
1. Faixa de resultado do dia: gasto, vendas pagas, custo por venda atribuída, líquido (real).
2. Jornada: Impressão → Clique → Visita → Visualização da oferta → Início efetivo de checkout → Informação de pagamento → Pagamento pendente → Pagamento aprovado → Entrega → Reembolso, com perda entre etapas.
3. Conciliação ClickMax × gateway × Meta com diferença em %.
4. Campanhas ligadas (orçamento, evento de otimização, destino, UTM).
5. Alertas: promessa incompatível, página ligada a oferta inativa, rastreamento sem prova.
6. Mudanças em produção e pendências de Bruno.

## Regras
- Sem dado pessoal: nada de nome, e-mail ou telefone de lead ou comprador; só contagens e ids de plataforma.
- Painel só de leitura: não altera produção.
- Construção: tipo e ferramenta a definir com Bruno (por exemplo, um dashboard publicado ou dashboards nativos do ClickMax). Não escolhido.
