// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


// Load necessary libraries
use <libs/obiscad/vector.scad>
use <libs/obiscad/attach.scad>
use <libs/obiscad/bcube.scad>
use <libs/standard_parts.scad>
use <libs/hole_for_screw.scad>

// Functions for animations. Quick and dirty implementation, will need some cleanup
animated_parts_number = 10;
animated_timePerPart = 1/animated_parts_number;
function animationBump(tbegin,tend,t=$t%1) = ((t >= tbegin) && (t <= tend)) ? (1+sin((t-tbegin)*360/(tend-tbegin)-90)) : 0;
function animatePart(n,dist=30,overlap=animated_timePerPart*0.25) = dist*animationBump((n-1)*animated_timePerPart-overlap,n*animated_timePerPart+overlap);


// Parameters for the bottom base
base_size_X			= 304.8+animatePart(1,overlap=0);
base_size_Y			= 261.62+animatePart(2);
base_thickness		= 8;
base_corner_radius	= 20;
base_corner_res		= 0;


// Parameters for the axes sizes
axes_Xsmooth_rodLen	= 265+animatePart(1,overlap=0);
axes_Ysmooth_rodLen	= 240+animatePart(2);
axes_Zsmooth_rodLen	= 100+animatePart(3);

axes_Xthreaded_rodLen	= axes_Xsmooth_rodLen+50;
axes_Ythreaded_rodLen	= axes_Ysmooth_rodLen-50;
axes_Zthreaded_rodLen	= axes_Zsmooth_rodLen+50;

axes_Xsmooth_rodD	= 8.5+animatePart(4,dist=5);
axes_Ysmooth_rodD	= 8.5+animatePart(4,dist=5);
axes_Zsmooth_rodD	= 8.5+animatePart(4,dist=5);

axes_Xthreaded_rodD	= 8+animatePart(4,dist=5);
axes_Ythreaded_rodD	= 8+animatePart(4,dist=5);
axes_Zthreaded_rodD	= 8+animatePart(4,dist=5);

// Parameters for the axes reference position
// Note: The reference coordinates are centered like this:
// Y axis reference is the Y smooth rod end, BACK of RIGHT FRAME
// X axis reference is the frontal X smooth rod end, RIGHT FRAME
// Z axis reference is the Z threaded rod, at the height of the Z nut, and relative to the X reference
axes_Yreference_height	= 30+animatePart(5);
axes_Xreference_height	= 60+animatePart(6); // relative to Y reference
axes_Zreference_height	= 45+animatePart(7)+animatePart(9); // relative to X reference

axes_Xreference_posY	= -70-animatePart(8)-animatePart(9); // relative to Y reference. Moves the X axis towards the front of the machine
axes_Zreference_posY	= 15; // relative to X reference. Positions Z nut between the Y rods

axes_Y_threaded_height = 25+animatePart(5);

axes_Ysmooth_separation	= 180+animatePart(1,overlap=0);
axes_Xsmooth_separation = 40+animatePart(9);
axes_Zsmooth_separation = 35+animatePart(10,overlap=0);



// Carriage positions (for rendering)
axes_Xcarriage_pos = axes_Xsmooth_rodLen/2+sin($t*360)*axes_Xsmooth_rodLen/3;
axes_Ycarriage_pos = axes_Ysmooth_rodLen/2+sin($t*360)*axes_Ysmooth_rodLen/3;
axes_Zcarriage_pos = axes_Zsmooth_rodLen/3+sin($t*360)*axes_Zsmooth_rodLen/4;



// Calculations
axes_Xreference_posX	= (axes_Ysmooth_separation-axes_Xsmooth_rodLen)/2; // relative to Y reference
axes_Y_smoothThreaded_verticalSeparation = axes_Yreference_height-axes_Y_threaded_height;

// Activate/Deactivate rendering auxiliary references (LCS axis, etc)
draw_references = true;



// Include Cyclone parts
include <Cyclone_X_carriage.scad>
include <Cyclone_Z_carriage.scad>
include <Cyclone_X_frames.scad>
include <Cyclone_Y_carriage.scad>
include <Cyclone_Y_frames.scad>


// BEGIN ASSEMBLING THE DESIGN
if(draw_references) %frame();

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



