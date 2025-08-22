import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Lorenz system parameters
sigma = 10.0
beta = 8.0 / 3.0
rho = 28.0

# Time discretization
dt = 0.01
steps = 10000

# Initialize arrays
xs = np.empty(steps)
ys = np.empty(steps)
zs = np.empty(steps)

# Initial condition
xs[0], ys[0], zs[0] = (1.0, 1.0, 1.0)

# Euler integration
for i in range(1, steps):
    x, y, z = xs[i - 1], ys[i - 1], zs[i - 1]
    xs[i] = x + sigma * (y - x) * dt
    ys[i] = y + (x * (rho - z) - y) * dt
    zs[i] = z + (x * y - beta * z) * dt

# Plotting
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot(xs, ys, zs, lw=0.5)
ax.set_title("Lorenz Attractor")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()
