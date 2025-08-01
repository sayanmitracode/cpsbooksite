class State:
    """
    A concrete or symbolic state represented as a list of (name, sort, value) tuples.
    """
    def __init__(self, var_list):
        self.components = []  # list of (name, sort, value)
        for v in var_list:
            if isinstance(v, tuple) and len(v) == 3:
                self.components.append(v)
            else:
                raise ValueError("Each variable must be a (name, sort, value) tuple")

    @classmethod
    def from_z3(cls, vars, vals):
        """
        Create a State from a list of z3 variables and corresponding concrete values.
        """
        components = []
        for var, val in zip(vars, vals):
            components.append((var.decl().name(), var.sort(), val))
        return cls(components)

    def to_z3_subst(self, vars):
        """Return a list of equalities for substitution: [v == val, ...]"""
        return [v == val for (_, _, val), v in zip(self.components, vars)]

    def __hash__(self):
        return hash(tuple(self.components))

    def __eq__(self, other):
        return isinstance(other, State) and self.components == other.components

    def __str__(self):
        """Return a string representation of the state for users to quickly understand 
        the state."""
        return "(" + ", ".join(f"{n}={v}" for n, _, v in self.components) + ")"

    def __repr__(self):
        """Return a more detailed representation of the state for debugging."""
        return "State([" + ", ".join(f"({n!r}, {s!r}, {v!r})" for (n, s, v) in self.components) + "])"

    def to_key(self):
        """Return a hashable canonical representation for graph keys."""
        return tuple((n, str(s), str(v)) for n, s, v in self.components)

    def get_values(self, name):
        """Return the value of the state component with the given name."""
        for (n, _, v) in self.components:
            if n == name:
                return v
        raise KeyError(f"No state component named '{name}'")
