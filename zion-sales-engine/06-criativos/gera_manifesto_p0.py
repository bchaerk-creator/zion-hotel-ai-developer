# ZION CREATIVE · P0 · gera docs/ads/mm47-p0/manifesto.json e COPIES.md (rodar da raiz do repositório: python3 zion-sales-engine/06-criativos/gera_manifesto_p0.py)
import json,os
BASE='https://bchaerk-creator.github.io/zion-hotel-ai-developer/ads/mm47-p0/'
DEST='https://infoprodutos-zion.clickmax.space/mini-mentoria'
TAGS='utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content={id}&utm_term={{{{ad.id}}}}&sck={{{{campaign.id}}}}&ad_id={{{{ad.id}}}}&campaign_id={{{{campaign.id}}}}&adset_id={{{{adset.id}}}}'
DESC='Mini Mentoria Zion · R$ 47 · pagamento único'
CTA='Acesse a plataforma por R$ 47'
CURTO='R$ 47, pagamento único, Pix ou cartão à vista. Reembolso em 7 dias.'
LONGO=('Mini Mentoria de Estruturação Zion: formação digital autônoma com 9 módulos e 70 conteúdos, e acesso à plataforma digital. '
'Você recebe aulas gravadas, fichas interativas "Faça agora", e-books por pilar, 2 planilhas de cálculo em branco, Kit do Investidor (guia e modelos), '
'kit com 9 comandos prontos para usar com IA e Dossiê em PDF.\n\nR$ 47, pagamento único, sem mensalidade. Pix ou cartão à vista. Reembolso em até 7 dias. '
'Sem reunião e sem atendimento individual. Parcerias e investimentos não são garantidos nem fazem parte da compra.')
A=[
dict(id='mm47p0-vp0-a1-dor-direta',conceito='v-P0 do campeão Curso Terreno A1 v2 (dor direta)',ecroi='E, O',formato='carrossel 5',files=['vp0-a1-dor-direta-%d.jpg'%i for i in range(1,6)],
 hook='Tem terreno, mas não tem capital?',headline='Tem terreno? Estruture primeiro',
 primeira='Acesse a plataforma por R$ 47 · Tem terreno, mas não tem capital? Aprenda o passo a passo para estruturar o seu projeto.',
 texto='Você tem um terreno e quer desenvolver o seu primeiro empreendimento de hospedagem, mas não sabe por onde começar?\n\nAprenda o passo a passo para estruturar o seu projeto: analisar o território, fazer o estudo de mercado, montar o orçamento e organizar o Dossiê, para apresentar a potenciais parceiros e investidores.\n\nConheça a Mini Mentoria de Estruturação Zion. Acesse a formação completa por apenas R$ 47, em pagamento único.\n\n'+LONGO,
 hipotese='Mantém a dor direta e as fotos reais do A1 v2; troca "curso" por Mini Mentoria Zion e põe o preço na primeira linha e no último cartão. Métrica: CTR de link e custo por visita à página.'),
dict(id='mm47p0-vp0-a3-saiba-o-custo',conceito='v-P0 do campeão Curso Terreno A3 v2 (saiba o custo)',ecroi='E, R, O',formato='carrossel 5',files=['vp0-a3-saiba-o-custo-%d.jpg'%i for i in range(1,6)],
 hook='Antes de falar com um investidor, saiba quanto custa o seu projeto.',headline='Saiba quanto custa o seu projeto',
 primeira='Acesse a plataforma por R$ 47 · Antes de falar com um investidor, saiba quanto custa o seu projeto.',
 texto='Sem números, é difícil apresentar um projeto. Aprenda o passo a passo: território, mercado e orçamento, no seu ritmo, com planilhas de cálculo em branco para preencher.\n\nMini Mentoria de Estruturação Zion por apenas R$ 47, em pagamento único.\n\n'+LONGO,
 hipotese='Mantém a promessa de orçamento (a mais concreta do A3). Métrica: CTR de link e início de checkout por clique.'),
dict(id='mm47p0-vp0-carrossel-c-narrativa',conceito='v-P0 do Carrossel C campeão (narrativa nova)',ecroi='E, C, R, O, I',formato='carrossel 7',files=['vp0-carrossel-c-narrativa-%d.jpg'%i for i in range(1,8)],
 hook='Você tem um terreno em um destino turístico, mas não tem capital para desenvolver?',headline='Terreno + projeto = destino',
 primeira='Acesse a plataforma por R$ 47 · Você tem um terreno em um destino turístico, mas não tem capital para desenvolver?',
 texto='Você tem um terreno e quer desenvolver o seu primeiro empreendimento de hospedagem, mas não sabe por onde começar?\n\nAprenda o passo a passo para estruturar o seu projeto, conhecer alternativas de desenvolvimento e prepará-lo para apresentar a potenciais parceiros e investidores. Conheça a Mini Mentoria de Estruturação Zion. Acesse a formação completa por apenas R$ 47, em pagamento único.\n\n'+LONGO,
 hipotese='Preserva a ordem do campeão de leads (dor, potencial, equação, o que você tem, autoridade, não precisa construir, convite), agora com oferta explícita. Atenção: o campeão gerou lead de sessão paga, não compra; o teste mede compra e visita qualificada. Métrica: CTR de link, deslizes e início de checkout.'),
dict(id='mm47p0-n01-autoridade-operacao',conceito='Autoridade (bastidor documentado da operação)',ecroi='E, O',formato='imagem',files=['n01-autoridade-operacao.jpg'],
 hook='A Zion opera hospedagens em Urubici e Florianópolis.',headline='O método vem da operação',
 primeira='Acesse a plataforma por R$ 47 · A Zion opera hospedagens em Urubici e Florianópolis. Agora você aprende o passo a passo para estruturar o seu projeto.',
 texto='A Mini Mentoria reúne, em passo a passo, a forma como estruturamos um empreendimento turístico. Formação digital, sem reunião.\n\n'+LONGO,
 hipotese='Autoridade só com fato documentado (CLAUDE.md). Anos de mercado e títulos só com confirmação de Bruno [NC]. Métrica: CTR e tempo na página.'),
dict(id='mm47p0-n02-dossie-passeio',conceito='Demonstração: passeio pela plataforma (Dossiê)',ecroi='I, O',formato='carrossel 4',files=['n02-dossie-passeio-%d.jpg'%i for i in range(1,5)],
 hook='Cada ficha vira uma página do seu Dossiê.',headline='Veja a plataforma por dentro',
 primeira='Acesse a plataforma por R$ 47 · Cada ficha vira uma página do seu Dossiê. Veja em três telas reais.',
 texto='Diagnóstico prévio, ficha "Faça agora" e pré-viabilidade: veja como você aplica o passo a passo dentro da plataforma e gera o Dossiê em PDF no final.\n\n'+LONGO,
 hipotese='Mostrar o produto funcionando reduz a desconfiança. Telas reais aula, diagnóstico e pré-viabilidade (sem raiox, implantação, agendar e mapa). Métrica: CTR e deslizes por impressão.'),
dict(id='mm47p0-n03-exemplo-ficticio',conceito='Caso real: sem caso documentado; exemplo resolvido fictício',ecroi='R, I',formato='imagem',files=['n03-exemplo-ficticio.jpg'],
 hook='Como a conta do projeto vira uma tabela (dados fictícios).',headline='Exemplo resolvido (dados fictícios)',
 primeira='Acesse a plataforma por R$ 47 · Veja como a conta de um projeto vira uma tabela. Exemplo com dados fictícios.',
 texto='Os números da imagem são fictícios, só para mostrar como a planilha em branco funciona. Não são referência de custo, de mercado nem resultado de aluno. Na Mini Mentoria você preenche com os números do seu projeto.\n\n'+LONGO,
 hipotese='Substitui o caso real inexistente. O rótulo "dados fictícios" é obrigatório na arte e no texto. Métrica: CTR e custo por visita.'),
dict(id='mm47p0-n04-tres-perguntas',conceito='Tutorial prático (3 perguntas antes de gastar)',ecroi='E, R',formato='imagem',files=['n04-tres-perguntas.jpg'],
 hook='Responda antes de gastar com a obra.',headline='3 perguntas antes da obra',
 primeira='Acesse a plataforma por R$ 47 · Responda antes de gastar com a obra: quanto custa, quem é o hóspede e quanto precisa entrar por mês?',
 texto='Se alguma das três perguntas ficou sem resposta, estruture primeiro. Na Mini Mentoria você aprende o passo a passo para respondê-las.\n\n'+LONGO,
 hipotese='Pergunta direta filtra curiosos e atrai quem já pensa em obra. Métrica: CTR e início de checkout.'),
dict(id='mm47p0-n05-ponto-de-partida',conceito='Transformação do conhecimento (processo)',ecroi='R, O, I',formato='imagem',files=['n05-ponto-de-partida.jpg'],
 hook='Do terreno e das dúvidas ao Dossiê organizado.',headline='Do terreno ao Dossiê',
 primeira='Acesse a plataforma por R$ 47 · Do terreno e das dúvidas ao Dossiê organizado.',
 texto='O ponto de chegada é um Dossiê em PDF com território, mercado, produto, modelo de negócio, masterplan e pré-viabilidade. É a transformação do seu conhecimento e dos seus documentos; o resultado externo depende de você e do mercado.\n\n'+LONGO,
 hipotese='Mostra o processo e separa o que a plataforma entrega do resultado externo. Métrica: CTR e tempo na página.'),
dict(id='mm47p0-n06-entregaveis-numeros',conceito='Demonstração dos entregáveis (oferta em números)',ecroi='O, I',formato='imagem',files=['n06-entregaveis-numeros.jpg'],
 hook='O que vem dentro, em números.',headline='O que vem dentro, em números',
 primeira='Acesse a plataforma por R$ 47 · 9 módulos, 70 conteúdos, acesso à plataforma digital e o Dossiê em PDF.',
 texto='Todos os números vêm do conteúdo verificado da turma (ver ENTREGAVEIS_VERIFICADOS.md).\n\n'+LONGO,
 hipotese='Concreto e verificável; bom para remarketing. Métrica: início de checkout e compra.'),
dict(id='mm47p0-n07-para-quem-e',conceito='Quebra de objeções / filtro (para quem é e para quem não é)',ecroi='R, C',formato='imagem',files=['n07-para-quem-e.jpg'],
 hook='É para você? Seja direto.',headline='É para você?',
 primeira='Acesse a plataforma por R$ 47 · É para você? Quem tem terreno ou ideia, quer entender custo e topa estudar. Não é reunião nem garantia de resultado.',
 texto='Para quem espera reunião, consultoria individual ou garantia de parceria, investimento ou renda, esta formação não serve. Para quem quer aprender o passo a passo e preencher as fichas no seu ritmo, sim.\n\n'+LONGO,
 hipotese='Filtrar antes do clique atrai comprador, não curioso (indicador P0). Métrica: razão compra/início de checkout.'),
]
out=[];md=['# Copies MM47 · P0 de coerência (Mini Mentoria de Estruturação Zion, R$ 47)\n',
'Botão do Meta em todos: **Saiba mais**. A chamada com preço está na arte e na primeira linha: **Acesse a plataforma por R$ 47**. Destino: '+DEST+' (sem parâmetros). Padrão único de UTM em `zion-sales-engine/09-tracking/PADRAO_UTM.md` (as Tags de URL vão coladas só no campo de parâmetros do anúncio). Descrição de todos: "'+DESC+'". Nada foi enviado ao Meta; depende de "aprovado" de Bruno.\n',
'Peças `vp0-*` = versões corrigidas dos campeões; `n0*` = conceitos novos. Layout: foto real sem pessoas em bloco próprio, sem texto sobre foto, telas reais só aula, diagnóstico e pré-viabilidade.\n']
for a in A:
    d=dict(a);d['arquivos']=[dict(arquivo='docs/ads/mm47-p0/'+f,url_publica=BASE+f) for f in a['files']];del d['files']
    d.update(cta_meta='Saiba mais',cta_arte=CTA,url_destino=DEST,url_tags=TAGS.format(id=a['id']),descricao=DESC,status='pronto para aprovação de Bruno; não enviado ao Meta',
      compliance='Sem reunião, consultoria, cadastro/inscrição, taxa, equipe entrará em contato, investimento, sócio ou renda como resultado; "Aprenda o passo a passo"; preço e condições claros; fotos reais sem pessoas.')
    out.append(d)
    md+=['## '+a['id'],'**Conceito:** '+a['conceito']+' · **ECROI:** '+a['ecroi']+' · **Formato:** '+a['formato']+' · **Hook (3 s):** '+a['hook'],'**Primeira linha:** '+a['primeira'],'**Texto principal**\n'+a['texto'],'**Título:** '+a['headline']+' · **Descrição:** '+DESC,'**CTA:** botão Saiba mais; arte: '+CTA,'**Tags de URL:** `'+d['url_tags']+'`','**Hipótese:** '+a['hipotese'],'**Arquivos:** '+', '.join(a['files']),'']
json.dump(out,open('docs/ads/mm47-p0/manifesto.json','w'),ensure_ascii=False,indent=2)
open('docs/ads/mm47-p0/COPIES.md','w').write('\n'.join(md))
print(len(out))
