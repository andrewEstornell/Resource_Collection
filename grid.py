import random as rand
import copy as copy


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STAY = (0, 0)
actions = [UP, DOWN, LEFT, RIGHT, STAY]
SPAWN = "SPAWN"
demo_ship_spawn_rate = 10000

class Ship:

    #add :
    def __init__(self, position, capacity, id):
        self.position = position
        self.id = id
        self.capacity = capacity
        self.cargo = 0
        self.last_action = None


class DemoShip:
    """
        Spawn in 4 corners, greedily closes the distance to the closest friendly ship and attempts to sink it
        Can only move every other turn
    """
    def __init__(self, position):
        self.position = position
        self.last_action = [0, 0]

    def find_closest_ship(self, ships):
        """
            Find the closest ship to sink
        :param ships: list of the current friendly ships on the board
        :return: closest ship
        """
        best_ship = None
        best_dist = float('inf')
        for ship in ships:
            dist = abs(ship.position[0] - self.position[0]) + abs(ship.position[1] - self.position[1])
            if dist < best_dist:
                best_dist = dist
                best_ship = ship
        return best_ship

    def move(self, ships):
        """
            Makes a move towards the closest ship
            Calls find_closest_ship
        :param ships: list of friendly ships to sink
        :return: None
        """

        ship = self.find_closest_ship(ships)
        destination = ship.position
        x_dist = self.position[0] - destination[0]
        y_dist = self.position[1] - destination[1]
        if rand.uniform(0, 1) > 0.5:
            if x_dist < 0:
                self.position[0] += 1
                self.last_action = [1, 0]
            elif x_dist > 0:
                self.position[0] -= 1
                self.last_action = [-1, 0]
            elif y_dist < 0:
                self.position[1] += 1
                self.last_action = [0, 1]
            elif y_dist > 0:
                self.position[1] -= 1
                self.last_action = [0, -1]
            else:
                self.last_action = [0, 0]
        else:
            if y_dist < 0:
                self.position[1] += 1
                self.last_action = [0, 1]
            elif y_dist > 0:
                self.position[1] -= 1
                self.last_action = [0, -1]
            elif x_dist < 0:
                self.position[0] += 1
                self.last_action = [1, 0]
            elif x_dist > 0:
                self.position[0] -= 1
                self.last_action = [-1, 0]

            else:
                self.last_action = [0, 0]
        for ship in ships:
            if ship.position == tuple(self.position):
                print("Ship", ship.id, "destroyed by demo ship")
                return ship
        return None


class Cell:

    def __init__(self, resources, obstruction):
        self.obstruction = obstruction
        if self.obstruction:
            self.resources = 0
        else:
            self.resources = resources
        self.ship = None
        self.is_drop_off_point = False


