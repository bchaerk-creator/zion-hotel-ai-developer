# Troca só a foto dos cartões 4 (o6) e 7 (o7) do Carrossel C original: o original tem mulher na foto
# (pessoa não autorizada como cliente/equipe). Mantém a meia-lua branca e a estrela do original
# (extraídas por máscara de branco puro) e a posição/recorte da foto. Uso: python3 -I troca_fotos.py SRC OUT
import sys, os
from PIL import Image
import numpy as np
SRC, OUT = sys.argv[1], sys.argv[2]
ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../assets'))
os.makedirs(OUT, exist_ok=True)

def cover(im, w, h, cx=.5, cy=.5):
    s = max(w/im.width, h/im.height)
    im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    x = round((im.width-w)*cx); y = round((im.height-h)*cy)
    return im.crop((x, y, x+w, y+h))

def troca(orig, foto, box, swirl_box, saida, cx=.5, cy=.5):
    o = Image.open(f'{SRC}/{orig}.png').convert('RGB')
    base = np.array(o).astype(float)
    x0, y0, x1, y1 = box
    new = np.array(cover(Image.open(f'{ASSETS}/{foto}').convert('RGB'), x1-x0, y1-y0, cx, cy)).astype(float)
    res = base.copy(); res[y0:y1, x0:x1] = new
    sx0, sy0, sx1, sy1 = swirl_box
    m = base[sy0:sy1, sx0:sx1].min(axis=2)
    a = np.clip((m-238)/(252-238), 0, 1)[..., None]
    reg = res[sy0:sy1, sx0:sx1]
    res[sy0:sy1, sx0:sx1] = reg*(1-a) + 255*a
    Image.fromarray(res.clip(0, 255).astype('uint8')).save(f'{OUT}/{saida}.png')

# cartão 4: foto de cima (0..795), meia-lua e estrela do original preservadas
troca('o6', 'store/dentro.webp', (0, 0, 1080, 795), (0, 240, 480, 1110), 'o6')
# cartão 7: foto da direita (x 572..1080), meia-lua do pé preservada
troca('o7', 'store/hero.webp', (572, 0, 1080, 1350), (370, 1020, 740, 1350), 'o7', cx=.3, cy=.55)
# cartão extra (gancho da plataforma Zion): mesmo layout do cartão 4 com outra foto real sem pessoas
troca('o6', 'store/deck.webp', (0, 0, 1080, 795), (0, 240, 480, 1110), 'o8')
print('ok')
