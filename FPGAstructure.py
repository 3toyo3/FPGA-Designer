import networkx as nx
import matplotlib.pyplot as plot

#TODO assumes that all nums are checked prior to assignment therefore not done in thsi program
class FPGA:
	FPGA_graph = []
	LUTS = []
	inputs = []
	outputs = []

	def __init__(self):
		self.FPGA_graph = nx.DiGraph()

	#initialize array
	#def __init__(self, input_num, output_num, LUTS_num):
	#	self.FPGA_graph = nx.DiGraph()
	#	self.inputs.append(None)*input_num
	#	self.outputs.append(None)*output_num
	#	self.LUTs.append(None)*LUTS_num

	#bitstream construction
	def __init__(self, LUTS, connects)
		self.FPGA_graph = nx.DiGraph()
		#graph.add_edges_from([("root", "a"), ("a", "b"), ("a", "e"), ("b", "c"), ("b", "d"), ("d", "e")])

	def connect_LUT(self, nodeFrom, nodeTo):
		#TODO check both exist
		dag.add_edges_from(nodeFrom, nodeTo)

	def get_connections(self):
		return list(self.FPGA_graph.edges())

	# takes a list of equations, assume indexed as to where they shuld go
	# assumes inputs exist
	def set_LUTS(self, equations):
		node_names=[]
		node_connects=[]

		for i in range(len(equations)):
			equation=equations[i]
			eqn = equation.split("=")
			node_name=eqn[0]
			input_nodes=eqnToNode(eqn[1])
			connect_nodes[(node, node_name) for node in nodes]
			node_names[i]=node_name
			node_connects=[i]
p		for i in range(len(node_names))
			self.FPGA_graph.create_node(node_names[i], data=equations[i])
			self.FPGA_graph.add_edges_from(node_connects[i])
		#TODO reorganize node_name from connections
		for node in node_names:
			self.LUTS.append(node)

	#takes one equation and a specific number
	def set_LUT(self, num, equation):
		#TODO check that it exists
		eqn_split=equation.split("=")
		output_eqn=eqn_split[0]
		input_eqn=eqn_split[1]

		self.LUTS[num]=output_eqn
		self.FPGA_graph.add_node(output_eqn, data=equation)

		nodes = eqnToNodes(input_eqn)
		connect_nodes[(node, output_eqn) for node in nodes]
		self.FPGA_graph.add_edges_from(connect_nodes)

	def get_LUTS(self): #returns all nodes
		eqns = []
		for node in self.LUTS
			eqn=self.FPGA_graph.nodes[node]
			eqns.append(eqn)
		return eqns

	def get_LUT(self, LUTnum):
		#TODO check if num even exists
		node = self.LUTS[LUTnum]
		eqn = self.FPGA_graph.nodes[node]
		return eqn

	def get_inputs(self):
		#update inputs list
		#check that no predecessors
		return self.inputs

	#assumes that passing a list of characters, already in order of what i want
	def set_inputs(self, inputs_list):
		for i in inputs_list:
			self.inputs.append(i)
			self.FPGA_graph.add_node(node)

	def set_input(self, input_place, input_value):
		if 0 <= output_place < len(self.inputs) and self.inputs[input_place] is not None:
			old = self.inputs[input_place]
			self.inputs.append(old)
		self.inputs[input_place] = input_value
		if FPGA_graph.has_node(input_value)
			pass
		else:
			self FPGA_graph.create_node(input_value)

	def get_outputs(self):
		#update outputs list
		#check that no successors
		return self.outputs

	def set_outputs(self, outputs_list):
		for i in outputs_list:
			self.outputs.append(i)
			if self.FPGA_graph.has_node(i):
				pass
			else:
				self.FPGA_graph.add_node(i)

	def set_output(self, output_place, output_value):
		if 0 <= output_place < len(self.outputs) and self.outputs[output_place] is not None:
			old = self.outputs[output_place]
			self.outputs.append(old)
		self.outputs[output_place]=output_value
		if self.FPGA_graph.has_node(output_value):
			pass
		else:
			self.FPGA_graph.create_node(output_value)

	def show_FPGA(self): #TODO display inputs as Io, I2, etc
		plot.figure(figsize=(8,6)) #optional
		pos = nx.spring_layout(self.FPGA_graph) #May need to change layout
		node_labels = {node: self.FPGA_graph.nodes[node] for node in self.FPGA_nodes()}
		nx.draw(self.FPGA_graph, pos, with_labels=True, labels=node_labels, node_size=500, node_color="skyblue",font_weight="bold",arrows=False)
		plot.title("FPGA Design")
		plot.show()

	#Takes a string input of terms only, and outputs set of node names
	def eqnToNodes(equation):
		nodes = set()
		for char in equation:
			if char.isalpha():
				nodes.add(char)
		return nodes
