# A verse agent that simulates the passage of time at a constant rate.
# It can be used to model a timer in a control system.
from typing import Tuple, List

import numpy as np
from scipy.integrate import ode
from verse import Scenario, ScenarioConfig
from verse import BaseAgent
from basic_timer import TimerMode
from verse.plotter.plotter2D import *
import plotly.graph_objects as go


class TimeAgent(BaseAgent):
    """Dynamics of time moving forward at a constant rate."""

    def __init__(self, id, code=None, file_name=None):
        """Contructor for the agent
        """
        # Calling the constructor of tha base class
        super().__init__(id, code, file_name)

    def dynamics(self, t, state):
        """Defines the RHS of the ODE used to simulate trajectories"""
        time = state
        time_dot = 1
        return [time_dot]


if __name__ == "__main__":
    # Set up scenario
    scenario = Scenario(ScenarioConfig(parallel=False))

    # Create an instance of the TimeAgent
    CONTROLLER = "/Users/mitras/Jekyll/cpsbook/Code/Chapter2/basic_timer.py"
    atimer = TimeAgent("red_timer", file_name=CONTROLLER)
    # Add agent and initial condition
    scenario.add_agent(atimer)
    # Remember the initial set is a list of initial sets for all the agents
    # and the initial set for each agent is a pair of lists of states defining
    # the lower and upper bounds of the initial set
    scenario.set_init([[[0]]], [(TimerMode.NORMAL,)])  # Initial time = 0

    trace = scenario.simulate_simple(20, 0.01, 6)
    # Plotting the trace


    # Plot
    fig = simulation_tree(
        trace,
        map=None,
        fig=go.Figure(),
        x_dim=0, y_dim=1,
        print_dim_list=None,
        map_type='lines',
        scale_type='trace',
        label_mode='None',
        sample_rate=1
    )
    fig.show()
    print(trace)
    print_tree_node_trace(trace.root)