from system_code import Box


class Plasma(Box):
    def __init__(
            self, name, volume, plasma_burning_rate,
            initial_concentration=0, generation_term=0):
        super().__init__(
            name, volume,
            initial_concentration, generation_term)
        self.plasma_burning_rate = plasma_burning_rate

    def internal_equation(self, box_conc_map, stepsize):
        """V*(c- c_n)/dt = generation - V*lambda*c - V*burning_rate*c

        Args:
            box_conc_map (dict): a map linking boxes names to their
                concentrations
            stepsize (float): the stepsize

        Returns:
            float: the value of internal equation of the box
        """
        super().internal_equation(box_conc_map, stepsize)

        plasma_burning_rate = self.plasma_burning_rate
        self.equation += -plasma_burning_rate*box_conc_map[self]*self.volume
