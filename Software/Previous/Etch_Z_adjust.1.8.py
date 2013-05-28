#!/usr/bin/python

# This code is from http://www.cnczone.com/forums/pcb_milling/82628-cheap_simple_height-probing.html

# sudo apt-get install python-tk

##  Introduction
#     This code when run will ask you: 
#     (1) what units your file uses (inch or mm)
#     (2) how many steps you want your probe gride to have on the X axis
#     (3) how many steps you want your probe gride to have on the Y axis
#     (4) which PCB G code file you want to etch

#     It then gets your mill to probe a grid on a blank PCB based on your spacing
#     It stores the probe Z values to memory, then uses those Z values to adjust Z heights for etch moves along the now well probed PCB.
#     You can reuse the generated file again and again as it will always start out by re-probing the surface before etching. 
#     It is based on a neat idea by Poul-Henning Kamp. See: http://phk.freebsd.dk/CncPcb/index.html

##  Where the output is saved
#     The output is saved to a new file where 
#     file_out_name = file_in_name + file_name_suffix, 
#     and the default file out suffix (which you could change by modifying the code) is "_Zadj_[grid size].ngc"
#     Finally, and this is very handy if you are running the Python code in EMC2, it outputs the file to the screen, and you are ready to roll.
#     You can always comment out the print line if you don't need it.

##  What it doesn't do
#     It doesn't reject spurious probe values - you need to make sure the PCB blank you use is clean and free of debris
#     It doesn't optimise X Y paths (you could use opti_qt.exe to do this first - see http://pcbgcode.org/read.php?6,5,5)) 
#     It doesn't optimise X Y moves between drills (Opti_qt can do this for 'simple drill moves', Gopt is apparently better for multiple drill sizes)
#     It doesn't adjust Z heights during arc etching (G02 and G03 moves) - this should not be a problem if arcs have a diameter of less than 10mm.
#     Feel free to address any of these issues!

##  How it works
#     This Python code parses your selected G code file and looks at every etch move: G01 Xaa Ybb Zcc Fdd, where Z is greater than -0.5 
#     It ignores milling and drilling moves ie where Z is deeper than -0.5mm.  
#     It finds the max and min values of X and Y from amongst the file's etch moves.
  
#     It then generates a custom G code routine that will probe a grid that encompasses those max and min X and Y values. 
#     The probe points are spaced by the selected grid spacing, and the Z values at each probe point are stored in memory. 

#     It generates a G code subroutine that will draw on the stored probe data and does the etching on the PCB at the adjusted heights. 
#     For long etch moves it puts in a way point at a distance of half the X grid spacing and calculates a new etch depth for each way point 
#     as it goes along.

#     All the etch moves in the original file(ie G01 Xaa Ybb Zcc Fdd (where Z is greater than -0.5) are then replaced by a subroutine call
#        in the format O200 sub [x_start] [y_start] [aa] [bb]  (where O200 is the etch subroutine referred to above)

# You can change the defaults a little further down

##  For ease of use you may want to change the default start up directory here:

# UNITLESS DEFAULTS: These values are not unit sensitive (and you can change these here too)
# Remember in EMC you can probe up to 4000 points, in Mach3 up to 1000
initial_directory = '/home/'
X_grid_lines      =  10
Y_grid_lines      =   5
units = "mm"
grid_def = "step size"
file_in_name = initial_directory
  
def Unit_set():
    global units,units_G_code,G_dest, X_dest,Y_dest,Z_dest,etch_definition,etch_speed,probe_speed,z_safety,z_probe
    global etch_depth,etch_max,etch_min,z_trivial,z_probe_detach,grid_clearance,step_size,step_max,step_min
    global X_grid_lines,Y_grid_lines,grid_max,grid_min,grid_def

       # INCH DEFAULTS: if units are inches, set the defaults in inches (you can change these here)
    if units == "inch": 
        units_G_code      =    20
        G_dest            =   '00'
        X_dest            = -3.000
        Y_dest            =  2.000
        Z_dest            =  2.000
        etch_definition   = -0.020
        etch_speed        =  4.000
        probe_speed       =  0.400
        z_safety          =  0.150  
        z_probe           = -0.150
        etch_depth        =  0.004
        etch_max          =  0.020 
        z_trivial         =  0.001
        z_probe_detach    =  2.000
        grid_clearance    =  0.001
        step_size         =  0.400

        # MM DEFAULTS: if units are mm, set the defaults in mm (you can change these here too)
    elif units == "mm": 
        units_G_code      =    21
        G_dest            =   '00'
        X_dest            = -80.00
        Y_dest            =  40.00
        Z_dest            =  40.00
        etch_definition   =  -0.50
        etch_speed        = 120.00
        probe_speed       =  25.00
        z_safety          =   1.00  
        z_probe           =  -1.00
        etch_depth        =   0.10
        etch_max          =   0.50
        z_trivial         =   0.02
        z_probe_detach    =  40.00
        grid_clearance    =   0.01
        step_size         =  10.00

