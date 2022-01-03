from scipy.optimize import fsolve
import math


def equations(p):
    x, y = p
    return (x+y**2-4, math.exp(x) + x*y - 3)

x, y = fsolve(equations, (1, 1))

print(equations((x, y)))
print(x, y)


# V*dc/dt = sum( flow_rate * c_inputs) - sum(flowrate*c) + generation
# V*(c- c_n)/dt = sum( flow_rate * c_inputs) - sum(flowrate*c) + generation