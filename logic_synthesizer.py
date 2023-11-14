import numpy as np

#TODO fix return functions
#TODO organize factorer
#TODO allow for options on factor level and minimization

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
					if char not in output:
						unique_inputs.append()
			inputs=",".join(unique_inputs)
			equation_ID.append(inputs)
			inputs = inputs.split(",")
			inputs=tuple(inputs)

			#make truth table
			size=len(unique_inputs)
			#TODO check array is correct
			truthtable = np.zeros([2]*size) #make array based on num of inputs
			terms = line.split('+')
			true_indice = []
			for term in terms:
				truth_value = []
				for i in range(len(inputs)):
					truth_value.append('*') #initialize array with *
				for i in range(len(term)):
					char = term[i]
					if char == "'":
						char = term[i-1]
						place = inputs.index(char)
						truth_value[place] = 0
					else:
						place = inputs.index(char)
						truth_value[place] = 1
				if len(truth_value) != len(inputs):
					print("Not matching in truth table generation")
				if '*' in truth_value:
					new_indices = dont_cares(truth_value)
				else:
					new_indices = truth_value
				for item in new_indices:
					true_indices.append(tuple(item)) #TODO check if this outputs correct type
			for indice in np.ndindex(truthtable.shape):
				if indice in true_indice:
					truthtable[indice] = 1
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

def dont_cares(true):
	none_holder = []
	none_holder.append(true)
	clean_holder = []

	while len(none_holder) > 0:
		if '*' in none_holder[0]:
			working = none_holder.pop(0)
			none_place = working.index('*')
			working[none_place] = 0
			none_holder.append(working)
			working[none_place] = 1
		else:
			working = none_holder.pop(0)
			clean_holder.append(working)

	return clean_holder

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
				factored.append(compare)

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
				factored.append(new_term)

	#TODO can these equations be decomposed by similar terms?
	#TODO if equation hasnt been changed, add to array so that every term is there. 


def mega_factor():
	equation_id = []
	common_literals = []
	mass_common_terms = {}
	enacted_equations = []

	#Find common literals in each equation
	for i in range(len(equations)):
		eqn = equations[i]
		eqn_terms = eqn.split("=")
		eqn_terms = eqn_term[1]
		terms = eqn_term.split("+")
		common_literals[i] = find_common_literals
		
	#Check if equations have common literals
	for i in range(len(common_literals)):
		for j in range (len(common_literals)):
			if i == j:
				pass
			else:
				common_mass_literals = set(common_literals[i].items()) & set(common_literals[j].items())
				if common_mass_literals:
					for key, value in common_entries:
        					if key in mass_common_terms:
        						mass_common_terms[key].append(i,j)
        					else:
        						mass_common_terms[key]=[i,j]
	
	# Factor common equations
	# for each item in mass common terms, 
		#turn to a set, 
		# then choose the longest one to enact
		# repeat if only the equations havent been enacted upon. 
			# if so, pop then factor. 
			# do till dictionary is empty.
	
	# Factor non common by what makes the most impact
	#To get the rest, check which have been enacted and remove from a sequence of to be enacted upon
	#if it has a dictionary, do
	#Factor those one by one based on highest value within dictionary entry
	#Add to factored list
	#Append any missing equations to factored list as basic and boring as is.

	#Return factored list
	#decompose and factor :)

def find_common_literals(words):
    common_letters = []
    common_series = []
    common_tally = {}

    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            common_set = set(words[i]) & set(words[j])
            common_letters.extend(common_set)

            common_sequence = ''.join(
                letter for letter in words[i] if letter in common_set
            )
            if common_sequence:
                common_series.append(common_sequence)

    common_series = list(set(common_series))

    for word in words:
        letters = list(word)
        for i in range(len(common_series)):
            common_term = common_series[i]
            common_letters = list(common_term)
            #print("Looking at {} and {}".format(str(letters), str(common_letters)))
            if all(item in letters for item in common_letters):
                if common_term in common_tally:
                    common_tally[common_term] = common_tally[common_term] + 1
                    #print("Old! {} now at {}".format(common_term, common_tally[common_term]))
                else:
                    common_tally[common_term] = 1
                    #print("New! {} created".format(common_term))
    #todo if common tally empty, return empty dictionary
    return common_tally

def factor_rewriter(eqn, common):
	# TODO
	print("Hello world")

