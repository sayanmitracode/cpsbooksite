from z3 import *
from Automaton import Automaton
from State import State

class DijkstraASYN(Automaton):
    def __init__(self, N, K):
        self.N = N
        self.K = K
        state_components = [(f"x{i}", IntSort(), 0) for i in range(N)]
        state_template = State(state_components)
        actions = [f"mov{i}" for i in range(N)]
        x_vars = [Const(f"x{i}", IntSort()) for i in range(N)]

        # Example initial predicate: no two adjacent nodes are equal
        init_pred = And(x_vars[0] != x_vars[1], x_vars[2] != x_vars[1]) if N >= 3 else x_vars[0] != x_vars[1]
        super().__init__(state_template, actions, init_pred, self.transition)

    def has_token(self, i, x_vars):
        """Return a Z3 BoolRef encoding 'node i has token' over x_vars"""
        if i == 0:
            return x_vars[0] == x_vars[self.N - 1]
        else:
            return x_vars[i] != x_vars[i - 1]

    def transition(self, s_vars, a, s_p_vars):
        if not a.startswith("mov"):
            return False

        i = int(a[len("mov"):])
        if not (0 <= i < self.N):
            return False

        token_cond = self.has_token(i, s_vars)
        if_token_constraints = []

        for j in range(self.N):
            if j == i:
                if i == 0:
                    update = s_p_vars[i] == (s_vars[i] + 1) % self.K
                else:
                    update = s_p_vars[i] == s_vars[i - 1]
                if_token_constraints.append(update)
            else:
                if_token_constraints.append(s_p_vars[j] == s_vars[j])

        # If node i does not have the token, transition is not allowed
        return And(token_cond, And(if_token_constraints))

    def format_state_label(self, state):
        return " ".join(str(val) for (_, _, val) in state.components)


if __name__ == "__main__":
    A = DijkstraASYN(N=3, K=4)

    init_state = A.sample_initial_state()
    trace = A.generate_single_execution(start_state=init_state,  max_len=15)
    A.print_execution(trace)
    G = A.reachability_tree(initial_state=init_state, max_depth=10, all_actions=True)
    A.plot_reachability_tree(G, title="Dijkstra Asynchronous Token Ring")
    
