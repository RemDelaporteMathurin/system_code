import matplotlib.pyplot as plt
import numpy as np
import pint
from scipy.optimize import fsolve

from system_code import LAMBDA


class System:
    def __init__(self, boxes: list, dt: float=0.2):
        self.boxes = boxes
        self.dt = pint.Quantity(dt, "seconds")
        self.equations = self.build_equations()
        self.current_time = pint.Quantity(0, "seconds")
        self.t = [self.current_time]
        """A container class for combining boxes into a system

        Args:
            boxes: a list of system_code.Box class instances to combine into a
                linked system
            dt: the time step to use when iterating through the equations. A
                smaller time step will be more accurate but take longer to
                solve. dt should be input in units of seconds
        """

    def build_equations(self):
        def equations(p):
            # fsolve can't accept func or x0 with units hence self.equations does not include units and .magnitude has been used
            # map the concentrations to the boxes
            box_conc_map = {}
            for i, box in enumerate(self.boxes):
                box_conc_map[box.name] = p[i]

            # V*(c- c_n)/dt = sum( flow_rate * c_inputs) - sum(flowrate*c) + generation - V*lambda*c
            list_of_eq = {}
            # if this is initialise then units need adding to this 0 value?
            # initialise all equations to 0
            for box in self.boxes:
                list_of_eq[box.name] = 0

            # build
            for i, box in enumerate(self.boxes):
                # build internal equation (derivative, sources, decay...)

                list_of_eq[box.name] = box.internal_equation(box_conc_map, self.dt)

                # for each output add inputs and outputs accordingly
                box_concentration = p[i]
                for name, flowrate in zip(box.outputs.keys(), box.outputs.values()):
                    flowrateQ = pint.Quantity(flowrate, "particles per second")
                    list_of_eq[box.name] += (
                        -flowrateQ.magnitude * box_concentration.magnitude
                    )
                    list_of_eq[name] += (
                        flowrateQ.magnitude * box_concentration.magnitude
                    )
            return [val for val in list_of_eq.values()]

        return equations

    def advance(self):
        # initial_guess = [box.old_concentration for box in self.boxes]
        initial_guess = [box.old_concentration.magnitude for box in self.boxes]
        # fsolve can't accept func or x0 with units hence initial_guess does not include units and .magnitude has been used

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
        durationQ = pint.Quantity(duration, "seconds")
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
            plt.plot(self.t, np.array(box.concentrations) * box.volume, label=box.name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Inventories")
        plt.show()
