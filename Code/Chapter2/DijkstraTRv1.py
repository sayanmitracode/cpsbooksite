from verse.plotter.plotter2D import simulation_tree #, dump_analysis_tree
from time_agent import TimeAgent  
from verse import Scenario, ScenarioConfig
import plotly.graph_objects as go
from enum import Enum, auto
import copy

class TRMode(Enum):
    NORMAL = auto()

class State:
    def __init__(self, time: float, x: list, mode: TRMode):
        self.time = time
        self.x = x
        self.mode = mode

def decisionLogic(ego: State):
    """
    Implements update(i) at every delta_t = 1.0
    """
    delta_t = 1.0
    N = 4
    K = 3

    output = copy.deepcopy(ego)
    t = ego.time
    x = ego.x.copy()
    
    i = int((t // delta_t) % N)
    if t % delta_t < 1e-4:  # approximate trigger condition at delta_t
        if i == 0:
            if x[0] == x[N - 1]:
                x[0] = (x[0] + 1) % K
        else:
            if x[i] != x[i - 1]:
                x[i] = x[i - 1]
    output.x = x
    return output



# Parameters
N = 4
init_x = [0 for _ in range(N)]
sim_time = 20
step_size = 0.01
max_branch = 6

# Create scenario
scenario = Scenario(ScenarioConfig(parallel=False))
CONTROLLER = "/Users/mitras/Jekyll/cpsbook/Code/Chapter2/DijkstraTRv1.py"
agent = TimeAgent("token-ring", file_name=CONTROLLER)
scenario.add_agent(agent)

# Initial state: time=0.0, x = [0, ..., 0]
scenario.set_init(
    [[[0.0] + init_x]],
    [(TRMode.NORMAL,)]
)

# Simulate
trace = scenario.simulate_simple(sim_time, step_size, max_branch)

# Plot
fig = simulation_tree(
    trace, map=None, fig=go.Figure(),
    x_dim=0, y_dim=1, map_type='lines',
    scale_type='trace', label_mode='None', sample_rate=1
)
fig.show()
