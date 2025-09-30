import numpy as np
import matplotlib.pyplot as plt

# System matrices
A = np.array([[0, 1], [-1, -1]])
B = np.array([[0], [1]])

# Input function u1
def u1(t):
    return 1.0 if t < 5 else -1.0

# RK4 stepper
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

# --- Phase portrait for multiple initial conditions ---
initial_conditions = [
    [-2, -2], [-2, 0], [-2, 2],
    [ 0, -2], [ 0, 0], [ 0, 2],
    [ 2, -2], [ 2, 0], [ 2, 2]
]

plt.figure(figsize=(7,7))

for x0 in initial_conditions:
    t, traj = simulate(x0, u1, T=10)
    plt.plot(traj[:,0], traj[:,1], label=f"x0={x0}")

# Mark initial points
for x0 in initial_conditions:
    plt.plot(x0[0], x0[1], 'ko')  # black dots

plt.title("Phase Portrait with input u1(t)")
plt.xlabel("x1")
plt.ylabel("x2")
plt.grid(True)
plt.axis("equal")
plt.legend(loc='upper right', fontsize='small')
plt.show()
