// ZG-CAP-02 · mechanism.scad · pedestal, mancal, eixo, cubo-aranha,
//                              braco de acionamento, atuador e limitadores
include <parameters.scad>

module tube(od, wt, len){
  difference(){ cylinder(d=od, h=len); translate([0,0,-1]) cylinder(d=od-2*wt, h=len+2); }
}

module pedestal(sx){
  color("DarkSlateGray"){
    // placa de base + chumbadores
    translate([sx*PED_X-BASE_PLATE[0]/2, -BASE_PLATE[1]/2, 0]) cube(BASE_PLATE);
    for(a=[-1,1], b=[-1,1])
      translate([sx*PED_X + a*110, b*110, -180]) cylinder(d=16, h=200, $fn=16);
    // coluna
    translate([sx*PED_X-PED_SECTION[0]/2, -PED_SECTION[1]/2, BASE_PLATE[2]])
      cube([PED_SECTION[0], PED_SECTION[1], PIVOT_HEIGHT-BASE_PLATE[2]]);
    // caixa do mancal
    translate([sx*PED_X, 0, PIVOT_HEIGHT]) rotate([0,90,0])
      translate([0,0,-45]) cylinder(d=110, h=90, center=false);
  }
}

module shaft(sx){
  color("Gainsboro")
    translate([sx*(PED_X+60), 0, PIVOT_HEIGHT]) rotate([0,-90*sx,0])
      cylinder(d=SHAFT_D, h=PED_OFFSET+140);
}

// cubo-aranha: chapa com 5 encaixes radiais, um por arco
module hub(sx, alpha=ALPHA){
  color("Gainsboro")
  translate([sx*PIVOT_HALF_SPAN, 0, PIVOT_HEIGHT]) rotate([alpha,0,0]){
    rotate([0,90,0]) cylinder(d=90, h=60, center=true);
    for(k=[0:N_RIBS-1]){
      e = EPS_1 + (EPS_2-EPS_1)*k/(N_RIBS-1);
      rotate([e-90,0,0]) translate([0,0,0])
        rotate([90,0,0]) translate([-9.5/2,-HUB_D/2,-30])
          cube([9.5, HUB_D/2, 60]);
    }
  }
}

// braco de acionamento (manivela) solidario ao cubo
module crank(sx, alpha=ALPHA){
  e = (EPS_1+EPS_2)/2 + CRANK_PHASE + alpha;
  color("Goldenrod")
  translate([sx*PIVOT_HALF_SPAN, 0, PIVOT_HEIGHT]) rotate([0,90,0])
    linear_extrude(height=12, center=true)
      polygon([[0,-40],[0,40],[CRANK_R*sin(e), CRANK_R*cos(e)]]);
}

function crank_pin(alpha) =
  let(e = (EPS_1+EPS_2)/2 + CRANK_PHASE + alpha)
    [CRANK_R*cos(e), CRANK_R*sin(e)];   // (y,z) relativo ao pivo

module actuator(sx, alpha=ALPHA){
  k = crank_pin(alpha);
  b = [ACT_BY, ACT_BZ];
  L = norm(k-b);
  ang = atan2(k[1]-b[1], k[0]-b[0]);
  color("DimGray")
  translate([sx*(PIVOT_HALF_SPAN-90), b[0], PIVOT_HEIGHT+b[1]])
    rotate([0,90,0]) rotate([0,0,ang-90])
      translate([0,0,0]) rotate([-90,0,0]) cylinder(d=45, h=L);
}

// limitadores mecanicos: batentes solidos no pedestal
module stops(sx){
  color("Firebrick"){
    e0 = (EPS_1+EPS_2)/2 + CRANK_PHASE;
    e1 = e0 + ALPHA_WORK;
    for(e=[e0,e1])
      translate([sx*(PIVOT_HALF_SPAN-40), (CRANK_R+70)*cos(e), PIVOT_HEIGHT+(CRANK_R+70)*sin(e)])
        rotate([0,90,0]) cylinder(d=60, h=40, center=true);
  }
}

module mechanism(alpha=ALPHA){
  for(sx=[-1,1]){
    pedestal(sx); shaft(sx); hub(sx,alpha); crank(sx,alpha);
    actuator(sx,alpha); stops(sx);
  }
}
