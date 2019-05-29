import random as rand
from grid import *

dead_blocks = []  # contains blocks that a ship is already set to land on
radius = 1 / 5


# the function that makes the greedy decision
def greedy_decision(grid, action_dict, it):
	"""
	param grid: GRID
	param action_dict: DICTIONARY, holds moves made by greedy algorithm

	The greedy_decision function makes a move for each ship. It either moves the ship towards the drop off point if the ship is at max capacity,
	or it makes a move using the greed_move function. It then validates that the move will not result in a crash. If it does it finds a move that will not
	result in a crash
	"""
	it -= 1
	move_to_make = 0
	for ship in grid.ships.values():

		#add blocks that would put ship within radius 1 of demolition ships to dead blocks

		# if the ship has no space left and needs to drop off cargo
		if ship.cargo == ship.capacity:
			if ship.position[0] < grid.starting_point[0]:  # go down
				move_to_make = DOWN
			elif ship.position[0] > grid.starting_point[0]:  # go up
				move_to_make = UP
			elif ship.position[1] < grid.starting_point[1]:  # go right
				move_to_make = RIGHT
			elif ship.position[1] > grid.starting_point[1]:  # go left
				move_to_make = LEFT
			else:
				print("ship is on starting point")
		# else continue collecting resources
		else:
			move = greedy_move(grid, ship)

			# if all blocks in surounding radius are 0, expand the radius that the greedy searches
			if grid.grid[move[0]][move[1]].resources == 0:
				global radius
				radius = min(radius * 2, 2)
			move_to_make = move

		#adds places where ship would be within 1 move of demo ship to dead blocks
		demo_dead_blocks = add_demo_dead_blocks(dead_blocks, ship, grid)
		#adds places where ship would go off edge to dead blocks
		off_edge_dead_blocks = off_edge(dead_blocks, ship, grid)
		# a check to make sure the move does not result in a crash
		potential_block = (ship.position[0] + move_to_make[0], ship.position[1] + move_to_make[1])
		if potential_block in dead_blocks:
			r = rand.random()
			#4 possible positons
			p1 = ship.position[0] + UP[0], ship.position[1] + UP[1]
			p2 = ship.position[0] + DOWN[0], ship.position[1] + DOWN[1]
			p3 = ship.position[0] + LEFT[0], ship.position[1] + LEFT[1]
			p4 = ship.position[0] + RIGHT[0], ship.position[1] + RIGHT[1]
			if r < .25:
				move_to_make = make_random_move(p1, p2, p3, p4, UP, DOWN, LEFT, RIGHT, dead_blocks)
			elif r < .5:
				move_to_make = make_random_move(p2, p3, p4, p1, DOWN, LEFT, RIGHT, UP, dead_blocks)
			elif r < .75:
				move_to_make = make_random_move(p3, p4, p1, p2, LEFT, RIGHT, UP, DOWN, dead_blocks)
			else:
				move_to_make = make_random_move(p4, p1, p2, p3, RIGHT, UP, DOWN, LEFT, dead_blocks)
			potential_block = (ship.position[0] + move_to_make[0], ship.position[1] + move_to_make[1])

		#the last demo_dead_blocks that were added to this list only apply to an individual ship
		for i in range(demo_dead_blocks + off_edge_dead_blocks):
			del(dead_blocks[-1])

		action_dict[ship.id] = move_to_make
		dead_blocks.append(potential_block)

	dead_blocks.clear()

