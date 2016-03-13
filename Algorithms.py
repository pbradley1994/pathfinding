import Queue

# Python implementation of the Breadth First Search algorithm
class BreadthFirstSearch(object):
	def __init__(self, start_node, goal_node=None):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.Queue()
		# Put the starting node into the frontier queue
		self.frontier.put(self.start_node)
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None

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
					self.came_from[next_node] = current_node
			return True
		else:
			return False

# Python implementation of Dijkstra's algorithm
class Dijkstra(object):
	def __init__(self, start_node, goal_node=None):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.PriorityQueue()
		# Put the starting node into the frontier queue
		self.frontier.put(self.start_node, 0)
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()
			# This node has now been visited
			current_node.status = "Visited"

			if self.goal_node and current_node is self.goal_node:
				return False
			#print(current_node.x, current_node.y)
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				new_cost = self.cost_so_far[current_node] + next_node.cost
				# We only care about those nodes that we have not visited
				if next_node not in self.came_from or (next_node in self.cost_so_far and new_cost < self.cost_so_far[next_node]):
					self.cost_so_far[next_node] = new_cost
					# Add the unvisited node to the frontier
					self.frontier.put(next_node, new_cost)
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return True
		else:
			return False

# Python implementation of Greedy Best First Algorithm
class GreedyBestFirstSearch(object):
	def __init__(self, start_node, goal_node=None):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.PriorityQueue()
		# Put the starting node into the frontier queue
		self.frontier.put(self.start_node, 0)
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()
			# This node has now been visited
			current_node.status = "Visited"

			if self.goal_node and current_node is self.goal_node:
				return False
			#print(current_node.x, current_node.y)
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				new_cost = self.cost_so_far[current_node] + next_node.cost
				# We only care about those nodes that we have not visited
				if next_node not in self.came_from or (next_node in self.cost_so_far and new_cost < self.cost_so_far[next_node]):
					self.cost_so_far[next_node] = new_cost
					# Add the unvisited node to the frontier
					self.frontier.put(next_node, self.heuristic(next_node))
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return True
		else:
			return False

	def heuristic(self, node):
		return abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y)

algorithm_dict = {"Breadth First Search": BreadthFirstSearch,
				  "Dijkstra's Algorithm": Dijkstra,
				  "Greedy Best-First Search": GreedyBestFirstSearch}