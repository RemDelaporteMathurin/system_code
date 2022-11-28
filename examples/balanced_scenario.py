import system_code as tsc

storage = tsc.Box("Storage", initial_inventory=1)
plasma = tsc.Box("Plasma", generation_term=-1, initial_inventory=1)
breeder = tsc.Box("Breeder", generation_term=1.05)

breeder.add_output(storage, 1)
storage.add_output(plasma, 0.45)

my_system = tsc.System([storage, plasma, breeder])
# my_system.run(20)
while my_system.current_time < 20:
    my_system.advance()

    # Example of conditional flowrate
    # if breeder.concentration*breeder.outputs["Storage"] > storage.concentration*storage.outputs["Plasma"]:
    #     storage.outputs["Out"] = (breeder.concentration*breeder.outputs["Storage"] - injection_rate)/storage.concentration

    # Modify flowrate according to injection rate
    injection_rate = 1
    storage.outputs[plasma] = injection_rate/storage.inventory
my_system.plot_inventories()
