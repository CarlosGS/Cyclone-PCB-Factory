


dremel_accessory_diam = 20;
dremel_accesory_height = 12;

aspirator_thickness_thick = 4;
aspirator_thickness_slim = 2;

aspirator_tube_diam = 15;
aspirator_tube_holder_height = 15;

aspirator_hole_height = 15;
aspirator_hole_diam = 15;

dremel_wrench_diam = 25;

// Useful MCAD functions reference

//use <MCAD/motors.scad>
//stepper_motor_mount(nema_standard=17, slide_distance=10, $fn=40, mochup=true);

//use <MCAD/boxes.scad>
//roundedBox([10,20,30], radius=2, sidesonly=false, $fn=60);

//include <MCAD/stepper.scad>
//motor(Nema17, size=NemaMedium, dualAxis=false);


//use <MCAD/teardrop.scad>
//teardrop(radius=10, length=20, angle=90);

//use <MCAD/nuts_and_bolts.scad>
//nutHole(size=3, tolerance=0.5, proj=-1);
//boltHole(size=3, length=10, tolerance=0.5, proj=-1, $fn=40);


use <MCAD/boxes.scad>


difference() {
	roundedBox([dremel_accessory_diam+aspirator_tube_diam*2+aspirator_thickness_thick*3,
		dremel_accessory_diam+aspirator_thickness_thick*2,
		dremel_accesory_height],
		radius=(dremel_accessory_diam+aspirator_thickness_thick*2)/2,
		sidesonly=true, $fn=60);
	
	cylinder(r=dremel_accessory_diam/2, h=dremel_accesory_height+0.1, $fn=60,center=true);
	translate([dremel_accessory_diam/2+aspirator_tube_diam/2+aspirator_thickness_thick,0,0])
		cylinder(r=aspirator_tube_diam/2, h=dremel_accesory_height+0.1, $fn=60,center=true);
}

