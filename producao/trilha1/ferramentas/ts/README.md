# Zion Exercícios · Trilha 1 · calculadoras em TypeScript

As contas das 12 páginas de exercício (`../aula-01.json` a `../aula-12.json`) em módulos TypeScript determinísticos, sem dependência, para colar no app Lovable (React + TypeScript). Nada foi publicado; Lovable e ClickMax não foram tocados.

## Arquivos

| Arquivo | O que é |
|---|---|
| `types.ts` | `Resposta`, `Respostas`, `Calculo`, `Veredito`, `ResultadoCalculos` |
| `util.ts` | leitura das respostas, contas seguras (sem NaN, sem divisão por zero), formatação pt-BR, datas |
| `t1-a01.ts` a `t1-a12.ts` | `export function calcular(r: Respostas): ResultadoCalculos`, uma por aula |
| `index.ts` | `export const calculadoras: Record<string, (r: Respostas) => ResultadoCalculos>`, chaves `"1-1"` a `"1-12"` |
| `tests/` | um teste por aula (Marina + caso cheio de "Não sei"), rodado com `node:test` |

## Como usar no Lovable

1. Copie a pasta `ts/` (menos `tests/` e este README) para `src/lib/exercicios/`.
2. Na página do exercício, chame a calculadora pelo slug do link curto, com as respostas do formulário:

```tsx
import { calculadoras, type Respostas, type ResultadoCalculos } from "@/lib/exercicios";
import aula from "@/data/aula-08.json"; // o JSON da aula (campos, prompt_ia, rodape)

function Resultado({ respostas }: { respostas: Respostas }) {
  const res: ResultadoCalculos = calculadoras[aula.slug](respostas);
  return (
    <section>
      {res.calculos.map((c) => (
        <div key={c.id} data-alerta={c.alerta ?? "neutro"}>
          <h4>{c.rotulo}</h4>
          <p>{c.texto}</p>
        </div>
      ))}
      <p>Veredito sugerido: {res.veredito_sugerido}. {res.motivo_veredito}</p>
      <small>{aula.rodape}</small>
    </section>
  );
}
```

3. Para a leitura da IA, mande o `prompt_ia` do JSON como prompt de sistema e, como mensagem do usuário, o JSON abaixo. O prompt diz que a IA recebe `{"respostas", "calculos"}` e pode ser mais cautelosa que o `veredito_sugerido`, nunca mais otimista.

```ts
const res = calculadoras[aula.slug](respostas);
const mensagem = JSON.stringify({
  respostas,
  calculos: {
    ...Object.fromEntries(res.calculos.map((c) => [c.id, { valor: c.valor, texto: c.texto, alerta: c.alerta, detalhes: c.detalhes }])),
    veredito_sugerido: res.veredito_sugerido,
    motivo_veredito: res.motivo_veredito,
  },
});
// system: aula.prompt_ia ; user: mensagem ; a resposta é só JSON (resumo, pontos_fortes, ponto_fragil, veredito, ...)
```

Na Aula 12, as respostas `veredito_p1` a `veredito_p10` podem vir pré-preenchidas com o `veredito` que a IA devolveu em cada aula (ou o `veredito_sugerido`, se a IA não rodou).

## Convenções das respostas

- **Percentual em pontos.** Campo `percentual` chega como o aluno digita: `78` quer dizer 78%. Nunca `0,78`.
- **Número** pode vir como `number` ou texto pt-BR (`"1.234,56"`, `"1.500"`, `"3,5"`). `R$`, `%` e espaços são ignorados.
- **Vazio vale "Não sei".** `null`, `""`, `[]`, campo ausente e `"nao_sei"` são tratados igual, conforme o `se_nao_sei` de cada cálculo.
- **Datas** (Aula 11): `"2027-06-01"` ou `"01/06/2027"`. Data impossível (31/02) conta como vazia. Contas em UTC, sem fuso.
- **Múltipla**: lista de `valor` das opções; valores fora da lista do JSON são ignorados.

## Convenções do resultado

- `calculos` tem um item por cálculo do JSON, **na ordem e com o mesmo `id`**; o último é `veredito_sugerido` (a Aula 1 não tem, como no JSON, e devolve `nao_se_aplica`).
- `valor`: o número principal. Percentuais saem em pontos (`38.5` = 38,5%); dinheiro em reais com 2 casas; `null` quando falta dado. Textos de escolha saem como texto (`"não volta"`, `"em branco"`, `"estimador, saindo"`).
- `detalhes` (extensão opcional ao tipo pedido): os outros números da conta, como piso e teto, mês a mês, datas. Arredondados a 4 casas, percentuais também em pontos.
- `alerta`: `ok`, `atencao` ou `critico`, só onde a fonte dá régua; sem régua, fica sem alerta.
- `texto`: português do Brasil, moeda `R$ 1.234,56` (negativo `-R$ 60.943,02`), percentual com vírgula, sem travessão. Um filtro final troca qualquer travessão que escape e qualquer NaN/Infinity por `null`.

