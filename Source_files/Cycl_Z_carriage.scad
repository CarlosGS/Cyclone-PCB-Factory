// Cyclone PCB Factory: a 3D printable CNC machine for PCB manufacture
// Created by Carlosgs (http://carlosgs.es)
// License: Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
 /*
 * August 2013 changes to design top-part mounting screw at same side as bottom-part.
 * also started introduced 2nd spindle diameter for a-symmetrical spindles. this is not working yet.
 * by Harry Binnema. 
 */

include <libs/MCAD/stepper.scad>
include <libs/MCAD/bearing.scad>
include <libs/MCAD/metric_fastners.scad>
include <libs/MCAD/nuts_and_bolts.scad>
use <libs/Write/Write.scad>
use <libs/linear_bearing.scad>
use <libs/obiscad/obiscad/vector.scad>
use <libs/obiscad/obiscad/attach.scad>
use <libs/obiscad/obiscad/bcube.scad>
use <libs/standard_parts.scad>
use <libs/MCAD/materials.scad>

Z_motorModel = Nema17;
motor_width = lookup(NemaSideSize, Z_motorModel);
motor_screw_head_diameter = METRIC_BOLT_CAP_DIAMETERS[3]+1+screwHoleTolerance;;

Z_bearing_width = bearingWidth(Z_threaded_rodBearingModel);

axis_distance = 21;

wall_thickness = Z_carriage_wall_thickness;
wall_height = motor_width;
wall_width = Z_carriage_wall_width;

axes_ZgearRatio = Z_motorGearRatio/Z_rodGearRatio; // Number of tooth (motor/rod)

Z_smooth_rods_sep = axes_Xsmooth_separation;

module Cyclone_Z_carriage(z_thread_rod_length=120, with_extra_parts=false, exploded=false) {
  // Settings
	linearBearingDiameter = linearBearing_D(Z_linearBearingModel);
  linearBearingLength = linearBearing_L(Z_linearBearingModel);
  spindle_holder_distance = linearBearingLength*2+3;
	gear_thickness = Z_gear_thickness;
	
	ZthreadedOffset = -3.5;
	axes_Xsmooth_separation = 16+ZthreadedOffset;
	Z_threaded_pos = motor_width/2+axis_distance+axes_Xsmooth_separation;
	spindle_front_offset = 10+ZthreadedOffset;
	
	rodNutSize = Z_threaded_rodNutSize;
	
	module dummySpindle(length=0) {
		translate([0,0,-length]) {
			translate([0,0,spindle_motor_length-5]) color([0.95,0.95,0.95]) cylinder(r=26,h=30);
			translate([0,0,spindle_motor_length-10]) color([0.95,0.95,0.95]) cylinder(r=10/2,h=5);
			translate([0,0,-10]) color([0.6,0.6,0.6]) cylinder(r=26,h=spindle_motor_length);
			translate([0,0,-40]) color([0.9,0.9,0.9]) cylinder(r=15/2,h=40);
			translate([0,0,-50]) color([0.4,0.4,0.4]) cylinder(r=20/2,h=10);
			translate([0,0,-50-20]) color([0.9,0.9,0.9]) cylinder(r1=1/2,r2=3/2,h=20);
		}
	}

	// Derived from Spindle mount for ShapeOko by Misan (http://www.thingiverse.com/thing:26740)
	module spindle_holder_holes(length,spindiam,top_part) {
		translate([0,spindle_front_offset,0])
		if (top_part){
			translate([0,38,0]) rotate([0,0,0]) {
			translate([0,0,-0.05]) {
				cylinder(r=spindle_motor_diam_top_smaller/2,h=length+2);
				intersection() {
					cylinder(r=spindle_motor_diam_top/2,h=length+2);
					cube([spindle_motor_diam_top,spindle_motor_sidelen,2*(length+2)],center=true);
				}
			}
			translate([0,-4,-0.01]) cube([90,4,length+2]);
			translate ([spindiam/2+15,15,length/2]) rotate([90,0,0]) cylinder(r=2,h=30);
			translate ([spindiam/2+15,-10.5,length/2]) rotate([90,0,0]) cylinder(r=3.5,h=4,$fn=6);
			translate ([spindiam/2+15,10.5,length/2]) rotate([0,0,0]) screw_and_nut(size=spindle_holder_screwSize,length=25,nutDepth=4,nutAddedLen=0,captiveLen=0,autoNutOffset=true,echoPart=true);
			}		
			}
		else
			{
			translate([0,38,0]) rotate([0,0,180]) {
			translate([0,0,-0.05]) cylinder(r=spindle_motor_diam/2,h=length+2);
			translate([0,0,-0.01]) cube([90,4,length+2]);
			translate ([spindiam/2+15,20,length/2]) rotate([90,0,0]) cylinder(r=2,h=30);
			translate ([spindiam/2+15,15,length/2]) rotate([90,0,0]) cylinder(r=3.5,h=4,$fn=6);
			translate ([spindiam/2+15,17,length/2]) rotate([0,0,0]) screw_and_nut(size=spindle_holder_screwSize,length=25,nutDepth=4,nutAddedLen=0,captiveLen=0,invert=true,autoNutOffset=true,echoPart=true);
			}
			}
	}
	
