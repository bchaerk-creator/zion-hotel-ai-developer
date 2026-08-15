// ZG-CAP-02 · canopy.scad · casca: arcos transversais, longarinas e tecido
include <parameters.scad>

// arco de tubo no plano XY, raio R, de a0 a a1 graus
module arc_tube(R, od, wt, a0, a1, steps=120){
  st = (a1-a0)/steps;
  for(i=[0:steps-1]){
    a = a0 + st*i;  b = a0 + st*(i+1);
    hull(){
      translate([R*cos(a), R*sin(a), 0]) sphere(d=od, $fn=20);
      translate([R*cos(b), R*sin(b), 0]) sphere(d=od, $fn=20);
    }
  }
}

// cunha solida entre eps=0 e eps=ANG em torno do eixo X
module wedge_x(ang, L){
  intersection(){
    translate([-L,-L,0]) cube([2*L,2*L,L]);
    rotate([ang,0,0]) translate([-L,-L,-L]) cube([2*L,2*L,L]);
  }
}

// ARCO TRANSVERSAL k (meridiano). eps = elevacao do plano do arco.
module rib(eps){
  translate([0,0,BUBBLE_ZC]) rotate([eps,0,0])
    arc_tube(SHELL_R, RIB_OD, RIB_WT, RIB_END_THETA, 180-RIB_END_THETA);
}

// LONGARINA j (paralelo). theta = estacao angular a partir do polo +X.
module purlin(theta, eps1, eps2){
  rho = SHELL_R*sin(theta);
  translate([SHELL_R*cos(theta), 0, BUBBLE_ZC]) rotate([0,-90,0])
    arc_tube(rho, PURLIN_OD, PURLIN_WT, 90-eps2, 90-eps1);
}

module structure(eps1=EPS_1, eps2=EPS_2){
  color("Silver"){
    for(k=[0:N_RIBS-1])
      rib(eps1 + (eps2-eps1)*k/(N_RIBS-1));
    for(j=[0:N_PURLINS-1]){
      x = -FABRIC_HALF_W + 2*FABRIC_HALF_W*j/(N_PURLINS-1);
      purlin(acos(x/SHELL_R), eps1, eps2);
    }
  }
}

module fabric(eps1=EPS_1, eps2=EPS_2){
  color("Tan", 0.92)
  intersection(){
    translate([0,0,BUBBLE_ZC])
      difference(){ sphere(r=SHELL_R+FABRIC_T); sphere(r=SHELL_R); }
    translate([0,0,BUBBLE_ZC]) rotate([eps1,0,0]) wedge_x(eps2-eps1, SHELL_R*1.4);
    translate([-FABRIC_HALF_W,-SHELL_R*2,-SHELL_R*2])
      cube([CANOPY_WIDTH, SHELL_R*4, SHELL_R*4]);
  }
}

// conjunto da casca, ja girado pelo angulo de abertura
module canopy(alpha=ALPHA){
  rotate([alpha,0,0]) translate([0,0,-BUBBLE_ZC]) translate([0,0,BUBBLE_ZC]){
    if(SHOW_STRUCT) structure();
    if(SHOW_FABRIC) fabric();
  }
}
