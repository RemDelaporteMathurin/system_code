from system_code import LAMBDA


class Box:
    def __init__(self, name, initial_inventory=0, generation_term=0):
        self.name = name
        self.initial_inventory = initial_inventory

        self.inventory = self.initial_inventory
        self.old_inventory = self.initial_inventory
        self.inventories = [self.inventory]
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
            flowrate (float): the flow rate in #/s
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

    def build_equation(self, box_inv_map, stepsize):
        """Builds the equation for the box excluding links with other boxes

        Args:
            box_inv_map (dict): a map linking boxes to their
                inventories
            stepsize (float): the stepsize

        Returns:
            float: the value of internal equation of the box
        """
        # (I - I_n)/dt = sum( flow_rate * I_inputs) - sum(flowrate*I) + generation - lambda*I

        self.equation = 0
        # (I - I_n)/dt
        self.equation += (
            -(box_inv_map[self] - self.old_inventory) / stepsize
        )
        # + generation
        self.equation += self.generation_term
        # - lambda*I
        self.equation += -box_inv_map[self] * LAMBDA

        # outputs
        for box, flowrate in self.outputs.items():
            if isinstance(box, Trap):
                continue
            self.equation += -flowrate * box_inv_map[self]

        for box, flow in self.constant_outputs.items():
            self.equation += -flow

        # inputs
        for box, flowrate in self.inputs.items():
            if isinstance(box, Trap):
                continue
            self.equation += flowrate * box_inv_map[box]

        for box, flow in self.constant_inputs.items():
            self.equation += flow

        # - V_t * k * c * (n - c_t) + V_t * p * c_t
        for trap in self.traps:
            self.equation += (
                -trap.volume
                * trap.k
                * box_inv_map[self]
                * (trap.n - box_inv_map[trap])
            )
            self.equation += trap.volume * trap.p * box_inv_map[trap]

    def reset(self):
        self.inventory = self.initial_inventory
        self.old_inventory = self.initial_inventory
        self.inventories = [self.inventory]
        # TODO what about generation term?


class Trap(Box):
    def __init__(self, k, p, n, name, volume, initial_inventory=0):
        super().__init__(name, initial_inventory)
        self.k = k
        self.p = p
        self.n = n
        self.volume = volume
        self.parent_box = None

    def build_equation(self, box_inv_map, stepsize):
        super().build_equation(box_inv_map, stepsize)

        # + V * k * c * (n - c_t) - V * p * c_t
        self.equation += (
            self.volume
            * self.k
            * box_inv_map[self.parent_box]
            * (self.n - box_inv_map[self])
        )
        self.equation += -self.volume * self.p * box_inv_map[self]
