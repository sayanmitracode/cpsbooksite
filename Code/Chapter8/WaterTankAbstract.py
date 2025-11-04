import os
import sys
from typing import List, Tuple

from z3 import (
    And,
    BoolSort,
    BoolVal,
    Const,
    IntSort,
    IntVal,
    Or,
    Solver,
    is_true,
)

# Ensure Chapter2 modules are importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)
CHAPTER2_DIR = os.path.join(REPO_ROOT, "Chapter2")
if CHAPTER2_DIR not in sys.path:
    sys.path.append(CHAPTER2_DIR)

from Chapter2.Automaton import Automaton  # noqa: E402
from Chapter2.State import State  # noqa: E402


class WaterTankAbstractAutomaton(Automaton):
    """Predicate abstraction with only P1: x <= H."""

    FILL_MODE = 0
    DRAIN_MODE = 1

    def __init__(self):
        mode_var = Const("mode", IntSort())
        safe_var = Const("safe", BoolSort())
        init_predicate = And(
            mode_var == IntVal(self.FILL_MODE),
            safe_var,
        )

        state_template = State(
            [
                ("mode", IntSort(), IntVal(self.FILL_MODE)),
                ("safe", BoolSort(), BoolVal(True)),
            ]
        )

        def transition(s_vars, action, s_prime_vars):
            mode, safe = s_vars
            mode_next, safe_next = s_prime_vars
            fill = IntVal(self.FILL_MODE)
            drain = IntVal(self.DRAIN_MODE)
            safe_true = BoolVal(True)
            safe_false = BoolVal(False)

            # Abstract behavior: no rate or guard info.
            fill_cases = [
                And(mode == fill, safe == safe_true, mode_next == fill, safe_next == safe_true),
                And(mode == fill, safe == safe_true, mode_next == fill, safe_next == safe_false),
                And(mode == fill, safe == safe_true, mode_next == drain, safe_next == safe_true),
                And(mode == fill, safe == safe_true, mode_next == drain, safe_next == safe_false),
            ]

            drain_cases = [
                And(mode == drain, safe == safe_true, mode_next == drain, safe_next == safe_true),
                And(mode == drain, safe == safe_true, mode_next == fill, safe_next == safe_true),
            ]

            unsafe_cases = [
                And(
                    safe == safe_false,
                    safe_next == safe_false,
                    Or(mode == fill, mode == drain),
                    Or(mode_next == fill, mode_next == drain),
                )
            ]

            if action == "step":
                return Or(*(fill_cases + drain_cases + unsafe_cases))
            return False

        super().__init__(state_template, ["step"], init_predicate, transition)

    def format_state_label(self, state: State) -> str:
        mode_val = state.get_values("mode").as_long()
        safe_val = state.get_values("safe")
        mode_str = "Fill" if mode_val == self.FILL_MODE else "Drain"
        safe_str = "Safe" if is_true(safe_val) else "Overflow"
        return f"{mode_str}, {safe_str}"


def enumerate_reachable_states(automaton: WaterTankAbstractAutomaton, max_depth: int = 4):
    init_state = automaton.sample_initial_state()
    graph = automaton.reachability_tree(
        initial_state=init_state,
        max_depth=max_depth,
        all_actions=True,
    )

    reachable: List[Tuple[int, State]] = []
    for node_key in graph.nodes:
        depth = graph.nodes[node_key]["depth"]
        state = graph.nodes[node_key]["state"]
        reachable.append((depth, state))

    reachable.sort(key=lambda item: (item[0], automaton.format_state_label(item[1])))
    return graph, reachable


if __name__ == "__main__":
    abstract = WaterTankAbstractAutomaton()
    graph, frontier = enumerate_reachable_states(abstract, max_depth=3)

    print("Reachable abstract states:")
    for depth, state in frontier:
        print(f"  depth {depth}: {abstract.format_state_label(state)}")

    abstract.plot_reachability_tree(
        graph,
        title="Reachability: Predicate Abstraction with P1",
    )
