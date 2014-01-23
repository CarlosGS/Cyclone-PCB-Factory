/*
 * Bearing model.
 * 
 * Originally by Hans Häggström, 2010.
 * Dual licenced under Creative Commons Attribution-Share Alike 3.0 and LGPL2 or later
 */

include <units.scad>
include <materials.scad>

// Example, uncomment to view
//bearing_test();
//bearing_hole_test();

module bearing_test(){
    bearing();
    bearing(pos=[5*cm, 0,0], angle=[90,0,0]);
    bearing(pos=[-2.5*cm, 0,0], model=Bearing688);
}

module bearing_hole_test(){
    difference(){
      translate([0, 0, 3.5]) cube(size=[30, 30, 7-10*epsilon], center=true);
      bearing(outline=true);
    }
}

BEARING_INNER_DIAMETER = 0;
BEARING_OUTER_DIAMETER = 1;
BEARING_WIDTH = 2;

Bearing608 = [8*mm, 22*mm, 7*mm];
Bearing627 = [7*mm, 22*mm, 7*mm];
Bearing688 = [8*mm, 16*mm, 5*mm];
SkateBearing = Bearing608;

function bearingWidth(model) = model[BEARING_WIDTH];
function bearingInnerDiameter(model) = model[BEARING_INNER_DIAMETER];
function bearingOuterDiameter(model) = model[BEARING_OUTER_DIAMETER];

module bearing(pos=[0,0,0], angle=[0,0,0], model=SkateBearing, outline=false,
                material=Steel, sideMaterial=Brass) {
  w = bearingWidth(model);
  innerD = outline==false ? bearingInnerDiameter(model) : 0;
  outerD = bearingOuterDiameter(model);
  
  innerRim = innerD + (outerD - innerD) * 0.2;
  outerRim = outerD - (outerD - innerD) * 0.2;
  midSink = w * 0.1;

  translate(pos) rotate(angle) union() {
    color(material)  
      difference() {
        // Basic ring
        Ring([0,0,0], outerD, innerD, w, material, material);

        if (outline==false) {
          // Side shields
          Ring([0,0,-epsilon], outerRim, innerRim, epsilon+midSink, sideMaterial, material);
          Ring([0,0,w-midSink], outerRim, innerRim, epsilon+midSink, sideMaterial, material);
        }
      }
  }

  module Ring(pos, od, id, h, material, holeMaterial) {
    color(material) {
      translate(pos)
        difference() {
          cylinder(r=od/2, h=h,  $fs = 0.01);
          color(holeMaterial) 
            translate([0,0,-10*epsilon]) 
              cylinder(r=id/2, h=h+20*epsilon,  $fs = 0.01);
        }
    }
  }
      
}


