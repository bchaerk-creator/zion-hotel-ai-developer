# Jornada 2 · Gestão · Módulo 3 · Preço, reservas e distribuição · Plano da lição (G03)

Status: plano de produção (10/11/2026). Entregável: **Tabela de Preço e Canais** (página 3 do Plano de Gestão): piso de tarifa por escrito, calendário de 12 meses (temporadas e diárias), mix de canais com o custo de cada canal e meta de venda direta. Não altera os módulos 0 e 2 nem ferramentas existentes; aponta, sem alterar, para o Precificador Inteligente (A02) e para a Ferramenta 01 · Diária Mínima, produtos vendidos à parte: os links vão para as páginas de vendas (`https://infoprodutos-zion.clickmax.space/zar-a02` e `https://infoprodutos-zion.clickmax.space/diaria-minima`), decisão de 10/11/2026.

## 1. A lição em uma frase
Aprenda o passo a passo para declarar o piso da sua diária por escrito, montar o calendário de doze meses com cinco faixas e as datas de pico, e saber quanto cada canal deixa por noite, com uma meta de venda direta.

## 2. Públicos e jornadas
- Desenvolvedor (vai abrir): usa o custo previsto e os preços dos concorrentes; a Tabela vira o preço de entrada e o piso declarado antes da primeira reserva (Panorama, Lançamento, passo "Defina o preço de entrada e o piso"). A ficha avisa.
- Gestor (dono que opera): público central; usa o custo da Folha Única do Mês (Módulo 2) e o mix real dos últimos três meses.
- Operador: monta a Tabela para propor ao dono.
Jornada A (quero começar) e B (já opero) tratadas na abertura, como nos módulos 0 e 2.

## 3. Fontes Zion e convenções
- **Panorama, Trilha B, G2 Distribuição e Canais**: "Estar em todos os canais não é distribuição. É dependência dividida."; mix atual dos últimos três meses; líquido por canal (comissão, taxa de cartão, custo de adquirir o hóspede); meta de venda direta "um número, não uma intenção. E o prazo"; básico técnico (motor de reservas e gestor de canais; sem isso, trabalho manual e reserva duplicada). Entregável da fonte: Mapa de Canais.
- **Panorama, Trilha B, G3 Preço e Receita**: "Calendário vazio quase nunca se resolve com desconto."; custo por diária vendida; "Declare o piso por escrito ... combinado com todo mundo que atende. Inclusive para véspera"; calendário de doze meses com diária-alvo por período; "Troque desconto por condição". Entregável da fonte: Tabela de Pricing com piso declarado e calendário de doze meses. Estudo de caso ilustrativo "O mês cheio que fechou no vermelho".
- **Jornada do COMO · Etapa 08 "Como eu cobro certo?"** (remissão): Diária de Referência Zion™ (6 a 9 concorrentes, descartar o mais caro e o mais barato, terço de baixo cerca de 15% abaixo, meio, terço de cima cerca de 20% acima; conferir com o custo da Etapa 09); As Cinco Faixas Zion™ (fatores de partida: vale 0,70 a 0,80; baixa 0,85 a 0,95; base 1,00; alta 1,35 a 1,60; pico 1,90 a 2,60); Mapa de Datas de Pico™ (preço próprio, mínimo de noites, abertura, cancelamento); Calendário de Preços Zion™ (meio de semana e fim de semana; 12 meses abertos); Política de Desconto™ (quatro situações, nunca abaixo do piso, nunca no pico; "o piso não é o custo: é o custo mais a margem mínima"); revisão trimestral.
- **Etapa 09**: Custo por Diária Vendida™ (Passo 08) e a regra do desconto em três faixas; Mapa de Margem por canal (Passo 10).
- Vocabulário para o membro: "custo por noite vendida" (= Custo por Diária Vendida™), "diária de referência", "piso", "plataforma" e "venda direta" (em vez de OTA), "gestor de canais" (em vez de channel manager), "motor de reservas". Sem siglas na tela.
- Mapa de fontes completo fora do repositório (`scratchpad/fontes/MAPA_FONTES_preco.md`).

