import random as rand
import copy as copy


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STAY = (0, 0)


class Vehicle:

    def __init__(self, position, capacity, id):
        self.position = position
        self.id = id
        self.capacity = capacity
        self.cargo = 0
        self.last_action = None


class Cell:

    def __init__(self, resources, obstruction):
        self.obstruction = obstruction
        if self.obstruction:
            self.resources = 0
        else:
            self.resources = resources
        self.vehicle = None
        self.is_drop_off_point = False


class Grid:

    def __init__(self, size, seed, max_resources, starting_point, vehicle_capacity, percent_pickup):
        """

        :param size: INT, grid will be size*size
        :param seed: INT, gives the seed that determines the random generation of the map
        :param max_resources: INT, maximum resources anyone Cell can spawn with
        :param starting_point: TUPLE, location for the first collection point to be placed
        """
        rand.seed(seed)
        self.total_collection = 0
        self.max_resources = max_resources
        self.size = size
        self.grid = [[Cell(resources=rand.randint(0, max_resources), obstruction=False) for j in range(size)]
                                                                                        for i in range(size)]
        self.percent_pickup = percent_pickup
        self.starting_point = starting_point
        # Sets the first drop off point
        self.grid[starting_point[0]][starting_point[1]].is_drop_off_point = True
        # Spawns 4 ships around the drop off point
        self.vehicles = {1: Vehicle((starting_point[0] - 1, starting_point[1]), vehicle_capacity, 1),
                         2: Vehicle((starting_point[0], starting_point[1] + 1), vehicle_capacity, 2),
                         3: Vehicle((starting_point[0] + 1, starting_point[1]), vehicle_capacity, 3),
                         4: Vehicle((starting_point[0], starting_point[1] - 1), vehicle_capacity, 4)}
        # Adds each vehicle to the vehicle is
        for vehicle in self.vehicles.values():
            self.grid[vehicle.position[0]][vehicle.position[1]].vehicle = vehicle

    def __repr__(self):
        ret_val = ""
        for i in range(self.size):
            ret_val += "|"
            for j in range(self.size):
                if self.grid[i][j].vehicle is not None:
                    ret_val += "X|"
                elif self.grid[i][j].is_drop_off_point:
                    ret_val += "O|"
                else:
                    ret_val += "_|"
            ret_val += "\n"
        return ret_val

    def perform_actions(self, action_dict):
        """
        :param action_dict: DICT, contains the action for a given vehicle, keyed by the vehicle id
        :return:
        """
        vehicle_ids = self.vehicles.keys()
        for id, ac in action_dict.items():
            # Validates id of the ship
            if id not in vehicle_ids:
                print("ship", id, "was given action", ac, "but is not in the list of surviving vehicles")
                exit(-1)
            # Validates the bounds of the action
            vehicle = self.vehicles[id]
            pos = list(vehicle.position)
            if pos[0] + ac[0] >= self.size or pos[1] + ac[1] >= self.size or pos[0] + ac[0] < 0 or pos[1] + ac[1] < 0:
                print("vehicle", id, "was given action", ac, "but pushed it off the edge of the board")


            # Performs the action
            self.grid[pos[0]][pos[1]].vehicle = None
            pos[0] += ac[0]
            pos[1] += ac[1]
            vehicle.position = tuple(pos)
            vehicle.last_action = ac

        # Checks for crashes and removes crashed vehicles
        vehicles = copy.deepcopy(list(self.vehicles.values()))
        for vehicle1 in vehicles:
            pos = vehicle1.position
            if pos[0] >= self.size or pos[1] >= self.size or pos[0] < 0 or pos[1] < 0:
                del self.vehicles[vehicle1.id]
                continue
            for vehicle2 in vehicles:
                if vehicle1.position == vehicle2.position and vehicle1.id != vehicle2.id:
                    if vehicle1.id in self.vehicles.keys():
                        del self.vehicles[vehicle1.id]
                    if vehicle2.id in self.vehicles.keys():
                        del self.vehicles[vehicle2.id]

        # Updates vehicles that did not crash
        for vehicle in self.vehicles.values():
            # Collects resources from current square
            resource_gain = int(min(vehicle.capacity, vehicle.cargo + self.grid[vehicle.position[0]][vehicle.position[1]].resources * self.percent_pickup) - vehicle.cargo)
            vehicle.cargo += resource_gain
            print("id:", vehicle.id, "|| resource gain:", resource_gain, "|| cargo,", vehicle.cargo)
            self.grid[vehicle.position[0]][vehicle.position[1]].resources -= resource_gain

            # If current square is a drop off, add cargo to the total collection
            if self.grid[vehicle.position[0]][vehicle.position[1]].is_drop_off_point:
                self.total_collection += vehicle.cargo
                vehicle.cargo = 0

            self.grid[vehicle.position[0]][vehicle.position[1]].vehicle = vehicle




