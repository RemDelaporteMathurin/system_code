import system_code as tsc

storage = tsc.Box("Storage", {"Plasma": 0.45}, volume=100, initial_concentration=1/100)
plasma = tsc.Box("Plasma", {}, volume=1, generation_term=-1, initial_concentration=1)
breeder = tsc.Box("Breeder", {"Storage": 1}, volume=1, generation_term=0.99)
out = tsc.Box("Out", outputs={}, volume=1, initial_concentration=0)
my_system = tsc.System([storage, plasma, breeder, out])
# my_system.run(20)
while my_system.current_time < 20:
    my_system.advance()

    injection_rate = 1
    storage.outputs["Plasma"] = injection_rate/storage.concentration

my_system.plot_inventories()
