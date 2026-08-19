/* =============================================================================
   ZION · SITE GENERATOR
   Plugin de Figma que desenha o site institucional da Zion Hotel Group
   International dentro do arquivo: design system (cores, tipografia,
   componentes) + páginas em Desktop 1440 e Mobile 390.

   Tudo é auto-layout nativo e 100% editável. Nenhuma imagem é embutida:
   os fundos territoriais são vetores reais (as mesmas curvas do site).
   ============================================================================= */

/* ----------------------------------------------------------------------------
   1. TOKENS
   -------------------------------------------------------------------------- */

var C = {
  black: '#040605',
  green: '#1B2117',
  cream: '#FEF5F0',
  sand:  '#DED6BF',
  earth: '#8B714E'
};

var PALETTE = [
  { key: 'black', name: 'Zion Black', hex: C.black, uso: 'Fundo padrão · 80% do site' },
  { key: 'green', name: 'Zion Green', hex: C.green, uso: 'Texto sobre fundo claro' },
  { key: 'cream', name: 'Zion Cream', hex: C.cream, uso: 'Texto sobre fundo escuro · seções claras' },
  { key: 'sand',  name: 'Zion Sand',  hex: C.sand,  uso: 'Labels, acentos, divisores' },
  { key: 'earth', name: 'Zion Earth', hex: C.earth, uso: 'CTAs, numerais, destaques' }
];

/* Pilhas de fonte: a primeira que existir no Figma é usada.
   Aventa é fonte comercial (Fontfabric); se não estiver instalada,
   cai para DM Sans / Outfit, exatamente como o fallback do CSS do site. */
var STACK_SERIF = ['Cormorant Garamond', 'Cormorant', 'EB Garamond', 'Playfair Display', 'Georgia', 'Times New Roman'];
var STACK_SANS  = ['Aventa', 'DM Sans', 'Outfit', 'Jost', 'Inter', 'Roboto', 'Arial'];

var WEIGHT_STYLES = {
  200: ['ExtraLight', 'Extra Light', 'Thin', 'Light', 'Book', 'Regular'],
  300: ['Light', 'Book', 'ExtraLight', 'Extra Light', 'Thin', 'Regular'],
  400: ['Regular', 'Book', 'Normal', 'Medium', 'Light'],
  500: ['Medium', 'Regular', 'SemiBold', 'Semi Bold', 'Book'],
  600: ['SemiBold', 'Semi Bold', 'Bold', 'Medium', 'Regular'],
  700: ['Bold', 'SemiBold', 'Semi Bold', 'Medium', 'Regular']
};

var AVAILABLE = null;   // Map<family, Set<style>>
var SERIF = 'Inter';
var SANS  = 'Inter';
var PAINT = {};         // hex -> PaintStyle

/* ----------------------------------------------------------------------------
   2. HELPERS BÁSICOS
   -------------------------------------------------------------------------- */

function hexToRgb(hex) {
  var h = hex.replace('#', '');
  return {
    r: parseInt(h.substring(0, 2), 16) / 255,
    g: parseInt(h.substring(2, 4), 16) / 255,
    b: parseInt(h.substring(4, 6), 16) / 255
  };
}

function solid(hex, opacity) {
  return { type: 'SOLID', color: hexToRgb(hex), opacity: opacity === undefined ? 1 : opacity };
}

/* Aplica cor. Quando a cor é chapada e faz parte da paleta, amarra ao estilo. */
function fill(node, hex, opacity) {
  node.fills = [solid(hex, opacity)];
  if ((opacity === undefined || opacity === 1) && PAINT[hex]) {
    try { node.fillStyleId = PAINT[hex].id; } catch (e) { /* segue com a cor crua */ }
  }
}

function stroke(node, hex, opacity, weight) {
  node.strokes = [solid(hex, opacity === undefined ? 1 : opacity)];
  node.strokeWeight = weight === undefined ? 1 : weight;
  node.strokeAlign = 'INSIDE';
}

/* Borda em lados específicos: sides = {top:1, bottom:1, left:0, right:0} */
function sideStroke(node, hex, opacity, sides) {
  stroke(node, hex, opacity, 1);
  try {
    node.strokeTopWeight    = sides.top    ? 1 : 0;
    node.strokeBottomWeight = sides.bottom ? 1 : 0;
    node.strokeLeftWeight   = sides.left   ? 1 : 0;
    node.strokeRightWeight  = sides.right  ? 1 : 0;
  } catch (e) { /* versões antigas do editor: mantém borda completa */ }
}

/* clamp() do CSS traduzido para o Figma: clamp(min, Xvw, max) num frame de W px */
function cl(min, vw, max, W) {
  return Math.round(Math.min(Math.max(min, (vw / 100) * W), max));
}

function isMobile(W) { return W < 700; }

/* Escala de espaçamento vertical entre desktop e mobile */
function sp(W, v) { return isMobile(W) ? Math.round(v * 0.6) : Math.round(v); }

/* padding lateral do .wrap (max-width 1140) e do .narrow (max-width 760) */
function padX(W, maxW) {
  var mw = maxW || 1140;
  return Math.max(Math.round(W * 0.06), Math.round((W - mw) / 2));
}

/* Largura útil do conteúdo dentro do wrap */
function inner(W, maxW) { return W - 2 * padX(W, maxW); }

/* ----------------------------------------------------------------------------
   3. FONTES
   -------------------------------------------------------------------------- */

function pickFamily(stack) {
  for (var i = 0; i < stack.length; i++) {
    if (AVAILABLE.has(stack[i])) return stack[i];
  }
  return 'Inter';
}

function pickStyle(family, weight, italic) {
  var styles = AVAILABLE.get(family) || new Set(['Regular']);
  var base = WEIGHT_STYLES[weight] || WEIGHT_STYLES[400];
  var cands = [];
  var i;
  if (italic) {
    for (i = 0; i < base.length; i++) {
      cands.push(base[i] === 'Regular' ? 'Italic' : base[i] + ' Italic');
    }
    cands.push('Italic', 'Light Italic', 'Medium Italic', 'Regular Italic');
  }
  for (i = 0; i < base.length; i++) cands.push(base[i]);
  cands.push('Regular', 'Medium', 'Book');
  for (i = 0; i < cands.length; i++) {
    if (styles.has(cands[i])) return cands[i];
  }
  var arr = Array.from(styles);
  return arr[0] || 'Regular';
}

var FONT_CACHE = {};
function fontOf(family, weight, italic) {
  var key = family + '|' + weight + '|' + (italic ? 'i' : 'n');
  if (!FONT_CACHE[key]) FONT_CACHE[key] = { family: family, style: pickStyle(family, weight, italic) };
  return FONT_CACHE[key];
}

async function loadFonts() {
  var list = await figma.listAvailableFontsAsync();
  AVAILABLE = new Map();
  for (var i = 0; i < list.length; i++) {
    var fn = list[i].fontName;
    if (!AVAILABLE.has(fn.family)) AVAILABLE.set(fn.family, new Set());
    AVAILABLE.get(fn.family).add(fn.style);
  }
  SERIF = pickFamily(STACK_SERIF);
  SANS  = pickFamily(STACK_SANS);

  var weights = [200, 300, 400, 500, 600, 700];
  var wanted = {};
  var fams = [SERIF, SANS];
  for (var f = 0; f < fams.length; f++) {
    for (var w = 0; w < weights.length; w++) {
      for (var it = 0; it < 2; it++) {
        var fn2 = fontOf(fams[f], weights[w], it === 1);
        wanted[fn2.family + '||' + fn2.style] = fn2;
      }
    }
  }
  var jobs = [];
  Object.keys(wanted).forEach(function (k) { jobs.push(figma.loadFontAsync(wanted[k])); });
  await Promise.all(jobs);
  return { serif: SERIF, sans: SANS };
}

/* ----------------------------------------------------------------------------
   4. NÓS
   -------------------------------------------------------------------------- */

/* Frame com auto-layout.
   o = { dir:'V'|'H'|'NONE', w, h, bg, bgOpacity, gap, pad | padY/padX | padT/padR/padB/padL,
         main:'MIN'|'CENTER'|'MAX'|'SPACE_BETWEEN', cross:'MIN'|'CENTER'|'MAX', wrap, clip } */
function F(name, o) {
  o = o || {};
  var f = figma.createFrame();
  f.name = name;
  f.fills = [];
  if (o.dir !== 'NONE') {
    f.layoutMode = o.dir === 'H' ? 'HORIZONTAL' : 'VERTICAL';
    f.primaryAxisSizingMode = 'AUTO';
    f.counterAxisSizingMode = 'AUTO';
    f.itemSpacing = o.gap || 0;
    f.primaryAxisAlignItems = o.main || 'MIN';
    f.counterAxisAlignItems = o.cross || 'MIN';
    if (o.wrap) { try { f.layoutWrap = 'WRAP'; } catch (e) {} }
  }
  var pt = o.padT !== undefined ? o.padT : (o.padY !== undefined ? o.padY : (o.pad || 0));
  var pb = o.padB !== undefined ? o.padB : (o.padY !== undefined ? o.padY : (o.pad || 0));
  var pl = o.padL !== undefined ? o.padL : (o.padX !== undefined ? o.padX : (o.pad || 0));
  var pr = o.padR !== undefined ? o.padR : (o.padX !== undefined ? o.padX : (o.pad || 0));
  f.paddingTop = pt; f.paddingBottom = pb; f.paddingLeft = pl; f.paddingRight = pr;
  if (o.bg) fill(f, o.bg, o.bgOpacity);
  if (o.w) {
    if (o.dir === 'H') f.primaryAxisSizingMode = 'FIXED'; else f.counterAxisSizingMode = 'FIXED';
    f.resize(o.w, o.h || Math.max(f.height, 1));
  }
  if (o.h) {
    if (o.dir === 'H') f.counterAxisSizingMode = 'FIXED'; else f.primaryAxisSizingMode = 'FIXED';
    f.resize(o.w || Math.max(f.width, 1), o.h);
  }
  f.clipsContent = o.clip === undefined ? false : o.clip;
  return f;
}

/* Anexa um nó e opcionalmente manda preencher a largura do pai */
function add(parent, node, fillW) {
  parent.appendChild(node);
  if (fillW) {
    try { node.layoutSizingHorizontal = 'FILL'; } catch (e) {}
  }
  return node;
}

/* Marca ranges de itálico: "texto com *ênfase* aqui" */
function parseEm(str) {
  var out = '';
  var ranges = [];
  var open = -1;
  for (var i = 0; i < str.length; i++) {
    var ch = str.charAt(i);
    if (ch === '*') {
      if (open < 0) open = out.length;
      else { ranges.push([open, out.length]); open = -1; }
    } else {
      out += ch;
    }
  }
  return { text: out, ranges: ranges };
}

/* Texto.
   o = { serif, w, italic, size, lh, ls, color, opacity, align, upper, maxW, name } */
function T(str, o) {
  o = o || {};
  var fam = o.serif ? SERIF : SANS;
  var weight = o.w || 400;
  var base = fontOf(fam, weight, !!o.italic);
  var t = figma.createText();
  t.fontName = base;
  var parsed = parseEm(str);
  t.characters = parsed.text;
  /* caixa alta como propriedade, não como conteúdo: o texto continua editável
     na forma original e o estilo tipográfico continua aplicável */
  if (o.upper) t.textCase = 'UPPER';
  if (parsed.ranges.length) {
    var em = fontOf(fam, weight, !o.italic);
    for (var i = 0; i < parsed.ranges.length; i++) {
      t.setRangeFontName(parsed.ranges[i][0], parsed.ranges[i][1], em);
    }
  }
  t.fontSize = o.size || 14;
  if (o.lh) t.lineHeight = { value: Math.round(o.lh * 100), unit: 'PERCENT' };
  if (o.ls) t.letterSpacing = { value: o.ls * 100, unit: 'PERCENT' };
  t.textAlignHorizontal = o.align || 'LEFT';
  fill(t, o.color || C.cream, o.opacity);
  t.textAutoResize = 'WIDTH_AND_HEIGHT';
  if (o.maxW) {
    t.textAutoResize = 'HEIGHT';
    t.resize(o.maxW, t.height);
  }
  t.name = o.name || (parsed.text.length > 34 ? parsed.text.substring(0, 34) + '…' : parsed.text);
  return t;
}

/* Reescreve o conteúdo de um nó de texto (inclusive dentro de instância),
   preservando os itálicos marcados com * */
function setRich(node, str) {
  var parsed = parseEm(str);
  var fam = node.fontName && node.fontName.family ? node.fontName.family : SANS;
  var current = node.fontName;
  node.characters = parsed.text;
  if (parsed.ranges.length && current && current.style) {
    var italic = current.style.indexOf('Italic') >= 0;
    var weight = current.style.indexOf('Light') >= 0 ? 300
               : current.style.indexOf('Medium') >= 0 ? 500
               : current.style.indexOf('Bold') >= 0 ? 700 : 400;
    var alt = fontOf(fam, weight, !italic);
    for (var i = 0; i < parsed.ranges.length; i++) {
      node.setRangeFontName(parsed.ranges[i][0], parsed.ranges[i][1], alt);
    }
  }
}

/* Sobrescreve um texto dentro de uma instância, pelo nome da camada */
function ov(instance, layerName, value) {
  var node = instance.findOne(function (n) { return n.name === layerName && n.type === 'TEXT'; });
  if (node) setRich(node, value);
  return node;
}

/* Filete horizontal */
function rule(hex, opacity, h) {
  var r = figma.createRectangle();
  r.name = 'Filete';
  r.resize(100, h || 1);
  fill(r, hex, opacity);
  return r;
}

