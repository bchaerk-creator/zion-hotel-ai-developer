# ZAIOS · Premissas financeiras, verificação de recursos e G2

Data: 08/11/2026. Documento só de leitura e análise: nada foi alterado na ZAIOS, no ClickMax ou no Lovable, e nenhum crédito foi consumido.

Situação da plataforma: **não validada**. Ela só conta como validada depois que o teste fechado de 15 itens for feito por pessoas e o resultado for registrado (ver `ENTREGAS_VALIDACAO_ACADEMY.md`).

---

## Parte 1 · Premissas financeiras de F01, F02 e F03

Nenhuma premissa abaixo está aprovada. Cada uma traz o valor, de onde vem, a fórmula, o resultado esperado no caso de referência, a sensibilidade e onde aparece na ZAIOS. Os casos usam **dados fictícios**. Cenários, não promessas.

### 1.1 Resumo para decisão

| # | Premissa | Valor hoje | Origem | Na ZAIOS | Configurável? | Para o Bruno decidir |
|---|---|---|---|---|---|---|
| 1 | Fator 0,82 (receita líquida sobre bruta) | 0,82 | F02 | **Não existe como número fixo.** É a soma de dois botões: deduções 17% e quebra 1% | Sim, os dois componentes | Aprovar 17% e 1% separadamente, ou trocar |
| 2 | Deduções sobre a receita (impostos, comissões de canal, taxas de cartão) | 17% | F02 | Botão de referência `REF_DEDUCOES` em P6 Receitas | Sim | Confirmar a faixa por regime tributário e canal |
| 3 | Quebra (inadimplência, cancelamento, estorno) | 1% | F02 | Botão `REF_QUEBRA` em P6 Receitas | Sim | Confirmar |
| 4 | Reserva de manutenção, abaixo do EBITDA | 3% da receita | F02 | Botão `REF_RESERVA` em P6 Receitas | Sim | Confirmar 3% ou outro valor |
| 5 | Retirada do dono | horas × R$ 40 × 4,33 | F02 | Membro informa horas e valor; o texto sugere R$ 40 | Sim (o valor-hora) | Confirmar R$ 40 por hora |
| 6 | Rampa do primeiro ano | 40%, 50%, 75% da ocupação-alvo | F02 | Texto de ajuda em P6 Receitas | Sim | Confirmar a curva |
| 7 | Taxa de desconto | 10% (ilustrativa) | F03 | **Não é usada.** O membro informa a taxa; não há valor-padrão | Já é do membro | Decidir se a Zion sugere uma taxa ou só explica como escolher |
| 8 | Múltiplo de saída | 6 vezes o resultado do ano 10 | F03 | Botão `REF_MULTIPLO_SAIDA = 6` em P6 Viabilidade | Sim | Aprovar 6, trocar, ou tirar o botão |
| 9 | Regra de decisão: payback | até 8 anos passa; até 12 ajustar; acima redesenhar | F03 | `passoPayback` em `src/calc/viabilidade.ts` | Sim | Aprovar os limites |
| 10 | Regra de decisão: colchão | menor saldo, com a contingência toda usada, de pelo menos 10% do CAPEX | F03 | `COLCHAO_MINIMO = 0.1` | Sim | Aprovar |
| 11 | Regra de decisão: cenário conservador | déficit de até 3 meses de custo fixo com retirada é "ajustar"; maior é "redesenhar" | F03 | `passoConservador` | Sim | Aprovar |
| 12 | Cenários | conservador: diária −10%, ocupação −20%; otimista: diária +10%, ocupação +15% | F03 | `CENARIOS` | Sim | Aprovar |
| 13 | Estresse | CAPEX +25%; receita −30%; abertura 6 meses depois (mostrado, fora dos 5 passos) | F01/F03 | `ESTRESSE_CAPEX`, `QUEDA_RECEITA`, `ATRASO_ABERTURA` | Sim | Aprovar |
| 14 | Faixas de CAPEX | OS&E 12% (10–15%); pré-abertura 5% (5–10%); contingência 20–25% (obra nova) ou 10–15% (reforma) | F01 | Botões e faixas em P5 CAPEX | Sim | Aprovar |
| 15 | Capital de giro | 6 vezes o custo fixo mensal, ou a soma dos meses negativos (regra B) | F01/F02 | P5 e P6 Receitas | Sim | Aprovar; a regra B é elaboração da ZAIOS |
| 16 | Régua de margem | 30% boa, 20% atenção, 10% risco | F02 | P6 Receitas | Sim | Aprovar |
| 17 | Faixas do Zion Score | — | Material da Academy | **Não usado na ZAIOS.** A ZAIOS usa semáforo (P1), Índice de Maturidade (G1) e Nota do Raio-X (V1) | — | Decidir se o Zion Score entra na ZAIOS ou fica só no material |
| 18 | Horizonte | fluxo de 10 anos; curva de caixa de 36 meses | F03 | `ANOS_FLUXO`, `MESES_CURVA` | Não (estrutura do método) | Só confirmar |

