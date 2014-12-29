// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

X_motorModel = Nema17;	
Xmotor_sideLen = lookup(NemaSideSize, X_motorModel); //42.20;
axes_XgearRatio = X_motorGearRatio/X_rodGearRatio; // Number of tooth (motor/rod)

module Cyclone_X_leftFrame() {
	scale([-1,1,1]) Cyclone_X_rightFrame(isLeft=true);
}

include <libs/MCAD/stepper.scad>
module Cyclone_X_rightFrame(isLeft=false) {

	footThickness = X_frame_footThickness;
	corner_radius = X_frame_corner_radius;
	frameFrontalThickness = X_frame_FrontalThickness;
	
	footScrewSize = X_Frame_footScrewSize;
	rodScrewSize = X_Frame_rodScrewSize;
	
	motorWallSeparation = X_motorWallSeparation;
	motorRotatedOffset = X_motorRotatedOffset;
	gearWallSeparation = X_gearWallSeparation;
	
	partThickness = X_frames_additional_thickness+rodScrewSize*2;
	
	dimX = partThickness;
	dimY = max(-axes_Xreference_posY,axes_Xsmooth_separation+axes_XgearSeparation*cos(motorRotatedOffset)+Xmotor_sideLen/2+1.6);
	dimZ = axes_Yreference_height+axes_Xreference_height+axes_Xsmooth_separation;
	
	footSeparation = footScrewSize*3;
	footWidth = dimX+2*footSeparation;
	
	rodNutSize = X_threaded_rodNutSize;
	rod_nut_len = METRIC_NUT_THICKNESS[rodNutSize];
	nut_separation = rod_nut_len/2;
  //rod_nut_len = 0.8*axes_Xthreaded_rodD;
	
	module Cyclone_XsubPart_gearCover() {
		margin = gearCover_margin;
		rodGearAddedMargin = rodGearAddedgearCover_margin;
		effectiveXgearSeparation = axes_XgearSeparation+0.5;
		wallThickness = gearCover_wallThickness;
		screwHeadSpaceHeight = gearCover_screwHeadSpaceHeight;
		screwHeadSpaceDiam = gearCover_screwHeadSpaceDiam;
		coverHeight = gearCoverHeight;
		coverExtraHeight = gearCoverExtraHeight;
		coverExtraRadius = gearCoverExtraRadius;
		nema_screw_separation = lookup(NemaDistanceBetweenMountingHoles, X_motorModel);
		truncationAngle = gearCover_truncationAngle;
	
		motorGearRadius = axes_XgearSeparation/(1+axes_XgearRatio)+gearCover_margin;
		rodGearRadius = axes_XgearSeparation/(1+1/axes_XgearRatio)+gearCover_margin+rodGearAddedgearCover_margin;
		