/* Espaçador vertical */
function gapBox(h) {
  var r = figma.createRectangle();
  r.name = 'Espaço';
  r.resize(1, h);
  r.fills = [];
  return r;
}

/* Linhas topográficas — os mesmos paths do site, como vetor de verdade */
var TERRAIN_HERO =
  '<path d="M-90,620 C220,560 380,660 620,600 S1050,520 1530,600"/>' +
  '<path d="M-90,660 C240,600 400,700 640,640 S1070,560 1530,640"/>' +
  '<path d="M-90,700 C260,645 420,740 660,680 S1090,605 1530,680"/>' +
  '<path d="M-90,580 C200,520 360,615 600,560 S1030,480 1530,560"/>' +
  '<path d="M-90,540 C180,485 340,570 580,520 S1010,445 1530,520"/>' +
  '<path d="M-90,745 C280,690 440,780 680,725 S1110,650 1530,725"/>' +
  '<path d="M-90,160 C300,220 500,120 780,180 S1200,260 1530,180" opacity=".55"/>' +
  '<path d="M-90,120 C280,180 480,85 760,140 S1180,215 1530,140" opacity=".55"/>' +
  '<path d="M-90,200 C320,255 520,160 800,215 S1220,300 1530,220" opacity=".55"/>';

var TERRAIN_BAND =
  '<path d="M-90,300 C240,240 420,360 700,300 S1150,220 1530,300"/>' +
  '<path d="M-90,350 C260,290 440,410 720,350 S1170,270 1530,350"/>' +
  '<path d="M-90,400 C280,340 460,460 740,400 S1190,320 1530,400"/>' +
  '<path d="M-90,250 C220,195 400,305 680,250 S1130,175 1530,250"/>' +
  '<path d="M-90,200 C200,150 380,255 660,200 S1110,130 1530,200"/>' +
  '<path d="M-90,450 C300,395 480,505 760,450 S1210,375 1530,450"/>' +
  '<path d="M-90,150 C180,105 360,205 640,150 S1090,85 1530,150"/>';

var TERRAIN_FINAL =
  '<path d="M-90,520 C260,460 460,580 740,520 S1190,440 1530,520"/>' +
  '<path d="M-90,570 C280,515 480,625 760,570 S1210,495 1530,570"/>' +
  '<path d="M-90,470 C240,415 440,525 720,470 S1170,395 1530,470"/>' +
  '<path d="M-90,620 C300,565 500,675 780,620 S1230,545 1530,620"/>' +
  '<path d="M-90,130 C280,185 480,90 760,145 S1180,220 1530,145" opacity=".6"/>' +
  '<path d="M-90,90 C260,145 460,55 740,105 S1160,180 1530,105" opacity=".6"/>';

function terrain(paths, vbW, vbH, w, h, opacity) {
  var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + Math.round(w) + '" height="' + Math.round(h) +
            '" viewBox="0 0 ' + vbW + ' ' + vbH + '" preserveAspectRatio="none">' +
            '<g fill="none" stroke="' + C.sand + '" stroke-width="1" opacity="' + opacity + '">' +
            paths + '</g></svg>';
  var node = figma.createNodeFromSvg(svg);
  node.name = 'Linhas Topográficas';
  node.fills = [];
  try { node.resize(Math.round(w), Math.round(h)); } catch (e) {}
  return node;
}

/* Coloca o vetor territorial como fundo absoluto de um frame já montado */
function backdrop(frame, paths, vbH, opacity) {
  var t = terrain(paths, 1440, vbH, frame.width, frame.height, opacity);
  frame.insertChild(0, t);
  try {
    t.layoutPositioning = 'ABSOLUTE';
    t.x = 0; t.y = 0;
    t.constraints = { horizontal: 'STRETCH', vertical: 'STRETCH' };
  } catch (e) {}
  frame.clipsContent = true;
  return t;
}

/* Transforma um frame montado em Component, preservando o auto-layout */
var COPY_PROPS = ['layoutMode', 'primaryAxisSizingMode', 'counterAxisSizingMode',
  'primaryAxisAlignItems', 'counterAxisAlignItems', 'itemSpacing', 'layoutWrap',
  'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
  'clipsContent', 'fills', 'fillStyleId', 'strokes', 'strokeAlign', 'strokeWeight',
  'strokeTopWeight', 'strokeBottomWeight', 'strokeLeftWeight', 'strokeRightWeight',
  'cornerRadius', 'opacity'];

function asComponent(frame, name, description) {
  var c = figma.createComponent();
  c.name = name;
  if (description) c.description = description;
  if (frame.layoutMode !== 'NONE') c.layoutMode = frame.layoutMode;
  for (var i = 0; i < COPY_PROPS.length; i++) {
    var k = COPY_PROPS[i];
    try {
      var v = frame[k];
      if (v !== undefined && v !== figma.mixed) c[k] = v;
    } catch (e) {}
  }
  var w = frame.width, h = frame.height;
  var kids = frame.children.slice();
  for (var j = 0; j < kids.length; j++) c.appendChild(kids[j]);
  try {
    if (frame.primaryAxisSizingMode === 'FIXED' || frame.counterAxisSizingMode === 'FIXED') c.resize(w, h);
  } catch (e) {}
  frame.remove();
  return c;
}

/* ----------------------------------------------------------------------------
   5. DESIGN SYSTEM: estilos de cor e de texto
   -------------------------------------------------------------------------- */

function buildColorStyles() {
  var collection = null, modeId = null;
  try {
    collection = figma.variables.createVariableCollection('Zion · Cores');
    modeId = collection.modes[0].modeId;
  } catch (e) { collection = null; }

  PALETTE.forEach(function (p) {
    var style = figma.createPaintStyle();
    style.name = 'Zion/' + p.name;
    style.description = p.uso + ' · ' + p.hex;
    var paint = solid(p.hex);
    if (collection) {
      try {
        var v = figma.variables.createVariable(p.name, collection, 'COLOR');
        v.setValueForMode(modeId, hexToRgb(p.hex));
        paint = figma.variables.setBoundVariableForPaint(paint, 'color', v);
      } catch (e) {}
    }
    style.paints = [paint];
    PAINT[p.hex] = style;
  });
}

var TEXT_SPECS = [
  { name: 'Display/Hero',        serif: true,  w: 300, size: 110, lh: 1.12, ls: 0.01, sample: 'Desenvolvemos destinos.' },
  { name: 'Display/H2 Seção',    serif: true,  w: 300, size: 58,  lh: 1.25, ls: 0.01, sample: 'Um grupo. Três formas de criar valor.' },
  { name: 'Display/H3 Bloco',    serif: true,  w: 400, size: 28,  lh: 1.3,  ls: 0.02, sample: 'Zion Hotel Development' },
  { name: 'Display/Citação',     serif: true,  w: 300, size: 40,  lh: 1.6,  ls: 0,    italic: true, sample: 'A terra já sabe o que quer ser.' },
  { name: 'Display/Numeral',     serif: true,  w: 300, size: 60,  lh: 1.1,  ls: 0.02, sample: 'R$ 1.571' },
  { name: 'Texto/Corpo',         serif: false, w: 300, size: 14.5, lh: 2.2, ls: 0,    sample: 'O projeto nasce do território e da tese financeira.' },
  { name: 'Texto/Apoio',         serif: false, w: 300, size: 13,  lh: 2,    ls: 0,    sample: 'Texto de apoio das listas e células.' },
  { name: 'Rótulo/Overline',     serif: false, w: 300, size: 10.5, lh: 1.9, ls: 0.34, upper: true, sample: 'Zion Hotel Group International' },
  { name: 'Rótulo/Splitword',    serif: false, w: 200, size: 16,  lh: 1.6,  ls: 0.5,  upper: true, sample: 'Modalidades' },
  { name: 'Rótulo/Botão',        serif: false, w: 400, size: 10.5, lh: 1.6, ls: 0.34, upper: true, sample: 'Solicitar Diagnóstico' },
  { name: 'Rótulo/Nav',          serif: false, w: 300, size: 10.5, lh: 1.6, ls: 0.26, upper: true, sample: 'Modalidades' }
];

function buildTextStyles() {
  var out = {};
  TEXT_SPECS.forEach(function (s) {
    var st = figma.createTextStyle();
    st.name = 'Zion/' + s.name;
    st.fontName = fontOf(s.serif ? SERIF : SANS, s.w, !!s.italic);
    st.fontSize = s.size;
    st.lineHeight = { value: Math.round(s.lh * 100), unit: 'PERCENT' };
    st.letterSpacing = { value: s.ls * 100, unit: 'PERCENT' };
    if (s.upper) st.textCase = 'UPPER';
    st.description = (s.serif ? SERIF : SANS) + ' · ' + s.w + ' · ' + s.size + 'px';
    out[s.name] = st;
  });
  return out;
}

/* ----------------------------------------------------------------------------
   6. PEÇAS DE TEXTO RECORRENTES
   -------------------------------------------------------------------------- */

function label(str, W, color) {
  return T(str, { w: 300, size: isMobile(W) ? 9.5 : 10.5, lh: 1.9, ls: 0.34,
                  upper: true, color: color || C.sand, name: 'Rótulo' });
}

/* .splitword — palavra em caps ligada por filete, marca editorial da Zion */
function splitword(word, W, dark, centered) {
  var row = F('Splitword', { dir: 'H', gap: 24, cross: 'CENTER', w: inner(W) });
  var color = dark ? C.sand : C.earth;
  var lineColor = dark ? C.cream : C.green;
  var lineOpacity = dark ? 0.3 : 0.35;
  if (centered) {
    var l0 = add(row, rule(lineColor, lineOpacity));
    l0.layoutGrow = 1;
  }
  add(row, T(word, { w: 200, size: cl(13, 1.4, 16, W), ls: 0.5, upper: true, color: color, name: 'Palavra' }));
  var l = add(row, rule(lineColor, lineOpacity));
  l.layoutGrow = 1;
  return row;
}

/* Cabeçalho de seção: splitword + H2 com ênfase em itálico */
function secHead(word, h2, W, dark, opts) {
  opts = opts || {};
  var box = F('Cabeçalho de Seção', { dir: 'V', gap: 26, w: inner(W, opts.maxW) });
  add(box, splitword(word, W, dark, opts.centered), true);
  if (h2) {
    var t = T(h2, {
      serif: true, w: 300, size: cl(32, 4.6, opts.big ? 58 : 54, W), lh: 1.25, ls: 0.01,
      color: dark ? C.cream : C.green, name: 'Título'
    });
    add(box, t, true);
    if (opts.centered) t.textAlignHorizontal = 'CENTER';
  }
  return box;
}

/* Seção base já com padding do .wrap */
function section(name, W, o) {
  o = o || {};
  var f = F(name, {
    dir: 'V',
    w: W,
    gap: o.gap === undefined ? sp(W, 88) : o.gap,
    bg: o.bg,
    padY: o.padY === undefined ? sp(W, 150) : o.padY,
    padX: padX(W, o.maxW),
    cross: o.cross || 'MIN'
  });
  return f;
}

/* ----------------------------------------------------------------------------
   7. CONTEÚDO (copy real do site em docs/)
   -------------------------------------------------------------------------- */

var NAV_HOME = ['Modalidades', 'Jornada', 'Ecossistema', 'Método', 'Projetos', 'Founder'];
var NAV_INTERNA = ['Development', 'Management', 'Collection', 'Ecossistema', 'Founder'];

var STATS = [
  { num: 'R$ 1.571', desc: 'Diária média validada em operação própria' },
  { num: '43%',      desc: 'Margem EBITDA em hospitalidade boutique' },
  { num: '05',       desc: 'Destinos em desenvolvimento simultâneo' },
  { num: '11',       desc: 'Unidades de negócio no ecossistema' }
];

