from tkinter import *
import time as time


class GUI:

    def __init__(self, grid, scale):
        self.max_hex_val = 3095
        self.root = Tk()
        self.scale = scale
        self.grid = grid
        self.size = grid.size * self.scale
        self.main_canvas = Canvas(self.root, width=self.size, height=self.size)
        self.rectangles = {}
        self.grid_rectangles = []
        self.demo_ship_recs = {}

        self.main_canvas.delete('grid_line')  # Will only remove the grid_line

        # Creates all vertical lines at intevals of 100
        for i in range(0, self.size, self.scale):
            self.main_canvas.create_line([(i, 0), (i, self.size)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, self.size, self.scale):
            self.main_canvas.create_line([(0, i), (self.size, i)], tag='grid_line')
        self.main_canvas.pack()

        for i in range(self.grid.size):
            row = []
            for j in range(self.grid.size):
                val = int(grid.grid[i][j].resources / grid.max_resources * self.max_hex_val) + 1

                scale = self.max_hex_val - val
                rec = self.main_canvas.create_rectangle(i*self.scale, j*self.scale, (i + 1)*self.scale, (j + 1)*self.scale,
                                                        fill='#' + format(scale + 1000, '03x') + format(scale + 100, '03x') + format(scale + 1000, '03x'))
                row.append(rec)
                if self.grid.grid[i][j].ship is not None:
                    ship = grid.grid[i][j].ship
                    rec = self.main_canvas.create_rectangle(ship.position[0]*self.scale, ship.position[1]*self.scale,
                                                            (ship.position[0] + 1)*self.scale, (ship.position[1] + 1)*self.scale,
                                                            fill="#111ddd111")
                    self.rectangles[ship.id] = rec

                elif self.grid.grid[i][j].is_drop_off_point:
                    self.main_canvas.create_rectangle(i*self.scale, j*self.scale, (i + 1)*self.scale, (j + 1)*self.scale,
                                                      fill="#222222fff")
            self.grid_rectangles.append(row)
        self.info = self.main_canvas.create_text(self.size - 200, 40, fill="#000fffaaa",
                                                 font="Times 40 italic bold", text="Score : 0")

    def update(self):
        ship_ids = list(self.grid.ships.keys())
        for id in ship_ids:
           if id not in self.rectangles.keys():
                rec = self.main_canvas.create_rectangle(self.grid.ships[id].position[0] * self.scale,
                                                        self.grid.ships[id].position[1] * self.scale,
                                                        (self.grid.ships[id].position[0] + 1) * self.scale,
                                                        (self.grid.ships[id].position[1] + 1) * self.scale,
                                                        fill="#111ddd111")
                self.rectangles[id] = rec

        ship_ids = list(self.grid.ships.keys())
        time.sleep(.1)
        for id in list(self.rectangles.keys()):
            if id not in ship_ids:
                print("ship", id, "crashed")
                self.main_canvas.delete(self.rectangles[id])
                #self.main_canvas.pack()
                #self.root.update()
                del self.rectangles[id]
                continue


            self.main_canvas.tag_raise(self.rectangles[id])
            if self.grid.ships[id].last_action is not None:
                self.main_canvas.move(self.rectangles[id],self.grid.ships[id].last_action[0]*self.scale,
                                      self.grid.ships[id].last_action[1]*self.scale)
            self.main_canvas.pack()
            self.root.update()

        for i in range(self.grid.size):
            for j in range(self.grid.size):
                val = int((self.grid.grid[i][j].resources / self.grid.max_resources) * self.max_hex_val) + 1

                scale = self.max_hex_val - val
                #print((scale, val), "|", end="")
                #print(format(scale, '03x'), end=" ")
                self.main_canvas.itemconfigure(self.grid_rectangles[i][j],
                                               fill='#' + format(scale + 1000, '03x') + format(scale + 100, '03x') + format(scale + 1000, '03x'))
            #print("")
        self.main_canvas.itemconfigure(self.info, text="Score : " + str(self.grid.total_collection))
        for id in self.grid.demo_ships.keys():
            if id not in self.demo_ship_recs.keys():
                rec = self.main_canvas.create_rectangle(self.grid.demo_ships[id].position[0] * self.scale,
                                                        self.grid.demo_ships[id].position[1] * self.scale,
                                                        (self.grid.demo_ships[id].position[0] + 1) * self.scale,
                                                        (self.grid.demo_ships[id].position[1] + 1) * self.scale,
                                                        fill="#fff000000")
                self.demo_ship_recs[id] = rec
            last_ac = self.grid.demo_ships[id].last_action
            if last_ac is not None and self.grid.iteration % self.grid.demo_ship_turn == 0:
                self.main_canvas.move(self.demo_ship_recs[id], self.grid.demo_ships[id].last_action[0]*self.scale,
                                      self.grid.demo_ships[id].last_action[1]*self.scale)

        self.main_canvas.pack()
        self.root.update()




