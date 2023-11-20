import numpy as np
from minimize import *

# Takes a file with list of equations and outputs a dictionary of each equation represented as a MD array
def textToArray(equations):
	names = {}

	for eqn in equations:
		print(eqn)
		seperate_formula=eqn.split("=")
		eqn_terms=seperate_formula[1]
		print(seperate_formula)
		output=seperate_formula[0]

		#store variables in unique string
		equation_ID=[output]
		unique_inputs=[]
		for char in eqn:
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
				true_indices.append(tuple(new_indices))
		for indice in np.ndindex(truthtable.shape):
			if indice in true_indices:
				truthtable[indice] = 1
				print("Term marked as true found for {}".format(equation_ID))
		names[equation_ID]=truthtable
	return names

#Takes a dictionary with equations' MD arrays, and outputs list of minimized equations, references miminize.py
def minimize_equations(names):
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
		if '*' in none_holder[0]:
			working = list(none_holder.pop(0))
			none_place = working.index('*')
			working[none_place] = 0
			working_zero=tuple(working)
			none_holder.append(working_zero)
			working[none_place] = 1
			working_one=tuple(working)
			none_holder.append(working_one)
		else:
			working = none_holder.pop(0)
			clean_holder.append(working)
	return clean_holder

# From a list of equations, checks if they are factorable and outputs a list of factored equations.
def substituition(equations):   #Todo  hyphens 
	eqns_list = []
	eqns_dict = {}
	#eqns_dict_new = {}
	#hyphen = False
	#mutable
	for eqn in equations: #puts every equation in dictionary
		seperate_eqn = eqn.split("=")
		eqns_dict[seperate_eqn[0]]=seperate_eqn[1]
	#eqns_dict_new = eqns_dict.copy()
	#print(eqns_dict_new)
	#is equation referenced?
	#for entry1 in eqns_dict:
	#	for entry2 in eqns_dict:
	#		if entry1 == entry2:
	#			pass
	#		else:
	#			if entry1 in eqns_dict[entry2]:
	#				print("Cool") #idk not necessarily anything currently
	#can I completely substitute an equation?
	# Entry 1 is what is going to be put it. IE: F = c+d
	# Entry 2 must have entry 1 within it G = ab+c+d
	for entry1 in eqns_dict:
		#if "(" in entry1:
		#	hyphen = True
		#	beginning = entry1.find("(")
		#	end = entry1.find(")")
		#	factored_term = 
		#TODO pull of ()
		#substitute_terms=eqns_dict[entry1].split("+") #All these terms must exist in.... 
		### TODO take out factor parts
		#print("Substitute")
		#print(substitute_terms)
		for entry2 in eqns_dict:
			if entry1 == entry2:
				pass
			else:
				equation_new = find_if_same(eqns_dict[entry1], eqns_dict[entry2], entry1)
				eqns_dict[entry2] = equation_new
				#substituted_terms=eqns_dict[entry2].split("+") #This equation
				#print("Substituted")
				#print(substituted_terms)
				#common=[term in substituted_terms for term in substitute_terms ] #r and c
				#print("Common")
				#print(common)
				#if all(common):
				#	# print("All are true?")
				#	for term in substitute_terms:
				#		#print(term )
				#		substituted_terms.remove(term)
				#	substituted_terms.append(entry1)
				#	#print(substituted_terms)
				#	new_term='+'.join(substituted_terms)
				#	eqns_dict_new[entry2]=new_term
	#print(eqns_dict_new)
	#print(eqns_dict)
	#make a list of strings
	for entry in eqns_dict:
		eqns_list.append(entry+"="+eqns_dict[entry])
	return eqns_list

def find_if_same(eqn1, eqn2, eq1_out):
	if "(" in eqn2 and ")" in eqn2:
		beginning = eqn2.find("(")
		end = eqn2.find(")")
		par_eqn = eqn2[beginning+1:end]
		par_eqn = find_if_same(eqn1, par_eqn, eq1_out)
		eqn_new = eqn2[:beginning] + par_eqn + eqn2[end+1:]
		#print(eqn_new)
	else:
		#print("Boo!")
		eqn1 = eqn1.split("+")
		eqn2 = eqn2.split("+")
		#print("Split {} {}".format(str(eqn1), str(eqn2)))
		common=[term in eqn2 for term in eqn1]
		if all(common):
			for term in eqn1:
				eqn2.remove(term)
			eqn2.append(eq1_out) #equation1 output
		eqn_new = '+'.join(eqn2)
        	#print(eqn_new)
	return eqn_new