var MODALIDADES = [
  {
    num: 'Modalidade 01', titulo: 'Zion Hotel Development',
    forwho: 'Para quem tem um território e quer transformá-lo em um ativo que gera receita e valoriza.',
    paras: [
      'A origem de tudo. Desenvolvimento imobiliário turístico completo: leitura territorial, estudo de viabilidade, concepção de produto, master plan, estruturação societária e captação de investidores. O projeto nasce do território e da tese financeira, nunca do palpite.',
      'Você entra com a terra e a visão. A Zion entra com o método, a marca e o acesso ao capital. No final, não existe "um hotel construído": existe um ativo estruturado, com tese, governança e caminho de saída.'
    ],
    quote: '"O ativo se transforma em resultado."',
    ctas: [{ t: 'Tenho um território', solid: false }, { t: 'Explorar a Modalidade', solid: false }],
    specs: [
      ['Diagnóstico', 'Zion Score™ e leitura territorial'],
      ['Viabilidade', 'Mercadológica e econômico-financeira'],
      ['Produto', 'Conceito, posicionamento e master plan'],
      ['Estrutura', 'SPE, governança e proteção patrimonial'],
      ['Captação', 'Tese, teaser, info memo e pitch'],
      ['Implantação', 'Governança de obra e milestones']
    ]
  },
  {
    num: 'Modalidade 02', titulo: 'Zion Hotel Management',
    forwho: 'Para quem tem um ativo pronto ou em operação e precisa que ele performe como investimento.',
    paras: [
      'O ativo pronto precisa performar. A Zion Hotel Management assume a operação com governança, controle de padrão e gestão de performance: jornada do hóspede, revenue management, SOPs, time treinado e relatórios periódicos para os investidores do ativo.',
      'A diferença entre um hotel que sobrevive e um ativo que performa está na disciplina da operação. Quem opera com método defende a diária, protege a margem e entrega o resultado que a tese prometeu.'
    ],
    quote: '"Consistência, controle e escalabilidade."',
    ctas: [{ t: 'Tenho um ativo operando', solid: false }, { t: 'Explorar a Modalidade', solid: false }],
    specs: [
      ['Operação', 'Gestão hoteleira completa do ativo'],
      ['Performance', 'Revenue, ADR, ocupação e GOP'],
      ['Padrão', 'SOPs, treinamento e experiência premium'],
      ['Governança', 'Relatórios e aderência à tese'],
      ['Hóspede', 'Jornada e hospitalidade experiencial']
    ]
  },
  {
    num: 'Modalidade 03', titulo: 'Zion Collection',
    forwho: 'Para projetos que querem carregar uma bandeira com padrão, curadoria e tese validada.',
    paras: [
      'A bandeira do grupo. Apenas projetos homologados carregam o selo Zion Collection: curadoria de destinos com identidade, padrão de experiência e tese validada. Cinco coleções, cada uma com vocação territorial própria.',
      'Uma bandeira não é um logotipo na fachada. É acesso a padrão, distribuição, comunidade de investidores e uma promessa que o hóspede reconhece antes de chegar. Por isso a homologação existe: o selo só vale porque nem todo projeto o recebe.'
    ],
    quote: '"A marca não é alugada. Ela é validada."',
    ctas: [{ t: 'Quero a bandeira', solid: false }, { t: 'Explorar a Modalidade', solid: false }],
    specs: [
      ['Bubble Collection', 'Glamping imersivo e contemplação'],
      ['Mountain Collection', 'Serra, clima frio e refúgios de altitude'],
      ['Beach Collection', 'Litoral premium e vida ao mar'],
      ['Wellness Collection', 'Regeneração, biofilia e bem-estar'],
      ['Signature Collection', 'Ativos únicos e icônicos por natureza']
    ]
  }
];

var JORNADA = [
  ['A terra *parada*', 'Um território com potencial enorme e nenhuma estrutura. Cada ano nesse estado é receita que não volta. É aqui que quase todos os projetos morrem: não por falta de potencial, por falta de método.'],
  ['O *diagnóstico*', 'O Zion Score™ lê a vocação do território e responde com um número de 0 a 10 se ele sustenta uma tese de destino. Sem achismo: mercado emissor, ADR de referência, CAPEX orientativo e concorrência.'],
  ['A *tese*', 'Viabilidade mercadológica e financeira em três cenários. O projeto ganha produto, posicionamento, master plan e uma tese que se sustenta na frente de qualquer investidor.'],
  ['A *estrutura*', 'SPE, governança, proteção patrimonial e desenho societário. O terreno deixa de ser um bem pessoal e vira um veículo de investimento pronto para receber capital.'],
  ['O *capital*', 'Teaser, information memorandum e pitch institucional na frente do investidor certo. O ativo bem estruturado atrai o capital. A ordem é essa, não o contrário.'],
  ['O *destino*', 'Implantação com governança e operação Zion Management. O território que estava parado agora recebe hóspedes, gera receita operacional e valoriza como patrimônio. E pode carregar a bandeira.']
];

var ECOSSISTEMA = [
  ['Zion Bubble Glamping', 'A operação pioneira do grupo em Florianópolis. Laboratório vivo da marca: benchmarks reais de ADR, ocupação e margem que alimentam todos os estudos de viabilidade.'],
  ['Zion Advisory', 'Consultoria estratégica para terrenistas, investidores e operadores. Diagnóstico, estruturação e direcionamento de ativos turísticos de terceiros.'],
  ['Zion Hospitality Academy', 'A escola do grupo. Formações, workshops e a série editorial Zion Land Development™: educar o mercado que a Zion mesma criou.'],
  ['Zion Capital', 'A ponte entre projetos estruturados e capital qualificado. Teses de investimento, ofertas estruturadas e relacionamento com investidores.'],
  ['Zion Exchange', 'Liquidez para ativos turísticos: intercâmbio, multipropriedade e novos modelos de acesso e saída para investidores e proprietários.'],
  ['Zion Design Studio', 'Direção criativa do grupo. Branding territorial, arquitetura de experiência e identidade de cada destino, do naming ao master plan conceitual.'],
  ['Zion Glamp Store', 'Fornecimento estratégico: estruturas, domos e equipamentos de glamping homologados pelo padrão Zion, para projetos próprios e de terceiros.'],
  ['Zion Hotel Group', 'Um grupo. Três modalidades. Um ecossistema completo a serviço do território.']
];

var METODO = [
  ['Zion Score™', 'Diagnóstico preliminar do território com nota de 0 a 10.'],
  ['Viabilidade Mercadológica', 'Fluxo turístico, sazonalidade, concorrência e posicionamento.'],
  ['Modelagem Financeira', 'CAPEX, EBITDA, TIR, VPL e payback em três cenários.'],
  ['Produto e Posicionamento', 'Conceito, narrativa territorial e diretrizes de master plan.'],
  ['Estruturação do Negócio', 'SPE, modelo societário e entrada de investidores.'],
  ['Apresentação a Investidores', 'Tese, teaser executivo, info memo e pitch institucional.'],
  ['Governança de Implantação', 'Milestones e aderência à tese até a operação performar.']
];

var PROJETOS = [
  ['Zion Bubble Glamping', 'Florianópolis · SC', 'Em operação'],
  ['Rota dos Milagres', 'Litoral Norte · AL', 'Estruturação'],
  ['Marchese di Ivrea', 'Serra Catarinense', 'Viabilidade'],
  ['Malhada do Caldeireiro', 'Rota dos Milagres · AL', 'Concepção']
];

var FAQ = [
  ['Preciso de capital próprio para desenvolver meu terreno?', 'Não é o capital que cria o projeto. É o projeto estruturado que atrai o capital. O papel da Zion é transformar o seu território em uma tese de investimento com viabilidade, governança e produto definidos, e colocá-la na frente do investidor certo. A ordem é essa, não o contrário.'],
  ['Meu terreno serve para um projeto turístico?', 'Essa é exatamente a pergunta que o Zion Score™ responde, com nota de 0 a 10: vocação do destino, mercado emissor, diária de referência, acesso e potencial construtivo. Alguns territórios pedem um glamping contemplativo, outros um resort de serra, outros nada. Saber isso antes de gastar um real em projeto é o que separa decisão de aposta.'],
  ['Não entendo nada de hotelaria. Isso é um problema?', 'Não. O developer não opera: ele estrutura. A operação é uma disciplina contratável, e é para isso que existe a Zion Hotel Management. O que não se contrata pronto é a estrutura do ativo, e é aí que a maioria erra sozinha. Operação se contrata. Estrutura se constrói.'],
  ['Quanto tempo leva do diagnóstico à operação?', 'Depende do porte e do licenciamento de cada território, mas o método existe para comprimir esse tempo com segurança: o Zion Score™ sai em dias, a tese completa de viabilidade em semanas, e cada etapa seguinte só começa quando a anterior está validada. O caminho mais rápido é o que não precisa ser refeito.'],
  ['O que é preciso para carregar a bandeira Zion Collection?', 'Homologação. A bandeira não é alugada: o projeto precisa passar pelo padrão Zion de experiência, tese e governança. É essa curadoria que protege o valor do selo para todos os que o carregam. O selo só vale porque nem todo projeto o recebe.'],
  ['Por onde eu começo?', 'Pelo Diagnóstico Territorial. Antes de arquiteto, antes de obra, antes de investidor: primeiro o território responde se sustenta um destino. É a decisão mais barata e mais importante de todo o processo. O próximo passo não é construir. É diagnosticar.']
];

