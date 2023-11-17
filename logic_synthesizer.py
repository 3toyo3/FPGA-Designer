import numpy as np
#from minimize import *

#TODO allow for options on factor level and minimization
#TODO convert for factoring and splitting

# TODO check this
# Takes a file with list of equations and outputs a dictionary of each equation represented as a MD array
def textToArray(filename):
	names = {}

	# check if exists : already done in initializer
	with open(filename, "r") as file:
		lines = file.readlines()
	file.close()

	for line in lines:
		if line.startswith('#'):
			pass #comments allowed :)
		else:
			eqn=line.replace(" ","")
			eqn=eqn.rstrip()
			#get output
			print(eqn)
			seperate_formula=eqn.split("=")
			eqn_terms=seperate_formula[1]
			print(seperate_formula)
			output=seperate_formula[0]

			#store variables in unique string
			equation_ID=[output]
			unique_inputs=[]
			for char in line:
				if char not in unique_inputs and char.isalpha():
					if char not in output:
						unique_inputs.append(char)
			#inputs=",".join(unique_inputs)
			equation_ID=equation_ID+unique_inputs
			equation_ID=",".join(equation_ID)
			inputs=tuple(unique_inputs)

			#make truth table
			size=len(unique_inputs)
			truthtable = np.zeros([2]*size) #make array based on num of inputs
			terms = eqn_terms.split('+')
			true_indices = []
			for term in terms:
				#print(true_indices)
				truth_value = []
				print(term)
				for i in range(len(inputs)):
					truth_value.append('*') #initialize array with *
				for i in range(len(term)): #Find if ' or normal
					char = term[i]
					print(char)
					if char == "'":
						char = term[i-1]
						place = inputs.index(char)
						truth_value[place] = 0
						#print("Zero")
					else:
						place = inputs.index(char)
						truth_value[place] = 1
						#print("One")
				if len(truth_value) != len(inputs):
					print("Not matching in truth table generation")
				if '*' in truth_value:
					print("Dont care")
					new_indices = dont_cares(truth_value)
					print(new_indices)
					for item in new_indices:
						#print("Item")
						#print(item)
						true_indices.append(tuple(item))
				else:
					new_indices = truth_value
					true_indices.append(tuple(item))
			for indice in np.ndindex(truthtable.shape):
				if indice in true_indices:
					truthtable[indice] = 1
					print("Term marked as true found for {}".format(equation_ID))
			names[equation_ID]=truthtable
	return names

#Takes a dictionary with equations' MD arrays, and outputs list of minimized equations
def minimize(names):
	equations=[]
	for entry in names:
		print(entry)
		truthtable=names[entry]
		new_string=minimized_sop(truthtable)
		print(new_string)
		#TODO Forcefully recreate equation

		equations.append(new_string)

	return equations

#Takes a list of characters, and if any char represents a dont care, expands the list
def dont_cares(true):
	none_holder = []
	none_holder.append(true)
	clean_holder = []
	while len(none_holder) > 0:
		#print("None holder")
		#print(none_holder)
		if '*' in none_holder[0]:
			working = list(none_holder.pop(0))
			#print("Working")
			#print(working)
			none_place = working.index('*')
			working[none_place] = 0
			working_zero=tuple(working)
			#print(working)
			none_holder.append(working_zero)
			#print(none_holder)
			working[none_place] = 1
			working_one=tuple(working)
			#print(working)
			none_holder.append(working_one)
		else:
			working = none_holder.pop(0)
			clean_holder.append(working)
	#print("Clean")
	return clean_holder

# From a list of equations, checks if they are factorable and outputs a list of factored equations.
def substituition(equations):
	eqns_list = []
	eqns_dict = {}
	eqns_dict_new = {}
	#mutable
	for eqn in equations: #puts every equation in dictionary
		seperate_eqn = eqn.split("=")
		eqns_dict[seperate_eqn[0]]=seperate_eqn[1] 
	eqns_dict_new = eqns_dict.copy()
	#print(eqns_dict_new)
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
		substitute_terms=eqns_dict[entry1].split("+") #All these terms must exist in....
		#print("Substitute")
		#print(substitute_terms)
		for entry2 in eqns_dict:
			if entry1 == entry2:
				pass
			else:
				substituted_terms=eqns_dict[entry2].split("+") #This equation
				#print("Substituted")
				#print(substituted_terms)
				common=[term in substituted_terms for term in substitute_terms ] #r and c
				#print("Common")
				#print(common)
				if all(common):
					# print("All are true?")
					for term in substitute_terms:
						#print(term )
						substituted_terms.remove(term)
					substituted_terms.append(entry1)
					#print(substituted_terms)
					new_term='+'.join(substituted_terms)
					eqns_dict_new[entry2]=new_term
	#print(eqns_dict_new)
	#print(eqns_dict)
	#make a list of strings
	for entry in eqns_dict_new:
		eqns_list.append(entry+"="+eqns_dict_new[entry])
	return eqns_list 

