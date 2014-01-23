/* 	Version 3
	Added support for font selection (default is Letters.dxf)
	Added WriteCube module
	Added Rotate for text (rotates on the plane of the text)
	Added writesphere
	Added space=     (spacing between characters in char widths) def=1
	Added writecylinder()

 By Harlan Martin
 harlan@sutlog.com
 January 2012

 (The file TestWrite.scad gives More usage examples)
 (This module requires the file Letters.dxf to reside in the same folder)
 (The file Letters.dfx was created with inkscape..Each letter is in its own layer)
 (This module seperates each letter in the string and imports it from Letters.dfx)
 
*/

	pi=3.1415926535897932384626433832795028841971693993751058209;
	pi2=pi*2;


// These control the default values for write() writesphere() writecube()
// if the parameters are not included in the call. Feel free to set your own
// defaults.

//default settings
	center=false;
	h = 4;			 //mm letter height
	t = 1; 			//mm letter thickness
	space =1; 			//extra space between characters in (character widths)
	rotate=0;			// text rotation (clockwise)
	font = "Letters.dxf";	//default for aditional fonts
	fontPath = "./"; // CGS MOD: Path for the DXF font files


// write cube defaults
	face = "front";	 // default face (top,bottom,left,right,back,front)
	up =0;		 //mm up from center on face of cube
	down=0;
	right =0;		 //mm left from center on face of cube
	left=0;		
	

// write sphere defaults
	rounded=false;	 //default for rounded letters on writesphere
	north=0; 		// intial text position (I suggest leave these 0 defaults)
	south=0;
	east=0;
	west=0;
	spin=0;
// writecylinder defaults
	middle=0;     //(mm toward middle of circle)
	ccw=false;   //write on top or bottom in a ccw direction
 	r1=0; 	//(not implimented yet)
	r2=0;	 	//(not implimented yet)
	


// Contact me if your interested in how to make your own font files
// Its tedious and time consuming, but not very hard


module writecylinder(text,where,radius,height){
	wid=(.125* h *5.5 * space);
	widall=wid*(len(text)-1)/2; 
	//angle that measures width of letters on sphere
	function NAngle(radius)=(wid/(pi2*radius))*360;
	//angle of half width of text
	function mmangle(radius)=(widall/(pi2*radius)*360);
	
	if ((face=="top")||(face=="bottom") ){
		if (face=="top" ){
			if (center==true){
				writecircle(text,where+[0,0,height/2],radius-h,rotate=rotate,font=font,h=h,t=t,
				space=space,east=east,west=west,middle=middle,ccw=ccw);
			}else{
				writecircle(text,where+[0,0,height],radius-h,rotate=rotate,font=font,h=h,t=t,
				space=space,east=east,west=west,middle=middle,ccw=ccw);
			}
		}else{
			rotate(180,[1,0,0])
			if (center==true){
				writecircle(text,where+[0,0,height/2],radius-h,rotate=rotate,font=font,h=h,t=t,
				space=space,east=east,west=west,middle=middle,ccw=ccw);
			}else{
				writecircle(text,where+[0,0,0],radius-h,rotate=rotate,font=font,h=h,t=t,
				space=space,east=east,west=west,middle=middle,ccw=ccw);
			}
		}
	
	}else{
//		if (radius>0){
			if (center==true)  {
				rotate(-mmangle(radius)*(1-abs(rotate)/90),[0,0,1])
				translate(where)
				writethecylinder(text,where,radius,height,r1=radius,r2=radius,h=h,
					rotate=rotate,t=t,font=font,face=face,up=up,down=down,
					east=east,west=west,center=center,space=space,rounded=rounded);
			} else{
				rotate(-mmangle(radius)*(1-abs(rotate)/90),[0,0,1])
				translate(where+[0,0,height/2])
					writethecylinder(text,where,radius,height,r1=radius,r2=radius,h=h,
					rotate=rotate,t=t,font=font,face=face,up=up,down=down,
					east=east,west=west,center=center,space=space,rounded=rounded);
			}
// the remarked out code is for cone shaped cylinders (not complete)
//		}else{
//			if (center==true)  {
//				rotate(-mmangle(radius)*(1-abs(rotate)/90),[0,0,1])
//				translate(where)
//				writethecylinder(text,where,radius,height,r1=r1,r2=r2,h=h,
//					rotate=rotate,t=t,font=font,face=face,up=up,down=down,
//					east=east,west=west,center=center,space=space,rounded=rounded);
//			} else{
//				rotate(-mmangle(radius)*(1-abs(rotate)/90),[0,0,1])
//				translate(where+[0,0,height/2])
//					writethecylinder(text,where,radius,height,r1=r1,r2=r2,h=h,
//					rotate=rotate,t=t,font=font,face=face,up=up,down=down,
//					east=east,west=west,center=center,space=space,rounded=rounded);
//			}
//		}
	}
}
module writecircle(text,where,radius){
	wid=(.125* h *5.5 * space);
	widall=wid*(len(text)-1)/2;
	//angle that measures width of letters on sphere
	function NAngle(radius)=(wid/(pi2*radius))*360;
	//angle of half width of text
	function mmangle(radius)=(widall/(pi2*radius)*360);	
	
