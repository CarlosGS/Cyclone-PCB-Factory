// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../libs/obiscad/bcube.scad>
use <../libs/obiscad/bevel.scad>
use <../libs/build_plate.scad>


module Y_rod_idler(show_printbed = 0) {

motor_stand_thickness = 5;

bearing_diameter = 22.4;
M8_rod_diam = 8.2;

smooth_rod_margin = 1;

smooth_rod_screw_sep = 8;
smooth_rod_screw_diam = 3;
smooth_rod_screw_len = 7;

frame_thickness = 4;
bottom_thickness = 4;
base_screw_diameter = 5;

Y_rod_height = 40;
Y_rod_dist_from_wall = 15;

Y_rod_support_lenght = Y_rod_dist_from_wall+smooth_rod_screw_sep+smooth_rod_screw_diam;

frame_width = 30;
frame_height = Y_rod_height-smooth_rod_margin;
wall_thickness = 5;

if(show_printbed) {
//for display only, doesn't contribute to final object
translate([frame_width/2,frame_height/2,0]) build_plate(3,110,140);
}

union() {
  // --------- Main frame --------- //  
  difference() {
  translate([frame_width/2,frame_height/2,frame_thickness/2])
    cube([frame_width,frame_height,frame_thickness],center=true);
  rotate([0,0,35]) cube([33,frame_height*10,frame_thickness*10],center=true);

  } // End of difference() command


// --------- Step with screws in the base --------- //  

  difference() {
  translate([0,frame_height-bottom_thickness,frame_thickness/2])
    cube([frame_width,bottom_thickness,Y_rod_support_lenght/2],center=false);
  // --------- Screws in the base --------- //
  rotate([90,0,0]) translate([frame_width/3,Y_rod_support_lenght/2.5,-frame_height]) {
    translate([-5,0,0])
      cylinder(r=base_screw_diameter/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
    translate([5,0,0])
      cylinder(r=base_screw_diameter/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
  }

  } // End of difference() command
  //Extra 2 screws @yopero
  difference() {
  translate([0,frame_height-bottom_thickness,frame_thickness/2+13])
    cube([frame_width,bottom_thickness,Y_rod_support_lenght/2+2],center=false);
  // --------- Screws in the base --------- //
  rotate([90,0,0]) translate([frame_width/3,Y_rod_support_lenght/2.5,-frame_height]) {
    translate([-5,13,0])
      cylinder(r=base_screw_diameter/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
    translate([5,13,0])
      cylinder(r=base_screw_diameter/2,h=2*smooth_rod_screw_len,center=true,$fn=6);
  }

  } // End of difference() command

// --------- Bevel base supports --------- //
translate([frame_width-frame_thickness,frame_height,frame_thickness-0.5])
  rotate([90,0,-90])
    bconcave_corner(cr=Y_rod_support_lenght-0.5, cres=0, l=frame_thickness*2, th=0.5, ext_corner=true);


// --------- Bevel Y rod support --------- //
translate([frame_width-frame_thickness,frame_height,frame_thickness-2])
  translate([0,-Y_rod_height+smooth_rod_margin,0]) {
    difference() {
      rotate([90,0,90]) // Bevel
        bconcave_corner(cr=Y_rod_support_lenght-smooth_rod_screw_len, cres=0, l=frame_thickness*2, th=smooth_rod_screw_len, ext_corner=true);

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

module base_screws(){


}
//Y_rod_idler(show_printbed = 1);
scale([-1,1,1]) Y_rod_idler(show_printbed = 1);
translate([0,-5,0])
rotate([180,0,0])
mirror([0,0,1]){
   scale([-1,1,1]) Y_rod_idler(show_printbed = 0);
}






