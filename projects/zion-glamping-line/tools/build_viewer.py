#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_viewer.py — gera os visualizadores 3D interativos (Three.js r128, HTML autocontido)
dos produtos ZION COCOON e ZION ZENITH a partir de geometry.py (fonte única de verdade).

Uso:
    python3 build_viewer.py [--out-json <dir>] [--cdn]

Saídas:
    ../cocoon/3d/zion-cocoon-3d.html
    ../zenith/3d/zion-zenith-3d.html
    <dir>/cocoon_geometry.json e <dir>/zenith_geometry.json (padrão: scratchpad ou ./build)

Por padrão as bibliotecas (three.min.js, OrbitControls.js, GLTFExporter.js) são embutidas
a partir de tools/vendor/ (three@0.128.0 = r128). Com --cdn usam-se as URLs do cdnjs.
O script é determinístico: mesma geometria => mesmo HTML.
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import geometry as G  # noqa: E402

CDN = {
    "three": "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
    "orbit": "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/examples/js/controls/OrbitControls.js",
    "gltf": "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/examples/js/exporters/GLTFExporter.js",
}
VENDOR = {
    "three": os.path.join(HERE, "vendor", "three.min.js"),
    "orbit": os.path.join(HERE, "vendor", "OrbitControls.js"),
    "gltf": os.path.join(HERE, "vendor", "GLTFExporter.js"),
}


# ----------------------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------------------
def rnd(o, nd=4):
    """arredonda recursivamente todos os floats (JSON menor e determinístico)."""
    if isinstance(o, float):
        r = round(o, nd)
        return 0.0 if r == 0 else r
    if isinstance(o, (list, tuple)):
        return [rnd(v, nd) for v in o]
    if isinstance(o, dict):
        return {k: rnd(v, nd) for k, v in o.items()}
    return o


def centroid(V, f):
    return [(V[f[0]][k] + V[f[1]][k] + V[f[2]][k]) / 3.0 for k in range(3)]


# ----------------------------------------------------------------------------------
# COCOON: dados extras derivados da geometria (sem alterar geometry.py)
# ----------------------------------------------------------------------------------
def cocoon_shell_offset(c, offset, nu, nv, x_start):
    """malha da concha deslocada (forro interno) — só faces de membrana."""
    xs = [x_start + (c.L - x_start) * (i / nu) for i in range(nu + 1)]
    verts, faces = [], []
    for x in xs:
        t0, t1 = c.theta_range(x)
        for j in range(nv + 1):
            th = t0 + (t1 - t0) * j / nv
            verts.append(c.section_point(x, th, offset))
    for i in range(nu):
        for j in range(nv):
            a0 = i * (nv + 1) + j
            a1 = a0 + 1
            b0 = a0 + (nv + 1)
            b1 = b0 + 1
            xm = (xs[i] + xs[i + 1]) / 2
            t0, t1 = c.theta_range(xm)
            thm = t0 + (t1 - t0) * (j + 0.5) / nv
            if not c.in_window(xm, thm):
                faces.append((a0, b0, b1))
                faces.append((a0, b1, a1))
    return dict(vertices=verts, faces=faces)


def cocoon_data():
    c = G.Cocoon()
    d = c.export()
    # forro interno (tecido tensionado) 12 cm para dentro da membrana, do plano de vidro à cauda
    d["liner"] = cocoon_shell_offset(c, -0.12, 64, 32, c.X_GLASS)
    # arcos e terças 6 cm para dentro da membrana (entre membrana e forro)
    d["arches_in"] = [dict(x=x, pts=c.section_curve(x, 48, offset=-0.06)) for x in c.ARCH_X]
    pur = []
    n = 60
    for v in c.PURLIN_V:
        pts = []
        for i in range(n + 1):
            x = c.X_FRONT + (8.6 - c.X_FRONT) * i / n
            t0, t1 = c.theta_range(x)
            pts.append(c.section_point(x, t0 + (t1 - t0) * v, -0.06))
        pur.append(pts)
    d["purlins_in"] = pur
    # trilhos da espinha de luz (treliça plana) nas bordas da claraboia
    x1, x2, ht = c.SPINE
    rails = []
    for sgn in (-1, 1):
        pts = []
        for i in range(25):
            x = x1 + (x2 - x1) * i / 24
            pts.append(c.section_point(x, math.pi / 2 + sgn * ht, -0.03))
        rails.append(pts)
    d["spine_rails"] = rails
    # laje/quadro de piso sob toda a concha (x 0,5 a 9,0)
    right, left = [], []
    for i in range(61):
        x = c.X_FRONT + (c.L - c.X_FRONT) * i / 60
        hw = c.floor_hw(x)
        right.append((x, -hw))
        left.append((x, hw))
    d["slab"] = right + left[::-1]
    # plano da fachada de vidro: x = x0 - k * z
    d["glass_plane"] = dict(x0=c.X_GLASS, k=c.tilt(c.X_GLASS) / 3.9)
    d["top"] = c.top(c.XMAX)
    return d


# ----------------------------------------------------------------------------------
# ZENITH: dados extras
# ----------------------------------------------------------------------------------
def zenith_data():
    z = G.Zenith()
    d = z.export()
    oc = [p for p in z.PEAKS if p.get("oculus")]
    # separa as faces da membrana dentro do anel do óculo (viram vidro)
    V = d["roof"]["vertices"]
    memb, ocul = [], []
    for f in d["roof"]["faces"]:
        cx, cy, _ = centroid(V, f)
        if any(math.hypot(cx - p["x"], cy - p["y"]) <= p["r"] * 0.98 for p in oc):
            ocul.append(f)
        else:
            memb.append(f)
    d["roof"] = dict(vertices=V, faces=memb, oculus=ocul)
    # forro: abre poço de luz sob os dois cumes
    LV = d["liner"]["vertices"]
    lf = []
    for f in d["liner"]["faces"]:
        cx, cy, _ = centroid(LV, f)
        if not any(math.hypot(cx - p["x"], cy - p["y"]) <= p["r"] * 1.02 for p in z.PEAKS):
            lf.append(f)
    d["liner"] = dict(vertices=LV, faces=lf)
    # topo dos postes externos (altura da borda da membrana no ponto)
    d["post_tops"] = [z.roof_z(x, y) for (x, y) in z.posts()]
    # cabo de borda: contorno da cobertura com a catenária entre postes
    x0, x1, y0, y1 = z.roof_bounds()
    edge = []
    n = 40
    for i in range(n):  # frente (x0), de y0 a y1
        y = y0 + (y1 - y0) * i / n
        edge.append((x0, y, z.edge_height(x0, y)))
    for i in range(n):  # lado y1, de x0 a x1
        x = x0 + (x1 - x0) * i / n
        edge.append((x, y1, z.edge_height(x, y1)))
    for i in range(n):  # fundos (x1), de y1 a y0
        y = y1 - (y1 - y0) * i / n
        edge.append((x1, y, z.edge_height(x1, y)))
    for i in range(n):  # lado y0, de x1 a x0
        x = x1 - (x1 - x0) * i / n
        edge.append((x, y0, z.edge_height(x, y0)))
    d["edge_cable"] = edge
    d["x_head"] = z.X_HEAD
    return d


