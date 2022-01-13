from system_code import Box
import pint


class Plasma(Box):
    def __init__(
        self,
        name,
        outputs,
        volume,
        plasma_burning_rate,
        initial_concentration=0,
        generation_term=0,
    ):
        super().__init__(name, outputs, volume, initial_concentration, generation_term)
        self.plasma_burning_rate = pint.Quantity(
            plasma_burning_rate, "particle per meter ** 3"
        )
        """A customized box class for burning (consumption / fusing / reacting) tritium

        Args:
            name: the stepsize
            outputs: a map linking boxes names to their concentrations (in units of particle per meter ** 3)
            volume: the volume of the box in units of meters**3
            plasma_burning_rate: the rate of tritium burning within the box in
                units of particle per meter ** 3
            fueling_rate: the rate of delivery out of the box to the output box
                in units of particle per second
            initial_concentration: the initial / starting concentration of
                tritium in units of particles per m3
            generation_term: the rate of tritium production on the box in units
                of particles per second
        """

    def internal_equation(self, box_conc_map, stepsize):
        """V*(c- c_n)/dt = generation - V*lambda*c - V*burning_rate*c

        Args:
            box_conc_map (dict): a map linking boxes names to their
                concentrations
            stepsize (float): the stepsize

        Returns:
            float: the value of internal equation of the box
        """
        equation = super().internal_equation(box_conc_map, stepsize)

        plasma_burning_rate = self.plasma_burning_rate
        equation += -plasma_burning_rate * box_conc_map[self.name] * self.volume
        return equation
