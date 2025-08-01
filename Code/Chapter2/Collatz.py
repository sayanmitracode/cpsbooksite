# collatz_automaton.py

from z3 import *
from Automaton import Automaton
from State import State
import matplotlib.pyplot as plt

# Define the state structure using the State class
state_template = State([("x", IntSort(), 0)])

# Initial predicate
x = Const("x", IntSort())
init_pred = (x == 7)

actions = ["update"]

# Transition function
def collatz_transition(state, action, state_prime):
    x, = state
    x_p, = state_prime
    if action == "update":
        return Or(
            And(x % 2 == 0, x_p == x / 2),
            And(x % 2 == 1, x_p == 3 * x + 1)
        )
    return False

# This function will become part of the automaton class
# Visualization function 
# def plot_multiple_execs(execs, labels=None, title="Execution Traces of x"):
#     plt.figure(figsize=(10, 5))
#     for i, exec in enumerate(execs):
#         x_vals = [s.get_values("x").as_long() for s in exec]
#         steps = list(range(len(x_vals)))
#         label = labels[i] if labels else f"Trace {i+1}"
#         plt.plot(steps, x_vals, marker='o', label=label)
#     plt.xlabel("Step")
#     plt.ylabel("x")
#     plt.title(title)
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()
#     plt.show()

if __name__ == "__main__":
    # Instantiate the automaton
    Collatz = Automaton(state_template, actions, init_pred, collatz_transition)

    print(Collatz.state_vars) 
    print(Collatz.actions)
    print(Collatz.init_predicate)
    s0= State([("x", IntSort(), IntVal(7))])
    print(repr(Collatz.post_one(s0, "update")))

    # Single trace from default init
    exec = Collatz.generate_single_execution(max_len=200)
    Collatz.print_execution(exec)

    # Multiple executions from different initial states
    initial_values = [5, 11, 19, 27, 47]
    execs = []
    labels = []

    for x0 in initial_values:
        init_state = State([("x", IntSort(), IntVal(x0))])
        exec = Collatz.generate_single_execution(start_state=init_state)
        execs.append(exec)
        labels.append(f"x={x0}")

    Collatz.plot_multiple_executions(execs, var_names=["x"], labels=labels)