		difference() {
			union() {
				// Cover for the rod gear
				rotate([0,90,0])
					cylinder(r=rodGearRadius+gearCover_wallThickness, h=coverHeight);
				translate([coverHeight,0,0])
					rotate([0,90,0])
						cylinder(r1=rodGearRadius+gearCover_wallThickness, r2=rodGearRadius+gearCover_wallThickness+coverExtraRadius, h=coverExtraHeight+gearCover_wallThickness);
				// Translate to motor position
				rotate([motorRotatedOffset,0,0]) {
					translate([0,effectiveXgearSeparation,0])
						rotate([-motorRotatedOffset,0,0]) {
							// Cover for the motor gear
							rotate([0,90,0]) cylinder(r=motorGearRadius+gearCover_wallThickness, h=coverHeight);
							translate([coverHeight,0,0])
								rotate([0,90,0]) cylinder(r1=motorGearRadius+gearCover_wallThickness, r2=motorGearRadius+gearCover_wallThickness+coverExtraRadius, h=coverExtraHeight+gearCover_wallThickness);
							// Cylinder for the support screw
							translate([0,-nema_screw_separation/2,nema_screw_separation/2])
								rotate([0,90,0]) cylinder(r=gearCover_screwHeadSpaceDiam/2+gearCover_wallThickness, h=coverHeight);
						}
				}
			}
			translate([-0.02,0,0])
				union() {
					// Truncation for avoiding collisions with Y carriage (needed for the Y gear cover)
					translate([0,-rodGearRadius/2,-rodGearRadius-0.5])
						rotate([0,90+gearCover_truncationAngle,0]) cube(rodGearRadius);
					// Hole for the rod gear
					rotate([0,90,0])
						cylinder(r=rodGearRadius, h=coverHeight);
					translate([coverHeight-0.02,0,0])
						rotate([0,90,0])
							cylinder(r1=rodGearRadius, r2=rodGearRadius+coverExtraRadius, h=coverExtraHeight);
					rotate([0,90,0])
						cylinder(r=rodGearRadius+coverExtraRadius, h=coverHeight+coverExtraHeight+gearCover_wallThickness+0.1);
					// Translate to motor position
					rotate([motorRotatedOffset,0,0]) {
						translate([0,effectiveXgearSeparation,0])
							rotate([-motorRotatedOffset,0,0]) {
								difference() {
									union() {
										// Hole for the motor gear
										rotate([0,90,0]) cylinder(r=motorGearRadius, h=coverHeight);
										translate([coverHeight-0.02,0,0])
											rotate([0,90,0]) cylinder(r1=motorGearRadius, r2=motorGearRadius+coverExtraRadius, h=coverExtraHeight);
										rotate([0,90,0]) cylinder(r=motorGearRadius+coverExtraRadius, h=coverHeight+coverExtraHeight+gearCover_wallThickness+0.1);
										// Outer hole for the support screw
										translate([0,-nema_screw_separation/2,nema_screw_separation/2])
											rotate([0,90,0]) cylinder(r=gearCover_screwHeadSpaceDiam/2, h=coverHeight+coverExtraHeight*2);
									}
									// Support screw holder
									translate([0,-nema_screw_separation/2,nema_screw_separation/2])
										rotate([0,90,0]) cylinder(r=gearCover_screwHeadSpaceDiam/2+gearCover_wallThickness, h=gearCover_wallThickness);
								}
								// Inner hole for the support screw
								translate([0,-nema_screw_separation/2,nema_screw_separation/2])
									rotate([0,90,0]) cylinder(r=(gearCover_screwHeadSpaceDiam+1)/2, h=coverHeight+0.1);
								// Holes for the other three screws
								translate([0,nema_screw_separation/2,nema_screw_separation/2])
									rotate([0,90,0]) cylinder(r=gearCover_screwHeadSpaceDiam/2, h=gearCover_screwHeadSpaceHeight/2);
								translate([gearCover_screwHeadSpaceHeight/2,nema_screw_separation/2,nema_screw_separation/2])
									rotate([0,90,0]) sphere(r=gearCover_screwHeadSpaceDiam/2);
								
								translate([0,nema_screw_separation/2,-nema_screw_separation/2])
									rotate([0,90,0]) cylinder(r=gearCover_screwHeadSpaceDiam/2, h=gearCover_screwHeadSpaceHeight/2);
								translate([gearCover_screwHeadSpaceHeight/2,nema_screw_separation/2,-nema_screw_separation/2])
									rotate([0,90,0]) sphere(r=gearCover_screwHeadSpaceDiam/2);
								
								translate([0,-nema_screw_separation/2,-nema_screw_separation/2])
									rotate([0,90,0]) cylinder(r=gearCover_screwHeadSpaceDiam/2, h=gearCover_screwHeadSpaceHeight/2);
								translate([gearCover_screwHeadSpaceHeight/2,-nema_screw_separation/2,-nema_screw_separation/2])
									rotate([0,90,0]) sphere(r=gearCover_screwHeadSpaceDiam/2);
							}
					}
				}
		}
	}

	module Cyclone_X_endstopHolder(holes=false) {
		// Endstop holder
		translate([-partThickness-0.04,19,-5+axes_Xsmooth_separation])
			rotate([-60,0,0]) {
				rotate([0,0,-90]) mirror([1,0,0])
					endstop_holder(holes, shortNuts=true, plasticColor=color_stillPart);
				if(holes)
					cube([partThickness+1,100,50]);
			}
	}
	
	// Crocodile clip holders and wire guide
	module Cyclone_X_frameHoles() {
		holeWidth = dimY/2;
		holeHeight = dimZ-footThickness-axes_Xsmooth_separation-27;
		
