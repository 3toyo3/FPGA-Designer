from logic_synthesizer import *
from minimize import *

#========tESTING ARRAY
filename="test_eqns.blif"
names=textToArray(filename)
equations=minimized_sop(names)

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
