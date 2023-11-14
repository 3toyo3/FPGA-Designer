class FPGA:
	LUTS={}
	connects=[] #TODO can be a part of lut above?
	inputs=[]
	output=[]

	def __init__(self, connects, inputs_num, outputs_num):
		#set sizes of elements
		for i in range(LUTnum):
			name = "LUT"+str()
			LUTS[name]="."
		#name = "LUT"+str(1)
		#LUTS[name] = "."
		self.LUTS=LUTS
		self.connects=connects

		inputs = [0]*inputs_num
		self.inputs=inputs

		outputs=[0]*outputs_num
		self.outputs=outputs

	def map_connections(self):
		print("Hello world!")
		#TODO output connections

	def get_connections(self):
		return self.connects

	# takes a list of equations, assume indexed as to where they shuld go
	def set_LUTS(self, equations):
		for i in range(len(equations)):
			name="LUT"+str(i)
			self.LUTS[name]=equations[i]

	#takes one equation and a specific number
	def set_LUT(self, num, equation):
		name="LUT"+str(num)
		if name in self.LUTS:
			self.LUTS[name]=equation
		else:
			print("This LUT doesn't exist")

	def get_LUTS(self):
		return tuple(self.LUTS.items()) #immutable

	def get_LUT(self, LUTnum):
		name = "LUT"+str(LUTnum)
		if name in self.LUTS:
			return self.LUTS[name]
		else:
			return "LUT not found"

	def get_inputs(self):
		return self.inputs

	#assumes that passing a list of characters
	def set_inputs(self, inputs_list):
		for i in range(len(inputs_list)):
			self.inputs[i]=inputs_list[i]

	def set_input(self, input_place, input_value):
		if 0 <= input_place <= len(self.inputs):
			self.inputs[input_place]=input_value
		else:
			print("That input is not valid")

	def get_outputs(self):
		return self.outputs

	def set_outputs(self, outputs_list):
		for i in range(len(outputs_list)):
			self.outputs[i]=outputs_list[i]

	def set_output(self, output_place, output_value):
		if 0 <= output_place <= len(self.outputs):
			self.outputs[output_place]=output_value
		else:
			print("That input is not valid")

	def show_FPGA(self):
		print("Hello world!") #TODO plantUML?
