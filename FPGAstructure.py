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

	def get_connections(self):
		return list(self.FPGA_graph.edges())

	def get_num_connections(self):
		#print("Num of connections: {}".format(self.FPGA_graph.number_of_edges))
		return self.FPGA_graph.number_of_edges()

	def get_num_internal_connections(self):
		exclude = self.inputs + self.outputs
		num_edges_excluded = self.FPGA_graph.number_of_edges() - sum(1 for u, v in self.FPGA_graph.edges() if u in exclude and v in exclude)
		return num_edges_excluded


	def get_lut_size(self): #samples three LUTS for the input size
		connection_count = 0
		if len(list(self.FPGA_graph.nodes())) > len(self.inputs): #checks assumption of above comment
			node1=self.LUTS[0]
			connections_of_1=list(self.FPGA_graph.predecessors(node1)) #only checks nodes with inputs
			node2=self.LUTS[2]
			connections_of_2=list(self.FPGA_graph.predecessors(node2))
			node3=self.LUTS[1]
			connections_of_3=list(self.FPGA_graph.predecessors(node3))
			connection_count=max(len(connections_of_3), len(connections_of_2), len(connections_of_1))
		#print("Connection: {}".format(connection_count))
		return connection_count

	def get_num_luts(self):
		#print(len(self.LUTS))
		return len(self.LUTS)

	def get_nodes(self):
		nodes=[]
		for node, data in self.FPGA_graph.nodes(data=True):
			nodes.append(f"Node {node}: {data}")
		return nodes

	def get_node_before(self, node_name):
		return list(self.FPGA_graph.predecessors(node_name ))

	#takes a list of lut objects
	def set_LUTS(self, luts):
		for lut in luts:
			#print(lut.name)
			node_name = chr(int(lut.output)+97) #TODO fix
			node_data = lut.name
			node_inputs = lut.inputs
			node_outputs = lut.external_output

			self.FPGA_graph.add_node(node_name, data=node_data)
			#make node connections
			connections = []
			for inp in node_inputs:
				connection=[inp, node_name]
				connections.append(connection)
			if not node_outputs:
				pass
			else:
				outs = node_outputs.split()
				for out in outs:
					#print(out)
					connection=[node_name,out]
					connections.append(connection)
			self.FPGA_graph.add_edges_from(connections)
			self.LUTS.append(node_name)


	def get_LUTS(self): #returns lut nodes
		eqns = []
		for node in self.LUTS:
			eqn=self.FPGA_graph.nodes[node]['data']
			eqns.append(node+"="+eqn)
		return eqns

	def get_LUT(self, LUTnum):
		if LUTnum <= len(self.LUTS):
			node = self.LUTS[LUTnum]
			eqn = self.FPGA_graph.nodes[node]['data']
			return eqn
		else:
			return "LUT{} doesn't exist".format(LUTnum)

	def get_inputs(self):
		return self.inputs

	def get_outputs(self):
		return self.outputs

	def show_FPGA(self):
		plot.figure(figsize=(8,6)) #optional
		pos = nx.shell_layout(self.FPGA_graph)
		node_colors = ['red' if node in self.outputs else 'skyblue' for node in self.FPGA_graph.nodes()]
		node_labels = {node: (str(self.FPGA_graph.nodes[node]['data']) if 'data' in self.FPGA_graph.nodes[node] else node) for node in self.FPGA_graph.nodes()}
		#node_labels = {node: self.FPGA_graph.nodes[node]['data'] for node in self.FPGA_graph.nodes()}
		nx.draw(self.FPGA_graph, pos, with_labels=True, labels=node_labels, node_size=500, node_color=node_colors,font_weight="bold",arrows=False)
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
			if len(output_nodes) != 0:
				print("Not enough external output nodes in the FPGA.")
				print("Recommend redesigning the FPGA for accurate results")
				print("These equations would need {} total outputs".format(len(output_nodes)+len(self.outputs)))
		else: #From bitstream
			for out in output_nodes:
				self.outputs.append(out)

	def updateInputs(self):
		input_nodes = [node for node in self.FPGA_graph.nodes() if not any(self.FPGA_graph.predecessors(node))]
		if self.initialized:
			for i in range(len(self.inputs)):
				node = output_nodes.pop(0)
				self.outputs[i]=node
			if len(output_nodes) != 0:
				print("Not enough external output nodes in the FPGA.")
				print("Recommend redesigning the FPGA for accurate results")
				print("These equations would need {} total outputs".format(len(output_nodes)+len(self.outputs)))
		else:
			for inp in input_nodes:
				self.inputs.append(inp)
