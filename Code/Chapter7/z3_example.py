from z3 import Int, And, Or, Not, Implies, Solver, AtMost, AtLeast, simplify, set_option, solve, Real,Bool, If
import z3

# Define Variables
# x = Int('x')
# x = Bool('x')
# x = Real('x')

# Simplify Math Expression
# x = Int('x')
# y = Int('y')
# print (simplify(x + y + 2*x + 3))
# print (simplify(x < y + x + 2))
# print (simplify(And(x + 1 >= 3, x**2 + x**2 + y**2 + 2 >= 5)))

# Solve Contrains
# x = Int('x')
# y = Int('y')
# solve(x>2, y < 10, x+2*y==7)
# solve(x>4, x<-1)

# Set Precision
# x = Real('x')
# solve(3*x == 1)
# set_option(rational_to_decimal=True)
# solve(3*x == 1)
# set_option(precision=30)
# solve(3*x == 1)

# Solve Boolean Constraints
# p = Bool('p')
# q = Bool('q')
# r = Bool('r')
# solve(Implies(p, q), r == Not(q), Or(Not(p), r))
