//---------------------------------------------------------------
//-- Openscad Bevel library
//-- Bevel the edges or add buttress to your parts!
//---------------------------------------------------------------
//-- This is a component of the obiscad opescad tools by Obijuan
//-- (C) Juan Gonzalez-Gomez (Obijuan)
//-- Sep-2012
//---------------------------------------------------------------
//-- Released under the GPL license
//---------------------------------------------------------------
use <vector.scad>
use <attach.scad>

//-----------------------------------------------------------------
//- Rotate a vector an angle teta around the axis given by the
//-- unit vector k
//-----------------------------------------------------------------
function Rot_axis_ang(p,k,teta) =
  p*cos(teta) + cross(k,p*sin(teta)) + k*dot(k,p)*(1-cos(teta));

//-- Transformation defined by rotating vfrom vector to vto
//-- It is applied to vector v
//-- It returns the transformed vector
function Tovector(vfrom, vto, v) = 
   Rot_axis_ang(v, unitv(cross(vfrom,vto)), anglev(vfrom,vto));

//-- Auxiliary function for extending a vector of 3 components to 4
function ev(v,c=0) = [v[0], v[1], v[2], c];

//-- Calculate the determinant of a matrix given by 3 row vectors
function det(a,b,c) = 
   a[0]*(b[1]*c[2]-b[2]*c[1])
 - a[1]*(b[0]*c[2]-b[2]*c[0])  
 + a[2]*(b[0]*c[1]-b[1]*c[0]);


//-- Sign function. It only returns 2 values: -1 when x is negative,
//-- or 1 when x=0 or x>0
function sign2(x) = sign(x)+1 - abs(sign(x));

//--------------------------------------------------------------------
//-- Beveled concave corner
//-- NOT AN INTERFACE MODULE (The user should call bconcave_corner instead)
//--
//-- Parameters:
//--   * cr: Corner radius
//--   * cres: Corner resolution
//--   * l: Length
//-    * th: Thickness
//--------------------------------------------------------------------
module bconcave_corner_aux(cr,cres,l,th)
{
  
  //-- vector for translating the  main cube
  //-- so that the top rigth corner is on the origin
  v1 = -[(cr+th)/2, (cr+th)/2, 0];

  //-- The part frame of reference is on the
  //-- internal corner
  v2 = [cr,cr,0];

  //-- Locate the frame of ref. in the internal
  //-- corner
  translate(v2)
  difference() {

    //-- Main cube for doing the corner
    translate(v1)
        //color("yellow",0.5)
        cube([cr+th, cr+th, l],center=true);
 
    //-- Cylinder used for beveling...
    cylinder(r=cr, h=l+1, center=true, $fn=4*(cres+1));
  }
}


//-----------------------------------------------------------------------------
//-- API MODULE
//--
//-- Beveled concave corner
//--
//-- Parameters:
//--   * cr: Corner radius
//--   * cres: Corner resolution
//--   * l: Length
//-    * th: Thickness
//--   * ext_corner: Where the origin is locate. By default it is located
//--       in the internal corner (concave zone). If true, 
//--       it will be in the external corner (convex zone)
//----------------------------------------------------------------------------
module bconcave_corner(cr=1,cres=4,th=1,l=10,ext_corner=false)
{
  //-- Locate the origin in the exterior edge
  if (ext_corner==true)
    translate([th,th,0]) 
      bconcave_corner_aux(cr,cres,l,th);
  else
     //-- Locate the origin in the interior edge
     translate([0.01, 0.01,0])
       bconcave_corner_aux(cr,cres,l,th);
}

//----------------------------------------------------------------------
//-- Auxiliary module (NOT FOR THE USER!)
//-- It is and standar "attach", particularized for placing concave
//-- corners
//----------------------------------------------------------------------
module bconcave_corner_attach_final(
        cfrom,  //-- Origin connector
        cto,    //-- Target connector
        cr,
        cres,
        l,
        th,
        ext_corner)
{
 
  //-- This block represent an attach operation
  //-- It is equivalent to:  attach(cto,cfrom)
  translate(cto[0])
    rotate(a=cto[2], v=cto[1])
      rotate(a=anglev(cfrom[1],cto[1]), 
             v=cross(cfrom[1],cto[1]) )
        translate(-cfrom[0]) 

  //-- Place the concave corner (along with some debug information)
  union() {
    //color("Blue")
    //connector(cfrom);
    //connector([cfrom[0],cnormal_v,0]);
    bconcave_corner(cr=cr,
             cres=cres, 
             l=l,
             th=th,
             ext_corner=ext_corner);
  }
}


