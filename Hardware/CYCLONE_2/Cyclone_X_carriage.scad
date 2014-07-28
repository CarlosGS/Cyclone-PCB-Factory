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
	
	linearBearingSeparation = 0;
	
	sideExtensions = linearBearingDiameter/3;
	
	ZrodHolderLength = 30;
	
	linearBearingLengthExtension = 6+max(axes_Zsmooth_rodD+axes_Zsmooth_separation-2*linearBearingLength-linearBearingSeparation, linearBearingSeparation);
	
	dimX = 2*linearBearingLength+linearBearingLengthExtension;
	
	difference() {
	//	color("lightblue") translate([-(axes_Zsmooth_separation+10)/2,-5,-5])
	//		cube([axes_Zsmooth_separation+10,axes_Xsmooth_separation+10,axes_Zreference_height+5]);
		*color("lightblue") translate([-dimX/2,-5,-sideExtensions])
			cube([dimX,axes_Xsmooth_separation+10,ZrodHolderLength]);
		hull() {
			rotate([0,90,0]) 
				bcube([linearBearingDiameter,linearBearingDiameter+sideExtensions, dimX], cr=3, cres=5);// cylinder(r=linearBearingDiameter/2, h=dimX, center=true);
			translate([0,axes_Xsmooth_separation,axes_Xsmooth_separation])
				rotate([0,90,0]) 
					bcube([linearBearingDiameter+sideExtensions,linearBearingDiameter, dimX], cr=3, cres=5);// cylinder(r=linearBearingDiameter/2, h=dimX, center=true);
		}
	
		translate([-dimX/2-0.5,0,-sideExtensions+ZrodHolderLength])
			cube([dimX+1,axes_Xsmooth_separation-axes_ZthreadedReference_posY,axes_Xsmooth_separation]);
		
		// ----- Holes for the linear bearings ------
		// Bottom right linear bearing
		translate([-linearBearingLength/2-linearBearingSeparation/2,0,0])
			rotate([0,0,90]) linearBearingHole(model=linearBearingModel, lateralExtension=sideExtensions*2, lengthExtension=linearBearingLengthExtension);
		// Bottom left linear bearing
		translate([linearBearingLength/2+linearBearingSeparation/2,0,0])
			rotate([0,0,90]) linearBearingHole(model=linearBearingModel, lateralExtension=sideExtensions*2, lengthExtension=linearBearingLengthExtension);
		// Top linear bearing
		translate([0,axes_Xsmooth_separation,axes_Xsmooth_separation])
			rotate([90,0,0]) rotate([0,0,90]) linearBearingHole(model=linearBearingModel, lateralExtension=sideExtensions*2, lengthExtension=linearBearingLength+linearBearingLengthExtension+linearBearingSeparation);
		
		// ----- Holes for the rods ------
		// TRANSLATE REFERENCE POSITION to the Z axis origin (right smooth rod)
		translate([-axes_Zsmooth_separation/2,axes_Zreference_posY,axes_Zreference_height]) {
			if(draw_references) %frame();
		
			// Z smooth rod (right)
			rotate([90,0,0]) standard_rod(diam=axes_Zsmooth_rodD, length=axes_Zsmooth_rodLen, threaded=false, renderPart=true);
			// Z smooth rod (left)
			translate([axes_Zsmooth_separation,0,0])
				rotate([90,0,0]) standard_rod(diam=axes_Zsmooth_rodD, length=axes_Zsmooth_rodLen, threaded=false, renderPart=true);
			// Z threaded rod
			translate([axes_Zsmooth_separation/2,axes_ZthreadedReference_posY,0])
				rotate([90,0,0]) standard_rod(diam=1.5*axes_Zthreaded_rodD, length=axes_Zthreaded_rodLen, threaded=true, renderPart=true);
		}
	}
}

