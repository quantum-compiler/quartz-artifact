from pytket.qasm import circuit_from_qasm_str
from pytket.passes import FullPeepholeOptimise
from pytket.passes import RebaseQuil
import os
from os.path import join, isfile
import time

def rewrite_ccz(q0, q1, q2) -> str:
    return f"cx q[{q1}], q[{q2}];\n"    + \
           f"u1(-0.25*pi) q[{q2}];\n"      + \
           f"cx q[{q0}], q[{q2}];\n"    + \
           f"u1(0.25*pi) q[{q2}];\n"       + \
           f"cx q[{q1}], q[{q2}];\n"    + \
           f"u1(-0.25*pi) q[{q2}];\n"      + \
           f"cx q[{q0}], q[{q2}];\n"    + \
           f"cx q[{q0}], q[{q1}];\n"    + \
           f"u1(-0.25*pi) q[{q1}];\n"      + \
           f"cx q[{q0}], q[{q1}];\n"    + \
           f"u1(0.25*pi) q[{q0}];\n"       + \
           f"u1(0.25*pi) q[{q1}];\n"       + \
           f"u1(0.25*pi) q[{q2}];\n"


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


if __name__ == "__main__":
    qasm_path = os.getcwd() + '/nam-benchmarks/'
    qasm_fns = [fn for fn in os.listdir(qasm_path) if isfile(join(qasm_path, fn)) and fn[-4:] == 'qasm']
    qasm_full_paths = [qasm_path + fn for fn in qasm_fns]
    f = FullPeepholeOptimise()
    r = RebaseQuil()
    
    for i in range(len(qasm_fns)):
        full_path = qasm_full_paths[i]
        c = circuit_from_qasm_str(replace_ccz(full_path))
        start = time.time()
        f.apply(c)
        r.apply(c)
        t = time.time() - start
        print(f"Optimization results of tket for {qasm_fns[i]} on Rigetti gate set")
        print(f"{c.n_gates} gates after {t:.3f} seconds")