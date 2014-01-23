//By Glen Chung, 2013.
//Dual licenced under Creative Commons Attribution-Share Alike 3.0 and LGPL2 or later

include <polyScrewThread_r1.scad>


$fn=200;

radius=52/2;
height=100;
thick=3;
pen_hole_radius=15/2;
pen_radius=9.2/2;


module spindle_shell(radius, thick, height) {
  hole_radius = height / 12;
  difference() {
    union() {
      if(1) difference() {
        cylinder(r=radius, h=height);

        translate([0,0,thick])
          cylinder(r=radius-thick, h=height+0.1);

        //holes
        for (angle = [0, 90, 180, 270])
          rotate([0,0,angle+45])
            translate([0,0,height/2])
            scale([1.0,1.0,height/(radius-0)/2])
            translate([radius-thick,0,0])
            rotate([-90,0,0])
            scale([1.5,2,1])
              sphere(r=hole_radius);
      }
      cylinder(r=22/2,h=8);
    }
    translate([0,0,-2])
      spindle_top_screw(pen_hole=11,height=21,with_hole=false);

    for(x=[radius, -radius])
      for(y=[radius, -radius])
        translate([x/2,y/2,-1])
          cylinder(r=2, h=8);
  }
}

module spindle_top_screw(pen_hole=10, thick=3, height=18, head_thick=6, with_hole=true) {
  if(1) difference() {
    if(1) translate([0,0,-head_thick])
      hex_screw(pen_hole+2*thick+1,4,55,height,1.5,2,pen_hole+2*thick+4,head_thick,0,0);
    if(with_hole)
      translate([0,0,-2+12])
        cylinder(r=(pen_hole+1)/2, h=height+3);
  }

  translate([0,0,-2+12])
    scale([1,1,1.5])
      difference() {
        sphere(r=(pen_hole-3)/2);

        translate([0,0,-6])
          cube([10,10,10],center=true);

        translate([0,0,pen_hole*0.6])
          cube([pen_hole,pen_hole,pen_hole],center=true);
      }
}

module pen_holder_single(thick, width, height) {
  difference() {
    translate([-thick,0,0])
      cube([thick*2, width, height]);

	translate([2*thick,0,0])
      rotate([0,0,atan((thick/2)/width)])
        translate([-thick,0,-height/2])
          cube([thick*2, width*2, height*2]);

	translate([-2*thick,0,0])
      rotate([0,0,-atan((thick/2)/width)])
        translate([-thick,0,-height/2])
          cube([thick*2, width*2, height*2]);

    rotate([-40,0,0])
      translate([-thick,0,0])
        cube([thick*2, width*2, height*2]);
  }
}

module pen_holder_four(height=60, radius=radius, thick=thick) {
  difference() {
    for(angle = [0, 90, 180, 270])
      rotate([0,0,angle])
        translate([0,-(radius-thick/2),0])
          rotate([0,0,-atan((pen_radius+0.4)/(radius-thick))])
            pen_holder_single(thick*0.8, radius, height);

    cylinder(r=pen_radius, h=150);
  }
}

module probe_holder()
{
  height = 20;
  probe_radius = 2/2;
  probe_hole_radius = probe_radius + 0.8/2;
  difference() {
    union(){
      difference() {
        cylinder(r=pen_radius+thick, h=height);
	    translate([0,0,-thick/2])
          cylinder(r=pen_radius-0.05, h=height+thick);
		translate([-(pen_radius+thick),0,height])
		  scale([1.6,4,1.5])
            sphere(r=pen_radius+thick);
      }
      translate([pen_radius+5, 0, 0])
      {
        difference(){
          cylinder(r=probe_hole_radius+2.2, h=height);
          translate([0,0,-thick/2])
            cylinder(r=probe_hole_radius, h=height+thick);
	    }
      }
    }
    translate([pen_radius+5*2, 0 , height/2])
	  scale([2,4,1.8])
        sphere(r=(probe_hole_radius+2));
	translate([-10,-pen_radius/2,-1])
	  cube([10, pen_radius, height]);
	translate([pen_radius+5, -probe_hole_radius*.8, height/2])
	  cube([10, probe_hole_radius*1.6, height]);
  }
  translate([20, 0, 0])
  difference() {
    cylinder(r=probe_radius+2.2, h=6);
	translate([0,0,2])
      cylinder(r=probe_radius, h=6);
	translate([0,-probe_radius/2, 2])
	  cube([10, probe_radius, height]);
  }
}

module pen_holder() {
  difference() {
    union() {
      spindle_shell(radius, thick, height);

      translate([40, 0, 6])
        spindle_top_screw(head_thick=6);

      translate([0,0,height-90])
        pen_holder_four(height=90);

      //pen
      if(0) translate([0,0,16])
        cylinder(r=pen_radius, h=135);
    }
    if(0) translate([0,0,-1]) cube([radius*2,radius*2,height+2]);

    for(angle = [0, 180])
      rotate([0,0,angle])
        rotate([0,0,-atan((pen_radius+0.4)/(radius-thick))])
          translate([-thick,2.5*thick,height-15])
            cube([radius+2*thick,radius,radius]);
  }
}

pen_holder();

translate([-60,0,0])
  probe_holder();


