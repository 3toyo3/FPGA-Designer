import networkx as nx

class FPGA:
	FPGA_graph = []

	def __init__(self):
		FPGA_graph = nx.DiGraph()

	#depends on bitstream
	def __init__(self, LUTS, connects)
		FPGA_graph = nx.DiGraph()

	#graph.add_edges_from([("root", "a"), ("a", "b"), ("a", "e"), ("b", "c"), ("b", "d"), ("d", "e")])

	def connect_LUT(self):
		print("Hello world!")
		#add_edge
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
		#add_node(A, eqn="blah")
		name="LUT"+str(num)
		if name in self.LUTS:
			self.LUTS[name]=equation
		else:
			print("This LUT doesn't exist")

	def get_LUTS(self):
		#graph.nodes()(data=True)
		return tuple(self.LUTS.items()) #immutable

	def get_LUT(self, LUTnum):
		name = "LUT"+str(LUTnum)
		if name in self.LUTS:
			return self.LUTS[name]
		else:
			return "LUT not found"

	def get_inputs(self):
		#grpah.node()
		#aka has neighbor successors, no predecssors
		#must check that outputs only
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
		#aka has neighbor predecssors. no successors
		#graph nodes only inputs
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
