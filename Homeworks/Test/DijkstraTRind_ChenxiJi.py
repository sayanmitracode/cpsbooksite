"""
Supporting material for the book
Verifying Cyberphysical Systems, by Sayan Mitra

Partial Python program for Checking inductive invariant of
Dijkstra's token ring algorithm for Mutual Exclusion 
Automaton name in the book DijkstrTR

:authors:
    - Chiao Hsieh
    - Sayan Mitra
"""

from z3 import Int, And, Or, Not, Implies, Solver, AtMost, AtLeast
import z3

# Choose a value for the number of processes; try with different values
N = 16
# Choose a value for the maximum value taken by each process
# K has to be greater than N; try different values
K = 32


def bounds(x_list):
    """
    Generate a Z3 Boolean expression that bounds each variable in [0, K)
    :param x_list: list of Z3 variables
    :return: Z3 Boolean expression bounding all variables
    """
    bounds_list=[]
    for i in range(0,N):
        con1=(x_list[i]>=0)
        con2=(x_list[i]<K)
        bounds_list.append(And(con1,con2))
    return And(bounds_list)


def has_token(x_list, j):
    """
    Generate a Z3 Boolean expression that represents whether P_j holds the token
    :param x_list: list of Z3 variables
    :param j: index of P_j
    :return: Z3 Boolean expression that if true then P_j is holding the token
    """
    con1=And(j==0,x_list[0]==x_list[N-1])
    con2=And(Not(j==0),Not(x_list[j]==x_list[j-1]))
    return Or(con1,con2)


def legal_config(x_list):
    """
    Generate a Z3 Boolean expression that represents whether the system is in a legal configuration
    :param x_list: list of Z3 variables
    :return: Z3 Boolean expression that if true then the system is in legal configuration
    """
    # Do not change
    args = [has_token(x_list, i) for i in range(0, N)]
    return And(AtMost(args + [1]), AtLeast(args + [1]))


def transition_relation(old_x_list, new_x_list):
    """
    Generate a Z3 Boolean expression representing transition
    :param old_x_list: variables before transition
    :param new_x_list: variables after transition
    :return: Z3 Boolean expression that when true means the old state can transit to the new state
    """
    tran_list=[]
    con1=has_token(old_x_list,0)
    con2=(new_x_list[0]==(old_x_list[0]+1)%K)
    con3=(new_x_list[0]==old_x_list[0])
    tran_list.append(Or(And(con1,con2),And(Not(con1),con3)))

    for i in range(1,N):
        con1=has_token(old_x_list,i)
        con2=(new_x_list[i]==old_x_list[i-1])
        con3=(new_x_list[i]==old_x_list[i])
        tran_list.append(Or(And(con1,con2),And(Not(con1),con3)))
    return And(tran_list)


def invariant(x_list):
    """
    Generate a Z3 Boolean expression representing invariant
    :param x_list: list of Z3 variables
    :return: Z3 Boolean expression of invariant
    """
    # Do not change
    return legal_config(x_list)


def prove(conjecture):
    # Do not change
    # Setting up solver
    s = Solver()
    # s.set("sat.cardinality.solver", True)  # Some options to speed up the solver

    s.add(Not(conjecture))  # Check unsat of negation for checking validity
    result = s.check()
    if result == z3.sat:
        print("Given formula is not valid.")
        print("Counter example: \n", s.model())
    elif result == z3.unsat:
        print("Given formula is valid.")
    else:  # result == z3.unknown
        print("Inconclusive. Z3 cannot solve with given options.")


def main():
    # 1. Create a list of z3 Int variables called prestate which is [x[0], x[1], x[2],....,x[15]]
    # use the range() function in Python and the parameter N
    # do not hardcode the list explicitly
    prestate = [Int("x["+str(i)+"]") for i in range(0,N)]
    # 2. create a list of z3 Int variables called poststate which is [x'[0], x'[1], x'[2],....,x'[N-1]]
    poststate = [Int("x'["+str(i)+"]") for i in range(0,N)] 

    # Do not change
    # Defines init as prestate that is legal
    init = legal_config(prestate)

    # 3. Write the base_case predicate using the Implies() function of z3
    base_case = Implies(And(legal_config(prestate),bounds(prestate)),And(legal_config(prestate),bounds(prestate)))

    # 4. Write the induction step predicate using the Implies() function of z3
    # prestate and poststate and transition_relation
    ind_case = Implies(And(legal_config(prestate),bounds(prestate),transition_relation(prestate,poststate)),And(legal_config(poststate),bounds(poststate)))
    
    # Do not change
    print("## Proving base case:")
    prove(base_case)
    print("## Proving induction case")
    prove(ind_case)


if __name__ == "__main__":
    main()

