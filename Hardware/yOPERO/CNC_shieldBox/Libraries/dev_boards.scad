// KSolids Dev Boards v1.0
// TheNewHobbyist 2013 http://thenewhobbyist.com
// e-mail: chris@thenewhobbyist
// twitter: @thenewhobbyist
//
// Description: 
// Included in this library are many popular development boards
// useful for designing cases, and closures and anything dev
// board related.
//
//	TODO:
//	Arduino UNO, DUO, Leonardo, Mega
//	Beagle board
//	Raspberry Pi
//	Pixie
//	Lillypad
//
// This work is licensed under a Creative Commons Attribution 3.0 Unported License.
//

module arduino_uno() {
	translate([-53.7/2,-68/2,0]) {	
		difference() {
			union() {
				color("SteelBlue") cube([53.7, 67, 1.8]);
				color("SteelBlue") translate([12,67,0]) cube([38.9, 1, 1.8]);
				// color("DimGray") translate([1,23.9,1.8]) cube([2.5,20.8,8]);
				// color("DimGray") translate([1,45.7,1.8]) cube([2.5,20.8,8]);
				// color("DimGray") translate([31.5,31.9,1.8]) cube([9.8,35.5,6.7]);
				// color("DimGray") translate([50.7,32.9,1.8]) cube([2.5,15.8,8]);
				// color("DimGray") translate([50.7,49.7,1.8]) cube([2.5,15.8,8]);
				//color("LightGrey") translate([48.2,21.9,4.05]) cylinder(r=3, h=4.5, center=true, $fn=25);
				//color("LightGrey") translate([48.2,29.4,4.05]) cylinder(r=3, h=4.5, center=true, $fn=25);
				//usb
				color("LightGrey") translate([9.6,-6.7,1.8]) cube([12,16.2,10.5]);
				//color("LightGrey") translate([22.9,52.6,1.8]) cube([6,6,2]);
				// color("RosyBrown") translate([25.9,55.6,4.05]) cylinder(r=1.5, h=1, center=true, $fn=25);
				// color("DimGray") translate([21.1,62.6,1.8]) cube([7.3,5,1]);
				//Power
				color("LightGrey") translate([41.2,-4,1.8]) cube([9,13.5,11]);
				// color("Gold") translate([22.1,63.6,2.8]) cube([5.5, 3, 7 ]);
				}
		// translate([-1.8,64.2,-.5]) rotate([0,0,45]) #cube([6.4,3.6,3]);
		// translate([12,67,-.5]) rotate([0,0,38.7]) cube([6.4,3.6,3]);
		// translate([45.359,70.2,-.5]) rotate([0,0,-30]) cube([6.4,3.6,3]);
		// translate([2.8,16.3,0]) cylinder(r=1.5, h=10, center=true, $fn=25);
		// translate([17,66.1,0]) cylinder(r=1.5, h=10, center=true, $fn=25);
		// translate([44.9,65.8,0]) cylinder(r=1.5, h=10, center=true, $fn=25);
		// translate([50.9,15.7,0]) cylinder(r=1.5, h=10, center=true, $fn=25);
		}
	}
}
module arduino_uno_mounting(h = 10) {
	translate([-53.7/2,-68/2,0]) {
		translate([2.8,16.3,0]) cylinder(r=1.5, h, center=true, $fn=25);
		translate([17,66.1,0]) cylinder(r=1.5, h, center=true, $fn=25);
		translate([44.9,65.8,0]) cylinder(r=1.5,h, center=true, $fn=25);
		translate([50.9,15.7,0]) cylinder(r=1.5, h, center=true, $fn=25);
	}
}

