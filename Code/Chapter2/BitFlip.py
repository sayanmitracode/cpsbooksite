# BitFlipAutomaton: A simple automaton over 3 bits with flip actions
# Author: Sayan Mitra (2025)

from z3 import *
from Automaton import Automaton

class BitFlipAutomaton(Automaton):
    """This is a subclass of Automaton for the BitFlip example 
    and it redefines the format_state_label method to convert Z3 Bool values to 0/1 strings."""
    def format_state_label(self, state):
        """Convert Z3 Bool values to 0/1 string."""
        return ''.join(['1' if is_true(v) else '0' for v in state])

# Define 3 boolean state variables
b2, b1, b0 = Bools("b2 b1 b0")
state_vars = [b2, b1, b0]
actions = ["flip2", "flip1", "flip0"]

# Initial state: all bits false (000)
init_pred = And(Not(b2), Not(b1), Not(b0))

# Transition relation: flipping one bit at a time
def bitflip_transition(s_vars, a, s_prime_vars):
    b2, b1, b0 = s_vars
    b2p, b1p, b0p = s_prime_vars
    if a == "flip0":
        return And(b0p == Not(b0), b1p == b1, b2p == b2)
    elif a == "flip1":
        return And(b1p == Not(b1), b0p == b0, b2p == b2)
    elif a == "flip2":
        return And(b2p == Not(b2), b0p == b0, b1p == b1)
    return False

# Run example
if __name__ == "__main__":
    BitFlip = BitFlipAutomaton(state_vars, actions, init_pred, bitflip_transition)

    G = BitFlip.reachability_tree(initial_state=[False, False, False], max_depth=3, all_actions=True)

    BitFlip.plot_reachability_tree(G, title="BitFlip Reachability Tree")
    # BitFlip.graphviz_reachability_tree(G, title="BitFlip Reachability Tree", layout="dot")