# ----------------------------------------------------------------------------------
# HTML / JS do visualizador
# ----------------------------------------------------------------------------------
HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — Modelo 3D</title>
<style>
  :root { --cream:#FEF5F0; --gold:#C9A84C; --bg:#040605; }
  html, body { margin:0; height:100%; background:var(--bg); color:var(--cream); font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; overflow:hidden; }
  canvas#c { display:block; width:100vw; height:100vh; }
  #hud { position:fixed; inset:0; pointer-events:none; }
  .brand { position:absolute; left:32px; top:28px; }
  .eyebrow { font-size:10px; letter-spacing:.42em; text-transform:uppercase; color:var(--gold); opacity:.95; }
  h1 { margin:6px 0 4px; font-family: Georgia, "Times New Roman", serif; font-weight:400; font-size:30px; letter-spacing:.32em; text-transform:uppercase; color:var(--cream); }
  .sub { font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(254,245,240,.62); }
  .bar { position:absolute; right:28px; top:32px; display:flex; gap:8px; pointer-events:auto; flex-wrap:wrap; justify-content:flex-end; }
  .bar button, .bar select { background:rgba(4,6,5,.55); color:var(--cream); border:1px solid rgba(254,245,240,.28); padding:8px 14px; font-size:10.5px; letter-spacing:.22em; text-transform:uppercase; cursor:pointer; backdrop-filter: blur(6px); border-radius:2px; font-family:inherit; }
  .bar button:hover { border-color:var(--gold); color:var(--gold); }
  .bar button.on { background:var(--gold); color:#0a0a0a; border-color:var(--gold); }
  .bar select { letter-spacing:.12em; }
  #hint { position:absolute; left:32px; bottom:24px; font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:rgba(254,245,240,.45); }
  #hint b { color:var(--gold); font-weight:400; }
  #load { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:11px; letter-spacing:.35em; text-transform:uppercase; color:rgba(254,245,240,.6); background:var(--bg); transition:opacity .6s; }
  #load.off { opacity:0; pointer-events:none; }
  @media (max-width:720px){ h1{font-size:20px} .bar{left:20px; right:20px; top:auto; bottom:48px; justify-content:flex-start} .brand{left:20px;top:18px} }
</style>
__LIBS__
</head>
<body>
<canvas id="c"></canvas>
<div id="hud">
  <div class="brand">
    <div class="eyebrow">Zion Glamping Line · Zion Shell System™</div>
    <h1>__TITLE__</h1>
    <div class="sub">__SUBTITLE__</div>
  </div>
  <div class="bar">
    <button data-view="ext_front">Exterior</button>
    <button data-view="int_living">Interior</button>
    <button id="bStruct">Estrutura</button>
    <button id="bNight">Noite</button>
    <button id="bCut">Cortar</button>
    <select id="views" title="Vistas"></select>
  </div>
  <div id="hint"><b>Arraste</b> para orbitar · <b>roda</b> para aproximar · <b>botão direito</b> para deslocar</div>
  <div id="load">A preparar o modelo…</div>
</div>
<script>
__DATA_SCRIPT__
</script>
<script>
(function(){
'use strict';
const MODEL = "__MODEL__";
const D = window.ZION_DATA;
window.sceneReady = false;
window.frameCount = 0;

// ---------- coordenadas: projeto (x=comprimento, y=largura, z=altura) -> Three (x, y=altura, z=-y) ----------
const V = p => new THREE.Vector3(p[0], p[2], -p[1]);
const Vx = (x, y, z) => new THREE.Vector3(x, z, -y);

// ---------- renderer / cena ----------
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.localClippingEnabled = true;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.05, 500);
const controls = new THREE.OrbitControls(camera, canvas);
controls.enableDamping = true; controls.dampingFactor = 0.08; controls.maxPolarAngle = Math.PI * 0.53;

// ---------- céu (gradiente) ----------
const skyU = { top: { value: new THREE.Color(0x040605) }, mid: { value: new THREE.Color(0x141f18) }, hor: { value: new THREE.Color(0x4a4a3a) }, sun: { value: new THREE.Vector3(0, 1, 0) }, sunI: { value: 0.35 } };
const sky = new THREE.Mesh(new THREE.SphereGeometry(380, 40, 20), new THREE.ShaderMaterial({
  uniforms: skyU, side: THREE.BackSide, depthWrite: false, fog: false,
  vertexShader: 'varying vec3 vW; void main(){ vW = normalize((modelMatrix*vec4(position,1.)).xyz); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
  fragmentShader: 'uniform vec3 top,mid,hor,sun; uniform float sunI; varying vec3 vW; void main(){ float h = clamp(vW.y,-0.05,1.0); vec3 c = mix(hor, mid, smoothstep(0.0,0.18,h)); c = mix(c, top, smoothstep(0.12,0.75,h)); float s = pow(max(dot(normalize(vW), normalize(sun)),0.0), 22.0); c += vec3(1.0,0.82,0.55)*s*sunI; gl_FragColor = vec4(c,1.0); }'
}));
sky.name = 'sky'; scene.add(sky);
scene.fog = new THREE.Fog(0x141c16, 45, 190); scene.fog.color.convertSRGBToLinear();

// ---------- luzes ----------
const hemi = new THREE.HemisphereLight(0xc6d4e2, 0x3d4a2f, 0.55); hemi.color.convertSRGBToLinear(); hemi.groundColor.convertSRGBToLinear(); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff0dc, 1.45); sun.color.convertSRGBToLinear();
const SUN_DAY = Vx(-11, -9, 15), SUN_NIGHT = Vx(9, 12, 14);
sun.position.copy(SUN_DAY); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -17; sun.shadow.camera.right = 17; sun.shadow.camera.top = 17; sun.shadow.camera.bottom = -17;
sun.shadow.camera.near = 1; sun.shadow.camera.far = 70; sun.shadow.bias = -0.0006; sun.shadow.normalBias = 0.03; sun.shadow.radius = 3;
sun.target.position.copy(Vx(4, 0, 0)); scene.add(sun); scene.add(sun.target);
const interiorLights = [];
function warmLight(x, y, z, iDay, dist) {
  const l = new THREE.PointLight(0xFFD9A0, iDay, dist, 2); l.color.convertSRGBToLinear(); l.position.copy(Vx(x, y, z)); l.userData.iDay = iDay * 0.5; l.userData.iNight = iDay * 2.2; l.intensity = l.userData.iDay; scene.add(l); interiorLights.push(l); return l;
}

// ---------- texturas (canvas, determinísticas) ----------
function lcg(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
function woodCanvas(w, h, base, dark, seed, grain) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d');
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  const r = lcg(seed);
  for (let i = 0; i < grain; i++) { g.fillStyle = 'rgba(0,0,0,' + (0.03 + r() * 0.07).toFixed(3) + ')'; const x = r() * w, y = r() * h; g.fillRect(x, y, 1 + r() * 2, 8 + r() * 60); }
  return { cv, g, dark };
}
function slatTexture() { // uma ripa 40 mm + fresta 40 mm por tile (pitch 80 mm)
  const { cv, g } = woodCanvas(64, 64, '#8a6a48', '#2a1d12', 7, 40);
  g.fillStyle = '#211710'; g.fillRect(34, 0, 30, 64);
  g.fillStyle = 'rgba(255,255,255,0.08)'; g.fillRect(0, 0, 3, 64);
  const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.encoding = THREE.sRGBEncoding; t.anisotropy = 4; return t;
}
function plankTexture(base, line, seed) { // 8 tábuas de 140 mm por tile (1,12 m), horizontais no canvas
  const { cv, g } = woodCanvas(256, 256, base, line, seed, 160);
  g.fillStyle = line; for (let i = 0; i < 8; i++) g.fillRect(0, i * 32, 256, 2);
  const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.encoding = THREE.sRGBEncoding; t.anisotropy = 4; return t;
}
const texSlat = slatTexture();
const texDeck = plankTexture('#8B6B4A', '#3d2c1c', 11);
const texFloor = plankTexture('#B99A73', '#7a6248', 23);

// ---------- materiais ----------
const M = {
  membrane: new THREE.MeshStandardMaterial({ color: 0xEDE6D6, roughness: 0.85, metalness: 0.0, side: THREE.DoubleSide, envMapIntensity: 0.35 }),
  liner: new THREE.MeshStandardMaterial({ color: 0xE8DCC6, roughness: 0.95, metalness: 0.0, side: THREE.DoubleSide, envMapIntensity: 0.25 }),
  glass: new THREE.MeshPhysicalMaterial({ color: 0xd8c5a6, transmission: 0.9, roughness: 0.05, metalness: 0.0, transparent: true, opacity: 0.55, side: THREE.DoubleSide, envMapIntensity: 1.4, clearcoat: 0.6, clearcoatRoughness: 0.05, depthWrite: false }),
  steel: new THREE.MeshStandardMaterial({ color: 0x3a3b3a, metalness: 0.7, roughness: 0.38 }),
  bronze: new THREE.MeshStandardMaterial({ color: 0x5b4732, metalness: 0.65, roughness: 0.4 }),
  cable: new THREE.MeshStandardMaterial({ color: 0x8c8f90, metalness: 0.9, roughness: 0.3 }),
  deck: new THREE.MeshStandardMaterial({ color: 0xffffff, map: texDeck, roughness: 0.82, metalness: 0.0 }),
  deckSide: new THREE.MeshStandardMaterial({ color: 0x6f5238, roughness: 0.85 }),
  woodInt: new THREE.MeshStandardMaterial({ color: 0xA8865E, roughness: 0.62, metalness: 0.0 }),
  woodSlat: new THREE.MeshStandardMaterial({ color: 0xffffff, map: texSlat, roughness: 0.7, metalness: 0.0 }),
  floor: new THREE.MeshStandardMaterial({ color: 0xffffff, map: texFloor, roughness: 0.55, metalness: 0.0 }),
  linen: new THREE.MeshStandardMaterial({ color: 0xF6F2EA, roughness: 0.92 }),
  white: new THREE.MeshStandardMaterial({ color: 0xF8F6F1, roughness: 0.28, metalness: 0.0 }),
  fabric: new THREE.MeshStandardMaterial({ color: 0xC9B79C, roughness: 0.95 }),
  plaster: new THREE.MeshStandardMaterial({ color: 0xEFE8DC, roughness: 0.9 }),
  dark: new THREE.MeshStandardMaterial({ color: 0x1c1d1c, roughness: 0.9 }),
  tile: new THREE.MeshStandardMaterial({ color: 0xd9d5cd, roughness: 0.35 }),
  grey: new THREE.MeshStandardMaterial({ color: 0x8a8d8a, roughness: 0.6, metalness: 0.3 }),
  water: new THREE.MeshPhysicalMaterial({ color: 0x6fb3c9, transmission: 0.55, roughness: 0.08, transparent: true, opacity: 0.85, clearcoat: 1.0, envMapIntensity: 1.2 }),
  led: new THREE.MeshBasicMaterial({ color: 0xffd9a0 }),
  ground: new THREE.MeshStandardMaterial({ color: 0x3d4a2f, roughness: 1.0 }),
  gravel: new THREE.MeshStandardMaterial({ color: 0x4b4d44, roughness: 1.0 }),
  leaf: new THREE.MeshStandardMaterial({ color: 0x27412a, roughness: 1.0 }),
  leaf2: new THREE.MeshStandardMaterial({ color: 0x334f2e, roughness: 1.0 }),
  trunk: new THREE.MeshStandardMaterial({ color: 0x3b2e22, roughness: 1.0 }),
};
// r128 trata cores hex como lineares: converter sRGB -> linear para as cores lerem como especificadas
const lin = hex => new THREE.Color(hex).convertSRGBToLinear();
for (const k in M) if (M[k].color) M[k].color.convertSRGBToLinear();
M.glass.userData.viewOpacity = M.glass.opacity;

// ---------- helpers geométricos ----------
const building = new THREE.Group(); building.name = MODEL === 'cocoon' ? 'ZION_COCOON' : 'ZION_ZENITH';
const site = new THREE.Group(); site.name = 'site';
scene.add(building); scene.add(site);

function shadowed(m, cast = true, recv = true) { m.castShadow = cast; m.receiveShadow = recv; return m; }
function add(m, parent) { (parent || building).add(m); return m; }

function tube(pts, r, mat, closed, segs, parent) {
  const curve = new THREE.CatmullRomCurve3(pts.map(V), !!closed, 'centripetal');
  const g = new THREE.TubeGeometry(curve, segs || Math.max(12, pts.length * 2), r, 8, !!closed);
  return add(shadowed(new THREE.Mesh(g, mat)), parent);
}
function bar(a, b, r, mat, parent) { // cilindro reto entre dois pontos (coord. projeto)
  const A = V(a), B = V(b); const d = new THREE.Vector3().subVectors(B, A); const len = d.length();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, 12), mat);
  m.position.copy(A).addScaledVector(d, 0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
  return add(shadowed(m), parent);
}
function boxMesh(x1, x2, y1, y2, z1, z2, mat, parent) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(Math.max(x2 - x1, 0.003), Math.max(z2 - z1, 0.003), Math.max(y2 - y1, 0.003)), mat);
  m.position.copy(Vx((x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2));
  return add(shadowed(m), parent);
}
function cylMesh(x, y, z1, z2, r, mat, parent, rTop) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rTop === undefined ? r : rTop, r, z2 - z1, 40), mat);
  m.position.copy(Vx(x, y, (z1 + z2) / 2));
  return add(shadowed(m), parent);
}
function shapeFrom(pts) { const s = new THREE.Shape(); pts.forEach((p, i) => i ? s.lineTo(p[0], p[1]) : s.moveTo(p[0], p[1])); s.closePath(); return s; }
function polyMesh(pts, z, mat, parent) { // polígono horizontal (x,y) em cota z
  const m = new THREE.Mesh(new THREE.ShapeGeometry(shapeFrom(pts)), mat);
  m.rotation.x = -Math.PI / 2; m.position.y = z;
  return add(shadowed(m, false, true), parent);
}
function slabMesh(pts, z1, z2, mat, parent) { // polígono extrudado de z1 a z2
  const m = new THREE.Mesh(new THREE.ExtrudeGeometry(shapeFrom(pts), { depth: z2 - z1, bevelEnabled: false }), mat);
  m.rotation.x = -Math.PI / 2; m.position.y = z1;
  return add(shadowed(m), parent);
}
function rectBox(p1, p2, z1, z2, t, mat, offset, parent) { // retângulo vertical entre p1 e p2 com espessura t; offset ao longo da normal exterior
  const dx = p2[0] - p1[0], dy = p2[1] - p1[1]; const L = Math.hypot(dx, dy);
  const n = outward(p1, p2);
  const cx = (p1[0] + p2[0]) / 2 + n[0] * (offset || 0), cy = (p1[1] + p2[1]) / 2 + n[1] * (offset || 0);
  const m = new THREE.Mesh(new THREE.BoxGeometry(L, z2 - z1, t), mat);
  m.position.copy(Vx(cx, cy, (z1 + z2) / 2)); m.rotation.y = Math.atan2(dy, dx);
  return add(shadowed(m), parent);
}
function indexedMesh(verts, faces, mat, parent, cast) {
  const g = new THREE.BufferGeometry();
  const pos = new Float32Array(verts.length * 3);
  verts.forEach((p, i) => { pos[i * 3] = p[0]; pos[i * 3 + 1] = p[2]; pos[i * 3 + 2] = -p[1]; });
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const idx = new Uint32Array(faces.length * 3); faces.forEach((f, i) => { idx[i * 3] = f[0]; idx[i * 3 + 1] = f[1]; idx[i * 3 + 2] = f[2]; });
  g.setIndex(new THREE.BufferAttribute(idx, 1)); g.computeVertexNormals();
  return add(shadowed(new THREE.Mesh(g, mat), cast !== false, true), parent);
}
function subtractBox(p, o, axis) { // subtrai a abertura o do painel p (eixo longo + z)
  const a1 = axis + '1', a2 = axis + '2';
  const olo = Math.max(p[a1], o[a1]), ohi = Math.min(p[a2], o[a2]);
  const zlo = Math.max(p.z1, o.z1), zhi = Math.min(p.z2, o.z2);
  if (olo >= ohi || zlo >= zhi) return [p];
  const out = [];
  if (p[a1] < olo - 1e-6) out.push(Object.assign({}, p, { [a2]: olo }));
  if (ohi < p[a2] - 1e-6) out.push(Object.assign({}, p, { [a1]: ohi }));
  if (p.z1 < zlo - 1e-6) out.push(Object.assign({}, p, { [a1]: olo, [a2]: ohi, z2: zlo }));
  if (zhi < p.z2 - 1e-6) out.push(Object.assign({}, p, { [a1]: olo, [a2]: ohi, z1: zhi }));
  return out;
}
let BODY_CENTER = [4.75, 0];
function outward(p1, p2) {
  const dx = p2[0] - p1[0], dy = p2[1] - p1[1]; const L = Math.hypot(dx, dy) || 1;
  let n = [dy / L, -dx / L];
  const mx = (p1[0] + p2[0]) / 2 - BODY_CENTER[0], my = (p1[1] + p2[1]) / 2 - BODY_CENTER[1];
  if (n[0] * mx + n[1] * my < 0) n = [-n[0], -n[1]];
  return n;
}

