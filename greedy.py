import random as rand

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STAY = (0, 0)
radius = 1/10

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

        
#finds the best position of the cell immediately surrounding the block with the greatest resource        
def greedy_move(grid, vehicle):
    pos = vehicle.position
    #scan some radius of the board and create a move vector
    move_vector = {}
    n = int(radius*.5*grid.size)
    for i in range(pos[0]-n, pos[0]+(n+1)):
        for j in range(pos[1]-n, pos[1]+(n+1)):
            if in_bound(i, j, grid.size):
                distance = abs(i-pos[0]) + abs(j-pos[1])
                if distance == 0:
                    distance = 1
                move_vector[(i, j)] = grid.grid[i][j].resources/(distance**2)
    #find the max of the move vector from that find the bext move 
    max_resource = max(move_vector.values())
    best_move = 0
    for move in move_vector:
        if max_resource == move_vector[move]:
            best_move = move
            break

    move_to_ret = 0

    #figure out direction of the best move and move towards it
    i = best_move[0]
    j = best_move[1]
    if pos[0] > i and pos[1] < j: #up and to the right
        move_to_ret = find_best_neighbor(UP, RIGHT, pos, grid)
    elif pos[0] < i and pos[1] < j: #down and to the right
        move_to_ret = find_best_neighbor(DOWN, RIGHT, pos, grid)
    elif pos[0] > i and pos[1] > j: #up and to the left
        move_to_ret = find_best_neighbor(UP, LEFT, pos, grid)
    elif pos[0] < i and pos[1] > j: #down and to the left
        move_to_ret = find_best_neighbor(DOWN, LEFT, pos, grid)
    elif pos[0] > i: #up
        move_to_ret = UP
    elif pos[0] < i: #down
        move_to_ret = DOWN
    elif pos[1] > j: #left
        move_to_ret = LEFT
    elif pos[1] < j: #right
        move_to_ret = RIGHT
    else:            #stay
        move_to_ret = STAY

    return move_to_ret

#makes sure potential coordinates are in bound
def in_bound(i, j, size):
    return i >= 0 and j >= 0 and i < size and j < size

def find_best_neighbor(move1, move2, pos, grid):
    pos_1 = (pos[0] + move1[0], pos[1] + move1[1]) #position on the grid of the first possible move
    pos_2 = (pos[0] + move2[0], pos[1] + move2[1]) #position on the grid of the second possible move

    if grid.grid[pos_1[0]][pos_1[1]].resources > grid.grid[pos_2[0]][pos_2[1]].resources:
        return move1
    else:
        return move2

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