var PAGES = {
  index: {
    file: 'index.html',
    titulo: 'Home · Grupo',
    hero: {
      kicker: 'Zion Hotel Group International · Florianópolis · Barcelona',
      h1: 'Desenvolvemos *destinos*.',
      sub: 'Enquanto o mercado constrói hotéis, nós estruturamos ativos. Três modalidades integradas: desenvolvemos, operamos e validamos com a bandeira. Do conceito à operação.',
      ctas: [{ t: 'Solicitar Diagnóstico', solid: true }, { t: 'Conhecer o Grupo', solid: false }],
      foot: ['Experiential Destination Development', 'MMXXVI'],
      big: true
    },
    final: {
      label: 'O próximo passo não é construir. É diagnosticar.',
      h2: 'Seu território pode ser\no próximo *destino Zion*.',
      p: 'O Diagnóstico Territorial Zion responde a única pergunta que importa antes de qualquer tijolo: isso é um destino ou apenas um terreno?',
      form: true,
      cta: 'Prefere conversar? Agendar Diagnóstico'
    }
  },
  development: {
    file: 'development.html',
    titulo: 'Modalidade 01 · Development',
    hero: {
      kicker: 'Zion Hotel Group International · Modalidade 01',
      h1: 'Do território ao *ativo estruturado*.',
      sub: 'Zion Hotel Development: desenvolvimento imobiliário turístico completo. Leitura territorial, viabilidade, produto, estrutura societária e captação. O projeto nasce do território e da tese financeira, nunca do palpite.',
      ctas: [{ t: 'Tenho um território', solid: true }]
    },
    forwho: '"Para quem tem uma terra com potencial enorme e sente que ela vale mais do que rende hoje: uma fazenda herdada, uma área na serra, um terreno de frente para o mar."',
    blocosTitulo: ['O processo', 'Sete etapas. Cada uma com *entregável concreto*.'],
    blocos: [
      ['00', 'Zion Score™', 'Diagnóstico preliminar do território com nota de 0 a 10: vocação do destino, mercado emissor, ADR de referência, CAPEX orientativo e concorrência regional. É a decisão mais barata e mais importante do processo.'],
      ['01', 'Viabilidade mercadológica', 'Perfil turístico, fluxo de visitantes, sazonalidade, infraestrutura, vetores de crescimento, oferta concorrente e benchmark nacional e internacional. O posicionamento estratégico nasce aqui.'],
      ['02', 'Viabilidade financeira', 'CAPEX detalhado, projeção de receitas e despesas, EBITDA, fluxo de caixa de longo prazo, TIR, VPL, payback e break-even. Três cenários: conservador, realista e otimista, com stress test.'],
      ['03', 'Produto e posicionamento', 'Conceito do empreendimento, narrativa territorial, definição de público, arquitetura de bandeira e diretrizes para o master plan. O projeto ganha identidade antes de ganhar planta.'],
      ['04', 'Estruturação do negócio', 'SPE, modelo societário, proteção patrimonial, estratégia de entrada de investidores e checklist de coordenação jurídica. O terreno deixa de ser um bem pessoal e vira veículo de investimento.'],
      ['05', 'Apresentação a investidores', 'Tese de investimento, teaser executivo, information memorandum e pitch deck institucional, adequados ao perfil de cada investidor. O ativo estruturado atrai o capital.'],
      ['06', 'Governança de implantação', 'Acompanhamento de milestones, validação de aderência à tese original, coordenação de stakeholders e relatórios periódicos até a operação performar.']
    ],
    banda: ['"Quem vai sozinho paga duas vezes: o custo do erro e o custo de reconstruir."', 'Por que existe método'],
    entregasTitulo: ['Entregas', 'O que você recebe *em mãos*.'],
    entregas: [
      ['Relatório Zion Score™', 'Nota do território, vocação, ADR de referência e CAPEX orientativo em documento executivo.'],
      ['Estudo de viabilidade completo', 'Mercadológico e financeiro, com três cenários, indicadores e valuation de saída.'],
      ['Conceito e master plan', 'Identidade do destino, narrativa territorial e diretrizes urbanísticas do empreendimento.'],
      ['Estrutura societária desenhada', 'SPE, governança e proteção patrimonial prontas para receber capital.'],
      ['Kit de captação', 'Teaser, information memorandum e pitch deck no padrão institucional Zion.'],
      ['Governança de implantação', 'Milestones, relatórios e acompanhamento até a abertura das portas.']
    ],
    final: {
      label: 'Modalidade 01 · Development',
      h2: 'Comece pelo que decide tudo:\n*o diagnóstico*.',
      p: 'O Zion Score™ responde se o seu território sustenta uma tese de destino, antes de qualquer investimento em projeto.',
      cta: 'Solicitar Diagnóstico'
    }
  },
  management: {
    file: 'management.html',
    titulo: 'Modalidade 02 · Management',
    hero: {
      kicker: 'Zion Hotel Group International · Modalidade 02',
      h1: 'O ativo pronto precisa *performar*.',
      sub: 'Zion Hotel Management: operação hoteleira com governança, controle de padrão e gestão de performance. A diferença entre um hotel que sobrevive e um ativo que entrega o resultado que a tese prometeu.',
      ctas: [{ t: 'Tenho um ativo operando', solid: true }]
    },
    forwho: '"Para quem tem um empreendimento pronto ou em operação, e investidores esperando que ele performe como o investimento que é."',
    blocosTitulo: ['Os pilares', 'Cinco disciplinas que *defendem a margem*.'],
    blocos: [
      ['01', 'Revenue management', 'Gestão ativa de diária, ocupação e canais. ADR, RevPAR e GOP acompanhados semanalmente, com precificação dinâmica por sazonalidade e demanda. É aqui que a diária média se defende.'],
      ['02', 'Padrão de experiência', 'SOPs completos, treinamento contínuo do time e auditoria de padrão. A experiência que o hóspede vive precisa ser a mesma que a marca prometeu, todos os dias, em todas as unidades.'],
      ['03', 'Jornada do hóspede', 'Do primeiro clique ao pós-estadia: reserva, chegada, imersão, gastronomia, despedida e retorno. Hospitalidade experiencial desenhada para gerar avaliação máxima e recompra.'],
      ['04', 'Gestão de custos e GOP', 'Estrutura de custos operacionais sob controle, indicadores por departamento e proteção do GOP. Margem não é sorte: é disciplina diária de operação.'],
      ['05', 'Governança e relatórios', 'Relatórios periódicos para proprietários e investidores, com indicadores, análise de aderência à tese e plano de ação. O investidor sabe, todo mês, o que o ativo entregou.']
    ],
    banda: ['"Margem não é sorte. É disciplina de operação, repetida todos os dias."', 'A tese da operação'],
    entregasTitulo: ['Indicadores', 'O que a gestão Zion *acompanha por você*.'],
    entregas: [
      ['ADR e RevPAR', 'Diária média e receita por unidade disponível, comparadas ao benchmark do mercado.'],
      ['Ocupação e sazonalidade', 'Taxa de ocupação por período, com estratégia ativa para baixa temporada.'],
      ['GOP e NOI', 'Resultado operacional bruto e líquido: o número que interessa ao investidor.'],
      ['Satisfação e reputação', 'Avaliações, NPS e reputação online como ativos de receita futura.'],
      ['Custos por departamento', 'Hospedagem, F&B e experiências com estrutura de custos individualizada.'],
      ['Aderência à tese', 'O realizado contra o projetado no estudo de viabilidade, mês a mês.']
    ],
    final: {
      label: 'Modalidade 02 · Management',
      h2: 'Seu ativo pode *render mais*.',
      p: 'Uma conversa de diagnóstico operacional mostra onde a margem está escapando e o que a gestão Zion faria diferente.',
      cta: 'Agendar Conversa'
    }
  },
  collection: {
    file: 'collection.html',
    titulo: 'Modalidade 03 · Collection',
    hero: {
      kicker: 'Zion Hotel Group International · Modalidade 03',
      h1: 'A marca não é alugada.\nEla é *validada*.',
      sub: 'Zion Collection: a bandeira do grupo. Curadoria de destinos com identidade, padrão de experiência e tese validada. Apenas projetos homologados carregam o selo.',
      ctas: [{ t: 'Quero a bandeira', solid: true }]
    },
    forwho: '"Para projetos que querem pertencer a algo maior: uma coleção de destinos com padrão reconhecível, distribuição e uma promessa que o hóspede identifica antes de chegar."',
    blocosTitulo: ['As coleções', 'Cinco coleções. Cada uma com *vocação territorial própria*.'],
    blocos: [
      ['I', 'Bubble Collection', 'Glamping imersivo e contemplação. Bolhas e estruturas transparentes em cenários de natureza intocada, para dormir sob as estrelas com conforto de hotel boutique. A coleção que nasceu com o grupo.'],
      ['II', 'Mountain Collection', 'Serra, clima frio e refúgios de altitude. Cabanas, chalés e experiências de montanha com gastronomia de fogo, lareira e silêncio. O luxo do isolamento bem servido.'],
      ['III', 'Beach Collection', 'Litoral premium e vida ao mar. Destinos de praia com arquitetura leve, pés na areia e curadoria de experiências náuticas e gastronômicas.'],
      ['IV', 'Wellness Collection', 'Regeneração, biofilia e bem-estar. Retiros com spa, terapias, alimentação viva e programação de reconexão. Hospitalidade transformacional no sentido literal.'],
      ['V', 'Signature Collection', 'Ativos únicos e icônicos por natureza. Propriedades que não cabem em categoria: uma fazenda histórica, uma ilha, um mirante impossível. O topo da curadoria Zion.']
    ],
    banda: ['"O selo só vale porque nem todo projeto o recebe."', 'O princípio da curadoria'],
    entregasTitulo: ['A bandeira', 'O que o selo *entrega ao projeto*.'],
    entregas: [
      ['Padrão de experiência', 'Manuais de marca e operação, SOPs e o padrão sensorial Zion aplicado ao destino.'],
      ['Distribuição e demanda', 'Presença nos canais do grupo, base de hóspedes e força de marketing compartilhada.'],
      ['Comunidade de investidores', 'Acesso ao ecossistema de capital que acompanha os projetos homologados.'],
      ['Homologação em quatro passos', 'Candidatura, auditoria de padrão e tese, adequação assistida e concessão do selo.'],
      ['Três modelos de adesão', 'Bandeira Zion, cobranding By Zion ou desenvolvimento white label: o grau certo de presença da marca para cada projeto.'],
      ['Rede entre destinos', 'Intercâmbio de hóspedes e experiências entre as unidades da coleção.']
    ],
    final: {
      label: 'Modalidade 03 · Collection',
      h2: 'Seu projeto tem *padrão Zion*?',
      p: 'A homologação começa com uma conversa e uma auditoria de padrão e tese. Se o projeto tiver o nível, a bandeira vem junto.',
      cta: 'Candidatar Meu Projeto'
    }
  },
  bruno: {
    file: 'bruno.html',
    titulo: 'Founder · Bruno Chaerk',
    hero: {
      kicker: 'Zion Hotel Group International · Florianópolis · Barcelona',
      h1: 'Bruno Chaerk',
      role: 'Founder · CEO · Developer Hoteleiro',
      mirror: 'Você tem uma terra incrível. Sente que ela vale muito mais do que rende hoje. E toda vez que tenta avançar, trava.',
      sub: 'Eu transformo territórios em destinos turísticos. Do conceito à operação: leitura territorial, viabilidade, marca, captação de investidores e gestão. Receita operacional e valorização patrimonial no mesmo ativo.',
      ctas: [{ t: 'Solicitar Diagnóstico Territorial', solid: false }],
      foot: ['Founder', 'MMXXVI']
    },
    sobre: {
      titulo: 'Developer hoteleiro. Estruturador de ativos. *Construtor de marcas.*',
      col1: 'Bruno Chaerk é founder e CEO da Zion Hotel Group International. Formado dentro de grandes redes hoteleiras internacionais na Espanha, trouxe para o Brasil uma leitura que o mercado local ainda não pratica: hotelaria não é imóvel com camas. É ativo estruturado, com marca, tese e saída.',
      col2: 'Hoje opera na interseção entre desenvolvimento imobiliário turístico, hospitalidade experiencial e estruturação financeira. Lê o território, desenha o produto, constrói a marca, modela o retorno e coloca o projeto na frente do capital certo.',
      creds: [
        'Background · Meliá · Barceló · Wyndham (Espanha)',
        'Base · Florianópolis, SC · Brasil',
        'Atuação · Desenvolvimento · Viabilidade · Captação · Marca · Operação'
      ]
    },
    colapso: {
      titulo: 'Por que sua terra *continua parada*.',
      itens: [
        ['Preciso de capital para começar.', 'O ativo bem estruturado atrai o capital. A ordem é essa, não o contrário.'],
        ['Preciso entender de hotelaria.', 'O developer não opera. Ele estrutura. Operação se contrata, estrutura se constrói.'],
        ['Ainda não é o momento certo.', 'Não existe momento certo. Existe estrutura certa.']
      ],
      custo: 'Existe um custo que não aparece em nenhum boleto: o custo da terra parada. Uma operação boutique validada no Brasil roda com diária média de R$ 1.571. Cada ano em que o seu território não vira produto é um ano de receita que não volta, num mercado que cresce sem esperar por ninguém.'
    },
    prova: {
      titulo: 'Números de quem *opera*, não de quem promete.',
      stats: [
        { num: 'R$ 1.571', desc: 'Diária média validada em operação própria' },
        { num: '43%', desc: 'Margem EBITDA em hospitalidade boutique' },
        { num: '05', desc: 'Projetos em desenvolvimento simultâneo' },
        { num: '03', desc: 'Modalidades integradas no grupo' }
      ],
      nota: 'Indicadores de operações e estudos conduzidos pela Zion Hotel Group International. Resultados variam conforme território, produto e estrutura.'
    },
    edu: {
      titulo: 'Antes de vender, *a Zion educa*.',
      paras: [
        'O mercado brasileiro de land development turístico ainda está sendo criado. Por isso Bruno publica diariamente: análises territoriais, bastidores de operação, viabilidade aberta e a série editorial Zion Land Development™.',
        'Quem aprende com a Zion chega pronto. A venda é consequência.'
      ],
      cta: 'Seguir @brunochaerkofc',
      pilares: [
        ['Terra', 'Potencial oculto e desenvolvimento territorial'],
        ['Hotelaria', 'Experiência, luxo natural, boutique hospitality'],
        ['Negócios', 'ROI, investidores, expansão de ativos'],
        ['Lifestyle', 'Liberdade, natureza, arquitetura'],
        ['Visão', 'O futuro do turismo e da economia da experiência']
      ]
    },
    final: {
      label: 'O próximo passo não é construir. É diagnosticar.',
      h2: 'Sua terra vale mais\ndo que *você imagina*.',
      p: 'O Diagnóstico Territorial Zion lê o seu território em profundidade e responde a única pergunta que importa antes de qualquer tijolo: isso é um destino ou apenas um terreno?',
      cta: 'Solicitar Diagnóstico'
    }
  }
};

var BANDA_HOME = ['"A terra já sabe o que quer ser. O nosso trabalho é escutar o território antes de desenhar o destino."', 'Leitura Territorial · O princípio de tudo'];

/* ----------------------------------------------------------------------------
   8. COMPONENTES
   -------------------------------------------------------------------------- */

var REG = {};   /* chave -> ComponentNode */

function I(key) {
  var c = REG[key];
  if (!c) throw new Error('Componente ausente: ' + key);
  return c.createInstance();
}

/* --- Botão --------------------------------------------------------------- */
function makeBotao(estilo, tema) {
  var dark = tema === 'Escuro';
  var solidBtn = estilo === 'Sólido';
  var f = F('Estilo=' + estilo + ', Tema=' + tema, {
    dir: 'H', padY: 17, padX: 52, cross: 'CENTER', main: 'CENTER'
  });
  if (solidBtn) fill(f, C.earth);
  stroke(f, C.earth, solidBtn ? 1 : 0.75, 1);
  var color = solidBtn ? C.cream : (dark ? C.cream : C.green);
  add(f, T('Solicitar Diagnóstico', {
    w: 400, size: 10.5, ls: 0.34, upper: true, color: color, name: 'rotulo'
  }));
  return f;
}

/* --- Nav ----------------------------------------------------------------- */
function makeNav(tipo) {
  var mobile = tipo === 'Mobile';
  var W = mobile ? 390 : 1440;
  var f = F('Tipo=' + tipo, {
    dir: 'H', w: W, padY: 20, padX: mobile ? 23 : 58,
    main: 'SPACE_BETWEEN', cross: 'CENTER', gap: 24, bg: C.black, bgOpacity: 0.9
  });
  sideStroke(f, C.cream, 0.07, { bottom: 1 });
  add(f, T('Zion', { serif: true, w: 400, size: 19, ls: 0.34, upper: true, color: C.cream, name: 'marca' }));
  var links = F('Links', { dir: 'H', gap: 30, cross: 'CENTER' });
  if (!mobile) {
    var arr = tipo === 'Home' ? NAV_HOME : NAV_INTERNA;
    for (var i = 0; i < arr.length; i++) {
      add(links, T(arr[i], { w: 300, size: 10.5, ls: 0.26, upper: true, color: C.sand, name: 'link' + (i + 1) }));
    }
  }
  var cta = F('CTA', { dir: 'H', padY: 11, padX: 24, cross: 'CENTER' });
  stroke(cta, C.earth, 0.75, 1);
  add(cta, T('Diagnóstico', { w: 400, size: 10.5, ls: 0.26, upper: true, color: C.cream, name: 'cta' }));
  add(links, cta);
  add(f, links);
  return f;
}

