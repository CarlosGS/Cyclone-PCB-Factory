// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

include <MCAD/nuts_and_bolts.scad>

module hole_for_screw(size=3,length=20,nutDepth=5,nutAddedLen=0,captiveLen=0,tolerance=0.15) {
	radius = METRIC_NUT_AC_WIDTHS[size]/2+tolerance;
	height = METRIC_NUT_THICKNESS[size]+tolerance;
	translate([0,-length/2,0]) {
	translate([0,-length/2+height+nutAddedLen+nutDepth-0.01,0])
		scale([1,(height+nutAddedLen)/height,1])
			rotate([90,0,0])
				hull() {
					nutHole(size=size, tolerance=tolerance, proj=-1);
					translate([0,captiveLen,0])
						nutHole(size=size, tolerance=tolerance, proj=-1);
				}
	translate([0,length/2-height+0.01,0]) //TODO (from MCAD): proper screw cap values: instead of "height" will use METRIC_BOLT_CAP_HEIGHTS[size]+tolerance;
		rotate([90,0,0])
			render() boltHole(size=size, length=length-2.6+0.5, tolerance=tolerance, proj=-1);
	}
}

module screw_and_nut(size=3,length=20,nutDepth=5,nutAddedLen=0,captiveLen=0,tolerance=0) {
	color("black")
		difference() {
			hole_for_screw(size,length,nutDepth,nutAddedLen,captiveLen,tolerance);
			rotate([0,45,0]) {
				cube([1,1,10],center=true);
				cube([10,1,1],center=true);
			}
	}
}

hole_for_screw(size=3,length=20,nutDepth=0,nutAddedLen=0,captiveLen=10);
