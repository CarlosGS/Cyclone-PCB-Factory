use <./Libraries/dev_boards.scad>
use <./Libraries/hex_structure.scad>

fileNameLogo = "./Libraries/cycloneLogoC.dxf";

baseHeight = 1.8;
baseOffset = 1;//actual width

baseSlotW = 2;
baseSlotL = 15;

screwDiameter = 3;
screwHeight = 18;

fanScrewDiameter = 3;
distanceFanScrews = 32;


screwAssembly = 17.9;
screwAssemblyWidth = 5.53;
screwAssemblyHeigth = 2;
/******************************/
cubeH = 45;
arduinoShortSide=53.7;
arduinoLongSide = 67;
arduinoLongSideAddon = 1;

baseLongSide =  arduinoLongSide + arduinoLongSideAddon + screwDiameter*2 +baseSlotW*2;

baseShortSide = arduinoShortSide  + screwDiameter*2 + baseSlotW*2;

module slotsScrewLongSide(){
	mountingScrew();
	translate([arduinoShortSide/2 + screwDiameter/2,0,0])
		slot(baseLongSide);
}
module slotsScrewShortSide(){
	rotate([0,0,90])
	translate([arduinoLongSide/2 + screwDiameter/2,0,0])
		slot(baseLongSide);
}
module slotsScrewShortSideBack(){
	slotsScrewShortSide();
	mirror([1,0,0])
 		slotsScrewShortSide();
}
module slotsScrewShortSideFront(){
		rotate([0,0,90])
			translate([(-baseLongSide + screwDiameter)/2,-baseSlotL*1.5,0])
		 		slot(baseLongSide);

}
module slotsScrewLongSideR(){
	slotsScrewLongSide();
	mirror([0,1,0])
 		slotsScrewLongSide();
}
module slotsScrewLongSideL(){
	mirror([1,0,0])
		slotsScrewLongSideR();
}

module bottom(top = 0){
	difference(){
		body();
		if(top){}
			else{
				arduino_uno_mounting();
				slotsScrewShortSideFront();
			}
		//arduino_uno();
		slotsScrewLongSideL();
		slotsScrewLongSideR();
		//slotsScrewShortSideBack();
		
	}
}
module top(){
	difference(){
		translate([0,0,cubeH])
		bottom(1);
		translate([0,0,cubeH]){
		fanDrills();
		cylinder(r=sqrt(2*(distanceFanScrews*distanceFanScrews))/2 - fanScrewDiameter, h= baseSlotW);}
	}
}

module body(){
	translate([-baseShortSide/2,-(baseLongSide)/2,0]){
		cube([baseShortSide, baseLongSide, baseHeight]);
	}
}
module mountingScrew(hh = screwHeight){
	translate([(arduinoShortSide+ screwDiameter+ baseSlotW)/2,0,0])
		cylinder(r = screwDiameter/2, h = hh , center=true, $fn = 96);
}
module slot(pos = 0, frac = 8){
	translate([0,pos/frac,0])
		cube([baseSlotW,baseSlotL,baseHeight]);
}

