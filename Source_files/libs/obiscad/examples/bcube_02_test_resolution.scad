use <obiscad/bcube.scad>

//-- Examples of use of the bcube() module

//-- Standar cube
translate([-15,15,0])
bcube([20,20,10]);

//-- Beveled cube (0 point resolution)
translate([15,15,0])
  bcube([20,20,10],cr=4);

//-- Beveled cube (1 point resolution)
translate([-15,-15,0])
  bcube([20,20,10],cr=4, cres=1);

//-- Beveled cube (4 points resolution)
translate([15,-15,0])
  bcube([20,20,10],cr=4, cres=4);