#From a list of equations, outputs a list of equations factored based on eachother
def mutual_factor(equations):
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

	#print("After finding common literals")
	#print(common_literals_per_eqn)

	#Remove any equations that cant be factored
	eqns_to_remove = [key for key, value in common_literals_per_eqn.items() if isinstance(value, dict) and not value]
	for eqn in eqns_to_remove:
    		common_literals_per_eqn.pop(eqn)

	print("Common literals in each eqn:")
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

	print("Shared common literals and their equations:")
	print(mass_common_terms)

	# Factor common equations
	if len(mass_common_terms)>0:
		factorsExist = True
	else:
		factorsExist = False
	while factorsExist:
		#most_common_term = max(mass_common_terms, key=lambda x: len(mass_common_terms[x]))
		most_common_term=get_most_useful(mass_common_terms)
		common_equations = mass_common_terms.pop(most_common_term)
		print("Most common term: {} and equations: {}".format(most_common_term, str(common_equations)))

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

		#print("New mass")
		#print(mass_common_terms)

		#Factore each equation that was found to be common
		for eqn in common_equations:
			terms = eqns_dict[eqn]
			#print("Gonna factor - group")
			#print(terms)
			#print(most_common_term)
			#print("In progress mass_factoring of {}".format(eqn))
			terms = factor(terms, most_common_term)
			#print()
			eqns_dict[eqn] = terms
			common_literals_per_eqn.pop(eqn)

		#then repeat until either dictionary is empty or the remaining entries are 1 length
		#all_length_one = all(len(value) == 1 for value in mass_common_terms.values())
		if len(mass_common_terms) == 0:
			#print("Yer")
			factorsExist = False

	print("Equations after mass factoring:")
	print(eqns_dict)
	print("Equations left to factor:")
	print(common_literals_per_eqn)
	# Factor non common by what makes the most impact
	for entry in common_literals_per_eqn:
		#print(entry)
		#Find most common term
		common_terms = common_literals_per_eqn[entry]
		#most_common_term = max(common_terms, key=common_terms.get)
		most_common_term = get_most_useful(common_terms)

		#Factor
		terms = eqns_dict[entry]
		#print("Gonna factor - alone")
		#print(terms)
		#print(most_common_term)
		terms = factor(terms, most_common_term)
		eqns_dict[entry]= terms

	#Turn dictionary to list
	for eqn in eqns_dict:
		new_terms = eqns_dict[eqn]
		if type(new_terms) is list:
			new_terms = "+".join(new_terms)
		eqns_list.append(eqn+"="+new_terms)
	print("Final equations:")
	return eqns_list

# From a list of terms, outputs the most common terms as a dictionary
def find_common_literals(words):
    common_letters = []
    common_series = []
    common_tally = {}

    #print("Finding common literals in {}".format(str(words)))
    #check each term to another for common letters
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            common_set = set(words[i]) & set(words[j])
            #print("Common set")
            #print(common_set)
            common_letters.extend(common_set)

            #if multiple letters are common, then combine them
            common_sequence = ''.join(
                letter for letter in words[i] if letter in common_set
            )
            if common_sequence:
                common_series.append(common_sequence)

    common_series = list(set(common_series)) # remove dupes
    #print("Common_series ")
    #print(common_series)

    #check each term for if they have a common term, and if so, store which one
    #this is character based rather than segment based so to catch cases like ab in acb and adb
    for word in words:
        letters = list(word)
        #print("Working on {}".format(word))
        for i in range(len(common_series)):
            common_term = common_series[i]
            common_letters = list(common_term)
            #print("Looking at {} and {}".format(str(letters), str(common_letters)))
            if all(item in letters for item in common_letters): #if all the letters are found, then the common term is in this term, therefore add to tally
            	if len(common_letters) != len(letters): #make sure cube free
                	if common_term in common_tally:
                		common_tally[common_term] = common_tally[common_term] + 1
                		#print("Old! {} now at {}".format(common_term, common_tally[common_term]))
                	else:
                    		common_tally[common_term] = 1
                    		#print("New! {} created".format(common_term)) 
    solo = []
    for entry in common_tally:
    	if common_tally[entry] == 1:
    		solo.append(entry)
    for entry in solo:
    	common_tally.pop(entry)
    #print("Final version")
    #print(common_tally)
    return common_tally

