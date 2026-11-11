import asyncio,edge_tts,os,json,subprocess
V=os.path.dirname(os.path.abspath(__file__))
S=["Você tem o terreno. Já imaginou as cabanas, a pousada, a bolha no meio da mata. E parou na mesma pergunta de todo mundo: de onde vem o dinheiro?",
"Investidor não coloca dinheiro em terreno. Coloca em projeto que ele entende. Terreno parado não é falta de capital. É falta de projeto no papel.",
"A Zion desenvolve, gere e opera hospedagens desde 2020, em Urubici e Florianópolis, e está desenvolvendo mais de 23 destinos pelo Brasil. O caminho que ensinamos é o que usamos nas nossas unidades.",
"São cinco etapas, nesta ordem: potencial do terreno, modelo de hospedagem, números, proposta e apresentação. Cada etapa produz um documento. No fim, o seu Dossiê, pronto para um sócio, um investidor ou a própria Zion olhar.",
"No Zion Collection Club você aprende as cinco etapas, inscreve o seu terreno no Radar do Land Bank e faz a sessão estratégica com a nossa equipe. Duas vezes de quarenta e oito e cinquenta. Entre para o clube. Seja você o próximo destino."]
async def main():
    out=[]
    for i,t in enumerate(S):
        p=f"{V}/n{i+1}.mp3"
        await edge_tts.Communicate(t,"pt-BR-AntonioNeural",rate="-3%",proxy=os.environ.get("HTTPS_PROXY")).save(p)
        d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
        out.append(d); print(i+1, round(d,1),"s")
    json.dump(out,open(f"{V}/dur.json","w"))
asyncio.run(main())
