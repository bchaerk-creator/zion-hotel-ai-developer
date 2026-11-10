"""Insere a galeria de vídeos (Conheça a Zion + 5 objeções) na página do Club, e o vídeo Conheça a Zion nas páginas Store, Investidores e Fundador."""
import pathlib
D = pathlib.Path('/home/user/zion-hotel-ai-developer/docs')
BASE = '../trilha1/trailer/'
VIDS = [
    ('video-zion', 'capa-zion', 'Conheça a Zion', 'Operações reais, o fundador, o método e a expansão.'),
    ('video-dor-parada', 'capa-dor-parada', 'Terra parada', 'As três travas e por que a terra para por falta de projeto.'),
    ('video-dor-capital', 'capa-dor-capital', 'Falta o capital', 'Ninguém coloca dinheiro num terreno. Coloca num projeto.'),
    ('video-dor-parceiro', 'capa-dor-parceiro', 'Quero um parceiro', 'Parceiro aparece para dividir papéis, não uma ideia.'),
    ('video-dor-medo', 'capa-dor-medo', 'Medo de errar', 'O erro caro acontece antes da obra.'),
    ('video-dor-comecar', 'capa-dor-comecar', 'Por onde começar', 'Não é falta de informação. É falta de sequência.'),
]
def video(v, c, w='100%'):
    return (f'<video controls playsinline preload="none" poster="{BASE}{c}.jpg" style="display:block;width:{w};aspect-ratio:9/16;border-radius:18px;background:#040605;box-shadow:0 24px 48px rgba(0,0,0,.35)">'
            f'<source src="{BASE}{v}.mp4" type="video/mp4"></video>')

def galeria_club():
    cards = ''.join(f'<div><div style="margin-bottom:12px"><b style="display:block;font-size:17px">{t}</b><span style="font-size:14px;opacity:.75">{s}</span></div>{video(v,c)}</div>' for v, c, t, s in VIDS)
    return f'''<!-- GALERIA DE VIDEOS -->
<section class="dark" id="videos">
  <div class="wrap">
    <p class="eyebrow">Para ver com calma</p>
    <h2>Quem somos e <em>as perguntas que mais ouvimos.</em></h2>
    <p class="lead soft">Seis vídeos curtos: a Zion por dentro, e uma resposta para cada objeção que chega nos formulários: terra parada, capital, parceiro, medo de errar e por onde começar.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:28px;margin-top:40px">{cards}</div>
    <p class="note soft" style="margin-top:28px">Conteúdo educacional. Não é oferta de investimento nem promessa de renda, retorno, crédito ou sociedade. A Zion avalia cada caso.</p>
  </div>
</section>

'''
def bloco_zion(k_cls, h_html, lead_cls, wrap_cls, sec_cls, anchor='conheca-a-zion'):
    return f'''<!-- CONHECA A ZION -->
<section class="{sec_cls}" id="{anchor}">
  <div class="{wrap_cls}" style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,64px);align-items:center;padding:clamp(56px,8vw,96px) 0">
    <div>
      <div class="{k_cls}">Conheça a Zion</div>
      <h2>{h_html}</h2>
      <p class="{lead_cls}">Vários glampings operados, os dois pioneiros do Brasil e mais de 23 destinos em desenvolvimento, o fundador com 20 anos de hotelaria internacional e o método: o que está do outro lado antes de você confiar o seu terreno a alguém.</p>
      <p class="{lead_cls}" style="font-size:13px;margin-top:14px;opacity:.75">Instagram: @zionbubble · @zionglampingcollection · @brunochaerkofc</p>
    </div>
    <div style="justify-self:center;width:min(100%,360px)">{video('video-zion','capa-zion')}</div>
  </div>
</section>
<style>@media (max-width:760px){{#{anchor} .{wrap_cls}{{grid-template-columns:1fr !important}}}}</style>

'''
# 1. Club
p = D/'land-members/index.html'; s = p.read_text(encoding='utf-8')
m = '<!-- AO SE INSCREVER -->'
if 'id="videos"' not in s:
    s = s.replace(m, galeria_club()+m, 1); p.write_text(s, encoding='utf-8'); print('club ok')
# 2. Store e Investidores: depois da seção do trailer
for page in ['store', 'investidores']:
    p = D/page/'index.html'; s = p.read_text(encoding='utf-8')
    if 'id="conheca-a-zion"' in s: continue
    i = s.index('<!-- TRAILER -->'); j = s.index('</section>', i)+len('</section>')
    j = s.index('\n', s.index('</style>', j))+1
    s = s[:j]+'\n'+bloco_zion('k', 'Quem está <em>do outro lado.</em>', 'lead', 'w', 'g')+s[j:]
    p.write_text(s, encoding='utf-8'); print(page, 'ok')
# 3. Fundador: antes da trajetória
p = D/'fundador/index.html'; s = p.read_text(encoding='utf-8')
if 'id="conheca-a-zion"' not in s:
    m = '<section class="g" id="trajetoria">'
    s = s.replace(m, bloco_zion('k', 'A Zion em <em>2 minutos.</em>', 'lead', 'w', 'g')+m, 1)
    p.write_text(s, encoding='utf-8'); print('fundador ok')
