import asyncio,edge_tts,os,json,subprocess
V=os.path.dirname(os.path.abspath(__file__))
S=["Com mais de vinte anos no mercado internacional e cinco anos no Brasil, desde 2020, a Zion é referência no setor de glamping no país. Estamos buscando novos parceiros e pessoas que queiram entrar nesse setor e aprender a faturar com hospedagem.",
"Você tem o terreno, a vontade e a ideia. O que falta é o caminho: por onde começar, com quem contar e como transformar isso em um destino que recebe hóspedes e gera receita.",
"Dentro do Zion Collection Club você ganha o que precisa para chegar lá: conhecimento, acesso aos melhores produtos do mercado, acesso a investimentos e a possibilidade de fazer parcerias e receber investidores. O seu terreno entra no Radar do Land Bank, e o capital pode vir da própria Zion ou do pool de investidores que a Zion reúne.",
"O nosso clube é o maior clube de glamping do Brasil, referência no setor. A Zion está em busca dos melhores destinos por todo o país. O seu pode ser o próximo destino da nossa expansão.",
"Entre para o clube. Transforme seu terreno em um destino turístico e faça parte dessa oportunidade."]
async def main():
    out=[]
    for i,t in enumerate(S):
        p=f"{V}/n{i+1}.mp3"
        await edge_tts.Communicate(t,"pt-BR-AntonioNeural",rate="-3%",proxy=os.environ.get("HTTPS_PROXY")).save(p)
        d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
        out.append(d); print(i+1, round(d,1),"s")
    json.dump(out,open(f"{V}/dur.json","w"))
asyncio.run(main())
