// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../libs/obiscad/bcube.scad>
use <../libs/obiscad/bevel.scad>
use <../libs/build_plate.scad>

module frame(with_motor = 1, show_printbed = 0) {

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

Y_rod_support_lenght = Y_rod_dist_from_wall+smooth_rod_screw_sep+smooth_rod_screw_diam;

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

  // Center is the motor shaft, and we apply the rotation keeping the motor horizontal
  // Screws for holding the motor
  rotate([0,0,-motor_axis_angle]) translate([motor_axis_distance,0,0]) rotate([0,0,motor_axis_angle]) {
    for(i=[-1,1])
      for(j=[-1,1]) {
        translate([i*motor_screw_distance/2,j*motor_screw_distance/2,0]) {
          // Screw hole
          translate([0,0,motor_stand_thickness/2])
            cylinder(r=motor_screw_diameter/2,h=10*frame_thickness,center=true,$fn=40);
        }
      }

  // Hole for the motor shaft
  translate([frame_width/2,0,0])
      cube([frame_width,20,10*motor_stand_thickness],cr=4,cres=10,center=true);
    cylinder(r=motor_center_diameter/2,h=10*motor_stand_thickness,center=true,$fn=40);

  // Level the motor area
  translate([0,0,motor_stand_thickness*2])
      bcube([motor_width,motor_width,frame_thickness],cr=5,cres=10);

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

} // End of union() command


}


// Toggle parameters and mirror to create the other side part
frame(with_motor = 1, show_printbed = 1);
//scale([-1,1,1]) frame(with_motor = 0, show_printbed = 1);

