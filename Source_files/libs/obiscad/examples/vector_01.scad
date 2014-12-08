//---------------------------------------------
//-- Example of use of the vector library
//---------------------------------------------
use <obiscad/vector.scad>


//-- Place a frame of refence in the origin
frame(l=10);

a = 20;

//-- Define some example vectors
v = [a,a,a];
vh = [a,a,0];  //-- Proyection on the z=0 plane
vv = [0,0,a];  //-- Proyection on the z axis

//-- Draw the vector
vector(v);

//-- Draw the proyection on the z=0 plane
color("Gray") vector(vh);

//-- Draw the proyection on the z axis, but
//-- locate it in the end of the previous vector
color("Gray") 
  translate(vh) vector(vv);

//-- Orientate a cube along the v vector
color("orange")
orientate(v=v,roll=0) 
    cube([2,2,20],center=true);

//-- Add a transparent cube
color("Gray",0.2)
  cube(a);

