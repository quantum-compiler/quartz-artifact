from pyquil.api import get_qc
from pyquil.gates import CNOT, H, RZ, X
import os
from os.path import join, isfile
import time
from pyquil.quil import Program
import numpy as np

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



def construct_program(fn):
    qasm_str = replace_ccz(fn)
    p = Program()
    qasm_cmds = qasm_str.split('\n')
    qubits_num_cmd = qasm_cmds[2]
    qubits_num = int(qubits_num_cmd[qubits_num_cmd.find('[')+1:qubits_num_cmd.find(']')])
    if qubits_num > 30:
        print("No support for circuits with more than 30 qubits")
        return p
    for cmd in qasm_cmds:
        if cmd == '':
            continue
        if cmd[0] == 'h':
            qubit = int(cmd[cmd.find('[')+1: cmd.find(']')])
            p += H(qubit)
        if cmd[0] == 'x':
            qubit = int(cmd[cmd.find('[')+1: cmd.find(']')])
            p += X(qubit)
        if cmd[0] == 'r':
            qubit = int(cmd[cmd.find('[')+1: cmd.find(']')])
            f = float(cmd[cmd.find('(')+1: cmd.find('*')])
            p += RZ(f * np.pi, qubit)
        if cmd[0] == 'c':
            qubit_0 = int(cmd[cmd.find('[')+1: cmd.find(']')])
            cmd = cmd[cmd.find(','):]
            qubit_1 = int(cmd[cmd.find('[')+1: cmd.find(']')])
            p += CNOT(qubit_0, qubit_1)
    return p


if __name__ == "__main__":
    qc = get_qc("30q-pyqvm", compiler_timeout=10000)
    qasm_path = os.getcwd() + '/nam-benchmarks/'
    qasm_fns = [fn for fn in os.listdir(qasm_path) if isfile(join(qasm_path, fn)) and fn[-4:] == 'qasm']
    for fn in qasm_fns:
        p = construct_program(qasm_path + fn)
        start = time.time()
        eq = qc.compile(p)
        t = time.time() - start
        gate_cnt = len(str(eq).split('\n')) - 2
        print(f"Optimization results of pyQuil for {fn} on Rigetti gate set")
        print(f"{gate_cnt} gates after {t:.3f} seconds")