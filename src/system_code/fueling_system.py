from system_code import Box


class StorageAndDeliverySystem(Box):
    def __init__(self, name, output, fueling_rate, initial_inventory):
        self.fueling_rate = fueling_rate
        self.flowrate = fueling_rate/initial_inventory
        self.output = output
        super().__init__(name, initial_inventory=initial_inventory, generation_term=0)
        self.outputs[output] = self.flowrate

    def update(self):
        """Updates the flowing rate to ensure a fixed fueling rate
        """
        self.outputs[self.output] = self.fueling_rate/self.inventory