### 1.2 Fórmulas usadas

Valores em centavos inteiros no código; percentuais como frações. Fórmulas completas em `src/calc/FORMULAS.md` do projeto Lovable.

**Cascata de receitas (F02, P6 Receitas)**
```
noites vendidas      = unidades × dias do mês × ocupação
receita bruta        = noites vendidas × diária média          (taxa de limpeza fora: decisão pendente)
receita líquida      = receita bruta × (1 − deduções − quebra)  → com 17% e 1%, fator 0,82
resultado operacional= receita líquida − custos variáveis − custos fixos − retirada do dono
retirada do dono     = horas por semana × valor-hora × 4,33
EBITDA − reserva     = resultado operacional − receita bruta × 3%
ponto de equilíbrio  = custos fixos ÷ (diária × fator − custo variável por noite)
```

**Viabilidade (F03, P6 Viabilidade)**
```
fluxo do ano t       = geração de caixa do ano t (rampa no ano 1)
VPL                  = −CAPEX + Σ fluxo_t ÷ (1 + taxa)^t        (fluxo no fim do ano)
valor de saída       = resultado do ano 10 × múltiplo, somado ao ano 10
TIR                  = taxa que zera o VPL (bisseção)
payback              = ano em que o caixa acumulado vira positivo (com fração)
payback descontado   = o mesmo com fluxos descontados
```

**Regra de decisão Zion em 5 passos** (conferida em `src/calc/viabilidade.ts`)
1. Geração de caixa do ano em regime, cenário base: ≥ 0 passa; negativa, redesenhar.
2. Cenário conservador: geração ≥ 0 passa; déficit de até 3 meses de custo fixo com retirada, ajustar; maior, redesenhar.
3. Payback simples do base: até 8 anos passa; até 12, ajustar; acima de 12 ou "não se paga", redesenhar.
4. VPL do base: sem saída ≥ 0 passa; negativo sem saída e positivo com saída, ajustar ("o projeto depende da venda do ativo"); negativo nos dois, redesenhar.
5. Colchão com a contingência toda usada: ≥ 10% do CAPEX passa; entre 0 e 10%, ajustar; negativo, redesenhar.

Leitura: algum redesenhar dá Redesenhar; senão, algum ajustar dá Ajustar; todos passam dá Avançar. O estresse (CAPEX +25%, receita −30%, 6 meses de atraso) é mostrado ao membro, mas não entra nos 5 passos.

### 1.3 Resultados esperados (casos de referência, dados fictícios)

Conferidos em Python, independente do código da ZAIOS, e usados como testes no projeto.

| Caso | Resultado esperado |
|---|---|
| F01 · CAPEX | Necessidade total R$ 1.237.400,00 |
| F02 · Caso P6 | Ponto de equilíbrio 223,25 noites por ano (20,4% de ocupação); resultado operacional R$ 108.846,84 |
| F03 · Caso 1 | VPL −R$ 1.110.447,78; payback 38,6 anos; TIR com saída −8,4% → **Redesenhar** |
| F03 · Caso 2 | Payback 5,75 anos; payback descontado 8,82 anos; VPL sem saída R$ 92.549,78; com saída R$ 624.599,52 → passa |
| Teste fechado (controle) | 3 unidades, diária R$ 680, ocupação 38% → R$ 282.948,00 por ano |

