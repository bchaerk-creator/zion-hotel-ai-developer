# Zion Knowledge Engine™

> Sistema central de conhecimento da Zion Hospitality Academy.
> Código: [`src/knowledge/`](../src/knowledge/) · Consulta: `python -m src.main knowledge`

---

## 1. O que este módulo é — e o que ele ainda não é

O Knowledge Engine se declara **fonte de verdade do Método Zion 360°**. Hoje ele é a
**estrutura** dessa fonte de verdade, não o conteúdo dela.

O motivo é simples e não deve ser contornado: os sete livros da Zion, o livro-mãe
*Transforme Seu Terreno em um Destino Turístico* e os materiais da mentoria **não estão
carregados no sistema**. Popular os bancos de conceitos a partir de memória seria violar a
Regra Suprema do próprio método — não inventar — logo no primeiro ato.

Então o que existe hoje:

- o **schema completo** com proveniência, hierarquia de sete níveis, versionamento e status;
- o **grafo** que conecta conceito → pilar → ferramenta → entregável → decisão → próximo pilar;
- a **auditoria** que expõe lacunas, divergências e afirmações sem fonte;
- **64 itens** populados apenas com o que é verificável: o que está implementado neste
  repositório e o que o fundador declarou explicitamente em sessão registrada.

Cada item traz a fonte. Cada ferramenta citada sem definição disponível entra com nome e
função preservados e status `PENDENTE_DE_FONTE` — nunca com conteúdo inventado.

---

## 2. Hierarquia da informação

| Nível | Tipo | Exemplo registrado |
|---|---|---|
| 1 | Princípio | "Comece pelo território" |
| 2 | Método | Método Zion 360° |
| 3 | Framework | Pirâmide Invertida© · Land Bank |
| 4 | Ferramenta | Zion Score™ · Engine de Carbono |
| 5 | Processo | Sequência dos sete pilares |
| 6 | Entregável | Diagnóstico Territorial |
| 7 | Case | *nenhum documentado* |

---

## 3. Proveniência — a distinção que sustenta tudo

Toda informação é marcada como **ZION** (vem dos materiais), **EXTERNO** (pesquisa ou
conhecimento de mercado) ou **INFERÊNCIA** (conclusão estratégica).

Inferência nunca se apresenta como metodologia oficial. Exemplo registrado na base: o
conceito de descasamento de caixa em ciclo longo, derivado da modelagem do Land Bank, está
marcado como INFERÊNCIA — é uma boa ideia, mas não é método Zion documentado.

Há também uma distinção mais sutil, implementada em código: **fonte disponível não é o mesmo
que conteúdo verificável.** O IPM-Z™ tem fonte disponível (o fundador o citou), mas conteúdo
não verificável (a definição não existe no sistema). `verificar_fonte` reporta os dois campos
separadamente, exatamente para que ninguém confunda "foi mencionado" com "está documentado".

---

## 4. Três divergências que precisam da sua decisão

O método existe hoje em dois mapas: a **Pirâmide Invertida©** (sete etapas, implementada
neste repositório) e o **Método Zion 360°** (sete pilares). Eles não são o mesmo mapa com
nomes diferentes. A regra do método proíbe escolher em silêncio, então as três divergências
estão registradas e nenhuma foi resolvida:

### D_ORDEM_PRODUTO_INVESTIMENTO
Na Pirâmide, a Viabilidade Econômico-Financeira (Etapa 2) vem **antes** de Produto (Etapa 3).
No 360°, Produto (03) vem **antes** de Investimento (05).

**Impacto:** muda o que o developer decide primeiro. Na Pirâmide, o número restringe o
produto. No 360°, o produto define o número a ser testado. São teses diferentes sobre como
se desenvolve, não diferença de redação.

### D_LANCAMENTO_AUSENTE
O 360° tem sete pilares; a Pirâmide termina na Etapa 6 (governança de implantação) e não
cobre Lançamento.

**Impacto:** dois dos onze erros documentados de developer são de lançamento — lançar tarde
e não criar demanda antes da abertura. O framework implementado no sistema não tem etapa que
os combata.

### D_NOME_INVESTIMENTO
"Investimento" no 360° pergunta *os números fecham?* — é viabilidade. Na Pirâmide, a Etapa 5
é captação, e viabilidade é a Etapa 2.

**Impacto:** aluno, mentor e agente de IA podem usar a mesma palavra para viabilidade e para
captação. É o tipo de ambiguidade que corrompe material didático e conversa comercial ao
mesmo tempo.

---

## 5. O que a auditoria encontra hoje

`python -m src.main knowledge` roda AUDITAR MÉTODO. Estado atual: **10 achados, 4 bloqueantes**.

Bloqueantes:
- 3 divergências entre fontes oficiais sem resolução
- 3 ferramentas com nome preservado e conteúdo ausente (IPM-Z™, DNA do Território™, Launch System)
- nenhum case com resultado documentado — **nenhuma prova pode ser afirmada por este sistema**
- 8 lacunas de fonte primária

Altas:
- ADR de R$ 1.571 e margem EBITDA de 43,46% circulam sem período de apuração
- pilares Produto, Estratégia e Implantação sem ferramenta documentada
- 5 das 10 decisões do developer não têm ferramenta Zion que as sustente

A matriz Conhecimento → Decisão mostra o mesmo de outro ângulo: dos sete pilares, três não
têm instrumentação completa.

---

## 6. O que carregar para destravar

Em ordem de impacto:

1. **Os sete livros e o livro-mãe.** Destravam o banco de conceitos inteiro.
2. **IPM-Z™.** É a ferramenta do pilar Mercado — sem ela, as decisões 02 e 03 ficam sem apoio.
3. **Um case completo** com contexto, decisão, execução e resultado. Sem isso o sistema não
   fornece prova para narrativa, oferta ou captação.
4. **Período e demonstrativo dos números de Urubici.** Enquanto não houver, esses números não
   deveriam sair em material externo.
5. **DNA do Território™ e Launch System.**

---

## 7. Como usar

```bash
python -m src.main knowledge                      # AUDITAR MÉTODO
python -m src.main knowledge --mapear "carbono"   # MAPEAR CONHECIMENTO
python -m src.main knowledge --fonte FE_IPM_Z     # VERIFICAR FONTE
python -m src.main knowledge -o output/auditoria.md
```

```python
from src.agents.knowledge_agent import KnowledgeAgent

agent = KnowledgeAgent()
agent.auditar_metodo()                 # determinístico
agent.conectar("C_TERRITORIO_PRIMEIRO")  # a cadeia completa do conceito
agent.ensinar("Zion Score")            # modo professor, com LLM
agent.criar_aula("Território")         # modo aula
agent.avaliar("Diagnóstico Territorial", conteudo)  # modo avaliação
```

A camada determinística roda sem chave de API. Os modos com LLM recebem, junto com a
pergunta, o estado real da base — incluindo as lacunas nomeadas e as divergências não
resolvidas. É essa injeção que impede o modelo de preencher buraco com invenção.
