// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


Ycarriage_linearBearingSeparation = 35;


module Cyclone_YsubPart_nutHolder() {
	
}

module Cyclone_Y_carriage() {
	baseHeight = 10;
	color("lightgreen") {
		translate([-10,-5,-5])
			cube([20,15,axes_Y_smoothThreaded_verticalSeparation+10+baseHeight]);
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
	
	translate([0,0,8+5+axes_Y_smoothThreaded_verticalSeparation+baseHeight])
		beveledBase(size=[axes_Ysmooth_separation+50,Ycarriage_linearBearingSeparation+100,8], radius=3, res=15);
}

