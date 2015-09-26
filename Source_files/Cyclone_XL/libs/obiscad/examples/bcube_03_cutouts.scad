//-------------------------------------------------------------------------
//-- Example of the beveled cube library (bcube)
//-------------------------------------------------------------------------

use <obiscad/bcube.scad>

//-- Set the Corner radius and resolution
cr=4;
cres=4;

//-- Build the object
difference() {
  bcube([40,40,10],cr,cres);
  bcube([20,20,12],cr,cres);
};
