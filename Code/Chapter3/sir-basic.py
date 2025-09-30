import numpy as np
import pylab as pl
import grid as hr   # keeping your custom grid class

class ODE:
    """Simple SIR model."""

    def __init__(self, betaval, gammaval, Nval, g0val, min, max):
        self.dimension = 3
        self.beta = betaval
        self.gamma = gammaval
        self.N = Nval
        self.g0 = g0val
        self.R0 = self.beta / self.gamma
        self.range = hr.Hyperrect(min, max)

    def f(self, x, t):
        """Right-hand side of ODE system."""
        S, I, R = x
        dS = -(self.beta * I * S) / self.N
        dI = (self.beta * I * S) / self.N - self.gamma * I
        dR = self.gamma * I
        return np.array([dS, dI, dR])

    def vectorfield(self, gridsize):
        """2D vector field (S vs I)."""
        x, y = np.meshgrid(np.linspace(self.range.ll[0], self.range.tr[0], gridsize),
                           np.linspace(self.range.ll[1], self.range.tr[1], gridsize))
        u, v = self.f([x, y, 0], 0)[:2]   # only first 2 components
        pl.quiver(x, y, u, v, color='0.75', linewidth=2)
        return

class ODESolver:
    def __init__(self, model):
        self.dimension = model.dimension
        self.f = model.f

    def simulate(self, InitialState, TimeSeq, dt=0.01):
        """Simple Euler integrator."""
        StateSeq = np.zeros((len(TimeSeq), self.dimension))
        StateSeq[0] = InitialState
        for k in range(1, len(TimeSeq)):
            StateSeq[k] = StateSeq[k-1] + dt * self.f(StateSeq[k-1], TimeSeq[k-1])
        return StateSeq

    def plotPhase(self, TimeSeq, StateSeq, dim1, dim2, LegendSeq=[]):
        pl.plot(StateSeq[:, dim1], StateSeq[:, dim2], color='.2', linewidth=2)
        if LegendSeq:
            pl.legend(LegendSeq, loc='upper right', fontsize='x-large')

    def plotTraj(self, TimeSeq, StateSeq, LegendSeq=[]):
        pl.plot(TimeSeq, StateSeq, linewidth=2)
        if LegendSeq:
            pl.legend(LegendSeq, loc='upper right', fontsize='x-large')

# Parameters
beta = 0.33
gamma = 0.17
N = 100 
I0 = 0.1
g0 = 3
min = [-5, -5]
max = [5, 5]

# Build model and solver
model = ODE(beta, gamma, N, g0, min, max)
solver = ODESolver(model)

# Time grid
tseq = np.arange(0.0, 100, 0.01)

# Simulate
sseq = solver.simulate([(1 - I0) * N, I0 * N, 0], tseq, dt=0.01)

# Plot trajectories
solver.plotTraj(tseq, sseq, ('Susceptible ($S$)', 'Infected ($I$)', 'Recovered ($R$)'))

# Optional: phase portrait
# solver.plotPhase(tseq, sseq, 0, 1, ('S vs I',))
# model.vectorfield(20)

pl.show()
