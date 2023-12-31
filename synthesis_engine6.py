from LUT6 import LUT6
import numpy as np
from minimize import *

LUTs=[]
first_unused_lut=0
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
lut_symbols = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
depth=1
ext_out=''

#This function initializes a desired number of LUTS
#*********************************************************************************************************************
def create_LUTs(num_luts):

    global LUTs
    global first_unused_lut

    if (num_luts >26):
        raise Exception("Too many LUTs")

    #Reset the LUTs
    LUTs=[]
    first_unused_lut=0
    

    #Create the LUTs
    for i in range(num_luts):
        LUTs.append(LUT6("",[],"",""))
#*********************************************************************************************************************


#This function prints information about the LUTs
#*********************************************************************************************************************
def print_LUTs():

    global LUTs
    global first_unused_lut
    global lut_symbols
   
    for i in range(first_unused_lut):
        print()
        print("LUT"+str(i))
        print(lut_symbols[i]+" = "+LUTs[i].name)
        print("External Output: "+LUTs[i].external_output)
        print()

#*********************************************************************************************************************

#This function displays details about a LUT at a certain index
#*********************************************************************************************************************
def print_LUT(index):
    print("FUNCTION IMPLEMENTED: "+LUTs[index].name)
    print("INPUTS: "+LUTs[index].inputs)
    print("OUTPUT: "+LUTs[index].output)
    print("External Output: "+LUTs[index].external_output)
#*********************************************************************************************************************

def get_LUT_global(lut_num):
	global LUTs
	return LUTs[lut_num]

def get_LUTS_global():
	global LUTs
	global first_unused_lut
	return LUTs[:first_unused_lut]

#This function returns the number of distinct variables in a string
#*********************************************************************************************************************
def num_distinct_variables(function):
    #Need to keep track of how many distinct variables were used
    count_variables=0
    variables_used=[]
    global first_unused_lut
    
    for i in range(len(function)):

        #If a letter has not been used yet, it is a distinct variable
        if (letters.count(function[i]) or lut_symbols.count(function[i])):
            
            

            conditional_prime=''
            if not(i==len(function)-1) and function[i+1]=="'":
                
                conditional_prime="'"
            if not(variables_used.count(function[i])) and not(variables_used.count(function[i]+"'")):
                count_variables+=1
                variables_used.append(function[i])#+conditional_prime)

    
    return count_variables,variables_used
#*********************************************************************************************************************

#This function returns True if a plus sign exists outside of any parenthesis
#*********************************************************************************************************************
def plus_sign_outside(function):
    
    open=0

    for i in range(len(function)):
        if function[i]=="(":
            open+=1
        if function[i]==")":
            open-=1
        if function[i]=="+" and open==0:
            return True
        
    return False
#*********************************************************************************************************************


#This function splits up an expression by plus signs that lie outside of parenthesis
#*********************************************************************************************************************
def split_by_plus_sign(function):

    #We will retun an array of string of length j
    j=0
    split_function=[function]
    
    #Keep track of open parenthesis
    open=0

    #Keep track of location of last slice
    last_index=0

    #Loop through each character is the function
    for i in range(len(function)):
        
        #Handling of parenthesis
        if function[i]=="(":
            open+=1
        if function[i]==")":
            open-=1

        #Split the function at plus signs outside of parenthesis
        if function[i]=="+" and open==0:
            split_function.append(function[i+1:])
            split_function[j]=function[last_index:i]
            last_index=i+1
            j+=1
    
    return split_function
#*********************************************************************************************************************


#This function splits up a expression by the outermost layer of parenthesis
#*********************************************************************************************************************
def split_by_parenthesis(function):
    #We will retun an array of string of length j
    j=0
    split_function=[function]
    
    #Keep track of open parenthesis
    open=0

    #Keep track of location of last slice
    last_index=0

    #Handle when the first char is an opening parenthesis
    if function[0]=="(":
        function=function[1:]
        open+=1
        

    #Loop through each character is the function
    for i in range(len(function)):
        
       
        if function[i]=="(":
             
            #Handling of the case where the fucntion begins with inputs and not a parenthesis
            if open==0 and not(i==0) and len(split_function)==1:
                split_function.append(function[i+1:])
                split_function[j]=function[last_index:i]
                last_index=i+1
                j+=1

            open+=1

        if function[i]==")":
            open-=1

            #If this is the end of the function, just take the closing parenthesis off
            if(open==0) and i==len(function)-1:
                split_function[j]=split_function[j][0:len(split_function[j])-1]

            #If this is not the end of the function, slice appropriately
            if open==0 and not(i==len(function)-1):
                split_function.append(function[i+2:])
                split_function[j]=function[last_index:i]
                last_index=i+2
                j+=1
            
    return split_function
