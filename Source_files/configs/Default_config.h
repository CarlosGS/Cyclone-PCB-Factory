// This file is part of Cyclone PCB Factory: an open-source 3D printable CNC machine for PCB manufacture
// http://reprap.org/wiki/Cyclone_PCB_Factory
// Original author: Carlosgs (http://carlosgs.es)
// License: CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International, http://creativecommons.org/licenses/by-sa/4.0/)
// Designed with http://www.openscad.org/

// Default machine config file


// --- Size parameters ---

	// --- Bottom base ---
		base_size_X			= 304.8 + animatePart(1,overlap=0);
		base_size_Y			= 261.62 + animatePart(2);
		base_thickness		= 8;
		base_corner_radius	= 20;
		base_corner_res		= 0;
		foot_offset = 25;
		
	// --- Axes reference position ---
	// Note: The reference coordinates are centred like this:
	// Y axis reference is the Y smooth rod end, BACK of RIGHT FRAME
	// X axis reference is the frontal X smooth rod end, RIGHT FRAME
	// Z axis reference is the Z threaded rod, at the height of the Z nut, and relative to the X reference
		axes_Yreference_height	= 40 + animatePart(5);
		axes_Xreference_height	= 74 + animatePart(6); // relative to Y reference
		axes_Zreference_height	= -3 + animatePart(7) + animatePart(9); // relative to X reference

		axes_Xreference_posY	= -81-animatePart(8)-animatePart(9); // relative to Y reference. Moves the X axis towards the front of the machine
		axes_Zreference_posY	= 14; // relative to X reference. Positions Z rods between the Y rods

		axes_Y_threaded_height = 30 + animatePart(5);

		axes_Ysmooth_separation	= 165 + animatePart(1,overlap=0);
		axes_Xsmooth_separation = 40 + animatePart(9);
		axes_Zsmooth_separation = 40 + animatePart(10,overlap=0);

		
	// --- Work bed ---
		Ycarriage_linearBearingSeparation = 50;
		workbed_size_X			= axes_Ysmooth_separation+50;
		workbed_size_Y			= Ycarriage_linearBearingSeparation+70;
		workbed_thickness		= 8+3;
		workbed_separation_from_Y_smooth_rod = 10;
		PCBholder_height = 10;
		PCB_dimX = 160;
		PCB_dimY = 100;
		PCB_dimZ = 1.6;
		PCB_holder_edge_length = 3;
		
	// --- Z carriage ---
	  Z_carriage_wall_thickness = 9;
	  Z_carriage_wall_width = 54;		
		
  // --- X frames ---
	  X_frames_additional_thickness = 5;
		X_frame_footThickness = 10;
		X_frame_corner_radius = 10;
		X_frame_FrontalThickness = 15;
		X_backlash_armThickness = 30;
		X_motorWallSeparation = 5;
		X_motorRotatedOffset = 5;
		X_gearWallSeparation = 5;
		
  // --- Y frames ---
		Y_frame_footThickness = 10;
		Y_motorWallSeparation = 5;
		Y_motorRotatedOffset = 5;
		Y_gearWallSeparation = 5;
		Y_foot_additional_separation = 5;
		Y_endstopHolderRotation = 5;
		Logo = true; // Add logo to the Y Smooth Rod Idlers
		
	// --- Axes sizes ---
	// *_rodLen = length
	// *_rodD = diameter
		// Y smooth rod
			axes_Ysmooth_rodLen	= 210 + animatePart(2);
			axes_Ysmooth_rodD	= 8.5 + animatePart(4,dist=5);
		// Y threaded rod
			axes_Ythreaded_rodLen	= axes_Ysmooth_rodLen-10;
			axes_Ythreaded_rodD	= 8.5 + animatePart(4,dist=5);
		// X smooth rod
			axes_Xsmooth_rodLen	= 250 + animatePart(1,overlap=0);
			axes_Xsmooth_rodD	= 8.5 + animatePart(4,dist=5);
		// X threaded rod
			axes_Xthreaded_rodLen	= axes_Xsmooth_rodLen+50;
			axes_Xthreaded_rodD	= 8.5 + animatePart(4,dist=5);
		// Z smooth rod
			axes_Zsmooth_rodLen	= 110 + animatePart(3);
			axes_Zsmooth_rodD	= 8.2 + animatePart(4,dist=5);
		// Z threaded rod
			axes_Zthreaded_rodLen	= 90;
			axes_Zthreaded_rodD	= 8.5 + animatePart(4,dist=5);
			
	// --- Bearings ---
		Y_linearBearingModel = "LM8UU";
		X_linearBearingModel = "LM8UU";
		X_linearBearingSeparation = 0;
		Z_linearBearingModel = "LM8UU";
		Z_threaded_rodBearingModel = 608;
		Y_threaded_rodBearingModel = 608;
		Y_threaded_rodBearingDepth = 3;
		X_threaded_rodBearingModel = 608;
		X_threaded_rod_bearingDepth = 3;
		
	// --- Steppers ---
		//Y_motorModel = Nema17;
		//X_motorModel = Nema17;
		//Z_motorModel = Nema17;
		Z_motor_adjust_margin = 5;

	// --- Screw sizes --- 
	// M3, M4, etc (integers only), at the moment only M3 and M4 will work.
		Y_frontFrame_footScrewSize = 3;
		Y_backFrame_footScrewSize = 3;
		Y_rightSmoothRodIdler_footScrewSize = 3;
		X_Frame_footScrewSize = 3;

		Y_threaded_rodNutSize = 8;
		X_threaded_rodNutSize = 8;
		Z_threaded_rodNutSize = 8;
		
		Y_nutHolder_screwSize = 3;
		Y_singleLinearBearingHolder_screwSize = 3;
		Y_PCBholder_screwSize = 3;
		
		Y_backlash_washer_D = 15.8;
	  Y_backlash_washer_thickness = 1.6;
		X_backlash_washer_D = 15.8-0.5;
		X_backlash_washer_thickness = 1.6-0.9;

		X_carriage_screwSize = 3;

		Y_rightSmoothRodIdler_rodScrewSize = 3;
		X_Frame_rodScrewSize = 3;
		
		spindle_holder_screwSize = 3;
		
	// --- Gears ---
		axes_XgearSeparation = 37;
	  X_rodGearRatio = 21; // Number of tooth
		X_motorGearRatio = 21; // Number of tooth
		X_gear_thickness = 10;
		Z_rodGearRatio = 15; // Number of tooth
		Z_motorGearRatio = 8; // Number of tooth
		Z_gear_thickness = 10;
		axes_YgearSeparation = 37;
		Y_rodGearRatio = 21; // Number of tooth
		Y_motorGearRatio = 21; // Number of tooth
		Y_gear_thickness = 10;
		
	// --- Gear Cover ---
	  gearCover_margin = 4;
		rodGearAddedgearCover_margin = 0;
		gearCover_wallThickness = 0.4*4;
		gearCover_screwHeadSpaceHeight = 4;
		gearCover_screwHeadSpaceDiam = 6;
		gearCoverHeight = 16;
		gearCoverExtraHeight = 5;
		gearCoverExtraRadius = -7;
		gearCover_truncationAngle = 10;
		
	// --- Spindle Motor ---
		spindle_motor_diam_top = 51.3;
		spindle_motor_diam_top_smaller = 47.5;
		spindle_motor_diam = 47.5;
		spindle_motor_sidelen = 32;
		spindle_holder_thickness = 8;
		spindle_motor_length = 90;
		
	// --- Text ---
		textHscale = 0.8;
		textThickness = 1.5;
		topText = "CYCLONE";
		bottomText = "PCB Factory";
		
	// --- Tolerances ---
		Y_threaded_rod_Tolerance = 0.5;
		Y_linearBearing_pressureFitTolerance = 0.5;
		PCB_holder_tolerance = 1;
		axes_Xsmooth_separation_tolerance = 0.5;
		X_threaded_rod_Tolerance = 0.5;
		Z_linearBearingHole_tolerance = 0.5;
		LinearBearingPressureFitTolerance = 0.4;
		screwHoleTolerance = 0.4;
		
		Z_threaded_rod_Tolerance = 0.5;
		
		
