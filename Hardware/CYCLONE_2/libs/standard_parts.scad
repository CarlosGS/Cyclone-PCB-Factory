// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

use <obiscad/obiscad/bcube.scad>
use <MCAD/metric_fastners.scad>

/*Oak = [0.65, 0.5, 0.4];*/
/*Pine = [0.85, 0.7, 0.45];*/
/*Birch = [0.9, 0.8, 0.6];*/
/*FiberBoard = [0.7, 0.67, 0.6];*/
/*BlackPaint = [0.2, 0.2, 0.2];*/
/*Iron = [0.36, 0.33, 0.33];*/
/*Steel = [0.65, 0.67, 0.72];*/
/*Stainless = [0.45, 0.43, 0.5];*/
/*Aluminum = [0.77, 0.77, 0.8];*/
/*Brass = [0.88, 0.78, 0.5];*/
/*Transparent = [1, 1, 1, 0.2];*/

// Activate to generate STL for the fully assembled machine
render_all_parts = false;

// Selects if the part is fully rendered or only in preview mode
module renderStandardPart(renderPart) {
	if(renderPart || render_all_parts) children();
	else %children();
}

module standard_paperSheet_A4(t=0.05, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		translate([0,0,t/2])
			color("white") cube([297,210,t], center=true);
	if(echoPart) echo(str("BOM: Paper sheet. A4. Thickness ", t, "mm"));
}

module standard_rod(diam=8, length=10, threaded=true, center=false, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		if(threaded) {
			color(BlackPaint) rotate([-90,0,0]) cylinder(r=diam/2, h=length, center=center);
			if(echoPart) echo(str("BOM: Rod. Threaded. Diameter ", diam, "mm. Length ", length, "mm"));
		} else {
			color(Stainless) rotate([-90,0,0]) cylinder(r=diam/2, h=length, center=center);
			if(echoPart) echo(str("BOM: Rod. Smooth. Diameter ", diam, "mm. Length ", length, "mm"));
		}
}

module rubberFoot(diam=40, thickness=8, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		color(BlackPaint)
			translate([0,0,-thickness])
				cylinder(r=diam/2, h=thickness);
	if(echoPart) echo(str("BOM: Rubber foot. Diameter ", diam, "mm. Thickness ", thickness, "mm"));
}


module beveledBase(size=[100,200,10], radius=10, res=15, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		color("brown")
			translate([0,0,-size.z/2])
				bcube(size, cr=radius, cres=res);
	if(echoPart) echo(str("BOM: Base. Size ", size, "mm"));
}




include <MCAD/nuts_and_bolts.scad>

module hole_for_screw(size=3,length=20,nutDepth=5,nutAddedLen=0,captiveLen=0,tolerance=0.45,rot=0,invert=false, echoPart=false) {
	radius = METRIC_NUT_AC_WIDTHS[size]/2+tolerance;
	height = METRIC_NUT_THICKNESS[size]+tolerance;
	rotate([0,0,invert ? 180 : 0])
	translate([0,invert ? length/2 : -length/2,0]) {
	translate([0,-length/2+height+nutAddedLen+nutDepth-0.01,0])
		scale([1,(height+nutAddedLen)/height,1])
			rotate([90,0,0])
				hull() {
					rotate([0,0,rot]) nutHole(size=size, tolerance=tolerance, proj=-1);
					translate([0,captiveLen,0])
						rotate([0,0,rot]) nutHole(size=size, tolerance=tolerance, proj=-1);
				}
	translate([0,length/2-height+0.01,0]) //TODO (from MCAD): proper screw cap values: instead of "height" will use METRIC_BOLT_CAP_HEIGHTS[size]+tolerance;
		rotate([90,0,0])
			render() boltHole(size=size, length=length-2.6+0.5, tolerance=tolerance, proj=-1);
	}
	if(echoPart) echo(str("BOM: Screw. M", size, ". Length ", length, "mm"));
	if(echoPart) echo(str("BOM: Nut. M", size, "."));
}

module screw_and_nut(size=3,length=20,nutDepth=5,nutAddedLen=0,captiveLen=0,tolerance=0, autoNutOffset=false, rot=0, invert=false, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		color(BlackPaint)
			difference() {
				if(autoNutOffset)
					hole_for_screw(size,length+METRIC_NUT_THICKNESS[size],nutDepth,nutAddedLen,captiveLen,tolerance,rot,invert, echoPart);
				else
					hole_for_screw(size,length,nutDepth,nutAddedLen,captiveLen,tolerance,rot,invert, echoPart);
				translate([0,invert ? -length-METRIC_NUT_THICKNESS[size] : 0,0])
				rotate([0,45,0]) {
					cube([1,1,10],center=true);
					cube([10,1,1],center=true);
				}
			}
}

module nut(size=8, chamfer=false, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		color(Steel)
			flat_nut(size, apply_chamfer=chamfer);
	if(echoPart) {
		if(chamfer)
			echo(str("BOM: Nut. M", size, ". With chamfer."));
		else
			echo(str("BOM: Nut. M", size, "."));
	}
}


