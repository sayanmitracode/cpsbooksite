from z3 import *
import networkx as nx
# from z3 import IntVal
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph

class Automaton:
    def __init__(self, state_vars, action_names, init_predicate, transition_relation):
        """
        state_vars: list of z3 variables (representing current state)
        action_names: list of strings
        init_predicate: z3.BoolRef over state_vars
        transition_relation: function (s_vars, a, s_prime_vars) -> z3.BoolRef
        """
        self.state_vars = state_vars
        self.action_names = action_names
        self.init_predicate = init_predicate
        self.transition_relation = transition_relation

        # For internal use: post-state vars (primed version of state_vars)
        self.state_vars_prime = [FreshConst(v.sort()) for v in self.state_vars]
    
    def normalize(self, vals):
        """Convert Python ints and floats to Z3 IntVal or RealVal as appropriate."""
        return [
            IntVal(v) if isinstance(v, int)
            else RealVal(v) if isinstance(v, float)
            else v
            for v in vals
        ]
    

    def is_initial(self, s_val):
        """Check if a concrete state valuation satisfies the initial predicate"""
        s = Solver()
        s.add([v == val for v, val in zip(self.state_vars, s_val)])
        s.add(self.init_predicate)
        return s.check() == sat

    def post_one(self, state, action):
        """Return one successor state for the given state and action."""
        if action not in self.action_names:
            raise ValueError(f"Unknown action: {action}")
        solver = Solver()
        subst = [v == val for v, val in zip(self.state_vars, state)]
        tr = self.transition_relation(self.state_vars, action, self.state_vars_prime)
        solver.add(subst + [tr])
        if solver.check() == sat:
            model = solver.model()
            return [model.eval(v, model_completion=True) for v in self.state_vars_prime]
        return None
    
    def post_action(self, state, action, max_solutions=10):
        """Return all---up to max_solutions---successor states for a given state and action."""
        if action not in self.action_names:
            raise ValueError(f"Unknown action: {action}")
        
        successors = []
        while True:
            result = self.post_one(state, action)
            if result is None:
                break
            successors.append(result)
            # Add a constraint to block this result
            blocking_clause = Or([v != val for v, val in zip(self.state_vars_prime, result)])
            solver = Solver()
            subst = [v == val for v, val in zip(self.state_vars, state)]
            tr = self.transition_relation(self.state_vars, action, self.state_vars_prime)
            solver.add(subst + [tr] + [blocking_clause])
            if len(successors) >= max_solutions or solver.check() != sat:
                break
        return successors

    def post(self, state, max_solutions_per_action=10):
        """Return all successors for a given state across all actions."""
        all_successors = []
        for action in self.action_names:
            succs = self.post_action(state, action, max_solutions=max_solutions_per_action)
            all_successors.extend(succs)
        return all_successors


    def generate_single_execution(self, start_vals=None, action_policy=None, max_len=100):
        """
        Generate a single concrete execution trace.
        start_vals: initial values for the state variables (if None, use initial predicate)
        action_policy: function that takes current state and returns an action name 
        or None to use the first action in action_names.
        max_len: maximum length of the trace
        Returns:
        - trace: list of (action, state) pairs. First action is None for initial state.
        """
        if start_vals is None:
            solver = Solver()
            solver.add(self.init_predicate)
            if solver.check() != sat:
                raise ValueError("No initial state satisfies the initial predicate.")
            model = solver.model()
            current = [model.eval(v, model_completion=True) for v in self.state_vars]
        else:
            current = [IntVal(v) if isinstance(v, int) else v for v in start_vals]

        trace = [(None, current)]  # (action, state)

        for _ in range(max_len):
            action = action_policy(current) if action_policy else self.action_names[0]
            next_state = self.post_one(current, action)
            if not next_state:
                break
            trace.append((action, next_state))
            current = next_state

        return trace



    def reachability_tree(self, initial_state, max_depth=5, action_policy=None, all_actions=False, max_branching=100):
        """
        Build a reachability tree from a given initial concrete state.

        Parameters:
        - initial_state: list of ints or Z3 ExprRefs representing initial state
        - max_depth: maximum depth of BFS
        - action_policy: function(state_list) -> action_name (optional)
        - all_actions: if True, explore all actions at each step
        - max_branching: maximum number of successors to explore per state and action

        Returns:
        - A networkx.DiGraph with nodes = list of Z3 values, edges labeled with actions
        """        
        def state_to_key(s):
            """Convert a state to a hashable key for the graph."""
            return tuple(str(v) for v in s)  # hashable, retains per-var identity

        root = self.normalize(initial_state)
        G = nx.DiGraph()
        root_key = state_to_key(root)
        G.add_node(root_key, state=root, depth=0)
        queue = [root]

        while queue:
            state = queue.pop(0)
            state_key = state_to_key(state)
            depth = G.nodes[state_key]['depth']
            if depth >= max_depth:
                continue

            # Choose actions
            actions = self.action_names if all_actions else [action_policy(state)] if action_policy else [self.action_names[0]]

            for action in actions:
                successors = self.post_action(state, action, max_solutions=max_branching)
                for succ in successors:
                    succ_key = state_to_key(succ)
                    if not G.has_node(succ_key):
                        G.add_node(succ_key, state=succ, depth=depth + 1)
                        queue.append(succ)
                    G.add_edge(state_key, succ_key, label=action)

        return G

    def format_state_label(self, state):
        """
        Override this in subclasses or instances to customize node labels in plots.
        """
        return ','.join(str(v) for v in state)
    

    def plot_reachability_tree(self, G, title="Reachability Tree", figsize=(10, 6)):
        pos = nx.spring_layout(G, seed=42)

        plt.figure(figsize=figsize)

        # Root node coloring
        root_key = min(G.nodes, key=lambda k: G.nodes[k]['depth'])
        node_colors = ['orange' if k == root_key else 'lightblue' for k in G.nodes]

        # State labels
        node_labels = {node: self.format_state_label(G.nodes[node]['state']) for node in G.nodes}
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

        # Draw edges with arc (curved) to show bidirectional transitions clearly
        for u, v, data in G.edges(data=True):
            label = data.get('label', '')
            rad = 0.2 if (v, u) in G.edges else 0.0  # curve only if reverse edge exists
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], connectionstyle=f"arc3,rad={rad}")
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label}, font_color='red')

        plt.title(title)
        plt.axis('off')
        plt.show()



    def graphviz_reachability_tree(self, G, title="Reachability Tree", layout="dot", figsize=(10, 6)):
        """
        Plot the reachability tree using pygraphviz for better layout.

        Parameters:
        - G: networkx.DiGraph with nodes having 'state' and 'depth'
        - title: plot title
        - layout: graphviz layout engine, e.g., 'dot', 'neato', 'fdp'
        - figsize: tuple for figure size
        """
        A = to_agraph(G)

        # Format node labels
        for node in A.nodes():
            state = G.nodes[str(node)]['state']
            label = self.format_state_label(state)
            if G.nodes[str(node)]['depth'] == 0:
                node.attr['color'] = 'red'
                node.attr['style'] = 'filled'
                node.attr['fillcolor'] = 'lightyellow'
            node.attr['label'] = label

        # Format edge labels
        for edge in A.edges():
            label = G.edges[edge[0], edge[1]].get('label', '')
            edge.attr['label'] = label

        A.layout(prog=layout)
        plt.figure(figsize=figsize)
        plt.title(title)
        plt.axis('off')
        plt.imshow(plt.imread(A.draw(format='png')))
        plt.show()


    def Transition(self, state_formula):
        """Compute image of a set under transition relation"""
        s = self.state_vars
        s_prime = self.state_vars_prime
        res = []
        for a in self.action_names:
            tr = self.transition_relation(s, a, s_prime)
            image = Exists(s, And(state_formula, tr))
            res.append(image)
        return simplify(Or(res))

    def reachability_analysis(self, max_iter=20):
        """Compute reachable set using fixed-point iteration"""
        s = self.state_vars
        Reach = self.init_predicate
        for i in range(max_iter):
            Reach_new = simplify(Or(Reach, self.Transition(Reach)))
            if eq(Reach_new, Reach):
                print(f"Fixed point reached at iteration {i}")
                break
            Reach = Reach_new
        return Reach

    def print_trace(self, trace):
        for i, state in enumerate(trace):
            print(f"Step {i}: {', '.join(map(str, state))}")