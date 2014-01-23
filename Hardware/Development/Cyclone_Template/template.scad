// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../libs/Write/Write.scad>
use <../libs/build_plate.scad>
use <../main_frame/frame.scad>
use <../Y_axis/Y_rod_idler.scad>
use <../Y_axis/motor_stand.scad>
use <../Y_axis/linear_bearing_holder.scad>
use <../Y_axis/Y_nut_holder.scad>
use <../XZ_axis/X_carriage.scad>
use <../XZ_axis/Z_carriage.scad>
use <../libs/rod.scad>
use <../libs/PCB_Machining_Vise/PCB_vise_1_Part1.scad>

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


X_Final_Threaded_Rod_Length = X_axis_sep+82;
X_Final_Smooth_Rod_Length = X_axis_sep+46;
Y_Final_Threaded_Rod_Length = Y_threaded_rod_length+38;
Y_Final_Smooth_Rod_Length = Y_axis_sep+8;
Y_threaded_rod_offset = 8;
Z_Final_Threaded_Rod_Length = 120;
Z_Final_Smooth_Rod_Length = 195;

X_Wood_Base = X_axis_sep+100;
Y_Wood_Base = Y_axis_sep+30;
Z_Wood_Base = 15;

X_PCB_BOARD = 150;
Y_PCB_BOARD = 100;
Z_PCB_BOARD = 1.5;
X_PCB_BOARD_OFFSET = 12;

//Travel (152 x 101 x 25)
X_Travel = 81; //0~152
Y_Travel = 80; //0~101
Z_Travel = 16; //0~27

//To display steppers, bearings, washers, nuts, bolts, micro-switches, etc.
Display_Extra_Parts = true;

//To enable exploded drawing view
Exploded_Drawing = false;

X_rod_sep_real = X_smooth_rods_sep_projected+smooth_rod_margin;

if(Display_Extra_Parts) //Non-Plastic Parts Header
  echo("Non-Plastic Parts, Quantity, Part");

module frame_right(with_extra_parts = false, exploded=false) {
  if(with_extra_parts)
    rotate([0,0,90]) scale([-1,1,1]) translate([-85,-23,135]) rotate([-90,0,0]) frame(with_motor = 0, with_extra_parts=with_extra_parts, exploded=exploded);
  else
    color([1,0.8,0]) rotate([0,0,90]) scale([-1,1,1]) translate([-85,-23,135]) rotate([-90,0,0]) frame(with_motor = 0, with_extra_parts=with_extra_parts, exploded=exploded);
}

module frame_left(with_extra_parts = false, exploded=false) {
  if(with_extra_parts)
    rotate([0,0,90]) scale([-1,-1,1]) translate([-85,-23,135]) rotate([-90,0,0]) frame(with_motor = 1, with_extra_parts=with_extra_parts, exploded=exploded);
  else
    color([1,1,0]) rotate([0,0,90]) scale([-1,-1,1]) translate([-85,-23,135]) rotate([-90,0,0]) frame(with_motor = 1, with_extra_parts=with_extra_parts, exploded=exploded);
}

module Y_rod_idler_left(with_extra_parts = false, exploded=false) {
  if(with_extra_parts)
    rotate([0,0,90]) scale([1,-1,1]) translate([-26,-17,39]) rotate([-90,0,0]) Y_rod_idler(with_extra_parts=with_extra_parts, exploded=exploded);
  else
    color([0.8,1,1]) rotate([0,0,90]) scale([1,-1,1]) translate([-26,-17,39]) rotate([-90,0,0]) Y_rod_idler(with_extra_parts=with_extra_parts, exploded=exploded);
}

module Y_rod_idler_right(with_extra_parts = false, exploded=false) {
  if(with_extra_parts)
    rotate([0,0,90]) translate([-26,-17,39]) rotate([-90,0,0]) Y_rod_idler(with_extra_parts=with_extra_parts, exploded=exploded);
  else
    color([1,1,1]) rotate([0,0,90]) translate([-26,-17,39]) rotate([-90,0,0]) Y_rod_idler(with_extra_parts=with_extra_parts, exploded=exploded);
}

