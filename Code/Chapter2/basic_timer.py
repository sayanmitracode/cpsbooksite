# basic_timer.py

from verse.plotter.plotter2D import simulation_tree
from time_agent import TimeAgent  
# from verse.agents.example_agent.timer_agent import TimeAgent  # Or replace with your actual path
from verse import Scenario, ScenarioConfig
import plotly.graph_objects as go
from enum import Enum, auto
import copy


class TimerMode(Enum):
    '''Any model should have at least one mode. 
    The timer always stays in this NORMAL mode'''
    NORMAL = auto()


class State:
    '''Continuous state of the timer is time in seconds.'''
    time: float
    mode: TimerMode

    def __init__(self, time: float, mode: TimerMode):
        pass


def decisionLogic(ego: State):
    # No decision branching — just returns the current state
    output = copy.deepcopy(ego)
    return output


    
if __name__ == "__main__":
    # Set up scenario
    scenario = Scenario(ScenarioConfig(parallel=False))
    
    # Define agent and controller path
    # This has to set properly
    CONTROLLER = "/Users/mitras/Jekyll/cpsbook/Code/Chapter2/basic_timer.py"
    timer_agent = TimeAgent("timer", file_name=CONTROLLER)

    # Add agent and initial condition
    scenario.add_agent(timer_agent)
    # Remember the initial set is a list of initial sets for all the agents
    # and the initial set for each agent is a pair of lists of states defining
    # the lower and upper bounds of the initial set
    scenario.set_init([[[0]]], [(TimerMode.NORMAL,)])  # Initial time = 0

    # Run simulation
    # The simulation time horizon is the first argument, the step size is the second argument,
    # and the maximum number of branching discrete steps is the third argument
    trace = scenario.simulate_simple(20, 0.01, 6)

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

