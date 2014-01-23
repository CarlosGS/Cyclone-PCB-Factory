// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../libs/obiscad/bcube.scad>
use <../libs/build_plate.scad>
use <../libs/Write/Write.scad>

// Adjust these values to match the thickness of the nuts you will use
M8_nut_height_margin = 0.1;
M8_nut_height = M8_nut_height_margin+6.2;

Y_rod_height = 40;
Y_rod_dist_from_workbed = 12.5;

Y_threaded_rod_height = Y_rod_height-8.218; // Obtained "by sight" using the template 3D assembled model
Y_threaded_rod_dist_from_workbed = (Y_rod_height-Y_threaded_rod_height)+Y_rod_dist_from_workbed;

nut_slot_thickness = 1;
nut_slot_length = 3;

bottom_thickness = 4;
base_width = 16;
base_length = 30;
base_screw_diameter = 5;

reinforcement_length = 7.5;

M8_rod_diameter = 8.2+1;
M8_nut_diameter = 15.3;

wall_thickness = 10;
wall_height = Y_threaded_rod_dist_from_workbed+11.5;
wall_width = base_width;

module text(dist=5) {
  lineWidth = 0.5;
  thickness = 2*0.75;
  textSize = 6;
  rotate([0,180,-90])
    write(str(dist," mm"),t=thickness,h=textSize,center=true);
}

module nut_holder_no_hole() {
  translate([0,wall_height])
  rotate([0,0,-90])
  union() {
	  translate([wall_height/2,wall_width/2,wall_thickness/2])
	    bcube([wall_height,wall_width,wall_thickness],cr=2,cres=10);
    difference() {
      union() { 
        translate([wall_height-bottom_thickness,wall_width-base_width]) {
          cube([bottom_thickness,base_width,base_length]);
          hull() {
            cube([bottom_thickness,5,10+reinforcement_length]);
            translate([-wall_height+bottom_thickness+5,0,wall_thickness])
              cube([0.001,5,0.001]);
          }
        }
      }
      // --- screws for the base ---
      translate([wall_height,wall_width-5.5,20])
        rotate([0,90,0]) {
          translate([-5,0,0])
            cylinder(r=base_screw_diameter/2,h=100,center=true,$fn=6);
          translate([5,0,0])
            cylinder(r=base_screw_diameter/2,h=100,center=true,$fn=6);
        }
      
    } // End of difference
  }
}


module nut_holder() {
   union() {
		difference() {
			nut_holder_no_hole();
	
			translate([base_width-3.7,Y_threaded_rod_dist_from_workbed,0]) {
			  // Hole for the M8 rod
			  hull() {
			    cylinder(r=M8_rod_diameter/2,h=100,$fn=25,center=true);
			    translate([10,0,0])
			      cylinder(r=M8_rod_diameter/2,h=100,$fn=25,center=true);
			  }
			
			  // Slot for the M8 nut
			  translate([0,0,wall_thickness/2]) {
			    cylinder(r=M8_nut_diameter/2,h=M8_nut_height,$fn=6,center=true);
	          translate([0,0,M8_nut_height/2-nut_slot_thickness/2])
	            cylinder(r=nut_slot_length+(M8_nut_diameter/2),h=nut_slot_thickness,$fn=6,center=true);
	          translate([0,0,-(M8_nut_height/2-nut_slot_thickness/2)])
	            cylinder(r=nut_slot_length+(M8_nut_diameter/2),h=nut_slot_thickness,$fn=6,center=true);
	        }
	        //translate([-8,-5,0])
	        //  text(M8_nut_height-M8_nut_height_margin);
			}
		} // End of difference
		translate([base_width-3.7,Y_threaded_rod_dist_from_workbed,0])
			translate([-8,-5,0])
				text(M8_nut_height-M8_nut_height_margin);
   } // End of union
}

module nut_holder_positioned() {
  rotate([90,0,0])
    translate([-(base_width-3.7),0,-wall_thickness/2])
      nut_holder();
}

//for display only, doesn't contribute to final object
build_plate(3,200,200);
rotate([0,-90,0])
  nut_holder();

