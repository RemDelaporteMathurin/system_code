import system_code as tsc

# all volumes are set to 1 which means initial_contraction is equivalent to amount

plasma = tsc.Plasma(
    name="Plasma",
    outputs={"Storage": 1},
    volume=1,
    plasma_burning_rate=1,
    initial_concentration=0,
)


breeder = tsc.Box(
    name="Breeder",
    outputs={"Storage": 1},
    volume=1,
    generation_term=1.05,
    initial_concentration=0,
)


storage = tsc.StorageAndDeliverySystem(
    name="Storage",
    output_name="Plasma",
    volume=1,
    fueling_rate=1,
    initial_concentration=5,
)


my_system = tsc.System([storage, plasma, breeder])
my_system.run(20)

my_system.plot_inventories()
