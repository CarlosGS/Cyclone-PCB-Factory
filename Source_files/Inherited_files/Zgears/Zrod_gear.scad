/* Derived by Carlosgs from:
 * http://www.thingiverse.com/thing:12789
 * An extruder gear set for the TechZone Huxley,
 *	featuring Herringbone teeth.
 * You will have to recalibrate your E_STEPS_PER_MM in
 *	your firmware (ratio changing from original techzone
 *	lasercut gears).
 * This use 2 modules from the MCAD library that you can
 *	get from https://github.com/elmom/MCAD.
 * 
 * Part - the motor gear mount hub with set screw hole -
 *	derived from http://www.thingiverse.com/thing:3104
 *	(thanks GilesBathgate) which is under GPL CC license.
 *
 * Copyright (C) 2011	Guy 'DeuxVis' P.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA	02110-1301, USA.
 * -- 
 *		 DeuxVis - device@ymail.com */

include <MCAD/involute_gears.scad>

M8_nut_diameter = 15.3;
nut_separation = 5;

SmallGear_N_Teeth = 15;
M8_rod_diam = 8.6;

// Increase the resolution of default shapes
$fa = 5; // Minimum angle for fragments [degrees]
$fs = 0.5; // Minimum fragment size [mm]

/* Herringbone gear module, adapted from MCAD/involute_gears */
module herringbone_gear( teeth=12, circles=0, shaft=5 ) {
	twist=0;//100;
	height=10;
	pressure_angle=30;

	diam = teeth*2;
	
	truncation_length = 2.8;
	truncation_height = height/2.5;

	module myGear() {
		difference() {
			gear(
				number_of_teeth=teeth,
				circular_pitch=320,
				pressure_angle=pressure_angle,
				clearance = 0.2,
				gear_thickness = height/2,
				rim_thickness = height/2,
				rim_width = 1,
				hub_thickness = height/2,
				hub_diameter=1,
				bore_diameter=shaft,
				circles=circles,
				twist=twist/teeth
			);
			mirror([0,0,1]) translate([0,0,-height/2-0.01]) {
				difference() {
					cylinder(r=diam/2+1, h=truncation_height);
					translate([0,0,-0.01])
						cylinder(r1=diam/2-truncation_length, r2=diam/2+1, h=truncation_height+0.02);
				}
			}
		}
	}
	
	myGear();
	mirror( [0,0,1] )
		myGear();
}

module cyclone_rod_gear(with_extra_parts=false, exploded=false) {
// Extruder Gear
difference() {
	union() {
		//gear
		rotate([180,0,0]) herringbone_gear( teeth=SmallGear_N_Teeth, circles=0, shaft=M8_rod_diam);
	}

	translate( [0, 0, (nut_separation/2)] ) cylinder( r=M8_nut_diameter/2, h=7, $fn=6 );
}
}

cyclone_rod_gear();
