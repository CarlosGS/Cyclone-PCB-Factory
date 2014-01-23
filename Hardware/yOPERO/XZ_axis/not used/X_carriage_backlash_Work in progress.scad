// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../libs/obiscad/bcube.scad>
use <../libs/obiscad/bevel.scad>
use <../libs/build_plate.scad>
use <../libs/teardrop.scad>

use <../libs/teardrop.scad>
include <./lm8uu_holder.scad>


cyl_res = 40;

layer_height = 0.4;

X_smooth_rods_sep = 50;
X_smooth_rods_sep_projected = sqrt((X_smooth_rods_sep*X_smooth_rods_sep)/2); // Be careful with this measure, it is not properly named since it is used with the following offset:
smooth_rod_margin = 1;

X_rod_sep_real = X_smooth_rods_sep_projected+smooth_rod_margin;
X_rod_sep_real_diag = sqrt(2*(X_rod_sep_real*X_rod_sep_real));

screw_diam = 4;

M8_rod_diam = 8.2;
M8_rod_hole_diam = M8_rod_diam+0.2;

M8_nut_diameter =  14.6 + .5;

// Adjust these values to match the thickness of the nuts you will use
//nut height between 6 - 7mm
M8_nut_height_Z = 4;
M8_nut_height_X = 6.5 + .5;
//SPRING ANTIBACKLASH

SPRING_OD = 11.76;
SPRING_LEN = 35;
SPRING_COMP = 10;
//SPRING ANTIBACKLASH

X_axis_nut_support_thickness = 10;

X_nut_screw_diam = 3;

lbearing_length = 24;

Z_smooth_rods_sep = 55;
Z_smooth_rods_len = 140;

Z_threaded_rod_len = 120;

lbearing_holder_length = Z_smooth_rods_sep+M8_rod_diam+5;

module rod(len=100) {
	color([0.8,0.8,0.8])
     rotate([90,0,0])
       cylinder(r=8/2,h=len,center=true,$fn=32);
}
module spring(len = SPRING_LEN, rad = SPRING_OD) {
	 translate([0,-SPRING_LEN/4 - M8_nut_height_X +1.5,0])
	    color([0.5,0.5,0.5]) 
	         rotate([90,0,0])
      			 cylinder(r = rad/2, h = len + 2, center=true,$fn=30);     			
}
module rodHole(len=100,radius=M8_rod_hole_diam/2, truncateMM=1) {
	color([0.8,0.8,0.8])
     rotate([90,-90,0])
       translate([0,0,-len/2])
         teardrop(radius, len, truncateMM);
}
//--->yOPERO
module X_nut_holder() {	  
	//x nut holder cover DEBUG only
	*translate([0,0,0-0])
		X_nut_holder_cover_v1();
	//x nut holder cover DEBUG only

		//block 		
		difference() {
			translate([0,-1.5,11.5])
				difference(){
					cube([M8_nut_diameter+8,13,42],center=true);
					translate([0,0,14])
						cube([M8_nut_diameter+10,13,10],center=true);
				}
			//X_Nut
			translate([0,-1.5,0])
				rotate([-90,0,0]) hull() {				
				rotate([0,0,90]){
					cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6,center=true);
				}
				

				// translate([0,0,-5])
				// 	cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6,center=true);
			
				}
		//spring diff
		spring();
		//Nut embedding
		rotate([90,0,0])
				rotate([0,0,90])
					cylinder(r=M8_rod_diam/2+2,h=40,center=true,$fn=6);
	
		
		//Upper screw 
		translate([M8_nut_height_X + 1.5,-1.5,0])
			cylinder(r=X_nut_screw_diam/2,h=60,center=true,$fn=20);
		//Lower screw 
		translate([-M8_nut_height_X - 1.5,-1.5,0])
			cylinder(r=X_nut_screw_diam/2,h=60,center=true,$fn=20);
		//Nut transversal cut 
		translate([0,-1.5,-M8_nut_diameter/2])
			cube([M8_nut_diameter+10,13,M8_nut_diameter],center=true);	
	}
}
module X_nut_holder_cover_antibacklash_base(){
	//x nut holder cover DEBUG only
	*translate([0,0,0-0])
		X_nut_holder_cover_v1();
	//x nut holder cover DEBUG only
		

