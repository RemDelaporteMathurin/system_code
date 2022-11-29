import system_code as tsc
import numpy as np
import sympy as sp


def test_one_box_only():
    """Makes a simple 'cycle' with 1 box with a trap and checks mass is conserved"""

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


def test_equation():
    """Checks that the produced equation is the correct one"""
    I_m = sp.Symbol("I_m")
    I_m_n = sp.Symbol("I_m_n")
    I_t = sp.Symbol("I_t")
    I_t_n = sp.Symbol("I_t_n")
    dt = sp.Symbol("dt")
    V_t = sp.Symbol("V_t")
    K = sp.Symbol("K")
    k = sp.Symbol("k")
    n = sp.Symbol("n")
    p = sp.Symbol("p")

    A = tsc.Box("A", initial_inventory=I_m_n)

    A_trap = tsc.Trap(
        k=k,
        p=p,
        n=n,
        volume=V_t,
        name="A_trap",
        initial_inventory=I_t_n,
        solid_fraction=K,
    )

    A.add_trap(A_trap)

    # run
    A_trap.build_equation({A: I_m, A_trap: I_t}, stepsize=dt)

    # test
    c_m = I_m * K / V_t  # kg/m3
    c_m = c_m / tsc.MOLAR_MASS  # at/m3
    c_t = I_t / V_t  # kg/m3
    c_t = c_t / tsc.MOLAR_MASS  # at/m3

    expected_equation = (
        -(I_t - I_t_n) / dt + V_t * (k * c_m * (n - c_t) - p * c_t) - tsc.LAMBDA * I_t
    )
    print(expected_equation)
    print(A_trap.equation)
    assert sp.simplify(A_trap.equation - expected_equation) == 0
