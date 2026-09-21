# Zion Investor Experience

Leia docs/MASTER.md antes de qualquer tarefa. Ele é a fonte única de números,
decisões e identidade visual. Os protótipos em docs/ são a referência aprovada.

## Regras
- Nenhum número fora de docs/MASTER.md ou de /data com fonte.
- Edição pública sem nenhum dado de retorno. Retorno só em /investor.
- Todo número público com SourceBadge. Sem fonte validada: selo "fonte em validação".
- Estrutura societária exatamente como em MASTER seção 2.
- Faturamento acumulado: R$ 9,88 mi até 30/06/2026. Não usar R$ 11,2 mi.
- Land bank nunca como hectares da Zion. Nunca nomes de proprietários.
- Crédito verde e certificações: possibilidade e processo, nunca aprovado ou obtido.
- Textos sem travessão longo. Nunca "rede de hotéis". Nunca "payback".

## Identidade
Tokens, tipografia, fotografia, movimento e componentes: MASTER seção 13.
Preto domina. Um único bloco dourado. Cormorant Garamond 300 e DM Sans.
Sem cantos arredondados, sem sombras, sem gradientes decorativos, sem ícones,
sem emoji, sem cartões idênticos em série.

## Qualidade
Responsivo até 360px. Foco visível. Contraste AA. Sem rolagem horizontal.
prefers-reduced-motion respeitado. Lighthouse acima de 90.

## Onde este projeto vive
Esta pasta é um projeto Next.js independente dentro do repositório
zion-hotel-ai-developer. A pasta docs/ da raiz do repositório é o site
público servido pelo GitHub Pages e não recebe nada deste projeto.
Os dados de /data são a fonte de verdade do site; docs/PLAN.md é o plano
aprovado por fase; `node scripts/validate-data.mjs` valida os JSON.
