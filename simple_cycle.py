import system_code as tsc
import matplotlib.pyplot as plt
import matplotx
import numpy as np

def run_system(trapping: bool):

    startup_inventory = 10
    storage_volume = 1
    storage = tsc.Box("Storage", {"Plasma": 0.45}, volume=storage_volume, initial_concentration=startup_inventory/storage_volume)

    n_dot = 1
    plasma = tsc.Box("Plasma", {"IFC": 3}, volume=1, generation_term=-n_dot, initial_concentration=1)

    TBR = 1.2
    ofc = tsc.Box("OFC", {"IFC": 1}, volume=1, generation_term=n_dot*TBR)
    ifc = tsc.Box("IFC", outputs={"Storage": 1}, volume=1, initial_concentration=0)

    if not trapping:
        my_system = tsc.System([storage, plasma, ifc, ofc])

        my_system.run(20)

    else:
        # system with trapping in OFC

        ofc_t = tsc.Box("OFC_T", {"OFC": 1}, volume=1)
        ofc.outputs["OFC_T"] = 1
        my_system = tsc.System([storage, plasma, ifc, ofc, ofc_t])

        while my_system.current_time < 20:

            k = 1
            p = 0.1
            n = 5

            # TODO be careful with conservation of mass and all
            gamma_ofc_to_ofct = ofc_t.volume*k*(n-ofc_t.concentration)
            gamma_ofct_to_ofc = ofc_t.volume*p*ofc_t.concentration
            ofc_t.outputs["OFC"] = gamma_ofct_to_ofc
            ofc.outputs["OFC_T"] = gamma_ofc_to_ofct

            my_system.advance()
    
    return my_system

for trapping in [True, False]:
    my_system = run_system(trapping)

    # plot
    if trapping:
        plt.title("Including trapping in OFC")
    else:
        plt.title("No trapping")

    for box in my_system.boxes:
        plt.plot(my_system.t, np.array(box.concentrations)*box.volume, label=box.name)
    matplotx.line_labels()
    plt.xlabel("Time")
    plt.ylabel("Inventories")
    plt.tight_layout()
    plt.show()