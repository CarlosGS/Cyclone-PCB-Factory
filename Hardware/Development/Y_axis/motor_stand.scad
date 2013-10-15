// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
// History:
//  - (05/25/2013) Added @yopero's four screw suggestion for the motor stand
//  - (05/28/2013) Added @yopero's four screw suggestion for the idle stand

include <MCAD/stepper.scad>
include <MCAD/bearing.scad>
include <MCAD/metric_fastners.scad>
include <MCAD/nuts_and_bolts.scad>
include <MCAD/materials.scad>
use <../libs/obiscad/bcube.scad>
use <../libs/build_plate.scad>
use <../Gears/rod_gear.scad>
use <../Gears/motor_gear.scad>
use <../libs/micro_switch.scad>

motor_width = 43;
motor_length = 49; // not used
motor_screw_distance = 31.3;
motor_center_diameter = 23;

motor_screw_diameter = 3.7;
motor_screw_head_diameter = 8;

motor_adjust_margin = 3;

bearing_diameter = 22.4;
M8_rod_diameter = 8.2;

axis_distance = 32;

wall_thickness = 8;
wall_height = 45;
wall_width = 70;

idler_width = 25;



// For the supports with screws
bottom_thickness = 5;
base_width = 20;
base_length = 20+wall_thickness;
base_screw_diameter = 5;



wall_extraWidth_left = base_width+5;
wall_extraWidth_right = 5;

totalWallWidth = wall_width+wall_extraWidth_left+wall_extraWidth_right;

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


module motorHolesY() {
    // Hole for the motor shaft
    hull() {
      translate([0,motor_adjust_margin/2,0])
        cylinder(r=motor_center_diameter/2,h=10*wall_thickness,center=true,$fn=40);
      translate([0,-motor_adjust_margin/2,0])
        cylinder(r=motor_center_diameter/2,h=10*wall_thickness,center=true,$fn=40);
    }

    // Hole for the screwdriver
    translate([-wall_height/2,0,wall_thickness/2]) rotate([0,90,0]) bcube([2*(wall_thickness-5),5,wall_height],cr=1);

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

module motor_stand_no_base(with_motor=true, with_extra_parts=false) {
  // --- additional parts for assembly instruction ---
  if(with_motor && with_extra_parts) {
    translate([motor_width/2,motor_width/2,0]) {
      // --- Nema 17 Stepper ---
      rotate([0,180,0])
        translate([0,0,-1])
          motor(Cyclone_Nema17, NemaLengthLong);
      // --- Motor Gear ---
      translate([0,0,12+5.5]) {
        rotate([180, 0, 30]) cyclone_motor_gear();
      }
      // --- M3 x 8mm grub screw to attach Gear to motor shaft ---
      translate([-2.5,0,12-3]) rotate([0, -90, 0]) color(Steel) cylinder(r=1.5, h=8);
    }
    translate([motor_width/2,motor_width/2,wall_thickness/2]) {
      rotate([0,0,15]) translate([0,axis_distance,2.5-wall_thickness/2]) {
        // --- Bearing ---
        bearing(model=608);
        // --- M8 Nut ---
        translate([0,0,7]) color(Steel)  flat_nut(8);
        // --- Rod Gear ---
        translate([0,0,1.5-wall_thickness/2+5+2.5+7+3]) rotate([0,180,15]) cyclone_rod_gear();
        // --- M8 Nut ---
        translate([0,0,1.5-wall_thickness/2+5+2.5+7+3+1.5++10]) rotate([0,180,0]) color(Steel) flat_nut(8);
      }
    }
    // --- M3 x 6mm bolts for holding the motor ---
    for(i=[-1,1]) for(j=[-1,1])
      translate([motor_width/2,motor_width/2,wall_thickness/2])
        translate([i*motor_screw_distance/2,j*motor_screw_distance/2,2.5-wall_thickness/2]) {
          rotate([0,180,0]) color(Steel) boltHole(size=3, length=6);
    }
  }

difference() {
  translate([wall_height/2,totalWallWidth/2-wall_extraWidth_left,wall_thickness/2])
    bcube([wall_height,totalWallWidth,wall_thickness],cr=4,cres=10);

  // Position relative to motor shaft
  translate([motor_width/2,motor_width/2,wall_thickness/2]) {

    if(with_motor)
      motorHolesY();

    // Bearing holes
    rotate([0,0,15]) translate([0,axis_distance,2.5-wall_thickness/2]) {
      cylinder(r=(M8_rod_diameter*2)/2,h=10*wall_thickness,center=true,$fn=40);
      cylinder(r=bearing_diameter/2,h=10*wall_thickness,center=false,$fn=60);
      if(!with_motor && with_extra_parts) {
        translate([0,0,7]) bearing(model=608);
      }
    }

  } // End of translate relative to motor shaft
} // End of difference