	// Creates the part where the alluminium spindle holder will be attached to. 
	// This part is joined to the current Z carriage instead of the dremel holder.
	module SpindleHolder(top_part=true, boltDiam=6, horizontalBoltDistance=70, verticalBoltDistance=18, holderWidth=90){

			holderHeight = (spindle_holder_distance+1.5)/2;
			translate([0,18,holderHeight/2]){
				difference(){
					union(){
						hull(){
							translate([(holderWidth)/2,-10,-0.5])cylinder(r=3,h=holderHeight-1,center=true);
							translate([-(holderWidth)/2,-10,-0.5])cylinder(r=3,h=holderHeight-1,center=true);
							translate([20,-21,-0.5])cylinder(r=8,h=holderHeight-1,center=true);
							translate([-20,-21,-0.5])cylinder(r=8,h=holderHeight-1,center=true);
						}
					}
					translate([0,-65,0])cylinder(r=48,h=holderHeight,center=true);
					translate([0,-30,0])cylinder(r=16,h=holderHeight,center=true);

					translate([horizontalBoltDistance/2,-36,holderHeight/2-verticalBoltDistance/2])
						scale([1,5,1])
							rotate([-90,360/12,0])
								union(){
									nutHole(6, units=MM,length=80, tolerance = +screwHoleTolerance, proj = -1);
									boltHole(6, units=MM,length=80, tolerance = +screwHoleTolerance, proj = -1);
								}
					translate([-horizontalBoltDistance/2,-36,holderHeight/2-verticalBoltDistance/2])
						scale([1,5,1])
							rotate([-90,360/12,0])
								union(){
									nutHole(6, units=MM,length=80, tolerance = +screwHoleTolerance, proj = -1);
									boltHole(6, units=MM,length=80, tolerance = +screwHoleTolerance, proj = -1);
								}
				}
				// Draw screws
				translate([horizontalBoltDistance/2,-25,holderHeight/2-verticalBoltDistance/2])
					rotate([0,0,180]) screw_and_nut(size=6,length=90, rot=90, invert=true, echoPart=true);
				translate([-horizontalBoltDistance/2,-25,holderHeight/2-verticalBoltDistance/2])
					rotate([0,0,180]) screw_and_nut(size=6,length=90, rot=90, invert=true, echoPart=true);
			}
	}
	
	module motorHolesZ() {
		nema_screw_separation = lookup(NemaDistanceBetweenMountingHoles, Z_motorModel);

		// Screws for holding the motor
		translate([0,0,-wall_thickness/1.9])
		stepperMotor_mount(wall_thickness+1, sideLen=0, slideOut=false);

		// Hole for the screwdriver
		translate([0,-wall_width/2,wall_thickness/2])
			rotate([0,90,90]) bcube([2*(wall_thickness-5),5,wall_height],cr=1);


		for(i=[-1,1]) for(j=[-1,1])
		translate([i*nema_screw_separation/2,j*nema_screw_separation/2,2.5-wall_thickness/2+3]) {
			hull() {
				translate([0,Z_motor_adjust_margin/2,0])
					cylinder(r=motor_screw_head_diameter/2,h=10*wall_thickness,center=false);
				translate([0,-Z_motor_adjust_margin/2,0])
					cylinder(r=motor_screw_head_diameter/2,h=10*wall_thickness,center=false);
			}
		}
	}

	module motor_stand_holes_Z() {
	  partThickness = wall_thickness;
		// Position relative to motor shaft
		translate([motor_width/2,motor_width/2,wall_thickness/2]) {
			motorHolesZ();

			// Bearing holes
			translate([0,axis_distance,0]) {
				bearingHole(depth=Z_bearing_width, thickness=partThickness, model=Z_threaded_rodBearingModel, tolerance=Z_radialBearingHole_tolerance);

				hull() {
						cylinder(r=(axes_Zsmooth_rodD*2)/2,h=10*wall_thickness,center=true);
					translate([0,-axis_distance,0])
						cylinder(r=(axes_Zsmooth_rodD*2)/2,h=10*wall_thickness,center=true);
				}
			}
		}
	}

	module linearBearingHolderZ(h=10) {
		linearBearingDiameter = linearBearing_D(Z_linearBearingModel);
		translate([0,0,1.5]) cylinder(r=linearBearingDiameter/2+Z_linearBearingHole_tolerance,h=h);
		cylinder(r=linearBearingDiameter/2.5,h=10*h,center=true);
	}

