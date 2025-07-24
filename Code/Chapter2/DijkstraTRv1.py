from verse.plotter.plotter2D import *
from verse.agents.example_agent.ball_agent import BallAgent
from verse import Scenario, ScenarioConfig
from enum import Enum, auto
import copy

# Parameters
N = 5  # Number of agents
K = 3  # Token values in 0 to K-1

# Define ID and Val types
ID = list(range(N))
Val = list(range(K))

# Create automaton
class DijkstraTR(Automaton):
    def __init__(self, N, K):
        super().__init__('DijkstraTR')
        self.N = N
        self.K = K
        self.ID = list(range(N))
        self.Val = list(range(K))

        # State: x[i] for each agent i
        self.vars = {f'x[{i}]': 0 for i in self.ID}  # Initial state: all 0

        self.define_transitions()

    def define_transitions(self):
        trans = []

        # Transition for agent 0
        def guard0(x):
            return x['x[0]'] == x[f'x[{self.N - 1}]']

        def update0(x):
            x_new = deepcopy(x)
            x_new['x[0]'] = (x['x[0]'] + 1) % self.K
            return x_new

        trans.append(SymbolicTransition(guard0, update0, name="update_0"))

        # Transitions for agent i > 0
        for i in range(1, self.N):
            def make_guard(i):
                return lambda x, i=i: x[f'x[{i}]'] != x[f'x[{i - 1}]']

            def make_update(i):
                return lambda x, i=i: {**x, f'x[{i}]': x[f'x[{i - 1}]']}

            trans.append(SymbolicTransition(make_guard(i), make_update(i), name=f"update_{i}"))

        self.transitions = trans


# Instantiate automaton
automaton = DijkstraTR(N=N, K=K)

# Define initial condition
init_state = {f'x[{i}]': 0 for i in range(N)}  # all start at 0

# Configure and run simulation
sim_config = SimulationConfig(init_state=init_state, time_horizon=20, sampling_time=1.0)
trace = simulate(automaton, sim_config)

# Plot result
for i in range(N):
    plt.plot([s[f'x[{i}]'] for s in trace], label=f'x[{i}]')
plt.xlabel('Step')
plt.ylabel('Value')
plt.title('Dijkstra Token Ring Automaton Simulation')
plt.legend()
plt.grid(True)
plt.show()
