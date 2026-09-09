# -*- coding: utf-8 -*-
"""
Gerador determinístico dos detalhes construtivos (SVG) da ZION GLAMPING COLLECTION.
Produtos: ZION COCOON e ZION ZENITH. Fonte de dados: ESPECIFICACAO_TECNICA.md.

Uso:  python3 tools/details.py            (escreve os SVG em ../detalhes/)
Dependências: biblioteca padrão + numpy.
"""
import math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "detalhes"))

W, H = 1600, 1000
BG = "#FEF5F0"
INK = "#1B2117"
GOLD = "#8B714E"
GLASS = "#C9D3D6"
PAPER2 = "#F6EAE2"
FONT = "DM Sans, Helvetica, Arial, sans-serif"
DATE = "SET 2026"

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


class Tr:
    """Transformação mm -> px. Origem (ox, oy) em px; y cresce para cima em mm."""
    def __init__(self, ox, oy, k):
        self.ox, self.oy, self.k = ox, oy, k
    def x(self, mm):
        return self.ox + mm * self.k
    def y(self, mm):
        return self.oy - mm * self.k
    def p(self, xmm, ymm):
        return (self.x(xmm), self.y(ymm))
    def d(self, mm):
        return mm * self.k


class Sheet:
    def __init__(self, num, title, unit, scale, subtitle=""):
        self.num, self.title, self.unit, self.scale, self.subtitle = num, title, unit, scale, subtitle
        self.body = []
        self.clip_id = 0

    # ---------------- primitivas ----------------
    def add(self, s):
        self.body.append(s)

    def line(self, x1, y1, x2, y2, w=0.9, color=INK, dash=None, cap="butt", opacity=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        o = ' opacity="%s"' % opacity if opacity else ""
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="%s"%s%s/>'
                 % (x1, y1, x2, y2, color, w, cap, d, o))

    def pl(self, pts, w=0.9, color=INK, fill="none", close=False, dash=None, join="round", opacity=None, cap="butt"):
        s = " ".join("%.1f,%.1f" % (p[0], p[1]) for p in pts)
        tag = "polygon" if close else "polyline"
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        o = ' opacity="%s"' % opacity if opacity else ""
        self.add('<%s points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="%s" stroke-linecap="%s"%s%s/>'
                 % (tag, s, fill, color, w, join, cap, d, o))

    def path(self, d, w=0.9, color=INK, fill="none", dash=None, opacity=None, cap="butt"):
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        o = ' opacity="%s"' % opacity if opacity else ""
        self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="%s"%s%s/>'
                 % (d, fill, color, w, cap, da, o))

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=0.9, rx=0, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="%s" rx="%s"%s/>'
                 % (x, y, w, h, fill, stroke, sw, rx, d))

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=0.9, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'
                 % (cx, cy, r, fill, stroke, sw, d))

    def ellipse(self, cx, cy, rx, ry, fill="none", stroke=INK, sw=0.9, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'
                 % (cx, cy, rx, ry, fill, stroke, sw, d))

    def text(self, x, y, s, size=13, anchor="start", color=INK, weight=None, italic=False,
             rotate=None, ls=None, caps=False, family=None):
        st = "font-size:%spx;" % size
        if weight: st += "font-weight:%s;" % weight
        if italic: st += "font-style:italic;"
        if ls: st += "letter-spacing:%s;" % ls
        if caps: st += "text-transform:uppercase;"
        tr = ' transform="rotate(%s %.1f %.1f)"' % (rotate, x, y) if rotate is not None else ""
        self.add('<text x="%.1f" y="%.1f" text-anchor="%s" fill="%s" style="%s"%s>%s</text>'
                 % (x, y, anchor, color, st, tr, esc(s)))

    def texts(self, x, y, lines, size=13, lh=None, color=INK, anchor="start", weight=None):
        lh = lh or size * 1.45
        for i, s in enumerate(lines):
            self.text(x, y + i * lh, s, size=size, color=color, anchor=anchor, weight=weight)

    # ---------------- elementos de desenho técnico ----------------
    def tick(self, x, y, color=GOLD):
        self.line(x - 4, y + 4, x + 4, y - 4, 0.9, color)

    def dim_h(self, x1, x2, y, label, ext=None, above=True, color=GOLD, size=13):
        """Cota horizontal entre x1 e x2 na altura y. ext = y de origem das linhas de chamada."""
        if ext is not None:
            for x in (x1, x2):
                self.line(x, ext, x, y + (4 if ext < y else -4), 0.5, color)
        self.line(x1 - 5, y, x2 + 5, y, 0.8, color)
        self.tick(x1, y, color); self.tick(x2, y, color)
        ty = y - 5 if above else y + size + 2
        self.text((x1 + x2) / 2, ty, label, size=size, anchor="middle", color=color)

    def dim_v(self, x, y1, y2, label, ext=None, left=True, color=GOLD, size=13):
        if ext is not None:
            for y in (y1, y2):
                self.line(ext, y, x + (4 if ext < x else -4), y, 0.5, color)
        self.line(x, min(y1, y2) - 5, x, max(y1, y2) + 5, 0.8, color)
        self.tick(x, y1, color); self.tick(x, y2, color)
        tx = x - 5 if left else x + 5 + size
        self.text(tx, (y1 + y2) / 2, label, size=size, anchor="middle", color=color, rotate=-90)

    def dim_a(self, x1, y1, x2, y2, label, off=18, color=GOLD, size=13):
        """Cota alinhada, deslocada 'off' px para a esquerda do vetor."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * off, dx / L * off
        ax, ay, bx, by = x1 + nx, y1 + ny, x2 + nx, y2 + ny
        self.line(x1, y1, ax + nx * 0.25, ay + ny * 0.25, 0.5, color)
        self.line(x2, y2, bx + nx * 0.25, by + ny * 0.25, 0.5, color)
        self.line(ax, ay, bx, by, 0.8, color)
        ang = math.degrees(math.atan2(dy, dx))
        for (px, py) in ((ax, ay), (bx, by)):
            self.add('<line x1="-4" y1="4" x2="4" y2="-4" stroke="%s" stroke-width="0.9" transform="translate(%.1f %.1f) rotate(%.1f)"/>'
                     % (color, px, py, ang))
        mx, my = (ax + bx) / 2 - ny / off * 5, (ay + by) / 2 + nx / off * 5
        rot = ang if -90 <= ang <= 90 else ang + 180
        self.text(mx, my, label, size=size, anchor="middle", color=color, rotate=rot)

    def arrow(self, x1, y1, x2, y2, w=1.0, color=GOLD, head=7, dash=None, both=False):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, color, w, d))
        self.head(x1, y1, x2, y2, color, head)
        if both:
            self.head(x2, y2, x1, y1, color, head)

    def head(self, x1, y1, x2, y2, color=GOLD, size=7):
        ang = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - size * math.cos(ang - 0.4), y2 - size * math.sin(ang - 0.4))
        p2 = (x2 - size * math.cos(ang + 0.4), y2 - size * math.sin(ang + 0.4))
        self.add('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="none"/>'
                 % (x2, y2, p1[0], p1[1], p2[0], p2[1], color))

    def callout(self, n, x, y, tx, ty, r=10):
        """Balão numerado em (tx,ty) com linha de chamada até (x,y)."""
        dx, dy = x - tx, y - ty
        L = math.hypot(dx, dy) or 1
        sx, sy = tx + dx / L * r, ty + dy / L * r
        self.line(sx, sy, x, y, 0.8, GOLD)
        self.circle(x, y, 1.8, fill=GOLD, stroke="none")
        self.circle(tx, ty, r, fill=BG, stroke=GOLD, sw=0.9)
        self.text(tx, ty + 4, str(n), size=11, anchor="middle", color=INK, weight=600)

    def label(self, x, y, tx, ty, s, size=12, color=INK, anchor=None):
        """Texto com linha de chamada (sem número)."""
        self.line(tx, ty, x, y, 0.8, GOLD)
        self.circle(x, y, 1.8, fill=GOLD, stroke="none")
        a = anchor or ("start" if tx >= x else "end")
        ox = 4 if a == "start" else -4
        self.text(tx + ox, ty + 4, s, size=size, anchor=a, color=color)

    def legend(self, x, y, items, cols=1, colw=440, lh=20, size=12.5, title="LEGENDA"):
        if title:
            self.text(x, y, title, size=11, color=GOLD, ls="0.2em", weight=600)
            y += 22
        per = math.ceil(len(items) / cols)
        for i, (n, s) in enumerate(items):
            cx = x + (i // per) * colw
            cy = y + (i % per) * lh
            self.circle(cx + 9, cy - 4, 9, fill=BG, stroke=GOLD, sw=0.9)
            self.text(cx + 9, cy - 0.5, str(n), size=10.5, anchor="middle", weight=600)
            self.text(cx + 26, cy, s, size=size)
        return y + per * lh

    def panel(self, x, y, w, h, title, sub=None):
        self.rect(x, y, w, h, fill="none", stroke=GOLD, sw=0.6)
        self.rect(x, y, w, 26, fill=PAPER2, stroke=GOLD, sw=0.6)
        self.text(x + 12, y + 18, title, size=12.5, weight=600, ls="0.12em", caps=True)
        if sub:
            self.text(x + w - 12, y + 18, sub, size=11, anchor="end", color=GOLD)

    def note(self, x, y, lines, size=12, w=None):
        if w:
            self.rect(x - 10, y - size - 4, w, size * 1.45 * len(lines) + 12, fill=PAPER2, stroke=GOLD, sw=0.6)
        self.texts(x, y, lines, size=size)

    def table(self, x, y, cols, rows, widths, size=12, lh=20, head=True):
        tot = sum(widths)
        cy = y
        if head:
            self.rect(x, cy - lh + 6, tot, lh, fill=PAPER2, stroke=GOLD, sw=0.6)
            cx = x
            for c, wdt in zip(cols, widths):
                self.text(cx + 6, cy, c, size=size - 1, weight=600, color=GOLD)
                cx += wdt
            cy += lh
        for r in rows:
            cx = x
            for c, wdt in zip(r, widths):
                self.text(cx + 6, cy, c, size=size)
                cx += wdt
            self.line(x, cy + 6, x + tot, cy + 6, 0.4, GOLD)
            cy += lh
        self.line(x, y - lh + 6, x, cy - lh + 6, 0.6, GOLD)
        self.line(x + tot, y - lh + 6, x + tot, cy - lh + 6, 0.6, GOLD)
        return cy

    # ---------------- hachuras / materiais ----------------
    def steel(self, x, y, w, h):
        self.rect(x, y, w, h, fill=INK, stroke=INK, sw=0.6)

    def steel_poly(self, pts):
        self.pl(pts, 0.8, INK, fill=INK, close=True)

    def wood(self, x, y, w, h, grain=True):
        self.rect(x, y, w, h, fill="url(#p-wood)", stroke=INK, sw=1.6)
        if grain and w > 30 and h > 8:
            n = max(1, int(h / 14))
            for i in range(n):
                yy = y + h * (i + 0.5) / n
                self.path("M%.1f,%.1f q%.1f,%.1f %.1f,0 t%.1f,0" % (x + 4, yy, w * 0.25, 3, w * 0.5, w * 0.46 - 8), 0.5, INK)

    def ins(self, x, y, w, h, pat="p-ins"):
        self.rect(x, y, w, h, fill="url(#%s)" % pat, stroke=INK, sw=0.9)

    def soil(self, x, y, w, h):
        self.rect(x, y, w, h, fill="url(#p-dots)", stroke="none")

    def glass(self, x1, y1, x2, y2, t=6):
        """Vidro: par de linhas finas com preenchimento azul-cinza pálido."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * t / 2, dx / L * t / 2
        pts = [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]
        self.pl(pts, 0.6, "#8A9DA3", fill=GLASS, close=True)

    def membrane(self, pts, w=3):
        self.pl(pts, w, GOLD, cap="round")

    def tube_cut(self, cx, cy, ro, t):
        """Tubo cortado (seção transversal): coroa em preto."""
        self.circle(cx, cy, ro, fill=INK, stroke=INK, sw=0.6)
        self.circle(cx, cy, ro - t, fill=BG, stroke=INK, sw=0.6)

    def tube_seen(self, x1, y1, x2, y2, d, w=0.9, fill=BG):
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * d / 2, dx / L * d / 2
        pts = [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]
        self.pl(pts, w, INK, fill=fill, close=True)
        # linha de eixo
        self.line(x1, y1, x2, y2, 0.4, INK, dash="8 3 1.5 3")

    def bolt_side(self, x, y, L, d, vertical=True, color=INK):
        """Parafuso visto de lado (cabeça + haste + porca)."""
        if vertical:
            self.rect(x - d * 0.9, y - d * 0.7, d * 1.8, d * 0.7, fill=INK, stroke="none")
            self.rect(x - d / 2, y, d, L, fill=BG, stroke=INK, sw=0.8)
            self.rect(x - d * 0.9, y + L - d * 0.8, d * 1.8, d * 0.8, fill=INK, stroke="none")
        else:
            self.rect(x - d * 0.7, y - d * 0.9, d * 0.7, d * 1.8, fill=INK, stroke="none")
            self.rect(x, y - d / 2, L, d, fill=BG, stroke=INK, sw=0.8)
            self.rect(x + L - d * 0.8, y - d * 0.9, d * 0.8, d * 1.8, fill=INK, stroke="none")

    def bolt_top(self, x, y, r):
        self.circle(x, y, r, fill=BG, stroke=INK, sw=0.9)
        self.circle(x, y, r * 0.45, fill=INK, stroke="none")

    def cable(self, x1, y1, x2, y2, w=1.6):
        self.line(x1, y1, x2, y2, w, INK)
        self.line(x1, y1, x2, y2, 0.5, BG, dash="3 4")

    def turnbuckle(self, x, y, ang, L=26, h=9):
        self.add('<g transform="translate(%.1f %.1f) rotate(%.1f)">' % (x, y, ang))
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="0.9" rx="2"/>' % (-L / 2, -h / 2, L, h, BG, INK))
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="none"/>' % (-L * 0.15, -h / 2, L * 0.3, h, INK))
        self.add('</g>')

    def break_line(self, x1, y1, x2, y2, amp=5):
        """Linha de interrupção em zigue-zague."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        ux, uy, nx, ny = dx / L, dy / L, -dy / L, dx / L
        n = max(2, int(L / 6))
        pts = []
        for i in range(n + 1):
            t = i / n
            s = amp * (1 if i % 2 else -1) if 0 < i < n else 0
            pts.append((x1 + ux * L * t + nx * s, y1 + uy * L * t + ny * s))
        self.pl(pts, 0.9, INK, fill=BG)

    def scale_bar(self, x, y, k, mm, label):
        """Escala gráfica: k px/mm, comprimento mm."""
        n = 4
        seg = k * mm / n
        for i in range(n):
            self.rect(x + i * seg, y, seg, 5, fill=(INK if i % 2 == 0 else BG), stroke=INK, sw=0.6)
        self.text(x, y - 4, "0", size=10, anchor="middle", color=GOLD)
        self.text(x + k * mm, y - 4, label, size=10, anchor="middle", color=GOLD)

    def north(self, x, y):
        self.circle(x, y, 14, stroke=GOLD, sw=0.8)
        self.pl([(x, y - 12), (x + 5, y + 6), (x, y + 2), (x - 5, y + 6)], 0.8, GOLD, fill=GOLD, close=True)
        self.text(x, y - 18, "N", size=11, anchor="middle", color=GOLD, weight=600)

    # ---------------- folha ----------------
    def header(self):
        self.rect(30, 30, W - 60, H - 60, fill="none", stroke=INK, sw=0.9)
        self.text(60, 78, self.title, size=20, ls="0.25em", caps=True, weight=600)
        if self.subtitle:
            self.text(60, 100, self.subtitle, size=13, color=GOLD)
        self.text(W - 60, 70, "ZION GLAMPING COLLECTION", size=11, anchor="end", color=GOLD, ls="0.25em", weight=600)
        self.text(W - 60, 90, "%s   |   %s" % (self.unit, self.num), size=12, anchor="end", color=INK, ls="0.1em")

    def title_block(self):
        x, y, w, h = W - 40 - 520, H - 40 - 90, 520, 90
        self.rect(x, y, w, h, fill=BG, stroke=INK, sw=1.2)
        self.line(x + 300, y, x + 300, y + h, 0.9, INK)
        self.line(x + 300, y + 45, x + w, y + 45, 0.9, INK)
        self.line(x + 410, y + 45, x + 410, y + h, 0.9, INK)
        self.add('<text x="%.1f" y="%.1f" fill="%s" style="font-size:12px;letter-spacing:0.22em;font-weight:600;font-variant:small-caps">Zion Glamping Collection</text>' % (x + 14, y + 24, GOLD))
        self.text(x + 14, y + 50, self.title, size=14, weight=600, caps=True)
        self.text(x + 14, y + 74, self.unit, size=11.5, color=GOLD, ls="0.15em")
        self.text(x + 312, y + 16, "ESCALA", size=9, color=GOLD, ls="0.15em")
        self.text(x + 312, y + 36, self.scale, size=13)
        self.text(x + 312, y + 61, "FOLHA", size=9, color=GOLD, ls="0.15em")
        self.text(x + 312, y + 84, self.num, size=20, weight=600)
        self.text(x + 422, y + 61, "DATA", size=9, color=GOLD, ls="0.15em")
        self.text(x + 422, y + 84, DATE, size=13)

    def defs(self):
        return """<defs>
<pattern id="p-wood" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="8" stroke="%(ink)s" stroke-width="0.5"/></pattern>
<pattern id="p-steel" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="4" stroke="%(ink)s" stroke-width="1.1"/></pattern>
<pattern id="p-ins" width="14" height="10" patternUnits="userSpaceOnUse">
  <path d="M0,5 L3.5,1 L7,5 L10.5,9 L14,5" fill="none" stroke="%(ink)s" stroke-width="0.6"/></pattern>
<pattern id="p-pir" width="9" height="7" patternUnits="userSpaceOnUse">
  <path d="M0,3.5 L2.25,0.8 L4.5,3.5 L6.75,6.2 L9,3.5" fill="none" stroke="%(ink)s" stroke-width="0.5"/></pattern>
<pattern id="p-dots" width="12" height="12" patternUnits="userSpaceOnUse">
  <circle cx="2" cy="3" r="0.8" fill="%(ink)s"/><circle cx="8" cy="7" r="0.8" fill="%(ink)s"/>
  <circle cx="5" cy="10" r="0.6" fill="%(ink)s"/><circle cx="10.5" cy="1.5" r="0.6" fill="%(ink)s"/></pattern>
<pattern id="p-gravel" width="14" height="14" patternUnits="userSpaceOnUse">
  <ellipse cx="3" cy="4" rx="2.2" ry="1.5" fill="none" stroke="%(ink)s" stroke-width="0.5"/>
  <ellipse cx="10" cy="9" rx="2.4" ry="1.6" fill="none" stroke="%(ink)s" stroke-width="0.5" transform="rotate(30 10 9)"/>
  <ellipse cx="11" cy="2" rx="1.6" ry="1.1" fill="none" stroke="%(ink)s" stroke-width="0.5"/></pattern>
<pattern id="p-osb" width="10" height="10" patternUnits="userSpaceOnUse">
  <line x1="1" y1="2" x2="4" y2="3" stroke="%(ink)s" stroke-width="0.6"/>
  <line x1="6" y1="7" x2="9" y2="5" stroke="%(ink)s" stroke-width="0.6"/>
  <line x1="2" y1="8" x2="4" y2="9" stroke="%(ink)s" stroke-width="0.6"/></pattern>
<pattern id="p-cem" width="6" height="6" patternUnits="userSpaceOnUse">
  <circle cx="1.5" cy="1.5" r="0.5" fill="%(ink)s"/><circle cx="4.5" cy="4" r="0.5" fill="%(ink)s"/></pattern>
<pattern id="p-ply" width="10" height="4" patternUnits="userSpaceOnUse">
  <line x1="0" y1="2" x2="10" y2="2" stroke="%(ink)s" stroke-width="0.35"/></pattern>
