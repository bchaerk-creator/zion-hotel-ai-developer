import asyncio,edge_tts,os,json,subprocess
V=os.path.dirname(os.path.abspath(__file__))
S=["Você tem uma hospedagem ou um terreno que já tem infraestrutura, e quer ser parceiro da Zion? É assim que a parceria funciona.",
"Você entra com a área e a infraestrutura: o deck de madeira, a instalação de luz, a água, a internet, a fossa e a mobília da unidade.",
"A Zion entra com a cabana, com a marca e a reputação, com o sistema e a gestão das reservas, e com a formação da equipe.",
"E quem opera? Um gerente local, contratado pela Zion e formado pela Zion, dentro dos padrões das nossas unidades.",
"Quanto fatura uma cabana dessas? Quanto você ganha? Isso a gente estrutura junto, na reunião: quantas cabanas cabem no seu local, quanto cada lado entra e como fica a conta no seu caso.",
"Quer saber mais? Entre para o clube e vire parceiro da Zion. Nós vamos te ajudar."]
async def main():
    out=[]
    for i,t in enumerate(S):
        p=f"{V}/n{i+1}.mp3"
        await edge_tts.Communicate(t,"pt-BR-AntonioNeural",rate="-3%",proxy=os.environ.get("HTTPS_PROXY")).save(p)
        d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
        out.append(d); print(i+1, round(d,1),"s")
    json.dump(out,open(f"{V}/dur.json","w"))
asyncio.run(main())
