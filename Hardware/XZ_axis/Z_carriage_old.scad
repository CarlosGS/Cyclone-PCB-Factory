// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../libs/obiscad/bcube.scad>
use <../libs/build_plate.scad>
use <../libs/Write/Write.scad>

include <./lm8uu_holder.scad>

bottom_thickness = 4;
base_width = 20;
base_length = 25;
base_screw_diameter = 5;

motor_width = 43;
motor_length = 49; // not used
motor_screw_distance = 31.3;
motor_center_diameter = 23;

motor_screw_diameter = 3.7;
motor_screw_head_diameter = 8;

bearing_diameter = 22.4;
M8_rod_diameter = 8.2;

axis_distance = 21;

wall_thickness = 5;
wall_height = motor_width;
wall_width = 54;

idler_width = 25;

lbearing_holder_length = 23*2;

Z_threaded_pos = motor_width/2+axis_distance;

Z_smooth_rods_sep = 55;

textHscale = 0.8;
textThickness = 1.5;

// Derived from Spindle mount for ShapeOko by Misan (http://www.thingiverse.com/thing:26740)
module spindle_holder(length=50,showSpindle=true) {
	$fn=6;
	translate([0,38,0]) rotate([0,0,180]) {

	if(showSpindle) scale([1,1,-1]) translate([0,0,-length]) {
		translate([0,0,85]) color([0.95,0.95,0.95]) cylinder(r=26,h=30,$fn=60);
		translate([0,0,80]) color([0.95,0.95,0.95]) cylinder(r=10/2,h=5,$fn=60);
		translate([0,0,-10]) color([0.6,0.6,0.6]) cylinder(r=26,h=90,$fn=60);
		translate([0,0,-40]) color([0.9,0.9,0.9]) cylinder(r=15/2,h=40,$fn=60);
		translate([0,0,-50]) color([0.4,0.4,0.4]) cylinder(r=20/2,h=10,$fn=60);
		translate([0,0,-50-20]) color([0.9,0.9,0.9]) cylinder(r1=1/2,r2=3/2,h=20,$fn=60);
	}

	difference() {
	union() {
	cylinder(r=30,h=length,$fn=60);

	// Write text in the front
	color([0.5,0.5,0.5]) scale([-1,1,-textHscale]) writecylinder("CYCLONE",[0,0,-length/(3*textHscale)],30,0,font="orbitron.dxf",space=1.1,h=12,t=textThickness,center=true,ccw=true);
	translate ([-30,0,0]) cube([60,38,length]);
	translate([28,-7,0]) cube([20,20,length]);

	color([0.5,0.5,0.5]) scale([-1,1,-textHscale]) writecylinder("PCB Factory",[0,0,-length/(1.5*textHscale)],30,0,font="orbitron.dxf",space=1.1,h=14/2,t=textThickness,center=true,ccw=true);
	translate ([-30,0,0]) cube([60,38,length]);
	translate([28,-7,0]) cube([20,20,length]);

	}
	
	translate([0,0,-0.05]) cylinder(r=26,h=length+2,$fn=60);
	
	translate([0,0,-0.01]) cube([90,3,length+2]);
	
	
	translate ([40,20,3*length/4]) rotate([90,0,0]) cylinder(r=2,h=30);
	translate ([40,20,length/4]) rotate([90,0,0]) cylinder(r=2,h=30);
	
	translate ([40,14,3*length/4]) rotate([90,0,0]) cylinder(r=3.5,h=4,$fn=6);
	translate ([40,14,length/4]) rotate([90,0,0]) cylinder(r=3.5,h=4,$fn=6);

	difference() {
		translate ([-30+15,0,-0.1]) cube([30,38.1,30]);
		cylinder(r=26+1,h=length,$fn=60);
	}
	
	}
	}
}

module motor_stand_no_base_Z(with_motor=true) {
difference() {
  translate([wall_height/2,wall_width/2,wall_thickness/2])
    bcube([wall_height,wall_width,wall_thickness],cr=4,cres=10);

  // Position relative to motor shaft
  translate([motor_width/2,motor_width/2,wall_thickness/2]) {
    if(with_motor) {
    // Hole for the motor shaft
    translate([0,-wall_width/2,0])
      cube([20,wall_width,10*wall_thickness],cr=4,cres=10,center=true);
    cylinder(r=motor_center_diameter/2,h=10*wall_thickness,center=true,$fn=40);

    // Screws for holding the motor
    for(i=[-1,1]) for(j=[-1,1])
    translate([i*motor_screw_distance/2,j*motor_screw_distance/2,0]) {
      cylinder(r=motor_screw_diameter/2,h=10*wall_thickness,center=true,$fn=40);
      cylinder(r=motor_screw_head_diameter/2,h=10*wall_thickness,center=false,$fn=40);
    }
    } // End if with motor

    // Bearing holes
    rotate([0,0,0]) translate([0,axis_distance,0]) {
      cylinder(r=(M8_rod_diameter*2)/2,h=10*wall_thickness,center=true,$fn=40);
      cylinder(r=bearing_diameter/2,h=10*wall_thickness,center=false,$fn=60);

    }

  } // End of translate relative to motor shaft
} // End of difference
}

module motor_stand_Z(with_motor=true) {
  union() {
    motor_stand_no_base_Z(with_motor);
  }
}

//for display only, doesn't contribute to final object
build_plate(3,200,200);

module Z_carriage(showSpindle=false) {
	rotate([0,0,-90]) translate([-wall_height/2,-Z_threaded_pos,0]) {
		motor_stand_Z();
		translate([wall_height/2,wall_width-4,0]) spindle_holder(lbearing_holder_length,showSpindle);
		translate([wall_height/2-Z_smooth_rods_sep/2,Z_threaded_pos,lbearing_holder_length/2]) rotate([-90,0,0]) lm8uu_bearing_holder_XZ(lbearing_holder_length);
		translate([wall_height/2+Z_smooth_rods_sep/2,Z_threaded_pos,lbearing_holder_length/2]) rotate([-90,0,0]) lm8uu_bearing_holder_XZ(lbearing_holder_length);
	}
}

Z_carriage(showSpindle=false);
