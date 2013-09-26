Description  
--------
This is a patch of Marlin by ErikZalm (https://github.com/ErikZalm/Marlin) that adds probing command (G30) with the functions developed by larsbrubaker (https://github.com/ErikZalm/Marlin/pull/323)

The changes made (marked as _CGS MOD_) are hereby released on the public domain.

Quick Information  
===================
You must setup two endstops for the Z axis, the lower one is considered our "probe"  

_Pin definitions (from "pins.h")_  
<pre>
  <code>
// We are using the Z_MIN endstop as a probe  
// Also, we have our Z_MAX endstop to limit the vertical movement of the spindle  
#define Z_PROBE_PIN 27  // using Sanguinololu, pin 36 (D27) , labeled A4  
#define Z_PROBE_HIT_VALUE 0 // Switch this if your probe gives an inverted value  
  </code>
</pre>

Disclaimer
===================
This hardware/software is provided “as is," and you use the hardware/software at your own risk. Under nocircumstances shall Carlosgs be liable for direct, indirect, special, incidental, or consequential damages resulting from the use, misuse, or inability to use this hardware/software, even if Carlosgs has been advised of the possibility of such damages.  

