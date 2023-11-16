import numpy as np

#TODO allow for options on factor level and minimization


# Takes a file with list of equations and outputs a dictionary of each equation represented as a MD array
def textToArray(filename, minimize):
	names = {}

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
	return names

#Takes a list of characters, and if any char represents a dont care, expands the list
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
def factor_level1(equations):
	eqns_list = []
	eqns_dict = {}
	#mutable
	for eqn in equations: #puts every equation in dictionary
		seperate_eqn = eqn.split("=")
		eqns_dict[seperate_eqn[0]]=seperate_eqn[1]
		
	#is equation referenced?
	for entry1 in eqns_dict:
		for entry2 in eqns_dict:
			if entry1 == entry2:
				pass
			else:
				if entry1 in eqns_dict[entry2]:
					print("Cool") #idk not necessarily anything currently
	#can I completely substitute an equation?
	for entry1 in eqns_dict:
		substitute_terms=eqns_dict[entry1].split("+")
		for entry2 in eqns_dict:
			if entry1 == entry2:
				pass
			else:
				substituted_terms=eqns_dict[entry2].split("+")
				common=[term in r_input_list for term in c_input_list]
				if len(common) == len(substitute_terms): #only remove if all exist
					for term in common:
						substituted_terms.remove(term)
					substituted_terms.append(entry1)
					new_term='+'.join(substituted_terms)
					eqns_dict[entry2]=new_term
	#make a list of strings
	for entry in eqns_dict:
		eqns_list.append(entry+"="+eqns_dict[entry2])
	return eqns_list

#From a list of equations, outputs a list of equations factored based on eachother
def factor_level2(equations):
	eqns_dict = {}
	common_literals_per_eqn = {}
	mass_common_terms = {}
	eqns_list = []

	#Set up equations
	for eqn in equations:
		eqn_split = eqn.split("=")
		eqn_inputs=eqn_split[1]
		eqn_inputs=eqn_inputs.split("+")
		eqns_dict[eqn_split[0]]=eqn_inputs

	common_literals_per_eqn = eqns_dict.copy()

	for entry in common_literals_per_eqn:
		eqn_terms = common_literals_per_eqn[entry]
		common_literals_per_eqn[entry]=find_common_literals(eqn_terms)

	#Check if equations have common literals
	for entry1 in common_literals_per_eqn:
		for entry2 in common_literals_per_eqn:
			if entry1 == entry2:
				pass
			else:
				common_mass_literals = set(common_literals_per_eqn[entry1].items()) & set(common_literals_per_eqn[entry2].items())
				if common_mass_literals:
					for key, value in common_mass_literals:
        					if key in mass_common_terms:
        						mass_common_terms[key].append(entry1)
        						mass_common_terms[key].append(entry2)
        					else:
        						mass_common_terms[key]=[entry1,entry2]
	# Remove dupes
	for term in mass_common_terms:
		mass_common_terms[term] = set(mass_common_terms[term])

	# Factor common equations
	factorsExist = True
	while factorsExist:
		most_common_term = max(mass_common_terms, key=lambda x: len(mass_common_terms[x]))
		common_equations = mass_common_terms.pop(most_common_term)

		#Check if the most_common_to_be_factor in other could-be-factors and removes
		for entry in mass_common_terms:
			for eqns in mass_common_terms[entry]:
				if eqn in common_equations:
					eqn.remove(eqn)

		#Factore each
		for eqn in common_equations:
			terms = eqns_dict[eqn]
			terms = factor(terms, most_common_term)
			eqns_dict[eqn] = terms

		#then repeat until either dictionary is empty or the remaining entries are 1 length
		all_length_one = all(len(value) == 1 for value in mass_common_terms.values())
		if len(mass_common_terms) == 0:
			factorsExist = False
		elif all_length_one:
			factorsExist = False
		else:
			pass

	# Factor non common by what makes the most impact
	for entry in common_literals_per_term:
		#Find most common term
		common_terms = common_literals_per_terms[entry]
		most_common_term = max(common_terms, key=common_terms.get)

		#Factor
		terms = eqns_dict[entry]
		terms = factor(terms, most_common_term)
		eqns_dict[entry]= terms

	#Turn dictionary to list
	for eqn in eqns_dict:
		new_terms = eqns_dict[eqn]
		new_terms = "+".join(new_terms)
		eqns_list.append(eqn+"="+new_terms)
	return eqns_list

# From a list of terms, outputs the most common terms as a dictionary
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

    common_series = list(set(common_series)) # remove dupes

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
    #TODO if common tally empty, return empty dictionary
    return common_tally

#Takes an equation string and common term, and factors it out and outputs it as a new string
#TODO make this work on only after the equal aka list of terms
def factor(eqn, common):
	working_str = eqn
	output = working_str.split("=")
	inputs = output[1]
	output = output[0]
	new_terms = []
	new_terms_no_factor = []

	chars_to_check = list(common)

	terms = inputs.split("+")
	for term in terms:
		new_term = []
		counting = []
		for char in char_to_check:
			counting.append(term.find(char))
		if -1 in counting:
			#cannot be factored so leave alone
			new_terms_no_factor.append(term)
			pass
		else:
			#parse factored terms
			for i in range(len(term)):
				if i in counting:
					pass
				else:
					new_term.append(term[i])
		#add to list
		new_terms.append(''.join(new_term))

	#craft string
	working_str = '+'.join(new_terms)
	working_str = common+"("+working_str+")"
	working_str = working_str + "+".join(new_terms_no_factor)
	return working_str