## Regras gerais que a página aplica

- **R1 · Vazio = Não sei** (acima).
- **R2 · Dado que falta nunca vira "avançar".** As `regras_veredito` são checadas na ordem do JSON. Se uma condição não pode ser checada porque falta dado (e nenhuma regra anterior disparou), o veredito sugerido é `testar`, com o motivo dizendo o que falta. É a leitura de "testar" das próprias regras ("a medida ainda depende de dado que falta"). Uma regra que dispara com dado conhecido continua valendo (por exemplo, `ajustar` por contingência fora da faixa mesmo com outra linha em branco).
- **R3 · Ordem de restrição** para juntar vereditos (Aula 12): pausar > testar > ajustar > avançar; página não feita = testar.

## Divergências entre a fórmula do JSON e a auditoria

| # | Aula | O que diverge | Qual está certo | O que o código faz |
|---|---|---|---|---|
| D1 | 2 | Marina (caminho "investigar", peso de 27%): a fórmula dá **ajustar**, porque checa `peso > 20%` antes de `investigar`. A auditoria e o próprio `regras_veredito.testar` ("é o veredito da Marina") dizem **testa**. | A auditoria: o método manda medir o mercado antes de renegociar, e a ordem pausar > testar > ajustar da Aula 12 põe testar antes. **Decisão do Bruno:** inverter as linhas de ajustar e testar na fórmula. | Segue a fórmula (ajustar). A IA pode descer para testar, que é mais cauteloso. |
| D2 | 3 | Absorção: o JSON escreve `sobra = noites_hoje + mais - menos`. Com a Marina isso dá 13.997 noites e cabem 99 cabanas. A auditoria (Passo 8) faz `sobra = mais - menos` = 499 noites, cabem 3. | A auditoria: as noites de hoje já são vendidas pelos comparáveis. | **Corrigido** para `mais - menos`. É o único ponto em que o código não copia o JSON. |
| D3 | 3 | A auditoria usa 38% na absorção (499 noites, 3,6 cabanas); a fórmula usa a ocupação do ano, 38,5% (506,5 noites, 3,6 cabanas). | As duas; 38,5% é o número do ano conferido no Passo 6. | Usa 38,5%. Cabem as mesmas 3. Um teste extra com 38% reproduz os 499. |
| D4 | 3 | Veredito da Marina: a Aula 3 diz "seguir com condições" (que o JSON mapeia para avançar); a regra do JSON dá **ajustar** (cabem 3 < 5) e a auditoria da Aula 12 registra "Ajusta (abre com 3)". | A Aula 12 e a regra (o molde "desenha para 5, abre com 3" está em `ajustar`). | Ajustar. |
| D5 | 8 | A auditoria arredonda a reserva para R$ 1.100 por mês (4,9%). Com `reserva_pct = 5`, a fórmula dá R$ 1.117,46, depois da reserva R$ 13.811,07 e margem de 5,15% (a auditoria: R$ 14.020,62 e 5,23%). | As duas contas estão certas; a diferença é o arredondamento da auditoria. Veredito igual (testa). | Segue a fórmula. O teste usa o percentual exato que dá R$ 1.100 (13.200 ÷ 268.191) e confere os 16 itens da auditoria; outro teste confere os 5% cheios. |
| D6 | 10 | Custo da captação: a auditoria calcula 2% a 5% sobre a necessidade (R$ 22.410,14 a R$ 56.025,35 no piso). A fórmula faz `externo ÷ (1 - taxa)`: R$ 1.143.374,51 a R$ 1.179.481,07, custo de R$ 22.867,49 a R$ 58.974,05. | A fórmula, que é o que o README do pacote pede ("percentual do que se capta"). A auditoria marca a conta como "só na auditoria". | Segue a fórmula. |
| D7 | 11 | A data das vendas na auditoria sai da data de abertura (1º de junho); a fórmula sai do início da alta. | Iguais na Marina (a alta começa no dia da abertura). Fica a decisão pendente 17 do README do pacote. | Segue a fórmula (início da alta). |