//-------------------------------------------------------------------------
//-- Auxiliary module (NOT FOR THE USER!)
//-- It is the general module for performing the bconcave corner attach
//-- All the parameters should be passed to it
//--
//--  External connectors are where de concave corner will be placed. They
//--  are provided by the user
//--
//--  Internal connectors refers to the connectors of the concave corner
//--
//--  Then an attach between the internal and external connectors is done
//-------------------------------------------------------------------------
module bconcave_corner_attach_aux(

         //-- External connectors
         edge_c, 
         normal_c,

         //-- Internal connectors
         iedge_c,
         inormal_c,

	 //-- Other params
         cr,
         cres,
         th,
         l,
         ext_corner)

{
  //-- Get the Corner vectors from the internal connectors
  cedge_v = iedge_c[1];         //-- Corner edge vector
  cnormal_v = inormal_c[1];     //-- Corner normal vector

  //-- Get the vector paralell and normal to the edge
  //-- From the external connectors
  edge_v = edge_c[1];      //-- Edge verctor
  enormal_v = normal_c[1]; //-- Edge normal vector

  //---------------------------------------------------------------
  //-- For doing a correct attach, first the roll angle for the  
  //-- external connector should be calculated. It determines the
  //-- orientation of the concave corner around the edge vector
  //--
  //-- This orientation is calculated using the edge normal vectors
  //-- that bisec the corner
  //--
  //-- There are 2 different cases: depending on the relative angle
  //-- between the internal and external edges. They can be parallel
  //-- or not
  //-----------------------------------------------------------------
  //-- The roll angle has two components: the value and the sign

  //-- Calculate the sign of the rotation (the sign of roll)
  s=sign2(det(cnormal_v,enormal_v,edge_v));

  //-- Calculate the roll when the edges are paralell
  rollp = s*anglev(cnormal_v, enormal_v);

  //-- Calculate the roll in the general case
  Tcnormal_v = Tovector(cedge_v, edge_v, cnormal_v);
  rollg=s*anglev(Tcnormal_v, enormal_v);

  //-- For the paralell case... use rollp
  if (mod(cross(cedge_v,edge_v))==0) {
    //echo("Paralell");

     //-- Place the concave bevel corner!
     bconcave_corner_attach_final(
       cfrom = [[0,0,0],   cedge_v,   0],
       cto   = [edge_c[0], edge_c[1], rollp],
       cr    = cr,
       cres  = cres,
       l     = l,
       th    = th,
       ext_corner = ext_corner);
  }

  //-- For the general case, use rollg
  else {
    //echo("not paralell");

     //-- Place the concave bevel corner!
     bconcave_corner_attach_final(
       cfrom = [[0,0,0],   cedge_v,   0],
       cto   = [edge_c[0], edge_c[1], rollg],
       cr    = cr,
       cres  = cres,
       l     = l,
       th    = th,
       ext_corner = ext_corner);
  }
}

//---------------------------------------------------------------------------
//-- API MODULE
//--
//--  Bevel an edge. A concave corner is located so that the calling 
//--  module can easily perform a difference() operation
//--
//--  Two connectors are needed:
//--    * edge_c   : Connector located on the edge, paralell to the edge
//--    * normal_c : Connector located on the same point than edge_c 
//--                 pointing to the internal corner part, in the direction
//--                 of the corner bisector
//--    * cr        : Corner radius
//--    * cres      : Corner resolution
//--    * l         : Corner length
//--------------------------------------------------------------------------  
module bevel(
           edge_c, 
           normal_c,
           cr=3,
           cres=3,
           l=5)
{

  //-- Call the general module with the correct internal connectors
  bconcave_corner_attach_aux(

         //-- External connectors
         edge_c   = edge_c,
         normal_c = normal_c,

	 //-- Internal connectors 
         iedge_c   = [[0,0,0], unitv([0,0,1]), 0],
         inormal_c = [[0,0,0], [-1,-1,0]       , 0],

         //-- The other params
         cr=cr,
         cres=cres,
         l=l,
         th=1,
         ext_corner=false);
}


