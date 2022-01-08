import system_code as tsc
import sympy as sp


def test_plasma_equation():
    """Checks that the correct internal equation is created for the plasma box
    """

    # build
    c = sp.Symbol("c")
    c_n = sp.Symbol("c_n")
    dt = sp.Symbol("dt")
    V = sp.Symbol("V")
    burning_rate = sp.Symbol("br")
    gamma = sp.Symbol("gamma")

    # run
    my_plasma = tsc.Plasma("plasma", {}, V, burning_rate, initial_concentration=c_n, generation_term=gamma)

    equation = my_plasma.internal_equation({"plasma": c}, stepsize=dt)

    expected_equation = -V*(c-c_n)/dt + V*gamma - V*tsc.LAMBDA*c - V*burning_rate*c

    # test
    assert sp.simplify(equation-expected_equation) == 0
