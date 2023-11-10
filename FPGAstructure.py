class FPGA:
	LUTS={}
	connects=[] #TODO
	inputs=[]
	output=[]

	def __init__(self,LUTnum, connects, inputs_num, outputs_num):
		for i in range(LUTnum):
			name = "LUT"+str(i)
			LUTS[name]="."
		self.LUTS=LUTS
		self.connects=connects

		inputs = [0]*inputs_num
		self.inputs=inputs

		outputs=[0]*outputs_num
		self.outputs=outputs

	def map_connections(self):
		#TODO output connections

	# takes a list of equations - User Interaction
	def set_LUTS(self, equations):
		#TODO make this done automatically?
		#TODO also check if number of luts is valid for size of equation
		print("You have % LUTS, please put 0-% to specify LUT.".format(len(LUTS),len(LUTS)))
		for equation in equations:
			spot=input('Which LUT should % go in?'.format(equation))
			name="LUT"+str(spot)
			self.LUTS[name]=equation

	#takes one equation and a specific number
	def set_LUT(self, num, equation):
		name="LUT"+str(num)
		#TODO check that it exists
		self.LUTS[name]=equation

	def get_LUTS(self):
		for entry in self.LUTS: #TODO change format?
			print(entry+": "+self.LUTS[entry])

	def get_LUT(self, LUTnum):
		#TODO check that num exists
		name = "LUT"+str(LUTnum)
		print(name+": "LUTS[name])

	def get_inputs(self):
		print(self.inputs)

	#assumes that passing a list of characters
	def set_inputs(self, inputs_list):
		#TODO check that appropriate sizes
		for i in range(len(inputs_list)):
			self.inputs[i]=inputs_list[i]

	def set_input(self, input_value, place): #TODO switch order of fields
		#TODO check that place is valid
		self.inputs[place]=input_value

	def get_outputs(self):
		print(self.outputs)

	def set_outputs(self, outputs_list):
		#TODO check appropriate sizes
		for i in range(len(outputs_list)):
			self.outputs[i]=outputs_list[i]

	def set_output(self, output_value, place): #TODO switch order of fields
		#TODO check that place is valid
		self.outputs[place]=output_value

	#TODO output visually?
