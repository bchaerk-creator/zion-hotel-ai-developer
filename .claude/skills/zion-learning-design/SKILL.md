---
name: zion-learning-design
description: Sistema de produção educacional da Zion Hospitality Business School (Mentoria Zion 360°). Use ao planejar, escrever, revisar ou converter qualquer material da formação — e-book HTML, apresentação de aula, roteiro, workbook, ferramenta, avaliação, kit NotebookLM ou resumo executivo — de qualquer uma das 52 unidades (Z00 a Z02 e pilares D, F, E, M, L, G, O). Aplica princípios de ciência da aprendizagem com evidência (prática de recuperação, espaçamento, codificação dupla, carga cognitiva, princípios multimídia, exemplos resolvidos) dentro da identidade editorial Zion e das regras de fonte e aprovação da escola.
---

# Zion Learning Design

Sistema para produzir os materiais da Mentoria Zion 360° com o mesmo padrão do módulo Z00 aprovado por Bruno Chaerk. Este arquivo é o fluxo; os detalhes estão em `references/`.

Leia também, antes de produzir: a skill `zion-editorial-ebook` (identidade visual) e o material de referência aprovado em `docs/escola/z00/` (e-book em `index.html`, aula em `apresentacao/index.html`).

## 1. Regras inegociáveis

1. **Fonte antes de texto.** Conceitos, frameworks com ™/®, citações, casos e números vêm apenas dos manuscritos e volumes da Zion indicados no pedido. Nunca invente framework, "Caso Zion", estatística ou citação. Fatos externos (leis, órgãos, dados de mercado) só com fonte oficial verificada e data de consulta.
2. **Exemplos ilustrativos são rotulados** como "Exemplo ilustrativo" e toda conta é conferida duas vezes.
3. **Sem promessas** de crédito, investidor, retorno ou aprovação. Temas jurídicos e regulatórios: nível introdutório, com remissão a profissional habilitado.
4. **Duas jornadas em todo módulo:** Jornada A (quero começar) e Jornada B (quero crescer), com aplicação explícita para cada uma.
5. **Aprovação por etapa:** plano editorial → e-book → derivados → publicação. Nada é publicado, enviado ou ativado no ClickMax sem autorização específica de Bruno. Aulas entram no ClickMax desativadas.
6. **Sem neuromitos:** não use "estilos de aprendizagem", "10% do cérebro" ou "hemisfério direito/esquerdo".

## 2. Fluxo de produção de um módulo

1. **Alinhamento (desenho reverso).** Escreva 5 a 7 objetivos com verbos observáveis (Bloom revisada: lembrar, compreender, aplicar, analisar, avaliar, criar). Defina o entregável do módulo e a atividade aplicada que comprova o objetivo. Só depois o conteúdo.
2. **Mapa de fontes.** Liste, por seção, a fonte e o trecho usado. Marque o que é elaboração própria.
3. **Plano editorial** para aprovação (objetivos, sumário, exemplos, fontes, ferramenta, exercício, entregáveis).
4. **E-book (fonte mestre).** Siga `references/ebook.md`. Capítulos podem ser escritos em paralelo por subagentes com o guia `references/componentes-html.md`; monte com um script e revise o conjunto.
5. **Derivados** a partir do e-book aprovado: apresentação (`references/aula.md`), roteiro (notas do apresentador), workbook, ferramenta, avaliação (`references/avaliacao.md`), kit NotebookLM, resumo executivo.
6. **Auditoria de qualidade** com `references/checklist-qualidade.md`. Renderize em 360 px e 1280 px, gere o PDF e confira páginas, sobreposição de texto em diagramas, links e contas.
7. **Entrega para aprovação**: arquivos, o que foi revisado, decisões de conteúdo pendentes.

## 3. Princípios de aprendizagem (resumo)

Detalhes, referências e regras práticas em `references/principios.md`.

| Princípio | No e-book | Na aula |
|---|---|---|
| Prática de recuperação | perguntas sem consulta ao fim de cada capítulo, antes do resumo | quiz relâmpago a cada 8 a 10 slides |
| Espaçamento | caixas "Revisite" que retomam capítulos anteriores | abrir a aula com 3 perguntas da aula anterior |
| Intercalação | exercícios que misturam conceitos | casos em que o aluno escolhe a ferramenta |
| Codificação dupla | um diagrama explicativo por conceito-chave | uma ideia, um visual, uma frase curta |
| Carga cognitiva | seções curtas, do simples ao complexo, termo definido antes do uso | até ~40 palavras por slide; explicação na fala |
| Coerência e redundância | sem enfeites; legenda junto do gráfico | não ler o slide; notas do apresentador carregam o texto |
| Sinalização e segmentação | "Neste capítulo", títulos que afirmam, destaques escassos | mapa da aula, blocos com abertura, barra de progresso |
| Exemplos resolvidos e esmaecimento | resolvido → parcialmente resolvido → em branco | conta revelada passo a passo |
| Previsão e geração | perguntas "o que você acha?" antes da explicação | slides de previsão com resposta revelada |
| Elaboração | "por que isso funciona no seu caso?" | "explique ao colega em 1 minuto" |
| Feedback elaborado | gabarito comentado da autoavaliação | revelar a resposta e o porquê |
| Reversão pela expertise | caixas por jornada; "se já domina, vá para…" | diagnóstico inicial A/B |

## 4. Referências desta skill

- `references/principios.md` · os 12 princípios com citações e regras práticas
- `references/ebook.md` · estrutura, densidade e padrões do e-book de ~120 páginas
- `references/aula.md` · padrão da aula de 60 minutos em 40 slides
- `references/avaliacao.md` · perguntas, atividade aplicada, rubricas e distratores
- `references/componentes-html.md` · componentes HTML do e-book Zion e regras de redação para subagentes
- `references/checklist-qualidade.md` · auditoria antes de entregar
