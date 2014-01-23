// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
 /*
 * August 2013 changes to design top-part mounting screw at same side as bottom-part.
 * also started introduced 2nd spindle diameter for a-symmetrical spindles. this is not working yet.
 * by Harry Binnema. 
 */

include <MCAD/stepper.scad>
include <MCAD/bearing.scad>
include <MCAD/metric_fastners.scad>
include <MCAD/nuts_and_bolts.scad>
include <MCAD/materials.scad>
use <../libs/obiscad/bcube.scad>
use <../libs/build_plate.scad>
use <../libs/Write/Write.scad>
use <../libs/linear_bearing.scad>
use <../libs/rod.scad>
use <motor_gear.scad>
use <rod_gear.scad>

spindle_motor_diam_top = 26*2;
spindle_motor_diam = 26*2;
spindle_holder_thickness = 8;
spindle_holder_distance = linearBearing_L("LM8UU")*2+3;
spindle_motor_length = 90;

bottom_thickness = 4;
base_width = 20;
base_length = 25;
base_screw_diameter = 5;

motor_width = 43;
motor_length = 49; // not used
motor_screw_distance = 31.3;
motor_center_diameter = 23;

motor_adjust_margin = 3;

motor_screw_diameter = 3.7;
motor_screw_head_diameter = 8;

bearing_diameter = 22.4;
M8_rod_diameter = 8.2;

axis_distance = 21;

wall_thickness = 9;
wall_height = motor_width;
wall_width = 54;

idler_width = 25;

lbearing_holder_length = 23*2;

Z_threaded_pos = motor_width/2+axis_distance;

Z_smooth_rods_sep = 55;

textHscale = 0.8;
textThickness = 1;

LM8UU_dia = 15.4;

Cyclone_Nema17 = [
                [NemaModel, 17],
                [NemaLengthShort, 33*mm],
                [NemaLengthMedium, 39*mm],
                [NemaLengthLong, 48*mm],
                [NemaSideSize, 42.30*mm],
                [NemaDistanceBetweenMountingHoles, 31.0*mm],
                [NemaMountingHoleDiameter, 4*mm],
                [NemaMountingHoleDepth, 5.5*mm], //actual is 4.5mm, motor() module is generating 1mm short
                [NemaMountingHoleLip, -1*mm],
                [NemaMountingHoleCutoutRadius, 0*mm],
                [NemaEdgeRoundingRadius, 7*mm],
                [NemaRoundExtrusionDiameter, 22*mm],
                [NemaRoundExtrusionHeight, 1.9*mm],
                [NemaAxleDiameter, 5*mm],
                [NemaFrontAxleLength, 24*mm],
                [NemaBackAxleLength, 15*mm],
                [NemaAxleFlatDepth, 0.5*mm],
                [NemaAxleFlatLengthFront, 15*mm],
                [NemaAxleFlatLengthBack, 14*mm]
         ];

module dummySpindle(length=0) {
	translate([0,0,-length]) {
		translate([0,0,spindle_motor_length-5]) color([0.95,0.95,0.95]) cylinder(r=26,h=30,$fn=60);
		translate([0,0,spindle_motor_length-10]) color([0.95,0.95,0.95]) cylinder(r=10/2,h=5,$fn=60);
		translate([0,0,-10]) color([0.6,0.6,0.6]) cylinder(r=26,h=spindle_motor_length,$fn=60);
		translate([0,0,-40]) color([0.9,0.9,0.9]) cylinder(r=15/2,h=40,$fn=60);
		translate([0,0,-50]) color([0.4,0.4,0.4]) cylinder(r=20/2,h=10,$fn=60);
		translate([0,0,-50-20]) color([0.9,0.9,0.9]) cylinder(r1=1/2,r2=3/2,h=20,$fn=60);
	}
}

// Derived from Spindle mount for ShapeOko by Misan (http://www.thingiverse.com/thing:26740)
module spindle_holder_holes(length,spindiam, basediam,top_part) {
	$fn=6;

