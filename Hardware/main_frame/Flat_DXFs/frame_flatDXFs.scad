// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

use <../frame.scad>

module frame_flatDXF(with_motor = 0, show_printbed = 1) {
  projection(cut=true)
    translate([0,0,-1]) {
      frame(with_motor, show_printbed);
    }
}

//frame_flatDXF(with_motor = 1, show_printbed = 1);
scale([-1,1,1]) frame_flatDXF(with_motor = 0, show_printbed = 1);
