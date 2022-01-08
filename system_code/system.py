import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

from system_code import LAMBDA


class System:
    def __init__(self, boxes, dt=0.2):
        self.boxes = boxes
        self.dt = dt
        self.equations = self.build_equations()
        self.current_time = 0
        self.t = [self.current_time]

    def build_equations(self):
        def equations(p):
            # map the concentrations to the boxes
            box_conc_map = {}
            for i, box in enumerate(self.boxes):
                box_conc_map[box.name] = p[i]

            # V*(c- c_n)/dt = sum( flow_rate * c_inputs) - sum(flowrate*c) + generation - V*lambda*c
            list_of_eq = {}
            # initialise all equations to 0
            for box in self.boxes:
                list_of_eq[box.name] = 0

            # build
            for i, box in enumerate(self.boxes):
                # build internal equation (derivative, sources, decay...)
                list_of_eq[box.name] += box.internal_equation(box_conc_map, self.dt)

                # for each output add inputs and outputs accordingly
                box_concentration = p[i]
                for name, flowrate in zip(box.outputs.keys(), box.outputs.values()):
                    list_of_eq[box.name] += -flowrate*box_concentration
                    list_of_eq[name] += flowrate*box_concentration
            return [val for val in list_of_eq.values()]
        return equations

    def advance(self):
        initial_guess = [box.old_concentration for box in self.boxes]
        concentrations = fsolve(self.equations, initial_guess)
        for box, new_concentration in zip(self.boxes, concentrations):
            box.concentration = new_concentration
            box.old_concentration = new_concentration
            box.concentrations.append(new_concentration)
            box.update()
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

    def update(self):
        return

    def internal_equation(self, box_conc_map, stepsize):
        """Builds the equation for the box excluding links with other boxes

        Args:
            box_conc_map (dict): a map linking boxes names to their
                concentrations
            stepsize (float): the stepsize

        Returns:
            float: the value of internal equation of the box
        """
        equation = 0
        # V*(c- c_n)/dt
        equation += -self.volume*(box_conc_map[self.name] - self.old_concentration)/stepsize
        # + V*generation
        equation += self.volume*self.generation_term
        # - V*lambda*c
        equation += -self.volume*box_conc_map[self.name]*LAMBDA
        return equation
