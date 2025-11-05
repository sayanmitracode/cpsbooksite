import cvxpy as cp
import numpy as np

def solve_min_b(A, b_delta=0.1, b_min =-5, verbose=False):
    """
    Solve for the minimum scalar b and positive definite matrix P
    satisfying:
        PA + A^T P <= 2bP,  P >> 0
    """
    n = A.shape[0]
    P = cp.Variable((n, n), symmetric=True)
    b_max, _ = np.linalg.eig(A)
    b_max = max(np.real(b_max))
    #b = cp.Variable()  # scalar
    b_max = np.ceil(b_max * 100) / 100
    # print(f"b_max: {b_max}")
    b_return, P_return, prob_status  = None, None, None
    
    for b in np.arange(b_max+b_delta, b_min, -b_delta):
        # print(b)
        objective = cp.Minimize(0)

        # Important: write the LMI so it's affine in variables (b and P)
        expr = P @ A + A.T @ P - 2 * b * P  # This is affine in b, P

        constraints = [
            P >> 1e-3 * np.eye(n),  # P positive definite
            expr << 0               # LMI constraint
        ]

        prob = cp.Problem(objective, constraints)

        # Try available solvers
        try:
            prob.solve(solver=cp.SCS, verbose=verbose)
        except cp.SolverError:
            prob.solve(solver=cp.CVXOPT, verbose=verbose)

        if prob.status in ["optimal", "optimal_inaccurate"]:
            b_return, P_return, prob_status = b, P.value, prob.status

        if prob.status not in ["optimal", "optimal_inaccurate"]:
            return b_return, P_return, prob_status
        
    return b_return, P_return, prob_status



# Example
if __name__ == "__main__":
    np.random.seed(1)
    A = np.random.randn(3, 3)
    # A = np.eye(3)
    print(f"A:\n{A}")
    b_opt, P_opt, status = solve_min_b(A)
    print(f"Status: {status}")
    print(f"Optimal b: {b_opt}")
    print("P:\n", P_opt)
