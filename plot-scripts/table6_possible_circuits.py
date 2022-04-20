# This file requires Python 3.8+
from math import factorial, prod
from collections import  defaultdict
from itertools import product

def n_parameter_expressions(m, p):
    """
    the parameter expressions are p_i, p_i + p_i, and p_i + p_j.

    we only allow each parameter to be used once.

    this returns the number of ways to assign p parameter expressions from m input parameters
    """
    assert m >= 0 and p >= 0, (m, p)
    if p == 0:
        return 1
    ways = 0
    if m >= 1:
        ways += 2 * m * n_parameter_expressions(m - 1, p - 1) # using one parameter
    if m >= 2:
        ways += m * (m - 1) / 2 * n_parameter_expressions(m - 2, p - 1) # using two parameters
    assert ways == int(ways)
    return int(ways)


# gate set is a list of gates, given as (n_qubits, n_parameters)

Nam = [
    (1, 0), # H
    (1, 0), # X
    (1, 1), # R_Z
    (2, 0), # CNOT
]

IBM = [
    (1, 1), # U1
    (1, 2), # U2
    (1, 3), # U3
    (2, 0), # CNOT
]

# OldRigetti = [
#     (1, 1), # R_X k=1
#     (1, 1), # R_Z
#     (2, 0), # CZ
# ]

Rigetti = [
    (1, 0), # R_X k=1
    (1, 0), # R_X k=2
    (1, 0), # R_X k=3
    (1, 1), # R_Z
    (2, 0), # CZ
]

gate_set = IBM
q = 3 # number of qubits
m = 4 # number of parameters


n_gates_by_arity = defaultdict(int)
for g in gate_set:
    n_gates_by_arity[g] += 1
arities = sorted(n_gates_by_arity.keys())

circuits_by_n = [] # circuits_by_n[n] is number of circuits with exactly n gates
for n in range(10):
    C = 0
    for ks in product(range(n + 1), repeat=len(arities)):
        if sum(ks) == n:
            p = sum(k * a[1] for k, a in zip(ks, arities))
            C += (
                n_parameter_expressions(m, p) * # ways to assign parameter expressions to p parameters
                prod(n_gates_by_arity[a] ** k for k, a in zip(ks, arities)) * # options for gate types
                prod(((factorial(q) / factorial(q - a[0])) if q >= a[0] else 0) ** k for k, a in zip(ks, arities)) * # options for qubits
                factorial(n) / prod(factorial(k) for k in ks) # sequence ordering
            )
    assert int(C) == C
    circuits_by_n.append(int(C))

print(circuits_by_n)
print('\n\nn number of circuits with at most n gates:')
for i in range(len(circuits_by_n)):
    print(f'{i} {sum(circuits_by_n[:i + 1]):,}')
