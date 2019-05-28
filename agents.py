from grid import *
import numpy as np


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
			"""
			self.input = np.zeros([input_size, 1])
			self.fitness = 0
			self.brain = [np.zeros(1)] # This should be a list of numpy arrays, each 2D array is a layer of the brain


		def play_game(self, gird):
			"""
				Plays through a game given by grid,
			:param gird: object containing the resource collection game
			:return: the score of the game (fitness of the brain)
			"""

			self.fitness = gird.total_collection
			return self.fitness

		def forward_pass(self, features):
			"""
				Performs a forward pass of the network, the end result is an action for the agent
			:param features: input from the agent the AI is controlling
			:return: index of the action that the agent should make
			"""
			input_to_next_layer = features
			for layer in self.brain:
				input_to_next_layer = layer*input_to_next_layer
			output = input_to_next_layer
			return output

	def __init__(self, input_size, seed, max_depth, max_nodes, output_size, population_size, mutate_prob):
		"""

		:param input_size: length of the feature vector
		:param seed: seed for random library
		:param max_depth: max number of hidden layers
		:param max_nodes: max number of nodes per layer
		:param output_size: number of actions the agent can take
		"""

		# Collection of brains
		self.population = [self.Brain(input_size, seed, max_depth, max_nodes, output_size) for _ in range(population_size)]
		self.mutate_prob = mutate_prob

	def calc_fitness(self):
		"""
			Plays the game for each brain and calculates the fitness
		:return: None
		"""
		for brain in self.population:
			grid = Grid() # fill in
			brain.play_game(grid)

	def spawn_with_mutations(self, brain):
		new_brain = copy.deepcopy(brain)
		for layer in new_brain.brain:
			for i in range(len(layer)):
				for j in range(len(layer[i])):
					if rand.uniform(0, 1) > self.mutate_prob:
						layer[i][j] += layer[i][j]*rand.uniform(-1, 1)
		return new_brain

	def spawn_next_generation(self):
		"""
			Runs the fitness of the brains
			Takes the top 25% and reproduces them
			spawns 50% more random brains
		:return:
		"""
		self.calc_fitness()
		brains_sorted_by_fitenss = sorted([(brain.fitness, brain) for brain in self.population], key=lambda x: x[0])

		# Make mutations

		# Spawn 50% more


















