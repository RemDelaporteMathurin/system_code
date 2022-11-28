import system_code as tsc
import sympy as sp


def test_plasma_equation():
    """Checks that the correct internal equation is created for the plasma box
    """

    # build
    I = sp.Symbol("I")
    I_n = sp.Symbol("I_n")
    dt = sp.Symbol("dt")
    burning_rate = sp.Symbol("br")
    gamma = sp.Symbol("gamma")

    # run
    my_plasma = tsc.Plasma("plasma", burning_rate, initial_inventory=I_n, generation_term=gamma)

    my_plasma.build_equation({my_plasma: I}, stepsize=dt)

    expected_equation = -(I-I_n)/dt + gamma - tsc.LAMBDA*I - burning_rate*I

    # test
    assert sp.simplify(my_plasma.equation-expected_equation) == 0
