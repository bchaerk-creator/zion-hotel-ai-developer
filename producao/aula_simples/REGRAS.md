# Aula simples · padrão aprovado por Bruno (16/10/2026)

Referência visual: `docs/escola/z01/apresentacao/index.html` (Z01, 40 slides). Abra e copie o espírito.

## Para quem
Dono de Airbnb, dono de terreno, pequeno empreendedor. Pessoa simples, prática, sem formação em hotelaria.

## Regras de linguagem (obrigatórias)
- Frases curtas. Uma ideia por slide. Palavras do dia a dia.
- Fale com "você".
- **Nada de histórias** nem personagens (sem Marina, sem Rafael, sem "um cliente nosso").
- **Nada de siglas e nomes técnicos na tela**: sem ™, sem RevPAR, ADR, CAPEX, VPL, TIR, APP, CAR, ECROI. Se o conceito for essencial, diga o que é em palavras simples ("quanto custa montar tudo antes de abrir", em vez de CAPEX). No máximo, o nome técnico entre parênteses uma vez, nas notas.
- Sem citação de fontes na tela ("Volume 01", "Manual", "Panorama"). A fonte fica no e-book.
- Nenhum travessão (—). Use vírgula, ponto ou dois-pontos.
- Todo número é exemplo e está marcado como exemplo. Nunca números reais da Zion, nunca promessa de renda.
- Notas do slide = o que o Bruno fala para a câmera, em 1 a 3 frases, em primeira pessoa, tom de conversa.

## Método didático
Cada ideia vira: **pergunta → o aluno toca → resposta com o porquê**. O aluno chega à conclusão sozinho.
Use figuras (ícones), opções para tocar, marcar, calcular, semáforo e verdadeiro ou falso. Pouco texto corrido.

## Estrutura dos 40 slides
1. `capa`
2. `cartoes` "Como esta aula funciona" (Toque, Marque, Calcule, Decida)
3. e 4. `escolha` revisão do módulo anterior (de memória)
5. `escolha` com `todas_certas` "Em qual situação você está?" (Quero começar / Quero crescer)
6. `fluxo` "O caminho de hoje" (3 a 5 passos)
7 a 39: **5 partes** (ou 6), cada uma começando com `secao` (kicker "Parte X de N"). Dentro de cada parte, alterne tipos: `escolha`, `fluxo`, `cartoes`, `marcar`, `calculadora` (quando houver conta), `semaforo`, `regra`, e um `vf` de revisão no fim de cada parte ou a cada duas partes. Inclua ao menos 12 `escolha`, 3 `vf`, 1 `semaforo`, 2 `marcar`. Inclua `calculadora` se o módulo tiver conta.
39. `cartoes` "O que você leva desta aula" (4 ideias)
40. `tarefa` "Preencha o seu <entregável>" (4 passos, apontando para a ferramenta do e-book)

Total exato: 40 slides.

## Ícones disponíveis
key, star, house, bed, pin, cal, user, tool, tree, camera, brain, drop, eye, sun, doc, chart, alert

## Formato do roteiro (JSON)
```json
{
  "codigo": "D01",
  "titulo": "Território e Localização",
  "slides": [
    {"tipo": "capa", "kicker": "Aula D01 · Desenvolver", "titulo": "O que o seu <em>lugar</em> deixa fazer?", "lead": "Uma frase do que a pessoa vai conseguir no fim.", "notas": "..."},
    {"tipo": "cartoes", "titulo": "Como esta aula funciona", "sub": "Quatro tipos de tela.", "itens": [{"icone": "star", "titulo": "Toque", "texto": "escolha uma opção"}], "notas": "..."},
    {"tipo": "escolha", "pergunta": "...?", "sub": "Toque na opção certa.", "opcoes": [
      {"icone": "doc", "texto": "...", "certa": false, "feedback": "<b>Não.</b> porque..."},
      {"icone": "eye", "texto": "...", "certa": true, "feedback": "<b>Isso!</b> porque..."}], "notas": "..."},
    {"tipo": "escolha", "todas_certas": true, "pergunta": "Em qual situação você está?", "opcoes": [{"icone": "pin", "texto": "Quero começar", "feedback": "..."}, {"icone": "chart", "texto": "Quero crescer", "feedback": "..."}], "notas": "..."},
    {"tipo": "fluxo", "titulo": "...", "sub": "...", "ultimo_apagado": false, "passos": [{"icone": "pin", "titulo": "...", "texto": "..."}], "notas": "..."},
    {"tipo": "secao", "kicker": "Parte 2 de 6", "titulo": "...", "lead": "...", "notas": "..."},
    {"tipo": "marcar", "titulo": "...?", "sub": "Toque em cada item que...", "contador": "Você marcou X de N.", "itens": [{"icone": "drop", "texto": "..."}], "notas": "..."},
    {"tipo": "semaforo", "titulo": "...", "sub": "...", "verde": {"titulo": "Siga", "texto": "..."}, "amarelo": {"titulo": "Ajuste", "texto": "..."}, "vermelho": {"titulo": "Pare e resolva", "texto": "..."}, "notas": "..."},
    {"tipo": "vf", "titulo": "Verdadeiro ou falso?", "frases": [{"frase": "...", "verdadeiro": true}], "notas": "..."},
    {"tipo": "regra", "kicker": "Regra de ouro", "texto": "Frase curta com <em>destaque</em>.", "escuro": true, "notas": "..."},
    {"tipo": "calculadora", "titulo": "Faça a sua conta", "sub": "...", "campos": {"d": {"rotulo": "Diária (R$)", "valor": 400}, "n": {"rotulo": "Noites vendidas no mês", "valor": 15}, "c": {"rotulo": "Custos do mês (R$)", "valor": 3500}}, "botoes": [{"texto": "Mês fraco", "valor": 8}, {"texto": "Mês normal", "valor": 15, "ativo": true}], "aviso": "Números de exemplo, só para ilustrar.", "notas": "..."},
    {"tipo": "tarefa", "titulo": "Preencha o seu ...", "sub": "Está no capítulo X do e-book.", "passos": [{"titulo": "...", "texto": "..."}], "notas": "..."}
  ]
}
```
A calculadora faz sempre: entra = d × n; sobra = entra − c. Use-a só quando a conta do módulo couber nessa forma (diária × noites − custos, ou valor × quantidade − custo).
Máximo de opções por `escolha`: 4. Texto de opção: até 8 palavras. Feedback: até 25 palavras, começando com `<b>Isso!</b>` ou `<b>Não.</b>` (ou similar).

## Como gerar
1. Leia o e-book do módulo (`docs/escola/<cod>/index.html`) e o plano, se houver.
2. Escreva o roteiro em `producao/aula_simples/roteiros/<COD>.json`.
3. Rode `python3 producao/aula_simples/gerar.py producao/aula_simples/roteiros/<COD>.json docs/escola/<cod>/apresentacao/index.html`.
4. Confira: 40 slides, nenhum travessão, nenhuma sigla na tela, nenhuma história.