	translate([20,8,-0.05]) cylinder(r=basediam/2,h=length+2,$fn=60);
	translate([-20,8,-0.05]) cylinder(r=basediam/2,h=length+2,$fn=60);
	if (top_part){
		translate([0,38,0]) rotate([0,0,0]) {
		translate([0,0,-0.05]) cylinder(r=spindiam/2,h=length+2,$fn=60);
		translate([0,-3,-0.01]) cube([90,3,length+2]);
		translate ([spindiam/2+15,15,length/2]) rotate([90,0,0]) cylinder(r=2,h=30);
		translate ([spindiam/2+15,-10.5,length/2]) rotate([90,0,0]) cylinder(r=3.5,h=4,$fn=6);
		}		
		}
	else
		{
		translate([0,38,0]) rotate([0,0,180]) {
		translate([0,0,-0.05]) cylinder(r=spindiam/2,h=length+2,$fn=60);
		translate([0,0,-0.01]) cube([90,3,length+2]);
		translate ([spindiam/2+15,20,length/2]) rotate([90,0,0]) cylinder(r=2,h=30);
		translate ([spindiam/2+15,15,length/2]) rotate([90,0,0]) cylinder(r=3.5,h=4,$fn=6);
		}
		}
}



module motorHolesZ() {
    // Hole for the motor shaft
    hull() {
      translate([0,motor_adjust_margin/2,0])
        cylinder(r=motor_center_diameter/2,h=10*wall_thickness,center=true,$fn=40);
      translate([0,-motor_adjust_margin/2,0])
        cylinder(r=motor_center_diameter/2,h=10*wall_thickness,center=true,$fn=40);
    }

    // Hole for the screwdriver
    translate([0,-wall_width/2,wall_thickness/2]) rotate([0,90,90]) bcube([2*(wall_thickness-5),5,wall_height],cr=1);

    // Screws for holding the motor
    for(i=[-1,1]) for(j=[-1,1])
    translate([i*motor_screw_distance/2,j*motor_screw_distance/2,2.5-wall_thickness/2]) {
      hull() {
        translate([0,motor_adjust_margin/2,0])
          cylinder(r=motor_screw_diameter/2,h=10*wall_thickness,center=true,$fn=40);
        translate([0,-motor_adjust_margin/2,0])
          cylinder(r=motor_screw_diameter/2,h=10*wall_thickness,center=true,$fn=40);
      }
      hull() {
        translate([0,motor_adjust_margin/2,0])
          cylinder(r=motor_screw_head_diameter/2,h=10*wall_thickness,center=false,$fn=40);
        translate([0,-motor_adjust_margin/2,0])
          cylinder(r=motor_screw_head_diameter/2,h=10*wall_thickness,center=false,$fn=40);
      }
    }
}


module motor_stand_holes_Z() {
//difference() {
//  translate([wall_height/2,wall_width/2,wall_thickness/2])
//    bcube([wall_height,wall_width,wall_thickness],cr=4,cres=10);

  // Position relative to motor shaft
  translate([motor_width/2,motor_width/2,wall_thickness/2]) {
    motorHolesZ();

    // Bearing holes
    rotate([0,0,0]) translate([0,axis_distance,0]) {
		hull() {
      	cylinder(r=(M8_rod_diameter*2)/2,h=10*wall_thickness,center=true,$fn=40);
			translate([0,-axis_distance,0])
				cylinder(r=(M8_rod_diameter*2)/2,h=10*wall_thickness,center=true,$fn=40);
		}
      cylinder(r=bearing_diameter/2,h=10*wall_thickness,center=false,$fn=60);

    }

  } // End of translate relative to motor shaft
//} // End of difference
}


module linearBearingHolderZ(h=10) {
	translate([0,0,1.5]) cylinder(r=LM8UU_dia/2,h=h,$fn=50);
	cylinder(r=LM8UU_dia/2.5,h=10*h,center=true,$fn=50);
}


module Z_solid_body(top_part=true) {
	hull() {
		if(top_part)
			translate([wall_height/2,wall_width/2,wall_thickness/2])
				bcube([wall_height,wall_width,wall_thickness],cr=4,cres=10);
		else
			translate([wall_height/2,wall_width,wall_thickness/2])
				bcube([wall_height,wall_width/2,wall_thickness],cr=4,cres=10);
		translate([wall_height/2,wall_width-4,0])
			translate([0,38,0])
				cylinder(r=spindle_motor_diam/2+spindle_holder_thickness,h=wall_thickness,$fn=60);
	}