#From a list of equations, outputs a list of equations factored based on eachother
def mutual_factor(equations): #TODO make sure works w multiple '
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

	#Find common literals
	common_literals_per_eqn = eqns_dict.copy()

	for entry in common_literals_per_eqn:
		eqn_terms = common_literals_per_eqn[entry]
		common_literals_per_eqn[entry]=find_common_literals(eqn_terms)

	#Remove any equations that cant be factored
	eqns_to_remove = [key for key, value in common_literals_per_eqn.items() if isinstance(value, dict) and not value]
	for eqn in eqns_to_remove:
    		common_literals_per_eqn.pop(eqn)

	print("Common p eqn")
	print(common_literals_per_eqn)

	#Check if two equations have common literals
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
	# Remove dupes from above
	for term in mass_common_terms:
		mass_common_terms[term] = set(mass_common_terms[term])

	print("Mass")
	print(mass_common_terms)

	# Factor common equations
	factorsExist = True
	while factorsExist:
		most_common_term = max(mass_common_terms, key=lambda x: len(mass_common_terms[x]))
		print(most_common_term)
		common_equations = mass_common_terms.pop(most_common_term)
		print("Common equations ")
		print(common_equations)

		#TODO make this work for cube-free
		#Check if the most_common_to_be_factor in other could-be-factors and removes
		for entry in mass_common_terms: #TODO check this w single?
			#print("Entry")
			#print(entry)
			entry_equations = tuple(mass_common_terms[entry])
			eqn_dupes = set(entry_equations)
			for eqn in entry_equations:
				#print("Inside removal")
				#print(eqn)
				if eqn in common_equations:
					#print("I should be removing {}".format(eqn))
					eqn_dupes.remove(eqn)
					#print("Yay!")
			#print("And now..")
			#print(entry_equations)
			#print(eqn_dupes)
			mass_common_terms[entry]=eqn_dupes

		#Remove any 1 term in dictionary
		not_mass_common_terms_anymore = [key for key, value in mass_common_terms.items() if len(value) == 1]
		for term in not_mass_common_terms_anymore:
			mass_common_terms.pop(term)

		print("New mass")
		print(mass_common_terms)

		#Factore each equation that was found to be common
		for eqn in common_equations:
			terms = eqns_dict[eqn]
			#print("Gonna factor - group")
			#print(terms)
			#print(most_common_term)
			terms = factor(terms, most_common_term)
			eqns_dict[eqn] = terms
			common_literals_per_eqn.pop(eqn)

		#then repeat until either dictionary is empty or the remaining entries are 1 length
		#all_length_one = all(len(value) == 1 for value in mass_common_terms.values())
		if len(mass_common_terms) == 0:
			#print("Yer")
			factorsExist = False

	print(eqns_dict)
	print(common_literals_per_eqn)
	# Factor non common by what makes the most impact
	for entry in common_literals_per_eqn:
		print(entry)
		#Find most common term
		common_terms = common_literals_per_eqn[entry]
		most_common_term = max(common_terms, key=common_terms.get)

		#Factor
		terms = eqns_dict[entry]
		print("Gonna factor - alone")
		print(terms)
		print(most_common_term)
		terms = factor(terms, most_common_term)
		eqns_dict[entry]= terms

	#Turn dictionary to list
	for eqn in eqns_dict:
		new_terms = eqns_dict[eqn]
		if type(new_terms) is list:
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
    return common_tally

#Takes an list of terms and common term, and factors it out and outputs it as a new string
def factor(terms, common):
	new_terms = []
	new_terms_no_factor = []

	chars_to_check = list(common)

	#terms = inputs.split("+")
	for term in terms:
		new_term = []
		counting = []
		for char in chars_to_check:
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
