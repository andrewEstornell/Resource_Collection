from gui import *
from grid import *
import random as rand

size = 51
seed = 1
spawning_cost = 100
max_resources = 400
starting_point = ((size-1)//2, (size-1)//2)
ship_capacity = 999999
percent_pickup = 1

gui_scale = 18

grid = Grid(size, seed, max_resources, spawning_cost, starting_point, ship_capacity, percent_pickup)
gui = GUI(grid, gui_scale)

it = 0
while True:
    it += 1
    actions = rand.choices([UP, DOWN, LEFT, RIGHT, STAY], k=100)

    action_dict = {}
    if grid.total_collection >= grid.spawning_cost:
        action_dict[-1] = SPAWN

    print(it, len(list(grid.ships.keys())))
    for i in list(grid.ships.keys()):
        action_dict[i] = actions[i - 1]
    grid.perform_actions(action_dict)
    gui.update()
    if len(list(grid.ships.keys())) == 0:
        break

print("Game finished with ", grid.total_collection, "score")
gui.root.mainloop()