// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

include <libs/MCAD/nuts_and_bolts.scad>


workbed_separation_from_Y_threaded_rod = axes_Y_smoothThreaded_verticalSeparation+workbed_separation_from_Y_smooth_rod+axes_Ysmooth_rodD/2;

module Cyclone_YsubPart_nutHolder() {
	footThickness = 10;
	screwSeparation = 10;
	rod_nut_len = 0.8*axes_Ythreaded_rodD;
	dimX = axes_Ythreaded_rodD*2+6;
	dimY = screwSeparation+22;
	dimZ = workbed_separation_from_Y_threaded_rod;
	holderExtension = 10;
	rodNutSize = Y_threaded_rodNutSize;
	washer_D = Y_backlash_washer_D;
	washer_thickness = Y_backlash_washer_thickness;
	screwSize = Y_nutHolder_screwSize;
	
	difference() {
		// Main shape
		translate([0,0,dimZ/2-holderExtension/2])
			color(color_movingPart) bcube([dimX,dimY,dimZ+holderExtension],cr=2,cres=10);
		// Hole for the rod
		hull() {
			standard_rod(diam=axes_Ythreaded_rodD+Y_threaded_rod_Tolerance, length=dimY*4, threaded=true, renderPart=true, center=true);
			translate([0,0,-holderExtension*2])
				standard_rod(diam=axes_Ythreaded_rodD+Y_threaded_rod_Tolerance, length=dimY*4, threaded=true, renderPart=true, center=true);
		}
		// Hole for the main nut
		translate([0,dimY/2+0.01+rod_nut_len/2,0])
			hull() {
				rotate([0,90,0]) hole_for_nut(size=rodNutSize,nutAddedLen=0,captiveLen=0,tolerance=0.1);
				translate([0,0,-holderExtension*2])
					rotate([0,90,0]) hole_for_nut(size=rodNutSize,nutAddedLen=0,captiveLen=0,tolerance=0.1);
			}
		translate([0,dimY/2+0.01-rod_nut_len/2-3,0]) {
			// Hole for the sliding nut
			hull() {
				rotate([0,90,0]) hole_for_nut(size=rodNutSize,nutAddedLen=dimY,captiveLen=0,tolerance=0.3);
				translate([0,0,-holderExtension*2])
					rotate([0,90,0]) hole_for_nut(size=rodNutSize,nutAddedLen=dimY,captiveLen=0,tolerance=0.3);
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
				hole_for_screw(size=screwSize,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0,tolerance=screwHoleTolerance);
		translate([0,+screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness])
			rotate([90,0,0])
				hole_for_screw(size=screwSize,length=workbed_thickness+footThickness,nutDepth=-dimZ,nutAddedLen=dimZ,captiveLen=0,tolerance=screwHoleTolerance);
	}
	translate([0,dimY/2+rod_nut_len/2,0])
		rotate([0,90,0]) rotate([90,0,0]) nut(size=rodNutSize, echoPart=true);
	translate([0,-dimY/2,0])
		rotate([0,90,0]) rotate([-90,0,0]) nut(size=rodNutSize, echoPart=true);
	translate([0,dimY/2+0.01-rod_nut_len/2-3,0])
		washer_single(diam=washer_D, thickness=washer_thickness, echoPart=true);
	translate([0,-screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness+screwSize])
		rotate([90,0,0]) screw_and_nut(size=screwSize,length=workbed_thickness+footThickness+screwSize,nutDepth=0,nutAddedLen=0,captiveLen=0,echoPart=true);
	translate([0,+screwSeparation/2,workbed_separation_from_Y_threaded_rod+workbed_thickness+screwSize])
		rotate([90,0,0]) screw_and_nut(size=screwSize,length=workbed_thickness+footThickness+screwSize,nutDepth=0,nutAddedLen=0,captiveLen=0,echoPart=true);
}

use <libs/linear_bearing.scad>
module Cyclone_YsubPart_singleLinearBearingHolder(onlyScrews=false) {
	linearBearingLength = linearBearing_L(Y_linearBearingModel);
	linearBearingDiameter = linearBearing_D(Y_linearBearingModel);
	
	plasticHolderLength = 3;
	
	dimX = linearBearingDiameter+linearBearingDiameter/2;
	dimY = linearBearingLength+2*plasticHolderLength;
	dimZ = workbed_separation_from_Y_smooth_rod+axes_Ysmooth_rodD/2;
	
	holderExtension = linearBearingDiameter/3;
	
	screwSize = Y_singleLinearBearingHolder_screwSize;
	
	footSeparation = screwSize*2;
	footThickness = 7;
	
	workbed_screws_aditional_length = PCBholder_height;
	
	if(onlyScrews) {
		// Hole for the screw and nut
		translate([dimX/2+footSeparation,0,dimZ+workbed_thickness+workbed_screws_aditional_length])
			rotate([90,0,0]) hole_for_screw(size=screwSize,length=workbed_screws_aditional_length+footThickness+workbed_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance);
		translate([dimX/2+footSeparation,0,dimZ+workbed_thickness+workbed_screws_aditional_length])
			rotate([90,0,0]) screw_and_nut(size=screwSize,length=workbed_screws_aditional_length+footThickness+workbed_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,echoPart=true);
	} else {
		difference() {
			// Main part
			color(color_movingPart) union() {
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
			linearBearingHole(model=Y_linearBearingModel, lateralExtension=holderExtension, pressureFitTolerance=LinearBearingPressureFitTolerance, lengthExtension=2*plasticHolderLength, holderLength=plasticHolderLength/2);

			// Hole for the screw and nut
			translate([dimX/2+footSeparation,0,dimZ+workbed_thickness+workbed_screws_aditional_length])
				rotate([90,0,0]) hole_for_screw(size=screwSize,length=workbed_screws_aditional_length+footThickness+workbed_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance);
		}

		translate([0,linearBearingLength/2,0])
			rotate([90,0,0]) linearBearing_single(model=Y_linearBearingModel, echoPart=true);
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
	holderArmLength = 30;
	
	holderL_thickness = 2;
	holderL_thickness_btm = 1;
	holderL_width = workbed_size_Y-PCB_dimY-PCB_holder_tolerance*2;
	holderL_innerWidth = holderL_width/2;

	screwSize = Y_PCBholder_screwSize;
	screwSeparation = screwSize*0.84;
	
	// Draw the PCB (transparent)
	%translate([0,0,PCBholder_height])
		color([0.2,0.6,0, 1]) cube([PCB_dimX+PCB_holder_tolerance*2,PCB_dimY+PCB_holder_tolerance*2,PCB_dimZ], center=true);
	%translate([0,0,PCBholder_height+PCB_dimZ/2])
		color([0.8,0.5,0, 1]) cube([PCB_dimX+PCB_holder_tolerance*2,PCB_dimY+PCB_holder_tolerance*2,PCB_dimZ/10], center=true);
	
	if(Render_PCBholderBottom) {
		difference() {
			color(color_stillPart) translate([0,0,PCBholder_height/2])
				bcube([workbed_size_X,workbed_size_Y,PCBholder_height], cr=25, cres=0);
			
			// Hole for the PCB
			translate([0,0,PCBholder_height])
				cube([PCB_dimX+PCB_holder_tolerance*2,PCB_dimY+PCB_holder_tolerance*2,PCB_dimZ], center=true);
			
			// Holes to split the part in two pieces
			translate([0,0,PCBholder_height/2])
				cube([PCB_dimX-PCB_holder_edge_length*2,PCB_dimY-PCB_holder_edge_length*2, 2*PCBholder_height+1], center=true);
			translate([-PCB_dimX/2+PCB_holder_edge_length,0,-0.5])
				cube([PCB_dimX-holderArmLength-PCB_holder_edge_length,workbed_size_Y, 2*PCBholder_height+1]);
			scale([-1,-1,1]) translate([-PCB_dimX/2+PCB_holder_edge_length,0,-0.5])
				cube([PCB_dimX-holderArmLength-PCB_holder_edge_length,workbed_size_Y, 2*PCBholder_height+1]);
			
			// Holes for the screws
			for (x = [-1,1], y=[-1,0,1]) {
				translate([x*(PCB_dimX/2+screwSeparation),y*PCB_dimY/4,PCBholder_height+screwSize])
					rotate([0,0,x*-90]) rotate([90,0,0]) hole_for_screw(size=screwSize,length=PCBholder_height+3,nutDepth=4.5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
			}
			translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+screwSize])
				rotate([90,0,0]) hole_for_screw(size=screwSize,length=PCBholder_height+3,nutDepth=4.5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
			scale([-1,-1,1]) translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+screwSize])
				rotate([90,0,0]) hole_for_screw(size=screwSize,length=PCBholder_height+3,nutDepth=4.5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);

		}
	}
	
	// Holder top L supports
	if(Render_PCBholderTop) {
		translate([0,0,0.5])
		difference() {
			color(color_movingPart) translate([0,0,PCBholder_height+(holderL_thickness+holderL_thickness_btm)/2])
				bcube([PCB_dimX+PCB_holder_tolerance*2+holderL_width, PCB_dimY+PCB_holder_tolerance*2+holderL_width, holderL_thickness+holderL_thickness_btm], cr=8, cres=0);
			translate([0,0,PCBholder_height+holderL_thickness_btm/2])
				bcube([PCB_dimX+PCB_holder_tolerance*2+holderL_innerWidth, PCB_dimY+PCB_holder_tolerance*2+holderL_innerWidth, holderL_thickness_btm], cr=8, cres=0);
			
			if(draw_references) %frame();
			
			translate([0,0,PCBholder_height/2])
				cube([PCB_dimX-PCB_holder_edge_length*2,PCB_dimY-PCB_holder_edge_length*2, 2*PCBholder_height+1], center=true);
			translate([-PCB_dimX/2+PCB_holder_edge_length,0,-0.5])
				cube([PCB_dimX-holderArmLength-PCB_holder_edge_length,workbed_size_Y, 2*PCBholder_height+1]);
			scale([-1,-1,1]) translate([-PCB_dimX/2+PCB_holder_edge_length,0,-0.5])
				cube([PCB_dimX-holderArmLength-PCB_holder_edge_length,workbed_size_Y, 2*PCBholder_height+1]);
			
			// Holes for the screws
			translate([0,0,holderL_thickness+(holderL_thickness+holderL_thickness_btm)/2]) {
				for (x = [-1,1], y=[-1,0,1]) {
					translate([x*(PCB_dimX/2+screwSeparation),y*PCB_dimY/4,PCBholder_height+screwSize])
						rotate([0,0,x*-90]) rotate([90,0,0]) hole_for_screw(size=screwSize,length=PCBholder_height*10,nutDepth=4.5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
				}
			
				translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+screwSize])
					rotate([90,0,0]) hole_for_screw(size=screwSize,length=PCBholder_height*10,nutDepth=4.5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
				scale([-1,-1,1]) translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+screwSize])
					rotate([90,0,0]) hole_for_screw(size=screwSize,length=PCBholder_height*10,nutDepth=4.5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
			}
		}
	}
	
	// Add the screws and nuts
	translate([0,0,holderL_thickness+(holderL_thickness+holderL_thickness_btm)/2]) {
		for (x = [-1,1], y=[-1,0,1]) {
			translate([x*(PCB_dimX/2+screwSeparation),y*PCB_dimY/4,PCBholder_height+screwSize])
				rotate([0,0,x*-90]) rotate([90,0,90]) screw_and_nut(size=screwSize,length=PCBholder_height+screwSize,nutDepth=4.5-screwSize,nutAddedLen=0,captiveLen=0,echoPart=true);
		}
		translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+screwSize])
			rotate([90,0,90]) screw_and_nut(size=screwSize,length=PCBholder_height+screwSize,nutDepth=4.5-screwSize,nutAddedLen=0,captiveLen=0,echoPart=true);
		scale([-1,-1,1]) translate([PCB_dimX/2-holderArmLength/2,PCB_dimY/2+screwSeparation,PCBholder_height+screwSize])
			rotate([90,0,90]) screw_and_nut(size=screwSize,length=PCBholder_height+screwSize,nutDepth=4.5-screwSize,nutAddedLen=0,captiveLen=0,echoPart=true);
	}
}

