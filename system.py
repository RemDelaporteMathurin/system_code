import sympy as sp
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt


class System:
    def __init__(self, boxes):
        self.boxes = boxes
        self.dt = 0.2
        self.equations = self.build_equations()
        self.current_time = 0
        self.t = [self.current_time]

    def build_equations(self):
        def equations(p):
            # V*(c- c_n)/dt = sum( flow_rate * c_inputs) - sum(flowrate*c) + generation
            list_of_eq = {}
            # initialise all equations to 0
            for box in self.boxes:
                list_of_eq[box.name] = 0

            # build
            for i, box in enumerate(self.boxes):
                list_of_eq[box.name] += -box.volume*(p[i] - box.old_concentration)/self.dt
                list_of_eq[box.name] += box.volume*box.generation_term
                for name, flowrate in zip(box.outputs.keys(), box.outputs.values()):
                    list_of_eq[box.name] += -flowrate*p[i]
                    list_of_eq[name] += flowrate*p[i]
            return [val for val in list_of_eq.values()]
        return equations

    def advance(self):
        initial_guess = [box.old_concentration for box in self.boxes]
        concentrations = fsolve(self.equations, initial_guess)
        for box, new_concentration in zip(self.boxes, concentrations):
            box.concentration = new_concentration
            box.old_concentration = box.concentration
            box.concentrations.append(new_concentration)
        self.current_time += self.dt
        self.t.append(self.current_time)
        self.equations = self.build_equations()

    def run(self, duration):
        start_time = self.current_time
        while self.current_time - start_time < duration:
            self.advance()

    def plot_concentrations(self):
        for box in self.boxes:
            plt.plot(self.t, box.concentrations, label=box.name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Concentrations")
        plt.show()

    def plot_inventories(self):
        for box in self.boxes:
            plt.plot(self.t, np.array(box.concentrations)*box.volume, label=box.name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Inventories")
        plt.show()


class Box:
    def __init__(self, name, outputs, volume, initial_concentration=0, generation_term=0):
        self.outputs = outputs
        self.name = name
        self.inputs = []
        self.volume = volume
        self.concentration = initial_concentration
        self.old_concentration = initial_concentration
        self.concentrations = [self.concentration]
        self.generation_term = generation_term


storage = Box("Storage", {"Plasma": 0.45}, volume=100, initial_concentration=1/100)
plasma = Box("Plasma", {}, volume=1, generation_term=-1, initial_concentration=1)
breeder = Box("Breeder", {"Storage": 1}, volume=1, generation_term=1.2)
out = Box("Out", outputs={}, volume=1, initial_concentration=0)
my_system = System([storage, plasma, breeder, out])
# my_system.run(20)
while my_system.current_time < 20:
    my_system.advance()

    # Example of conditional flowrate
    # if breeder.concentration*breeder.outputs["Storage"] > storage.concentration*storage.outputs["Plasma"]:
    #     storage.outputs["Out"] = (breeder.concentration*breeder.outputs["Storage"] - injection_rate)/storage.concentration

    # Modify flowrate according to injection rate
    injection_rate = 1
    storage.outputs["Plasma"] = injection_rate/storage.concentration
my_system.plot_inventories()
