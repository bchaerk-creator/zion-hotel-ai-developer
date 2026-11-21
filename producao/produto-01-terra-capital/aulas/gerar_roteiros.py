"""Gera aulas/ROTEIROS.md (20 microaulas + boas-vindas + encerramento) e estima duração (2,5 palavras/s). Uso: python3 -I aulas/gerar_roteiros.py"""
import json, pathlib, re
A = pathlib.Path(__file__).resolve().parent; P = A.parent
d = json.load(open(P/"src/aulas.json")); N = lambda t: len(re.findall(r"\S+", t))
dur = lambda t: round(N(t)/2.5)
out = ["# Roteiros · Produto 01 · Você tem terra. Falta capital?\n",
 "Roteiros prontos para gravar. **Nenhum vídeo foi gravado ou gerado.** Duração estimada a 2,5 palavras por segundo (leitura calma); validar na gravação. Meta: até 120 s por aula.",
 "Estrutura de cada aula: abertura com pergunta (10 s) → conteúdo (60 a 90 s) → tarefa (10 a 20 s) → transição. Tela: ferramenta aberta com dados fictícios. Legendas obrigatórias. Voz e imagem: só com autorização expressa de quem aparece (Bruno ou outra pessoa).\n"]
tot = 0
for a in d["aulas"]:
    ab = a["pergunta"]; cont = a["texto"]; tar = f"Agora coloque isso em prática. {a['acao']}"; tr = "Na próxima aula, seguimos com a jornada." if a["n"] < 20 else "Revise seu plano todo mês e leve o dossiê a profissionais habilitados."
    sec = dur(ab)+dur(cont)+dur(tar)+dur(tr); tot += sec
    flag = "" if sec <= 120 else " ⚠ acima de 120 s: cortar frases"
    out.append(f"## Aula {a['n']} · {a['titulo']} (Pilar {a['pilar']})\n**Duração estimada:** {sec} s{flag}\n\n- **Abertura (≈{dur(ab)} s):** {ab}\n- **Conteúdo (≈{dur(cont)} s):** {cont}\n- **Tarefa (≈{dur(tar)} s):** {tar}\n- **Transição (≈{dur(tr)} s):** {tr}\n- **Na tela:** ferramenta “{a['ferramenta']}” com os dados fictícios do portal; destacar o número que a frase cita.\n")
out.append(f"**Total das 20 aulas (estimativa):** {tot//60} min {tot%60} s de vídeo. O restante dos 70 a 100 minutos vem das tarefas e das ferramentas.\n")
bv = "Olá. Eu sou o Bruno Chaerk, da Zion Hotel Group International. Se você tem um terreno e não tem capital para investir, esta jornada é para você. Aqui você vai aprender o passo a passo para organizar o seu projeto: quanto falta, o que precisa estar documentado, que caminhos existem para completar o capital e como apresentar tudo com clareza. Eu não prometo crédito, sócio ou investidor. Prometo método. Cada aula tem no máximo dois minutos e uma tarefa curta, e as ferramentas ficam abertas ao lado. Comece pela primeira aula."
en = "Você chegou ao fim da jornada. Agora você tem uma lacuna de capital calculada, um cenário ruim testado, um checklist com pendências visíveis e um dossiê preliminar. O próximo passo é levar isso a um advogado, a um contador e, quando estiver claro, a possíveis parceiros. Revise o seu plano todo mês. O patrimônio é um ponto de partida; o projeto precisa mostrar demanda, viabilidade e capacidade de execução. Obrigado por fazer esse caminho."
out.append(f"## Vídeo institucional de boas-vindas (≈{dur(bv)} s)\n{bv}\n\n**Imagens:** retrato de Bruno (`docs/assets/bruno/`) e fotos reais da Zion Bubble Glamping (`docs/assets/operacoes/`, sem pessoas: op04 a op12). Nada de imagem gerada como foto real. Texto na tela: “Material educativo. Sem promessa de crédito, sócio ou retorno.”\n**Depende de Bruno:** gravar a voz/imagem ou autorizar narração; aprovar o texto.\n")
out.append(f"## Vídeo de encerramento (≈{dur(en)} s)\n{en}\n\n**Imagens:** tela do dossiê pronto (dados fictícios) e foto real da Zion. **Depende de Bruno:** gravar ou autorizar narração.\n")
(A/"ROTEIROS.md").write_text("\n".join(out)); print("ok", tot, "s total")
over = [a["n"] for a in d["aulas"] if (dur(a["pergunta"])+dur(a["texto"])+dur(f"Agora coloque isso em prática. {a['acao']}")+dur("Na próxima aula, seguimos com a jornada.")) > 120]; print("acima de 120 s:", over)
