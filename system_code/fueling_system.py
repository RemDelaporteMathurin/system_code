from system_code import Box
import pint


class StorageAndDeliverySystem(Box):
    def __init__(
        self,
        name: str,
        output_name: dict,
        volume: float,
        fueling_rate: float,
        initial_concentration: float,
    ):
        self.fueling_rate = pint.Quantity(fueling_rate, "particle per second")
        self.initial_concentration = pint.Quantity(
            initial_concentration, "particle per meter**3"
        )
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
        """A customized box class storing tritium and deliverying tritium to
        other boxes (e.g plasma box) 

        Args:
            name: the stepsize
            output_name: the box name to output to
            volume: the volume of the box in units of meters**3
            fueling_rate: the rate of delivery out of the box to the output box
                in units of particle per second
            initial_concentration: the initial / starting concentration of
                tritium in units of particles per m3
        """

    def update(self):
        """Updates the flowing rate to ensure a fixed fueling rate"""
        self.outputs[self.output_name] = self.fueling_rate / self.concentration
