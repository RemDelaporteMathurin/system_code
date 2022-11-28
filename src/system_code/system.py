import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt


class System:
    def __init__(self, boxes, dt=0.2):
        self.boxes = boxes
        self.initial_dt = dt
        self.dt = self.initial_dt
        self.equations = self.build_equations()
        self.current_time = 0
        self.t = [self.current_time]

    @property
    def boxes_and_traps(self):
        boxes = self.boxes
        traps = []
        for box in boxes:
            traps += box.traps
        return boxes + traps

    def build_equations(self):
        def equations(p):
            # map the inventories to the boxes
            box_conc_map = {}
            for i, box in enumerate(self.boxes_and_traps):
                box_conc_map[box] = p[i]

            # build

            for box in self.boxes_and_traps:
                box.build_equation(box_conc_map, self.dt)

            return [box.equation for box in self.boxes_and_traps]
        return equations

    def advance(self):
        initial_guess = [box.old_inventory for box in self.boxes_and_traps]
        inventories = fsolve(self.equations, initial_guess)
        for box, new_inventory in zip(self.boxes_and_traps, inventories):
            box.inventory = new_inventory
            box.old_inventory = new_inventory
            box.inventories.append(new_inventory)
            box.update()
        self.current_time += self.dt
        self.t.append(self.current_time)
        self.equations = self.build_equations()

    def run(self, duration):
        start_time = self.current_time
        while self.current_time - start_time < duration:
            self.advance()

    def reset(self):
        self.dt = self.initial_dt
        self.current_time = 0
        self.t = [self.current_time]
        for box in self.boxes:
            box.reset()
        self.equations = self.build_equations()


    def plot_inventories(self):
        for box in self.boxes:
            plt.plot(self.t, np.array(box.inventories), label=box.name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Inventories")
        plt.show()
