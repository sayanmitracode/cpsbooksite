from z3 import *
from Automaton import Automaton
from State import State

class DijkstraSTR(Automaton):
    def __init__(self, N, K):
        self.N = N
        self.K = K
        state_components = [(f"x{i}", IntSort(), 0) for i in range(N)]
        state_template = State(state_components)
        actions = ["update"]
        x_vars = [Const(f"x{i}", IntSort()) for i in range(N)]
        # A simple initial predicate could be all zeros 
        #init_pred = x_vars[0] == 0  # for example
        # A more interesting initial predicate
        init_pred = And(x_vars[0] != x_vars[1], x_vars[2] != x_vars[1])
        super().__init__(state_template, actions, init_pred, self.transition)

    def has_token(self, i, x_vars):
        """
        Implement this function to return a Z3 BoolRef 
        encoding the condition that node i currently has the token.
        """
    
        if i == 0:
            return True # TODO For node 0, the token condition depends on x_vars[0] and x_vars[N-1].
        else:
            return True # TODO For other nodes, the token condition depends on x_vars[i] and x_vars[i-1].

    def transition(self, s_vars, a, s_p_vars):
        if a != "update":
            return False

        constraints = []
        for i in range(self.N):
            token_cond = self.has_token(i, s_vars)
            if i == 0:
                update = s_p_vars[i] == (s_vars[i] + 1) % self.K
            else:
                update = s_p_vars[i] == s_vars[i - 1]
            constraints.append(If(token_cond, update, s_p_vars[i] == s_vars[i]))
        return And(constraints)


    def format_state_label(self, state):
        return " ".join(str(val) for (_, _, val) in state.components)


if __name__ == "__main__":
    A = DijkstraSTR(N=3, K=4)

    init_state = A.sample_initial_state()
    trace = A.generate_single_execution(start_state=init_state, max_len=15)
    A.print_execution(trace)
    G = A.reachability_tree(initial_state=init_state, max_depth=15)
    A.plot_reachability_tree(G, title="Dijkstra Synchronous Token Ring")