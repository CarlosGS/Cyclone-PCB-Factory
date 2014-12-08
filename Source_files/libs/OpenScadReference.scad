
// Useful OpenScad command reference:

//use <MCAD/motors.scad>
//stepper_motor_mount(nema_standard=17, slide_distance=10, $fn=40, mochup=true);

//use <MCAD/boxes.scad>
//roundedBox([10,20,30], radius=2, sidesonly=false, $fn=60);

//use <libs/obiscad/bcube.scad>
//bcube([20,20,10],cr=4, cres=10);

//include <MCAD/stepper.scad>
//motor(Nema17, size=NemaMedium, dualAxis=false);

//use <MCAD/teardrop.scad>
//teardrop(radius=10, length=20, angle=90);

//use <MCAD/nuts_and_bolts.scad>
//nutHole(size=3, tolerance=0.5, proj=-1);
//boltHole(size=3, length=10, tolerance=0.5, proj=-1, $fn=40);

//use <libs/hole_for_screw.scad>
//hole_for_screw(size=3,length=15,nutDepth=0,nutAddedLen=3.5,captiveLen=0);




//-- Connector definitions
//				att. point	att. axis	roll
//C_origin	= [ [0,0,0],     [0,0,1],    0 ];
//C_other		= [ [0,0,20],    [0,1,1],    5 ];

//
//if(draw_references) {
//	%frame();
//	%connector(C_origin);
//	%connector(C_other);
//}

//attach(a,origin) cylinder(r=0.25, h=20, $fn=3);

