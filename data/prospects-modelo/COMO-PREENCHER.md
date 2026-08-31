# Como sair de zero contatos em uma tarde

Preencha `modelo-contatos.csv` e rode:

```bash
zion-ai prospects importar -f modelo-contatos.csv --fonte "cadastur-urubici"
zion-ai prospects listar --score-minimo 75
```

O Lead Score pontua cada linha e devolve a fila. Quem tiver 75+ é classe A.

## Colunas

`nome` é a única obrigatória. Todas as outras melhoram o score:

| Coluna | Peso no score | Onde achar |
|---|---|---|
| `municipio` + `uf` | até 30 pts (localização + potencial financeiro, herdados do destino) | óbvio |
| `area_ha` **ou** `unidades` | até 30 pts (qualidade do ativo + expansão) | site, anúncio, CADASTUR |
| `email`/`telefone`/`instagram`/`site` | até 10 pts | site oficial, rodapé |
| `notas` | 10 pts — **só pontua se preenchida** | sua observação sobre a dor |

`notas` é o campo que mais gente deixa vazio e é o que mais move a agulha.
Escreva a dor que você percebeu: "site sem tarifário", "anúncio parado há um ano",
"só tem 4 chalés iguais aos do vizinho". Isso é o que separa lead de nome.

## As três praças e onde procurar

**Urubici / SC** — 79 pts · serra, glamping 15/15
**Cambará do Sul / RS** — 76 pts · cânions, oferta muito abaixo da demanda
**Canela / RS** — 83 pts · maior score do Sul

Em cada uma, nesta ordem:

1. **CADASTUR** (cadastur.turismo.gov.br) — filtre por município e tipo
   "Meio de Hospedagem". Traz razão social, CNPJ e endereço. É cadastro público
   federal. Rende 20–40 por município.
2. **ABIH/SC e ABIH/RS** — página de associados.
3. **Secretaria municipal de turismo** — quase toda tem uma lista de meios
   de hospedagem no site.
4. **Site de cada pousada** — pegue o e-mail comercial do rodapé. É aqui que
   sai o contato de verdade, e é legítimo: a empresa publicou como canal.
5. **Imobiliárias com CRECI** da praça — para terreno, o corretor é o caminho,
   não a matrícula.

**Não use** Airbnb, Booking ou TripAdvisor como fonte de contato. Servem para
ler a oferta do destino — quantos chalés, que faixa de preço, onde está o gap.

## Meta

150 registros nas três praças. Uns 50 saem em A ou A+. Aí a campanha roda.
