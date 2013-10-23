// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)

module rod(len=100, threaded=false, dia=8) {
   rotate([90,0,0]) {
   if(threaded)
     color([0.5,0.5,0.5]) cylinder(r=dia/2,h=len,center=true,$fn=30);
   else
     color([0.8,0.8,0.8]) cylinder(r=dia/2,h=len,center=true,$fn=30);
   }
}

