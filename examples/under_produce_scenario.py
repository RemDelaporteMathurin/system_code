import system_code as tsc

storage = tsc.Box("Storage", initial_inventory=1)
plasma = tsc.Box("Plasma", generation_term=-1, initial_inventory=1)
breeder = tsc.Box("Breeder", generation_term=0.99)

breeder.add_output(storage, 1)
storage.add_constant_output(plasma, 1)

my_system = tsc.System([storage, plasma, breeder])
my_system.run(20)

my_system.plot_inventories()
