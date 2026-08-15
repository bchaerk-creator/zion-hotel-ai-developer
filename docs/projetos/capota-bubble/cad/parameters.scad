// =====================================================================
// ZG-CAP-02  ·  CAPOTA RETRATIL "CHAPEU" PARA BUBBLE GLAMPING ZION
// parameters.scad  ·  todas as variaveis do projeto. Unidades: MILIMETROS.
// Projeto executivo preliminar para prototipo. Nao certificado.
// =====================================================================

// ---------------------------------------------------------------- BOLHA
BUBBLE_DIAMETER = 6000;   // maior largura da bolha
BUBBLE_HEIGHT   = 3600;   // apice acima do piso acabado

// Derivados: a bolha e uma esfera truncada pelo piso.
// Maior largura = 2R, apice = zc + R.
BUBBLE_R  = BUBBLE_DIAMETER/2;                 // 3000
BUBBLE_ZC = BUBBLE_HEIGHT - BUBBLE_R;          // 600  <-- centro da esfera
BUBBLE_BASE_R = sqrt(BUBBLE_R*BUBBLE_R - BUBBLE_ZC*BUBBLE_ZC); // 2939

// ---------------------------------------------------------------- FOLGA
CLEARANCE = 150;          // folga radial constante capota <-> membrana (100..150)
SHELL_R   = BUBBLE_R + CLEARANCE;              // 3150

// --------------------------------------------------------------- PIVO
// REGRA DE OURO DO PROJETO:
// Uma casca rigida so mantem folga constante contra uma esfera se o eixo de
// rotacao PASSAR PELO CENTRO DESSA ESFERA. Qualquer outra altura faz o
// envelope da bolha variar com o angulo e a casca colide ou tem de ser
// gigante. Por isso PIVOT_HEIGHT e DERIVADO, nao arbitrado.
PIVOT_HEIGHT = BUBBLE_ZC;                      // 600
PIVOT_HALF_SPAN = SHELL_R;                     // 3150 - os arcos convergem no polo

// --------------------------------------------------------- ARCO COBERTO
EPS_1 = 40;               // borda dianteira da capota, em graus de elevacao
EPS_2 = 130;              // borda traseira
// Curso: limitado pelo solo. A borda traseira nao pode descer abaixo de
// GROUND_GAP. asin((zc - GROUND_GAP)/SHELL_R) da a folga angular extra.
GROUND_GAP = 100;
ALPHA_MAX = 180 + asin((BUBBLE_ZC - GROUND_GAP)/SHELL_R) - EPS_2;  // ~59
ALPHA_WORK = 55;          // curso homologado, com reserva
ALPHA = 0;                // 0 = FECHADA ; ALPHA_WORK = ABERTA

// ------------------------------------------------------------ ESTRUTURA
N_RIBS   = 5;             // arcos transversais (meridianos)
RIB_OD   = 50;            // tubo circular de aluminio - diametro externo
RIB_WT   = 3;             // espessura de parede
PURLIN_OD = 32;           // longarinas (paralelos)
PURLIN_WT = 2;
N_PURLINS = 5;            // longarinas por lado incluindo a central

RIB_END_THETA = 6;        // arcos terminam a 6 graus do polo, no cubo-aranha
FABRIC_HALF_W = 2900;     // meia largura util do tecido (CANOPY_WIDTH/2)
CANOPY_WIDTH  = 2*FABRIC_HALF_W;               // 5800

// -------------------------------------------------------------- MECANISMO
SHAFT_D    = 30;          // eixo inox 304
HUB_D      = 700;         // cubo-aranha, chapa 9,5 mm
PED_OFFSET = 250;         // pedestal afastado do polo, para fora
PED_X      = PIVOT_HALF_SPAN + PED_OFFSET;     // 3400
PED_SECTION= [120,120];   // coluna do pedestal
BASE_PLATE = [300,300,12];
CRANK_R    = 500;         // braco de acionamento no cubo
CRANK_PHASE= 200;         // angulo do braco em relacao a bissetriz da casca

// ACT_B = ancoragem fixa do atuador, coordenadas (y,z) RELATIVAS ao pivo
ACT_BY = -820;
ACT_BZ = -260;

// ---------------------------------------------------------------- TECIDO
FABRIC_T   = 1.2;         // espessura aparente para o modelo 3D
FABRIC_GSM = 600;         // g/m2

// --------------------------------------------------------------- RENDER
$fn = 64;
SHOW_BUBBLE  = true;
SHOW_FABRIC  = true;
SHOW_STRUCT  = true;
SHOW_MECH    = true;
SHOW_GROUND  = true;

// ------------------------------------------------------------- VERIFICA
assert(PIVOT_HEIGHT == BUBBLE_ZC,
  "PIVOT_HEIGHT precisa coincidir com o centro da esfera da bolha, senao a casca colide.");
assert(ALPHA <= ALPHA_MAX + 0.001,
  "ALPHA acima do curso geometrico: a borda traseira desce abaixo do piso.");
assert(FABRIC_HALF_W < SHELL_R,
  "Largura do tecido maior que o vao entre polos.");
