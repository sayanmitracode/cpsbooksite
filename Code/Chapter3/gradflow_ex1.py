import numpy as np
import matplotlib.pyplot as plt

# === Generate synthetic data ===
np.random.seed(0)
n = 20
# x = np.linspace(0, 5, n)
# y = 2.5 * x + np.random.normal(0, 1, n)   # true slope = 2.5

x = np.linspace(0, 500, n)   # much larger x values -> huge A
# y = 2.5 * x + np.random.normal(0, 100, n)
y = 0.5 * x**2 + np.random.normal(0, 0.5, n)   # nonlinear relationship with small noise


# === Compute constants A, B, and optimum ===
A = np.sum(x**2)
B = np.sum(x * y)
theta_star = B / A   # analytical minimizer

# === Gradient descent iterations ===
eta = 0.001   # learning rate
steps = 200
theta_gd = [0.0]   # start from theta(0)=0
for k in range(steps):
    grad = A * theta_gd[-1] - B
    theta_next = theta_gd[-1] - eta * grad
    theta_gd.append(theta_next)

# === Gradient flow (continuous-time) ===
k_vals = np.arange(steps+1)
t_vals = eta * k_vals  # rescale time to match GD iterations
theta0 = 0.0
theta_flow = theta_star + (theta0 - theta_star) * np.exp(-A * t_vals)

# === Errors ===
error_gd = np.array(theta_gd) - theta_star
error_flow = theta_flow - theta_star
theoretical_decay = (theta0 - theta_star) * np.exp(-A * eta * k_vals)

# === Create figure with 2x2 layout ===
fig, axs = plt.subplots(2, 2, figsize=(12,10))

# (1) Theta convergence
axs[0,0].plot(t_vals/eta, theta_flow, 'r-', label="Gradient Flow")
axs[0,0].plot(k_vals, theta_gd, 'bo-', markersize=3, label="Gradient Descent")
axs[0,0].axhline(theta_star, color='k', linestyle='--', label=r"$\theta^*$")
axs[0,0].set_xlabel("Iterations (k)")
axs[0,0].set_ylabel(r"$\theta$")
axs[0,0].set_title("Theta Convergence")
axs[0,0].legend()
axs[0,0].grid(True)

# (2) Error decay (log scale)
axs[0,1].plot(k_vals, np.abs(error_gd), 'bo-', markersize=3, label="GD Error |θ-θ*|")
axs[0,1].plot(t_vals/eta, np.abs(error_flow), 'r-', label="Flow Error |θ-θ*|")
axs[0,1].plot(k_vals, np.abs(theoretical_decay), 'g--', label="Theoretical exp decay")
axs[0,1].set_yscale("log")
axs[0,1].set_xlabel("Iterations (k)")
axs[0,1].set_ylabel(r"|θ - θ*| (log scale)")
axs[0,1].set_title("Error Decay (Exponential)")
axs[0,1].legend()
axs[0,1].grid(True, which="both")

# (3) Data with evolving line fits (selected iterations)
axs[1,0].scatter(x, y, color='black', label="Data")
for k in [0, 1, 5, 20, 100, 200]:
    y_pred = theta_gd[k] * x
    axs[1,0].plot(x, y_pred, label=f"θ(k={k})")
axs[1,0].set_xlabel("x")
axs[1,0].set_ylabel("y")
axs[1,0].set_title("Line Fit Evolution (Selected Iterations)")
axs[1,0].legend()

# (4) Final fitted line vs data
axs[1,1].scatter(x, y, color='black', label="Data")
axs[1,1].plot(x, theta_gd[-1]*x, 'b-', label=f"Final GD fit θ={theta_gd[-1]:.2f}")
axs[1,1].plot(x, theta_star*x, 'r--', label=f"Optimal fit θ*={theta_star:.2f}")
axs[1,1].set_xlabel("x")
axs[1,1].set_ylabel("y")
axs[1,1].set_title("Final Learned Line vs Optimal Line")
axs[1,1].legend()

plt.tight_layout()
plt.show()