</defs>""" % dict(ink=INK)

    def svg(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
                'font-family="%s" fill="%s">\n' % (W, H, W, H, FONT, INK))
        bg = '<rect x="0" y="0" width="%d" height="%d" fill="%s"/>\n' % (W, H, BG)
        return head + self.defs() + "\n" + bg + "\n".join(self.body) + "\n</svg>\n"

    def write(self, name):
        self.header()
        self.title_block()
        os.makedirs(OUT, exist_ok=True)
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(self.svg())
        print("gravado", p)


# ==================================================================================
# Geometria de apoio (copiada da fonte paramétrica, tools/geometry.py)
# ==================================================================================
def sef(t, n):
    t = min(max(t, 0.0), 1.0)
    return (1.0 - t ** n) ** (1.0 / n)

class CocoonGeo:
    L = 9.0; XMAX = 3.2; AMAX = 2.95; N_FRONT = 4.0; N_REAR = 3.0; N_B = 2.0
    ZC = 0.75; B_FRONT = 3.10; B_MAX = 3.20; B_MIN = 0.35
    ARCH_X = [0.5, 1.7, 2.9, 4.1, 5.3, 6.5, 7.6, 8.5]
    ARCH_L = [10.4, 11.1, 11.2, 11.1, 10.8, 10.1, 8.8, 6.9]
    PURLIN_V = [0.10, 0.22, 0.34, 0.5, 0.66, 0.78, 0.90]

    def a(self, x):
        if x < self.XMAX:
            return self.AMAX * sef((self.XMAX - x) / self.XMAX, self.N_FRONT)
        return self.AMAX * sef((x - self.XMAX) / (self.L - self.XMAX), self.N_REAR)

    def b(self, x):
        if x < self.XMAX:
            t = (self.XMAX - x) / self.XMAX
            return self.B_FRONT + (self.B_MAX - self.B_FRONT) * (1 - t ** 2)
        t = (x - self.XMAX) / (self.L - self.XMAX)
        return self.B_MIN + (self.B_MAX - self.B_MIN) * sef(t, self.N_B)

    def top(self, x):
        return self.ZC + self.b(x)

    def floor_hw(self, x):
        a, b = self.a(x), self.b(x)
        if b <= self.ZC or a <= 0:
            return 0.0
        return a * math.sqrt(max(0.0, 1 - (self.ZC / b) ** 2))

    def arch_pts(self, x, n=80):
        """Pontos (y, z) do arco na seção x, do pé esquerdo ao pé direito."""
        a, b = self.a(x), self.b(x)
        if b <= self.ZC:
            return []
        phi0 = math.asin(-self.ZC / b)
        pts = []
        for i in range(n + 1):
            phi = math.pi - phi0 - (math.pi - 2 * phi0) * i / n
            pts.append((a * math.cos(phi), self.ZC + b * math.sin(phi)))
        return pts

COC = CocoonGeo()

# ---------- plantas simplificadas (usadas em DET-06 a DET-09) ----------
def cocoon_plan(sh, ox, oy, k, rooms=True, deck=True, furniture=True, labels=True):
    """Planta do Cocoon: origem em (x=0, y=0) do projeto; k px/m; x para a direita, y para cima."""
    X = lambda xm: ox + xm * k
    Y = lambda ym: oy - ym * k
    # contorno máximo (z = 0,75) e contorno do piso
    xs = np.linspace(0.0, 9.0, 120)
    outer = [(X(x), Y(COC.a(x))) for x in xs] + [(X(x), Y(-COC.a(x))) for x in xs[::-1]]
    sh.pl(outer, 1.6, INK, fill="none", close=True)
    flo = [(X(x), Y(COC.floor_hw(x))) for x in xs] + [(X(x), Y(-COC.floor_hw(x))) for x in xs[::-1]]
    sh.pl(flo, 0.7, INK, fill="none", close=True, dash="5 3")
    # lábio frontal (anel A0 inclinado, topo avança 0,55)
    a0 = COC.a(0.5)
    sh.pl([(X(0.5), Y(a0)), (X(-0.05), Y(a0 * 0.75)), (X(-0.05), Y(-a0 * 0.75)), (X(0.5), Y(-a0))], 0.9, INK, dash="3 2")
    if deck:
        sh.rect(X(-3.0), Y(3.25), 4.0 * k, 6.5 * k, fill="none", stroke=INK, sw=0.9)
        for i in range(1, 27):
            yy = Y(3.25) + i * 6.5 * k / 27
            sh.line(X(-3.0), yy, X(1.0), yy, 0.3, INK)
    # fachada de vidro em x = 1,0 e parede do banho em x = 6,2
    sh.line(X(1.0), Y(COC.floor_hw(1.0)), X(1.0), Y(-COC.floor_hw(1.0)), 2.2, "#8A9DA3")
    if rooms:
        hw = COC.floor_hw(6.2)
        sh.rect(X(6.2), Y(hw), 0.12 * k, 2 * hw * k, fill=INK, stroke="none")
        sh.rect(X(6.2), Y(-hw + 0.3), 0.12 * k, 0.8 * k, fill=BG, stroke="none")   # passagem
    if furniture:
        sh.rect(X(4.17), Y(0.965), 2.03 * k, 1.93 * k, fill="none", stroke=INK, sw=0.5)      # cama king
        sh.line(X(4.17), Y(0.965), X(4.17 + 0.5), Y(-0.965), 0.4, INK)
        sh.rect(X(1.6), Y(-1.2), 1.6 * k, 0.8 * k, fill="none", stroke=INK, sw=0.5)          # chaise
        sh.rect(X(2.2), Y(2.3), 1.4 * k, 0.6 * k, fill="none", stroke=INK, sw=0.5)           # console
        sh.rect(X(7.2), Y(1.3), 1.55 * k, 0.76 * k, fill="none", stroke=INK, sw=0.5, rx=6)   # banheira
        sh.rect(X(6.4), Y(-0.6), 0.95 * k, 0.95 * k, fill="none", stroke=INK, sw=0.5)        # chuveiro
        sh.rect(X(6.4), Y(1.35), 1.5 * k, 0.55 * k, fill="none", stroke=INK, sw=0.5)         # bancada
        sh.ellipse(X(8.0), Y(-0.5), 0.2 * k, 0.28 * k, stroke=INK, sw=0.5)                    # bacia
    if labels:
        sh.text(X(2.4), Y(-2.3), "ESTAR", size=9, anchor="middle", color=GOLD, ls="0.15em")
        sh.text(X(5.1), Y(-2.1), "SUÍTE", size=9, anchor="middle", color=GOLD, ls="0.15em")
        sh.text(X(7.5), Y(-1.9), "BANHO", size=9, anchor="middle", color=GOLD, ls="0.15em")
        if deck:
            sh.text(X(-1.0), Y(0), "DECK", size=9, anchor="middle", color=GOLD, ls="0.15em")
    return X, Y


def zenith_plan(sh, ox, oy, k, roof=True, rooms=True, furniture=True, labels=True):
    X = lambda xm: ox + xm * k
    Y = lambda ym: oy - ym * k
    if roof:
        # contorno da cobertura com bordas em catenária entre postes
        posts = [(-2.4, -3.7), (-2.4, 3.7), (10.5, -3.7), (10.5, 3.7), (4.0, -3.7), (4.0, 3.7), (10.5, 0.0)]
        def cat(p, q, s, n=16):
            pts = []
            for i in range(n + 1):
                t = i / n
                x = p[0] + (q[0] - p[0]) * t; y = p[1] + (q[1] - p[1]) * t
                # flecha em planta para dentro (efeito visual da catenária)
                dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy)
                nx, ny = -dy / L, dx / L
                pts.append((x + nx * s * 4 * t * (1 - t), y + ny * s * 4 * t * (1 - t)))
            return pts
        seq = [(-2.4, -3.7), (4.0, -3.7), (10.5, -3.7), (10.5, 0.0), (10.5, 3.7), (4.0, 3.7), (-2.4, 3.7)]
        poly = []
        for i in range(len(seq)):
            p, q = seq[i], seq[(i + 1) % len(seq)]
            poly += [(X(a), Y(b)) for a, b in cat(p, q, 0.25)]
        sh.pl(poly, 1.2, INK, fill="none", close=True)
        for (px, py) in posts:
            sh.circle(X(px), Y(py), 3.5, fill=INK, stroke="none")
        # cumes
        sh.circle(X(6.3), Y(0.4), 0.6 * k, stroke=INK, sw=0.9)
        sh.circle(X(6.3), Y(0.4), 0.07 * k, fill=INK, stroke="none")
        sh.circle(X(1.6), Y(1.6), 0.35 * k, stroke=INK, sw=0.9)
        sh.circle(X(1.6), Y(1.6), 0.057 * k, fill=INK, stroke="none")
    # corpo, terraço e passarela
    sh.rect(X(0), Y(2.7), 9.5 * k, 5.4 * k, fill="none", stroke=INK, sw=1.6)
    sh.rect(X(0.1), Y(2.6), 9.3 * k, 5.2 * k, fill="none", stroke=INK, sw=0.6)
    sh.rect(X(-3.0), Y(3.4), 3.0 * k, 6.8 * k, fill="none", stroke=INK, sw=0.9)
    sh.rect(X(0.0), Y(3.5), 9.5 * k, 0.8 * k, fill="none", stroke=INK, sw=0.9)
    for i in range(1, 20):
        yy = Y(3.4) + i * 6.8 * k / 20
        sh.line(X(-3.0), yy, X(0), yy, 0.3, INK)
    sh.circle(X(-1.55), Y(-2.05), 0.95 * k, stroke=INK, sw=0.7)
    sh.circle(X(-1.55), Y(-2.05), 0.75 * k, stroke=INK, sw=0.4)
    # fachada frontal envidraçada
    sh.line(X(0.05), Y(2.6), X(0.05), Y(-2.6), 2.2, "#8A9DA3")
    if rooms:
        sh.rect(X(6.2), Y(2.6), 0.25 * k, 5.2 * k, fill=INK, stroke="none")
        sh.rect(X(6.2), Y(2.55), 0.25 * k, 1.1 * k, fill=BG, stroke="none")
        sh.line(X(3.55), Y(2.6), X(3.55), Y(-2.6), 0.5, INK, dash="4 3")
    if furniture:
        sh.rect(X(4.17), Y(0.965 + 0.4), 2.03 * k, 1.93 * k, fill="none", stroke=INK, sw=0.5)   # cama sob o óculo
        sh.rect(X(0.6), Y(0.2), 0.9 * k, 2.2 * k, fill="none", stroke=INK, sw=0.5)               # sofá
        sh.rect(X(1.4), Y(2.55), 2.0 * k, 0.72 * k, fill="none", stroke=INK, sw=0.5)             # ilha do café
        sh.rect(X(6.6), Y(2.5), 2.0 * k, 0.6 * k, fill="none", stroke=INK, sw=0.5)               # bancada dupla
        sh.rect(X(7.9), Y(-1.4), 1.2 * k, 1.1 * k, fill="none", stroke=INK, sw=0.5)              # chuveiro
        sh.rect(X(7.6), Y(2.5 - 1.0), 1.7 * k, 0.75 * k, fill="none", stroke=INK, sw=0.5, rx=6)  # banheira
        sh.ellipse(X(6.9), Y(-1.9), 0.2 * k, 0.28 * k, stroke=INK, sw=0.5)                       # bacia
    if labels:
        sh.text(X(1.8), Y(-2.0), "ESTAR", size=9, anchor="middle", color=GOLD, ls="0.15em")
        sh.text(X(4.9), Y(-2.0), "SUÍTE", size=9, anchor="middle", color=GOLD, ls="0.15em")
        sh.text(X(8.0), Y(0.2), "BANHO", size=9, anchor="middle", color=GOLD, ls="0.15em")
        sh.text(X(-1.5), Y(1.8), "TERRAÇO", size=9, anchor="middle", color=GOLD, ls="0.15em")
    return X, Y


# ==================================================================================
# DET-01  Seção do envelope do COCOON no arco
# ==================================================================================
def det01():
    sh = Sheet("DET-01", "Seção do envelope no arco", "ZION COCOON", "1:5 (1 mm = 1,4 px)",
               "Corte longitudinal (plano x-z) perpendicular ao arco A3. Camadas de fora (acima) para dentro (abaixo).")
    k = 1.4
    t = Tr(120, 250, k)          # y em mm cresce para cima; profundidade = -mm
    D = lambda mm: t.y(-mm)      # profundidade abaixo da face externa da membrana
    xc = 300                     # eixo do arco (mm)
    W_ = 560
    X = t.x
    sh.panel(60, 120, 880, 560, "Seção 1  -  envelope no arco (cortado) e entre arcos", "escala 1:5")

    # --- linha de eixo do arco
    sh.line(X(xc), D(-40), X(xc), D(230), 0.5, INK, dash="10 3 2 3")

    # --- forro (mais interno) : linha 2 px
    sh.line(X(0), D(196), X(W_), D(196), 2.2, INK)
    # trilho secundário 40 x 20 pendurado no talão
    sh.rect(X(xc - 20), D(175), 40 * k, 20 * k, fill=BG, stroke=INK, sw=1.6)
    sh.rect(X(xc - 20), D(190), 40 * k, 5 * k, fill=INK, stroke="none")
    # talão chapa 8 mm soldado ao arco (115 a 175)
    sh.rect(X(xc - 4), D(114), 8 * k, 61 * k, fill=INK, stroke="none")
    # --- terças Ø48,3 (vistas) : eixo a 139 mm, dos dois lados do talão
    for (x1, x2) in ((0, xc - 4), (xc + 4, W_)):
        sh.tube_seen(X(x1), D(139), X(x2), D(139), 48.3 * k, 0.9)
        # ponteira rosqueada: tampa + parafuso M16 no talão
        xe = x2 if x1 == 0 else x1
        sgn = -1 if x1 == 0 else 1
        sh.rect(X(xe + sgn * 0.5 - (0 if sgn < 0 else 0)) - (0 if sgn < 0 else 0) - (12 * k if sgn < 0 else 0), D(139) - 12 * k, 12 * k, 24 * k, fill=INK, stroke="none")
    sh.bolt_side(X(xc - 22), D(139), 44 * k, 8, vertical=False)
    # --- arco Ø88,9 x 3,6 (cortado)
    sh.tube_cut(X(xc), D(70.5), 44.45 * k, 3.6 * k)
    # --- isolamento entre arcos: manta refletiva 60-64, lã PET 64-114
    for (x1, x2) in ((0, xc - 48), (xc + 48, W_)):
        sh.rect(X(x1), D(60), (x2 - x1) * k, 4 * k, fill="url(#p-steel)", stroke=INK, sw=0.6)
        sh.ins(X(x1), D(64), (x2 - x1) * k, 50 * k)
    # junta de PET comprimida contra o arco
    for xj in (xc - 48, xc + 48):
        sh.path("M%.1f,%.1f q%.1f,%.1f 0,%.1f" % (X(xj), D(64), (6 if xj > xc else -6) * k, 25 * k, 50 * k), 0.9, INK)
    # --- câmara ventilada 60 mm com setas
    for xa in (60, 160, 440, 520):
        sh.arrow(X(xa), D(52), X(xa + 26), D(10), 0.8, GOLD, head=6)
    sh.text(X(110), D(35), "ar", size=10, color=GOLD, anchor="middle")
    sh.text(X(480), D(35), "ar", size=10, color=GOLD, anchor="middle")
    # --- presilha inox sobre o tubo + parafuso M8 no perfil keder
    sh.path("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (X(xc - 30), D(58), 33 * k, 33 * k, X(xc + 30), D(58)), 3.0, INK)
    sh.rect(X(xc - 30), D(58), 3 * k, 20 * k, fill=INK, stroke="none")
    sh.rect(X(xc + 27), D(58), 3 * k, 20 * k, fill=INK, stroke="none")
    # --- perfil de alumínio duplo keder 70 x 24 (cortado, hachura densa)
    rail = [(xc - 35, 1), (xc + 35, 1), (xc + 35, 34), (xc + 31, 34), (xc + 31, 24), (xc + 10, 24),
            (xc + 10, 15), (xc - 10, 15), (xc - 10, 24), (xc - 31, 24), (xc - 31, 34), (xc - 35, 34)]
    sh.pl([(X(a), D(b)) for a, b in rail], 1.2, INK, fill="url(#p-steel)", close=True)
    # canais keder (Ø10) com cordão Ø8
    for xk, sgn in ((xc - 22, -1), (xc + 22, 1)):
        sh.circle(X(xk), D(11), 5.5 * k, fill=BG, stroke=INK, sw=1.0)
        sh.circle(X(xk), D(11), 4 * k, fill=GOLD, stroke=INK, sw=0.6)
        # fenda de saída do keder
        sh.line(X(xk + sgn * 3), D(1), X(xk + sgn * 5.5), D(6), 1.2, BG)
    sh.bolt_side(X(xc), D(4), 30 * k, 6, vertical=True)
    # --- membrana externa: dois painéis, saem do keder e correm sobre o perfil
    for sgn in (-1, 1):
        xk = xc + sgn * 22
        pts = [(X(xk + sgn * 5), D(7)), (X(xk + sgn * 12), D(0)), (X(xc + sgn * 60), D(-1)),
               (X(xc + sgn * 150), D(4)), (X(xc + sgn * 260 if sgn > 0 else 0), D(2 if sgn > 0 else 1))]
        sh.membrane(pts)
    # gotejamento / pingadeira
    for sgn in (-1, 1):
        xa = xc + sgn * 40
        sh.line(X(xa), D(36), X(xa), D(56), 0.8, GOLD, dash="2 2")
        sh.head(X(xa), D(40), X(xa), D(58), GOLD, 5)
    # --- cotas (à esquerda)
    xd = X(-22)
    sh.dim_v(xd, D(0), D(60), "60", ext=X(0), left=True)
    sh.dim_v(xd, D(60), D(64), "", ext=X(0), left=True)
    sh.dim_v(xd, D(64), D(114), "50", ext=X(0), left=True)
    sh.dim_v(xd, D(114), D(196), "82", ext=X(0), left=True)
    sh.dim_v(X(-52), D(0), D(196), "196 (espessura total do envelope)", ext=None, left=True)
    sh.dim_h(X(xc - 44.45), X(xc + 44.45), D(-24), "Ø 88,9", ext=D(26))
    sh.dim_h(X(xc - 35), X(xc + 35), D(-44), "70", ext=None)
    sh.dim_h(X(xc + 4), X(W_), D(215), "terça Ø48,3 entre arcos (vão 1,20 m)", ext=None, above=False)
    # --- balões
    C = sh.callout
    C(1, X(80), D(1), X(60), D(-40))
    C(2, X(xc - 22), D(11), X(xc - 90), D(-40))
    C(3, X(xc + 33), D(20), X(xc + 100), D(-40))
    C(4, X(xc + 30), D(60), X(xc + 140), D(-12))
    C(5, X(xc + 20), D(100), X(xc + 150), D(85))
    C(6, X(200), D(30), X(240), D(-12))
    C(7, X(120), D(62), X(60), D(50))
    C(8, X(150), D(90), X(60), D(90))
    C(9, X(470), D(139), X(520), D(160))
    C(10, X(xc + 2), D(165), X(xc + 70), D(185))
    C(11, X(xc - 20), D(185), X(xc - 70), D(190))
    C(12, X(80), D(196), X(60), D(175))
    C(13, X(xc + 40), D(52), X(xc + 110), D(30))
    C(14, X(xc + 50), D(90), X(xc + 120), D(120))
    C(15, X(xc + 20), D(1), X(xc + 75), D(-70))
    C(16, X(180), D(114), X(150), D(150))
    sh.line(X(0), D(114), X(xc - 48), D(114), 1.2, INK, dash="2 2")
    sh.line(X(xc + 48), D(114), X(W_), D(114), 1.2, INK, dash="2 2")
    sh.scale_bar(X(20), D(230), k, 100, "100 mm")

    # ---------- detalhe ampliado do perfil keder ----------
    sh.panel(970, 120, 570, 420, "Detalhe A  -  perfil duplo keder e solda HF", "escala 1:2 (1 mm = 3,0 px)")
    k2 = 3.0
    t2 = Tr(1255, 296, k2)
    D2 = lambda mm: t2.y(-mm)
    X2 = t2.x
    xc2 = 0
    # tubo (topo)
    sh.add('<clipPath id="clipA"><rect x="980" y="150" width="550" height="380"/></clipPath>')
    sh.add('<g clip-path="url(#clipA)">')
    sh.tube_cut(X2(0), D2(70.5), 44.45 * k2, 3.6 * k2)
    sh.path("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (X2(-30), D2(58), 33 * k2, 33 * k2, X2(30), D2(58)), 5.0, INK)
    sh.rect(X2(-31.5), D2(58), 3 * k2, 20 * k2, fill=INK, stroke="none")
    sh.rect(X2(28.5), D2(58), 3 * k2, 20 * k2, fill=INK, stroke="none")
    rail2 = [(a - xc, b) for a, b in rail]
    sh.pl([(X2(a), D2(b)) for a, b in rail2], 1.4, INK, fill="url(#p-steel)", close=True)
    for xk, sgn in ((-22, -1), (22, 1)):
        sh.circle(X2(xk), D2(11), 5.5 * k2, fill=BG, stroke=INK, sw=1.2)
        sh.circle(X2(xk), D2(11), 4 * k2, fill=GOLD, stroke=INK, sw=0.8)
        sh.line(X2(xk + sgn * 3.2), D2(0.5), X2(xk + sgn * 5.2), D2(6.5), 2.6, BG)
        # membrana dobrada em torno do cordão (bainha soldada HF 40 mm)
        d = "M%.1f,%.1f A%.1f,%.1f 0 1 %d %.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (
            X2(xk + sgn * 4.5), D2(6.8), 4.6 * k2, 4.6 * k2, 1 if sgn > 0 else 0, X2(xk + sgn * 4.5), D2(15.2),
            X2(xk + sgn * 4.5), D2(6.8), X2(xk + sgn * 40), D2(-1))
        # arco completo em torno do cordão
        d = "M%.1f,%.1f A%.1f,%.1f 0 1 %d %.1f,%.1f" % (X2(xk + sgn * 4.4), D2(9.0), 4.4 * k2, 4.4 * k2,
                                                        0 if sgn > 0 else 1, X2(xk + sgn * 4.4), D2(13.0))
        sh.path(d, 3, GOLD)
        sh.membrane([(X2(xk + sgn * 4.4), D2(9.0)), (X2(xk + sgn * 9), D2(2)), (X2(xk + sgn * 14), D2(-0.5)),
                     (X2(xk + sgn * 75), D2(-0.5))])
        sh.membrane([(X2(xk + sgn * 4.4), D2(13.0)), (X2(xk + sgn * 3.6), D2(6.5)), (X2(xk + sgn * 8), D2(2.2))])
        # zona de solda HF hachurada
        sh.rect(X2(xk + sgn * 9) - (12 * k2 if sgn < 0 else 0), D2(-0.5), 12 * k2, 4.5 * k2, fill="url(#p-steel)", stroke="none")
    sh.bolt_side(X2(0), D2(4), 30 * k2, 5, vertical=True)
    sh.add('</g>')
    sh.dim_h(X2(-35), X2(35), D2(-30), "70", ext=D2(1))
    sh.dim_v(X2(-52), D2(1), D2(34), "24 + 10", ext=X2(-35), left=True)
    sh.label(X2(-40), D2(1.5), X2(-62), D2(-38), "solda HF 40 mm", size=11, anchor="end")
    sh.label(X2(22), D2(11), X2(58), D2(-38), "cordão keder Ø8 PVC", size=11, anchor="start")
    sh.label(X2(0), D2(24), X2(52), D2(50), "parafuso inox M8 x 30 @ 300", size=11, anchor="start")
    sh.label(X2(-31), D2(64), X2(-56), D2(64), "presilha inox 3 mm", size=11, anchor="end")
    sh.label(X2(33), D2(30), X2(52), D2(30), "pingadeira (aba 10)", size=11, anchor="start")
    sh.label(X2(44), D2(70), X2(56), D2(64), "arco Ø88,9 x 3,6", size=11, anchor="start")

    # ---------- legenda ----------
    items = [
        (1, "Membrana externa poliéster/PVC + laca PVDF, 950 a 1050 g/m², 1,0 mm, classe B1"),
        (2, "Cordão keder Ø8 mm em bainha soldada HF (40 mm), tratamento anti-wicking"),
        (3, "Perfil de alumínio duplo keder 70 x 24 mm, anodizado bronze"),
        (4, "Presilha inox 3 mm + parafuso M8 a cada 300 mm sobre o arco"),
        (5, "Arco Ø88,9 x 3,6 mm, aço A500, galvanizado + pó RAL 7022 (cortado)"),
        (6, "Câmara ventilada 60 mm: entrada nas frestas da base, saída na cumeeira"),
        (7, "Manta refletiva de alumínio dupla face (bolha) 4 mm, emendas fitadas"),
        (8, "Lã de PET reciclada 50 mm, 25 kg/m³, λ = 0,040 W/mK (R = 1,25)"),
        (9, "Terça Ø48,3 x 3,0 mm (vista), segmentos 1,20 m, ponteiras rosqueadas M16"),
        (10, "Talão em chapa 8 mm soldado ao arco: recebe as terças (2 lados)"),
        (11, "Trilho secundário de alumínio 40 x 20 mm do forro, fixado ao talão"),
        (12, "Forro tensionado acústico Trevira CS (M1), cor areia, NRC 0,6"),
        (13, "Condensado da face interna: pingadeira do perfil lança sobre a manta"),
        (14, "Junta de lã PET comprimida contra o arco (ponte térmica controlada)"),
        (15, "Junção dos painéis de membrana: um cordão em cada canal (duplo keder)"),
        (16, "Malha inox 25 x 25 sobre as terças: apoio do isolamento entre arcos"),
    ]
    sh.legend(60, 712, items, cols=2, colw=445, lh=19, size=11)

    # ---------- tabela de camadas / U ----------
    sh.text(970, 578, "RESISTÊNCIA TÉRMICA DO ENVELOPE (ISO 6946)", size=11, color=GOLD, ls="0.2em", weight=600)
    rows = [("Rse (externo)", "-", "0,04"), ("Membrana PVDF", "1", "0,00"), ("Câmara ventilada", "60", "0,00*"),
            ("Manta refletiva (bolha)", "4", "0,10"), ("Lã PET 25 kg/m³", "50", "1,25"),
            ("Câmara interna", "82", "0,13"), ("Forro tensionado", "1", "0,00"), ("Rsi (interno)", "-", "0,10"),
            ("TOTAL  R = 1,62 m²K/W", "196", "U = 0,62 W/m²K")]
    sh.table(970, 602, ["Camada", "e (mm)", "R (m²K/W)"], rows, [250, 90, 170], size=11.5, lh=18)
    sh.text(970, 792, "* câmara fortemente ventilada: desprezada; a membrana atua como proteção à chuva e ao sol.",
            size=10.5, color=GOLD)
    sh.text(970, 808, "Especificação: U ≈ 0,6 W/m²K (envelope). Vidros duplos: U ≈ 1,6 W/m²K.", size=10.5, color=GOLD)
    sh.write("DET-01_cobertura_cocoon.svg")


# ==================================================================================
# DET-02  Cobertura do ZENITH: anel do cume (óculo) e beiral
# ==================================================================================
def det02():
    sh = Sheet("DET-02", "Cobertura Zenith: cume e beiral", "ZION ZENITH", "1:10 (cume) / 1:8 (beiral)",
               "Seção vertical pelo mastro principal M1 e anel do Zênite; seção pelo anel de beiral sobre pilar.")
    # ---------------- Painel A: anel do cume ----------------
    sh.panel(60, 120, 840, 560, "Seção A  -  anel do Zênite Ø1200 com óculo de vidro", "escala 1:10 (1 mm = 0,34 px)")
    k = 0.34
    t = Tr(470, 632, k)   # mastro topo (z=0) em y=632
    X, Y = t.x, t.y
    sh.add('<clipPath id="clipA2"><rect x="62" y="148" width="836" height="530"/></clipPath>')
    sh.add('<g clip-path="url(#clipA2)">')
    # eixo
    sh.line(X(0), Y(1050), X(0), Y(-260), 0.5, INK, dash="12 3 2 3")
    # mastro Ø139,7 x 4,5 (cortado, abaixo do capitel)
    sh.rect(X(-69.85), Y(0), 4.5 * k + 1, 240 * k, fill=INK, stroke="none")
    sh.rect(X(69.85) - 4.5 * k - 1, Y(0), 4.5 * k + 1, 240 * k, fill=INK, stroke="none")
    sh.line(X(-69.85), Y(0), X(-69.85), Y(-240), 0.9, INK)
    sh.line(X(69.85), Y(0), X(69.85), Y(-240), 0.9, INK)
    sh.break_line(X(-75), Y(-125), X(75), Y(-125), 4)
    # capitel usinado: bujão Ø130 x 100 dentro do mastro + flange Ø220 x 25 + cubo cônico 120 mm
    sh.rect(X(-65), Y(0), 130 * k, 100 * k, fill="url(#p-steel)", stroke=INK, sw=1.2)
    sh.rect(X(-110), Y(25), 220 * k, 25 * k, fill="url(#p-steel)", stroke=INK, sw=1.2)
    sh.pl([(X(-70), Y(25)), (X(70), Y(25)), (X(45), Y(145)), (X(-45), Y(145))], 1.2, INK, fill="url(#p-steel)", close=True)
    # parafusos de fixação do capitel (M12 radiais)
    sh.bolt_side(X(-88), Y(-45), 30 * k, 5, vertical=False)
    sh.bolt_side(X(62), Y(-45), 30 * k, 5, vertical=False)
    # braços da coroa Ø48,3: um no plano (esquerda) e dois projetados (direita, foreshortened)
    ang = math.radians(56)
    Larm = 950
    p0 = (-55, 100)
    p1 = (p0[0] - Larm * math.cos(ang), p0[1] + Larm * math.sin(ang))
    sh.tube_seen(X(p0[0]), Y(p0[1]), X(p1[0]), Y(p1[1]), 48.3 * k, 1.2)
    for fs in (0.5,):
        q0 = (55, 100)
        q1 = (q0[0] + Larm * math.cos(ang) * fs, q0[1] + Larm * math.sin(ang))
        sh.tube_seen(X(q0[0]), Y(q0[1]), X(q1[0]), Y(q1[1]), 48.3 * k, 0.9)
    # anel Ø1200: chapa curvada 80 x 10 (cortada nos dois lados) - eixo a z = 750
    zr = p1[1]
    for sgn in (-1, 1):
        sh.rect(X(sgn * 600 - 5), Y(zr + 40), 10 * k, 80 * k, fill=INK, stroke=INK, sw=0.6)
        # gusset de ligação braço/anel
        if sgn < 0:
            sh.pl([(X(-595), Y(zr - 30)), (X(-595), Y(zr + 20)), (X(-540), Y(zr + 5))], 0.9, INK, fill="url(#p-steel)", close=True)
        else:
            sh.pl([(X(595), Y(zr - 30)), (X(595), Y(zr + 20)), (X(540), Y(zr + 5))], 0.9, INK, fill="url(#p-steel)", close=True)
    # ligação do braço direito (projetado) ao anel: linha oculta
    sh.line(X(q1[0]), Y(q1[1]), X(590), Y(zr), 0.6, INK, dash="4 3")
    # perfil arredondado de alumínio no topo do anel + membrana passando e chapa-anel aparafusada
    for sgn in (-1, 1):
        xo = sgn * 600
        # perfil de topo arredondado (alumínio) 40 x 30
        sh.path("M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 %d %.1f,%.1f L%.1f,%.1f Z" % (
            X(xo - sgn * 15), Y(zr + 40), X(xo - sgn * 15), Y(zr + 60), 25 * k, 25 * k, 1 if sgn > 0 else 0,
            X(xo + sgn * 25), Y(zr + 60), X(xo + sgn * 25), Y(zr + 40)), 1.0, INK, fill="url(#p-steel)")
        # chapa-anel de alumínio 60 x 8 aparafusada na face externa + gaxeta EPDM
        sh.rect(X(xo + sgn * 5) - (8 * k if sgn < 0 else 0), Y(zr + 38), 8 * k, 60 * k, fill="url(#p-steel)", stroke=INK, sw=0.9)
        sh.rect(X(xo + sgn * 5) - (3 * k if sgn < 0 else 0) + (0 if sgn < 0 else 0), Y(zr + 38), 3 * k, 60 * k, fill=INK, stroke="none")
        sh.bolt_side(X(xo + sgn * 30) - (0), Y(zr + 8), 45 * k, 4, vertical=False) if sgn > 0 else \
            sh.bolt_side(X(xo - 45), Y(zr + 8), 45 * k, 4, vertical=False)
        # membrana: sobe pela face externa, passa sobre o perfil arredondado e desce em 45°
        mem = [(X(xo + sgn * 15), Y(zr - 20)), (X(xo + sgn * 15), Y(zr + 55)),
               (X(xo + sgn * 5), Y(zr + 70)), (X(xo - sgn * 10), Y(zr + 72))]
        sh.membrane(mem)
        slope = [(X(xo + sgn * 15), Y(zr - 20)), (X(xo + sgn * 420), Y(zr - 20 - 364))]
        sh.membrane(slope)
        # setas de escoamento
        sh.arrow(X(xo + sgn * 200), Y(zr - 130), X(xo + sgn * 320), Y(zr - 235), 0.9, GOLD, head=6)
    # moldura de alumínio com ruptura térmica da cúpula (sobre o anel, Ø1200 externo)
    for sgn in (-1, 1):
        xo = sgn * 600
        fr = [(xo - sgn * 70, zr + 72), (xo + sgn * 10, zr + 72), (xo + sgn * 10, zr + 150), (xo - sgn * 70, zr + 150)]
        sh.pl([(X(a), Y(b)) for a, b in fr], 1.2, INK, fill="url(#p-steel)", close=True)
        sh.rect(X(xo - sgn * 30) - (0 if sgn > 0 else 10 * k), Y(zr + 150), 10 * k, 78 * k, fill=BG, stroke=INK, sw=0.6)  # ruptura (poliamida)
        # gaxeta EPDM sob a moldura
        sh.rect(X(xo - sgn * 70) - (0 if sgn > 0 else 80 * k), Y(zr + 80), 80 * k, 8 * k, fill=INK, stroke="none")
    # cúpula de vidro laminado (arco de círculo) com espessura 12 mm
    R = 1400; sag = R - math.sqrt(R * R - 560 * 560)
    for off in (0, 12):
        d = "M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (X(-560), Y(zr + 150 + off), (R + off) * k, (R + off) * k, X(560), Y(zr + 150 + off))
        sh.path(d, 0.7, "#8A9DA3")
    dpath = ("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z" %
             (X(-560), Y(zr + 150), R * k, R * k, X(560), Y(zr + 150), X(560), Y(zr + 162), (R + 12) * k, (R + 12) * k, X(-560), Y(zr + 162)))
    sh.path(dpath, 0.5, "#8A9DA3", fill=GLASS)
    # anel do forro Ø1100 (alumínio 40 x 40) com segundo vidro plano 6+6
    zl = 520
    for sgn in (-1, 1):
        sh.rect(X(sgn * 550) - (40 * k if sgn < 0 else 0), Y(zl + 20), 40 * k, 40 * k, fill="url(#p-steel)", stroke=INK, sw=0.9)
        # pendural do anel do forro ao braço
        sh.line(X(sgn * 530), Y(zl + 20), X(sgn * 430), Y(zl + 320), 0.7, INK, dash="5 3")
    sh.glass(X(-510), Y(zl + 6), X(510), Y(zl + 6), t=12 * k)
    # isolamento (manta + lã) terminando no anel do forro
    for sgn in (-1, 1):
        xo = sgn * 600
        a = [(xo + sgn * 60, zr - 100), (xo + sgn * 60 + sgn * 700, zr - 100 - 700 * math.tan(math.radians(41)))]
        # faixa de isolamento paralela à membrana (offset 60 mm)
        d0 = 60
        ang_m = math.atan2(780, 900)
        nx, ny = math.sin(ang_m), math.cos(ang_m)
        p_a = (xo + sgn * 40 + sgn * nx * d0, zr - 20 - ny * d0)
        p_b = (p_a[0] + sgn * 360, p_a[1] - 360 * 780 / 900)
        for (dd, pat) in ((0, "p-steel"), (4, "p-ins")):
            th = 4 if dd == 0 else 50
            q1 = (p_a[0] + sgn * nx * dd, p_a[1] - ny * dd); q2 = (p_b[0] + sgn * nx * dd, p_b[1] - ny * dd)
            q3 = (q2[0] + sgn * nx * th, q2[1] - ny * th); q4 = (q1[0] + sgn * nx * th, q1[1] - ny * th)
            sh.pl([(X(a), Y(b)) for a, b in (q1, q2, q3, q4)], 0.7, INK, fill="url(#%s)" % pat, close=True)
    # forro tensionado (linha 2 px) do anel do forro para baixo em 40°
    for sgn in (-1, 1):
        sh.line(X(sgn * 560), Y(zl + 20), X(sgn * 960), Y(zl + 20 - 400 * 0.72), 2.2, INK)
    sh.add('</g>')
    # cotas
    sh.dim_h(X(-600), X(600), Y(zr + 250), "Ø 1200 (anel, chapa 80 x 10)", ext=Y(zr + 40))
    sh.label(X(69.85), Y(-100), X(150), Y(-118), "Ø139,7 x 4,5", size=11, anchor="start")
    sh.dim_v(X(-1080), Y(0), Y(zr), "750 (topo do mastro ao eixo do anel)", ext=X(-600), left=True)
    sh.dim_v(X(700), Y(zr + 40), Y(zr - 40), "80", ext=X(605), left=False, size=11)
    sh.text(X(-330), Y(zr - 80), "≈ 41°", size=11, color=GOLD, anchor="middle")
    sh.text(X(0), Y(zr + 205), "óculo Ø1080 livre", size=11, color=GOLD, anchor="middle")
    # balões
    C = sh.callout
    C(1, X(-69.85), Y(-60), X(-190), Y(-90))
    C(2, X(-50), Y(60), X(-190), Y(60))
    C(3, X(-380), Y(400), X(-470), Y(330))
    C(4, X(-600), Y(zr - 20), X(-720), Y(zr - 100))
    C(5, X(-595), Y(zr + 65), X(-720), Y(zr + 110))
    C(6, X(-615), Y(zr + 20), X(-740), Y(zr + 10))
    C(7, X(0), Y(zr + 162 + sag), X(150), Y(zr + 330))
    C(8, X(-630), Y(zr + 110), X(-740), Y(zr + 200))
    C(9, X(-540), Y(zl + 40), X(-680), Y(zl + 5))
    C(10, X(0), Y(zl + 12), X(250), Y(zl - 60))
    C(11, X(-800), Y(zr - 180), X(-820), Y(zr - 320))
    C(12, X(860), Y(zr - 232), X(960), Y(zr - 150))
    C(13, X(-820), Y(zl + 20 - 260 * 0.72), X(-700), Y(zl - 300))
    sh.scale_bar(90, 660, k, 500, "500 mm")

    # ---------------- Painel B: beiral ----------------
    sh.panel(930, 120, 610, 560, "Seção B  -  anel de beiral sobre pilar", "escala 1:8 (1 mm = 0,5 px)")
    k2 = 0.5
    t2 = Tr(1230, 330, k2)   # x=0 eixo do pilar; y=0 -> topo do anel de beiral (z = 2,90 m)
    X2, Y2 = t2.x, t2.y
    sh.add('<clipPath id="clipB2"><rect x="932" y="148" width="606" height="530"/></clipPath>')
    sh.add('<g clip-path="url(#clipB2)">')
    # exterior à esquerda (x negativo), interior à direita
    # anel de beiral 150 x 100 x 4 (cortado): 100 de largura, 150 de altura, topo em z=0
    sh.rect(X2(-50), Y2(0), 100 * k2, 150 * k2, fill=BG, stroke=INK, sw=1.6)
    sh.rect(X2(-50), Y2(0), 100 * k2, 4 * k2, fill=INK, stroke="none")
    sh.rect(X2(-50), Y2(-146), 100 * k2, 4 * k2, fill=INK, stroke="none")
    sh.rect(X2(-50), Y2(0), 4 * k2, 150 * k2, fill=INK, stroke="none")
    sh.rect(X2(46), Y2(0), 4 * k2, 150 * k2, fill=INK, stroke="none")
    # chapa de topo do pilar 150 x 150 x 8 e pilar Ø101,6 x 4 abaixo (cortado)
    sh.rect(X2(-75), Y2(-150), 150 * k2, 8 * k2, fill=INK, stroke="none")
    for sgn in (-1, 1):
        sh.rect(X2(sgn * 50.8) - (4 * k2 if sgn > 0 else 0), Y2(-158), 4 * k2, 600 * k2, fill=INK, stroke="none")
    # tubo de queda Ø75 dentro do pilar
    sh.line(X2(-37.5), Y2(-158), X2(-37.5), Y2(-760), 0.8, INK, dash="6 3")
    sh.line(X2(37.5), Y2(-158), X2(37.5), Y2(-760), 0.8, INK, dash="6 3")
    sh.arrow(X2(0), Y2(-260), X2(0), Y2(-420), 0.9, GOLD, head=6)
    # painel SIP 100 mm à direita/esquerda do pilar? O pilar fica embutido: SIP dos dois lados no corte longitudinal.
    # Aqui a seção é transversal ao corpo: o SIP (100 mm) está sob o anel, centrado no pilar.
    # OSB 12 / PIR 76 / OSB 12 abaixo da chapa de topo, começando 60 mm abaixo (a chapa do pilar fica no núcleo)
    zs = -158
    sh.rect(X2(-50), Y2(zs), 12 * k2, 600 * k2, fill="url(#p-osb)", stroke=INK, sw=0.9)
    sh.rect(X2(38), Y2(zs), 12 * k2, 600 * k2, fill="url(#p-osb)", stroke=INK, sw=0.9)
    sh.rect(X2(-38), Y2(zs), 76 * k2, 600 * k2, fill="url(#p-pir)", stroke="none")
    # pilar cortado (paredes) sobre o PIR
    for sgn in (-1, 1):
        sh.rect(X2(sgn * 50.8) - (4 * k2 if sgn > 0 else 0), Y2(-158), 4 * k2, 600 * k2, fill=INK, stroke="none")
    # revestimento externo (esquerda): placa cimentícia 12 + ripas 25 + ripado 40 x 40
    sh.rect(X2(-62), Y2(zs), 12 * k2, 600 * k2, fill="url(#p-cem)", stroke=INK, sw=0.9)
    sh.rect(X2(-87), Y2(zs), 25 * k2, 600 * k2, fill=BG, stroke=INK, sw=0.6)   # câmara ventilada
    for i in range(7):
        zz = zs - 20 - i * 80
        sh.wood(X2(-127), Y2(zz), 40 * k2, 40 * k2, grain=False)
    # revestimento interno (direita): tecido/madeira 15 sobre ripas 20
    sh.rect(X2(50), Y2(zs), 20 * k2, 600 * k2, fill=BG, stroke=INK, sw=0.6)
    sh.wood(X2(70), Y2(zs), 15 * k2, 600 * k2, grain=False)
    # perfil de borda arredondado (alumínio, R 40) no canto externo superior do anel
    sh.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z" % (
        X2(-50), Y2(0), X2(-50), Y2(-40), X2(-70), Y2(-40), 40 * k2, 40 * k2, X2(-50), Y2(0)),
        1.0, INK, fill="url(#p-steel)")
    sh.pl([(X2(-50), Y2(0)), (X2(-50), Y2(-40)), (X2(-90), Y2(-40)), (X2(-90), Y2(-10)), (X2(-80), Y2(0))],
          1.0, INK, fill="url(#p-steel)", close=True)
    # trilho keder da membrana principal sobre o anel (alumínio 40 x 24) : membrana vem do interior descendo
    sh.rect(X2(-20), Y2(0), 40 * k2, 24 * k2, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.circle(X2(-10), Y2(12), 5 * k2, fill=GOLD, stroke=INK, sw=0.6)
    sh.bolt_side(X2(8), Y2(24), 30 * k2, 4, vertical=True)
    # membrana principal: desce do interior (direita, acima) com inclinação ~28°, passa sobre o perfil arredondado
    sh.membrane([(X2(600), Y2(24 + 600 * 0.53)), (X2(-8), Y2(26)), (X2(-60), Y2(25)), (X2(-90), Y2(5)), (X2(-98), Y2(-20))])
    sh.arrow(X2(300), Y2(24 + 300 * 0.53 + 40), X2(120), Y2(24 + 120 * 0.53 + 40), 0.9, GOLD, head=6)
    # calha oculta 80 x 60 de alumínio na face externa do anel, sob o perfil arredondado
    g = [(-90, -42), (-90, -110), (-170, -110), (-170, -50)]
    sh.pl([(X2(a), Y2(b)) for a, b in g], 1.4, INK, fill="none")
    sh.pl([(X2(a), Y2(b)) for a, b in [(-90, -44), (-92, -108), (-168, -108), (-168, -52)]], 0.5, INK, fill="none")
    sh.arrow(X2(-105), Y2(-30), X2(-120), Y2(-95), 0.9, GOLD, head=6)   # gotejamento
    # saída da calha para o tubo de queda (tubo Ø50 atravessando o painel -> pilar)
    sh.rect(X2(-90), Y2(-95), 45 * k2, 14 * k2, fill=BG, stroke=INK, sw=0.8)
    # tampa/fascia de alumínio externa cobrindo a calha (chapa dobrada 2 mm)
    sh.pl([(X2(-98), Y2(-20)), (X2(-178), Y2(-20)), (X2(-178), Y2(-130)), (X2(-150), Y2(-130))], 1.6, INK)
    # trilho keder da aba (membrana em balanço) na face inferior externa da fascia
    sh.rect(X2(-190), Y2(-130), 40 * k2, 22 * k2, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.circle(X2(-178), Y2(-141), 5 * k2, fill=GOLD, stroke=INK, sw=0.6)
    sh.membrane([(X2(-186), Y2(-152)), (X2(-230), Y2(-160)), (X2(-620), Y2(-235))])
    sh.arrow(X2(-380), Y2(-150), X2(-520), Y2(-177), 0.9, GOLD, head=6)
    # fresta de ventilação alta (entrada de ar) entre fascia e membrana principal: seta
    sh.arrow(X2(-140), Y2(-10), X2(-60), Y2(40), 0.9, GOLD, head=6, dash="3 2")
    # isolamento interno da cobertura (manta + lã) e forro chegando ao anel pelo interior
    sh.pl([(X2(70), Y2(-20)), (X2(600), Y2(-20 + 530 * 0.53))], 0.6, INK, fill="none")
    ang_m = math.atan(0.53); nx, ny = -math.sin(ang_m), math.cos(ang_m)
    pa = (70, -60); pb = (600, -60 + 530 * 0.53)
    for (dd, th, pat) in ((0, 4, "p-steel"), (4, 50, "p-ins")):
        q1 = (pa[0] + nx * dd, pa[1] + ny * dd); q2 = (pb[0] + nx * dd, pb[1] + ny * dd)
        q3 = (q2[0] + nx * th, q2[1] + ny * th); q4 = (q1[0] + nx * th, q1[1] + ny * th)
        sh.pl([(X2(a), Y2(b)) for a, b in (q1, q2, q3, q4)], 0.7, INK, fill="url(#%s)" % pat, close=True)
    sh.line(X2(85), Y2(-175), X2(600), Y2(-175 + 515 * 0.53), 2.2, INK)   # forro
    sh.rect(X2(70), Y2(-158), 15 * k2, 30 * k2, fill="url(#p-steel)", stroke=INK, sw=0.8)  # trilho do forro
    # fita LED no perímetro do forro
    sh.circle(X2(92), Y2(-168), 3, fill=GOLD, stroke="none")
    sh.add('</g>')
    # cotas do beiral
    sh.dim_v(X2(-330), Y2(0), Y2(-150), "150", ext=X2(-50), left=True)
    sh.dim_h(X2(-50), X2(50), Y2(60), "100", ext=Y2(0))
    sh.dim_h(X2(-50), X2(50), Y2(-700), "SIP 100", ext=None, above=False)
    sh.dim_h(X2(-170), X2(-90), Y2(-118), "80", ext=None, above=False, size=11)
    sh.text(X2(-330), Y2(-330), "EXTERIOR", size=10, color=GOLD, ls="0.2em")
    sh.text(X2(120), Y2(-330), "INTERIOR", size=10, color=GOLD, ls="0.2em")
    sh.text(X2(-330), Y2(-192), "z = 2,90 (topo do anel)", size=10.5, color=GOLD, anchor="middle")
    # balões do beiral (numeração continua)
    C(14, X2(0), Y2(-70), X2(200), Y2(-90))
    C(15, X2(-50.8), Y2(-300), X2(-230), Y2(-260))
    C(16, X2(-72), Y2(-22), X2(-260), Y2(20))
    C(17, X2(-130), Y2(-80), X2(-280), Y2(-100))
    C(18, X2(-178), Y2(-141), X2(-320), Y2(-180))
    C(19, X2(0), Y2(-500), X2(200), Y2(-500))
    C(20, X2(-107), Y2(-400), X2(-260), Y2(-430))
    C(21, X2(77), Y2(-400), X2(200), Y2(-420))
    C(22, X2(-10), Y2(12), X2(120), Y2(60))
    C(23, X2(0), Y2(-154), X2(200), Y2(-160))
    C(24, X2(-100), Y2(20), X2(-200), Y2(120))
    C(25, X2(-37.5), Y2(-640), X2(-230), Y2(-620))

    items = [
        (1, "Mastro M1 Ø139,7 x 4,5 mm, 5,05 m (topo em z = 5,05)"), (2, "Capitel usinado: bujão Ø130 x 100 + flange Ø220 x 25, 2 x M12 radiais"),
        (3, "Braço da coroa Ø48,3 x 3,0 mm, L = 0,95 m (3 a 120°)"), (4, "Anel do cume: chapa curvada 80 x 10 mm, Ø1200, gusset ao braço"),
        (5, "Perfil arredondado de alumínio no topo do anel (R 25)"), (6, "Chapa-anel de alumínio 60 x 8, M8 @ 150 + gaxeta EPDM"),
        (7, "Cúpula de vidro laminado 6+6 mm curvo (R 1400), low-e"), (8, "Moldura da cúpula: alumínio com ruptura térmica, gaxeta EPDM"),
        (9, "Anel do forro Ø1100 em alumínio 40 x 40, pendurado nos braços"), (10, "Segundo vidro plano laminado 6+6 mm (câmara de ar entre vidros)"),
        (11, "Membrana PVDF deixando o anel com ≈ 41°, pré-tensão 2,5 kN/m"), (12, "Escoamento da chuva ao beiral e às bordas em catenária"),
        (13, "Isolamento (manta + lã PET 50 mm) e forro paralelos à membrana"),
        (14, "Anel de beiral: tubo retangular 150 x 100 x 4,0 mm (viga-anel)"), (15, "Pilar Ø101,6 x 4,0 mm embutido no painel, chapa de topo 150 x 150 x 8"),
        (16, "Perfil de borda arredondado (alumínio R 40) + fascia 2 mm"), (17, "Calha oculta de alumínio 80 x 60 mm, saída Ø50 ao pilar"),
        (18, "Trilho keder da aba em balanço (membrana até os postes externos)"), (19, "Painel SIP 100 mm (OSB 12 / PIR 76 / OSB 12)"),
        (20, "Placa cimentícia 12 + câmara 25 + ripado termotratado 40 x 40"), (21, "Acabamento interno: painel madeira/tecido 15 mm sobre ripas 20"),
        (22, "Trilho keder da membrana principal sobre o anel (alumínio 40 x 24)"), (23, "Chapa de topo do pilar soldada ao anel de beiral"),
        (24, "Entrada de ar da câmara ventilada pela fresta alta (tela anti-inseto)"), (25, "Tubo de queda Ø75 mm dentro do pilar (2 pilares)"),
    ]
    sh.legend(60, 712, items, cols=3, colw=480, lh=17.5, size=10.5)
    sh.write("DET-02_cobertura_zenith.svg")


# ==================================================================================
# DET-03  Ancoragens
# ==================================================================================
def det03():
    sh = Sheet("DET-03", "Ancoragens", "COMUM", "1:5 / 1:20 / 1:2,5",
               "(a) pé de arco do Cocoon no quadro do deck; (b) pé articulado e estai dos postes externos do Zenith; (c) bolsa de cabo de borda e chapa de canto.")
    # ---------------- (a) pé de arco ----------------
    sh.panel(60, 120, 600, 560, "(a)  Pé de arco Cocoon sobre viga de borda", "1:5 (1 mm = 0,8 px)")
    k = 0.8
    t = Tr(400, 470, k)    # x=0 eixo do pé do arco; y=0 topo do piso acabado. Exterior à esquerda.
    X, Y = t.x, t.y
    sh.add('<clipPath id="c3a"><rect x="62" y="148" width="596" height="530"/></clipPath>')
    sh.add('<g clip-path="url(#c3a)">')
    # viga de borda: 2 x U 150 x 60 x 3 (caixão) - cortada, abaixo do contrapiso
    zt = -32          # topo das vigas (abaixo do compensado 18 + piso 14)
    for x0 in (-60, 0):
        sh.pl([(X(x0), Y(zt)), (X(x0 + 60), Y(zt)), (X(x0 + 60), Y(zt - 150)), (X(x0), Y(zt - 150))], 1.2, INK, fill="none", close=True)
        # espessura 3 mm: paredes
        inner = [(x0 + 3, zt - 3), (x0 + 57, zt - 3), (x0 + 57, zt - 147), (x0 + 3, zt - 147)]
        sh.pl([(X(a), Y(b)) for a, b in inner], 0.6, INK, fill="none", close=True)
        sh.rect(X(x0), Y(zt), 60 * k, 3 * k, fill=INK, stroke="none")
        sh.rect(X(x0), Y(zt - 147), 60 * k, 3 * k, fill=INK, stroke="none")
        sh.rect(X(x0 if x0 == 0 else x0 + 57), Y(zt), 3 * k, 150 * k, fill=INK, stroke="none")
        # enrijecedores (lábios) de 15 mm
        lip_x = x0 + 57 if x0 == -60 else x0
        sh.rect(X(lip_x - (0 if x0 == -60 else 0)), Y(zt), 3 * k, 15 * k, fill=INK, stroke="none")
        sh.rect(X(lip_x), Y(zt - 135), 3 * k, 15 * k, fill=INK, stroke="none")
    # vigota 50 x 150 vista (corre em y) - lado interno
    sh.rect(X(60), Y(zt), 300 * k, 150 * k, fill="url(#p-ply)", stroke=INK, sw=0.9)
    sh.text(X(190), Y(zt - 125), "vigota 50 x 150 @ 400 (vista)", size=10, anchor="middle", color=GOLD)
    # PIR 50 entre vigotas e manta inferior
    sh.ins(X(60), Y(zt - 100), 300 * k, 50 * k, "p-pir")
    sh.line(X(-120), Y(zt - 152), X(360), Y(zt - 152), 2.0, GOLD)
    # compensado naval 18 + piso de engenharia 14 (interior, à direita do eixo do arco)
    sh.rect(X(-60), Y(zt + 18), 420 * k, 18 * k, fill="url(#p-ply)", stroke=INK, sw=0.9)
    sh.wood(X(30), Y(0), 330 * k, 14 * k, grain=False)
    # chapa de base 200 x 150 x 10 sobre o compensado (topo do piso), com calço
    sh.rect(X(-100), Y(zt + 18 + 10), 200 * k, 10 * k, fill=INK, stroke="none")
    # arco Ø88,9 inclinado 12° para dentro (visto, cortado no topo do painel)
    ang = math.radians(12)
    L = 330
    top = (L * math.sin(ang), zt + 28 + L * math.cos(ang))
    sh.tube_seen(X(0), Y(zt + 28), X(top[0]), Y(top[1]), 88.9 * k, 1.2)
    # enrijecedores 8 mm (2) triangulares 80 x 60
    for sgn in (-1, 1):
        base = sgn * 44.45
        pts = [(base, zt + 28), (base + sgn * 60, zt + 28), (base + 80 * math.sin(ang) * 0 + 0, zt + 28 + 80)]
        pts = [(base + sgn * 0 + (80 * math.sin(ang)), zt + 28 + 80)] if False else pts
        sh.pl([(X(a), Y(b)) for a, b in pts], 0.9, INK, fill="url(#p-steel)", close=True)
    # chumbadores M16 (2 visíveis): atravessam chapa, compensado e mesa superior da viga; porca + arruela abaixo
    for xb in (-75, 75):
        sh.rect(X(xb - 8), Y(zt + 28 + 10), 16 * k, 10 * k, fill=INK, stroke="none")    # cabeça
        sh.rect(X(xb - 8), Y(zt + 28), 16 * k, 70 * k, fill=BG, stroke=INK, sw=0.8)     # haste
        sh.rect(X(xb - 14), Y(zt - 3), 28 * k, 14 * k, fill=INK, stroke="none")         # porca + arruela chapa
    sh.text(X(135), Y(zt + 45), "M16 (4)", size=9.5, anchor="start", color=GOLD)
    # --- lado exterior (esquerda): trilho de base 100 x 50 x 3 sobre o deck, grampo keder, calha oculta 80
    xr = -175     # eixo do trilho (mm)
    sh.rect(X(xr - 25), Y(zt + 18 + 100), 50 * k, 100 * k, fill=BG, stroke=INK, sw=1.6)
    sh.rect(X(xr - 22), Y(zt + 18 + 97), 44 * k, 94 * k, fill=BG, stroke=INK, sw=0.6)
    sh.rect(X(xr - 25), Y(zt + 118), 50 * k, 3 * k, fill=INK, stroke="none")
    sh.rect(X(xr - 25), Y(zt + 21), 50 * k, 3 * k, fill=INK, stroke="none")
    sh.rect(X(xr - 25), Y(zt + 118), 3 * k, 100 * k, fill=INK, stroke="none")
    sh.rect(X(xr + 22), Y(zt + 118), 3 * k, 100 * k, fill=INK, stroke="none")
    sh.bolt_side(X(xr), Y(zt + 122), 60 * k, 5, vertical=True)     # parafuso M10 @ 600 ao quadro
    # grampo keder de alumínio na face externa superior do trilho
    sh.rect(X(xr - 55), Y(zt + 118), 30 * k, 26 * k, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.circle(X(xr - 44), Y(zt + 107), 5 * k, fill=GOLD, stroke=INK, sw=0.6)
    sh.bolt_side(X(xr - 25), Y(zt + 110), 22 * k, 4, vertical=False)
    # membrana: desce paralela ao arco (25 mm fora da face externa do tubo) até o grampo
    off = 44.45 + 26
    mtop = (top[0] - off * math.cos(ang), top[1] + off * math.sin(ang))
    mbot = (153 * math.sin(ang) - off * math.cos(ang), zt + 28 + 153 * math.cos(ang) + off * math.sin(ang))
    sh.membrane([(X(mtop[0]), Y(mtop[1])), (X(mbot[0]), Y(mbot[1])), (X(xr - 40), Y(zt + 135)), (X(xr - 48), Y(zt + 112))])
    # perfil keder no arco (visto, junto ao tubo) - simplificado como faixa
    kr = 44.45 + 4
    sh.pl([(X(top[0] - kr * math.cos(ang)), Y(top[1] + kr * math.sin(ang))),
           (X(-kr * math.cos(ang) + 60 * math.sin(ang)), Y(zt + 28 + kr * math.sin(ang) + 60 * math.cos(ang)))], 5, INK)
    # calha oculta 80 x 60 de alumínio fixada na face externa do trilho, sob a borda da membrana
    gx = xr - 55
    sh.pl([(X(gx), Y(zt + 92)), (X(gx), Y(zt + 40)), (X(gx - 80), Y(zt + 40)), (X(gx - 80), Y(zt + 100))], 1.4, INK)
    sh.pl([(X(gx - 2), Y(zt + 90)), (X(gx - 2), Y(zt + 42)), (X(gx - 78), Y(zt + 42)), (X(gx - 78), Y(zt + 98))], 0.5, INK)
    sh.arrow(X(gx - 30), Y(zt + 125), X(gx - 40), Y(zt + 60), 0.9, GOLD, head=6)
    # tela anti-inseto / fresta de ventilação da câmara entre calha e membrana
    sh.arrow(X(gx - 120), Y(zt + 130), X(gx - 20), Y(zt + 165), 0.9, GOLD, head=6, dash="3 2")
    # deck externo: ripas 20 x 140 com 6 mm de folga sobre vigotas próprias (vistas)
    sh.rect(X(gx - 250), Y(zt + 18 + 20), 170 * k, 20 * k, fill="url(#p-wood)", stroke=INK, sw=1.2)
    sh.line(X(gx - 140), Y(zt + 38), X(gx - 140), Y(zt + 18), 2.5, BG)
    sh.rect(X(gx - 250), Y(zt + 18), 170 * k, 18 * k, fill="url(#p-ply)", stroke=INK, sw=0.6)  # vigota vista (simplificada)
    # rodapé interno com fita LED e forro chegando
    sh.rect(X(52), Y(zt + 28 + 120), 12 * k, 110 * k, fill="url(#p-wood)", stroke=INK, sw=0.9)
    sh.circle(X(68), Y(zt + 28 + 112), 2.5, fill=GOLD, stroke="none")
    sh.line(X(64), Y(zt + 28 + 120), X(120), Y(zt + 400), 2.0, INK)   # forro interno
    # isolamento (manta + PET) paralelo ao arco pelo interior
    sh.add('</g>')
    # cotas
    sh.dim_h(X(-100), X(100), Y(zt - 185), "200 (chapa de base)", ext=None, above=False, size=11)
    sh.dim_h(X(gx - 80), X(gx), Y(zt + 25), "80", ext=None, above=False, size=11)
    sh.dim_h(X(xr - 25), X(xr + 25), Y(zt + 140), "50", ext=None, size=11)
    sh.text(X(-330), Y(zt + 260), "EXTERIOR", size=10, color=GOLD, ls="0.2em")
    sh.text(X(200), Y(zt + 260), "INTERIOR", size=10, color=GOLD, ls="0.2em")
    sh.text(X(230), Y(6), "piso acabado z = 0", size=10, color=GOLD)
    sh.text(X(110), Y(zt + 250), "12°", size=11, color=GOLD)
    C = sh.callout
    C(1, X(52), Y(zt + 28 + 250), X(180), Y(zt + 330))
    C(2, X(-90), Y(zt + 33), X(-250), Y(zt + 5))
    C(3, X(50), Y(zt + 28 + 45), X(150), Y(zt + 130))
    C(4, X(75), Y(zt + 28 + 50), X(190), Y(zt + 60))
    C(5, X(30), Y(zt - 60), X(-60), Y(zt - 110))
    C(6, X(xr), Y(zt + 70), X(xr + 60), Y(zt + 220))
    C(7, X(xr - 44), Y(zt + 107), X(xr - 100), Y(zt + 240))
    C(8, X(gx - 40), Y(zt + 60), X(gx - 150), Y(zt + 90))
    C(9, X(mtop[0] + 8), Y(mtop[1] - 40), X(-250), Y(zt + 330))
    C(10, X(gx - 200), Y(zt + 30), X(gx - 200), Y(zt - 60))
    C(11, X(200), Y(zt + 10), X(300), Y(zt + 130))
    C(12, X(66), Y(zt + 28 + 112), X(220), Y(zt + 200))
    C(13, X(gx - 60), Y(zt + 150), X(gx - 170), Y(zt + 200))
    sh.scale_bar(80, 660, k, 200, "200 mm")

    # ---------------- (b) pé do poste + estai ----------------
    sh.panel(690, 120, 420, 560, "(b)  Poste externo Zenith: base e estai", "1:20 e 1:5")
    k2 = 0.12
    t2 = Tr(905, 560, k2)    # x=0 base do poste; y=0 nível do solo
    X2, Y2 = t2.x, t2.y
    sh.add('<clipPath id="c3b"><rect x="692" y="148" width="416" height="530"/></clipPath>')
    sh.add('<g clip-path="url(#c3b)">')
    sh.soil(X2(-500), Y2(0), 1500 * k2, 400 * k2)
    sh.line(X2(-500), Y2(0), X2(1000), Y2(0), 0.9, INK)
    a8 = math.radians(8)
    Lp = 2650
    ptop = (-Lp * math.sin(a8), Lp * math.cos(a8) + 250)   # base a 250 mm do solo, inclinado para fora (esquerda)
    sh.tube_seen(X2(0), Y2(250), X2(ptop[0]), Y2(ptop[1]), 76.1 * k2, 1.0)
    # olhal no topo + cabo de borda (esquerda/direita para os cantos) e estai para a direita (para fora do corpo?)
    # Postes inclinam para fora do corpo; estai vai para fora, até estaca de tração.
    sh.circle(X2(ptop[0]), Y2(ptop[1] + 40), 4, fill=BG, stroke=INK, sw=1.2)
    stay_anchor = (-1500, 0)
    sh.cable(X2(ptop[0] - 30), Y2(ptop[1] + 30), X2(stay_anchor[0]), Y2(stay_anchor[1] + 150), 1.6)
    mid = ((ptop[0] - 30 + stay_anchor[0]) / 2, (ptop[1] + 30 + 150) / 2)
    angs = math.degrees(math.atan2(-(ptop[1] + 30 - 150) * k2, (stay_anchor[0] - ptop[0] + 30) * k2))
    sh.turnbuckle(X2(mid[0]), Y2(mid[1]), angs, 30, 9)
    # estaca de tração: haste Ø76 com hélice Ø300, 2,0 m, cabeça com olhal
    sh.rect(X2(stay_anchor[0] - 38), Y2(150), 76 * k2, 850 * k2, fill=BG, stroke=INK, sw=1.0)
    sh.pl([(X2(stay_anchor[0] - 150), Y2(-500)), (X2(stay_anchor[0] + 150), Y2(-600))], 1.6, INK)
    sh.break_line(X2(stay_anchor[0] - 60), Y2(-720), X2(stay_anchor[0] + 60), Y2(-720), 4)
    sh.text(X2(stay_anchor[0]), Y2(-860), "L 2,0 m", size=9.5, anchor="middle", color=GOLD)
    sh.circle(X2(stay_anchor[0]), Y2(150), 4, fill=BG, stroke=INK, sw=1.2)
    # cabo de borda saindo do olhal (dois cantos, vistos em perspectiva simplificada)
    sh.cable(X2(ptop[0]), Y2(ptop[1] + 40), X2(ptop[0] + 1300), Y2(ptop[1] + 40 - 300), 1.4)
    sh.membrane([(X2(ptop[0] + 60), Y2(ptop[1] + 30)), (X2(ptop[0] + 1300), Y2(ptop[1] + 30 + 1300 * 0.30))])
    # base articulada sobre estaca do poste
    sh.rect(X2(-75), Y2(250), 150 * k2, 10 * k2, fill=INK, stroke="none")
    sh.rect(X2(-38), Y2(240), 76 * k2, 850 * k2, fill=BG, stroke=INK, sw=1.0)
    sh.pl([(X2(-150), Y2(-500)), (X2(150), Y2(-600))], 1.6, INK)
    sh.break_line(X2(-60), Y2(-720), X2(60), Y2(-720), 4)
    sh.add('</g>')
    sh.dim_v(X2(-1650), Y2(250), Y2(ptop[1]), "2,65 m", ext=None, left=True, size=11)
    sh.text(X2(ptop[0] + 60), Y2(ptop[1] - 500), "8°", size=11, color=GOLD)
    sh.dim_h(X2(stay_anchor[0]), X2(0), Y2(-950), "1,50 m", ext=None, above=False, size=11)
    C(14, X2(ptop[0] / 2 - 20), Y2(ptop[1] / 2 + 100), X2(400), Y2(1300))
    C(15, X2(mid[0]), Y2(mid[1]), X2(mid[0] + 250), Y2(mid[1] - 350))
    C(16, X2(stay_anchor[0] + 38), Y2(-300), X2(stay_anchor[0] + 450), Y2(-350))
    C(17, X2(ptop[0]), Y2(ptop[1] + 40), X2(ptop[0] + 350), Y2(ptop[1] - 250))
    C(18, X2(ptop[0] + 500), Y2(ptop[1] + 40 - 167), X2(ptop[0] + 900), Y2(ptop[1] - 400))
    # detalhe da base articulada 1:5
    k3 = 0.7
    t3 = Tr(1010, 662, k3)
    X3, Y3 = t3.x, t3.y
    sh.rect(935, 445, 170, 228, fill=BG, stroke=GOLD, sw=0.5, dash="3 2")
    sh.text(1100, 460, "base articulada  1:5", size=10, color=GOLD, anchor="end")
    sh.rect(X3(-38), Y3(0), 76 * k3, 40 * k3, fill=BG, stroke=INK, sw=1.0)              # topo da estaca
    sh.rect(X3(-75), Y3(40), 150 * k3, 8 * k3, fill=INK, stroke="none")                  # chapa da estaca 150 x 150 x 8
    sh.rect(X3(-75), Y3(58), 150 * k3, 10 * k3, fill=INK, stroke="none")                 # chapa de base 150 x 150 x 10
    for xb in (-55, 55):
        sh.bolt_side(X3(xb), Y3(70), 34 * k3, 4, vertical=True)
    sh.rect(X3(-6), Y3(58 + 60), 12 * k3, 60 * k3, fill="url(#p-steel)", stroke=INK, sw=0.9)   # orelha central 12 mm
    # garfo do poste (2 chapas 10 mm) e pino Ø20
    for xf in (-18, 8):
        sh.rect(X3(xf), Y3(58 + 95), 10 * k3, 65 * k3, fill=INK, stroke="none")
    sh.circle(X3(0), Y3(58 + 95 - 30 + 30), 10 * k3, fill=BG, stroke=INK, sw=1.2)
    sh.circle(X3(0), Y3(58 + 95), 3 * k3, fill=INK, stroke="none")
    # poste inclinado 8° saindo do garfo
    ptop3 = (-60 * math.sin(a8), 58 + 150 + 60 * math.cos(a8))
    sh.tube_seen(X3(0), Y3(58 + 150), X3(ptop3[0]), Y3(ptop3[1]), 76.1 * k3, 1.2)
    sh.label(X3(0), Y3(153), X3(20), Y3(215), "pino Ø20 inox", size=9.5, anchor="start")
    sh.label(X3(-13), Y3(130), X3(-30), Y3(195), "garfo 2 x ch. 10", size=9.5, anchor="end")
    sh.label(X3(70), Y3(62), X3(60), Y3(20), "ch. 150 x 150 x 10 + 4 M12", size=9.5, anchor="end")

    # ---------------- (c) bolsa de cabo e chapa de canto ----------------
    sh.panel(1140, 120, 400, 560, "(c)  Cabo de borda Ø12", "1:2,5 e 1:5")
    k4 = 1.6
    t4 = Tr(1250, 300, k4)
    X4, Y4 = t4.x, t4.y
    # bolsa: membrana dobrada em torno do cabo Ø12 (folga: bolsa Ø32) e soldada HF 40 mm
    sh.circle(X4(0), Y4(0), 6 * k4, fill=BG, stroke=INK, sw=1.2)
    for a in range(0, 360, 60):
        sh.circle(X4(3.4 * math.cos(math.radians(a))), Y4(3.4 * math.sin(math.radians(a))), 2.6 * k4 * 0.9, fill=BG, stroke=INK, sw=0.6)
    sh.circle(X4(0), Y4(0), 2.6 * k4, fill=BG, stroke=INK, sw=0.6)
    # membrana: linha principal vindo da direita, dobra em volta do cabo e volta soldada sob a principal
    d = "M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f L%.1f,%.1f" % (
        X4(140), Y4(16), X4(10), Y4(16), 16 * k4, 16 * k4, X4(10), Y4(-16), X4(90), Y4(-16))
    sh.path(d, 3, GOLD, cap="round")
    sh.rect(X4(40), Y4(-14), 45 * k4, 5, fill="url(#p-steel)", stroke="none")
    sh.text(X4(62), Y4(-24), "solda HF 40", size=9.5, anchor="middle", color=GOLD)
    sh.rect(X4(40), Y4(16 + 3), 45 * k4, 5, fill="url(#p-steel)", stroke="none")   # faixa de reforço superior
    sh.dim_h(X4(-16), X4(16), Y4(30), "Ø32 bolsa", ext=None, size=10)
    sh.dim_h(X4(-6), X4(6), Y4(-40), "Ø12", ext=None, above=False, size=10)
    sh.text(X4(150), Y4(2), "membrana", size=10, color=GOLD)
    sh.text(X4(150), Y4(-32), "faixa de reforço", size=10, color=GOLD)
    sh.text(X4(150), Y4(-44), "(2ª camada 200 mm)", size=10, color=GOLD)
    C(19, X4(0), Y4(0), X4(-40), Y4(-35))
    C(20, X4(-16), Y4(0), X4(-50), Y4(20))
    # chapa de canto no topo do poste (planta) 1:5
    k5 = 0.6
    t5 = Tr(1290, 560, k5)
    X5, Y5 = t5.x, t5.y
    sh.text(1160, 410, "chapa de canto (planta, no olhal do poste)  1:5", size=10, color=GOLD)
    plate = [(-40, -20), (160, -110), (200, -70), (200, 70), (160, 110)]
    sh.pl([(X5(a), Y5(b)) for a, b in plate], 1.4, INK, fill="url(#p-steel)", close=True)
    # olhal do poste (esquerda) com pino
    sh.bolt_top(X5(0), Y5(0), 10 * k5)
    sh.circle(X5(0), Y5(0), 30 * k5, fill="none", stroke=INK, sw=1.2)
    sh.text(X5(0), Y5(45), "olhal do poste", size=9.5, anchor="middle", color=GOLD)
    # dois esticadores garfo-garfo com os cabos de borda saindo em direções diferentes
    for (hx, hy, ang_) in ((175, -85, 38), (175, 85, -38)):
        sh.bolt_top(X5(hx), Y5(hy), 7 * k5)
        ex, ey = hx + 60 * math.cos(math.radians(ang_)), hy - 60 * math.sin(math.radians(ang_))
        sh.turnbuckle(X5(hx + 45 * math.cos(math.radians(ang_))), Y5(hy - 45 * math.sin(math.radians(ang_))), -ang_, 40, 10)
        sh.cable(X5(hx + 70 * math.cos(math.radians(ang_))), Y5(hy - 70 * math.sin(math.radians(ang_))),
                 X5(hx + 190 * math.cos(math.radians(ang_))), Y5(hy - 190 * math.sin(math.radians(ang_))), 1.6)
    # cinta de poliéster do canto da membrana com fivela na chapa
    sh.bolt_top(X5(120), Y5(0), 6 * k5)
    sh.rect(X5(130), Y5(8), 90 * k5, 16 * k5, fill=BG, stroke=GOLD, sw=1.2)
    sh.text(X5(232), Y5(4), "cinta 50", size=9.5, anchor="start", color=GOLD)
    sh.pl([(X5(235), Y5(-25)), (X5(340), Y5(-95))], 3, GOLD)   # membrana de canto (bordas)
    sh.pl([(X5(235), Y5(25)), (X5(340), Y5(95))], 3, GOLD)
    sh.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (X5(340), Y5(-95), X5(300), Y5(0), X5(340), Y5(95)), 0.6, GOLD, dash="3 2")
    sh.text(X5(340), Y5(-112), "membrana", size=9.5, color=GOLD, anchor="middle")
    sh.text(X5(-70), Y5(-190), "cabo de borda Ø12", size=9.5, color=GOLD)
    sh.text(X5(-70), Y5(200), "cabo de borda Ø12", size=9.5, color=GOLD)
    C(21, X5(80), Y5(-55), X5(-30), Y5(-120))
    C(22, X5(175 + 45 * math.cos(math.radians(38))), Y5(85 - 45 * math.sin(math.radians(38))), X5(120), Y5(190))
    C(23, X5(160), Y5(8), X5(80), Y5(110))

    items = [
        (1, "Arco Ø88,9 x 3,6 mm, inclinado 12° para dentro na base (elipse de seção)"),
        (2, "Chapa de base 200 x 150 x 10 mm soldada ao tubo (solda em todo o contorno, a = 6)"),
        (3, "Enrijecedores 2 x chapa 8 mm, 80 x 60 mm"),
        (4, "Chumbadores M16 classe 8.8 zincados (4 por pé), porca + arruela chapa 50 x 50 x 5"),
        (5, "Viga de borda: 2 x U enrijecido 150 x 60 x 3,0 (caixão), galvanizado Z275"),
        (6, "Trilho de base 100 x 50 x 3,0 curvado em planta, parafuso M10 @ 600 ao quadro"),
        (7, "Grampo keder de alumínio 30 x 26 na face externa do trilho (borda inferior da membrana)"),
        (8, "Calha oculta de alumínio 80 x 60 sob a borda da concha, queda aos tubos Ø75"),
        (9, "Membrana externa descendo paralela ao arco (perfil keder sobre o arco)"),
        (10, "Deck externo: ripas 20 x 140 com folga 6 mm sobre vigotas próprias"),
        (11, "Compensado naval 18 mm + piso de engenharia 14 mm"),
        (12, "Rodapé de madeira com fita LED 2700 K (indireta) e chegada do forro"),
        (13, "Fresta de ventilação da câmara (tela anti-inseto inox)"),
        (14, "Poste externo Ø76,1 x 3,6 mm, 2,65 m, inclinado 8° para fora"),
        (15, "Estai cabo inox Ø10 mm com esticador garfo-garfo M16"),
        (16, "Estaca helicoidal de tração Ø76 / hélice Ø300, L 2,0 m, cabeça com olhal"),
        (17, "Olhal no topo do poste (chapa 10 mm) para chapa de canto"),
        (18, "Cabo de borda Ø12 e membrana em catenária (flecha 0,30 a 0,35 m)"),
        (19, "Cabo de aço inox AISI 316 Ø12 mm, 7 x 19"),
        (20, "Bolsa de borda Ø32 soldada HF 40 mm, com faixa de reforço"),
        (21, "Chapa de canto inox 8 mm com furos Ø18 (olhal, 2 esticadores, cinta)"),
        (22, "Esticador garfo-garfo M16 inox + terminal prensado com sapatilha"),
        (23, "Cinta de poliéster 50 mm do canto da membrana com fivela de catraca"),
    ]
    sh.legend(60, 712, items, cols=3, colw=480, lh=17.5, size=10.5)
    sh.write("DET-03_ancoragem.svg")


# ==================================================================================
# DET-04  Fundação e deck elevado
# ==================================================================================
def det04():
    sh = Sheet("DET-04", "Fundação e deck elevado", "COMUM", "1:20 / 1:50",
               "Estacas helicoidais, cabeçotes ajustáveis, vigas U galvanizadas, vigotas de madeira e camadas de piso. Mínima movimentação de terra; sistema removível.")
    # ---------------- painel 1: seção 1:20 ----------------
    sh.panel(60, 120, 900, 560, "Seção transversal do deck  -  terreno plano", "escala 1:20 (1 mm = 0,19 px)")
    k = 0.19
    t = Tr(140, 392, k)        # x em mm a partir da esquerda; y=0 nível do solo
    X, Y = t.x, t.y
    sh.add('<clipPath id="c4a"><rect x="62" y="148" width="896" height="530"/></clipPath>')
    sh.add('<g clip-path="url(#c4a)">')
    sh.soil(X(-400), Y(0), 4800 * k, 1600 * k)
    sh.line(X(-400), Y(0), X(4400), Y(0), 1.0, INK)
    zdeck = 600                 # topo das vigas U a 600 mm do solo
    piles = [(300, 1250), (2700, 1250)]
    for (px, Lp) in piles:
        # haste Ø76 com interrupção (L real 1,5 a 2,5 m)
        sh.rect(X(px - 38), Y(zdeck - 60), 76 * k, (zdeck - 60 + 700) * k, fill=BG, stroke=INK, sw=1.0)
        sh.break_line(X(px - 60), Y(-700), X(px + 60), Y(-700), 4)
        sh.rect(X(px - 38), Y(-850), 76 * k, (Lp - 850 - 40) * k, fill=BG, stroke=INK, sw=1.0)
        sh.pl([(X(px - 150), Y(-Lp + 160)), (X(px + 150), Y(-Lp + 80))], 1.6, INK)
        sh.pl([(X(px - 150), Y(-Lp + 80)), (X(px + 150), Y(-Lp + 0))], 0.9, INK)
        sh.pl([(X(px - 38), Y(-Lp + 40)), (X(px), Y(-Lp)), (X(px + 38), Y(-Lp + 40))], 1.0, INK, fill=BG)
        # cabeçote ajustável: rosca M36 com porca de travamento e chapa 150 x 150 x 8
        sh.rect(X(px - 18), Y(zdeck - 8), 36 * k, 200 * k, fill="url(#p-steel)", stroke=INK, sw=0.9)
        sh.rect(X(px - 32), Y(zdeck - 75), 64 * k, 22 * k, fill=INK, stroke="none")
        sh.rect(X(px - 75), Y(zdeck), 150 * k, 8 * k, fill=INK, stroke="none")
        # viga U 150 x 60 cortada sobre a chapa
        sh.pl([(X(px - 30), Y(zdeck + 150)), (X(px - 30), Y(zdeck + 8)), (X(px + 30), Y(zdeck + 8)), (X(px + 30), Y(zdeck + 150)),
               (X(px + 16), Y(zdeck + 150)), (X(px + 16), Y(zdeck + 130)), (X(px + 12), Y(zdeck + 130)), (X(px + 12), Y(zdeck + 146)),
               (X(px + 26), Y(zdeck + 146)), (X(px + 26), Y(zdeck + 12)), (X(px - 26), Y(zdeck + 12)), (X(px - 26), Y(zdeck + 146)),
               (X(px - 12), Y(zdeck + 146)), (X(px - 12), Y(zdeck + 130)), (X(px - 16), Y(zdeck + 130)), (X(px - 16), Y(zdeck + 150))],
              0.8, INK, fill=INK, close=True)
    # viga U longitudinal vista entre estacas (face da alma)
    sh.rect(X(-300), Y(zdeck + 150), 4300 * k, 150 * k, fill="none", stroke=INK, sw=0.9)
    sh.line(X(-300), Y(zdeck + 15), X(4000), Y(zdeck + 15), 0.4, INK, dash="4 3")
    sh.line(X(-300), Y(zdeck + 135), X(4000), Y(zdeck + 135), 0.4, INK, dash="4 3")
    # vigotas 50 x 150 @ 400 cortadas (interior até x = 2400; deck externo além)
    zj = zdeck + 150
    for i in range(11):
        xj = -100 + i * 400
        sh.wood(X(xj), Y(zj + 150), 50 * k, 150 * k, grain=False)
    # PIR 50 entre vigotas (só no interior) + manta de fechamento inferior
    for i in range(6):
        xj = -50 + i * 400
        sh.ins(X(xj), Y(zj + 50), 350 * k, 50 * k, "p-pir")
    sh.line(X(-100), Y(zj - 1), X(2350), Y(zj - 1), 2.0, GOLD)
    # linha da concha / parede em x = 2400 (dashed)
    sh.line(X(2400), Y(zj + 700), X(2400), Y(zdeck - 100), 0.7, GOLD, dash="8 4")
    sh.text(X(2400), Y(zj + 720), "borda da concha / parede", size=10, anchor="middle", color=GOLD)
    # compensado 18 + piso 14 (interior)
    sh.rect(X(-100), Y(zj + 168), 2500 * k, 18 * k, fill="url(#p-ply)", stroke=INK, sw=0.8)
    sh.rect(X(-100), Y(zj + 182), 2500 * k, 14 * k, fill="url(#p-wood)", stroke=INK, sw=0.8)
    # deck externo: ripas 20 x 140 com 6 mm de folga sobre vigotas próprias (as vigotas já desenhadas)
    xd = 2450
    while xd < 4200:
        sh.rect(X(xd), Y(zj + 150 + 20 + 12), 140 * k, 20 * k, fill="url(#p-wood)", stroke=INK, sw=0.8)
        xd += 146
    sh.rect(X(2420), Y(zj + 162), 1800 * k, 12 * k, fill=BG, stroke=INK, sw=0.5)     # calço 12 mm nivelando o deck
    # zona molhada opcional (nota)
    sh.add('</g>')
    # cotas
    sh.dim_h(X(300), X(2700), Y(-330), "2,40 m (malha de estacas)", ext=None, above=True)
    sh.dim_v(X(-250), Y(0), Y(zdeck), "≈ 600", ext=None, left=True, size=11)
    sh.dim_v(X(-250), Y(zdeck), Y(zj), "150", ext=None, left=True, size=11)
    sh.dim_v(X(-250), Y(zj), Y(zj + 150), "150", ext=None, left=True, size=11)
    sh.dim_v(X(-250), Y(zj + 150), Y(zj + 182), "32", ext=None, left=True, size=10)
    sh.dim_h(X(300), X(700), Y(zj + 260), "400", ext=Y(zj + 150), size=11)
    sh.dim_h(X(2450), X(2596), Y(zj + 260), "140 + 6", ext=Y(zj + 182), size=11)
    sh.dim_v(X(3900), Y(-1250), Y(0), "L = 1,5 a 2,5 m", ext=None, left=False, size=11)
    sh.dim_h(X(2550), X(2850), Y(-1080), "Ø300", ext=None, above=False, size=10)
    sh.text(X(1500), Y(-400), "solo natural: sem escavação, sem concreto", size=10.5, color=GOLD, anchor="middle")
    C = sh.callout
    C(1, X(300), Y(-400), X(-100), Y(-500))
    C(2, X(300), Y(-1150), X(700), Y(-1250))
    C(3, X(300), Y(zdeck + 100), X(-100), Y(zdeck - 350))
    C(4, X(2700), Y(zdeck + 4), X(3200), Y(zdeck - 350))
    C(5, X(2700), Y(zdeck + 80), X(3200), Y(zdeck + 30))
    C(6, X(1500), Y(zdeck + 75), X(1500), Y(zdeck - 350))
    C(7, X(725), Y(zj + 75), X(500), Y(zj + 450))
    C(8, X(1125), Y(zj + 25), X(900), Y(zj + 520))
    C(9, X(600), Y(zj), X(1300), Y(zj + 450))
    C(10, X(1500), Y(zj + 159), X(1700), Y(zj + 450))
    C(11, X(1900), Y(zj + 189), X(2100), Y(zj + 550))
    C(12, X(3400), Y(zj + 172), X(3600), Y(zj + 450))
    C(13, X(3700), Y(zj + 168), X(3900), Y(zj + 550))
    sh.scale_bar(90, 665, k, 1000, "1,0 m")

    # ---------------- painel 2: terreno inclinado 1:50 ----------------
    sh.panel(990, 120, 550, 560, "Variante  -  terreno inclinado (exemplo 10%)", "escala 1:50 (1 mm = 0,09 px)")
    k2 = 0.09
    t2 = Tr(1050, 428, k2)
    X2, Y2 = t2.x, t2.y
    sh.add('<clipPath id="c4b"><rect x="992" y="148" width="546" height="530"/></clipPath>')
    sh.add('<g clip-path="url(#c4b)">')
    # terreno: desce para a direita com 8% ao longo de 5,5 m
    slope = 0.10
    ground = [(x, 200 - slope * x) for x in range(0, 5601, 200)]
    poly = [(X2(a), Y2(b)) for a, b in ground] + [(X2(5600), Y2(-3000)), (X2(0), Y2(-3000))]
    sh.pl(poly, 0.9, INK, fill="url(#p-dots)", close=True)
    zd = 700     # topo das vigas
    piles2 = [(400, 1500), (2800, 2000), (5200, 2500)]
    for (px, Lp) in piles2:
        g = 200 - slope * px
        sh.rect(X2(px - 38), Y2(zd - 60), 76 * k2, (Lp + zd - g - 60) * k2, fill=BG, stroke=INK, sw=0.9)
        sh.pl([(X2(px - 150), Y2(g - Lp + 250)), (X2(px + 150), Y2(g - Lp + 170))], 1.4, INK)
        sh.rect(X2(px - 75), Y2(zd), 150 * k2, 8 * k2, fill=INK, stroke="none")
        sh.rect(X2(px - 30), Y2(zd + 150), 60 * k2, 150 * k2, fill=INK, stroke="none")
        sh.text(X2(px + (110 if px < 5000 else -110)), Y2(g - Lp + 60), "L %s m" % f(Lp / 1000), size=9.5, anchor=("start" if px < 5000 else "end"), color=GOLD)
    sh.rect(X2(100), Y2(zd + 150), 5400 * k2, 150 * k2, fill="none", stroke=INK, sw=0.8)
    sh.rect(X2(100), Y2(zd + 150 + 180), 5400 * k2, 180 * k2, fill="url(#p-ply)", stroke=INK, sw=0.8)
    sh.line(X2(100), Y2(zd + 330), X2(5500), Y2(zd + 330), 1.6, INK)
    # guarda-corpo em cabos inox no lado baixo (direita): montantes a cada 1,2 m, 5 cabos
    for xm in (5450, 4250, 3050):
        sh.rect(X2(xm - 20), Y2(zd + 330 + 1100), 40 * k2, 1100 * k2, fill=INK, stroke="none")
    for i in range(5):
        zc = zd + 330 + 180 + i * 200
        sh.line(X2(3050), Y2(zc), X2(5450), Y2(zc), 0.7, INK)
    sh.rect(X2(3050), Y2(zd + 330 + 1100 + 40), 2400 * k2, 40 * k2, fill="url(#p-wood)", stroke=INK, sw=0.8)   # corrimão de madeira
    sh.add('</g>')
    sh.dim_v(X2(5800), Y2(zd + 330), Y2(zd + 330 + 1100), "1,10", ext=None, left=False, size=10)
    sh.dim_v(X2(-150), Y2(200), Y2(200 - slope * 5600), "0,56 (10%)", ext=None, left=True, size=10)
    sh.dim_h(X2(400), X2(2800), Y2(200 - slope * 2800 - 300), "2,40", ext=None, above=False, size=10)
    sh.dim_h(X2(2800), X2(5200), Y2(200 - slope * 5200 - 300), "2,40", ext=None, above=False, size=10)
    sh.text(X2(1500), Y2(zd + 480), "deck nivelado", size=10, anchor="middle", color=GOLD)
    C(14, X2(4250), Y2(zd + 330 + 700), X2(3300), Y2(zd + 330 + 1300))
    C(15, X2(5200), Y2(zd - 300), X2(4500), Y2(zd - 600))
    sh.note(1010, 175, ["Mínima movimentação de terra; sistema removível.",
                        "Cabeçote ajustável (curso 150 mm) absorve desnível",
                        "até 8% sem corte; acima disso, estacas de",
                        "comprimentos diferentes (1,5 / 2,0 / 2,5 m).",
                        "Capacidade: 25 a 40 kN (compr.) / 15 a 25 kN (tração)."], size=10)

    items = [
        (1, "Estaca helicoidal galvanizada, haste Ø76 mm, instalada por motor hidráulico"),
        (2, "Hélice Ø300 mm (chapa 8 mm), ponta cônica; L = 1,5 a 2,5 m conforme sondagem"),
        (3, "Cabeçote ajustável rosqueado M36, curso 150 mm, porca de travamento"),
        (4, "Chapa do cabeçote 150 x 150 x 8 mm com 4 furos para a viga U"),
        (5, "Viga U enrijecida 150 x 60 x 3,0 mm galvanizada Z275 (cortada nas estacas)"),
        (6, "Viga U longitudinal (vista); malha 2,4 x 2,4 m (Cocoon) / 2,4 x 2,7 m (Zenith)"),
        (7, "Vigota de madeira tratada 50 x 150 mm @ 400 mm (pinus CCA-C ou eucalipto)"),
        (8, "Isolamento PIR 50 mm entre vigotas, encaixado"),
        (9, "Manta de fechamento inferior (respirável, anti-roedor) grampeada às vigotas"),
        (10, "Compensado naval 18 mm parafusado @ 150 mm nas bordas"),
        (11, "Piso de engenharia 14 mm (carvalho ou cumaru); zona molhada: cimentícia 12 + porcelanato"),
        (12, "Deck externo: cumaru ou termotratada 20 x 140 mm, folga 6 mm, fixação oculta"),
        (13, "Vigotas próprias do deck sobre calço 12 mm (nível do piso interno)"),
        (14, "Guarda-corpo: montantes de aço 40 x 40, 5 cabos inox Ø4 @ 200, corrimão de madeira"),
        (15, "Estaca mais longa no lado baixo; deck sempre nivelado"),
    ]
    sh.legend(60, 712, items, cols=2, colw=560, lh=18, size=11)
    sh.write("DET-04_fundacao.svg")


# ==================================================================================
# DET-05  Esquadrias
# ==================================================================================
def lens_pts(cx, cy, hw, hh, n=1.5, m=64):
    """Superelipse (lente) n = 1,5."""
    pts = []
    for i in range(m):
        t = 2 * math.pi * i / m
        c, s_ = math.cos(t), math.sin(t)
        x = cx + hw * (abs(c) ** (2 / n)) * (1 if c >= 0 else -1)
        y = cy + hh * (abs(s_) ** (2 / n)) * (1 if s_ >= 0 else -1)
        pts.append((x, y))
    return pts


def wall_layers(sh, X, Y, ang, x0, z0, L, sgn_out=-1, liner=True):
    """Camadas do envelope do Cocoon inclinadas (ang rad da vertical), começando em (x0,z0) subindo L mm.
    Exterior no lado sgn_out (x negativo = esquerda). Retorna função para offset."""
    ux, uz = math.sin(ang), math.cos(ang)        # ao longo da parede (para cima)
    nx, nz = sgn_out * math.cos(ang), -sgn_out * math.sin(ang)  # normal para fora
    def P(s, d):
        return (X(x0 + ux * s + nx * d), Y(z0 + uz * s + nz * d))
    # membrana (d = 0), câmara 60, manta 4, PET 50, câmara interna, forro a d = -196
    sh.membrane([P(0, 0), P(L, 0)])
    for (d1, d2, pat) in ((-60, -64, "p-steel"), (-64, -114, "p-ins")):
        sh.pl([P(0, d1), P(L, d1), P(L, d2), P(0, d2)], 0.6, INK, fill="url(#%s)" % pat, close=True)
    if liner:
        sh.pl([P(0, -196), P(L, -196)], 2.2, INK)
    return P


def det05():
    sh = Sheet("DET-05", "Esquadrias", "COMUM", "1:10 / 1:5 / 1:60",
               "(a) Janela Olho do Cocoon; (b) fachada de vidro inclinada 8° do Cocoon; (c) fachada frontal do Zenith; (d) fresta no painel SIP.")
    C = sh.callout
    # ---------------- (a) Janela Olho ----------------
    sh.panel(60, 120, 700, 350, "(a)  Janela Olho 1600 x 950: seção vertical e elevação", "1:10 (1 mm = 0,22 px) / 1:40")
    k = 0.22
    t = Tr(330, 410, k)     # origem: peitoril externo da janela (x=0, z=0). Exterior à esquerda.
    X, Y = t.x, t.y
    sh.add('<clipPath id="c5a"><rect x="62" y="148" width="696" height="320"/></clipPath>')
    sh.add('<g clip-path="url(#c5a)">')
    ang = math.radians(28)     # parede inclinada para dentro no topo
    ux, uz = math.sin(ang), math.cos(ang)
    nx, nz = -math.cos(ang), math.sin(ang)   # normal para fora (esquerda/cima)
    def P(s, d):
        return (X(ux * s + nx * d), Y(uz * s + nz * d))
    for (s0, s1) in ((-260, -20), (970, 1140)):
        sh.membrane([P(s0, 0), P(s1, 0)])
        for (d1, d2, pat) in ((-60, -64, "p-steel"), (-64, -114, "p-ins")):
            sh.pl([P(s0, d1), P(s1, d1), P(s1, d2), P(s0, d2)], 0.6, INK, fill="url(#%s)" % pat, close=True)
        sh.pl([P(s0, -196), P(s1, -196)], 2.2, INK)
    # requadro de madeira laminada 220 x 40 (peitoril e verga), perpendicular à parede
    for (s0, s1) in ((-20, 20), (930, 970)):
        sh.pl([P(s0, 10), P(s1, 10), P(s1, -210), P(s0, -210)], 1.6, INK, fill="url(#p-wood)", close=True)
    # grampo de alumínio da membrana no bordo externo do requadro + gaxeta
    sh.pl([P(-50, 12), P(-5, 12), P(-5, 4), P(-50, 4)], 0.8, INK, fill="url(#p-steel)", close=True)
    sh.pl([P(970, 12), P(1015, 12), P(1015, 4), P(970, 4)], 0.8, INK, fill="url(#p-steel)", close=True)
    # pingadeira de alumínio na verga (sobre o grampo)
    sh.pl([P(1020, 6), P(1020, 30), P(925, 30), P(925, 18)], 1.4, INK)
    # marco de alumínio com ruptura térmica 60 x 70 encaixado no requadro (terço externo)
    for (s0, s1) in ((20, 80), (870, 930)):
        sh.pl([P(s0, -40), P(s1, -40), P(s1, -110), P(s0, -110)], 1.0, INK, fill="url(#p-steel)", close=True)
        sh.pl([P(s0, -70), P(s1, -70), P(s1, -80), P(s0, -80)], 0.5, INK, fill=BG, close=True)   # ruptura poliamida
    sh.circle(P(870, -60)[0], P(870, -60)[1], 3, fill=INK, stroke="none")   # dobradiça superior
    p1, p2 = P(80, -75), P(870, -75)
    sh.glass(p1[0], p1[1], p2[0], p2[1], t=24 * k)
    a2 = ang + math.radians(15)
    L2 = 790
    hinge = P(870, -60)
    end = (hinge[0] - (L2 * k) * math.sin(a2), hinge[1] + (L2 * k) * math.cos(a2))
    sh.line(hinge[0], hinge[1], end[0], end[1], 0.7, INK, dash="5 3")
    sh.text((hinge[0] + end[0]) / 2 - 12, (hinge[1] + end[1]) / 2, "folha aberta 15°", size=9.5, anchor="end", color=GOLD)
    sh.circle(P(35, -35)[0], P(35, -35)[1], 2.2, fill=INK, stroke="none")
    sh.circle(P(915, -35)[0], P(915, -35)[1], 2.2, fill=INK, stroke="none")
    sh.line(P(-12, 8)[0], P(-12, 8)[1], P(-12, 30)[0], P(-12, 30)[1], 1.2, INK)   # friso pingadeira do peitoril
    sh.circle(P(60, -200)[0], P(60, -200)[1], 2.5, fill=GOLD, stroke="none")
    sh.circle(P(900, -200)[0], P(900, -200)[1], 2.5, fill=GOLD, stroke="none")
    sh.add('</g>')
    sh.dim_a(P(-20, -215)[0], P(-20, -215)[1], P(-20, 10)[0], P(-20, 10)[1], "220", off=14, size=10)
    sh.dim_a(P(20, -130)[0], P(20, -130)[1], P(930, -130)[0], P(930, -130)[1], "950 (vão)", off=-16, size=10)
    sh.text(X(-300), Y(560), "EXTERIOR", size=9.5, color=GOLD, ls="0.2em")
    sh.text(X(600), Y(300), "INTERIOR", size=9.5, color=GOLD, ls="0.2em")
    C(1, P(1060, 0)[0], P(1060, 0)[1], X(-70), Y(1000))
    C(2, P(0, -100)[0], P(0, -100)[1], X(60), Y(-150))
    C(3, P(50, -75)[0], P(50, -75)[1], X(250), Y(-90))
    C(4, P(500, -75)[0], P(500, -75)[1], X(140), Y(700))
    C(5, P(875, -62)[0], P(875, -62)[1], X(760), Y(520))
    C(6, P(995, 8)[0], P(995, 8)[1], X(150), Y(1060))
    C(7, P(-12, 20)[0], P(-12, 20)[1], X(-230), Y(130))
    C(8, P(1080, -196)[0], P(1080, -196)[1], X(540), Y(1080))
    C(9, P(60, -200)[0], P(60, -200)[1], X(340), Y(-30))
    # elevação da lente 1:40
    lk = 0.1
    cx, cy = 650, 300
    sh.pl(lens_pts(cx, cy, 800 * lk, 475 * lk), 1.2, INK, fill=GLASS, close=True)
    sh.pl(lens_pts(cx, cy, 800 * lk + 22, 475 * lk + 22), 0.8, INK, close=True)
    sh.dim_h(cx - 80, cx + 80, cy - 80, "1600", ext=None, size=10)
    sh.dim_v(cx + 108, cy - 47.5, cy + 47.5, "950", ext=None, left=False, size=10)
    sh.text(cx, cy + 90, "elevação 1:40 (lente, n = 1,5)", size=9.5, anchor="middle", color=GOLD)

    # ---------------- (b) fachada de vidro do Cocoon ----------------
    sh.panel(790, 120, 750, 350, "(b)  Fachada de vidro Cocoon inclinada 8°: elevação e detalhes", "1:60 / 1:5")
    ek = 0.065
    ex, ey = 990, 452
    pts = [(ex + p[0] * 1000 * ek, ey - p[1] * 1000 * ek) for p in COC.arch_pts(1.0, 100)]
    sh.pl(pts, 1.6, INK, fill="none")
    sh.line(pts[0][0], ey, pts[-1][0], ey, 1.6, INK)
    inner = [(ex + p[0] * 1000 * ek * 0.955, ey - (p[1] * 1000 - 40) * ek * 0.96) for p in COC.arch_pts(1.0, 100)]
    sh.pl(inner, 0.8, INK, fill=GLASS)
    for xm in (-1700, -600, 500):
        top_z = COC.ZC + COC.b(1.0) * math.sqrt(max(0, 1 - (xm / 1000 / COC.a(1.0)) ** 2))
        sh.line(ex + xm * ek, ey, ex + xm * ek, ey - top_z * 1000 * ek + 6, 1.2, INK)
    sh.rect(ex + 500 * ek, ey - 2400 * ek, 1000 * ek, 2400 * ek, fill="none", stroke=INK, sw=1.4)
    sh.line(ex + 500 * ek, ey - 2400 * ek, ex + 1500 * ek, ey, 0.5, INK)
    sh.circle(ex + 640 * ek, ey - 1100 * ek, 2.2, fill=INK, stroke="none")
    sh.line(ex - 2700 * ek, ey - 800 * ek, ex + 2700 * ek, ey - 800 * ek, 0.4, GOLD, dash="4 3")
    sh.line(ex - 2300 * ek, ey - 2200 * ek, ex + 2300 * ek, ey - 2200 * ek, 0.4, GOLD, dash="4 3")
    sh.dim_h(ex + 500 * ek, ex + 1500 * ek, ey + 12, "1000", ext=None, above=False, size=9.5)
    sh.dim_v(ex + 1650 * ek, ey - 2400 * ek, ey, "2400", ext=None, left=False, size=9.5)
    sh.text(802, 163, "elevação 1:60, plano inclinado 8°, vão ≈ 5,6 x 3,9 m", size=9.5, color=GOLD)
    C(10, ex - 2400 * ek, ey - 2000 * ek, ex - 2900 * ek, ey - 900 * ek)
    C(11, ex - 600 * ek, ey - 1500 * ek, ex - 1100 * ek, ey - 400 * ek)
    C(12, ex + 1000 * ek, ey - 1800 * ek, ex + 2200 * ek, ey - 2900 * ek)
    # detalhe topo 1:5
    k5 = 0.5
    t5 = Tr(1310, 262, k5)
    X5, Y5 = t5.x, t5.y
    sh.text(1240, 168, "detalhe topo  1:5", size=9.5, color=GOLD)
    sh.tube_cut(X5(0), Y5(0), 50.8 * k5, 4 * k5)
    sh.rect(X5(-20), Y5(51), 40 * k5, 22 * k5, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.membrane([(X5(0), Y5(73)), (X5(80), Y5(78)), (X5(260), Y5(60))])
    sh.add('<g transform="rotate(-8 %.1f %.1f)">' % (X5(0), Y5(-50)))
    sh.rect(X5(-60), Y5(-50), 120 * k5, 60 * k5, fill="url(#p-steel)", stroke=INK, sw=1.0)
    sh.rect(X5(-12), Y5(-110), 24 * k5, 120 * k5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.rect(X5(-40), Y5(-110), 80 * k5, 18 * k5, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.add('</g>')
    sh.bolt_side(X5(-35), Y5(-52), 35 * k5, 4, vertical=True)
    sh.bolt_side(X5(35), Y5(-52), 35 * k5, 4, vertical=True)
    sh.label(X5(-30), Y5(30), X5(-80), Y5(60), "anel A0 Ø101,6 x 4, inclinado 8°", size=9.5, anchor="end")
    sh.label(X5(-58), Y5(-80), X5(-100), Y5(-120), "anel alumínio 120 x 60 curvo", size=9.5, anchor="end")
    sh.label(X5(-5), Y5(-190), X5(-60), Y5(-215), "vidro 6 lam + 12 Ar + 6 temp", size=9.5, anchor="end")
    sh.label(X5(170), Y5(69), X5(190), Y5(110), "membrana da concha", size=9.5, anchor="start")
    # detalhe soleira 1:5
    t6 = Tr(1462, 430, k5)
    X6, Y6 = t6.x, t6.y
    sh.text(1395, 320, "detalhe soleira  1:5", size=9.5, color=GOLD)
    sh.rect(X6(-140), Y6(0), 280 * k5, 18 * k5, fill="url(#p-ply)", stroke=INK, sw=0.8)
    sh.wood(X6(-140), Y6(14), 80 * k5, 14 * k5, grain=False)
    sh.rect(X6(-60), Y6(14), 120 * k5, 14 * k5, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.rect(X6(-50), Y6(0), 100 * k5, 60 * k5, fill=BG, stroke=INK, sw=1.0)
    sh.rect(X6(-45), Y6(-4), 90 * k5, 50 * k5, fill="url(#p-steel)", stroke="none")
    sh.rect(X6(-8), Y6(14 + 60), 16 * k5, 60 * k5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.rect(X6(-14), Y6(14 + 12), 28 * k5, 12 * k5, fill=INK, stroke="none")
    sh.wood(X6(60), Y6(14), 80 * k5, 14 * k5, grain=False)
    sh.label(X6(0), Y6(-30), X6(-70), Y6(-52), "mola de piso 100 x 60", size=9.5, anchor="end")
    sh.label(X6(4), Y6(60), X6(30), Y6(90), "porta pivotante", size=9.5, anchor="start")

    # ---------------- (c) fachada frontal do Zenith ----------------
    sh.panel(60, 485, 700, 320, "(c)  Fachada frontal Zenith 5400 x 2750: 2 fixas + 2 de correr", "1:50 / 1:5")
    fk = 0.075
    fx, fy = 300, 782
    sh.rect(fx - 2700 * fk, fy - 2750 * fk, 5400 * fk, 2750 * fk, fill=GLASS, stroke=INK, sw=1.4)
    for i in range(1, 4):
        xx = fx - 2700 * fk + i * 1350 * fk
        sh.line(xx, fy - 2750 * fk, xx, fy, 1.0, INK)
    sh.rect(fx - 1350 * fk, fy - 2750 * fk + 4, 1350 * fk, 2750 * fk - 8, fill="none", stroke=INK, sw=0.5)
    sh.rect(fx, fy - 2750 * fk + 4, 1350 * fk, 2750 * fk - 8, fill="none", stroke=INK, sw=0.5)
    sh.arrow(fx - 1200 * fk, fy - 1400 * fk, fx - 300 * fk, fy - 1400 * fk, 0.9, GOLD, head=6)
    sh.arrow(fx + 1200 * fk, fy - 1400 * fk, fx + 300 * fk, fy - 1400 * fk, 0.9, GOLD, head=6)
    sh.text(fx - 2025 * fk, fy - 1400 * fk, "FIXA", size=9, anchor="middle", color=GOLD)
    sh.text(fx + 2025 * fk, fy - 1400 * fk, "FIXA", size=9, anchor="middle", color=GOLD)
    sh.line(fx - 2900 * fk, fy, fx + 2900 * fk, fy, 1.6, INK)
    sh.dim_h(fx - 2700 * fk, fx + 2700 * fk, fy + 14, "5400 (4 x 1350)", ext=None, above=False, size=9.5)
    sh.dim_v(fx - 2850 * fk, fy - 2750 * fk, fy, "2750", ext=None, left=True, size=9.5)
    C(13, fx - 2025 * fk, fy - 2300 * fk, fx - 2400 * fk, fy - 3000 * fk)
    C(14, fx + 600 * fk, fy - 2300 * fk, fx + 900 * fk, fy - 3000 * fk)
    C(15, fx + 1900 * fk, fy, fx + 2500 * fk, fy - 500 * fk)
    # detalhe soleira 1:5
    t7 = Tr(650, 700, 0.5)
    X7, Y7 = t7.x, t7.y
    sh.text(540, 530, "soleira com drenagem  1:5", size=9.5, color=GOLD)
    sh.add('<clipPath id="c5c"><rect x="535" y="535" width="223" height="268"/></clipPath>')
    sh.add('<g clip-path="url(#c5c)">')
    sh.wood(X7(-220), Y7(0), 200 * 0.5, 20 * 0.5, grain=False)
    sh.rect(X7(-220), Y7(-20), 200 * 0.5, 18 * 0.5, fill="url(#p-ply)", stroke=INK, sw=0.6)
    sh.wood(X7(60), Y7(0), 200 * 0.5, 14 * 0.5, grain=False)
    sh.rect(X7(60), Y7(-14), 200 * 0.5, 18 * 0.5, fill="url(#p-ply)", stroke=INK, sw=0.6)
    sh.rect(X7(-240), Y7(-38), 520 * 0.5, 150 * 0.5, fill="url(#p-ply)", stroke=INK, sw=0.8)
    sh.pl([(X7(-20), Y7(0)), (X7(-20), Y7(-40)), (X7(60), Y7(-40)), (X7(60), Y7(0))], 1.4, INK, fill=BG)
    for xg in (0, 40):
        sh.rect(X7(xg - 3), Y7(-2), 6 * 0.5, 14 * 0.5, fill=INK, stroke="none")
    sh.rect(X7(-12), Y7(120), 24 * 0.5, 108 * 0.5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.rect(X7(-14), Y7(20), 28 * 0.5, 22 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.6)
    sh.circle(X7(0), Y7(6), 4, fill=BG, stroke=INK, sw=0.8)
    sh.rect(X7(28), Y7(120), 24 * 0.5, 130 * 0.5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.rect(X7(26), Y7(0), 28 * 0.5, 12 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.6)
    sh.line(X7(-20), Y7(-38), X7(-120), Y7(-70), 1.2, INK)
    sh.line(X7(-20), Y7(-42), X7(-120), Y7(-74), 1.2, INK)
    sh.arrow(X7(-60), Y7(-54), X7(-110), Y7(-70), 0.9, GOLD, head=5)
    sh.arrow(X7(-200), Y7(30), X7(-120), Y7(30), 0.9, GOLD, head=5, dash="3 2")
    sh.add('</g>')
    sh.label(X7(50), Y7(-40), X7(90), Y7(-98), "trilho embutido 120 x 40", size=9.5, anchor="end")
    sh.label(X7(-90), Y7(-62), X7(-110), Y7(-125), "dreno Ø20 à calha", size=9.5, anchor="end")
    sh.label(X7(-12), Y7(60), X7(-60), Y7(80), "roldana inox (correr)", size=9.5, anchor="end")
    sh.label(X7(40), Y7(100), X7(70), Y7(150), "folha fixa", size=9.5, anchor="start")
    sh.text(X7(-215), Y7(40), "deck", size=9.5, color=GOLD)
    sh.text(X7(150), Y7(40), "piso", size=9.5, color=GOLD)

    # ---------------- (d) fresta no painel SIP ----------------
    sh.panel(790, 485, 750, 320, "(d)  Fresta de vidro no painel SIP 100 com rufos", "1:5 (1 mm = 0,5 px)")
    t8 = Tr(1080, 735, 0.5)
    X8, Y8 = t8.x, t8.y
    sh.add('<clipPath id="c5d"><rect x="792" y="513" width="746" height="290"/></clipPath>')
    sh.add('<g clip-path="url(#c5d)">')
    def sip(z0, z1):
        h = (z1 - z0) * 0.5
        sh.rect(X8(-50), Y8(z1), 12 * 0.5, h, fill="url(#p-osb)", stroke=INK, sw=0.8)
        sh.rect(X8(38), Y8(z1), 12 * 0.5, h, fill="url(#p-osb)", stroke=INK, sw=0.8)
        sh.rect(X8(-38), Y8(z1), 76 * 0.5, h, fill="url(#p-pir)", stroke="none")
        sh.rect(X8(-62), Y8(z1), 12 * 0.5, h, fill="url(#p-cem)", stroke=INK, sw=0.8)
        sh.rect(X8(-87), Y8(z1), 25 * 0.5, h, fill=BG, stroke=INK, sw=0.5)
        sh.rect(X8(50), Y8(z1), 20 * 0.5, h, fill=BG, stroke=INK, sw=0.5)
        sh.wood(X8(70), Y8(z1), 15 * 0.5, h, grain=False)
    sip(-120, -20)
    sip(320, 440)
    for zz in range(-150, 440, 80):
        if -40 < zz < 330:
            continue
        sh.wood(X8(-127), Y8(zz + 40), 40 * 0.5, 40 * 0.5, grain=False)
    sh.wood(X8(-50), Y8(0), 100 * 0.5, 20 * 0.5, grain=False)
    sh.wood(X8(-50), Y8(320), 100 * 0.5, 20 * 0.5, grain=False)
    sh.rect(X8(-45), Y8(60), 60 * 0.5, 60 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.rect(X8(-45), Y8(300), 60 * 0.5, 60 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.rect(X8(-27), Y8(240), 24 * 0.5, 180 * 0.5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.pl([(X8(-62), Y8(420)), (X8(-62), Y8(330)), (X8(-100), Y8(322)), (X8(-100), Y8(310))], 1.4, INK)
    sh.pl([(X8(-45), Y8(62)), (X8(-100), Y8(40)), (X8(-100), Y8(28))], 1.4, INK)
    sh.pl([(X8(-62), Y8(62)), (X8(-62), Y8(-60))], 1.4, INK)
    for zz in (62, 298):
        sh.circle(X8(-48), Y8(zz), 2.2, fill=INK, stroke="none")
    sh.arrow(X8(-110), Y8(300), X8(-118), Y8(250), 0.9, GOLD, head=5)
    sh.arrow(X8(-110), Y8(35), X8(-118), Y8(-10), 0.9, GOLD, head=5)
    sh.add('</g>')
    sh.dim_v(X8(-180), Y8(60), Y8(300), "300", ext=None, left=True, size=10)
    sh.dim_h(X8(-50), X8(50), Y8(-135), "SIP 100", ext=None, above=True, size=10)
    sh.text(X8(-380), Y8(250), "EXTERIOR", size=9.5, color=GOLD, ls="0.2em")
    sh.text(X8(140), Y8(180), "INTERIOR", size=9.5, color=GOLD, ls="0.2em")
    C(16, X8(-15), Y8(330), X8(170), Y8(420))
    C(17, X8(-15), Y8(200), X8(170), Y8(300))
    C(18, X8(-90), Y8(318), X8(-240), Y8(400))
    C(19, X8(-80), Y8(48), X8(-240), Y8(-20))
    C(20, X8(-107), Y8(120), X8(-240), Y8(140))
    C(21, X8(0), Y8(10), X8(170), Y8(60))

    items = [
        (1, "Envelope: membrana + câmara 60 + manta + lã PET 50 + forro"),
        (2, "Requadro em madeira laminada 220 x 40 (anel da lente)"),
        (3, "Marco de alumínio com ruptura térmica 60 x 70, bronze"),
        (4, "Vidro duplo 6 lam + 12 Ar + 6 temp, low-e (U 1,6)"),
        (5, "Basculante de projeção: dobradiça superior + braços de fricção"),
        (6, "Grampo de alumínio da membrana + gaxeta EPDM + pingadeira"),
        (7, "Peitoril inclinado 5% com friso pingadeira; canal de condensação"),
        (8, "Forro tensionado fechando no requadro"),
        (9, "Fita LED 2700 K oculta no requadro"),
        (10, "Anel A0 Ø101,6 x 4,0 a 8° com anel de alumínio 120 x 60 curvo"),
        (11, "Montantes de alumínio 60 x 120 RPT; travessas a 0,8 e 2,2 m"),
        (12, "Porta pivotante de vidro 1000 x 2400 com mola de piso"),
        (13, "Folha fixa 1350 x 2750 (vidro duplo)"),
        (14, "Folha de correr 1350 x 2750, roldanas inox, fecho multiponto"),
        (15, "Trilho embutido nivelado com deck e piso; dreno à calha"),
        (16, "Marco de alumínio RPT 60 x 60 fixado ao requadro de madeira"),
        (17, "Vidro duplo 6 + 12 + 6 (fresta fixa, 300 mm de altura)"),
        (18, "Rufo de verga: alumínio 1,5 mm atrás da cimentícia, pingadeira"),
        (19, "Rufo de peitoril inclinado, aba vertical 120 mm"),
        (20, "Câmara ventilada 25 mm com tela anti-inseto"),
        (21, "Requadro de madeira 40 mm selando o núcleo PIR (selante + tarucel)"),
    ]
    sh.legend(60, 828, items, cols=3, colw=323, lh=14, size=9.5, title=None)
    sh.write("DET-05_esquadrias.svg")


# ==================================================================================
# DET-06  Drenagem
# ==================================================================================
def flow_arrow(sh, x1, y1, x2, y2):
    sh.arrow(x1, y1, x2, y2, 0.8, GOLD, head=5)


def det06():
    sh = Sheet("DET-06", "Drenagem pluvial", "COMUM", "1:100 (plantas) / 1:6 (seções)",
               "Escoamento da membrana, calhas ocultas, tubos de queda Ø75, pingadeiras e dispersão. Chuva de projeto 150 mm/h.")
    C = sh.callout
    # ---------------- planta Cocoon ----------------
    sh.panel(60, 120, 520, 470, "Planta  -  ZION COCOON", "1:100 (1 m = 40 px)")
    k = 40
    X, Y = cocoon_plan(sh, 200, 380, k, rooms=False, furniture=False, labels=False)
    sh.north(540, 170)
    # setas de escoamento: da cumeeira para os rodapés (laterais)
    for xm in (1.2, 2.4, 3.6, 4.8, 6.0, 7.2, 8.2):
        a = COC.a(xm)
        flow_arrow(sh, X(xm), Y(0.35), X(xm), Y(a * 0.85))
        flow_arrow(sh, X(xm), Y(-0.35), X(xm), Y(-a * 0.85))
    sh.line(X(0.5), Y(0), X(9.0), Y(0), 0.6, INK, dash="6 3")
    sh.text(X(4.6), Y(0.12), "cumeeira / Espinha de Luz", size=9, anchor="middle", color=GOLD)
    # calhas ocultas nos rodapés (linha tracejada grossa acompanhando a borda da concha, ambos os lados)
    xs = np.linspace(0.6, 8.9, 60)
    for sg in (1, -1):
        sh.pl([(X(x), Y(sg * (COC.a(x) - 0.12))) for x in xs], 2.0, GOLD, dash="6 3")
    # tubos de queda Ø75 nas extremidades (frente e cauda), caixas de brita
    for (xd, yd) in ((0.7, 2.3), (0.7, -2.3), (8.6, 1.2), (8.6, -1.2)):
        sh.circle(X(xd), Y(yd), 5, fill=BG, stroke=INK, sw=1.2)
        sh.circle(X(xd), Y(yd), 1.8, fill=INK, stroke="none")
    for (xd, yd, bx, by) in ((0.7, 2.3, -0.4, 3.6), (0.7, -2.3, -0.4, -3.6), (8.6, 1.2, 10.2, 2.4), (8.6, -1.2, 10.2, -2.4)):
        sh.line(X(xd), Y(yd), X(bx), Y(by), 1.2, INK, dash="4 2")
        sh.rect(X(bx) - 16, Y(by) - 12, 32, 24, fill="url(#p-gravel)", stroke=INK, sw=0.8)
    # ligação à cisterna / dispersão
    sh.line(X(10.2), Y(2.4), X(10.2), Y(-2.4), 1.0, INK, dash="4 2")
    sh.rect(X(10.6), Y(0.5), 30, 40, fill=BG, stroke=INK, sw=1.0, rx=3)
    sh.text(X(10.6) + 15, Y(0) + 4, "CIST", size=7.5, anchor="middle", color=INK)
    sh.line(X(10.2), Y(0), X(10.6), Y(0), 1.0, INK, dash="4 2")
    # cauda: condensadora não interfere; nota
    C(1, X(2.4), Y(1.6), X(3.5), Y(3.4))
    C(2, X(4.8), Y(COC.a(4.8) - 0.12), X(6.0), Y(3.6))
    C(3, X(0.7), Y(2.3), X(1.8), Y(3.9))
    C(4, X(-0.4), Y(3.6), X(-1.4), Y(2.6))
    C(5, X(10.6), Y(0.5), X(9.9), Y(-3.2))
    sh.text(X(-2.9), Y(-4.35), "deck: ripas com folga 6 mm drenam livremente", size=9, color=GOLD)

    # ---------------- planta Zenith ----------------
    sh.panel(600, 120, 620, 470, "Planta  -  ZION ZENITH", "1:100 (1 m = 40 px)")
    X2, Y2 = zenith_plan(sh, 760, 372, k, rooms=False, furniture=False, labels=False)
    # setas radiais dos cumes
    for (px, py) in ((6.3, 0.4), (1.6, 1.6)):
        for a in range(0, 360, 45):
            r0, r1 = 0.9, 2.1
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            flow_arrow(sh, X2(px + r0 * ca), Y2(py + r0 * sa), X2(px + r1 * ca), Y2(py + r1 * sa))
    # vale entre cumes (linha)
    sh.line(X2(3.9), Y2(3.7), X2(4.1), Y2(-3.7), 0.6, INK, dash="6 3")
    sh.text(X2(4.0), Y2(3.9), "vale", size=9, anchor="middle", color=GOLD)
    # calhas ocultas no anel de beiral, laterais do corpo
    for yy in (2.7, -2.7):
        sh.line(X2(0.2), Y2(yy), X2(9.3), Y2(yy), 2.0, GOLD, dash="6 3")
    # tubos de queda dentro de 2 pilares (3,2; -2,7) e (6,4; 2,7)
    for (xd, yd) in ((3.2, -2.7), (6.4, 2.7)):
        sh.circle(X2(xd), Y2(yd), 5, fill=BG, stroke=INK, sw=1.2)
        sh.circle(X2(xd), Y2(yd), 1.8, fill=INK, stroke="none")
    # pingadeiras nos pontos baixos das catenárias (meio de cada vão) sobre canaletas de brita
    lows = [(-2.4, 0.0), (0.8, -3.7), (7.25, -3.7), (0.8, 3.7), (7.25, 3.7), (10.5, 1.85), (10.5, -1.85)]
    for (lx, ly) in lows:
        sh.pl([(X2(lx) - 5, Y2(ly) - 5), (X2(lx), Y2(ly) + 4), (X2(lx) + 5, Y2(ly) - 5)], 0.9, GOLD, fill=GOLD, close=True)
    # canaletas de brita ao longo das bordas (fora do contorno)
    sh.rect(X2(-2.9), Y2(4.2), 13.9 * k, 0.4 * k, fill="url(#p-gravel)", stroke=INK, sw=0.6)
    sh.rect(X2(-2.9), Y2(-3.8), 13.9 * k, 0.4 * k, fill="url(#p-gravel)", stroke=INK, sw=0.6)
    sh.rect(X2(10.6), Y2(4.2), 0.4 * k, 8.4 * k, fill="url(#p-gravel)", stroke=INK, sw=0.6)
    sh.rect(X2(-3.3), Y2(4.2), 0.4 * k, 8.4 * k, fill="url(#p-gravel)", stroke=INK, sw=0.6)
    # ligação dos tubos de queda a caixas de brita / cisterna
    sh.line(X2(3.2), Y2(-2.7), X2(3.2), Y2(-4.6), 1.2, INK, dash="4 2")
    sh.line(X2(6.4), Y2(2.7), X2(6.4), Y2(4.6), 1.2, INK, dash="4 2")
    sh.rect(X2(3.2) - 16, Y2(-4.6) - 12, 32, 24, fill="url(#p-gravel)", stroke=INK, sw=0.8)
    sh.rect(X2(6.4) - 16, Y2(4.6) - 12, 32, 24, fill="url(#p-gravel)", stroke=INK, sw=0.8)
    C(6, X2(7.4), Y2(1.5), X2(8.6), Y2(0.2))
    C(7, X2(4.8), Y2(-2.7), X2(5.4), Y2(-4.6))
    C(8, X2(3.2), Y2(-2.7), X2(2.2), Y2(-4.6))
    C(9, X2(7.25), Y2(3.7), X2(8.4), Y2(4.9))
    C(10, X2(10.8), Y2(2.0), X2(11.6), Y2(3.4))
    C(11, X2(-1.55), Y2(-2.05), X2(-1.0), Y2(-4.0))
    sh.north(1180, 170)

    # ---------------- seções das calhas 1:5 ----------------
    sh.panel(1240, 120, 300, 470, "Calha oculta 80 mm", "seções 1:6")
    # (i) rodapé do Cocoon
    sh.text(1252, 160, "no trilho de base (Cocoon)", size=9.5, color=GOLD)
    kk = 0.4
    ta = Tr(1400, 300, kk)
    XA, YA = ta.x, ta.y
    sh.rect(XA(-25), YA(100), 50 * kk, 100 * kk, fill=BG, stroke=INK, sw=1.4)     # trilho 100 x 50
    sh.rect(XA(-22), YA(97), 44 * kk, 94 * kk, fill=BG, stroke=INK, sw=0.5)
    sh.rect(XA(-55), YA(100), 30 * kk, 26 * kk, fill="url(#p-steel)", stroke=INK, sw=0.8)   # grampo keder
    sh.circle(XA(-44), YA(89), 5 * kk, fill=GOLD, stroke=INK, sw=0.6)
    sh.membrane([(XA(-48), YA(94)), (XA(-40), YA(117)), (XA(30), YA(240))])
    sh.pl([(XA(-55), YA(74)), (XA(-55), YA(22)), (XA(-135), YA(22)), (XA(-135), YA(82))], 1.4, INK)   # calha 80 x 60
    sh.rect(XA(-160), YA(0), 300 * kk, 18 * kk, fill="url(#p-ply)", stroke=INK, sw=0.6)                   # compensado
    sh.wood(XA(-260), YA(20), 100 * kk, 20 * kk, grain=False)                                            # deck
    sh.wood(XA(25), YA(14), 110 * kk, 14 * kk, grain=False)                                              # piso interno
    sh.arrow(XA(-70), YA(105), XA(-95), YA(45), 0.9, GOLD, head=5)
    sh.line(XA(-95), YA(22), XA(-95), YA(-40), 1.2, INK, dash="4 2")   # saída ao tubo Ø75
    sh.arrow(XA(-95), YA(-5), XA(-95), YA(-38), 0.9, GOLD, head=5)
    sh.dim_h(XA(-135), XA(-55), YA(-15), "80", ext=None, above=False, size=9.5)
    sh.text(XA(-115), YA(-60), "Ø75", size=9, anchor="middle", color=GOLD)
    sh.text(XA(-240), YA(80), "ext.", size=9, color=GOLD)
    sh.text(XA(60), YA(50), "int.", size=9, color=GOLD)
    C(12, XA(-95), YA(50), XA(-200), YA(150))
    C(13, XA(-44), YA(89), XA(-70), YA(200))
    # (ii) beiral do Zenith
    sh.text(1252, 392, "no anel de beiral (Zenith)", size=9.5, color=GOLD)
    tb = Tr(1440, 505, kk)
    XB, YB = tb.x, tb.y
    sh.rect(XB(-50), YB(0), 100 * kk, 150 * kk, fill=BG, stroke=INK, sw=1.4)   # anel 150 x 100
    sh.rect(XB(-46), YB(-4), 92 * kk, 142 * kk, fill=BG, stroke=INK, sw=0.5)
    sh.pl([(XB(-50), YB(0)), (XB(-50), YB(-40)), (XB(-90), YB(-40)), (XB(-90), YB(-10)), (XB(-80), YB(0))], 1.0, INK, fill="url(#p-steel)", close=True)
    sh.rect(XB(-20), YB(0), 40 * kk, 24 * kk, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.membrane([(XB(130), YB(24 + 130 * 0.53)), (XB(-8), YB(26)), (XB(-60), YB(25)), (XB(-90), YB(5)), (XB(-98), YB(-20))])
    sh.pl([(XB(-90), YB(-42)), (XB(-90), YB(-110)), (XB(-170), YB(-110)), (XB(-170), YB(-50))], 1.4, INK)
    sh.pl([(XB(-98), YB(-20)), (XB(-178), YB(-20)), (XB(-178), YB(-130)), (XB(-150), YB(-130))], 1.6, INK)
    sh.rect(XB(-190), YB(-130), 40 * kk, 22 * kk, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.membrane([(XB(-186), YB(-152)), (XB(-300), YB(-175))])
    sh.arrow(XB(-105), YB(-30), XB(-120), YB(-95), 0.9, GOLD, head=5)
    sh.rect(XB(-90), YB(-95), 45 * kk, 14 * kk, fill=BG, stroke=INK, sw=0.7)   # saída Ø50 ao pilar
    sh.line(XB(-37.5), YB(-150), XB(-37.5), YB(-180), 0.8, INK, dash="5 3")
    sh.line(XB(37.5), YB(-150), XB(37.5), YB(-180), 0.8, INK, dash="5 3")
    sh.arrow(XB(0), YB(-155), XB(0), YB(-178), 0.9, GOLD, head=5)
    sh.text(XB(0), YB(-198), "Ø75 no pilar", size=9, anchor="middle", color=GOLD)
    sh.dim_h(XB(-170), XB(-90), YB(-125), "80", ext=None, above=False, size=9.5)
    C(14, XB(-130), YB(-80), XB(-250), YB(-60))

    # ---------------- tabela de vazões ----------------
    sh.text(60, 630, "VAZÕES DE PROJETO  (i = 150 mm/h; Q = A x i / 3600)", size=11, color=GOLD, ls="0.2em", weight=600)
    rows = [
        ("Cocoon: concha completa", "45,5", "6,83", "1,90", "2 x Ø75 (extremidades)", "0,95"),
        ("Cocoon: por lado (rodapé)", "22,8", "3,41", "0,95", "1 x Ø75 por lado", "0,95"),
        ("Zenith: faixas laterais às calhas", "2 x 24,0", "2 x 3,60", "2 x 1,00", "Ø75 em 2 pilares", "1,00"),
        ("Zenith: balanço frontal (catenária)", "17,8", "2,67", "0,74", "pingadeiras e canaleta", "-"),
        ("Zenith: balanços laterais e fundos", "29,7", "4,46", "1,24", "pingadeiras e canaleta", "-"),
    ]
    sh.table(60, 655, ["Superfície", "A (m²)", "Q (m³/h)", "Q (L/s)", "Destino", "Q/tubo (L/s)"], rows,
             [230, 80, 90, 80, 190, 100], size=11, lh=19)
    sh.texts(60, 785, [
        "Capacidade de um tubo de queda Ø75 mm (NBR 10844, condutor vertical): ≈ 2,3 L/s > 1,00 L/s de projeto (folga > 2x).",
        "Calha oculta 80 x 60 mm com declividade 0,5% para os tubos; vazão máxima ≈ 1,6 L/s por trecho de calha.",
        "Dispersão: caixa de brita 0,6 x 0,6 x 0,8 m por tubo (solo permeável) ou cisterna 2.000 L para reuso em irrigação e descargas.",
        "Deck e passarela: ripas com folga 6 mm; solo sob o deck protegido com manta geotêxtil + brita 5 cm.",
    ], size=10.5, lh=16)
    items = [
        (1, "Escoamento da membrana da cumeeira aos rodapés (inclinação mínima 12°)"),
        (2, "Calha oculta de alumínio 80 mm no trilho de base, ambos os lados"),
        (3, "Tubo de queda Ø75 mm nas extremidades da concha (4 pontos)"),
        (4, "Caixa de brita 0,6 x 0,6 x 0,8 m (dispersão no solo)"),
        (5, "Cisterna opcional 2.000 L (reuso) sob o deck da cauda"),
        (6, "Escoamento radial dos dois cumes; vale entre eles drena às bordas"),
        (7, "Calha oculta no anel de beiral, laterais do corpo (2 x 9,1 m)"),
        (8, "Tubo de queda Ø75 dentro de 2 pilares Ø101,6 (x 3,2 e x 6,4)"),
        (9, "Pingadeira no ponto baixo de cada catenária entre postes"),
        (10, "Canaleta de brita 40 cm sob as bordas em balanço"),
        (11, "Hidromassagem sob o beiral: extravasor ligado à rede de esgoto"),
        (12, "Calha 80 x 60 com saída Ø75; tela de folhas removível"),
        (13, "Membrana clamped no grampo keder; pingadeira lança na calha"),
        (14, "Calha do beiral com saída Ø50 e tubo Ø75 dentro do pilar (ver DET-02)"),
    ]
    sh.legend(960, 626, items, cols=1, colw=300, lh=16.5, size=9.5)
    sh.write("DET-06_drenagem.svg")


# ==================================================================================
# DET-07  Elétrica
# ==================================================================================
def sym_socket(sh, x, y, usb=False, ext=False):
    sh.circle(x, y, 5, fill=BG, stroke=INK, sw=1.0)
    sh.line(x - 5, y, x + 5, y, 1.0, INK)
    sh.line(x, y - 5, x, y - 9, 1.0, INK)
    if usb:
        sh.text(x + 7, y + 3, "U", size=7, color=GOLD, weight=600)
    if ext:
        sh.circle(x, y, 7, fill="none", stroke=INK, sw=0.6)


def sym_switch(sh, x, y, n=1):
    sh.circle(x, y, 3.5, fill=INK, stroke="none")
    sh.line(x, y, x + 7, y - 7, 1.0, INK)
    if n > 1:
        sh.line(x + 2, y - 4, x + 9, y - 11 + 4, 1.0, INK)


def sym_light(sh, x, y, kind="down"):
    if kind == "down":
        sh.circle(x, y, 4.5, fill=BG, stroke=INK, sw=1.0)
        sh.line(x - 3.2, y - 3.2, x + 3.2, y + 3.2, 0.9, INK)
        sh.line(x - 3.2, y + 3.2, x + 3.2, y - 3.2, 0.9, INK)
    elif kind == "wall":
        sh.circle(x, y, 4, fill=BG, stroke=INK, sw=1.0)
        sh.line(x - 4, y + 4, x + 4, y + 4, 1.4, INK)
    elif kind == "deck":
        sh.pl([(x, y - 5), (x + 4.5, y + 3), (x - 4.5, y + 3)], 0.9, INK, fill=BG, close=True)


def det07():
    sh = Sheet("DET-07", "Instalação elétrica", "COMUM", "1:100 / sem escala",
               "Pontos, circuitos e caminhos dos cabos (piso técnico e atrás do forro). Diagrama unifilar com proteções.")
    C = sh.callout
    k = 44
    # ---------------- planta Cocoon ----------------
    sh.panel(60, 120, 640, 420, "Planta elétrica  -  ZION COCOON (220 V mono, QD 12 módulos, 6,5 kW)", "1:100")
    X, Y = cocoon_plan(sh, 220, 330, k, deck=True)
    # quadro no ático técnico (x 6,3 a 8,8, z > 2,4) - projeção tracejada
    sh.rect(X(6.35), Y(1.9), 2.4 * k, 3.8 * k, fill="none", stroke=GOLD, sw=0.6, dash="3 2")
    sh.text(X(7.55), Y(-2.3), "ÁTICO TÉCNICO", size=7.5, anchor="middle", color=GOLD, ls="0.1em")
    sh.rect(X(6.5) - 8, Y(1.5) - 8, 16, 16, fill=INK, stroke="none")
    sh.text(X(6.5) + 12, Y(1.5) + 4, "QD", size=8, weight=600)
    # entrada de energia pela cauda (poste/rede), medidor externo
    sh.line(X(10.6), Y(0.0), X(9.0), Y(0.0), 1.2, INK)
    sh.line(X(9.0), Y(0.0), X(6.6), Y(1.4), 1.2, INK, dash="6 3")
    sh.rect(X(10.6) - 6, Y(0) - 8, 12, 16, fill=BG, stroke=INK, sw=1.0)
    sh.text(X(10.6), Y(-0.4), "med.", size=7.5, anchor="middle", color=GOLD)
    # condensadora na cauda
    sh.rect(X(9.2), Y(-0.9), 0.9 * k, 0.4 * k, fill="none", stroke=INK, sw=0.9)
    sh.text(X(9.65), Y(-1.5), "COND", size=7, anchor="middle", color=GOLD)
    sh.line(X(6.6), Y(1.4), X(9.2), Y(-1.1), 0.8, INK, dash="2 2")
    # caminhos: piso técnico (tracejado) e atrás do forro (traço-ponto)
    sh.line(X(6.5), Y(1.4), X(1.4), Y(2.1), 0.8, INK, dash="5 3")
    sh.line(X(6.5), Y(1.4), X(1.4), Y(-2.1), 0.8, INK, dash="5 3")
    sh.line(X(6.5), Y(1.5), X(4.2), Y(0.0), 0.8, INK, dash="5 3")
    sh.line(X(6.5), Y(1.6), X(2.0), Y(0.9), 0.8, INK, dash="7 2 1 2")
    # tomadas: junto à cama (2 USB), sofá (USB), console, banho, cauda (condensadora)
    sym_socket(sh, X(4.3), Y(1.3), usb=True)
    sym_socket(sh, X(4.3), Y(-1.3), usb=True)
    sym_socket(sh, X(1.5), Y(-1.7), usb=True)
    sym_socket(sh, X(2.4), Y(2.2))
    sym_socket(sh, X(3.6), Y(2.2))
    sym_socket(sh, X(7.0), Y(1.4))
    sym_socket(sh, X(7.0), Y(-1.2))
    sym_socket(sh, X(-1.0), Y(2.9), ext=True)
    # interruptores: entrada (2 teclas), suíte (cabeceira, 2 lados), banho
    sym_switch(sh, X(1.15), Y(-2.2), 2)
    sym_switch(sh, X(6.05), Y(1.1))
    sym_switch(sh, X(6.05), Y(-1.1))
    sym_switch(sh, X(6.4), Y(-0.3))
    # iluminação: fitas LED (linha dourada) nos rodapés, requadros e espinha; embutidos no banho; arandelas
    xs = np.linspace(1.05, 8.8, 60)
    for sg in (1, -1):
        sh.pl([(X(x), Y(sg * (COC.floor_hw(x) - 0.08))) for x in xs], 1.6, GOLD)
    sh.rect(X(1.75), Y(0.35), 4.7 * k, 0.7 * k, fill="none", stroke=GOLD, sw=1.6)
    for (wx, wy, lx, ly) in ((2.35, 2.6, 0.8, 0.3), (4.55, 2.6, 0.8, 0.3), (3.25, -2.6, 0.8, 0.3), (5.35, -2.6, 0.7, 0.3), (7.45, 2.0, 0.55, 0.25), (8.05, -1.4, 0.45, 0.25)):
        sh.rect(X(wx - lx), Y(wy + ly), 2 * lx * k, 2 * ly * k, fill="none", stroke=GOLD, sw=1.4, rx=6)
    for (lx, ly) in ((6.9, 1.6), (6.9, -0.4), (8.0, 0.4)):
        sym_light(sh, X(lx), Y(ly))
    sym_light(sh, X(4.6), Y(1.6), "wall"); sym_light(sh, X(4.6), Y(-1.6), "wall")
    sym_light(sh, X(0.75), Y(1.0), "down")
    for dx in (-2.5, -1.2, 0.2):
        sym_light(sh, X(dx), Y(3.1), "deck"); sym_light(sh, X(dx), Y(-3.1), "deck")
    # exaustor do banho e solar opcional
    sh.circle(X(7.0), Y(0.3), 5, fill=BG, stroke=INK, sw=0.9); sh.text(X(7.0), Y(0.3) + 3, "E", size=7, anchor="middle")
    sh.rect(X(9.6), Y(2.2), 1.2 * k, 0.7 * k, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.text(X(10.2), Y(2.6), "PV 3 kWp (opc.)", size=7.5, anchor="middle", color=GOLD)
    sh.rect(X(9.6), Y(1.2), 0.5 * k, 0.5 * k, fill="none", stroke=INK, sw=0.8)
    sh.text(X(10.3), Y(0.45), "bateria 10 kWh", size=7.5, anchor="middle", color=GOLD)
    C(1, X(6.5), Y(1.5), X(5.6), Y(3.5))
    C(2, X(4.3), Y(1.3), X(3.9), Y(3.4))
    C(3, X(2.0), Y(0.35), X(2.6), Y(-0.9))
    C(4, X(-1.2), Y(3.1), X(-2.0), Y(2.2))
    C(5, X(9.65), Y(-0.9), X(9.9), Y(-2.4))
    C(6, X(9.6), Y(2.55), X(8.7), Y(3.3))
    C(7, X(3.0), Y(1.9), X(2.6), Y(3.5))

    # ---------------- planta Zenith ----------------
    sh.panel(720, 120, 820, 420, "Planta elétrica  -  ZION ZENITH (220 V mono, QD 16 módulos, 8,0 kW)", "1:100")
    X2, Y2 = zenith_plan(sh, 900, 330, k, roof=True)
    sh.rect(X2(6.6), Y2(2.5), 2.7 * k, 5.0 * k, fill="none", stroke=GOLD, sw=0.6, dash="3 2")
    sh.text(X2(8.0), Y2(3.0), "ÁTICO TÉCNICO (z 2,50 a 2,90)", size=7.5, anchor="middle", color=GOLD)
    sh.rect(X2(6.7) - 8, Y2(2.0) - 8, 16, 16, fill=INK, stroke="none")
    sh.text(X2(6.7) + 12, Y2(2.0) + 4, "QD", size=8, weight=600)
    sh.line(X2(11.0), Y2(2.0), X2(6.7), Y2(2.0), 1.2, INK)
    sh.rect(X2(11.0) - 6, Y2(2.0) - 8, 12, 16, fill=BG, stroke=INK, sw=1.0)
    sh.text(X2(11.0), Y2(2.45), "med.", size=7.5, anchor="middle", color=GOLD)
    sh.rect(X2(9.8), Y2(-0.5), 0.9 * k, 0.4 * k, fill="none", stroke=INK, sw=0.9)
    sh.text(X2(10.25), Y2(-1.1), "COND", size=7, anchor="middle", color=GOLD)
    sh.line(X2(6.7), Y2(2.0), X2(9.8), Y2(-0.7), 0.8, INK, dash="2 2")
    # caminhos
    sh.line(X2(6.7), Y2(2.0), X2(0.5), Y2(2.2), 0.8, INK, dash="5 3")
    sh.line(X2(6.7), Y2(2.0), X2(0.5), Y2(-2.2), 0.8, INK, dash="5 3")
    sh.line(X2(6.7), Y2(2.0), X2(-1.55), Y2(-2.05), 0.8, INK, dash="5 3")
    sh.line(X2(6.7), Y2(2.1), X2(1.6), Y2(1.6), 0.8, INK, dash="7 2 1 2")
    sh.line(X2(6.7), Y2(2.1), X2(6.3), Y2(0.4), 0.8, INK, dash="7 2 1 2")
    # tomadas
    sym_socket(sh, X2(4.5), Y2(2.2), usb=True); sym_socket(sh, X2(4.5), Y2(-0.9), usb=True)
    sym_socket(sh, X2(0.6), Y2(1.6), usb=True); sym_socket(sh, X2(0.6), Y2(-1.4))
    sym_socket(sh, X2(2.2), Y2(2.3)); sym_socket(sh, X2(3.3), Y2(2.3))
    sym_socket(sh, X2(7.2), Y2(2.3)); sym_socket(sh, X2(8.6), Y2(-2.3))
    sym_socket(sh, X2(-0.5), Y2(3.2), ext=True); sym_socket(sh, X2(9.3), Y2(3.3), ext=True)
    # hidromassagem: alimentação dedicada
    sh.rect(X2(-1.55) - 7, Y2(-2.05) - 7, 14, 14, fill=BG, stroke=INK, sw=1.0)
    sh.text(X2(-1.55), Y2(-2.05) + 3, "H", size=8, anchor="middle", weight=600)
    # interruptores
    sym_switch(sh, X2(0.3), Y2(-2.4), 2); sym_switch(sh, X2(6.05), Y2(1.7)); sym_switch(sh, X2(6.05), Y2(-0.9))
    sym_switch(sh, X2(6.55), Y2(-2.3)); sym_switch(sh, X2(-0.2), Y2(3.2))
    # iluminação
    sh.rect(X2(0.3), Y2(2.45), 8.9 * k, 4.9 * k, fill="none", stroke=GOLD, sw=1.6)    # perímetro do forro
    sh.rect(X2(0.35), Y2(2.35), 5.8 * k, 4.7 * k, fill="none", stroke=GOLD, sw=0.9, dash="2 2")  # rodapé
    sh.circle(X2(6.3), Y2(0.4), 0.55 * k, fill="none", stroke=GOLD, sw=1.6)          # óculo
    sym_light(sh, X2(4.4), Y2(1.9), "wall"); sym_light(sh, X2(4.4), Y2(-1.1), "wall")
    for (lx, ly) in ((7.3, 1.5), (7.3, -0.5), (8.5, 0.4), (8.5, -1.5), (2.0, 0.6)):
        sym_light(sh, X2(lx), Y2(ly))
    for dx in (-2.6, -1.5, -0.4):
        sym_light(sh, X2(dx), Y2(3.6), "deck"); sym_light(sh, X2(dx), Y2(-3.6), "deck")
    for dx in (1.5, 4.5, 7.5):
        sym_light(sh, X2(dx), Y2(3.7), "deck")
    sh.circle(X2(8.0), Y2(-0.6), 5, fill=BG, stroke=INK, sw=0.9); sh.text(X2(8.0), Y2(-0.6) + 3, "E", size=7, anchor="middle")
    sh.rect(X2(9.9), Y2(-2.3), 1.2 * k, 0.7 * k, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.text(X2(10.5), Y2(-3.4), "PV 3 kWp + bat. (opc.)", size=7.5, anchor="middle", color=GOLD)
    C(8, X2(6.7), Y2(2.0), X2(5.6), Y2(3.4))
    C(9, X2(-1.55), Y2(-1.4), X2(-2.4), Y2(0.6))
    C(10, X2(6.3), Y2(0.95), X2(5.0), Y2(0.9))
    C(11, X2(1.6), Y2(1.6), X2(1.2), Y2(3.2))
    C(12, X2(1.5), Y2(3.7), X2(2.2), Y2(4.4))
    C(13, X2(10.25), Y2(-0.5), X2(11.2), Y2(0.3))

    # ---------------- diagrama unifilar ----------------
    sh.panel(60, 560, 790, 300, "Diagrama unifilar (Cocoon / Zenith)", "sem escala")
    x0, y0 = 80, 640
    sh.text(x0, y0 - 40, "rede 220 V, 60 Hz, F+N+PE", size=10, color=GOLD)
    sh.line(x0, y0, x0 + 40, y0, 1.2, INK)
    sh.rect(x0 + 40, y0 - 10, 26, 20, fill=BG, stroke=INK, sw=1.0); sh.text(x0 + 53, y0 + 4, "kWh", size=7, anchor="middle")
    sh.line(x0 + 66, y0, x0 + 96, y0, 1.2, INK)
    # DPS
    sh.rect(x0 + 96, y0 - 10, 26, 20, fill=BG, stroke=INK, sw=1.0); sh.text(x0 + 109, y0 + 4, "DPS", size=7, anchor="middle")
    sh.line(x0 + 109, y0 + 10, x0 + 109, y0 + 26, 0.9, INK); sh.line(x0 + 101, y0 + 26, x0 + 117, y0 + 26, 1.2, INK)
    sh.line(x0 + 122, y0, x0 + 150, y0, 1.2, INK)
    # disjuntor geral
    sh.line(x0 + 150, y0, x0 + 172, y0 - 12, 1.4, INK); sh.line(x0 + 176, y0, x0 + 200, y0, 1.2, INK)
    sh.text(x0 + 163, y0 - 18, "geral 40 A (Coc.) / 50 A (Zen.)", size=9, anchor="middle", color=GOLD)
    # DR geral 30 mA (iluminação e tomadas gerais) -> barramento
    sh.rect(x0 + 200, y0 - 10, 34, 20, fill=BG, stroke=INK, sw=1.0); sh.text(x0 + 217, y0 + 4, "DR 30mA", size=6.5, anchor="middle")
    sh.line(x0 + 234, y0, x0 + 260, y0, 1.2, INK)
    # barramento vertical
    bx = x0 + 260
    circuits = [
        ("C1  Climatização (evaporadora + condensadora)", "20 A", "4 mm²", "C", True),
        ("C2  Aquecedor de água / bomba de calor", "25 A", "6 mm²", "C", True),
        ("C3  Tomadas gerais (estar, suíte) com USB", "20 A", "2,5 mm²", "B", False),
        ("C4  Iluminação LED 2700 K + drivers 24 V", "10 A", "1,5 mm²", "B", False),
        ("C5  Banho (tomadas, exaustor, piso radiante opc.)", "20 A", "2,5 mm²", "B + DR 30 mA", False),
        ("C6  Hidromassagem 3 kW (Zenith)", "32 A", "6 mm²", "C + DR 30 mA", True),
        ("C7  Deck / externo (balizadores, tomada IP66)", "10 A", "1,5 mm²", "B + DR 30 mA", False),
        ("C8  Reserva / solar 3 kWp + bateria (inversor híbrido)", "20 A", "4 mm²", "C", True),
    ]
    sh.line(bx, y0 - 20, bx, y0 + 20 + 22 * (len(circuits) - 1) + 6, 2.2, INK)
    for i, (name, amp, cab, cur, direct) in enumerate(circuits):
        yy = y0 - 12 + i * 22
        sh.line(bx, yy, bx + 30, yy, 1.0, INK)
        sh.line(bx + 30, yy, bx + 48, yy - 10, 1.3, INK)
        sh.line(bx + 52, yy, bx + 90, yy, 1.0, INK)
        sh.text(bx + 100, yy + 4, name, size=9.5)
        sh.text(bx + 350, yy + 4, amp, size=9.5, weight=600)
        sh.text(bx + 385, yy + 4, cab, size=9.5)
        sh.text(bx + 432, yy + 4, cur, size=9)
    sh.text(bx + 350, y0 - 26, "disj.", size=8, color=GOLD); sh.text(bx + 385, y0 - 26, "cabo", size=8, color=GOLD); sh.text(bx + 432, y0 - 26, "curva / proteção", size=8, color=GOLD)
    sh.texts(x0 + 10, y0 + 185, ["Cabos em eletroduto corrugado no piso técnico (entre vigotas) e atrás do forro;",
                                "caixas 4 x 2 em madeira nos rodapés. Aterramento: haste 2,4 m + malha nas estacas;",
                                "equipotencialização da estrutura metálica (arcos, mastros, anel de beiral)."], size=9, lh=13, color=GOLD)
    C(14, x0 + 217, y0 - 10, x0 + 217, y0 - 60)

    # ---------------- legenda / símbolos ----------------
    sh.text(870, 585, "SÍMBOLOS", size=11, color=GOLD, ls="0.2em", weight=600)
    sy = 606
    sym_socket(sh, 850 + 30, sy); sh.text(900, sy + 4, "tomada 2P+T 10/20 A; U = com USB; duplo = externa IP66", size=9.2)
    sym_switch(sh, 880, sy + 22, 2); sh.text(900, sy + 26, "interruptor (1 ou 2 teclas)", size=9.5)
    sym_light(sh, 880, sy + 44); sh.text(900, sy + 48, "embutido LED no forro (banho, ático)", size=9.5)
    sym_light(sh, 880, sy + 66, "wall"); sh.text(900, sy + 70, "arandela / luz de leitura nos criados", size=9.5)
    sym_light(sh, 880, sy + 88, "deck"); sh.text(900, sy + 92, "balizador de deck 12 V IP67", size=9.5)
    sh.line(870, sy + 108, 890, sy + 108, 1.6, GOLD); sh.text(900, sy + 112, "fita LED 2700 K (rodapé, requadros, espinha, óculo, forro)", size=9.2)
    sh.line(870, sy + 130, 890, sy + 130, 0.8, INK, dash="5 3"); sh.text(900, sy + 134, "cabo no piso técnico (entre vigotas)", size=9.5)
    sh.line(870, sy + 152, 890, sy + 152, 0.8, INK, dash="7 2 1 2"); sh.text(900, sy + 156, "cabo atrás do forro / na câmara interna", size=9.5)
    sh.line(870, sy + 174, 890, sy + 174, 0.8, INK, dash="2 2"); sh.text(900, sy + 178, "linha frigorígena + alimentação da condensadora", size=9.5)
    items = [(1, "Quadro de distribuição no ático técnico (acesso por alçapão)"), (2, "Tomadas com USB junto à cama (2 lados)"),
             (3, "Fita LED na Espinha de Luz e nos requadros das janelas"), (4, "Balizadores de deck 12 V"),
             (5, "Condensadora na cauda, atrás do painel ripado"), (6, "Kit solar 3 kWp + bateria 10 kWh (opcional)"),
             (7, "Fita LED indireta no rodapé da concha (2 lados)"), (8, "QD 16 módulos no ático do banho"),
             (9, "Hidromassagem: circuito próprio 32 A com DR 30 mA"), (10, "Fita LED no anel do forro do Óculo"),
             (11, "Totem do mastro M2 com tomadas e luz da Ilha do Café"), (12, "Balizadores no terraço e na passarela"),
             (13, "Condensadora atrás do corpo, oculta pelo ripado"), (14, "DR geral 30 mA + DPS classe II na entrada")]
    sh.legend(1255, 585, items, cols=1, colw=300, lh=15.5, size=9.0, title="LEGENDA")
    sh.write("DET-07_eletrica.svg")


# ==================================================================================
# DET-08  Hidráulica
# ==================================================================================
def pipe(sh, pts, kind):
    """kind: 'cold' (traço), 'hot' (dourado), 'drain' (grosso), 'vent' (traço-ponto), 'grey' (pontilhado)."""
    if kind == "cold":
        sh.pl(pts, 1.0, INK, dash="6 3")
    elif kind == "hot":
        sh.pl(pts, 1.4, GOLD)
    elif kind == "drain":
        sh.pl(pts, 2.4, INK)
    elif kind == "vent":
        sh.pl(pts, 0.9, INK, dash="7 2 1 2")
    elif kind == "grey":
        sh.pl(pts, 1.2, GOLD, dash="2 3")


def valve(sh, x, y, ang=0):
    sh.add('<g transform="translate(%.1f %.1f) rotate(%s)">' % (x, y, ang))
    sh.add('<polygon points="-6,-4 0,0 -6,4" fill="%s" stroke="%s" stroke-width="0.8"/>' % (BG, INK))
    sh.add('<polygon points="6,-4 0,0 6,4" fill="%s" stroke="%s" stroke-width="0.8"/>' % (BG, INK))
    sh.add('</g>')


def det08():
    sh = Sheet("DET-08", "Instalações hidráulicas", "COMUM", "1:100 / esquemático",
               "Água fria PEX 25, água quente, esgoto Ø40/50 ao coletor Ø100 (i = 2%), ventilação, tratamento e opção de águas cinzas.")
    C = sh.callout
    k = 44
    # ---------------- planta Cocoon ----------------
    sh.panel(60, 120, 560, 400, "Planta hidráulica  -  ZION COCOON", "1:100")
    X, Y = cocoon_plan(sh, 130, 320, k, deck=False)
    # entrada de água fria pela cauda -> registro + filtro -> aquecedor no ático (x 6,5..8,8)
    pipe(sh, [(X(10.4), Y(1.6)), (X(9.0), Y(1.6)), (X(8.3), Y(1.6))], "cold")
    valve(sh, X(9.6), Y(1.6)); sh.rect(X(9.1) - 5, Y(1.6) - 5, 10, 10, fill=BG, stroke=INK, sw=0.9); sh.text(X(9.1), Y(1.6) + 3, "F", size=7, anchor="middle")
    sh.rect(X(7.6) - 12, Y(1.5) - 10, 24, 20, fill=BG, stroke=INK, sw=1.0); sh.text(X(7.6), Y(1.5) + 3, "AQ", size=8, anchor="middle", weight=600)
    pipe(sh, [(X(8.3), Y(1.6)), (X(7.85), Y(1.6))], "cold")
    # frias: bancada, chuveiro, bacia, banheira, ducha externa? (não), torneira do minibar
    pipe(sh, [(X(8.3), Y(1.6)), (X(8.3), Y(1.1)), (X(6.9), Y(1.1)), (X(6.9), Y(0.3))], "cold")   # ramal frio banho
    pipe(sh, [(X(8.3), Y(1.1)), (X(8.3), Y(-0.4))], "cold")                                     # bacia
    pipe(sh, [(X(6.9), Y(1.1)), (X(2.9), Y(2.3))], "cold")                                     # minibar
    # quentes (do AQ): bancada, chuveiro, banheira
    pipe(sh, [(X(7.4), Y(1.5)), (X(7.1), Y(1.5)), (X(7.1), Y(1.0)), (X(6.85), Y(1.0)), (X(6.85), Y(0.3))], "hot")
    pipe(sh, [(X(7.4), Y(1.5)), (X(7.4), Y(2.0)), (X(7.6), Y(2.0))], "hot")
    # pontos: bancada (7,1; 1,6), chuveiro (6,9; 0), bacia (8,0; -0,5), banheira (7,9; 1,3)
    for (px, py, lab) in ((7.15, 1.75, "LV"), (6.88, 0.0, "CH"), (8.0, -0.5, "BS"), (7.95, 1.3, "BH")):
        sh.circle(X(px), Y(py), 4.5, fill=BG, stroke=INK, sw=0.9); sh.text(X(px), Y(py) + 2.5, lab, size=6, anchor="middle")
    # esgoto: ramais Ø40 (LV, CH), Ø50 (BH), Ø100 (BS) -> coletor Ø100 sob o deck com 2% -> saída pela cauda
    pipe(sh, [(X(7.15), Y(1.75)), (X(7.5), Y(0.6))], "drain")
    pipe(sh, [(X(6.88), Y(0.0)), (X(7.5), Y(0.6))], "drain")
    pipe(sh, [(X(7.95), Y(1.3)), (X(8.2), Y(0.6))], "drain")
    pipe(sh, [(X(7.5), Y(0.6)), (X(8.2), Y(0.6)), (X(8.0), Y(-0.5)), (X(8.6), Y(-0.6)), (X(10.5), Y(-0.6))], "drain")
    sh.circle(X(8.9), Y(-0.6), 6, fill=BG, stroke=INK, sw=1.0); sh.text(X(8.9), Y(-0.6) + 3, "CI", size=6.5, anchor="middle")
    sh.arrow(X(9.3), Y(-0.9), X(10.2), Y(-0.9), 0.8, GOLD, head=5); sh.text(X(9.75), Y(-1.2), "i = 2%", size=8, anchor="middle", color=GOLD)
    # ventilação Ø50 subindo pela cauda até o respiro
    pipe(sh, [(X(8.2), Y(0.6)), (X(8.6), Y(1.9)), (X(9.0), Y(1.9))], "vent")
    sh.text(X(9.05), Y(2.05), "VENT Ø50", size=7, color=GOLD)
    # águas cinzas opcionais: desvio com válvula de 3 vias
    pipe(sh, [(X(8.2), Y(0.6)), (X(9.6), Y(0.6)), (X(10.5), Y(0.6))], "grey")
    valve(sh, X(9.4), Y(0.6)); sh.text(X(10.4), Y(0.9), "AC", size=7, color=GOLD)
    C(1, X(9.6), Y(1.6), X(10.0), Y(2.7))
    C(2, X(7.6), Y(1.5), X(6.2), Y(2.8))
    C(3, X(8.9), Y(-0.6), X(9.4), Y(-2.2))
    C(4, X(8.8), Y(1.9), X(8.0), Y(3.0))
    C(5, X(10.0), Y(0.6), X(10.9), Y(0.1))
    C(6, X(2.9), Y(2.3), X(2.0), Y(3.2))

    # ---------------- planta Zenith ----------------
    sh.panel(640, 120, 640, 400, "Planta hidráulica  -  ZION ZENITH", "1:100")
    X2, Y2 = zenith_plan(sh, 800, 320, k, roof=False)
    pipe(sh, [(X2(11.0), Y2(1.8)), (X2(9.5), Y2(1.8)), (X2(8.6), Y2(1.8))], "cold")
    valve(sh, X2(10.3), Y2(1.8)); sh.rect(X2(9.9) - 5, Y2(1.8) - 5, 10, 10, fill=BG, stroke=INK, sw=0.9); sh.text(X2(9.9), Y2(1.8) + 3, "F", size=7, anchor="middle")
    sh.rect(X2(8.0) - 12, Y2(1.8) - 10, 24, 20, fill=BG, stroke=INK, sw=1.0); sh.text(X2(8.0), Y2(1.8) + 3, "AQ", size=8, anchor="middle", weight=600)
    # frios: bancada dupla (7,6; 2,2), chuveiro (8,5; -1,9), bacia (6,9; -1,9), banheira (8,45; 1,7), ilha do café (2,4; 2,2), hidro (-1,55; -2,05), ducha externa (9,0; 3,1)
    pipe(sh, [(X2(8.6), Y2(1.8)), (X2(8.6), Y2(1.2)), (X2(6.9), Y2(1.2)), (X2(6.9), Y2(-1.9))], "cold")
    pipe(sh, [(X2(8.6), Y2(1.2)), (X2(8.5), Y2(-1.9))], "cold")
    pipe(sh, [(X2(6.9), Y2(1.2)), (X2(2.4), Y2(2.0))], "cold")
    pipe(sh, [(X2(2.4), Y2(2.0)), (X2(0.3), Y2(-2.3)), (X2(-1.55), Y2(-2.05))], "cold")
    pipe(sh, [(X2(8.6), Y2(1.8)), (X2(9.0), Y2(3.1))], "cold")
    # quentes
    pipe(sh, [(X2(7.7), Y2(1.9)), (X2(7.6), Y2(2.2))], "hot")
    pipe(sh, [(X2(7.7), Y2(1.9)), (X2(7.7), Y2(1.0)), (X2(8.4), Y2(1.0)), (X2(8.45), Y2(1.65))], "hot")
    pipe(sh, [(X2(7.7), Y2(1.0)), (X2(7.75), Y2(-1.9)), (X2(8.4), Y2(-1.9))], "hot")
    pipe(sh, [(X2(7.7), Y2(1.0)), (X2(2.3), Y2(1.9)), (X2(2.3), Y2(2.15))], "hot")
    for (px, py, lab) in ((7.6, 2.25, "LV"), (8.5, -1.9, "CH"), (6.9, -1.9, "BS"), (8.45, 1.7, "BH"), (2.4, 2.25, "PIA"), (9.0, 3.15, "DE")):
        sh.circle(X2(px), Y2(py), 4.5, fill=BG, stroke=INK, sw=0.9); sh.text(X2(px), Y2(py) + 2.5, lab, size=6, anchor="middle")
    # esgoto
    pipe(sh, [(X2(7.6), Y2(2.25)), (X2(7.8), Y2(0.3))], "drain")
    pipe(sh, [(X2(8.45), Y2(1.7)), (X2(8.3), Y2(0.3))], "drain")
    pipe(sh, [(X2(8.5), Y2(-1.9)), (X2(8.0), Y2(-0.6))], "drain")
    pipe(sh, [(X2(6.9), Y2(-1.9)), (X2(8.0), Y2(-0.6))], "drain")
    pipe(sh, [(X2(7.8), Y2(0.3)), (X2(8.3), Y2(0.3)), (X2(8.0), Y2(-0.6)), (X2(9.5), Y2(-0.7)), (X2(11.0), Y2(-0.7))], "drain")
    pipe(sh, [(X2(2.4), Y2(2.25)), (X2(2.4), Y2(2.9)), (X2(9.6), Y2(2.9)), (X2(9.8), Y2(-0.7))], "drain")   # pia pela passarela
    pipe(sh, [(X2(9.0), Y2(3.15)), (X2(9.6), Y2(2.9))], "drain")
    sh.circle(X2(9.8), Y2(-0.7), 6, fill=BG, stroke=INK, sw=1.0); sh.text(X2(9.8), Y2(-0.7) + 3, "CI", size=6.5, anchor="middle")
    sh.arrow(X2(10.2), Y2(-1.0), X2(10.9), Y2(-1.0), 0.8, GOLD, head=5); sh.text(X2(10.55), Y2(-1.3), "i = 2%", size=8, anchor="middle", color=GOLD)
    pipe(sh, [(X2(8.3), Y2(0.3)), (X2(9.2), Y2(0.6)), (X2(9.6), Y2(0.6))], "vent"); sh.text(X2(9.7), Y2(0.75), "VENT Ø50", size=7, color=GOLD)
    # hidromassagem: circuito próprio (bomba + filtro + aquecedor 3 kW) em caixa técnica sob o terraço
    sh.rect(X2(-2.9), Y2(-3.0), 0.9 * k, 0.5 * k, fill="none", stroke=INK, sw=0.9)
    sh.text(X2(-2.45), Y2(-3.85), "B+F+AQ 3 kW", size=7, anchor="middle", color=GOLD)
    sh.pl([(X2(-2.45), Y2(-3.0)), (X2(-2.3), Y2(-2.5)), (X2(-1.55), Y2(-2.05))], 1.0, INK)
    sh.pl([(X2(-2.0), Y2(-3.0)), (X2(-1.2), Y2(-2.6))], 1.0, INK)
    pipe(sh, [(X2(-2.45), Y2(-3.5)), (X2(-2.45), Y2(-4.2)), (X2(9.5), Y2(-4.2)), (X2(9.5), Y2(-0.7))], "drain")   # extravasor/dreno da hidro
    C(7, X2(10.3), Y2(1.8), X2(10.9), Y2(3.0))
    C(8, X2(8.0), Y2(1.8), X2(7.0), Y2(3.3))
    C(9, X2(-1.55), Y2(-2.05), X2(-0.6), Y2(-3.4))
    C(10, X2(9.8), Y2(-0.7), X2(10.9), Y2(-2.2))
    C(11, X2(2.4), Y2(2.9), X2(4.5), Y2(3.6))
    C(12, X2(9.0), Y2(3.15), X2(8.0), Y2(4.0))

    # ---------------- isométrico esquemático ----------------
    sh.panel(1300, 120, 240, 400, "Esquema vertical (sem escala)", "")
    ix, iy = 1338, 472
    def iso(u, v, w):   # u ao longo, v transversal, w altura
        return (ix + u * 0.5 + v * 0.35, iy - w - v * 0.2)
    # piso e ático
    sh.pl([iso(0, 0, 0), iso(200, 0, 0), iso(200, 120, 0), iso(0, 120, 0)], 0.6, INK, close=True)
    sh.pl([iso(0, 0, 60), iso(200, 0, 60), iso(200, 120, 60), iso(0, 120, 60)], 0.4, GOLD, dash="3 2", close=True)
    sh.text(iso(-10, 120, 66)[0], iso(-10, 120, 66)[1] - 2, "ático técnico", size=8, color=GOLD)
    sh.pl([iso(0, 0, -30), iso(200, 0, -30), iso(200, 120, -30), iso(0, 120, -30)], 0.4, GOLD, dash="3 2", close=True)
    sh.text(iso(150, 0, -30)[0], iso(150, 0, -30)[1] + 13, "vazio do deck", size=8, color=GOLD)
    # entrada PEX 25 -> registro -> filtro -> sobe ao ático -> aquecedor
    pipe(sh, [iso(230, 0, -30), iso(200, 0, -30), iso(200, 0, 65)], "cold")
    valve(sh, iso(215, 0, -30)[0], iso(215, 0, -30)[1])
    sh.rect(iso(190, 0, 70)[0] - 9, iso(190, 0, 70)[1] - 7, 18, 14, fill=BG, stroke=INK, sw=1.0); sh.text(iso(190, 0, 70)[0], iso(190, 0, 70)[1] + 3, "AQ", size=7, anchor="middle")
    pipe(sh, [iso(200, 0, 65), iso(120, 0, 65), iso(120, 0, 25)], "cold")
    pipe(sh, [iso(181, 0, 70), iso(130, 10, 70), iso(130, 10, 25)], "hot")
    for (u, v, lab) in ((120, 0, "CH"), (150, 40, "LV"), (90, 60, "BH"), (60, 90, "BS")):
        p = iso(u, v, 25)
        sh.circle(p[0], p[1], 4.5, fill=BG, stroke=INK, sw=0.9); sh.text(p[0], p[1] + 2.5, lab, size=6, anchor="middle")
        pipe(sh, [p, iso(u, v, -20)], "drain")
    pipe(sh, [iso(120, 0, -20), iso(60, 90, -20), iso(20, 90, -22), iso(-30, 90, -26)], "drain")
    pipe(sh, [iso(150, 40, -20), iso(60, 90, -20)], "drain")
    pipe(sh, [iso(90, 60, -20), iso(60, 90, -20)], "drain")
    pipe(sh, [iso(60, 90, -20), iso(60, 90, 80), iso(60, 90, 100)], "vent")
    sh.text(iso(60, 90, 104)[0], iso(60, 90, 104)[1] - 3, "vent Ø50 ao respiro", size=7.5, color=GOLD, anchor="middle")
    # tratamento
    sh.rect(iso(-60, 90, -26)[0] - 26, iso(-60, 90, -26)[1] - 8, 52, 20, fill=BG, stroke=INK, sw=1.0)
    sh.text(iso(-60, 90, -26)[0], iso(-60, 90, -26)[1] + 6, "fossa + filtro", size=7, anchor="middle")
    sh.text(iso(-60, 90, -26)[0], iso(-60, 90, -26)[1] + 26, "ou ETE compacta", size=7, anchor="middle", color=GOLD)
    sh.text(iso(110, 90, -30)[0], iso(110, 90, -30)[1] + 14, "Ø100 i = 2%", size=8, color=GOLD, anchor="start")

    # ---------------- notas e legenda ----------------
    sh.text(60, 560, "ESPECIFICAÇÕES", size=11, color=GOLD, ls="0.2em", weight=600)
    sh.texts(60, 582, [
        "Água fria: PEX Ø25 mm (entrada) e Ø20 nos ramais, em conduíte no piso técnico; registro geral, filtro Y e válvula redutora (3 bar).",
        "Água quente: aquecedor a gás 23 L/min (Cocoon) / 30 L/min (Zenith) ou bomba de calor 200 L / 300 L no ático; PEX Ø20 isolado 9 mm.",
        "Pressurização: reservatório 100 L + pressurizador 0,5 CV no ático (Cocoon) quando a rede for por gravidade; retorno de AQ opcional.",
        "Esgoto: ramais Ø40 (lavatório, chuveiro), Ø50 (banheira) e Ø100 (bacia) com sifões; coletor Ø100 PVC sob o deck, i = 2%, CI a cada 15 m.",
        "Ventilação: coluna Ø50 até 0,30 m acima da cobertura (cauda do Cocoon / atrás do Respiro no Zenith), com terminal anti-inseto.",
        "Tratamento: fossa séptica 1.500 L + filtro anaeróbio 1.000 L + sumidouro (NBR 7229) ou estação compacta de lodo ativado (4 pessoas).",
        "Águas cinzas (opcional): desvio de chuveiro, banheira e lavatório para tanque 500 L com filtro e cloração; reuso em irrigação.",
        "Hidromassagem Zenith Ø1,90: skid com bomba 1 CV, filtro de cartucho, aquecedor elétrico 3 kW e ozônio; enchimento AF, esgoto ao coletor.",
    ], size=10, lh=15.5)
    items = [(1, "Entrada AF PEX 25 com registro e filtro"), (2, "Aquecedor no ático técnico"),
             (3, "Caixa de inspeção Ø300 no coletor Ø100"), (4, "Coluna de ventilação Ø50"),
             (5, "Desvio de águas cinzas (opcional)"), (6, "Ponto de água do minibar (estar)"),
             (7, "Entrada AF Zenith pelos fundos"), (8, "Aquecedor 30 L/min ou BC 300 L (ático do banho)"),
             (9, "Hidromassagem: skid próprio sob o terraço"), (10, "CI e saída do coletor pelos fundos"),
             (11, "Esgoto da Ilha do Café pela passarela"), (12, "Ducha externa na passarela")]
    sh.legend(60, 728, items, cols=3, colw=320, lh=15, size=9.2, title=None)
    # legenda de linhas
    lx, ly = 1050, 585
    pipe(sh, [(lx, ly), (lx + 30, ly)], "cold"); sh.text(lx + 38, ly + 4, "água fria PEX", size=9)
    pipe(sh, [(lx, ly + 18), (lx + 30, ly + 18)], "hot"); sh.text(lx + 38, ly + 22, "água quente PEX isolado", size=9)
    pipe(sh, [(lx, ly + 36), (lx + 30, ly + 36)], "drain"); sh.text(lx + 38, ly + 40, "esgoto Ø40/50/100", size=9)
    pipe(sh, [(lx, ly + 54), (lx + 30, ly + 54)], "vent"); sh.text(lx + 38, ly + 58, "ventilação Ø50", size=9)
    pipe(sh, [(lx, ly + 72), (lx + 30, ly + 72)], "grey"); sh.text(lx + 38, ly + 76, "águas cinzas (opcional)", size=9)
    valve(sh, lx + 15, ly + 90); sh.text(lx + 38, ly + 94, "registro / válvula", size=9)
    sh.text(lx + 200, ly + 4, "LV lavatório   CH chuveiro   BH banheira", size=9, color=GOLD)
    sh.text(lx + 200, ly + 22, "BS bacia   PIA ilha do café   DE ducha ext.", size=9, color=GOLD)
    sh.text(lx + 200, ly + 40, "CI caixa de inspeção   F filtro   AQ aquecedor", size=9, color=GOLD)
    sh.write("DET-08_hidraulica.svg")


# ==================================================================================
# DET-09  Climatização e ventilação
# ==================================================================================
def det09():
    sh = Sheet("DET-09", "Climatização e ventilação", "COMUM", "1:100 (plantas) / 1:75 (seções)",
               "Evaporadora dutada no ático técnico, difusores lineares, retorno no banho, condensadora oculta, ventilação natural pela câmara e exaustão com recuperação.")
    C = sh.callout
    k = 40
    def duct(pts, w=5):
        sh.pl(pts, w, INK, opacity=0.25)
        sh.pl(pts, 0.8, INK)
    def airflow(x1, y1, x2, y2, color=GOLD):
        sh.arrow(x1, y1, x2, y2, 1.0, color, head=6)
    # ---------------- Cocoon planta ----------------
    sh.panel(60, 120, 520, 330, "Planta  -  ZION COCOON (12.000 BTU inverter, dutado)", "1:100")
    X, Y = cocoon_plan(sh, 120, 292, k, deck=False)
    sh.rect(X(6.6), Y(1.4), 1.0 * k, 0.6 * k, fill="url(#p-steel)", stroke=INK, sw=1.0)
    sh.text(X(7.1), Y(0.55), "EVAP", size=7, anchor="middle", color=GOLD)
    duct([(X(6.6), Y(1.1)), (X(6.3), Y(1.1)), (X(6.3), Y(-1.1))])
    duct([(X(6.3), Y(0.0)), (X(3.0), Y(0.0)), (X(3.0), Y(2.0))])
    # difusores lineares: cabeceira (2) e estar (1)
    for (dx, dy) in ((6.25, 0.8), (6.25, -0.8)):
        sh.rect(X(dx) - 3, Y(dy) - 0.5 * k, 6, 1.0 * k, fill=GOLD, stroke="none")
    sh.rect(X(3.0) - 0.5 * k, Y(2.05) - 3, 1.0 * k, 6, fill=GOLD, stroke="none")
    airflow(X(6.1), Y(0.8), X(5.4), Y(0.8)); airflow(X(6.1), Y(-0.8), X(5.4), Y(-0.8)); airflow(X(3.0), Y(2.0), X(3.0), Y(1.3))
    # retorno no forro do banho
    sh.rect(X(7.2) - 0.35 * k, Y(-0.6) - 0.25 * k, 0.7 * k, 0.5 * k, fill="none", stroke=INK, sw=0.9)
    for i in range(4):
        sh.line(X(7.2) - 0.3 * k, Y(-0.6) - 0.2 * k + i * 0.13 * k, X(7.2) + 0.3 * k, Y(-0.6) - 0.2 * k + i * 0.13 * k, 0.5, INK)
    sh.text(X(7.2), Y(-1.2), "RET", size=7, anchor="middle", color=GOLD)
    airflow(X(5.9), Y(-1.5), X(6.7), Y(-1.0), INK)
    # condensadora na cauda + linha frigorígena + dreno de condensado
    sh.rect(X(9.2), Y(-0.6), 0.9 * k, 0.4 * k, fill="none", stroke=INK, sw=0.9); sh.text(X(9.65), Y(-1.25), "COND", size=7, anchor="middle", color=GOLD)
    sh.pl([(X(7.6), Y(1.1)), (X(9.2), Y(-0.8))], 0.8, INK, dash="2 2")
    sh.pl([(X(7.6), Y(1.4)), (X(8.9), Y(2.0)), (X(9.0), Y(2.2))], 0.8, GOLD, dash="4 2")
    sh.text(X(9.05), Y(2.35), "dreno", size=7, color=GOLD)
    # exaustor do banho com recuperador (HRV) + ducto ao exterior pela cauda
    sh.circle(X(7.9), Y(0.9), 6, fill=BG, stroke=INK, sw=0.9); sh.text(X(7.9), Y(0.9) + 3, "HRV", size=5.5, anchor="middle")
    duct([(X(8.1), Y(0.9)), (X(9.1), Y(0.9))], 4)
    # janelas basculantes (estar e suíte) com setas de ar
    for (wx, wy, sg) in ((2.35, 2.75, -1), (4.55, 2.75, -1), (3.25, -2.75, 1), (5.35, -2.75, 1)):
        airflow(X(wx), Y(wy + sg * 0.5), X(wx), Y(wy - sg * 0.4))
    sh.text(X(2.35), Y(3.35), "basc.", size=7, anchor="middle", color=GOLD); sh.text(X(3.25), Y(-3.5), "basc.", size=7, anchor="middle", color=GOLD)
    C(1, X(7.1), Y(1.1), X(8.2), Y(2.6))
    C(2, X(6.25), Y(0.8), X(5.2), Y(2.7))
    C(3, X(7.2), Y(-0.6), X(8.2), Y(-2.2))
    C(4, X(9.65), Y(-0.6), X(10.5), Y(0.4))
    C(5, X(7.9), Y(0.9), X(9.8), Y(1.7))

    # ---------------- Cocoon seção longitudinal ----------------
    sh.panel(60, 470, 520, 300, "Seção longitudinal  -  COCOON (ventilação e ar)", "1:75 (1 m = 50 px)")
    ks = 50
    sx, sy = 95, 735
    SX = lambda xm: sx + xm * ks
    SY = lambda zm: sy - zm * ks
    xs = np.linspace(0.0, 9.0, 120)
    prof = [(SX(x), SY(COC.top(x))) for x in xs]
    # lábio: topo avança 0,55 em x=0
    prof = [(SX(-0.05), SY(3.85))] + prof
    sh.pl(prof, 1.6, INK)
    inner = [(SX(x), SY(COC.top(x) - 0.2)) for x in np.linspace(0.6, 8.9, 100)]
    sh.pl(inner, 2.2, INK)
    sh.pl([(SX(-0.05), SY(3.85)), (SX(0.5), SY(0))], 1.6, INK)   # lábio
    sh.line(SX(-0.6), SY(0), SX(10.4), SY(0), 1.6, INK)
    sh.line(SX(1.0), SY(0), SX(1.0 - 0.5), SY(3.75), 2.2, "#8A9DA3")   # fachada de vidro inclinada
    sh.rect(SX(6.2), SY(2.4), 0.12 * ks, 2.4 * ks, fill=INK, stroke="none")   # parede do banho
    sh.line(SX(6.3), SY(2.4), SX(8.8), SY(2.4), 0.9, INK)                     # piso do ático
    sh.text(SX(7.4), SY(2.65), "ÁTICO", size=7.5, anchor="middle", color=GOLD)
    sh.rect(SX(6.7), SY(3.0), 1.0 * ks, 0.45 * ks, fill="url(#p-steel)", stroke=INK, sw=0.9)
    duct([(SX(6.7), SY(2.75)), (SX(6.35), SY(2.75)), (SX(6.35), SY(1.9))])
    duct([(SX(6.7), SY(2.85)), (SX(6.35), SY(2.85)), (SX(6.35), SY(2.6)), (SX(3.0), SY(2.9)), (SX(3.0), SY(2.6))])
    airflow(SX(6.25), SY(1.9), SX(5.5), SY(1.7)); airflow(SX(3.0), SY(2.55), SX(3.0), SY(1.9))
    airflow(SX(6.0), SY(0.9), SX(6.9), SY(2.2), INK)   # retorno pelo forro do banho
    sh.rect(SX(9.2), SY(0.4), 0.9 * ks, 0.4 * ks, fill="none", stroke=INK, sw=0.9)
    sh.text(SX(9.65), SY(-0.25), "COND", size=7, anchor="middle", color=GOLD)
    sh.rect(SX(9.05), SY(1.5), 0.08 * ks, 1.5 * ks, fill="url(#p-wood)", stroke=INK, sw=0.6)   # painel ripado
    # ventilação da câmara: entrada nas frestas da base (x=0,5 e cauda), saída no respiro da cumeeira
    for xr in (1.4, 2.6, 5.5, 7.0, 8.2):
        z0 = COC.top(xr)
        airflow(SX(xr - 0.3), SY(z0 - 0.12), SX(xr + 0.3), SY(z0 - 0.1))
    airflow(SX(0.55), SY(0.15), SX(0.9), SY(1.2))
    airflow(SX(3.9), SY(3.98), SX(4.2), SY(4.35))
    sh.text(SX(4.25), SY(4.45), "respiro na cumeeira (Espinha)", size=7.5, color=GOLD)
    sh.text(SX(0.6), SY(-0.25), "fresta na base", size=7.5, anchor="middle", color=GOLD)
    airflow(SX(8.7), SY(0.15), SX(8.4), SY(0.9))
    # janela basculante: seta
    airflow(SX(2.35), SY(2.3), SX(2.9), SY(1.9))
    sh.text(SX(1.5), SY(1.5), "basculante", size=7.5, color=GOLD)
    # HRV
    sh.circle(SX(7.9), SY(2.7), 6, fill=BG, stroke=INK, sw=0.9); sh.text(SX(7.9), SY(2.7) + 3, "HRV", size=5.5, anchor="middle")
    duct([(SX(8.05), SY(2.7)), (SX(9.0), SY(2.7)), (SX(9.15), SY(2.5))], 4)
    airflow(SX(9.2), SY(2.45), SX(9.5), SY(2.0))
    sh.text(SX(7.0), SY(4.35), "operação até -15 °C (bomba de calor)", size=8, color=GOLD)
    sh.text(SX(7.0), SY(4.05), "piso radiante elétrico opcional", size=8, color=GOLD)
    sh.text(SX(7.0), SY(3.75), "no banho (150 W/m²)", size=8, color=GOLD)
    sh.pl([(SX(6.3), SY(0.05)), (SX(8.8), SY(0.05))], 3, GOLD, dash="2 2")
    C(6, SX(4.05), SY(4.2), SX(3.0), SY(4.3))
    C(7, SX(0.75), SY(0.8), SX(-0.5), SY(1.2))

    # ---------------- Zenith planta ----------------
    sh.panel(600, 120, 620, 330, "Planta  -  ZION ZENITH (18.000 BTU inverter, dutado)", "1:100")
    X2, Y2 = zenith_plan(sh, 740, 292, k, roof=True)
    sh.rect(X2(7.4), Y2(0.9), 1.1 * k, 0.6 * k, fill="url(#p-steel)", stroke=INK, sw=1.0)
    sh.text(X2(7.95), Y2(0.05), "EVAP", size=7, anchor="middle", color=GOLD)
    duct([(X2(7.4), Y2(0.6)), (X2(6.5), Y2(0.6)), (X2(6.5), Y2(-1.4))])
    duct([(X2(6.5), Y2(0.6)), (X2(6.5), Y2(2.2))])
    duct([(X2(6.5), Y2(2.2)), (X2(3.55), Y2(2.2)), (X2(3.55), Y2(-2.0))])
    for (dx, dy) in ((6.15, 1.6), (6.15, -0.9)):
        sh.rect(X2(dx) - 3, Y2(dy) - 0.5 * k, 6, 1.0 * k, fill=GOLD, stroke="none")
        airflow(X2(dx - 0.1), Y2(dy), X2(dx - 0.9), Y2(dy))
    for (dx, dy) in ((3.5, 1.2), (3.5, -1.2)):
        sh.rect(X2(dx) - 3, Y2(dy) - 0.5 * k, 6, 1.0 * k, fill=GOLD, stroke="none")
        airflow(X2(dx - 0.1), Y2(dy), X2(dx - 0.9), Y2(dy))
    sh.rect(X2(7.6) - 0.35 * k, Y2(-1.2) - 0.25 * k, 0.7 * k, 0.5 * k, fill="none", stroke=INK, sw=0.9)
    for i in range(4):
        sh.line(X2(7.6) - 0.3 * k, Y2(-1.2) - 0.2 * k + i * 0.13 * k, X2(7.6) + 0.3 * k, Y2(-1.2) - 0.2 * k + i * 0.13 * k, 0.5, INK)
    sh.text(X2(7.6), Y2(-1.85), "RET", size=7, anchor="middle", color=GOLD)
    airflow(X2(6.3), Y2(-2.2), X2(7.1), Y2(-1.5), INK)
    sh.rect(X2(9.9), Y2(0.3), 0.9 * k, 0.4 * k, fill="none", stroke=INK, sw=0.9); sh.text(X2(10.35), Y2(-0.35), "COND", size=7, anchor="middle", color=GOLD)
    sh.pl([(X2(8.5), Y2(0.6)), (X2(9.9), Y2(0.1))], 0.8, INK, dash="2 2")
    sh.pl([(X2(8.5), Y2(0.9)), (X2(9.4), Y2(2.7))], 0.8, GOLD, dash="4 2"); sh.text(X2(9.45), Y2(2.95), "dreno à calha", size=7, color=GOLD)
    sh.circle(X2(8.6), Y2(-1.9), 6, fill=BG, stroke=INK, sw=0.9); sh.text(X2(8.6), Y2(-1.9) + 3, "HRV", size=5.5, anchor="middle")
    duct([(X2(8.8), Y2(-1.9)), (X2(9.6), Y2(-1.9))], 4)
    # Respiro: chaminé no cume 2 com veneziana; entradas de ar nas frestas altas
    sh.circle(X2(1.6), Y2(1.6), 0.35 * k, fill=BG, stroke=INK, sw=1.2)
    for a in range(0, 360, 90):
        ca, sa = math.cos(math.radians(a + 45)), math.sin(math.radians(a + 45))
        airflow(X2(1.6 + 1.6 * ca), Y2(1.6 + 1.6 * sa), X2(1.6 + 0.6 * ca), Y2(1.6 + 0.6 * sa))
    sh.text(X2(1.6), Y2(2.75), "RESPIRO", size=7, anchor="middle", color=GOLD, ls="0.1em")
    for (fx, fy) in ((2.0, -2.65), (5.0, -2.65), (8.0, 2.65)):
        airflow(X2(fx), Y2(fy - 0.5 * (1 if fy < 0 else -1)), X2(fx), Y2(fy + 0.4 * (1 if fy < 0 else -1)))
    sh.text(X2(2.0), Y2(-3.45), "fresta alta", size=7, anchor="middle", color=GOLD)
    C(8, X2(7.95), Y2(0.6), X2(9.0), Y2(1.9))
    C(9, X2(6.15), Y2(1.6), X2(5.2), Y2(2.9))
    C(10, X2(3.5), Y2(1.2), X2(2.6), Y2(0.4))
    C(11, X2(7.6), Y2(-1.2), X2(6.8), Y2(-3.0))
    C(12, X2(10.35), Y2(0.3), X2(11.2), Y2(1.2))
    C(13, X2(1.6), Y2(1.3), X2(0.4), Y2(-0.6))
    C(14, X2(8.6), Y2(-1.9), X2(9.8), Y2(-3.0))

    # ---------------- Zenith seção longitudinal ----------------
    sh.panel(600, 470, 620, 300, "Seção longitudinal  -  ZENITH (ventilação e ar)", "≈ 1:95 (1 m = 40 px)")
    sx2, sy2 = 730, 758
    ks2 = 40
    SX2 = lambda xm: sx2 + xm * ks2
    SY2 = lambda zm: sy2 - zm * ks2
    sh.line(SX2(-3.0), SY2(0), SX2(10.6), SY2(0), 1.6, INK)
    # paredes e anel de beiral
    sh.rect(SX2(0), SY2(2.75), 0.1 * ks, 2.75 * ks, fill=GLASS, stroke="#8A9DA3", sw=0.8)
    sh.rect(SX2(9.4), SY2(2.75), 0.1 * ks, 2.75 * ks, fill=INK, stroke="none")
    sh.rect(SX2(6.2), SY2(2.75), 0.25 * ks, 2.75 * ks, fill=INK, stroke="none")
    sh.rect(SX2(-0.05), SY2(2.9), 9.6 * ks, 0.15 * ks, fill=INK, stroke="none")
    # membrana: das bordas (2,65 nos postes) aos cumes (5,8 em x 6,3; 4,6 em x 1,6), vale entre
    mem = [(SX2(-2.4), SY2(2.65)), (SX2(0.0), SY2(3.3)), (SX2(1.6), SY2(4.6)), (SX2(3.9), SY2(3.7)), (SX2(6.3), SY2(5.8)), (SX2(8.5), SY2(3.8)), (SX2(10.5), SY2(2.65))]
    sh.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (
        mem[0] + (SX2(0.0), SY2(2.75)) + mem[1] + mem[2] + (SX2(3.9), SY2(3.5)) + mem[3] + (SX2(5.4), SY2(3.9)) + mem[4] + mem[5] + (SX2(9.5), SY2(2.9)) + mem[6]), 3, GOLD)
    # mastros e coroas
    sh.line(SX2(6.3), SY2(0), SX2(6.3), SY2(5.05), 2.5, INK); sh.line(SX2(1.6), SY2(0), SX2(1.6), SY2(4.0), 2.0, INK)
    sh.line(SX2(5.7), SY2(5.8), SX2(6.9), SY2(5.8), 2.0, INK)
    sh.line(SX2(1.25), SY2(4.6), SX2(1.95), SY2(4.6), 2.0, INK)
    sh.line(SX2(6.3), SY2(5.05), SX2(5.7), SY2(5.8), 1.0, INK); sh.line(SX2(6.3), SY2(5.05), SX2(6.9), SY2(5.8), 1.0, INK)
    sh.line(SX2(1.6), SY2(4.0), SX2(1.25), SY2(4.6), 1.0, INK); sh.line(SX2(1.6), SY2(4.0), SX2(1.95), SY2(4.6), 1.0, INK)
    # óculo (vidro) e chaminé do Respiro (veneziana motorizada)
    sh.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (SX2(5.7), SY2(5.8), SX2(6.3), SY2(6.25), SX2(6.9), SY2(5.8)), 1.0, "#8A9DA3", fill=GLASS)
    sh.rect(SX2(1.35), SY2(5.15), 0.5 * ks, 0.55 * ks, fill=BG, stroke=INK, sw=1.0)
    for i in range(4):
        sh.line(SX2(1.35), SY2(4.7 + i * 0.12), SX2(1.85), SY2(4.65 + i * 0.12), 0.6, INK)
    sh.rect(SX2(1.25), SY2(5.25), 0.7 * ks, 0.1 * ks, fill=INK, stroke="none")
    airflow(SX2(1.6), SY2(4.2), SX2(1.6), SY2(5.0))
    airflow(SX2(1.9), SY2(5.05), SX2(2.3), SY2(5.25))
    sh.text(SX2(2.4), SY2(5.35), "Respiro: chaminé com veneziana motorizada", size=7.5, color=GOLD)
    # forro tensionado (linha 2) abaixo da membrana (offset ~0,25)
    forro = [(SX2(0.0), SY2(2.9)), (SX2(1.6), SY2(4.25)), (SX2(3.9), SY2(3.35)), (SX2(6.3), SY2(5.3)), (SX2(9.4), SY2(2.9))]
    sh.pl(forro, 2.0, INK)
    sh.rect(SX2(6.45), SY2(2.9), 2.95 * ks, 0.4 * ks, fill="none", stroke=GOLD, sw=0.6, dash="3 2")   # ático
    sh.text(SX2(7.9), SY2(2.55), "ÁTICO", size=7.5, anchor="middle", color=GOLD)
    sh.rect(SX2(7.4), SY2(2.85), 1.1 * ks, 0.3 * ks, fill="url(#p-steel)", stroke=INK, sw=0.9)
    duct([(SX2(7.4), SY2(2.7)), (SX2(6.5), SY2(2.7)), (SX2(6.5), SY2(2.1))]); airflow(SX2(6.4), SY2(2.1), SX2(5.6), SY2(1.9))
    duct([(SX2(6.5), SY2(2.7)), (SX2(3.6), SY2(3.3)), (SX2(3.6), SY2(2.3))]); airflow(SX2(3.5), SY2(2.3), SX2(2.8), SY2(2.0))
    airflow(SX2(6.7), SY2(1.0), SX2(7.4), SY2(2.4), INK)
    # câmara ventilada: ar entra nas frestas altas e sobe ao Respiro
    for (xa, za, xb, zb) in ((0.6, 3.1, 1.2, 4.0), (3.3, 3.55, 2.3, 4.2), (5.0, 4.4, 4.2, 3.85), (8.8, 3.4, 7.6, 4.3)):
        airflow(SX2(xa), SY2(za), SX2(xb), SY2(zb))
    airflow(SX2(-0.4), SY2(2.4), SX2(0.2), SY2(3.0))
    sh.text(SX2(-2.6), SY2(2.2), "fresta alta (entrada)", size=7.5, color=GOLD)
    sh.rect(SX2(9.9), SY2(0.4), 0.9 * ks, 0.4 * ks, fill="none", stroke=INK, sw=0.9); sh.text(SX2(10.35), SY2(-0.25), "COND", size=7, anchor="middle", color=GOLD)
    sh.rect(SX2(9.75), SY2(1.5), 0.08 * ks, 1.5 * ks, fill="url(#p-wood)", stroke=INK, sw=0.6)
    sh.pl([(SX2(0.2), SY2(0.05)), (SX2(9.3), SY2(0.05))], 3, GOLD, dash="2 2")
    sh.text(SX2(2.2), SY2(0.22), "piso radiante elétrico opcional (suíte e banho)", size=7.5, color=GOLD)
    C(15, SX2(1.6), SY2(5.0), SX2(0.4), SY2(5.5))
    C(16, SX2(6.3), SY2(6.0), SX2(7.6), SY2(6.1))

    # ---------------- legenda / notas ----------------
    items = [
        (1, "Evaporadora dutada inverter 12.000 BTU (Q/F) no ático, até -15 °C"),
        (2, "Difusores lineares 1,0 m na parede da cabeceira (2) e no estar (1)"),
        (3, "Grelha de retorno no forro do banho com filtro G4"),
        (4, "Condensadora na cauda, sobre base, oculta pelo painel ripado"),
        (5, "Exaustor do banho 150 m³/h com recuperador de calor (HRV)"),
        (6, "Respiro contínuo na cumeeira: saída da câmara ventilada (tela + capa)"),
        (7, "Fresta de entrada de ar na base da concha (tela anti-inseto)"),
        (8, "Evaporadora dutada inverter 18.000 BTU no ático do banho"),
        (9, "Difusores lineares na parede da cabeceira (suíte)"),
        (10, "Difusores lineares no estar (divisória x 3,55)"),
        (11, "Retorno no forro do banho"),
        (12, "Condensadora atrás do corpo, oculta pelo ripado"),
        (13, "Respiro: cume 2 com chaminé Ø0,70 e veneziana motorizada"),
        (14, "Exaustor do banho com recuperador (HRV)"),
        (15, "Chaminé do Respiro: tiragem natural da câmara e do interior"),
        (16, "Óculo do Zênite: vidro duplo (cúpula + vidro interno), sem abertura"),
    ]
    sh.legend(1240, 140, items, cols=1, colw=300, lh=16.5, size=9.0)
    sh.note(1250, 460, ["Notas", "Linhas frigorígenas isoladas 3/8 + 5/8 (Cocoon)", "e 1/2 + 3/4 (Zenith) em canaleta oculta.",
                        "Dreno de condensado Ø20 com sifão à calha.", "Dutos flexíveis isolados Ø150/Ø200; velocidade",
                        "< 4 m/s; ruído nos difusores < 30 dB(A).", "Aquecimento: ciclo reverso (bomba de calor)",
                        "+ piso radiante elétrico opcional 150 W/m².", "Ventilação natural: câmara ventilada 60 mm,",
                        "basculantes (Cocoon), Respiro (Zenith), frestas.", "Renovação mínima: 27 m³/h/pessoa (NBR 16401)."], size=9.2, w=300)
    sh.text(60, 800, "Legenda das setas:  dourada = ar de insuflamento / ventilação natural;  preta = retorno.  Dutos representados em cinza.", size=9.5, color=GOLD)
    sh.write("DET-09_climatizacao.svg")


# ==================================================================================
# DET-10  Sistema de arcos do COCOON
# ==================================================================================
def det10():
    sh = Sheet("DET-10", "Sistema de arcos", "ZION COCOON", "1:40 / 1:5 / sem escala",
               "Arco típico A3 em 3 segmentos com luvas internas, tabela dos 8 arcos, ligação das terças, presilha keder, contraventamento e anel frontal A0.")
    C = sh.callout
    # ---------------- Painel A: elevação do arco A3 ----------------
    sh.panel(60, 120, 700, 450, "Elevação do arco A3 (x = 2,90 m, L = 11,2 m)", "1:40 (1 m = 95 px)")
    k = 95
    cx, fy = 410, 535
    pts = COC.arch_pts(2.9, 160)
    P = [(cx + y * k, fy - z * k) for (y, z) in pts]
    # comprimento desenvolvido e posição das luvas (z = 2,30)
    seg = [0.0]
    for i in range(1, len(pts)):
        seg.append(seg[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    Ltot = seg[-1]
    zj = 2.3
    jl = next(i for i in range(len(pts)) if pts[i][1] >= zj)
    jr = next(i for i in range(len(pts) - 1, -1, -1) if pts[i][1] >= zj)
    # arco: tubo Ø88,9 (8,4 px) com eixo tracejado
    sh.pl(P, 88.9 * k / 1000 + 1.2, INK)
    sh.pl(P, 88.9 * k / 1000 - 1.0, BG)
    sh.pl(P, 0.5, INK, dash="8 3 2 3")
    # perfil keder (dourado) pela face externa
    Po = [(cx + y * k * 1.03, fy - (COC.ZC + (z - COC.ZC) * 1.03) * k) for (y, z) in pts]
    sh.pl(Po, 1.6, GOLD)
    # luvas internas Ø76 x 200 (hachura) nas juntas
    for j in (jl, jr):
        x, y = P[j]
        dx, dy = P[j + 1][0] - P[j - 1][0], P[j + 1][1] - P[j - 1][1]
        L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        sh.pl([(x - ux * 9.5, y - uy * 9.5), (x + ux * 9.5, y + uy * 9.5)], 6.5, INK, dash="2 1.5")
        sh.line(x - uy * 12, y + ux * 12, x + uy * 12, y - ux * 12, 0.9, GOLD)
    sh.text(P[jl][0] - 26, P[jl][1] + 4, "luva", size=9, anchor="end", color=GOLD)
    sh.text(P[jr][0] + 26, P[jr][1] + 4, "luva", size=9, anchor="start", color=GOLD)
    # terças Ø48,3 (cortadas) na face interna, nas 7 posições
    for v in COC.PURLIN_V:
        idx = int(v * (len(pts) - 1))
        y, z = pts[idx]
        # normal para dentro
        i0, i1 = max(idx - 1, 0), min(idx + 1, len(pts) - 1)
        dx, dy = pts[i1][0] - pts[i0][0], pts[i1][1] - pts[i0][1]
        L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
        # garantir que aponta para o centro
        if (y + nx * 0.1) ** 2 + (z - COC.ZC + ny * 0.1) ** 2 > y * y + (z - COC.ZC) ** 2:
            nx, ny = -nx, -ny
        px, py = cx + (y + nx * 0.07) * k, fy - (z + ny * 0.07) * k
        sh.circle(px, py, 48.3 * k / 2000, fill=BG, stroke=INK, sw=1.0)
    # espinha de luz (treliça 300 mm) no topo
    sh.rect(cx - 0.35 * k, fy - COC.top(2.9) * k - 2, 0.7 * k, 0.3 * k, fill="url(#p-steel)", stroke=INK, sw=0.9)
    # chapas de base 200 x 10 e chumbadores
    for (x, y) in (P[0], P[-1]):
        sh.rect(x - 0.1 * k, y - 1.5, 0.2 * k, 3, fill=INK, stroke="none")
        sh.rect(x - 0.075 * k, y - 4, 2, 6, fill=INK, stroke="none"); sh.rect(x + 0.075 * k - 2, y - 4, 2, 6, fill=INK, stroke="none")
    sh.line(cx - 3.3 * k, fy, cx + 3.3 * k, fy, 1.6, INK)
    # cotas
    a3 = COC.a(2.9)
    sh.dim_h(cx - a3 * k, cx + a3 * k, fy + 40, "5,86 (largura máxima, z = 0,75)", ext=None, above=False, size=10)
    hw = COC.floor_hw(2.9)
    sh.dim_h(cx - hw * k, cx + hw * k, fy + 20, "%s (no piso)" % f(2 * hw).replace(".", ","), ext=None, above=False, size=10)
    sh.dim_v(cx + 3.15 * k, fy - COC.top(2.9) * k, fy, "3,94", ext=None, left=False, size=10)
    sh.dim_v(cx - 3.15 * k, fy - COC.ZC * k, fy, "0,75", ext=None, left=True, size=10)
    sh.dim_v(cx - 3.15 * k, fy - zj * k, fy - COC.ZC * k, "1,55", ext=None, left=True, size=10)
    sh.text(cx, fy - 2.75 * k, "coroa  L ≈ %s m" % f(seg[jr] - seg[jl]).replace(".", ","), size=10, anchor="middle", color=GOLD)
    sh.text(P[jl // 2][0] + 30, P[jl // 2][1] + 4, "perna  L ≈ %s m" % f(seg[jl]).replace(".", ","), size=10, anchor="start", color=GOLD)
    sh.text(P[(jr + len(pts)) // 2][0] - 30, P[(jr + len(pts)) // 2][1] + 4, "perna  L ≈ %s m" % f(Ltot - seg[jr]).replace(".", ","), size=10, anchor="end", color=GOLD)
    sh.text(cx, fy - 2.05 * k, "elipse: a = 2,93 m, b = 3,19 m, centro z = 0,75 m", size=10, anchor="middle", color=GOLD)
    sh.text(cx, fy - 1.8 * k, "tubo Ø88,9 x 3,6, calandrado a frio, R mín. 2,9 m", size=10, anchor="middle", color=GOLD)
    C(1, P[40][0], P[40][1], P[40][0] + 60, P[40][1] + 30)
    C(2, P[jr][0], P[jr][1], P[jr][0] + 55, P[jr][1] - 30)
    idx = int(0.66 * (len(pts) - 1)); y, z = pts[idx]
    C(3, cx + y * 0.965 * k, fy - (COC.ZC + (z - COC.ZC) * 0.965) * k, cx + y * 0.965 * k - 50, fy - (COC.ZC + (z - COC.ZC) * 0.965) * k + 40)
    C(4, Po[100][0], Po[100][1], Po[100][0] + 55, Po[100][1] - 20)
    C(5, cx, fy - COC.top(2.9) * k + 10, cx + 90, fy - COC.top(2.9) * k + 45)
    C(6, P[-1][0], P[-1][1] - 2, P[-1][0] + 50, P[-1][1] - 30)

    # ---------------- Painel B: detalhes 1:5 ----------------
    sh.panel(790, 120, 750, 290, "Detalhes  -  luva interna, ponteira da terça e presilha keder", "1:5 (1 mm = 0,8 px)")
    kd = 0.8
    # (i) luva
    t1 = Tr(960, 270, kd)
    X1, Y1 = t1.x, t1.y
    sh.text(805, 162, "luva interna Ø76 x 200 + 4 x M12", size=9.5, color=GOLD)
    for (x0, x1) in ((-170, -3), (3, 170)):
        sh.rect(X1(x0), Y1(44.45), (x1 - x0) * kd, 88.9 * kd, fill="none", stroke=INK, sw=1.2)
        sh.rect(X1(x0), Y1(44.45), (x1 - x0) * kd, 3.6 * kd, fill=INK, stroke="none")
        sh.rect(X1(x0), Y1(-40.85), (x1 - x0) * kd, 3.6 * kd, fill=INK, stroke="none")
    sh.rect(X1(-100), Y1(38.05), 200 * kd, 76.1 * kd, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.rect(X1(-97), Y1(35), 194 * kd, 70 * kd, fill=BG, stroke=INK, sw=0.5)
    for xb in (-60, 60):
        sh.bolt_side(X1(xb), Y1(50), 100 * kd, 6, vertical=True)
    for xb in (-30, 30):
        sh.circle(X1(xb), Y1(0), 6 * kd, fill=BG, stroke=INK, sw=0.8, dash="2 2")
    sh.line(X1(-175), Y1(0), X1(175), Y1(0), 0.5, INK, dash="8 3 2 3")
    sh.dim_h(X1(-100), X1(100), Y1(-62), "200", ext=None, above=False, size=10)
    sh.dim_h(X1(-60), X1(60), Y1(75), "120 (2 x M12 a 90°)", ext=None, size=10)
    sh.text(X1(0), Y1(-90), "junta 6 mm selada; tubo externo Ø88,9 x 3,6", size=9, anchor="middle", color=GOLD)
    C(7, X1(-80), Y1(30), X1(-150), Y1(-70))
    C(8, X1(60), Y1(-45), X1(130), Y1(-70))
    # (ii) ponteira rosqueada da terça
    t2 = Tr(1200, 270, kd)
    X2, Y2 = t2.x, t2.y
    sh.text(1105, 162, "ponteira rosqueada M16 no talão", size=9.5, color=GOLD)
    sh.rect(X2(-4), Y2(80), 8 * kd, 140 * kd, fill=INK, stroke="none")        # talão chapa 8
    sh.path("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (X2(-60), Y2(80), 62 * kd, 62 * kd, X2(60), Y2(80)), 1.2, INK)  # face do arco
    for sg in (-1, 1):
        x0 = 4 if sg > 0 else -110
        sh.rect(X2(x0), Y2(24.15), 106 * kd, 48.3 * kd, fill="none", stroke=INK, sw=1.2)
        sh.rect(X2(x0), Y2(24.15), 106 * kd, 3 * kd, fill=INK, stroke="none")
        sh.rect(X2(x0), Y2(-21.15), 106 * kd, 3 * kd, fill=INK, stroke="none")
        # inserto rosqueado soldado
        sh.rect(X2(4 if sg > 0 else -34), Y2(16), 30 * kd, 32 * kd, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.bolt_side(X2(-40), Y2(0), 80 * kd, 8, vertical=False)
    sh.text(X2(0), Y2(-62), "terças Ø48,3 x 3,0 em segmentos de 1,20 m", size=9, anchor="middle", color=GOLD)
    sh.text(X2(0), Y2(-78), "parafuso M16 x 80 atravessando o talão", size=9, anchor="middle", color=GOLD)
    C(9, X2(60), Y2(10), X2(100), Y2(70))
    C(10, X2(0), Y2(60), X2(-50), Y2(100))
    # (iii) presilha keder
    t3 = Tr(1420, 250, 1.2)
    X3, Y3 = t3.x, t3.y
    sh.text(1345, 162, "presilha keder @ 300", size=9.5, color=GOLD)
    sh.tube_cut(X3(0), Y3(-70), 44.45 * 1.2, 3.6 * 1.2)
    sh.path("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (X3(-30), Y3(-58), 33 * 1.2, 33 * 1.2, X3(30), Y3(-58)), 3.5, INK)
    sh.rect(X3(-31.5), Y3(-58), 3 * 1.2, 20 * 1.2, fill=INK, stroke="none"); sh.rect(X3(28.5), Y3(-58), 3 * 1.2, 20 * 1.2, fill=INK, stroke="none")
    rail = [(-35, 0), (35, 0), (35, -33), (31, -33), (31, -23), (10, -23), (10, -14), (-10, -14), (-10, -23), (-31, -23), (-31, -33), (-35, -33)]
    sh.pl([(X3(a), Y3(b)) for a, b in rail], 1.2, INK, fill="url(#p-steel)", close=True)
    for xk in (-22, 22):
        sh.circle(X3(xk), Y3(-10), 5.5 * 1.2, fill=BG, stroke=INK, sw=1.0); sh.circle(X3(xk), Y3(-10), 4 * 1.2, fill=GOLD, stroke=INK, sw=0.6)
    sh.bolt_side(X3(0), Y3(-3), 30 * 1.2, 5, vertical=True)
    sh.membrane([(X3(-90), Y3(1)), (X3(-27), Y3(1))]); sh.membrane([(X3(27), Y3(1)), (X3(90), Y3(1))])
    C(11, X3(-30), Y3(-62), X3(-70), Y3(-100))
    C(12, X3(30), Y3(-18), X3(75), Y3(-40))

    # ---------------- Painel C: contraventamento + A0 + isométrica ----------------
    sh.panel(790, 430, 750, 270, "Contraventamento em X, anel frontal A0 e conceito do pórtico", "1:60 / sem escala")
    ke = 22
    ox, oy = 810, 675
    EX = lambda xm: ox + xm * ke
    EY = lambda zm: oy - zm * ke
    sh.line(EX(-0.6), EY(0), EX(9.6), EY(0), 1.2, INK)
    for i, xa in enumerate(COC.ARCH_X):
        sh.line(EX(xa), EY(0), EX(xa), EY(COC.top(xa)), 2.0, INK)
        sh.text(EX(xa), EY(COC.top(xa)) - 5, "A%d" % (i + 1), size=8, anchor="middle", color=GOLD)
    # A0 inclinado 8° (base x = 0,5, topo x = -0,05)
    sh.line(EX(0.5), EY(0), EX(-0.05), EY(3.85), 2.0, GOLD)
    sh.text(EX(-0.15), EY(3.85) - 5, "A0", size=8, anchor="middle", color=GOLD)
    sh.text(EX(-0.55), EY(1.8), "8°", size=9, color=GOLD)
    # terças (7 níveis, simplificado como 4 linhas)
    for zz in (0.9, 1.9, 2.8, 3.5):
        xs_ = [x for x in COC.ARCH_X if COC.top(x) > zz + 0.1]
        if len(xs_) > 1:
            sh.line(EX(xs_[0]), EY(zz), EX(xs_[-1]), EY(zz), 0.6, INK)
    # cabos em X nos vãos A1-A2 e A6-A7 com esticadores
    for (xa, xb) in ((0.5, 1.7), (6.5, 7.6)):
        za, zb = COC.top(xa) * 0.92, COC.top(xb) * 0.92
        sh.cable(EX(xa), EY(0.2), EX(xb), EY(zb), 1.1); sh.cable(EX(xb), EY(0.2), EX(xa), EY(za), 1.1)
        sh.turnbuckle(EX((xa + xb) / 2), EY((0.2 + zb) / 2), -math.degrees(math.atan2((zb - 0.2) * ke, (xb - xa) * ke)), 12, 5)
    sh.text(EX(1.1), EY(-0.5), "X A1-A2", size=8, anchor="middle", color=GOLD)
    sh.text(EX(7.05), EY(-0.5), "X A6-A7", size=8, anchor="middle", color=GOLD)
    sh.text(EX(9.9), EY(3.4), "cabos inox Ø8 (8 un.),", size=9, color=GOLD)
    sh.text(EX(9.9), EY(2.8), "esticadores M12", size=9, color=GOLD)
    C(13, EX(1.1), EY(1.6), EX(2.3), EY(0.6))
    C(14, EX(0.2), EY(2.1), EX(1.6), EY(4.0))
    # isométrica do conceito
    s_ = 21
    icx, icy = 1300, 555
    def iso(x, y, z):
        return (icx + (x - y) * 0.866 * s_, icy + (x + y) * 0.5 * s_ - z * s_)
    sh.text(1395, 692, "conceito: arcos + terças + espinha + trilhos de base", size=9, anchor="middle", color=GOLD)
    # trilhos de base (contorno do piso)
    xs = np.linspace(0.5, 8.9, 50)
    base = [iso(x, COC.floor_hw(x), 0) for x in xs] + [iso(x, -COC.floor_hw(x), 0) for x in xs[::-1]]
    sh.pl(base, 0.8, INK, close=True)
    # arcos
    arcs = []
    for xa in COC.ARCH_X:
        ap = COC.arch_pts(xa, 40)
        arcs.append(ap)
        sh.pl([iso(xa, y, z) for (y, z) in ap], 1.1, INK)
    # A0 inclinado
    ap = COC.arch_pts(0.5, 40)
    sh.pl([iso(0.5 - 0.55 * (z / 3.85), y, z) for (y, z) in ap], 1.1, GOLD)
    # terças
    for v in COC.PURLIN_V:
        line = []
        for xa, ap in zip(COC.ARCH_X, arcs):
            y, z = ap[int(v * (len(ap) - 1))]
            line.append(iso(xa, y, z))
        sh.pl(line, 0.5, INK)
    # espinha (treliça) no topo
    sh.pl([iso(x, 0, COC.top(x)) for x in np.linspace(1.75, 6.45, 20)], 1.6, GOLD)
    sh.pl([iso(x, 0, COC.top(x) - 0.3) for x in np.linspace(1.75, 6.45, 20)], 0.7, GOLD)
    for x in np.linspace(1.75, 6.45, 9):
        sh.line(iso(x, 0, COC.top(x))[0], iso(x, 0, COC.top(x))[1], iso(x, 0, COC.top(x) - 0.3)[0], iso(x, 0, COC.top(x) - 0.3)[1], 0.5, GOLD)
    sh.text(iso(9.6, 0, 0)[0], iso(9.6, 0, 0)[1], "cauda", size=8, color=GOLD)
    sh.text(iso(-0.3, 0, 0)[0] - 30, iso(-0.3, 0, 0)[1] + 4, "frente", size=8, color=GOLD)

    # ---------------- Painel D: tabela dos arcos + legenda ----------------
    sh.panel(60, 590, 700, 270, "Tabela dos arcos (tubo Ø88,9 x 3,6 mm, 3 segmentos cada)", "")
    rows = [("A0", "0,50 (base) / -0,05 (topo)", "Ø101,6 x 4,0", "-", "3,85", "10,1*", "anel frontal inclinado 8°")]
    for i, (xa, L) in enumerate(zip(COC.ARCH_X, COC.ARCH_L)):
        rows.append(("A%d" % (i + 1), f(xa).replace(".", ","), "Ø88,9 x 3,6", f(round(2 * COC.a(xa), 2)).replace(".", ","),
                     f(round(COC.top(xa), 2)).replace(".", ","), f(L).replace(".", ","), "2 pernas + coroa; luvas em z = 2,30" if COC.top(xa) > 2.6 else "2 segmentos (luva na coroa)"))
    sh.table(70, 640, ["Arco", "x (m)", "Tubo", "Largura máx. (m)", "Topo z (m)", "L desenv. (m)", "Segmentação"], rows,
             [40, 150, 85, 105, 70, 85, 190], size=9.5, lh=17)
    sh.text(70, 826, "* A0: anel elíptico completo (fechado sob o piso pela viga de borda); apoiado no trilho de base com chapa 150 x 150 x 10 própria.  Total de tubo Ø88,9: 80,4 m.", size=9, color=GOLD)
    sh.text(70, 842, "Todos os segmentos calandrados a frio, galvanizados a fogo após corte/solda e pintados a pó; marcação A1-E / A1-C / A1-D por segmento.", size=9, color=GOLD)
    items = [(1, "Perna do arco (segmento inferior), pé com chapa 200 x 150 x 10"), (2, "Junta com luva interna Ø76 x 200, 4 x M12 8.8 (2 por lado, a 90°)"),
             (3, "Terça Ø48,3 x 3,0 na face interna (7 linhas)"), (4, "Perfil duplo keder de alumínio na face externa (ver DET-01)"),
             (5, "Espinha de Luz: treliça 300 mm (Ø42,4 + diagonais Ø26,9) entre A2 e A6"), (6, "Chapa de base com 4 chumbadores M16 (ver DET-03)"),
             (7, "Luva usinada Ø76,1 x 3,6 x 200, folga 2,8 mm por lado, cola epóxi estrutural"), (8, "Furos Ø13 para M12; 2º par a 90° (oculto)"),
             (9, "Ponteira: inserto rosqueado M16 soldado à terça"), (10, "Talão chapa 8 mm soldado ao arco, furo Ø18"),
             (11, "Presilha inox 3 mm abraçando o arco, parafuso M8"), (12, "Perfil duplo keder 70 x 24 com pingadeira"),
             (13, "Cabos inox Ø8 em X, esticadores M12, olhais nos pés e nas coroas"), (14, "Anel A0 Ø101,6 x 4,0 inclinado 8°, com anel de vidro 120 x 60")]
    sh.legend(790, 726, items, cols=2, colw=380, lh=15.5, size=9.0, title=None)
    sh.write("DET-10_arcos_cocoon.svg")


# ==================================================================================
# DET-11  Mastros e coroas do ZENITH
# ==================================================================================
def det11():
    sh = Sheet("DET-11", "Mastros e coroas", "ZION ZENITH", "1:45 / 1:5 / 1:40",
               "Mastros M1 e M2 com bases articuladas, capitéis usinados, coroas de 3 braços, anéis de cume, anel de beiral parafusado e geometria dos postes estaiados.")
    C = sh.callout
    # ---------------- Painel A: elevações M1 e M2 ----------------
    sh.panel(60, 120, 520, 580, "Elevações  -  mastros M1 e M2", "1:47 (1 mm = 0,08 px)")
    k = 0.08
    t = Tr(230, 672, k)
    X, Y = t.x, t.y
    # --- M1
    sh.line(X(0), Y(-30), X(0), Y(6400), 0.4, INK, dash="10 3 2 3")
    sh.rect(X(-125), Y(12), 250 * k, 12 * k, fill=INK, stroke="none")                    # chapa 250 x 250 x 12
    sh.rect(X(-40), Y(110), 80 * k, 98 * k, fill="url(#p-steel)", stroke=INK, sw=0.8)     # articulação (garfo + pino)
    sh.circle(X(0), Y(70), 15 * k, fill=BG, stroke=INK, sw=0.8)
    sh.rect(X(-69.85), Y(5050), 139.7 * k, 4940 * k, fill=BG, stroke=INK, sw=1.2)        # mastro
    sh.rect(X(-110), Y(5075), 220 * k, 25 * k, fill="url(#p-steel)", stroke=INK, sw=0.8)  # flange do capitel
    sh.pl([(X(-70), Y(5075)), (X(70), Y(5075)), (X(45), Y(5195)), (X(-45), Y(5195))], 0.8, INK, fill="url(#p-steel)", close=True)
    ang = math.radians(56); Larm = 950
    zr = 5150 + Larm * math.sin(ang) - 0   # eixo do anel
    for (dx, fs) in ((-1, 1.0), (1, 0.5)):
        x1 = dx * (55 + Larm * math.cos(ang) * fs)
        sh.tube_seen(X(dx * 55), Y(5150), X(x1), Y(zr), 48.3 * k, 0.9)
    sh.line(X(0), Y(5150), X(0), Y(zr), 0.9, INK, dash="3 2")   # 3º braço (para trás)
    sh.rect(X(-600), Y(zr + 40), 1200 * k, 80 * k, fill="none", stroke=INK, sw=1.4)   # anel Ø1200 (visto)
    sh.rect(X(-600), Y(zr + 40), 1200 * k, 80 * k, fill="url(#p-steel)", stroke="none")
    # cúpula
    R = 1400
    sh.path("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (X(-560), Y(zr + 130), R * k, R * k, X(560), Y(zr + 130)), 1.0, "#8A9DA3")
    sh.path("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z" % (
        X(-560), Y(zr + 130), R * k, R * k, X(560), Y(zr + 130), X(560), Y(zr + 142), (R + 12) * k, (R + 12) * k, X(-560), Y(zr + 142)), 0.5, "#8A9DA3", fill=GLASS)
    # membrana deixando o anel
    for sg in (-1, 1):
        sh.membrane([(X(sg * 615), Y(zr + 20)), (X(sg * 1300), Y(zr + 20 - 685 * 0.87))])
    # cotas M1
    sh.dim_v(X(-760), Y(0), Y(5050), "5,05 (mastro)", ext=None, left=True, size=10)
    sh.dim_v(X(-760), Y(5050), Y(zr), "0,75", ext=None, left=True, size=10)
    sh.label(X(600), Y(zr + 40), X(700), Y(zr + 330), "anel Ø1200", size=9.5, anchor="start")
    sh.label(X(69.85), Y(2600), X(200), Y(2650), "Ø139,7 x 4,5", size=9.5, anchor="start")
    sh.text(X(0), Y(-160), "M1", size=11, anchor="middle", weight=600)
    C(1, X(-69.85), Y(1500), X(-250), Y(1600))
    C(2, X(0), Y(90), X(-250), Y(300))
    C(3, X(0), Y(5130), X(250), Y(5000))
    C(4, X(-330), Y(zr - 300), X(-450), Y(zr - 500))
    C(5, X(-590), Y(zr), X(-700), Y(zr + 300))
    C(6, X(0), Y(zr + 130 + 110), X(200), Y(zr + 420))
    C(7, X(900), Y(zr + 20 - 285 * 0.87), X(1000), Y(zr - 600))
    # --- M2
    t2 = Tr(455, 672, k)
    X2, Y2 = t2.x, t2.y
    sh.line(X2(0), Y2(-30), X2(0), Y2(5500), 0.4, INK, dash="10 3 2 3")
    sh.rect(X2(-100), Y2(12), 200 * k, 12 * k, fill=INK, stroke="none")
    sh.rect(X2(-35), Y2(100), 70 * k, 88 * k, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.rect(X2(-57.15), Y2(4000), 114.3 * k, 3900 * k, fill=BG, stroke=INK, sw=1.2)
    sh.rect(X2(-90), Y2(4022), 180 * k, 22 * k, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.pl([(X2(-57), Y2(4022)), (X2(57), Y2(4022)), (X2(38), Y2(4120)), (X2(-38), Y2(4120))], 0.8, INK, fill="url(#p-steel)", close=True)
    ang2 = math.radians(48); Larm2 = 700
    zr2 = 4090 + Larm2 * math.sin(ang2)
    for (dx, fs) in ((-1, 1.0), (1, 0.5)):
        sh.tube_seen(X2(dx * 45), Y2(4090), X2(dx * (45 + Larm2 * math.cos(ang2) * fs)), Y2(zr2), 48.3 * k, 0.9)
    sh.line(X2(0), Y2(4090), X2(0), Y2(zr2), 0.9, INK, dash="3 2")
    sh.rect(X2(-350), Y2(zr2 + 40), 700 * k, 80 * k, fill="url(#p-steel)", stroke=INK, sw=1.4)
    # chaminé com veneziana e capa
    sh.rect(X2(-330), Y2(zr2 + 40 + 450), 660 * k, 450 * k, fill=BG, stroke=INK, sw=1.0)
    for i in range(5):
        zz = zr2 + 90 + i * 80
        sh.line(X2(-330), Y2(zz), X2(330), Y2(zz + 25), 0.7, INK)
    sh.pl([(X2(-420), Y2(zr2 + 40 + 470)), (X2(0), Y2(zr2 + 40 + 620)), (X2(420), Y2(zr2 + 40 + 470))], 1.4, INK, fill="url(#p-steel)", close=True)
    for sg in (-1, 1):
        sh.membrane([(X2(sg * 365), Y2(zr2 + 20)), (X2(sg * 900), Y2(zr2 + 20 - 535 * 0.72))])
    sh.dim_v(X2(430), Y2(0), Y2(4000), "4,00 (mastro)", ext=None, left=False, size=10)
    sh.dim_v(X2(430), Y2(4000), Y2(zr2), "0,52", ext=None, left=False, size=9)
    sh.dim_h(X2(-350), X2(350), Y2(zr2 + 40 + 700), "Ø700", ext=None, size=10)
    sh.label(X2(57.15), Y2(2000), X2(150), Y2(2050), "Ø114,3 x 4,0", size=9.5, anchor="start")
    sh.text(X2(0), Y2(-160), "M2", size=11, anchor="middle", weight=600)
    sh.line(X(-900), Y(0), X2(700), Y(0), 1.4, INK)
    sh.text(X2(300), Y2(60), "piso acabado z = 0", size=9, color=GOLD)
    C(8, X2(-330), Y2(zr2 + 300), X2(-520), Y2(zr2 + 450))
    C(9, X2(200), Y2(zr2 + 40 + 550), X2(500), Y2(zr2 + 650))
    sh.scale_bar(80, 692, k, 1000, "1,0 m")

    # ---------------- Painel B: base articulada M1 1:5 ----------------
    sh.panel(600, 120, 330, 300, "Base articulada do M1", "1:5 (1 mm = 0,6 px)")
    kb = 0.6
    tb = Tr(735, 380, kb)
    XB, YB = tb.x, tb.y
    sh.rect(XB(-160), YB(0), 320 * kb, 18 * kb, fill="url(#p-ply)", stroke=INK, sw=0.6)         # compensado
    sh.rect(XB(-125), YB(12), 250 * kb, 12 * kb, fill=INK, stroke="none")                         # chapa 250 x 250 x 12
    sh.rect(XB(-160), YB(-18), 320 * kb, 42 * kb, fill="url(#p-ply)", stroke=INK, sw=0.6)        # viga U dupla (vista, cortada)
    for xb in (-95, 95):
        sh.bolt_side(XB(xb), YB(12), 60 * kb, 6, vertical=True)
    sh.rect(XB(-8), YB(112), 16 * kb, 100 * kb, fill="url(#p-steel)", stroke=INK, sw=0.9)         # orelha central 16 mm
    for xf in (-30, 14):
        sh.rect(XB(xf), YB(140), 16 * kb, 100 * kb, fill=INK, stroke="none")                      # garfo 2 x 16
    sh.circle(XB(0), YB(70), 15 * kb, fill=BG, stroke=INK, sw=1.2)                                # pino Ø30
    sh.circle(XB(0), YB(70), 4 * kb, fill=INK, stroke="none")
    sh.rect(XB(-69.85), YB(300), 139.7 * kb, 160 * kb, fill=BG, stroke=INK, sw=1.2)               # mastro
    sh.rect(XB(-69.85), YB(300), 4.5 * kb, 160 * kb, fill=INK, stroke="none"); sh.rect(XB(65.35), YB(300), 4.5 * kb, 160 * kb, fill=INK, stroke="none")
    sh.rect(XB(-75), YB(140), 150 * kb, 10 * kb, fill=INK, stroke="none")                         # chapa de fundo do mastro
    sh.break_line(XB(-75), YB(300), XB(75), YB(300), 4)
    sh.dim_h(XB(-125), XB(125), YB(-40), "250 x 250 x 12", ext=None, above=False, size=9.5)
    sh.label(XB(0), YB(70), XB(60), YB(60), "pino Ø30 inox + anéis", size=9, anchor="start")
    sh.label(XB(-22), YB(200), XB(-60), YB(240), "garfo 2 x ch. 16", size=9, anchor="end")
    sh.label(XB(95), YB(40), XB(120), YB(0), "4 x M16", size=9, anchor="start")
    sh.text(XB(80), YB(300), "articulação: içamento", size=8.5, color=GOLD)
    sh.text(XB(80), YB(280), "por rotação; libera", size=8.5, color=GOLD)
    sh.text(XB(80), YB(260), "momento na base", size=8.5, color=GOLD)
    C(10, XB(0), YB(120), XB(80), YB(160))

    # ---------------- Painel C: anel de beiral ----------------
    sh.panel(950, 120, 590, 300, "Anel de beiral 150 x 100 x 4: segmentos e emenda", "1:60 / 1:5")
    kr = 18
    rx, ry = 985, 300
    RX = lambda xm: rx + xm * kr
    RY = lambda ym: ry - ym * kr
    sh.rect(RX(0), RY(2.7), 9.5 * kr, 5.4 * kr, fill="none", stroke=INK, sw=2.4)
    # 6 segmentos: emendas em (3,2; ±2,7), (6,4; ±2,7), (9,5; 0), (0; 0)
    joints = [(3.2, 2.7), (6.4, 2.7), (3.2, -2.7), (6.4, -2.7), (0, 0), (9.5, 0)]
    for (jx, jy) in joints:
        sh.rect(RX(jx) - 4, RY(jy) - 4, 8, 8, fill=BG, stroke=INK, sw=1.0)
    for (cxp, cyp) in ((0, -2.7), (0, 2.7), (9.5, -2.7), (9.5, 2.7), (3.2, -2.7), (3.2, 2.7), (6.4, -2.7), (6.4, 2.7), (9.5, 0.0), (0.0, 0.0)):
        sh.circle(RX(cxp), RY(cyp), 2.2, fill=INK, stroke="none")
    sh.text(RX(4.75), RY(3.35), "S1  (0 a 3,2)     S2  (3,2 a 6,4)     S3  (6,4 a 9,5)", size=7.5, anchor="middle", color=GOLD)
    sh.text(RX(4.75), RY(-3.3), "S4, S5, S6 simétricos; cantos soldados em fábrica", size=7.5, anchor="middle", color=GOLD)
    sh.text(RX(4.75), RY(0), "6 segmentos, 29,8 m; emendas nos pilares", size=7.5, anchor="middle", color=GOLD)
    sh.text(RX(-0.6), RY(1.2), "5,40", size=8, anchor="middle", color=GOLD, rotate=-90)
    C(11, RX(0), RY(-1.8), RX(-0.9), RY(-1.2))
    # emenda 1:5
    ke_ = 0.6
    te = Tr(1390, 300, ke_)
    XE, YE = te.x, te.y
    sh.text(1240, 165, "emenda: chapas de topo 220 x 170 x 10 + 4 x M16", size=9, color=GOLD)
    for (x0, x1) in ((-170, -10), (10, 170)):
        sh.rect(XE(x0), YE(75), (x1 - x0) * ke_, 150 * ke_, fill="none", stroke=INK, sw=1.2)
        sh.rect(XE(x0), YE(75), (x1 - x0) * ke_, 4 * ke_, fill=INK, stroke="none")
        sh.rect(XE(x0), YE(-71), (x1 - x0) * ke_, 4 * ke_, fill=INK, stroke="none")
    sh.rect(XE(-10), YE(110), 10 * ke_, 220 * ke_, fill=INK, stroke="none")
    sh.rect(XE(0), YE(110), 10 * ke_, 220 * ke_, fill=INK, stroke="none")
    for zb in (95, -95):
        sh.bolt_side(XE(-30), YE(zb), 60 * ke_, 6, vertical=False)
    sh.rect(XE(-75), YE(-75), 150 * ke_, 8 * ke_, fill=INK, stroke="none")      # chapa de topo do pilar
    sh.rect(XE(-50.8), YE(-83), 101.6 * ke_, 80 * ke_, fill=BG, stroke=INK, sw=1.0)
    sh.rect(XE(-50.8), YE(-83), 4 * ke_, 80 * ke_, fill=INK, stroke="none"); sh.rect(XE(46.8), YE(-83), 4 * ke_, 80 * ke_, fill=INK, stroke="none")
    sh.break_line(XE(-55), YE(-163), XE(55), YE(-163), 3)
    sh.dim_v(XE(200), YE(75), YE(-75), "150", ext=None, left=False, size=9)
    sh.dim_v(XE(-200), YE(110), YE(-110), "220", ext=None, left=True, size=9)
    sh.label(XE(-30), YE(95), XE(-90), YE(150), "M16 8.8 (4)", size=9, anchor="end")
    sh.label(XE(50), YE(-120), XE(120), YE(-140), "pilar Ø101,6 x 4,0", size=9, anchor="start")
    C(12, XE(5), YE(0), XE(90), YE(40))

    # ---------------- Painel D: postes e estais ----------------
    sh.panel(600, 440, 620, 260, "Poste externo inclinado 8° e estai  -  geometria", "1:40 (1 m = 25 px)")
    kp = 25
    px0, py0 = 900, 660
    PX = lambda xm: px0 + xm * kp
    PY = lambda zm: py0 - zm * kp
    sh.line(PX(-4.0), PY(0), PX(3.5), PY(0), 1.0, INK)
    sh.soil(PX(-4.0), PY(0), 7.5 * kp, 1.2 * kp)
    a8 = math.radians(8)
    top = (-2.65 * math.sin(a8), 2.65 * math.cos(a8))
    sh.tube_seen(PX(0), PY(0.25), PX(top[0]), PY(top[1] + 0.25), 76.1 * kp / 1000 + 2, 1.0)
    sh.circle(PX(top[0]), PY(top[1] + 0.3), 3, fill=BG, stroke=INK, sw=1.0)
    anchor = (-1.5, 0.15)
    sh.cable(PX(top[0] - 0.05), PY(top[1] + 0.28), PX(anchor[0]), PY(anchor[1]), 1.4)
    sh.turnbuckle(PX((top[0] + anchor[0]) / 2), PY((top[1] + 0.28 + anchor[1]) / 2), -math.degrees(math.atan2((top[1] + 0.28 - anchor[1]), (top[0] - anchor[0]))) + 180, 16, 6)
    sh.rect(PX(anchor[0]) - 3, PY(anchor[1]), 6, 1.0 * kp, fill=BG, stroke=INK, sw=0.9)
    sh.pl([(PX(anchor[0] - 0.15), PY(-0.7)), (PX(anchor[0] + 0.15), PY(-0.8))], 1.4, INK)
    sh.rect(PX(0) - 3, PY(0.25), 6, 1.0 * kp, fill=BG, stroke=INK, sw=0.9)
    sh.pl([(PX(-0.15), PY(-0.7)), (PX(0.15), PY(-0.8))], 1.4, INK)
    # membrana e cabo de borda (para o corpo, à direita)
    sh.membrane([(PX(top[0] + 0.1), PY(top[1] + 0.3)), (PX(2.4), PY(2.9)), (PX(3.4), PY(3.3))])
    sh.cable(PX(top[0]), PY(top[1] + 0.3), PX(2.0), PY(top[1] + 0.05), 1.0)
    # geometria: ângulos e componentes
    sh.line(PX(0), PY(0.25), PX(0), PY(top[1] + 0.25), 0.5, GOLD, dash="3 2")
    sh.text(PX(-0.55), PY(2.2), "8°", size=9, color=GOLD)
    sh.dim_h(PX(top[0]), PX(0), PY(top[1] + 0.9), "0,37", ext=None, size=9)
    sh.dim_h(PX(anchor[0]), PX(0), PY(-1.05), "1,50", ext=None, above=False, size=9)
    sh.dim_v(PX(0.7), PY(0.25), PY(top[1] + 0.25), "2,65", ext=None, left=False, size=9)
    ang_stay = math.degrees(math.atan2(top[1] + 0.28 - anchor[1], -(anchor[0] - top[0])))
    sh.text(PX(-1.15), PY(0.45), "estai %s°" % f(round(ang_stay)), size=9, color=GOLD)
    sh.texts(PX(1.6), PY(1.9), ["Poste Ø76,1 x 3,6: T_membrana ≈ 6 a 9 kN", "→ compressão no poste ≈ 8 kN;",
                                "estai Ø10 inox: F ≈ 8,5 kN (MBL 60 kN);", "estaca de tração: 15 a 25 kN (FS ≥ 2)."], size=8.5, lh=12, color=GOLD)
    C(13, PX(top[0] / 2), PY(top[1] / 2 + 0.25), PX(-1.6), PY(2.2))
    C(14, PX(anchor[0]), PY(anchor[1] - 0.3), PX(-2.4), PY(0.9))

    # ---------------- caminho de cargas ----------------
    sh.note(1250, 466, ["CAMINHO DE CARGAS E PREMISSAS",
                        "Vento V0 = 45 m/s, q ≈ 1,2 kN/m²; uplift de projeto 1,3 kN/m²",
                        "x 95 m² ≈ 125 kN (10 pilares + 7 postes estaiados + 16 estacas).",
                        "Membrana: pré-tensão 2,5 kN/m → anéis de cume (tração radial)",
                        "→ coroas de 3 braços → capitel usinado → mastro em compressão",
                        "(M1: 45 kN de projeto) → base articulada → quadro U 150 → estacas.",
                        "M1 Ø139,7 x 4,5: A = 19,1 cm², i = 4,78 cm, λ ≈ 106,",
                        "N_Rd ≈ 300 kN >> 45 kN (folga para neve e vento assimétrico).",
                        "Anel de beiral: viga-anel comprimida pela membrana + diafragma SIP.",
                        "Cabo de borda Ø12: T = p L² / 8f ≈ 2,5 x 6,5² / (8 x 0,35) ≈ 38 kN",
                        "(MBL 85 kN); esticadores nos postes; verificar no form-finding.",
                        "Postes a 8°: componente horizontal da borda vai ao estai."], size=9, w=290)
    items = [(1, "Mastro M1 Ø139,7 x 4,5 mm, 5,05 m, galvanizado + pó"), (2, "Base articulada: chapa 250 x 250 x 12, garfo, pino Ø30"),
             (3, "Capitel usinado (bujão + flange Ø220 + cubo cônico)"), (4, "Braço da coroa Ø48,3 x 3,0, L 0,95 m, 3 a 120°"),
             (5, "Anel do Zênite: chapa curvada 80 x 10, Ø1200"), (6, "Óculo: cúpula de vidro laminado sobre moldura RPT"),
             (7, "Membrana deixando o anel a ≈ 41°"), (8, "Chaminé do Respiro Ø660 com veneziana motorizada"),
             (9, "Capa da chaminé (chapa de alumínio) com tela"), (10, "Orelha central 16 mm soldada à chapa de base"),
             (11, "Emendas do anel de beiral sobre os pilares"), (12, "Chapas de topo 220 x 170 x 10 soldadas (a = 5)"),
             (13, "Poste Ø76,1 x 3,6, 2,65 a 2,90 m, olhal no topo"), (14, "Estaca helicoidal de tração com olhal; estai Ø10 + esticador")]
    sh.legend(60, 728, items, cols=3, colw=325, lh=15.5, size=9.0, title=None)
    sh.write("DET-11_mastros_zenith.svg")


# ==================================================================================
def main():
    for fn in (det01, det02, det03, det04, det05, det06, det07, det08, det09, det10, det11):
        fn()


if __name__ == "__main__":
    main()
