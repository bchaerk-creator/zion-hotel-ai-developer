// ZG-CAP-02 · assembly.scad · conjunto geral
// Uso:  openscad -D ALPHA=27 -o vista.png assembly.scad
include <parameters.scad>
use <bubble.scad>
use <canopy.scad>
use <mechanism.scad>

if(SHOW_GROUND) ground();
if(SHOW_BUBBLE) bubble();
canopy(ALPHA);
if(SHOW_MECH) mechanism(ALPHA);
