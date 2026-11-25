import json,os
BASE='https://bchaerk-creator.github.io/zion-hotel-ai-developer/ads/mm47-fase03/'
DEST='https://infoprodutos-zion.clickmax.space/mini-mentoria'
# Padrao unico em 09-tracking/PADRAO_UTM.md: URL de destino SEM parametros; as tags vao em campo separado (colar so nas Tags de URL do Meta).
TAGS='utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content={id}&utm_term={{{{ad.id}}}}&sck={{{{campaign.id}}}}&ad_id={{{{ad.id}}}}&campaign_id={{{{campaign.id}}}}&adset_id={{{{adset.id}}}}'
DESC='Mini Mentoria de Estruturação · R$ 47'
CORPO=("O que você recebe: 9 módulos e 70 aulas e materiais, com 12 meses de acesso: aulas gravadas, fichas \"Faça agora\", e-books, "
"planilhas de cálculo em branco, kit do investidor (modelos), kit de prompts e Dossiê de Desenvolvimento.\n\n"
"Sem reunião e sem atendimento individual. Parcerias e investimentos não fazem parte do produto; são possibilidades sujeitas à análise. "
"R$ 47, pagamento único, Pix ou cartão à vista, reembolso em 7 dias.")
A=[
dict(id='mm47f3-c03-custo-escondido',conceito='C03 Dor específica',ecroi='E (Espelhamento) com O',formato='imagem 1080x1350',files=['c03-custo-escondido.png'],
 headline='Quanto custa deixar tudo pronto?',
 primeira='R$ 47 · Você sabe o preço da cabana. Sabe quanto custa deixar tudo pronto?',
 texto='Quando a conta começa, aparecem estrada, energia, fossa, projeto, taxas, móveis e enxoval.\n\nNa Mini Mentoria de Estruturação você aprende o passo a passo para montar o orçamento de abertura e a pré-viabilidade do seu projeto, com planilhas de cálculo em branco para preencher com os seus números.\n\n'+CORPO,
 hipotese='Dor concreta de custo gera mais cliques qualificados que a dor genérica de capital. Métrica: CTR de link e custo por visualização da página.'),
dict(id='mm47f3-c06-obra-ultimo-passo',conceito='C06 Colapso de crença',ecroi='C (Colapso de Crença) com R',formato='imagem 1080x1350',files=['c06-obra-ultimo-passo.png'],
 headline='Estruture antes de construir',
 primeira='R$ 47 · "Primeiro eu construo, depois eu vejo se dá certo." Começar pela obra é começar pelo último passo.',
 texto='Antes de gastar com a obra, dá para organizar território, mercado, produto, modelo de negócio, masterplan e a conta do projeto.\n\nNa Mini Mentoria de Estruturação você aprende o passo a passo, em sete pilares, para estruturar um empreendimento turístico no papel.\n\n'+CORPO,
 hipotese='Confrontar a crença "construir primeiro" atrai quem ainda não estruturou. Métrica: CTR de link e taxa de início de checkout por clique.'),
dict(id='mm47f3-c08-oferta-47',conceito='C10 Apresentação objetiva da oferta',ecroi='O (Orientação) com I',formato='imagem 1080x1350',files=['c08-oferta-47.png'],
 headline='Mini Mentoria por R$ 47',
 primeira='R$ 47 · Mini Mentoria de Estruturação: aprenda o passo a passo para estruturar o seu empreendimento turístico.',
 texto='Pagamento único, Pix ou cartão à vista, reembolso em 7 dias e 12 meses de acesso.\n\n'+CORPO,
 hipotese='Oferta direta converte melhor em público quente (remarketing) do que em frio. Métrica: início de checkout e compra em remarketing.'),
dict(id='mm47f3-c09-objecoes',conceito='C08 Quebra de objeções',ecroi='R (Reconhecimento) com C',formato='imagem 1080x1350',files=['c09-objecoes.png'],
 headline='Quatro perguntas honestas',
 primeira='R$ 47 · É reunião? Preciso de capital? E se eu não gostar? Garante parceria? Respostas diretas.',
 texto='Não é reunião nem consultoria: é acesso a uma plataforma. Você não precisa ter o capital para começar a estruturar. Há reembolso em 7 dias. E parceria ou investimento não fazem parte do produto.\n\n'+CORPO,
 hipotese='Responder objeções antes do clique reduz abandono no checkout. Métrica: razão compra/início de checkout.'),
dict(id='mm47f3-c10-obra-ou-estrutura',conceito='C07 Comparação de alternativas',ecroi='R (Reconhecimento) com O',formato='imagem 1080x1350',files=['c10-obra-ou-estrutura.png'],
 headline='Obra primeiro ou estrutura primeiro?',
 primeira='R$ 47 · Obra primeiro ou estrutura primeiro? A Mini Mentoria ensina a segunda forma, em sete pilares.',
 texto='Começar pela obra deixa as dúvidas de custo, mercado e projeto para o meio do caminho. Começar pela estrutura responde essas perguntas no papel.\n\nAprenda o passo a passo na Mini Mentoria de Estruturação.\n\n'+CORPO,
 hipotese='Comparar abordagens (não concorrentes) ajuda quem está decidindo como começar. Métrica: CTR de link e tempo na página.'),
dict(id='mm47f3-c02-plataforma-por-dentro',conceito='C02 Demonstração real da plataforma (carrossel 5 cartões)',ecroi='I (Implementação) com O',formato='carrossel 1080x1350, 5 cartões',
 files=['c02-plataforma-%d.png'%i for i in range(1,6)],
 headline='Veja por dentro da plataforma',
 primeira='R$ 47 · Veja por dentro da plataforma: capturas reais das telas da Mini Mentoria de Estruturação.',
 texto='Marco Zero, diagnóstico prévio e pré-viabilidade: veja como você aplica o passo a passo dentro da plataforma.\n\n'+CORPO,
 hipotese='Mostrar o produto funcionando reduz a desconfiança de infoproduto. Métrica: CTR de link e deslizes por impressão.'),
dict(id='mm47f3-c04-ordem-certa',conceito='C04 Tutorial prático / carrossel educativo (6 cartões)',ecroi='O (Orientação) com I',formato='carrossel 1080x1350, 6 cartões',
 files=['c04-ordem-certa-%d.png'%i for i in range(1,7)],
 headline='A ordem certa para estruturar',
 primeira='R$ 47 · A ordem certa para estruturar um empreendimento turístico, em sete pilares.',
 texto='Marco Zero, território, mercado, produto, modelo de negócio, masterplan, pré-viabilidade e Dossiê: veja a ordem do passo a passo.\n\nAprenda esse caminho na Mini Mentoria de Estruturação.\n\n'+CORPO,
 hipotese='Conteúdo educativo entrega valor antes do pedido e filtra curiosos. Métrica: CTR de link e custo por início de checkout.'),
]
out=[]
for a in A:
    d=dict(a);d['arquivos']=[dict(arquivo='docs/ads/mm47-fase03/'+f,url_publica=BASE+f) for f in a['files']];del d['files']
    d['cta_meta']='Saiba mais';d['cta_arte']='Aprenda o passo a passo · R$ 47'
    d['url_destino']=DEST;d['url_tags']=TAGS.format(id=a['id']);d['url_tags_teste_ab']={'A':TAGS.format(id=a['id']+'-varA'),'B':TAGS.format(id=a['id']+'-varB')};d['descricao']=DESC;d['status']='pronto para aprovação de Bruno; não enviado ao Meta'
    out.append(d)