#Takes an list of terms and common term, and factors it out and outputs it as a new string
def factor(terms, common):
	new_terms = []
	new_terms_no_factor = []

	chars_to_check = list(common)
	#print("Chars to check:")
	#print(chars_to_check)

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
		#print("Before: {} and After: {}".format(term, new_term))
	#craft string
	new_terms = [char for char in new_terms if char] #remove emptys
	#print("Leftovers from factoring: {}".format(str(new_terms)))
	#print("Remainders from factoring: {}".format(str(new_terms_no_factor)))
	#print("Crafting str")
	working_str = '+'.join(new_terms)
	#print(working_str)
	working_str = common+"("+working_str+")"
	#print("Crafting str")
	#print(working_str)
	if len(new_terms_no_factor) != 0:
		working_str = working_str + "+"
		#print(working_str)
	working_str = working_str + "+".join(new_terms_no_factor)
	#print("Crafting str")
	#print(working_str)
	return working_str

#converts equations so that they can be split properly (a -> A')
def toSplitter(equations):
	new_equations = []
	for eqn in equations:
		new_eqn = []
		for char in eqn:
			if char.isalpha() and char.islower():
				new_eqn.append(char.upper())
				new_eqn.append("'")
			else:
				new_eqn.append(char)
		new_eqn=''.join(new_eqn)
		new_equations.append(new_eqn)
	return new_equations

#converts equations so that they can be factored properly (A' -> a)
def toFactorer(equations):
	new_equations = []
	for eqn in equations:
		new_eqn=[]
		for i in range(len(eqn)):
			if eqn[i] == "'":
				new_eqn[-1]=new_eqn[-1].lower()
			else:
				new_eqn.append(eqn[i])
		new_eqn=''.join(new_eqn)
		new_equations.append(new_eqn)
	return new_equations

#def get_terms_from_eqn(equation):
#	substituted_terms = []
#	factored = False
#	if "(" in equation:
#		beginning = equation.find("(")
#		end = equation.find(")")
#		factor_term = eqn[beginning+1:end]
#		substituted_terms.append(factor_term)
#		factored = True
#	for i in 
#	#TODO

def distribute(equation):
	split_equation = equation.split("=")
	output = split_equation[0]
	inputs = split_equation[1]

	factor_multipliers = []
	factor_inners = []
	new_terms = []

	new_eqn = inputs
	#find parenthesis
	if "(" and ")" in inputs:
		#print("Found")
		beginning = new_eqn.find("(")
		end = new_eqn.find(")")
		factor_inners.append(new_eqn[beginning+1:end])
		new_eqn = new_eqn[:beginning]+"$"+new_eqn[end+1:]
		#print("After substituition of $")
		#print(new_eqn)
	new_eqn=new_eqn.split("+")
	#find multipliers
	for term in new_eqn:
		if "$" in term:
			place=term.find("$")
			factor_multipliers.append(term[:place]+term[place+1:])
		else:
			new_terms.append(term)
	#print("After finding multipliers")
	#print(factor_multipliers)
	#print(new_terms)
	#expand
	for i in range(len(factor_inners)):
		terms = factor_inners[i]
		#print("before for loop")
		#print(terms)
		terms = terms.split("+")
		#print(terms)
		for term in terms:
			#print("Term {}".format(term))
			new_terms.append(term+factor_multipliers[i])
			#print(new_terms)
	new_equation = output +"="+ "+".join(new_terms)
	return new_equation

def get_most_useful(dictionary):
	entries = list(dictionary.keys())
	length_entry = []
	for i in range(len(entries)):
		length_entry.append(len(entries[i]))
	values_of = list(dictionary.values())

	print("In most useful: entries, lengths of such, values of, and values updated")
	print(entries)
	print(length_entry)
	print(values_of)

	#make it so that values is how many hits
	if all(isinstance(item, int) for item in values_of): #check if it is of integers
		pass #this is for the case where we are using common_per_eqn aka a dictionary with values of how common
	else: #this is for when using mass terms, where values are a list
		for i in range(len(values_of)):
			values_of[i] = len(values_of[i])
	print(values_of)

	top_entry=""
	top_value=0
	for i in range(len(length_entry)):
		if length_entry[i] >= len(top_entry):
			if values_of[i] >= top_value:
				top_entry = entries[i]
				top_value = values_of[i]
	print("Most common entry: {}, with {} hits".format(top_entry, top_value))
	return top_entry
