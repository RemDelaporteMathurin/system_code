from system_code import LAMBDA, ureg
from typing import Tuple
import pint
class Box:
    def __init__(
        self,
        name: str,
        outputs: dict,
        volume: Tuple[float, str],
        initial_concentration: Tuple[float, str] =  (0, 'particle per meter**3'),
        generation_term: float = 0,
        # generation_term: Tuple[float, str] = (0, 'particle per second'),
    ):
        self.outputs = outputs
        self.name = name
        self.inputs = []
        self.volume = pint.Quantity(volume[0], volume[1])
        self.concentration = pint.Quantity(initial_concentration[0], initial_concentration[1])
        self.old_concentration = pint.Quantity(initial_concentration[0], initial_concentration[1])
        self.concentrations = [self.concentration]
        self.generation_term = generation_term
        # self.generation_term = pint.Quantity(generation_term[0], generation_term[1])

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
        # equation = pint.Quantity(0, 'meter ** -3')
        # V*(c- c_n)/dt
        print(self.old_concentration)
        equation1 = (
            -self.volume * (pint.Quantity(box_conc_map[self.name], 'meter ** -3') - self.old_concentration) / stepsize
        )
        # + V*generation
        equation2 = self.volume * pint.Quantity(self.generation_term, 'second**-1')
        # - V*lambda*c
        equation3 = -self.volume * pint.Quantity(box_conc_map[self.name], 'meter ** -3') * LAMBDA
        print('\nequations')
        print(equation1)
        print(equation2)
        print(equation3)
        all_equations = equation1 + equation2 + equation3
        return all_equations