#*********************************************************************************************************************

#This function takes in a factored string and splits it into functions of 4 variables, assigning to the LUTs
#*********************************************************************************************************************
def split(function):


    global LUTs
    global first_unused_lut
    global depth
    global ext_out

    if function[1]=="=":
        depth=1
        ext_out=function[0]
        function=function[2:]


    #Base case: The function only conists of one input
    if num_distinct_variables(function)[0]==1:
        return ""
    
    #Base case: function contains 6 inputs, can now implement on LUT
    elif num_distinct_variables(function)[0]<=6:
        
        #Build the LUT
        LUTs[first_unused_lut].name=function
        LUTs[first_unused_lut].inputs= num_distinct_variables(function)[1]
        LUTs[first_unused_lut].output=str(first_unused_lut)
        if depth==1:
            LUTs[first_unused_lut].external_output=ext_out

        #Now move to the next LUT
        first_unused_lut+=1

        #Return the name of the LUT in place of the function it implemented
        return(lut_symbols[first_unused_lut-1])
    

    #If the function has a plus sign outside all parenthesis
    elif plus_sign_outside(function):
        
        
        #Divide the function up by plus signs
        split_function=split_by_plus_sign(function)

        
        

        #Want to know the number of inputs per slice
        inputs_per_slice=np.zeros(len(split_function))
        for i in range(len(split_function)):
            inputs_per_slice[i]=num_distinct_variables(split_function[i])[0]
            

            #First condition: If one of the slices has exactly 6 inputs
            if inputs_per_slice[i]==6:
                
                
                #rebuild the function
                next_function=""
                for j in range(len(split_function)):
                    
                    
                    if i>j:
                        next_function+=split_function[j]+"+"
                    elif i==j:
                        depth+=1
                        next_function+=split(split_function[j])
                        depth-=1
                    if j>i:
                        
                        next_function+="+"+split_function[j]

                
                return split(next_function)
                
        
        #Second condition: can we build a 6 input LUT from multiple slices?
        for i in range(2**(len(inputs_per_slice))):
            temp_code=str(bin(i))
            temp_code=temp_code[2:]
            code=""
            for j in range(0,len(inputs_per_slice)-len(temp_code)):
                code+='0'
            code+=temp_code
            

            sum=0
            six_input_function=""
            rest_of_function=""
            for j in range(len(code)):
                if code[j]=="1":
                    sum+=inputs_per_slice[j]
                    six_input_function+=split_function[j]+'+'
                else:
                    rest_of_function+=split_function[j]+'+'

            if sum==6:
                
                six_input_function=six_input_function[:len(six_input_function)-1]
                depth+=1
                temp=split(six_input_function)
                depth-=1
                
                return split(rest_of_function+temp)
                
        
        #Third Condition: Are there any slices greater than 6 inputs that can be broken up?
        for i in range(len(inputs_per_slice)):
            if inputs_per_slice[i]>6:

                #rebuild the function
                next_function=""
                for j in range(len(split_function)):
                    
                    
                    if i>j:
                        next_function+=split_function[j]+"+"
                    elif i==j:
                        depth+=1
                        next_function+=split(split_function[j])
                        depth-=1
                    if j>i:
                        
                        next_function+="+"+split_function[j]

                return split(next_function)


        #Fourth Condition: The sum of inputs_per_slice is less than 6
        if np.sum(inputs_per_slice) < 6:
            LUTs[first_unused_lut].name=function
            LUTs[first_unused_lut].inputs= num_distinct_variables(function)[1]
            LUTs[first_unused_lut].output=str(first_unused_lut)

            #Now move to the next LUT
            first_unused_lut+=1
            depth=0
            return split(lut_symbols[first_unused_lut-1])

        #Take the slice with the greatest number of inputs and build a LUT from that
        max=np.max(inputs_per_slice)
        index=np.where(inputs_per_slice==max)
        index=index[0][0]
        next_function=""

        LUTs[first_unused_lut].name=split_function[index]
        LUTs[first_unused_lut].inputs= num_distinct_variables(split_function[index])[1]
        LUTs[first_unused_lut].output=str(first_unused_lut)

        #Now move to the next LUT
        first_unused_lut+=1

        #Return the name of the LUT in place of the function it implemented

        for j in range(len(split_function)): 
                    
            if index>j:
                next_function+=split_function[j]+"+"
            elif index==j:
                
                next_function+=lut_symbols[first_unused_lut-1]
            if j>index:
                        
                next_function+="+"+split_function[j]
            
        return split(next_function)


    #If the function doesn't have plus sign outside all parenthesis but has parenthesis
    elif not(function.find("(")==-1):
        
        
        #Divide the function up by plus signs
        split_function=split_by_parenthesis(function)
        
        

        #Want to know the number of inputs per slice
        inputs_per_slice=np.zeros(len(split_function))
        
        for i in range(len(split_function)):
            inputs_per_slice[i]=num_distinct_variables(split_function[i])[0]
            

            #First condition: If one of the slices has exactly 6 inputs
            if inputs_per_slice[i]==6:
                
                #rebuild the function
                next_function=""
                for j in range(len(split_function)):
                    
                    
                    if i>j:
                        next_function+="("+split_function[j]+")"
                    elif i==j:
                        depth+=1
                        next_function+="("+split(split_function[j])+")"
                        depth-=1
                    if j>i:
                        
                        next_function+="("+split_function[j]+")"

                
                return split(next_function)
                
        
        #Second condition: can we build a 6 input LUT from multiple slices?
        for i in range(2**(len(inputs_per_slice))):
            temp_code=str(bin(i))
            temp_code=temp_code[2:]
            code=""
            for j in range(0,len(inputs_per_slice)-len(temp_code)):
                code+='0'
            code+=temp_code
           

            sum=0
            six_input_function=""
            rest_of_function=""
            for j in range(len(code)):
                if code[j]=="1":
                    sum+=inputs_per_slice[j]
                    six_input_function+="("+split_function[j]+")"
                else:
                    rest_of_function+="("+split_function[j]+")"

            if sum==6:
                six_input_function=six_input_function[:len(six_input_function)]
                depth+=1
                temp=split(six_input_function)
                depth-=1
                return split(rest_of_function+"("+temp+")")
                
        
        #Third Condition: Are there any slices greater than 6 inputs that can be broken up?
        for i in range(len(inputs_per_slice)):
            if inputs_per_slice[i]>6:

                #rebuild the function
                next_function=""
                for j in range(len(split_function)):
                    
                    
                    if i>j:
                        next_function+="("+split_function[j]+")"
                    elif i==j:
                        depth+=1
                        next_function+="("+split(split_function[j])+")"
                        depth-=1
                    if j>i:
                        
                        next_function+="("+split_function[j]+")"

                
                return split(next_function)
        
        #Take the slice with the greatest number of inputs and build a LUT from that
        max=np.max(inputs_per_slice)
        index=np.where(inputs_per_slice==max)
        index=index[0][0]
        next_function=""

        LUTs[first_unused_lut].name=split_function[index]
        LUTs[first_unused_lut].inputs= num_distinct_variables(split_function[index])[1]
        LUTs[first_unused_lut].output=str(first_unused_lut)

        #Now move to the next LUT
        first_unused_lut+=1

        #Return the name of the LUT in place of the function it implemented

        for j in range(len(split_function)): 
                    
            if index>j:
                next_function+=split_function[j]+"+"
            elif index==j:
                
                next_function+=lut_symbols[first_unused_lut-1]
            if j>index:
                        
                next_function+="+"+split_function[j]
            
        
          
        return split(next_function)
               

    #If there's no addition signs and no parenthesis, we are dealing with a "blob" of inputs
    #This can be fixed just by adding parenthesis around the inputs
    next_function="("
    for i in range(len(function)):
        if i==len(function)-1 and not(function[i]=="'"):
            next_function+=function[i]+")"
        elif (letters.count(function[i]) or lut_symbols.count(function[i])):
            next_function+=function[i]
            if function[i+1]=="'":
                next_function+="'"
            next_function+=")("
    if next_function[-1]=="(":
        next_function=next_function[:len(next_function)-1]
    
    depth=0
    return(split(next_function))
