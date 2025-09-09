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
        """
        Implement this function to return a Z3 BoolRef 
        encoding the condition that node i currently has the token.
        """
    
        if i == 0:
            return True # TODO For node 0, the token condition depends on x_vars[0] and x_vars[N-1].
        else:
            return True # TODO For other nodes, the token condition depends on x_vars[i] and x_vars[i-1].
        
    def transition(self, s_vars, a, s_p_vars):
        """
        Implement the transition relation for Dijkstra's asynchronous token ring.

        Guidance:
        - The action `a` will be one of the strings "mov0", "mov1", ..., "mov{N-1}".
        - Extract the index of the moving process from `a`.
        - A process can only update if it currently **has the token**.
        * Use the `has_token(i, s_vars)` function to get a Z3 BoolRef for this condition.
        - If the process has the token:
            - For node 0: update its state as (s_vars[0] + 1) % K
            - For other nodes: copy the state of the previous node
        - All other processes remain unchanged.
        - The method should return a Z3 BoolRef representing the conjunction of all these constraints.
        """

        if not a.startswith("mov"):
            return False

        i = int(a[len("mov"):])
        if not (0 <= i < self.N):
            return False

        token_cond = True # TODO add token condition for node i. 
        if_token_constraints = []

        for j in range(self.N):
            if j == i:
                if i == 0:
                    update = s_p_vars[i] == (s_vars[i] + 1) % self.K
                else:
                    update = s_p_vars[i] == s_vars[i - 1]
                if_token_constraints.append(True) # TODO update node j 
            else:
                if_token_constraints.append(True) # TODO enforce node j does not change if j!=i
                
        # If node i does not have the token, transition is not allowed
        return True # TODO transition happens only when node i hase the token and satisfies constraints.

    def format_state_label(self, state):
        return " ".join(str(val) for (_, _, val) in state.components)


if __name__ == "__main__":
    A = DijkstraASYN(N=3, K=4)

    init_state = A.sample_initial_state()
    trace = A.generate_single_execution(start_state=init_state,  max_len=15)
    A.print_execution(trace)
    G = A.reachability_tree(initial_state=init_state, max_depth=10, all_actions=True)
    A.plot_reachability_tree(G, title="Dijkstra Asynchronous Token Ring")
    