/* --- Rodapé -------------------------------------------------------------- */
function makeRodape(tipo, bp) {
  var mob = bp === 'Mobile';
  var W = mob ? 390 : 1440;
  var pad = padX(W);
  var f = F('Tipo=' + tipo + ', Breakpoint=' + bp, {
    dir: 'V', w: W, padT: tipo === 'Institucional' ? sp(W, 96) : sp(W, 64), padB: sp(W, 56),
    padX: pad, gap: sp(W, 88), bg: C.black
  });
  sideStroke(f, C.cream, 0.08, { top: 1 });

  if (tipo === 'Institucional') {
    var cols = F('Colunas', { dir: mob ? 'V' : 'H', gap: mob ? 44 : 64, w: inner(W) });
    var colW = mob ? inner(W) : Math.floor((inner(W) - 3 * 64) / 4.4);

    var c0 = F('Marca', { dir: 'V', gap: 20, w: mob ? colW : Math.round(colW * 1.4) });
    add(c0, T('Zion', { serif: true, w: 400, size: 26, ls: 0.3, upper: true, color: C.cream, name: 'marca' }));
    add(c0, T('Zion Hotel Group International. Desenvolvemos destinos: ativos turísticos que conectam território, experiência e valor.',
      { w: 300, size: 12.5, lh: 2.1, color: C.sand, maxW: mob ? colW : 280, name: 'descricao' }));
    add(cols, c0);

    var grupos = [
      ['Modalidades', ['Zion Hotel Development', 'Zion Hotel Management', 'Zion Collection']],
      ['Ecossistema', ['Zion Bubble Glamping', 'Zion Advisory', 'Zion Hospitality Academy', 'Zion Capital', 'Zion Design Studio']],
      ['Grupo', ['Método', 'Projetos', 'Founder', '@brunochaerkofc']]
    ];
    for (var g = 0; g < grupos.length; g++) {
      var col = F('Coluna ' + grupos[g][0], { dir: 'V', gap: 14, w: colW });
      var h4 = add(col, T(grupos[g][0], { w: 400, size: 10, ls: 0.3, upper: true, color: C.earth, name: 'titulo' }));
      h4.name = 'titulo';
      for (var l = 0; l < grupos[g][1].length; l++) {
        add(col, T(grupos[g][1][l], { w: 300, size: 12, ls: 0.08, color: C.sand, name: 'link' }));
      }
      add(cols, col);
    }
    add(f, cols);
  }

  var row = F('Linha', { dir: mob ? 'V' : 'H', w: inner(W), main: mob ? 'MIN' : 'SPACE_BETWEEN',
                         cross: mob ? 'MIN' : 'CENTER', gap: mob ? 12 : 20,
                         padT: tipo === 'Institucional' ? 44 : 0 });
  if (tipo === 'Institucional') sideStroke(row, C.cream, 0.08, { top: 1 });
  var itens = tipo === 'Institucional'
    ? ['Zion Hotel · Group International', 'Florianópolis · Barcelona', '© 2026 · Desenvolvemos Destinos']
    : ['Zion Hotel · Group International', 'Florianópolis · Barcelona', 'Grupo', '@brunochaerkofc', '© 2026 · Desenvolvemos Destinos'];
  for (var r = 0; r < itens.length; r++) {
    add(row, T(itens[r], { w: 300, size: 9.5, ls: 0.28, upper: true, color: C.sand, name: 'item' + (r + 1) }));
  }
  add(f, row, true);
  return f;
}

/* --- Indicador ----------------------------------------------------------- */
function makeIndicador() {
  var f = F('Indicador', { dir: 'V', gap: 16, padY: 72, padX: 32, cross: 'CENTER', w: 310 });
  add(f, T('R$ 1.571', { serif: true, w: 300, size: 60, lh: 1.1, ls: 0.02, color: C.cream, align: 'CENTER', name: 'num' }), true);
  var d = add(f, T('Diária média validada em operação própria',
    { w: 300, size: 10, lh: 2, ls: 0.26, upper: true, color: C.sand, align: 'CENTER', name: 'desc' }), true);
  d.textAlignHorizontal = 'CENTER';
  return f;
}

/* --- Linha de Especificação ---------------------------------------------- */
function makeSpecRow() {
  var f = F('Linha de Especificação', { dir: 'H', w: 420, padY: 19, gap: 24, main: 'SPACE_BETWEEN', cross: 'BASELINE' });
  sideStroke(f, C.cream, 0.09, { bottom: 1 });
  add(f, T('Diagnóstico', { w: 500, size: 11, ls: 0.26, upper: true, color: C.cream, name: 'titulo' }));
  var v = add(f, T('Zion Score™ e leitura territorial', { w: 300, size: 12, color: C.sand, align: 'RIGHT', name: 'valor' }));
  v.textAlignHorizontal = 'RIGHT';
  return f;
}

/* --- Bloco de Processo --------------------------------------------------- */
function makeBloco(bp) {
  var mob = bp === 'Mobile';
  var W = mob ? 344 : 1140;
  var f = F('Breakpoint=' + bp, { dir: mob ? 'V' : 'H', w: W, padY: 44, gap: mob ? 12 : 40, cross: mob ? 'MIN' : 'MIN' });
  sideStroke(f, C.cream, 0.09, { top: 1 });
  var n = T('00', { serif: true, w: 300, size: 30, color: C.earth, name: 'n' });
  if (!mob) { add(f, n); n.resize(110, n.height); }
  else add(f, n);
  var t = T('Zion Score™', { serif: true, w: 400, size: mob ? 21 : 27, lh: 1.3, color: C.cream, name: 'titulo' });
  var p = T('Descrição da etapa do processo, com entregável concreto e linguagem territorial.',
    { w: 300, size: 13.5, lh: 2.1, color: C.sand, name: 'desc' });
  if (mob) {
    add(f, t, true); add(f, p, true);
  } else {
    add(f, t); t.textAutoResize = 'HEIGHT'; t.resize(Math.round((W - 110 - 80) * 0.4), t.height);
    add(f, p); p.textAutoResize = 'HEIGHT'; p.resize(Math.round((W - 110 - 80) * 0.6), p.height);
  }
  return f;
}

/* --- Célula (grid claro) ------------------------------------------------- */
function makeCelula() {
  var f = F('Célula', { dir: 'V', gap: 14, padY: 50, padX: 46, w: 570 });
  sideStroke(f, C.green, 0.14, { bottom: 1, right: 1 });
  add(f, T('Zion Advisory', { serif: true, w: 400, size: 24, ls: 0.02, color: C.green, name: 'titulo' }), true);
  add(f, T('Descrição da unidade ou entrega, em tom institucional e direto.',
    { w: 300, size: 13, lh: 2, color: C.green, opacity: 0.72, name: 'desc' }), true);
  return f;
}

/* --- Item de FAQ --------------------------------------------------------- */
function makeFaq() {
  var f = F('Item de FAQ', { dir: 'V', w: 860, padT: 34, padB: 40, gap: 18 });
  sideStroke(f, C.green, 0.14, { bottom: 1 });
  var head = F('Pergunta', { dir: 'H', main: 'SPACE_BETWEEN', cross: 'CENTER', gap: 32 });
  add(f, head, true);
  var q = add(head, T('Por onde eu começo?', { serif: true, w: 400, size: 26, lh: 1.4, color: C.green, name: 'pergunta' }));
  q.layoutGrow = 1;
  add(head, T('+', { serif: true, w: 300, size: 30, color: C.earth, name: 'sinal' }));
  add(f, T('Resposta objetiva, com a frase de virada em destaque no final.',
    { w: 300, size: 14, lh: 2.2, color: C.green, opacity: 0.75, name: 'resposta' }), true);
  return f;
}

/* --- Ato da Jornada ------------------------------------------------------ */
function makeAto(bp) {
  var mob = bp === 'Mobile';
  var W = mob ? 344 : 1140;
  var f = F('Breakpoint=' + bp, { dir: mob ? 'V' : 'H', w: W, padY: 44, gap: mob ? 12 : 40, cross: 'MIN' });
  sideStroke(f, C.green, 0.14, { bottom: 1 });
  var a = T('Ato 1', { w: 300, size: 10, ls: 0.3, upper: true, color: C.earth, name: 'ato' });
  add(f, a);
  if (!mob) a.resize(120, a.height);
  var t = T('A terra *parada*', { serif: true, w: 400, size: mob ? 20 : 28, lh: 1.3, ls: 0.02, color: C.green, name: 'titulo' });
  var p = T('Descrição do ato da jornada.', { w: 300, size: 13, lh: 2, color: C.green, opacity: 0.72, name: 'desc' });
  if (mob) { add(f, t, true); add(f, p, true); }
  else {
    add(f, t); t.textAutoResize = 'HEIGHT'; t.resize(Math.round((W - 120 - 80) * 0.42), t.height);
    add(f, p); p.textAutoResize = 'HEIGHT'; p.resize(Math.round((W - 120 - 80) * 0.58), p.height);
  }
  return f;
}

/* --- Etapa do Método ----------------------------------------------------- */
function makeEtapa(bp) {
  var mob = bp === 'Mobile';
  var W = mob ? 344 : 1140;
  var f = F('Breakpoint=' + bp, { dir: mob ? 'V' : 'H', w: W, padY: 34, gap: mob ? 10 : 36, cross: 'MIN' });
  sideStroke(f, C.cream, 0.09, { top: 1 });
  var n = T('00', { serif: true, w: 300, size: 30, ls: 0.08, color: C.earth, name: 'n' });
  add(f, n);
  if (!mob) n.resize(90, n.height);
  var t = T('Zion Score™', { w: 500, size: 12, ls: 0.24, upper: true, color: C.cream, name: 'titulo' });
  var p = T('Entregável da etapa.', { w: 300, size: 13, lh: 2, color: C.sand, name: 'desc' });
  if (mob) { add(f, t, true); add(f, p, true); }
  else {
    add(f, t); t.textAutoResize = 'HEIGHT'; t.resize(Math.round((W - 90 - 72) * 0.38), t.height);
    add(f, p); p.textAutoResize = 'HEIGHT'; p.resize(Math.round((W - 90 - 72) * 0.62), p.height);
  }
  return f;
}

/* --- Projeto ------------------------------------------------------------- */
function makeProjeto(bp) {
  var mob = bp === 'Mobile';
  var W = mob ? 344 : 1140;
  var f = F('Breakpoint=' + bp, { dir: mob ? 'V' : 'H', w: W, padY: 40, gap: mob ? 8 : 32, cross: mob ? 'MIN' : 'BASELINE' });
  sideStroke(f, C.green, 0.14, { top: 1 });
  var nome = T('Zion Bubble Glamping', { serif: true, w: 400, size: mob ? 24 : 32, ls: 0.02, color: C.green, name: 'nome' });
  var local = T('Florianópolis · SC', { w: 300, size: 11, ls: 0.24, upper: true, color: C.green, opacity: 0.55, name: 'local' });
  var status = T('Em operação', { w: 300, size: 11, ls: 0.24, upper: true, color: C.earth, name: 'status' });
  if (mob) { add(f, nome, true); add(f, local, true); add(f, status, true); }
  else {
    var u = W - 2 * 32;
    add(f, nome); nome.textAutoResize = 'HEIGHT'; nome.resize(Math.round(u * 0.5), nome.height);
    add(f, local); local.textAutoResize = 'HEIGHT'; local.resize(Math.round(u * 0.25), local.height);
    add(f, status); status.textAutoResize = 'HEIGHT'; status.resize(Math.round(u * 0.25), status.height);
    status.textAlignHorizontal = 'RIGHT';
  }
  return f;
}

function buildComponents(host) {
  var made = [];

  function push(node) { host.appendChild(node); made.push(node); return node; }

  /* Botão — 4 variantes */
  var btns = [];
  ['Sólido', 'Contorno'].forEach(function (e) {
    ['Escuro', 'Claro'].forEach(function (t) {
      var c = asComponent(makeBotao(e, t), 'Estilo=' + e + ', Tema=' + t);
      host.appendChild(c);
      btns.push(c);
      REG['Botão/' + e + '/' + t] = c;
    });
  });
  var setBtn = figma.combineAsVariants(btns, host);
  setBtn.name = 'Botão';
  setBtn.description = 'CTA institucional Zion · caps 10.5px · tracking .34em · borda Zion Earth';
  made.push(setBtn);

  /* Nav — 3 variantes */
  var navs = [];
  ['Home', 'Interna', 'Mobile'].forEach(function (t) {
    var c = asComponent(makeNav(t), 'Tipo=' + t);
    host.appendChild(c);
    navs.push(c);
    REG['Nav/' + t] = c;
  });
  var setNav = figma.combineAsVariants(navs, host);
  setNav.name = 'Nav';
  made.push(setNav);

  /* Rodapé — 4 variantes (tipo × breakpoint) */
  var foots = [];
  ['Institucional', 'Simples'].forEach(function (t) {
    ['Desktop', 'Mobile'].forEach(function (bp) {
      var c = asComponent(makeRodape(t, bp), 'Tipo=' + t + ', Breakpoint=' + bp);
      host.appendChild(c);
      foots.push(c);
      REG['Rodapé/' + t + '/' + bp] = c;
    });
  });
  var setFoot = figma.combineAsVariants(foots, host);
  setFoot.name = 'Rodapé';
  made.push(setFoot);

  /* Simples */
  REG['Indicador'] = push(asComponent(makeIndicador(), 'Indicador', 'Número vivo da prova social'));
  REG['Linha de Especificação'] = push(asComponent(makeSpecRow(), 'Linha de Especificação'));
  REG['Célula'] = push(asComponent(makeCelula(), 'Célula', 'Célula de grid em seções claras'));
  REG['Item de FAQ'] = push(asComponent(makeFaq(), 'Item de FAQ'));

  /* Com breakpoint */
  [['Bloco de Processo', makeBloco], ['Ato da Jornada', makeAto],
   ['Etapa do Método', makeEtapa], ['Projeto', makeProjeto]].forEach(function (pair) {
    var vs = [];
    ['Desktop', 'Mobile'].forEach(function (bp) {
      var c = asComponent(pair[1](bp), 'Breakpoint=' + bp);
      host.appendChild(c);
      vs.push(c);
      REG[pair[0] + '/' + bp] = c;
    });
    var s = figma.combineAsVariants(vs, host);
    s.name = pair[0];
    made.push(s);
  });

  return made;
}

/* Instancia um componente com breakpoint conforme a largura */
function IB(key, W) { return I(key + '/' + (isMobile(W) ? 'Mobile' : 'Desktop')); }

/* ----------------------------------------------------------------------------
   9. SEÇÕES DE PÁGINA
   -------------------------------------------------------------------------- */

function botao(texto, solidBtn, dark, W) {
  var inst = I('Botão/' + (solidBtn ? 'Sólido' : 'Contorno') + '/' + (dark ? 'Escuro' : 'Claro'));
  ov(inst, 'rotulo', texto);
  if (isMobile(W)) {
    try {
      inst.layoutSizingHorizontal = 'FIXED';
      inst.resize(Math.min(inner(W), 300), inst.height);
    } catch (e) {}
  }
  return inst;
}