// ---------- mobiliário genérico ----------
function furniture(list) {
  const walls = list.filter(f => f.kind === 'wall'), openings = list.filter(f => f.kind === 'opening');
  const g = new THREE.Group(); g.name = 'mobiliario'; building.add(g);
  for (const f of list) {
    const isBox = f.x1 !== undefined;
    switch (f.kind) {
      case 'opening': break;
      case 'wall': {
        let pieces = [Object.assign({}, f)];
        const axis = (f.y2 - f.y1) > (f.x2 - f.x1) ? 'y' : 'x';
        for (const o of openings) pieces = pieces.flatMap(p => subtractBox(p, o, axis));
        pieces.forEach(p => boxMesh(p.x1, p.x2, p.y1, p.y2, p.z1, p.z2, M.plaster, g));
        break; }
      case 'bed': {
        boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z1 + 0.28, M.woodInt, g);
        boxMesh(f.x1 + 0.02, f.x2 - 0.02, f.y1 + 0.02, f.y2 - 0.02, f.z1 + 0.28, f.z2, M.linen, g);
        // colcha em areia na metade dos pés
        const px = (f.x1 + f.x2) / 2 - 0.1;
        boxMesh(f.x1 + 0.03, px, f.y1 - 0.06, f.y2 + 0.06, f.z2 - 0.02, f.z2 + 0.04, M.fabric, g);
        break; }
      case 'pillow': {
        const ym = (f.y1 + f.y2) / 2; const x2 = f.x2 - 0.06, x1 = x2 - 0.5;
        boxMesh(x1, x2, f.y1 + 0.08, ym - 0.05, f.z1, f.z2 + 0.08, M.linen, g);
        boxMesh(x1, x2, ym + 0.05, f.y2 - 0.08, f.z1, f.z2 + 0.08, M.linen, g);
        break; }
      case 'sofa': case 'chair': case 'bench': {
        boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1 + 0.12, f.z2, M.fabric, g);
        boxMesh(f.x1 + 0.05, f.x2 - 0.05, f.y1 + 0.05, f.y2 - 0.05, f.z1, f.z1 + 0.12, M.woodInt, g);
        if (f.kind !== 'bench') { // encosto no lado mais afastado do centro do ambiente
          const dx = f.x2 - f.x1, dy = f.y2 - f.y1; const cx = (f.x1 + f.x2) / 2, cy = (f.y1 + f.y2) / 2;
          const h = f.z2 + 0.38, t = 0.16;
          if (dx >= dy) { const back = (cy - BODY_CENTER[1]) > 0 ? [f.y2 - t, f.y2] : [f.y1, f.y1 + t]; boxMesh(f.x1, f.x2, back[0], back[1], f.z2, h, M.fabric, g); }
          else { const back = (cx - BODY_CENTER[0]) > 0 ? [f.x2 - t, f.x2] : [f.x1, f.x1 + t]; boxMesh(back[0], back[1], f.y1, f.y2, f.z2, h, M.fabric, g); }
        }
        break; }
      case 'table':
        if (isBox) boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, M.woodInt, g);
        else { cylMesh(f.x, f.y, f.z2 - 0.04, f.z2, f.r, M.woodInt, g); cylMesh(f.x, f.y, f.z1, f.z2 - 0.04, 0.05, M.steel, g); cylMesh(f.x, f.y, f.z1, f.z1 + 0.02, f.r * 0.7, M.steel, g); }
        break;
      case 'cabinet': case 'totem':
        boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, f.kind === 'totem' ? M.woodSlat : M.woodInt, g);
        if (f.kind === 'cabinet') boxMesh(f.x1 - 0.01, f.x2 + 0.01, f.y1 - 0.01, f.y2 + 0.01, f.z2 - 0.03, f.z2, M.dark, g);
        break;
      case 'vanity':
        boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1 + 0.15, f.z2 - 0.04, M.woodInt, g);
        boxMesh(f.x1 - 0.01, f.x2 + 0.01, f.y1 - 0.01, f.y2 + 0.01, f.z2 - 0.04, f.z2, M.white, g);
        { const dx = f.x2 - f.x1, dy = f.y2 - f.y1; const cx = (f.x1 + f.x2) / 2, cy = (f.y1 + f.y2) / 2;
          if (dx >= dy) { cylMesh(cx - dx * 0.25, cy, f.z2, f.z2 + 0.12, 0.19, M.white, g); cylMesh(cx + dx * 0.25, cy, f.z2, f.z2 + 0.12, 0.19, M.white, g); }
          else { cylMesh(cx, cy - dy * 0.25, f.z2, f.z2 + 0.12, 0.19, M.white, g); cylMesh(cx, cy + dy * 0.25, f.z2, f.z2 + 0.12, 0.19, M.white, g); } }
        break;
      case 'wc':
        boxMesh(f.x1 + 0.08, f.x2 - 0.08, f.y1 + 0.05, f.y2 - 0.05, f.z1, f.z2, M.white, g);
        boxMesh(f.x1 + 0.1, f.x2 - 0.1, f.y1 + 0.08, f.y2 - 0.08, f.z2, f.z2 + 0.03, M.white, g);
        break;
      case 'shower': boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2 + 0.01, M.tile, g); break;
      case 'glass': boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, M.glass, g).castShadow = false; break;
      case 'tub':
        boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, M.white, g);
        boxMesh(f.x1 + 0.08, f.x2 - 0.08, f.y1 + 0.08, f.y2 - 0.08, f.z2 - 0.01, f.z2 + 0.001, M.water, g);
        break;
      case 'ceiling': boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, M.liner, g); break;
      case 'hvac': boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, M.grey, g); break;
      case 'condenser':
        boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, M.grey, g);
        boxMesh(f.x1 + 0.05, f.x2 - 0.05, f.y1 + 0.05, f.y2 - 0.05, -0.55, f.z1, M.dark, g);
        // painel ripado que oculta a condensadora
        boxMesh(f.x1 - 0.12, f.x2 + 0.12, f.y1 - 0.12, f.y2 + 0.12, -0.5, f.z2 + 0.3, M.woodSlat, g);
        break;
      default:
        if (isBox) boxMesh(f.x1, f.x2, f.y1, f.y2, f.z1, f.z2, M.woodInt, g); else cylMesh(f.x, f.y, f.z1, f.z2, f.r, M.woodInt, g);
    }
  }
  return g;
}