		crocodileHolderStepLenght = 12/2;
		crocodileHolderThick = 5;
		crocodileHolderSlim = 2.5;
		crocodileHoldersSeparation = holeWidth/3;
		
		wireSlotSeparation = dimX; // Distance from outer wall
		wireSlotThicknessThick = 4;
		wireSlotThicknessSlim = 3;
		wireSlotDepth = 5;
		
		wireHoleDiam = 10;
		
		module SingleCrocodileClipHolder() {
			translate([-partThickness/2,0,0]) union() {
				rotate([0,90,0]) bcube([crocodileHolderStepLenght*2,crocodileHolderThick,partThickness*2], cr=1, cres=10);
				rotate([0,90,0]) bcube([crocodileHolderStepLenght*4,crocodileHolderSlim,partThickness*2], cr=1, cres=10);
			}
		}
		
		// Translate to lower-front corner
		translate([0,frameFrontalThickness, -axes_Yreference_height-axes_Xreference_height+footThickness+0.01]) {
			color(color_stillPart)
				difference() {
					// Main hole
					translate([-partThickness/2,holeWidth/2,holeHeight/2])
						rotate([0,90,0]) bcube([holeHeight,holeWidth,partThickness*2], cr=15, cres=10);
					// Translate to top center position
					translate([0,holeWidth/2,holeHeight]) {
						// Crocodile clip holders
						translate([0,crocodileHoldersSeparation/2,0])
							SingleCrocodileClipHolder();
						translate([0,-crocodileHoldersSeparation/2,0])
							SingleCrocodileClipHolder();
					}
				}
			if(isLeft) {
				// Wire slot
				translate([wireSlotDepth-dimX, dimY-frameFrontalThickness-wireSlotSeparation-wireSlotThicknessSlim/2, dimZ/2+0.01]) {
					translate([-wireSlotDepth,0,0])
						rotate([0,0,180]) cube([wireSlotDepth*2,wireSlotThicknessSlim,dimZ], center=true);
					cylinder(r=wireSlotThicknessThick/2, h=dimZ, center=true);
					translate([0,0,-dimZ/2+wireHoleDiam/2])
						rotate([0,-90,0]) cylinder(r=wireSlotThicknessThick/2, h=wireSlotDepth*2);
					// Wire hole (thick)
					translate([-wireSlotDepth-wireHoleDiam/2-0.01,0,-dimZ/2+wireHoleDiam/2])
						rotate([90,90,0]) cylinder(r=wireHoleDiam/2, h=100, center=true);
				}
			}
		}
	}
	
