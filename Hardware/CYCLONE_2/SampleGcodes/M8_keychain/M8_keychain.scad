
l = 40;
d1 = 15;
d2 = d1*1.5;
d3 = 4;
d4 = 14.65;

difference() {
	union() {
		square([d1,l], center=true);
		translate([0,l/2])
			circle(r=d1/2, $fn=40);
		translate([0,-l/2])
			circle(r=d2/2, $fn=40);
	}
	translate([0,l/2])
		circle(r=d3/2, $fn=40);
	translate([0,-l/2-d4/3])
		rotate(90) circle(r=d4/2, $fn=6);
	translate([0,-l/2-d4*1.3])
		rotate(90) circle(r=d4, $fn=6);
}

