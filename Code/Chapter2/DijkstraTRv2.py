import matplotlib.pyplot as plt
import numpy as np
import random

def has_token(x, i, N):
    """Return True if process i has the token."""
    if i == 0:
        return x[0] == x[N - 1]
    else:
        return x[i] != x[i - 1]

def simulate_token_ring(N, K, T, delta_t):
    # All 0's initially 
    # x = [0] * N
    # Random initial condition
    x = random.choices(range(K), k=N)  # Initialize x with random values in [0, K-1]
    token_map = []  # List of lists: at each time step, which agents have the token
    times = []
    t = 0.0

    while t <= T:
        # Check who has token before update
        token_status = [has_token(x, i, N) for i in range(N)]
        token_map.append(token_status)
        times.append(t)

        # Apply update(i)
        i = int((t // delta_t) % N)
        if i == 0:
            if x[0] == x[N - 1]:
                x[0] = (x[0] + 1) % K
        else:
            if x[i] != x[i - 1]:
                x[i] = x[i - 1]

        t += delta_t

    return times, token_map

# Parameters
N = 20
K = 21
T = 20
delta_t = 1.0

# Run simulation
times, token_map = simulate_token_ring(N, K, T, delta_t)

# Plot: vertical dots for each agent at each time
plt.figure(figsize=(10, 5))
for t_idx, t in enumerate(times):
    for i in range(N):
        color = 'red' if token_map[t_idx][i] else 'black'
        plt.plot(t, i, 'o', color=color)

plt.xlabel("Time")
plt.ylabel("Process ID")
plt.yticks(range(N))
plt.title(f"Token Possession Over Time (N={N}, K={K})")
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