	difference() {
		// Main block
		union() {
			color(color_stillPart) translate([-axes_Xreference_posX-dimX-0.01,axes_Xreference_posY,-axes_Yreference_height]) {
				cube([dimX,dimY,dimZ-axes_Xsmooth_separation]);
				translate([-footWidth/2+dimX,dimY/2,footThickness/2]) bcube([footWidth,dimY,footThickness], cr=corner_radius, cres=10);
			}
			rodHolder(rodD=axes_Ysmooth_rodD, screwSize=rodScrewSize, height=axes_Yreference_height, sideLen=-axes_Xreference_posX-1);
			// TRANSLATE REFERENCE POSITION to the left frame, X lower smooth rod end
			translate([-axes_Xreference_posX,axes_Xreference_posY,axes_Xreference_height]) {
				// TRANSLATE REFERENCE POSITION to the threaded rod
				translate([-0.01,axes_Xsmooth_separation,0]) {
					rotate([0,-90,0])
					 	color(color_stillPart) cylinder(r=axes_Xsmooth_separation,h=partThickness);
					if(isLeft) 
						Cyclone_X_endstopHolder(holes=false);
				}
			}
		}
		
		// TRANSLATE REFERENCE POSITION to the left frame, X lower smooth rod end
		color(color_stillPart) translate([-axes_Xreference_posX,axes_Xreference_posY,axes_Xreference_height]) {
			rotate([0,0,90]) standard_rod(diam=axes_Xsmooth_rodD, length=partThickness*4, threaded=false, renderPart=true, center=true);
			rotate([0,0,-90])
				rotate([0,90,0])
					rodHolder(rodD=axes_Xsmooth_rodD, screwSize=rodScrewSize, negative=true);
			// Crocodile clip holders and wire guide
			Cyclone_X_frameHoles();
			
			// TRANSLATE REFERENCE POSITION to the threaded rod
			translate([+0.01,axes_Xsmooth_separation,0]) {
				
				// Rod radial bearing hole
				rotate([0,-90,0]) bearingHole(depth=X_threaded_rod_bearingDepth, thickness=partThickness, model=X_threaded_rodBearingModel);
				
				// Translate to motor position
				if(!isLeft)
					translate([-motorWallSeparation,0,0])
					rotate([motorRotatedOffset,0,0])
						translate([0,axes_XgearSeparation,0])
							rotate([-motorRotatedOffset,0,0])
								rotate([0,90,0]) stepperMotor_mount(motorWallSeparation, sideLen=Xmotor_sideLen, slideOut=true);
			// Endstop holder
			if(isLeft) 
						Cyclone_X_endstopHolder(holes=true);
			
			translate([0,0,axes_Xsmooth_separation]) {
				rotate([0,0,90]) standard_rod(diam=axes_Xsmooth_rodD, length=partThickness*4, threaded=false, renderPart=true, center=true);
				rotate([0,0,-90])
					rodHolder(rodD=axes_Xsmooth_rodD, screwSize=rodScrewSize, negative=true);
			}
			}
		}
		// Holes for the screws
		translate([-axes_Xreference_posX-dimX-footSeparation,axes_Xreference_posY+footSeparation,-axes_Yreference_height+footThickness]) {
			rotate([0,90,0])
					rotate([0,0,90])
						hole_for_screw(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, invert=true);
			translate([0,dimY/2,0])
				rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, invert=true);
			translate([0,dimY-2*footSeparation,0])
				rotate([0,90,0])
						rotate([0,0,90])
							hole_for_screw(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,tolerance=screwHoleTolerance, invert=true);
		}
	}
	
	// Draw rod holders, motor, gears, screws
	// TRANSLATE REFERENCE POSITION to the left frame, X lower smooth rod end
	translate([-axes_Xreference_posX,axes_Xreference_posY,axes_Xreference_height]) {
		if(draw_references) color("red") %frame(20);
		rotate([0,0,-90])
			rotate([0,90,0])
				rodHolder(rodD=axes_Ysmooth_rodD, screwSize=rodScrewSize);
		// TRANSLATE REFERENCE POSITION to the threaded rod
		translate([0,axes_Xsmooth_separation,0]) {
			if(draw_references) color("green") %frame(20);
			translate([-X_threaded_rod_bearingDepth,0,0]) rotate([0,90,0])
				radialBearing(echoPart=true);
			translate([14-X_threaded_rod_bearingDepth-0.5,0,0]) rotate([0,-90,0]){ // replace 14 with bearing hight - X_threaded_rod_bearingDepth
				nut(size=rodNutSize, echoPart=true);
				if(isLeft) {
					translate([0,0,-rod_nut_len])
						rotate([0,0,45]) nut(size=rodNutSize, chamfer=true, echoPart=true);
				}
			}
			if(!isLeft) {
				translate([X_threaded_rod_bearingDepth+(2*rod_nut_len)-(nut_separation/2)-2,0,0]) {
					translate([X_gear_thickness+(nut_separation/2),0,0])
						rotate([0,-90,0])
							rotate([0,0,45]) nut(size=rodNutSize, chamfer=true, echoPart=true);
					if(Render_X_rodGear) {
							rotate([0,-90,0]) color(color_movingPart)
							cyclone_rod_gear(Gear_N_Teeth=X_rodGearRatio, gearHeight=X_gear_thickness, nutSize=8, tolerance=screwHoleTolerance);
					}
				}
				// Translate to motor position
			  rotate([motorRotatedOffset,0,0]) {
					translate([0,axes_XgearSeparation,0])
						rotate([-motorRotatedOffset,0,0]) {
							translate([-motorWallSeparation,0,0]) rotate([0,90,0])
							  stepperMotor(screwHeight=motorWallSeparation, echoPart=true);
							if(Render_X_motorGear) {
								translate([X_threaded_rod_bearingDepth+(2*rod_nut_len)-(nut_separation/2)-2,0,0])
									rotate([0,-90,0]) color(color_movingPart)
										cyclone_motor_gear(Gear_N_Teeth=X_motorGearRatio, gearHeight=X_gear_thickness, tolerance=screwHoleTolerance);
							}
						}
				}
				if(Render_X_gearCover) {
					// Draw the X gear cover
					translate([0.1,0,0])
						color(color_stillPart) Cyclone_XsubPart_gearCover();
				}
			}
			translate([0,0,axes_Xsmooth_separation])
				rotate([0,0,-90])
					rodHolder(rodD=axes_Ysmooth_rodD, screwSize=rodScrewSize);
		}
	}
	translate([-axes_Xreference_posX-dimX-footSeparation,axes_Xreference_posY+footSeparation,-axes_Yreference_height+footThickness]) {
		rotate([0,90,0])
				rotate([0,0,90])
					screw_and_nut(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,invert=true,autoNutOffset=true,echoPart=true);
		translate([0,dimY/2,0])
			rotate([0,90,0])
					rotate([0,0,90])
						screw_and_nut(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,invert=true,autoNutOffset=true,echoPart=true);
		translate([0,dimY-2*footSeparation,0])
			rotate([0,90,0])
					rotate([0,0,90])
						screw_and_nut(size=footScrewSize,length=footThickness+base_thickness,nutDepth=0,nutAddedLen=0,captiveLen=0,invert=true,autoNutOffset=true,echoPart=true);
	}
}