class Grid:

    def __init__(self, size, seed, max_resources, spawning_cost, starting_point, ship_capacity, percent_pickup, sparsity,
                 demo_ship_turn):
        """

        :param size: INT, grid will be size*size
        :param seed: INT, gives the seed that determines the random generation of the map
        :param max_resources: INT, maximum resources anyone Cell can spawn with
        :param starting_point: TUPLE, location for the first collection point to be placed
        """
        rand.seed(seed)
        self.demo_ship_turn = demo_ship_turn
        self.iteration = 0
        self.ship_capacity = ship_capacity
        self.total_collection = 0
        self.max_resources = max_resources
        self.size = size
        self.spawning_cost = spawning_cost

        self.grid = [[Cell(resources=int(rand.uniform(0, 1) > sparsity)*rand.randint(0, max_resources), obstruction=False) for j in range(size)]
                                                                                        for i in range(size)]



        self.percent_pickup = percent_pickup
        self.starting_point = starting_point
        # Sets the first drop off point
        self.grid[starting_point[0]][starting_point[1]].is_drop_off_point = True
        self.grid[starting_point[0]][starting_point[1]].resources = 0
        # Spawns 4 ships around the drop off point
        self.ships = {1: Ship((starting_point[0] - 1, starting_point[1]), ship_capacity, 1),
                      2: Ship((starting_point[0], starting_point[1] + 1), ship_capacity, 2),
                      3: Ship((starting_point[0] + 1, starting_point[1]), ship_capacity, 3),
                      4: Ship((starting_point[0], starting_point[1] - 1), ship_capacity, 4)}

        self.demo_ships = {5: DemoShip([1, 1]), 6: DemoShip([self.size - 2, 1]),
                           7: DemoShip([1, self.size - 2]), 8: DemoShip([self.size - 2, self.size - 2])}
        
        s = 0
        for i in range(size):
            for j in range(size):
                s += self.grid[i][j].resources
        self.total_resources = s
        self.drop_offs = {-1: starting_point}
        self.next_id = 9
        # Adds each ship to the ship is
        for ship in self.ships.values():
            self.grid[ship.position[0]][ship.position[1]].ship = ship

    def __repr__(self):
        ret_val = ""
        for i in range(self.size):
            ret_val += "|"
            for j in range(self.size):
                if self.grid[i][j].ship is not None:
                    ret_val += "X|"
                elif self.grid[i][j].is_drop_off_point:
                    ret_val += "O|"
                else:
                    ret_val += "_|"
            ret_val += "\n"
        return ret_val

    def perform_actions(self, action_dict):
        """
        :param action_dict: DICT, contains the action for a given ship, keyed by the ship id
        :return:
        """
        #returns an iterator of the ship keys
        ship_ids = self.ships.keys()
        
        drop_off_ids = self.drop_offs.keys()#not sure

        #id is the key and the action (tuple)
        for id, ac in action_dict.items():
        
            # Validates id of the ship
            if id in drop_off_ids:
                if ac == SPAWN: #if one of the actions is to spawn a new ship
                    if self.spawning_cost <= self.total_collection: #if the ships collected enough resources to spawn a new ship
                        #add to the dictionary of ships a new ship and spawn it at drop_off
                        self.ships[self.next_id] = Ship(self.drop_offs[id], self.ship_capacity, self.next_id)
                        self.next_id += 1
                        self.total_collection -= self.spawning_cost #deduct from the total_collection the spawning cost since it has been used to spawn new ship
                        continue
                    else:#not enough resources to spawn the new ship
                        print("the action SPAWN was given but it cost", self.spawning_cost,
                              "while the total_collection was only", self.total_collection)
                        exit(-4)
                        
            elif id not in ship_ids: #a ship was given an action to perform but was not actually in the remaining ships
                print("ship", id, "was given action", ac, "but is not in the list of surviving ships")
                exit(-1)
                
            # Validates the bounds of the action
            if ac not in actions: #if the action is not one of the valid UP DOWN RIGHT LEFT STAY
                print("ship", id, "was given invalid action", ac)
                exit(-2)
                
            if id not in ship_ids: #an additional check that the ship id in action_dict is still alive
                print("ship", id, "was given action", ac, "but is not in the list of surviving ships")
                exit(-3)

            # Validates the bounds of the action. Makes sure ship doesn't go off the board
            ship = self.ships[id] #ship object
            pos = list(ship.position) #converts the ship position tuple to a list
            if pos[0] + ac[0] >= self.size or pos[1] + ac[1] >= self.size or pos[0] + ac[0] < 0 or pos[1] + ac[1] < 0:
                print("ship", id, "was given action", ac, "but pushed it off the edge of the board")


            # Performs the action
            self.grid[pos[0]][pos[1]].ship = None
            pos[0] += ac[0]
            pos[1] += ac[1]
            ship.position = tuple(pos)
            ship.last_action = ac

        # Checks for crashes and removes crashed ships
        ships = copy.deepcopy(list(self.ships.values()))
        for ship1 in ships:
            pos = ship1.position
            if pos[0] >= self.size or pos[1] >= self.size or pos[0] < 0 or pos[1] < 0:
                del self.ships[ship1.id]
                continue
            for ship2 in ships:
                if ship1.position == ship2.position and ship1.id != ship2.id: #if they are on same square but not the same ship
                    if ship1.id in self.ships.keys():
                        del self.ships[ship1.id]
                    if ship2.id in self.ships.keys():
                        del self.ships[ship2.id]

        # Updates ships that did not crash
        for ship in self.ships.values():
            # Collects resources from current square
            resource_gain = int(min(ship.capacity, ship.cargo + self.grid[ship.position[0]][ship.position[1]].resources * self.percent_pickup) - ship.cargo)
            ship.cargo += resource_gain
            #print("id:", ship.id, "|| resource gain:", resource_gain, "|| cargo,", ship.cargo)
            self.grid[ship.position[0]][ship.position[1]].resources -= resource_gain
            self.total_resources -= resource_gain
            
            # If current square is a drop off, add cargo to the total collection
            if self.grid[ship.position[0]][ship.position[1]].is_drop_off_point:
                self.total_collection += ship.cargo
                ship.cargo = 0

            self.grid[ship.position[0]][ship.position[1]].ship = ship

        if self.total_resources == 0:
            print("Game Over. No more Resources")
            print("Score: ", self.total_collection)
            exit(1)

        # Performs demo ship actions on even rounds
        if self.iteration % demo_ship_spawn_rate == 0 and self.iteration != 0:
            self.demo_ships[self.next_id] = DemoShip([1, 1])
            self.next_id += 1
            self.demo_ships[self.next_id] = DemoShip([1, self.size - 2])
            self.next_id += 1
            self.demo_ships[self.next_id] = DemoShip([self.size - 2, 1])
            self.next_id += 1
            self.demo_ships[self.next_id] = DemoShip([self.size - 2, self.size - 2])
            self.next_id += 1

        if self.iteration % self.demo_ship_turn == 0:
            for demo_ship in self.demo_ships.values():
                s = demo_ship.move(list(self.ships.values()))
                if s is not None:
                    del self.ships[s.id]
                if len(list(self.ships.values())) == 0:
                    print("Game Over. Demo ship destroyed last cargo ship")
                    print("Score: ", self.total_collection)
                    exit(1)
        self.iteration += 1

