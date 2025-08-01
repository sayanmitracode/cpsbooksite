from z3 import *
from Automaton import Automaton
from State import State

class IncDecAutomaton(Automaton):
    """Subclass of Automaton for the IncDec example to redefine the format_state_label method
    which converts a single integer state to a string representation."""
    def format_state_label(self, state):
        return str(state.get_values("x"))

# Define the state using the State class template
state_template = State([("x", IntSort(), 0)])
actions = ["inc", "dec"]
init_pred = (Const("x", IntSort()) == 0)

def incdec_transition(s_vars, a, s_prime_vars):
    x, = s_vars
    x_p, = s_prime_vars
    if a == "inc":
        return x_p == x + 1
    elif a == "dec":
        return x_p == x - 1
    return False

def policy(state):
    x_val = state.get_values("x").as_long()
    if x_val < 10:
        return "inc"
    elif x_val > -10:
        return "dec"
    return "inc"

if __name__ == "__main__":
    IncDec = IncDecAutomaton(state_template, actions, init_pred, incdec_transition)

    exec1 = IncDec.generate_single_execution(max_len=10)
    exec2 = IncDec.generate_single_execution(action_policy=policy, max_len=10)

    print("Execution trace with default policy:")
    IncDec.print_execution(exec1)
    print("\nExecution trace with custom policy:")
    IncDec.print_execution(exec2)

    init_state = State([("x", IntSort(), IntVal(0))])
    G = IncDec.reachability_tree(initial_state=init_state, max_depth=4, all_actions=True)
    IncDec.plot_reachability_tree(G, title="IncDec Reachability Tree")
    IncDec.graphviz_reachability_tree(G, title="IncDec Reachability Tree", layout="dot", figsize=(10, 10))