	if (ccw==true){
		rotate(-rotate+east-west,[0,0,1]){
			rotate(-mmangle(radius-middle),[0,0,1]){
			translate(where)
				for (r=[0:len(text)-1]){
					rotate(-90+r*NAngle(radius-middle),[0,0,1]) // bottom out=-270+r 
					translate([radius-middle,0,0])
					//rotate(90,[1,0,0])
					//rotate(90,[0,1,0])
					rotate(-270,[0,0,1])  // flip text (botom out = -270)
					write(text[r],center=true,h=h,t=t,font=font);
				}
			}
		}
	}else{
		rotate(-rotate-east+west,[0,0,1]){
			rotate(mmangle(radius-middle),[0,0,1]){
			translate(where)
				for (r=[0:len(text)-1]){
					rotate(90-r*NAngle(radius-middle),[0,0,1]) // bottom out=-270+r 
					translate([radius-middle,0,0])
					//rotate(90,[1,0,0])
					//rotate(90,[0,1,0])
					rotate(270,[0,0,1])  // flip text (botom out = -270)
					write(text[r],center=true,h=h,t=t,font=font);
				}
			}
		}		
	}

}
module writethecylinder(text,where,radius,height,r1,r2){
	wid=(.125* h *5.5 * space);
	widall=wid*(len(text)-1)/2; 
	//angle that measures width of letters on sphere
	function NAngle(radius)=(wid/(pi2*radius))*360*(1-abs(rotate)/90);
	//angle of half width of text

	function mmangle(radius)=(widall/(pi2*radius)*360);
			translate([0,0,up-down])
			rotate(east-west,[0,0,1])
			for (r=[0:len(text)-1]){
				rotate(-90+(r*NAngle(radius)),[0,0,1])
				translate([radius,0,-r*((rotate)/90*wid)+(len(text)-1)/2*((rotate)/90*wid)])
				rotate(90,[1,0,0])
				rotate(90,[0,1,0])
				write(text[r],center=true,h=h,rotate=rotate,t=t,font=font);
		//echo("zloc=",height/2-r*((rotate)/90*wid)+(len(text)-1)/2*((rotate)/90*wid));
			}

}


module writesphere(text,where,radius){
	wid=(.125* h *5.5 * space);
	widall=wid*(len(text)-1)/2;
	
	echo("-----------------",widall,wid,mmangle(radius));
	//angle that measures width of letters on sphere
	function NAngle(radius)=(wid/(pi2*radius))*360;
	//angle of half width of text
	function mmangle(radius)=(widall/(pi2*radius)*360);	

