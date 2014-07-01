//---------------------------------------------------------------
//-- Utils. General utilities...
//-- This is a component of the obiscad opescad tools by Obijuan
//-- (C) Juan Gonzalez-Gomez (Obijuan)
//-- Sep-2012
//---------------------------------------------------------------
//-- Released under the GPL license
//---------------------------------------------------------------

//-----------------------------------------------------
//-- Functions for converting a scalar into a vector:
//-----------------------------------------------------
//-- The scalar is interpreted as the x coordinate
function VX(x) = [x,0,0];

//-- The scalar is interpreted as the y coordinate
function VY(y) = [0,y,0];

//-- The scalar is interpreted as the z coordinate
function VZ(z) = [0,0,z];


//-----------------------------------------
//-- Definition for accessing vector componentes easily
//--------------------------------------------------------
X = 0;
Y = 1;
Z = 2;


