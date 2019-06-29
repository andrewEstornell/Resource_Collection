from grid import *
import numpy as np
import math

ENEMY = -1
FRIENDLY = -.1

class SingleGeneticAI:
	"""
		This genetic AI controls a single agent, if there are N agents, there are N of these AIs
		The AI controls each agent by passing a real valued feature vector through a feed-forward neural network
		The networks parameters (connections, weights, etc) are initialized randomly and updated through genetic mutation
	"""

	class Brain:

		def __init__(self, input_size, seed, max_depth, max_nodes, output_size):
			"""
			 Creates a neural network
			:param input_size:
			:param seed:
			:param max_depth:
			:param max_nodes:
			:param output_size:
			:param radius:
			"""
			rand.seed(seed)
			m = input_size//2 #number of neurons in 1st hidden layer
			self.input_size = input_size
			self.bias = [np.zeros([m,1]), np.zeros([1,1])]
			self.input = np.zeros([input_size, 1])
			self.fitness = 0
			self.brain = [np.zeros([m, input_size]), np.zeros([output_size, m])] # This should be a list of numpy arrays, each 2D array is a layer of the brain
			for layer in self.brain:
				for i in range(len(layer)):
					for j in range(len(layer[0])):
						layer[i][j] = rand.uniform(-1, 1)


		@staticmethod
		def in_bounds(i, j, size):
			return 0 <= i < size and 0 <= j < size
 
		@staticmethod
		def sigmoid(arr):
			return 1/(1+np.exp(-arr))

		def play_game(self, grid, depth):
			"""
				Plays through a game given by grid,
			:param grid: object containing the resource collection game
			:return: the score of the game (fitness of the brain)
			"""
			while not grid.is_game_over:
				action_dict = {}
				for ship in grid.ships.values():
					action_dict[ship.id] = self.minimax(grid, ship.id, depth)
			self.fitness = grid.total_collection
			return self.fitness

		def minimax(self, grid, id, depth):
			ship = grid.ships[id]
			moves = [(ship.position[0] + action[0], ship.position[1] + action[1]) for action in actions
					 	if self.in_bounds(ship.position[0] + action[0], ship.position[1] + action[1], grid.size)]
			best_move = None
			best_value = float("-inf")
			for move in moves:
				value = self.maxi(grid, id, depth)
				if value >= best_value:
					best_value = value
					best_move = move
			return (abs(best_move[0] - ship.position[0]), abs(best_move[1] - ship.position[1]))

		def maxi(self, grid, id, depth):
			if depth <= 0:
				return self.heuristic_eval(grid, id)
			elif grid.is_game_over is True:
				return grid.total_collection

			ship = grid.ships[id]
			moves = [(ship.position[0] + action[0], ship.position[1] + action[1]) for action in actions
					 if self.in_bounds(ship.position[0] + action[0], ship.position[1] + action[1], grid.size)]

			best_value = float("-inf")
			for move in moves:
				new_grid = copy.deepcopy(grid)
				valid_move = (abs(move[0] - ship.position[0]), abs(move[1] - ship.position[1]))
				action_dict = {id: valid_move}
				print("Pos",ship.position)
				print("move",move)
				grid.perform_actions(action_dict)
				value = self.maxi(new_grid, id, depth - 1)
				if value > best_value:
					best_value = value
			return best_value

		def heuristic_eval(self, state, id):
			"""
			:param state: GRID
			:return:
			"""
			board = state
			piece = state.ships[id]

			self.extract_features(board, piece)
			eval = self.forward_pass(self.input)
			return eval

		def forward_pass(self, features):
			"""
				Performs a forward pass of the network, the end result is a real number
			:param features: LIST, input from the agent the AI is controlling
			:return: FLOAT
			"""

			input_to_next_layer = features
			i = 0
			for layer in self.brain:
				input_to_next_layer = np.dot(layer, input_to_next_layer) + self.bias[i]
				i+=1
				if i < len(self.brain):
					input_to_next_layer = np.tanh(input_to_next_layer)

			output = self.sigmoid(input_to_next_layer)
			return output

		def extract_features(self, board, piece):
			"""
				scans a portion of the board surrounding the piece and extracts features for each cell
			:param state: GRID, this is the grid that the game is played on
			:return: LIST, returns a list of features that will be forward propagated through the neural network
			"""
			n = int(math.sqrt(self.input_size)//2)
			enemy_cells = []
			for vals in board.demo_ships.values():
				enemy_cells.append(tuple(vals.position))

			ind = 0

			for i in range(piece.position[0]-n, piece.position[0]+n+1):
				for j in range(piece.position[1]-n, piece.position[1]+n+1):
					if (i,j) in enemy_cells: #if enemy
						self.input[ind] = ENEMY
					elif board.grid[i][j].ship and (i,j) != piece.position: #if friendly ship
						self.input[ind] = FRIENDLY
					elif not self.in_bounds(i, j, board.size): #if out of bound cell
						self.input[ind] = ENEMY
					else: #if it is a resource block
						self.input[ind] = float(board.grid[i][j].resources/board.max_resources) #feature scaling
					ind += 1

	def __init__(self, input_size, seed, max_depth, max_nodes, output_size, population_size, mutate_prob):
		"""
		:param input_size: length of the feature vector
		:param seed: seed for random library
		:param max_depth: max number of hidden layers
		:param max_nodes: max number of nodes per layer
		:param output_size: number of actions the agent can take
		"""

		# Collection of brains
		self.max_depth = max_depth
		self.population = [self.Brain(input_size, seed, max_depth, max_nodes, output_size) for _ in range(population_size)]
		self.mutate_prob = mutate_prob

	def calc_fitness(self, base_grid):
		"""
			Plays the game for each brain and calculates the fitness
		:return: None
		"""

		for brain in self.population:
			grid = copy.deepcopy(base_grid)
			brain.fitness = brain.play_game(grid, self.max_depth)


	def spawn_with_mutations(self, brain):
		new_brain = copy.deepcopy(brain)
		for layer in new_brain.brain:
			for i in range(len(layer)):
				for j in range(len(layer[i])):
					if rand.uniform(0, 1) > self.mutate_prob:
						layer[i][j] += layer[i][j]*rand.uniform(-1, 1)
		return new_brain

	def spawn_next_generation(self, base_grid):
		"""
			Runs the fitness of the brains
			Takes the top 25% and reproduces them
			spawns 50% more random brains
		:return:
		"""

		self.calc_fitness(base_grid)
		brains_sorted_by_fitenss = sorted([(brain.fitness, brain) for brain in self.population], key=lambda x: x[0])
		top_50 = [brain[1] for brain in brains_sorted_by_fitenss][:len(brains_sorted_by_fitenss)//2]

		next_generation = []
		for brain in top_50:
			next_generation.append(self.spawn_with_mutations(brain))
			next_generation.append(self.spawn_with_mutations(brain))

		return next_generation