	rotate(east-west,[0,0,1]){
	rotate(south-north,[1,0,0]){
	rotate(spin,[0,1,0]){
	rotate(-mmangle(radius),[0,0,1]){
		if ( rounded== false ){
			translate(where)
			for (r=[0:len(text)-1]){
				rotate(-90+r*NAngle(radius),[0,0,1])
				translate([radius,0,0])
				rotate(90,[1,0,0])
				rotate(90,[0,1,0])
				write(text[r],center=true,h=h,rotate=rotate,t=t,font=font);
			}
		}else{
			difference(){
				translate(where)
				for (r=[0:len(text)-1]){
					rotate(-90+r*NAngle(radius),[0,0,1])
					translate([radius,0,0])
					rotate(90,[1,0,0])
					rotate(90,[0,1,0])
					write(text[r],center=true,h=h,rotate=rotate,t=t*2+h,font=font);
				}
				difference(){ //rounded outside
					sphere(radius+(t*2+h)*2);
					sphere(radius+t/2);
				}
				sphere(radius-t/2); // rounded inside for indented text
			} 
		}
	}
}}}
}


module writecube(text,where,size){
	if (str(size)[0] != "["){  
		// its a square cube (size was not a matrix so make it one)
		writethecube(text,where,[size,size,size],h=h,rotate=rotate,space=space,
		t=t,font=font,face=face,up=up,down=down,right=right,left=left);

	}else{
		// its not square
		writethecube(text,where,size,h=h,rotate=rotate,space=space,
		t=t,font=font,face=face,up=up,down=down,right=right,left=left);
	}
}
// I split the writecube module into 2 pieces.. easier to add features later
module writethecube(text,where,size){
		if (face=="front") {
			translate([where[0]+right-left,where[1]-size[1]/2,where[2]+up-down])
			rotate(90,[1,0,0])
			write(text,center=true,h=h,rotate=rotate,t=t,font=font);
		}
		if (face=="back") {
			translate([where[0]+right-left,where[1]+size[1]/2,where[2]+up-down])
			rotate(90,[1,0,0])   // rotate around the x axis
			rotate(180,[0,1,0])  // rotate around the y axis (z before rotation)
			write(text,center=true,h=h,rotate=rotate,t=t,font=font);
		}
		if (face=="left") {
			translate([where[0]-size[0]/2,where[1]-right+left,where[2]+up-down ])
			rotate(90,[1,0,0])   // rotate around the x axis
			rotate(90,[0,-1,0])  // rotate around the y axis  (z before rotation)
			write(text,center=true,h=h,rotate=rotate,t=t,font=font);
		}
		if (face=="right") {
			translate([where[0]+size[0]/2,where[1]+right-left,where[2] +up-down])
			rotate(90,[1,0,0])   // rotate around the x axis
			rotate(90,[0,1,0])  // rotate around the y axis  (z before rotation)
			write(text,center=true,h=h,rotate=rotate,t=t,font=font);
		}
		if (face=="top") {
			translate([where[0]+right-left,where[1]+up-down,where[2]+size[2]/2 ])
			write(text,center=true,h=h,rotate=rotate,t=t,font=font);
		}
		if (face=="bottom") {
			translate([where[0]+right-left,where[1]-up+down,where[2]-size[2]/2 ])
			rotate(180,[1,0,0])
			write(text,center=true,h=h,rotate=rotate,t=t,font=font);
		}
}

module write(word){
	
