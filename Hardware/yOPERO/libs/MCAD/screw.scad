// Parametric screw-like things (ball screws, augers)
// License: GNU GPL 2.0 or later.
// © 2010 by Elmo Mäntynen

include <curves.scad>

/* common screw parameter
length
pitch = length/rotations: the distance between the turns of the thread
outside_diameter
inner_diameter: thickness of the shaft
*/

//Uncomment to see examples
//test_auger();
//test_ball_groove();
//test_ball_groove2();
//test_ball_screw();

module helix(pitch, length, slices=500){
    rotations = length/pitch;
    linear_extrude(height=length, center=false, convexity=10, twist=360*rotations, slices=slices, $fn=100)
        child(0);
}

module auger(pitch, length, outside_diameter, inner_diameter) {
    union(){
        helix(pitch, length)
        polygon(points=[[10,10],[100,1],[100,-1],[10,-10]], paths=[[0,1,2,3]]);
        cylinder(h=length, r=20);
    }
}

module test_auger(){translate([300, 0, 0]) auger(100, 300);}


module ball_groove(pitch, length, diameter, ball_radius=10) {
    helix(pitch, length, slices=100)
        translate([diameter, 0, 0])
        circle(r = ball_radius);
}

module test_ball_groove(){ translate([0, 300, 0]) ball_groove(100, 300, 10);}

module ball_groove2(pitch, length, diameter, ball_radius, slices=200){
    rotations = length/pitch;
    radius=diameter/2;
    offset = length/slices;
    union(){
        for (i = [0:slices]) {
            assign (z = i*offset){
                translate(helix_curve(pitch, radius, z)) sphere(ball_radius, $fa=5, $fs=1);
            }
        }
    }
}

module test_ball_groove2(){translate([0, 0, 0]) ball_groove2(100, 300, 100, 10);}

module ball_screw(pitch, length, bearing_radius=2) {

}

module test_ball_screw(){}
