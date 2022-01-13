from system_code import LAMBDA, ureg
from typing import Tuple
import pint
class Box:
    def __init__(
        self,
        name: str,
        outputs: dict,
        volume: float,
        initial_concentration: float = 0,
        generation_term: float = 0,
        # generation_term: Tuple[float, str] = (0, 'particle per second'),
    ):
        self.outputs = outputs
        self.name = name
        self.inputs = []
        self.volume = pint.Quantity(volume, 'meter**3')
        self.concentration = pint.Quantity(initial_concentration, 'particle per meter**3')
        self.old_concentration = pint.Quantity(initial_concentration, 'particle per meter**3')
        self.concentrations = [self.concentration]
        self.generation_term = pint.Quantity(generation_term, 'particle per second')
    """

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

        concentration = pint.Quantity(box_conc_map[self.name], 'particles meter ** -3')

        print('volume units=', self.volume.units)
        print('concentration units=', concentration.units)
        print('old_concentration units=', self.old_concentration.units)
        print('stepsize units=', stepsize.units)

        # V*(c- c_n)/dt
        equation1 = (
            -self.volume * (concentration - self.old_concentration) / stepsize
        )

        # + V*generation
        equation2 = self.volume * self.generation_term

        # - V*lambda*c
        equation3 = -self.volume * concentration * LAMBDA
        print('\nequations')
        print('equation units', equation1.units)
        print('equation units', equation2.units)
        print('equation units', equation3.units)

        input()
        # fails with
        # Cannot convert from 'particle / second' ([substance] / [time]) to 'meter ** 3 * particle / second' ([length] ** 3 * [substance] / [time])

        all_equations = equation1 + equation2 + equation3


        return all_equations
