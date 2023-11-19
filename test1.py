from logic_synthesizer import *
from minimize import *
from FPGAstructure import *
import networkx as nx
from FPGAinitializer import get_equations

#========tESTING eqns stuff
#filename="test_eqns.blif"
eqns=get_equations()
print(eqns)
#eqns=textToArray(eqns)
#eqns=minimize_equations(eqns)
eqns=toFactorer(eqns)
print("Factorer")
print(eqns)
eqns=toSplitter(eqns)
print("Splitter")
print(eqns)

#===============FPGA
#FPGA1=FPGA()
#FPGA1.set_LUTS(eqns)
#print("LUTS")
#print(FPGA1.get_nodes())
#print("Nodes before J")
#print(FPGA1.get_node_before('J'))

#print("Inputs")
#FPGA1.updateInputs()
#print(FPGA1.get_nodes())
#FPGA1.updateOutputs()

#IN LIBRARY
#print("Nodes")
#print(FPGA1.get_nodes())
#for node, data in FPGA1.nodes(data=True):
#	print(f"Node {node}: {data}")
#print(list(FPGA1.nodes()))

#METHODS
#print("LUTS")
#print(FPGA1.get_LUTS())
#print("inputs")
#print(FPGA1.get_inputs())
#print("outputs")
#print(FPGA1.get_outputs())
#FPGA1.show_FPGA()

#=========testing dont_care
#letters=['*','1' ,'1']
#names=dont_cares(letters)

#=========testing factors
#equations = []
#with open(filename,"r") as file:
#	lines=file.readlines()
#file.close()

#for line in lines:
#	if line.startswith('#'):
#		pass
#	else:
#		eqn=line.replace(" ","")
#		eqn=eqn.rstrip()
#		equations.append(eqn)
#print(equations)

#factored=mutual_factor(equations)
#print(factored)

#===========testing factor
#eqn = ["ABC","ABD"]
#common = "AB"
#print(eqn)
#new_eqn=factor(eqn,common)
#print(new_eqn)
