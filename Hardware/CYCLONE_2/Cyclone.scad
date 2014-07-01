// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
// Designed with http://www.openscad.org/


// Include necessary libraries
use <libs/obiscad/vector.scad>
use <libs/obiscad/attach.scad>
use <libs/obiscad/bcube.scad>
use <libs/standard_parts.scad>
use <libs/hole_for_screw.scad>




// Parameters for the bottom base
base_size_X			= 304.8;
base_size_Y			= 261.62;
base_thickness		= 8;
base_corner_radius	= 20;
base_corner_res		= 0;


// Parameters for the axes sizes
axes_Xsmooth_rodLen	= 295;
axes_Ysmooth_rodLen	= 255;
axes_Zsmooth_rodLen	= 150;

axes_Xthreaded_rodLen	= 300;
axes_Ythreaded_rodLen	= 300;
axes_Zthreaded_rodLen	= 100;

axes_Xsmooth_rodD	= 8.5;
axes_Ysmooth_rodD	= 8.5;
axes_Zsmooth_rodD	= 8.5;

axes_Xthreaded_rodD	= 8;
axes_Ythreaded_rodD	= 8;
axes_Zthreaded_rodD	= 8;

// Parameters for the axes reference position
// Note: The reference coordinates are centered like this:
// Y axis reference is the Y smooth rod, BACK of LEFT FRAME
// X axis reference is the X threaded rod edge, LEFT FRAME
// Z axis reference is the Z threaded rod, at the height of the Z nut, and relative to the X reference
axes_Yreference_height	= 30;
axes_Xreference_height	= 60; // relative to Y reference
axes_Zreference_height	= 35; // relative to X reference

axes_Xreference_posY	= 60; // relative to Y reference. Moves the X axis to the front of the machine
axes_Zreference_posY	= 15; // relative to X reference. Positions Z nut between the Y rods


axes_Ysmooth_separation	= 210;
axes_Xsmooth_separation = 40;


// Parameters for the axis-nut offsets (along same axes)
axes_Xnut_offset = 10;
axes_Ynut_offset = 0;

// Carriage positions (for rendering)
axes_Xcarriage_pos = 70;
axes_Ycarriage_pos = 40;
axes_Zcarriage_pos = 20;

// Draw auxiliary reference (LCS axis, etc)
draw_references = true;




// Useful command reference:
//use <MCAD/motors.scad>
//stepper_motor_mount(nema_standard=17, slide_distance=10, $fn=40, mochup=true);

//use <MCAD/boxes.scad>
//roundedBox([10,20,30], radius=2, sidesonly=false, $fn=60);

//use <libs/obiscad/bcube.scad>
//bcube([20,20,10],cr=4, cres=10);

//include <MCAD/stepper.scad>
//motor(Nema17, size=NemaMedium, dualAxis=false);

//use <MCAD/teardrop.scad>
//teardrop(radius=10, length=20, angle=90);

//use <MCAD/nuts_and_bolts.scad>
//nutHole(size=3, tolerance=0.5, proj=-1);
//boltHole(size=3, length=10, tolerance=0.5, proj=-1, $fn=40);

//use <libs/hole_for_screw.scad>
//hole_for_screw(size=3,length=15,nutDepth=0,nutAddedLen=3.5,captiveLen=0);




//-- Connector definitions
//				att. point	att. axis	roll
//C_origin	= [ [0,0,0],     [0,0,1],    0 ];
//C_other		= [ [0,0,20],    [0,1,1],    5 ];

//
//if(draw_references) {
//	%frame();
//	%connector(C_origin);
//	%connector(C_other);
//}

//attach(a,origin) cylinder(r=0.25, h=20, $fn=3);



// BEGIN ASSEMBLING THE DESIGN

// Dummy part for allowing rendering of all objects with %
cube([10,20,30]);

// Main base for the machine
beveledBase([base_size_X,base_size_Y,base_thickness], radius=base_corner_radius, res=base_corner_res);
//%color("brown") translate([0,0,-base_thickness/2]) bcube([base_size_X,base_size_Y,base_thickness], cr=base_corner_radius, cres=base_corner_res);


// A4 paper sheet for reference
standard_paperSheet_A4();


// Cyclone foot stands
foot_offset = 40;
translate([0,0,-base_thickness]) {
	translate([base_size_X/2-foot_offset,base_size_Y/2-foot_offset])
		rubberFoot();
	translate([-base_size_X/2+foot_offset,base_size_Y/2-foot_offset])
		rubberFoot();
	translate([-base_size_X/2+foot_offset,-base_size_Y/2+foot_offset])
		rubberFoot();
	translate([base_size_X/2-foot_offset,-base_size_Y/2+foot_offset])
		rubberFoot();
}

// CHANGE REFERENCE POSITION to the left frame, Y smooth rod end
translate([axes_Ysmooth_separation/2,-axes_Ysmooth_rodLen/2,axes_Yreference_height]) {
	if(draw_references) %frame();
}

// CHANGE REFERENCE POSITION to the left frame, Y smooth rod end
translate([axes_Ysmooth_separation/2,-axes_Ysmooth_rodLen/2,axes_Yreference_height]) {
	if(draw_references) %frame();

	// Draw left Y smooth rod
	standard_rod(diam=axes_Ysmooth_rodD, length=axes_Ysmooth_rodLen, threaded=false);
	// Draw right Y smooth rod
	translate([-axes_Ysmooth_separation,0,0])
		standard_rod(diam=axes_Ysmooth_rodD, length=axes_Ysmooth_rodLen, threaded=false);

	// CHANGE REFERENCE POSITION to the left frame, Y smooth rod end
	translate([axes_Xsmooth_rodLen/2-axes_Ysmooth_separation/2,axes_Xreference_posY,axes_Xreference_height]) {
		if(draw_references) %frame();
		// Draw X threaded rod
		rotate([0,0,90]) standard_rod(diam=axes_Xsmooth_rodD, length=axes_Xsmooth_rodLen, threaded=true);
		// Draw bottom X smooth rod
		translate([0,axes_Xsmooth_separation,0])
			rotate([0,0,90]) standard_rod(diam=axes_Xsmooth_rodD, length=axes_Xsmooth_rodLen, threaded=false);
		// Draw top X smooth rod
		translate([0,0,axes_Xsmooth_separation])
			rotate([0,0,90]) standard_rod(diam=axes_Xsmooth_rodD, length=axes_Xsmooth_rodLen, threaded=false);
		
		// CHANGE REFERENCE POSITION to the X carriage (nut)
		translate([-axes_Xcarriage_pos,0,0]) {
			if(draw_references) %frame();
			cyclone_X_carriage();
			
			// CHANGE REFERENCE POSITION to the X carriage (nut)
			translate([0,axes_Zreference_posY,axes_Zreference_height]) {
				if(draw_references) %frame();
				cyclone_Z_carriage();
			}
		}
	}

}


