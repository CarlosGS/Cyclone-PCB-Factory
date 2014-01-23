//Endstop Holder by NewtonrRob
//http://www.thingiverse.com/thing:30085
//http://creativecommons.org/licenses/by-sa/3.0/

include <MCAD/units.scad>
include <MCAD/materials.scad>
include <MCAD/metric_fastners.scad>
include <MCAD/nuts_and_bolts.scad>
use <micro_switch.scad>

module end_stop_holder(with_extra_parts=false, exploded=false) {
difference() {
	union() {
		cube([4,43,10]);  //4,45,10
		translate([8, 15,0]) cylinder(h = 10, r = 8, $fn = 50);
		cube([16, 15,10]);

		translate([17,6,5]) cube([2,5.75,10], center=true);
		translate([17,6,5]) rotate(a=[60,0,0]) cube([2,5.75,10], center=true);
		translate([17,6,5]) rotate(a=[120,0,0]) cube([2,5.75,10], center=true);
	}
	translate([8, 15,-epsilon]) cylinder(h = 10+2*epsilon, r = 4, $fn = 50);
	translate([5, -epsilon, -epsilon]) cube([6, 15+epsilon,10+2*epsilon]);
	translate([-10, 6, 5]) rotate(a=[0, 90, 0]) cylinder(h = 30, r = 1.5, $fn= 20);
	translate([-10, 28, 5]) rotate(a=[0, 90, 0]) cylinder(h = 30, r = 1, $fn= 20);
	translate([-10, 38, 5]) rotate(a=[0, 90, 0]) cylinder(h = 30, r = 1, $fn= 20);
	translate([17,6,5]) cube([2+epsilon,3.5,6], center=true);
	translate([17,6,5]) rotate(a=[60,0,0]) cube([2+epsilon,3.5,6], center=true);
	translate([17,6,5]) rotate(a=[120,0,0]) cube([2+epsilon,3.5,6], center=true);
}

  if(with_extra_parts) {
    end_stop_holder_extras(exploded_distance=(exploded?8:0));
  }

  module end_stop_holder_extras(exploded_distance=0) {
    echo("Non-Plastic Parts, 6, Washer M3 to attach micro switch on end_stop_holder");
    for(i = [0:2] ) {
      translate([4+i*0.3+(i+1)*0.2*exploded_distance, 28, 5]) rotate([0, 90, 0]) color(Steel) washer(3);
      translate([4+i*0.3+(i+1)*0.2*exploded_distance, 38, 5]) rotate([0, 90, 0]) color(Steel) washer(3);
    }

    echo("Non-Plastic Parts, 1, Micro Switch on end_stop_holder");
    translate([4+3*0.3+exploded_distance, 28-5.15+(10-9.5)/2, 5-2])
      rotate([90,0,90])
        micro_switch(with_extra_parts=true, exploded=(exploded_distance!=0));

    echo("Non-Plastic Parts, 1, Bolt M3 x 18 mm to attach end_stop_holder on smooth rod");
    translate([-3*exploded_distance,6,5])
      rotate([0,90,0])
        color(Steel) boltHole(size=3, length=18);

    echo("Non-Plastic Parts, 1, Nut M3 to attach end_stop_holder on smooth rod");
    translate([17+0.9*3/2+exploded_distance,6,5])
      rotate([0,-90,0])
        rotate([0,0,30]) color(Steel) flat_nut(3);
  }

}


end_stop_holder();
