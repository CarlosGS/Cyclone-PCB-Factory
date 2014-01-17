// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <./libs/Write/Write.scad>
use <../libs/build_plate.scad>
use <../main_frame/frame_hex-grid_6screws.scad>
use <../Y_axis/Y_rod_idler_YOP.scad>
use <../Y_axis/motor_holder.scad>
use <../Y_axis/linear_bearing_holder.scad>
use <../Y_axis/Y_nut_holder.scad>
use <../XZ_axis/X_carriage_YOP.scad>
use <../XZ_axis/Z_carriage.scad>

X_axis_sep = 210;
Y_axis_sep = 210;
Y_threaded_rod_length = (Y_axis_sep/2)+40;
Y_linear_bearing_dist = Y_axis_sep/2-25-20;

Y_rod_height = 40;
Y_rod_dist_from_workbed = 12.5;

Y_threaded_rod_height = Y_rod_height-8.218; // Obtained "by sight"
Y_threaded_rod_dist_from_workbed = (Y_rod_height-Y_threaded_rod_height)+Y_rod_dist_from_workbed;

workbed_X = X_axis_sep+20;
workbed_Y = 122;//Y_linear_bearing_dist+25+20-3;
workbed_thickness = 10;

X_threaded_rod_height = 99.65;
X_smooth_rods_sep = 50;
X_smooth_rods_sep_projected = sqrt((X_smooth_rods_sep*X_smooth_rods_sep)/2); // Be careful with this measure, it is not properly named since it is used with the following offset:
smooth_rod_margin = 1;

X_rod_sep_real = X_smooth_rods_sep_projected+smooth_rod_margin;

module frame_right() {
  color([1,0.8,0]) rotate([0,0,90]) scale([-1,1,1]) translate([-85,-23,135]) rotate([-90,0,0]) frame(with_motor = 0);
}

module frame_left() {
  color([1,1,0]) rotate([0,0,90]) scale([-1,-1,1]) translate([-85,-23,135]) rotate([-90,0,0]) frame(with_motor = 1);
}

module Y_rod_idler_left() {
  color([0.8,1,1]) rotate([0,0,180]) translate([26,0,40]) rotate([-90,0,0])  Y_rod_idler_leftX(1);
}

module Y_rod_idler_right() {
  color([1,1,1]) rotate([0,0,180]) translate([-26,0,40]) rotate([-90,0,0]) Y_rod_idler_rightX(1);
}

module Y_motor_stand() {
  color([0,1,1]) rotate([0,90,0]) translate([-45,0,52.4]) rotate([-90,0,0]) motor_stand();
}

module Y_idle_stand() {
  color([0,1,0.8]) rotate([90,270,0]) translate([45,-52.4,0]) idle_stand();
}

module linear_bearing_holder() {
  color([1,0.5,0])
    rotate([0,-90,-90]) translate([3,0,0]) lm8uu_bearing_holder();
}

module Y_nut_holder() {
  color([0.5,0.5,0])
     nut_holder_positioned();
}

module cnc_workbed() {

  // ---- work bed ----
  translate([0,0,-workbed_thickness/2+1]) {
    color([0.5,1,0.5,0.5]) { // Transparent color
      %cube([workbed_X,workbed_Y,workbed_thickness],center=true);
      difference() {
        cube([workbed_X,workbed_Y,workbed_thickness],center=true);
        cube([workbed_X-1,workbed_Y-1,workbed_thickness+1],center=true);
      }
    }
  }

  // --- Y axis nut holder
  rotate([0,0,180])
    Y_nut_holder();

  // ---- work bed linear bearing position ----
  translate([-X_axis_sep/2,-Y_linear_bearing_dist/2,0])
    rotate([0,0,180])
      linear_bearing_holder();
  translate([-X_axis_sep/2,Y_linear_bearing_dist/2,0])
    rotate([0,0,180])
      linear_bearing_holder();
  translate([X_axis_sep/2,-Y_linear_bearing_dist/2,0])
    linear_bearing_holder();
  translate([X_axis_sep/2,Y_linear_bearing_dist/2,0])
    linear_bearing_holder();
}

module X_carriage() {
  translate([0,X_rod_sep_real/2,0])
    rotate([0,0,90])
      X_carriage_assembled(Show_Nut_Cover = 1,show_printbed = 0, show_Xrods = 0, show_Zrods = 1);
}

module Z_carriage_piece() {
  translate([0,0,41])
    rotate([0,0,90])
        Z_carriage_assembled();

}