	// For the linear bearing holders
	hull() {
		translate([wall_height/2-Z_smooth_rods_sep/2,Z_threaded_pos,0])
			cylinder(r=3+LM8UU_dia/2,h=wall_thickness,$fn=50);
		translate([wall_height/2+Z_smooth_rods_sep/2,Z_threaded_pos,0])
			cylinder(r=3+LM8UU_dia/2,h=wall_thickness,$fn=50);
	}

	// For the claw of the spindle holder
if(top_part){
	translate([wall_height/2,wall_width-4,0])
		translate([0,38,0]) {
			rotate([0,0,0]) {
				translate([spindle_motor_diam/2,-12.5,0]) cube([25,20,wall_thickness]);
				
	// Write text in the front
	color([0.5,0.5,0.5])
			rotate([0,0,180]) scale([-1,1,-textHscale])
				writecylinder("CYCLONE",[0,0,-wall_thickness/(2*textHscale)],spindle_motor_diam/2+spindle_holder_thickness,0,font="orbitron.dxf",space=1.1,h=wall_thickness,t=textThickness,center=true,ccw=true);
			}
		}
}
else
translate([wall_height/2,wall_width-4,0])
		translate([0,38,0]) {
			
			rotate([0,0,180]) {
			translate([spindle_motor_diam/2,-7,0]) cube([25,20,wall_thickness]);
			color([0.2,0.2,0.5])
			scale([1,1,textHscale])
				writecylinder("PCB Factory",[0,0,wall_thickness/(2*textHscale)+1],spindle_motor_diam/2+spindle_holder_thickness,0,font="orbitron.dxf",space=1.1,h=wall_thickness-2,t=textThickness,center=true,ccw=true);
			}
		}
}

//for display only, doesn't contribute to final object
//build_plate(3,200,200);

module Z_carriage(showSpindle=false,top_part=true, with_extra_parts=false, exploded=false) {

	difference() {
		rotate([0,0,-90]) translate([-wall_height/2,-Z_threaded_pos,0]) {
			difference () {
				Z_solid_body(top_part);
				if(top_part) motor_stand_holes_Z();
				translate([wall_height/2,wall_width-4,0])
					spindle_holder_holes(wall_thickness,spindle_motor_diam,base_screw_diameter,top_part);
				translate([wall_height/2-Z_smooth_rods_sep/2,Z_threaded_pos,0])
					linearBearingHolderZ(wall_thickness);
				translate([wall_height/2+Z_smooth_rods_sep/2,Z_threaded_pos,0])
					linearBearingHolderZ(wall_thickness);
			}
		}

		// Hole for the threaded rod
		if(!top_part) {
			hull() {
				cylinder(r=2+M8_rod_diameter/2,h=wall_thickness*10,center=true,$fn=30);
				translate([-15,0,0])
					cylinder(r=2+M8_rod_diameter/2,h=wall_thickness*10,center=true,$fn=30);
			}
		}

		// Truncation in the base for avoiding collision with the X axis
		if(!top_part) translate([-15,0,0]) rotate([0,45,0]) cube([20,100,10],center=true);
	}
	if(showSpindle) rotate([0,0,-90]) translate([0,wall_width-4-Z_threaded_pos,0])
			translate([0,38,-20+8]) dummySpindle();
    if(with_extra_parts) {
      Z_carriage_extras(top_part=top_part, exploded_distance=exploded?27:0);
    }
}