// ---------- terreno e árvores ----------
function buildSite(cx, cy) {
  const GZ = -0.55;
  const ground = new THREE.Mesh(new THREE.CircleGeometry(220, 72), M.ground);
  ground.rotation.x = -Math.PI / 2; ground.position.set(cx, GZ - 0.01, -cy); ground.receiveShadow = true; site.add(ground);
  const gravel = new THREE.Mesh(new THREE.CircleGeometry(11.5, 64), M.gravel);
  gravel.rotation.x = -Math.PI / 2; gravel.position.set(cx, GZ, -cy); gravel.receiveShadow = true; site.add(gravel);
  const rnd = lcg(20260907);
  const trunkG = new THREE.CylinderGeometry(0.14, 0.2, 1, 8);
  const coneG = new THREE.ConeGeometry(1, 1, 9);
  const sphG = new THREE.SphereGeometry(1, 10, 8);
  for (let i = 0; i < 64; i++) {
    const ang = rnd() * Math.PI * 2, rad = 19 + rnd() * 48;
    const x = cx + Math.cos(ang) * rad, y = cy + Math.sin(ang) * rad;
    const s = 0.8 + rnd() * 1.1; const kind = rnd();
    const t = new THREE.Mesh(trunkG, M.trunk); t.scale.set(s, 2.2 * s, s); t.position.set(x, GZ + 1.1 * s, -y); t.castShadow = true; site.add(t);
    if (kind < 0.6) {
      const c1 = new THREE.Mesh(coneG, rnd() < 0.5 ? M.leaf : M.leaf2); c1.scale.set(2.2 * s, 5.5 * s, 2.2 * s); c1.position.set(x, GZ + 2.2 * s + 2.75 * s, -y); c1.castShadow = true; site.add(c1);
      const c2 = new THREE.Mesh(coneG, M.leaf); c2.scale.set(1.6 * s, 4 * s, 1.6 * s); c2.position.set(x, GZ + 2.2 * s + 5.2 * s, -y); c2.castShadow = true; site.add(c2);
    } else {
      const c = new THREE.Mesh(sphG, rnd() < 0.5 ? M.leaf : M.leaf2); c.scale.set(2.6 * s, 2.3 * s, 2.6 * s); c.position.set(x, GZ + 2.2 * s + 1.8 * s, -y); c.castShadow = true; site.add(c);
    }
  }
}
function steps(xEdge, y1, y2) { // dois degraus descendo do deck (z=0) ao terreno (-0.55), na aresta x = xEdge (deck do lado +x)
  boxMesh(xEdge - 0.3, xEdge, y1, y2, -0.55, -0.18, M.deck); boxMesh(xEdge - 0.6, xEdge - 0.3, y1, y2, -0.55, -0.36, M.deck);
}

