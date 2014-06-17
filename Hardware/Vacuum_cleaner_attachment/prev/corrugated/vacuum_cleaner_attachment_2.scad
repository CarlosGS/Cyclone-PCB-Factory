
tube_diameter = 17;
tube_len = 16.5;
corrugation_depth = 1;

vacuum_cleaner_diam = 30;
vacuum_cleaner_tube_len = 1;
adapter_len = 25-6;

part_diam = 60+15;

tube_separation = tube_diameter+26+5;
tube_angle = 5;

$fn=60;

module corrugated_tube_shape(incL=0) {
$fn=40;
union() {
cylinder(r=tube_diameter/2-corrugation_depth,h=tube_len+incL);
for (i = [0:3.75:tube_len+incL-0.1]) {
translate([0,0,i])
cylinder(r=tube_diameter/2, h=3);
}
}
}

module corrugated_tube_attachment() {
difference() {
//cylinder(r=tube_diameter/2+5, h=30, $fn=30, center=true);
cube([tube_diameter+10,tube_diameter+10,30],center=true);
cylinder(r=tube_diameter/2-corrugation_depth, h=31, $fn=30, center=true);
for (i = [-4:4]) {
translate([0,0,i*3.75])
cylinder(r=tube_diameter/2, h=3, $fn=30, center=true);
}
translate([50,0,0])
cube([100,100,100],center=true);
}
}

*translate([0,-(tube_diameter+10)/2,0]) {
corrugated_tube_attachment();
translate([0,tube_diameter+10,0])
	corrugated_tube_attachment();
}


module vacuum_cleaner_adapter_shape() {
translate([0,tube_separation/2,0])
	rotate([-tube_angle,0,0])
	corrugated_tube_shape(5);
translate([0,-tube_separation/2,0])
	rotate([tube_angle,0,0])
	corrugated_tube_shape(5);

hull() {
translate([0,tube_separation/2,0])
	rotate([-tube_angle,0,0])
	cylinder(r=tube_diameter/2,h=0.01);
translate([0,0,-adapter_len])
	cylinder(r=vacuum_cleaner_diam/2,h=0.01);
}

hull() {
translate([0,-tube_separation/2,0])
	rotate([tube_angle,0,0])
	cylinder(r=tube_diameter/2,h=0.01);
translate([0,0,-adapter_len])
	cylinder(r=vacuum_cleaner_diam/2,h=0.01);
}

translate([0,0,6])
cylinder(r=27/2,h=50);

cylinder(r=(27-3)/2,h=100,center=true);

translate([0,0,-adapter_len-vacuum_cleaner_tube_len])
cylinder(r=vacuum_cleaner_diam/2,h=vacuum_cleaner_tube_len);

//translate([0,0,-adapter_len-vacuum_cleaner_tube_len]) cylinder(r=vacuum_cleaner_diam/2,h=vacuum_cleaner_tube_len);
}

difference() {
	translate([-part_diam/4,-part_diam/2,-adapter_len-vacuum_cleaner_tube_len]) cube([part_diam,part_diam,tube_len+adapter_len+vacuum_cleaner_tube_len]);
	vacuum_cleaner_adapter_shape();
	translate([0,-part_diam/2,-adapter_len-vacuum_cleaner_tube_len]) cube([part_diam,part_diam,tube_len+adapter_len+vacuum_cleaner_tube_len]);
}
