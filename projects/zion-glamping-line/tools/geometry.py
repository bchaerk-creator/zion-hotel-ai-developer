# -*- coding: utf-8 -*-
"""
Geometria paramétrica dos produtos ZION COCOON e ZION ZENITH.
Fonte única de verdade para desenhos 2D (SVG), isométrica e modelo 3D (Three.js).
Unidades: metros. Eixos: x = comprimento (0 = fachada frontal), y = largura (0 = eixo), z = altura (0 = piso acabado).
"""
import math, json
import numpy as np

# ----------------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------------
def sef(t, n):
    """Fator de superelipse: 1 em t=0, 0 em t=1."""
    t = min(max(t, 0.0), 1.0)
    return (1.0 - t ** n) ** (1.0 / n)

def box(x1, x2, y1, y2, z1, z2, kind, name=""):
    return dict(x1=x1, x2=x2, y1=y1, y2=y2, z1=z1, z2=z2, kind=kind, name=name)

def cyl(x, y, z1, z2, r, kind, name=""):
    return dict(x=x, y=y, z1=z1, z2=z2, r=r, kind=kind, name=name)

# ==================================================================================
# ZION COCOON
# ==================================================================================
class Cocoon:
    NAME = "ZION COCOON"
    L = 9.6            # comprimento do piso (x = 0 ... 9,6)
    X_FRONT = 0.45     # posição do anel frontal (piso)
    X_GLASS = 0.9      # plano da fachada de vidro (piso)
    XMAX = 3.4         # x da largura máxima
    AMAX = 3.0         # semi-eixo horizontal máximo (largura da concha 6,00 m em z = ZC)
    N_FRONT = 4.0      # expoente da superelipse (frente cheia)
    N_REAR = 3.0       # expoente da superelipse (cauda afilada)
    N_B = 2.0          # expoente da altura na cauda
    ZC = 0.75          # altura do centro da elipse de seção
    B_FRONT = 3.35     # semi-eixo vertical na frente (topo 4,10)
    B_MAX = 3.45       # semi-eixo vertical máximo (topo 4,20)
    B_MIN = 0.35       # semi-eixo vertical na ponta da cauda
    TILT = 0.6         # inclinação do lábio frontal (topo avança 0,60 m)
    TILT_X = 2.6       # extensão da zona cisalhada
    ARCH_X = [0.45, 1.65, 2.85, 4.05, 5.25, 6.45, 7.65, 8.75]   # posições dos arcos (8)
    PURLIN_V = [0.10, 0.22, 0.34, 0.5, 0.66, 0.78, 0.90]  # terças (fração da seção)
    SPINE = (1.9, 6.6, 0.105)   # espinha de luz: x1, x2, meio-ângulo (rad)
    X_PARTITION = 6.6  # parede do banho
    X_FLOOR_END = 9.4
    DECK = dict(x1=-3.7, x2=0.9, y1=-3.25, y2=3.25)  # deck frontal 4,6 x 6,5 = 29,9 m²

    # Janelas "olho" (lente): xc, theta_c (rad), meio-comp (m), meio-ângulo (rad)
    WINDOWS = [
        dict(name="Olho estar (dir.)",   xc=2.3, tc=0.22,           lx=0.80, lt=0.15),
        dict(name="Olho suíte (dir.)",   xc=4.9, tc=0.22,           lx=0.80, lt=0.15),
        dict(name="Olho banho (dir.)",   xc=7.9, tc=0.50,           lx=0.55, lt=0.125),
        dict(name="Olho estar (esq.)",   xc=3.4, tc=math.pi-0.22,   lx=0.80, lt=0.15),
        dict(name="Olho suíte (esq.)",   xc=5.7, tc=math.pi-0.22,   lx=0.70, lt=0.135),
        dict(name="Olho banheira (esq.)",xc=8.5, tc=math.pi-0.35,   lx=0.45, lt=0.115),
    ]

    # ---- perfis ----
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
        """meia-largura do piso (interseção da concha com z=0)."""
        a, b = self.a(x), self.b(x)
        if b <= self.ZC or a <= 0:
            return 0.0
        return a * math.sqrt(1 - (self.ZC / b) ** 2)

    def tilt(self, x):
        return self.TILT * max(0.0, 1 - (x - self.X_FRONT) / self.TILT_X)

    def shear(self, x, z):
        return x - self.tilt(x) * (z / 4.15)

    def theta_range(self, x):
        b = self.b(x)
        if b <= self.ZC:
            return -math.pi / 2, 3 * math.pi / 2
        t0 = math.asin(self.ZC / b)
        return -t0, math.pi + t0

    def section_point(self, x, theta, offset=0.0):
        """ponto 3D da seção em x, ângulo theta. offset = deslocamento normal (m)."""
        a, b = self.a(x) + offset, self.b(x) + offset
        y = a * math.cos(theta)
        z = self.ZC + b * math.sin(theta)
        return (self.shear(x, z), y, z)

    def section_curve(self, x, n=64, offset=0.0):
        t0, t1 = self.theta_range(x)
        return [self.section_point(x, t0 + (t1 - t0) * i / n, offset) for i in range(n + 1)]

    def section_local(self, x, n=64):
        """seção sem cisalhamento (y, z) para o corte transversal."""
        t0, t1 = self.theta_range(x)
        a, b = self.a(x), self.b(x)
        return [(a * math.cos(t0 + (t1 - t0) * i / n), self.ZC + b * math.sin(t0 + (t1 - t0) * i / n)) for i in range(n + 1)]

    def in_window(self, x, theta):
        for w in self.WINDOWS:
            dx = abs(x - w["xc"]) / w["lx"]
            dt = abs(theta - w["tc"]) / w["lt"]
            if dx ** 1.5 + dt ** 1.5 <= 1.0:
                return True
        x1, x2, ht = self.SPINE
        if x1 <= x <= x2 and abs(theta - math.pi / 2) <= ht:
            return True
        return False

    def window_outline(self, w, n=48):
        """contorno 3D da janela lente"""
        pts = []
        for i in range(n):
            ang = 2 * math.pi * i / n
            c, s = math.cos(ang), math.sin(ang)
            # superelipse n=1.5 : |u|^1.5+|v|^1.5=1
            r = (abs(c) ** 1.5 + abs(s) ** 1.5) ** (-1 / 1.5)
            x = w["xc"] + w["lx"] * r * c
            th = w["tc"] + w["lt"] * r * s
            pts.append(self.section_point(x, th, 0.01))
        return pts

    # ---- malha da concha ----
    def shell_mesh(self, nu=88, nv=44):
        xs = [self.X_FRONT + (self.L - self.X_FRONT) * (i / nu) for i in range(nu + 1)]
        verts, groups = [], []
        for x in xs:
            t0, t1 = self.theta_range(x)
            for j in range(nv + 1):
                th = t0 + (t1 - t0) * j / nv
                verts.append(self.section_point(x, th))
        faces_m, faces_g = [], []
        for i in range(nu):
            for j in range(nv):
                a0 = i * (nv + 1) + j
                a1 = a0 + 1
                b0 = a0 + (nv + 1)
                b1 = b0 + 1
                xm = (xs[i] + xs[i + 1]) / 2
                t0, t1 = self.theta_range(xm)
                thm = t0 + (t1 - t0) * (j + 0.5) / nv
                tgt = faces_g if self.in_window(xm, thm) else faces_m
                tgt.append((a0, b0, b1)); tgt.append((a0, b1, a1))
        return dict(vertices=verts, membrane=faces_m, glass=faces_g)

    def arches(self):
        return [dict(x=x, pts=self.section_curve(x, 48)) for x in self.ARCH_X]

    def purlins(self, n=60):
        out = []
        for v in self.PURLIN_V:
            pts = []
            for i in range(n + 1):
                x = self.X_FRONT + (9.2 - self.X_FRONT) * i / n
                t0, t1 = self.theta_range(x)
                pts.append(self.section_point(x, t0 + (t1 - t0) * v))
            out.append(pts)
        return out

    def floor_outline(self, n=80):
        """polígono do piso interno (x de X_GLASS a X_FLOOR_END)"""
        right, left = [], []
        for i in range(n + 1):
            x = self.X_GLASS + (self.X_FLOOR_END - self.X_GLASS) * i / n
            hw = self.floor_hw(x)
            right.append((x, -hw)); left.append((x, hw))
        return right + left[::-1]

    def shell_plan_outline(self, n=80):
        """contorno da concha em planta (largura máxima, z = ZC), com cisalhamento no topo ignorado"""
        right, left = [], []
        for i in range(n + 1):
            x = self.X_FRONT + (self.L - self.X_FRONT) * i / n
            a = self.a(x)
            right.append((x, -a)); left.append((x, a))
        return right + left[::-1]

    def front_ring(self, n=64):
        return self.section_curve(self.X_FRONT, n)

    def glass_ring(self, n=64):
        return self.section_curve(self.X_GLASS, n, offset=-0.06)

    def furniture(self):
        F = []
        # piso interno / hood
        F.append(box(6.6, 6.7, -2.8, 2.8, 0, 2.6, "wall", "Parede do banho"))
        F.append(box(6.6, 6.7, 1.0, 1.85, 0, 2.1, "opening", "Porta de correr"))
        F.append(box(4.5, 6.55, -0.97, 0.97, 0.0, 0.55, "bed", "Cama king 1,93 x 2,03"))
        F.append(box(4.5, 6.55, -0.97, 0.97, 0.55, 0.62, "pillow", ""))
        F.append(box(5.95, 6.55, 1.05, 1.55, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(5.95, 6.55, -1.55, -1.05, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(3.1, 4.5, 1.6, 2.2, 0, 1.5, "cabinet", "Armário baixo embutido"))
        F.append(box(1.2, 2.6, 1.6, 2.2, 0, 0.9, "cabinet", "Café / minibar"))
        F.append(box(1.15, 2.75, -2.25, -1.45, 0, 0.45, "sofa", "Chaise de contemplação"))
        F.append(box(3.2, 3.9, -2.25, -1.55, 0, 0.75, "chair", "Poltrona"))
        F.append(cyl(1.95, -0.95, 0, 0.45, 0.28, "table", "Mesa lateral"))
        # banho
        F.append(box(6.75, 7.3, -2.05, -0.55, 0, 0.85, "vanity", "Bancada 1,50 m"))
        F.append(box(7.4, 8.1, 0.95, 1.7, 0, 0.42, "wc", "Bacia sanitária"))
        F.append(box(7.65, 8.6, -1.75, -0.8, 0, 0.02, "shower", "Chuveiro 0,95 x 0,95"))
        F.append(box(7.65, 7.68, -1.75, -0.8, 0, 2.1, "glass", ""))
        F.append(box(7.55, 9.15, -0.38, 0.38, 0, 0.58, "tub", "Banheira 1,60 x 0,76"))
        F.append(box(6.7, 9.35, -2.3, 2.3, 2.4, 2.45, "ceiling", "Forro do banho / ático técnico"))
        # equipamentos
        F.append(box(7.0, 8.0, -0.6, 0.4, 2.5, 2.78, "hvac", "Evaporadora dutada 12k BTU"))
        F.append(box(9.95, 10.7, -0.45, 0.35, 0.0, 0.62, "condenser", "Condensadora"))
        return F

    def spec(self):
        return dict(
            name=self.NAME, L=self.L, W=2 * self.AMAX, H=self.top(self.XMAX),
            floor_area=self.floor_area(), deck_area=(self.DECK["x2"] - self.DECK["x1"]) * (self.DECK["y2"] - self.DECK["y1"]),
        )

    def floor_area(self):
        n = 400
        s = 0
        for i in range(n):
            x = self.X_GLASS + (self.X_FLOOR_END - self.X_GLASS) * (i + 0.5) / n
            s += 2 * self.floor_hw(x) * (self.X_FLOOR_END - self.X_GLASS) / n
        return s

    def membrane_area(self):
        m = self.shell_mesh(60, 30)
        V = np.array(m["vertices"])
        def area(faces):
            s = 0
            for f in faces:
                p, q, r = V[f[0]], V[f[1]], V[f[2]]
                s += 0.5 * np.linalg.norm(np.cross(q - p, r - p))
            return s
        return area(m["membrane"]), area(m["glass"])

    def arch_lengths(self):
        out = []
        for x in self.ARCH_X:
            pts = np.array(self.section_curve(x, 96))
            out.append(float(np.sum(np.linalg.norm(np.diff(pts, axis=0), axis=1))))
        return out

    def export(self):
        return dict(
            name=self.NAME,
            shell=self.shell_mesh(),
            arches=self.arches(),
            purlins=self.purlins(),
            front_ring=self.front_ring(),
            glass_ring=self.glass_ring(),
            floor=self.floor_outline(),
            deck=self.DECK,
            furniture=self.furniture(),
            windows=[dict(name=w["name"], pts=self.window_outline(w)) for w in self.WINDOWS],
            spine=self.SPINE,
            x_glass=self.X_GLASS, x_partition=self.X_PARTITION,
        )


# ==================================================================================
# ZION ZENITH
# ==================================================================================
class Zenith:
    NAME = "ZION ZENITH"
    L = 9.5; W = 5.4            # corpo (externo)
    H_WALL = 2.75               # topo do painel de parede
    Z_EAVE = 2.9                # anel de beiral (topo da viga)
    Z_EDGE = 2.65               # topo dos postes externos
    OVER_F, OVER_S, OVER_R = 2.4, 1.0, 1.0   # balanços da cobertura: frente, lados, fundos
    PEAKS = [
        dict(name="Cume principal (Zênite)", x=6.3, y=0.4, h=5.8, r=0.6, mast_top=5.05, oculus=True),
        dict(name="Cume secundário (Respiro)", x=1.6, y=1.6, h=4.6, r=0.35, mast_top=4.0, oculus=False),
    ]
    DECK = dict(x1=-3.0, x2=0.0, y1=-3.4, y2=3.4)          # terraço frontal 3,0 x 6,8
    WALK = dict(x1=0.0, x2=9.5, y1=2.7, y2=3.5)            # passarela lateral 0,8
    HOTTUB = dict(x=-1.55, y=-2.05, r=0.95)
    X_HEAD = 6.2                                            # parede da cabeceira

    def roof_bounds(self):
        return (-self.OVER_F, self.L + self.OVER_R, -self.W / 2 - self.OVER_S, self.W / 2 + self.OVER_S)

    def posts(self):
        x0, x1, y0, y1 = self.roof_bounds()
        return [(x0, y0), (x0, y1), (x1, y0), (x1, y1), (4.0, y0), (4.0, y1), (x1, 0.0)]

    def columns(self):
        return [(0, -2.7), (0, 2.7), (9.5, -2.7), (9.5, 2.7), (3.2, -2.7), (3.2, 2.7), (6.4, -2.7), (6.4, 2.7), (9.5, 0.0), (0.0, 0.0)]

    # --- borda recortada (catenária entre postes) ---
    def edge_height(self, x, y):
        x0, x1, y0, y1 = self.roof_bounds()
        posts = self.posts()
        # identifica a aresta
        if abs(x - x0) < 1e-6:   # frente: vão único entre cantos
            t = (y - y0) / (y1 - y0); S = 0.35
        elif abs(x - x1) < 1e-6:  # fundos: poste no meio
            t = (y - y0) / (y1 - y0); t = (t * 2) % 1.0; S = 0.28
        else:                     # laterais: poste em x=4.0
            if x < 4.0: t = (x - x0) / (4.0 - x0)
            else: t = (x - 4.0) / (x1 - 4.0)
            S = 0.30
        return self.Z_EDGE - S * 4 * t * (1 - t)

    def _ray_to_rect(self, px, py, dx, dy, x0, x1, y0, y1):
        """distância do ponto (px,py) até o retângulo ao longo de (dx,dy)."""
        best = 1e9
        if abs(dx) > 1e-9:
            for xb in (x0, x1):
                t = (xb - px) / dx
                if t > 0:
                    yy = py + t * dy
                    if y0 - 1e-9 <= yy <= y1 + 1e-9: best = min(best, t)
        if abs(dy) > 1e-9:
            for yb in (y0, y1):
                t = (yb - py) / dy
                if t > 0:
                    xx = px + t * dx
                    if x0 - 1e-9 <= xx <= x1 + 1e-9: best = min(best, t)
        return best

    def roof_z(self, x, y):
        """altura da membrana externa em (x,y)."""
        bx0, bx1, by0, by1 = 0.0, self.L, -self.W / 2, self.W / 2
        inside = bx0 <= x <= bx1 and by0 <= y <= by1
        if inside:
            base = self.Z_EAVE
            ws = []
            for p in self.PEAKS:
                dx, dy = x - p["x"], y - p["y"]
                d = math.hypot(dx, dy)
                if d <= p["r"]:
                    ws.append(1.0 * (p["h"] - base)); continue
                D = self._ray_to_rect(p["x"], p["y"], dx / d, dy / d, bx0, bx1, by0, by1)
                t = (d - p["r"]) / max(D - p["r"], 1e-6)
                w = max(0.0, 1 - t) ** 2.0
                ws.append(w * (p["h"] - base))
            pnorm = 2.6
            comb = sum(w ** pnorm for w in ws) ** (1 / pnorm)
            return base + comb
        # balanço
        dxo = max(0.0, bx0 - x, x - bx1)
        dyo = max(0.0, abs(y) - by1)
        ox = self.OVER_F if x < bx0 else self.OVER_R
        s = max(dxo / ox, dyo / self.OVER_S)
        s = min(s, 1.0)
        # ponto de borda correspondente
        x0, x1, y0, y1 = self.roof_bounds()
        if dxo / ox >= dyo / self.OVER_S:
            ex = x0 if x < bx0 else x1
            ey = min(max(y, y0), y1)
        else:
            ey = y0 if y < 0 else y1
            ex = min(max(x, x0), x1)
        e = self.edge_height(ex, ey)
        return self.Z_EAVE + (e - self.Z_EAVE) * (s ** 0.9)

    def liner_z(self, x, y):
        return self.roof_z(x, y) - 0.30

    def roof_mesh(self, nx=72, ny=44, liner=False):
        x0, x1, y0, y1 = self.roof_bounds()
        if liner:
            x0, x1, y0, y1 = 0.0, self.L, -self.W / 2, self.W / 2
        verts, faces = [], []
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            for j in range(ny + 1):
                y = y0 + (y1 - y0) * j / ny
                z = self.liner_z(x, y) if liner else self.roof_z(x, y)
                verts.append((x, y, z))
        for i in range(nx):
            for j in range(ny):
                a0 = i * (ny + 1) + j; a1 = a0 + 1; b0 = a0 + ny + 1; b1 = b0 + 1
                faces.append((a0, b0, b1)); faces.append((a0, b1, a1))
        return dict(vertices=verts, faces=faces)

    def ridge_profile(self, y, n=120):
        """perfil longitudinal da cobertura em y (para elevação lateral / corte)."""
        x0, x1, _, _ = self.roof_bounds()
        return [(x0 + (x1 - x0) * i / n, self.roof_z(x0 + (x1 - x0) * i / n, y)) for i in range(n + 1)]

    def cross_profile(self, x, n=80):
        _, _, y0, y1 = self.roof_bounds()
        return [(y0 + (y1 - y0) * i / n, self.roof_z(x, y0 + (y1 - y0) * i / n)) for i in range(n + 1)]

    def silhouette_side(self, n=120):
        """máximo de z ao longo de y para cada x (elevação lateral)."""
        x0, x1, y0, y1 = self.roof_bounds()
        out = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            out.append((x, max(self.roof_z(x, y0 + (y1 - y0) * j / 40) for j in range(41))))
        return out

    def silhouette_front(self, n=100):
        x0, x1, y0, y1 = self.roof_bounds()
        out = []
        for j in range(n + 1):
            y = y0 + (y1 - y0) * j / n
            out.append((y, max(self.roof_z(x0 + (x1 - x0) * i / 60, y) for i in range(61))))
        return out

    def walls(self):
        """painéis de parede e vidros: lista de retângulos verticais (x1,y1)-(x2,y2), z1,z2, kind"""
        W = []
        h = self.H_WALL
        # frente: vidro total (x=0)
        W.append(dict(p1=(0, -2.7), p2=(0, 2.7), z1=0, z2=h, kind="glass", name="Fachada panorâmica 5,4 x 2,75 (4 folhas, 2 de correr)"))
        # direita (y=-2.7): vidro até a cabeceira, madeira no banho
        W.append(dict(p1=(0, -2.7), p2=(6.4, -2.7), z1=0, z2=h, kind="glass", name="Vidro lateral suíte 6,4 x 2,75"))
        W.append(dict(p1=(6.4, -2.7), p2=(9.5, -2.7), z1=0, z2=h, kind="wood", name="Painel isolado + ripado"))
        W.append(dict(p1=(8.3, -2.7), p2=(9.3, -2.7), z1=1.9, z2=2.4, kind="window", name="Janela alta do chuveiro"))
        # esquerda (y=+2.7): madeira com janela horizontal do café
        W.append(dict(p1=(0, 2.7), p2=(9.5, 2.7), z1=0, z2=h, kind="wood", name="Painel isolado + ripado"))
        W.append(dict(p1=(0.5, 2.7), p2=(2.7, 2.7), z1=1.1, z2=2.2, kind="window", name="Janela horizontal do café"))
        W.append(dict(p1=(3.9, 2.7), p2=(5.9, 2.7), z1=1.9, z2=2.4, kind="window", name="Fresta alta do closet"))
        # fundos (x=9.5): madeira + fresta da banheira
        W.append(dict(p1=(9.5, -2.7), p2=(9.5, 2.7), z1=0, z2=h, kind="wood", name="Painel isolado + ripado"))
        W.append(dict(p1=(9.5, -0.8), p2=(9.5, 1.6), z1=1.5, z2=2.15, kind="window", name="Fresta da banheira"))
        return W

    def furniture(self):
        F = []
        F.append(box(6.2, 6.45, -2.6, 1.5, 0, 2.75, "wall", "Parede da cabeceira (com mastro)"))
        F.append(box(6.2, 6.45, 1.5, 2.6, 0, 2.2, "opening", "Passagem 1,10 m / porta de correr"))
        F.append(box(4.1, 6.15, -0.97, 0.97, 0, 0.55, "bed", "Cama king 1,93 x 2,03"))
        F.append(box(4.1, 6.15, -0.97, 0.97, 0.55, 0.62, "pillow", ""))
        F.append(box(5.65, 6.15, 1.05, 1.55, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(5.65, 6.15, -1.55, -1.05, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(3.55, 3.95, -0.7, 0.7, 0, 0.45, "bench", "Banco aos pés"))
        F.append(box(3.8, 5.8, 2.0, 2.6, 0, 2.4, "cabinet", "Closet 2,0 x 0,6"))
        F.append(box(2.55, 3.45, -1.05, 1.15, 0, 0.8, "sofa", "Sofá 2,2 m"))
        F.append(box(1.35, 1.95, -0.35, 0.45, 0, 0.35, "table", "Mesa de centro"))
        F.append(box(0.5, 2.4, -2.5, -1.7, 0, 0.45, "sofa", "Chaise de contemplação"))
        F.append(box(1.32, 1.88, 1.32, 1.88, 0, 2.75, "totem", "Totem do mastro 2"))
        F.append(box(0.6, 2.6, 1.88, 2.6, 0, 0.9, "cabinet", "Ilha do café / minibar"))
        # banho
        F.append(box(6.5, 7.05, -1.7, 0.3, 0, 0.85, "vanity", "Bancada dupla 2,0 m"))
        F.append(box(7.3, 8.1, -2.6, -1.8, 0, 0.42, "wc", "Bacia sanitária"))
        F.append(box(7.2, 7.25, -2.6, -1.3, 0, 1.5, "wall", "Divisória do WC"))
        F.append(box(8.3, 9.4, -2.6, -1.4, 0, 0.02, "shower", "Chuveiro 1,1 x 1,2"))
        F.append(box(8.3, 8.33, -2.6, -1.4, 0, 2.1, "glass", "Vidro do box"))
        F.append(box(8.6, 9.35, -0.5, 1.2, 0, 0.58, "tub", "Banheira 1,70 x 0,75"))
        F.append(box(6.45, 9.4, -2.6, 2.6, 2.5, 2.55, "ceiling", "Forro do banho / ático técnico"))
        F.append(box(7.2, 8.2, 0.3, 1.3, 2.6, 2.88, "hvac", "Evaporadora dutada 18k BTU"))
        F.append(box(9.85, 10.65, -2.2, -1.4, 0, 0.62, "condenser", "Condensadora"))
        return F

    def masts(self):
        M = []
        for p in self.PEAKS:
            M.append(dict(x=p["x"], y=p["y"], z1=0.0, z2=p["mast_top"], r=0.07, name="Mastro Ø139,7 x 4,5"))
        return M

    def crowns(self):
        """braços da coroa: do topo do mastro ao anel do cume (3 braços)"""
        C = []
        for p in self.PEAKS:
            arms = []
            for k in range(3):
                ang = math.pi / 2 + 2 * math.pi * k / 3
                arms.append([(p["x"], p["y"], p["mast_top"]), (p["x"] + p["r"] * math.cos(ang), p["y"] + p["r"] * math.sin(ang), p["h"] - 0.05)])
            C.append(dict(peak=p["name"], arms=arms, ring=[(p["x"] + p["r"] * math.cos(2 * math.pi * i / 36), p["y"] + p["r"] * math.sin(2 * math.pi * i / 36), p["h"]) for i in range(37)]))
        return C

    def floor_area(self):
        return (self.L - 0.2) * (self.W - 0.2)

    def roof_area(self):
        m = self.roof_mesh(48, 30)
        V = np.array(m["vertices"]); s = 0
        for f in m["faces"]:
            p, q, r = V[f[0]], V[f[1]], V[f[2]]
            s += 0.5 * np.linalg.norm(np.cross(q - p, r - p))
        x0, x1, y0, y1 = self.roof_bounds()
        return s, (x1 - x0) * (y1 - y0)

    def export(self):
        return dict(
            name=self.NAME, L=self.L, W=self.W, h_wall=self.H_WALL, z_eave=self.Z_EAVE,
            roof=self.roof_mesh(), liner=self.roof_mesh(56, 34, liner=True),
            roof_bounds=self.roof_bounds(), posts=self.posts(), columns=self.columns(),
            walls=self.walls(), furniture=self.furniture(), masts=self.masts(), crowns=self.crowns(),
            peaks=self.PEAKS, deck=self.DECK, walk=self.WALK, hottub=self.HOTTUB,
        )


if __name__ == "__main__":
    import os, sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    c, z = Cocoon(), Zenith()
    print("COCOON piso interno m2:", round(c.floor_area(), 2), "membrana/vidro m2:", [round(v, 1) for v in c.membrane_area()])
    print("COCOON arcos (m):", [round(v, 2) for v in c.arch_lengths()], "altura max:", round(c.top(c.XMAX), 2))
    for x in [0.5, 1.0, 2, 3.2, 4, 5, 6.2, 7, 8, 8.5, 8.8]:
        print(f"  x={x}: a={c.a(x):.2f} b={c.b(x):.2f} top={c.top(x):.2f} floor_hw={c.floor_hw(x):.2f}")
    print("ZENITH piso interno m2:", round(z.floor_area(), 2), "cobertura (sup, proj):", [round(v, 1) for v in z.roof_area()])
    for p in z.PEAKS:
        print("  pico", p["name"], round(z.roof_z(p["x"], p["y"]), 2))
    print("  z(0,0)=", round(z.roof_z(0, 0), 2), " z(4,0)=", round(z.roof_z(4, 0), 2), " z(-2.4,0)=", round(z.roof_z(-2.4, 0), 2), " z(4,-3.7)=", round(z.roof_z(4, -3.7), 2))
    json.dump(c.export(), open(os.path.join(out, "cocoon_geometry.json"), "w"))
    json.dump(z.export(), open(os.path.join(out, "zenith_geometry.json"), "w"))
    print("json ok")
