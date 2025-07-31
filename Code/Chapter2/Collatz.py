# model of an automaton that simulates the Collatz conjecture
# It generates traces of the state variable x, which follows the rules:
# - If x is even, the next state is x / 2
# - If x is odd, the next state is 3 * x + 1
# This is a deterministic, integer-valued automaton. 
# For arbitrary initial values, it is Unknown whether it will reach 1.
# Sayan Mitra, 2025

from z3 import *
from Automaton import Automaton
import matplotlib.pyplot as plt


x = Int('x')
state_vars = [x]
action_names = ["update"]
init_predicate = x == 47

def collatz_transition(s_vars, a, s_prime_vars):
    x, = s_vars
    x_p, = s_prime_vars
    if a == "update":
        return Or(
            And(x % 2 == 0, x_p == x / 2),
            And(x % 2 == 1, x_p == 3 * x + 1)
        )
    return False


def plot_multiple_execs(execs, labels=None, title="Execution Traces of x"):
    """
    execs: list of executions (each execution is a list of single-variable states)
    labels: optional list of labels for the executions
    """
    plt.figure(figsize=(10, 5))

    for i, exec in enumerate(execs):
        x_vals = [s[0].as_long() for s in exec]  # Extracting x python values from the z3
        steps = list(range(len(x_vals)))
        label = labels[i] if labels else f"Trace {i+1}"
        plt.plot(steps, x_vals, marker='o', label=label)

    plt.xlabel("Step")
    plt.ylabel("x")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Create the automaton instance
    Collatz = Automaton(state_vars, action_names, init_predicate, collatz_transition)

    # Example execution
    trace = Collatz.generate_single_execution(max_len=200)
    Collatz.print_trace(trace)

    #for i, s in enumerate(trace):
    #   print(f"Step {i}: {s[0]}")

    initial_values = [5, 11, 19, 27, 47]
    traces = []
    labels = []

    for x0 in initial_values:
        exec = Collatz.generate_single_execution(start_vals=[x0])
        state_exec = [state for (_, state) in exec]
        traces.append(state_exec)
        labels.append(f"x={x0}")


    plot_multiple_execs(traces, labels, title="Collatz Executions from Various Initial Values")
