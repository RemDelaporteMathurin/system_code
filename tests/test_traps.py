import system_code as tsc
import numpy as np

def test_one_box_only():
    """Makes a simple 'cycle' with 1 box with a trap and checks mass is conserved
    """

    A = tsc.Box("A", initial_inventory=1)

    A_trap = tsc.Trap(k=0.1, p=0.1, n=1, volume=2, name="A_trap")

    A.add_trap(A_trap)

    sys = tsc.System([A])

    sys.run(2)

    inv_A = np.array(A.inventories)
    inv_A_trapped = np.array(A_trap.inventories)
    total_inv = inv_A + inv_A_trapped
    print(inv_A)
    print(inv_A_trapped)
    print(total_inv)
    # TODO radioactive decay is on, careful
    assert np.isclose(total_inv, A.initial_inventory).all()