module sideHalf(){
		difference(){
			translate([baseShortSide/2-3.5,-(baseLongSide)/2,0])
				cube([baseSlotW,baseLongSide,(cubeH + baseHeight)/2]);
			mountingScrew(screwAssembly*2);
			translate([baseShortSide/2 - 3.5,-screwAssemblyWidth/2,baseHeight+2])
				cube([baseSlotW,screwAssemblyWidth,screwAssemblyHeigth]);
	}
}
module side(){
	sideHalf();
	translate([0,0,cubeH +baseHeight])
		mirror([0,0,-1])
 			sideHalf();
	
}
module frontHalf(){
	difference(){
		translate([0,-(baseLongSide)/2 +1.5,0])
			cube([(baseShortSide -7)/2 , baseSlotW, cubeH +baseHeight]);
		
	}
	translate([baseShortSide/2 - screwDiameter/2 -baseSlotW,-baseLongSide/2 + screwDiameter/2,cubeH/4])							
		cube([baseSlotW,baseSlotW,(cubeH +screwDiameter/2)/2]);
	
}
module front(back = 0){
	difference(){
		difference(){
			union(){
				frontHalf();
				mirror([1,0,0])
					frontHalf();
			}		
			top();
			bottom();
		}
		if (back){
			translate([-baseShortSide/2,-baseLongSide/2 +screwDiameter/2,0])
				cube([baseShortSide,baseSlotW,baseSlotW]);
			translate([-arduinoShortSide/3,-baseLongSide/2 ,cubeH*0.9])
				rotate([90,180,180])
					resize([32,32,4])
						linear_extrude(file = fileNameLogo, height=2);
	
		}
			else{
				translate([0,0,4.4])
					arduino_uno();
				translate([16,-baseLongSide/2 +4,42])
					rotate([90,180,0])
						resize([23,23,3])
							linear_extrude(file = fileNameLogo, height=2);
		}	
	}
}
module back(){
	mirror([0,1,0])
		front(1);
}

module sideLeft(){
	
		mirror([1,0,0])
	 		side(); 	

}
module Right(){
	difference(){
		side();
		
		bottom();
		top();
		front();
		back();
	}
}
module Left(){
	mirror([1,0,0])
	Right();
}
module hexframe(){
	union(){
		frame();		
		translate([0,1.5,38.5])
			rotate([0,90,0])
				linear_extrude(height=baseSlotW){	
					lattice(6,6,4.5);//lattice(3,3,9);
			}
		}
	}
module frame(){
	difference(){	
			cube([baseSlotW,baseLongSide/2,cubeH]);
			translate([0,1.5,1.5])
				cube([baseSlotW,baseLongSide/2 -3,cubeH-3]);
	}
}
module outerFrame(){
		difference(){	
			translate([0,0,0])
				cube([baseSlotW+4,baseLongSide/2+90,cubeH+90],center=true);
			translate([0,0,0])
				cube([baseSlotW+4, baseLongSide/2  , cubeH]);
			
		}

}
module hexInt(){
	difference(){
		hexframe();
		outerFrame();

	}
}

//hexInt();
module RightaddHex(){
	difference(){
		Right();
		translate([baseShortSide/2-3.5,5,5])
			cube([baseSlotW,baseLongSide/2 -10,cubeH-23]);
		translate([baseShortSide/2 -3.5,-baseLongSide/2+5,5])
			cube([baseSlotW,baseLongSide/2 -10,cubeH-23]);
		}

	translate([baseShortSide/2 -3.5,5,5])
		resize([baseSlotW,baseLongSide/2 -10,cubeH-10])
			hexInt();
	
	translate([baseShortSide/2 -3.5,-baseLongSide/2+5,5])
		resize([baseSlotW,baseLongSide/2 -10,cubeH-10])
			hexInt();	
}
module LeftaddHex(){
	mirror([1,0,0])
	RightaddHex();
}
module fanDrills(){
	i = 0;
	j = 0;
	di = distanceFanScrews;
	dj = distanceFanScrews;
	nj=2;
	ni = 2;
	for (i = [0:ni-1], j = [0:nj -1]){
		translate([-distanceFanScrews/2 +i*di, -distanceFanScrews/2+j*dj, 0])
			cylinder(r=fanScrewDiameter/2, h = 30,center=true, $fn=96);
	}
}
/******Animation*******/
// animation = 70;
// bottom();
// translate([0,0,$t*animation])
// top();
// translate([0,$t*animation,0])
// back();
// translate([0,$t*-animation,0])
// front();
// translate([$t*animation,0,0])
// RightaddHex();
// translate([$t*-animation,0,0])
// LeftaddHex();
// translate([0,0,2.4])
// arduino_uno();

/******All Parts*******/
// front();
// back();
// bottom();
// top();
// RightaddHex();
// LeftaddHex();