		//block 		
		difference() {
				translate([0,-1.5,-M8_nut_diameter/2])
				difference(){
						cube([M8_nut_diameter+8,13,M8_nut_diameter],center=true);
					
				}
			//X_Nut
			translate([0,-1.5,0])
				rotate([-90,0,0]) hull() {				
				rotate([0,0,90]){
					cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6,center=true);
				}
				

				// translate([0,0,-5])
				// 	cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6,center=true);
			
				}
		//spring diff
		spring(len=SPRING_LEN/2);
		//Nut embedding
		rotate([90,0,0])
				rotate([0,0,90])
					cylinder(r=M8_rod_diam/2+2,h=40,center=true,$fn=6);
	
		
		//Upper screw 
		translate([M8_nut_height_X + 1.5,-1.5,0])
			#cylinder(r=X_nut_screw_diam/2,h=60,center=true,$fn=20);
		//Lower screw 
		translate([-M8_nut_height_X - 1.5,-1.5,0])
			cylinder(r=X_nut_screw_diam/2,h=60,center=true,$fn=20);
		//Nut transversal cut 
		// translate([0,-1.5,-M8_nut_diameter/2])
		// 	cube([M8_nut_diameter+10,13,M8_nut_diameter],center=true);	
	}
}

module X_nut_holder_cover_v12(){
		//upper join
		translate([-M8_nut_height_X-3,-(13/4+1.25),-2])
			difference(){			
				rotate([90,0,0])
					cylinder(r=X_nut_screw_diam,h=13/2,center=true,$fn=20);
			//screw 
			rotate([90,0,0])
				cylinder(r=X_nut_screw_diam/2,h=400,center=true,$fn=20);
			}
			difference() {
				translate([0,-1.5,11.5])
				cube([M8_nut_diameter+6,12.5,42],center=true);
	
			//block
			rotate([0,45,0]) translate([0,0,-26])
				cube([20,20,20],center=true);
			//bold
			translate([0,-1.5,0])
				rotate([-90,0,0]) hull() {
			
			rotate([0,0,90])
					cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6,center=true);
			}
		//Nut embedding
		rotate([90,0,0])
				rotate([0,0,90])
					cylinder(r=M8_rod_diam/2+2,h=40,center=true,$fn=6);
		//Joints body
		translate([-M8_nut_height_X-3,13/4-2,-2])
			rotate([90,0,0])
				cylinder(r=X_nut_screw_diam,h=20,center=true,$fn=20);
		
		//Upper screw
		translate([M8_nut_height_X+2,-1.5,0])
			cylinder(r=X_nut_screw_diam/2,h=60,center=true,$fn=20);
		//corte para obtener unicamente el nut cover
		translate([0,-1.5,13.25+M8_nut_diameter/2])
			cube([M8_nut_diameter+6,13,42],center=true);	
	}
	
}
//yOPERO<----
module X_nut_holder_cover_v1(){
		//upper join
		translate([-M8_nut_height_X-2,-(13/4+1.25),-2])
			difference(){			
				rotate([90,0,0])
					cylinder(r=X_nut_screw_diam,h=13/2,center=true,$fn=20);
			//taladro m2
			rotate([90,0,0])
				cylinder(r=X_nut_screw_diam/2,h=400,center=true,$fn=20);
			}
			difference() {
				translate([0,-1.5,11.5])
				cube([M8_nut_diameter+6,12.5,42],center=true);
	
			//embellecedor
			rotate([0,45,0]) translate([0,0,-26])
				cube([20,20,20],center=true);
			//bold
				translate([0,-1.5,0])
					rotate([-90,0,0]) hull() {
			
			rotate([0,0,90])
					cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6,center=true);
		}
		//bold embedding
		rotate([90,0,0])
				rotate([0,0,90])
					cylinder(r=M8_rod_diam/2+2,h=40,center=true,$fn=6);
		//Taladro base
		translate([-M8_nut_height_X-2,13/4-2,-2])
			rotate([90,0,0])
				cylinder(r=X_nut_screw_diam,h=20,center=true,$fn=20);
		//taladro m2
		*rotate([90,0,0])
				cylinder(r=X_nut_screw_diam/2,h=40,center=true,$fn=20);
		//Taladro superior >seguro
		translate([M8_nut_height_X+1,-1.5,0])
			cylinder(r=X_nut_screw_diam/2,h=60,center=true,$fn=20);
		//corte para obtener unicamente el nut cover
		translate([0,-1.5,13.25+M8_nut_diameter/2])
			cube([M8_nut_diameter+6,13,42],center=true);	
	}
	
}
//yOPERO<----

