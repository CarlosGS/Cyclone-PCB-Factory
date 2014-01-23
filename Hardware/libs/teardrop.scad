// Downloaded from https://raw.github.com/reprap/huxley/master/OpenSCAD-huxley/Original-files/teardrop.scad
// Make a RepRap teardrop with its axis along Z
// If truncated is true, chop the apex; if not, come to a point

// I stole this function from Erik...


module teardrop(radius, height, truncateMM)
{
	union()
	{
		if(truncateMM > 0)
		{
			intersection()
			{
				translate([truncateMM,0,height/2]) 
					scale([1,1,height])
						cube([radius*2.8275,radius*2,1],center=true);
				scale([1,1,height]) 
						rotate([0,0,3*45])
							cube([radius,radius,1]);
			}
		} else
		{
			scale([1,1,height])
				rotate([0,0,3*45])
					cube([radius,radius,1]);
		}
		cylinder(r=radius, h = height, $fn=20);
	}
}

//teardrop(5, 20, 1);