function ctaRow(ctas, dark, W, center) {
  var row = F('CTAs', { dir: 'H', gap: 20, wrap: !isMobile(W), main: center ? 'CENTER' : 'MIN', cross: 'CENTER' });
  if (isMobile(W)) { row.layoutMode = 'VERTICAL'; row.counterAxisAlignItems = center ? 'CENTER' : 'MIN'; }
  for (var i = 0; i < ctas.length; i++) add(row, botao(ctas[i].t, ctas[i].solid, dark, W));
  return row;
}

function navFor(page, W) {
  var inst = isMobile(W) ? I('Nav/Mobile') : I(page === 'index' ? 'Nav/Home' : 'Nav/Interna');
  inst.name = 'Nav';
  return inst;
}

function hero(data, W, minH) {
  var pad = Math.round(W * 0.06);
  var f = F('Hero', {
    dir: 'V', w: W, bg: C.black, gap: 0,
    padT: sp(W, 180), padB: sp(W, 140), padX: pad, cross: 'CENTER', main: 'CENTER'
  });

  var k = add(f, label(data.kicker, W));
  k.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 56)));

  var h1 = add(f, T(data.h1, {
    serif: true, w: 300, size: cl(40, data.big ? 8 : 6.6, data.big ? 110 : 88, W),
    lh: 1.13, ls: 0.01, color: C.cream, align: 'CENTER',
    maxW: Math.min(inner(W, 9999), data.big ? 900 : 960), name: 'H1'
  }));
  h1.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 44)));

  if (data.role) {
    var role = add(f, label(data.role, W));
    role.textAlignHorizontal = 'CENTER';
    add(f, gapBox(sp(W, 40)));
  }
  if (data.mirror) {
    var m = add(f, T(data.mirror, {
      serif: true, w: 300, italic: true, size: cl(19, 2.4, 30, W), lh: 1.7,
      color: C.sand, align: 'CENTER', maxW: Math.min(inner(W, 9999), 640), name: 'Espelhamento'
    }));
    m.textAlignHorizontal = 'CENTER';
    add(f, gapBox(sp(W, 36)));
  }

  var sub = add(f, T(data.sub, {
    w: 300, size: cl(13, 1.5, 16, W), lh: 2.2, color: C.sand, align: 'CENTER',
    maxW: Math.min(inner(W, 9999), 560), name: 'Subtítulo'
  }));
  sub.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 72)));

  add(f, ctaRow(data.ctas, true, W, true));

  if (minH && f.height < minH) {
    f.primaryAxisSizingMode = 'FIXED';
    f.resize(W, minH);
  }
  backdrop(f, TERRAIN_HERO, 800, 0.14);

  if (data.foot && !isMobile(W)) {
    /* a altura precisa ser lida antes do append: enquanto o nó não é marcado
       como absoluto ele entra no fluxo e infla o frame */
    var hBefore = f.height;
    var foot = F('Rodapé do Hero', { dir: 'H', w: W - 2 * pad, main: 'SPACE_BETWEEN', cross: 'CENTER' });
    add(foot, T(data.foot[0], { w: 300, size: 9.5, ls: 0.28, upper: true, color: C.sand, opacity: 0.8 }));
    add(foot, T(data.foot[1], { w: 300, size: 9.5, ls: 0.28, upper: true, color: C.sand, opacity: 0.8 }));
    f.appendChild(foot);
    try {
      foot.layoutPositioning = 'ABSOLUTE';
      foot.x = pad; foot.y = hBefore - 34 - foot.height;
      foot.constraints = { horizontal: 'STRETCH', vertical: 'MAX' };
    } catch (e) {}
  }
  return f;
}

function numbersBar(stats, W) {
  var f = F('Números Vivos', { dir: isMobile(W) ? 'V' : 'H', w: W, bg: C.black });
  sideStroke(f, C.cream, 0.08, { top: 1, bottom: 1 });
  for (var i = 0; i < stats.length; i++) {
    if (i > 0) {
      var line = add(f, rule(C.cream, 0.08));
      if (isMobile(W)) { line.resize(W, 1); }
      else { line.resize(1, 10); try { line.layoutSizingVertical = 'FILL'; } catch (e) {} }
    }
    var inst = I('Indicador');
    ov(inst, 'num', stats[i].num);
    ov(inst, 'desc', stats[i].desc);
    add(f, inst);
    try { inst.layoutSizingHorizontal = 'FILL'; } catch (e) {}
    if (isMobile(W)) { inst.paddingTop = 44; inst.paddingBottom = 44; }
  }
  return f;
}

function manifesto(W) {
  var f = section('Manifesto', W, { maxW: 760, cross: 'CENTER', gap: sp(W, 40) });
  fill(f, C.black);
  add(f, splitword('Manifesto', W, true, true), true);
  var p = add(f, T('Projetamos e estruturamos ativos que conectam território, experiência e valor. Do conceito à operação, criamos projetos com identidade, consistência e relevância de longo prazo.',
    { serif: true, w: 300, size: cl(22, 3.2, 38, W), lh: 1.8, color: C.cream, align: 'CENTER',
      maxW: inner(W, 760), name: 'Manifesto' }), true);
  p.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 24)));
  var s = add(f, label('Zion · Um lugar elevado', W));
  s.textAlignHorizontal = 'CENTER';
  return f;
}

function terrainBand(quote, sub, W) {
  var f = F('Faixa Territorial', {
    dir: 'V', w: W, bg: C.black, padY: sp(W, 200), padX: Math.round(W * 0.06),
    cross: 'CENTER', gap: sp(W, 40)
  });
  sideStroke(f, C.cream, 0.06, { top: 1, bottom: 1 });
  var q = add(f, T(quote, {
    serif: true, w: 300, italic: true, size: cl(22, 3.4, 42, W), lh: 1.6,
    color: C.cream, align: 'CENTER', maxW: Math.min(inner(W, 9999), 760), name: 'Citação'
  }));
  q.textAlignHorizontal = 'CENTER';
  var l = add(f, label(sub, W));
  l.textAlignHorizontal = 'CENTER';
  backdrop(f, TERRAIN_BAND, 600, 0.12);
  return f;
}

function forwhoBand(texto, W) {
  var f = F('Para Quem', { dir: 'V', w: W, bg: C.black, padY: sp(W, 88), padX: padX(W), cross: 'CENTER' });
  sideStroke(f, C.cream, 0.08, { top: 1, bottom: 1 });
  var p = add(f, T(texto, {
    serif: true, w: 300, italic: true, size: cl(19, 2.8, 32, W), lh: 1.8,
    color: C.cream, align: 'CENTER', maxW: Math.min(inner(W), 820), name: 'Recorte'
  }));
  p.textAlignHorizontal = 'CENTER';
  return f;
}

function modalidadeBlock(m, W) {
  var f = F('Modalidade · ' + m.titulo, {
    dir: 'V', w: W, bg: C.black, padY: sp(W, 130), padX: padX(W), gap: 0
  });
  sideStroke(f, C.cream, 0.09, { top: 1 });
  add(f, T(m.num, { w: 200, size: 12, ls: 0.5, upper: true, color: C.earth, name: 'Numeração' }));
  add(f, gapBox(22));
  add(f, T(m.titulo, { serif: true, w: 300, size: cl(30, 4.4, 54, W), lh: 1.2, ls: 0.01, color: C.cream, name: 'Título' }), true);
  add(f, gapBox(20));
  add(f, T(m.forwho, { serif: true, w: 300, italic: true, size: cl(17, 2, 21, W), color: C.sand,
                       maxW: inner(W), name: 'Para quem' }), true);
  add(f, gapBox(sp(W, 56)));

  var body = F('Corpo', { dir: isMobile(W) ? 'V' : 'H', gap: isMobile(W) ? 44 : 88, w: inner(W), cross: 'MIN' });
  var colL = F('Narrativa', { dir: 'V', gap: 22 });
  var colR = F('Especificações', { dir: 'V', gap: 0 });
  var wL, wR;
  if (isMobile(W)) { wL = inner(W); wR = inner(W); }
  else {
    var usable = inner(W) - 88;
    wL = Math.round(usable * 0.55); wR = usable - wL;
  }
  colL.counterAxisSizingMode = 'FIXED'; colL.resize(wL, 10);
  colR.counterAxisSizingMode = 'FIXED'; colR.resize(wR, 10);

  for (var i = 0; i < m.paras.length; i++) {
    add(colL, T(m.paras[i], { w: 300, size: 14.5, lh: 2.2, color: C.cream, opacity: 0.92, name: 'Parágrafo' }), true);
  }
  add(colL, gapBox(14));
  add(colL, T(m.quote, { serif: true, w: 300, italic: true, size: 21, lh: 1.6, color: C.sand, name: 'Frase' }), true);
  add(colL, gapBox(22));
  add(colL, ctaRow(m.ctas, true, W, false));

  for (var s = 0; s < m.specs.length; s++) {
    var inst = I('Linha de Especificação');
    ov(inst, 'titulo', m.specs[s][0]);
    ov(inst, 'valor', m.specs[s][1]);
    add(colR, inst, true);
    if (s === 0) sideStroke(inst, C.cream, 0.09, { top: 1, bottom: 1 });
  }

  add(body, colL);
  add(body, colR);
  add(f, body, true);
  return f;
}

function blocosSection(titulo, blocos, W, dark) {
  var f = section('Blocos · ' + titulo[0], W, { gap: sp(W, 88) });
  fill(f, dark ? C.black : C.cream);
  add(f, secHead(titulo[0], titulo[1], W, dark), true);
  var list = F('Lista', { dir: 'V', w: inner(W) });
  for (var i = 0; i < blocos.length; i++) {
    var inst = IB('Bloco de Processo', W);
    ov(inst, 'n', blocos[i][0]);
    ov(inst, 'titulo', blocos[i][1]);
    ov(inst, 'desc', blocos[i][2]);
    add(list, inst, true);
    if (i === blocos.length - 1) sideStroke(inst, C.cream, 0.09, { top: 1, bottom: 1 });
  }
  add(f, list, true);
  return f;
}

function gridCelulas(itens, W, bg) {
  var grid = F('Grid', { dir: 'V', w: inner(W), gap: 0 });
  sideStroke(grid, C.green, 0.14, { top: 1 });
  var cols = isMobile(W) ? 1 : 2;
  for (var i = 0; i < itens.length; i += cols) {
    var row = F('Linha', { dir: 'H', w: inner(W), gap: 0 });
    for (var j = 0; j < cols && i + j < itens.length; j++) {
      var inst = I('Célula');
      ov(inst, 'titulo', itens[i + j][0]);
      ov(inst, 'desc', itens[i + j][1]);
      add(row, inst);
      try { inst.layoutSizingHorizontal = 'FILL'; } catch (e) {}
      if (j === cols - 1 || i + j === itens.length - 1) sideStroke(inst, C.green, 0.14, { bottom: 1 });
      if (isMobile(W)) { inst.paddingLeft = 0; inst.paddingRight = 0; }
    }
    add(grid, row, true);
  }
  return grid;
}

function entregasSection(titulo, itens, W) {
  var f = section('Entregas · ' + titulo[0], W, { gap: sp(W, 88) });
  fill(f, C.cream);
  add(f, secHead(titulo[0], titulo[1], W, false), true);
  add(f, gridCelulas(itens, W, C.cream), true);
  return f;
}

function jornadaSection(W) {
  var f = section('Jornada', W, { gap: sp(W, 88) });
  fill(f, C.cream);
  add(f, secHead('Jornada', 'Do terreno parado ao destino que performa, *em seis atos*.', W, false), true);
  var list = F('Atos', { dir: 'V', w: inner(W) });
  sideStroke(list, C.green, 0.14, { top: 1 });
  for (var i = 0; i < JORNADA.length; i++) {
    var inst = IB('Ato da Jornada', W);
    ov(inst, 'ato', 'Ato ' + (i + 1));
    ov(inst, 'titulo', JORNADA[i][0]);
    ov(inst, 'desc', JORNADA[i][1]);
    add(list, inst, true);
  }
  add(f, list, true);
  return f;
}

function ecossistemaSection(W) {
  var f = section('Ecossistema', W, { gap: sp(W, 60) });
  fill(f, C.sand);
  add(f, secHead('Ecossistema', 'O ciclo completo do desenvolvimento, *sob um mesmo teto*.', W, false), true);
  add(f, T('Em volta das três modalidades, o grupo opera unidades complementares que fecham o ciclo do desenvolvimento hoteleiro: da educação do mercado ao capital, do design ao fornecimento.',
    { w: 300, size: 15, lh: 2.2, color: C.green, maxW: Math.min(inner(W), 620), name: 'Introdução' }));
  add(f, gridCelulas(ECOSSISTEMA, W, C.sand), true);
  add(f, gapBox(sp(W, 50)));
  var q = add(f, T('"Território, experiência e valor."', {
    serif: true, w: 300, italic: true, size: cl(22, 3, 34, W), lh: 1.7,
    color: C.green, align: 'CENTER', maxW: inner(W), name: 'Frase'
  }), true);
  q.textAlignHorizontal = 'CENTER';
  return f;
}

