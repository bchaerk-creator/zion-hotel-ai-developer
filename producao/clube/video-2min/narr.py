import asyncio,edge_tts,os,json,subprocess
V=os.path.dirname(os.path.abspath(__file__))
S=["A Zion é referência em hospedagens na natureza e em hospedagens de experiência. Desenvolvemos, gerimos e operamos as nossas unidades desde 2020, e estamos em busca dos melhores destinos por todo o Brasil. O seu pode ser o próximo.",
"O Zion Collection Club é a porta de entrada. Dentro do clube você entende mais sobre o setor, se prepara para ele e tem acesso aos melhores produtos do mercado: a formação, uma sessão estratégica de direcionamento inicial com a nossa equipe e o Radar do Land Bank.",
"Como funciona: em cinco etapas, nesta ordem. Potencial do terreno, modelo de hospedagem, números, proposta e apresentação. Cada etapa produz um documento. No fim, o seu projeto está pronto para ser apresentado.",
"E de onde vem o capital? Com o projeto no radar, ele pode vir da própria Zion, que avalia novas sedes pelo Brasil, ou do pool de investidores e parceiros que a Zion reúne. O clube abre o caminho para o parceiro, o sócio ou o investidor certo.",
"A Zion está em busca dos melhores destinos por todo o Brasil, e o seu pode ser o próximo. Entre para o clube e faça parte dessa oportunidade."]
async def main():
    out=[]
    for i,t in enumerate(S):
        p=f"{V}/n{i+1}.mp3"
        await edge_tts.Communicate(t,"pt-BR-AntonioNeural",rate="-3%",proxy=os.environ.get("HTTPS_PROXY")).save(p)
        d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
        out.append(d); print(i+1, round(d,1),"s")
    json.dump(out,open(f"{V}/dur.json","w"))
asyncio.run(main())
