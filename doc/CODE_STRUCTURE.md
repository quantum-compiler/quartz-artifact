This file documents the organization of our artifact code repo.

In `src/python/verifier/gates.py`
* methods for constructing a matrix representation for different quantum gates

In `src/python/verifier/verifier.py`
* `search_phase_factor_to_check_equivalence`: search the phase factor between two quantum circuits to be verified
* `equivalent`: use the Z3 SMT solver to examine the equivalence of two quantum circuits
* `find_equivalences`: to do

In `src/quartz/context/context.h`
* `class Context`: define the execution context for a quantum device, including the set of gates supported by the processor

In `src/quartz/parser/qasm_parser.h`
* `class QASMParser`: parse an input QASM file to Quartz's DAG representation
* 
