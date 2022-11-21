from system_code import LAMBDA


class Box:
    def __init__(self, name, outputs, volume, initial_concentration=0, generation_term=0):
        self.outputs = outputs
        self.name = name
        self.volume = volume
        self.initial_concentration = initial_concentration

        self.concentration = self.initial_concentration
        self.old_concentration = self.initial_concentration
        self.concentrations = [self.concentration]
        self.generation_term = generation_term

        self.equation = 0

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
        self.equation = 0
        # V*(c- c_n)/dt
        self.equation += -self.volume*(box_conc_map[self.name] - self.old_concentration)/stepsize
        # + V*generation
        self.equation += self.volume*self.generation_term
        # - V*lambda*c
        self.equation += -self.volume*box_conc_map[self.name]*LAMBDA

    def reset(self):
        self.concentration = self.initial_concentration
        self.old_concentration = self.initial_concentration
        self.concentrations = [self.concentration]
        # TODO what about generation term?
