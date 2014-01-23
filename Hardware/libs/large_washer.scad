////By Glen Chung, 2013.
//Dual licenced under Creative Commons Attribution-Share Alike 3.0 and LGPL2 or later

include <MCAD/units.scad>
include <MCAD/materials.scad>

LARGE_WASHER_D1 = 0;  //Inner diameter
LARGE_WASHER_D2 = 1;  //Outer diameter
LARGE_WASHER_H  = 2;  //Height

// Large Washer dimensions
//  model == X   ?   [      D1,       D2,       H]:
function largeWasherDimensions(model=3) =
    model == 3   ?   [  3.2*mm,   9.0*mm,  0.8*mm]:
    model == 4   ?   [  4.3*mm,  12.0*mm,  1.0*mm]:
    model == 5   ?   [  5.3*mm,  15.0*mm,  1.0*mm]:
    model == 6   ?   [  6.4*mm,  18.0*mm,  1.6*mm]:
    model == 8   ?   [  8.4*mm,  24.0*mm,  2.0*mm]:
    model == 10  ?   [ 10.5*mm,  30.0*mm,  2.5*mm]:
    model == 12  ?   [ 13.0*mm,  37.0*mm,  3.0*mm]:
    model == 16  ?   [ 17.0*mm,  50.0*mm,  3.0*mm]:
    model == 20  ?   [ 21.0*mm,  60.0*mm,  4.0*mm]:
    model == 24  ?   [ 25.0*mm,  72.0*mm,  5.0*mm]:
    model == 30  ?   [ 33.0*mm,  92.0*mm,  6.0*mm]:
  /*model == 36  ?*/ [ 39.0*mm, 110.0*mm,  8.0*mm];

function largeWasher_D1(model) = largeWasherDimensions(model)[LARGE_WASHER_D1];
function largeWasher_D2(model) = largeWasherDimensions(model)[LARGE_WASHER_D2];
function largeWasher_H(model)  = largeWasherDimensions(model)[LARGE_WASHER_H];

module large_washer(dia=3)
{
  d1 = largeWasher_D1(dia);
  d2 = largeWasher_D2(dia);
  h  = largeWasher_H(dia);
  difference()
  {
    cylinder(r=d2/2,h=h);
    translate([0,0,-h/2]) cylinder(r=d1/2,h=h*2);
  }
}

//examples
//large_washer(); //m3
//large_washer(5); //m5