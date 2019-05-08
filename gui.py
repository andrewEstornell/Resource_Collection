from tkinter import *
import time as time


class GUI:

    def __init__(self, grid, scale):
        self.root = Tk()
        self.scale = scale
        self.grid = grid
        size = grid.size * self.scale
        self.main_canvas = Canvas(self.root, width=size, height=size)
        self.rectangles = {}
        self.grid_rectangles = []

        self.main_canvas.delete('grid_line')  # Will only remove the grid_line

        # Creates all vertical lines at intevals of 100
        for i in range(0, size, self.scale):
            self.main_canvas.create_line([(i, 0), (i, size)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, size, self.scale):
            self.main_canvas.create_line([(0, i), (size, i)], tag='grid_line')
        self.main_canvas.pack()

        for i in range(self.grid.size):
            row = []
            for j in range(self.grid.size):
                val = int(grid.grid[i][j].resources / grid.max_resources * 999)

                scale = 999 - val
                rec = self.main_canvas.create_rectangle(i*self.scale, j*self.scale, (i + 1)*self.scale, (j + 1)*self.scale,
                                                        fill='#' + str(scale) + str(scale) + str(scale))
                row.append(rec)
                if self.grid.grid[i][j].vehicle is not None:
                    vehicle = grid.grid[i][j].vehicle
                    rec = self.main_canvas.create_rectangle(vehicle.position[0]*self.scale, vehicle.position[1]*self.scale,
                                                            (vehicle.position[0] + 1)*self.scale, (vehicle.position[1] + 1)*self.scale,
                                                            fill="green")
                    self.rectangles[vehicle.id] = rec

                elif self.grid.grid[i][j].is_drop_off_point:
                    self.main_canvas.create_rectangle(i*self.scale, j*self.scale, (i + 1)*self.scale, (j + 1)*self.scale,
                                                      fill="blue")
            self.grid_rectangles.append(row)

    def update(self):
        vehicle_ids = list(self.grid.vehicles.keys())
        for id in list(self.rectangles.keys()):
            if id not in vehicle_ids:
                print("vehicle", id, "crashed")
                self.main_canvas.delete(self.rectangles[id])
                #self.main_canvas.pack()
                #self.root.update()
                del self.rectangles[id]
                continue

            time.sleep(0.1)

            self.main_canvas.tag_raise(self.rectangles[id])
            self.main_canvas.move(self.rectangles[id],
                                  self.grid.vehicles[id].last_action[0]*self.scale, self.grid.vehicles[id].last_action[1]*self.scale)
            self.main_canvas.pack()
            self.root.update()

        for i in range(self.grid.size):
            for j in range(self.grid.size):
                val = int(self.grid.grid[i][j].resources / self.grid.max_resources * 999)

                scale = 999 - val
                self.main_canvas.itemconfigure(self.grid_rectangles[i][j], fill='#' + str(scale) + str(scale) + str(scale))
                #self.main_canvas.itemconfigure(self.grid_rectangles[i][j], fill='#000fff000')



