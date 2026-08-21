# Land Bank — Agregação Territorial e Crédito de Carbono

> Módulo transversal do Zion Hotel AI Developer. Não é uma etapa da Pirâmide Invertida©:
> roda em paralelo a todas elas, porque terra é insumo de todas.

---

## 1. A tese em uma frase

Uma gleba isolada quase nunca paga o custo fixo de um projeto de carbono. O que paga é o
**projeto agrupado**: várias glebas sob um único documento de concepção, uma única validação
e uma única linha de verificação. O Land Bank não é uma lista de terrenos — é uma máquina de
atingir escala mínima por cluster.

---

## 2. Por que agrupar

O custo de estruturar um projeto de carbono é praticamente o mesmo para 200 ha e para 2.000 ha:

| Item | Ordem de grandeza | Depende da área? |
|---|---|---|
| Documento de concepção (PDD) | R$ 250 mil | não |
| Validação por auditor credenciado | R$ 180 mil | pouco |
| Inventário florestal e mapeamento | R$ 150 mil | sim, mas com forte ganho de escala |
| Jurídico e cadeia dominial | R$ 80 mil | por gleba, não por hectare |
| Verificação (a cada 5 anos) | R$ 120 mil | pouco |
| MRV anual | R$ 60 mil fixos + R$ 25/ha | parcialmente |

Diluídos em 300 ha, esses custos inviabilizam o projeto. Diluídos em 1.500 ha, viram ruído.
Por isso o módulo trabalha com dois limiares configuráveis:

- **Escala mínima:** 500 ha elegíveis por cluster — abaixo disso, não estruturar.
- **Escala alvo:** 1.000 ha elegíveis por cluster — a partir daí o custo fixo deixa de mandar.

Consequência estratégica direta: **terra que leva um cluster subescala até o limiar vale mais
que terra maior que apenas engorda um cluster que já fechou escala.** A fila de agregação do
módulo aplica exatamente esse critério.

---

## 3. As rotas metodológicas

| Rota | Aplica-se a | tCO2e/ha/ano (Mata Atlântica) | CAPEX/ha | Observação |
|---|---|---:|---:|---|
| Restauração por plantio (ARR) | pastagem degradada, solo exposto | 14 | R$ 20 mil | maior volume, maior custo |
| Regeneração natural assistida | capoeira, regeneração inicial | 11 | R$ 8 mil | melhor custo por crédito quando há fonte de propágulo |
| Sistema agroflorestal (SAF) | área agrícola em transição | 7 | R$ 28 mil | receita agrícola paralela, fora deste modelo |
| Desmatamento evitado (REDD) | floresta nativa sob ameaça real | estoque × taxa de desmatamento | zero | exige demonstrar a ameaça |
| Manejo florestal melhorado (IFM) | floresta degradada | 2,5 | R$ 1,2 mil | volume baixo, entrada barata |

A engine sugere a rota a partir do uso do solo de cada talhão. Para forçar outra rota, use o
campo `metodologia_forcada` no talhão.

**A rota é a alavanca mais subestimada.** Trocar plantio por regeneração natural assistida onde
o sítio permite reduz o CAPEX em 60% e derruba o custo por crédito, ao preço de uma curva de
crescimento mais lenta. Vale rodar as duas configurações antes de fechar contrato.

---

## 4. O que mata uma gleba

Bloqueios duros — a área não gera crédito enquanto não forem resolvidos:

- **Supressão de vegetação nativa dentro da janela de corte de 10 anos.** Inviabiliza rota de
  remoção e contamina as salvaguardas do projeto inteiro. Uma gleba assim dentro de um cluster
  é risco para todas as outras.
- **Litígio dominial.** Sem cadeia dominial limpa não há titularidade do crédito. Nenhum
  standard registra, nenhum comprador sério assina.
- **Sobreposição com terra indígena, território quilombola ou unidade de conservação de
  proteção integral.** Exige consulta livre, prévia e informada concluída antes de qualquer
  passo. Não é obstáculo burocrático, é requisito de legitimidade.

Pendências sanáveis — atrasam, não matam:

- CAR inexistente ou com pendência. Regularizar antes do PDD.
- Matrícula sem georreferenciamento.
- Ausência de coordenadas do centroide (impede clusterizar com precisão).

Potencial condicionado — não usar em captação:

- Área com passivo legal de recomposição (APP e Reserva Legal). Restaurar ali já é obrigação
  legal, então a adicionalidade é contestável. O módulo separa esses hectares do núcleo
  bancável de propósito. Eles podem entrar no projeto mais adiante, com tese de adicionalidade
  bem construída, mas **não entram em projeção apresentada a investidor**.

