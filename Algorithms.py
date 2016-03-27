import Queue, collections

# Python implementation of the Breadth First Search algorithm
class BreadthFirstSearch(object):
	def __init__(self, start_node, goal_node):
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
		# No implementation of cost
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()
			# This node has now been visited
			current_node.status = "Visited"
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				# We only care about those nodes that we have not visited
				if next_node.status == "Unexplored":
					self.cost_so_far[next_node] = self.cost_so_far[current_node] + 1
					# Add the unvisited node to the frontier
					self.frontier.put(next_node)
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return True
		else:
			return False

# Python implementation of Dijkstra's algorithm
class Dijkstra(object):
	def __init__(self, start_node, goal_node):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.PriorityQueue()
		self.frontier_keeper = {}
		# Put the starting node into the frontier queue
		self.frontier.put((0, self.start_node))
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()[1]
			# This node has now been visited
			current_node.status = "Visited"

			if self.goal_node and current_node is self.goal_node:
				return False
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				new_cost = self.cost_so_far[current_node] + next_node.cost
				# We only care about those nodes that we have not visited
				if next_node not in self.came_from or new_cost < self.cost_so_far[next_node]:
					self.cost_so_far[next_node] = new_cost
					# Add the unvisited node to the frontier
					self.frontier.put((new_cost, next_node))
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return True
		else:
			return False

# Python implementation of Greedy Best First Algorithm
class GreedyBestFirstSearch(object):
	def __init__(self, start_node, goal_node):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.PriorityQueue()
		# Put the starting node into the frontier queue
		self.frontier.put((0, self.start_node))
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()[1]
			# This node has now been visited
			current_node.status = "Visited"

			if self.goal_node and current_node is self.goal_node:
				return False
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				new_cost = self.cost_so_far[current_node] + next_node.cost
				# We only care about those nodes that we have not visited
				if next_node not in self.came_from or new_cost < self.cost_so_far[next_node]:
					self.cost_so_far[next_node] = new_cost
					# Add the unvisited node to the frontier
					self.frontier.put((self.heuristic(next_node), next_node))
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return True
		else:
			return False

	def heuristic(self, node):
		return abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y)

# Python implementation of A* Algorithm
class AStar(object):
	def __init__(self, start_node, goal_node):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.PriorityQueue()
		# Put the starting node into the frontier queue
		self.frontier.put((0, self.start_node))
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()[1]
			# This node has now been visited
			current_node.status = "Visited"

			if self.goal_node and current_node is self.goal_node:
				return False
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				new_cost = self.cost_so_far[current_node] + next_node.cost
				# We only care about those nodes that we have not visited
				if next_node not in self.came_from or new_cost < self.cost_so_far[next_node]:
					self.cost_so_far[next_node] = new_cost
					# Add the unvisited node to the frontier
					self.frontier.put((self.heuristic(next_node) + new_cost, next_node))
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return True
		else:
			return False

	def heuristic(self, node):
		return abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y)

# Python implementation of Dynamic Weighting A*
class Dynamic(object):
	def __init__(self, start_node, goal_node):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.PriorityQueue()
		# Put the starting node into the frontier queue
		self.frontier.put((0, self.start_node))
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			current_node = self.frontier.get()[1]
			# This node has now been visited
			current_node.status = "Visited"

			if self.goal_node and current_node is self.goal_node:
				return False
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				new_cost = self.cost_so_far[current_node] + next_node.cost
				# We only care about those nodes that we have not visited
				if next_node not in self.came_from or new_cost < self.cost_so_far[next_node]:
					self.cost_so_far[next_node] = new_cost
					# Add the unvisited node to the frontier
					priority = self.heuristic(next_node) * self.weight(next_node) + new_cost
					self.frontier.put((priority, next_node))
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return True
		else:
			return False

	def heuristic(self, node):
		return abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y)

	# Ranges between 2, at the start node, and 0.5, at the goal node.
	def weight(self, node):
		return 0.5 + 1.5*self.heuristic(node)/self.heuristic(self.start_node)

