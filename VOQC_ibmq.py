from pyvoqc.voqc import VOQC
import os
from os.path import join, isfile
import time

def VOQC_optimize_nam(fn):
    circ = VOQC(fn)
    start = time.time()
    circ.optimize_nam()
    circ.optimize_ibm()
    t = time.time() - start
    return circ.total_gate_count(), t
    

if __name__ == "__main__":
    qasm_path = os.getcwd() + '/nam-benchmarks/'
    qasm_fns = [fn for fn in os.listdir(qasm_path) if isfile(join(qasm_path, fn)) and fn[-4:] == 'qasm']
    for fn in qasm_fns:
        r = VOQC_optimize_nam(qasm_path + fn)
        print(f"Optimization results of VOQC for {fn} on IBMQ gate set")
        print(f"{r[0]} gates after pass 'optimize_nam' and pass 'optimize_ibm' after {r[1]:.3f} seconds")