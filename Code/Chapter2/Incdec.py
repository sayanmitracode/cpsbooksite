# IncDecAutomaton: Increments or decrements a single integer variable
# Author: Sayan Mitra (2025)

from z3 import *
from Automaton import Automaton

class IncDecAutomaton(Automaton):
    """This is a subclass of Automaton for the IncDec example mainly to redefine the format_state_label method
    which converts a single integer state to a string representation."""
    def format_state_label(self, state):
        """Format single integer state as a string."""
        return str(state[0])

# Define single integer state variable
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

# Optional: define a simple policy
def policy(s):
    x, = s
    if x.as_long() < 10:
        return "inc"
    elif x.as_long() > -10:
        return "dec"
    return "inc"

# Run example
if __name__ == "__main__":
    IncDec = IncDecAutomaton(state_vars, action_names, init_pred, incdec_transition)

    exec1 = IncDec.generate_single_execution(max_len=10)
    exec2 = IncDec.generate_single_execution(action_policy=policy, max_len=10)

    print("Execution trace with default policy:")
    IncDec.print_trace(exec1)
    print("\nExecution trace with custom policy:")
    IncDec.print_trace(exec2)

    G = IncDec.reachability_tree(initial_state=[0], max_depth=4, all_actions=True)
    IncDec.plot_reachability_tree(G, title="IncDec Reachability Tree")