---

## 5. Instrumentos de agregação

Comprar terra é o caminho mais caro e quase nunca o melhor. O que precisa ser travado é o
**direito ao crédito**, pelo prazo do período de creditação.

| Instrumento | Quando usar | Cuidado central |
|---|---|---|
| Compra | terra colada no ativo hoteleiro, com valor de uso além do carbono | imobiliza capital que renderia mais em originação |
| Arrendamento de carbono | restauração de longo prazo em área de terceiro | o prazo precisa cobrir todo o período de creditação, com sucessão amarrada |
| Cessão de direitos de carbono | floresta em pé, dono quer manter a terra | definir titularidade do crédito com precisão registral |
| Parceria com repartição de receita | dono quer participar do resultado | definir se o split é sobre receita bruta ou líquida |
| Servidão ambiental | proteção de longo prazo averbada na matrícula | avaliar antes de averbar, o efeito é duradouro |
| Permuta por participação | dono quer virar sócio do destino | alinha incentivo, mas dilui equity |

### O split é uma alavanca, não uma formalidade

Repartir 40% da **receita bruta** com o terrenista enquanto a Zion banca 100% do CAPEX de
restauração não é prática de mercado — é transferir risco para quem paga a conta. O modelo
default do módulo usa `base_reparticao = "liquida"`: a Zion recupera o custo investido e o
que sobra é repartido. Mesmo percentual, resultado completamente diferente, sem mexer em
uma tonelada sequer.

---

## 6. O descasamento de caixa

É aqui que projeto de carbono quebra, e não por falta de tonelada:

```
ano 0        CAPEX de restauração + estruturação saem do caixa
ano 1-4      só custo: manutenção do plantio, MRV, proteção da área
ano 5        primeira verificação → primeira emissão → primeiro real entra
ano 5-30     emissões a cada ciclo de verificação
```

Quatro a cinco anos de caixa negativo antes do primeiro crédito. Quatro alavancas resolvem,
nesta ordem de custo:

1. **Escala** — agregar área dilui custo fixo sem aumentar custo por hectare. É a alavanca mais barata.
2. **Rota metodológica** — regeneração natural assistida no lugar de plantio, onde o sítio permitir.
3. **Split** — repartição sobre receita líquida, após recuperação do CAPEX.
4. **Pré-venda com adiantamento** — offtaker paga adiantado aceitando deságio. É financiamento,
   não receita extra: só depois de esgotar as três anteriores.

O módulo calcula, por cluster, o **preço de equilíbrio** (quanto o crédito precisa valer para
o VPL zerar) e a **pré-venda mínima** (que fração precisa ser vendida adiantado para o VPL
virar no preço modelado). São os dois números que decidem a conversa.

---

## 7. Checklist documental por gleba

Antes de qualquer real de CAPEX:

- [ ] Matrícula atualizada, com georreferenciamento e cadeia dominial de 20 anos
- [ ] CAR ativo, sem pendência, com polígono compatível com a matrícula
- [ ] Certidões negativas: federal, estadual, municipal, trabalhista e ambiental
- [ ] Confirmação de ausência de sobreposição com TI, território quilombola e UC
- [ ] Histórico de cobertura vegetal dos últimos 10 anos (para a janela de corte)
- [ ] Situação de posse efetiva: quem está na área hoje e sob qual título
- [ ] Contrato com cláusula expressa de titularidade do crédito de carbono
- [ ] Prazo de vinculação da área compatível com o período de creditação
- [ ] Cláusula de sucessão: o compromisso sobrevive à venda da terra

---

## 8. Sequência de 24 meses

| Trimestre | Foco | Marco verificável |
|---|---|---|
| T1 | Originação e triagem | portfólio mapeado, glebas bloqueadas descartadas |
| T2 | Regularização documental | CAR e matrícula regulares nas glebas do cluster âncora |
| T3 | Contratação | escala mínima atingida com instrumentos assinados |
| T4 | Inventário de campo | fatores de remoção medidos substituindo os paramétricos |
| T5 | PDD e escolha do standard | documento de concepção submetido |
| T6 | Validação | projeto validado por auditor credenciado |
| T7 | Implantação | primeira safra de restauração plantada |
| T8 | Offtake | contrato de pré-venda assinado |

Regularização documental **antes** de CAPEX. Sempre. Plantar em terra com pendência dominial
é converter capital em passivo.

