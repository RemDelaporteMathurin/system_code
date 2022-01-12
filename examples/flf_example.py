import system_code as tsc

# all volumes are set to 1 which means initial_contraction is equivalent to amount

plasma = tsc.Plasma(
    name="Plasma",
    outputs ={"Storage": 1},
    volume=(1, 'meter **3'),
    plasma_burning_rate=1,
    initial_concentration=(0, 'meter **-3')
)


breeder = tsc.Box(
    name="Breeder",
    outputs ={"Storage": 1},
    volume=(1, 'meter **3'),
    generation_term=1.05,
    initial_concentration=(0, 'meter **-3')
)


storage = tsc.StorageAndDeliverySystem(
    name="Storage",
    output_name ="Plasma",
    volume=(1, 'meter **3'),
    fueling_rate=(1, 'second ** -1'),
    initial_concentration=(5, 'meter **-3')
)


my_system = tsc.System([storage, plasma, breeder])
my_system.run((20, 'seconds'))

my_system.plot_inventories()
