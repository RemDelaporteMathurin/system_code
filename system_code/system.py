import matplotlib.pyplot as plt
import numpy as np
import pint
from scipy.optimize import fsolve

from system_code import LAMBDA


class System:
    def __init__(self, boxes, dt=(0.2, 'seconds')):
        self.boxes = boxes
        self.dt = pint.Quantity(dt[0], dt[1])
        self.equations = self.build_equations()
        self.current_time = pint.Quantity(0, 'seconds')
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
                print(box_conc_map)

                list_of_eq[box.name] += box.internal_equation(box_conc_map, self.dt)

                # for each output add inputs and outputs accordingly
                box_concentration = p[i]
                for name, flowrate in zip(box.outputs.keys(), box.outputs.values()):
                    flowrateQ = pint.Quantity(flowrate[0], flowrate[1])
                    # list_of_eq[box.name] += -flowrateQ.magnitude*box_concentration.magnitude
                    # list_of_eq[name] += flowrateQ.magnitude*box_concentration.magnitude
                    list_of_eq[box.name] += -flowrateQ*box_concentration.magnitude
                    list_of_eq[name] += flowrateQ*box_concentration.magnitude
                    # print(flowrateQ.magnitude*box_concentration.magnitude)
            return [val for val in list_of_eq.values()]
        return equations

    def advance(self):
        # initial_guess = [box.old_concentration for box in self.boxes]
        initial_guess = [box.old_concentration.magnitude for box in self.boxes]
        print(initial_guess)
        print(self.equations)
        # fsolve can't accept func or x0 with units
        concentrations = fsolve(self.equations, initial_guess)
        print('concentrations', concentrations)
        input()
        print()
        for box, new_concentration in zip(self.boxes, concentrations):
            box.concentration = new_concentration
            box.old_concentration = new_concentration
            box.concentrations.append(new_concentration)
            box.update()
        self.current_time += self.dt
        self.t.append(self.current_time)
        self.equations = self.build_equations()

    def run(self, duration):
        durationQ = pint.Quantity(duration[0], duration[1])
        start_time = self.current_time
        while self.current_time - start_time < durationQ:
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