## 4. Objetivos (verbos observáveis)
1. Explicar por que o preço começa pelo custo e por que preço fixo o ano inteiro erra nas duas direções (compreender).
2. Calcular o líquido por noite de cada canal e a comissão média do mix (aplicar).
3. Calcular a diária de referência a partir de seis a nove concorrentes (aplicar).
4. Calcular o custo da noite no canal mais caro e declarar o piso por escrito, com quem o conhece e três condições no lugar de desconto (aplicar, criar).
5. Montar o calendário de doze meses com cinco faixas e as datas de pico (criar).
6. Avaliar a Tabela pelas regras da fonte, identificar a causa principal e definir uma meta de venda direta com prazo (avaliar, criar).

## 5. As seis etapas
| Etapa | Peça | Duração |
|---|---|---|
| Diagnosticar | Abertura da ficha: situação e 4 perguntas (preço com faixas? piso escrito? líquido por canal? meta de venda direta?) → nível 1 a 4 | 1 min |
| Compreender | Aula em vídeo (12 cenas, cerca de 6 min) + resumo em PDF (8 páginas) | 6 min + leitura |
| Observar | Tutorial da ficha com o exemplo "Cabanas do Vale" (continuação dos módulos 0 e 2) | 4 min |
| Executar | Ficha "A minha Tabela de Preço e Canais" (6 telas) + planilha "Tabela de Preço e Canais" | 20 a 30 min |
| Validar | Resultado em cinco partes + critério de conclusão (selo) | 3 min |
| Entregar | PDF da Tabela (página 3 do Plano) + plano de ação + próxima etapa (Módulo 4) + prompt de IA | 2 min |

## 6. Regras da ferramenta (testáveis, `src/logic.js`)
### 6.1 Entradas
Custo: `custoVariavelNoite`, `custoNoiteVendida` (obrigatórios; o segundo não pode ser menor que o primeiro), `diariaAtual`, `noitesPorEstadia` (vazio = 1, com aviso), `receitaMes` (opcional). Botão "Trazer os números da minha Folha Única" lê `zion-t2-financas` com a lógica do Módulo 2 (sem alterá-la).
Canais (até 5): nome, % da receita (mix), comissão %, taxa de pagamento %, outro custo por reserva (R$), venda direta (sim/não); `impostoPct` global; `gestorCanais`, `motorReservas`. Bloqueios: mix ≠ 100%, negativo, deduções ≥ 100%, canal sem nome, nenhum canal. Aviso: nenhuma linha de venda direta.
Referência: até 9 concorrentes, `terco` (baixo 0,85, meio 1, cima 1,20), `referencia` (obrigatória). Avisos: menos de 3; de 3 a 5.
Piso: `margemMinima` %, `pisoDeclarado` (obrigatório, não pode passar da referência; abaixo do custo = aviso), `quemConhece`, três `condicoes`.
Calendário: fatores (vale, baixa, alta, pico; base fixa 1,00; aviso fora do ponto de partida da fonte; bloqueio ≤ 0 ou > 5), `ano` (2024 a 2099), `mesInicio`, faixa de meio de semana e de fim de semana de cada um dos 12 meses (vale, baixa, base, alta).
Picos (até 8): nome, mês, noites (inteiro ≥ 1), fator (0,01 a 5), mínimo de noites; bloqueio se as noites de pico de um mês passam dos dias do mês. Meta de venda direta % e prazo (obrigatórios).

### 6.2 Cálculo
- Deduções do canal = comissão + pagamento + imposto. Líquido por noite = referência × (1 − deduções) − custo por reserva ÷ noites por estadia. Depois do custo variável = líquido − custo variável por noite.
- Custo da noite no canal (elaboração declarada da regra da fonte "custo mais comissão") = (custo por noite vendida + custo por reserva ÷ noites por estadia) ÷ (1 − deduções). O canal mais caro é o de maior valor entre os canais com venda; piso calculado = esse custo × (1 + margem mínima).
- Limite do variável (regra das três faixas) = (custo variável + custo por reserva ÷ noites) ÷ (1 − deduções) no canal mais caro.
- Comissão média ponderada = Σ mix × comissão; venda direta atual = Σ mix dos canais diretos; comissão que deixaria de sair num mês = receita do mês × (meta − atual) × comissão média dos canais pagos (conta, não previsão).
- Referência: média dos concorrentes sem o maior e o menor (mínimo 3) × fator da posição.
- Diária da faixa = referência × fator. Noites do mês: fim de semana = noites de sexta e de sábado do calendário real; as noites de pico saem primeiro do meio de semana (convenção declarada). Média do mês = (noites de semana × diária + noites de fim de semana × diária + Σ noites de pico × referência × fator da data) ÷ dias. Diária média do calendário = soma das 12 médias ponderadas ÷ noites do ano.