#*********************************************************************************************************************


#This function returns an array as a string
#*********************************************************************************************************************
def to_string(array):
    return_string=''
    for i in range(len(array)):
        return_string+=str(int(array[i]))
    return return_string
#*********************************************************************************************************************

#This function creates the bitstream for the virtual FPGA
#*********************************************************************************************************************
def write_bitstream(filename):
    global LUTs
    global first_unused_lut

    #Initialize the bitstream
    bitstream=''

    #Walk through each LUT 
    for i in range(first_unused_lut):

        #First handle the code for the variables
        variables=LUTs[i].inputs

        #52 bits for external inputs and their complements, 26 bits for internal connections
        inputcode=np.zeros(78,np.int8)
        
        
        #Walk through each variable and build the correct bitstream
        for j in range(len(variables)):

            try:
                index=letters.index(variables[j][0])
            except ValueError:
                index=-1

            if not(index == -1):
                index*=2
                if len(variables[j]) >1 and variables[j][1]=="'":
                    index+=1
                
            else:
                index=52+lut_symbols.index(variables[j][0])
        
            inputcode[index]=1

            #Add to the bitstream
            bitstream+=to_string(inputcode)
            

            inputcode=np.zeros(78,np.int8)
            #bitstream+=' '
        for j in range(6-len(variables)):
            inputcode=np.zeros(78,np.int8)
            bitstream+=to_string(inputcode)

        
        
      
        
        #Now handle the output of the LUT

        #Translate to a format that Ysatis' function accepts
        
        function=translate(LUTs[i].inputs,LUTs[i].name)
        #print(function)
        #distribute(function)

        #Build the truth table
        function_temp=lut_symbols[i]+"="+function
        while(1):
            
            try:
                index=function_temp.index("(")
            except ValueError:
                index=-1
            if(index==-1):
                break
            function_temp=distribute(function_temp)
        
        
        array=eqnToArray(function_temp)
        

        #Add to the bitstream
        array=array.flatten()
        
        repeat=64/len(array)
        for i in range(int(repeat)):
            bitstream+=to_string(array)

    
        

    #Take care of output connections
    for i in range(first_unused_lut):
        code=np.zeros(26,np.int8)
        if not(LUTs[i].external_output==''):
            index=letters.index(LUTs[i].external_output)
            code[index]=1
        bitstream+=to_string(code)
        
    
        
    #Finally, write the bitstream
    f = open(filename, "w")
    f.write(bitstream)
    f.close()
