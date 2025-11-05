import cvxpy as cp
import numpy as np
from solver import solve_min_b
from tqdm import tqdm

# ========================================
# Parameters
# ========================================
dt = 0.1
T = 10.0
N = int(T / dt) + 1
t = np.linspace(0, T, N)
v = 1.0  # forward velocity
theta_ref = np.deg2rad(30)
np.random.seed(1)

# ========================================
# 1) Reference trajectory
# ========================================
u_ref = 0.8 * np.sin(0.8 * t) + 0.4 * np.sin(2.2 * t)

x_lead = np.zeros((N, 3))  # [x, y, theta]
x_lead[0] = [0.0, 0.0, 0.0]

# A = np.array([[0, 0, -v * np.sin(theta_ref)],
#               [0, 0,  v * np.cos(theta_ref)],
#               [0, 0, 0]])

# B = np.array([[0],
#               [0],
#               [1]])

# for k in range(N - 1):
#     xdot = A @ x_lead[k] + B.flatten() * u_ref[k]
#     x_lead[k + 1] = x_lead[k] + dt * xdot

for k in range(N - 1):
    theta = x_lead[k, 2]
    xdot = np.array([v*np.cos(theta), v*np.sin(theta), 0 + u_ref[k]])
    x_lead[k + 1] = x_lead[k] + dt * xdot

# ========================================
# 2) Closed-loop control with P-controller + noise
# ========================================
Kxl, Kxu= -0.006, 0.006
Kyl, Kyu= -0.12, 0.12
Kzl, Kzu= -0.17, 0.17
noi_x = np.random.uniform(Kxl, Kxu, size=(1000,1)) 
noi_y = np.random.uniform(Kyl, Kyu, size=(1000,1)) 
noi_z = np.random.uniform(Kzl, Kzu, size=(1000,1)) 
noi = np.hstack((noi_x, noi_y, noi_z))

K = np.array([0.6, 0.4, 3.0])

# Define multiple initial states for the follower
initial_states = [
    np.array([0.2, -0.5, 0.2]),  # Original initial state
    np.array([0.5, -0.3, 0.1]),
    np.array([-0.2, 0.4, -0.1])
]

# Store all follower trajectories
x_fol_list = []
u_list = []

for init_state in initial_states:
    x_fol = np.zeros((N, 3))
    x_fol[0] = init_state
    u = np.zeros(N)

    for k in range(N - 1):
        theta = x_fol[k, 2]
        u[k] = u_ref[k] - K.dot(-x_lead[k] + x_fol[k]) + noi[k].dot(-x_lead[k] + x_fol[k])
        xdot = np.array([v * np.cos(theta), v * np.sin(theta), u[k]])
        x_fol[k + 1] = x_fol[k] + dt * xdot

    x_fol_list.append(x_fol)
    u_list.append(u)


# ========================================
# 3) Error analysis
# ========================================
Df = np.zeros((N, 3, 3))
Df[:, 0, 2] = -v * np.sin(x_lead[:,2])
Df[:, 1, 2] = v * np.cos(x_lead[:,2])

Dg = np.zeros((N, 3, 3))
Dg[:, 2, :] = -K

De = np.zeros((N, 3, 3))
De[:, 2, :] = np.array([Kxl, Kyl, Kzl])[None, :]

Ddyn = Df + Dg + De
b_list, P_list, status_list = [], [], []

for k in tqdm(range(N), desc="Processing iterations"):
    b_opt, P_opt, status = solve_min_b(Ddyn[k], b_min=-5, verbose=False)
    b_list.append(b_opt)
    P_list.append(P_opt)
    status_list.append(status)

x_e_list = []  # Store error trajectories for all followers
x_e_Norm_list = []  # Store Lyapunov norm values for all followers

x_e_0_norm_max = 0

for x_fol in x_fol_list:
    x_e = -x_lead + x_fol  # Compute error for this follower
    x_e_list.append(x_e)

    x_e_Norm = np.zeros(N)
    x_e_0_norm = np.sqrt(x_e[0].T @ P_list[0] @ x_e[0])
    x_e_0_norm_max = np.max([x_e_0_norm_max, x_e_0_norm])  # Find the maximum initial norm

    for k in range(N):
        x_e_Norm[k] = np.sqrt(x_e[k].T @ P_list[0] @ x_e[k])
    x_e_Norm_list.append(x_e_Norm)