module rodHolder(rodD=8.5, screwSize=3, height=0, sideLen=0, thickness=5, space=2, negative=false) {
	screwAditionalDistance = rodD/2;
	dimX = rodD+4*screwSize+screwAditionalDistance;
	dimY = X_frames_additional_thickness+screwSize*2;
	dimZ = rodD/2+thickness;
	
	corner_radius = 4;
	
	if(negative) {
		translate([screwSize+screwAditionalDistance,-dimY/2,dimZ])
				rotate([90,0,0])
					hole_for_screw(size=screwSize,length=dimZ+15,nutDepth=5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
		translate([-screwSize-screwAditionalDistance,-dimY/2,dimZ])
			rotate([90,0,0])
				hole_for_screw(size=screwSize,length=dimZ+15,nutDepth=5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
	} else {
		difference() {
			union() {
				//if(Render_rodHolder) {
					color(color_movingPart) translate([0,-dimY/2,dimZ/2+space/4]) bcube([dimX,dimY,dimZ-space/2],cr=corner_radius,cres=10);
				//}
				color(color_stillPart)
					if(sideLen>dimX/2)
						translate([sideLen/2-dimX/4,-dimY/2,-height/2-space/4]) bcube([dimX/2+sideLen,dimY,height-space/2],cr=corner_radius,cres=10);
					else
						translate([0,-dimY/2,-height/2-space/4]) bcube([dimX,dimY,height-space/2],cr=corner_radius,cres=10);
			}
			translate([screwSize+screwAditionalDistance,-dimY/2,dimZ])
				rotate([90,0,0])
					hole_for_screw(size=screwSize,length=dimZ+15,nutDepth=5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
			translate([-screwSize-screwAditionalDistance,-dimY/2,dimZ])
				rotate([90,0,0])
					hole_for_screw(size=screwSize,length=dimZ+15,nutDepth=5,nutAddedLen=0,captiveLen=10,tolerance=screwHoleTolerance, rot=90);
			standard_rod(diam=rodD, length=dimY*4, threaded=false, renderPart=true, center=true);
			//rodHolder(rodD=rodD, screwSize=screwSize, negative=true);
		}
		// Draw screws
		translate([screwSize+screwAditionalDistance,-dimY/2,dimZ+0.01])
			rotate([90,0,0])
				screw_and_nut(size=screwSize,length=dimZ+15,nutDepth=5,nutAddedLen=0,captiveLen=0,rot=90,echoPart=true);
		translate([-screwSize-screwAditionalDistance,-dimY/2,dimZ+0.01])
			rotate([90,0,0])
				screw_and_nut(size=screwSize,length=dimZ+15,nutDepth=5,nutAddedLen=0,captiveLen=0,rot=90,echoPart=true);
	}
}
