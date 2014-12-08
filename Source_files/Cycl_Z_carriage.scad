// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

// TO-DO: Re-program the carriage in a parametric manner

module Cyclone_Z_carriage() {
	color(color_stillPart)
		translate([axes_Zsmooth_separation/2,0,0]) rotate([0,0,-90])
			import("Inherited_files/stl/Cycl_Zcarriage.stl");
	
	// Bearings
	linearBearing_single(model="LM8UU", echoPart=true);
	translate([axes_Zsmooth_separation,0,0])
		linearBearing_single(model="LM8UU", echoPart=true);
	translate([0,0,24.5])
		linearBearing_single(model="LM8UU", echoPart=true);
	translate([axes_Zsmooth_separation,0,24.5])
		linearBearing_single(model="LM8UU", echoPart=true);
	
	// Motor
	translate([axes_Zsmooth_separation/2,30,51]) rotate([180,0,0])
		stepperMotor(screwHeight=0, echoPart=true);
	
	// Dremel tool
	translate([axes_Zsmooth_separation/2,-40,-40]) {
		color([0.2,0.2,0.2]) %cylinder(r1=30/2, r2=50/2, h=40);
		translate([0,0,50])
			color([0.2,0.2,0.2]) %cylinder(r=50/2, h=80);
		translate([0,0,50+80])
			color([0.2,0.2,0.2]) %cylinder(r1=50/2, r2=30/2, h=10);
		translate([0,0,-20])
			color([0.4,0.4,0.4]) %cylinder(r1=12/2, r2=10/2, h=20);
		translate([0,0,-20-20])
			color([0.9,0.9,0.9]) %cylinder(r1=0.5/2, r2=3/2, h=20);
	}
}

