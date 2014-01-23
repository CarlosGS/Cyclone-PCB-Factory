//Designed by Forgetful_Guy
//From http://www.thingiverse.com/thing:63578
//License: http://creativecommons.org/publicdomain/zero/1.0/

include <MCAD/metric_fastners.scad>
include <MCAD/materials.scad>
use <../large_washer.scad>
use <./PCB_vise_1_Part2.scad>


module PCB_vise_1_Part1(with_extra_parts=false, exploded=false) {
  import("./PCB_vise_1_Part1.STL");


  if(with_extra_parts)
    PCB_vise_1_Part1_extras(exploded_distance=(exploded?5:0));

  module PCB_vise_1_Part1_extras(exploded_distance=0) {
    echo("Non-Plastic Parts, 2, Large Washer M5 for PCB_vise_1_Part1");
    echo("Non-Plastic Parts, 2, Self Tapping Screw 4.8 x 19 mm for PCB_vise_1_Part1");
    echo("Non-Plastic Parts, 5, Nut M3 for PCB_vise_1_Part1");
    color(Steel) {
      translate([10,20,8.0+exploded_distance]) {
        large_washer(5);
        translate([0,0,largeWasher_H(5)+2+5*exploded_distance]) rotate([180,0,0]) csk_bolt(4.8, 19);
      }
      translate([10,20+40,8.0+exploded_distance]) {
        large_washer(5);
        translate([0,0,largeWasher_H(5)+2+5*exploded_distance]) rotate([180,0,0]) csk_bolt(4.8, 19);
      }
      translate([24-2*exploded_distance,14,8+0.6])
        flat_nut(3);
      translate([24-2*exploded_distance,14+28,8+0.6])
        flat_nut(3);
      translate([24-2*exploded_distance,14+28*2,8+0.6])
        flat_nut(3);
      translate([33,4-2*exploded_distance,8+0.6])
        flat_nut(3);
      translate([33+22,4-2*exploded_distance,8+0.6])
        flat_nut(3);
    }
  }
}


module PCB_vise_1(with_extra_parts=false, exploded=false) {
  PCB_vise_1_Part1(with_extra_parts=with_extra_parts, exploded=exploded);
  translate([20,0,15+0.8])
    PCB_vise_1_Part2(with_extra_parts=with_extra_parts, exploded=exploded);
}

PCB_vise_1(with_extra_parts=false, exploded=false);