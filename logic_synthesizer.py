import numpy as np
from minimize import *
from truthTable import *

# Takes a file with list of equations and outputs a dictionary of each equation represented as a MD array
def textToArray(equations):
	names = {}
	for eqn in equations:
		seperate_formula=eqn.split("=")
		eqn_terms=seperate_formula[1]
		output=seperate_formula[0]

		#store variables in unique string
		equation_ID=[output]
		unique_inputs=[]
		for char in eqn:
			if char not in unique_inputs and char.isalpha():
				if char not in output:
					unique_inputs.append(char)
		equation_ID=equation_ID+unique_inputs
		equation_ID=",".join(equation_ID)

		truthtable = eqnToArray(eqn)
		names[equation_ID]=truthtable
		print("Finished {}".format(eqn))
	return names

#Takes a dictionary with equations' MD arrays, and outputs list of minimized equations, references miminize.py
def minimize_equations(names):
	equations=[]
	for entry in names:
		truthtable=names[entry]
		new_string=minimized_sop(truthtable)
		#TODO Forcefully recreate equation 
		equations.append(entry[0] +"=" +new_string)
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
def substituition(equations): 
	eqns_list = []
	eqns_dict = {}
	#mutable
	for eqn in equations: #puts every equation in dictionary
		seperate_eqn = eqn.split("=")
		eqns_dict[seperate_eqn[0]]=seperate_eqn[1]

	#can I completely substitute an equation?
	# Entry 1 is what is going to be put it. IE: F = c+d
	# Entry 2 must have entry 1 within it G = ab+c+d
	for entry1 in eqns_dict:
		for entry2 in eqns_dict:
			if entry1 == entry2:
				pass
			else:
				equation_new = find_if_same(eqns_dict[entry1], eqns_dict[entry2], entry1)
				eqns_dict[entry2] = equation_new
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
	else:
		eqn1 = eqn1.split("+")
		eqn2 = eqn2.split("+")
		common=[term in eqn2 for term in eqn1]
		if all(common):
			for term in eqn1:
				eqn2.remove(term)
			eqn2.append(eq1_out) #equation1 output
		eqn_new = '+'.join(eqn2)
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

	#Remove any equations that cant be factored
	eqns_to_remove = [key for key, value in common_literals_per_eqn.items() if isinstance(value, dict) and not value]
	for eqn in eqns_to_remove:
    		common_literals_per_eqn.pop(eqn)

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

	# Factor common equations
	if len(mass_common_terms)>0:
		factorsExist = True
	else:
		factorsExist = False
	while factorsExist:
		most_common_term=get_most_useful(mass_common_terms)
		common_equations = mass_common_terms.pop(most_common_term)

		#Check if the most_common_to_be_factor in other could-be-factors and removes
		for entry in mass_common_terms: #TODO check this w single?
			entry_equations = tuple(mass_common_terms[entry])
			eqn_dupes = set(entry_equations)
			for eqn in entry_equations:
				if eqn in common_equations:
					eqn_dupes.remove(eqn)
			mass_common_terms[entry]=eqn_dupes

		#Remove any 1 term in dictionary
		not_mass_common_terms_anymore = [key for key, value in mass_common_terms.items() if len(value) == 1]
		for term in not_mass_common_terms_anymore:
			mass_common_terms.pop(term)

		#Factore each equation that was found to be common
		for eqn in common_equations:
			terms = eqns_dict[eqn]
			terms = factor(terms, most_common_term)
			eqns_dict[eqn] = terms
			common_literals_per_eqn.pop(eqn)

		#then repeat until either dictionary is empty or the remaining entries are 1 length
		#all_length_one = all(len(value) == 1 for value in mass_common_terms.values())
		if len(mass_common_terms) == 0:
			factorsExist = False

	# Factor non common by what makes the most impact
	for entry in common_literals_per_eqn:
		#Find most common term
		common_terms = common_literals_per_eqn[entry]
		most_common_term = get_most_useful(common_terms)

		#Factor
		terms = eqns_dict[entry]
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

    #check each term to another for common letters
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            common_set = set(words[i]) & set(words[j])
            common_letters.extend(common_set)

            #if multiple letters are common, then combine them
            common_sequence = ''.join(
                letter for letter in words[i] if letter in common_set
            )
            if common_sequence:
                common_series.append(common_sequence)

    common_series = list(set(common_series)) # remove dupes

    #check each term for if they have a common term, and if so, store which one
    #this is character based rather than segment based so to catch cases like ab in acb and adb
    for word in words:
        letters = list(word)
        for i in range(len(common_series)):
            common_term = common_series[i]
            common_letters = list(common_term)
            if all(item in letters for item in common_letters): #if all the letters are found, then the common term is in this term, therefore add to tally
            	if len(common_letters) != len(letters): #make sure cube free
                	if common_term in common_tally:
                		common_tally[common_term] = common_tally[common_term] + 1
                	else:
                    		common_tally[common_term] = 1
    solo = []
    for entry in common_tally:
    	if common_tally[entry] == 1:
    		solo.append(entry)
    for entry in solo:
    	common_tally.pop(entry)
    return common_tally

#Takes an list of terms and common term, and factors it out and outputs it as a new string
def factor(terms, common):
	new_terms = []
	new_terms_no_factor = []

	chars_to_check = list(common)
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
	new_terms = [char for char in new_terms if char] #remove emptys
	working_str = '+'.join(new_terms)
	working_str = common+"("+working_str+")"
	if len(new_terms_no_factor) != 0:
		working_str = working_str + "+"
	working_str = working_str + "+".join(new_terms_no_factor)
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
		beginning = new_eqn.find("(")
		end = new_eqn.find(")")
		factor_inners.append(new_eqn[beginning+1:end])
		new_eqn = new_eqn[:beginning]+"$"+new_eqn[end+1:]
	new_eqn=new_eqn.split("+")
	#find multipliers
	for term in new_eqn:
		if "$" in term:
			place=term.find("$")
			factor_multipliers.append(term[:place]+term[place+1:])
		else:
			new_terms.append(term)
	#expand
	for i in range(len(factor_inners)):
		terms = factor_inners[i]
		terms = terms.split("+")
		for term in terms:
			new_terms.append(term+factor_multipliers[i])
	new_equation = output +"="+ "+".join(new_terms)
	return new_equation

def get_most_useful(dictionary):
	entries = list(dictionary.keys())
	length_entry = []
	for i in range(len(entries)):
		length_entry.append(len(entries[i]))
	values_of = list(dictionary.values())


	#make it so that values is how many hits
	if all(isinstance(item, int) for item in values_of): #check if it is of integers
		pass #this is for the case where we are using common_per_eqn aka a dictionary with values of how common
	else: #this is for when using mass terms, where values are a list
		for i in range(len(values_of)):
			values_of[i] = len(values_of[i])

	top_entry=""
	top_value=0
	for i in range(len(length_entry)):
		if length_entry[i] >= len(top_entry):
			if values_of[i] >= top_value:
				top_entry = entries[i]
				top_value = values_of[i]
	return top_entry

