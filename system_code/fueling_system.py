from system_code import Box
from typing import Tuple
import pint

class StorageAndDeliverySystem(Box):
    def __init__(
        self,
        name: str,
        output_name: dict,
        volume: Tuple[float, str],
        fueling_rate: Tuple[float, str],
        initial_concentration: Tuple[float, str],
    ):
        self.fueling_rate = pint.Quantity(fueling_rate[0], fueling_rate[1])
        self.initial_concentration = pint.Quantity(initial_concentration[0], initial_concentration[1])
        self.flowrate = self.fueling_rate / self.initial_concentration
        self.output_name = output_name
        outputs = {output_name: self.flowrate}
        super().__init__(
            name,
            outputs,
            volume,
            initial_concentration=initial_concentration,
            generation_term=0,
        )

    def update(self):
        """Updates the flowing rate to ensure a fixed fueling rate"""
        self.outputs[self.output_name] = self.fueling_rate / self.concentration
