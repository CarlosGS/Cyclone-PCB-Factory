// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

module mirrorOrNot(mirrorPart=false, axes=[-1,1,1]) {
	if(mirrorPart) scale(axes) children();
	else children();
}



use <libs/MCAD/bearing.scad>


Y_motorModel = Nema17;
Ymotor_sideLen = lookup(NemaSideSize, Y_motorModel); //42.20;
axes_YgearRatio = Y_motorGearRatio/Y_rodGearRatio; // Number of tooth (motor/rod)


module Cyclone_Y_frontFrame() {
	screwSize = Y_frontFrame_footScrewSize;
	
	motorWallSeparation = Y_motorWallSeparation;
	motorRotatedOffset = Y_motorRotatedOffset;
	gearWallSeparation = Y_gearWallSeparation;
	
	motor_YgearSeparation_projected = axes_YgearSeparation*cos(-motorRotatedOffset);

	rod_nut_len = METRIC_NUT_THICKNESS[Y_threaded_rodNutSize];
	nut_separation = rod_nut_len/2;
	gear_thickness = Y_gear_thickness;
	bearing_width = bearingWidth(Y_threaded_rodBearingModel);
	bearing_diam = bearingOuterDiameter(Y_threaded_rodBearingModel);
	bearingDepth = Y_threaded_rodBearingDepth;
	partThickness = 5+screwSize*2;
	
	dimX = bearing_diam+partThickness;
	dimY = partThickness;
	dimZ = axes_Y_threaded_height;
	
	footSeparation = screwSize*2;
	foot_additional_separation = Y_foot_additional_separation;
	footThickness = Y_frame_footThickness;
	
	rodNutSize = Y_threaded_rodNutSize;
	
	
	module Cyclone_YsubPart_gearCover() {
		margin = gearCover_margin;
		rodGearAddedMargin = rodGearAddedgearCover_margin;
		effectiveYgearSeparation = axes_YgearSeparation+0.5;
		wallThickness = gearCover_wallThickness;
		screwHeadSpaceHeight = gearCover_screwHeadSpaceHeight;
		screwHeadSpaceDiam = gearCover_screwHeadSpaceDiam;
		coverHeight = gearCoverHeight;
		coverExtraHeight = gearCoverExtraHeight;
		coverExtraRadius = gearCoverExtraRadius;
		nema_screw_separation = lookup(NemaDistanceBetweenMountingHoles, Y_motorModel);
		truncationAngle = gearCover_truncationAngle;
		
		motorGearRadius = axes_YgearSeparation/(1+axes_YgearRatio)+margin;
		rodGearRadius = axes_YgearSeparation/(1+1/axes_YgearRatio)+margin+rodGearAddedMargin;
		