def Unit_sel():
    global units, G_dest, X_dest,Y_dest,Z_dest,etch_definition,etch_speed,probe_speed,z_safety,z_probe
    global etch_depth,etch_max,etch_min,z_trivial,z_probe_detach,grid_clearance,step_size,step_max,step_min
    global X_grid_lines,Y_grid_lines,grid_max,grid_min,grid_def, file_in_name
    
    units = get_units.get()
    Unit_set()
    
    # Refresh the defaults in the display
    RB_step.config(text = "grid step size (" + units + ")")
    L_etch_depth.config(text = "Etch depth (" + units + "):")
    Ent_etch_depth.delete(0, END)
    Ent_etch_depth.insert(0, etch_depth)
    Ent_step.config(state=NORMAL)
    Ent_step.delete(0, END)
    Ent_step.insert(0, step_size)
    if get_grid_def.get() == "grid lines":
        Ent_step.config(state=DISABLED)
  
def Def_sel():
    grid_def = get_grid_def.get()
    if grid_def == "step size":
        Ent_X.config(state=DISABLED)
        Ent_Y.config(state=DISABLED)
        Ent_step.config(state=NORMAL)
    
    elif grid_def == "grid lines":
        Ent_X.config(state=NORMAL)
        Ent_Y.config(state=NORMAL)
        Ent_step.config(state=DISABLED)
        Ent_X.delete(0, END)
        Ent_X.insert(0, X_grid_lines)
        Ent_Y.delete(0, END)
        Ent_Y.insert(0, Y_grid_lines)        

def Browse():
    global file_in_name
    import tkFileDialog
    file_in_name = tkFileDialog.askopenfilename(parent=top,initialdir=initial_directory,
                                        filetypes= [('nc files', '*.ngc'),('nc files', '*.nc')],title='Choose file to import:')
    L_file_in_name.config(text = file_in_name)

def OK() : top.destroy()

# Entry validation functions
def IntCheck(new_string) :
    if new_string == "": new_string = "0"
    try:
        v = int(new_string)
        if v > 99 or v < 0: return False
        return True
            # True means accept the new string
    except ValueError:
        return False
            # False means don't accept it

def EtchCheck(new_string) :
    global etch_max
    if new_string == "": new_string = "0"
    try:
        v = float(new_string)
        if v > etch_max or v < 0: return False
        if len(new_string) > 6 : return False
        return True        
    except ValueError:
        return False
            # False means don't accept it

def StepCheck(new_string) :
    if new_string == "": new_string = "0"
    try:
        v = float(new_string)
        if v < 0: return False
        if len(new_string) > 6 : return False
        return True
            # True means accept the new string
    except ValueError:
        return False
            # False means don't accept it

def get_num(line,char_ptr,num_chars):
    char_ptr=char_ptr+1
    numstr = ''
    good   = '-.0123456789'  
    while char_ptr < num_chars:
        digit = line[char_ptr]
        if good.find(digit) != -1:
           numstr = numstr + digit
           char_ptr = char_ptr + 1
        else: break    
    return numstr

def test_X(X_min, X_max):
    if X_dest < X_min : X_min = X_dest
    elif X_dest > X_max : X_max = X_dest
    return X_min, X_max

def test_Y(Y_min, Y_max):
    if Y_dest < Y_min : Y_min = Y_dest
    elif Y_dest > Y_max : Y_max = Y_dest
    return Y_min, Y_max
            