module Z_carriage_extras(top_part=true, exploded_distance=0) {
  if(top_part) {
    echo("Non-Plastic Parts, 1, Nema 17 for Z axis");
    translate([-motor_width/2,0,1-exploded_distance])
      rotate([0,180,0])
        motor(Cyclone_Nema17, NemaLengthLong);

    echo("Non-Plastic Parts, 4, Bolt M3 x 6 mm for Z motor");
    for(i=[-1,1]) for(j=[-1,1])
      translate([-motor_width/2,0,0])
        translate([i*motor_screw_distance/2,j*motor_screw_distance/2,2.5+exploded_distance*0.7]) {
          rotate([0,180,0]) color(Steel) boltHole(size=3, length=6);
    }

    translate([-motor_width/2,0,7+5+wall_thickness/2+2.9])
      rotate([0,0,-90])
        cyclone_motor_z_gear(with_extra_parts=true, exploded=(exploded_distance!=0));

    echo("Non-Plastic Parts, 1, Bearing 608 for Z motor");
    translate([0,0,wall_thickness/2])
      bearing(model=608);

    translate([0,0,3/2+0.8*8+wall_thickness/2+7+exploded_distance/2])
      rotate([180,0,11])
        cyclone_rod_z_gear(with_extra_parts=true, exploded=(exploded_distance!=0));

    echo("Non-Plastic Parts, 2, Bolt M5 x 55 mm to attach Z_carriage top and bottom");
    rotate([0,0,-90]) translate([-wall_height/2,-Z_threaded_pos,0])
      translate([wall_height/2,wall_width-4,0]) color(Steel) {
        translate([20,8,-0.05-2.5*exploded_distance])
          boltHole(size=5, length=55);
        translate([-20,8,-0.05-2.5*exploded_distance])
          boltHole(size=5, length=55);
      }
  }
  else
  {
    echo("Non-Plastic Parts, 1, Spindle");

    echo("Non-Plastic Parts, 2, Nut M5 to attach Z_carriage top and bottom");
    rotate([0,0,-90]) translate([-wall_height/2,-Z_threaded_pos,0])
      translate([wall_height/2,wall_width-4,0]) color(Steel) {
        translate([20,8,-0.8*5-0.5*exploded_distance])
          flat_nut(5);
        translate([-20,8,-0.8*5-0.5*exploded_distance])
          flat_nut(5);
      }
  }

  if(top_part)
    echo("Non-Plastic Parts, 2, Linear Bearing LM8UU for Z_carriage top part");
  else
    echo("Non-Plastic Parts, 2, Linear Bearing LM8UU for Z_carriage bottom part");
  rotate([0,0,-90])
  translate([-wall_height/2,-Z_threaded_pos,0]) {
    translate([wall_height/2-Z_smooth_rods_sep/2,Z_threaded_pos,0])
      translate([0,0,1.5-exploded_distance])
        linearBearing(model="LM8UU");
    translate([wall_height/2+Z_smooth_rods_sep/2,Z_threaded_pos,0])
	    translate([0,0,1.5-exploded_distance])
	      linearBearing(model="LM8UU");
  }

  if(top_part) {
    echo("Non-Plastic Parts, 1, Bolt M3 x 20 mm for Z_carriage part");
    echo("Non-Plastic Parts, 1, Nut M3 for Z_carriage top part");
  }
  else {
    echo("Non-Plastic Parts, 1, Bolt M3 x 20 mm for Z_carriage bottom part");
    echo("Non-Plastic Parts, 1, Nut M3 for Z_carriage bottom part");
  }
  rotate([0,top_part ? 0:180,-90]) translate([-wall_height/2,0,0])
  translate([wall_height/2,wall_width+(top_part?-1:-1.5),0]) {
    translate ([spindle_motor_diam/2+15,exploded_distance,top_part ? wall_thickness/2:-wall_thickness/2]) rotate([90,0,0])
      color(Steel) boltHole(size=3, length=20);
    translate ([spindle_motor_diam/2+15,-20.4-0.5*exploded_distance,top_part ? wall_thickness/2:-wall_thickness/2]) rotate([90,0,180])
      color(Steel) flat_nut(3);
  }
}

module Z_carriage_assembled(z_thread_rod_length=120, with_extra_parts=false, exploded=false) {
	Z_carriage(showSpindle=true,top_part=false,with_extra_parts=with_extra_parts, exploded=exploded);
	translate([0,0,spindle_holder_distance]) rotate([180,0,0]) Z_carriage(showSpindle=false,top_part=true,
      with_extra_parts=with_extra_parts, exploded=exploded);

    if(z_thread_rod_length)
      translate([0,0,-z_thread_rod_length/2+spindle_holder_distance]) rotate([90,0,0])
        rod(len=z_thread_rod_length, threaded=true);
}


Z_carriage_assembled();



