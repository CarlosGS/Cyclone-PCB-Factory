// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

include <MCAD/stepper.scad>
include <MCAD/bearing.scad>
include <MCAD/metric_fastners.scad>
include <MCAD/nuts_and_bolts.scad>
use <../Gears/rod_gear.scad>
use <../Gears/motor_gear.scad>
use <../libs/obiscad/bcube.scad>
use <../libs/obiscad/bevel.scad>
use <../libs/build_plate.scad>
use <../smooth_rod_fix/smooth_rod_fix.scad>
use <../libs/End_Stop_Holder.scad>
use <../libs/micro_switch.scad>



layer_thickness = 0.4;

motor_width = 43+1;
motor_length = 49; // not used
motor_screw_distance = 31.3;
motor_center_diameter = 23;

motor_screw_diameter = 4;
motor_screw_head_diameter = 8;

motor_stand_thickness = 5;

bearing_diameter = 22.4;
M8_rod_diam = 8.2;

X_smooth_rods_sep = 50;
X_smooth_rods_sep_projected = sqrt((X_smooth_rods_sep*X_smooth_rods_sep)/2); // Be careful with this measure, it is not properly named since it is used with the following offset:
smooth_rod_margin = 1;

smooth_rod_screw_sep = 8;
smooth_rod_screw_diam = 3;
smooth_rod_screw_len = 7;

X_rods_corner_shaft_size = X_smooth_rods_sep*0.65;

frame_thickness = 10;
frame_width = 90;
frame_height = 135;
frame_corner_radius = 5;

X_threaded_rod_posX = X_smooth_rods_sep_projected;
X_threaded_rod_posY = X_smooth_rods_sep_projected;
motor_axis_distance = 32;
motor_axis_angle = 15;
X_motor_gear_margin = 35;

frame_hole_height = 80;
bottom_thickness = 5;
wall_thickness = 5;
base_screw_diameter = 5;
base_screw_distance = 33;

Y_rod_height = 40;
Y_rod_dist_from_wall = 15;

Y_rod_support_lenght = Y_rod_dist_from_wall+smooth_rod_screw_sep+smooth_rod_screw_diam+3;

motor_adjust_margin = 3;

