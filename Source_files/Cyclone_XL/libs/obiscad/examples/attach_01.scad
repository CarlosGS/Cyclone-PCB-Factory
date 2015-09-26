use <obiscad/vector.scad>
use <obiscad/attach.scad>


//-- Example of simple part to be attached to another
module arm(debug=false)
{

  //-- In debug mode show the connector and frame of reference
  if (debug) {
    frame(l=10);
    connector(a);
  }

  //color("Brown",0.5)    //-- Debug: make the part transparent
  color("Brown")
  difference() {
    cube(asize,center=true);

    translate([0, -asize[1]/2,0])
      cube([asize[0]/2, asize[1]/3, asize[2]+1],center=true);
  }
}

//-------------------------------
debug=true;

//-------------------- Main part Data -------------------
//-- It is a cube, with 2 connectors
size = [20,20,20];

//-- Connectors
//--     att. point     att. axis    roll
c1 = [ [0,0,size[2]/2],  [0,0,1],     20 ];  //-- Top connector
c2 = [ [-size[0]/2,0,0], [-1,0,0],    -30 ];   //-- Left connector

//-- Draw the cube and its connectos
if (debug) {
  connector(c1);
  connector(c2);
}

//color("Yellow",0.5)  //-- Debug: make the part transparent
cube(size,center=true);


//-------------- Attachable part data ----------------------
//-- It is a cube with 1 connector
asize = [10,40,3];

//-- Connector
//--    att. point                 att. axis  roll
a = [ [0, asize[1]/2-3,-asize[2]/2], [0,0,1],   0  ];

//-- Draw the attachable part apart
translate([40,0,0]) arm(debug);

//------- Attach the parts! -------
attach(c1,a) arm(debug);
attach(c2,a) arm(debug);


