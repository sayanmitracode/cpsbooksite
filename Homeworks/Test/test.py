import numpy as np
import matplotlib.pyplot as plt

# ========================================
# Parameters
# ========================================
dt = 0.01
T = 10.0
N = int(T / dt) + 1
t = np.linspace(0, T, N)
v = 1.0  # forward velocity

# ========================================
# 1) Reference trajectory
# ========================================
u_ref = 0.8 * np.sin(0.8 * t) + 0.4 * np.sin(2.2 * t)

x_ref = np.zeros((N, 3))  # [x, y, theta]
x_ref[0] = [0.0, 0.0, 0.0]

for k in range(N - 1):
    theta = x_ref[k, 2]
    xdot = np.array([v, theta, u_ref[k]])
    x_ref[k + 1] = x_ref[k] + dt * xdot

# ========================================
# 2) Closed-loop control with P-controller + noise
# ========================================
K = np.array([0.3, 0.2, 3.0])
x = np.zeros((N, 3))
x[0] = np.array([0.2, -0.5, 0.2])
u = np.zeros(N)

for k in range(N - 1):
    # add random noise proportional to current state
    err = x_ref[k] - x[k] + np.random.uniform(-0.1, 0.1, size=3) * x[k]
    u[k] = K.dot(err)
    theta = x[k, 2]
    xdot = np.array([v, theta, u[k]])
    x[k + 1] = x[k] + dt * xdot

# ========================================
# 3) Plot all results in one figure
# ========================================
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Linearized Dubins Car: Reference vs P-Control (with Noise)", fontsize=14)

# (1) Trajectories
axs[0, 0].plot(x_ref[:, 0], x_ref[:, 1], label="Reference Trajectory")
axs[0, 0].plot(x[:, 0], x[:, 1], label="Actual Trajectory (P-Control + Noise)")
axs[0, 0].set_xlabel("x")
axs[0, 0].set_ylabel("y")
axs[0, 0].legend()
axs[0, 0].set_title("Trajectories")
axs[0, 0].axis("equal")
axs[0, 0].grid(True)

# (2) Theta (heading)
axs[0, 1].plot(t, x_ref[:, 2], label="theta_ref")
axs[0, 1].plot(t, x[:, 2], label="theta_actual")
axs[0, 1].set_xlabel("time [s]")
axs[0, 1].set_ylabel("theta [rad]")
axs[0, 1].set_title("Heading over Time")
axs[0, 1].legend()
axs[0, 1].grid(True)

# (3) Control signals
axs[1, 0].plot(t, u_ref, label="u_ref (open-loop)")
axs[1, 0].plot(t, u, label="u_closed_loop (P-control + Noise)")
axs[1, 0].set_xlabel("time [s]")
axs[1, 0].set_ylabel("u (steering rate)")
axs[1, 0].set_title("Control Signals")
axs[1, 0].legend()
axs[1, 0].grid(True)

# (4) State errors (x_ref - x)
err_all = x_ref - x
axs[1, 1].plot(t, err_all[:, 0], label="x error")
axs[1, 1].plot(t, err_all[:, 1], label="y error")
axs[1, 1].plot(t, err_all[:, 2], label="theta error")
axs[1, 1].set_xlabel("time [s]")
axs[1, 1].set_ylabel("error")
axs[1, 1].set_title("State Tracking Errors")
axs[1, 1].legend()
axs[1, 1].grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# ========================================
# Summary
# ========================================
final_error = x_ref[-1] - x[-1]
print("Final state error (x_ref - x_actual):", final_error)
print("Gains K:", K)