#*********************************************************************************************************************
    


#This function build the LUTs from the bitstream
#*********************************************************************************************************************
def build_from_bitstream(filename):

    global LUTs
    global first_unused_lut

    #Read the bitstream
    f = open(filename, "r")
    bitstream= f.read()
    f.close()
    
    #Make the LUTs
    num_luts= int(len(bitstream)/558)
    
    create_LUTs(num_luts)

    first_unused_lut=num_luts
   
    #Walk through each LUT
    for i in range(num_luts):
        
        
        
        #Get the working section of the bitstream
        working_bitstream=bitstream[i*532:i*532+10000]

        for var in range(6):
            
            var_working_bitstream=working_bitstream[var*78:var*78+78]
            

            for j in range(len(var_working_bitstream)):
                if var_working_bitstream[j]=='1':
            
                
                    #If the input is one of the external inputs
                    if j<52:

                        index=0
                        conditional_prime=""
                        if j % 2==0:
                            index= j/2
                        else:
                            index=(j-1)/2
                            conditional_prime="'"
                    
                    
                        LUTs[i].inputs.append(letters[int(index)]+conditional_prime)
                
                    #If the input comes from another LUT
                    else:
                        index=j-52
                        LUTs[i].inputs.append(lut_symbols[int(index)])

        #Now rebuild the functions
        
        #Get the working bitstream
        working_bitstream=bitstream[532*i+468:532*i+468+64]
        
        
        
        #Truth table that will be passed to minimized_SOP
        truthtable = np.zeros((2,2,2,2,2,2))
        
        for j in range(64):
            truthtable[dec_to_binary_6bit(j)[5]][dec_to_binary_6bit(j)[4]][dec_to_binary_6bit(j)[3]][dec_to_binary_6bit(j)[2]][dec_to_binary_6bit(j)[1]][dec_to_binary_6bit(j)[0]]=int(working_bitstream[j])
        
        function=minimized_sop(truthtable)
        

        
        
        #Assign the function to the LUT
        LUTs[i].name=translate_reverse(LUTs[i].inputs,function)


        #Finally rebuild the output connections
        working_bitstream=bitstream[532*num_luts+i*26:532*num_luts+i*26+26]
        for j in range(len(working_bitstream)):
            if working_bitstream[j] =="1":
                LUTs[i].external_output=letters[j]


