// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


use <libs/linear_bearing.scad>
module Cyclone_X_carriage() {
	linearBearingModel = "LM8UU";
	linearBearingLength = linearBearing_L(linearBearingModel);
	linearBearingDiameter = linearBearing_D(linearBearingModel);
	
	// Correction is needed to account for 3D printer tolerances
	axes_effective_Xsmooth_separation = axes_Xsmooth_separation-0.5;
	
	linearBearingSeparation = 0;
	
	sideExtensions = linearBearingDiameter/3+2;
	
	ZrodHolderLength = 30;
	
	screwSize = 3; // M3, M4, etc (integers only)
	screwLength = linearBearingDiameter+sideExtensions;
	screwAditionalLength = 2;
	
	screwExtension = screwSize*1.2;
	
	linearBearingLengthExtension = 6+max(axes_Zsmooth_rodD+axes_Zsmooth_separation-2*linearBearingLength-linearBearingSeparation, linearBearingSeparation);
	
	dimX = 2*linearBearingLength+linearBearingLengthExtension;
	
	module Cyclone_XsubPart_ZnutHolder(holes=false) {
		rod_nut_len = 0.8*axes_Zthreaded_rodD;
		rodTolerance = 0.5;
		rodSize = 8; // M3, M4, etc (integers only)
		dimZ = rod_nut_len+3; // Nut holder thickness
		
		if(!holes) {
			rotate([0,180,0])
				hull() {
					cylinder(r=axes_Zthreaded_rodD+1, h=dimZ);
					translate([0,-axes_Zreference_posY-axes_ZthreadedReference_posY+axes_effective_Xsmooth_separation,dimZ/2])
						cube([dimX,0.1,dimZ], center=true);
				}
		} else {
			// Hole for the main Z nut
			translate([0,0,0.1]) rotate([90,0,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=0,tolerance=0.1);
			// Hole for the Z threaded rod
			translate([0,0,-axes_effective_Xsmooth_separation+dimZ])
				rotate([90,0,0]) standard_rod(diam=axes_Zthreaded_rodD+rodTolerance, length=axes_effective_Xsmooth_separation*2, threaded=true, renderPart=true, center=true);
			translate([0,0,-dimZ-0.01]) rotate([180,0,0]) cylinder(r=axes_Zthreaded_rodD, h=axes_effective_Xsmooth_separation+dimZ, $fn=6);
		}
	}
	
	module Cyclone_XsubPart_XnutHolder(holes=false) {
		rod_nut_len = 0.8*axes_Xthreaded_rodD;
		rodTolerance = 0.5;
		rodSize = 8; // M3, M4, etc (integers only)
		washer_D = 15.8;
		washer_thickness = 1.6;
		
		armWidth = axes_Xthreaded_rodD*2+5;
		
		armThickness = rod_nut_len*2;
		