from Tkinter import *
## Don't change these ...
file_in  = []
file_out = []
intro    = []
numstr   = ''
char     = ''

Unit_set()
top = Tk()
top.title("Etch_Z_adjust setup")

# Define the Tkinter variables
get_units       = StringVar()
get_grid_def    = StringVar()
get_X           = IntVar()
get_Y           = IntVar()
get_step        = DoubleVar()
get_etch        = DoubleVar()
get_file_in     = StringVar()

# define the label, radiobutton, button and entry widgets:
# Label widgets:
L_blank1        = Label(top, text="")
L_blank2        = Label(top, text="")
L_blank3        = Label(top, text="")                       
L_blank4        = Label(top, text="")
L_blank5        = Label(top, text="")    
L_units         = Label(top, text="Units to use:")
L_grid_def      = Label(top, text="Define grid by:")
L_X_eq          = Label(top, text="X  = ")
L_Y_eq          = Label(top, text="Y  = ")
L_etch_depth    = Label(top, text="Etch depth:")
L_file_in_quest = Label(top, text="File to import:")
L_file_in_name  = Label(top, text="")

# Radiobutton widgets:
RB_inch         = Radiobutton(top, padx=45, text="inch",                 variable=get_units,    value="inch",       command=Unit_sel)
RB_mm           = Radiobutton(top, padx=45, text="millimetre",           variable=get_units,    value="mm",         command=Unit_sel)
RB_lines        = Radiobutton(top, padx=45, text="number of grid lines", variable=get_grid_def, value="grid lines", command=Def_sel)
RB_step         = Radiobutton(top, padx=45, text="grid step size",       variable=get_grid_def, value="step size",  command=Def_sel)

# Button widgets:
B_browse        = Button(top, text ="Browse...", command = Browse)
B_cancel        = Button(top, text ="CANCEL",    command = OK)
B_OK            = Button(top, text ="OK",        command = OK)

# Entry widgets with ***validation***

# top.register(func_name) gives a number that when called by validatecommand as a command
# enables validatecommand to pass Tk % parameters to the function called eg func_name. 
# ' %P' (the space is important) is the string value in the Entry widget that would result if the edit was allowed.
# See http://www.tcl.tk/man/tcl8.4/TkCmd/entry.htm#M16 for a list of these % parameters.

val_int  = top.register(IntCheck)
val_etch = top.register(EtchCheck)
val_step = top.register(StepCheck)

Ent_X           = Entry(master=top, width = 2,  textvariable = get_X,
                        validate = "key", validatecommand = val_int + ' %P')
Ent_Y           = Entry(master=top, width = 2,  textvariable = get_Y,
                        validate = "key", validatecommand = val_int + ' %P')
Ent_step        = Entry(master=top, width = 6,  textvariable = get_step,
                        validate = "key", validatecommand = val_step + ' %P')
Ent_etch_depth  = Entry(master=top, width = 6,  textvariable = get_etch,
                        validate = "key", validatecommand = val_etch + ' %P ')
Ent_file_in     = Entry(master=top, width = 70, textvariable =  get_file_in, justify = RIGHT, state = DISABLED)  


# lay out the widgets:
L_file_in_quest.grid(row=0, column=0)
B_browse.grid       (row=0, column=1)
L_file_in_name.grid (row=1, column=0, columnspan = 7)
L_blank5.grid       (row=2, column=0, columnspan = 7)

L_units.grid        (row=3, column=0, sticky=W, padx = 25)
RB_mm.grid          (row=4, column=0, sticky=W)
RB_inch.grid        (row=5, column=0, sticky=W)
L_blank2.grid       (row=6, column=0)

L_etch_depth.grid   (row=7, column=0, sticky=W, padx = 25)
Ent_etch_depth.grid (row=7, column=1, sticky=W)
L_blank3.grid       (row=8, column=1)

L_grid_def.grid     (row=3, column=1, sticky=W, padx = 25)
RB_step.grid        (row=4, column=1, sticky=W)
Ent_step.grid       (row=4, column=2, sticky=W)

RB_lines.grid       (row=5, column=1, sticky=W)
L_X_eq.grid         (row=6, column=1, sticky=E)
Ent_X.grid          (row=6, column=2, sticky=W)
L_Y_eq.grid         (row=7, column=1, sticky=E)
Ent_Y.grid          (row=7, column=2, sticky=W)


