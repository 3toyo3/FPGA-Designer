# FPGA-Designer
This program takes an input of equations and maps it to a virtual FPGA.
* Construct FPGA from user input on number of LUTS, external connections, and LUT type.
* Take an .eqns file for mapping equations to LUTS
* Optimize equations with function minimzation, substituition, and multi-level factoring.
* Save design as a bitstream file for later use.

From a design, the user can see:
* One or all LUT assignments
* Connections between LUTS
* External connections
* Resource allocation
* Graph representation of the FPGA

## Files
* FPGAinitializer.py : This program interacts with the user to create the FPGA design.
* FPGAstructure.py : This program holds the FPGA class. The connections and equations are tracked with a Directed Acyclic Graph while two lists hold the external inputs and outputs.
* logic_synthesis.py : This program is responsible for optimizing the equations by parsing, factoring equations in relation to eachother, distributing and substituition.
* truthTable.py : This program constructs a MD array of an equation.
* minimize.py : From the MD array of above, this program minimizes each equation using the Quine-McCluskey minimization technique.
* LUT.py and LUT6.py : These hold LUT objects, which is used for LUT assignment.
* synthesis_engine.py and synthesis_engine6.py : These programs assign LUTS by splitting equations into either 4 or 6 input equations as well as handles the bitstream in relation to LUT assignment.
* *.eqns : These files hold the equations for the FPGA design. Demo files are specifically made to show this program's capabilities.
* *.bits : This is a bitstream file, used to recreate a previously designed FPGA.
