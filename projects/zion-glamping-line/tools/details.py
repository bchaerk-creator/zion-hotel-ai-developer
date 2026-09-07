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
        self.text(x + 14, y + 24, "Zion Glamping Collection", size=12, ls="0.22em", weight=600, color=GOLD,
                  family=None)
        self.add('<text x="%.1f" y="%.1f" fill="%s" style="font-size:12px;letter-spacing:0.22em;font-weight:600;font-variant:small-caps"></text>' % (x + 14, y + 24, GOLD))
        self.text(x + 14, y + 50, self.title, size=14, weight=600, caps=True)
        self.text(x + 14, y + 74, self.unit, size=11.5, color=GOLD, ls="0.15em")
        self.text(x + 312, y + 16, "ESCALA", size=9, color=GOLD, ls="0.15em")
        self.text(x + 312, y + 36, self.scale, size=13)
        self.text(x + 312, y + 61, "FOLHA", size=9, color=GOLD, ls="0.15em")
        self.text(x + 312, y + 84, self.num, size=20, weight=600)
        self.text(x + 422, y + 61, "DATA", size=9, color=GOLD, ls="0.15em")
        self.text(x + 422, y + 84, DATE, size=13)
        self.text(x + 422 + 0, y + 16, "", size=9)

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
    sh.pl([(X2(a), D2(b)) for a, b in rail if True], 1.4, INK, fill="url(#p-steel)", close=True) if False else None
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
        sh.pl([(X(p[0]), Y(p[1])) for p in a], 8, "url(#p-ins)") if False else None
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
    C(14, X(-500), Y(zr - 160), X(-600), Y(zr - 300)) if False else None
    C(15, X(390), Y(zr - 200 + 300), X(520), Y(zr + 250 - 300)) if False else None
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
    sh.text(X(-150), Y(zt + 45), "M16 (4)", size=9.5, anchor="middle", color=GOLD)
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
    t3 = Tr(1010, 655, k3)
    X3, Y3 = t3.x, t3.y
    sh.rect(935, 445, 170, 228, fill=BG, stroke=GOLD, sw=0.5, dash="3 2")
    sh.text(942, 668, "base articulada  1:5", size=10, color=GOLD)
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
    ptop3 = (-95 * math.sin(a8), 58 + 150 + 95 * math.cos(a8))
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
    sh.membrane([(X4(10), Y4(-16)), (X4(90), Y4(-16)), (X4(90), Y4(-12)), (X4(140), Y4(-12))]) if False else None
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
    sh.text(X5(160), Y5(38), "cinta 50", size=9.5, anchor="middle", color=GOLD)
    sh.pl([(X5(235), Y5(-25)), (X5(340), Y5(-95))], 3, GOLD)   # membrana de canto (bordas)
    sh.pl([(X5(235), Y5(25)), (X5(340), Y5(95))], 3, GOLD)
    sh.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (X5(340), Y5(-95), X5(300), Y5(0), X5(340), Y5(95)), 0.6, GOLD, dash="3 2")
    sh.text(X5(300), Y5(-4), "membrana", size=9.5, color=GOLD, anchor="middle")
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
    sh.text(X(1300), Y(zj + 60), "PIR 50 entre vigotas", size=9.5, color=GOLD, anchor="middle") if False else None
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
    sh = Sheet("DET-05", "Esquadrias", "COMUM", "1:10 / 1:5 / 1:40",
               "(a) Janela Olho do Cocoon; (b) fachada de vidro inclinada 8° do Cocoon; (c) fachada frontal do Zenith; (d) fresta no painel SIP.")
    C = sh.callout
    # ---------------- (a) Janela Olho ----------------
    sh.panel(60, 120, 700, 400, "(a)  Janela Olho 1600 x 950: seção vertical e elevação", "1:10 (1 mm = 0,32 px) / 1:40")
    k = 0.32
    t = Tr(430, 470, k)     # origem: peitoril externo da janela (x=0, z=0). Exterior à esquerda.
    X, Y = t.x, t.y
    sh.add('<clipPath id="c5a"><rect x="62" y="148" width="696" height="370"/></clipPath>')
    sh.add('<g clip-path="url(#c5a)">')
    ang = math.radians(28)     # parede inclinada para dentro no topo
    ux, uz = math.sin(ang), math.cos(ang)
    nx, nz = -math.cos(ang), math.sin(ang)   # normal para fora (esquerda/cima)
    def P(s, d):
        return (X(ux * s + nx * d), Y(uz * s + nz * d))
    # camadas abaixo e acima da janela
    wall_layers(sh, X, Y, ang, 0, 0, 0, -1)
    for (s0, s1) in ((-330, -20), (970, 1280)):
        sh.membrane([P(s0, 0), P(s1, 0)])
        for (d1, d2, pat) in ((-60, -64, "p-steel"), (-64, -114, "p-ins")):
            sh.pl([P(s0, d1), P(s1, d1), P(s1, d2), P(s0, d2)], 0.6, INK, fill="url(#%s)" % pat, close=True)
        sh.pl([P(s0, -196), P(s1, -196)], 2.2, INK)
    # requadro de madeira laminada 220 x 40 (peitoril e verga), perpendicular à parede
    for (s0, s1) in ((-20, 20), (930, 970)):
        sh.pl([P(s0, 10), P(s1, 10), P(s1, -210), P(s0, -210)], 1.6, INK, fill="url(#p-wood)", close=True)
    # grampo de alumínio da membrana no bordo externo do requadro + gaxeta
    for (s0, s1, sg) in ((-20, -5, 1), (970, 985, -1)):
        sh.pl([P(s0 - 30 * sg if sg > 0 else s0, 12), P(s1 if sg > 0 else s1 + 30, 12), P(s1 if sg > 0 else s1 + 30, 4), P(s0 - 30 * sg if sg > 0 else s0, 4)],
              0.8, INK, fill="url(#p-steel)", close=True)
    # pingadeira de alumínio na verga (sobre o grampo)
    sh.pl([P(1000, 6), P(1000, 30), P(925, 30), P(925, 18)], 1.4, INK)
    # marco de alumínio com ruptura térmica 60 x 70 encaixado no requadro (terço externo)
    for (s0, s1) in ((20, 80), (870, 930)):
        sh.pl([P(s0, -40), P(s1, -40), P(s1, -110), P(s0, -110)], 1.0, INK, fill="url(#p-steel)", close=True)
        sh.pl([P(s0, -70), P(s1, -70), P(s1, -80), P(s0, -80)], 0.5, INK, fill=BG, close=True)   # ruptura poliamida
    # folha basculante (projeção): dobradiça superior, aberta 15° para fora
    sh.circle(P(870, -60)[0], P(870, -60)[1], 3, fill=INK, stroke="none")
    # vidro fechado 6 lam + 12 ar + 6 temp
    p1, p2 = P(80, -75), P(870, -75)
    sh.glass(p1[0], p1[1], p2[0], p2[1], t=24 * k)
    # folha aberta (linha fina tracejada) girando na dobradiça superior
    a2 = ang + math.radians(15)
    L2 = 790
    hinge = P(870, -60)
    end = (hinge[0] - math.sin(a2) * L2 * k * 0 - (L2 * k) * math.sin(a2), hinge[1] + (L2 * k) * math.cos(a2))
    sh.line(hinge[0], hinge[1], end[0], end[1], 0.7, INK, dash="5 3")
    sh.text(end[0] - 10, end[1] + 12, "abertura 15° (braço de fricção)", size=9.5, anchor="end", color=GOLD)
    # gaxetas EPDM + silicone e canal de condensação no peitoril
    sh.circle(P(35, -35)[0], P(35, -35)[1], 2.2, fill=INK, stroke="none")
    sh.circle(P(915, -35)[0], P(915, -35)[1], 2.2, fill=INK, stroke="none")
    sh.line(P(-12, 8)[0], P(-12, 8)[1], P(-12, 30)[0], P(-12, 30)[1], 1.2, INK)   # pingadeira do peitoril (friso)
    # forro chegando ao requadro; fita LED no requadro
    sh.circle(P(60, -200)[0], P(60, -200)[1], 2.5, fill=GOLD, stroke="none")
    sh.circle(P(900, -200)[0], P(900, -200)[1], 2.5, fill=GOLD, stroke="none")
    sh.add('</g>')
    sh.dim_a(P(-20, -215)[0], P(-20, -215)[1], P(-20, 10)[0], P(-20, 10)[1], "220", off=16, size=10)
    sh.dim_a(P(20, -130)[0], P(20, -130)[1], P(930, -130)[0], P(930, -130)[1], "950 (vão)", off=-18, size=10)
    sh.text(X(-330), Y(120), "EXTERIOR", size=9.5, color=GOLD, ls="0.2em")
    sh.text(X(150), Y(120), "INTERIOR", size=9.5, color=GOLD, ls="0.2em")
    C(1, P(200, 0)[0], P(200, 0)[1], X(-260), Y(400))
    C(2, P(0, -100)[0], P(0, -100)[1], X(-120), Y(-10))
    C(3, P(50, -75)[0], P(50, -75)[1], X(120), Y(30))
    C(4, P(500, -75)[0], P(500, -75)[1], X(90), Y(500))
    C(5, P(875, -62)[0], P(875, -62)[1], X(560), Y(470))
    C(6, P(960, 25)[0], P(960, 25)[1], X(20), Y(1000)) if False else None
    C(6, P(960, 26)[0], P(960, 26)[1], X(-330), Y(870))
    C(7, P(-12, 20)[0], P(-12, 20)[1], X(-240), Y(-10))
    C(8, P(1100, -196)[0], P(1100, -196)[1], X(200), Y(1000))
    C(9, P(60, -200)[0], P(60, -200)[1], X(260), Y(200))
    # elevação da lente 1:40 (canto inferior direito do painel)
    lk = 0.1
    cx, cy = 655, 440
    sh.pl(lens_pts(cx, cy, 800 * lk, 475 * lk), 1.2, INK, fill=GLASS, close=True)
    sh.pl(lens_pts(cx, cy, 800 * lk + 22 * 1.0, 475 * lk + 22 * 1.0), 0.8, INK, close=True)
    sh.dim_h(cx - 80, cx + 80, cy - 78, "1600", ext=None, size=10)
    sh.dim_v(cx + 100, cy - 47.5, cy + 47.5, "950", ext=None, left=False, size=10)
    sh.text(cx, cy + 90, "elevação 1:40 (superelipse n = 1,5)", size=9.5, anchor="middle", color=GOLD)

    # ---------------- (b) fachada de vidro do Cocoon ----------------
    sh.panel(790, 120, 750, 400, "(b)  Fachada de vidro Cocoon inclinada 8°: elevação e detalhes", "1:40 / 1:5")
    # elevação 1:40 (0,1 px/mm): contorno da concha em x = 1,0 (a ≈ 2,79, b ≈ 3,14)
    ek = 0.1
    ex, ey = 1000, 470
    a_, b_ = COC.a(1.0) * 1000, COC.b(1.0) * 1000
    pts = [(ex + p[0] * 1000 * ek, ey - p[1] * 1000 * ek) for p in COC.arch_pts(1.0, 100)]
    sh.pl(pts, 1.6, INK, fill="none")
    sh.line(pts[0][0], ey, pts[-1][0], ey, 1.6, INK)
    # anel de alumínio 120 x 60 (offset 120 mm para dentro)
    inner = [(ex + p[0] * 1000 * ek * 0.955, ey - (p[1] * 1000 - 40) * ek * 0.96) for p in COC.arch_pts(1.0, 100)]
    sh.pl(inner, 0.8, INK, fill=GLASS)
    # montantes verticais a cada ~1,1 m e porta pivotante à direita (1000 x 2400)
    for xm in (-1700, -600, 500):
        top_z = COC.ZC + COC.b(1.0) * math.sqrt(max(0, 1 - (xm / 1000 / COC.a(1.0)) ** 2))
        sh.line(ex + xm * ek, ey, ex + xm * ek, ey - top_z * 1000 * ek + 8, 1.2, INK)
    sh.rect(ex + 500 * ek, ey - 2400 * ek, 1000 * ek, 2400 * ek, fill="none", stroke=INK, sw=1.4)
    sh.line(ex + 500 * ek, ey - 2400 * ek, ex + 1500 * ek, ey, 0.5, INK)
    sh.circle(ex + 640 * ek, ey - 1100 * ek, 2.5, fill=INK, stroke="none")     # puxador
    sh.line(ex - 3000 * ek, ey - 800 * ek, ex + 3000 * ek, ey - 800 * ek, 0.4, GOLD, dash="4 3")   # travessa
    sh.line(ex - 2500 * ek, ey - 2200 * ek, ex + 2500 * ek, ey - 2200 * ek, 0.4, GOLD, dash="4 3")
    sh.dim_h(ex + 500 * ek, ex + 1500 * ek, ey + 14, "1000", ext=None, above=False, size=10)
    sh.dim_v(ex + 1600 * ek, ey - 2400 * ek, ey, "2400", ext=None, left=False, size=10)
    sh.dim_h(pts[0][0], pts[-1][0], ey + 36, "≈ 5,60 m", ext=None, above=False, size=10)
    sh.text(ex, ey - 3550 * ek, "elevação 1:40 (plano inclinado 8°)", size=9.5, anchor="middle", color=GOLD)
    C(10, ex - 2100 * ek, ey - 2400 * ek, ex - 2650 * ek, ey - 3300 * ek)
    C(11, ex - 600 * ek, ey - 1600 * ek, ex - 1200 * ek, ey - 500 * ek)
    C(12, ex + 1000 * ek, ey - 1800 * ek, ex + 2100 * ek, ey - 3000 * ek)
    # detalhe topo 1:5 (anel A0 Ø101,6 + anel alumínio 120 x 60 + vidro)
    k5 = 0.5
    t5 = Tr(1330, 300, k5)
    X5, Y5 = t5.x, t5.y
    sh.text(1240, 168, "detalhe topo  1:5", size=9.5, color=GOLD)
    a8 = math.radians(8)
    sh.tube_cut(X5(0), Y5(0), 50.8 * k5, 4 * k5)
    # perfil keder da membrana no anel (topo) e membrana indo para trás (direita = interior/cobertura)
    sh.rect(X5(-20), Y5(51), 40 * k5, 22 * k5, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.membrane([(X5(0), Y5(73)), (X5(80), Y5(78)), (X5(260), Y5(60))])
    # anel de alumínio 120 x 60 parafusado sob o tubo, inclinado 8°; vidro pendurado
    sh.add('<g transform="rotate(-8 %.1f %.1f)">' % (X5(0), Y5(-50)))
    sh.rect(X5(-60), Y5(-50), 120 * k5, 60 * k5, fill="url(#p-steel)", stroke=INK, sw=1.0)
    sh.rect(X5(-12), Y5(-110), 24 * k5, 180 * k5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.rect(X5(-40), Y5(-110), 80 * k5, 18 * k5, fill="url(#p-steel)", stroke=INK, sw=0.8)
    sh.add('</g>')
    sh.bolt_side(X5(-35), Y5(-52), 35 * k5, 4, vertical=True)
    sh.bolt_side(X5(35), Y5(-52), 35 * k5, 4, vertical=True)
    sh.label(X5(0), Y5(0), X5(-70), Y5(40), "anel A0 Ø101,6 x 4, 8°", size=9.5, anchor="end")
    sh.label(X5(-58), Y5(-80), X5(-100), Y5(-110), "anel alumínio 120 x 60 curvo", size=9.5, anchor="end")
    sh.label(X5(0), Y5(-200), X5(60), Y5(-215), "vidro 6 lam + 12 Ar + 6 temp", size=9.5, anchor="start")
    sh.label(X5(150), Y5(66), X5(150), Y5(110), "membrana da concha", size=9.5, anchor="start")
    sh.text(X5(-140), Y5(-30), "8°", size=10, color=GOLD)
    # detalhe soleira 1:5 (mola de piso da porta pivotante)
    t6 = Tr(1450, 470, k5)
    X6, Y6 = t6.x, t6.y
    sh.text(1240, 470, "detalhe soleira  1:5", size=9.5, color=GOLD)
    sh.rect(X6(-160), Y6(0), 320 * k5, 18 * k5, fill="url(#p-ply)", stroke=INK, sw=0.8)     # compensado
    sh.wood(X6(-160), Y6(14), 100 * k5, 14 * k5, grain=False)
    sh.rect(X6(-60), Y6(14), 120 * k5, 14 * k5, fill="url(#p-steel)", stroke=INK, sw=0.8)   # tampa da mola
    sh.rect(X6(-50), Y6(0), 100 * k5, 60 * k5, fill=BG, stroke=INK, sw=1.0)                # caixa da mola de piso
    sh.rect(X6(-45), Y6(-4), 90 * k5, 50 * k5, fill="url(#p-steel)", stroke="none")
    sh.rect(X6(-8), Y6(14 + 60), 16 * k5, 60 * k5, fill=GLASS, stroke="#8A9DA3", sw=0.6)  # vidro da porta
    sh.rect(X6(-14), Y6(14 + 12), 28 * k5, 12 * k5, fill=INK, stroke="none")                # pivô
    sh.wood(X6(60), Y6(14), 100 * k5, 14 * k5, grain=False)
    sh.label(X6(0), Y6(-30), X6(90), Y6(-40), "mola de piso (caixa 100 x 60)", size=9.5, anchor="start")
    sh.label(X6(0), Y6(60), X6(60), Y6(80), "porta pivotante 1000 x 2400", size=9.5, anchor="start")

    # ---------------- (c) fachada frontal do Zenith ----------------
    sh.panel(60, 540, 700, 320, "(c)  Fachada frontal Zenith 5400 x 2750: 2 fixas + 2 de correr", "1:40 / 1:5")
    fk = 0.08
    fx, fy = 300, 800
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
    sh.dim_h(fx - 2700 * fk, fx + 2700 * fk, fy + 16, "5400 (4 x 1350)", ext=None, above=False, size=10)
    sh.dim_v(fx - 2850 * fk, fy - 2750 * fk, fy, "2750", ext=None, left=True, size=10)
    C(13, fx - 2025 * fk, fy - 2200 * fk, fx - 2400 * fk, fy - 3200 * fk)
    C(14, fx + 600 * fk, fy - 2200 * fk, fx + 900 * fk, fy - 3200 * fk)
    C(15, fx, fy - 2750 * fk, fx + 1800 * fk, fy - 3200 * fk)
    # detalhe soleira 1:5: trilho embutido nivelado com o deck, drenagem
    t7 = Tr(600, 730, 0.5)
    X7, Y7 = t7.x, t7.y
    sh.text(465, 588, "soleira com drenagem  1:5", size=9.5, color=GOLD)
    sh.add('<clipPath id="c5c"><rect x="450" y="595" width="308" height="262"/></clipPath>')
    sh.add('<g clip-path="url(#c5c)">')
    # exterior à esquerda: deck 20 x 140 sobre vigota; interior à direita: piso 14 sobre compensado 18
    sh.wood(X7(-220), Y7(0), 200 * 0.5, 20 * 0.5, grain=False)
    sh.rect(X7(-220), Y7(-20), 200 * 0.5, 18 * 0.5, fill="url(#p-ply)", stroke=INK, sw=0.6)
    sh.wood(X7(60), Y7(0), 200 * 0.5, 14 * 0.5, grain=False)
    sh.rect(X7(60), Y7(-14), 200 * 0.5, 18 * 0.5, fill="url(#p-ply)", stroke=INK, sw=0.6)
    sh.rect(X7(-240), Y7(-38), 520 * 0.5, 150 * 0.5, fill="url(#p-ply)", stroke=INK, sw=0.8)   # vigota/viga de borda (vista)
    # trilho de alumínio embutido: canal 120 x 40 com 2 guias e dreno
    sh.pl([(X7(-20), Y7(0)), (X7(-20), Y7(-40)), (X7(60), Y7(-40)), (X7(60), Y7(0))], 1.4, INK, fill=BG)
    for xg in (0, 40):
        sh.rect(X7(xg - 3), Y7(-2), 6 * 0.5, 14 * 0.5, fill=INK, stroke="none")
    # folhas: fixa (direita) e de correr (esquerda), vidros 6+12+6 sobre os trilhos
    sh.rect(X7(-12), Y7(120), 24 * 0.5, 108 * 0.5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.rect(X7(-14), Y7(20), 28 * 0.5, 22 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.6)   # carrinho/roldana
    sh.circle(X7(0), Y7(6), 4, fill=BG, stroke=INK, sw=0.8)
    sh.rect(X7(28), Y7(120), 24 * 0.5, 130 * 0.5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    sh.rect(X7(26), Y7(0), 28 * 0.5, 12 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.6)
    # dreno do canal: furos Ø8 + tubo Ø20 ao exterior / calha
    sh.line(X7(-20), Y7(-38), X7(-120), Y7(-70), 1.2, INK)
    sh.line(X7(-20), Y7(-42), X7(-120), Y7(-74), 1.2, INK)
    sh.arrow(X7(-60), Y7(-54), X7(-110), Y7(-70), 0.9, GOLD, head=5)
    sh.arrow(X7(-200), Y7(30), X7(-120), Y7(30), 0.9, GOLD, head=5, dash="3 2")
    sh.add('</g>')
    sh.label(X7(20), Y7(-40), X7(60), Y7(-90), "trilho embutido 120 x 40, nivelado", size=9.5, anchor="start")
    sh.label(X7(-70), Y7(-56), X7(-160), Y7(-105), "dreno Ø20 à calha", size=9.5, anchor="end")
    sh.label(X7(0), Y7(30), X7(-120), Y7(80), "roldana inox, folha de correr", size=9.5, anchor="end")
    sh.label(X7(40), Y7(90), X7(80), Y7(110), "folha fixa", size=9.5, anchor="start")
    sh.text(X7(-160), Y7(150), "deck", size=9.5, color=GOLD)
    sh.text(X7(130), Y7(150), "piso interno", size=9.5, color=GOLD)

    # ---------------- (d) fresta no painel SIP ----------------
    sh.panel(790, 540, 750, 320, "(d)  Fresta de vidro no painel SIP 100 com rufos", "1:5 (1 mm = 0,5 px)")
    t8 = Tr(1060, 700, 0.5)
    X8, Y8 = t8.x, t8.y
    sh.add('<clipPath id="c5d"><rect x="792" y="568" width="746" height="290"/></clipPath>')
    sh.add('<g clip-path="url(#c5d)">')
    # parede SIP vertical (exterior à esquerda): trecho abaixo (peitoril) e acima (verga) da fresta de 300 mm
    def sip(z0, z1):
        h = (z1 - z0) * 0.5
        sh.rect(X8(-50), Y8(z1), 12 * 0.5, h, fill="url(#p-osb)", stroke=INK, sw=0.8)
        sh.rect(X8(38), Y8(z1), 12 * 0.5, h, fill="url(#p-osb)", stroke=INK, sw=0.8)
        sh.rect(X8(-38), Y8(z1), 76 * 0.5, h, fill="url(#p-pir)", stroke="none")
        sh.rect(X8(-62), Y8(z1), 12 * 0.5, h, fill="url(#p-cem)", stroke=INK, sw=0.8)   # cimentícia
        sh.rect(X8(-87), Y8(z1), 25 * 0.5, h, fill=BG, stroke=INK, sw=0.5)              # câmara
        sh.rect(X8(50), Y8(z1), 20 * 0.5, h, fill=BG, stroke=INK, sw=0.5)
        sh.wood(X8(70), Y8(z1), 15 * 0.5, h, grain=False)
    sip(-260, -20)
    sip(320, 560)
    for zz in range(-250, 560, 80):
        if -20 < zz < 320:
            continue
        sh.wood(X8(-127), Y8(zz + 40), 40 * 0.5, 40 * 0.5, grain=False)
    # requadro de madeira 40 mm fechando o núcleo (peitoril e verga)
    sh.wood(X8(-50), Y8(0), 100 * 0.5, 20 * 0.5, grain=False)
    sh.wood(X8(-50), Y8(320), 100 * 0.5, 20 * 0.5, grain=False)
    # marco de alumínio RPT 60 x 60 e vidro duplo (fresta 300 de altura)
    sh.rect(X8(-45), Y8(60), 60 * 0.5, 60 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.rect(X8(-45), Y8(300), 60 * 0.5, 60 * 0.5, fill="url(#p-steel)", stroke=INK, sw=0.9)
    sh.rect(X8(-27), Y8(240), 24 * 0.5, 180 * 0.5, fill=GLASS, stroke="#8A9DA3", sw=0.6)
    # rufo de verga: chapa de alumínio dobrada, por trás da cimentícia, sobre o marco, com pingadeira
    sh.pl([(X8(-62), Y8(420)), (X8(-62), Y8(330)), (X8(-100), Y8(322)), (X8(-100), Y8(310))], 1.4, INK)
    # rufo de peitoril com pingadeira e inclinação
    sh.pl([(X8(-45), Y8(62)), (X8(-100), Y8(40)), (X8(-100), Y8(28))], 1.4, INK)
    sh.pl([(X8(-62), Y8(62)), (X8(-62), Y8(-60))], 1.4, INK)   # aba do rufo por trás da cimentícia
    # selante + tarucel
    for zz in (62, 298):
        sh.circle(X8(-48), Y8(zz), 2.2, fill=INK, stroke="none")
    # tela anti-inseto na câmara e fluxo de água
    sh.arrow(X8(-110), Y8(300), X8(-118), Y8(250), 0.9, GOLD, head=5)
    sh.arrow(X8(-110), Y8(35), X8(-118), Y8(-10), 0.9, GOLD, head=5)
    sh.add('</g>')
    sh.dim_v(X8(-160), Y8(60), Y8(300), "300", ext=None, left=True, size=10)
    sh.dim_h(X8(-50), X8(50), Y8(-140), "SIP 100", ext=None, above=False, size=10)
    sh.text(X8(-300), Y8(150), "EXTERIOR", size=9.5, color=GOLD, ls="0.2em")
    sh.text(X8(110), Y8(150), "INTERIOR", size=9.5, color=GOLD, ls="0.2em")
    C(16, X8(-15), Y8(330), X8(150), Y8(480))
    C(17, X8(-15), Y8(200), X8(150), Y8(260))
    C(18, X8(-90), Y8(318), X8(-220), Y8(420))
    C(19, X8(-80), Y8(48), X8(-220), Y8(-40))
    C(20, X8(-107), Y8(120), X8(-220), Y8(200))
    C(21, X8(0), Y8(10), X8(150), Y8(40))

    items = [
        (1, "Membrana externa + câmara 60 + manta + lã PET 50 + forro (ver DET-01)"),
        (2, "Requadro em madeira laminada 220 x 40 mm (anel da lente), fecha as camadas"),
        (3, "Marco de alumínio com ruptura térmica 60 x 70, bronze anodizado"),
        (4, "Vidro duplo 6 lam + 12 Ar + 6 temp, low-e (U 1,6 W/m²K)"),
        (5, "Basculante de projeção: dobradiça superior contínua + braços de fricção"),
        (6, "Grampo de alumínio da membrana ao requadro + gaxeta EPDM + pingadeira"),
        (7, "Peitoril inclinado 5% com friso pingadeira; canal de condensação no marco"),
        (8, "Forro tensionado fechando no requadro"),
        (9, "Fita LED 2700 K oculta no requadro"),
        (10, "Anel A0 Ø101,6 x 4,0 inclinado 8° com anel de alumínio 120 x 60 curvo"),
        (11, "Montantes de alumínio 60 x 120 com ruptura térmica; travessas a 0,8 e 2,2 m"),
        (12, "Porta pivotante de vidro 1000 x 2400, mola de piso, à direita da fachada"),
        (13, "Folha fixa 1350 x 2750 (vidro duplo)"),
        (14, "Folha de correr 1350 x 2750 sobre roldanas inox, fecho multiponto"),
        (15, "Trilho embutido nivelado com o deck e o piso (acessível), dreno à calha"),
        (16, "Marco de alumínio RPT 60 x 60 fixado ao requadro de madeira"),
        (17, "Vidro duplo 6 + 12 + 6 (fresta 300 mm de altura, fixa)"),
        (18, "Rufo de verga: alumínio 1,5 mm por trás da cimentícia, pingadeira 12 mm"),
        (19, "Rufo de peitoril inclinado, aba vertical 120 mm por trás da cimentícia"),
        (20, "Câmara ventilada 25 mm com tela anti-inseto; escoamento pela fachada"),
        (21, "Requadro de madeira 40 mm selando o núcleo PIR (selante + tarucel)"),
    ]
    sh.legend(60, 890, items, cols=3, colw=330, lh=13.5, size=9.2, title=None)
    sh.write("DET-05_esquadrias.svg")

