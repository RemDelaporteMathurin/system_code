from system_code import LAMBDA


class Box:
    def __init__(self, name, volume, initial_concentration=0, generation_term=0):
        self.name = name
        self.volume = volume
        self.initial_concentration = initial_concentration

        self.concentration = self.initial_concentration
        self.old_concentration = self.initial_concentration
        self.concentrations = [self.concentration]
        self.generation_term = generation_term

        self.equation = 0
        self.inputs = {}
        self.outputs = {}

    def add_output(self, box, flowrate):
        """Adds a link from this component to another.
        This add the target box to this self.outputs and
        this component to box.inputs

        Args:
            box (Box): the target box
            flowrate (float): the flow rate in m3/s
        """
        if box in self.outputs or self in box.inputs:
            raise ValueError("Link already exists")

        self.outputs[box] = flowrate
        box.inputs[self] = flowrate

    def update(self):
        return

    def build_equation(self, box_conc_map, stepsize):
        """Builds the equation for the box excluding links with other boxes

        Args:
            box_conc_map (dict): a map linking boxes to their
                concentrations
            stepsize (float): the stepsize

        Returns:
            float: the value of internal equation of the box
        """
        # V*(c- c_n)/dt = sum( flow_rate * c_inputs) - sum(flowrate*c) + generation - V*lambda*c

        self.equation = 0
        # V*(c- c_n)/dt
        self.equation += -self.volume*(box_conc_map[self] - self.old_concentration)/stepsize
        # + V*generation
        self.equation += self.volume*self.generation_term
        # - V*lambda*c
        self.equation += -self.volume*box_conc_map[self]*LAMBDA

        # outputs
        for flowrate in self.outputs.values():
            self.equation += -flowrate*box_conc_map[self]

        # inputs
        for box, flowrate in self.inputs.items():
            self.equation += flowrate*box_conc_map[box]

    def reset(self):
        self.concentration = self.initial_concentration
        self.old_concentration = self.initial_concentration
        self.concentrations = [self.concentration]
        # TODO what about generation term?