module X_nut_holder_cover() {
	X_nut_screw_diam = X_nut_screw_diam*1.2;
	scale([1,1,-1]) rotate([-90,0,0])
	difference() {
		translate([0,0,7])
			cube([M8_nut_diameter+2,3,67],center=true);
		rotate([0,45,0]) translate([0,0,-16])
			cube([20,20,20],center=true);

		rotate([0,45,0]) translate([0,0,19])
			cube([60,20,20],center=true);

		rotate([-90,0,0]) hull() {
			translate([0,-1,0.5])
				rotate([0,0,90])
					cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6);
			translate([0,10,0.5])
				rotate([0,0,90])
					cylinder(r=M8_nut_diameter/2,h=M8_nut_height_X,$fn=6);
		}
		rotate([90,0,0])
				rotate([0,0,90])
					cylinder(r=M8_rod_diam/2+2,h=40,center=true,$fn=6);
		translate([-4,0,10])
			rotate([90,0,0])
				cylinder(r=X_nut_screw_diam/2,h=40,center=true,$fn=20);
	}
}

module X_carriage(show_printbed = 0, show_support = 1) {
  if(show_printbed) {
    //for display only, doesn't contribute to final object
    translate([0,0,-lbearing_holder_width/2])
      build_plate(3,110,140);
  }

  difference() {

  union() {

  // Origin is set on the base of the Z threaded rod
  // ---------- Support for the X nut -------------
  translate([-X_rod_sep_real/2,-lbearing_holder_length/2+X_axis_nut_support_thickness/2+0,0]) {
    rotate([180,235,0]){ X_nut_holder();
  }
}
  // Now, the origin is set on the top smooth rod, and we make a 45deg turn
  translate([-X_rod_sep_real/2,0,X_rod_sep_real])
   rotate([0,45,0]) {
     // --------- Linear bearing supports ------------
	  lm8uu_bearing_holder_XZ(lbearing_holder_length);
	  translate([X_rod_sep_real_diag,0,0])
	    lm8uu_bearing_holder_XZ(lbearing_holder_length);
	  difference() {
       union() { // Join both linear bearing holders
	      translate([X_rod_sep_real_diag/2,0,lbearing_holder_height/4+2])
	        cube([X_rod_sep_real_diag+8,lbearing_holder_length,lbearing_holder_height/2],center=true);
         rotate([0,-45,0]) // Draw a cube for the Z nut holder
           translate([M8_nut_diameter,0,0])
	          cube([M8_nut_diameter*1.5,lbearing_holder_length,lbearing_holder_height/2],center=true);
       }
       // Leave clear the inside of the bearing holders
	    rotate([90,0,0]) {
	      cylinder(r=lbearing_holder_extDiam-1, h=lbearing_holder_length+0.1, center=true, $fn=40);
	      translate([X_rod_sep_real_diag,0,0])
	        cylinder(r=lbearing_holder_extDiam-1, h=lbearing_holder_length+0.1, center=true, $fn=40);
	    }
	  }
   }

   // ------- Z smooth rods holder -------
	translate([0,Z_smooth_rods_sep/2,30/2])
     cube([M8_rod_diam+9,M8_rod_diam+5,50],center=true);
	translate([0,-Z_smooth_rods_sep/2,30/2])
     cube([M8_rod_diam+9,M8_rod_diam+5,50],center=true);
	if(show_support) translate([0,0,-10+2/2])
     cube([M8_rod_diam+9,lbearing_holder_length,2],center=true);

   } // End of union

   // -------- Z axis rod holes --------
	translate([0,0,40-M8_nut_height_Z])
     cylinder(r=M8_nut_diameter/2,h=100,$fn=6);// Nut holder (Z)
	rotate([90,0,0]) {
	  translate([0,70/2-5,0]) // --- Hole for the threaded rod ---
       rodHole(len=50,radius=M8_rod_diam/2+2, truncateMM=2.5);
	  translate([0,Z_smooth_rods_len/2-5,Z_smooth_rods_sep/2])
	    rodHole(len=Z_smooth_rods_len);
	  translate([0,Z_smooth_rods_len/2-5,-Z_smooth_rods_sep/2])
	    rodHole(len=Z_smooth_rods_len);
	}

   } // End of difference
}