Upper_Norm = np.zeros(N)
acc_b = 0.0
for k in range(N):
    acc_b += b_list[k] * dt
    Upper_Norm[k] = x_e_0_norm_max * np.exp(acc_b)

# ========================================
# 4) Plot all results in one figure
# ========================================
import matplotlib.pyplot as plt
fig, axs = plt.subplots(3, 3, figsize=(10, 10))
fig.suptitle("Dubins Car: Leader & Follower (Pose Noise)", fontsize=14)

# (1) Trajectories
axs[0, 0].plot(x_lead[:, 0], x_lead[:, 1], label="Leader Traj")
#axs[0, 0].plot(x_fol[:, 0], x_fol[:, 1], label="Follower Traj")
for i, x_fol in enumerate(x_fol_list):
    axs[0, 0].plot(x_fol[:, 0], x_fol[:, 1], label=f"Follower {i+1} Traj")
axs[0, 0].set_xlabel("x")
axs[0, 0].set_ylabel("y")
axs[0, 0].legend()
axs[0, 0].set_title("Trajectories")
axs[0, 0].axis("equal")
axs[0, 0].grid(True)

# (2) Theta (heading)
axs[0, 1].plot(t, x_lead[:, 2], label="Leader Theta")
# axs[0, 1].plot(t, x_fol[:, 2], label="Follower Theta")
for i, x_fol in enumerate(x_fol_list):
    axs[0, 1].plot(t, x_fol[:, 2], label=f"Follower {i+1} Theta")
axs[0, 1].set_xlabel("time [s]")
axs[0, 1].set_ylabel("theta [rad]")
axs[0, 1].set_title("Heading over Time")
axs[0, 1].legend()
axs[0, 1].grid(True)

# (3) Control signals
axs[0, 2].plot(t, u_ref, label="u_ref (Leader)")
# axs[0, 2].plot(t, u, label="u (Follower)")
for i, u_fol in enumerate(u_list):
    axs[0, 2].plot(t, u_fol, label=f"u (Follower {i+1})")
axs[0, 2].set_xlabel("time [s]")
axs[0, 2].set_ylabel("u (steering rate)")
axs[0, 2].set_title("Control Signals")
axs[0, 2].legend()
axs[0, 2].grid(True)

# (4) State errors (x_ref - x)
custom_colors = ["orange", "green", "red"]  # Use the same color cycle as trajectories

# x-dimension error
for i, x_e in enumerate(x_e_list):
    axs[1, 0].plot(t, x_e[:, 0], label=f"Follower {i+1} x error", color=custom_colors[i])
axs[1, 0].set_xlabel("time [s]")
axs[1, 0].set_ylabel("x error")
axs[1, 0].set_title("State Tracking Errors: x-dimension")
axs[1, 0].legend()
axs[1, 0].grid(True)

# y-dimension error
for i, x_e in enumerate(x_e_list):
    axs[1, 1].plot(t, x_e[:, 1], label=f"Follower {i+1} y error", color=custom_colors[i])
axs[1, 1].set_xlabel("time [s]")
axs[1, 1].set_ylabel("y error")
axs[1, 1].set_title("State Tracking Errors: y-dimension")
axs[1, 1].legend()
axs[1, 1].grid(True)

# theta-dimension error
for i, x_e in enumerate(x_e_list):
    axs[1, 2].plot(t, x_e[:, 2], label=f"Follower {i+1} theta error", color=custom_colors[i])
axs[1, 2].set_xlabel("time [s]")
axs[1, 2].set_ylabel("theta error")
axs[1, 2].set_title("State Tracking Errors: theta-dimension")
axs[1, 2].legend()
axs[1, 2].grid(True)

# (5) Norm of errors and upper bound
# axs[2, 0].plot(t, x_e_Norm[:], label="actual Lyp value")
for i, x_e_Norm in enumerate(x_e_Norm_list):
    axs[2, 0].plot(t, x_e_Norm[:], label=f"Follower {i+1} actual Lyp value", color=custom_colors[i])
axs[2, 0].plot(t, Upper_Norm[:], label="Upper Lyp value", linestyle='--', color = 'blue')
axs[2, 0].set_xlabel("time [s]")
axs[2, 0].set_ylabel("Norm Value")
axs[2, 0].set_title("")
axs[2, 0].legend()
axs[2, 0].grid(True)



plt.show()