### 6.3 Leituras (regras das fontes, sem nota)
Referência × custo (Etapa 08 P03: referência que não cobre o custo = estrutura de custo); piso × custo e × piso calculado; regra do desconto em três faixas (Etapa 09 P08) no canal mais caro; calendário (preço fixo erra nas duas direções; diária média das diárias-alvo, não previsão); fim de semana (Etapa 08 P07: em destino de escapada curta, 25% a 60% mais); canais (maior e menor margem, comissão média); venda direta (meta × atual, com a conta da comissão).

### 6.4 Causa principal e prioridades (até três, nesta ordem)
1 referência abaixo do custo da noite → 2 piso abaixo do custo da noite → 3 faixa ou data abaixo do piso → 4 preço fixo o ano inteiro → 5 datas de pico sem regra (nenhuma data ou mínimo menor que 2) → 6 sem venda direta → 7 dois ou mais canais pagos sem gestor de canais → 8 venda direta sem motor de reservas → 9 piso só na cabeça (sem "quem já sabe"). Nada dispara: "Tabela dentro das regras da fonte" (marcar as quatro revisões trimestrais). A ordem segue a lógica das fontes: custo antes de preço (Etapa 08 P03, Etapa 09 P08), piso antes do calendário (G3 passos 01 a 03), canais depois (G2 "define o custo de aquisição que o G3 precisa cobrir").

### 6.5 Critério de conclusão (selo)
Tabela com referência, piso escrito, os 12 meses com faixa, mix de canais com percentual em todas as linhas somando 100%, meta de venda direta acima da atual com prazo; plano de ação com 10 letras ou mais e prazo; PDF baixado.

## 7. Telas da ficha
0 Abertura → 1 O custo da noite → 2 Os seus canais → 3 A diária de referência → 4 O piso e as condições → 5 As cinco faixas e os doze meses → 6 Datas de pico e meta de venda direta → Resultado (piso em destaque; 1 a tabela: faixas, calendário, picos, canais, folha do piso; 2 significado; 3 atenção; 4 o que fazer; 5 como verificar; próxima etapa Módulo 4; complementos: planilha, Precificador, Ferramenta 01).

## 8. Planilha "Tabela de Preço e Canais" (em branco e exemplo)
Abas: Comece aqui · Custo e Referência · Mapa de Canais · Piso · Calendário 12 meses (contagem de sextas e sábados por fórmula, sem função de 2010) · Datas de pico · Resumo (causa principal na mesma ordem da ficha) · Checklist da revisão (10 itens). Testada no LibreOffice contra conta independente em Python (inclusive calendário que atravessa o ano e fevereiro bissexto).