---

## 9. Acoplamento com a tese hoteleira

A camada de carbono não é um negócio paralelo, é um multiplicador do ativo turístico:

- **Narrativa de destino.** Restauração visível é ativo de experiência do hóspede, não custo
  ambiental. Trilha, viveiro, monitoramento de fauna, plantio pelo hóspede.
- **Atratividade para capital com mandato ESG.** Muda o perfil de investidor acessível e a
  estrutura de dívida disponível.
- **Uso do solo.** Área restaurada é área que não seria edificável de qualquer forma. O carbono
  monetiza o que já estava fora do master plan.
- **Retenção de terra.** O contrato de carbono trava a área por 30 anos por um custo de entrada
  muito menor que a compra, preservando a opção de desenvolvimento futuro no entorno.

**O que não pode ser prometido a investidor:** volume de crédito de área não contratada, prazo
de emissão (depende de auditor e registro), receita de área com adicionalidade condicionada, e
preço futuro de tCO2e. Potencial é pipeline; só o contratado é estoque, e o relatório separa os
dois em toda tabela justamente por isso.

---

## 10. Como usar o módulo

```bash
# Análise determinística — roda sem chave de API
python -m src.main land-bank --input data/exemplo_land_bank.json

# Com relatório em Markdown e exportação JSON
python -m src.main land-bank -i data/exemplo_land_bank.json \
    -o output/land_bank.md --json output/land_bank.json

# Com a camada estratégica de IA (requer OPENAI_API_KEY)
python -m src.main land-bank -i data/exemplo_land_bank.json --ia

# Pelo orquestrador, como módulo 7
python -m src.main run --stage 7 --input data/exemplo_land_bank.json
```

Via código:

```python
from src.agents.land_bank_agent import LandBankAgent

agent = LandBankAgent()
resultado, relatorio = agent.analisar(dados)   # determinístico
saida = agent.execute(dados)                   # + estratégia com LLM
```

### Estrutura do arquivo de entrada

`data/exemplo_land_bank.json` é a referência completa. O essencial por gleba:

```json
{
  "id": "GL-URU-02",
  "nome": "Fazenda Rio Bonito",
  "municipio": "Rio Rufino",
  "uf": "SC",
  "bioma": "mata_atlantica",
  "latitude": -27.9163,
  "longitude": -49.7789,
  "area_total_ha": 640.0,
  "status_dominial": "em_negociacao",
  "instrumento": "arrendamento_carbono",
  "percentual_receita_terrenista": 0.35,
  "car_ativo": true,
  "matricula_regular": true,
  "custo_negociacao_brl": 180000.0,
  "talhoes": [
    {"id": "T1", "area_ha": 420.0, "uso_solo": "pastagem_ativa"},
    {"id": "T2", "area_ha": 180.0, "uso_solo": "floresta_conservada"},
    {"id": "T3", "area_ha": 40.0, "uso_solo": "corpo_dagua"}
  ]
}
```

Sem talhões mapeados, informe `uso_solo_predominante` e a gleba é avaliada como talhão único —
com a pendência registrada no relatório.

---

## 11. Limites do modelo

O que este módulo **é**: uma ferramenta de priorização territorial e dimensionamento de tese.
Serve para decidir qual terra perseguir primeiro, quanta área falta para um cluster fechar
conta e qual alavanca puxar.

O que este módulo **não é**: substituto de inventário florestal de campo, de análise dominial
por advogado, de consulta a comunidades ou de documento de concepção de projeto. Os fatores de
remoção por bioma, os preços de crédito e os custos são ordens de grandeza calibradas sobre
referências públicas do mercado voluntário brasileiro. Antes de contrato, captação ou emissão,
todos precisam ser substituídos por dado medido e cotação real.

Pontos específicos a calibrar quando houver dado de campo:

- Taxa de desmatamento da linha de base — hoje é um parâmetro único, quando deveria ser
  regional e específico por cluster.
- Fatores de remoção — variam com sítio, espécies, histórico de uso e regime de chuvas dentro
  do mesmo bioma.
- Preço do crédito — depende de standard, safra, co-benefícios certificados e do comprador.
- Custo de implantação — varia com topografia, distância de viveiro e disponibilidade de mão de obra.

O marco regulatório brasileiro de mercado de carbono está em fase de regulamentação. A
titularidade do crédito, o tratamento tributário e a interação com o mercado regulado devem ser
confirmados com assessoria jurídica antes de cada contrato — este módulo não substitui essa
verificação.
