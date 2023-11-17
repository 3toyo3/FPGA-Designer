import numpy as np
import sys #exit
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
		LUTS_num=input("Number of LUTS: ")
		if LUTS_num.isnumeric():
			if int(LUTS_num)>0:
				LUTS_num = int(LUTS_num)
				break
		print("Input must be a integer that is greater than 0.")
	bits.append(LUTS_num) #bits 1

def get_LUT_type():
	while True:
		print("What type of LUTs are you using?")
		print("4: 4-input  6: 6-input")
		LUTS_type=input()
		if LUTS_type == '4':
			LUTS_type=4
			break
		elif LUTS_type == '6':
			LUTS_type=6
			break
		else:
			print("Invalid input. Please pick option A or B.")
	bits.append(LUTS_type) #bits 2

def get_connectivity():
	while True:
		print("What kind of connectivity between the LUTs?")
		print("A: Fully-connected  B:Partially-connected (file required)")
		connect_type=input()
		if connect_type.upper()=='A':
			connect_type=9
			break
		elif connect_type.upper()=='B':
			connect_type=2
			print("This program currently doesn't support partial connection between LUTS.") #TODO erase once done
			break
		else:
			print("Invalid input. Please pick option A or B")
	bits.append(connect_type) #bits 3

def specify_connectivity(connect_type): #TODO this function
	if connect_type == 2:
		while True:
			filename = input("File Name: ")
			if check_file(filename):
				with open(filename, 'r') as file: #TODO fix this assumption
					line = file.readline() #must be on one line
				#TODO any processing
				connections = line
				break
			else:
				print("That file doesn't seem to exist.")
	else:
		print("Fully connected")
		connections = 1
		#TODO Fully connected
		#Specify here
	bits.append(connections) #bit 4

def get_IO():
	while True:
		input_num=input("How many inputs? ")
		output_num=input("How many outputs? ")
		if input_num.isnumeric() & output_num.isnumeric():
			if (int(input_num) > 0) & (int(output_num) > 0):
				input_num = int(input_num)
				output_num = int(output_num)
				bits.append(input_num) #bits 5
				bits.append("0") #bits 6
				bits.append(output_num) #bits 7
				bits.append("0") #bits 8
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
		#gather, minimize, and stuff optimize
	bits.append('F'+str(equations)) #bits 8  # TODO turn , to .
	#from here also append the I/O and connections again
	#TODO make sure before minimizing to convert case. also make sure output of minimizer puts out the correct variables of the equation

def output_prompt():
	print("FPGA Display Options:")
	print("[1] Show all LUT assignments")
	print("[2] Show specific LUT assignment")
	print("[3] Show internal connections")
	print("[4] Show external input assignments")
	print("[5] Show external output assignments")
	print("[6] Craft bitstream of current FPGA")
	print("[7] Show resource allocation")
	#print("[8] Show FPGA visually") #TODO decomment once done
	print("[h] Show this prompt again")
	print("[q] Quit program")

def main():
	global bits
	useBitstream = False
	print("Setting up FPGA...")

	while True:
		print("Do you have a existing design in the form of a bitstream file?")
		print("A: Yes  B: No")
		bitstream_Exist=input()
		if bitstream_Exist.upper()=='A':
			useBitstream=True
			while True:
				bitstream_file=input("Bitstream Filename: ")
				if check_file(bitstream_file):
					if bitstream_file[-5:] == ".bits":
						print("File exists.")
						break
					else:
						print("Make sure that your file is a .bits file")
				else:
					print("Sorry that file doesn't seem to exist")
		elif bitstream_Exist.upper()=='B':
			print("Creating a new FPGA...")
			break
		else:
			print("Invalid input. Please pick option A or B.")

	if useBitstream:
		with open(bitstream_file, 'r') as file:
			rawbits = file.read()
		rawbits = rawbits.strip('[]')
		rawbits = rawbits.split(',')
		if len(rawbits) == 10:
			bits = rawbits
		else:
			print("This bitstream was improperly formatted. Closing program.")
			sys.exit()

	# MAKE NEW FPGA via USER INPUT
	else:
		get_LUTS_num()
		get_LUT_type()
		get_connectivity()
		specify_connectivity(bits[3])
		get_IO()
		get_equations()

	# Construct FPGA
	# After this point, program assumes that optimized and connections are drawn
	LUTS_num = bits[1]
	LUTS_type = bits[2]
	connect_type = bits[3]
	connectivity = bits[4]
	input_num = bits[5]

	inputs = bits[6]
	#format inputs as a list
	inputs = inputs.strip('[]')
	inputs = inputs.replace(" ", "")
	inputs = inputs.split('.')

	output_num = bits[7]
	outputs = bits[8]
	#format outputs to a list
	outputs = outputs.strip('[]')
	outputs = outputs.replace(" ", "")
	outputs = outputs.split('.')

	equations = bits[9]
	#format equations into a list
	equations = equations.strip('[]')
	equations = equations[1:]
	equations = equations.replace(" ", "")
	equations = equations.split('.')

	fpgaDesign=FPGA(LUTS_num, connections, input_num, output_num)

	#Put LUTS
	if len(equations) <= int(LUTS_num):
		fpgaDesign.set_LUTS(equations)
	else:
		print("These equations cannot fit on the FPGA with {} LUTS".format(LUTS_num))
	#Put inputs
	if len(inputs) <= int(input_num):
		fpgaDesign.set_inputs(inputs)
	else:
		print("This program requires more inputs then necessary")
	#Put outputs
	if len(outputs) <= int(output_num):
		fpgaDesign.set_outputs(outputs)
	#TODO connections

	#User output
	key = 'i'
	output_prompt()
	while key != 'q':
		key=input("What do you want to do?")
		if key=='1':  # Show all LUT assignments
			LUTS = fpgaDesign.get_LUTS()
			for i in LUTS:
				if i[1] == ".":
					print("{}: Empty".format(i[0]))
				else:
					print("{}: {}".format(i[0],i[1]))
		elif key == '2': # Show specific LUT assignment
			num = input("Which LUT do you want to see? 1-{}".format(LUTs_num))
			LUT = fpgaDesign.get_LUT(num)
			if LUT == ".":
				print("LUT{} is empty".format(num))
			else:
				print(LUT)
		elif key == '3': # Show internal connections
			conn = fpgaDesign.get_connections()
			print(conn)
		elif key == '4': # Show external inputs
			ex_inputs = fpgaDesign.get_inputs()
			print(ex_inputs)
		elif key == '5': # Show external outputs
			ex_outputs = fpgaDesign.get_outputs()
			print(ex_outputs)
		elif key == '6': # Craft bitstream
			filename = input("Please put a name for the bitstream file.")
			filename = filename + ".bits"
			with open(filename, 'w') as file:
				file.write(str(bits))
			print("Saved as {}".format(filename))
		elif key == '7': # Show resource allocation
			LUTS = fpgaDesign.get_LUTS()
			used_LUTS = 0
			for i in LUTS:
				if i[1] != "."
					empty+=1
			print("% of LUT: {}".format()) #luts / connections of nodes
			print("% of connections: {}".format()) #number of connections
			print("Total memory required: {}".format()) #size of bitstream
		elif key == '8': # Show FPGA visually
			fpgaDesign.show_FPGA()
		elif key == 'h':
			output_prompt()
		elif key == 'q': #quit
			sys.exit()
		else:
			print("Enter h to see prompts again.")

if __name__=="__main__":
	main()
