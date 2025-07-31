from z3 import *

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


    def generate_execution(self, start_vals=None, action_policy=None, max_len=100):
        """
        Generate a concrete execution trace.
        
        Parameters:
        - start_vals: list of z3 values or Python ints; if None, pick arbitrary state satisfying init_predicate
        - action_policy: function(state) -> action_name (optional); defaults to first action
        - max_len: maximum number of steps
        
        Returns:
        - trace: list of states (each is a list of values for state_vars)
        """
        if start_vals is None:
            # Pick an arbitrary initial state satisfying the init_predicate
            solver = Solver()
            solver.add(self.init_predicate)
            if solver.check() != sat:
                raise ValueError("No initial state satisfies the initial predicate.")
            model = solver.model()
            current = [model.eval(v, model_completion=True) for v in self.state_vars]
        else:
            current = [IntVal(v) if isinstance(v, int) else v for v in start_vals]

        trace = [current]

        for _ in range(max_len):
            action = action_policy(current) if action_policy else self.action_names[0]
            next_state = self.post_one(current, action)
            if not next_state:
                break
            trace.append(next_state)
            current = next_state
        return trace



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