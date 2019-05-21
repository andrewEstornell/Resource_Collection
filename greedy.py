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
            pos = greedy_move(grid, vehicle)
            if grid.grid[pos[0]][pos[1]].resources == 0:#if all surounding blocks are 0, arbitrarily move left
                pos = LEFT
            move_to_make = pos
        action_dict[vehicle.id] = move_to_make

#if the blocks in the radius surounding the ship are all 0, and the ship is on a 0 block, then the ship should move towards the quadrant of the cell with the greatest resources
def find_best_quadrant(grid):
    half = grid.size//2
    quadrant_resources = {}
    quadrant_resources[1] = 0
    quadrant_resources[2] = 0
    quadrant_resources[3] = 0
    quadrant_resources[4] = 0
    for i in range(grid.size):
        for j in range(grid.size):
            res = grid.grid[i][j].resources
            if i < half and j < half:
                quadrant_resources[1] += res
            elif i < half:
                quadrant_resources[2] += res
            elif j < half:
                quadrant_resources[3] += res
            else:
                quadrant_resources[4] += res
    max_res = max(quadrant_resources.values())
    for i in quadrant_resources.keys():
        if quadrant_resources[i] == max_res:
            return i

        
#finds the best position of the cell immediately surrounding the block with the greatest resource        
def greedy_move(grid, vehicle):
    up = (vehicle.position[0]-1, vehicle.position[1])
    down = (vehicle.position[0]+1, vehicle.position[1])
    left = (vehicle.position[0], vehicle.position[1]-1)
    right = (vehicle.position[0], vehicle.position[1]+1)
    stay = (vehicle.position[0], vehicle.position[1])
    max_resource = max(grid.grid[up[0]][up[1]].resources, grid.grid[down[0]][down[1]].resources, grid.grid[left[0]][left[1]].resources, grid.grid[right[0]][right[1]].resources, grid.grid[stay[0]][stay[1]].resources)

    if grid.grid[up[0]][up[1]].resources == max_resource: #if up is the cell with max resources
        return UP
    elif grid.grid[down[0]][down[1]].resources == max_resource: #if down is the cell with max resources
        return DOWN
    elif grid.grid[left[0]][left[1]].resources == max_resource: #if left is the cell with max resources
        return LEFT
    elif grid.grid[right[0]][right[1]].resources == max_resource: #if right is the cell with max resources
        return RIGHT
    else: #if stay is the cell with max resources
        return STAY


