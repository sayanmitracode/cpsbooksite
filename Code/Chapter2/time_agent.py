# Example agent.
from typing import Tuple, List

import numpy as np
from scipy.integrate import ode

from verse import BaseAgent
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
    # Create an instance of the TimeAgent
    atimer = TimeAgent("red_timer", file_name="basic_timer.py")
    trace = atimer.TC_simulate({"none"}, [0], 10, 0.05)
    # Plotting the trace
    # x_dim is the simulation time and y_dim is the state of the timer which is also time
    # the two should be the same
    fig = simulation_tree(trace, map=None, fig=go.Figure(), x_dim=0, y_dim=1, print_dim_list=None, map_type='lines', scale_type='trace', label_mode='None', sample_rate=1)
    fig.show()
    print(trace)