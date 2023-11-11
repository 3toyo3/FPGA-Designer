import numpy as np
from os.path import exists
from FPGAstructure import *
from logic_synthesizer import *

# This program sets up the FPGA based on user input

bits=['I'] #for bitstream

def check_file(filename):
	file_exists = exists(filename)
	return file_exists

def get_LUTS_num():
	while True:
		LUTS_num=input("How many LUTS?")
		if LUTS_num.isnumeric(): #check that is a number
			if int(LUTS_num)>0: #check that is greater than 0
				LUTS_num = int(LUTS_num)
				break
		print("Input must be a integer that is greater than 0.")
	bits.append(LUTS_num) #bits 1

def get_LUT_type():
	while True:
		print("What type of LUTs are you using?")
		print("4: 4-input  6: 6-input")
		LUTS_type=input()
		if LUTS_type == '4': #TODO check that char comparison works for string input
			LUTS_type=4
			break
		elif LUTS_type == '6': #TODO check that char comparison works for string input
			LUTS_type=6
			break
		else:
			print("Invalid input. Please pick option A or B.")
	bits.append(LUTS_num) #bits 2

def get_connectivty():
	while True:
		print("What kind of connectivity between the LUTs?")
		print("A: Fully-connected  B:Partially-connected(file required)")
		connect_type=input()
		if connect_type=='A': #TODO check that char comparison works for string input
			connect_type=9
			break
		elif connect_type=='B': #TODO check that char comparison works for string input
			connect_type=2
			# TODO file
			print("This program currently doesn't support partial connection between LUTS.")
			break
		else:
			print("Invalid input. Please pick option A or B")
	#TODO make more specific?
	bits.append(connect_type) #bits 3

def get_IO():
	while True:
		input_num=input("How many inputs?")
		output_num=input("How many outputs?")
		if input_num.isnumeric() && output_num.isnumeric(): #TODO Check that this is true
			if (int(input_num) > 0) && (output_num > 0): #TODO check that this works
				input_num = int(input_num)
				output_num = int(output_num)
				bits.append(input_num) #bits 5
				bits.append("Input list") #bits 6
				bits.append(output_num) #bits 7
				bits.append("Output list") #bits 8
				break
		print("Inputs must be integers greater than 0")

def get_equations(): #TODO expand into optimizing and stuff
	while True:
		print("Please input blif file for the logic expressions")
		blif_file_path=input()
		if exists(blif_file_path):
			if blif_file_path[-5:]==".blif":
				break
				#TODO craft equations here
			else:
				print("Please choose a blif file.")
			break
		else:
			print("File {} doesnt exist.".format(blif_file_path))
			print("Please try again.")
		#TODO append equations to bits
		#bits.append('F'+str(equations)) #bits 8		

def output_prompt():
	print("FPGA Display Options:")
	print("[1] Show all LUT assignments")
	print("[2] Show specific LUT assignment")
	print("[3] Show internal connections")
	print("[4] Show external input assignments")
	print("[5] Show external output assignments")
	print("[6] Craft bitstream of current FPGA")
	print("[7] Show resource allocation")
	#print("[8] Show FPGA visually")
	print("[h] Show this prompt again")
	print("[q] Quit program")

def main():	
	bool useBitstream = False
	print("Setting up FPGA...")
	
	while True:
		print("Do you have a existing design in the form of a bitstream file?")
		print("A: Yes  B: No")
		bitstream_Exist=input()
		if bitstream_Exist=='A':
			useBitstream=True
			while True:
				bitstream_file=input("Please put filename of bitstream.")
				if check_file(bitstream_file):
					break	
				else: 
					print("Sorry that file doesn't seem to exist")
		elif bitstream_Exist=='B':
			print("Creating a new FPGA...")
			break
		else:
			print("Invalid input. Please pick option A or B.")
	
	if useBitstream:
		bits = first line #turn to list
	
	# MAKE NEW FPGA via USER INPUT
	else:
		get_LUTS_num()
		get_LUTS_type()
		get_connectivity()
			#TODO specify connection from bit[3]
		get_IO()
		get_equations()
		#TODO construct FPGA via connections, optimization, and putting equations in order of where they go
	
	# Construct FPGA
	# After this point, program assumes that optimized and connections are drawn
	LUTS_num = bits[1]
	LUTS_type = bits[2]
	connectivity = bits[4]
	input_num = bits[5]
	inputs = bits[6] #TODO turn to list
	output_num = bits[7]
	outputs = bits[8] #TODO turn to list
	equations = bits[9] #TODO turn to list

	fpgaDesign=FPGA(LUTS_num, connections, input_num, output_num)
	if len(equations) == len(LUTS_num): #check that can fit
		fpgaDesign.set_LUTS(equations)
	else:
		print("These equations cannot fit on the FPGA with {} LUTS".format(LUTS_num))
	#TODO then do inputs and outputs based on equations or on connections
	#check sizes before passing
	
	#User output
	key = 'i'
	output_prompt()
	while key != 'q':
		key=input("What do you want to do?")
		if key=='1':  # Show all LUT assignments
			LUTS = fpgaDesign.get_LUTS()
			for i in LUTS:
				print(i) # TODO format
		elif key == '2': # Show specific LUT assignment
			num = input("Which LUT do you want to see? 1-{}".format(LUTs_num))
			LUT = fpgaDesign.get_LUT(num)
			print(LUT)
		elif key == '3': # Show internal connections
			conn = fpgaDesign.get_connections()
			print(conn)
		elif key == '4': # Show external inputs
			ex_inputs = fpgaDesign.get_inputs()
			print(ex_inputs)
		elif key == '5': # Show external outputs
			ex_inputs = fpgaDesign.get_outputs()
			print(ex_outputs)
		elif key == '6': # Craft bitstream
			#TODO output file, choose name
			print("Saved as {}".format(name_here))
		elif key == '7': # Show resource allocation
		elif key == '8': # Show FPGA visually
		elif key == 'h':
			output_prompt()
		elif key == 'q': #quit
			break
		else:
			print("Enter h to see prompts again.")

if __name_==""__main__":
	main()
