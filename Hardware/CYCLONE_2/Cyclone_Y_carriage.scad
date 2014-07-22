// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


module Cyclone_YsubPart_nutHolder() {
	workbed_separation_from_Y_threaded_rod = axes_Y_smoothThreaded_verticalSeparation+workbed_separation_from_Y_smooth_rod+axes_Ysmooth_rodD/2;
	footThickness = 10;
	screwSeparation = 14;
	dimX = 15;
	dimY = screwSeparation*2;
	dimZ = workbed_separation_from_Y_threaded_rod+10;
	#translate([-10,-dimY/2,-10])
		cube([dimX,dimY,dimZ]);
	translate([0,-screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness])
		rotate([90,0,0])
			hole_for_screw(size=3,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0);
	translate([0,+screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness])
		rotate([90,0,0])
			hole_for_screw(size=3,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0);
}

module Cyclone_Y_carriage() {
	baseHeight = workbed_separation_from_Y_smooth_rod-1;
	color("lightgreen") {
		Cyclone_YsubPart_nutHolder();
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
}