os.makedirs('docs/ads/mm47-fase03',exist_ok=True)
json.dump(out,open('docs/ads/mm47-fase03/manifesto.json','w'),ensure_ascii=False,indent=2)
md=['# Copies MM47 · Fase 03 (Mini Mentoria R$ 47)\n','Botão em todos: **Saiba mais**. Destino: '+DEST+'. Padrão único de UTM, `sck` e ids em `zion-sales-engine/09-tracking/PADRAO_UTM.md`: a URL abaixo é só o destino, e as **Tags de URL** vão coladas uma vez no campo de parâmetros do anúncio (não cole na URL). Nada foi enviado ao Meta: material para aprovação de Bruno.\nArtes: fundo sólido, sem foto e sem pessoas; telas reais da plataforma onde aparecem. Rodapé de cada arte traz as condições.\n']
for a in out:
    md+=['## '+a['id'],'**Conceito:** '+a['conceito']+' · **ECROI:** '+a['ecroi']+' · **Formato:** '+a['formato'],'**Primeira linha:** '+a['primeira'],'**Texto principal**\n'+a['texto'],'**Título:** '+a['headline']+' · **Descrição:** '+a['descricao'],'**URL de destino (sem parâmetros):** '+a['url_destino'],'**Tags de URL (colar só no campo de parâmetros do anúncio):** `'+a['url_tags']+'`','**Hipótese:** '+a['hipotese'],'']
open('docs/ads/mm47-fase03/COPIES.md','w').write('\n'.join(md))
print(len(out),max(len(a['headline']) for a in out))