// =====================================================================================
// ZION COCOON
// =====================================================================================
function buildCocoon() {
  BODY_CENTER = [4.9, 0];
  const S = D.shell;
  const memb = indexedMesh(S.vertices, S.membrane, M.membrane); memb.name = 'membrana';
  const glassShell = indexedMesh(S.vertices, S.glass, M.glass, null, false); glassShell.name = 'vidros_concha';
  const liner = indexedMesh(D.liner.vertices, D.liner.faces, M.liner); liner.name = 'forro'; liner.castShadow = false;
  // estrutura
  const st = new THREE.Group(); st.name = 'estrutura'; building.add(st);
  D.arches_in.forEach(a => tube(a.pts, 0.045, M.steel, false, 72, st));
  D.purlins_in.forEach(p => tube(p, 0.024, M.steel, false, 90, st));
  tube(D.front_ring, 0.05, M.steel, false, 96, st);
  D.spine_rails.forEach(p => tube(p, 0.021, M.steel, false, 40, st));
  // fachada de vidro: polígono em leque + montantes + travessa + porta pivotante
  const ring = D.glass_ring, gp = D.glass_plane;
  { const cx = [0, 0, 0]; ring.forEach(p => { cx[0] += p[0] / ring.length; cx[1] += p[1] / ring.length; cx[2] += p[2] / ring.length; });
    const verts = [cx].concat(ring); const faces = []; for (let i = 1; i < verts.length - 1; i++) faces.push([0, i, i + 1]);
    const gm = indexedMesh(verts, faces, M.glass, null, false); gm.name = 'fachada_vidro';
    tube(ring, 0.04, M.bronze, false, 96, st); }
  const xAt = z => gp.x0 - gp.k * z;
  function crossY(y) { const out = []; for (let i = 0; i < ring.length - 1; i++) { const a = ring[i], b = ring[i + 1]; if ((a[1] - y) * (b[1] - y) <= 0 && a[1] !== b[1]) { const t = (y - a[1]) / (b[1] - a[1]); out.push([a[0] + (b[0] - a[0]) * t, y, a[2] + (b[2] - a[2]) * t]); } } return out.sort((p, q) => q[2] - p[2]); }
  function crossZ(z) { const out = []; for (let i = 0; i < ring.length - 1; i++) { const a = ring[i], b = ring[i + 1]; if ((a[2] - z) * (b[2] - z) <= 0 && a[2] !== b[2]) { const t = (z - a[2]) / (b[2] - a[2]); out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, z]); } } return out.sort((p, q) => p[1] - q[1]); }
  [-1.6, -0.5, 0.5, 1.6].forEach(y => { const top = crossY(y)[0]; if (top) bar([xAt(0.02), y, 0.02], top, 0.03, M.bronze, st); });
  { const c = crossZ(2.4); if (c.length >= 2) bar(c[0], c[c.length - 1], 0.03, M.bronze, st); }
  { const y1 = 0.6, y2 = 1.6, z1 = 0.03, z2 = 2.4; const P = (y, z) => [xAt(z), y, z];
    bar(P(y1, z1), P(y1, z2), 0.02, M.bronze, st); bar(P(y2, z1), P(y2, z2), 0.02, M.bronze, st); bar(P(y1, z1), P(y2, z1), 0.02, M.bronze, st);
    bar(P(y1 + 0.12, 0.85), P(y1 + 0.12, 1.35), 0.014, M.bronze, st); }
  // janelas lente: requadro de madeira
  D.windows.forEach(w => { const t = tube(w.pts, 0.04, M.woodInt, true, 72); t.name = w.name; });
  // piso, laje e deck
  polyMesh(D.floor, 0.004, M.floor).name = 'piso';
  slabMesh(D.slab, -0.5, 0.0, M.dark).name = 'quadro_piso';
  const dk = D.deck;
  boxMesh(dk.x1, dk.x2, dk.y1, dk.y2, -0.12, 0, M.deck).name = 'deck';
  M.deck.map.repeat.set((dk.x2 - dk.x1) / 1.12, 1);
  boxMesh(dk.x1 + 0.25, dk.x2, dk.y1 + 0.25, dk.y2 - 0.25, -0.55, -0.12, M.deckSide);
  steps(dk.x1, -1.3, 1.3);
  // guarda-corpo em cabo de aço nas laterais do deck
  [[dk.y1 + 0.08], [dk.y2 - 0.08]].forEach(([y]) => { for (let x = dk.x1 + 0.1; x <= dk.x2 - 0.5; x += 1.3) bar([x, y, 0], [x, y, 1.0], 0.02, M.steel); for (const z of [0.35, 0.65, 0.98]) bar([dk.x1 + 0.1, y, z], [dk.x2 - 0.5, y, z], 0.006, M.cable); });
  // fita LED nos rodapés (indireta)
  tube(D.floor.map(p => [p[0], p[1] * 0.985, 0.06]), 0.012, M.led, true, 160).castShadow = false;
  furniture(D.furniture);
  // luzes internas quentes (2700 K) junto ao rodapé + espinha
  warmLight(2.2, 0, 0.4, 0.55, 7); warmLight(5.0, 0, 0.4, 0.55, 7); warmLight(7.6, 0, 0.4, 0.45, 5); warmLight(3.6, 0, 3.2, 0.35, 8); warmLight(0.3, 0, 2.0, 0.25, 5);
  buildSite(4.0, 0);
}

