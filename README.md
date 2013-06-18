Cyclone-PCB-Factory v0.9.7  
===================

The first 3D-printable (Rep-Rap alike) CNC machine, intended for PCB manufacture.  

![ScreenShot](https://github.com/carlosgs/Cyclone-PCB-Factory/raw/master/Media/Cyclone_built_v0.9.7.jpg)

Mail list / Forum  
--
If you are interested in this project, please consider joining our mail list:  
**<https://groups.google.com/forum/#!forum/cyclone-pcb-factory>**  

Wiki entry on RepRap.org  
--
<http://reprap.org/wiki/Cyclone_PCB_Factory>  

**To-Do list**  
--  
- **Hardware:**  
 - Reinforce left&right frames  
 - Reinforce screw holders in the Z axis parts  
 - Add Endstop holder files (same of Prusa/Mendel)  
 - Create holder for a vacuum cleaner  
- **Software:**  
 - Export Z probing results to a standarized file  
 - Create a graphical user interface  
 - Fix bug in GcodeParser.py that doesn't mind the depth of the cuts, this affects only when cutting the edges with >1 passes  
- **Firmware:**  
 - Keep motors always on, in order to do homing only once each milling session  
- **Misc:**  
 - Create assembly instructions  

News  
--  
**Hardware**  
- Note: The linear bearings of the X carriage must be glued in place (use epoxy or similar) since vibrations produced by the spindle motor move the bearings out of place.  
- v0.9.7 has an improved Z carriage: uses much less plastic, it holds the spindle tightly and leaves more metal surface exposed for better cooling.  
- v0.9.6b has a robust Y axis motor stand (improvement suggested and tested by **Yopero**), and the Z carriage now shows the name of the machine (how cool is that? :P)  

**Software**  
- Note: The timeout for commands of the edge needs to be increased, since the moves are really slow.  
- First Z probing results are promising, read: <https://plus.google.com/u/0/113437723819360223498/posts/9VCHqqnirj6> and <https://plus.google.com/u/0/113437723819360223498/posts/89W2cv1fgQW>  
- Added the python probing script (v0.1) and Octave/Matlab visualizer  
- Based on PyGerber2Gcode.py script  

**Firmware**  
- No news, it is Marlin with support for G30 probing command  

Interesting links & Misc. ideas  
--
- **Open Source SMT Pick and Place Hardware and Software** <https://github.com/openpnp/openpnp> via **Marcos Villacampa** (@MarkVillacampa)  
- **Water-cooled spindle motors!** <http://www.goodluckbuy.com/electronics/motor-and-controller.html> via **Marcos Villacampa** (@MarkVillacampa)  
- **We could use a thermistor to measure the temperature of the spindle motor:** this way the software could "let it rest" when it gets too hot.  

Videos  
--  
- v0.9.6 Y axis concept by Yopero <http://www.youtube.com/watch?v=XzcobonQP40>  
- v0.9.5 Probing a PCB <http://www.youtube.com/watch?v=m5zXL8k5T9E>  
- v0.9.5 Milling MDF <http://www.youtube.com/watch?v=2QpxjheEjEc> and <http://www.youtube.com/watch?v=zjav0hBtmYA>  
- v0.8 Drawing test: <http://www.youtube.com/watch?v=Y-HSdE89JOM>  
- v0.7.5 XY axis test: <http://www.youtube.com/watch?v=9umlq4oHG64>  
- v0.7.5 High speed XY test: <http://www.youtube.com/watch?v=H3uYCXryj60>  

Bill of materials  
--  
<https://docs.google.com/spreadsheet/ccc?key=0AsQp8IK25R4IdGk3LTdOWmpFR0Nrc0RhaVJaUC1CMUE>  
**TODO:** Add general hardware, motors and electronics to the list.  

Notes  
--  
- Using a thick wood piece as the main base.  
- As shown in one of the pictures, a cheap dremel-like drill has nice bearings and is a good option as the main tool. **Finally it will be using a proper spindle** (check the BOM for the reference).  
- Desired working range of >=100mm for the X axis and >=160mm for the Y axis.  
- Parts are designed to be printable with the small volume of a Printrbot Jr  
- Bed leveling will be done with probing and an appropriate software.  

Software: existing work  
--  
Here is a compilation of links that have inspired the software controller (specifically the Z probing technique):  

- <http://www.re-innovation.co.uk/web12/index.php/en/blog-75/181-making-pcbs-with-a-cnc-machine>  
- <http://phk.freebsd.dk/CncPcb/>  
- <http://wiki.linuxcnc.org/cgi-bin/wiki.pl?Touch_Probe>  
- <http://things.onshoulders.org/software/PcbSubtraction.php>  
- <http://www.cnczone.com/forums/pcb_milling/82628-cheap_simple_height-probing-5.html>  
- <http://drillcity.stores.yahoo.net/>  
- <http://www.drewtronics.net/>  

- **Examples of the PCB probing method**  
 - onshouldersTv: Open Source Circuit Boards at Home <http://www.youtube.com/watch?v=L-5SRtwx3kY>  
 - PCB routing using the Probe method <http://www.youtube.com/watch?v=fwgT9sCL8fs>  
- <http://pcbgcode.org/>  
- <http://sourceforge.net/apps/mediawiki/pcb2gcode/index.php?title=Main_Page>  
- Very interesting toguether with cam.py: <http://code.google.com/p/pygerber2gcode/>  
- <http://replicat.org/generators>  
- For arranging panels: <http://ruggedcircuits.com/gerbmerge/>  

License  
--
License: **Attribution - Share Alike - Creative Commons (<http://creativecommons.org/licenses/by-sa/3.0/>)**  

Authors:  
--
- **Carlosgs (<http://carlosgs.es>)**
- **yOPERO (<http://yopero-tech.blogspot.com.es/>)**

Special thanks  
--  
- Y axis improvement by **yOPERO** <https://github.com/carlosgs/Cyclone-PCB-Factory/pull/1>  
- Z axis concepts by **Quim Borras** and the spindle motor holder by **Misan** were really useful!! Also, **Diego Viejo**'s machine was of great inspiration for the Z axis (<https://plus.google.com/u/0/photos/113930344830086538817/albums/5868944432651911713?authkey=CLDJgdehlN773gE>) **Thank you all!!**  
- This design woudn't have been possible without the encouragement of the **Panda CNC community** (<https://plus.google.com/u/0/communities/102402711800402614517>)  
- Also, thanks to **Obijuan** (<http://iearobotics.com>) for naming the machine Cyclone :)  

Derived from / we have used / inspirational  
--
- "Linear actuator concept for CNC machines" by **Carlosgs** (<http://www.thingiverse.com/thing:45103>)  
- "Parametric openscad beveled cube" by **Obijuan** (<http://www.thingiverse.com/thing:29842>)  
- "Minimal footprint friction-fit LM8UU holder" by **thantik** (<http://www.thingiverse.com/thing:23041>)  
- "Spindle mount for ShapeOko" by **Misan** (<http://www.thingiverse.com/thing:26740>)  
- "Carro Z para Cyclone CNC mill intended for PCB" by **Quim** (<http://www.thingiverse.com/thing:80718>)  
- Write.scad (and DXF fonts) by **HarlanDMii** (<http://www.thingiverse.com/thing:16193>)  
- "PCB Machining Vise" by **Forgetful_Guy** (<http://www.thingiverse.com/thing:63578>)  

Credit for the ideas used  
--  
The origin of Cyclone took place while I was inside the **Panda CNC** community (<https://plus.google.com/u/0/communities/102402711800402614517>). This is from December 2012 to mid-February 2013.  
Here is the credit for the ideas that were used:  

* _Let's design a 3D-printable CNC for PCB milling, it will be named Panda:_ **Guillermo Welch** (mid-December, via Google Talk)  
* _X carriage rod distribution:_ **César Augusto Fernández Cano** claims Cyclone's X axis is a derivate of his concept: <https://plus.google.com/u/0/111421387442355054591/posts/QrfYtEuZBaj>  
* _100x160mm workspace:_ **David Martin** <https://dl.dropboxusercontent.com/u/16122275/PandaCNC_credit/workplace_size.png>  
* _Using gears to drive the X-Y axes:_ **Guillermo Welch** <https://plus.google.com/u/0/101232926728463427403/posts/QjZGNcWcgGg>  
* _Regarding the woodbase:_ **Guillermo Welch** always contemplated the possibility of attaching the machine (optionally) to a woodbase. I decided to use the base as a main structural part instead. See <https://dl.dropboxusercontent.com/u/16122275/PandaCNC_credit/woodbase.png> (screenshot from <https://plus.google.com/u/0/113437723819360223498/posts/8LDCSSVWqCS>)  
* _List of CNC endmill types:_ **David Martin** <https://dl.dropboxusercontent.com/u/16122275/PandaCNC_credit/cnc_endmill_types.png>  

Please note I have taken screenshots of the post that are on the closed G+ Panda community (<https://plus.google.com/u/0/communities/116318709564872967169>). You can register and see by yourself.  

**All other development present on Cyclone has nothing to do with Panda and is not related to the Panda project.**  


Render (v0.9.7)  
--
![ScreenShot](https://github.com/carlosgs/Cyclone-PCB-Factory/raw/master/Media/Cyclone_render_v0.9.7.png)

Disclaimer  
--
This hardware/software is provided "as is", and you use the hardware/software at your own risk. Under nocircumstances shall any author be liable for direct, indirect, special, incidental, or consequential damages resulting from the use, misuse, or inability to use this hardware/software, even if the authors have been advised of the possibility of such damages.  

