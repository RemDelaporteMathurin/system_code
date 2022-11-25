import system_code as tsc

n_dot = 8.99e-7  # kg T burned / s
TBR = 1.3
TBE = 0.005

# OFC
plasma = tsc.Box("plasma", volume=1, generation_term=-n_dot)
blanket = tsc.Box("blanket", volume=1, generation_term=n_dot * TBR)
first_wall = tsc.Box("first wall", volume=1)
divertor = tsc.Box("divertor", volume=1)
t_extraction_system = tsc.Box("TES", volume=1)
heat_exchanger = tsc.Box("HX", volume=1)

# IFC
fueling_system = tsc.Box("fueling system", volume=1)
storage_and_management = tsc.Box("storage and management", volume=1)
isotope_seperation_system = tsc.Box("ISS", volume=1)
vacuum_pump = tsc.Box("vacuum pump", volume=1)
fuel_cleanup = tsc.Box("fuel cleanup", volume=1)
detritiation_system = tsc.Box("detritiation system", volume=1)

# links

plasma.add_output(first_wall, flowrate=1)
plasma.add_output(divertor, flowrate=1)
plasma.add_output(vacuum_pump, flowrate=1)

tau_bz = 3600  # s
blanket.add_output(t_extraction_system, flowrate=1)
blanket.add_output(first_wall, flowrate=1)
blanket.add_output(divertor, flowrate=1)

tau_fw = 1000  # s
first_wall.add_output(blanket, flowrate=1)

tau_div = 1000  # s
divertor.add_output(blanket, flowrate=1)

tau_tes = 24 * 3600  # s
t_extraction_system.add_output(heat_exchanger, flowrate=1)
t_extraction_system.add_output(isotope_seperation_system, flowrate=1)

tau_hx = 1000  # s
heat_exchanger.add_output(blanket, flowrate=1)

tau_iss = 3.7 * 3600  # s
isotope_seperation_system.add_output(storage_and_management, flowrate=1)
isotope_seperation_system.add_output(detritiation_system, flowrate=1)

tau_det = 1 * 3600  # s
detritiation_system.add_output(isotope_seperation_system, flowrate=1)

tau_vp = 600  # s
vacuum_pump.add_output(fuel_cleanup, flowrate=1)
vacuum_pump.add_output(storage_and_management, flowrate=1)  # DIR

tau_fc = 0.3 * 3600  # s
fuel_cleanup.add_output(isotope_seperation_system, flowrate=1)

fueling_system.add_output(plasma, flowrate=1)

storage_and_management.add_output(fueling_system, flowrate=1)

# system

system = tsc.System(
    [
        plasma,
        blanket,
        divertor,
        first_wall,
        t_extraction_system,
        heat_exchanger,
        isotope_seperation_system,
        detritiation_system,
        vacuum_pump,
        fuel_cleanup,
        fueling_system,
        storage_and_management,
    ]
)