B_cancel.grid       (row=11, column=0)
B_OK.grid           (row=11, column=1)
L_blank4.grid       (row=12, column=1)

# set the initial units to mm 
RB_mm.select()
Unit_sel()

# set the initial grid definition to step size
RB_step.select()
Def_sel()

top.mainloop()

units        = get_units.get()
grid_def     = get_grid_def.get()
step_size    = get_step.get()
etch_depth   = - get_etch.get()
X_grid_lines = get_X.get()
Y_grid_lines = get_Y.get()

# read in G code file
if file_in_name != None:   
    f = open(file_in_name, 'r')
    for line in f:
        file_in.append(line)
    f.close()

# Check for max and min values in your ngc file
is_first_X = True
is_first_Y = True
is_first_Z = True

# check each line
line_ptr=0
num_lines=len(file_in)
while line_ptr < num_lines:
    line = file_in[line_ptr]
    X_start = X_dest
    Y_start = Y_dest
    Z_start = Z_dest
    
# check each character
    char_ptr = 0
    num_chars= len(line)
    while char_ptr < num_chars:
        char = line[char_ptr]      
        if '(;'.find(char) != -1:
            break              
        elif char == 'G' :
            G_dest = get_num(line,char_ptr,num_chars)   
        elif char == 'X' :
            X_dest = float(get_num(line,char_ptr,num_chars))
        elif char == 'Y' :
            Y_dest = float(get_num(line,char_ptr,num_chars))
        elif char == 'Z' :
            Z_dest = float(get_num(line,char_ptr,num_chars))
        char_ptr = char_ptr + 1
        
    # if the line is an etch move, then replace the line with an etch call        
    if G_dest == '01' and Z_dest > etch_definition:

        line = 'O200 call [%.4f] [%.4f] [%.4f] [%.4f]\n' % (X_start, Y_start, X_dest, Y_dest)

        # and now check for max and min X and Y values
        if is_first_X == True :
            X_min = X_dest
            X_max = X_dest
            is_first_X = False
        else : (X_min, X_max) = test_X(X_min, X_max)

        if is_first_Y == True :
            Y_min = Y_dest
            Y_max = Y_dest
            is_first_Y = False
        else : (Y_min, Y_max) = test_Y(Y_min, Y_max)
         
    file_out.append(line)
    line_ptr=line_ptr+1

