// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


use <libs/linear_bearing.scad>
use <libs/standard_parts.scad>
module Cyclone_X_carriage_alt() {
	linearBearingLength = linearBearing_L(X_linearBearingModel);
	linearBearingDiameter = linearBearing_D(X_linearBearingModel);
	
	// Correction is needed to account for 3D printer tolerances
	axes_effective_Xsmooth_separation = axes_Xsmooth_separation-axes_Xsmooth_separation_tolerance;
	
	sideExtensions = linearBearingDiameter/3+2;
	
	ZrodHolderLength = 30;
	
	screwSize = X_carriage_screwSize;
	screwLength = linearBearingDiameter+sideExtensions;
	screwAditionalLength = 2;
	
	screwExtension = screwSize*1.2;
	
	linearBearingLengthExtension = 6+max(axes_Zsmooth_rodD+axes_Zsmooth_separation-2*linearBearingLength-X_linearBearingSeparation, X_linearBearingSeparation);
	
	dimX = 2*linearBearingLength+linearBearingLengthExtension;
	
	module Cyclone_XsubPart_ZnutHolder(holes=false) {
		rod_nut_len = 0.8*axes_Zthreaded_rodD;
		rodTolerance = X_threaded_rod_Tolerance;
		rodSize = Z_threaded_rodNutSize; // M3, M4, etc (integers only)
		dimZ = 20; // Nut holder thickness
		Z_bearing_width = bearingWidth(608);
		
		if(!holes) {
			rotate([0,180,0])
				hull() {
					cylinder(r=axes_Zthreaded_rodD+1, h=dimZ);
					translate([0,-axes_Zreference_posY-axes_ZthreadedReference_posY+axes_effective_Xsmooth_separation,dimZ/2])
						cube([dimX,0.1,dimZ], center=true);
				}
		} else {
			// Hole for the main Z nut
			translate([0,0,0.1]) rotate([90,0,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=0, tolerance=0.2);
			// Hole for the Z threaded rod
			translate([0,0,-axes_effective_Xsmooth_separation+dimZ])
				rotate([90,0,0]) standard_rod(diam=axes_Zthreaded_rodD+rodTolerance, length=axes_effective_Xsmooth_separation*2, threaded=true, renderPart=true, center=true);
			translate([0,0,-dimZ-0.01]) rotate([180,0,0]) cylinder(r=axes_Zthreaded_rodD*0.9, h=axes_effective_Xsmooth_separation+dimZ*2, $fn=6);
		}
	}
	
	module Cyclone_XsubPart_XnutHolder(holes=false) {
		rod_nut_len = 0.8*axes_Xthreaded_rodD;
		rodSize = X_threaded_rodNutSize; // M3, M4, etc (integers only)
		washer_D = X_backlash_washer_D;
		washer_thickness = X_backlash_washer_thickness;
		
		holderExtension = 10;
		
		armWidth = axes_Xthreaded_rodD*2+6;
		
