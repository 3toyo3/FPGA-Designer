import numpy as np
import sys #exit
from os.path import exists
from os.path import getsize
from FPGAstructure import *
from logic_synthesizer import *
import synthesis_engine as sy
import synthesis_engine6 as sy6

# This program sets up the FPGA based on user input

#TODO partial connections, bitstream

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
	return LUTS_num

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
	return LUTS_type

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
	return connect_type

def specify_connectivity(connect_type): #TODO this function
	if connect_type == 2:
		connections = 1
		#while True:
		#	filename = input("File Name: ")
		#	if check_file(filename):
		#		with open(filename, 'r') as file: #TODO fix this assumption
		#			line = file.readline() #must be on one line
		#		#TODO any processing
		#		connections = line
		#		break
		#	else:
		#		print("That file doesn't seem to exist.")
	else:
		print("Fully connected")
		connections = 1
		#TODO Fully connected
		#Specify here
	return connections

def get_IO():
	while True:
		input_num=input("How many inputs? ")
		output_num=input("How many outputs? ")
		if input_num.isnumeric() & output_num.isnumeric():
			if (int(input_num) > 0) & (int(output_num) > 0):
				input_num = int(input_num)
				output_num = int(output_num)
				break
		print("Inputs must be integers greater than 0")
	return input_num, output_num

def get_equations():
	equations = []
	while True:
		print("Please input blif file for the logic expressions")
		blif_file_path=input()
		if exists(blif_file_path):
			if blif_file_path[-5:]==".blif":
				with open(blif_file_path, 'r') as file:
					lines_list=file.readlines()
				break
			else:
				print("Please choose a blif file.")
			break
		else:
			print("File {} doesnt exist.".format(blif_file_path))
			print("Please try again.")
	for line in lines_list:
		if line.startswith('#'):
			pass
		else:
			eqn = line.replace(" ","")
			eqn = eqn.strip() #remove \n
			equations.append(eqn)
	return equations

def basic_prompt(word):
	while True:
		print("Do you want the FPGA to be {}?".format(word))
		user_input = input("A: Yes  B: No")
		if user_input is 'A':
			user_input = True
		elif user_input is 'B':
			user_input = False
		else:
			print("Please pick option A or B.o")
	return user_input

#integration
def craft_new_FPGA( LUTS_num, LUT_type, connect_type, connections, input_num, output_num, equations): #TODO partial equations
	#optimizes equations
	minimized=basic_prompt("minimized")
	if minimized:
		equations_arrays=textToArray(equations)
		equations=minimize_equations(equations_arrays)
	equations_backup = equations[:] #makes a deep copy just in case
	factored=basic_prompt("factored")
	if factored:
		equations=toFactorer(equations) #changes string format
		equations=mutual_factor(equations)
	subs=basic_prompt("substituted")
	if subs:
		equations=substituition(equations)
	equations=toSplitter(equations) #changes string format
	if LUT_type == 4:
		print("LUT4")
		eqns = sy.assign_LUTS(eqns,LUTS_num)
	elif LUT_type == 6:
		print("LUT6")
		eqns = sy.assign_LUTS(eqns, LUTS_num)
	#TODO partial equations here or below..

	#At this point, you have the final equations for assignment
	if LUTS_num < len(equations):
		print("This FPGA doesn't have enough LUTS. Using minimized equations instead.")
		equations = equations_backup
		if LUTS_num < len(equations):
			print("This FPGA still doesn't have enough LUTS.")
			print("Ending program...")
			sys.exit()

	FPGA1 = FPGA()
	FPGA1.initializeIO(input_num, output_num)
	FPGA1.set_LUTS(equations)
	if connect_type == 2: #partial
		FPGA1.set_connections(connections) #TODO
	FPGA1.updateOutputs()
	FPGA1.updateInputs()
	return FPGA1

#TODO assuming bitstream parser returns a list of equations...
def recraft_FPGA(equations):
	FPGA1 = FPGA()
	FPGA1.set_LUTS(equations)
	FPGA1.updateOutputs()
	FPGA1.updateInputs()
	return FPGA1


def output_prompt():
	print("FPGA Display Options:")
	print("[1] Show all LUT assignments")
	print("[2] Show specific LUT assignment")
	print("[3] Show internal connections")
	print("[4] Show external input assignments")
	print("[5] Show external output assignments")
	print("[6] Craft bitstream of current FPGA")
	print("[7] Show resource allocation")
	print("[8] Show FPGA visually")
	print("[h] Show this prompt again")
	print("[q] Quit program")

def main():
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

	#===============Recraft FPGA
	if useBitstream:
		with open(bitstream_file, 'r') as file:
			rawbits = file.read()
		rawbits = rawbits.strip('[]')
		rawbits = rawbits.split(',')
		if len(rawbits) == 10:
			bits = rawbits
			#TODO parse bitstream for equations
			FPGA1 = recraft_FPGA(equations)
		else:
			print("This bitstream was improperly formatted. Closing program.")
			sys.exit()

	#================MAKE NEW FPGA via USER INPUT
	else:
		LUTS_num = get_LUTS_num()
		LUT_type = get_LUT_type()
		connect_type = get_connectivity()
		connections = specify_connections()
		input_num, output_num = getIO()
		equations = get_equations()

		FPGA1 = create_new_FPGA(LUTS_num, LUT_type, connect_type, connections, input_num, output_num, equations)

	#================User output
	key = 'i'
	output_prompt()
	while key != 'q':
		key=input("What do you want to do?")
		if key=='1':  # Show all LUT assignments
			LUTS = fpgaDesign.get_LUTS()
			for i in range(len(LUTS)):
				print("LUT{}: {}".format(i,LUTS[i]))
		elif key == '2': # Show specific LUT assignment
			num = input("Which LUT do you want to see? 1-{}".format(LUTs_num))
			if num <= fpgaDesign.get_num_luts(): #makesure no index error
				LUT = fpgaDesign.get_LUT(num)
				print(LUT)
			else:
				print("LUT{} doesn't exist".format(num))
		elif key == '3': # Show internal connections
			conn = fpgaDesign.get_connections()
			print(conn)
		elif key == '4': # Show external inputs
			ex_inputs = fpgaDesign.get_inputs()
			for i in range(len(ex_inputs)):
				print("I{}: {}".format(i, ex_inputs[i]))
		elif key == '5': # Show external outputs
			ex_outputs = fpgaDesign.get_outputs()
			for i in range(len(ex_outputs)):
				print("O{}: {}".format(i, ex_outputs[i]))
		elif key == '6': # Craft bitstream
			bitstream_file = input("Please put a name for the bitstream file.")
			bitstream_file = bitstream_file + ".bits"
			with open(filename, 'w') as file:
				file.write(str(bits)) #TODO craft bitstream
			print("Saved as {}".format(bitstream_file))
		elif key == '7': # Show resource allocation
			used_LUTS = fpgaDesign.get_num_luts() #TODO get total number of luts
			used_connections = fpgaDesign.get_num_connections()
			total_connection = fpgaDesign.get_lut_size() * used_LUTS
			if 'total_LUTS' in locals():
				print("% of LUT: {}".format((used_LUTS/total_LUTS) * 100)) #luts / connections of nodes
			else:
				print("% of LUT: {} used".format(used_LUTS))
			print("% of connections: {}".format((used_connections/total_connection) * 100)) #number of connections
			bitstream_exists=check_file(bitstream_file)
			if bitstream_exists:
				print("Total memory required: {}".format(getsize(filename))) #size of bitstream
			else:
				print("-- Create bitstream to find total memory required --")
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
