import system_code as tsc
import sympy as sp


def test_plasma_equation():
    """Checks that the correct internal equation is created for the plasma box
    """

    # build
    c = sp.Symbol("c")
    c_n = sp.Symbol("c_n")
    dt = sp.Symbol("dt")
    burning_rate = sp.Symbol("br")
    gamma = sp.Symbol("gamma")

    # run
    my_plasma = tsc.Plasma("plasma", burning_rate, initial_concentration=c_n, generation_term=gamma)

    my_plasma.build_equation({my_plasma: c}, stepsize=dt)

    expected_equation = -(c-c_n)/dt + gamma - tsc.LAMBDA*c - burning_rate*c

    # test
    assert sp.simplify(my_plasma.equation-expected_equation) == 0
