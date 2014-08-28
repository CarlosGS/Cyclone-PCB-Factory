// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

include <MCAD/nuts_and_bolts.scad>


workbed_separation_from_Y_threaded_rod = axes_Y_smoothThreaded_verticalSeparation+workbed_separation_from_Y_smooth_rod+axes_Ysmooth_rodD/2;

PCBholder_height = 10;

module Cyclone_YsubPart_nutHolder() {
	footThickness = 10;
	screwSeparation = 10;
	rod_nut_len = 0.8*axes_Ythreaded_rodD;
	dimX = axes_Ythreaded_rodD*2+6;
	dimY = screwSeparation+22;
	dimZ = workbed_separation_from_Y_threaded_rod;
	holderExtension = 10;
	rodTolerance = 0.5;
	rodSize = 8; // M3, M4, etc (integers only)
	washer_D = 15.8;
	washer_thickness = 1.6;
	
	difference() {
		// Main shape
		translate([0,0,dimZ/2-holderExtension/2])
			bcube([dimX,dimY,dimZ+holderExtension],cr=2,cres=10);
		// Hole for the rod
		hull() {
			standard_rod(diam=axes_Ythreaded_rodD+rodTolerance, length=dimY*4, threaded=true, renderPart=true, center=true);
			translate([0,0,-holderExtension*2])
				standard_rod(diam=axes_Ythreaded_rodD+rodTolerance, length=dimY*4, threaded=true, renderPart=true, center=true);
		}
		// Hole for the main nut
		translate([0,dimY/2+0.01+rod_nut_len/2,0])
			hull() {
				rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=0,tolerance=0.1);
				translate([0,0,-holderExtension*2])
					rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=0,captiveLen=0,tolerance=0.1);
			}
		translate([0,dimY/2+0.01-rod_nut_len/2-3,0]) {
			// Hole for the sliding nut
			hull() {
				rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=dimY,captiveLen=0,tolerance=0.3);
				translate([0,0,-holderExtension*2])
					rotate([0,90,0]) hole_for_nut(size=rodSize,nutAddedLen=dimY,captiveLen=0,tolerance=0.3);
			}
			// Hole for the washer
			hull() {
				washer_single(diam=washer_D, thickness=washer_thickness, renderPart=true, tolerance=0.3);
				translate([0,0,-holderExtension*2])
					washer_single(diam=washer_D, thickness=washer_thickness, renderPart=true, tolerance=0.3);
			}
		}
		// Holes for the supporting screws
		translate([0,-screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness])
			rotate([90,0,0])
				hole_for_screw(size=3,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0);
		translate([0,+screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness])
			rotate([90,0,0])
				hole_for_screw(size=3,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0);
	}
	translate([0,dimY/2+rod_nut_len/2,0])
		rotate([0,90,0]) rotate([90,0,0]) nut(size=8, echoPart=true);
	translate([0,-dimY/2,0])
		rotate([0,90,0]) rotate([-90,0,0]) nut(size=8, echoPart=true);
	translate([0,dimY/2+0.01-rod_nut_len/2-3,0])
		washer_single(diam=washer_D, thickness=washer_thickness, echoPart=true);
}


use <libs/linear_bearing.scad>
module Cyclone_YsubPart_singleLinearBearingHolder(onlyScrews=false) {
	linearBearingModel = "LM8UU";
	linearBearingLength = linearBearing_L(linearBearingModel);
	linearBearingDiameter = linearBearing_D(linearBearingModel);
	
	plasticHolderLength = 3;
	
	dimX = linearBearingDiameter+linearBearingDiameter/2;
	dimY = linearBearingLength+2*plasticHolderLength;
	dimZ = workbed_separation_from_Y_smooth_rod+axes_Ysmooth_rodD/2;
	
	holderExtension = linearBearingDiameter/3;
	
	screwSize = 3; // M3, M4, etc (integers only)
	
	footSeparation = screwSize*2;
	footThickness = 7;
	
	workbed_screws_aditional_length = PCBholder_height;
	
	linearBearing_pressureFitTolerance = 0.5;
	
	if(onlyScrews) {
		// Hole for the screw and nut
		translate([dimX/2+footSeparation,0,dimZ+workbed_thickness+workbed_screws_aditional_length])
			rotate([90,0,0]) hole_for_screw(size=screwSize,length=workbed_screws_aditional_length+footThickness+workbed_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0);
	} else {
		difference() {
			// Main part
			union() {
				translate([0,0,dimZ/2])
					bcube([dimX,dimY,dimZ], cr=3, cres=0);
				translate([0,0,dimZ])
					hull() {
						translate([screwSize/2,0,-footThickness/2])
							bcube([dimX+screwSize,dimY,footThickness], cr=3, cres=0);
						translate([dimX/2+footSeparation,0,-footThickness/2])
							cylinder(r=screwSize+3,h=footThickness,center=true);
					}
				translate([0,0,-holderExtension/2])
					bcube([dimX,dimY,holderExtension], cr=3, cres=0);
			}
			// Hole for linear bearing
			linearBearingHole(model=linearBearingModel, lateralExtension=holderExtension, lengthExtension=2*plasticHolderLength, holderLength=plasticHolderLength/2);
			//linearBearingHole(model=linearBearingModel);
			// Hole for the screw and nut
			translate([dimX/2+footSeparation,0,dimZ+workbed_thickness+workbed_screws_aditional_length])
				rotate([90,0,0]) hole_for_screw(size=screwSize,length=workbed_screws_aditional_length+footThickness+workbed_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0);
		}

		translate([0,linearBearingLength/2,0])
			rotate([90,0,0]) linearBearing_single(model=linearBearingModel, echoPart=true);
	}
}