module raspberry_pi(){
	translate([-54/2,81.9/2,0]){
	rotate([0, 0, 270]) {
	union(){
	color("DarkGreen") cube([81.9, 54, 1.8]);
	color("LightGrey") translate([12.2,6.2,1.8]) cylinder(r=3.4, h=10.1, $fn=25);
	color("LightGrey") translate([-3.9,2.2,1.8]) cube([7.8, 7.6, 2.9]);
	color("LightGrey") translate([37.1,-2.1,1.8]) cube([12.4, 12, 4.6]);
	color("LightGrey") translate([63.9,2.2,1.8]) cube([20.9, 15, 12]);	
	color("LightGrey") translate([73.2,25.1,1.8]) cube([14.7, 12, 9.9]);
	color("DimGray") translate([55.3,0,1.8]) cube([4.4, 22, 5]);
	color("DimGray") translate([7.9,16.9,1.8]) cube([4.4, 22, 5]);
	color("DimGray") translate([1.4,48.4,1.8]) cube([31.2, 4.8, 2.4]);
	color("Gold") translate([2.1,49.1,1.8]) cube([29.8, 3.4, 6]);

	color("DimGray") rotate([270,0,0]) translate([56.2, -8.5, 44.1]) {
		cube([13,7.5,12]);
		translate([6.5,3.5,12]) cylinder(r=3, h=4, $fn=25);
	}
	
	rotate([270,0,0]) translate([39.6,-11.5,43.8]) {
		color("Yellow") cube([10,10.5,10.2]);
		color("LightGrey") translate([5,5,10.2]) cylinder(r=3.95, h=8, $fn=25);
	}
}	
}
}
}


module arduino_mega() {
	rotate([0,0,270]) {
		translate([-101.6/2, -53.5/2, 0]) {
			union() {
				difference() {
					color("SteelBlue") cube([101.6,53.5,1.6]);
					translate([-.02,-.02,-.2]) cube([2.5, 12, 2]);
					translate([-.02,52.1,-.2]) cube([3.1, 1.8, 2]);
					translate([11.4,3.2,-5]) cylinder(r=1.6, h=10, $fn=25);
					translate([5.2,50.8,-5]) cylinder(r=1.6, h=10, $fn=25);
					translate([86.4,2.5,-5]) cylinder(r=1.6, h=10, $fn=25);
					translate([86.4,50.8,-5]) cylinder(r=1.6, h=10, $fn=25);
				}
				color("DimGray") translate([44,18.1,1.6]) cube([13.8, 13.8, .7]);
				color("LightGrey") translate([92.1,9,1.6]) cube([16, 12, 11]);
				color("LightGrey") translate([89.5,40.7,1.6]) cube([14.6, 9, 11]);
				color("DimGray") translate([34.3,21.5,1.6]) cube([5.2, 7.8, 2]);
				color("Gold") translate([35.3,22.5,3.6]) cube([3.2, 5.8, 6]);
				color("LightGrey") translate([24.2,22.4,1.6]) cube([6, 7, 3]);
				color("RosyBrown") translate([27.2,25.9,4.6]) cylinder(r=2.1, h=1.5, $fn=25);
				color("DimGray") translate([13.9,1.3,1.6]) cube([21, 2, 9]);
				color("DimGray") translate([36.1,1.3,1.6]) cube([21, 2, 9]);
				color("DimGray") translate([58.5,1.3,1.6]) cube([21, 2, 9]);
				color("DimGray") translate([8.2,49.9,1.6]) cube([21, 2, 9]);
				color("DimGray") translate([31.2,49.9,1.6]) cube([21, 2, 9]);
				color("DimGray") translate([53.9,49.9,1.6]) cube([16, 2, 9]);
				color("DimGray") translate([3,1,1.6]) cube([5, 46.8, 9]);
			}
		}
	}
}

module arduino_mega_mounting() {
	rotate([0,0,270]) {
		translate([-101.6/2, -53.5/2, 0]) {
			translate([11.4,3.2,-5]) cylinder(r=1.6, h=10, $fn=25);
			translate([5.2,50.8,-5]) cylinder(r=1.6, h=10, $fn=25);
			translate([86.4,2.5,-5]) cylinder(r=1.6, h=10, $fn=25);
			translate([86.4,50.8,-5]) cylinder(r=1.6, h=10, $fn=25);
		}
	}
}



