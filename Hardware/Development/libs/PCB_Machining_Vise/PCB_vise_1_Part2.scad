//Designed by Forgetful_Guy
//From http://www.thingiverse.com/thing:63578
//License: http://creativecommons.org/publicdomain/zero/1.0/

include <MCAD/nuts_and_bolts.scad>
include <MCAD/materials.scad>

module PCB_vise_1_Part2(with_extra_parts=false, exploded=false) {
  import("./PCB_vise_1_Part2.STL");


  if(with_extra_parts)
    PCB_vise_1_Part2_extras(exploded_distance=(exploded?5:0));

  module PCB_vise_1_Part2_extras(exploded_distance=0) {
    echo("Non-Plastic Parts, 5, Bolt M3 x 16 mm for PCB_vise_1_Part2");
    color(Steel) {
      translate([4,14,2.5+4*exploded_distance])
        rotate([180,0,0]) boltHole(size=3, length=16);
      translate([4,14+28,2.5+4*exploded_distance])
        rotate([180,0,0]) boltHole(size=3, length=16);
      translate([4,14+28*2,2.5+4*exploded_distance])
        rotate([180,0,0]) boltHole(size=3, length=16);
      translate([13,4,2.5+4*exploded_distance])
        rotate([180,0,0]) boltHole(size=3, length=16);
      translate([13+22,4,2.5+4*exploded_distance])
        rotate([180,0,0]) boltHole(size=3, length=16);
    }
  }
}


PCB_vise_1_Part2(with_extra_parts=false, exploded=false);