module cnc(show_printbed = 1) {
  // ---- build plate ----
  if(show_printbed) {
  //for display only, doesn't contribute to final object
  translate([X_axis_sep/2,Y_axis_sep/2,0])
    build_plate(3,297,210); // A4
  }

  // ---- main frames ----
  frame_left();
  translate([X_axis_sep,0,0])
    frame_right();

  // ---- Y rod idlers ----
  translate([0,Y_axis_sep,0]) {
    Y_rod_idler_right();
    translate([X_axis_sep,0,0])
      Y_rod_idler_left();
  }

  // ---- Y threaded rod motor and idler ----
  translate([X_axis_sep/2,Y_axis_sep/2,0]) {
    translate([0,Y_threaded_rod_length/2,0]) Y_motor_stand();
    translate([0,-Y_threaded_rod_length/2,0]) Y_idle_stand();
  }
}

module reference(dist=200,offset=0) {
  lineWidth = 0.5;
  thickness = 5;
  textSize = 5;
  translate([offset,0,0]) write(str(dist," mm"),t=thickness,h=textSize,center=true);
  translate([0,textSize,0]) {
    cube([dist,lineWidth,thickness],center=true);
    translate([dist/2,0,0]) cube([lineWidth,5,thickness],center=true);
    translate([-dist/2,0,0]) cube([lineWidth,5,thickness],center=true);
  }
}

module cnc_base_template() {
  projection(cut=true) translate([0,0,-1]) {
    cnc(); // Main structure
    translate([X_axis_sep/2,Y_axis_sep/2,0]) { // Reference rulers
      reference(X_axis_sep,60);
      translate([-20,0,0])
        rotate([0,0,90])
          reference(Y_threaded_rod_length,40);
    }
  }
}

module cnc_workbed_template() {
  projection(cut=true) translate([0,0,-1]) {
    cnc_workbed(); // Main structure
    translate([0,-20,0])
      reference(workbed_X,60);
    translate([-20,0,0])
      rotate([0,0,90])
        reference(workbed_Y,40);
  }
}

module rod(len=100) {
  color([0.8,0.8,0.8])
     rotate([90,0,0])
       cylinder(r=8/2,h=len,center=true,$fn=30);
}

module cnc_assembled(Y_offset=0,X_offset=0,Z_offset=0) {
  translate([-X_axis_sep/2,-Y_axis_sep/2])
    cnc();
  translate([0,0,Y_rod_height]) { // Y rod height, centered
    // --- workbed ---
    translate([0,Y_offset,12.5])
      rotate([0,180,0])
        cnc_workbed();

    // --- Y threaded rod ---
    translate([0,0,Y_threaded_rod_height-Y_rod_height])
      color([0.5,0.5,0.5]) rod(Y_threaded_rod_length+60);
    //extra threaded rod for stability 
    translate([64,0,Y_threaded_rod_height-Y_rod_height])
      color([0.5,0.5,0.5]) rod(Y_threaded_rod_length+60);

    // --- Y smooth rods ---
    translate([X_axis_sep/2,0,0])
      rod(Y_axis_sep+15);
    translate([-X_axis_sep/2,0,0])
      rod(Y_axis_sep+15);
  }

  translate([0,-19,99.65]) { // X threaded rod height, centered over SMOOTH rod
    // --- X axis ---
    translate([0,-X_rod_sep_real,0]) {
      translate([-X_offset,0,0]) {
        X_carriage();
        translate([0,X_rod_sep_real/2,Z_offset])
          Z_carriage_piece();
      }
      //X motor threaded rod
      translate([0,-48,-20])
      rotate([0,0,90])
        color([0.5,0.5,0.5]) rod(X_axis_sep+80);
      //X motor threaded rod
      rotate([0,0,90])
        color([0.5,0.5,0.5]) rod(X_axis_sep+80);
      //X Upper smoth rod
      translate([0,0,X_rod_sep_real])
        rotate([0,0,90])
          rod(X_axis_sep+60);
    }
    //X Upper smoth rod
    rotate([0,0,90])
      rod(X_axis_sep+60);/// WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      /// INCOHERENT X_axis_sep!!!!!!!!!!!
  }

  // --- Wood base ---
  translate([0,0,-15/2-0.1])
    color([0.7,0.6,0.4]) 
      cube([X_axis_sep+70,Y_axis_sep+30,15],center=true);
}

rotate([0,0,90])cnc_assembled(Y_offset=30,X_offset=-50,Z_offset=10);

//rotate([0,0,90]) cnc_base_template(); // So the generated dxf matches inkscape's default orientation
//  cnc_workbed_template();
