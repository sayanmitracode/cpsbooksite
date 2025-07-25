# This is a simulation of Synchronous version of Dijkstra's Token Ring algorithm.
# It simulates a token ring with N processes, each having a state variable x[i].
# In each round, each process with a token updates its state; processes without token do nothing
# Sayan Mitra, 2025

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
    x = random.choices(range(K), k=N)
    token_map = []
    times = []
    t = 0.0

    while t <= T:
        x_old = x.copy()
        times.append(t)
        token_map.append([has_token(x_old, i, N) for i in range(N)])

        # Update x based on x_old
        for i in range(N):
            if has_token(x_old, i, N):
                if i == 0:
                    x[i] = (x_old[0] + 1) % K
                else:
                    x[i] = x_old[i - 1]

        t += delta_t

    return times, token_map

# Parameters
N = 20
K = 21
T = 20
delta_t = 1.0

# Run simulation
times, token_map = simulate_token_ring(N, K, T, delta_t)

# Plot: red = has token, black = doesn't
plt.figure(figsize=(12, 6))
for t_idx, t in enumerate(times):
    for i in range(N):
        color = 'red' if token_map[t_idx][i] else 'black'
        plt.plot(t, i, 'o', color=color)

plt.xlabel("Time")
plt.ylabel("Process ID")
plt.yticks(range(N))
plt.title(f"Synchronous Dijkstra Token Ring (N={N}, K={K})")
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
