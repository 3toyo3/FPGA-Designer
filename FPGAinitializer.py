import numpy as np
from os.path import exists
# This program sets up the FPGA based on user input

bits=['I'] #for bitstream

def main():
	bool newDesign = False
	print("Setting up FPGA...")

	#LUTS number
	while True:
		LUTS_num=input("How many LUTS?")
		if LUTS_num.isnumeric(): #check that is a number
			if int(LUTS_num)>0: #check that is greater than 0
				LUTS_num = int(LUTS_num)
				bits.append(LUTS_num) #for bitstream
				break
		print("Input must be a integer that is greater than 0.") #TODO check that this doesnt print if correct input
	#LUTS type
	while True:
		print("What type of LUTs are you using?")
		print("4: 4-input  6: 6-input")
		LUTS_type=input()
		if LUTS_type == '4': #TODO check that char comparison works for string input
			LUTS_type=4
			bits.append(LUTS_type)
			break
		elif LUTS_type == '6': #TODO line 24 comment
			LUTS_type=6
			bits.append(LUTS_type)
			break
		else:
			print("Invalid input. Please pick option A or B.")
	# connectivity
	while True:
		print("What kind of connectivity between the LUTs?")
		print("A: Fully-connected  B:Partially-connected(file required)")
		connect_type=input()
		if connect_type=='A': #TODO line 24 comment
			connect_type=1
			bits.append(connect_type)
			break
		elif connect_type=='B': #TODO line 24 comment
			connect_type=2
			bits.append(connect_type)
			#TODO File input here
			print("This program currently doesn't support partial connection between LUTS.")
		else:
			print("Invalid input. Please pick option A or B")
		#TODO specify connection
		#bits.append(connection_detail)
	# I/O
	while True:
		input_num=input("How many inputs?")
		output_num=input("How many outputs?")
		if input_num.isnumeric() && output_num.isnumeric(): #TODO Check that this is true
			if (int(input_num) > 0) && (output_num > 0): #TODO check that this works
				input_num = int(input_num)
				output_num = int(output_num)
				bits.append(input_num)
				bits.append(output_num)
				break
		print("Inputs must be integers greater than 0")
	# logic expressions
	while True:
		print("Please input blif file for the logic expressions")
		blif_file_path=input()
		if exists(blif_file_path):
			if blif_file_path[-5:]==".blif":
				break
			else:
				print("Please choose a blif file.")
			break
		else:
			print("File {} doesnt exist.".format(blif_file_path))
			print("Please try again.")
		#TODO append equations to bits
		#bits.append('F'+str(equations))
	# bitstream #TODO move this to front
	while True:
		print("Do you have a existing design in the form of a bitstream file?")
		print("A: Yes  B: No")
		bitstream_Exist=input()
		if bitstream_Exist=='A':
			#TODO get file
			newDesign = False
			break
		elif bitstream_Exist=='B':
			newDesign=True
			break
			#TODO make this enact the rest of the circuit
		else:
			print("Invalid input. Please pick option A or B.")

if __name_==""__main__":
	main()
