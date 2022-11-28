from system_code import Box


class Plasma(Box):
    def __init__(
            self, name, plasma_burning_rate,
            initial_concentration=0, generation_term=0):
        super().__init__(
            name,
            initial_concentration, generation_term)
        self.plasma_burning_rate = plasma_burning_rate

    def build_equation(self, box_conc_map, stepsize):
        """V*(c- c_n)/dt = generation - V*lambda*c - V*burning_rate*c

        Args:
            box_conc_map (dict): a map linking boxes to their
                concentrations
            stepsize (float): the stepsize

        Returns:
            float: the value of internal equation of the box
        """
        super().build_equation(box_conc_map, stepsize)

        plasma_burning_rate = self.plasma_burning_rate
        self.equation += -plasma_burning_rate*box_conc_map[self]
