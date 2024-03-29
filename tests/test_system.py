import numpy as np
import system_code as tsc
import pytest


def test_constant_inventory():
    """Builds a closed system with an inventory of 2 and checks this inventory
    doesn't vary
    """
    # build
    A = tsc.Box("A", initial_inventory=2)
    B = tsc.Box("B")
    C = tsc.Box("C")

    A.add_output(B, 1)
    B.add_output(C, 1)
    C.add_output(A, 1)

    system = tsc.System([A, B, C])

    # run
    system.run(20)

    # test
    inventory = np.zeros(len(system.t))
    for box in system.boxes:
        inventory += np.array(box.inventories)

    assert np.allclose(inventory, 2)


def test_mass_conservation_system():
    """Checks the inventory is conserved with generation
    """
    # build
    generation_source = 1
    conc_init_A = 2

    A = tsc.Box("A", initial_inventory=conc_init_A)
    B = tsc.Box("B", generation_term=generation_source)
    C = tsc.Box("C", generation_term=generation_source)

    A.add_output(B, 1)
    B.add_output(C, 1)
    C.add_output(A, 1)

    system = tsc.System([A, B, C])

    # run
    system.run(20)

    # test
    inventory = np.zeros(len(system.t))
    for box in system.boxes:
        inventory += np.array(box.inventories)

    assert np.allclose(
        inventory,
        conc_init_A + 2*generation_source*np.array(system.t)
        )


def test_mass_conservation_box():
    """Checks that the computed concentration matches with the analytical
    solution
    """
    # build
    F_AB = 2
    A = tsc.Box("A", initial_inventory=2)
    B = tsc.Box("B", generation_term=0)
    C = tsc.Box("C", generation_term=0)

    A.add_output(B, F_AB)
    B.add_output(C, 1)
    C.add_output(A, 0)

    system = tsc.System([A, B, C], dt=0.01)

    # run
    system.run(20)

    # test
    concentration_A = np.array(A.inventories)
    expected = A.inventories[0] * \
        np.exp((tsc.LAMBDA-F_AB)*np.array(system.t))

    # TODO: try to replicate this with pure scipy, this is weird
    assert np.allclose(concentration_A, expected, rtol=0.07, atol=1e-5)


def test_decay():
    """Checks that concentration of a box decays with time
    """
    A = tsc.Box("A", initial_inventory=3)
    half_life = np.log(2)/tsc.LAMBDA
    system = tsc.System([A], dt=half_life/30)

    system.run(half_life)

    assert A.inventories[-1] == \
        pytest.approx(A.inventories[0]/2, rel=0.05)


def test_reset():
    """Checks that when reset, the attributes of the system are reset too
    """
    # build
    F_AB = 2
    A = tsc.Box("A", initial_inventory=2)
    B = tsc.Box("B", generation_term=0)
    C = tsc.Box("C", generation_term=0)

    A.add_output(B, F_AB)
    B.add_output(C, 1)
    C.add_output(A, 0)

    system = tsc.System([A, B, C], dt=0.01)

    system.run(2)
    old_eqs = system.equations
    # run

    system.reset()
    # test

    assert system.current_time == 0
    assert system.dt == system.initial_dt
    for box in system.boxes:
        assert len(box.inventories) == 1
    assert system.equations != old_eqs
