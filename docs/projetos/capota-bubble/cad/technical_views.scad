// ZG-CAP-02 · technical_views.scad · projecoes 2D para exportar em DXF/SVG
// Uso:  openscad -D VIEW=\"frontal\" -o frontal.dxf technical_views.scad
include <parameters.scad>
use <bubble.scad>
use <canopy.scad>
use <mechanism.scad>

VIEW = "frontal";   // frontal | lateral | superior | traseira

module modelo(){ bubble(); canopy(ALPHA); mechanism(ALPHA); }

if(VIEW=="superior")      projection(cut=false) modelo();
else if(VIEW=="frontal")  projection(cut=false) rotate([-90,0,0]) modelo();
else if(VIEW=="traseira") projection(cut=false) rotate([-90,0,180]) modelo();
else if(VIEW=="lateral")  projection(cut=false) rotate([-90,0,-90]) modelo();
else if(VIEW=="corte_t")  projection(cut=true)  rotate([-90,0,0]) modelo();
else if(VIEW=="corte_l")  projection(cut=true)  rotate([-90,0,-90]) modelo();
