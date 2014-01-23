//use this to include a build plate visualization in your openSCAD scripts. Very useful for things designed to be edited in Makerbot Customizer

//to use, either include or use <utils/build_plate.scad>

//then just call build_plate(); with the following arguments (also, you have to have a real object in your scene for this to render)

//putting 0 as the first argument will give you a Replicator 2 build plate
//putting 1 as the first argument will give you a Replicator 1 build plate
//putting 2 as the first argument will give you a Thingomatic build plate
//putting 3 as the first argument will give you a manually adjustable build plate (note: if you use this option, you need to specify your build plates X length (in mm) as the second argument and the Y length (in mm) as the third argument. eg. build_plate(3,150,120);)

/*

to give your user control of which build plate they see in Customizer, include the following code:

use <utils/build_plate.scad>

//for display only, doesn't contribute to final object
build_plate_selector = 0; //[0:Replicator 2,1: Replicator,2:Thingomatic,3:Manual]
//when Build Plate Selector is set to "manual" this controls the build plate x dimension
build_plate_manual_x = 100; //[100:400]
//when Build Plate Selector is set to "manual" this controls the build plate y dimension
build_plate_manual_y = 100; //[100:400]

build_plate(build_plate_selector,build_plate_manual_x,build_plate_manual_y);

*/




//to see how this works, uncomment the following code

//build_plate_selector = 0; //[0:Replicator 2,1: Replicator,2:Thingomatic,3:Manual]
//build_plate_manual_x = 100; //[100:400]
//build_plate_manual_y = 100; //[100:400]
//
//build_plate(build_plate_selector,build_plate_manual_x,build_plate_manual_y);
//
//cube(5);


module build_plate(bp,manX,manY){

		translate([0,0,-.52]){
			if(bp == 0){
				%cube([285,153,1],center = true);
			}
			if(bp == 1){
				%cube([225,145,1],center = true);
			}
			if(bp == 2){
				%cube([120,120,1],center = true);
			}
			if(bp == 3){
				%cube([manX,manY,1],center = true);
			}
		
		}
		translate([0,0,-.5]){
			if(bp == 0){
				for(i = [-14:14]){
					translate([i*10,0,0])
					%cube([.5,153,1.01],center = true);
				}
				for(i = [-7:7]){
					translate([0,i*10,0])
					%cube([285,.5,1.01],center = true);
				}	
			}
			if(bp == 1){
				for(i = [-11:11]){
					translate([i*10,0,0])
						%cube([.5,145,1.01],center = true);
				}
				for(i = [-7:7]){
					translate([0,i*10,0])
						%cube([225,.5,1.01],center = true);
				}
			}
			if(bp == 2){
				for(i = [-6:6]){
					translate([i*10,0,0])
						%cube([.5,120,1.01],center = true);
				}
				for(i = [-6:6]){
					translate([0,i*10,0])
						%cube([120,.5,1.01],center = true);
				}
			}
			if(bp == 3){
				for(i = [-(floor(manX/20)):floor(manX/20)]){
					translate([i*10,0,0])
						%cube([.5,manY,1.01],center = true);
				}
				for(i = [-(floor(manY/20)):floor(manY/20)]){
					translate([0,i*10,0])
						%cube([manX,.5,1.01],center = true);
				}
			}
		}
}