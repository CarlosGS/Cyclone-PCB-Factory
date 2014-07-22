// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

include <MCAD/nuts_and_bolts.scad>

module Cyclone_YsubPart_nutHolder() {
	workbed_separation_from_Y_threaded_rod = axes_Y_smoothThreaded_verticalSeparation+workbed_separation_from_Y_smooth_rod+axes_Ysmooth_rodD/2;
	footThickness = 10;
	screwSeparation = 25;
	rod_nut_len = 0.8*axes_Ythreaded_rodD;
	dimX = axes_Ythreaded_rodD*2+5;
	dimY = screwSeparation+10;
	dimZ = workbed_separation_from_Y_threaded_rod;
	holderExtension = 10;
	rodTolerance = 0.5;
	rodSize = 8; // M3, M4, etc (integers only)
	washer_D = 15.8;
	washer_thickness = 1.6;
	
	difference() {
		// Main shape
		translate([0,0,dimZ/2-holderExtension/2])
			bcube([dimX,dimY,dimZ+holderExtension],cr=3,cres=10);
		// Hole for the rod
		hull() {
			standard_rod(diam=axes_Ythreaded_rodD+rodTolerance, length=dimY*4, threaded=true, renderPart=true, center=true);
			translate([0,0,-holderExtension*2])
				standard_rod(diam=axes_Ythreaded_rodD+rodTolerance, length=dimY*4, threaded=true, renderPart=true, center=true);
		}
		// Hole for the main nut
		translate([0,dimY/2+0.01,0])
			hull() {
				rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=0,tolerance=0.1);
				translate([0,0,-holderExtension*2])
					rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=0,tolerance=0.1);
			}
		translate([0,dimY/2+0.01-rod_nut_len-3,0]) {
			// Hole for the sliding nut
			hull() {
				rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=dimY,captiveLen=0,tolerance=0.5);
				translate([0,0,-holderExtension*2])
					rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=dimY,captiveLen=0,tolerance=0.5);
			}
			// Hole for the washer
			hull() {
				washer_single(diam=washer_D, thickness=washer_thickness, renderPart=true);
				translate([0,0,-holderExtension*2])
					washer_single(diam=washer_D, thickness=washer_thickness, renderPart=true);
			}
		}
		// Holes for the supporting screws
		translate([0,-screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness])
			rotate([90,0,0])
				hole_for_screw(size=3,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0);
		translate([0,+screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness])
			rotate([90,0,0])
				hole_for_screw(size=3,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0);
	}
	translate([0,dimY/2,0])
		rotate([0,90,0]) rotate([90,0,0]) nut(size=8, echoPart=true);
	translate([0,-dimY/2,0])
		rotate([0,90,0]) rotate([-90,0,0]) nut(size=8, echoPart=true);
	translate([0,dimY/2+0.01-rod_nut_len-3,0])
		washer_single(diam=washer_D, thickness=washer_thickness, tolerance=0, echoPart=true);
}

module Cyclone_Y_carriage() {
	baseHeight = workbed_separation_from_Y_smooth_rod-1;
	//projection(cut = true) translate([0,0,-axes_Y_smoothThreaded_verticalSeparation-baseHeight-axes_Ysmooth_rodD/2]){
		Cyclone_YsubPart_nutHolder();
		color("lightgreen") {
			translate([0,0,axes_Y_smoothThreaded_verticalSeparation+baseHeight/2]) {
				translate([axes_Ysmooth_separation/2,Ycarriage_linearBearingSeparation/2])
					cube([10,10,10+baseHeight], center=true);
				translate([-axes_Ysmooth_separation/2,Ycarriage_linearBearingSeparation/2])
					cube([10,10,10+baseHeight], center=true);
				translate([-axes_Ysmooth_separation/2,-Ycarriage_linearBearingSeparation/2])
					cube([10,10,10+baseHeight], center=true);
				translate([axes_Ysmooth_separation/2,-Ycarriage_linearBearingSeparation/2])
					cube([10,10,10+baseHeight], center=true);
			}
		}
	
		color([0.9,0.8,0.8,0.5]) translate([0,0,8+5+axes_Y_smoothThreaded_verticalSeparation+baseHeight])
			beveledBase(size=[workbed_size_X,workbed_size_Y,workbed_thickness], radius=3, res=15, echoPart=true);
	//}
}

