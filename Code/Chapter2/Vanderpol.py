from z3 import *
from Automaton import Automaton
from State import State

class VanDerPolAutomaton(Automaton):
    def __init__(self, mu=1.0, dt=0.1):
        self.mu = mu
        self.dt = dt

        state_template = State([
            ("x1", RealSort(), 0.0),
            ("x2", RealSort(), 0.0)
        ])
        actions = ["step"]

        x1, x2 = Reals("x1 x2")
        init_pred = And(x1 == 0, x2 == 1)

        super().__init__(state_template, actions, init_pred, self.transition)

    def transition(self, s_vars, a, s_p_vars):
        if a != "step":
            return False

        x1, x2 = s_vars
        x1p, x2p = s_p_vars
        mu, dt = self.mu, self.dt

        # Euler-discretized Van der Pol dynamics
        dx1 = x2
        dx2 = mu * (1 - x1**2) * x2 - x1

        return And(
            x1p == x1 + dt * dx1,
            x2p == x2 + dt * dx2
        )

    def format_state_label(self, state):
        x1 = state.get_values("x1")
        x2 = state.get_values("x2")
        return f"{float(x1):.2f}, {float(x2):.2f}"


if __name__ == "__main__":
    A = VanDerPolAutomaton(mu=1.0, dt=0.1)

    init_state = A.sample_initial_state()
    exec = A.generate_single_execution(start_state=init_state, max_len=50)
    print("Single execution from initial state:")
    # A.print_execution(exec)
    A.plot_multiple_executions(
        execs=[exec],
        labels=["Van der Pol"],
        var_names=["x1", "x2"],
        title="Van der Pol Oscillator Trajectory"
    )
    # G = A.reachability_tree(initial_state=init_state, max_depth=20)
    # A.plot_reachability_tree(G, title="Van der Pol Reachability Tree")
