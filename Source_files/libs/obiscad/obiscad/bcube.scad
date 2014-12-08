//------------------------------------------------------------------------------
//  Bevel edge cube.
//  (c) Juan Gonzalez-Gomez (Obijuan), Sep-2012
//------------------------------------------------------------------------------

//----------------- IMPLEMENTATION USING THE MINKOWSKI OPERATOR ----------------

//------------------------------------------------------------------------------
//-- Bevel Cube main function
//-- Parameters:
//--   * Size:  Cube size
//--   * cr : Corner radius (if cr==0, a standar cube is built)
//--   * cres:  Corner resolution (in points). cres=0 means flat corners
//------------------------------------------------------------------------------
module bcube(size,cr=0,cres=0)
{
  //-- Internal cube size
  bsize = size - 2*[cr,cr,0];

  //-- Get the (x,y) coorner coordinates in the 1st cuadrant
  x = bsize[0]/2;
  y = bsize[1]/2;

  //-- A corner radius of 0 means a standar cube!
  if (cr==0)
    cube(bsize,center=true);
  else {

      
      //-- The height of minkowski object is double. So
      //-- we sould scale by 0.5
      scale([1,1,0.5])

      //-- This translation is for centering the minkowski objet
      translate([-x, -y,0])

      //-- Built the  beveled cube with minkowski
      minkowski() {

        //-- Internal cube
        cube(bsize,center=true);

        //-- Cylinder in the corner (1st cuadrant)
        translate([x,y, 0])
          cylinder(r=cr, h=bsize[2],center=true, $fn=4*(cres+1));
      }
  }

}


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


