// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/


module Cyclone_Y_rightSmoothRodIdler() {
	color("lightcyan")
		translate([-5,0,-axes_Yreference_height]) {
			cube([20,10,axes_Yreference_height+5]);
		}
}


module Cyclone_Y_leftSmoothRodIdler() {
	scale([-1,1,1]) Cyclone_Y_rightSmoothRodIdler();
}

