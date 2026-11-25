#!/usr/bin/env python3
"""ZION CREATIVE · Captação corrigida: gera docs/ads/captacao-p0/manifesto.json e COPIES.md e roda o grep de termos proibidos.
Uso: python3 -I gera_manifesto_captacao.py   (da pasta 06-criativos)"""
import json, re, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/ads/captacao-p0'))
BASE = 'https://bchaerk-creator.github.io/zion-hotel-ai-developer/ads/captacao-p0/'
TAGS = 'utm_source=meta&utm_medium=paid&utm_campaign=captacao&utm_content={id}&utm_term={{{{ad.id}}}}&sck={{{{campaign.id}}}}&ad_id={{{{ad.id}}}}&campaign_id={{{{campaign.id}}}}&adset_id={{{{adset.id}}}}'
COMUM = ('A Zion também tem formações pagas, como a Mini Mentoria de Estruturação Zion, por R$ 47 em pagamento único. Você só compra se quiser.')
CLARO = 'Não é reunião, consultoria nem avaliação do seu terreno. Não prometemos investimento, parceria nem renda.'
P = [
 dict(id='capt-c-carrossel-c', conceito='Carrossel C v-captação (campeão, 7 cartões, ordem preservada)', formato='carrossel 7 cartões PNG 1080x1350',
  hook='Você tem um terreno em um destino turístico, mas não tem capital para desenvolver?',
  primeira='Cadastro gratuito · Você tem um terreno ou projeto em destino turístico, mas não tem capital para desenvolver?',
  corpo=['Antes do capital, vem o projeto. A Zion organiza, em formação digital, o passo a passo para estruturar um empreendimento turístico: território, mercado, orçamento e pré-viabilidade.',
         'Cadastre-se de graça e receba conteúdos para dar os primeiros passos. O cadastro é gratuito e não obriga a nenhuma compra.', COMUM, CLARO],
  titulo='Cadastro gratuito: estruture o projeto', descricao='Formação paga a partir de R$47',
  arquivos=[f'docs/ads/captacao-p0/capt-c-carrossel-c-{i}.png' for i in range(1,8)],
  urls=[BASE+f'capt-c-carrossel-c-{i}.png' for i in range(1,8)]),
 dict(id='capt-v02-dono-terreno', conceito='Vídeo 02 Dono de Terreno v-captação (hook preservado; sem o áudio original)', formato='vídeo 9:16, 52 s, mudo com texto na tela (ou regravado por Bruno com o roteiro)',
  hook='Ei, você, dono de terreno!',
  primeira='Cadastro gratuito · Dono de terreno, você não precisa começar pela obra.',
  corpo=['Você tem a área, mas não sabe por onde começar ou não tem capital? Antes do capital, vem o projeto. Cadastre-se de graça e receba conteúdos da Zion sobre como estruturar um projeto de hospedagem.',
         'O cadastro é gratuito e não obriga a nenhuma compra. ' + COMUM, CLARO],
  titulo='Dono de terreno? Comece pelo projeto', descricao='Formação paga a partir de R$47',
  arquivos=['(fora do repositório) scratchpad/cap/video/capt-v02-dono-terreno-sem-audio.mp4'], urls=[None]),
 dict(id='capt-v01-terreno-capital', conceito='Vídeo 01 Terreno Capital v-captação (hook preservado; sem o áudio original)', formato='vídeo 9:16, 46 s, mudo com texto na tela (ou regravado por Bruno com o roteiro)',
  hook='Você aí, dono de terreno.',
  primeira='Cadastro gratuito · Terreno parado há tanto tempo? Comece estruturando, não construindo.',
  corpo=['Você não precisa começar construindo um hotel. Aprenda a estruturar antes de construir: território, mercado, orçamento e Dossiê. Cadastre-se de graça e receba conteúdos para dar os primeiros passos.',
         'O cadastro é gratuito e não obriga a nenhuma compra. ' + COMUM, CLARO],
  titulo='Terreno parado? Comece estruturando', descricao='Formação paga a partir de R$47',
  arquivos=['(fora do repositório) scratchpad/cap/video/capt-v01-terreno-capital-sem-audio.mp4'], urls=[None]),
]
man=[]
for p in P:
    texto='\n\n'.join([p['primeira']]+p['corpo'])
    assert len(p['titulo'])<=40 and len(p['descricao'])<=30,(p['id'],len(p['titulo']),len(p['descricao']))
    man.append(dict(id=p['id'],conceito=p['conceito'],formato=p['formato'],hook=p['hook'],texto_principal=texto,titulo=p['titulo'],descricao=p['descricao'],
      arquivos=[dict(arquivo=a,url_publica_esperada=u) for a,u in zip(p['arquivos'],p['urls'])],
      cta_meta='Cadastre-se (SIGN_UP); alternativa: Saiba mais (LEARN_MORE)', tipo_destino='formulário nativo do Meta NOVO (texto em FORMULARIO_CAPTACAO_TEXTOS.md); formulários existentes não são editáveis',
      url_tags=TAGS.format(id=p['id']), cta_arte='Cadastro gratuito · Formação paga a partir de R$47',
      status='pronto para aprovação de Bruno; não enviado ao Meta; criar sempre pausado',
      compliance='Cadastro gratuito dito na arte/fala e no texto; formação paga e Mini Mentoria R$47 citadas; sem reunião, consultoria, avaliação do terreno, investimento, parceria ou renda; fotos reais sem pessoas'))
json.dump(man,open(os.path.join(R,'manifesto.json'),'w'),ensure_ascii=False,indent=1)
L=['# Copies · Captação corrigida (Caminho A) · cadastro gratuito + formação paga','',
 'Textos para os 3 criativos de captação (Carrossel C, Vídeo 02, Vídeo 01). Destino: formulário nativo do Meta NOVO (ver `zion-sales-engine/06-criativos/FORMULARIO_CAPTACAO_TEXTOS.md`). Botão: Cadastre-se (SIGN_UP). UTM: tags de URL coladas uma vez, `utm_campaign=captacao`. Nada foi enviado ao Meta; criar sempre pausado e ativar só com "aprovado" de Bruno.','']
for p,m in zip(P,man):
    L+=[f'## {p["id"]} · {p["conceito"]}','',f'- **Título (até 40):** {p["titulo"]} ({len(p["titulo"])})',f'- **Descrição (até 30):** {p["descricao"]} ({len(p["descricao"])})','- **Botão:** Cadastre-se',f'- **Tags de URL:** `{m["url_tags"]}`','','**Texto principal:**','',*['> '+x if x else '>' for x in m['texto_principal'].split('\n')],'']
open(os.path.join(R,'COPIES.md'),'w').write('\n'.join(L)+'\n')
print('manifesto e COPIES gerados:',[p['id'] for p in P])
