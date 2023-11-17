import numpy as np
import math

#We need to be able to handle a lot of inputs
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]


#This function takes in a truth table of any size and returns an array of on-set minterms in [1,0,1] format
#********************************************************************************************************
def decomp_truthtable(truthtable):

    #Flatten the truth table    
    truthtable_copy=truthtable.copy()
    truthtable_copy=truthtable_copy.reshape(-1)
    num_inputs=int(math.log2(len(truthtable_copy)))

    #Array of minterms in [1,0,1] format
    minterms=np.array([])

    #Check if each element in the truth table is equal to 1
    for i in range(0,len(truthtable_copy)):
        if truthtable_copy[i]==1:

            #Need to make an array to build the minterm
            minterm=np.array([])

            #Copy i to work with the index so as not to corrupt it
            index=i

            #Decimal to Binary
            for j in range(0,num_inputs):
            
                if index % 2 ==1:
                    minterm=np.append(minterm,1)
                    index=(index-1)/2
                else:
                    minterm=np.append(minterm,0)
                    index=index/2

            #flip the minterm and add it to the list
            minterm=np.flip(minterm)
            minterms=np.append(minterms,minterm)

    #Reshape the minterm array from the 1xn array
    minterms=minterms.reshape(int(len(minterms)/num_inputs),int(num_inputs))

    return minterms
#********************************************************************************************************


#This function finds prime implicants from minterms using recursion
#********************************************************************************************************
def find_prime_implicants(prime_implicants, working_terms):

    #Don't want to alter original array
    working_terms_copy=working_terms.copy()

    #Need to keep track of minterms passed to a recursive call of this function
    next_working_terms=[]
    
    #Base case
    if len(working_terms)==0:
        return prime_implicants
    
    #Loop through each term
    for i in range (len(working_terms_copy)):

        matchfound=False #If this is still false after comparing with all other terms, then it is a prime implicant

        #Need to compare with every other term
        for j in range (0,len(working_terms_copy)):

            #compare the terms
            compare=0
            index_diff=0
            for k in range(0,len(working_terms_copy[j])):
                
                if working_terms_copy[i][k] == working_terms_copy[j][k]:
                    compare+=1
                else:
                    index_diff=k
           
           
            #If there is exactly one different input, we combine terms
            if (compare==len(working_terms_copy[i])-1):
                matchfound=True
                if i<j:
                    
                    term_to_add=working_terms_copy[i].copy()
                    term_to_add[index_diff]=-1
                    next_working_terms.append(term_to_add)
                    
            
            #If there is a duplicate, skip it and let the last copy be added
            elif(compare==len(working_terms_copy[i]) and i<j):
                matchfound=True

        #If a term has no expansion, it's a prime implicant
        if matchfound==False:
            prime_implicants.append(working_terms_copy[i])

    #Utilize recursion
    return find_prime_implicants(prime_implicants,next_working_terms)
#********************************************************************************************************



#This function generates a table to help find essential prime implicants
#********************************************************************************************************
def generate_coverage_table(prime_implicants,minterms):

    #Setup a coverage table
    coveragetable=np.zeros((len(prime_implicants),len(minterms)))
    
    #See which minterms are covered by each implicant
    for implicant in range(len(prime_implicants)):
        for minterm in range(len(minterms)):

            #Compare a minterm and a prime implicant
            compare=0
            for i in range(len(prime_implicants[implicant])):
                if prime_implicants[implicant][i]==minterms[minterm][i] or prime_implicants[implicant][i]==-1:
                    compare+=1
            
            #If each value of the minterm is covered, then this implicant covers
            if compare==len(prime_implicants[implicant]):
                coveragetable[implicant][minterm]=1
                
    return coveragetable
#********************************************************************************************************




