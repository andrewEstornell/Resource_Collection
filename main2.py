from agents import *
from gui import *
from grid import *
import pickle
MAX_GENERATIONS = 20

size = 10
seed = 1
spawning_cost = 2000
max_resources = 400
starting_point = ((size - 1) // 2, (size - 1) // 2)
ship_capacity = 2000
percent_pickup = 0.3
sparsity = 0.5

gui_scale = 18

grid = Grid(size, seed, max_resources, spawning_cost, starting_point, ship_capacity, percent_pickup, sparsity, 5)
gui = GUI(grid, gui_scale)

LOAD = False #should we load brains
#test for git purposes
file_name = 'geneticAI.obj'
if __name__=='__main__':
    it = 0

    if (LOAD):
        with open(file_name, 'rb') as input:
            genetic_ai = pickle.load(input)
    else:
        genetic_ai = SingleGeneticAI(25, 1, 3, 50, 1, 100, .5)

    #running AI
    while it < MAX_GENERATIONS:
        genetic_ai.calc_fitness(grid)
        genetic_ai.spawn_next_generation(grid)
        it+=1

    #saving output
    with open(file_name, 'wb') as output:
        pickle.dump(genetic_ai, output)

