

module micro_switch() {
  difference() {
    cube([19.8, 10.8, 6.4]);

    translate([5.15, 2, 0]) {
      translate([0, 0, -0.5])
      cylinder(h = 7.4, R=2.6, $fn=100);
      translate([9.5, 0, -0.5])
      cylinder(h = 7.4, R=2.0, $fn=100);
    }
  }
  translate([2.8, 10.8, 1.2])
  rotate([0,0,10])
  cube([17,1,4]);
}

micro_switch();