Tudo o mais bate com as contas conferidas: Aula 2 (15.000 m², 30%, R$ 12 / R$ 40 / R$ 120 mil, 2,4 vezes, 27,0%), Aula 3 (R$ 1.846, 40,9%, R$ 645,45, R$ 263,71, 38,5%, 66%, R$ 90.703, R$ 4.260), Aula 4 (11% acima), Aula 6 (20,8%, 13,6%, 15,2%), Aula 7 (192 m², 40,6%, CAPEX de R$ 963.240 a R$ 1.531.800, proporções, R$ 321.080 a R$ 510.600, R$ 33.333, R$ 120.750, R$ 270.000), Aula 8 (415,8 noites até a diária de R$ 687,75 e a taxa de 6,26%), Aula 9 (ano 1 de -R$ 60.943,02, giro de R$ 124.500, menor saldo de R$ 63.556,98, 4,9 meses, colchão de 6,6% e 4,1%, payback de 74,05 e 114,60 anos, conservador de -R$ 37.576,83, otimista de R$ 64.814,12, R$ 798,07, 35,33%, rampa no piso -R$ 79.932,33), Aula 10 (reforço de R$ 32.767,02 e R$ 89.623,02, Régua de R$ 1.120.507,02 e R$ 1.745.923,02, 65,13% e 74,42%), Aula 11 (03/03, 02/01, 02/03, 16/02, 13/04, 04/05, 1.500 / 1.000 / 3.000, R$ 32.987,49 / R$ 65.974,99 / R$ 131.949,97) e Aula 12 (avança 4, ajusta 1, testa 5; ritmo nas páginas 1, 7, 8, 9 e 10).

Aulas 1 e 5 não têm conta na auditoria: o teste usa as respostas que o e-book descreve (Aula 12, "A ficha de entrada da Marina, refeita hoje"; Aula 5, o veredito "avança") e confere o veredito. Aula 6 e Aula 4 usam as frases, provas e escolhas do e-book.

## Fórmulas ambíguas e a escolha feita

**Aula 1**
- `linha_ficha` com "Não sei" escreve "não sei" no lugar da letra (ex.: `não sei, 5 de 5, A, etapa 4`).
- Ocupação abaixo da faixa: a fonte não tem leitura; o texto só diz "abaixo da faixa". `alerta_extra` (65% ou mais sem procura extraordinária) vale `critico`; `alerta_alto`, `atencao`.

**Aula 2**
- Subtração em Não sei entra como zero (JSON); a área sai "no máximo, provisória". Se as subtrações passarem da matrícula, a área aparece com alerta e os preços que dependem dela ficam em branco.
- Empate no menor limite: o texto nomeia todos os que empatam.
- `conta_nao_sei` conta os 12 campos que aceitam Não sei (tudo menos a área da matrícula e a lista de documentos), com vazio contando como Não sei.
- Peso: até 10% ok; acima de 10% até 20% sensível; acima de 20% alerta.

**Aula 3**
- Amplitude exatamente 3: a régua é "acima de 3", então 3,0 cai em "entre 2 e 3, só o número". A Marina tem 1.150 ÷ 380 = 3,03; o teste usa 3,03.
- Faixa da ocupação do ano abaixo de 35% e acima de 85%: o texto diz que está fora da régua e mostra a faixa mais próxima.
- Mês com zero meses (ex.: nenhum mês fraco) não exige a ocupação daquele período.
- Pausar pela absorção só quando a série e os alvarás são conhecidos. Com crescimento ou unidades em obra em Não sei (entram como zero, como manda o JSON), a sobra sai incompleta e o veredito fica em testar. Sem essa trava, "Não sei" no crescimento levaria sempre a pausar.
- `cabem_agora` nunca sai negativo (mínimo 0).

**Aula 4**
- Lista negra: compara sem acento e sem maiúscula, com palavra inteira, nas formas único/única/únicos/únicas, incrível/incríveis, exclusivo(a)(s), inesquecível/inesquecíveis, encantador/encantadora(s)/encantadores, premium(s).
- Teste do vizinho ou dos cinco segundos em branco conta como "não fiz". Provas em branco contam como 0 provas.
- Mix acima de 4: `arredondar(unidades × 2/3)` com arredondamento comum (6 → 4 e 2; 5 → 3 e 2).

**Aula 5**
- As horas em horário de hóspede não têm mínimo na fonte (pendente 8): a página usa só a escolha "as horas cobrem ou não".
- Pela R2, Não sei em valorização, receita formal, unidades da fase um (quem opera sozinho) ou "quer operar" (quem opera sozinho) dá testar.