function metodoSection(W) {
  var f = section('Método', W, { gap: sp(W, 60) });
  fill(f, C.black);
  add(f, secHead('Método', 'A Pirâmide Invertida©: a ordem que *protege o capital*.', W, true), true);
  add(f, T('Metodologia proprietária do grupo: sete etapas com entregável concreto. O projeto nasce do território e da tese financeira, não do sonho da arquitetura. É o método que conecta as três modalidades.',
    { w: 300, size: 15, lh: 2.2, color: C.sand, maxW: Math.min(inner(W), 620), name: 'Introdução' }));
  var list = F('Etapas', { dir: 'V', w: inner(W) });
  for (var i = 0; i < METODO.length; i++) {
    var inst = IB('Etapa do Método', W);
    ov(inst, 'n', '0' + i);
    ov(inst, 'titulo', METODO[i][0]);
    ov(inst, 'desc', METODO[i][1]);
    add(list, inst, true);
    if (i === METODO.length - 1) sideStroke(inst, C.cream, 0.09, { top: 1, bottom: 1 });
  }
  add(f, list, true);
  return f;
}

function scoreSection(W) {
  var f = F('Zion Score', {
    dir: 'V', w: W, bg: C.black, padY: sp(W, 210), padX: Math.round(W * 0.06), cross: 'CENTER', gap: 0
  });
  sideStroke(f, C.cream, 0.06, { top: 1, bottom: 1 });
  var big = add(f, T('10', { serif: true, w: 300, size: cl(90, 15, 190, W), lh: 1, color: C.earth, align: 'CENTER', name: 'Nota' }));
  big.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 36)));
  var h2 = add(f, T('Todo território tem uma nota.\nVocê ainda não sabe *a da sua terra*.', {
    serif: true, w: 300, size: cl(28, 4.6, 54, W), lh: 1.35, color: C.cream, align: 'CENTER',
    maxW: Math.min(inner(W, 9999), 900), name: 'Título'
  }));
  h2.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 36)));
  var p = add(f, T('O Zion Score™ avalia vocação do destino, mercado emissor, diária de referência e potencial construtivo, e devolve um número de 0 a 10. É a diferença entre apostar e decidir.', {
    w: 300, size: 15, lh: 2.2, color: C.sand, align: 'CENTER', maxW: Math.min(inner(W, 9999), 560), name: 'Apoio'
  }));
  p.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 64)));
  add(f, botao('Descobrir o Zion Score da minha terra', true, true, W));
  backdrop(f, TERRAIN_FINAL, 700, 0.12);
  return f;
}

function projetosSection(W) {
  var f = section('Projetos', W, { gap: sp(W, 88) });
  fill(f, C.sand);
  add(f, secHead('Projetos', 'Destinos em *desenvolvimento*.', W, false), true);
  var list = F('Lista', { dir: 'V', w: inner(W) });
  for (var i = 0; i < PROJETOS.length; i++) {
    var inst = IB('Projeto', W);
    ov(inst, 'nome', PROJETOS[i][0]);
    ov(inst, 'local', PROJETOS[i][1]);
    ov(inst, 'status', PROJETOS[i][2]);
    add(list, inst, true);
    if (i === PROJETOS.length - 1) sideStroke(inst, C.green, 0.14, { top: 1, bottom: 1 });
  }
  add(f, list, true);
  return f;
}

function founderSection(W) {
  var f = section('Founder', W, { gap: sp(W, 60) });
  fill(f, C.black);
  add(f, secHead('Founder', null, W, true), true);
  var grid = F('Grid', { dir: isMobile(W) ? 'V' : 'H', gap: isMobile(W) ? 52 : 96, w: inner(W), cross: 'CENTER' });
  var colW = isMobile(W) ? inner(W) : Math.round((inner(W) - 96) / 2);

  var left = F('Bio', { dir: 'V', gap: 20 });
  left.counterAxisSizingMode = 'FIXED'; left.resize(colW, 10);
  add(left, T('Bruno Chaerk', { serif: true, w: 300, size: cl(34, 5, 62, W), lh: 1.15, color: C.cream, name: 'Nome' }), true);
  add(left, label('Founder · CEO · Developer Hoteleiro', W));
  add(left, gapBox(10));
  add(left, T('Formado dentro de grandes redes hoteleiras internacionais na Espanha, Bruno lidera o grupo com uma convicção: hotelaria não é imóvel com camas. É ativo estruturado, com marca, tese e saída.',
    { w: 300, size: 14.5, lh: 2.2, color: C.cream, opacity: 0.92, name: 'Bio' }), true);
  var creds = F('Credenciais', { dir: 'V', gap: 13 });
  ['Background · Meliá · Barceló · Wyndham (Espanha)', 'Base · Florianópolis, SC · Brasil'].forEach(function (c) {
    var box = F('Credencial', { dir: 'V', padT: 13 });
    sideStroke(box, C.cream, 0.09, { top: 1 });
    add(box, T(c, { w: 300, size: 10.5, ls: 0.26, upper: true, color: C.sand, name: 'Credencial' }), true);
    add(creds, box, true);
  });
  add(left, creds, true);
  add(left, gapBox(18));
  add(left, botao('Conhecer o Founder', false, true, W));

  var right = F('Citação', { dir: 'V' });
  right.counterAxisSizingMode = 'FIXED'; right.resize(colW, 10);
  add(right, T('"Você tem uma terra incrível. Eu transformo territórios em destinos."', {
    serif: true, w: 300, italic: true, size: cl(22, 2.8, 32, W), lh: 1.8, color: C.sand, name: 'Citação'
  }), true);

  add(grid, left); add(grid, right);
  add(f, grid, true);
  return f;
}

function faqSection(W) {
  var f = section('FAQ', W, { gap: sp(W, 88) });
  fill(f, C.cream);
  add(f, secHead('Perguntas', 'O que todo dono de terra *pergunta primeiro*.', W, false), true);
  var list = F('Lista', { dir: 'V', w: Math.min(inner(W), 860) });
  sideStroke(list, C.green, 0.14, { top: 1 });
  for (var i = 0; i < FAQ.length; i++) {
    var inst = I('Item de FAQ');
    ov(inst, 'pergunta', FAQ[i][0]);
    ov(inst, 'resposta', FAQ[i][1]);
    add(list, inst, true);
    if (isMobile(W)) {
      var q = inst.findOne(function (n) { return n.name === 'pergunta'; });
      if (q) q.fontSize = 19;
    }
  }
  add(f, list);
  return f;
}

/* Mock do formulário HubSpot embutido no CTA final da home */
function formMock(W) {
  var w = Math.min(inner(W, 9999), 620);
  var f = F('Formulário HubSpot (embed)', { dir: 'V', w: w, bg: C.cream, padY: 44, padX: 40, gap: 26 });
  add(f, T('Diagnóstico Territorial', { serif: true, w: 400, size: 24, color: C.green, name: 'Título' }), true);
  ['Nome completo', 'E-mail', 'WhatsApp', 'Onde fica o seu território?'].forEach(function (campo) {
    var box = F('Campo · ' + campo, { dir: 'V', gap: 10, padB: 12 });
    sideStroke(box, C.green, 0.25, { bottom: 1 });
    add(box, T(campo, { w: 300, size: 10, ls: 0.26, upper: true, color: C.green, opacity: 0.6, name: 'Rótulo' }), true);
    add(box, T(' ', { w: 300, size: 14, color: C.green, name: 'Valor' }), true);
    add(f, box, true);
  });
  add(f, botao('Enviar', true, false, W));
  return f;
}

function finalSection(data, W) {
  var f = F('CTA Final', {
    dir: 'V', w: W, bg: C.black, padY: sp(W, 190), padX: Math.round(W * 0.06), cross: 'CENTER', gap: 0
  });
  var l = add(f, label(data.label, W));
  l.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 40)));
  var h2 = add(f, T(data.h2, {
    serif: true, w: 300, size: cl(30, 5.4, 66, W), lh: 1.3, color: C.cream, align: 'CENTER',
    maxW: Math.min(inner(W, 9999), 900), name: 'Título'
  }));
  h2.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 44)));
  var p = add(f, T(data.p, {
    w: 300, size: 15, lh: 2.2, color: C.sand, align: 'CENTER', maxW: Math.min(inner(W, 9999), 560), name: 'Apoio'
  }));
  p.textAlignHorizontal = 'CENTER';
  add(f, gapBox(sp(W, 60)));
  if (data.form) {
    add(f, formMock(W));
    add(f, gapBox(sp(W, 44)));
  }
  add(f, botao(data.cta, !data.form, true, W));
  backdrop(f, TERRAIN_FINAL, 700, 0.12);
  return f;
}

function rodapeFor(tipo, W) {
  var inst = I('Rodapé/' + tipo + '/' + (isMobile(W) ? 'Mobile' : 'Desktop'));
  inst.name = 'Rodapé · ' + tipo;
  return inst;
}

/* ----------------------------------------------------------------------------
   10. PÁGINAS
   -------------------------------------------------------------------------- */

function pageFrame(nome, W) {
  var f = F(nome, { dir: 'V', w: W, bg: C.black, gap: 0, clip: true });
  return f;
}

function buildIndex(W) {
  var d = PAGES.index;
  var p = pageFrame((isMobile(W) ? 'Mobile' : 'Desktop') + ' · Home', W);
  add(p, navFor('index', W), true);
  add(p, hero(d.hero, W, isMobile(W) ? 720 : 900), true);
  add(p, numbersBar(STATS, W), true);
  add(p, manifesto(W), true);
  add(p, terrainBand(BANDA_HOME[0], BANDA_HOME[1], W), true);

  var head = section('Modalidades · Cabeçalho', W, { padB: 0, gap: 0 });
  head.paddingBottom = 0;
  fill(head, C.black);
  add(head, secHead('Modalidades', 'Um grupo. Três formas de *criar valor* no território.', W, true, { big: true }), true);
  add(p, head, true);

  for (var i = 0; i < MODALIDADES.length; i++) {
    var mod = modalidadeBlock(MODALIDADES[i], W);
    if (i === MODALIDADES.length - 1) sideStroke(mod, C.cream, 0.09, { top: 1, bottom: 1 });
    add(p, mod, true);
  }

  add(p, jornadaSection(W), true);
  add(p, ecossistemaSection(W), true);
  add(p, metodoSection(W), true);
  add(p, scoreSection(W), true);
  add(p, projetosSection(W), true);
  add(p, founderSection(W), true);
  add(p, faqSection(W), true);
  add(p, finalSection(d.final, W), true);
  add(p, rodapeFor('Institucional', W), true);
  return p;
}

function buildModalidade(key, W) {
  var d = PAGES[key];
  var p = pageFrame((isMobile(W) ? 'Mobile' : 'Desktop') + ' · ' + d.titulo, W);
  add(p, navFor(key, W), true);
  add(p, hero(d.hero, W, isMobile(W) ? 660 : 800), true);
  add(p, forwhoBand(d.forwho, W), true);
  add(p, blocosSection(d.blocosTitulo, d.blocos, W, true), true);
  add(p, terrainBand(d.banda[0], d.banda[1], W), true);
  add(p, entregasSection(d.entregasTitulo, d.entregas, W), true);
  add(p, finalSection(d.final, W), true);
  add(p, rodapeFor('Simples', W), true);
  return p;
}