// --- Render options ---

	// --- Part colours ---
		blueColor = [0.3,0.6,0.9];
		redColor = [0.8,0.3,0.3];
		yellowColor = [0.9,0.9,0.1];
		blackColor = [0.2,0.2,0.2];
		color_movingPart = yellowColor+[0.1,0.1,0.1];
		color_stillPart = yellowColor;

	// --- DXF output ---
	// Activate/Deactivate rendering auxiliary references (LCS axis, etc)
		draw_references = false; // Show reference axis's
		render_DXF_base = false; // Render bottom base for DXF export
		render_DXF_workbed = false; // Render work bed for DXF export
		render_bases_outline = false; //Toggle for rendering outline DXFs
		DXF_offset = 0.4; //Needed to adjust the tolerance of the laser cutter
		
	// --- Carriage positions ---
		axes_Xcarriage_pos = axes_Xsmooth_rodLen/2+sin($t*360)*axes_Xsmooth_rodLen/3;
		axes_Ycarriage_pos = axes_Ysmooth_rodLen/2+sin($t*360)*axes_Ysmooth_rodLen/4.1;
		axes_Zcarriage_pos = axes_Zsmooth_rodLen/2+sin($t*360)*axes_Zsmooth_rodLen/8;	
		
	// --- Parts ---
		Render_X_leftFrame = true;
		Render_X_rightFrame = true;
		Render_X_carriage = true;
		Render_Z_carriage = true;
		Render_Z_carriageTop = true;
		Render_Z_carriageBottom = true;
		Render_Y_leftSmoothRodIdler = true;
		Render_Y_rightSmoothRodIdler = true;
		Render_Y_frontFrame = true;
		Render_Y_backFrame = true;
		Render_Y_carriage = true;
		Render_control_board = true;
		Render_Y_gearCover = true;
		Render_Y_motorGear = true;
		Render_Y_rodGear = true;
		Render_X_gearCover = true;
		Render_X_motorGear = true;
		Render_X_rodGear = true;
		Render_PCBholderTop = true;
		Render_PCBholderBottom = true;
		Render_YsubPart_linearBearingHolders = true;
		Render_YsubPart_nutHolder = true;
		//Render_rodHolder = true;
		
		alt_XZ_carriage = false;
		
		