		if(!holes) {
			translate([armThickness/2,0,-axes_effective_Xsmooth_separation/2+washer_D/2])
				rotate([0,90,0]) bcube([axes_effective_Xsmooth_separation,armWidth,armThickness], cr=3,cres=10);
		} else {
			if(draw_references) %frame();
			translate([-0.01+rod_nut_len/2+6,0,0])
				hull() {
					rotate([0,0,-90]) hole_for_nut(size=8,nutAddedLen=-1.25,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
					translate([2,0,0])
						rotate([0,0,-90]) hole_for_nut(size=6,nutAddedLen=0,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
				}
			translate([armThickness+0.01,0,0])
				rotate([0,0,-90]) hole_for_nut(size=6,nutAddedLen=armThickness,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
		}
	}
	
	difference() {
		// Main shape
		union() {
			hull() {
				rotate([0,90,0]) 
					bcube([linearBearingDiameter,linearBearingDiameter+sideExtensions, dimX], cr=3, cres=5);
				translate([0,axes_effective_Xsmooth_separation,axes_effective_Xsmooth_separation])
					rotate([0,90,0]) 
						bcube([linearBearingDiameter+sideExtensions,linearBearingDiameter, dimX], cr=3, cres=5);
			}
			translate([0,0,-screwExtension/2])
				rotate([0,90,0])
					bcube([linearBearingDiameter+screwExtension,linearBearingDiameter+sideExtensions, dimX], cr=3, cres=5);
			translate([0,axes_effective_Xsmooth_separation+screwExtension/2,axes_effective_Xsmooth_separation])
				rotate([0,90,0]) 
					bcube([linearBearingDiameter+sideExtensions,linearBearingDiameter+screwExtension, dimX], cr=3, cres=5);
			// Bottom right screw
			translate([-linearBearingLength/2-linearBearingSeparation/2,0,-linearBearingDiameter/2-screwExtension/2])
				rotate([90,0,0]) cylinder(r=screwSize*2,h=screwLength, center=true, $fn=6);
			// Bottom left screw
			translate([linearBearingLength/2+linearBearingSeparation/2,0,-linearBearingDiameter/2-screwExtension/2])
				rotate([90,0,0]) cylinder(r=screwSize*2,h=screwLength, center=true, $fn=6);
			// Top screw
			translate([0,axes_effective_Xsmooth_separation+screwExtension/2+linearBearingDiameter/2,axes_effective_Xsmooth_separation])
				cylinder(r=screwSize*2,h=screwLength, center=true, $fn=6);
			// Z nut holder
			translate([0,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation+(linearBearingDiameter+sideExtensions)/2])
				Cyclone_XsubPart_ZnutHolder(holes=false);
			// X nut holder
			translate([-dimX/2,axes_effective_Xsmooth_separation,0])
				rotate([-135,0,0]) Cyclone_XsubPart_XnutHolder(holes=false);
		}
		
		// ----- Hole for the Z carriage space ------
		difference() {
			translate([-dimX/2-0.5,0,-sideExtensions+ZrodHolderLength])
				cube([dimX+1,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation]);
			translate([0,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation+(linearBearingDiameter+sideExtensions)/2])
				Cyclone_XsubPart_ZnutHolder(mainPart=true);
		}
		
		// ----- Hole for the spindle tool ------
		translate([0,-35+8.5,0])
			cylinder(r=35/2, h=100, center=true);
		
		// ----- Holes for the linear bearings ------
		// Bottom right linear bearing
		translate([-linearBearingLength/2-linearBearingSeparation/2,0,0])
			rotate([0,0,90]) linearBearingHole(model=linearBearingModel, lateralExtension=sideExtensions*2+screwExtension*2, lengthExtension=linearBearingLengthExtension);
		// Bottom left linear bearing
		translate([linearBearingLength/2+linearBearingSeparation/2,0,0])
			rotate([0,0,90]) linearBearingHole(model=linearBearingModel, lateralExtension=sideExtensions*2+screwExtension*2, lengthExtension=linearBearingLengthExtension);
		// Top linear bearing
		translate([0,axes_effective_Xsmooth_separation,axes_effective_Xsmooth_separation])
			rotate([90,0,0]) rotate([0,0,90]) linearBearingHole(model=linearBearingModel, lateralExtension=sideExtensions*2+screwExtension*2, lengthExtension=linearBearingLength+linearBearingLengthExtension+linearBearingSeparation);
	
		// ----- Holes for the screws ------
		// Bottom right screw
		translate([-linearBearingLength/2-linearBearingSeparation/2,-screwLength/2-screwAditionalLength/2,-linearBearingDiameter/2-screwExtension/2])
			rotate([0,0,180]) hole_for_screw(size=screwSize,length=screwLength+screwAditionalLength,nutDepth=0,nutAddedLen=0,captiveLen=0);
		// Bottom left screw
		translate([linearBearingLength/2+linearBearingSeparation/2,-screwLength/2-screwAditionalLength/2,-linearBearingDiameter/2-screwExtension/2])
			rotate([0,0,180]) hole_for_screw(size=screwSize,length=screwLength+screwAditionalLength,nutDepth=0,nutAddedLen=0,captiveLen=0);
		// Top screw
		translate([0,axes_effective_Xsmooth_separation+screwExtension/2+linearBearingDiameter/2,axes_effective_Xsmooth_separation+screwLength/2+screwAditionalLength/2])
			rotate([90,0,0]) hole_for_screw(size=screwSize,length=screwLength+screwAditionalLength,nutDepth=0,nutAddedLen=0,captiveLen=0);
		
		// ----- Hole for the Z nut ------
		translate([0,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation+(linearBearingDiameter+sideExtensions)/2])
			Cyclone_XsubPart_ZnutHolder(holes=true);
		
		// ----- Hole for the X nut ------
		translate([-dimX/2,axes_effective_Xsmooth_separation,0])
			rotate([-135,0,0]) Cyclone_XsubPart_XnutHolder(holes=true);
		
		// ----- Holes for the rods ------
		// TRANSLATE REFERENCE POSITION to the Z axis origin (right smooth rod)
		translate([-axes_Zsmooth_separation/2,axes_Zreference_posY,axes_Zreference_height]) {
			// Z smooth rod (right)
			cylinder(r=axes_Zsmooth_rodD/2, h=axes_Zsmooth_rodLen);
			// Z smooth rod (left)
			translate([axes_Zsmooth_separation,0,0])
				cylinder(r=axes_Zsmooth_rodD/2, h=axes_Zsmooth_rodLen);
		}
	}
	// Draw linear bearings
	rotate([0,90,0]) linearBearing_single(model=linearBearingModel, echoPart=true);
	rotate([0,-90,0]) linearBearing_single(model=linearBearingModel, echoPart=true);
	translate([linearBearingLength/2,axes_effective_Xsmooth_separation,axes_effective_Xsmooth_separation])
			rotate([0,-90,0]) linearBearing_single(model=linearBearingModel, echoPart=true);			
}

