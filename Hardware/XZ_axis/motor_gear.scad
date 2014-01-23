/* Derived by Carlosgs from:
 * http://www.thingiverse.com/thing:12789
 * An extruder gear set for the TechZone Huxley,
 *  featuring Herringbone teeth.
 * You will have to recalibrate your E_STEPS_PER_MM in
 *  your firmware (ratio changing from original techzone
 *  lasercut gears).
 * This use 2 modules from the MCAD library that you can
 *  get from https://github.com/elmom/MCAD.
 * 
 * Part - the motor gear mount hub with set screw hole -
 *  derived from http://www.thingiverse.com/thing:3104
 *  (thanks GilesBathgate) which is under GPL CC license.
 *
 * August 2013 added 2 extra setscrews to ensure centered usage.
 * by Harry Binnema. 
 *
* Copyright (C) 2011  Guy 'DeuxVis' P.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 * -- 
 *     DeuxVis - device@ymail.com */

include <MCAD/materials.scad>
include <MCAD/teardrop.scad>
include <MCAD/involute_gears.scad>

motor_shaft_diameter=5.4;
pos=15.4-1; //position hole for grubnut
nholes = 7;
shaft_diam=10;
shaft_height=7;

/* Herringbone gear module, adapted from MCAD/involute_gears */
module herringbone_gear( teeth=12, circles=0, shaft=5 ) {
  twist=200;
  height=10;
  pressure_angle=30;

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

	mirror( [0,0,1] )
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
}

module cyclone_motor_z_gear(with_extra_parts=false, exploded=false) {
// Motor gear
rotate([180,0,0]) union() difference() {	 
  union() {

    //gear
    herringbone_gear( teeth=8 );

    translate( [0, 0, 12] ) mirror( [0, 0, 1] ) difference() {
      //shaft
      cylinder( r=shaft_diam, h=shaft_height, $fn=40 );

      //captive nut and grub holes
	for (i=[0:2]){ //3 symmetric grubscrews

 	rotate([0,0,i*120]){     
 		translate( [0, 20, 3.5] ) rotate( [90, 0, 0] ) union() {
        //entrance for nut
          translate( [0, -4.4, pos] ) cube( [5.9, 5.8, 2.45], center=true );
        //nut hole
        translate( [0, 0, pos-1.2] ) rotate( [0, 0, 30] )
          cylinder( r=6/2+0.2, h=2.6, $fn=6 );
        //grub screw hole
        translate( [0, 0, 9] ) cylinder( r=1.5, h=10, $fn=20 );
      				}
				}
			}
   		}
  }

  //shaft hole
  translate( [0, 0, -6] ) cylinder( r=motor_shaft_diameter/2, h=20, $fn=30 );
}

  if(with_extra_parts)
    cyclone_motor_z_gear_extras(exploded_distance = (exploded?24:0));

  module cyclone_motor_z_gear_extras(exploded_distance=0) {
    echo("Non-Plastic Parts, 1, Grub Screw M3 x 8 mm to attach Z motor gear to motor shaft");
    translate([0,-2.5-exploded_distance,-(12-3.5)]) rotate([90, 0, 0]) color(Steel) cylinder(r=1.5, h=8, $fn=30);
  }
}

cyclone_motor_z_gear();
