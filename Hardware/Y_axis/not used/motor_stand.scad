// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../libs/obiscad/bcube.scad>
use <../libs/build_plate.scad>

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

axis_distance = 32;

wall_thickness = 5;
wall_height = 45;
wall_width = 70;

idler_width = 25;

module motor_stand_no_base(with_motor=true) {
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
    rotate([0,0,15]) translate([0,axis_distance,0]) {
      cylinder(r=(M8_rod_diameter*2)/2,h=10*wall_thickness,center=true,$fn=40);
      cylinder(r=bearing_diameter/2,h=10*wall_thickness,center=false,$fn=60);

    }

  } // End of translate relative to motor shaft
} // End of difference
}

module motor_stand(with_motor=true) {
  union() {
    motor_stand_no_base(with_motor);
    difference() {
      union() {
        translate([wall_height-bottom_thickness,wall_width-base_width]) {
          cube([bottom_thickness,base_width,base_length]);
          hull() {
            cube([bottom_thickness,5,base_length]);
            translate([-18,0,0])
              cube([0.001,5,0.001]);
          }
        }
      }
      // --- screws for the base ---
      translate([wall_height,wall_width-5,15])
        rotate([0,90,0]) {
          translate([-5,0,0])
            cylinder(r=base_screw_diameter/2,h=100,center=true,$fn=6);
          translate([5,0,0])
            cylinder(r=base_screw_diameter/2,h=100,center=true,$fn=6);
        }
    } // End of difference
  }
}


module idle_stand() {
  intersection() { // Remove the motor part
    motor_stand(with_motor=false);
    translate([wall_height/2,wall_width/2+35,wall_thickness/2])
      bcube([wall_height,wall_width,100],cr=4,cres=10);
  }
}

//for display only, doesn't contribute to final object
build_plate(3,200,200);

motor_stand();
//idle_stand();
