# Simulador de investimento · Zion Glamping Store (14/11/2026)

Página nova e separada: `docs/store/simulador/` (index.html + logic.js). A página da Store (`docs/store/index.html`) **não foi alterada**.
URL: https://bchaerk-creator.github.io/zion-hotel-ai-developer/store/simulador/

## Conta
Receita/ano = diária × 365 × ocupação × nº de bolhas. EBITDA = receita × margem.
Investimento = soma dos itens × (1 + margem de segurança) × nº de bolhas.
Rentabilidade anual = EBITDA ÷ investimento. Prazo = investimento ÷ EBITDA.
Sem imposto sobre o lucro, depreciação, financiamento, curva de ocupação do 1º ano, terreno ou reposição da bolha.

## De onde vêm os números
- Premissas de Bruno (14/11): diária R$ 1.550, ocupação 65%, EBITDA 40%, bolha R$ 80 mil (valor de referência, editável).
- Case validado da Zion, já publicado na Store: R$ 1.571 e 60% de ocupação (botão na página).
- Itens 2 a 6 (já publicados na Store, por unidade): deck 50 m² × R$ 250 = 12.500; luz 10.000; água e esgoto ou fossa 8.500; mobiliário, equipamentos e enxoval 25.915; piso interno 3.931.
- Itens 7 a 10 (banheiro/anexos, projeto e licenças, frete e instalação, outros) e a margem de segurança começam em zero: **Bruno preenche**. Nada foi inventado.
- O botão "exemplo com dados fictícios" preenche esses itens com valores de teste e mostra a etiqueta "Dados fictícios".

## Resultado com os números acima (conta independente no teste)
Receita R$ 367.737,50; EBITDA R$ 147.095; investimento R$ 140.846; rentabilidade 104,4% ao ano; prazo de cerca de 11,5 meses. Com os itens 7 a 10 em zero esse número está superestimado, e a página avisa.

## Testes
`node producao/store/simulador/test_logic.js` (10 testes de lógica) e `node producao/store/simulador/e2e.js <pasta de prints>` (Playwright, celular e computador: valores, exemplo fictício, edição, WhatsApp, sem rolagem lateral).

## Decisões de Bruno pendentes
1. A página pública da Store não mostra preço da bolha ("preço especial à vista"). O simulador mostra R$ 80 mil como referência editável: manter ou deixar o campo vazio?
2. A Store publica 60% de ocupação; o simulador abre com 65% (premissa de trabalho). Qual deve ser o padrão público?
3. Ligar o simulador na página da Store (botão ou seção): mexe em página existente, só com "aprovado".
4. Preencher os itens 7 a 10 com o orçamento real da Zion.
5. Revisão jurídica do texto de rentabilidade (risco de ser lido como oferta de investimento).