// =====================================================================================
// ZION ZENITH
// =====================================================================================
function buildZenith() {
  BODY_CENTER = [D.L / 2, 0];
  const R = D.roof;
  indexedMesh(R.vertices, R.faces, M.membrane).name = 'membrana';
  indexedMesh(R.vertices, R.oculus, M.glass, null, false).name = 'oculo_membrana';
  const liner = indexedMesh(D.liner.vertices, D.liner.faces, M.liner); liner.name = 'forro'; liner.castShadow = false;
  const st = new THREE.Group(); st.name = 'estrutura'; building.add(st);
  // mastros, coroas e anéis
  D.masts.forEach(m => cylMesh(m.x, m.y, m.z1, m.z2, m.r, M.steel, st));
  D.crowns.forEach(c => { c.arms.forEach(a => bar(a[0], a[1], 0.024, M.steel, st)); tube(c.ring, 0.04, M.steel, true, 48, st); });
  D.peaks.forEach(p => {
    if (p.oculus) { // cúpula de vidro laminado sobre o anel + poço de luz até o forro
      const Rs = (p.r * p.r + 0.15 * 0.15) / 0.3; const phi = Math.asin(p.r / Rs);
      const dome = new THREE.Mesh(new THREE.SphereGeometry(Rs, 40, 10, 0, Math.PI * 2, 0, phi), M.glass);
      dome.position.copy(Vx(p.x, p.y, p.h - (Rs - 0.15))); dome.name = 'oculo'; add(dome);
      const well = new THREE.Mesh(new THREE.CylinderGeometry(p.r, p.r, 0.34, 40, 1, true), M.woodInt); well.position.copy(Vx(p.x, p.y, p.h - 0.17)); well.material = M.woodInt.clone(); well.material.side = THREE.DoubleSide; add(shadowed(well));
    } else { // chaminé do Respiro com veneziana
      cylMesh(p.x, p.y, p.h - 0.02, p.h + 0.32, p.r * 0.92, M.woodSlat);
      cylMesh(p.x, p.y, p.h + 0.32, p.h + 0.42, p.r * 1.25, M.steel, null, p.r * 0.5);
      const grille = new THREE.Mesh(new THREE.CircleGeometry(p.r, 32), M.dark); grille.rotation.x = -Math.PI / 2; grille.position.copy(Vx(p.x, p.y, p.h - 0.3)); add(grille);
    }
  });
  // anel de beiral (tubo retangular 150 x 100) e pilares
  const hw = D.W / 2;
  boxMesh(-0.075, D.L + 0.075, -hw - 0.075, -hw + 0.075, 2.75, 2.9, M.steel, st); boxMesh(-0.075, D.L + 0.075, hw - 0.075, hw + 0.075, 2.75, 2.9, M.steel, st);
  boxMesh(-0.075, 0.075, -hw, hw, 2.75, 2.9, M.steel, st); boxMesh(D.L - 0.075, D.L + 0.075, -hw, hw, 2.75, 2.9, M.steel, st);
  D.columns.forEach(c => cylMesh(c[0], c[1], 0, 2.9, 0.05, M.steel, st));
  // postes externos inclinados 8° com estais, cabo de borda
  D.posts.forEach((p, i) => {
    const dx = p[0] - BODY_CENTER[0], dy = p[1]; const L = Math.hypot(dx, dy); const nx = dx / L, ny = dy / L;
    const top = [p[0], p[1], D.post_tops[i]]; const base = [p[0] - nx * 0.37, p[1] - ny * 0.37, -0.55];
    bar(base, top, 0.038, M.steel, st); cylMesh(base[0], base[1], -0.6, -0.5, 0.16, M.dark, st);
    bar(top, [p[0] + nx * 1.4, p[1] + ny * 1.4, -0.55], 0.006, M.cable, st);
  });
  tube(D.edge_cable, 0.012, M.cable, true, 200, st);
  // paredes
  const wood = D.walls.filter(w => w.kind === 'wood'), wins = D.walls.filter(w => w.kind === 'window'), glz = D.walls.filter(w => w.kind === 'glass');
  const T = 0.10;
  wood.forEach(w => {
    const dx = w.p2[0] - w.p1[0], dy = w.p2[1] - w.p1[1]; const L = Math.hypot(dx, dy); const ux = dx / L, uy = dy / L;
    const proj = p => (p[0] - w.p1[0]) * ux + (p[1] - w.p1[1]) * uy;
    const shape = new THREE.Shape(); shape.moveTo(0, w.z1); shape.lineTo(L, w.z1); shape.lineTo(L, w.z2); shape.lineTo(0, w.z2); shape.closePath();
    wins.forEach(o => {
      const d1 = Math.abs((o.p1[0] - w.p1[0]) * uy - (o.p1[1] - w.p1[1]) * ux); if (d1 > 1e-3) return;
      const u1 = Math.min(proj(o.p1), proj(o.p2)), u2 = Math.max(proj(o.p1), proj(o.p2)); if (u2 < 0 || u1 > L) return;
      const h = new THREE.Path(); h.moveTo(u1, o.z1); h.lineTo(u2, o.z1); h.lineTo(u2, o.z2); h.lineTo(u1, o.z2); h.closePath(); shape.holes.push(h);
      // vidro da janela no meio da espessura + requadro bronze
      rectBox(o.p1, o.p2, o.z1, o.z2, 0.02, M.glass, -T / 2).castShadow = false;
      const n = outward(o.p1, o.p2); const off = -T / 2 + 0.005;
      const q1 = [o.p1[0] + n[0] * off, o.p1[1] + n[1] * off], q2 = [o.p2[0] + n[0] * off, o.p2[1] + n[1] * off];
      rectBox(q1, q2, o.z1 - 0.03, o.z1, T, M.bronze, 0); rectBox(q1, q2, o.z2, o.z2 + 0.03, T, M.bronze, 0);
    });
    const geo = new THREE.ExtrudeGeometry(shape, { depth: T, bevelEnabled: false });
    const mat = M.woodSlat.clone(); mat.map = texSlat.clone(); mat.map.needsUpdate = true; mat.map.repeat.set(12.5, 1);
    const m = new THREE.Mesh(geo, mat); shadowed(m);
    // base: X local -> direção da parede; Y -> altura; Z -> normal (dy, -dx); painel fica no interior da linha
    const xA = new THREE.Vector3(ux, 0, -uy), yA = new THREE.Vector3(0, 1, 0), zA = new THREE.Vector3().crossVectors(xA, yA);
    const nSpec = [zA.x, -zA.z]; const o = outward(w.p1, w.p2); const inwardExtrude = (nSpec[0] * o[0] + nSpec[1] * o[1]) < 0;
    const pos = Vx(w.p1[0], w.p1[1], 0); if (!inwardExtrude) pos.addScaledVector(zA, -T);
    m.matrixAutoUpdate = false; m.matrix.makeBasis(xA, yA, zA).setPosition(pos); m.name = w.name; add(m);
  });
  glz.forEach(w => {
    rectBox(w.p1, w.p2, w.z1, w.z2, 0.024, M.glass, -0.05).castShadow = false;
    rectBox(w.p1, w.p2, w.z1, w.z1 + 0.06, 0.08, M.bronze, -0.05); rectBox(w.p1, w.p2, w.z2 - 0.06, w.z2, 0.08, M.bronze, -0.05);
    const dx = w.p2[0] - w.p1[0], dy = w.p2[1] - w.p1[1]; const L = Math.hypot(dx, dy); const n = Math.max(1, Math.round(L / 1.35));
    const nn = outward(w.p1, w.p2);
    for (let i = 0; i <= n; i++) { const t = i / n; const x = w.p1[0] + dx * t - nn[0] * 0.05, y = w.p1[1] + dy * t - nn[1] * 0.05; bar([x, y, w.z1], [x, y, w.z2], 0.03, M.bronze, st); }
  });
  // piso, laje, terraço, passarela, hidromassagem
  boxMesh(0, D.L, -hw, hw, -0.02, 0.0, M.floor).name = 'piso';
  M.floor.map.repeat.set(D.L / 1.12, 1);
  boxMesh(0, D.L, -hw, hw, -0.4, -0.02, M.dark).name = 'quadro_piso';
  const dk = D.deck, wk = D.walk;
  boxMesh(dk.x1, dk.x2, dk.y1, dk.y2, -0.12, 0, M.deck).name = 'terraco'; M.deck.map.repeat.set((dk.x2 - dk.x1) / 1.12, 1);
  boxMesh(dk.x1 + 0.25, dk.x2, dk.y1 + 0.25, dk.y2 - 0.25, -0.55, -0.12, M.deckSide);
  boxMesh(wk.x1, wk.x2, wk.y1, wk.y2, -0.12, 0, M.deck).name = 'passarela';
  boxMesh(wk.x1, wk.x2, wk.y1 + 0.1, wk.y2 - 0.1, -0.55, -0.12, M.deckSide);
  steps(dk.x1, -1.0, 1.4);
  const ht = D.hottub;
  cylMesh(ht.x, ht.y, 0, 0.8, ht.r, M.woodSlat).name = 'hidromassagem';
  cylMesh(ht.x, ht.y, 0.8, 0.86, ht.r + 0.05, M.woodInt);
  cylMesh(ht.x, ht.y, 0.7, 0.72, ht.r - 0.12, M.water).castShadow = false;
  // espreguiçadeiras e ducha externa
  [[-2.2, 0.9], [-2.2, 2.2]].forEach(([x, y]) => { boxMesh(x - 0.95, x + 0.95, y - 0.35, y + 0.35, 0.05, 0.38, M.fabric); boxMesh(x - 0.95, x - 0.35, y - 0.35, y + 0.35, 0.38, 0.75, M.fabric); });
  bar([9.0, 3.1, 0], [9.0, 3.1, 2.2], 0.025, M.steel); bar([9.0, 3.1, 2.2], [9.0, 2.75, 2.2], 0.02, M.steel);
  // fitas LED (perímetro do forro e rodapé)
  const per = [[0.15, -hw + 0.15], [D.L - 0.15, -hw + 0.15], [D.L - 0.15, hw - 0.15], [0.15, hw - 0.15]];
  tube(per.map(p => [p[0], p[1], 2.58]), 0.012, M.led, true, 32).castShadow = false;
  tube(per.map(p => [p[0], p[1], 0.05]), 0.012, M.led, true, 32).castShadow = false;
  furniture(D.furniture);
  warmLight(1.8, 0.2, 2.45, 0.55, 7); warmLight(5.0, 0, 2.5, 0.6, 8); warmLight(8.0, -0.4, 2.35, 0.45, 6); warmLight(-1.5, 0.4, 2.2, 0.35, 6); warmLight(5.0, 0, 4.6, 0.3, 6);
  buildSite(4.0, 0);
}

