include <MCAD/materials.scad>
include <MCAD/metric_fastners.scad>

module micro_switch(with_extra_parts=false) {
  difference() {
    cube([19.8, 10.8, 6.4]);

    translate([5.15, 2, 0]) {
      translate([0, 0, -0.5])
      cylinder(h = 7.4, R=2.6, $fn=100);
      translate([9.5, 0, -0.5])
      cylinder(h = 7.4, R=2.6, $fn=100);
    }
  }
  translate([2.8, 10.8, 1.2])
  rotate([0,0,10])
  cube([17,1,4]);

  if(with_extra_parts) {
    // --- Self tapping screw 2.2 x 13mm ---
    translate([5.15, 2, 0]) color(Steel) {
      translate([0, 0, 0.5+6.4])
        rotate([180,0,0]) csk_bolt(2.2, 13);
      translate([9.5, 0, 0.5+6.4])
        rotate([180,0,0]) csk_bolt(2.2, 13);
    }
  }
}

micro_switch();
