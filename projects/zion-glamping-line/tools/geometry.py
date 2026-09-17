# -*- coding: utf-8 -*-
"""
Geometria paramétrica dos produtos ZION CASULO e ZION SAFARI.
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
# ZION CASULO
# ==================================================================================
class Cocoon:
    NAME = "ZION CASULO"
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
    # REV 01: cada Olho centrado num vão entre arcos (1,20 m), para que o recorte da membrana não cruze o perfil keder
    # do arco: lentes de 0,95 x 0,80 m (estar e suíte) e 0,80 x 0,55 m (banho e banheira).
    WINDOWS = [
        dict(name="Olho estar (dir.)",   xc=2.25, tc=0.22,          lx=0.47, lt=0.12),
        dict(name="Olho suíte (dir.)",   xc=4.65, tc=0.22,          lx=0.47, lt=0.12),
        dict(name="Olho banho (dir.)",   xc=8.20, tc=0.50,          lx=0.40, lt=0.11),
        dict(name="Olho estar (esq.)",   xc=3.45, tc=math.pi-0.22,  lx=0.47, lt=0.12),
        dict(name="Olho suíte (esq.)",   xc=5.85, tc=math.pi-0.22,  lx=0.47, lt=0.12),
        dict(name="Olho banheira (esq.)",xc=8.20, tc=math.pi-0.35,  lx=0.40, lt=0.11),
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

    # ---- Bico: membrana em balanço sobre o deck (ponta erguida) ----
    BICO = dict(E=2.40, TW=1.15, LIFT=0.30, P=0.85, RIDGE_OFF=-0.085)
    # E = balanço da ponta além do anel frontal (m) · TW = meio-ângulo (rad) do anel coberto pelo bico
    # LIFT = quanto a ponta se ergue acima do topo do anel (m) · P = expoente da borda (< 1 = ponta mais aguda)

    def bico_ext(self, theta):
        """avanço da membrana (m) além do anel frontal na direção -x, no ângulo theta do anel."""
        d = abs(theta - math.pi / 2) / self.BICO["TW"]
        return 0.0 if d >= 1.0 else self.BICO["E"] * (1.0 - d) ** self.BICO["P"]

    def bico_point(self, theta, s, offset=0.0):
        """ponto 3D do bico: theta no anel frontal, s de 0 (anel) a 1 (borda livre); offset normal aproximado (m)."""
        x0, y0, z0 = self.section_point(self.X_FRONT, theta, offset)
        e = self.bico_ext(theta); u = s * e / self.BICO["E"]
        return (x0 - s * e, y0 * (1.0 + 0.02 * u), z0 + self.BICO["LIFT"] * u ** 1.5)

    def bico_thetas(self, n=32):
        tw = self.BICO["TW"]
        return [math.pi / 2 - tw + 2 * tw * i / n for i in range(n + 1)]

    def bico_edge(self, n=32, offset=0.0):
        """borda livre do bico (curva 3D) da lateral direita à esquerda, passando pela ponta."""
        return [self.bico_point(t, 1.0, offset) for t in self.bico_thetas(n)]

    def bico_tip(self):
        return self.bico_point(math.pi / 2, 1.0)

    def bico_ridge(self, n=12, offset=None):
        """cumeeira em balanço: de A1 ao anel frontal e daí à ponta (eixo do tubo, sob a membrana)."""
        off = self.BICO["RIDGE_OFF"] if offset is None else offset
        pts = [self.section_point(self.ARCH_X[1], math.pi / 2, off), self.section_point(self.X_FRONT, math.pi / 2, off)]
        pts += [self.bico_point(math.pi / 2, i / n, off) for i in range(1, n + 1)]
        return pts

    def bico_ribs(self, fracs=(0.5,), n=24):
        """costelas intermediárias do bico (tubos curvos entre as bordas), em frações do balanço."""
        off = self.BICO["RIDGE_OFF"]
        return [[self.bico_point(t, f, off) for t in self.bico_thetas(n)] for f in fracs]

    def bico_ties(self):
        """tirantes sob o bico: do ponto a 60 % da cumeeira até o anel frontal, a ±0,80 rad do topo."""
        off = self.BICO["RIDGE_OFF"]
        top = self.bico_point(math.pi / 2, 0.6, off)
        return [[top, self.section_point(self.X_FRONT, math.pi / 2 + sgn * 0.8, off)] for sgn in (-1, 1)]

    def bico_mesh(self, nu=32, nv=10):
        verts, faces = [], []
        ths = self.bico_thetas(nu)
        for t in ths:
            for j in range(nv + 1):
                verts.append(self.bico_point(t, j / nv))
        for i in range(nu):
            for j in range(nv):
                a0 = i * (nv + 1) + j; a1 = a0 + 1; b0 = a0 + (nv + 1); b1 = b0 + 1
                faces.append((a0, b0, b1)); faces.append((a0, b1, a1))
        return dict(vertices=verts, faces=faces)

    def bico_area(self):
        m = self.bico_mesh(48, 12); V = np.array(m["vertices"]); s = 0.0
        for f in m["faces"]:
            p, q, r = V[f[0]], V[f[1]], V[f[2]]
            s += 0.5 * np.linalg.norm(np.cross(q - p, r - p))
        return float(s)

    def bico_tube_lengths(self):
        """comprimentos (m): cumeeira (A1 → ponta), cada tubo de borda (ponta → anel), costela, cada tirante."""
        def ln(pts):
            P = np.array(pts); return float(np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1)))
        edge = self.bico_edge(48, self.BICO["RIDGE_OFF"]); half = edge[: len(edge) // 2 + 1]
        return dict(ridge=ln(self.bico_ridge(24)), edge=ln(half), rib=ln(self.bico_ribs()[0]), tie=ln(self.bico_ties()[0]))

    def bico_export(self):
        return dict(mesh=self.bico_mesh(), edge=self.bico_edge(48), ridge=self.bico_ridge(16), ribs=self.bico_ribs(), ties=self.bico_ties(),
                    tip=self.bico_tip(), edges=[self.bico_edge(48, self.BICO["RIDGE_OFF"])], E=self.BICO["E"], area=self.bico_area())

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
        F.append(box(3.4, 4.5, 2.2, 2.85, 0, 1.5, "cabinet", "Armário baixo embutido (acoplado à concha)"))
        F.append(box(1.2, 3.2, 2.15, 2.8, 0, 0.9, "cabinet", "Mini cozinha acoplada à concha: geladeira, forno, cooktop 2 bocas, cuba, air fryer"))
        F.append(box(1.8, 2.4, 2.35, 2.8, 0.9, 0.92, "cooktop", "Cooktop de indução 2 bocas"))
        F.append(box(2.85, 3.15, 2.3, 2.7, 0.9, 1.25, "appliance", "Air fryer"))
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
            bico=self.bico_export(),
        )


# ==================================================================================
# ZION SAFARI
# ==================================================================================
class Zenith:
    NAME = "ZION SAFARI"
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
    print("CASULO piso interno m2:", round(c.floor_area(), 2), "membrana/vidro m2:", [round(v, 1) for v in c.membrane_area()])
    print("CASULO arcos (m):", [round(v, 2) for v in c.arch_lengths()], "altura max:", round(c.top(c.XMAX), 2))
    for x in [0.5, 1.0, 2, 3.2, 4, 5, 6.2, 7, 8, 8.5, 8.8]:
        print(f"  x={x}: a={c.a(x):.2f} b={c.b(x):.2f} top={c.top(x):.2f} floor_hw={c.floor_hw(x):.2f}")
    print("SAFARI piso interno m2:", round(z.floor_area(), 2), "cobertura (sup, proj):", [round(v, 1) for v in z.roof_area()])
    for p in z.PEAKS:
        print("  pico", p["name"], round(z.roof_z(p["x"], p["y"]), 2))
    print("  z(0,0)=", round(z.roof_z(0, 0), 2), " z(4,0)=", round(z.roof_z(4, 0), 2), " z(-2.4,0)=", round(z.roof_z(-2.4, 0), 2), " z(4,-3.7)=", round(z.roof_z(4, -3.7), 2))
    json.dump(c.export(), open(os.path.join(out, "cocoon_geometry.json"), "w"))
    json.dump(z.export(), open(os.path.join(out, "zenith_geometry.json"), "w"))
    print("json ok")


# ==================================================================================
# ZION LODGE (terceiro produto da linha: pavilhão octogonal com lanterna, unidade de entrada)
# ==================================================================================
class Lodge:
    NAME = "ZION LODGE"
    F = 6.8                       # distância entre faces do octógono (m)
    M = 0.0                       # inserção retangular no meio (octógono alongado); 0 = octógono regular
    N = 8
    CODE = "lodge"
    LABEL = "ZION LODGE 38"
    Z_EAVE = 2.7                  # anel de beiral (topo)
    Z_LANTERN = 4.6               # base da lanterna (anel de compressão)
    Z_TOP = 5.2                   # tampa da lanterna
    R_LANTERN = 0.75              # raio do anel da lanterna
    OVER = 0.9                    # beiral da membrana além dos pilares
    DECK_D = 2.6                  # profundidade do deck frontal (3 faces)
    DECK_FACES = [2, 3, 4, 5]     # vértices que delimitam as faces com deck
    SAIL = dict(z_post=2.4, reach=2.6)   # vela frontal sobre o deck

    def side(self):
        return self.F * math.tan(math.pi / self.N)

    def r_corner(self):
        return (self.F / 2) / math.cos(math.pi / self.N)

    def vertices(self, r=None, rot=math.pi / 8):
        """vértices do octógono (frente = face entre os vértices 3 e 4, voltada para -x); alongado por M no eixo x."""
        r = r or self.r_corner()
        out = []
        for k in range(self.N):
            x, y = r * math.cos(rot + 2 * math.pi * k / self.N), r * math.sin(rot + 2 * math.pi * k / self.N)
            out.append((x + (self.M / 2 if x > 0 else -self.M / 2), y))
        return out

    def lantern_centers(self):
        return [(0.0, 0.0)] if self.M < 0.5 else [(-self.M / 2, 0.0), (self.M / 2, 0.0)]

    def floor_area(self):
        return 2 * (1 + math.sqrt(2)) * self.side() ** 2 + self.M * self.F

    def deck_pts(self):
        """deck em três faces frontais (faces 3, 4, 5 do octógono, lado -x)."""
        V = self.vertices()
        ro = self.r_corner() + self.DECK_D / math.cos(math.pi / self.N)
        Vo = self.vertices(ro)
        idx = self.DECK_FACES
        inner = [V[i] for i in idx]; outer = [Vo[i] for i in idx]
        return inner + outer[::-1]

    def deck_area(self):
        pts = self.deck_pts(); a = 0
        for i in range(len(pts)):
            x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]; a += x1 * y2 - x2 * y1
        return abs(a) / 2

    def roof_z(self, d):
        """altura da membrana a uma distância radial d do centro (perfil cônico com curva de tensão)."""
        r0, r1 = self.R_LANTERN, self.r_corner() + self.OVER
        if d <= r0: return self.Z_LANTERN
        t = (d - r0) / (r1 - r0)
        z_edge = self.Z_EAVE - 0.35
        return self.Z_LANTERN - (self.Z_LANTERN - z_edge) * (t ** 1.25)

    # ---- fechamentos, layout, estrutura ----
    GLASS_FACES = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]     # cinco faces de vidro (frente = face 3-4, voltada para -x)
    WALL_FACES = [(6, 7), (7, 0), (0, 1)]                      # três faces opacas (banho e cabeceira)
    X_PART = 1.55                                              # parede-corda do banho (x)
    DOOR = dict(face=(3, 4), y1=-1.0, y2=1.0, h=2.4)           # porta de correr frontal 2,00 x 2,40
    SAIL_POSTS = None

    def walls(self):
        V = self.vertices(); W = []
        for (i, j) in self.GLASS_FACES:
            W.append(dict(p1=V[i], p2=V[j], z1=0, z2=self.Z_EAVE - 0.15, kind="glass", name="Vidro insulado fixo / porta de correr" if (i, j) == (3, 4) else "Vidro insulado fixo"))
        for (i, j) in self.WALL_FACES:
            W.append(dict(p1=V[i], p2=V[j], z1=0, z2=self.Z_EAVE - 0.15, kind="wood", name="Painel SIP 100 mm + ripado"))
        W.append(dict(p1=V[7], p2=V[0], z1=1.6, z2=2.2, kind="window", name="Fresta alta da banheira 1,60 x 0,60"))
        yc = math.sqrt(self.r_corner() ** 2 - self.X_PART ** 2)
        W.append(dict(p1=(self.X_PART, -yc), p2=(self.X_PART, yc), z1=0, z2=2.4, kind="partition", name="Parede-corda do banho (LSF + painel)"))
        return W

    def furniture(self):
        F = []
        F.append(box(self.X_PART, self.X_PART + 0.1, -2.6, 2.6, 0, 2.4, "wall", "Parede do banho"))
        F.append(box(self.X_PART, self.X_PART + 0.1, -0.5, 0.4, 0, 2.1, "opening", "Porta de correr do banho"))
        F.append(box(-0.55, 1.45, -0.97, 0.97, 0, 0.55, "bed", "Cama king 1,93 x 2,03"))
        F.append(box(-0.55, 1.45, -0.97, 0.97, 0.55, 0.62, "pillow", ""))
        F.append(box(-0.55, 0.05, 1.1, 1.7, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(-0.55, 0.05, -1.7, -1.1, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(0.2, 1.9, 2.2, 2.95, 0, 0.9, "cabinet", "Café / minibar"))
        F.append(box(0.2, 1.9, -2.95, -2.2, 0, 2.2, "cabinet", "Closet"))
        F.append(box(-2.7, -1.5, -1.2, 1.2, 0, 0.8, "sofa", "Sofá 2,40"))
        F.append(cyl(-1.15, 0.0, 0, 0.45, 0.3, "table", "Mesa lateral"))
        F.append(box(-2.9, -1.9, 1.7, 2.5, 0, 0.75, "chair", "Poltrona"))
        F.append(box(1.75, 2.45, 1.0, 2.4, 0, 0.85, "vanity", "Bancada 1,40"))
        F.append(box(2.7, 3.4, 1.6, 2.3, 0, 0.42, "wc", "Bacia sanitária"))
        F.append(box(2.4, 3.35, -1.6, -0.7, 0, 0.02, "shower", "Chuveiro 0,95 x 0,90"))
        F.append(box(2.4, 2.43, -1.6, -0.7, 0, 2.1, "glass", "Vidro do box"))
        F.append(box(1.8, 2.7, -2.5, -1.75, 0, 0.58, "tub", "Banheira 0,90 x 0,75 (sentar)"))
        F.append(box(self.X_PART, 3.4, -2.6, 2.6, 2.4, 2.45, "ceiling", "Forro do banho / ático técnico"))
        F.append(box(2.0, 3.0, -0.5, 0.5, 2.5, 2.7, "hvac", "Evaporadora dutada 9k BTU"))
        F.append(box(4.3, 5.0, -2.2, -1.5, 0, 0.62, "condenser", "Condensadora"))
        return F

    def columns(self):
        return self.vertices()

    def sail_posts(self):
        px = -self.r_corner() - self.SAIL["reach"]
        return [(px, -1.8), (px, 1.8)]

    def rafters(self):
        """8 caibros radiais: do vértice (anel de beiral) ao anel da lanterna mais próxima (+ 2 caibros de cumeeira no alongado)."""
        out = []
        for (x, y) in self.vertices():
            cx = self.M / 2 if x > 0 else -self.M / 2
            ang = math.atan2(y, x - cx)
            out.append([(x, y, self.Z_EAVE), (cx + self.R_LANTERN * math.cos(ang), self.R_LANTERN * math.sin(ang), self.Z_LANTERN)])
        if self.M >= 0.5:
            for sg in (-1, 1):
                out.append([(-self.M / 2, sg * self.R_LANTERN, self.Z_LANTERN), (self.M / 2, sg * self.R_LANTERN, self.Z_LANTERN)])
        return out

    def _rim(self, na=64):
        """amostras em volta do perímetro: (cx, ux, uy, r_edge) — centro da lanterna, direção radial unitária e raio até o beiral."""
        ro = self.r_corner() + self.OVER / math.cos(math.pi / self.N)
        def r_edge(ang):
            k = (ang - math.pi / 8) % (2 * math.pi / self.N) - math.pi / self.N
            return ro * math.cos(math.pi / self.N) / math.cos(k)
        out = []
        if self.M < 0.5:
            for j in range(na):
                ang = 2 * math.pi * j / na
                out.append((0.0, math.cos(ang), math.sin(ang), r_edge(ang)))
            return out
        half = na // 2; seg = max(4, na // 8); ry = self.F / 2 + self.OVER
        for j in range(half + 1):                                   # arco direito: -90° -> +90° em torno de (+M/2, 0)
            ang = -math.pi / 2 + math.pi * j / half
            out.append((self.M / 2, math.cos(ang), math.sin(ang), r_edge(ang)))
        for j in range(1, seg):                                     # topo: de +M/2 a -M/2, direção +y
            out.append((self.M / 2 - self.M * j / seg, 0.0, 1.0, ry))
        for j in range(half + 1):                                   # arco esquerdo: 90° -> 270° em torno de (-M/2, 0)
            ang = math.pi / 2 + math.pi * j / half
            out.append((-self.M / 2, math.cos(ang), math.sin(ang), r_edge(ang)))
        for j in range(1, seg):                                     # base: de -M/2 a +M/2, direção -y
            out.append((-self.M / 2 + self.M * j / seg, 0.0, -1.0, ry))
        return out

    def roof_mesh(self, nr=14, na=64):
        """membrana cônica em gomos: anel da(s) lanterna(s) -> beiral (polígono com balanço OVER). No octógono alongado
        a superfície é gerada em torno do 'estádio' que liga as duas lanternas (cumeeira reta entre elas)."""
        verts, faces = [], []
        rim = self._rim(na); n = len(rim)
        for i in range(nr + 1):
            t = i / nr
            for (cx, ux, uy, re) in rim:
                r = self.R_LANTERN + (re - self.R_LANTERN) * t
                z = self.roof_z(r) if t < 1 else self.Z_EAVE - 0.35
                verts.append((cx + r * ux, r * uy, z))
        for i in range(nr):
            for j in range(n):
                a0 = i * n + j; a1 = i * n + (j + 1) % n; b0 = a0 + n; b1 = a1 + n
                faces.append((a0, b0, b1)); faces.append((a0, b1, a1))
        if self.M >= 0.5:   # cumeeira plana entre as duas lanternas
            k = len(verts); r = self.R_LANTERN; z = self.Z_LANTERN
            verts += [(-self.M / 2, -r, z), (self.M / 2, -r, z), (self.M / 2, r, z), (-self.M / 2, r, z)]
            faces += [(k, k + 1, k + 2), (k, k + 2, k + 3)]
        return dict(vertices=verts, faces=faces)

    def piles(self):
        """estacas helicoidais sob piso e deck (malha ~2,4 x 1,7 m) + uma sob cada poste da vela."""
        R = self.r_corner(); pts = []
        for x in (-2.4, 0.0, 2.4):
            for y in (-2.55, -0.85, 0.85, 2.55):
                pts.append((x, y))
        for (x, y) in ((-3.4, 0.0), (3.4, 0.0), (0.0, -3.4), (0.0, 3.4)): pts.append((x, y))
        px = -R - self.DECK_D
        for y in (-3.2, -1.1, 1.1, 3.2): pts.append((-4.7, y))
        for y in (-1.8, 1.8): pts.append((px + 0.2, y))
        return pts

    def spec(self):
        return dict(name=self.NAME, F=self.F, side=self.side(), floor_area=self.floor_area(), deck_area=self.deck_area(), z_eave=self.Z_EAVE, z_top=self.Z_TOP)

    def export(self):
        return dict(name=self.NAME, vertices=self.vertices(), walls=self.walls(), furniture=self.furniture(), rafters=self.rafters(), roof=self.roof_mesh(),
                    deck=self.deck_pts(), sail_posts=self.sail_posts(), piles=self.piles(), lantern=dict(r=self.R_LANTERN, z1=self.Z_LANTERN, z2=self.Z_TOP), z_eave=self.Z_EAVE)


class Lodge24(Lodge):
    """ZION LODGE 24: octógono compacto de 5,40 m entre faces (24 m²), deck em uma face, lanterna única. Referência de mercado: lodges de 23 m²."""
    NAME = "ZION LODGE 24"; LABEL = "ZION LODGE 24"; CODE = "lodge24"
    F = 5.4; M = 0.0
    Z_EAVE = 2.6; Z_LANTERN = 4.2; Z_TOP = 4.7; R_LANTERN = 0.6; OVER = 0.8
    DECK_D = 2.0; DECK_FACES = [3, 4]
    SAIL = dict(z_post=2.3, reach=2.0)
    X_PART = 1.2
    GLASS_FACES = [(2, 3), (3, 4), (4, 5)]
    WALL_FACES = [(5, 6), (6, 7), (7, 0), (0, 1), (1, 2)]

    def walls(self):
        V = self.vertices(); W = []
        for (i, j) in self.GLASS_FACES:
            W.append(dict(p1=V[i], p2=V[j], z1=0, z2=self.Z_EAVE - 0.15, kind="glass", name="Vidro insulado fixo / porta de correr" if (i, j) == (3, 4) else "Vidro insulado fixo"))
        for (i, j) in self.WALL_FACES:
            W.append(dict(p1=V[i], p2=V[j], z1=0, z2=self.Z_EAVE - 0.15, kind="wood", name="Painel SIP 100 mm + ripado"))
        W.append(dict(p1=V[1], p2=V[2], z1=1.1, z2=2.1, kind="window", name="Janela do café 1,60 x 1,00"))
        W.append(dict(p1=V[5], p2=V[6], z1=1.6, z2=2.2, kind="window", name="Fresta alta do banho"))
        yc = math.sqrt(self.r_corner() ** 2 - self.X_PART ** 2)
        W.append(dict(p1=(self.X_PART, -yc), p2=(self.X_PART, yc), z1=0, z2=2.3, kind="partition", name="Parede-corda do banho"))
        return W

    def furniture(self):
        F = []
        F.append(box(self.X_PART, self.X_PART + 0.1, -2.3, 2.3, 0, 2.3, "wall", "Parede do banho"))
        F.append(box(self.X_PART, self.X_PART + 0.1, -0.35, 0.45, 0, 2.1, "opening", "Porta de correr do banho"))
        F.append(box(-0.85, 1.15, -0.97, 0.97, 0, 0.55, "bed", "Cama king 1,93 x 2,03"))
        F.append(box(-0.85, 1.15, -0.97, 0.97, 0.55, 0.62, "pillow", ""))
        F.append(box(0.65, 1.15, 1.05, 1.5, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(0.65, 1.15, -1.5, -1.05, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(-1.2, 0.4, 1.75, 2.35, 0, 0.9, "cabinet", "Café / minibar"))
        F.append(box(-1.2, 0.4, -2.35, -1.75, 0, 2.2, "cabinet", "Closet"))
        F.append(box(-2.45, -1.7, -0.8, 0.8, 0, 0.75, "chair", "Poltronas (2)"))
        F.append(cyl(-1.65, 0.0, 0, 0.45, 0.25, "table", "Mesa lateral"))
        F.append(box(1.4, 2.0, 0.6, 1.8, 0, 0.85, "vanity", "Bancada 1,20"))
        F.append(box(2.1, 2.7, 1.1, 1.8, 0, 0.42, "wc", "Bacia sanitária"))
        F.append(box(1.8, 2.7, -1.75, -0.85, 0, 0.02, "shower", "Chuveiro 0,90 x 0,90"))
        F.append(box(1.8, 1.83, -1.75, -0.85, 0, 2.1, "glass", "Vidro do box"))
        F.append(box(self.X_PART, 2.9, -2.2, 2.2, 2.3, 2.35, "ceiling", "Forro do banho"))
        F.append(box(1.6, 2.4, -0.4, 0.4, 2.4, 2.55, "hvac", "Evaporadora hi-wall / dutada 9k BTU"))
        F.append(box(3.6, 4.3, -1.6, -0.9, 0, 0.62, "condenser", "Condensadora"))
        return F

    def piles(self):
        pts = [(x, y) for x in (-1.9, 0.0, 1.9) for y in (-1.9, 0.0, 1.9)]
        pts += [(-2.9, 0.0), (2.9, 0.0), (0.0, -2.9), (0.0, 2.9)]
        pts += [(-4.3, -1.0), (-4.3, 1.0)]
        return pts

    def sail_posts(self):
        px = -self.r_corner() - self.SAIL["reach"]
        return [(px, -1.1), (px, 1.1)]


class Lodge28(Lodge):
    """ZION LODGE 28: octógono alongado (4,20 m entre faces + 3,60 m de corpo = 7,80 m), duas lanternas, deck frontal em três faces. Referência de mercado: lodges de 26 m² + terraço 17 m²."""
    NAME = "ZION LODGE 28"; LABEL = "ZION LODGE 28"; CODE = "lodge28"
    F = 4.2; M = 3.6
    Z_EAVE = 2.6; Z_LANTERN = 4.0; Z_TOP = 4.45; R_LANTERN = 0.55; OVER = 0.8
    DECK_D = 2.2; DECK_FACES = [2, 3, 4, 5]
    SAIL = dict(z_post=2.3, reach=2.2)
    X_PART = 1.9
    GLASS_FACES = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    WALL_FACES = [(6, 7), (7, 0), (0, 1)]

    def walls(self):
        V = self.vertices(); W = []
        for (i, j) in self.GLASS_FACES:
            W.append(dict(p1=V[i], p2=V[j], z1=0, z2=self.Z_EAVE - 0.15, kind="glass", name="Vidro insulado fixo / porta de correr" if (i, j) == (3, 4) else "Vidro insulado fixo"))
        for (i, j) in self.WALL_FACES:
            W.append(dict(p1=V[i], p2=V[j], z1=0, z2=self.Z_EAVE - 0.15, kind="wood", name="Painel SIP 100 mm + ripado"))
        W.append(dict(p1=V[7], p2=V[0], z1=1.6, z2=2.2, kind="window", name="Fresta alta do banho"))
        W.append(dict(p1=(self.X_PART, -2.1), p2=(self.X_PART, 2.1), z1=0, z2=2.3, kind="partition", name="Parede do banho"))
        return W

    def furniture(self):
        F = []
        F.append(box(self.X_PART, self.X_PART + 0.1, -2.1, 2.1, 0, 2.3, "wall", "Parede do banho"))
        F.append(box(self.X_PART, self.X_PART + 0.1, -0.4, 0.4, 0, 2.1, "opening", "Porta de correr do banho"))
        F.append(box(-0.85, 1.15, -0.97, 0.97, 0, 0.55, "bed", "Cama king 1,93 x 2,03"))
        F.append(box(-0.85, 1.15, -0.97, 0.97, 0.55, 0.62, "pillow", ""))
        F.append(box(0.65, 1.15, 1.05, 1.5, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(0.65, 1.15, -1.5, -1.05, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(-1.2, 0.6, 1.5, 2.05, 0, 0.9, "cabinet", "Café / minibar"))
        F.append(box(-1.2, 0.6, -2.05, -1.5, 0, 2.2, "cabinet", "Closet"))
        F.append(box(-3.4, -2.2, -1.0, 1.0, 0, 0.8, "sofa", "Sofá 2,00"))
        F.append(cyl(-1.75, 0.0, 0, 0.45, 0.28, "table", "Mesa de centro"))
        F.append(box(2.1, 2.7, 0.6, 1.9, 0, 0.85, "vanity", "Bancada 1,30"))
        F.append(box(2.9, 3.5, 1.2, 1.9, 0, 0.42, "wc", "Bacia sanitária"))
        F.append(box(2.5, 3.5, -1.9, -0.9, 0, 0.02, "shower", "Chuveiro 1,00 x 1,00"))
        F.append(box(2.5, 2.53, -1.9, -0.9, 0, 2.1, "glass", "Vidro do box"))
        F.append(box(self.X_PART, 3.9, -2.1, 2.1, 2.3, 2.35, "ceiling", "Forro do banho"))
        F.append(box(2.2, 3.2, -0.4, 0.4, 2.4, 2.55, "hvac", "Evaporadora dutada 9k BTU"))
        F.append(box(4.5, 5.2, -1.6, -0.9, 0, 0.62, "condenser", "Condensadora"))
        return F

    def piles(self):
        pts = [(x, y) for x in (-2.8, -1.4, 0.0, 1.4, 2.8) for y in (-1.5, 0.0, 1.5)]
        pts += [(-3.9, 0.0), (3.9, 0.0)]
        pts += [(-5.4, -1.4), (-5.4, 1.4), (-4.4, -2.6), (-4.4, 2.6)]
        return pts

    def sail_posts(self):
        px = -self.r_corner() - self.M / 2 - self.SAIL["reach"]
        return [(px, -1.3), (px, 1.3)]


LODGES = {"lodge": Lodge, "lodge24": Lodge24, "lodge28": Lodge28}


# ==================================================================================
# ZION CÁPSULA
# ==================================================================================
class Capsule:
    """Cápsula monocoque: seção em superelipse (3,20 x 3,20 m) extrudada em 8,40 m, com calota de vidro na frente (Visor)
    e calota fechada atrás (compartimento técnico). Eixos: x = comprimento (0 = ponta do Visor), y = largura (0 = eixo),
    z = altura (0 = piso interno acabado). A unidade viaja inteira e pousa sobre quatro pés telescópicos."""
    NAME = "ZION CÁPSULA"; CODE = "capsule"; TAG = "ZK"
    L = 8.40           # comprimento externo total
    A = 1.60           # semi-largura externa (largura 3,20)
    B = 1.60           # semi-altura externa (altura da casca 3,20)
    ZC = 0.85          # centro da seção acima do piso interno
    N = 3.2            # expoente da superelipse da seção (cantos cheios)
    X_NOSE = 1.20      # comprimento da calota frontal (Visor)
    X_TAIL = 0.90      # comprimento da calota traseira
    N_END = 2.3        # expoente das calotas
    SKIN = 0.14        # envelope: ACM 4 mm + PIR 60 mm + câmara 40 mm + compensado curvado 12 mm (+ anéis embutidos)
    Z_GROUND = -1.05   # terreno em relação ao piso interno (0,42 m livres sob a barriga)
    X_PART = 5.60      # parede do banho
    X_TECH = 7.55      # início do compartimento técnico (calota traseira)
    RINGS = [0.75 + 0.6 * i for i in range(12)]          # 12 anéis a cada 0,60 m
    STRINGER_DEG = [90, 55, 125, 20, 160, -20, 200]       # 7 longarinas (ângulo a partir de +y, no plano da seção)
    LIGHT_RING = (3.95, 4.40)                             # Anel de Luz: faixa de vidro sobre a cama (x1, x2)
    LIGHT_ANG = math.radians(65)                          # meio-ângulo do anel a partir do zênite
    PORTHOLES = [dict(name="Olho da suíte", x=3.35, side=-1, r=0.32, z=1.35),
                 dict(name="Olho do banho", x=6.35, side=+1, r=0.26, z=1.60)]
    VISOR_JOINTS = [-0.95, -0.45, 0.45, 0.95]             # juntas verticais dos 5 gomos de vidro curvo
    DOOR = dict(y1=-0.45, y2=0.45, h=2.05)                # porta pivotante no gomo central do Visor
    LEGS = [(1.5, -1.0), (1.5, 1.0), (6.9, -1.0), (6.9, 1.0)]
    DECK = dict(x1=-2.4, x2=0.2, y1=-1.6, y2=1.6)         # 2,6 x 3,2 = 8,3 m²

    # ---- perfil longitudinal ----
    def s(self, x):
        """fator de escala da seção (1 no corpo, 0 nas pontas)."""
        if x < self.X_NOSE: return sef((self.X_NOSE - x) / self.X_NOSE, self.N_END)
        if x > self.L - self.X_TAIL: return sef((x - (self.L - self.X_TAIL)) / self.X_TAIL, self.N_END)
        return 1.0

    def _pt(self, th, s, a, b):
        c, sn = math.cos(th), math.sin(th)
        y = a * s * math.copysign(abs(c) ** (2 / self.N), c)
        z = self.ZC + b * s * math.copysign(abs(sn) ** (2 / self.N), sn)
        return y, z

    def section(self, x, n=48, inner=False):
        """seção transversal em x: lista de (x, y, z) no sentido anti-horário a partir de +y (th = 0)."""
        a, b = (self.A - self.SKIN, self.B - self.SKIN) if inner else (self.A, self.B)
        s = self.s(x); out = []
        for i in range(n):
            th = 2 * math.pi * i / n
            y, z = self._pt(th, s, a, b); out.append((x, y, z))
        return out

    def top(self, x): return self.ZC + self.B * self.s(x)
    def bottom(self, x): return self.ZC - self.B * self.s(x)
    def half_width(self, x): return self.A * self.s(x)

    def hw_at(self, x, z, inner=True):
        """meia-largura da seção na altura z (0 se fora)."""
        a, b = (self.A - self.SKIN, self.B - self.SKIN) if inner else (self.A, self.B)
        s = self.s(x)
        if s <= 1e-6: return 0.0
        u = abs(z - self.ZC) / (b * s)
        if u >= 1: return 0.0
        return a * s * (1 - u ** self.N) ** (1 / self.N)

    def floor_hw(self, x): return self.hw_at(x, 0.0, inner=True)

    def floor_range(self, hw_min=0.25):
        xs = [i * 0.01 for i in range(int(self.L * 100) + 1)]
        ok = [x for x in xs if self.floor_hw(x) >= hw_min]
        return (ok[0], min(ok[-1], self.X_TECH)) if ok else (0, 0)

    def floor_area(self):
        x0, x1 = self.floor_range(); n = 400; a = 0.0
        for i in range(n):
            x = x0 + (x1 - x0) * (i + 0.5) / n; a += 2 * self.floor_hw(x) * (x1 - x0) / n
        return a

    def deck_area(self):
        D = self.DECK; return (D["x2"] - D["x1"]) * (D["y2"] - D["y1"])

    def floor_outline(self, n=60):
        x0, x1 = self.floor_range(0.05)
        top = [(x0 + (x1 - x0) * i / n, self.floor_hw(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
        return top + [(x, -y) for x, y in top[::-1]]

    def plan_outline(self, n=80):
        pts = [(self.L * i / n, self.half_width(self.L * i / n)) for i in range(n + 1)]
        return pts + [(x, -y) for x, y in pts[::-1]]

    def profile(self, n=80):
        """silhueta no plano y = 0: topo e barriga (x, z)."""
        xs = [self.L * i / n for i in range(n + 1)]
        return [(x, self.top(x)) for x in xs] + [(x, self.bottom(x)) for x in xs[::-1]]

    # ---- regiões da casca ----
    def region(self, x, th):
        """'visor' (calota frontal de vidro), 'ring' (Anel de Luz), 'shell' (casca opaca)."""
        z = self._pt(th, self.s(x), self.A, self.B)[1]
        if x < self.X_NOSE - 0.02 and z > -0.02: return "visor"
        x1, x2 = self.LIGHT_RING
        if x1 <= x <= x2 and abs(((th - math.pi / 2 + math.pi) % (2 * math.pi)) - math.pi) <= self.LIGHT_ANG: return "ring"
        return "shell"

    def shell_mesh(self, nx=64, na=40):
        """malha da casca por região: {regiao: (vertices, faces)}."""
        xs = [0.01 + (self.L - 0.02) * i / nx for i in range(nx + 1)]
        secs = [self.section(x, na) for x in xs]
        verts = [p for sec in secs for p in sec]
        out = {"visor": [], "ring": [], "shell": []}
        for i in range(nx):
            for j in range(na):
                a, b = i * na + j, i * na + (j + 1) % na
                c, d = (i + 1) * na + (j + 1) % na, (i + 1) * na + j
                xm = (xs[i] + xs[i + 1]) / 2; thm = 2 * math.pi * (j + 0.5) / na
                r = self.region(xm, thm); out[r].append((a, b, c)); out[r].append((a, c, d))
        return {k: (verts, f) for k, f in out.items()}

    def shell_area(self, region=None, nx=120, na=72):
        """área da casca (m²) total ou por região."""
        m = self.shell_mesh(nx, na); tot = 0.0
        for k, (V, F) in m.items():
            if region and k != region: continue
            V = np.array(V)
            for (a, b, c) in F:
                tot += 0.5 * np.linalg.norm(np.cross(V[b] - V[a], V[c] - V[a]))
        return tot

    # ---- estrutura ----
    def rings(self, n=48):
        return [self.section(x, n, inner=False) for x in self.RINGS]

    def ring_perimeter(self):
        pts = self.section(self.RINGS[3], 96); return sum(math.dist(pts[i][1:], pts[(i + 1) % 96][1:]) for i in range(96))

    def stringers(self):
        out = []
        for deg in self.STRINGER_DEG:
            th = math.radians(deg)
            out.append([(x, *self._pt(th, self.s(x), self.A - 0.05, self.B - 0.05)) for x in [self.RINGS[0] + (self.RINGS[-1] - self.RINGS[0]) * i / 30 for i in range(31)]])
        return out

    def chassis(self):
        """vigas longitudinais U 150 e travessas U 100 do piso (x1, x2, y1, y2, z1, z2)."""
        F = [box(0.55, 7.75, -1.05, -0.95, -0.22, -0.07, "beam", "Longarina U 150 direita"), box(0.55, 7.75, 0.95, 1.05, -0.22, -0.07, "beam", "Longarina U 150 esquerda")]
        for x in self.RINGS:
            hw = max(0.6, self.hw_at(x, -0.15, inner=True) - 0.05)
            F.append(box(x - 0.04, x + 0.04, -hw, hw, -0.2, -0.08, "beam", "Travessa U 100"))
        return F

    def legs(self):
        return [dict(x=x, y=y, z1=self.Z_GROUND, z2=self.ZC - self.B * (1 - (abs(y) / self.A) ** self.N) ** (1 / self.N) + 0.05, r=0.05) for (x, y) in self.LEGS]

    # ---- programa ----
    def furniture(self):
        F = []
        F.append(box(self.X_PART - 0.04, self.X_PART + 0.04, -1.4, 1.4, 0, 2.25, "wall", "Parede do banho"))
        F.append(box(self.X_PART - 0.04, self.X_PART + 0.04, 0.25, 1.05, 0, 2.05, "opening", "Porta de correr 0,80"))
        F.append(box(3.15, 5.13, -0.79, 0.79, 0, 0.52, "bed", "Cama queen 1,58 x 1,98"))
        F.append(box(3.15, 5.13, -0.79, 0.79, 0.52, 0.58, "pillow", ""))
        F.append(box(4.7, 5.1, 0.85, 1.25, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(4.7, 5.1, -1.25, -0.85, 0, 0.5, "table", "Criado-mudo"))
        F.append(box(3.1, 4.4, 0.95, 1.35, 0, 2.0, "cabinet", "Closet 1,30 x 0,40"))
        F.append(box(1.3, 2.9, -1.3, -0.5, 0, 0.45, "sofa", "Chaise de contemplação 1,60 x 0,80"))
        F.append(box(1.25, 1.9, 0.6, 1.3, 0, 0.75, "chair", "Poltrona"))
        F.append(box(1.95, 3.0, 0.85, 1.35, 0, 0.9, "cabinet", "Café / minibar 1,05 x 0,50"))
        F.append(cyl(2.25, -0.05, 0, 0.45, 0.25, "table", "Mesa lateral"))
        F.append(box(5.75, 6.95, 0.75, 1.3, 0, 0.85, "vanity", "Bancada 1,20 m"))
        F.append(box(5.75, 6.4, -1.3, -0.72, 0, 0.42, "wc", "Bacia sanitária"))
        F.append(box(6.6, 7.5, -1.3, -0.4, 0, 0.02, "shower", "Chuveiro 0,90 x 0,90"))
        F.append(box(6.6, 6.63, -1.3, -0.4, 0, 2.0, "glass", ""))
        F.append(box(self.X_TECH, 8.1, -0.9, 0.9, 0, 1.6, "hvac", "Compartimento técnico: boiler 80 L, quadro, evaporadora"))
        return F

    def export(self):
        return dict(name=self.NAME, code=self.CODE, L=self.L, A=self.A, B=self.B, ZC=self.ZC, N=self.N, floor_area=self.floor_area(), deck_area=self.deck_area(),
                    rings=self.RINGS, legs=self.LEGS, deck=self.DECK, light_ring=self.LIGHT_RING, furniture=self.furniture())
