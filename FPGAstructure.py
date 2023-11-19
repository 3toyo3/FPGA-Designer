import networkx as nx
import matplotlib.pyplot as plot

#TODO assumes that all nums are checked prior to assignment therefore not done in thsi program
class FPGA:
	FPGA_graph = []
	LUTS = []
	inputs = []
	outputs = []
	initialized=False

	def __init__(self, input_num=None):
		if input_num is None:
			self.FPGA_graph = nx.DiGraph()
		else:
			self.FPGA_graph = nx.DiGraph()
			self.inputs = [None]*input_num
			for i in range(len(self.inputs)):
				node_name = "I"+str(i)
				self.FPGA_graph.add_node(node_name,date=None)


	#	#graph.add_edges_from([("root", "a"), ("a", "b"), ("a", "e"), ("b", "c"), ("b", "d"), ("d", "e")])
	def connect_LUTS(self, connections):
		self.FPGA_graph.add_edges_from(connections)

	def connect_LUT(self, nodeFrom, nodeTo):
		self.FPGA_graph.add_edges_from(nodeFrom, nodeTo)

	def get_connections(self):
		return list(self.FPGA_graph.edges())

	def get_num_connections(self):
		return self.FPGA_graph.number_of_edges()

	def get_lut_size(self): #samples three LUTS for the input size
		connection_count = 0
		if len(list(self.FPGA_graph.nodes())) > len(self.inputs): #checks assumption of above comment
			node1=self.LUT[0]
			connections_of_1=list(self.FPGA_graph.predecessors(node1)) #only checks nodes with inputs
			node2=self.output[0]
			connections_of_2=list(self.FPGA_graph.predecessors(node2))
			node3=self.LUT[1]
			connections_of_3=list(self.FPGA_graph.predecessors(node3))
			connection_count=max(connections_of_3, connections_of_2, connections_of_1)
		return connection_count

	def get_num_luts(self):
		num_nodes = self.FPGA_graph.number_of_nodes()
		luts_num = num_nodes - len(self.input)
		if luts_num == len(self.LUTS):
			return luts_num
		else:
			return len(self.LUTS)

	def get_nodes(self):
		nodes=[]
		for node, data in self.FPGA_graph.nodes(data=True):
			nodes.append(f"Node {node}: {data}")
		return nodes

	def get_node_before(self, node_name):
		return list(self.FPGA_graph.predecessors(node_name ))

	# takes a list of equations, assume indexed as to where they should go
	# assumes inputs exist
	def set_LUTS(self, equations):
		node_names=[]
		node_connects=[]

		for equation in equations:
			eqn = equation.split("=")
			node_name=eqn[0]
			input_nodes=self.eqnToNodes(eqn[1])
			connect_nodes = []
			for node in input_nodes:
				connection=[node, node_name]
				connect_nodes.append(connection)
			#print("Node name: {}".format(node_name))
			#print(connect_nodes)
			node_names.append(node_name)
			node_connects.append(connect_nodes)
		for i in range(len(node_names)):
			self.FPGA_graph.add_node(node_names[i], data=equations[i])
			self.FPGA_graph.add_edges_from(node_connects[i])
		for node in node_names:
			self.LUTS.append(node)

	#takes one equation and a specific number
	def set_LUT(self, num, equation):
		eqn_split=equation.split("=")
		output_eqn=eqn_split[0]
		input_eqn=eqn_split[1]

		self.LUTS[num]=output_eqn
		self.FPGA_graph.add_node(output_eqn, data=equation)

		connect_nodes=[]
		nodes = eqnToNodes(input_eqn)
		for node in nodes:
			connection=[node, output_eqn]
			connect_nodes.append(connection)
		self.FPGA_graph.add_edges_from(connect_nodes)

	def get_LUTS(self): #returns all nodes
		eqns = []
		for node in self.LUTS:
			eqn=self.FPGA_graph.nodes[node]
			eqns.append(eqn)
		return eqns

	def get_LUT(self, LUTnum):
		if LUTnum <= len(self.LUTS):
			node = self.LUTS[LUTnum]
			eqn = self.FPGA_graph.nodes[node]
			return eqn
		else:
			return "LUT{} doesn't exist".format(LUTnum)

	def get_inputs(self):
		return self.inputs

	#assumes that passing a list of characters, already in order of what i want
	def set_inputs(self, inputs_list):
		for i in range(len(inputs_list)):
			self.inputs[i] = inputs_list[i]
			node_name="I"+str(i)
			self.FPGA_graph.add_node(node_name, date=inputs_list[i])

	def set_input(self, input_place, input_value):
		#if 0 <= output_place < len(self.inputs) and self.inputs[input_place] is not None:
		#	old = self.inputs[input_place]
		#	self.inputs.append(old)
		self.inputs[input_place] = input_value
		node_name = "I"+str(input_place)
		self.FPGA_graph.create_node(node_name, data=input_value) #TODO potential to overwrite here

	def get_outputs(self):
		return self.outputs

	def set_outputs(self, outputs_list):
		for i in outputs_list:
			self.outputs.append(i)
			self.FPGA_graph.add_node(i)
			#if self.FPGA_graph.has_node(i):
			#	pass
			#else:
			#	self.FPGA_graph.add_node(i)

	def set_output(self, output_place, output_value):
		if 0 <= output_place < len(self.outputs) and self.outputs[output_place] is not None:
			old = self.outputs[output_place]
			self.outputs.append(old) #TODO potential to overwrite here
		self.outputs[output_place]=output_value
		self.FPGA_graph.create_node(output_value)
		#if self.FPGA_graph.has_node(output_value):
		#	pass
		#else:
		#	self.FPGA_graph.create_node(output_value)

	def show_FPGA(self):
		plot.figure(figsize=(8,6)) #optional
		pos = nx.shell_layout(self.FPGA_graph)
		node_labels = {node: self.FPGA_graph.nodes[node]['data'] for node in self.FPGA_graph.nodes()}
		nx.draw(self.FPGA_graph, pos, with_labels=True, labels=node_labels, node_size=500, node_color="skyblue",font_weight="bold",arrows=False)
		plot.title("FPGA Design")
		plot.show()

	#Takes a string input of terms only, and outputs set of node names
	def eqnToNodes(self,equation):
		nodes = set()
		for char in equation:
			if char.isalpha():
				nodes.add(char)
		return nodes

	def initializeIO(input_num, output_num): 
		self.inputs = [None]*input_num
		self.outputs = [None] * output_num
		self.initialized=True

	def updateOutputs(self):
		output_nodes = [node for node in self.FPGA_graph.nodes() if not any(self.FPGA_graph.successors(node))]

		if self.initialized: #If output num was used aka new design
			for i in range(len(self.outputs)):
				node = output_nodes.pop(0)
				self.outputs[i]=node
		else: #From bitstream
			for out in output_nodes:
				self.outputs.append(out )
		if len(output_nodes) != 0:
			print("Not enough external output nodes in the FPGA.")
			print("Recommend redesigning the FPGA for accurate results")
			print("These equations would need {} total outputs".format(len(output_nodes)+len(self.outputs)))

	def updateInputs(self):
		input_nodes = []
		input_nodeless = [] #created forcefully by adding edges etc.

		nodes_no_inputs = [node for node in self.FPGA_graph.nodes() if not any(self.FPGA_graph.predecessors(node))]
		for node in nodes_no_inputs:
			if 'I' in node:
				input_nodes.append(node)
			else:
				input_nodeless.append(node)
		input_nodes.sort()
		for i in range(len(input_nodeless)):
			input_value = input_nodeless[i]
			if len(input_nodes) == 0:
				input_node = "I"+str(i)
			else:
				input_node = input_nodes.pop(0)
			self.FPGA_graph.add_node(input_node,data=input_value)
			# move connections
			successors = list(self.FPGA_graph.successors(input_value))
			self.FPGA_graph.remove_node(input_value)
			for successor in successors:
				self.FPGA_graph.add_edge(input_node, successor)
		new_inputs = input_nodeless + input_nodes
		if self.initialized: #If inputnum and output num used AKA new design
			for i in len(range(self.inputs)):
				self.inputs[i] = new_inputs.pop(0)
		else: #If crafted from bitstream
			for inp in new_inputs:
				self.inputs.append(inp)
		if len(new_inputs) != 0:
			print("Not enough external inputs in the FPGA.")
			print("Recommend redesigning the FPGA for accurate results")
			print("These equations would need {} total inputs.".format(len(self.inputs)+len(new_inputs)))
