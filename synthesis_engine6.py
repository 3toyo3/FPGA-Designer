from LUT6 import LUT6
import numpy as np

LUTs=[]
first_unused_lut=0
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]
lut_symbols = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n"]

#This function initializes a desired number of LUTS
#*********************************************************************************************************************
def create_LUTs(num_luts):

    global LUTs
    global first_unused_lut

    #Reset the LUTs
    LUTs=[]
    first_unused_lut=0
    

    #Create the LUTs
    for i in range(num_luts):
        LUTs.append(LUT6("",[],""))
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
        print()

#*********************************************************************************************************************

#This function displays details about a LUT at a certain index
#*********************************************************************************************************************
def print_LUT(index):
    print("FUNCTION IMPLEMENTED: "+LUTs[index].name)
    print("INPUTS: "+LUTs[index].inputs)
    print("OUTPUT: "+LUTs[index].output)
#*********************************************************************************************************************

def get_LUT_global(lut_num):
	global LUTs
	return LUTs[lut_num]

def get_LUTS_global():
	global LUTs
	return LUTs

#This function returns the number of distinct variables in a string
#*********************************************************************************************************************
def num_distinct_variables(function):
    #Need to keep track of how many distinct variables were used
    count_variables=0
    variables_used=[]
    global first_unused_lut

    for i in range(len(function)):

        #If a letter has not been used yet, it is a distinct variable
        if (letters.count(function[i]) or lut_symbols.count(function[i])) and not(variables_used.count(function[i])):
            count_variables+=1
            variables_used.append(function[i])
    
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

#This function takes in a factored string and splits it into functions of 6 variables, assigning to the LUTs
#*********************************************************************************************************************
def split(function):


    global LUTs
    global first_unused_lut



    #Base case: The function only conists of one input
    if num_distinct_variables(function)[0]==1:
        return ""
    
    #Base case: function contains 6 inputs, can now implement on LUT
    elif num_distinct_variables(function)[0]==6:
        
        #Build the LUT
        LUTs[first_unused_lut].name=function
        LUTs[first_unused_lut].inputs= num_distinct_variables(function)[1]
        LUTs[first_unused_lut].output=str(first_unused_lut)

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
                        next_function+=split(split_function[j])
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
                return split(rest_of_function+split(six_input_function))
                
        
        #Third Condition: Are there any slices greater than 6 inputs that can be broken up?
        for i in range(len(inputs_per_slice)):
            if inputs_per_slice[i]>6:

                #rebuild the function
                next_function=""
                for j in range(len(split_function)):
                    
                    
                    if i>j:
                        next_function+=split_function[j]+"+"
                    elif i==j:
                        next_function+=split(split_function[j])
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
            return lut_symbols[first_unused_lut-1]

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
            
        
        print(next_function)
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
                        next_function+="("+split(split_function[j])+")"
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
                return split(rest_of_function+"("+split(six_input_function)+")")
                
        
        #Third Condition: Are there any slices greater than 6 inputs that can be broken up?
        for i in range(len(inputs_per_slice)):
            if inputs_per_slice[i]>6:

                #rebuild the function
                next_function=""
                for j in range(len(split_function)):
                    
                    
                    if i>j:
                        next_function+="("+split_function[j]+")"
                    elif i==j:
                        next_function+="("+split(split_function[j])+")"
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
    
    return(split(next_function))
#*********************************************************************************************************************


    
        

#*********************************************************************************************************************


#Testing
create_LUTs(8)
print(split("AB'(C+D)+A(D'+E'FG)+AB'(I+JK)"))
print_LUTs()
print(LUTs[5].output)