		difference() {
			union() {
				// Cover for the rod gear
				rotate([90,0,0])
					cylinder(r=rodGearRadius+wallThickness, h=coverHeight);
				translate([0,-coverHeight,0])
					rotate([90,0,0])
						cylinder(r1=rodGearRadius+wallThickness, r2=rodGearRadius+wallThickness+coverExtraRadius, h=coverExtraHeight+wallThickness);
				// Translate to motor position
				rotate([0,-motorRotatedOffset,0]) {
					translate([-effectiveYgearSeparation,0,0])
						rotate([0,motorRotatedOffset,0]) {
							// Cover for the motor gear
							rotate([90,0,0]) cylinder(r=motorGearRadius+wallThickness, h=coverHeight);
							translate([0,-coverHeight,0])
								rotate([90,0,0]) cylinder(r1=motorGearRadius+wallThickness, r2=motorGearRadius+wallThickness+coverExtraRadius, h=coverExtraHeight+wallThickness);
							// Cylinder for the support screw
							translate([nema_screw_separation/2,0,-nema_screw_separation/2])
								rotate([90,0,0]) cylinder(r=screwHeadSpaceDiam/2+wallThickness, h=coverHeight);
						}
				}
			}
			translate([0,0.01,0])
				union() {
					// Truncation for avoiding collisions with Y carriage
					translate([-rodGearRadius/2,0,rodGearRadius+0.5])
						rotate([90-truncationAngle,0,0]) cube(rodGearRadius);
					rotate([90,0,0])
						cylinder(r=rodGearRadius, h=coverHeight);
						// Hole for the rod gear
						rotate([90,0,0])
							cylinder(r=rodGearRadius, h=coverHeight);
						translate([0,-coverHeight+0.02,0])
							rotate([90,0,0])
								cylinder(r1=rodGearRadius, r2=rodGearRadius+coverExtraRadius, h=coverExtraHeight);
						rotate([90,0,0])
							cylinder(r=rodGearRadius+coverExtraRadius, h=coverHeight+coverExtraHeight+wallThickness+0.1);
					// Translate to motor position
					rotate([0,-motorRotatedOffset,0]) {
						translate([-effectiveYgearSeparation,0,0])
							rotate([0,motorRotatedOffset,0]) {
								difference() {
									union() {
										// Hole for the motor gear
										rotate([90,0,0]) cylinder(r=motorGearRadius, h=coverHeight);
										translate([0,-coverHeight+0.02,0])
											rotate([90,0,0]) cylinder(r1=motorGearRadius, r2=motorGearRadius+coverExtraRadius, h=coverExtraHeight);
										rotate([90,0,0]) cylinder(r=motorGearRadius+coverExtraRadius, h=coverHeight+coverExtraHeight+wallThickness+0.1);
										// Outer hole for the support screw
										translate([nema_screw_separation/2,0,-nema_screw_separation/2])
											rotate([90,0,0]) cylinder(r=screwHeadSpaceDiam/2, h=coverHeight+coverExtraHeight*2);
									}
									// Support screw holder
									translate([nema_screw_separation/2,0,-nema_screw_separation/2])
										rotate([90,0,0]) cylinder(r=screwHeadSpaceDiam/2+wallThickness, h=wallThickness);
								}
								// Inner hole for the support screw
								translate([nema_screw_separation/2,0,-nema_screw_separation/2])
									rotate([90,0,0]) cylinder(r=(screwSize+1)/2, h=coverHeight+0.1);
								// Holes for the other three screws
								translate([nema_screw_separation/2,0,nema_screw_separation/2])
									rotate([90,0,0]) cylinder(r=screwHeadSpaceDiam/2, h=screwHeadSpaceHeight/2);
								translate([nema_screw_separation/2,-screwHeadSpaceHeight/2,nema_screw_separation/2])
									rotate([90,0,0]) sphere(r=screwHeadSpaceDiam/2);
								
								translate([-nema_screw_separation/2,0,-nema_screw_separation/2])
									rotate([90,0,0]) cylinder(r=screwHeadSpaceDiam/2, h=screwHeadSpaceHeight/2);
								translate([-nema_screw_separation/2,-screwHeadSpaceHeight/2,-nema_screw_separation/2])
									rotate([90,0,0]) sphere(r=screwHeadSpaceDiam/2);
								
								translate([-nema_screw_separation/2,0,nema_screw_separation/2])
									rotate([90,0,0]) cylinder(r=screwHeadSpaceDiam/2, h=screwHeadSpaceHeight/2);
								translate([-nema_screw_separation/2,-screwHeadSpaceHeight/2,nema_screw_separation/2])
									rotate([90,0,0]) sphere(r=screwHeadSpaceDiam/2);
							}
					}
				}
		}
	}
	
