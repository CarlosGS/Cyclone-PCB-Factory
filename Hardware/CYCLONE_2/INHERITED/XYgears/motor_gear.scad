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
 * August 2013 added 2 extra setscrews to ensure centered usage.
 * by Harry Binnema. 
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

include <MCAD/materials.scad>
include <MCAD/teardrop.scad>
include <MCAD/involute_gears.scad>

motor_shaft_diameter=5.6;
BigGear_N_Teeth = 21; // 24

nholes = 9; // 7
holes_diam = 6;
hole_distance_from_center = 13.5-4.5+holes_diam/2;

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
					cylinder(r=diam/2, h=truncation_height);
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

module cyclone_motor_gear(with_extra_parts=false, exploded=false) {
// Motor gear
union() difference() {	 
	union() {

		//gear
		herringbone_gear( teeth=BigGear_N_Teeth );

		translate( [0, 0, 12] ) mirror( [0, 0, 1] ) difference() {
			//shaft
			cylinder( r=9, h=15);
			//captive nut and grub holes
			translate( [0, 19.5, 3.5] ) rotate( [90, 0, 0] ) union() {
				//enterance
				translate( [0, -3, 14.5] ) cube( [6, 6, 2.8], center=true );
				//nut
				translate( [0, 0, 14.5] ) rotate( [0, 0, 30] )
					cylinder( r=6/2+0.5, h=2.8, $fn=6, center=true);
				//grub hole
				translate( [0, 0, 9] ) cylinder( r=3.3/2, h=10);
			}
		}
	}

	//holes to save plastic
	//for(i=[0:nholes-1])
	//	rotate( [0, 0, i*360/(nholes)+45])
	//		translate( [hole_distance_from_center, 0] )
	//			cylinder( r=holes_diam/2, h=11, center=true);

	//shaft hole
	translate( [0, 0, -6] ) cylinder( r=motor_shaft_diameter/2, h=20);
}
}


cyclone_motor_gear();
