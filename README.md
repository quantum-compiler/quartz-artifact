# Artifacts for Quartz

## Getting Started

Install dependencies:

```shell
pip install z3-solver
```

## Table 2: Evaluating the Quartz Generator and Verifier

Run the following script:

```shell
bash run_table2.sh
```

In the output of the script, lines starting with `***` indicate the numbers used in Table 2. We expect the numbers to
differ a little from the numbers in the submission due to floating-point errors.

## Characteristics and the Number of Transformations for the Three Gate Sets

Run the following script:

```shell
bash gen_ecc_set.sh
```

In the output, `*** ch(...) = ...` denotes the characteristics for each gate set.

`*** Number of transformations of ... = ...` denotes the number of transformations for each gate set. We expect the
numbers of transformations to differ a little from the numbers in the submission due to floating-point errors.

The generated ECC Sets are stored in Json files with file name formatted like
this: `{Gate set name}_{number of gates}_{number_of qubits}_complete_ECC_set.json`.

## Table 3: Comparing Quartz with existing quantum circuit optimizers on the Nam gate set {𝑅𝑧(𝜆),𝑋,𝐻,𝐶𝑁𝑂𝑇}

### The results of Qiskit

### The results of Nam

We refer the results of Nam on Nam's gate set to the paper "A verified optimizer for Quantum circuits" (https://dl.acm.org/doi/10.1145/3434318). Specifically, the results can be found at Table 2, column "Nam(H)" in this paper.

### The results of VOQC

### The results of Quartz


## Table 4: Comparing Quartz with existing circuit optimizers on the IBM gate set

### The results of Qiskit

### The results of tket
### The results of VOQC
### The results of Quartz

## Table 5: Comparing Quartz with Quilc and t|ket⟩ on the Rigetti gate set (𝑅𝑥 (𝑘𝜋/2)(𝑘 ∈Z),𝑅𝑧(𝜆),𝐶𝑍)

### The results of tket
### The results of VOQC
### The results of Quartz