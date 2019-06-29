from agents import *
from gui import *
from grid import *

MAX_GENERATIONS = 500

size = 10
seed = 25
spawning_cost = 2000
max_resources = 400
starting_point = ((size - 1) // 2, (size - 1) // 2)
ship_capacity = 2000
percent_pickup = 0.3
sparsity = 0.5

gui_scale = 18

grid = Grid(size, seed, max_resources, spawning_cost, starting_point, ship_capacity, percent_pickup, sparsity, 5)
gui = GUI(grid, gui_scale)

if __name__=='__main__':
    it = 0
    genetic_ai = SingleGeneticAI(25, 1, 3, 50, 1, 100, .5)
    while it < MAX_GENERATIONS:
        genetic_ai.calc_fitness(grid)
        genetic_ai.spawn_next_generation(grid)
        it+=1
