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
        self.constant_inputs = {}
        self.outputs = {}
        self.constant_outputs = {}
        self.traps = []

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

    def add_constant_output(self, box, flow):
        """Adds a constant flow from this component to another.

        Args:
            box (Box): the target box
            flow (float): the flow in /s
        """
        self.constant_outputs[box] = flow
        box.constant_inputs[self] = flow

    def add_trap(self, trap):
        """Add a trap to the component

        Args:
            trap (Trap): the trap object
        """
        self.traps.append(trap)
        trap.parent_box = self
        self.add_output(trap, 0)  # TODO: needed?

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
        self.equation += (
            -self.volume * (box_conc_map[self] - self.old_concentration) / stepsize
        )
        # + V*generation
        self.equation += self.volume * self.generation_term
        # - V*lambda*c
        self.equation += -self.volume * box_conc_map[self] * LAMBDA

        # outputs
        for box, flowrate in self.outputs.items():
            if isinstance(box, Trap):
                continue
            self.equation += -flowrate * box_conc_map[self]

        for box, flow in self.constant_outputs.items():
            self.equation += -flow

        # inputs
        for box, flowrate in self.inputs.items():
            if isinstance(box, Trap):
                continue
            self.equation += flowrate * box_conc_map[box]

        for box, flow in self.constant_inputs.items():
            self.equation += flow

        # - V * k * c * (n - c_t) + V * p * c_t
        for trap in self.traps:
            self.equation += (
                -trap.volume
                * trap.k
                * box_conc_map[self]
                * (trap.n - box_conc_map[trap])
            )
            self.equation += trap.volume * trap.p * box_conc_map[trap]

    def reset(self):
        self.concentration = self.initial_concentration
        self.old_concentration = self.initial_concentration
        self.concentrations = [self.concentration]
        # TODO what about generation term?


class Trap(Box):
    def __init__(self, k, p, n, name, volume, initial_concentration=0):
        super().__init__(name, volume, initial_concentration)
        self.k = k
        self.p = p
        self.n = n
        self.parent_box = None

    def build_equation(self, box_conc_map, stepsize):
        super().build_equation(box_conc_map, stepsize)

        # + V * k * c * (n - c_t) - V * p * c_t
        self.equation += (
            self.volume
            * self.k
            * box_conc_map[self.parent_box]
            * (self.n - box_conc_map[self])
        )
        self.equation += -self.volume * self.p * box_conc_map[self]
