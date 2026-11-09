# Atualização das ressalvas H1/H2

Comando 05E · 09/11/2026 · **Proposta para revisão do Bruno. Não é homologação matemática definitiva nem econômica.** Atualiza a seção 4 do parecer do Comando 05D (`docs/academy/comando-05d/PARECER_HOMOLOGACAO_MATEMATICA.md`), que fica preservado como estava.

As classes são as mesmas:
- **H1:** homologável;
- **H2:** homologável com ressalvas;
- **H3:** não homologável;
- **H4:** fora do escopo matemático.

H1 e H2 dizem respeito só à correção matemática, para as versões registradas no controle de versões do 05D. Elas não aprovam a metodologia nem a viabilidade.

## 1. O que muda

| Ferramenta · grupo | 05D | 05E (proposta) | Por quê | Ressalva que continua |
|---|---|---|---|---|
| **ZAIOS · EBITDA com custos do modelo** | H2 | **H1** | Aluguel, gestão e royalty conferem com o cálculo independente (4 casos) | Gestão e royalty sobre a receita bruta (convenção da ZAIOS) |
| **ZAIOS · outras receitas, custo por estadia, sazonalidade** | não testado | **H1** | 5 casos conferem | D9 e D14 pendentes (regra, não matemática) |
| **ZAIOS · composição: 1º ano, capital de giro A/B, captação, curva de caixa, colchão, cenários, estresse, régua** | fora do alcance | **H2** | Os 16 valores conferem com o cálculo independente, mas num **cenário único** | Ampliar para pró-labore, sazonalidade e outras receitas passando pela composição, e para abertura fora de janeiro |
| **ZAIOS · G2 (resultado gerencial, margem, cobertura da reserva)** | fora do alcance | **H1** | 9 casos conferem com os exemplos documentados | O7 (impostos como despesa variável); D12 pendente |
| **ZAIOS · G3 (noites, ocupação, diária, RevPAR, TRevPAR, despesa por noite, ano bissexto)** | fora do alcance | **H1** | 7 casos conferem | Diária sem taxa de limpeza (D14) |
| **B08 · VPL e TIR** | H2 | **H1** | Conferem com rampa, reajuste, extras e comissão separada, e com valor residual | Residual em % é divergência D7-C (metodologia) |
| **B08 · payback** | H2 | **H2** | O simples confere em mais um cenário | O descontado fica nulo além de 10 anos (D8 pendente) |
| **B08 · ponto de equilíbrio** | H2 | **H2** | A conta está certa com e sem reserva | O3: a reserva dentro das deduções eleva o equilíbrio (consequência da D2-C) |
| **A09 · payback** | H2 | **H1** (valor) | Confere em um cenário com contingência, extras, comissão e gestão | O rótulo continua sendo "payback simplificado", estático e sem limite (D8, O4) |
| **A09 · receita (dias no ano)** | H2 | **H2** | Confere com o que a ferramenta define | D5. **Correção do 05D:** o campo aceita 31 noites/mês, então o ano pode ter **372** dias, não "no máximo 360" |
| **A09 · deduções com gestão** | H1 (com O2) | **H1** (com O2) | A conta está certa | O2: gestão como dedução |
| **B06 · inteiro** | H2 | **H2** | Cobertura ampliada para os 3 perfis, desembolso mensal e custo/m² (17 casos) | A independência é parcial: não há documento-fonte da regra, que foi descrita a partir do código. Também D6 |
| **F05 · orçamento** | H1 | **H1** (cobertura ampliada) | Diferença verba − total, R$/m² interna e total, versão em branco | — |
| **Folha J2 · indicadores, fôlego, equilíbrio, saldo de caixa, custos do modelo** | H2 | **H1** | 12 casos conferem com o dicionário, em 2 cenários derivados do exemplo oficial | O6: custos do modelo em R$; D12 pendente. Deduções e resultado operacional seguem H2 (sem teste novo) |
| **Folha J2 · reserva de reposição** | H2 | **H2** | Sem mudança | D2-C: base na receita real |
| **Folha J2 · 92 testes próprios** | não revisados | **não revisados** | Fora do escopo desta etapa | — |

