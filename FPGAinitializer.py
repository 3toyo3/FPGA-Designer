import numpy as np
import sys #exit
from os.path import exists
from os.path import getsize
from FPGAstructure import *
from logic_synthesizer import *

# This program sets up the FPGA based on user input

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
		eqn = line.strip() #remove \n
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

#integration sorta
def craft_new_FPGA(): #TODO partial equations
	#TODO clean equations
	minimized=basic_prompt("minimized")
	if minimized:
		#textToArray
		#minimize
	factored=basic_prompt("factored")
	if factored:
		#factor2
	#substituition
	if LUT_type == 4:
		#LUT4
	elseif LUT_type == 6:
		#LUT6
	#final equaitons
	#TODO partial equations
	#compare to LUTnum
	#FPGA using input_num
	#FPGA using output_num
	#for each equation in FPGA
		#put in

#TODO
#def recraft_FPGA():

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
			#TODO parse bitstream
			#TODO craft FPGA here
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

		#craft FPGA globally
		#fpgaDesign=FPGA()

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
				print("% of LUT: {} used".format(used_LUTS)
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
