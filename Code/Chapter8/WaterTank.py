import os
import sys
from typing import Callable, List, Optional, Tuple

from z3 import And, Const, IntSort, IntVal, Or, RealSort, RealVal

# Ensure Chapter2 modules are importable when running this file directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)
CHAPTER2_DIR = os.path.join(REPO_ROOT, "Chapter2")
if CHAPTER2_DIR not in sys.path:
    sys.path.append(CHAPTER2_DIR)

from Chapter2.Automaton import Automaton  # noqa: E402
from Chapter2.State import State  # noqa: E402


class WaterTankAutomaton(Automaton):
    """Discrete-time abstraction of the one-tank hybrid controller."""

    FILL_MODE = 0
    DRAIN_MODE = 1

    def __init__(
        self,
        a: float = 5.0,
        b: float = 0.5,
        ell: float = 2.0,
        upper: float = 8.5,
        capacity: float = 10.0,
        dt: float = 0.5,
        initial_level: float = 4.5,
    ):
        self.a = a
        self.b = b
        self.ell = ell
        self.upper = upper
        self.capacity = capacity
        self.dt = dt

        state_template = State(
            [
                ("mode", IntSort(), IntVal(self.FILL_MODE)),
                ("x", RealSort(), RealVal(str(initial_level))),
            ]
        )

        mode_var = Const("mode", IntSort())
        level_var = Const("x", RealSort())
        init_predicate = And(
            mode_var == IntVal(self.FILL_MODE), level_var == RealVal(str(initial_level))
        )

        def transition(s_vars, action, s_prime_vars):
            mode, level = s_vars
            mode_next, level_next = s_prime_vars
            a_val = RealVal(str(self.a))
            b_val = RealVal(str(self.b))
            ell_val = RealVal(str(self.ell))
            upper_val = RealVal(str(self.upper))
            dt_val = RealVal(str(self.dt))

            fill_update = level_next == level + dt_val * (a_val - b_val * level)
            drain_update = level_next == level + dt_val * (-b_val * level)

            stay_fill = And(
                mode == IntVal(self.FILL_MODE),
                level < upper_val,
                mode_next == IntVal(self.FILL_MODE),
                fill_update,
            )
            switch_to_drain = And(
                mode == IntVal(self.FILL_MODE),
                level >= upper_val,
                mode_next == IntVal(self.DRAIN_MODE),
                fill_update,
            )
            stay_drain = And(
                mode == IntVal(self.DRAIN_MODE),
                level > ell_val,
                mode_next == IntVal(self.DRAIN_MODE),
                drain_update,
            )
            switch_to_fill = And(
                mode == IntVal(self.DRAIN_MODE),
                level <= ell_val,
                mode_next == IntVal(self.FILL_MODE),
                drain_update,
            )

            if action == "step":
                return Or(stay_fill, switch_to_drain, stay_drain, switch_to_fill)
            return False

        actions = ["step"]
        super().__init__(state_template, actions, init_predicate, transition)


def simulate_execution(
    automaton: WaterTankAutomaton,
    steps: int = 200,
    policy: Optional[Callable[[State], str]] = None,
) -> List[Tuple[Optional[str], State]]:
    """Generate a single execution using the provided policy."""
    if policy is None:
        policy = lambda _: "step"
    return automaton.generate_single_execution(action_policy=policy, max_len=steps)


if __name__ == "__main__":
    tank = WaterTankAutomaton()
    execution = simulate_execution(tank, steps=120)

    print("Sample execution (first 15 steps):")
    for idx, (action, state) in enumerate(execution[:15]):
        prefix = "Init" if action is None else action
        print(f"{idx:02d}: {prefix} -> {state}")

    tank.plot_multiple_executions(
        [execution],
        labels=["Water Level"],
        var_names=["x"],
        title="Water Tank Controller",
    )
