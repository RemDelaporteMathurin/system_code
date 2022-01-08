from system_code import LAMBDA


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
        # + generation
        equation += self.volume*self.generation_term
        # - V*lambda*c
        equation += -self.volume*box_conc_map[self.name]*LAMBDA
        return equation