module hole_for_nut(size=3,nutAddedLen=0,captiveLen=0,rot=0,tolerance=0.35) {
	radius = METRIC_NUT_AC_WIDTHS[size]/2+tolerance;
	height = METRIC_NUT_THICKNESS[size]+tolerance;
	scale([1,(height+nutAddedLen)/height,1])
		rotate([90,0,0])
			hull() {
				rotate([0,0,rot]) nutHole(size=size, tolerance=tolerance, proj=-1);
				translate([0,captiveLen,0])
					rotate([0,0,rot]) nutHole(size=size, tolerance=tolerance, proj=-1);
			}
}


module screw_single(size=3,length=10,tolerance=0, renderPart=false, echoPart=false) {
	height = METRIC_NUT_THICKNESS[size]+tolerance;
	color(BlackPaint)
	renderStandardPart(renderPart)
	difference() {
	translate([0,-length/2,0]) {
		translate([0,length/2-height+0.01,0]) //TODO (from MCAD): proper screw cap values: instead of "height" will use METRIC_BOLT_CAP_HEIGHTS[size]+tolerance;
			rotate([90,0,0])
				boltHole(size=size, length=length-2.6+0.5, tolerance=tolerance, proj=-1);
		}
		rotate([0,45,0]) {
			cube([1,1,10],center=true);
			cube([10,1,1],center=true);
		}
	}
	if(echoPart) echo(str("BOM: Screw. M", size, ". Length ", length, "mm"));
}

use <MCAD/motors.scad>
include <MCAD/stepper.scad>
module stepperMotor_mount(height, tolerance=0.15, slide_distance=6, sideLen=42.20, slideOut=false, renderPart=false) {
	render() union() {
	linear_extrude(height=height) offset(delta = tolerance, join_type = "round") union() {
		stepper_motor_mount(nema_standard=17, slide_distance=slide_distance, mochup=false);
		if(slideOut) translate([0,50]) square([22,100],center=true);
	}
	if(slideOut)
		translate([0,25,-25]) bcube([sideLen+2*tolerance,sideLen+slide_distance+2*tolerance+50,50],cr=3,cres=10);
	else
		translate([0,0,-25]) bcube([sideLen+2*tolerance,sideLen+slide_distance+2*tolerance,50],cr=3,cres=10);
	}
}

module stepperMotor(screwHeight=10, renderPart=false, echoPart=false) {
	nema_screw_separation = lookup(NemaDistanceBetweenMountingHoles, Nema17);
	realScrewLength = screwHeight+METRIC_NUT_THICKNESS[3];
	echo("BOM:");
	scale([1,1,-1]) renderStandardPart(renderPart) {
		translate([0,0,-1]) motor(Nema17, size=NemaMedium, dualAxis=false);
		translate([nema_screw_separation/2,nema_screw_separation/2,-realScrewLength]) rotate([-90,0,0]) screw_single(size=3,length=realScrewLength+5,echoPart=echoPart);
		translate([nema_screw_separation/2,-nema_screw_separation/2,-realScrewLength]) rotate([-90,0,0]) screw_single(size=3,length=realScrewLength+5,echoPart=echoPart);
		translate([-nema_screw_separation/2,-nema_screw_separation/2,-realScrewLength]) rotate([-90,0,0]) screw_single(size=3,length=realScrewLength+5,echoPart=echoPart);
		//translate([-nema_screw_separation/2,nema_screw_separation/2,-realScrewLength]) rotate([-90,0,0]) screw_single(size=3,length=realScrewLength+5,echoPart=echoPart);
	}
	//if(echoPart) echo(str("BOM: Motor. Nema17")); // The motor library already outputs motor information
}



module motorGear(r=30,h=10,renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		color("lightgreen") cylinder(r=r,h=h)
	if(echoPart) echo(str("BOM: Gear. Motor."));
}

module rodGear(r=30,h=10,renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		color("lightgreen") cylinder(r=r,h=h)
	if(echoPart) echo(str("BOM: Gear. Rod."));
}



use <MCAD/bearing.scad>
module bearingHole(depth=3, thickness=10, model=608, tolerance=1) {
	bearingD = bearingOuterDiameter(model)+tolerance;
	union() {
		cylinder(r=bearingD/2,h=depth);
		translate([0,0,depth-0.01]) cylinder(r1=bearingD/2,r2=bearingD/2-1,h=1.5);
		cylinder(r=bearingD/2-1,h=thickness+0.1);
	}
}

module radialBearing(model=608, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		bearing(model=model, outline=false);
	if(echoPart) echo(str("BOM: Radial bearing. Model ",model));
}

module washer_single(diam=15.8, thickness=1.6, tolerance=0, renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		color(Steel)
			rotate([90,0,0]) translate([0,0,-tolerance])
				difference() {
					cylinder(r=diam/2+tolerance, h=thickness+2*tolerance);
					cylinder(r=diam/4, h=4*thickness, center=true);
				}
	if(echoPart) echo(str("BOM: Washer. Diameter ", diam, "mm. Thickness ", thickness, "mm"));
}