		if(!holes) {
			// Main shape
			translate([X_backlash_armThickness/2,0,-axes_effective_Xsmooth_separation/2+holderExtension])
				rotate([0,90,0]) bcube([axes_effective_Xsmooth_separation,armWidth,X_backlash_armThickness], cr=3,cres=10);
			*translate([32/2,0,0])
				rotate([180,0,0]) rotate([0,0,90]) Cyclone_YsubPart_nutHolder();
		} else {
			if(draw_references) %frame();
			translate([-rod_nut_len/2+1,0,0]) rotate([0,0,-90]) rotate([180,0,0]) {
				// Hole for the main nut
				hull() {
					rotate([0,180,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
					translate([0,-3.25,0])
						rotate([0,180,0]) hole_for_nut(size=rodSize-2,nutAddedLen=0,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
				}
				translate([0,3,0])
					hull() {
						rotate([0,180,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
						translate([0,4,0])
							rotate([0,180,0]) hole_for_nut(size=rodSize+2,nutAddedLen=0,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
					}
				// Hole for the sliding nut
				translate([0,-rod_nut_len-3-washer_thickness/2,0]) hull() {
					rotate([0,180,0]) hole_for_nut(size=rodSize,nutAddedLen=X_backlash_armThickness,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.3);
					translate([0,-2.25,0])
						rotate([0,180,0]) hole_for_nut(size=rodSize,nutAddedLen=X_backlash_armThickness,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.3);
				}
				// Hole for the rod
				rotate([0,180,0])hole_for_nut(size=rodSize-2,nutAddedLen=X_backlash_armThickness,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
			}
			// Hole for the washer
			translate([rod_nut_len/2+3+1,0,0]) rotate([0,0,-90]) rotate([180,0,0])
				hull() {
					hull() {
						washer_single(diam=washer_D, thickness=washer_thickness, renderPart=true, tolerance=0.3);
						translate([0,0,-holderExtension*2])
							washer_single(diam=washer_D, thickness=washer_thickness, renderPart=true, tolerance=0.3);
					}
					hull() {
						washer_single(diam=rodSize, thickness=4.5+washer_thickness, renderPart=true, tolerance=0.3);
						translate([0,0,-holderExtension*2])
							washer_single(diam=rodSize, thickness=4.5+washer_thickness, renderPart=true, tolerance=0.3);
					}
				}
			*translate([-0.01+rod_nut_len/2+6,0,0])
				hull() {
					rotate([0,0,-90]) hole_for_nut(size=rodSize,nutAddedLen=-1.25,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
					translate([2,0,0])
						rotate([0,0,-90]) hole_for_nut(size=rodSize-2,nutAddedLen=0,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
				}
			*translate([X_backlash_armThickness+0.01,0,0])
				rotate([0,0,-90]) hole_for_nut(size=rodSize-2,nutAddedLen=X_backlash_armThickness,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
		}
	}
	
	module Cyclone_XsubPart_XnutHolder_SINGLE_NUT(holes=false) {
		rod_nut_len = 0.8*axes_Xthreaded_rodD;
		rodSize = X_threaded_rodNutSize; // M3, M4, etc (integers only)
		washer_D = X_backlash_washer_D;
		
		armWidth = axes_Xthreaded_rodD*2+5;
		
		X_backlash_armThickness = rod_nut_len*2;
		
		if(!holes) {
			translate([X_backlash_armThickness/2,0,-axes_effective_Xsmooth_separation/2+washer_D/2])
				rotate([0,90,0]) bcube([axes_effective_Xsmooth_separation,armWidth,X_backlash_armThickness], cr=3,cres=10);
		} else {
			if(draw_references) %frame();
			translate([-0.01+rod_nut_len/2+6,0,0])
				hull() {
					rotate([0,0,-90]) hole_for_nut(size=8,nutAddedLen=-1.25,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
					translate([2,0,0])
						rotate([0,0,-90]) hole_for_nut(size=6,nutAddedLen=0,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
				}
			translate([X_backlash_armThickness+0.01,0,0])
				rotate([0,0,-90]) hole_for_nut(size=6,nutAddedLen=X_backlash_armThickness,captiveLen=axes_Xthreaded_rodD*3,rot=90,tolerance=0.1);
		}
	}
	
	module Cyclone_XsubPart_XendstopBumper() {
		XendBumper_x = 5;
		XendBumper_y = 53;
		XendBumper_z = 12;
		XendBumper_D = 15;
		translate([XendBumper_x/2, XendBumper_y/2-axes_Xsmooth_separation/2, -XendBumper_z/2-linearBearingDiameter/2]) {
				rotate([0,90,0]) bcube([XendBumper_z,XendBumper_y,XendBumper_x], cr=XendBumper_z/2-0.01, cres=10);
				translate([0,XendBumper_y/2-XendBumper_z/2,0])
					rotate([0,90,0]) cylinder(r=XendBumper_D/2, h=XendBumper_x, center=true);
					//rotate([0,90,0]) bcube([XendBumper_z,XendBumper_y,XendBumper_x], cr=XendBumper_z/2-0.01, cres=10);
			}
	}
	
	color(color_movingPart) difference() {
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
			translate([-linearBearingLength/2-X_linearBearingSeparation/2,0,-linearBearingDiameter/2-screwExtension/2])
				rotate([90,0,0]) cylinder(r=screwSize*2,h=screwLength, center=true, $fn=6);
			// Bottom left screw
			translate([linearBearingLength/2+X_linearBearingSeparation/2,0,-linearBearingDiameter/2-screwExtension/2])
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
			// X endstop bumper
			translate([-dimX/2,axes_effective_Xsmooth_separation,axes_effective_Xsmooth_separation])
				Cyclone_XsubPart_XendstopBumper();
		}
		
		// ----- Hole for the Z carriage space ------
		difference() {
			translate([-dimX/2-0.5,0,-sideExtensions+ZrodHolderLength])
				cube([dimX+1,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation]);
			translate([0,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation+(linearBearingDiameter+sideExtensions)/2])
				Cyclone_XsubPart_ZnutHolder(mainPart=true);
		}
		
		// ----- Hole for the radial bearing ------
			translate([0,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation-(linearBearingDiameter+sideExtensions)/2]) rotate([180,0,0]) bearingHole(depth=Z_bearing_width);
			translate([0,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_effective_Xsmooth_separation-(linearBearingDiameter+sideExtensions)/2]) rotate([180,0,0]) nut(size=axes_Xthreaded_rodD, echoPart=true);
		
		// ----- Hole for the spindle tool ------
		translate([0,-35+8.5,0])
			cylinder(r=34/2, h=100, center=true);
		
		// ----- Holes for the linear bearings ------
		// Bottom right linear bearing
		translate([-linearBearingLength/2-X_linearBearingSeparation/2,0,0])
			rotate([0,0,90]) linearBearingHole(model=X_linearBearingModel, lateralExtension=sideExtensions*2+screwExtension*2, pressureFitTolerance=LinearBearingPressureFitTolerance, lengthExtension=linearBearingLengthExtension);
		// Bottom left linear bearing
		translate([linearBearingLength/2+X_linearBearingSeparation/2,0,0])
			rotate([0,0,90]) linearBearingHole(model=X_linearBearingModel, lateralExtension=sideExtensions*2+screwExtension*2, pressureFitTolerance=LinearBearingPressureFitTolerance, lengthExtension=linearBearingLengthExtension);
		// Top linear bearing
		translate([0,axes_effective_Xsmooth_separation,axes_effective_Xsmooth_separation])
			rotate([90,0,0]) rotate([0,0,90]) linearBearingHole(model=X_linearBearingModel, lateralExtension=sideExtensions*2+screwExtension*2, pressureFitTolerance=LinearBearingPressureFitTolerance, lengthExtension=linearBearingLength+linearBearingLengthExtension+X_linearBearingSeparation);
	
		// ----- Holes for the screws ------
		// Bottom right screw
		translate([-linearBearingLength/2-X_linearBearingSeparation/2,-screwLength/2-screwAditionalLength/2,-linearBearingDiameter/2-screwExtension/2])
			rotate([0,0,180]) hole_for_screw(size=screwSize,length=screwLength+screwAditionalLength,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance);
		// Bottom left screw
		translate([linearBearingLength/2+X_linearBearingSeparation/2,-screwLength/2-screwAditionalLength/2,-linearBearingDiameter/2-screwExtension/2])
			rotate([0,0,180]) hole_for_screw(size=screwSize,length=screwLength+screwAditionalLength,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance);
		// Top screw
		translate([0,axes_effective_Xsmooth_separation+screwExtension/2+linearBearingDiameter/2,axes_effective_Xsmooth_separation+screwLength/2+screwAditionalLength/2])
			rotate([90,0,0]) hole_for_screw(size=screwSize,length=screwLength+screwAditionalLength,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance);
		
		// ----- Hole for the Z nut ------
		translate([0,axes_Zreference_posY+axes_ZthreadedReference_posY,axes_Zreference_height])
		  cylinder(r=8.5+Z_threaded_rod_Tolerance, h=axes_Zsmooth_rodLen);
			//cylinder(r=axes_Zthreaded_rodD*0.9, h=axes_effective_Xsmooth_separation+dimZ*2);
			//	Cyclone_XsubPart_ZnutHolder(holes=true);
			
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
	rotate([0,90,0]) linearBearing_single(model=X_linearBearingModel, echoPart=true);
	rotate([0,-90,0]) linearBearing_single(model=X_linearBearingModel, echoPart=true);
	translate([linearBearingLength/2,axes_effective_Xsmooth_separation,axes_effective_Xsmooth_separation])
			rotate([0,-90,0]) linearBearing_single(model=X_linearBearingModel, echoPart=true);			
}
