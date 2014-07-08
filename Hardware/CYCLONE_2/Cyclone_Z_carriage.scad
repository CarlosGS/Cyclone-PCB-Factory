// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/



module Cyclone_Z_carriage() {
	color("cyan") translate([-5,-100+5,0]) {
	cube([axes_Zsmooth_separation+10,100,10]);
	translate([0,0,30])
		cube([axes_Zsmooth_separation+10,100,10]);
	}
}

