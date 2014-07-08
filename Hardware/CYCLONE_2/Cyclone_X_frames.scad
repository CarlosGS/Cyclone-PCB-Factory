// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


module Cyclone_X_rightFrame() {
	color("lightyellow")
		translate([axes_Xreference_posX,axes_Xreference_posY-5,-axes_Yreference_height]) {
			cube([15,-axes_Xreference_posY+5,axes_Yreference_height+axes_Xreference_height+axes_Xsmooth_separation+5]);
		}
	color("lightyellow") // smooth rod idler
		translate([axes_Xreference_posX,-10,-axes_Yreference_height]) {
			cube([abs(axes_Xreference_posX)+5,10,axes_Yreference_height+5]);
		}
}


module Cyclone_X_leftFrame() {
	scale([-1,1,1]) Cyclone_X_rightFrame();
}

