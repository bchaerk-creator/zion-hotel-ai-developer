# -*- coding: utf-8 -*-
"""Mini-biblioteca SVG para os desenhos técnicos Zion (plantas, elevações, cortes, isométricas)."""
import math

CREAM = "#FEF5F0"; GREEN = "#1B2117"; SAND = "#DED6BF"; EARTH = "#8B714E"; BLACK = "#040605"
WOOD = "#D9C4A3"; WOOD2 = "#B99A73"; TILE = "#D8D6CF"; GLASS = "#BFD0D6"; MEMB = "#EDE6D6"; STEEL = "#3A3B3A"
FONT = "'DM Sans','Aventa',Helvetica,Arial,sans-serif"

def fmt(v):
    """formata metros com vírgula: 9,00"""
    return f"{v:.2f}".replace(".", ",")

class Sheet:
    def __init__(self, w=1600, h=1000, scale=80.0, ox=120, oy=700, flip_y=True, bg=CREAM, flip_x=False):
        self.w, self.h, self.s, self.ox, self.oy, self.flip = w, h, scale, ox, oy, flip_y
        self.fx = -1 if flip_x else 1
        self.parts = []
        self.defs = []
        self.bg = bg
        self._pattern_ids = set()

    # --- coordenadas ---
    def X(self, x): return self.ox + self.fx * x * self.s
    def Y(self, y): return self.oy - y * self.s if self.flip else self.oy + y * self.s
    def P(self, x, y): return f"{self.X(x):.2f},{self.Y(y):.2f}"

    # --- primitivas ---
    def add(self, s): self.parts.append(s)
    def line(self, x1, y1, x2, y2, stroke=GREEN, sw=1.0, dash=None, opacity=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{self.X(x1):.2f}" y1="{self.Y(y1):.2f}" x2="{self.X(x2):.2f}" y2="{self.Y(y2):.2f}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{opacity}" stroke-linecap="round"/>')
    def poly(self, pts, fill="none", stroke=GREEN, sw=1.0, close=True, dash=None, opacity=1.0, extra=""):
        d = " ".join(self.P(x, y) for x, y in pts)
        tag = "polygon" if close else "polyline"
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<{tag} points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{ds} opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')
    def rect(self, x1, y1, x2, y2, **kw):
        self.poly([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], **kw)
    def circle(self, x, y, r, fill="none", stroke=GREEN, sw=1.0, dash=None, opacity=1.0):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{self.X(x):.2f}" cy="{self.Y(y):.2f}" r="{r * self.s:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{ds} opacity="{opacity}"/>')
    def circle_px(self, x, y, rpx, fill="none", stroke=GREEN, sw=1.0):
        self.add(f'<circle cx="{self.X(x):.2f}" cy="{self.Y(y):.2f}" r="{rpx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self, x, y, s, size=13, fill=GREEN, anchor="middle", weight=400, rotate=0, spacing=0, italic=False, px=False, dy=0):
        X = x if px else self.X(x); Y = y if px else self.Y(y)
        tr = f' transform="rotate({rotate} {X:.2f} {Y:.2f})"' if rotate else ""
        st = f"font-family:{FONT};font-size:{size}px;font-weight:{weight};letter-spacing:{spacing}em;{'font-style:italic;' if italic else ''}"
        self.add(f'<text x="{X:.2f}" y="{Y + dy:.2f}" fill="{fill}" text-anchor="{anchor}" style="{st}"{tr}>{s}</text>')
    def text_px(self, X, Y, s, **kw):
        self.text(X, Y, s, px=True, **kw)

    # --- cotas ---
    def dim(self, x1, y1, x2, y2, offset=0.5, label=None, color=EARTH, size=13, side="auto", ext=True):
        """cota entre dois pontos (horizontal ou vertical), com linha de cota deslocada 'offset' (m)."""
        if label is None:
            label = fmt(math.hypot(x2 - x1, y2 - y1))
        if abs(y2 - y1) < 1e-9:  # horizontal
            yy = y1 + offset
            if ext:
                self.line(x1, y1, x1, yy + (0.08 if offset > 0 else -0.08), color, 0.7)
                self.line(x2, y2, x2, yy + (0.08 if offset > 0 else -0.08), color, 0.7)
            self.line(x1, yy, x2, yy, color, 0.8)
            for x in (x1, x2):
                self._tick(x, yy, color)
            self.text((x1 + x2) / 2, yy, label, size, color, dy=-4 if self.flip else -4)
        elif abs(x2 - x1) < 1e-9:  # vertical
            xx = x1 + offset
            if ext:
                self.line(x1, y1, xx + (0.08 if offset > 0 else -0.08), y1, color, 0.7)
                self.line(x2, y2, xx + (0.08 if offset > 0 else -0.08), y2, color, 0.7)
            self.line(xx, y1, xx, y2, color, 0.8)
            for y in (y1, y2):
                self._tick(xx, y, color, vertical=True)
            self.text(xx, (y1 + y2) / 2, label, size, color, rotate=-90 if self.flip else 90, dy=-4)
        else:
            self.line(x1, y1, x2, y2, color, 0.8)
            self.text((x1 + x2) / 2, (y1 + y2) / 2, label, size, color, dy=-4)
    def _tick(self, x, y, color, vertical=False):
        X, Y = self.X(x), self.Y(y); t = 4
        self.add(f'<line x1="{X - t:.1f}" y1="{Y + t:.1f}" x2="{X + t:.1f}" y2="{Y - t:.1f}" stroke="{color}" stroke-width="1.1"/>')
    def dim_chain(self, xs, y, offset, color=EARTH, size=12, vertical=False):
        for a, b in zip(xs[:-1], xs[1:]):
            if vertical: self.dim(y, a, y, b, offset, color=color, size=size)
            else: self.dim(a, y, b, y, offset, color=color, size=size)
    def leader(self, x, y, tx, ty, label, size=12, color=GREEN, anchor="start", dot=True):
        self.line(x, y, tx, ty, color, 0.7)
        if dot: self.circle_px(x, y, 2.2, fill=color, stroke=color)
        self.text(tx, ty, label, size, color, anchor=anchor, dy=-3)
    def callout(self, x, y, n, r=9, color=GREEN):
        self.circle_px(x, y, r, fill=CREAM, stroke=color, sw=1.0)
        self.text(x, y, str(n), 11, color, dy=4, weight=600)

    # --- padrões ---
    def pattern(self, pid):
        if pid in self._pattern_ids: return f"url(#{pid})"
        self._pattern_ids.add(pid)
        if pid == "hatch":
            self.defs.append(f'<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{GREEN}" stroke-width="0.8"/></pattern>')
        elif pid == "hatch2":
            self.defs.append(f'<pattern id="hatch2" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" stroke="{GREEN}" stroke-width="1.2"/></pattern>')
        elif pid == "wood":
            self.defs.append(f'<pattern id="wood" width="60" height="9" patternUnits="userSpaceOnUse"><rect width="60" height="9" fill="{WOOD}"/><line x1="0" y1="8.5" x2="60" y2="8.5" stroke="{WOOD2}" stroke-width="0.6" opacity="0.7"/></pattern>')
        elif pid == "deck":
            self.defs.append(f'<pattern id="deck" width="9" height="60" patternUnits="userSpaceOnUse"><rect width="9" height="60" fill="{WOOD2}"/><line x1="8.5" y1="0" x2="8.5" y2="60" stroke="{EARTH}" stroke-width="0.9" opacity="0.8"/></pattern>')
        elif pid == "tile":
            self.defs.append(f'<pattern id="tile" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="24" height="24" fill="{TILE}"/><path d="M0 0H24V24" fill="none" stroke="#B9B7AE" stroke-width="0.6"/></pattern>')
        elif pid == "insul":
            self.defs.append(f'<pattern id="insul" width="12" height="8" patternUnits="userSpaceOnUse"><path d="M0 4 Q3 0 6 4 T12 4" fill="none" stroke="{EARTH}" stroke-width="0.8"/></pattern>')
        elif pid == "soil":
            self.defs.append(f'<pattern id="soil" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.8" fill="{EARTH}"/><circle cx="7" cy="6" r="0.8" fill="{EARTH}"/></pattern>')
        elif pid == "grass":
            self.defs.append(f'<pattern id="grass" width="14" height="10" patternUnits="userSpaceOnUse"><path d="M2 10 L3 5 M5 10 L7 4 M9 10 L10 6 M12 10 L13 7" stroke="#7F8B6A" stroke-width="0.8" fill="none"/></pattern>')
        return f"url(#{pid})"

    # --- elementos de folha ---
    def title_block(self, product, title, scale_txt, sheet, subtitle="", date="SET 2026"):
        W, H = 560, 96
        X0, Y0 = self.w - W - 30, self.h - H - 24
        self.add(f'<rect x="{X0}" y="{Y0}" width="{W}" height="{H}" fill="{CREAM}" stroke="{GREEN}" stroke-width="1.2"/>')
        self.add(f'<line x1="{X0 + 200}" y1="{Y0}" x2="{X0 + 200}" y2="{Y0 + H}" stroke="{GREEN}" stroke-width="0.8"/>')
        self.add(f'<line x1="{X0}" y1="{Y0 + 46}" x2="{X0 + W}" y2="{Y0 + 46}" stroke="{GREEN}" stroke-width="0.8"/>')
        self.text_px(X0 + 100, Y0 + 24, "ZION", size=20, weight=800, spacing=0.35)
        self.text_px(X0 + 100, Y0 + 38, "GLAMPING COLLECTION", size=8.5, weight=400, spacing=0.3, fill=EARTH)
        self.text_px(X0 + 100, Y0 + 68, product, size=12, weight=700, spacing=0.2)
        self.text_px(X0 + 100, Y0 + 84, "ZION HOTEL GROUP INTERNATIONAL", size=7.5, spacing=0.2, fill=EARTH)
        self.text_px(X0 + 214, Y0 + 22, title.upper(), size=14, weight=700, spacing=0.12, anchor="start")
        self.text_px(X0 + 214, Y0 + 38, subtitle, size=10, fill=EARTH, anchor="start")
        self.text_px(X0 + 214, Y0 + 66, f"ESCALA {scale_txt}", size=10, spacing=0.15, anchor="start")
        self.text_px(X0 + 214, Y0 + 84, "PROJETO CONCEITUAL · ESTUDO PRELIMINAR", size=8, fill=EARTH, spacing=0.1, anchor="start")
        self.text_px(X0 + W - 14, Y0 + 66, f"FOLHA {sheet}", size=10, spacing=0.15, anchor="end", weight=600)
        self.text_px(X0 + W - 14, Y0 + 84, date, size=8, fill=EARTH, spacing=0.15, anchor="end")

    def header(self, title, sub=""):
        self.text_px(40, 46, title.upper(), size=22, weight=700, spacing=0.28, anchor="start")
        if sub: self.text_px(40, 68, sub, size=12, fill=EARTH, anchor="start", spacing=0.08)
        self.add(f'<line x1="40" y1="82" x2="{self.w - 40}" y2="82" stroke="{GREEN}" stroke-width="0.6" opacity="0.5"/>')

    def north(self, X, Y, r=22, angle=0):
        self.add(f'<g transform="translate({X},{Y}) rotate({angle})"><circle r="{r}" fill="none" stroke="{GREEN}" stroke-width="0.8"/><polygon points="0,{-r + 3} {-6},{r - 9} 0,{r - 15} 6,{r - 9}" fill="{GREEN}"/><text y="{-r - 6}" text-anchor="middle" style="font-family:{FONT};font-size:11px;font-weight:600" fill="{GREEN}">N</text></g>')

    def scalebar(self, x, y, meters=5, step=1):
        """barra de escala sempre desenhada da esquerda para a direita (independente de flip_x)."""
        X0 = self.X(x); Y0 = self.Y(y); h = 0.12 * self.s
        for i in range(0, meters, step):
            fill = GREEN if i % 2 == 0 else CREAM
            self.add(f'<rect x="{X0 + i * self.s:.1f}" y="{Y0 - h:.1f}" width="{step * self.s:.1f}" height="{h:.1f}" fill="{fill}" stroke="{GREEN}" stroke-width="0.7"/>')
        for i in range(0, meters + 1, step):
            self.text_px(X0 + i * self.s, Y0 + 14, f"{i}", size=10)
        self.text_px(X0 + meters * self.s + 14, Y0 - 2, "m", size=10, anchor="start")

    def legend(self, X, Y, items, size=11, colw=260):
        for i, (n, label) in enumerate(items):
            self.callout_px(X, Y + i * 20, n)
            self.text_px(X + 16, Y + i * 20 + 4, label, size=size, anchor="start")
    def callout_px(self, X, Y, n, r=8):
        self.add(f'<circle cx="{X}" cy="{Y}" r="{r}" fill="{CREAM}" stroke="{GREEN}" stroke-width="1"/>')
        self.text_px(X, Y + 3.6, str(n), size=10, weight=600)

    def render(self):
        defs = "<defs>" + "".join(self.defs) + "</defs>"
        body = "\n".join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" font-family="{FONT}">'
                f'{defs}<rect width="{self.w}" height="{self.h}" fill="{self.bg}"/>{body}</svg>')
    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render())


# --- projeção isométrica / painter ---
def iso_project(p, scale, ox, oy, mirror=(-1, -1)):
    x, y, z = p
    x, y = x * mirror[0], y * mirror[1]
    u = (x - y) / math.sqrt(2)
    v = (-x - y + 2 * z) / math.sqrt(6)
    depth = (x + y + z) / math.sqrt(3)
    return (ox + u * scale, oy - v * scale, depth)

def shade(hexcol, k):
    """escurece/clareia a cor hex por fator k (0..1.2)"""
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    r, g, b = [max(0, min(255, int(c * k))) for c in (r, g, b)]
    return f"#{r:02x}{g:02x}{b:02x}"
