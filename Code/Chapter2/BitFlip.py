from z3 import *
from Automaton import Automaton
from State import State

class BitFlipAutomaton(Automaton):
    """Subclass of Automaton for the BitFlip example.
    Redefines format_state_label to show state as 0/1 string."""
    def format_state_label(self, state):
        return ''.join(['1' if is_true(state.get_values(f"b{i}")) else '0' for i in reversed(range(3))])

# Define the state using the State class template
state_template = State([
    ("b0", BoolSort(), False),
    ("b1", BoolSort(), False),
    ("b2", BoolSort(), False),
])
actions = ["flip0", "flip1", "flip2"]
x0 = Const("b0", BoolSort())
x1 = Const("b1", BoolSort())
x2 = Const("b2", BoolSort())
init_pred = And(Not(x2), Not(x1), Not(x0))

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

if __name__ == "__main__":
    BitFlip = BitFlipAutomaton(state_template, actions, init_pred, bitflip_transition)

    init_state = State([
        ("b0", BoolSort(), False),
        ("b1", BoolSort(), False),
        ("b2", BoolSort(), False)
    ])
    exec = BitFlip.generate_single_execution(max_len=200)
    BitFlip.print_execution(exec)

    G = BitFlip.reachability_tree(initial_state=init_state, max_depth=3, all_actions=True)

    BitFlip.plot_reachability_tree(G, title="BitFlip Reachability Tree")
    BitFlip.graphviz_reachability_tree(G, title="BitFlip Reachability Tree", layout="dot", figsize=(10, 10))
