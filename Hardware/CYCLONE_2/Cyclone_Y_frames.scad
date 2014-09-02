// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

module mirrorOrNot(mirrorPart=false, axes=[-1,1,1]) {
	if(mirrorPart) scale(axes) children();
	else children();
}



use <MCAD/bearing.scad>



Ymotor_sideLen = 42.20;

axes_YgearSeparation = 37;
axes_YgearRatio = 21/21; // Number of tooth (motor/rod)


module Cyclone_Y_frontFrame() {
	*color("red")
		translate([-10,0,-axes_Y_threaded_height])
			cube([20,10,axes_Y_threaded_height+5]);
	
	screwSize = 3; // M3, M4, etc (integers only)
	
	motorWallSeparation = 5;
	motorRotatedOffset = 5;
	gearWallSeparation = 5;
	
	motor_YgearSeparation_projected = axes_YgearSeparation*cos(-motorRotatedOffset);
	
	rod_nut_len = 0.8*axes_Ythreaded_rodD;
	gear_thickness = 5;
	bearing_width = bearingWidth(608);
	bearing_diam = bearingOuterDiameter(608);
	bearingDepth = 3;
	partThickness = 5+screwSize*2;
	
	dimX = bearing_diam+partThickness;
	dimY = partThickness;
	dimZ = axes_Y_threaded_height;
	
	footSeparation = screwSize*2;
	foot_additional_separation = 5;
	footThickness = 10;
	