// TRANSLATE REFERENCE POSITION to the RIGHT frame, Y smooth rod end
translate([-axes_Ysmooth_separation/2,axes_Ysmooth_rodLen/2,axes_Yreference_height]) {
	if(draw_references) %frame();

	// Draw right Y smooth rod
	rotate([0,0,180]) standard_rod(diam=axes_Ysmooth_rodD, length=axes_Ysmooth_rodLen, threaded=false);
	
	Cyclone_X_rightFrame();
	
	
	// TRANSLATE REFERENCE POSITION to the LEFT frame, Y smooth rod end
	translate([axes_Ysmooth_separation,0,0]) {
		if(draw_references) %frame();
		
		// Draw right Y smooth rod
		rotate([0,0,180]) standard_rod(diam=axes_Ysmooth_rodD, length=axes_Ysmooth_rodLen, threaded=false);
		
		Cyclone_X_leftFrame();
	}
	
	
	// TRANSLATE REFERENCE POSITION to the right frame, X lower smooth rod end
	translate([axes_Xreference_posX,axes_Xreference_posY,axes_Xreference_height]) {
		if(draw_references) %frame();
		
		// Draw bottom X smooth rod
		rotate([0,0,-90]) standard_rod(diam=axes_Xsmooth_rodD, length=axes_Xsmooth_rodLen, threaded=false);
		// Draw X threaded rod
		translate([-(axes_Xthreaded_rodLen-axes_Xsmooth_rodLen)/2,axes_Xsmooth_separation,0])
			rotate([0,0,-90]) standard_rod(diam=axes_Xthreaded_rodD, length=axes_Xthreaded_rodLen, threaded=true);
		// Draw top X smooth rod
		translate([0,axes_Xsmooth_separation,axes_Xsmooth_separation])
			rotate([0,0,-90]) standard_rod(diam=axes_Xsmooth_rodD, length=axes_Xsmooth_rodLen, threaded=false);
		
		
		// TRANSLATE REFERENCE POSITION to the X carriage (centered)
		translate([axes_Xcarriage_pos,0,0]) {
			if(draw_references) %frame();
			
			Cyclone_X_carriage();
			
			
			// TRANSLATE REFERENCE POSITION to the Z axis origin (top of X carriage, right smooth rod)
			translate([-axes_Zsmooth_separation/2,axes_Zreference_posY,axes_Zreference_height]) {
				if(draw_references) %frame();
				
				// Draw Z smooth rod (right)
				rotate([90,0,0]) standard_rod(diam=axes_Zsmooth_rodD, length=axes_Zsmooth_rodLen, threaded=false);
				// Draw Z smooth rod (left)
				translate([axes_Zsmooth_separation,0,0])
					rotate([90,0,0]) standard_rod(diam=axes_Zsmooth_rodD, length=axes_Zsmooth_rodLen, threaded=false);
				// Draw Z threaded rod
				translate([axes_Zsmooth_separation/2,0,0])
					rotate([90,0,0]) standard_rod(diam=axes_Zthreaded_rodD, length=axes_Zthreaded_rodLen, threaded=true);
				
				
				// TRANSLATE REFERENCE POSITION to the Z axis reference
					translate([0,0,axes_Zcarriage_pos]) {
						if(draw_references) %frame();
						
						Cyclone_Z_carriage();
					}
			}
		}
	}

}









// TRANSLATE REFERENCE POSITION to the FRONT RIGHT Y rod idler, Y smooth rod end
translate([-axes_Ysmooth_separation/2,-axes_Ysmooth_rodLen/2,axes_Yreference_height]) {
	if(draw_references) %frame();
	
	Cyclone_Y_rightSmoothRodIdler();
}

// TRANSLATE REFERENCE POSITION to the FRONT LEFT Y rod idler, Y smooth rod end
translate([axes_Ysmooth_separation/2,-axes_Ysmooth_rodLen/2,axes_Yreference_height]) {
	if(draw_references) %frame();
	
	Cyclone_Y_leftSmoothRodIdler();
}


// TRANSLATE REFERENCE POSITION to the FRONT Y frame, Y threaded rod end
translate([0,-axes_Ythreaded_rodLen/2,axes_Y_threaded_height]) {
	if(draw_references) %frame();
	
	// Draw Y threaded rod
	standard_rod(diam=axes_Ythreaded_rodD, length=axes_Ythreaded_rodLen, threaded=true);
	
	Cyclone_Y_frontFrame();
	
	
	// TRANSLATE REFERENCE POSITION to the BACK Y frame, Y threaded rod end
	translate([0,axes_Ythreaded_rodLen,0]) {
		if(draw_references) %frame();
		
		Cyclone_Y_backFrame();
	}
}


// TRANSLATE REFERENCE POSITION to the CENTERED Y carriage nut, Y threaded rod
translate([0,-axes_Ysmooth_rodLen/2+axes_Ycarriage_pos,axes_Y_threaded_height]) {
	if(draw_references) %frame();
	
	Cyclone_Y_carriage();
}



