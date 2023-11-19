# FPGA-Designer
This program takes an input of equations and maps it to a virtual FPGA. The program takes a .blif file (please refer to blif files within repo on how to structure) and creates the FPGA based on user inputs for the number of LUTS, external connections, and internal connections. This program also allows for the design to be saved as a bitstream file.
This allows for the program to recraft the design later. With the FPGA design, the user can then see where each function was mapped, the connections between each, the external assignments, the resource allocations, and a visual of the FPGA connections. This program also allows for optimizations such as function minimization, substituition, and multi-level factoring in order to reduce the number of gates. The user can choose what optimizations to implement when crafting the FPGA.

## Files
* FPGAinitializer.py : This program interacts with the user to create the FPGA design.
* FPGAstructure.py : This program holds the FPGA class. The connections and equations are tracked with a Directed Acyclic Graph while two lists hold the external inputs and outputs.
* logic_synthesis.py : This program is responsible for optimizing the equations by constructing a MD array of each equation, factoring equations in relation to eachother, and substituition.
* minimize.py : From the MD array of above, this program minimizes each equation using the Quine-McCluskey minimization technique.
* LUT.py and LUT6.py : These hold LUT objects, which is used for LUT assignment.
* synthesis_engine.py and synthesis_engine6.py : These programs assign LUTS by splitting equations into either 4 or 6 input equations as well as handles the bitstream in relation to LUT assignment.
* *.blif : These files hold the equations for the FPGA design. Demo files are specifically made to show this program's capabilities.
* *.bits : This is a bitstream file, used to recreate a previously designed FPGA.
