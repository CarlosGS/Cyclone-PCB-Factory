// //  Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// // Created by @yOPERO 
// // License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)


use <../libs/build_plate.scad>
use <../libs/MCAD/nuts_and_bolts.scad>
fileNameLogo = "../libs/logo/cyclonelogoC.dxf";

M8_rod_diam = 8.2;
M3_rod_diam = 3.2;

smooth_rod_margin = 1;
Y_rod_height = 40;

base_screw_len = 7;
base_screw_diameter = 5;

frame_width = 25;
frame_height = Y_rod_height-smooth_rod_margin;
frame_depth = 10;

module mainBlock(){
  union(){
    //main block
    translate([0,Y_rod_height/2,0])
        cube([frame_width,Y_rod_height,frame_depth],center=true);
    //top of the block
    hull(){
      translate([frame_width/2 - M8_rod_diam,0,0])
        cylinder(r=M8_rod_diam,h=frame_depth,center = true, $fn=40);

      translate([-frame_width/4,-frame_width/8,0])
        cube([frame_width/2,frame_depth,frame_depth],center=true);
    }
  }
}

module M8rod(){
    cylinder(r=M8_rod_diam/2,h=50,center=true,$fn=40);
}

module gap(){
    translate([-frame_width/4,-frame_depth/8,0])
        cube([frame_width/2,frame_depth/8,frame_depth],center=true);
}

module hole(){
    scale([0.77,1.5,0.77])
    //main block shirnked
        translate([0,Y_rod_height/2 +2+ M8_rod_diam/2,0])
          cube([frame_width,Y_rod_height,frame_depth],center=true);
}

module M3rodAndNut(){
    //M3 screw hole
    translate([-frame_width/4,0,0])
      rotate([90,0,0])        
        cylinder(r=M3_rod_diam/2,h=50,center=true,$fn=40);
    //M3 nut trap
    hull(){
    	translate([-frame_width/4,6,0])
        	rotate([90,0,0])
           		nutHole(3);
    	translate([-frame_width/2,6,0])
        	rotate([90,0,0])
           		nutHole(3); 
        }  	
}

module supportL(){
    mirror([0,0,0])
    translate([17,40 -10/4,0]){
        difference(){
          cube([10,5,10], center = true);
          rotate([90,0,0])
            cylinder(r=base_screw_diameter/2,h=2*base_screw_len,center=true,$fn=6);
      }
    }
}

module supportR(){
    mirror([1,0,0,])
      supportL();
}

module mainBody(){
  mainBlock();
  supportR();
  supportL();
}

module logo(mirror = 0){
	logoDepth =-1.2;
	if(mirror){		
		translate([-frame_width/2 + 1.5,Y_rod_height/4,-frame_depth/2])
			resize([20,20,1.2])
				linear_extrude(file = fileNameLogo, height=2);
	}else{
		mirror([1,0,0])
		translate([-frame_width/2 + 1.5,Y_rod_height/4,-frame_depth/2])
				resize([20,20,1.2])
					linear_extrude(file = fileNameLogo, height=2);
	}
}

module Y_rod_idler(side = 0, logo = 0){
	/*if left, side = 1
	  if right, side = 0*/
	mirror([side,0,0])
	difference(){
	    mainBody();
	    M8rod();
	    M3rodAndNut();
	    gap();
	    hole(); 
      if(logo)
        logo(side);	      
	}
}

module show_printbed(){
	translate([frame_width/2,frame_height/2,-frame_depth/2]) build_plate(3,150,140);
}

module Y_rod_idler_leftX(logo){
	translate([-25,0,0])	
		Y_rod_idler(1, logo);
}

module Y_rod_idler_rightX(logo){
	translate([25,0,0])	
		Y_rod_idler(0, logo);
}

/***************************************************************/
//Y_rod_idler_rightX(logo = 1);
Y_rod_idler_leftX(logo = 1);
// Y_rod_idler_right(); // Without logo
// Y_rod_idler_right(); // Without logo
//show_printbed();






