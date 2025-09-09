from z3 import *
import networkx as nx
# from z3 import IntVal
from State import State
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph
import io
import ast  # safer than eval

class Automaton:
    def __init__(self, states, actions, init_predicate, transition):
        """
        states: instance of State defining structure of state space, must have a 'components' attribute
        actions: list of action names (strings)
        init_predicate: z3.BoolRef over state_vars
        transition: function (s_vars, a, s_prime_vars) -> z3.BoolRef
        """
        self.states = states
        self.state_vars = [Const(n, s) for n, s, _ in self.states.components]
        self.actions = actions
        self.init_predicate = init_predicate
        self.transition = transition
        self.state_vars_prime = [FreshConst(v.sort()) for v in self.state_vars]

    def is_initial(self, state):
        """Check if a concrete state valuation satisfies the initial predicate"""
        solver = Solver()
        solver.add(state.to_z3_subst(self.state_vars))
        solver.add(self.init_predicate)
        return solver.check() == sat
    
    def sample_initial_state(self):
        solver = Solver()
        solver.add(self.init_predicate)
        if solver.check() == sat:
            model = solver.model()
            vals = [model.eval(v, model_completion=True) for v in self.state_vars]
            return State.from_z3(self.state_vars, vals)
        else:
            raise ValueError("No satisfying initial state found.")

    def enabled(self, state, action):
        """Return True if there exists at least one successor for the given state and action."""
        if action not in self.actions:
            return False
        solver = Solver()
        solver.add(state.to_z3_subst(self.state_vars))
        tr = self.transition(self.state_vars, action, self.state_vars_prime)
        solver.add(tr)
        return solver.check() == sat

    def post_one(self, state, action):
        """Return a single successor state for the given state and action.
        returns error if the action is not valid or not enabled."""
        if action not in self.actions:
            raise ValueError(f"Unknown action: {action}")

        if not self.enabled(state, action):
            raise ValueError(f"Action '{action}' is not enabled in state {state}")

        solver = Solver()
        solver.add(state.to_z3_subst(self.state_vars))
        tr = self.transition(self.state_vars, action, self.state_vars_prime)
        solver.add(tr)

        if solver.check() == sat:
            model = solver.model()
            vals = [model.eval(v, model_completion=True) for v in self.state_vars_prime]
            return State.from_z3(self.state_vars, vals)
        
        # Technically unreachable due to the enabled check above, but for safety:
        return None


    def post_action(self, state, action, max_solutions=10):
        """ Return a list of successor states for the given state and action.
        state: a State instance
        returns a possibly empty list of successor states"""
        if action not in self.actions:
            raise ValueError(f"Unknown action: {action}")

        successors = []
        seen = set()
        while len(successors) < max_solutions:
            next_state = self.post_one(state, action)
            if next_state is None or next_state in seen:
                break
            successors.append(next_state)
            seen.add(next_state)
            blocking_clause = Or([v != val for v, val in zip(self.state_vars_prime, [c[2] for c in next_state.components])])
            solver = Solver()
            solver.add(state.to_z3_subst(self.state_vars))
            solver.add(self.transition(self.state_vars, action, self.state_vars_prime))
            solver.add(blocking_clause)
            if solver.check() != sat:
                break
        return successors

    def post(self, state, max_solutions_per_action=10):
        all_successors = []
        for action in self.actions:
            all_successors.extend(self.post_action(state, action, max_solutions_per_action))
        return all_successors

    def generate_single_execution(self, start_state=None, action_policy=None, max_len=100):
        """        Generate a single execution trace starting from the given state.
        start_state: a State instance,"""
        current = start_state if start_state is not None else self.sample_initial_state()
        trace = [(None, current)]

        for _ in range(max_len):
            enabled_actions = [a for a in self.actions if self.enabled(current, a)]

            if not enabled_actions:
                print(f"Deadlock: No enabled action from state {str(current)}")
                break

            action = action_policy(current) if action_policy else enabled_actions[0]
            next_state = self.post_one(current, action)

            if not next_state:
                print(f"Transition failure: action '{action}' enabled but post_one returned None")
                break

            trace.append((action, next_state))
            current = next_state

        return trace       
   
    def print_execution(self, execution):
        """
        Print the sequence of actions and states in an execution trace.
        execution: list of (action, state) tuples
        """
        for i, (a, s) in enumerate(execution):
            if a is None:
                print(f"Step {i}: Init -> {str(s)}")
            else:
                print(f"Step {i}: {a} -> {str(s)}")

    def plot_multiple_executions(self, execs, labels=None, var_names=None, title="Execution Traces"):
        plt.figure(figsize=(10, 5))
        linestyles = ['-', '--', ':']
        colors = plt.cm.tab10.colors

        for i, exec in enumerate(execs):
            steps = list(range(len(exec)))
            label = labels[i] if labels else f"Trace {i+1}"
            if var_names:
                for j, name in enumerate(var_names[:3]):
                    y_vals = []
                    for (_, s) in exec:
                        val = s.get_values(name)
                        if val.is_int():
                            y_vals.append(val.as_long())
                        else:
                            y_vals.append(float(val.as_decimal(5).replace("?", "")))
                    style = linestyles[j % len(linestyles)]
                    plt.plot(steps, y_vals, linestyle=style, color=colors[i % len(colors)], label=f"{label}: {name}")


            # if var_names:
            #     for j, name in enumerate(var_names[:3]):
            #         y_vals = [s.get_values(name).as_long() for (_, s) in exec]
            #         style = linestyles[j % len(linestyles)]
            #         plt.plot(steps, y_vals, linestyle=style, color=colors[i % len(colors)], label=f"{label}: {name}")
            # else:
            #     y_vals = [s.get_values("x").as_long() for (_, s) in exec]
            #     plt.plot(steps, y_vals, linestyle='-', color=colors[i % len(colors)], label=label)

        plt.xlabel("Step")
        plt.ylabel("State Variable Value")
        plt.title(title)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()                

    def reachability_tree(self, initial_state, max_depth=5, action_policy=None, all_actions=False, max_branching=100):
        """Generate a reachability tree starting from the initial state.
        initial_state: a State instance
        action_policy: function that takes a state and returns an action name
        if action_policy is None, will use the first enabled action
        all_actions: if True, will consider all enabled actions at each state
        max_branching: maximum number of successors to explore per action"""
        G = nx.DiGraph()
        root_key = initial_state.to_key()
        G.add_node(root_key, state=initial_state, depth=0)
        queue = [initial_state]

        while queue:
            state = queue.pop(0)
            state_key = state.to_key()
            depth = G.nodes[state_key]['depth']
            if depth >= max_depth:
                continue
            
            if all_actions:
                actions = [a for a in self.actions if self.enabled(state, a)]
            elif action_policy:
                candidate = action_policy(state)
                actions = [candidate] if self.enabled(state, candidate) else []
            else:
                actions = [self.actions[0]] if self.enabled(state, self.actions[0]) else []
        
            # actions = self.actions if all_actions else [action_policy(state)] if action_policy else [self.actions[0]]
            for action in actions:
                successors = self.post_action(state, action, max_solutions=max_branching)
                for succ in successors:
                    succ_key = succ.to_key()
                    if not G.has_node(succ_key):
                        G.add_node(succ_key, state=succ, depth=depth + 1)
                        queue.append(succ)
                    G.add_edge(state_key, succ_key, label=action)
        return G

 
    def plot_reachability_tree(self, G, title="Reachability Tree", figsize=(10, 6)):
        """Plot the reachability tree using matplotlib and networkx."""
 
        pos = nx.circular_layout(G) # nx.spring_layout(G, seed=42)
        # change this to nx.shell_layout(), nx.circular_layout(), or nx.planar_layout()

        plt.figure(figsize=figsize)
        root_key = min(G.nodes, key=lambda k: G.nodes[k]['depth'])
        node_colors = ['orange' if k == root_key else 'lightblue' for k in G.nodes]
        # Use the custom format_state_label if defined; fallback to str(state)
        node_labels = {
            k: self.format_state_label(G.nodes[k]['state']) 
            if hasattr(self, 'format_state_label') 
            else str(G.nodes[k]['state']) 
            for k in G.nodes
        }
        # node_labels = {k: str(G.nodes[k]['state']) for k in G.nodes}
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

        for u, v, data in G.edges(data=True):
            label = data.get('label', '')
            rad = 0.2 if (v, u) in G.edges else 0.0
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], connectionstyle=f"arc3,rad={rad}")
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label}, font_color='red')
        
        plt.title(title)
        plt.axis('off')
        plt.show()

    def graphviz_reachability_tree(self, G, title="Reachability Tree", layout="dot", figsize=(10, 6)):
        """Visualize the reachability tree using Graphviz and matplotlib."""
        A = to_agraph(G)
        for node in A.nodes():
            node_str = node.get_name()
            key = ast.literal_eval(node_str)
            if isinstance(key, tuple):
                key = tuple(key)
            state = G.nodes[key]['state']
            label = self.format_state_label(state) if hasattr(self, 'format_state_label') else str(state)
            if G.nodes[key]['depth'] == 0:
                node.attr.update({'color': 'red', 'style': 'filled', 'fillcolor': 'orange'})
            else:
                node.attr.update({'color': 'none', 'style': 'filled', 'fillcolor': 'lightblue'})
            node.attr['label'] = label

        for edge in A.edges():
            src = ast.literal_eval(edge[0])
            dst = ast.literal_eval(edge[1])
            label = G.edges[(src, dst)].get('label', '')
            edge.attr['label'] = label

        A.layout(prog=layout)
        png_data = A.draw(format='png')
        plt.figure(figsize=figsize)
        plt.title(title)
        plt.axis('off')
        plt.imshow(plt.imread(io.BytesIO(png_data)))
        plt.show()

