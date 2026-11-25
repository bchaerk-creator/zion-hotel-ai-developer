# 12 · Dashboard (especificação)

**Dono:** DATA (indicadores: FINANCE). **Situação (25/11/2026):** painel comercial P0 preparado em `dashboard.html` (somente leitura, sem dados reais no repositório). Definições em `INDICADORES_P0.md`. Publicar ou conectar a produção continua exigindo 'aprovado' de Bruno.

## Objetivo
Responder, todo dia e em um só lugar, se estamos vendendo, quanto custa vender e onde o funil perde, sem misturar o que foi medido com o que foi suposto.

## Perguntas diárias
Lista literal do Comando Mestre (13 perguntas):

1. Quanto investimos?
2. Quantas vendas foram aprovadas?
3. Qual produto vendeu?
4. Qual anúncio vendeu?
5. Qual foi o CPA?
6. Qual foi o custo por checkout?
7. Qual foi a conversão do checkout?
8. Qual foi a receita após taxas?
9. Qual foi a margem?
10. Onde estamos perdendo compradores?
11. Quais criativos precisam ser renovados?
12. Quais campanhas possuem condições de escala?
13. Qual é o próximo gargalo a resolver?

**Regras do comando para o painel:**
- diferenciar dados reais, estimativas, hipóteses e dados indisponíveis;
- priorizar compras aprovadas e receita conciliada;
- mostrar indicadores por conta, campanha, conjunto, anúncio, produto e origem de tráfego.

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


## Painel P0 pronto para uso (25/11/2026)
Arquivos: `dashboard.html` (página única, mobile-first, sem CDN), `gerar_dados.py`, `dados_exemplo.json` (**dados fictícios**), `exemplos/MODELO_*.csv` (fictícios), `INDICADORES_P0.md`, testes `test_gerar_dados.py` e `test_dashboard.js`.

1. Exporte (fora do repositório) Meta por dia e anúncio, vendas do ClickMax, eventos do funil (ClickMax/GTM) e, se tiver, o extrato da Ticto. Colunas em `exemplos/MODELO_*.csv` e no topo de `gerar_dados.py`.
2. Gere o JSON: `python3 -I gerar_dados.py --meta meta.csv --vendas vendas.csv --eventos eventos.csv --ticto ticto.csv --saida dados.json --checkout-start efetivo|carregamento|desconhecido` (sem `--ficticio`: o rótulo vira "dados reais").
3. Abra `dashboard.html` por um servidor local (`python3 -m http.server`) ou carregue o arquivo no botão da página. Para abrir por duplo clique: acrescente `--html-base dashboard.html --html-saida painel.html` (JSON embutido).
4. `dados.json`, `painel*.html` e CSVs reais ficam **fora** do repositório (`.gitignore`).

Testes: `python3 -I test_gerar_dados.py` e `node test_dashboard.js` (Playwright, 390×844 e 1366×800).