if (MODEL === 'cocoon') buildCocoon(); else buildZenith();

// ---------- ambiente (reflexos): cubemap de 8 bits por CubeCamera (robusto em WebGL por software) ----------
const HASH = {}; (location.hash || '').replace(/^#/, '').split('&').forEach(kv => { const [k, v] = kv.split('='); if (k) HASH[k] = v === undefined ? '1' : v; });
if (HASH.env !== '0') {
  try {
    const es = new THREE.Scene(); es.add(sky.clone());
    const eg = new THREE.Mesh(new THREE.CircleGeometry(300, 32), new THREE.MeshBasicMaterial({ color: lin(0x2c3524) })); eg.rotation.x = -Math.PI / 2; eg.position.y = -0.55; es.add(eg);
    const rt = new THREE.WebGLCubeRenderTarget(128, { format: THREE.RGBFormat, generateMipmaps: true, minFilter: THREE.LinearMipmapLinearFilter, encoding: THREE.LinearEncoding });
    const cc = new THREE.CubeCamera(0.1, 1000, rt); cc.position.set(4, 1.5, 0); es.add(cc); cc.update(renderer, es);
    scene.environment = rt.texture;
  } catch (e) { console.warn('env', e); }
}

// ---------- modos: noite / estrutura / corte ----------
const state = { night: false, structure: false, cut: false };
const clipPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0); // mantém y (projeto) <= 0
const bMats = new Set(); building.traverse(o => { if (o.material) bMats.add(o.material); });
function applyModes() {
  // noite
  if (state.night) {
    skyU.top.value.set(0x020303); skyU.mid.value.set(0x070c09); skyU.hor.value.set(0x1a1a14); skyU.sunI.value = 0.0;
    scene.fog.color.copy(lin(0x05080a)); scene.fog.near = 30; scene.fog.far = 130;
    hemi.intensity = 0.14; hemi.color.copy(lin(0x5b6f95)); sun.intensity = 0.22; sun.color.copy(lin(0x8fa6c8)); sun.position.copy(SUN_NIGHT);
    interiorLights.forEach(l => l.intensity = l.userData.iNight); M.led.color.copy(lin(0xffe2b0)); renderer.toneMappingExposure = 1.25;
  } else {
    skyU.top.value.set(0x040605); skyU.mid.value.set(0x141f18); skyU.hor.value.set(0x4a4a3a); skyU.sunI.value = 0.35;
    scene.fog.color.copy(lin(0x141c16)); scene.fog.near = 45; scene.fog.far = 190;
    hemi.intensity = 0.55; hemi.color.copy(lin(0xc6d4e2)); sun.intensity = 1.45; sun.color.copy(lin(0xfff0dc)); sun.position.copy(SUN_DAY);
    interiorLights.forEach(l => l.intensity = l.userData.iDay); M.led.color.copy(lin(0xffd9a0)); renderer.toneMappingExposure = 1.05;
  }
  skyU.sun.value.copy(sun.position).normalize();
  // estrutura
  for (const m of [M.membrane, M.liner]) { m.transparent = state.structure; m.opacity = state.structure ? 0.15 : 1.0; m.depthWrite = !state.structure; m.needsUpdate = true; }
  // corte
  bMats.forEach(m => { m.clippingPlanes = state.cut ? [clipPlane] : []; });
  document.getElementById('bNight').classList.toggle('on', state.night);
  document.getElementById('bStruct').classList.toggle('on', state.structure);
  document.getElementById('bCut').classList.toggle('on', state.cut);
}