module Y_motor_stand() {
  rotate([0,90,0]) translate([-45,0,52.4]) rotate([-90,0,0]) {
    if(Display_Extra_Parts)
      motor_stand(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
    else
      color([0,1,1]) motor_stand();
  }
}

module Y_idle_stand() {
  rotate([0,90,180]) translate([-45,0,52.4]) rotate([-90,0,0])
  if(Display_Extra_Parts)
    idle_stand(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
  else
    color([0,1,0.8]) idle_stand();
}

module linear_bearing_holder() {
  rotate([0,-90,-90]) translate([3,0,0])
    if(Display_Extra_Parts)
      lm8uu_bearing_holder(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
    else
      color([1,0.5,0]) lm8uu_bearing_holder(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
}

module Y_nut_holder() {
  if(Display_Extra_Parts)
    nut_holder_positioned(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
  else
    color([0.5,0.5,0])
       nut_holder_positioned();
}

module cnc_workbed(template=false) {

  // ---- work bed ----
  translate([0,0,-workbed_thickness/2+(template?2:0)]) {
    translate([0,0,template?-2:0])
    color([0.5,1,0.5,0.5]) { // Transparent color
      %cube([workbed_X,workbed_Y,workbed_thickness+(template?4:0)],center=true);
      difference() {
        cube([workbed_X,workbed_Y,workbed_thickness+(template?4:0)],center=true);
        cube([workbed_X-1,workbed_Y-1,workbed_thickness+(template?4:0)+1],center=true);
      }
    }

    translate([X_PCB_BOARD_OFFSET/2-28-X_PCB_BOARD/2,8+Y_PCB_BOARD/2,-(workbed_thickness)/2])
      rotate([180,0,0]) PCB_vise_1(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
    translate([X_PCB_BOARD_OFFSET/2+28+X_PCB_BOARD/2,-8-Y_PCB_BOARD/2,-(workbed_thickness)/2])
      rotate([180,0,180]) PCB_vise_1(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
    if(Display_Extra_Parts) {
      // --- PCB Board ---
      echo("Non-Plastic Parts, 1, Double sided PCB ", X_PCB_BOARD, " x ", Y_PCB_BOARD, " x ", Z_PCB_BOARD);
      translate([X_PCB_BOARD_OFFSET/2,0,-(workbed_thickness)/2-15])
        color([0.72,0.45,0.20]) cube([X_PCB_BOARD,Y_PCB_BOARD,Z_PCB_BOARD],center=true);
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
      X_carriage_assembled(show_printbed = 0, show_Xrods = 0, z_smooth_rods_len = Z_Final_Smooth_Rod_Length, with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
}

module Z_carriage_piece() {
  translate([0,0,35+Z_Travel])
    rotate([0,0,90])
        Z_carriage_assembled(z_thread_rod_length=Z_Final_Threaded_Rod_Length, with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
}

module cnc(show_printbed = 1) {
  // ---- build plate ----
  if(show_printbed) {
  //for display only, doesn't contribute to final object
  translate([X_axis_sep/2,Y_axis_sep/2,0])
    build_plate(3,297,210); // A4
  }

  // ---- main frames ----
  frame_left(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
  translate([X_axis_sep,0,0])
    frame_right(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);

  // ---- Y rod idlers ----
  translate([0,Y_axis_sep,0]) {
    Y_rod_idler_left(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
    translate([X_axis_sep,0,0])
      Y_rod_idler_right(with_extra_parts=Display_Extra_Parts, exploded=Exploded_Drawing);
  }

  // ---- Y threaded rod motor and idler ----
  translate([X_axis_sep/2,Y_axis_sep/2,0]) {
    translate([0,Y_threaded_rod_length/2,0]) Y_motor_stand();
    translate([0,-Y_threaded_rod_length/2+Y_threaded_rod_offset,0]) Y_idle_stand();
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

module cnc_workbed_template(top_side=false) {
  offset = top_side ? (workbed_thickness+1):-1;
  projection(cut=true) rotate([top_side?180:0,0,0]) translate([0,0,offset]) {
    cnc_workbed(template=true); // Main structure

    rotate([top_side?180:0,0,0]) {
      translate([0,-20,offset])
        reference(workbed_X,60);
      translate([-20,0,offset])
        rotate([0,0,90])
          reference(workbed_Y,40);
    }
  }
}

module cnc_assembled(Y_offset=0,X_offset=0,Z_offset=0) {
  translate([-X_axis_sep/2,-Y_axis_sep/2])
    cnc();
  translate([0,0,Y_rod_height]) { // Y rod height, centered
    // --- workbed ---
    translate([0,Y_offset-73+Y_Travel,12.5])
      rotate([0,180,0])
        cnc_workbed();

    // --- Y threaded rod ---
    translate([0,6+Y_threaded_rod_offset/2,Y_threaded_rod_height-Y_rod_height])
      rod(Y_Final_Threaded_Rod_Length, threaded=true);

    // --- Y smooth rods ---
    translate([X_axis_sep/2,0,0])
      rod(Y_Final_Smooth_Rod_Length);
    translate([-X_axis_sep/2,0,0])
      rod(Y_Final_Smooth_Rod_Length);
  }

  translate([0,-19,99.65]) { // X threaded rod height, centered over SMOOTH rod
    // --- X axis ---
    translate([0,-X_rod_sep_real,0]) {
      translate([-X_offset+31-X_PCB_BOARD_OFFSET-X_Travel,0,0]) {
        X_carriage();
        translate([0,X_rod_sep_real/2,Z_offset])
          Z_carriage_piece();
      }
      rotate([0,0,90])
        translate([0,6,0]) rod(X_Final_Threaded_Rod_Length, threaded=true);
      translate([0,0,X_rod_sep_real])
        rotate([0,0,90])
          rod(X_Final_Smooth_Rod_Length);
    }
    rotate([0,0,90])
      rod(X_Final_Smooth_Rod_Length);/// WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      /// INCOHERENT X_axis_sep!!!!!!!!!!!
  }

  // --- Wood base ---
  translate([0,0,-15/2-0.1])
    color([0.7,0.6,0.4]) 
      cube([X_Wood_Base,Y_Wood_Base,Z_Wood_Base],center=true);
}

rotate([0,0,90])cnc_assembled(Y_offset=30,X_offset=-50,Z_offset=10);

//rotate([0,0,90]) cnc_base_template(); // So the generated dxf matches inkscape's default orientation
//  cnc_workbed_template(top_side=true);
//  cnc_workbed_template(top_side=false);

echo("Non-Plastic Parts, 1, Machine Base ", X_Wood_Base, " x ", Y_Wood_Base, " x ", Z_Wood_Base);
echo("Non-Plastic Parts, 1, Work Bed ", workbed_X, " x ",workbed_Y, " x ", workbed_thickness);
echo("Non-Plastic Parts, 2, Smooth Rod for X axis, M8 x ", X_Final_Smooth_Rod_Length);
echo("Non-Plastic Parts, 1, Threaded Rod for X axis, M8 x ", X_Final_Threaded_Rod_Length);
echo("Non-Plastic Parts, 2, Smooth Rod for Y axis, M8 x ", Y_Final_Smooth_Rod_Length);
echo("Non-Plastic Parts, 1, Threaded Rod for Y axis, M8 x ", Y_Final_Threaded_Rod_Length);
echo("Non-Plastic Parts, 2, Smooth Rod for Z axis, M8 x ", Z_Final_Smooth_Rod_Length);
echo("Non-Plastic Parts, 1, Threaded Rod for Z axis, M8 x ", Z_Final_Threaded_Rod_Length);
