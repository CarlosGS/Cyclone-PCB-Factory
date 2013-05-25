
// As Cyclone v0.9, this part is derived from the holder for the Y workbed
// The difference is that mount_plate(); is not shown, only the holder itself
// Plus it has been simplified and variables given a better name

// LM8UU bushing holder modified for its use in Cyclone PCB Factory
// Modified to have only one center screw

// Derived by Carlosgs from:

// LM8UU bushing holder
// http://www.thingiverse.com/thing:23041 by thantik
// Inspired/derived from:

//http://www.thingiverse.com/thing:14942
//Which is derived from:
// http://www.thingiverse.com/thing:14814
//And is a drop-in replacement for:
//http://www.thingiverse.com/thing:10287

// main body dimensions
lbearing_holder_width = 20;
lbearing_gap_width = 14;
lbearing_holder_height = 16;
//lbearing_holder_length = 20;
LM8UU_dia = 15.0;
lbearing_holder_extDiam = LM8UU_dia/2+3;

lbearing_holder_rodPos = LM8UU_dia/2+2;

module lm8uu_bearing_holder_XZ(lbearing_holder_length = 20) {
	rotate([0,180,0]) translate([0,0,-lbearing_holder_rodPos])
	intersection() {
      difference()
		{
			union()
			{
				translate([-lbearing_holder_width/2,-lbearing_holder_length/2,0])
					cube([lbearing_holder_width,lbearing_holder_length,lbearing_holder_height]);
			}
		
			// bushing hole
			translate([0,0,lbearing_holder_rodPos])
				rotate([90,0,0])
					cylinder(r=LM8UU_dia/2, h=lbearing_holder_length+0.1, center=true, $fn=40);
		
			// top gap
			translate([0,0,20])
				cube([lbearing_gap_width-1,lbearing_holder_length+0.1,20],center=true);
		}
		translate([0,0,lbearing_holder_rodPos])
			rotate([90,0,0])
				cylinder(r=lbearing_holder_extDiam, h=lbearing_holder_length+0.1, center=true, $fn=40);
	}
}

