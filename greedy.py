import random as rand

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STAY = (0, 0)

#the function that makes the greedy decision
def greedy_decision(grid, action_dict):
    move_to_make = 0
    for vehicle in grid.vehicles.values():

        #if the vehicle has no space left and needs to drop off cargo
        if vehicle.cargo == vehicle.capacity:
            if vehicle.position[0] < grid.starting_point[0]: #go down
                move_to_make = DOWN
            elif vehicle.position[0] > grid.starting_point[0]: #go up
                move_to_make = UP
            elif vehicle.position[1] < grid.starting_point[1]: #go right
                move_to_make = RIGHT
            elif vehicle.position[1] > grid.starting_point[1]: #go left
                move_to_make = LEFT
            else:
                print("Vehicle is on starting point")
        #else continue collecting resources
        else:    
            pos = pos_of_max_resource(grid, vehicle)
            if grid.grid[pos[0]][pos[1]].resources == 0:#if all surounding blocks are 0, arbitrarily move left
                pos = LEFT
            move_to_make = pos
        action_dict[vehicle.id] = move_to_make
        
#finds the best position of the cell immediately surrounding the block with the greatest resource        
def pos_of_max_resource(grid, vehicle):
    up = (vehicle.position[0]-1, vehicle.position[1])
    down = (vehicle.position[0]+1, vehicle.position[1])
    left = (vehicle.position[0], vehicle.position[1]-1)
    right = (vehicle.position[0], vehicle.position[1]+1)
    max_resource = max(grid.grid[up[0]][up[1]].resources, grid.grid[down[0]][down[1]].resources, grid.grid[left[0]][left[1]].resources, grid.grid[right[0]][right[1]].resources)
    print("MAX", max_resource)
    if grid.grid[up[0]][up[1]].resources == max_resource:
        return UP
    elif grid.grid[down[0]][down[1]].resources == max_resource:
        return DOWN
    elif grid.grid[left[0]][left[1]].resources == max_resource:
        return LEFT
    else:
        return RIGHT
    
def random_decision(grid, action_dict):
    #returns 100 tuples that can randomly be one of the move options
    actions = rand.choices([UP, DOWN, LEFT, RIGHT, STAY], k=100)

    #iterate through the vehicles and assign a random move to each
    for i in list(grid.vehicles.keys()):
        action_dict[i] = actions[i - 1]