### 1.4 Sensibilidade das premissas

**Deduções (fator)** · caso F02
| Deduções | Fator | Resultado operacional | Ponto de equilíbrio |
|---|---|---|---|
| 12% | 0,87 | R$ 122.994,24 | 210,6 noites |
| **17%** | **0,82** | **R$ 108.846,84** | **223,2 noites** |
| 22% | 0,77 | R$ 94.699,44 | 237,6 noites |

Cada 5 pontos de dedução mudam o resultado em cerca de R$ 14 mil por ano (13%). Deduções reais variam muito com o regime tributário (Simples, lucro presumido) e com o canal de venda (comissão de OTA de 13% a 18% contra venda direta). Por isso um número único é arriscado.

**Quebra** · resultado operacional: 0% → R$ 108.846,84; 1% → R$ 106.017,36; 2% → R$ 103.187,88.

**Reserva** · 3% → R$ 8.488,44 por ano; 5% → R$ 14.147,40.

**Taxa de desconto** · F03 Caso 2, VPL sem saída
| Taxa | VPL | Passo 4 |
|---|---|---|
| 8% | R$ 203.127,39 | passa |
| **10%** | **R$ 92.549,78** | passa |
| 12% | −R$ 3.883,97 | **vira "ajustar"** (positivo só com a saída) |

**Achado principal:** com 12% o mesmo projeto muda de decisão. A taxa é a premissa mais sensível. Hoje a ZAIOS não sugere taxa (o membro informa), o que é correto, mas o material F03 usa 10% como ilustração. Recomendo que o texto explique como escolher a taxa (custo do dinheiro do membro mais prêmio de risco) e mostre o resultado em mais de uma taxa.

**Múltiplo de saída** · F03 Caso 2, VPL com saída a 10%: 4× → R$ 447.249,61; **6× → R$ 624.599,52**; 8× → R$ 801.949,44. Neste caso não muda a decisão, porque o VPL sem saída já é positivo. Mas quando o VPL sem saída é negativo, o valor de saída decide entre "ajustar" e "redesenhar" no passo 4: aí o múltiplo pesa na decisão. Recomendo apresentar a saída sempre ao lado do resultado sem saída, como já é feito.

### 1.5 Os parâmetros devem ser configuráveis?

Sim, os de referência. Hoje são constantes no código: mudar qualquer valor exige um pedido ao Lovable e uma nova publicação.

Proposta, para **depois** do teste fechado e da validação destas premissas (estimativa de 5 a 8 créditos, não autorizada):
- Uma tabela "Parâmetros Zion" editável só pelo admin, com histórico de versões.
- Cada resultado guarda a versão dos parâmetros usada, para que um Dossiê antigo continue reproduzível.
- Ficam fixos no código só os itens estruturais (10 anos, 36 meses, a forma das fórmulas).
- Os botões de referência continuam marcados como "Referência Zion" e o membro pode trocar qualquer valor.

---

## Parte 2 · Verificação dos 11 recursos e 5 vídeos

Rodado em 08/11/2026 sobre as cópias publicadas, sem alterar nada.

### 2.1 Ferramentas

| Recurso | Como foi verificado | Resultado |
|---|---|---|
| Diária Mínima (planilha 01) | Recálculo no LibreOffice comparado a uma regra independente em Python | 21 de 21 ok |
| Kit de Mensagens 11 | Idem, mais checagem de erro em todas as células | 26 de 26 ok |
| Controle de Enxoval 13 | Idem | 18 de 18 ok |
| Checklist de Limpeza 17 | Idem, com 7 cenários aleatórios | 31 de 31 ok |
| Quadro de Ocorrências 14 (extra, não está entre os 11) | Idem | 13 de 13 ok |
| A01 | Navegador real, 3 perfis, desktop e celular, validação, recarga, PDF | 78 de 78 ok |
| A02 Precificador | Idem | 43 de 43 ok |
| A03 Calculadora de Custos e Rentabilidade | Idem | 79 de 79 ok |
| A06 Auditor da Experiência | Idem | 47 de 47 ok |
| A07 Assistente de Conversão de Reservas | Idem | 48 de 48 ok |
| G2, G3 e P2 (ZAIOS) | Testes automáticos do projeto (396 passando) | **Falta o teste humano** (itens do teste fechado) |