//---------------------------------------------------------------------------
//-- API MODULE
//--
//--  Attach a Beveled concave corner
//--  Two connectors are needed:
//--    * edge_c   : Connector located on the edge, paralell to the edge
//--    * normal_c : Connector located on the same point than edge_c 
//--                 pointing to the internal corner part, in the direction
//--                 of the corner bisector
//--    * cr        : Corner radius
//--    * cres      : Corner resolution
//--    * l         : Corner length
//--    * th        : Corner thickness (not visible when ext_corner=false)
//--    * ext_corner: If the exterior corner is used as a reference
//--------------------------------------------------------------------------  
module bconcave_corner_attach(
           edge_c, 
           normal_c,
           cr=3,
           cres=3,
           l=5, 
           th=1,
           ext_corner=false)
{

  //-- Call the general module with the correct internal connectors
  bconcave_corner_attach_aux(

         //-- External connectors
         edge_c   = edge_c,
         normal_c = normal_c,

	 //-- Internal connectors 
         iedge_c   = [[0,0,0], unitv([0,0,1]), 0],
         inormal_c = [[0,0,0], [1,1,0]       , 0],

         //-- The other params
         cr=cr,
         cres=cres,
         l=l,
         th=th,
         ext_corner=ext_corner);

}
  
//-----------------------------------------------------------
//---   TEST MODULES
//-----------------------------------------------------------

//-----------------------------------------------------------------
//--  Testing the Bevel operator... All the 12 edges of a cube
//--  are beveled. All the cases are covered, so it is a good
//--  test for finding bugs!
//----------------------------------------------------------------
module Test1_beveled_cube()
{
  //-------- Main object
  size=[30,30,30];


  //-- Define all the edges connectors
  ec1 = [[size[0]/2, 0,size[2]/2], [0,1,0], 0];
  en1 = [ec1[0],                   [1,0,1], 0];

  ec2 = [[-size[0]/2, 0,size[2]/2], [0,1,0], 0];
  en2 = [ec2[0],                   [-1,0,1], 0];

  ec3 = [[-size[0]/2, 0,-size[2]/2], [0,1,0], 0];
  en3 = [ec3[0],                   [-1,0,-1], 0];

  ec4 = [[size[0]/2, 0,-size[2]/2], [0,1,0], 0];
  en4 = [ec4[0],                   [1,0,-1], 0];

  ec5 = [[0, size[0]/2,size[2]/2], [1,0,0], 0];
  en5 = [ec5[0],                   [0,1,1], 0];

  ec6 = [[0, -size[0]/2,size[2]/2], [1,0,0], 0];
  en6 = [ec6[0],                   [0,-1,1], 0];

  ec7 = [[0, -size[0]/2,-size[2]/2], [1,0,0], 0];
  en7 = [ec7[0],                   [0,-1,-1], 0];

  ec8 = [[0, size[0]/2,-size[2]/2], [1,0,0], 0];
  en8 = [ec8[0],                    [0,1,-1], 0];

  ec9 = [[size[2]/2, size[0]/2,0 ], [0,0,1], 0];
  en9 = [ec9[0],                    [1,1,0], 0];

  ec10 = [[size[2]/2, -size[0]/2,0 ], [0,0,1], 0];
  en10 = [ec10[0],                    [1,-1,0], 0];

  ec11 = [[-size[2]/2, -size[0]/2,0 ], [0,0,1], 0];
  en11 = [ec11[0],                    [-1,-1,0], 0];

  ec12 = [[-size[2]/2, size[0]/2,0 ], [0,0,1], 0];
  en12 = [ec12[0],                    [-1,1,0], 0];


  //-- for Debuging... Show a specefic connector
  *connector(ec12);
  *connector(en12);

