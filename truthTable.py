import numpy as np
# Takes string of equation and outputs a truth table as a MD array

def eqnToArray(eqn):
	#print(eqn)
	seperate_formula=eqn.split("=")
	eqn_terms=seperate_formula[1]
	#print(seperate_formula)
	output=seperate_formula[0]

	unique_inputs=[]
	for char in eqn:
		if char not in unique_inputs and char.isalpha():
			if char not in output:
				unique_inputs.append(char)
	inputs=tuple(unique_inputs)

	#make truth table
	size=len(inputs)
	truthtable = np.zeros([2]*size) #make array based on num of inputs
	terms = eqn_terms.split('+')
	true_indices = []
	for term in terms:
		#print(true_indices)
		truth_value = []
		#print(term)
		for i in range(len(inputs)):
			truth_value.append('*') #initialize array with *
		for i in range(len(term)): #Find if ' or normal
			char = term[i]
			#print(char)
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
			#print("Dont care")
			new_indices = dont_cares(truth_value)
			#print(new_indices)
			for item in new_indices:
				#print("Item")
				#print(item)
				true_indices.append(tuple(item))
		else:
			#print(truth_value)
			#print(item)
			new_indices = truth_value
			true_indices.append(tuple(new_indices))
	for indice in np.ndindex(truthtable.shape):
		if indice in true_indices:
			truthtable[indice] = 1
			#print("{} term marked as true".format(indice))
	return truthtable

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

#print("See me?")