	translate([0,2*rod_nut_len+gear_thickness-nut_separation,0]) {
		translate([0,bearing_width-bearingDepth,0]) {
			if(draw_references) color("blue") %frame(20);
			difference() {
				// Main block
				color(color_stillPart) union() {
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
						bearingHole(depth=bearingDepth, thickness=partThickness, model=Y_threaded_rodBearingModel);
				translate([0,dimY/2,-dimZ+footThickness]) {
					translate([footSeparation+dimX/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance,rot=90, invert=true);
					translate([dimX/3,dimY/2+footSeparation+foot_additional_separation,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
					translate([-footSeparation-foot_additional_separation-motor_YgearSeparation_projected-Ymotor_sideLen/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
				}
				// Translate to motor axis position
				rotate([0,-motorRotatedOffset,0]) {
					translate([-axes_YgearSeparation,0,0])
						rotate([0,motorRotatedOffset,0]) {
							translate([0,motorWallSeparation-0.01,0])
							rotate([0,0,90]) rotate([0,-90,0]) 
								stepperMotor_mount(motorWallSeparation, sideLen=Ymotor_sideLen, slideOut=false);
						}
				}
			}
		
			// Draw vitamins (nuts, bolts, bearings)
			translate([0,dimY/2,-dimZ+footThickness]) {
				translate([footSeparation+dimX/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,rot=90,invert=true,autoNutOffset=true,echoPart=true);
				translate([dimX/3,dimY/2+footSeparation+foot_additional_separation,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,rot=90,invert=true,autoNutOffset=true,echoPart=true);
				translate([-footSeparation-foot_additional_separation-motor_YgearSeparation_projected-Ymotor_sideLen/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,rot=90,invert=true,autoNutOffset=true,echoPart=true);
			}
			// Translate to motor position
			rotate([0,-motorRotatedOffset,0]) {
				translate([-axes_YgearSeparation,0,0])
					rotate([0,motorRotatedOffset,0]) {
						translate([0,motorWallSeparation,0])
							rotate([90,0,0])
								stepperMotor(screwHeight=motorWallSeparation, echoPart=true);
						if(Render_Y_motorGear) {
							translate([0,-(bearing_width-bearingDepth)-motorWallSeparation-nut_separation,0])
								rotate([-90,180,0]) color(color_movingPart)
									cyclone_motor_gear(Gear_N_Teeth=Y_motorGearRatio, gearHeight=gear_thickness, tolerance=screwHoleTolerance);
						}
					}
			}
			if(Render_Y_gearCover) {
				// Draw the Y gear cover
				translate([0,-0.1,0])
					color(color_stillPart) Cyclone_YsubPart_gearCover();
			}
		}
		rotate([-90,0,0])
			radialBearing(echoPart=true);
	}
	translate([0,0.1,0])
		rotate([-90,0,0]) rotate([0,0,45]) nut(size=rodNutSize, chamfer=true, echoPart=true);
	if(Render_Y_rodGear) {
		translate([0,2*rod_nut_len-(nut_separation/2),0])
			rotate([-90,0,0]) color(color_movingPart)
				cyclone_rod_gear(Gear_N_Teeth=Y_rodGearRatio, gearHeight=gear_thickness, nutSize=Y_threaded_rodNutSize, tolerance=screwHoleTolerance);
	}
	translate([0,rod_nut_len+gear_thickness-nut_separation,0])
		rotate([-90,0,0])	nut(size=rodNutSize, echoPart=true);
}

module Cyclone_Y_backFrame() {
	
	screwSize = Y_backFrame_footScrewSize;
	
	rodNutSize = Y_threaded_rodNutSize;
	//rod_nut_len = 0.8*axes_Ythreaded_rodD;
	rod_nut_len = METRIC_NUT_THICKNESS[rodNutSize];
	bearing_width = bearingWidth(Y_threaded_rodBearingModel);
	bearing_diam = bearingOuterDiameter(Y_threaded_rodBearingModel);
	bearingDepth = Y_threaded_rodBearingDepth;
	partThickness = 5+screwSize*2;
	
	dimX = bearing_diam+partThickness;
	dimY = partThickness;
	dimZ = 0;
	
	footSeparation = screwSize*2;
	foot_additional_separation = Y_foot_additional_separation;
	footThickness = Y_frame_footThickness;
	
	endstopHolderRotation = Y_endstopHolderRotation;
	
	translate([0,-2*rod_nut_len,0]) {
		translate([0,bearingDepth-bearing_width,0]) {
			difference() {
				union() {
					color(color_stillPart) {
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
					}
					translate([0,-dimY-0.01,dimX/2])
						rotate([0,endstopHolderRotation,0])
							endstop_holder(holes=false, plasticColor=color_stillPart);
				}
				
				translate([0,-dimY-0.01,dimX/2])
					rotate([0,endstopHolderRotation,0])
						endstop_holder(holes=true);
				
				translate([0,0.01,0])
					rotate([90,0,0])
						bearingHole(depth=bearingDepth, thickness=partThickness, model=Y_threaded_rodBearingModel);
				translate([0,-dimY/2,-axes_Y_threaded_height+footThickness]) {
					translate([-footSeparation-dimX/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
					translate([footSeparation+dimX/2,0,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
					translate([0,dimY/2+footSeparation+foot_additional_separation,0])
						rotate([0,90,0])
							rotate([0,0,90])
								hole_for_screw(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
				}
			}
		
			// Draw vitamins (nuts, bolts, bearings)
			translate([0,-dimY/2,-axes_Y_threaded_height+footThickness]) {
				translate([-footSeparation-dimX/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,rot=90,invert=true,autoNutOffset=true,echoPart=true);
				translate([footSeparation+dimX/2,0,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,rot=90,invert=true,autoNutOffset=true,echoPart=true);
				translate([0,dimY/2+footSeparation+foot_additional_separation,0])
					rotate([0,90,0])
						rotate([0,0,90])
							screw_and_nut(size=screwSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,rot=90,invert=true,autoNutOffset=true,echoPart=true);
			}
		}
		rotate([90,0,0])
			radialBearing(echoPart=true);
	}
	translate([0,0.01,0])
		rotate([90,0,0])
			rotate([0,0,45]) nut(size=rodNutSize, chamfer=true, echoPart=true);
	translate([0,-rod_nut_len,0])
		rotate([90,0,0])
			nut(size=rodNutSize, echoPart=true);
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
	
	footScrewSize = Y_rightSmoothRodIdler_footScrewSize;
	rodScrewSize = Y_rightSmoothRodIdler_rodScrewSize;
	
	dimX = holderOuterRadius*2;
	dimY = 5+footScrewSize*2;
	dimZ = axes_Yreference_height;
	
	slotHeight = 3;
	screwLength = holderOuterRadius*2;
	
	logoDepth = dimY/4;
	
	
	footSeparation = footScrewSize*2;
	footThickness = Y_frame_footThickness;
	
	color(color_stillPart) difference() {
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
						hole_for_screw(size=rodScrewSize,length=screwLength+10,nutDepth=10,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
		translate([dimX/2,dimY/2,0])
			cube([dimX+1,dimY+1,slotHeight],center=true);
		if(Logo){
			translate([(dimX-holderOuterRadius)/2,-0.1,-(dimZ+axes_Ysmooth_rodD/2)/2])
				scale([1,-1,1])
					rotate([90,0,0])
						Cyclone_logo(sizemm = min(dimX+holderOuterRadius-5,dimZ-axes_Ysmooth_rodD/2-5), thickness = logoDepth, mirrorLogo = mirrorLogo);
		}
		translate([0,dimY/2,-axes_Yreference_height+footThickness]) {
			translate([-holderOuterRadius-footSeparation,0,0])
				rotate([0,90,0])
					rotate([0,0,90])
						hole_for_screw(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
			translate([holderOuterRadius*2+footSeparation,0,0])
				rotate([0,90,0])
					rotate([0,0,90])
						hole_for_screw(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
			translate([holderOuterRadius/2,dimY/2+footSeparation,0])
				rotate([0,90,0])
					rotate([0,0,90])
						hole_for_screw(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, rot=90, invert=true);
		}
	}
	// Draw nuts and bolts
	translate([2.5+holderOuterRadius,dimY/2,holderOuterRadius])
		rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=rodScrewSize,length=screwLength+10,nutDepth=10,nutAddedLen=0,captiveLen=0,rot=90,echoPart=true);
	translate([0,dimY/2,-axes_Yreference_height+footThickness]) {
		translate([-holderOuterRadius-footSeparation,0,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,autoNutOffset=true,rot=90,invert=true,echoPart=true);
		translate([holderOuterRadius*2+footSeparation,0,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,autoNutOffset=true,rot=90,invert=true,echoPart=true);
		translate([holderOuterRadius/2,dimY/2+footSeparation,0])
			rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,autoNutOffset=true,rot=90,invert=true,echoPart=true);
	}
}

module Cyclone_Y_leftSmoothRodIdler() {
	scale([-1,1,1]) Cyclone_Y_rightSmoothRodIdler(mirrorLogo = true);
}
