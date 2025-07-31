# A simple automaton that increments or decrements a state variable
# This automaton has two actions: "inc" to increment and "dec" to decrement
# Sayan Mitra, 2025

from z3 import *
from Automaton import Automaton

x = Int('x')
state_vars = [x]
action_names = ["inc", "dec"]
init_pred = (x == 0)

def incdec_transition(s_vars, a, s_prime_vars):
    x, = s_vars
    x_p, = s_prime_vars
    if a == "inc":
        return x_p == x + 1
    elif a == "dec":
        return x_p == x - 1
    return False

def policy(s):
    """Simple policy that increments if x < 10, decrements if x > -10."""
    x, = s
    if x.as_long() < 10:
        return "inc"
    elif x.as_long() > -10:
        return "dec"
    else:
        return "inc"
    return None

# Export the automaton instance
if __name__ == "__main__":
    # Create the automaton instance
    IncDec = Automaton(state_vars, action_names, init_pred, incdec_transition)
    trace1 = IncDec.generate_execution(max_len=50)
    trace2 = IncDec.generate_execution(action_policy=policy, max_len=50)
    IncDec.print_trace(trace1)
    IncDec.print_trace(trace2)