# Python implementation of A* Algorithm with priority cut-off of 5 (For bidirectional search)
class CutOffAStar(object):
	def __init__(self, start_node, goal_node):
		self.start_node = start_node
		self.goal_node = goal_node
		self.reset()

	def reset(self):
		# Set up the frontier queue
		self.frontier = Queue.PriorityQueue()
		# Put the starting node into the frontier queue
		self.frontier.put((0, self.start_node))
		self.start_node.status = "Frontier"
		# Keeps track of how we got to each node
		self.came_from = {}
		self.came_from[self.start_node] = None
		self.cost_so_far = {}
		self.cost_so_far[self.start_node] = 0

	def update(self, graph):
		if not self.frontier.empty():
			# Get a node from the queue
			priority, current_node = self.frontier.get()
			# This node has now been visited
			current_node.status = "Visited"

			if self.goal_node and current_node is self.goal_node:
				return 'goal'
			# Need to get 
			elif self.cost_so_far[current_node] >= 5:
				return current_node
			# Loop through the neighbors of this node
			for next_node in graph.get_neighbors(current_node):
				new_cost = self.cost_so_far[current_node] + next_node.cost
				# We only care about those nodes that we have not visited
				if next_node not in self.came_from or new_cost < self.cost_so_far[next_node]:
					self.cost_so_far[next_node] = new_cost
					# Add the unvisited node to the frontier
					self.frontier.put((self.heuristic(next_node) + new_cost, next_node))
					next_node.status = "Frontier"
					self.came_from[next_node] = current_node
			return 'continue'
		else:
			return 'done'

	def heuristic(self, node):
		return abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y)

# Python implementation of Bidirectional Retargeting Search
class Bidirectional(object):
	def __init__(self, start_node, goal_node):
		self.start_node = start_node
		self.goal_node = goal_node

		self.reset()

	def reset(self):
		self.node_a = self.start_node
		self.node_b =  self.goal_node
		self.my_algorithm = CutOffAStar(self.node_a, self.node_b)
		self.state = 'Forward'
		# Keeps track of how we got to each node
		self.came_from = {}
		self.cost_so_far = {}

		self.forward_path = []
		self.backward_path = []

	def update(self, graph):
		output = self.my_algorithm.update(graph)
		# Update main algorithm with necessary info
		self.came_from.update(self.my_algorithm.came_from)
		self.cost_so_far.update(self.my_algorithm.cost_so_far)

		# Determine output and if we need to retarget again.
		if output == 'goal' or output == 'done':
			if self.state == 'Forward':
				self.forward_path.append(self.process_path(self.my_algorithm.goal_node))
			else:
				self.backward_path.append(self.process_path(self.my_algorithm.goal_node))
			return False
		elif output == 'continue':
			return True
		elif self.state == 'Forward':
			self.node_a = output
			self.forward_path.append(self.process_path(output))
			self.my_algorithm = CutOffAStar(self.node_b, self.node_a)
			self.state = 'Backward'
			return True
		elif self.state == 'Backward':
			self.node_b = output
			self.backward_path.append(self.process_path(output))
			self.my_algorithm = CutOffAStar(self.node_a, self.node_b)
			self.state = 'Forward'
			return True

	def process_path(self, node):
		current = node
		path = [current]
		while current in self.my_algorithm.came_from:
			current = self.my_algorithm.came_from[current]
			if current:
				path.append(current)
		return path

algorithm_dict = collections.OrderedDict([("Breadth First Search", BreadthFirstSearch),
				  ("Dijkstra's Algorithm", Dijkstra),
				  ("Greedy Best-First Search", GreedyBestFirstSearch),
				  ("A* Algorithm", AStar),
				  ("Dynamic Weight A*", Dynamic),
				  ("Bidirectional Retargeting Search", Bidirectional)])