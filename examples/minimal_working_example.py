"""
A minimal example for solving a problem.
"""

import cvxpy
from cvxpy.reductions.solvers.conic_solvers import scipy_conif

x = cvxpy.Variable()
problem = cvxpy.Problem(
    objective = cvxpy.Maximize(2*x+(x-1)),
    constraints=[x <= 2])
print()
print(problem.solve())

problem = cvxpy.Problem(
    objective = cvxpy.Maximize(2*x+(x-1)),
    constraints=[x <= 2])
print()
print(problem.solve(solver=cvxpy.SCIPY, scipy_options={"method":"highs"}))