  translate([motor_width/2,motor_width/2,wall_thickness/2])
    rotate([0,0,15]) translate([0,axis_distance,2.5-wall_thickness/2]) color(Steel) {
      if(!with_motor && with_extra_parts) {
        bearing(model=608);
        translate([0,0,7]) washer(8);
        translate([0,0,6.4+7+0.8]) rotate([0,180,0]) flat_nut(8);
       }
    }
}

module holder(h=35,noScrews=false,base_width_inc=0, with_extra_parts=false) {
    difference() {
      union() {
        translate([wall_height-bottom_thickness,0]) {
          if(!noScrews) cube([bottom_thickness,base_width+base_width_inc,base_length]);
          hull() {
            cube([bottom_thickness,5,base_length]);
            translate([-h,0,0])
              cube([0.001,5,0.001]);
          }
        }
      }
      // --- screws for the base ---
      if(!noScrews) translate([wall_height,base_width/2+2.5,base_length/1.5])
        rotate([0,90,0]) {
          translate([-5,0,0])
            cylinder(r=base_screw_diameter/2,h=100,center=true,$fn=7);
          translate([5,0,0])
            cylinder(r=base_screw_diameter/2,h=100,center=true,$fn=7);
        }
    } // End of difference

    // --- Self tapping screw 2.9 x 16mm ---
    if(with_extra_parts) {
      translate([wall_height,base_width/2+2.5,base_length/1.5]) color(Steel)
        rotate([0,90,0]) {
          translate([-5,0,-bottom_thickness-.2])
            csk_bolt(2.9, 16);
          translate([5,0,-bottom_thickness-.2])
            csk_bolt(2.9, 16);
        }
    }
}

module motor_stand(with_motor=true, with_extra_parts=false) {
  union() {
    motor_stand_no_base(with_motor=with_motor, with_extra_parts=with_extra_parts);
    translate([0,wall_width]) holder(noScrews=true, with_extra_parts=false);
    translate([0,52.4-5/2]) holder(h=12,base_width_inc=1, with_extra_parts=with_extra_parts);
    translate([0,-wall_extraWidth_left+base_width]) scale([1,-1,1]) holder(with_extra_parts=with_extra_parts);
  }
}


module idle_stand(with_extra_parts=false) {
	union() {
		intersection() { // Remove the motor part
			motor_stand(with_motor=false, with_extra_parts=with_extra_parts);
           union() {
			  translate([wall_height/2,wall_width/2+52.4-(wall_width+wall_extraWidth_right-52.4),wall_thickness/2])
			    bcube([wall_height,wall_width,100],cr=4,cres=10);
			  translate([wall_height/2,wall_width/2+52.4-(wall_width+wall_extraWidth_right-52.4),wall_thickness/2])
			    bcube([wall_height*2,wall_width/6,100],cr=4,cres=10); //keep self tapping screw
           }
		}
		translate([0,wall_width+5-2*(wall_width+wall_extraWidth_right-52.4)]) holder(noScrews=true, with_extra_parts=with_extra_parts);
		translate([0,52.4+5/2]) scale([1,-1,1]) holder(h=15,base_width_inc=1, with_extra_parts=with_extra_parts);
	}

    if(!with_motor && with_extra_parts) {
    // --- micro switch ---
      translate([0,motor_width-idler_width/2,wall_thickness])
        rotate([-90, 0, 90])
          micro_switch(with_extra_parts);
    }
}

//for display only, doesn't contribute to final object
build_plate(3,200,200);

//motor_stand();
idle_stand();
