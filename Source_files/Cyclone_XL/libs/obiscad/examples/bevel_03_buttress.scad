//-----------------------------------------------------------------------
//-- Example: how to use the bconcave_corner_attach to add buttress easily
//-- to the union of two ortogonal parts
//-----------------------------------------------------------------------

use <obiscad/bevel.scad>
use <obiscad/attach.scad>

//-- Parts parameters
th = 3;
bsize = [30,30,th];
size = [bsize[0],th,20];

//-- The two ortogonal parts
translate([0,0,size[2]/2])
  cube(size,center=true);

cube(bsize,center=true);

//-- Define the connectors
ec1 = [ [bsize[0]/4, -th/2, th/2], [1,0,0],  0];
en1 = [ ec1[0],                    [0,-1,1], 0];

ec2 = [ [-bsize[0]/4, -th/2, th/2], [1,0,0], 0];
en2 = [ ec2[0],           [0,-1,1], 0];

ec3 = [ [0, th/2, th/2], [1,0,0], 0];
en3 = [ ec3[0],           [0,1,1], 0];

//-- Debuging
*connector(ec3);
*connector(en3);

//-- Attach the bconcave_corner part for adding the buttress

//-- 2 small buttress bisector
bconcave_corner_attach(ec1,en1,l=th,cr=5,cres=0);
bconcave_corner_attach(ec2,en2,l=th,cr=5,cres=0);

//-- 1 bigger rounded buttress
bconcave_corner_attach(ec3,en3,l=bsize[0]/2,cr=8,cres=6);

