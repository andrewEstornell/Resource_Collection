from gui import *
from grid import *
from greedy import greedy_decision

size = 50
seed = 10
spawning_cost = 10000
max_resources = 400
starting_point = ((size-1)//2, (size-1)//2)
vehicle_capacity = 10000
percent_pickup = 1

gui_scale = 18

grid = Grid(size, seed, max_resources, spawning_cost, starting_point, vehicle_capacity, percent_pickup)
gui = GUI(grid, gui_scale)

if __name__=='__main__':
    it = 0
    while True:
        it += 1

        action_dict = {}
        greedy_decision(grid, action_dict)

        #if the total resources collected are greater than the cost, add a spawn action
        if grid.total_collection >= grid.spawning_cost:
            action_dict[-1] = SPAWN
            
        
        print("iteration:",it)
        for id in grid.vehicles.keys():
            print("Vehicle", id, "contains", grid.vehicles[id].cargo, "resources")
    
        #action_dict is a dictionary with vehicle number: random move
        grid.perform_actions(action_dict)
        gui.update()

        #if there are no more vehicles in the game
        if len(list(grid.vehicles.keys())) == 0:
            break

    print("Game finished with ", grid.total_collection, "score")
    gui.root.mainloop()

