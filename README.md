Cyclone-PCB-Factory v0.9.6  
===================

The first 3D-printable (Rep-Rap alike) CNC machine, intended for PCB manufacture.

Disclaimer  
--
This hardware/software is provided “as is," and you use the hardware/software at your own risk. Under nocircumstances shall Carlosgs be liable for direct, indirect, special, incidental, or consequential damages resulting from the use, misuse, or inability to use this hardware/software, even if Carlosgs has been advised of the possibility of such damages.  

News:  
--  
**Hardware:**  
* v0.9.6 has a robust Y axis motor stand (improvement suggested and tested by Yopero), and the Z carriage now shows the name of the machine (how cool is that? :P)  

**Software:**  
* First Z probing results are promising, read: https://plus.google.com/u/0/113437723819360223498/posts/9VCHqqnirj6  and https://plus.google.com/u/0/113437723819360223498/posts/89W2cv1fgQW  
* Added the python probing script (v0.1) and Octave/Matlab visualizer  

**Firmware:**  
* No news, it is Marlin with support for G30 probing command  

Videos:  
--  
- v0.9.6 Y axis concept by Yopero http://www.youtube.com/watch?v=XzcobonQP40
- v0.9.5 Probing a PCB http://www.youtube.com/watch?v=m5zXL8k5T9E  
- v0.9.5 Milling MDF http://www.youtube.com/watch?v=2QpxjheEjEc and http://www.youtube.com/watch?v=zjav0hBtmYA  
- v0.8 Drawing test: http://www.youtube.com/watch?v=Y-HSdE89JOM  
- v0.7.5 XY axis test: http://www.youtube.com/watch?v=9umlq4oHG64  
- v0.7.5 High speed XY test: http://www.youtube.com/watch?v=H3uYCXryj60  

Bill of materials:  
--  
https://docs.google.com/spreadsheet/ccc?key=0AsQp8IK25R4IdGk3LTdOWmpFR0Nrc0RhaVJaUC1CMUE  

Notes:  
--  
- Using a thick wood piece as the main base.  
- As shown in one of the pictures, a cheap dremel-like drill has nice bearings and is a good option as the main tool. **Finally it will be using a proper spindle** (check the BOM for the reference).  
- Desired working range of >=100mm for the X axis and >=160mm for the Y axis.  
- Parts are designed to be printable with the small volume of a Printrbot Jr  
- Bed leveling will be done with probing and an appropriate software.  

To-Do list:  
--  
- [99% DONE] Design parts for the X axis (this includes Z axis too, **will be using a proper spindle instead of a hand-drill**)  
- [DONE] Design parts for the Y axis  
- [DONE] Create template for the screws in the wood base  
- Software, testing, milling a PCB (till then, it can't be v1.0 :P)...  

Software  
--  
Here is a compilation of links that I find interesting for the software controller:  

- http://www.re-innovation.co.uk/web12/index.php/en/blog-75/181-making-pcbs-with-a-cnc-machine  
- http://phk.freebsd.dk/CncPcb/  
- http://wiki.linuxcnc.org/cgi-bin/wiki.pl?Touch_Probe  
- http://things.onshoulders.org/software/PcbSubtraction.php  
- http://www.cnczone.com/forums/pcb_milling/82628-cheap_simple_height-probing-5.html  
- http://drillcity.stores.yahoo.net/  
- http://www.drewtronics.net/  

- **Examples of the PCB probing method**  
 - onshouldersTv: Open Source Circuit Boards at Home http://www.youtube.com/watch?v=L-5SRtwx3kY  
 - PCB routing using the Probe method http://www.youtube.com/watch?v=fwgT9sCL8fs  
- http://pcbgcode.org/  
- http://sourceforge.net/apps/mediawiki/pcb2gcode/index.php?title=Main_Page  
- Very interesting toguether with cam.py: http://code.google.com/p/pygerber2gcode/  
- http://replicat.org/generators  
- For arranging panels: http://ruggedcircuits.com/gerbmerge/  

License: CC-BY-SA  
--  
Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/).  

Derived/uses:
--
- "Linear actuator concept for CNC machines" by Carlosgs (http://www.thingiverse.com/thing:45103)  
- "Parametric openscad beveled cube" by Obijuan (http://www.thingiverse.com/thing:29842)  
- "Minimal footprint friction-fit LM8UU holder" by thantik (http://www.thingiverse.com/thing:23041)  
- "Spindle mount for ShapeOko" by Misan (http://www.thingiverse.com/thing:26740)  
- "Carro Z para Cyclone CNC mill intended for PCB" by Quim (http://www.thingiverse.com/thing:80718)  
- Write.scad (and DXF fonts) by HarlanDMii (http://www.thingiverse.com/thing:16193)  
- "PCB Machining Vise" by Forgetful_Guy (http://www.thingiverse.com/thing:63578)  

Special thanks:  
--  
- Z axis concepts by **Quim Borras** and the spindle motor holder by **Misan** were really useful!! Also, **Diego Viejo**'s machine was of great inspiration for the Z axis (https://plus.google.com/u/0/photos/113930344830086538817/albums/5868944432651911713?authkey=CLDJgdehlN773gE) **Thank you all!!**  
- This design woudn't have been possible without the encouragement of the **Panda CNC community** (https://plus.google.com/u/0/communities/102402711800402614517)  
- Also, thanks to **Obijuan** (http://iearobotics.com) for naming the machine Cyclone :)  

Credit for the ideas used  
--  
The origin of Cyclone took place while I was inside the __Panda CNC__ community (https://plus.google.com/u/0/communities/102402711800402614517). This is from December 2012 to mid-February 2013.  
Here is the credit for the ideas that were used:  

* __Let's design a 3D-printable CNC for PCB milling, it will be named Panda:__ Guillermo Welch (mid-December, via Google Talk)  
* __X carriage rod distribution:__ CÃ©sar Augusto FernÃ¡ndez Cano claims Cyclone's X axis is a derivate of his concept: https://plus.google.com/u/0/111421387442355054591/posts/QrfYtEuZBaj  
* __100x160mm workspace:__ David Martin https://dl.dropboxusercontent.com/u/16122275/PandaCNC_credit/workplace_size.png  
* __Using gears to drive the X-Y axes:__ Guillermo Welch https://plus.google.com/u/0/101232926728463427403/posts/QjZGNcWcgGg  
* __Regarding the woodbase:__ Guillermo Welch always contemplated the possibility of attaching the machine (optionally) to a woodbase. I decided to use the base as a main structural part instead. See https://dl.dropboxusercontent.com/u/16122275/PandaCNC_credit/woodbase.png (screenshot from https://plus.google.com/u/0/113437723819360223498/posts/8LDCSSVWqCS)  
* __List of CNC endmill types:__ David Martin https://dl.dropboxusercontent.com/u/16122275/PandaCNC_credit/cnc_endmill_types.png  

Please note I have taken screenshots of the post that are on the closed G+ Panda community (https://plus.google.com/u/0/communities/116318709564872967169). You can register and see by yourself.  

**All other development present on Cyclone has nothing to do with Panda and is not related to the Panda project.**  

