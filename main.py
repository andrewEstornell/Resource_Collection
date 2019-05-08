from gui import *
from grid import *
import random as rand


grid = Grid(41, 1, 200, (20, 20), 9999999, 0.9)
gui = GUI(grid, 20)

while True:
    actions = rand.choices([UP, DOWN, LEFT, RIGHT], k=4)

    action_dict = {}
    for i in list(grid.vehicles.keys()):
        action_dict[i] = actions[i - 1]
    grid.perform_actions(action_dict)
    gui.update()

gui.root.mainloop()

