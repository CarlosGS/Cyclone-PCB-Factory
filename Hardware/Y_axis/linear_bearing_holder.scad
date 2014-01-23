
// LM8UU bushing holder modified for its use in Cyclone PCB Factory
// Modified to have only one center screw

// Derived by Carlosgs from:

// LM8UU bushing holder
// http://www.thingiverse.com/thing:23041 by thantik
// Inspired/derived from:

//http://www.thingiverse.com/thing:14942
//Which is derived from:
// http://www.thingiverse.com/thing:14814
//And is a drop-in replacement for:
//http://www.thingiverse.com/thing:10287

include <MCAD/materials.scad>
include <MCAD/metric_fastners.scad>
use <../libs/linear_bearing.scad>

// screw/nut dimensions
screw_dia = 4;
nut_dia = 8.5;
nut_height=2;

// main body dimensions
body_width = 20;
gap_width = 14;
body_height = 16;
body_length=23;
LM8UU_dia = 15.0;
screw_elevation = body_height-1.5;

//mounting plate dimensions
plate_height = 4;
plate_length=body_length;
plate_width=body_width+11;
screw_space_x = -14.5*2;
screw_space_y = 0;

module mount_plate()
{
	difference()
	{
		//bottom plate
		translate([-plate_width+body_width/2,-plate_length/2,-3])
			cube([plate_width,plate_length,plate_height]);

		//screw holes
		translate([screw_space_x/2,screw_space_y/2,-8.1])
			cylinder(r=screw_dia/2, h=plate_height+10, $fn=20);
//		translate([-screw_space_x/2,-screw_space_y/2,-8.1])
//			cylinder(r=screw_dia/2, h=plate_height+1, $fn=20);

		//nut traps


	}
}

module lm8uu_bearing_holder(with_extra_parts=false, exploded=false) {
	intersection() {
     rotate([90,0,90])
      difference()
		{
			union()
			{
				mount_plate();
		
				translate([-body_width/2,-body_length/2,0])
					cube([body_width,body_length,body_height]);
			}
		
			// bushing hole
			translate([0,0,LM8UU_dia/2+2])
				rotate([90,0,0])
					cylinder(r=LM8UU_dia/2, h=body_length+0.1, center=true, $fn=40);
		
			// top gap
			translate([0,0,20])
				cube([gap_width-1,body_length+0.1,20],center=true);
		}
	   rotate([90,45,90])
	     //cube([plate_width+3,plate_width+3,100],center=true);
	     cylinder(r=(plate_width+10)/2,h=100,center=true,$fn=8);
	}
  if(with_extra_parts)
    lm8uu_bearing_holder_extras(exploded_distance=(exploded?1.3*linearBearing_L("LM8UU"):0));

  module lm8uu_bearing_holder_extras(exploded_distance=0) {
    echo("Non-Plastic Parts, 1, Linear Bearing LM8UU for lm8uu_bearing_holder");
    rotate([90,0,90]) translate([0,0,LM8UU_dia/2+2]) rotate([90,0,0])
      translate([0,0,exploded_distance])
        linearBearing(pos=[0,0,-linearBearing_L("LM8UU")/2], model="LM8UU");

    screw_size = 3.5;
    screw_length = 13;
    echo("Non-Plastic Parts, 1, Self Tapping Screw 3.5 x 13 mm to attach lm8uu_bearing_holder on work bed");
    translate([plate_height-3+0.2+0.5*exploded_distance,screw_space_x/2,0]) rotate([0,-90,0])
      color(Steel) csk_bolt(screw_size, screw_length);
  }

}



lm8uu_bearing_holder();

