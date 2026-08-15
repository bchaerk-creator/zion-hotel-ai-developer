// ZG-CAP-02 · bubble.scad · geometria de referencia da Bubble (nao e peca)
include <parameters.scad>

module bubble(){
  color("LightSteelBlue", 0.18)
  difference(){
    translate([0,0,BUBBLE_ZC]) sphere(r = BUBBLE_R);
    translate([-BUBBLE_R*2, -BUBBLE_R*2, -BUBBLE_R*2])
      cube([BUBBLE_R*4, BUBBLE_R*4, BUBBLE_R*2]);   // corta no piso
  }
}

module ground(){
  color("DimGray", 0.35)
    translate([0,0,-30]) cylinder(h=30, r=BUBBLE_R*1.8, $fn=96);
}