if is_first_X == False :

    # then there were etch moves so get to work!

    # first stretch the X and Y max and min values a _tiny_ amount so the grid is just outside all the etch points
    X_min = X_min - grid_clearance
    X_max = X_max + grid_clearance
    Y_min = Y_min - grid_clearance
    Y_max = Y_max + grid_clearance    

    # Use max and min values for the etch moves to work out the probe grid dimensions
    X_span = X_max - X_min
    X_grid_origin = X_min 
    Y_span = Y_max - Y_min
    Y_grid_origin = Y_min

    # Now work out the X and Y step sizes
    if grid_def == "step size" :  
        X_grid_lines = 2 + int(X_span/step_size)
        Y_grid_lines = 2 + int(Y_span/step_size)
        
    # Make sure grid lines are at least 2 
    if X_grid_lines < 2 : X_grid_lines = 2
    if Y_grid_lines < 2 : Y_grid_lines = 2
    
    Y_step_size = Y_span / (Y_grid_lines - 1)
    X_step_size = X_span / (X_grid_lines - 1)

    # Now we can name the output file
    file_name_suffix = "_Zadj_%dx%d.ngc" % (X_grid_lines, Y_grid_lines)
    n = file_in_name.rfind(".")
    if n != -1:
        file_out_name = file_in_name[0:n] + file_name_suffix
    else: file_out_name = file_in_name + file_name_suffix

    # OK now output the G code intro (probe subroutine + etch subroutine + customised grid code)
    from time import localtime, strftime
    line = "(imported from   " + file_in_name + " at " + strftime("%I:%M %p on %d %b %Y", localtime())+ ")\n"
    intro.append(line)
    line = "(output saved as " + file_out_name + ")\n\n"
    intro.append(line)
    line =  "(G code configuration section)\n(you can change these values in the python code or in the G code output:)\n"
    intro.append(line)
    line = ("G%2d (" + units + ")\n") % (units_G_code)
    intro.append(line)
    line = "#<_etch_speed>    =  %.4f \n" % (etch_speed)
    intro.append(line)
    line = "#<_probe_speed>   =   %.4f \n" % (probe_speed)
    intro.append(line)
    line = "#<_z_safety>      =    %.4f \n" % (z_safety)
    intro.append(line)
    line = "#<_z_probe>       =   %.4f \n" % (z_probe)
    intro.append(line)
    line = "#<_etch_depth>    =   %.4f \n\n" % (etch_depth)
    intro.append(line)
    line = "(Don't change these values here, they were calculated earlier)\n"
    intro.append(line)
    line =  '#<_x_grid_origin> =  %.4f \n' % (X_grid_origin) 
    intro.append(line )
    line =  '#<_x_grid_lines>  =    %.4f \n' % (X_grid_lines )
    intro.append(line)
    line =  '#<_y_grid_origin> =    %.4f \n' % (Y_grid_origin)
    intro.append(line)
    line =  '#<_y_grid_lines>  =    %.4f \n' % (Y_grid_lines )
    intro.append(line)
    line =  '#<_x_step_size>   =    %.4f \n' % (X_step_size)  
    intro.append(line)
    line =  '#<_y_step_size>   =    %.4f \n' % (Y_step_size)  
    intro.append(line)

    line =  """#<_last_z_etch>   =   #<_etch_depth>

    O100 sub (probe subroutine)
         G00 X [#<_x_grid_origin> + #<_x_step_size>*#<_grid_x>]   
         G38.2 Z#<_z_probe> F#<_probe_speed>   
         #[1000 + #<_grid_x> + #<_grid_y> * #<_x_grid_lines>] = #5063   
         G00 Z#<_z_safety>
    O100 endsub

    O200 sub (etch subroutine)
         ( This subroutine calculates way points on the way to x_dest, y_dest, )
         ( and calculates the Z adjustment at each way point.                  )
         ( It moves to each way point using the etch level and etch speed set  )
         ( in the configuration section above.                                 )

         #<x_start>         = #1
         #<y_start>         = #2
         #<x_dest>          = #3
         #<y_dest>          = #4
         #<distance>        = sqrt[ [#<x_dest> - #<x_start>]**2 + [#<y_dest> - #<y_start>]**2 ]
         #<waypoint_number> = fix[#<distance> / [#<_x_step_size>/2]]
         #<x_step>          = [[#<x_dest> - #<x_start>] / [#<waypoint_number> + 1]]
         #<y_step>          = [[#<y_dest> - #<y_start>] / [#<waypoint_number> + 1]]
         
         O201 while [#<waypoint_number> ge 0]
              #<_x_way>     =  [#<x_dest> - #<waypoint_number> * #<x_step>]
              #<_y_way>     =  [#<y_dest> - #<waypoint_number> * #<y_step>]   
              #<_grid_x_w>  =  [[#<_x_way> - #<_x_grid_origin>]/#<_x_step_size>]
              #<_grid_y_w>  =  [[#<_y_way> - #<_y_grid_origin>]/#<_y_step_size>]
              #<_grid_x_0>  =  fix[#<_grid_x_w>]
              #<_grid_y_0>  =  fix[#<_grid_y_w>]
              #<_grid_x_1>  =  fup[#<_grid_x_w>]
              #<_grid_y_1>  =  fup[#<_grid_y_w>]
              #<_cell_x_w>  =  [#<_grid_x_w> - #<_grid_x_0>]
              #<_cell_y_w>  =  [#<_grid_y_w> - #<_grid_y_0>]

              (Bilinear interpolation equations from http://en.wikipedia.org/wiki/Bilinear_interpolation)
              #<F00>        =  #[1000 + #<_grid_x_0> + #<_grid_y_0> * #<_x_grid_lines>]
              #<F01>        =  #[1000 + #<_grid_x_0> + #<_grid_y_1> * #<_x_grid_lines>]
              #<F10>        =  #[1000 + #<_grid_x_1> + #<_grid_y_0> * #<_x_grid_lines>]
              #<F11>        =  #[1000 + #<_grid_x_1> + #<_grid_y_1> * #<_x_grid_lines>] 
              #<b1>         =  #<F00>
              #<b2>         =  [#<F10> - #<F00>]
              #<b3>         =  [#<F01> - #<F00>]
              #<b4>         =  [#<F00> - #<F10> - #<F01> + #<F11>]          
              #<z_adj>      =  [#<b1> + #<b2>*#<_cell_x_w> + #<b3>*#<_cell_y_w> + #<b4>*#<_cell_x_w>*#<_cell_y_w>]
              #<z_etch>     =  [#<_etch_depth> + #<z_adj>]
                       
              (ignore trivial z axis moves)
              """
    intro.append(line)
    line = "O202 if [abs[#<z_etch> - #<_last_z_etch> ] lt %.4f]" % (z_trivial)
    intro.append(line)
    line = """
                   #<z_etch> = #<_last_z_etch> 
              O202 else
                   #<_last_z_etch> = #<z_etch>
              O202 endif
              
              (now do the move)
              G01 X#<_x_way>  Y#<_y_way>  Z[#<z_etch>] F[#<_etch_speed>]
              
              (and then go to the next way point)
              #<waypoint_number> = [#<waypoint_number> - 1]         
         O201 endwhile
    O200 endsub

    ( Probe section                                                 )
    ( This section probes the grid and writes the probe results     )
    ( sequentially to variables #1000, #1001, #1002 etc etc         )
    ( such that the result at x,y on the grid is stored in          )
    (               #[1000 + x + y*[x_grid_lines]]                  )

    ( You'll run out of memory if you probe more than 4,000 points! ) 

    #<_grid_x> = 0
    #<_grid_y> = 0

    G00 Z#<_z_safety>
    G00 X#<_x_grid_origin> Y#<_y_grid_origin>
    O001 while [#<_grid_y> lt #<_y_grid_lines>]
         G00 Y[#<_y_grid_origin> + #<_y_step_size> * #<_grid_y>]    
         O002 if [[#<_grid_y> / 2] - fix[#<_grid_y> / 2] eq 0]
              #<_grid_x> = 0
              O003 while [#<_grid_x> lt #<_x_grid_lines>]
                   O100 call (probe subroutine)
                   #<_grid_x> = [#<_grid_x> + 1]
              O003 endwhile       
         O002 else 
              #<_grid_x> = #<_x_grid_lines>
              O004 while [#<_grid_x> gt 0]
                   #<_grid_x> = [#<_grid_x> - 1]  
                   O100 call (probe subroutine)  
              O004 endwhile
         O002 endif
         #<_grid_y> = [#<_grid_y> + 1]
    O001 endwhile
    """
    intro.append(line)
    line = "G00 Z%.4f \n" % (z_probe_detach)
    intro.append(line)
    line = """
    ( Main ngc program section                                                          )
    ( Python has replaced all G01 etch moves from original file eg G01 Xaa Ybb Zcc Fdd  )
    ( with an adjusted etch move in the format O200 sub [x_start] [y_start] [aa] [bb]   )
    ( O200 is the etch subroutine                                                       )

    (MSG, OK folks - power up the mill...)

    M00

    """
    intro.append(line)

    # create and then save the output file
    file_out = intro + file_out

    f = open(file_out_name, 'w')
    for line in file_out:
        f.write(line)
    f.close()


    # now output the altered ngc file to the screen
    for line in file_out:
        print line,
    
else:
    from Tkinter import *
    def OK() : top.destroy()

    top = Tk()
    top.title("   Check file")
    var = IntVar()

    L1 = Label(top, text="")
    L2 = Label(top, text="Sorry, no etch moves found in that file.", font = "12")
    L3 = Label(top, text="")
    L4 = Label(top, text="Check file name, units, etch move definition etc.", font = "12")
    L5 = Label(top, text="")
    L6 = Label(top, text="")
    B1 = Button(top, text ="OK", command = OK, font = "18")

    L1.pack()
    L2.pack(anchor = W, padx=45)
    L3.pack()
    L4.pack(anchor = W, padx=45)
    L5.pack()    
    B1.pack()
    L6.pack()
    top.mainloop()
  
    
