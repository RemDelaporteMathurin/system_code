from typing import Dict

import pint

from system_code import LAMBDA


class Box:
    def __init__(
        self,
        name: str,
        outputs: Dict[str, float],
        volume: float,
        initial_concentration: float = 0,
        generation_term: float = 0,
    ):
        self.name = name
        self.outputs = outputs
        self.volume = pint.Quantity(volume, "meter**3")
        self.inputs = []
        self.concentration = pint.Quantity(
            initial_concentration, "particle per meter**3"
        )
        self.old_concentration = pint.Quantity(
            initial_concentration, "particle per meter**3"
        )
        self.concentrations = [self.concentration]
        self.generation_term = pint.Quantity(generation_term, "particle / meter ** 3 / second")
        """A generic box class for adaptation into more specialized classes 

        Args:
            name: the stepsize
            outputs: a map linking boxes names to their concentrations
            volume: the volume of the box in units of meters**3
            initial_concentration: the initial / starting concentration of
                tritium in units of particles per m3
            generation_term: the rate of tritium generation within the box in
                units of particle per meter**3
        """

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

        concentration = pint.Quantity(box_conc_map[self.name], "particles meter ** -3")

        print("volume units=", self.volume.units)
        print("concentration units=", concentration.units)
        print("old_concentration units=", self.old_concentration.units)
        print("stepsize units=", stepsize.units)

        # V*(c- c_n)/dt
        equation1 = -self.volume * (concentration - self.old_concentration) / stepsize

        # + V*generation
        equation2 = self.volume * self.generation_term

        # - V*lambda*c
        equation3 = -self.volume * concentration * LAMBDA
        print("\nequations")
        print("equation units", equation1.units)
        print("equation units", equation2.units)
        print("equation units", equation3.units, "\n")

        # fails with
        # Cannot convert from 'particle / second' ([substance] / [time]) to 'meter ** 3 * particle / second' ([length] ** 3 * [substance] / [time])

        all_equations = equation1 + equation2 + equation3

        return all_equations