function buildBruno(W) {
  var d = PAGES.bruno;
  var p = pageFrame((isMobile(W) ? 'Mobile' : 'Desktop') + ' · Founder', W);
  add(p, navFor('bruno', W), true);
  add(p, hero(d.hero, W, isMobile(W) ? 720 : 900), true);

  /* Sobre */
  var sobre = section('Sobre', W, { gap: sp(W, 60) });
  fill(sobre, C.cream);
  add(sobre, secHead('Sobre', d.sobre.titulo, W, false), true);
  var grid = F('Colunas', { dir: isMobile(W) ? 'V' : 'H', gap: isMobile(W) ? 40 : 96, w: inner(W), cross: 'MIN' });
  var cw = isMobile(W) ? inner(W) : Math.round((inner(W) - 96) / 2);
  var c1 = F('Coluna 1', { dir: 'V', gap: 20 });
  c1.counterAxisSizingMode = 'FIXED'; c1.resize(cw, 10);
  add(c1, T(d.sobre.col1, { w: 300, size: 14.5, lh: 2.2, color: C.green, name: 'Parágrafo' }), true);
  var c2 = F('Coluna 2', { dir: 'V', gap: 20 });
  c2.counterAxisSizingMode = 'FIXED'; c2.resize(cw, 10);
  add(c2, T(d.sobre.col2, { w: 300, size: 14.5, lh: 2.2, color: C.green, name: 'Parágrafo' }), true);
  var creds = F('Credenciais', { dir: 'V', gap: 13 });
  d.sobre.creds.forEach(function (c) {
    var box = F('Credencial', { dir: 'V', padT: 13 });
    sideStroke(box, C.green, 0.16, { top: 1 });
    add(box, T(c, { w: 300, size: 10.5, ls: 0.26, upper: true, color: C.earth, name: 'Credencial' }), true);
    add(creds, box, true);
  });
  add(c2, creds, true);
  add(grid, c1); add(grid, c2);
  add(sobre, grid, true);
  add(p, sobre, true);

  /* Colapso de crença */
  var colapso = section('Visão · Colapso de Crença', W, { gap: sp(W, 60) });
  fill(colapso, C.black);
  add(colapso, secHead('Visão', d.colapso.titulo, W, true), true);
  var itens = F('Itens', { dir: 'V', w: inner(W), gap: 0 });
  d.colapso.itens.forEach(function (it, idx) {
    var row = F('Crença ' + (idx + 1), { dir: isMobile(W) ? 'V' : 'H', gap: isMobile(W) ? 12 : 40, padY: 34, cross: 'MIN' });
    sideStroke(row, C.cream, 0.09, { top: 1 });
    var old = T(it[0], { serif: true, w: 300, italic: true, size: isMobile(W) ? 17 : 21, lh: 1.6,
                         color: C.sand, opacity: 0.55, name: 'Crença' });
    var neo = T(it[1], { w: 300, size: 14, lh: 2.1, color: C.cream, name: 'Virada' });
    add(row, old); add(row, neo);
    if (!isMobile(W)) {
      old.textAutoResize = 'HEIGHT'; old.resize(Math.round((inner(W) - 40) * 0.4), old.height);
      neo.textAutoResize = 'HEIGHT'; neo.resize(Math.round((inner(W) - 40) * 0.6), neo.height);
    } else {
      try { old.layoutSizingHorizontal = 'FILL'; neo.layoutSizingHorizontal = 'FILL'; } catch (e) {}
    }
    add(itens, row, true);
    if (idx === d.colapso.itens.length - 1) sideStroke(row, C.cream, 0.09, { top: 1, bottom: 1 });
  });
  add(colapso, itens, true);
  add(colapso, gapBox(sp(W, 20)));
  add(colapso, T(d.colapso.custo, { w: 300, size: 15, lh: 2.2, color: C.sand,
                                    maxW: Math.min(inner(W), 760), name: 'Custo Invisível' }));
  add(p, colapso, true);

  add(p, terrainBand(BANDA_HOME[0], BANDA_HOME[1], W), true);

  /* Prova */
  var prova = section('Resultados', W, { gap: sp(W, 60) });
  fill(prova, C.black);
  add(prova, secHead('Resultados', d.prova.titulo, W, true), true);
  var bar = F('Indicadores', { dir: isMobile(W) ? 'V' : 'H', w: inner(W), gap: 0 });
  sideStroke(bar, C.cream, 0.1, { top: 1, bottom: 1 });
  d.prova.stats.forEach(function (s, i) {
    if (i > 0) {
      var line = add(bar, rule(C.cream, 0.1));
      if (isMobile(W)) line.resize(inner(W), 1);
      else { line.resize(1, 10); try { line.layoutSizingVertical = 'FILL'; } catch (e) {} }
    }
    var inst = I('Indicador');
    ov(inst, 'num', s.num);
    ov(inst, 'desc', s.desc);
    add(bar, inst);
    try { inst.layoutSizingHorizontal = 'FILL'; } catch (e) {}
  });
  add(prova, bar, true);
  var nota = add(prova, T(d.prova.nota, { w: 300, size: 11, lh: 1.9, color: C.sand, opacity: 0.65,
                                          align: 'CENTER', maxW: inner(W), name: 'Nota' }), true);
  nota.textAlignHorizontal = 'CENTER';
  add(p, prova, true);

  /* Educação */
  var edu = section('Aprenda', W, { gap: sp(W, 60) });
  fill(edu, C.cream);
  add(edu, secHead('Aprenda', null, W, false), true);
  var eg = F('Colunas', { dir: isMobile(W) ? 'V' : 'H', gap: isMobile(W) ? 44 : 96, w: inner(W), cross: 'MIN' });
  var ew = isMobile(W) ? inner(W) : Math.round((inner(W) - 96) / 2);
  var el = F('Texto', { dir: 'V', gap: 24 });
  el.counterAxisSizingMode = 'FIXED'; el.resize(ew, 10);
  add(el, T(d.edu.titulo, { serif: true, w: 300, size: cl(26, 4, 46, W), lh: 1.35, color: C.green, name: 'Título' }), true);
  d.edu.paras.forEach(function (t) {
    add(el, T(t, { w: 300, size: 14.5, lh: 2.2, color: C.green, name: 'Parágrafo' }), true);
  });
  add(el, botao(d.edu.cta, false, false, W));
  var er = F('Pilares', { dir: 'V', gap: 0 });
  er.counterAxisSizingMode = 'FIXED'; er.resize(ew, 10);
  sideStroke(er, C.green, 0.14, { top: 1 });
  d.edu.pilares.forEach(function (pl) {
    var row = F('Pilar', { dir: 'H', padY: 24, gap: 20, main: 'SPACE_BETWEEN', cross: 'BASELINE' });
    sideStroke(row, C.green, 0.14, { bottom: 1 });
    add(row, T(pl[0], { serif: true, w: 400, size: 20, ls: 0.02, color: C.green, name: 'Pilar' }));
    var v = add(row, T(pl[1], { w: 300, size: 11.5, lh: 1.8, color: C.green, opacity: 0.6, align: 'RIGHT', name: 'Descrição' }));
    v.textAlignHorizontal = 'RIGHT';
    add(er, row, true);
  });
  add(eg, el); add(eg, er);
  add(edu, eg, true);
  add(p, edu, true);

  add(p, finalSection(d.final, W), true);
  add(p, rodapeFor('Simples', W), true);
  return p;
}

/* ----------------------------------------------------------------------------
   11. DOCUMENTAÇÃO DO DESIGN SYSTEM
   -------------------------------------------------------------------------- */

function docTitle(txt, sub) {
  var f = F('Título · ' + txt, { dir: 'V', gap: 12 });
  add(f, T(txt, { serif: true, w: 300, size: 46, lh: 1.2, color: C.cream, name: 'Título' }));
  if (sub) add(f, T(sub, { w: 300, size: 13, lh: 1.9, color: C.sand, maxW: 720, name: 'Apoio' }));
  return f;
}

function swatchGrid() {
  var f = F('Paleta', { dir: 'H', gap: 24 });
  PALETTE.forEach(function (p) {
    var card = F('Swatch · ' + p.name, { dir: 'V', gap: 0, w: 240 });
    var chip = F('Cor', { dir: 'V', w: 240, h: 180, bg: p.hex });
    if (p.hex === C.black) stroke(chip, C.cream, 0.15, 1);
    add(card, chip);
    var info = F('Info', { dir: 'V', gap: 6, padT: 16 });
    add(info, T(p.name, { w: 500, size: 13, ls: 0.06, color: C.cream, name: 'Nome' }));
    add(info, T(p.hex, { w: 300, size: 11, ls: 0.16, color: C.sand, name: 'Hex' }));
    add(info, T(p.uso, { w: 300, size: 11, lh: 1.7, color: C.sand, opacity: 0.7, maxW: 240, name: 'Uso' }));
    add(card, info, true);
    add(f, card);
  });
  return f;
}

function typeSpecimen(styles) {
  var f = F('Tipografia', { dir: 'V', gap: 0, w: 1140 });
  sideStroke(f, C.cream, 0.09, { top: 1 });
  TEXT_SPECS.forEach(function (s) {
    var row = F('Estilo · ' + s.name, { dir: 'H', gap: 40, padY: 30, cross: 'MIN' });
    sideStroke(row, C.cream, 0.09, { bottom: 1 });
    var meta = F('Meta', { dir: 'V', gap: 6, w: 260 });
    add(meta, T(s.name, { w: 500, size: 11, ls: 0.2, upper: true, color: C.cream, name: 'Nome' }), true);
    add(meta, T((s.serif ? SERIF : SANS) + ' · ' + s.w + ' · ' + s.size + 'px · lh ' + s.lh +
                (s.ls ? ' · ls ' + s.ls + 'em' : ''),
      { w: 300, size: 10.5, lh: 1.8, color: C.sand, opacity: 0.75, name: 'Specs' }), true);
    add(row, meta);
    var sample = T(s.sample, {
      serif: s.serif, w: s.w, italic: s.italic, size: s.size, lh: s.lh, ls: s.ls,
      upper: s.upper, color: C.cream, name: 'Amostra'
    });
    add(row, sample);
    sample.textAutoResize = 'HEIGHT';
    sample.resize(1140 - 260 - 40, sample.height);
    try { sample.textStyleId = styles[s.name].id; } catch (e) {}
    add(f, row, true);
  });
  return f;
}

function buildDesignSystem(styles, host) {
  var f = F('Fundamentos', { dir: 'V', w: 1440, bg: C.black, padY: 100, padX: 150, gap: 80 });
  add(f, docTitle('Zion · Design System',
    'Fundamentos do site institucional. Fonte display: ' + SERIF + '. Fonte de texto: ' + SANS +
    '. Todas as cores estão publicadas como estilos (Zion/…) e como variáveis.'), true);
  add(f, splitword('Cores', 1440, true), true);
  add(f, swatchGrid());
  add(f, splitword('Tipografia', 1440, true), true);
  add(f, typeSpecimen(styles), true);
  host.appendChild(f);
  return f;
}

/* ----------------------------------------------------------------------------
   12. MAIN
   -------------------------------------------------------------------------- */

var BUILDERS = {
  index: buildIndex,
  development: function (W) { return buildModalidade('development', W); },
  management: function (W) { return buildModalidade('management', W); },
  collection: function (W) { return buildModalidade('collection', W); },
  bruno: buildBruno
};

var ORDER = ['index', 'development', 'management', 'collection', 'bruno'];

function place(nodes, startX, startY, gap) {
  var x = startX;
  var maxH = 0;
  for (var i = 0; i < nodes.length; i++) {
    nodes[i].x = x;
    nodes[i].y = startY;
    x += nodes[i].width + gap;
    if (nodes[i].height > maxH) maxH = nodes[i].height;
  }
  return { nextX: x, height: maxH };
}

function wrapSection(name, nodes, color) {
  if (!nodes.length) return null;
  var s;
  try { s = figma.createSection(); } catch (e) { return null; }
  s.name = name;
  var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  nodes.forEach(function (n) {
    minX = Math.min(minX, n.x); minY = Math.min(minY, n.y);
    maxX = Math.max(maxX, n.x + n.width); maxY = Math.max(maxY, n.y + n.height);
  });
  var pad = 120;
  s.x = minX - pad; s.y = minY - pad;
  s.resizeWithoutConstraints((maxX - minX) + pad * 2, (maxY - minY) + pad * 2);
  try { s.fills = [solid(color || '#0D0F0E')]; } catch (e) {}
  nodes.forEach(function (n) { s.appendChild(n); });
  return s;
}

async function run(opts) {
  var fonts = await loadFonts();

  var page = figma.createPage();
  page.name = 'Zion · Site';
  try { page.backgrounds = [solid('#0A0C0B')]; } catch (e) {}
  figma.currentPage = page;

  buildColorStyles();
  var styles = buildTextStyles();

  /* Componentes ficam fora da área visível das páginas e depois viram Section */
  var compHost = page;
  var compNodes = buildComponents(compHost);

  var created = [];
  var y = 0;

  /* Fundamentos */
  var dsNodes = [];
  if (opts.sistema) {
    var ds = buildDesignSystem(styles, page);
    ds.x = 0; ds.y = 0;
    dsNodes.push(ds);
    y = ds.height + 320;
  }

  /* Componentes: empilhados em coluna */
  var compY = y;
  var cx = 0;
  compNodes.forEach(function (n) {
    n.x = cx;
    n.y = compY;
    cx += n.width + 120;
  });
  var compH = 0;
  compNodes.forEach(function (n) { compH = Math.max(compH, n.height); });
  y = compY + compH + 320;

  /* Páginas */
  var desktop = [], mobile = [];
  for (var i = 0; i < ORDER.length; i++) {
    var key = ORDER[i];
    if (!opts.paginas[key]) continue;
    if (opts.desktop) {
      figma.ui.postMessage({ type: 'progresso', texto: 'Desenhando ' + PAGES[key].titulo + ' · Desktop' });
      desktop.push(BUILDERS[key](1440));
    }
    if (opts.mobile) {
      figma.ui.postMessage({ type: 'progresso', texto: 'Desenhando ' + PAGES[key].titulo + ' · Mobile' });
      mobile.push(BUILDERS[key](390));
    }
  }

  var deskH = 0;
  if (desktop.length) {
    var r1 = place(desktop, 0, y, 200);
    deskH = r1.height;
  }
  if (mobile.length) {
    place(mobile, 0, y + (deskH ? deskH + 400 : 0), 160);
  }

  /* Sections organizadoras */
  var secs = [];
  if (dsNodes.length) secs.push(wrapSection('00 · Fundamentos', dsNodes));
  if (compNodes.length) secs.push(wrapSection('01 · Componentes', compNodes));
  if (desktop.length) secs.push(wrapSection('02 · Páginas · Desktop 1440', desktop));
  if (mobile.length) secs.push(wrapSection('03 · Páginas · Mobile 390', mobile));

  created = desktop.concat(mobile);
  var focus = secs.filter(Boolean);
  if (focus.length) {
    figma.currentPage.selection = focus;
    figma.viewport.scrollAndZoomIntoView(focus);
  }

  var aviso = '';
  if (fonts.sans !== 'Aventa') {
    aviso = ' · Aventa não está instalada neste Figma; usei ' + fonts.sans +
            ' como fallback (mesma pilha do CSS do site).';
  }
  return 'Site Zion gerado: ' + created.length + ' frame(s) e ' + Object.keys(REG).length +
         ' componentes.' + aviso;
}

/* ---- ponte com a UI ----------------------------------------------------- */

figma.showUI(__html__, { width: 380, height: 560, themeColors: false });

figma.ui.onmessage = async function (msg) {
  if (msg.type === 'cancelar') { figma.closePlugin(); return; }
  if (msg.type !== 'gerar') return;
  try {
    var resultado = await run(msg.opts);
    figma.closePlugin(resultado);
  } catch (err) {
    console.error(err);
    figma.ui.postMessage({ type: 'erro', texto: String(err && err.message ? err.message : err) });
    figma.notify('Erro ao gerar: ' + (err && err.message ? err.message : err), { error: true, timeout: 8000 });
  }
};
