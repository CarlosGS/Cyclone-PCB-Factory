// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


Ycarriage_linearBearingSeparation = 60;

module Cyclone_Y_carriage() {
	color("lightgreen") {
		translate([-10,-5,-5])
			cube([20,15,axes_Y_smoothThreaded_verticalSeparation+10]);
		translate([0,0,axes_Y_smoothThreaded_verticalSeparation]) {
			translate([axes_Ysmooth_separation/2,Ycarriage_linearBearingSeparation/2])
				cube([10,10,10], center=true);
			translate([-axes_Ysmooth_separation/2,Ycarriage_linearBearingSeparation/2])
				cube([10,10,10], center=true);
			translate([-axes_Ysmooth_separation/2,-Ycarriage_linearBearingSeparation/2])
				cube([10,10,10], center=true);
			translate([axes_Ysmooth_separation/2,-Ycarriage_linearBearingSeparation/2])
				cube([10,10,10], center=true);
		}
	}
	
	translate([0,0,8+5+axes_Y_smoothThreaded_verticalSeparation])
		beveledBase(size=[axes_Ysmooth_separation+50,Ycarriage_linearBearingSeparation+50,8], radius=3, res=15);
}