	module Z_solid_body(top_part=true) {
		union() {
			color(color_stillPart) hull() {
				if(top_part)
					translate([wall_height/2,wall_width/2,wall_thickness/2])
						bcube([wall_height,wall_width,wall_thickness],cr=4,cres=10);
				else
					translate([wall_height/2,wall_width,wall_thickness/2])
						bcube([wall_height,wall_width/2,wall_thickness],cr=4,cres=10);
				translate([0,spindle_front_offset,0])
					translate([wall_height/2,wall_width-4,0])
					translate([0,38,0])
						if(top_part)
							cylinder(r=spindle_motor_diam_top/2+spindle_holder_thickness,h=wall_thickness);
						else
							cylinder(r=spindle_motor_diam/2+spindle_holder_thickness,h=wall_thickness);
			}
	
			// For the linear bearing holders
			hull() {
				translate([wall_height/2-Z_smooth_rods_sep/2,Z_threaded_pos,0])
					cylinder(r=3+linearBearingDiameter/2,h=wall_thickness);
				translate([wall_height/2+Z_smooth_rods_sep/2,Z_threaded_pos,0])
					cylinder(r=3+linearBearingDiameter/2,h=wall_thickness);
			}
			
			// Select tool holder
			if(tool==dremel)
			{
				// For the claw of the spindle holder
				translate([0,spindle_front_offset,0])
				if(top_part){
					translate([wall_height/2,wall_width-4,0])
						translate([0,38,0]) {
							rotate([0,0,0]) {
								translate([spindle_motor_diam_top/2,-12.5,0]) cube([20,20,wall_thickness]);
								
					// Write text in the front
					color([0.5,0.5,0.5])
							rotate([0,0,180]) scale([-1,1,-textHscale])
								writecylinder(topText,[0,0,-wall_thickness/(2*textHscale)],spindle_motor_diam_top/2+spindle_holder_thickness,0,font="orbitron.dxf",space=1.1,h=wall_thickness,t=textThickness,center=true,ccw=true);
							}
						}
				}
				else
				translate([wall_height/2,wall_width-4,0])
					translate([0,38,0]) {
						
						rotate([0,0,180]) {
						translate([spindle_motor_diam/2,-7-0.5,0]) cube([22,20,wall_thickness]);
						color([0.2,0.2,0.5])
						scale([1,1,textHscale])
							writecylinder(bottomText,[0,0,wall_thickness/(2*textHscale)+1],spindle_motor_diam/2+spindle_holder_thickness,0,font="orbitron.dxf",space=1.1,h=wall_thickness-2,t=textThickness,center=true,ccw=true);
						}
					}
			}else{
				//Tool = SpindleHolder
				translate([(wall_height/2+Z_smooth_rods_sep/2)/2+0.5,Z_threaded_pos,0])
					SpindleHolder(top_part=top_part,boltDiam=spindle_holder_bolt_diam, horizontalBoltDistance=spindle_holder_bolt_X_separation, verticalBoltDistance=spindle_holder_bolt_Z_separation);
			}
		}
	}

	module Z_carriage(showSpindle=false,top_part=true, with_extra_parts=false, exploded=false) {
		difference() {
			rotate([0,0,-90]) translate([-wall_height/2,-Z_threaded_pos,0]) {
				difference () {
					Z_solid_body(top_part);
					if(top_part) motor_stand_holes_Z();
					if(tool==dremel) { 
						translate([wall_height/2,wall_width-4,0])
							spindle_holder_holes(wall_thickness,spindle_motor_diam,top_part);
					}
					
					translate([wall_height/2-Z_smooth_rods_sep/2,Z_threaded_pos,0])
						linearBearingHolderZ(10*wall_thickness);
					translate([wall_height/2+Z_smooth_rods_sep/2,Z_threaded_pos,0])
						linearBearingHolderZ(10*wall_thickness);
					if(tool==spindle_holder)
					{//Substract dremel holder
						translate([(wall_height/2+Z_smooth_rods_sep/2)/2,Z_threaded_pos+51,25])cube([200,80,51], center=true);
					} else {// Additional drills next to the linear bearings
						translate([wall_height/2-Z_smooth_rods_sep/2,Z_threaded_pos+14,0])
							cylinder(r=4.5/2,h=50,center=true);
						translate([wall_height/2+Z_smooth_rods_sep/2,Z_threaded_pos+14,0])
							cylinder(r=4.5/2,h=50,center=true);
					}
				}
			}

			// Hole for the threaded rod
			if(!top_part) {
				translate([-axes_Xsmooth_separation,0,0]) 
					cylinder(r=6+axes_Zsmooth_rodD,h=wall_thickness*10,center=true);
			}

			// Truncation in the base for avoiding collision with the X axis
			if(!top_part) translate([-15-axes_Xsmooth_separation+11+ZthreadedOffset,0,0]) cube([20,100,50],center=true);
		}
	}
	
