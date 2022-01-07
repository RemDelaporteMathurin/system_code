from system_code import Box


class StorageAndDeliverySystem(Box):
    def __init__(self, name, output_name, volume, fueling_rate, initial_concentration):
        self.fueling_rate = fueling_rate
        self.flowrate = fueling_rate/initial_concentration
        self.output_name = output_name
        outputs = {output_name: self.flowrate}
        super().__init__(name, outputs, volume, initial_concentration=initial_concentration, generation_term=0)

    def update(self):
        """Updates the flowing rate to ensure a fixed fueling rate
        """
        self.outputs[self.output_name] = self.fueling_rate/self.concentration
