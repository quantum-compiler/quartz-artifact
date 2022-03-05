from qiskit import QuantumCircuit, transpile
import os
from os.path import join, isfile
from concurrent.futures import ProcessPoolExecutor
import time

def rewrite_ccz(q0, q1, q2) -> str:
    return f"cx q[{q1}], q[{q2}];\n"    + \
           f"rz(-0.25*pi) q[{q2}];\n"      + \
           f"cx q[{q0}], q[{q2}];\n"    + \
           f"rz(0.25*pi) q[{q2}];\n"       + \
           f"cx q[{q1}], q[{q2}];\n"    + \
           f"rz(-0.25*pi) q[{q2}];\n"      + \
           f"cx q[{q0}], q[{q2}];\n"    + \
           f"cx q[{q0}], q[{q1}];\n"    + \
           f"rz(-0.25*pi) q[{q1}];\n"      + \
           f"cx q[{q0}], q[{q1}];\n"    + \
           f"rz(0.25*pi) q[{q0}];\n"       + \
           f"rz(0.25*pi) q[{q1}];\n"       + \
           f"rz(0.25*pi) q[{q2}];\n"


def replace_ccz(fn) -> str:
    qasm_str = ''
    with open(fn, "r") as f:
        for l in f:
            if l[:3] == 'ccz':
                qs = []
                strs = l.split('[')[1:]
                for s in strs:
                    qs.append(int(s[:s.find(']')]))
                qasm_str += rewrite_ccz(*qs)
            else:
                qasm_str += l
    return qasm_str



def qiskit_optimize_nam(fn):
    qasm_str = replace_ccz(fn)
    circ = QuantumCircuit.from_qasm_str(qasm_str)
    gate_cnts = []
    optimize_times = []
    for i in range(3):
        start = time.time()
        optimized_circ = transpile(circ, basis_gates=['rz', 'cx', 'h', 'x'], optimization_level=i)
        optimize_times.append(time.time() - start)
        count_dict = optimized_circ.count_ops()
        gate_cnts.append(sum([count_dict[k] for k in count_dict]))
    return gate_cnts, optimize_times

if __name__ == "__main__":
    qasm_path = os.getcwd() + '/nam-benchmarks/'
    qasm_fns = [fn for fn in os.listdir(qasm_path) if isfile(join(qasm_path, fn)) and fn[-4:] == 'qasm']
    qasm_full_paths = [qasm_path + fn for fn in qasm_fns]
    with ProcessPoolExecutor(max_workers=32) as executor:
        results = executor.map(qiskit_optimize_nam, qasm_full_paths)
    i = 0
    for r in results:
        fn = qasm_fns[i]
        i += 1
        print(f"Optimization results of Qiskit for {fn} on Nam's gate set")
        for j in range(3):
            print(f"{r[0][j]} gates after level {j + 1} optimization after {r[1][j]:.3f} seconds")