## 2. O que não muda

- **H3:** nenhum grupo.
- **H4:** todos os parâmetros de referência e os limites da Régua Única (deduções 17%, quebra 1%, reserva 4% e faixa, R$ 40/h, rampa 40/50/75%, OS&E, pré-abertura, contingências, cenários, múltiplo 6×, 8 e 12 anos, colchão de 10%, 3 meses de fixo).
- **Integridade da cópia da ZAIOS:** ressalva aberta. Tudo o que está classificado para a ZAIOS vale **sob a condição** de que a cópia corresponda ao commit `ec21ad5`.

## 3. Quadro consolidado proposto (05D + 05E)

| Grupo de cálculo | ZAIOS | B08 | A09 | B06 | F05 | Folha J2 |
|---|---|---|---|---|---|---|
| Receita, ocupação, noites | H1 | H1 | H2 (D5, até 372 dias) | — | — | H1 (indicadores) |
| Outras receitas, estadia, sazonalidade | H1 | — | — | — | — | — |
| Deduções e custos variáveis | H1 | H1 | H1 (O2) | — | — | H2 (sem teste novo) |
| Quebra e perdas | H1 (%); R$ N/I (D3-A) | N/I | N/I | — | — | H2 |
| Reserva de reposição (mecânica) | H1 | H2 (D2-C) | N/I | — | — | H2 (D2-C) |
| Pró-labore | H1 | N/I | N/I | — | — | H2 |
| Resultado operacional | H1 | H1 | H1 | — | — | H2 (sem teste novo) |
| EBITDA com custos do modelo | **H1** | — | — | — | — | **H1** (O6) |
| Retorno anual / acumulado | H1 / N/I | H1 / H1 (rótulos D1) | H1 (rótulo D1) | — | — | — |
| VPL e TIR | H1 | **H1** | — | — | — | — |
| Payback | H1 | H2 (D8) | **H1** (valor; D8, O4) | — | — | — |
| Ponto de equilíbrio | H1 | H2 (O3) | H1 | — | — | **H1** |
| Fôlego e caixa | — | — | — | — | — | **H1** (D12) |
| Composição (1º ano, giro, captação, curva, colchão, cenários, estresse) | **H2** (cenário único) | — | — | — | — | — |
| G2 e G3 | **H1** (O7) | — | — | — | — | — |
| CAPEX e contingência | H1 (F01) | — | — | H2 (independência parcial; D6) | H1 | — |
| Valor de saída | H1 (múltiplo); N/I (D7-C) | H2 (D7-C) | — | — | — | — |
| Régua: lógica | H1 | N/I | N/I | — | — | — |
| Régua: limites e parâmetros | H4 | H4 | H4 | H4 | H4 | H4 |

## 4. Riscos que continuam registrados (nenhum foi corrigido)

| Risco | Situação em 09/11/2026 | Evidência 05E |
|---|---|---|
| ZAIOS mostra o veredito antes da homologação | Aberto | `C-ZAIOS-C-veredito` |
| ZAIOS usa faixa de reserva de 3–5%; a aprovada é 3–6% | Aberto | Caso do 05D (T9) |
| A09 coloca a gestão nas deduções | Aberto (O2) | `C-A09-G-1` |
| B08 inclui a reserva nas deduções para o equilíbrio | Aberto (O3) | `C-B08-E-2` |
| D5, D6, D8, D9, D10, D12, D13 e D14 sem decisão | Abertos | `C-A09-D-1` (D5) e casos do 05D |
| **Novo · O6:** a Folha J2 recebe aluguel, gestão e marca em R$; o dicionário os define como % da receita | Para classificar | `C-J2-M-*` |
| **Novo · O7:** a G2 da ZAIOS classifica impostos como despesa variável; o dicionário trata tributos sobre a receita como dedução | Para classificar | `C-G2-impostos` |
| **Novo · correção do 05D:** o A09 aceita até 372 dias/ano (31 × 12), não "no máximo 360" | Corrigir o texto do parecer numa próxima versão (só documento) | `C-A09-D-1`, `C-A09-D-2` |
