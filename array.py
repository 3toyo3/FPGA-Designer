from logic_synthesizer import dont_cares

def eqnToArray(eqn)
	print(eqn)
	seperate_formula=eqn.split("=")
	eqn_terms=seperate_formula[1]
	print(seperate_formula)
	output=seperate_formula[0]

	unique_inputs=[]
	for char in eqn:
		if char not in unique_inputs and char.isalpha():
			if char not in output:
				unique_inputs.append(char)
	#inputs=tuple(unique_inputs)

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
			#print("Dont care")
			new_indices = dont_cares(truth_value)
			#print(new_indices)
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
			print("{} term marked as true".format(indice))
	return truthtable