// ---------- vistas ----------
const PRESETS = {
  cocoon: {
    ext_front: { pos: [-9.6, 7.8, 1.6], tgt: [3.2, 0.1, 1.45], fov: 42, label: 'Exterior frontal' },
    ext_side: { pos: [3.4, 14.0, 2.2], tgt: [4.6, 0, 1.5], fov: 40, label: 'Exterior lateral' },
    ext_rear: { pos: [18.0, -7.5, 2.6], tgt: [6.2, 0, 1.4], fov: 40, label: 'Exterior cauda' },
    ext_aerial: { pos: [-7.5, -11.5, 12.5], tgt: [3.6, 0, 0.3], fov: 45, label: 'Vista aérea' },
    int_living: { pos: [1.35, -0.55, 1.55], tgt: [6.4, 0.1, 1.85], fov: 66, label: 'Interior · estar' },
    int_bed: { pos: [5.75, 0.25, 1.25], tgt: [-2.0, -0.5, 1.35], fov: 66, label: 'Interior · suíte' },
    int_bath: { pos: [6.5, 1.35, 1.5], tgt: [8.8, -0.55, 0.8], fov: 70, label: 'Interior · banho' },
    night: { like: 'ext_front', night: true, label: 'Noite' },
    structure: { pos: [-8.5, 9.8, 4.8], tgt: [4.2, 0, 1.3], fov: 42, structure: true, label: 'Estrutura' },
    section: { pos: [4.7, 15.0, 3.6], tgt: [4.7, 0, 1.3], fov: 38, cut: true, label: 'Corte longitudinal' },
  },
  zenith: {
    ext_front: { pos: [-12.5, -9.5, 1.7], tgt: [3.6, 0.1, 2.3], fov: 44, label: 'Exterior frontal' },
    ext_side: { pos: [2.5, -16.0, 2.4], tgt: [4.6, 0, 2.3], fov: 40, label: 'Exterior lateral' },
    ext_rear: { pos: [20.5, 8.5, 3.0], tgt: [6.0, 0, 2.3], fov: 40, label: 'Exterior fundos' },
    ext_aerial: { pos: [-9.5, -12.5, 13.5], tgt: [4.0, 0, 1.0], fov: 45, label: 'Vista aérea' },
    int_living: { pos: [0.5, -0.7, 1.3], tgt: [5.6, 0.3, 3.1], fov: 76, label: 'Interior · estar' },
    int_bed: { pos: [5.9, 0.0, 1.2], tgt: [-2.5, -0.7, 1.3], fov: 66, label: 'Interior · suíte' },
    int_bath: { pos: [6.6, 2.15, 1.5], tgt: [9.2, -0.7, 0.85], fov: 68, label: 'Interior · banho' },
    night: { like: 'ext_front', night: true, label: 'Noite' },
    structure: { pos: [-10.5, 10.5, 5.5], tgt: [4.6, 0, 2.2], fov: 42, structure: true, label: 'Estrutura' },
    section: { pos: [4.7, 16.0, 3.4], tgt: [4.7, 0, 1.7], fov: 38, cut: true, label: 'Corte longitudinal' },
  }
}[MODEL];

function setView(name) {
  let p = PRESETS[name]; if (!p) { console.warn('vista desconhecida', name); return false; }
  const base = p.like ? PRESETS[p.like] : p;
  camera.position.copy(Vx(base.pos[0], base.pos[1], base.pos[2]));
  controls.target.copy(Vx(base.tgt[0], base.tgt[1], base.tgt[2]));
  camera.fov = base.fov || 45; camera.updateProjectionMatrix();
  state.night = !!p.night; state.structure = !!p.structure; state.cut = !!p.cut;
  applyModes(); controls.update();
  document.getElementById('views').value = name;
  return true;
}
window.setView = setView;

// UI
const sel = document.getElementById('views');
Object.keys(PRESETS).forEach(k => { const o = document.createElement('option'); o.value = k; o.textContent = PRESETS[k].label; sel.appendChild(o); });
sel.addEventListener('change', () => setView(sel.value));
document.querySelectorAll('.bar button[data-view]').forEach(b => b.addEventListener('click', () => setView(b.dataset.view)));
document.getElementById('bNight').addEventListener('click', () => { state.night = !state.night; applyModes(); });
document.getElementById('bStruct').addEventListener('click', () => { state.structure = !state.structure; applyModes(); });
document.getElementById('bCut').addEventListener('click', () => { state.cut = !state.cut; applyModes(); });
function fromHash() { const m = /view=([a-z_]+)/i.exec(location.hash || ''); if (!(m && setView(m[1]))) setView('ext_front'); }
window.addEventListener('hashchange', fromHash);
window.addEventListener('resize', () => { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight); });

// GLB de toda a edificação (sem terreno / árvores)
window.exportGLB = function () {
  return new Promise((resolve, reject) => {
    try {
      const saved = { op: M.glass.opacity, cut: state.cut }; M.glass.opacity = 0.35; bMats.forEach(m => { m.clippingPlanes = []; });
      new THREE.GLTFExporter().parse(building, buf => { M.glass.opacity = saved.op; state.cut = saved.cut; applyModes(); resolve(buf); }, { binary: true, truncateDrawRange: true, embedImages: true });
    } catch (e) { reject(e); }
  });
};

fromHash();
let first = true;
function loop() {
  controls.update();
  renderer.render(scene, camera);
  window.frameCount++;
  if (first) { first = false; document.getElementById('load').classList.add('off'); window.sceneReady = true; }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""


def libs_block(cdn):
    if cdn:
        return "\n".join('<script src="%s"></script>' % CDN[k] for k in ("three", "orbit", "gltf"))
    out = []
    for k in ("three", "orbit", "gltf"):
        with open(VENDOR[k], "r", encoding="utf-8") as fh:
            src = fh.read()
        out.append("<script>/* %s (three r128, embutido) */\n%s\n</script>" % (os.path.basename(VENDOR[k]), src))
    return "\n".join(out)


def build_html(model, data, title, subtitle, cdn):
    js = json.dumps(rnd(data), separators=(",", ":"), sort_keys=True, ensure_ascii=False)
    js = js.replace("</", "<\\/")
    html = HTML
    html = html.replace("__LIBS__", libs_block(cdn))
    html = html.replace("__DATA_SCRIPT__", "window.ZION_DATA = %s;" % js)
    html = html.replace("__MODEL__", model).replace("__TITLE__", title).replace("__SUBTITLE__", subtitle)
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-json", default=None, help="pasta para os JSON de geometria (padrão: $ZION_SCRATCH ou ./build)")
    ap.add_argument("--cdn", action="store_true", help="usar cdnjs em vez de embutir tools/vendor/*.js")
    args = ap.parse_args()
    out_json = args.out_json or os.environ.get("ZION_SCRATCH") or os.path.join(HERE, "build")
    os.makedirs(out_json, exist_ok=True)

    cdn = args.cdn or not all(os.path.exists(v) for v in VENDOR.values())
    if cdn and not args.cdn:
        print("aviso: tools/vendor/ incompleto; a usar cdnjs")

    models = [
        ("cocoon", cocoon_data(), "ZION COCOON", "Cabana biomórfica em casulo · 41 m² internos + deck 26 m²",
         os.path.join(PROJECT, "cocoon", "3d", "zion-cocoon-3d.html")),
        ("zenith", zenith_data(), "ZION ZENITH", "Cabana escultural de dois cumes · 48 m² internos + terraço 20 m²",
         os.path.join(PROJECT, "zenith", "3d", "zion-zenith-3d.html")),
    ]
    for model, data, title, subtitle, out_html in models:
        jpath = os.path.join(out_json, "%s_geometry.json" % model)
        with open(jpath, "w", encoding="utf-8") as fh:
            json.dump(rnd(data), fh, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        os.makedirs(os.path.dirname(out_html), exist_ok=True)
        html = build_html(model, data, title, subtitle, cdn)
        with open(out_html, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("%-40s %7.0f kB   (json %s, %.0f kB)" % (os.path.relpath(out_html, PROJECT), len(html.encode("utf-8")) / 1024, os.path.basename(jpath), os.path.getsize(jpath) / 1024))


if __name__ == "__main__":
    main()