module X_carriage_assembled(show_printbed = 0, show_Xrods = 0, show_Zrods = 0) {
  X_carriage(show_printbed);

  if(show_Xrods){
	  // ---- Rods (for reference) ----
	  translate([-X_rod_sep_real/2,0,0]) {
	    color([0.5,0.5,0.5]) rod(len=100);
	  }
	  translate([-X_rod_sep_real/2,0,X_rod_sep_real]) {
	    rod(len=100);
	  }
	  translate([X_rod_sep_real/2,0,0]) {
	    rod(len=100);
	  }
  }

  if(show_Zrods)
	  translate([0,0,0])
	    rotate([90,0,0]) {
	      translate([0,Z_threaded_rod_len/2-10,0])
	        color([0.5,0.5,0.5]) rod(len=Z_threaded_rod_len);
	      translate([0,Z_smooth_rods_len/2-5,Z_smooth_rods_sep/2])
	        rod(len=Z_smooth_rods_len);
	      translate([0,Z_smooth_rods_len/2-5,-Z_smooth_rods_sep/2])
	        rod(len=Z_smooth_rods_len);
	    }
}

module X_carriage_print_plate() {
  //for display only, doesn't contribute to final object
  build_plate(3,110,140);
  translate([0,0,lbearing_holder_length/2])
	  rotate([90,0,0])
	    X_carriage(show_printbed = 0, show_support = 1);
}

X_carriage_assembled(show_printbed = 0,show_Xrods = 1,show_Zrods = 0);
//X_carriage_print_plate();



//uncomment the line below to get the x nut cover
module backlash2(){

	translate([0,SPRING_LEN+M8_nut_diameter/2,0])
		X_nut_holder_cover_antibacklash_base();
	
	
}
module backlash1(){
	
	union(){
		mirror([0,1,0])
			translate([0,0,-0.1])
				rotate([0,0,0])
					X_nut_holder_cover_antibacklash_base();
		
	}
	
}
module antibacklash_cover(){
difference(){
union(){
	//front left nut
	backlash1();	
	//front right nut
	backlash2();
	//back left nut
	mirror([0,0,1])
		backlash1();
	//Middle body
	difference(){
		translate([0,SPRING_LEN/2+5,-M8_nut_diameter/2])
			cube([M8_nut_diameter+8,SPRING_LEN-5,M8_nut_diameter/2],center=true);
	translate([0,SPRING_LEN,0])
		spring(SPRING_LEN-5);
	}
}
//triming to save plastic
translate([0,0,-M8_nut_diameter-2])
	cube([M8_nut_diameter+10,13*10,M8_nut_diameter],center=true);
translate([0,0,M8_nut_diameter+2])
	cube([M8_nut_diameter+10,13*10,M8_nut_diameter],center=true);
}
}
#translate([-X_rod_sep_real/2-.1,-lbearing_holder_length/2+X_axis_nut_support_thickness/2+SPRING_LEN+7.5 ,0]) {
    rotate([180,235,0])

	antibacklash_cover();
}