def avoid_demo(db, ship, grid):
	"""
	:param db: LIST dead blocks
	:param ship: SHIP
	:param grid: GRID
	:return: INT, number of avoided demo ships
	avoid demo ships on turns where they do not move
	"""
	to_ret = 0
	up = (ship.position[0] + UP[0], ship.position[1] + UP[1])
	down = (ship.position[0] + DOWN[0], ship.position[1] + DOWN[1])
	left = (ship.position[0] + LEFT[0], ship.position[1] + LEFT[1])
	right = (ship.position[0] + RIGHT[0], ship.position[1] + RIGHT[1])
	demo_ship_blocks = []
	for demo_ship in grid.demo_ships.values():
		demo_ship_blocks.append(tuple(demo_ship.position))
	if up in demo_ship_blocks:
		to_ret += 1
		db.append(up)
	if down in demo_ship_blocks:
		to_ret += 1
		db.append(down)
	if left in demo_ship_blocks:
		to_ret += 1
		db.append(left)
	if right in demo_ship_blocks:
		to_ret += 1
		db.append(right)
	return to_ret

def off_edge(db, ship, grid):
	"""
	:param db: LIST, dead blocks
	:param ship: SHIP
	:param grid: GRID
	:return: INT, number of potential off edge blocks
	adds blocks that would be off map to dead blocks
	"""
	to_ret = 0
	n = grid.size
	up = (ship.position[0] + UP[0], ship.position[1] + UP[1])
	down = (ship.position[0] + DOWN[0], ship.position[1] + DOWN[1])
	left = (ship.position[0] + LEFT[0], ship.position[1] + LEFT[1])
	right = (ship.position[0] + RIGHT[0], ship.position[1] + RIGHT[1])
	if not in_bound(up[0], up[1], n):
		to_ret += 1
		db.append(up)
	if not in_bound(down[0], down[1], n):
		to_ret += 1
		db.append(down)
	if not in_bound(left[0], left[1], n):
		to_ret += 1
		db.append(left)
	if not in_bound(right[0], right[1], n):
		to_ret += 1
		db.append(right)
	return to_ret
def make_random_move(p1, p2, p3, p4, m1, m2, m3, m4, db):
	"""
	:param p1: TUPLE
	:param p2: TUPLE
	:param p3: TUPLE
	:param p4: TUPLE
	:param m1: TUPLE
	:param m2: TUPLE
	:param m3: TUPLE
	:param m4: TUPLE
	:param db: DICTIONARY
	:return: TUPLE
	p represent the possible positions on the board
	m represent the corresponding move towards those positions
	"""
	if p1 not in db:
		return m1
	elif p2 not in db:
		return m2
	elif p3 not in db:
		return m3
	elif p4 not in db:
		return m4
	else:
		return STAY
#looks at all the positions where demolition ships create dead block and adds them to the dead_blocks list
def add_demo_dead_blocks(db, ship, grid):
	"""
	:param db: LIST, contains dead blocks
	:param ship: SHIP
	:param grid: GRID
	:return: INT, number of dead blocks added
	create the 4 possible moves: up, down, left, and right, and see if they are surrounded by demo ships. If so, mark them
	as dead blocks
	"""
	num_dead = 0
	up = (ship.position[0] + UP[0], ship.position[1] + UP[1])
	down = (ship.position[0] + DOWN[0], ship.position[1] + DOWN[1])
	left = (ship.position[0] + LEFT[0], ship.position[1] + LEFT[1])
	right = (ship.position[0] + RIGHT[0], ship.position[1] + RIGHT[1])
	if has_demo_neighbors(up, grid):
		num_dead += 1
		db.append(up)
	if has_demo_neighbors(down, grid):
		num_dead += 1
		db.append(down)
	if has_demo_neighbors(left, grid):
		num_dead += 1
		db.append(left)
	if has_demo_neighbors(right, grid):
		num_dead += 1
		db.append(right)
	return num_dead

def has_demo_neighbors(pos, grid):
	"""
	:param pos: TUPLE, potential position of the block to inspect
	:param grid: GRID
	:return: BOOLEAN, true if pos has demo ship around it
	Looks at all surrounding blocks for demo ships, if there is one then the position will be marked as a dead block
	"""
	to_ret = False
	up = (pos[0] + UP[0], pos[1] + UP[1])
	down = (pos[0] + DOWN[0], pos[1] + DOWN[1])
	left = (pos[0] + LEFT[0], pos[1] + LEFT[1])
	right = (pos[0] + RIGHT[0], pos[1] + RIGHT[1])
	l = [up, down, left, right, pos]
	for demo_ship in grid.demo_ships.values():
		if tuple(demo_ship.position) in l:
			to_ret = True
			break
	return to_ret

