import numpy as np
import matplotlib.pyplot as plt

# System matrices
A = np.array([[0, 1], [-1, -1]])
B = np.array([[0], [1]])

# Inputs
def u1(t):
    return 1.0 if t < 5 else -1.0

def u2(t):
    return 0.5 if t < 3 else 0.0

def u_zero(t):
    return 0.0

# RK4 stepper for dx/dt = A x + B u(t)
def rk4_step(x, t, dt, u_func):
    def f(x, t):
        return A @ x + B.flatten() * u_func(t)
    k1 = f(x, t)
    k2 = f(x + 0.5*dt*k1, t + 0.5*dt)
    k3 = f(x + 0.5*dt*k2, t + 0.5*dt)
    k4 = f(x + dt*k3, t + dt)
    return x + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

# Simulator
def simulate(x0, u_func, T=10, dt=0.01):
    steps = int(T/dt)
    t_vals = np.linspace(0, T, steps+1)
    traj = np.zeros((steps+1, len(x0)))
    traj[0] = x0
    x = np.array(x0, dtype=float)
    for k in range(steps):
        x = rk4_step(x, t_vals[k], dt, u_func)
        traj[k+1] = x
    return t_vals, traj

# Simulation horizon
T = 10

# Set up figure
fig, axs = plt.subplots(3, 2, figsize=(12,12))

# --- Row 1: Input signals ---
t_vals = np.linspace(0, T, 1000)
axs[0,0].plot(t_vals, [u1(t) for t in t_vals], 'r', label="u1(t)")
axs[0,0].plot(t_vals, [u2(t) for t in t_vals], 'b', label="u2(t)")
axs[0,0].set_title("Discontinuous Inputs u1, u2")
axs[0,0].set_xlabel("t"); axs[0,0].set_ylabel("u(t)")
axs[0,0].legend(); axs[0,0].grid()

a1, a2 = 1.5, -1.0
axs[0,1].plot(t_vals, [a1*u1(t)+a2*u2(t) for t in t_vals], 'k', label="a1*u1 + a2*u2")
axs[0,1].set_title("Combined Input")
axs[0,1].set_xlabel("t"); axs[0,1].set_ylabel("u(t)")
axs[0,1].legend(); axs[0,1].grid()

# --- Row 2: Continuity & dependence ---
t, traj = simulate([1, 0], u1)
axs[1,0].plot(t, traj[:,0], label="x1(t)")
axs[1,0].plot(t, traj[:,1], label="x2(t)")
axs[1,0].set_title("Continuity with Discontinuous Input")
axs[1,0].set_xlabel("t"); axs[1,0].set_ylabel("states")
axs[1,0].legend(); axs[1,0].grid()

t, traj1 = simulate([1, 0], u_zero)
t, traj2 = simulate([1.2, 0], u_zero)
axs[1,1].plot(t, traj1[:,0], label="x0=(1,0)")
axs[1,1].plot(t, traj2[:,0], label="x0=(1.2,0)")
axs[1,1].set_title("Continuous Dependence on Initial State")
axs[1,1].set_xlabel("t"); axs[1,1].set_ylabel("x1(t)")
axs[1,1].legend(); axs[1,1].grid()

# --- Row 3: Superposition & decomposition ---
x01, x02 = np.array([1,0]), np.array([0,1])
u_combo = lambda t: a1*u1(t) + a2*u2(t)
t, x_combo = simulate(a1*x01+a2*x02, u_combo)
t, x1 = simulate(x01, u1)
t, x2 = simulate(x02, u2)
axs[2,0].plot(t, x_combo[:,0], 'k', linewidth=2, label="Combo traj")
axs[2,0].plot(t, a1*x1[:,0], 'r--', label="a1 * x1(t)")
axs[2,0].plot(t, a2*x2[:,0], 'b--', label="a2 * x2(t)")
axs[2,0].plot(t, (a1*x1[:,0] + a2*x2[:,0]), 'g:', linewidth=2, label="Sum of parts")
axs[2,0].set_title("Superposition Principle")
axs[2,0].set_xlabel("t"); axs[2,0].set_ylabel("x1(t)")
axs[2,0].legend(); axs[2,0].grid()

x0 = np.array([1,0])
t, x_full = simulate(x0, u1)
t, x_h = simulate(x0, u_zero)
t, x_f = simulate([0,0], u1)
axs[2,1].plot(t, x_full[:,0], 'k', linewidth=2, label="Full solution")
axs[2,1].plot(t, x_h[:,0], 'r--', label="Homogeneous (IC only)")
axs[2,1].plot(t, x_f[:,0], 'b--', label="Forced (input only)")
axs[2,1].plot(t, (x_h+x_f)[:,0], 'g:', linewidth=2, label="Sum of parts")
axs[2,1].set_title("Decomposition Property")
axs[2,1].set_xlabel("t"); axs[2,1].set_ylabel("x1(t)")
axs[2,1].legend(); axs[2,1].grid()

plt.tight_layout()
plt.show()