	// Carriages	
	if(Render_Z_carriageBottom) {
		rotate([0,0,-90])
			Z_carriage(showSpindle=true,top_part=false,with_extra_parts=with_extra_parts, exploded=exploded);
	}
	if(Render_Z_carriageTop) {
		translate([0,0,spindle_holder_distance+1.5]) rotate([180,0,-90])
			Z_carriage(showSpindle=false,top_part=true,with_extra_parts=with_extra_parts, exploded=exploded);
	}
	
	// Bearings
	translate([-axes_Zsmooth_separation/2,0,1.5])
		linearBearing_single(model=Z_linearBearingModel, echoPart=true);
	translate([axes_Zsmooth_separation/2,0,1.5])
		linearBearing_single(model=Z_linearBearingModel, echoPart=true);
	translate([-axes_Zsmooth_separation/2,0,linearBearingLength+0.5+1.5])
		linearBearing_single(model=Z_linearBearingModel, echoPart=true);
	translate([axes_Zsmooth_separation/2,0,linearBearingLength+0.5+1.5])
		linearBearing_single(model=Z_linearBearingModel, echoPart=true);
	translate([0,axes_Xsmooth_separation,spindle_holder_distance+1.5-wall_thickness/2])	
		rotate([180,0,0])
			radialBearing(echoPart=true);
		
  // Motor
	translate([0,axes_Xsmooth_separation+axis_distance,spindle_holder_distance+1.5]) rotate([180,0,0])
		stepperMotor(screwHeight=wall_thickness/2+1.5, echoPart=true);
		
	// Gears
	color(color_stillPart) {
		translate([0,axes_Xsmooth_separation+axis_distance+2,spindle_holder_distance+2-wall_thickness-gear_thickness])
			cyclone_motor_gear(Gear_N_Teeth=Z_motorGearRatio,gearHeight=gear_thickness+5,tolerance=screwHoleTolerance);
		translate([0,axes_Xsmooth_separation,spindle_holder_distance+1.5-wall_thickness/2-Z_bearing_width*2-gear_thickness/4])
			cyclone_rod_gear(Gear_N_Teeth=Z_rodGearRatio,gearHeight=gear_thickness,nutSize=8,tolerance= screwHoleTolerance);
	}
		
	// Nuts	
	translate([0,axes_Xsmooth_separation,spindle_holder_distance+1.5-wall_thickness/2-Z_bearing_width*2])
	  nut(size=rodNutSize, echoPart=true);
	translate([0,axes_Xsmooth_separation,spindle_holder_distance+1.5-wall_thickness/2-Z_bearing_width*2-gear_thickness*1.4])
	  nut(size=rodNutSize, chamfer=true, echoPart=true);
	  
	if( tool == dremel){
	  // Dremel tool
		translate([0,-40,-40]) {
			color([0.2,0.2,0.2]) %cylinder(r1=30/2, r2=50/2, h=40);
			translate([0,0,50])
				color([0.2,0.2,0.2]) %cylinder(r=50/2, h=80);
			translate([0,0,50+80])
				color([0.2,0.2,0.2]) %cylinder(r1=50/2, r2=30/2, h=10);
			translate([0,0,-20])
				color([0.4,0.4,0.4]) %cylinder(r1=12/2, r2=10/2, h=20);
			translate([0,0,-20-20])
				color([0.9,0.9,0.9]) %cylinder(r1=0.5/2, r2=3/2, h=20);
			
		}
	}
	if( tool == spindle_holder){
	  // Spindle tool
		translate([0,-45,0]) {
			translate([0,0,25]) color([0.8,0.8,0.8]) %difference() {
				bcube([90,70,50],cr=10,cres=10);
				cube([200,5,200],center=true);
			}
			translate([0,0,90-5]) color([0.95,0.95,0.95]) %cylinder(r=26,h=30,$fn=60);
			translate([0,0,90-10]) color([0.95,0.95,0.95]) %cylinder(r=10/2,h=5,$fn=60);
			translate([0,0,-10]) color([0.6,0.6,0.6]) %cylinder(r=26,h=90,$fn=60);
			translate([0,0,-40]) color([0.9,0.9,0.9]) %cylinder(r=15/2,h=40,$fn=60);
			translate([0,0,-50]) color([0.4,0.4,0.4]) %cylinder(r=20/2,h=10,$fn=60);
			translate([0,0,-50-20]) color([0.9,0.9,0.9]) %cylinder(r1=1/2,r2=3/2,h=20,$fn=60);
		}
	}
}