Cyclone_Nema17 = [
                [NemaModel, 17],
                [NemaLengthShort, 33*mm],
                [NemaLengthMedium, 39*mm],
                [NemaLengthLong, 48*mm],
                [NemaSideSize, 42.30*mm],
                [NemaDistanceBetweenMountingHoles, 31.0*mm],
                [NemaMountingHoleDiameter, 4*mm],
                [NemaMountingHoleDepth, 5.5*mm], //actual is 4.5mm, motor() module is generating 1mm shorter
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

module frame(with_motor = 1, show_printbed = 0, with_extra_parts=false, exploded=false) {

if(show_printbed) {
//for display only, doesn't contribute to final object
translate([frame_width/2,frame_height/2,0]) build_plate(3,110,140);
}

union() {
difference() {
  // --------- Main frame --------- //  
  translate([frame_width/2,frame_height/2,frame_thickness/2])
    cube([frame_width,frame_height,frame_thickness],center=true);


  // --------- Smooth Y rods --------- //
  translate([X_smooth_rods_sep_projected,-smooth_rod_margin,0]) {
    cylinder(r=M8_rod_diam/2,h=10*frame_thickness,center=true,$fn=40);
    // Screws
    rotate([90,0,0]) translate([0,frame_thickness/2,0]) {
      translate([-smooth_rod_screw_sep,0,0])
        cylinder(r=smooth_rod_screw_diam/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
      translate([smooth_rod_screw_sep,0,0])
        cylinder(r=smooth_rod_screw_diam/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
    }
  }
  translate([-smooth_rod_margin,X_smooth_rods_sep_projected,0]) {
    cylinder(r=M8_rod_diam/2,h=10*frame_thickness,center=true,$fn=40);
    // Screws
    rotate([0,90,0]) translate([-frame_thickness/2,0,0]) {
      translate([0,-smooth_rod_screw_sep,0])
        cylinder(r=smooth_rod_screw_diam/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
      translate([0,smooth_rod_screw_sep,0])
        cylinder(r=smooth_rod_screw_diam/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
    }
  }


  // --------- Holes to save plastic --------- //
  // Corner shaft
  rotate([0,0,45])
    cube([X_rods_corner_shaft_size,X_rods_corner_shaft_size,frame_thickness*3],center=true);
  // Hole next to the corner shaft
  rotate([0,0,45]) translate([28,0,0])
    bcube([15,25,frame_thickness*3],cr=2,cres=10);
  // Hole to remove the motor part
  if(with_motor==0)
    translate([frame_width,0,0])
      bcube([frame_width-10,frame_hole_height+bottom_thickness,frame_thickness*3],cr=2,cres=10);


  // --------- Large hole in the frame --------- //
  translate([(frame_width-wall_thickness)/2,frame_height-frame_hole_height/2-bottom_thickness,0])
    bcube([frame_width-wall_thickness-frame_thickness,frame_hole_height,frame_thickness*3],cr=2,cres=10);


  // --------- Screws in the base --------- //
  rotate([90,0,0]) translate([frame_width/2,frame_thickness/2,-frame_height]) {
    translate([-base_screw_distance,0,0])
      cylinder(r=base_screw_diameter/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
    translate([base_screw_distance*0.8,0,0])
      cylinder(r=base_screw_diameter/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
    translate([base_screw_distance*0.2,0,0])
      cylinder(r=base_screw_diameter/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
  }


  // --------- X motor assembly, position relative to X threaded rod --------- //
  translate([X_threaded_rod_posX,X_threaded_rod_posY,0]) {
  // Threaded Y rod hole
  translate([0,0,(motor_stand_thickness/2)+layer_thickness])
    cylinder(r=(M8_rod_diam*2)/2,h=10*frame_thickness,center=false,$fn=40);
  // Threaded X rod bearing hole
  translate([0,0,0])
    cylinder(r=bearing_diameter/2,h=motor_stand_thickness,center=true,$fn=40);

  if(with_motor) {
// ------- BEGIN MOTOR HOLES --------
  // Center is the motor shaft, and we apply the rotation keeping the motor horizontal
  // Screws for holding the motor
  rotate([0,0,-motor_axis_angle]) translate([motor_axis_distance,0,0]) rotate([0,0,90+motor_axis_angle]) {
    
    // Hole for the motor shaft
    hull() {
      translate([0,motor_adjust_margin/2,0])
        cylinder(r=motor_center_diameter/2,h=10*wall_thickness,center=true,$fn=40);
      translate([0,-motor_adjust_margin/2,0])
        cylinder(r=motor_center_diameter/2,h=10*wall_thickness,center=true,$fn=40);
    }

    // Screws for holding the motor
    for(i=[-1,1]) for(j=[-1,1])
    translate([i*motor_screw_distance/2,j*motor_screw_distance/2,0]) {
      hull() {
        translate([0,motor_adjust_margin/2,0])
          cylinder(r=motor_screw_diameter/2,h=10*wall_thickness,center=true,$fn=40);
        translate([0,-motor_adjust_margin/2,0])
          cylinder(r=motor_screw_diameter/2,h=10*wall_thickness,center=true,$fn=40);
      }
    }

    // Level the motor area
    hull() {
      translate([0,motor_adjust_margin/2-10,motor_stand_thickness*2])
        bcube([motor_width,motor_width+20,frame_thickness],cr=5,cres=10);
      translate([0,-motor_adjust_margin/2,motor_stand_thickness*2])
        bcube([motor_width,motor_width,frame_thickness],cr=5,cres=10);
    }
// ------- END MOTOR HOLES --------
  } // End of centering over motor shaft

  } // End of if(with_motor)

  } // End of centering over X threaded rod

} // End of difference() command


// --------- Support column for the triangular structure --------- //
translate([frame_width/4,frame_height-frame_hole_height/2-bottom_thickness,frame_thickness/2])
  rotate([0,0,-23])
    cube([wall_thickness,sqrt((frame_width*frame_width)/4+(frame_hole_height*frame_hole_height)),frame_thickness],center=true);


// --------- Bevel base supports --------- //
translate([wall_thickness/2,frame_height,frame_thickness-0.5])
  rotate([90,0,-90])
    bconcave_corner(cr=Y_rod_support_lenght-0.5, cres=0, l=wall_thickness, th=0.5, ext_corner=true);
translate([frame_width-frame_thickness/2,frame_height,frame_thickness-0.5])
  rotate([90,0,-90])
    bconcave_corner(cr=Y_rod_support_lenght-0.5, cres=0, l=frame_thickness, th=0.5, ext_corner=true);
// Long bevel
translate([frame_width/2,frame_height,frame_thickness-0.5])
  rotate([90,0,-90])
    bconcave_corner(cr=wall_thickness-0.5, cres=0, l=frame_width, th=0.5, ext_corner=true);


// --------- Bevel Y rod support --------- //
translate([frame_width-frame_thickness/2,frame_height,frame_thickness-2])
  translate([0,-Y_rod_height+smooth_rod_margin,0]) {
    difference() {
      rotate([90,0,90]) // Bevel
        bconcave_corner(cr=Y_rod_support_lenght-smooth_rod_screw_len, cres=0, l=frame_thickness, th=smooth_rod_screw_len, ext_corner=true);

      translate([0,-smooth_rod_margin,Y_rod_dist_from_wall]) rotate([0,90,0]) {
        cylinder(r=M8_rod_diam/2,h=10*frame_thickness,center=true,$fn=40);
        // Screws
        rotate([90,0,0]) {
          translate([-smooth_rod_screw_sep,0,-1])
            cylinder(r=smooth_rod_screw_diam/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
          translate([smooth_rod_screw_sep,0,-1])
            cylinder(r=smooth_rod_screw_diam/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
        }
      }
  }
  }

  if(with_extra_parts)
    frame_extras(with_motor=with_motor, exploded_distance=(exploded?30:0));

} // End of union() command

}

module frame_extras(with_motor=1, exploded_distance=0) {
  if(with_motor) {
    translate([X_threaded_rod_posX,X_threaded_rod_posY,0]) {
      rotate([0,0,-motor_axis_angle]) translate([motor_axis_distance,0,0]) rotate([0,0,90+motor_axis_angle]) {
        translate([0,0,wall_thickness-1]) {
          echo("Non-Plastic Parts, 1, Nema 17 for X axis");
          translate([0,0,exploded_distance]) motor(Cyclone_Nema17, NemaLengthLong);

          // --- Motor gear ---
          translate([0,0,-12-5.5+1-0.5*exploded_distance])
            cyclone_motor_gear(with_extra_parts=true, exploded=(exploded_distance!=0));
        }

        echo("Non-Plastic Parts, 4, Bolt M3 x 8 mm to attach motor on frame");
        for(i=[-1,1]) for(j=[-1,1])
          translate([i*motor_screw_distance/2,j*motor_screw_distance/2,0])
            translate([0,0,-0.4*exploded_distance]) {
              rotate([0,0,0]) color(Steel) boltHole(size=3, length=8);
          }
      }
    }

    translate([X_threaded_rod_posX,X_threaded_rod_posY,0]) {
      rotate([0,0,0])  {
        echo("Non-Plastic Parts, 1, Bearing 608 for motor frame");
        translate([0,0,-1.0-7/2-0.2*exploded_distance]) bearing(model=608);

        // --- Rod Gear ---
        translate([0,0,-8-1.0-7/2-1.0*exploded_distance])
          rotate([0,0,6])
            cyclone_rod_gear(with_extra_parts=true, exploded=(exploded_distance!=0));
      }
    }
  }

  screw_size = 2.9;
  screw_length = 16;
  echo("Non-Plastic Parts, 3, Self Tapping Screw 2.9 x 16 mm to attach frame on base");
  rotate([90,0,0]) translate([frame_width/2,frame_thickness/2,-frame_height+frame_thickness/2+.2+exploded_distance]) color(Steel) {
      translate([-base_screw_distance,0,0]) rotate([180,0,0])
        csk_bolt(screw_size, screw_length);
      translate([base_screw_distance*0.8,0,0]) rotate([180,0,0])
        csk_bolt(screw_size, screw_length);
      translate([base_screw_distance*0.2,0,0]) rotate([180,0,0])
        csk_bolt(screw_size, screw_length);
  }

  // --- X smooth rod fix ---
  translate([X_smooth_rods_sep_projected,-smooth_rod_margin,0])
    rotate([90,0,0]) translate([0,frame_thickness/2,8.5+0.5*exploded_distance])
      rotate([180,0,0]) smooth_rod_fix(with_extra_parts=true, exploded=(exploded_distance!=0));
  translate([-smooth_rod_margin,X_smooth_rods_sep_projected,0])
    rotate([0,90,0]) translate([-frame_thickness/2,0,-8.5-0.5*exploded_distance])
      rotate([0,0,90]) smooth_rod_fix(with_extra_parts=true, exploded=(exploded_distance!=0));
  // --- Y smooth rod fix ---
  translate([frame_width-frame_thickness/2,frame_height,frame_thickness-2])
    translate([0,-Y_rod_height+smooth_rod_margin,0])
      translate([0,-smooth_rod_margin-8.5-0.5*exploded_distance,Y_rod_dist_from_wall]) rotate([90,90,180])
        smooth_rod_fix(with_extra_parts=true, exploded=(exploded_distance!=0));

  if(with_motor) {

//   this seems to reduce working area of Y axis
    if(false) {
      translate([frame_width-frame_thickness/2,frame_height,frame_thickness-2])
        translate([0,-Y_rod_height+smooth_rod_margin,0])
          translate([0,-smooth_rod_margin,Y_rod_dist_from_wall])
            translate([-frame_thickness/2-0.5*exploded_distance, 15, 8]) rotate([180,0,0]) rotate([0,-90,0])
              end_stop_holder(with_extra_parts=true, exploded=(exploded_distance!=0));
    }

//  this seems to reduce working area of X axis
    if(false) {
      translate([X_smooth_rods_sep_projected,-smooth_rod_margin,0])
        translate([15+0.5*exploded_distance, -8, frame_thickness])
          rotate([180,180,-90])
            end_stop_holder(with_extra_parts=true, exploded=(exploded_distance!=0));
    }

//  this seems to reduce working area of X axis
    if(false) {
      echo("Non-Plastic Parts, 1, Micro Switch on motor frame for X axis");
      rotate([90, 0, -45])
        translate([X_rods_corner_shaft_size/2-19.8,0,-X_rods_corner_shaft_size/2+0.5*exploded_distance])
          micro_switch(with_extra_parts=true, exploded=(exploded_distance!=0));
    }
  }

  if(!with_motor) {
    translate([X_threaded_rod_posX,X_threaded_rod_posY,0]) {
      rotate([0,0,0])  {
        echo("Non-Plastic Parts, 1, Bearing 608 for no motor frame");
        translate([0,0,-1.0-7/2-0.2*exploded_distance]) bearing(model=608);

        echo("Non-Plastic Parts, 1, Nut M8 to attach threaded rod on no motor frame");
        translate([0,0,-6.5-1.0-7/2-0.6*exploded_distance]) rotate([0,0,0]) color(Steel) flat_nut(8);
      }
    }

    //this is not how carlosgs designed
    if(false) {
      echo("Non-Plastic Parts, 1, Micro Switch on no motor frame for X axis");
      rotate([90, 0, -45])
        translate([X_rods_corner_shaft_size/2-19.8,0,-X_rods_corner_shaft_size/2+0.5*exploded_distance])
          micro_switch(with_extra_parts=true, exploded=(exploded_distance!=0));
    }

    //Y end_stop_holder
    if(true) {
        translate([frame_width-frame_thickness/2,frame_height,frame_thickness-2])
          translate([0,-Y_rod_height+smooth_rod_margin,0])
            translate([0,-smooth_rod_margin,Y_rod_dist_from_wall])
              translate([-frame_thickness/2-0.5*exploded_distance, 8, -15]) rotate([90,0,0]) rotate([0,-90,0])
                end_stop_holder(with_extra_parts=true, exploded=(exploded_distance!=0));
    }

    //this seems to reduce working area of Y axis
    if(false) {
      echo("Non-Plastic Parts, 1, Micro Switch on no motor frame for Y axis");
      translate([frame_width-frame_thickness/2+10.8/2-0.5,frame_height-19.8-2,frame_thickness])
        translate([0,-Y_rod_height+smooth_rod_margin,0])
          translate([0,-smooth_rod_margin-8.5-0.5*exploded_distance,0])
            rotate([0, 0, 90])
              micro_switch(with_extra_parts=true, exploded=(exploded_distance!=0));
    }

    //Carlosgs design of X end_stop_holder
    if(true) {
      translate([X_smooth_rods_sep_projected,-smooth_rod_margin,0])
        translate([15+0.5*exploded_distance, -8, frame_thickness])
          rotate([180,180,-90])
            end_stop_holder(with_extra_parts=true, exploded=(exploded_distance!=0));
    }

  }
}


// Toggle parameters and mirror to create the other side part
//frame(with_motor = 1, show_printbed = 1);
scale([-1,1,1]) frame(with_motor = 0, show_printbed = 1);

