// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

module mirrorOrNot(mirrorPart=false, axes=[-1,1,1]) {
	if(mirrorPart) scale(axes) children();
	else children();
}





module Cyclone_Y_frontFrame() {
	color("red")
		translate([-10,0,-axes_Y_threaded_height])
			cube([20,10,axes_Y_threaded_height+5]);
}


module Cyclone_Y_backFrame() {
	scale([1,-1,1]) Cyclone_Y_frontFrame();
}








module Cyclone_logo(sizemm = 30, thickness = 10, mirrorLogo = false) {
	dxf_logo_size = 50; // Real size of the logo in the DXF file
	scale_factor = sizemm/dxf_logo_size;
	if(mirrorLogo)
		mirror([ 1, 0, 0 ]) linear_extrude(height=thickness) scale(scale_factor) import("dxf/CycloneLogo.dxf", layer="logo");
	else
		linear_extrude(height=thickness) scale(scale_factor) import("dxf/CycloneLogo.dxf", layer="logo");
}

module Cyclone_Y_rightSmoothRodIdler(mirrorLogo = false) {
	holderThickness = 5;
	holderOuterRadius = holderThickness+axes_Ysmooth_rodD/2;
	
	screwSize = 3; // M3, M4, etc (integers only)
	
	dimX = holderOuterRadius*2;
	dimY = 10+screwSize*2;
	dimZ = axes_Yreference_height;
	
	slotHeight = 3;
	screwLength = holderOuterRadius*2;
	
	logoDepth = dimY/4;
	
	
	footSeparation = screwSize*2;
	footThickness = 10;
	
	color("lightcyan") {
		difference() {
			union() {
				translate([0,0,-axes_Yreference_height])
					cube([dimX,dimY,dimZ+holderThickness+axes_Ysmooth_rodD/2]);
				translate([-holderOuterRadius,0,-axes_Yreference_height])
					cube([dimX,dimY,dimZ]);
				rotate([-90,0,0]) cylinder(r=holderOuterRadius, h=dimY);
				translate([0,dimY/2,-axes_Yreference_height])
					hull() {
						translate([-holderOuterRadius-footSeparation,0,0])
							cylinder(r=dimY/2,h=footThickness);
						translate([holderOuterRadius*2+footSeparation,0,0])
							cylinder(r=dimY/2,h=footThickness);
						translate([holderOuterRadius/2,dimY/2+footSeparation,0])
							cylinder(r=dimY/2,h=footThickness);
					}
			}
			standard_rod(diam=axes_Ysmooth_rodD, length=dimY*4, threaded=false, renderPart=true, center=true);
			translate([2.5+holderOuterRadius,dimY/2,holderOuterRadius])
				rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=screwLength+10,nutDepth=10,nutAddedLen=0,captiveLen=10);
			translate([dimX/2,dimY/2,0])
				cube([dimX+1,dimY+1,slotHeight],center=true);
			translate([(dimX-holderOuterRadius)/2,-0.1,-(dimZ+axes_Ysmooth_rodD/2)/2])
				scale([1,-1,1])
					rotate([90,0,0])
						Cyclone_logo(sizemm = min(dimX+holderOuterRadius-5,dimZ-axes_Ysmooth_rodD/2-5), thickness = logoDepth, mirrorLogo = mirrorLogo);
			translate([0,dimY/2,-axes_Yreference_height+footThickness]) {
				translate([-holderOuterRadius-footSeparation,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0);
				translate([holderOuterRadius*2+footSeparation,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0);
				translate([holderOuterRadius/2,dimY/2+footSeparation,0])
					rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0);
			}
		}
	}
	// Draw nuts and bolts
	translate([2.5+holderOuterRadius,dimY/2,holderOuterRadius])
		rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=screwLength+10,nutDepth=10,nutAddedLen=0,captiveLen=0, echoPart=true);
	translate([0,dimY/2,-axes_Yreference_height+footThickness]) {
		translate([-holderOuterRadius-footSeparation,0,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, autoNutOffset=true, echoPart=true);
		translate([holderOuterRadius*2+footSeparation,0,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, autoNutOffset=true, echoPart=true);
		translate([holderOuterRadius/2,dimY/2+footSeparation,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, autoNutOffset=true, echoPart=true);
	}
}


module Cyclone_Y_leftSmoothRodIdler() {
	scale([-1,1,1]) Cyclone_Y_rightSmoothRodIdler(mirrorLogo = true);
}