#This function selects the essential prime implicants from the prime implicants given the minterms
#********************************************************************************************************
def essential_prime_implicants(prime_implicants,minterms):

    #Don't want to alter the contents of the original prime_implicants
    prime_implicants=prime_implicants.copy()

    #Array to store essential prime implicants
    essential_prime_implicants=[]
    
    #Generate a coverage table
    coveragetable=generate_coverage_table(prime_implicants,minterms)

    minterm_index=0
    while 1:

        #If the index is equal to the length, all "solo columns" have been taken care of, and we are done
        
        if minterm_index >= len(minterms):
            break
       
        #If there is a minterm that is only covered by one implicant...
        working_column= coveragetable[:,minterm_index]
        
        if sum(working_column)==1:
            #The implicant that covers it is a prime implicant
            index=np.where(coveragetable[:,minterm_index]==1)
            essential_prime_implicants.append(prime_implicants[index[0][0]])
            

            #Get rid of the minterms covered by the prime implicant
            minterms_covered_index=np.where(coveragetable[index[0][0],:]==1)
            minterms=np.delete(minterms,[minterms_covered_index[0]],0)    
            
            
            #Get rid of the prime implicant
            prime_implicants=np.delete(prime_implicants,index[0][0],0)

            #Generate a new coveragetable
            coveragetable=generate_coverage_table(prime_implicants,minterms)  
            minterm_index=0
        else:
            minterm_index=minterm_index+1


    return essential_prime_implicants,prime_implicants,minterms
#********************************************************************************************************

#This function builds and SOP strings
#********************************************************************************************************
def format(terms):

    sop=""

    #Special Case: Output=0
    if len(terms)==0:
        return "F= 0"


    #Special Case: Output=1
    specialcase=True
    for i in range(len(terms[0])):
        if terms[0][i] != -1:
            specialcase=False
    if specialcase==True:
        return "F= 1"

    #Build the string
    for i in range(len(terms)):
        for j in range(len(terms[0])):
            if terms[i][j] != -1:
                sop+=letters[j]
                if terms[i][j]==0:
                    sop+="'"

        #Don't need plus sign after last term
        if i != len(terms)-1:
            sop+="+"

    return sop
#********************************************************************************************************


#This function chooses the terms that will appear in the SOP
#********************************************************************************************************
def choose_terms(essential_prime_implicants,prime_implicants,minterms):

    terms=essential_prime_implicants.copy()

   
    #Keep track of which minterms still need to be covered
    minterms_remaining=minterms

    #Now, use prime implicants to cover the remaining minterms
    while len(minterms_remaining)>0:

        #This index will keep track of which prime implicant we are using
        prime_implicants_index=0


        #Generate a coveragetable
        coveragetable=generate_coverage_table(prime_implicants,minterms_remaining)

        #We want to know which prime implicant covers the most remaining minterms
        sumrows=[]
        for i in range(0, len(prime_implicants)):
            sumrows.append(sum(coveragetable[i,:]))
        max_minterms_covered=np.max(sumrows)
        prime_implicants_index=np.where(sumrows==max_minterms_covered)
        

        #Add this prime implicant to out list of terms
        terms.append(prime_implicants[prime_implicants_index[0][0]])

        #Remove the minterms covered
        minterms_covered_index=np.where(coveragetable[prime_implicants_index[0][0],:]==1)
        minterms_remaining=np.delete(minterms_remaining,[minterms_covered_index[0]],0) 

        #Remove the prime implicant
        prime_implicants=np.delete(prime_implicants,[prime_implicants_index[0][0]],0)

    return terms
#********************************************************************************************************


#This function combines everything into one step: making the SOP from the truthtable
#********************************************************************************************************
def minimized_sop(truthtable):
    working_terms=decomp_truthtable(truthtable)
    prime_implicants=[]
    prime_implicants=find_prime_implicants(prime_implicants,working_terms)
    results=essential_prime_implicants(prime_implicants, working_terms)
    results=choose_terms(results[0],results[1],results[2])
    results=format(results)
    return results
#********************************************************************************************************
    



    










#Testing
#********************************************************************************************************
truthtable = np.zeros((2,2,2))
truthtable[0][0][0]=1
truthtable[0][0][1]=1
truthtable[0][1][0]=1

truthtable[1][1][0]=1
truthtable[1][1][1]=1

print(minimized_sop(truthtable))

