//-----------------------------------------------------------------------
//-- Example: how to use the bevel module to bevel some edges of a Cube
//-----------------------------------------------------------------------

use <obiscad/bevel.scad>
use <obiscad/attach.scad>

//-- Cube size
size=[40,40,15];

//-- Define the connectors for beveling the for top edges

//-- Top-right beveling (rounded)
ec1 = [ [size[0]/2, 0, size[2]/2], [0,1,0], 0];
en1 = [ ec1[0],                    [1,0,1], 0];

//-- Top-left beveling (straight)
ec2 = [ [-size[0]/2, 0, size[2]/2], [0,1,0], 0];
en2 = [ ec2[0],                    [-1,0,1], 0];

//-- Top-front beveling (straight)
ec3 = [ [0, -size[1]/2, size[2]/2], [1,0,0], 0];
en3 = [ ec3[0],                    [0,-1,1], 0];

//-- Top-back beveling (rounded-low-res)
ec4 = [ [0, size[1]/2, size[2]/2], [1,0,0], 0];
en4 = [ ec4[0],                    [0,1,1], 0];

//-- Debug!
*connector(ec4);
*connector(en4);


//-- Perform the beveling!
difference() {

  //-- Main cube
  cube(size,center=true);

  //-- concave_corners for doing the beveling
  bevel(ec1, en1, cr = 8, cres=10, l=size[1]+2);
  bevel(ec2, en2, cr = 4, cres=0, l=size[1]+2);
  bevel(ec3, en3, cr = 10, cres=0, l=size[0]/4);
  bevel(ec4, en4, cr = 10, cres=2, l=size[0]/4);

}

  