	echo (h);
	echo (word);
	echo ("There are " ,len(word) ," letters in this string");
//	echo ("The second letter is ",word[1]);
//	echo (str(word[0],"_"));
rotate(rotate,[0,0,-1]){
	for (r = [0:len(word)]){   // count off each character
		// if the letter is lower case, add an underscore to the end for file lookup
		if ((word[r] == "a" ) || (word[r]== "b")  || (word[r]== "c") 
	 	  || (word[r]== "d") || (word[r]== "e") || (word[r]== "f") 
	 	  || (word[r]== "g") || (word[r]== "h")  || (word[r]== "i") 
       	  	  || (word[r]== "j") || (word[r]== "k") || (word[r]== "l")
       	 	  || (word[r]== "m") || (word[r]== "n") || (word[r]== "o") 
       	 	  || (word[r]== "p") || (word[r]== "q") || (word[r]== "r") 
	 	  || (word[r]== "s") || (word[r]== "t") || (word[r]== "u") 
       	 	  || (word[r]== "v") || (word[r]== "w") || (word[r]== "x") 
       	 	  || (word[r]== "y" )|| (word[r]== "z")){
			if (center == true)  {
				translate([0,-h/2,0]){
					scale([.125*h,.125*h,t]){	
						translate([ (-len(word)*5.5*space/2) + (r*5.5*space),0,0])
						linear_extrude(height=1,convexity=10,center=true){
							import(file = str(fontPath,font) ,layer=str(word[r],"_"));
						}
					}
				}
			}else{
				translate([0,0,t/2]){
					scale([.125*h,.125*h,t]){	
						translate([r*5.5*space,0,0])
						linear_extrude(height=1,convexity=10,center=true){
							import(file = str(fontPath,font) ,layer=str(word[r],"_"));
						}
					}
				}
			}

		}else{
			if (center == true)  {
				translate([0,-h/2,0]){
					scale([.125*h,.125*h,t]){
						translate([ (-len(word)*5.5*space/2) + (r*5.5*space),0,0])
						linear_extrude(height=1,convexity=10,center=true){
							import(file = str(fontPath,font) ,layer=str(word[r]));
						}
					}
				}
			}else{
				translate([0,0,t/2]){
					scale([.125*h,.125*h,t]){
						translate([r*5.5*space,0,0])
						linear_extrude(height=1,convexity=10,center=true){
							import(file = str(fontPath,font) ,layer=str(word[r]));
						}
					}
				}
			}
		}
	}
}
}

/*writecylinder test
translate([0,0,0])
%cylinder(r=20,h=40,center=true);
color([1,0,0])
writecylinder("rotate=90",[0,0,0],20,40,center=true,down=0,rotate=90);
writecylinder("rotate = 30,east = 90",[0,0,0],20,40,center=true,down=0,rotate=30,east=90);
writecylinder("ccw = true",[0,0,0],20,40,center=true,down=0,face="top",ccw=true);
writecylinder("middle = 8",[0,0,0],20,40,h=3,center=true,down=0,face="top",middle=8);
writecylinder("face = top",[0,0,0],20,40,center=true,down=0,face="top");
writecylinder("east=90",[0,0,0],20,40,h=3,center=true,down=0,face="top",east=90);
writecylinder("west=90",[0,0,0],20,40,h=3,center=true,down=0,face="top",ccw=true,west=90);
writecylinder("face = bottom",[0,0,0],20,40,center=true,down=0,face="bottom"); 
*/
/*writesphere test
sphere(20);
color([1,0,0])
writesphere("Hello World",[0,0,0],20,t=1,h=6);
*/
/* writecube test
translate([30,30,30])
cube([10,15,30],center=true);
write("hello",center=true,rotate =30);
color([1,0,0])
writecube( "front",[30,30,30],[10,15,30],h=5,rotate=-90);
color([0,1,0])
writecube( "back",[30,30,30],size=[10,15,30],h=5,face="back",rotate=90,t=4);
color([0,0,1])
writecube( "left",[30,30,30],[10,15,30],h=5,face="left",up=5);
color([1,1,0])
writecube( "right",where=[30,30,30],size=[10,15,30],h=5,face="right",rotate=55);
color([1,0,1])
writecube( "top",where=[30,30,30],size=[10,15,30],h=5,face="top");
color([1,1,1])
writecube( "bttm",where=[30,30,30],size=[10,15,30],h=5,face="bottom",rotate=90);
*/

