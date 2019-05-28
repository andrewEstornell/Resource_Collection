from gui import *
from grid import *
from greedy import greedy_decision

MAX_ITERATIONS = 500

size = 25
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

if __name__ == '__main__':
	it = 0
	while True:
		it += 1

		action_dict = {}
		greedy_decision(grid, action_dict, it)

		# if the total resources collected are greater than the cost, add a spawn action
		#if grid.total_collection >= grid.spawning_cost:
		#	action_dict[-1] = SPAWN

		print("iteration:", it)

		grid.perform_actions(action_dict)
		gui.update()

		# if there are no more ships in the game
		if len(list(grid.ships.keys())) == 0:
			break
		if grid.total_resources == 0:
			break
		if it >= MAX_ITERATIONS:
			print("max iterations reached, game over")
			print(grid.total_collection)
			break

	print("Game finished with ", grid.total_collection, "score")
	gui.root.mainloop()
