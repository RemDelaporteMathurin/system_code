import system_code as tsc


class Plasma(tsc.Box):
    def __init__(self, name, outputs, volume, initial_concentration=0, generation_term=0):
        super().__init__(name, outputs, volume, initial_concentration=initial_concentration, generation_term=generation_term)

    def internal_equation(self, box_conc_map, stepsize):
        equation = super().internal_equation(box_conc_map, stepsize)

        plasma_burning_rate = 10
        equation += -plasma_burning_rate*box_conc_map[self.name]*self.volume
        return equation


class Breeder(tsc.Box):
    def __init__(self, name, outputs, volume, initial_concentration=0):
        super().__init__(name, outputs, volume, initial_concentration=initial_concentration, generation_term=0)

    def internal_equation(self, box_conc_map, stepsize):
        equation = super().internal_equation(box_conc_map, stepsize)

        TBR = 1.1
        plasma_burning_rate = 10
        equation += TBR*plasma_burning_rate*box_conc_map["Plasma"]*self.volume
        return equation


storage = tsc.StorageAndDeliverySystem("Storage", "Plasma", volume=1, fueling_rate=2, initial_concentration=2.4)
plasma = Plasma("Plasma", {"Pumping": 1}, volume=1)
pumping = tsc.Box("Pumping", {"Storage": 1}, volume=1)
breeder = Breeder("Breeder", {"Storage": 2}, volume=1)

my_system = tsc.System([storage, plasma, breeder, pumping], dt=1)

my_system.run(50)
my_system.plot_inventories()
