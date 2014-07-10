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
	color("lightred")
		translate([-10,0,-axes_Y_threaded_height])
			cube([20,10,axes_Y_threaded_height+5]);
}


module Cyclone_Y_backFrame() {
	scale([1,-1,1]) Cyclone_Y_frontFrame();
}


module Cyclone_Y_rightSmoothRodIdler(mirrorLogo = false) {
	color("lightcyan")
		translate([-5,0,-axes_Yreference_height]) {
			cube([20,10,axes_Yreference_height+5]);
		}
	translate([0,-10,0]) rotate([90,0,0]) linear_extrude(height=10, center = true) {
		if(mirrorLogo) scale([-1,1]) import("dxf/CycloneLogo.dxf");
		else import("dxf/CycloneLogo.dxf");
	}
}


module Cyclone_Y_leftSmoothRodIdler() {
	scale([-1,1,1]) Cyclone_Y_rightSmoothRodIdler(mirrorLogo = true);
}