**Aula 6**
- Base da régua de apoio = área fechada (unidades × área fechada + apoio), escolha do pacote (pendente 9).
- Consulta prévia "não feita" ou "protocolada" não trava o avançar; Não sei trava (R2).

**Aula 7**
- Deck e apoio em Não sei entram como zero e a área sai "provisória, obra subestimada" (o JSON não diz; a alternativa seria deixar todo o CAPEX em branco).
- Infraestrutura e projetos em Não sei entram como zero e o CAPEX sai "parcial" (JSON).
- `pct_ffe_piso` é a proporção do FF&E no CAPEX piso, como na fórmula.
- Corte da experiência em Não sei: testar (R2), antes de checar a contingência.
- Dois ou mais fatores de risco com contingência abaixo de 15%: só aviso, não muda o veredito.

**Aula 8**
- Contribuição por noite zero ou negativa: não existe equilíbrio; conta como folga negativa, e com margem negativa a página pausa.
- `diaria_criterio` usa o fixo com a reserva calculada sobre a receita de hoje, como a fórmula e a auditoria.
- Reserva fora de 3% a 5%: aviso no texto, sem mudar o veredito.

**Aula 9**
- Mês marcado como alta e vale ao mesmo tempo conta como alta, com aviso.
- O menor saldo da curva inclui o dia da abertura (saldo 0 = giro) e os 24 meses; o mês 13 em diante segue o regime do calendário.
- No veredito, colchão e payback são lidos pelo lado mais exigente (o menor colchão e o maior payback, entre piso e teto), para nunca sair mais otimista. Na Marina os dois lados já disparam.
- Fôlego entre 2 e 4 meses ou acima de 6: a fonte não dá leitura; fica sem alerta.
- "Levemente" e "muito" negativo: sem número na fonte; o texto mostra a razão conservador ÷ base (pendente 12).
- Diária "só mercado", "Não sei" ou em branco contam como não testada.

**Aula 10**
- O score só sai com as cinco notas entre 0 e 100; nota fora disso conta como em branco.
- Capital próprio maior que a necessidade: nada a captar (externo 0), sem custo de captação.
- Capital próprio em Não sei: a necessidade sai "antes do capital próprio" e a participação fica em branco (JSON). No teste da Marina, o capital próprio é 0, que é a hipótese da auditoria (item 6: o aporte cobre os usos antes do custo); na ficha da Aula 12 ele está em branco.
- Pergunta do capital ou conservador em Não sei: testar (R2).

**Aula 11**
- Semanas das vendas: contadas no Calendário dos Noventa Dias, com a semana 1 começando no limite da obra (abertura menos 91 dias), como na auditoria (semana 7 em 13/04, semana 10 em 04/05). Lida ao pé da letra ("7 a 9 semanas antes da abertura"), a venda ao público viria antes da lista.
- Antecedência em Não sei: janela de 150 a 90 dias antes da alta; a comparação com a obra usa o fim da janela.
- Abertura de 1 a 27 dias antes da alta: entre as duas leituras da fonte, sem alerta.
- Veredito anterior em branco conta como "não fiz" (testar). Condição de abertura em Não sei conta como vazia (ajustar, pela fórmula).

**Aula 12**
- A página 0 não tem veredito: entra só em "páginas completas" e a Etapa 1 usa as páginas 1 e 2.
- A fórmula diz `veredito_sugerido = veredito_projeto`; a regra de avançar pede também todas as páginas completas. O código segue a fórmula e, quando tudo avança com página incompleta, o motivo avisa.

## Testes

Pré-requisito: Node 18 ou mais novo. As dependências de teste (`tsx`, `typescript`, `@types/node`) não ficam nesta pasta; foram instaladas no scratchpad.

```bash
# numa pasta qualquer:  npm i tsx@4.19.2 typescript@5.6.3 @types/node@22.10.2
cd exercicios/ts
<pasta>/node_modules/.bin/tsx --test tests/*.test.ts
<pasta>/node_modules/.bin/tsc --noEmit --strict --target es2022 --lib es2022 --module esnext --moduleResolution bundler --types node --skipLibCheck *.ts tests/*.ts
```

Resultado em 25/10/2026: 32 testes, 32 passando; `tsc --strict` sem erro. Cada teste também confere que os `id` saem na ordem do JSON, que não há NaN, Infinity nem travessão, e que todo cálculo tem texto. Os casos de Não sei incluem formulário vazio (`{}`) e zeros em todos os divisores.
