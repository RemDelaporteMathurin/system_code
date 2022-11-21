from system_code import Box


class StorageAndDeliverySystem(Box):
    def __init__(self, name, output, volume, fueling_rate, initial_concentration):
        self.fueling_rate = fueling_rate
        self.flowrate = fueling_rate/initial_concentration
        self.output = output
        super().__init__(name, volume, initial_concentration=initial_concentration, generation_term=0)
        self.outputs[output] = self.flowrate

    def update(self):
        """Updates the flowing rate to ensure a fixed fueling rate
        """
        self.outputs[self.output] = self.fueling_rate/self.concentration
