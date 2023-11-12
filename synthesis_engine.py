from LUT import LUT4
import numpy as np

LUTs=[]
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]

#This function initializes a desired number of LUTS
#*********************************************************************************************************************
def create_LUTs(num_luts):

    #Reset the LUTs
    LUTs=[]

    #Create the LUTs
    for i in range(num_luts):
        LUTs.append(LUT4("",[],""))
#*********************************************************************************************************************



#This function displays details about a LUT at a certain index
#*********************************************************************************************************************
def print_LUT(index):
    print("FUNCTION IMPLEMENTED: "+LUTs[index].name)
    print("INPUTS: "+LUTs[index].inputs)
    print("OUTPUT: "+LUTs[index].output)
#*********************************************************************************************************************


#This function takes in a factored string and splits it into functions of 4 variables, assigning to the LUTs
#*********************************************************************************************************************
def split(function,first_unused_LUT):

    #Need to keep track of how many distinct variables were used
    count_variables=0
    variables_used=[]

    #It will be important to keep track of unclosed parenthesis
    unclosed=0

    #Loop thorugh the function
    i=0
    while len(function)>0:

        #If a letter has not been used yet, it is a distinct variable
        if letters.count(function[i]) and not(variables_used.count(function[i])):
            count_variables+=1
        if function[i]=="(":
            unclosed+=1
        if function[i]==")":
            unclosed-=1
            print('reached')
        

        if (count_variables==4) or i==len(function):
            print()

    #Base case: function contains 4 or less variables, can now implement on LUT
    if count_variables<=4:
        LUTs[first_unused_LUT].name=function
        LUTs[first_unused_LUT].inputs=variables_used
        LUTs[first_unused_LUT].output='out'+str(first_unused_LUT)
        


    
        

#*********************************************************************************************************************


#Testing
num_luts=4
create_LUTs(4)
split("(A+B)(CD)",0)

