import numpy as np
import system_code as tsc
import pytest


def test_constant_inventory():
    """Builds a closed system with an inventory of 2 and checks this inventory
    doesn't vary
    """
    # build
    A = tsc.Box("A", {"B": 1}, volume=1, initial_concentration=2)
    B = tsc.Box("B", {"C": 1}, volume=1)
    C = tsc.Box("C", {"A": 1}, volume=1)
    system = tsc.System([A, B, C])

    # run
    system.run(20)

    # test
    inventory = np.zeros(len(system.t))
    for box in system.boxes:
        inventory += box.volume * np.array(box.concentrations)

    assert np.allclose(inventory, 2)


def test_mass_conservation_system():
    """Checks the inventory is conserved with generation
    """
    # build
    generation_source = 1
    conc_init_A = 2
    vol_A, vol_B, vol_C = 2, 3, 4

    A = tsc.Box("A", {"B": 1}, volume=vol_A, initial_concentration=conc_init_A)
    B = tsc.Box("B", {"C": 1}, volume=vol_B, generation_term=generation_source)
    C = tsc.Box("C", {"A": 1}, volume=vol_C, generation_term=generation_source)
    system = tsc.System([A, B, C])

    # run
    system.run(20)

    # test
    inventory = np.zeros(len(system.t))
    for box in system.boxes:
        inventory += box.volume * np.array(box.concentrations)

    assert np.allclose(
        inventory,
        vol_A*conc_init_A + (vol_B+vol_C)*generation_source*np.array(system.t)
        )


def test_mass_conservation_box():
    """Checks that the computed concentration matches with the analytical
    solution
    """
    # build
    F_AB = 2
    A = tsc.Box("A", {"B": F_AB}, volume=1, initial_concentration=2)
    B = tsc.Box("B", {"C": 1}, volume=1, generation_term=0)
    C = tsc.Box("C", {"A": 0}, volume=1, generation_term=0)
    system = tsc.System([A, B, C], dt=0.01)

    # run
    system.run(20)

    # test
    concentration_A = np.array(A.concentrations)
    expected = A.concentrations[0] * \
        np.exp((tsc.LAMBDA-F_AB/A.volume)*np.array(system.t))

    # TODO: try to replicate this with pure scipy, this is weird
    assert np.allclose(concentration_A, expected, rtol=0.07, atol=1e-5)


def test_decay():
    """Checks that concentration of a box decays with time
    """
    A = tsc.Box("A", {}, volume=2, initial_concentration=3)
    half_life = np.log(2)/tsc.LAMBDA
    system = tsc.System([A], dt=half_life/30)

    system.run(half_life)

    assert A.concentrations[-1] == \
        pytest.approx(A.concentrations[0]/2, rel=0.05)
