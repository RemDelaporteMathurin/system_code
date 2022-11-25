import system_code as tsc
import sympy as sp


def test_add_constant_output():
    c1 = sp.Symbol("c1")
    c2 = sp.Symbol("c2")
    dt = sp.Symbol("dt")
    V1 = sp.Symbol("V1")
    V2 = sp.Symbol("V2")
    flow = sp.Symbol("flow")

    box1 = tsc.Box("box1", volume=V1)
    box2 = tsc.Box("box2", volume=V2)

    box1.add_constant_output(box2, flow=flow)

    box1.build_equation({box1: c1, box2: c2}, stepsize=dt)
    box2.build_equation({box1: c1, box2: c2}, stepsize=dt)

    expected_equation_1 = -V1 * (c1 - 0) / dt - V1 * tsc.LAMBDA * c1 - flow
    expected_equation_2 = -V2 * (c2 - 0) / dt - V2 * tsc.LAMBDA * c2 + flow

    # test
    assert sp.simplify(box1.equation - expected_equation_1) == 0
    assert sp.simplify(box2.equation - expected_equation_2) == 0