module Cyclone_Y_carriage() {
	if(render_DXF_workbed) {
		offset(delta = DXF_offset) projection(cut = true)
			translate([0,0,-workbed_separation_from_Y_threaded_rod]) {
				Cyclone_YsubPart_nutHolder();
				translate([0,0,axes_Y_smoothThreaded_verticalSeparation])
					Cyclone_YsubPart_linearBearingHolders();
				translate([0,0,workbed_separation_from_Y_threaded_rod+workbed_thickness])
					beveledBase(size=[workbed_size_X,workbed_size_Y,workbed_thickness], radius=3, res=15, echoPart=true, renderPart=render_bases_outline);
			}
	} else {
		if(draw_references) color("red") %frame(20);
		if(Render_YsubPart_nutHolder){
			rotate([0,0,180])
				Cyclone_YsubPart_nutHolder();
		}
		translate([0,0,axes_Y_smoothThreaded_verticalSeparation]) {
			if(Render_YsubPart_linearBearingHolders)
				Cyclone_YsubPart_linearBearingHolders();
			if(Render_PCBholderTop || Render_PCBholderBottom) {
				difference() {
					translate([0,0,workbed_separation_from_Y_threaded_rod+workbed_thickness-axes_Y_smoothThreaded_verticalSeparation])
						Cyclone_YsubPart_PCBholder();
					Cyclone_YsubPart_linearBearingHolders(onlyScrews=true);
				}
			}
		}
		color([0.9,0.9,0.9, 0.5]) translate([0,0,workbed_separation_from_Y_threaded_rod+workbed_thickness])
			beveledBase(size=[workbed_size_X,workbed_size_Y,workbed_thickness], radius=3, res=15, echoPart=true);
	}
}
