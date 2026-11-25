#!/usr/bin/env python3
"""Monta o HTML de cada pagina com o bloco de entregaveis a partir do backup (HTML no ar antes da mudanca).
Saidas em /tmp/.../scratchpad/entregaveis/novo-<slug>.html. Uso: python3 -I aplicar_bloco.py <saida_dir>"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build_bloco import bloco, CSS as BCSS
AQUI = Path(__file__).parent
saida = Path(sys.argv[1])

def limpar_body(h):
    b = h[h.find('<body') :]
    b = b[b.find('>') + 1 :]
    b = re.sub(r'<script.*?</script>', '', b, flags=re.S)
    b = b.replace('</body></html>', '').replace('</body>', '').replace('</html>', '')
    b = re.sub(r'\s(data-style-guide-[a-z-]+|data-text-color|shadow-[a-z-]+)="[^"]*"', '', b)
    b = re.sub(r'<div class="cm-checkout">.*?</iframe></div>', '<div data-cx-checkout></div>', b, flags=re.S)
    b = re.sub(r'<div[^>]*class="cm-checkout"[^>]*>.*?</iframe></div>', '<div data-cx-checkout></div>', b, flags=re.S)
    return b

def css_autor(css):
    i = css.find('*{box-sizing:border-box}html{scroll-behavior')
    j = css.find('}sub{vertical-align:baseline}')
    c = css[i:j + 1].replace('html html body', 'html body').replace('border-image:;', '')
    return re.sub(r'\(width>=(\d+)px\)', r'(min-width:\1px)', c)

def doc(title, desc, css, body):
    return ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">\n'
            f'<style>{css}{BCSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')

def inserir(body, depois_de_id, sec):
    m = re.search(r'<section[^>]*id="%s"[^>]*>.*?</section>' % depois_de_id, body, flags=re.S)
    assert m, depois_de_id
    return body[:m.end()] + sec + body[m.end():]

SEC = bloco(css=False)
for slug, css_file, antes_id, title in [
    ('inscricao-47', 'inscricao-47-antes.css', 'metodo', 'Zion Collection | Inscricao R$ 47'),
    ('inscricao-curta', 'inscricao-curta-antes.css', 'metodo', 'Zion Collection Club | Faça a sua inscrição'),
]:
    html = (AQUI / 'backup' / f'{slug}-antes.html').read_text(encoding='utf-8')
    body = inserir(limpar_body(html), antes_id, SEC)
    css = css_autor((AQUI / 'backup' / css_file).read_text(encoding='utf-8'))
    (saida / f'novo-{slug}.html').write_text(doc(title, 'Acesso à plataforma Zion Collection, pagamento único.', css, body), encoding='utf-8')
# parceiro-zion: gerador do repositorio (lt47/build.py), conferido contra o no ar
lt = (AQUI.parent / 'lt47' / 'index.html').read_text(encoding='utf-8')
m = re.search(r'<style>(.*?)</style>', lt, flags=re.S)
body = lt[lt.find('<body>') + 6 : lt.find('</body>')]
body = inserir(body, 'zzz', '') if False else body
# a secao 'offer' (Veja a plataforma por dentro) e a 4a secao
secs = list(re.finditer(r'<section data-cx-section="offer".*?</section>', body, flags=re.S))
assert len(secs) == 1
k = secs[0].end()
body = body[:k] + SEC + body[k:]
t = re.search(r'<title>(.*?)</title>', lt).group(1)
d = re.search(r'<meta name="description" content="(.*?)">', lt).group(1)
(saida / 'novo-parceiro-zion.html').write_text(doc(t, d, m.group(1), body), encoding='utf-8')
print('ok')
