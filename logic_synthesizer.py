import numpy as np

names = {}
equations = []
factored = []

# Takes a file with list of equations and a bool to minimize, and outputs a list of equations.
def textToArray(filename, minimize):
	global names
	global equations

	# check if exists : already done in initializer
	with open(filename, "r") as file:
		lines = file.readlines()
	file.close()

	for line in lines: 
		if line.startswith('#'):
			pass #comments allowed :)
		else:
			line=line.replace(" ","")
			#get output
			seperate_formula=eqn.split("=")
			seperate_formula=seperate_formula[1]
			output=seperate_formula[:-1]

			#store variables in unique string
			equation_ID=[output]
			unique_inputs=[]
			for char in line: #TODO check ifs
				if char not in unique_inputs and char.isalpha():
					if char not output:
						unique_inputs.append()
			inputs=",".join(unique_inputs)
			equation_ID.append(inputs)

			#make truth table
			size=len(unique_inputs)
			#TODO check array is correct
			truthtable = np.zeros([2]*size) #make array based on num of inputs
			terms = line.split()
			for term in terms:
				# check if a char is a char or char'
				# for each literal go to that array index and set as 1
			names[equation_ID]=truthtable

			#if minimized, minimize from entry
			if minimize:
				sample = prime_implicants(truthtable)
				sample1 = essential_prime_implicants(sample, truthtable)
				preserved_prime_implicants = sample.copy()
				eqn = format_sop(choose_terms(sample,sample1, truthtable))
			else:
				eqn = line
			equations.append(eqn)


# TODO: put cleaned minimizer here :)

# From a list of equations, checks if they are factorable and outputs a list of factored equations.
def factor():
	global equations
	global factored
	#is equation referenced?
	for eqn in equations:
		#get output
		seperate_equation=eqn.split("=")
		output=seperate_equation[1]

		for i in range(len(eqn)):
			if output in equations[i]:
				print("Referenced") #TODO make this meaningful

	#is the equation reused but without referring to output? -- substituion
	for eqn in equations:
		#get output and inputs
		seperate_equation=eqn.split("=")
		reused_output=seperate_equation[1]
		reused_inputs=seperate_equation[2]
		r_input_list=reused_inputs.split("+")

		#check other equations
		for i in range(len(eqn)):
			compare_sep_equation=equation[1].split("=")
			compare_outputs=compare_sep_equation[1]
			compare_inputs=compare_sep_equation[2]
			c_input_list=compare_inputs.split("+")

			#check if the same terms exist
			common=[term in r_input_list for term in c_input_list]
			if len(common) == len(r_input_list): #only remove if all exist
				for term in common:
					c_input_list.remove(term)
				c_input_list.append(reused_output) #TODO make sure this is string
				new_term=compare_outputs+"="+'+'.join(c_input_list)
				factored.append(compare)

	#TODO can these equations be decomposed by similar terms?