	translate([0,2*rod_nut_len+gear_thickness,0]) {
		translate([0,bearing_width-bearingDepth,0]) {
			if(draw_references) color("blue") %frame(20);
			difference() {
				// Main block
				union() {
					hull() {
						rotate([-90,0,0])
							cylinder(r=dimX/2,h=dimY);
						translate([-dimX/2,0,-dimZ])
							cube([dimX,dimY,dimZ]);
						translate([-20,0,0]) {
							rotate([-90,0,0])
								cylinder(r=dimX/2,h=dimY);
							translate([-dimX/2,0,-dimZ])
								cube([dimX/2,dimY,dimZ]);
						}
					}
					translate([0,dimY/2,-dimZ]) {
						hull() {
							translate([0,0,0])
								cylinder(r=dimY/2,h=footThickness);
							translate([-footSeparation-foot_additional_separation-motor_YgearSeparation_projected-Ymotor_sideLen/2,0,0])
								cylinder(r=dimY/2,h=footThickness);
						}
						translate([-motor_YgearSeparation_projected-Ymotor_sideLen/2-2,-dimY/2,1])
							cube([dimX,dimY,dimZ/2]);
					}
					translate([0,dimY/2,-dimZ])
						hull() {
							cylinder(r=dimY/2,h=footThickness);
							translate([footSeparation+dimX/2,0,0])
								cylinder(r=dimY/2,h=footThickness);
							translate([dimX/3,dimY/2+footSeparation+foot_additional_separation,0])
								cylinder(r=dimY/2,h=footThickness);
						}
				}
				translate([0,-0.01,0])
					rotate([-90,0,0])
						bearingHole(depth=bearingDepth, thickness=partThickness);
				translate([0,dimY/2,-dimZ+footThickness]) {
					translate([footSeparation+dimX/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
					translate([dimX/3,dimY/2+footSeparation+foot_additional_separation,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
					translate([-footSeparation-foot_additional_separation-motor_YgearSeparation_projected-Ymotor_sideLen/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
				}
				// Translate to motor axis position
				rotate([0,-motorRotatedOffset,0]) {
					translate([-axes_XgearSeparation,0,0])
						rotate([0,motorRotatedOffset,0]) {
							translate([0,motorWallSeparation-0.01,0])
							rotate([0,0,90]) rotate([0,-90,0]) stepperMotor_mount(motorWallSeparation, sideLen=Ymotor_sideLen, slideOut=false);
						}
				}
			}
		
			// Draw vitamins (nuts, bolts, bearings)
			translate([0,dimY/2,-dimZ+footThickness]) {
				translate([footSeparation+dimX/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true, autoNutOffset=true, echoPart=true);
				translate([dimX/3,dimY/2+footSeparation+foot_additional_separation,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true, autoNutOffset=true, echoPart=true);
				translate([-footSeparation-foot_additional_separation-motor_YgearSeparation_projected-Ymotor_sideLen/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true, autoNutOffset=true, echoPart=true);
			}
			// Translate to motor position
			rotate([0,-motorRotatedOffset,0]) {
				translate([-axes_XgearSeparation,0,0])
					rotate([0,motorRotatedOffset,0]) {
						translate([0,motorWallSeparation,0])
							rotate([90,0,0])
								stepperMotor(screwHeight=motorWallSeparation, echoPart=true);
						translate([0,-rod_nut_len-gear_thickness-bearing_width+bearingDepth,0])
							rotate([-90,0,0]) motorGear(r=axes_XgearSeparation/(1+axes_XgearRatio), echoPart=true);
					}
			}
		}
		rotate([-90,0,0])
			radialBearing(echoPart=true);
	}
	translate([0,0.01,0])
		rotate([-90,0,0])
			rotate([0,0,45]) nut(size=axes_Ythreaded_rodD, chamfer=true, echoPart=true);
	translate([0,rod_nut_len+gear_thickness,0])
		rotate([-90,0,0])
			nut(size=axes_Ythreaded_rodD, echoPart=true);
	translate([0,rod_nut_len,0])
		rotate([-90,0,0])
			rodGear(r=axes_YgearSeparation/(1+1/axes_YgearRatio), echoPart=true);
}







module Cyclone_Y_backFrame() {
	
	screwSize = 3; // M3, M4, etc (integers only)
	
	rod_nut_len = 0.8*axes_Ythreaded_rodD;
	bearing_width = bearingWidth(608);
	bearing_diam = bearingOuterDiameter(608);
	bearingDepth = 3;
	partThickness = 5+screwSize*2;
	
	dimX = bearing_diam+partThickness;
	dimY = partThickness;
	dimZ = 0;
	
	footSeparation = screwSize*2;
	foot_additional_separation = 5;
	footThickness = 10;
	
	endstopHolderRotation = 5;
	
	translate([0,-2*rod_nut_len,0]) {
		translate([0,bearingDepth-bearing_width,0]) {
			difference() {
				union() {
					rotate([90,0,0])
						cylinder(r=dimX/2,h=dimY);
					translate([-dimX/2,-dimY,-axes_Y_threaded_height])
						cube([dimX,dimY,axes_Y_threaded_height]);
					translate([0,-dimY/2,-axes_Y_threaded_height])
						hull() {
							translate([-footSeparation-dimX/2,0,0])
								cylinder(r=dimY/2,h=footThickness);
							translate([footSeparation+dimX/2,0,0])
								cylinder(r=dimY/2,h=footThickness);
							translate([0,dimY/2+footSeparation+foot_additional_separation,0])
								cylinder(r=dimY/2,h=footThickness);
						}
					translate([0,-dimY-0.01,dimX/2])
						rotate([0,endstopHolderRotation,0])
							endstop_holder(holes=false);
				}
				
				translate([0,-dimY-0.01,dimX/2])
					rotate([0,endstopHolderRotation,0])
						endstop_holder(holes=true);
				
				translate([0,0.01,0])
					rotate([90,0,0])
						bearingHole(depth=bearingDepth, thickness=partThickness);
				translate([0,-dimY/2,-axes_Y_threaded_height+footThickness]) {
					translate([-footSeparation-dimX/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
					translate([footSeparation+dimX/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
					translate([0,dimY/2+footSeparation+foot_additional_separation,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
				}
			}
		
			// Draw vitamins (nuts, bolts, bearings)
			translate([0,-dimY/2,-axes_Y_threaded_height+footThickness]) {
				translate([-footSeparation-dimX/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true, autoNutOffset=true, echoPart=true);
				translate([footSeparation+dimX/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true, autoNutOffset=true, echoPart=true);
				translate([0,dimY/2+footSeparation+foot_additional_separation,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true, autoNutOffset=true, echoPart=true);
			}
		}
		rotate([90,0,0])
			radialBearing(echoPart=true);
	}
	translate([0,0.01,0])
		rotate([90,0,0])
			rotate([0,0,45]) nut(size=axes_Ythreaded_rodD, chamfer=true, echoPart=true);
	translate([0,-rod_nut_len,0])
		rotate([90,0,0])
			nut(size=axes_Ythreaded_rodD, echoPart=true);
}














module Cyclone_logo(sizemm = 30, thickness = 10, mirrorLogo = false) {
	dxf_logo_size = 50; // Real size of the logo in the DXF file
	scale_factor = sizemm/dxf_logo_size;
	if(mirrorLogo)
		mirror([ 1, 0, 0 ]) linear_extrude(height=thickness) scale(scale_factor) import("dxf/CycloneLogo.dxf", layer="logo");
	else
		linear_extrude(height=thickness) scale(scale_factor) import("dxf/CycloneLogo.dxf", layer="logo");
}

module Cyclone_Y_rightSmoothRodIdler(mirrorLogo = false) {
	holderThickness = 5;
	holderOuterRadius = holderThickness+axes_Ysmooth_rodD/2;
	
	screwSize = 3; // M3, M4, etc (integers only)
	
	dimX = holderOuterRadius*2;
	dimY = 5+screwSize*2;
	dimZ = axes_Yreference_height;
	
	slotHeight = 3;
	screwLength = holderOuterRadius*2;
	
	logoDepth = dimY/4;
	
	
	footSeparation = screwSize*2;
	footThickness = 10;
	
	color("lightcyan") {
		difference() {
			union() {
				translate([0,0,-axes_Yreference_height])
					cube([dimX,dimY,dimZ+holderThickness+axes_Ysmooth_rodD/2]);
				translate([-holderOuterRadius,0,-axes_Yreference_height])
					cube([dimX,dimY,dimZ]);
				rotate([-90,0,0]) cylinder(r=holderOuterRadius, h=dimY);
				translate([0,dimY/2,-axes_Yreference_height])
					hull() {
						translate([-holderOuterRadius-footSeparation,0,0])
							cylinder(r=dimY/2,h=footThickness);
						translate([holderOuterRadius*2+footSeparation,0,0])
							cylinder(r=dimY/2,h=footThickness);
						translate([holderOuterRadius/2,dimY/2+footSeparation,0])
							cylinder(r=dimY/2,h=footThickness);
					}
			}
			standard_rod(diam=axes_Ysmooth_rodD, length=dimY*4, threaded=false, renderPart=true, center=true);
			translate([2.5+holderOuterRadius,dimY/2,holderOuterRadius])
				rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=screwLength+10,nutDepth=10,nutAddedLen=0,captiveLen=10, rot=90);
			translate([dimX/2,dimY/2,0])
				cube([dimX+1,dimY+1,slotHeight],center=true);
			translate([(dimX-holderOuterRadius)/2,-0.1,-(dimZ+axes_Ysmooth_rodD/2)/2])
				scale([1,-1,1])
					rotate([90,0,0])
						Cyclone_logo(sizemm = min(dimX+holderOuterRadius-5,dimZ-axes_Ysmooth_rodD/2-5), thickness = logoDepth, mirrorLogo = mirrorLogo);
			translate([0,dimY/2,-axes_Yreference_height+footThickness]) {
				translate([-holderOuterRadius-footSeparation,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
				translate([holderOuterRadius*2+footSeparation,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
				translate([holderOuterRadius/2,dimY/2+footSeparation,0])
					rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, rot=90, invert=true);
			}
		}
	}
	// Draw nuts and bolts
	translate([2.5+holderOuterRadius,dimY/2,holderOuterRadius])
		rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=screwLength+10,nutDepth=10,nutAddedLen=0,captiveLen=0, rot=90, echoPart=true);
	translate([0,dimY/2,-axes_Yreference_height+footThickness]) {
		translate([-holderOuterRadius-footSeparation,0,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, autoNutOffset=true, rot=90, invert=true, echoPart=true);
		translate([holderOuterRadius*2+footSeparation,0,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, autoNutOffset=true, rot=90, invert=true, echoPart=true);
		translate([holderOuterRadius/2,dimY/2+footSeparation,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0, autoNutOffset=true, rot=90, invert=true, echoPart=true);
	}
}


module Cyclone_Y_leftSmoothRodIdler() {
	scale([-1,1,1]) Cyclone_Y_rightSmoothRodIdler(mirrorLogo = true);
}