## 9. Exemplo didático (dados fictícios, conferido duas vezes: lógica e planilha)
Cabanas do Vale, 4 unidades, a mesma dos módulos 0 e 2. Custo variável por noite R$ 28,32 e custo por noite vendida R$ 153,04 (Folha de outubro do Módulo 2); diária praticada R$ 280; 2,32 noites por estadia; receita de hospedagem de um mês R$ 16.240.
Canais (mix dos últimos três meses): Plataforma A 50% (comissão 16%), Plataforma B 20% (15%), venda direta por site e WhatsApp 30% (0%); taxa de pagamento 1,5% e imposto 6% em todos. Comissão média ponderada **11,0%** (a mesma da Folha do Módulo 2). Deduções 23,5% / 22,5% / 7,5%. Na referência de R$ 300: líquido por noite **R$ 229,50 / 232,50 / 277,50**; depois do custo variável **R$ 201,18 / 204,18 / 249,18** (diferença de R$ 48 por noite entre a venda direta e a Plataforma A). Gestor de canais: sim; motor de reservas: não.
Referência: concorrentes 270, 280, 290, 300, 310, 320 e 360; sem 270 e 360, média de 5 = **R$ 300**; posição do meio → referência R$ 300.
Piso: custo da noite na Plataforma A = 153,04 ÷ 0,765 = **R$ 200,05**; margem mínima 10% → piso calculado **R$ 220,06**; piso escrito **R$ 225** (75% da referência). Limite do variável 28,32 ÷ 0,765 = R$ 37,02. Quem sabe: "Eu e quem responde o WhatsApp". Condições: terceira noite com café da manhã incluso; saída tardia até as 14 h; cesta de boas-vindas.
Faixas (fatores 0,75 / 0,90 / 1,00 / 1,50 / 2,20): **R$ 225 / 270 / 300 / 450 / 660**. Calendário de jan a dez de 2027 (meio de semana / fim de semana): jan baixa/base, fev baixa/base, mar vale/baixa, abr vale/baixa, mai vale/base, jun base/alta, jul alta/alta, ago base/alta, set baixa/base, out baixa/base, nov vale/baixa, dez baixa/base. Datas de pico: Carnaval (fev, 4 noites, 2,20, mínimo 4, R$ 660), Corpus Christi (mai, 4, 1,90, mínimo 3, R$ 570), Festival de inverno, evento local (jul, 3, 2,00, mínimo 2, R$ 600), Réveillon (dez, 5, 2,40, mínimo 5, R$ 720). Noites: vale 84, baixa 122, base 99, alta 44, pico 16 = 365. Outubro: média **R$ 279,68** (coerente com a diária média de R$ 280 da Folha). Diária média do calendário **R$ 305,92**. Amplitude 3,2 (720 ÷ 225).
Meta de venda direta: 30% → **40% até 30/06/2027**; com a mesma receita de R$ 16.240, deixaria de pagar cerca de **R$ 255,20** de comissão num mês (16.240 × 10% × 15,71%), conta com os números, não previsão.
Causa principal: **venda direta sem motor de reservas** (única prioridade). Ação: instalar um motor de reservas no site ligado ao calendário.

## 10. Versão autônoma e acompanhada
Mesmo conteúdo; no acompanhamento a Tabela é revisada pela equipe Zion no marco da semana 6, com a rubrica (coerência 40, justificativa 30, riscos 20, clareza 10), e a prioridade 1 vira compromisso do encontro.

## 11. Lacunas das fontes e elaborações declaradas
- A fonte não dá fórmula nem percentual para a margem mínima do piso ("custo mais a margem mínima"): a fórmula do piso é elaboração e a margem é decisão do membro (exemplo 10%).
- A fonte não define régua para comissão média nem número para a meta de venda direta: a ficha só exige meta acima da atual e com prazo.
- Contagem de fim de semana (sexta e sábado) e a regra de descontar as noites de pico primeiro do meio de semana são convenções desta lição.
- O exemplo da Etapa 08 usa valores de serra (referência R$ 560) que não foram reaproveitados: o exemplo desta lição é a Cabanas do Vale.
- Custo por noite vendida alinhado em R$ 153,04 em toda a jornada (153,0414 sem arredondar as parcelas; decisão de 10/11/2026). O botão "Trazer da Folha" traz o mesmo valor do exemplo.

## 12. Compatibilidade com o ZAIOS
Chave local `zion-t2-preco`; estado com `situacao`, `diag`, custos, `canais[]`, `concorrentes[]`, `terco`, `referencia`, `margemMinima`, `pisoDeclarado`, `quemConhece`, `condicoes[]`, `fatores`, `ano`, `mesInicio`, `meses[]`, `picos[]`, `metaDireta`, `prazoMeta`, `acao`, `prazo`, `pdf`. A lógica roda igual no Node. Dependência futura: ler o custo da Folha do membro no servidor, em vez do aparelho.