  //-- Parameters for all the beveled edges
  //-- It can be changed for testing
  cr=2;
  cres=0;

  //-- Remove from the main cube the concave corner parts
  difference() {

    //-- Draw the main cube
    cube(size,center=true); 

    //-- Attach the concave corners for beveling!
    bevel(ec1,en1,cr=cr,cres=0, l=size[1]+2);
    bevel(ec2,en2,cr=cr,cres=0, l=size[1]+2);
    bevel(ec3,en3,cr=cr,cres=0, l=size[1]+2);
    bevel(ec4,en4,cr=cr,cres=0, l=size[1]+2);

    bevel(ec5,en5,cr=cr,cres=0, l=size[0]+2);
    bevel(ec6,en6,cr=cr,cres=0, l=size[0]+2);
    bevel(ec7,en7,cr=cr,cres=0, l=size[0]+2);
    bevel(ec8,en8,cr=cr,cres=0, l=size[0]+2);

    bevel(ec9,en9,cr=cr,cres=0, l=size[0]+2);
    bevel(ec10,en10,cr=cr,cres=0, l=size[0]+2);
    bevel(ec11,en11,cr=cr,cres=0, l=size[0]+2);
    bevel(ec12,en12,cr=cr,cres=0, l=size[0]+2);

  }
}

//----------------------------------------------------------------
//-- Testing the bconcave_corner_attach operator
//-- It is used for adding buttress between two ortogonal parts
//----------------------------------------------------------------
module Test2_buttress()
{
  size=[30,30,30];
  th=3;
  l=2;
  cr = 6;
 

  //-- A cross. It divides the space in 4 quadrants
  difference() {  
    cube(size,center=true);
    translate([size[0]/4 + th/2, 0, size[0]/4 + th/2])
      cube([size[0]/2, size[1]+2, size[2]/2],center=true);

    translate([-size[0]/4 - th/2, 0, size[0]/4 + th/2])
      cube([size[0]/2, size[1]+2, size[2]/2],center=true);

    translate([-size[0]/4 - th/2, 0, -size[0]/4 - th/2])
      cube([size[0]/2, size[1]+2, size[2]/2],center=true);

    translate([size[0]/4 + th/2, 0, -size[0]/4 - th/2])
      cube([size[0]/2, size[1]+2, size[2]/2],center=true);
  }

  ec1 = [[th/2, size[1]/2-l/2, th/2], [0,1,0], 0];
  en1 = [ec1[0],[1,0,1],0];

  ec2 = [[th/2, -size[1]/2+l/2, th/2], [0,1,0], 0];
  en2 = [ec2[0],[1,0,1],0];

  ec3 = [[-th/2, 0, th/2], [0,1,0], 0];
  en3 = [ec3[0],[-1,0,1],0];

  ec4 = [[-th/2, 0, -th/2], [0,1,0], 0];
  en4 = [ec4[0],[-1,0,-1],0]; 

  ec5 = [[th/2, 0, -th/2], [0,1,0], 0];
  en5 = [ec5[0],[1,0,-1],0]; 

  *connector(ec5);
  *connector(en5);
 
  //-- quadrant 1:  two buttress
  bconcave_corner_attach(ec1,en1,cr, l=l, cres=0);
  bconcave_corner_attach(ec2,en2,cr, l=l, cres=0);
  
  //-- quadrant 2:  one bit buttress
  bconcave_corner_attach(ec3,en3,cr=3, l=size[1], cres=0);

  //-- quadrant 3: a Rounded buttress
  bconcave_corner_attach(ec4,en4,cr=8, l=size[1], cres=5);

  //-- Quadrant 4: A rounded buttress in the middle
  bconcave_corner_attach(ec5,en5,cr=8, l=size[1]/3, cres=5);

}

//-------------------------------------------------------------------
//--   TESTS
//-------------------------------------------------------------------

//-- example 1: A beveled concave corner
bconcave_corner(cr=15, cres=10, l=10, th=3, ext_corner=true);

//-- Example 2: Testing the bevel() operator
//Test1_beveled_cube();

//-- Example 3: Testing the bconcave_corner_attach() operator
//Test2_buttress();