#*********************************************************************************************************************        
        
        
#This function will convert to functions to A,B,C,D for the purposes of truth table generation
#*********************************************************************************************************************
def translate(inputs,function):
    
    l_symbols=["0","1","2","3","4","5"]
    temp_lut_symbols=l_symbols
    
    

    temp_inputs=inputs
    
    #for i in range(len(temp_inputs)):
        #for j in range(i,len(temp_inputs)):
            #if temp_inputs[i]+"'"==temp_inputs[j]:
                #temp=inputs[i]
                #inputs[i]=inputs[j]
                #inputs[j]=temp

                #temp=temp_lut_symbols[i]
                #temp_lut_symbols[i]=temp_lut_symbols[j]
                #temp_lut_symbols[j]=temp

    
    
                

    for i in range(len(inputs)):
        
        function=function.replace(inputs[i],temp_lut_symbols[i+6-len(inputs)])
        
        
    
    for i in range(len(inputs)):
        function=function.replace(l_symbols[i+6-len(inputs)],letters[i+6-len(inputs)])
        
  
    
    return function
#*********************************************************************************************************************

#This function is necessary for decoding LUT output from the bitstream
#*********************************************************************************************************************
def translate_reverse(inputs,function):
    
    l_symbols=["0","1","2","3","4","5"]
    
    for i in range(len(inputs)-1,-1,-1):
        function=function.replace(letters[i+6-len(inputs)],l_symbols[i+6-len(inputs)])
    for i in range(len(inputs)-1,-1,-1):
        function=function.replace(l_symbols[i+6-len(inputs)],inputs[i])
        
    return function
#*********************************************************************************************************************         

#Decimal to Binary
#*********************************************************************************************************************
def dec_to_binary_6bit(num):
    code0=0
    code1=0
    code2=0
    code3=0
    code4=0
    code5=0

    if num%2==1:
        code0=1
        num -=1
    num /=2
    if num%2==1:
        code1=1
        num -=1
    num /=2
    if num%2==1:
        code2=1
        num -=1
    num /=2
    if num%2==1:
        code3=1
        num -=1
    num /=2
    if num%2==1:
        code4=1
        num -=1
    num /=2
    if num%2==1:
        code5=1
    
    return code0,code1,code2,code3,code4,code5
#*********************************************************************************************************************
        

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


 
#Main Function
#*********************************************************************************************************************
def assign_LUTs(functions,num_luts):
    global depth
    create_LUTs(num_luts)
    for i in range(len(functions)):
        depth=0
        split(functions[i])
    #print_LUTs()
#*********************************************************************************************************************    
        

#*********************************************************************************************************************


#Testing

#test=["F=AB+CD","G=AB'C+A'BD","H=A+B+C+D","J=A'BC'D+AB'CD'","K=A'B'C+ABC'+A'BCD","L=AB'C'D+A'BC+B'CD","M=AB'C+A'BC'D","N=A'BC+AC'D+B'CD'","O=ABD+A'B'CD'","P=A'BC'+AB'CD'"]
#test=["G=AB'+A'CD'E+FK(G+H+I')+I","F=A'+AB+CD'+E"]
#assign_LUTs(test,30)
#filename='bitstream.txt'
#write_bitstream(filename)
#build_from_bitstream(filename)
#print('**********************************************************************************************')
#print_LUTs()
