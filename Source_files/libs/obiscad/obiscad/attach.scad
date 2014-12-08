//---------------------------------------------------------------
//-- Openscad Attachment library
//-- Attach parts easily. Make your designs more reusable and clean
//---------------------------------------------------------------
//-- This is a component of the obiscad opescad tools by Obijuan
//-- (C) Juan Gonzalez-Gomez (Obijuan)
//-- Sep-2012
//---------------------------------------------------------------
//-- Released under the GPL license
//---------------------------------------------------------------

use <vector.scad>

//--------------------------------------------------------------------
//-- Draw a connector
//-- A connector is defined a 3-tuple that consist of a point
//--- (the attachment point), and axis (the attachment axis) and
//--- an angle the connected part should be rotate around the 
//--  attachment axis
//--
//--- Input parameters:
//--
//--  Connector c = [p , n, ang] where:
//--
//--     p : The attachment point
//--     v : The attachment axis
//--   ang : the angle
//--------------------------------------------------------------------
module connector(c)
{
  //-- Get the three components from the connector
  p = c[0];
  v = c[1];
  ang = c[2];

  //-- Draw the attachment poing
  color("Gray") point(p);

  //-- Draw the attachment axis vector (with a mark)
  translate(p)
    rotate(a=ang, v=v)
    color("Gray") vector(unitv(v)*6, l_arrow=2, mark=true);
}


//-------------------------------------------------------------------------
//--  ATTACH OPERATOR
//--  This operator applies the necesary transformations to the 
//--  child (attachable part) so that it is attached to the main part
//--  
//--  Parameters
//--    a -> Connector of the main part
//--    b -> Connector of the attachable part
//-------------------------------------------------------------------------
module attach(a,b)
{
  //-- Get the data from the connectors
  pos1 = a[0];  //-- Attachment point. Main part
  v    = a[1];  //-- Attachment axis. Main part
  roll = a[2];  //-- Rolling angle
  
  pos2 = b[0];  //-- Attachment point. Attachable part
  vref = b[1];  //-- Atachment axis. Attachable part
                //-- The rolling angle of the attachable part is not used

  //-------- Calculations for the "orientate operator"------
  //-- Calculate the rotation axis
  raxis = cross(vref,v);
    
  //-- Calculate the angle between the vectors
  ang = anglev(vref,v);
  //--------------------------------------------------------.-

  //-- Apply the transformations to the child ---------------------------

  //-- Place the attachable part on the main part attachment point
  translate(pos1)
    //-- Orientate operator. Apply the orientation so that
    //-- both attachment axis are paralell. Also apply the roll angle
    rotate(a=roll, v=v)  rotate(a=ang, v=raxis)
      //-- Attachable part to the origin
      translate(-pos2)
	child(0); 
}


//--------------------------------------------------------------------
//---   An example of the attach operator
//---  
//---  There are two parts: the main body and an arm
//---  They both are cubes (for simplicity)
//---
//--   In the main body there are 2 connectors defined, so that
//--  the arm can be attached to any of them (or both if you like)
//------------------------------------------------------------------

//-- In the debug mode the connectors and additional information
//-- are shown
debug=true;

//-- Define the Main part: A cube
//-- Two attachment points are defined: one on the top, another in the
//--- left side
size = [10,10,10];

//-- Connectors defined:

//--     Att. point       Att. Axis  Roll
c1 = [ [0,0,size[2]/2],  [0,0,1],     20];  //-- Connector on the top
c2 = [ [-size[0]/2,0,0], [-1,0,0],    90];  //-- Connector on the left


//-- Draw the main part along with the connectors (for debugging)
cube(size,center=true);

//-- In debug mode: Draw the main part connectors!
if (debug) {
  connector(c1);
  connector(c2);
}

//-- Define the Attachable part. It is another cube, with one connector
asize = [5,20,3];
a = [ [0,asize[1]/2-3,-asize[2]/2], [0,0,1], 0  ];


//-- Do the attach!
//-- Just change c1 by c2 to attach the part to the other 
//-- connector. Super-easy!! :-)
//-- Modify the c1 and c2 roll angle for rotating the attachable
//--  part to the desired orientation
attach(c1,a)
  //-- This is the attachable part! 
  union() {
    cube(asize,center=true);  //-- The part

    //-- In debug mode show additional info:
    if (debug) {
      frame(l=10);    //-- The part frame of reference.
      connector(a);   //-- Show the part connector
    }
  };

  




