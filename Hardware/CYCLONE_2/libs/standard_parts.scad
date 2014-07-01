// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
// Designed with http://www.openscad.org/

use <obiscad/bcube.scad>

$render_standard_parts = false;

module renderStandardPart() {
	if($render_standard_parts) children();
	else %children();
}

module standard_paperSheet_A4(t=0.05) {
	renderStandardPart()
		translate([0,0,t/2])
			color("white") cube([297,210,t], center=true);
}

module standard_rod(diam=8, length=10, threaded=true, center=false, $fn=18) {
	renderStandardPart()
		if(threaded) {
			color("black") rotate([-90,0,0]) cylinder(r=diam/2, h=length, center=center);
		} else {
			color("grey") rotate([-90,0,0]) cylinder(r=diam/2, h=length, center=center);
		}
}

module rubberFoot(diam=40, thickness=8) {
	renderStandardPart()
		color("black")
			translate([0,0,-thickness])
				cylinder(r=diam/2, h=thickness);
}


module beveledBase(size=[100,200,10], radius=10, res=15) {
	renderStandardPart()
		color("brown")
			translate([0,0,-size.z/2])
				bcube(size, cr=radius, cres=res);
}