# finds the best position of the cell immediately surrounding the block with the greatest resource
def greedy_move(grid, ship):
	"""
        :param grid: GRID
        :param ship: SHIP
        :return: TUPLE, the move the greedy makes
        The greedy_move function evaluates all the cells in a predefined radius. The cells are put into a dictionary with the position of the cell
        as a key and the value of its resources/ the distance from the ship squared. Then the cell with the most resources is determined.
        After that, a move is determined based on where the cell is. If the cell is simply up, down, left, or right of the ship then that is the move
        that will be picked. If the cell is up/right, up/left, down/right, or down/left from the ship, then the ship will move towards that cell
        in the most greedy way possible.
        """
	pos = ship.position
	# scan some radius of the board and create a move vector
	move_vector = {}
	n = int(radius * .5 * grid.size)
	for i in range(pos[0] - n, pos[0] + (n + 1)):
		for j in range(pos[1] - n, pos[1] + (n + 1)):
			if in_bound(i, j, grid.size):
				distance = abs(i - pos[0]) + abs(j - pos[1])
				if distance == 0:
					distance = 1
				move_vector[(i, j)] = grid.grid[i][j].resources / (distance ** 2)
	# find the max of the move vector from that find the bext move
	max_resource = max(move_vector.values())
	best_move = 0
	for move in move_vector:
		if max_resource == move_vector[move]:
			best_move = move
			break

	move_to_ret = 0

	# figure out direction of the best move and move towards it greedily
	i = best_move[0]
	j = best_move[1]

	if pos[0] > i and pos[1] < j:  # up and to the right
		move_to_ret = find_best_neighbor(UP, RIGHT, pos, grid)
	elif pos[0] < i and pos[1] < j:  # down and to the right
		move_to_ret = find_best_neighbor(DOWN, RIGHT, pos, grid)
	elif pos[0] > i and pos[1] > j:  # up and to the left
		move_to_ret = find_best_neighbor(UP, LEFT, pos, grid)
	elif pos[0] < i and pos[1] > j:  # down and to the left
		move_to_ret = find_best_neighbor(DOWN, LEFT, pos, grid)
	elif pos[0] > i:  # up
		move_to_ret = UP
	elif pos[0] < i:  # down
		move_to_ret = DOWN
	elif pos[1] > j:  # left
		move_to_ret = LEFT
	elif pos[1] < j:  # right
		move_to_ret = RIGHT
	else:  # stay
		move_to_ret = STAY

	return move_to_ret


# makes sure potential coordinates are in bound
def in_bound(i, j, size):
	"""
        param i: INT, row coordinate of the grid
        param j: INT, column coordinate of the grid
        param size: INT, size of grid
        in_bound returns True if i and j are both on the board, False otherwise
        """
	return i >= 0 and j >= 0 and i < size and j < size


# finds the neighbor with the most resources
def find_best_neighbor(move1, move2, pos, grid):
	"""
        param move1: TUPLE
        param move2: TUPLE, move 1 and move 2 are one of the predefined moves at the top
        param pos: TUPLE, position of the ship
        param grid: GRID
        find_best_neighbor finds which neighbor has a higher resource count and returns that move
        """
	pos_1 = (pos[0] + move1[0], pos[1] + move1[1])  # position on the grid of the first possible move
	pos_2 = (pos[0] + move2[0], pos[1] + move2[1])  # position on the grid of the second possible move

	if grid.grid[pos_1[0]][pos_1[1]].resources > grid.grid[pos_2[0]][pos_2[1]].resources:
		return move1
	else:
		return move2
