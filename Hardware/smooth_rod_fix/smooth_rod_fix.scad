// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

include <MCAD/metric_fastners.scad>
include <MCAD/materials.scad>
use <../libs/obiscad/bcube.scad>
use <../libs/obiscad/bevel.scad>
use <../libs/build_plate.scad>

M8_rod_diam = 8.2;

smooth_rod_margin = 1;

smooth_rod_screw_sep = 8;
smooth_rod_screw_diam = 3+1;
smooth_rod_screw_len = 7;

part_x = smooth_rod_screw_sep*3;
part_y = 8;
part_z = 8;

//for display only, doesn't contribute to final object
translate([frame_width/2,frame_height/2,0]) build_plate(3,110,140);

module smooth_rod_fix(with_extra_parts=false, exploded=false) {
translate([0,0,part_z/2]) difference() {
  // --------- Main frame --------- //  
  bcube([part_x,part_y,part_z],center=true,cr=2,cres=10);


  // --------- Smooth Y rods --------- //
  rotate([90,0,0]) translate([0,part_z/2+smooth_rod_margin/2,0]) {
    cylinder(r=M8_rod_diam/2,h=part_y*2,center=true,$fn=40);
    // Screws
    rotate([90,0,0]) translate([0,0,0]) {
      translate([-smooth_rod_screw_sep,0,0])
        cylinder(r=smooth_rod_screw_diam/2,h=10*part_z,center=true,$fn=30);
      translate([smooth_rod_screw_sep,0,0])
        cylinder(r=smooth_rod_screw_diam/2,h=10*part_z,center=true,$fn=30);
    }
  }

} // End of difference() command

  if(with_extra_parts)
      smooth_rod_fix_extras(exploded_distance=(exploded?20:0));

  module smooth_rod_fix_extras(exploded_distance=0) {
    screw_size = 2.9;
    screw_length = 16;
    echo("Non-Plastic Parts, 2, Self Tapping Screw 2.9 x 16 mm for smooth_rod_fix");
    color(Steel) {
      translate([0,0,-.2-exploded_distance]) {
        translate([-smooth_rod_screw_sep,0,0])
          csk_bolt(screw_size, screw_length);
        translate([smooth_rod_screw_sep,0,0])
          csk_bolt(screw_size, screw_length);
      }
    }
  }

}

smooth_rod_fix();