module Cyclone_YsubPart_linearBearingHolders(onlyScrews=false) {
	translate([axes_Ysmooth_separation/2,Ycarriage_linearBearingSeparation/2])
		Cyclone_YsubPart_singleLinearBearingHolder(onlyScrews=onlyScrews);
	translate([axes_Ysmooth_separation/2,-Ycarriage_linearBearingSeparation/2])
		Cyclone_YsubPart_singleLinearBearingHolder(onlyScrews=onlyScrews);
	scale([-1,1,1]) translate([axes_Ysmooth_separation/2,Ycarriage_linearBearingSeparation/2])
		Cyclone_YsubPart_singleLinearBearingHolder(onlyScrews=onlyScrews);
	scale([-1,1,1]) translate([axes_Ysmooth_separation/2,-Ycarriage_linearBearingSeparation/2])
		Cyclone_YsubPart_singleLinearBearingHolder(onlyScrews=onlyScrews);
}




module Cyclone_YsubPart_PCBholder() {
	PCB_dimX = 160;
	PCB_dimY = 100;
	PCB_dimZ = 1.6;
	
	PCB_holder_edge_length = 3;
	PCB_holder_tolerance = 1;
	
	screwSeparation = 2.5;
	
	holderArmLength = 30;
	
	difference() {
		translate([0,0,PCBholder_height/2])
			bcube([workbed_size_X,workbed_size_Y,PCBholder_height], cr=25, cres=0);
		translate([0,0,PCBholder_height/2])
			cube([PCB_dimX-PCB_holder_edge_length*2,PCB_dimY-PCB_holder_edge_length*2,PCBholder_height+1], center=true);
		translate([0,0,PCBholder_height])
			color("green") cube([PCB_dimX+PCB_holder_tolerance*2,PCB_dimY+PCB_holder_tolerance*2,PCB_dimZ], center=true);
		
		translate([-PCB_dimX/2+PCB_holder_edge_length,0,-0.5])
			cube([PCB_dimX-holderArmLength-PCB_holder_edge_length,workbed_size_Y,PCBholder_height+1]);
		scale([-1,-1,1]) translate([-PCB_dimX/2+PCB_holder_edge_length,0,-0.5])
			cube([PCB_dimX-holderArmLength-PCB_holder_edge_length,workbed_size_Y,PCBholder_height+1]);
		
		for (x = [-1,1], y=[-1,0,1]) {
			translate([x*(PCB_dimX/2+screwSeparation),y*PCB_dimY/4,PCBholder_height+2.9])
				rotate([0,0,x*-90]) rotate([90,0,0]) hole_for_screw(size=3,length=PCBholder_height+3,nutDepth=4.5,nutAddedLen=0,captiveLen=10, rot=90);
		}
		
		translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+2.9])
			rotate([90,0,0]) hole_for_screw(size=3,length=PCBholder_height+3,nutDepth=4.5,nutAddedLen=0,captiveLen=10, rot=90);
		scale([-1,-1,1]) translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+2.9])
			rotate([90,0,0]) hole_for_screw(size=3,length=PCBholder_height+3,nutDepth=4.5,nutAddedLen=0,captiveLen=10, rot=90);

	}
}



module Cyclone_Y_carriage() {
	if(render_DXF_workbed) {
		offset(delta = DXF_offset) projection(cut = true)
			translate([0,0,-workbed_separation_from_Y_threaded_rod]) {
				Cyclone_YsubPart_nutHolder();
				translate([0,0,axes_Y_smoothThreaded_verticalSeparation])
					Cyclone_YsubPart_linearBearingHolders();
				color([0.9,0.8,0.8,0.5]) translate([0,0,workbed_separation_from_Y_threaded_rod+workbed_thickness])
					beveledBase(size=[workbed_size_X,workbed_size_Y,workbed_thickness], radius=3, res=15, echoPart=true, renderPart=render_bases_outline);
			}
	} else {
		if(draw_references) color("red") %frame(20);
		rotate([0,0,180]) Cyclone_YsubPart_nutHolder();
		translate([0,0,axes_Y_smoothThreaded_verticalSeparation]) {
			Cyclone_YsubPart_linearBearingHolders();
			difference() {
				translate([0,0,workbed_separation_from_Y_threaded_rod+workbed_thickness-axes_Y_smoothThreaded_verticalSeparation])
					Cyclone_YsubPart_PCBholder();
				Cyclone_YsubPart_linearBearingHolders(onlyScrews=true);
			}
		}
		color([0.9,0.8,0.8,0.5]) translate([0,0,workbed_separation_from_Y_threaded_rod+workbed_thickness])
			beveledBase(size=[workbed_size_X,workbed_size_Y,workbed_thickness], radius=3, res=15, echoPart=true);
	}
}

