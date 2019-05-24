import random as rand

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STAY = (0, 0)

dead_blocks = []
radius = 1/5


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
            move = greedy_move(grid, vehicle)

            #if all blocks in surounding radius are 0, expand the radius that the greedy searches
            if grid.grid[move[0]][move[1]].resources == 0:
                global radius
                radius = min(radius*2, 1)
                    
            move_to_make = move

        #a check to make sure the move does not result in a crash
        potential_block = (vehicle.position[0] + move_to_make[0], vehicle.position[1]+move_to_make[1])
        if potential_block in dead_blocks:
            if (vehicle.position[0] + UP[0], vehicle.position[1] + UP[1]) not in dead_blocks:
                move_to_make = UP
            elif (vehicle.position[0] + DOWN[0], vehicle.position[1] + DOWN[1]) not in dead_blocks:
                move_to_make = DOWN
            elif (vehicle.position[0] + LEFT[0], vehicle.position[1] + LEFT[1]) not in dead_blocks:
                move_to_make = LEFT
            elif (vehicle.position[0] + RIGHT[0], vehicle.position[1] + RIGHT[1]) not in dead_blocks:
                move_to_make = RIGHT
            else:
                move_to_make = STAY
            potential_block = (vehicle.position[0] + move_to_make[0], vehicle.position[1]+move_to_make[1])
            
        action_dict[vehicle.id] = move_to_make
        dead_blocks.append(potential_block) 
        
    dead_blocks.clear()
        
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

    #figure out direction of the best move and move towards it greedily
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

#finds the neighbor with the most resources
def find_best_neighbor(move1, move2, pos, grid):
    pos_1 = (pos[0] + move1[0], pos[1] + move1[1]) #position on the grid of the first possible move
    pos_2 = (pos[0] + move2[0], pos[1] + move2[1]) #position on the grid of the second possible move

    if grid.grid[pos_1[0]][pos_1[1]].resources > grid.grid[pos_2[0]][pos_2[1]].resources:
        return move1
    else:
        return move2
