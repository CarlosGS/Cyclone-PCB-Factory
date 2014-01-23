//By Glen Chung, 2013.
//Dual licenced under Creative Commons Attribution-Share Alike 3.0 and LGPL2 or later

include <MCAD/units.scad>
include <MCAD/materials.scad>

LINEAR_BEARING_dr = 0;  //Inscribed circle
LINEAR_BEARING_D  = 1;  //Outer diameter
LINEAR_BEARING_L  = 2;  //Length
LINEAR_BEARING_B  = 3;  //Outer locking groove B
LINEAR_BEARING_D1 = 4;  //Outer locking groove D1
LINEAR_BEARING_W  = 5;  //W


// Common bearing names
LinearBearing = "LM8UU";

// Linear Bearing dimensions
//  model == "XXXXX"   ?   [    dr,      D,      L,        B,      D1,       W]:
function linearBearingDimensions(model) =
    model == "LM3UU"   ?   [  3*mm,   7*mm,  10*mm,   0.0*mm,   0.0*mm, 0.00*mm]:
    model == "LM4UU"   ?   [  4*mm,   8*mm,  12*mm,   0.0*mm,   0.0*mm, 0.00*mm]:
    model == "LM5UU"   ?   [  5*mm,  10*mm,  15*mm,  10.2*mm,   9.6*mm, 1.10*mm]:
    model == "LM6UU"   ?   [  6*mm,  12*mm,  19*mm,  13.5*mm,  11.5*mm, 1.10*mm]:
    model == "LM8SUU"  ?   [  8*mm,  15*mm,  17*mm,  11.5*mm,  14.3*mm, 1.10*mm]:
    model == "LM10UU"  ?   [ 10*mm,  19*mm,  29*mm,  22.0*mm,  18.0*mm, 1.30*mm]:
    model == "LM12UU"  ?   [ 12*mm,  21*mm,  30*mm,  23.0*mm,  20.0*mm, 1.30*mm]:
    model == "LM13UU"  ?   [ 13*mm,  23*mm,  32*mm,  23.0*mm,  22.0*mm, 1.30*mm]:
    model == "LM16UU"  ?   [ 16*mm,  28*mm,  37*mm,  26.5*mm,  27.0*mm, 1.60*mm]:
    model == "LM20UU"  ?   [ 20*mm,  32*mm,  42*mm,  30.5*mm,  30.5*mm, 1.60*mm]:
    model == "LM25UU"  ?   [ 25*mm,  40*mm,  59*mm,  41.0*mm,  38.0*mm, 1.85*mm]:
    model == "LM30UU"  ?   [ 30*mm,  45*mm,  64*mm,  44.5*mm,  43.0*mm, 1.85*mm]:
    model == "LM35UU"  ?   [ 35*mm,  52*mm,  70*mm,  49.5*mm,  49.0*mm, 2.10*mm]:
    model == "LM40UU"  ?   [ 40*mm,  60*mm,  80*mm,  60.5*mm,  57.0*mm, 2.10*mm]:
    model == "LM50UU"  ?   [ 50*mm,  80*mm, 100*mm,  74.0*mm,  76.5*mm, 2.60*mm]:
    model == "LM60UU"  ?   [ 60*mm,  90*mm, 110*mm,  85.0*mm,  86.5*mm, 3.15*mm]:
    model == "LM80UU"  ?   [ 80*mm, 120*mm, 140*mm, 105.5*mm, 116.0*mm, 4.15*mm]:
    model == "LM100UU" ?   [100*mm, 150*mm, 150*mm, 125.5*mm, 145.0*mm, 4.15*mm]:
  /*model == "LM8UU"   ?*/ [  8*mm,  15*mm,  24*mm,  17.5*mm,  14.3*mm, 1.10*mm];


function linearBearing_dr(model) = linearBearingDimensions(model)[LINEAR_BEARING_dr];
function linearBearing_D(model)  = linearBearingDimensions(model)[LINEAR_BEARING_D];
function linearBearing_L(model)  = linearBearingDimensions(model)[LINEAR_BEARING_L];
function linearBearing_B(model)  = linearBearingDimensions(model)[LINEAR_BEARING_B];
function linearBearing_D1(model) = linearBearingDimensions(model)[LINEAR_BEARING_D1];
function linearBearing_W(model)  = linearBearingDimensions(model)[LINEAR_BEARING_W];

module linearBearing(pos=[0,0,0], angle=[0,0,0], model=LinearBearing,
                material=Steel, sideMaterial=BlackPaint) {
  dr = linearBearing_dr(model);
  D  = linearBearing_D(model);
  L  = linearBearing_L(model);
  B  = linearBearing_B(model);
  D1 = linearBearing_D1(model);
  W  = linearBearing_W(model);

  innerRim = dr + (D - dr) * 0.2;
  outerRim = D - (D - dr) * 0.2;
  midSink = W/4;

  translate(pos) rotate(angle) union() {
    color(material)
      difference() {
        // Basic ring
        Ring([0,0,0], D, dr, L, material, material);

        if(W) {
          // Side shields
          Ring([0,0,-epsilon], outerRim, innerRim, L*epsilon+midSink, sideMaterial, material);
          Ring([0,0,L-midSink-epsilon], outerRim, innerRim, L*epsilon+midSink, sideMaterial, material);
          //Outer locking groove
          Ring([0,0,(L-B)/2], D+epsilon, outerRim+W/2, W, material, material);
          Ring([0,0,L-(L-B)/2], D+epsilon, outerRim+W/2, W, material, material);
        }
      }
      if(W)
        Ring([0,0,midSink], D-L*epsilon, dr+L*epsilon, L-midSink*2, sideMaterial, sideMaterial);
  }

  module Ring(pos, od, id, h, material, holeMaterial) {
    color(material) {
      translate(pos)
        difference() {
          cylinder(r=od/2, h=h,  $fn = 100);
          color(holeMaterial)
            translate([0,0,-10*epsilon])
              cylinder(r=id/2, h=h+20*epsilon,  $fn = 100);
        }
    }
  }

}


//examples
//linearBearing(model="LM8UU");
//linearBearing(model="LM10UU");