Os testes automáticos conferem cálculo e funcionamento. Eles não substituem uma leitura de conteúdo: textos, exemplos e linguagem de cada ferramenta ainda precisam da revisão da Zion antes de entrar num módulo.

### 2.2 Vídeos tutoriais

| Vídeo | Duração | Formato | Áudio |
|---|---|---|---|
| zar-a01 | 2 min 10 s | 1280 × 720 | presente, nível normal |
| zar-a02 | 2 min 14 s | 1280 × 720 | presente, nível normal |
| zar-a03 | 2 min 12 s | 1280 × 720 | presente, nível normal |
| zar-a06 | 2 min 14 s | 1280 × 720 | presente, nível normal |
| zar-a07 | 2 min 13 s | 1280 × 720 | presente, nível normal |

Os arquivos abrem, têm imagem e áudio, e o áudio está num nível uniforme. **Ponto de atenção:** as telas mostram o cabeçalho "Zion Collection Club". Se esse nome não for mais o usado no ecossistema, os vídeos precisam de nova gravação ou de um aviso antes de entrar nos módulos. Ninguém assistiu aos vídeos inteiros com atenção ao conteúdo: isso fica para a revisão humana.

---

## Parte 3 · O G2 atende o controle por imóvel?

Planilha por imóvel: **suspensa**, como pedido.

| Necessidade | O G2 atende? | Como está hoje |
|---|---|---|
| Controle por imóvel | **Em parte** | Cada lançamento pertence a um empreendimento. Se cada imóvel for cadastrado como um empreendimento, o controle funciona. Dentro de um empreendimento não há separação por unidade |
| Consolidação de unidades | **Não** | Não há visão que some vários empreendimentos do mesmo membro |
| Despesas compartilhadas | **Não** | Não há rateio. Uma despesa comum (contador, internet, lavanderia) precisa ser dividida à mão |
| Comparação de resultados | **Não** | Não há tela que compare imóveis lado a lado. Cada Dossiê mostra um empreendimento |
| Exportação | **Em parte** | Só "Baixar meus dados" (JSON), a exportação do admin e as tabelas no PDF do Dossiê. Não há CSV nem XLSX |

**Conclusão:** o G2 atende quem tem um imóvel ou trata cada imóvel separado. Não atende quem opera várias unidades e quer ver o conjunto.

**Recomendação:** se o teste fechado confirmar que membros com várias unidades precisam disso, ampliar o G2 em vez de criar uma planilha nova:
1. Campo opcional "unidade" no lançamento.
2. Regra de rateio de despesas comuns (por unidade, por noites vendidas ou por receita).
3. Visão consolidada e comparação lado a lado.
4. Exportação em CSV.

Estimativa: 6 a 10 créditos. **Não autorizado e não iniciado.** Antes, o Bruno decide se essa necessidade é real para o público da Academy.

---

## Parte 4 · Bíblia Operacional Zion

- Autorizada só como referência interna para os POPs e os módulos O03 e O02.
- Antes de qualquer uso: revisar, anonimizar (sem nomes de hóspedes, colaboradores, fornecedores, endereços ou números internos) e conferir se cada prática ainda vale hoje.
- Nada da Bíblia é publicado como está. Procedimento antigo não é tratado como adequado sem a validação da Zion.

---

## O que espera decisão

1. Resultado do teste fechado de 15 itens (Bruno e 2 ou 3 membros).
2. Aprovação, ajuste ou troca de cada premissa da tabela 1.1.
3. Se o Zion Score entra na ZAIOS ou fica só no material.
4. Se o nome "Zion Collection Club" nos vídeos ainda vale.
5. Se a ampliação do G2 é necessária.
6. Pendências anteriores: taxa de limpeza na receita, e-mail de contato nos Termos, revisão jurídica, texto e remetente do e-mail de acesso.

Nada será produzido (e-books, aulas, POPs) e nenhuma plataforma será alterada até essas respostas.
