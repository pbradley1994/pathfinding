import Queue

# Python implementation of the Breadth First Search algorithm
class BreadthFirstSearch1(object):
	def __init__(self, start_node):
		# Set up the frontier queue
		self.frontier = Queue.Queue()
		# Put the starting node into the frontier queue
		self.frontier.put(start_node)
		start_node.status = "Frontier"

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()
			# This node has now been visited
			current_node.status = "Visited"
			#print(current_node.x, current_node.y)
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				# We only care about those nodes that we have not visited
				if next_node.status == "Unexplored":
					# Add the unvisited node to the frontier
					self.frontier.put(next_node)
					next_node.status = "Frontier"
			return True
		else:
			return False