include <linear_bearing.scad>

module linearBearing_single(model="LM8UU", renderPart=false, echoPart=false) {
	renderStandardPart(renderPart)
		linearBearing(model=model);
	if(echoPart) echo(str("BOM: Linear bearing. Model ", model));
}

module linearBearingHole(model="LM8UU", lateralExtension=10, pressureFitTolerance=0.25, lengthExtension=6, holderLength=1.5, tolerance=0.1) {
	linearBearingLength = linearBearing_L(model);
	linearBearingDiameter = linearBearing_D(model);
	
	dimY = linearBearingLength+lengthExtension;
	
	// Hole for linear bearing
	translate([0,linearBearingLength/2,0])
		rotate([90,0,0])
		translate([0,0,-tolerance])
			cylinder(r=linearBearingDiameter/2+tolerance, h=linearBearingLength+2*tolerance);
	// Slot for inserting the bearing
	translate([0,0,-lateralExtension/2])
		cube([linearBearingDiameter-pressureFitTolerance*2,dimY+0.01,lateralExtension+0.01], center=true);
	// Plastic holders to keep the bearing in place
	translate([0,linearBearingLength/2,0])
		hull() {
			translate([0,holderLength,0])
				rotate([90,0,0]) cylinder(r=linearBearingDiameter/2-pressureFitTolerance, h=0.01, center=true);
			rotate([90,0,0]) cylinder(r=linearBearingDiameter/2, h=0.01, center=true);
		}
	scale([1,-1,1]) translate([0,linearBearingLength/2,0])
		hull() {
			translate([0,holderLength,0])
				rotate([90,0,0]) cylinder(r=linearBearingDiameter/2-pressureFitTolerance, h=0.01, center=true);
			rotate([90,0,0]) cylinder(r=linearBearingDiameter/2, h=0.01, center=true);
		}
	rotate([90,0,0]) cylinder(r=linearBearingDiameter/2-pressureFitTolerance, h=dimY+1, center=true);//linearBearingHole(model=linearBearingModel, renderPart=true);
}



module control_board() {
	rotate([0,0,180])
	translate([15,0]) {
		difference() {
			translate([-15,-12.5])
				cube([102.5,64.5,1.6]);
			translate([0,0,5]) rotate([90,0,0]) hole_for_screw(size=3,length=10,nutDepth=0,nutAddedLen=0,captiveLen=0);
			translate([82.5,0,5]) rotate([90,0,0]) hole_for_screw(size=3,length=10,nutDepth=0,nutAddedLen=0,captiveLen=0);
			translate([0,48.5,5]) rotate([90,0,0]) hole_for_screw(size=3,length=10,nutDepth=0,nutAddedLen=0,captiveLen=0);
		}
		%translate([-15,-12.5,1.6])
			color("green") cube([102.5,64.5,15]);
	}
}


module endstop_holder(holes=false, shortNuts=false) {
	boardX = 41;
	boardY = 16.05;
	boardZ = 1.62;
	
	holderX = 29;
	holderY = 8;
	holderZ = 6;
	
	screwWallSep = 2.75;
	
	if(holes) {
		translate([0,0,-boardZ]) {
			// PCB
			cube([boardX,boardY,boardZ+10]);
			// Endstop pins
			translate([6.2,6.5,-3])
				cube([13.5,5,3]);
			// Connector pins
			translate([26.7,3.5,-3])
				cube([3,7.8,3]);
		}
		translate([0,screwWallSep,3]) {
			translate([3.7,0,0])
				rotate([90,0,0])
					hole_for_screw(size=3,length=15,nutDepth=shortNuts?5:0,nutAddedLen=shortNuts?0:5,captiveLen=10,rot=90);
			translate([22.7,0,0])
				rotate([90,0,0])
					hole_for_screw(size=3,length=15,nutDepth=shortNuts?5:0,nutAddedLen=shortNuts?0:5,captiveLen=10,rot=90);
		}
	} else {
		translate([holderX/2,holderY/2,-holderZ/2-boardZ])
			bcube([holderX,holderY,holderZ], cr=2, cres=4);
		// PCB
		color("lightgrey") translate([0,0,-boardZ])
			%cube([boardX,boardY,boardZ]);
		// Endstop
		color("grey") translate([6.8,0,0])
			%cube([12.8,6.5,6.3]);
		color("lightgrey") translate([6.8+12.8-1,0,0])
			rotate([0,0,180+15])
				%cube([12.8,0.2,6.3]);
		// Screws
		translate([0,screwWallSep,3]) {
			translate([3.7,0,0])
				rotate([90,0,0])
					screw_and_nut(size=3,length=10,nutDepth=0, rot=90, echoPart=true);
			translate([22.7,0,0])
				rotate([90,0,0])
					screw_and_nut(size=3,length=10,nutDepth=0, rot=90, echoPart=true);
		}
	}
}


