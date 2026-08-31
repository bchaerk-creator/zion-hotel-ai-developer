# Carteira de Prospects

Repositório de clientes potenciais da Zion, com pontuação de aderência ao perfil
ideal e coleta opcional de páginas públicas via [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai).

## Como está dividido

| Camada | Onde | Dependência |
|---|---|---|
| Modelo do prospect | `src/models/prospect.py` | pydantic (já no projeto) |
| Repositório SQLite | `src/prospects/repositorio.py` | biblioteca padrão |
| Pontuação ICP | `src/prospects/icp.py` | nenhuma |
| Coleta web | `src/prospects/coletor.py` | **ScrapeGraphAI (opcional)** |
| CLI | `src/main.py`, grupo `prospects` | click, rich |

O núcleo roda no Python 3.11 do projeto, sem instalar nada novo. Só a coleta
automática exige o extra.

## Instalação

```bash
# Uso normal — importar CSV, pontuar, listar, exportar
pip install -e .

# Com coleta automática (~100 pacotes, exige Python 3.12+)
pip install -e ".[prospects]"
```

O ScrapeGraphAI 2.x **não roda em Python 3.11**. A 1.76 roda, mas está quebrada:
importa `ChatOllama` de um módulo que exige `langchain-community>=0.4`, versão em
que esse símbolo já não existe. Por isso o extra pede 3.12.

## Uso

```bash
# Importar uma planilha e pontuar cada linha
zion-ai prospects importar -f leads.csv --fonte "feira-abav-2026"

# Ver a fila de abordagem
zion-ai prospects listar --modalidade development --uf SC --score-minimo 7

# Painel da carteira
zion-ai prospects resumo

# Exportar (só quem pode ser abordado)
zion-ai prospects exportar -o output/prospects.csv

# Registrar pedido de oposição do titular
zion-ai prospects nao-contatar fazenda-santa-clara

# Coleta automática — requer o extra e OPENAI_API_KEY
zion-ai prospects coletar -u https://exemplo.com.br/hoteis --simular
```

Colunas aceitas no CSV de importação: `nome` (obrigatória), `empresa`, `email`,
`telefone`, `site`, `instagram`, `municipio`, `uf`, `bioma`, `area_ha`, `unidades`.

## Pontuação ICP

Heurística determinística de 0 a 10, em três blocos. Ordena a fila de abordagem;
não prevê fechamento.

| Bloco | Peso | O que pesa |
|---|---|---|
| Território | 3,0 | UF na praça prioritária (SC, RS, PR, SP, MG, RJ) ou de expansão; bioma com vocação mapeada |
| Ativo | 4,0 | Área entre 3 e 500 ha, ou 5 a 40 UHs em operação — a faixa onde o modelo Zion fecha conta |
| Acionabilidade | 3,0 | Canais de contato disponíveis; modalidade já definida |

Os pesos vivem no topo de `src/prospects/icp.py`. Ajuste conforme a praça mudar.

A modalidade é inferida do que a pessoa tem: terra sem operação → Development;
operação → Management. A distinção entre Management e Collection depende de
posicionamento, que nenhum dado coletado revela — fica para revisão humana.

## LGPD

A carteira trata dado de contato profissional para prospecção B2B. As guardas
não são enfeite:

**Em todo registro**
- `origem.fonte` e `origem.coletado_em` — de onde veio e quando. Sem isso não há
  como demonstrar boa-fé numa fiscalização da ANPD.
- `base_legal` — legítimo interesse (Art. 7º, IX) por padrão.
- `revisar_ate` — 365 dias. `prospects_vencidos()` lista o que passou do prazo;
  a LGPD manda não guardar além do necessário (Art. 15, I).

**Oposição do titular (Art. 18, § 2º)**
- `zion-ai prospects nao-contatar <id>` marca o registro e o tira da exportação.
- O registro **não é apagado**: manter o id com a marca é o que impede uma coleta
  futura de trazê-lo de volta sem ninguém perceber.

**Na coleta**
- `robots.txt` é consultado antes de qualquer requisição, e falha de rede nega.
- Intervalo mínimo de 2 s por domínio.
- Redes sociais estão na lista de bloqueio (`DOMINIOS_BLOQUEADOS`) — por decisão,
  não por limitação técnica.

**Nunca versionado:** `data/prospects/` está no `.gitignore`. A carteira é dado
de negócio e não entra no repositório.

Isto é engenharia de conformidade, não parecer jurídico. Antes de operar coleta
em escala, valide o programa com o jurídico de vocês.

## Custo da coleta

Cada página coletada é uma chamada de LLM. Usa a `OPENAI_API_KEY` e o
`ZION_MODEL` já configurados. Rode com `--simular` primeiro para ver o que sairia
antes de gravar e gastar.

## Testes

```bash
python -m unittest tests.test_prospects -v
```

30 testes, sem exigir ScrapeGraphAI instalado — inclusive um servidor local que
verifica se a guarda de `robots.txt` realmente distingue permitido de proibido,
em vez de só negar tudo.
