# Artifact for Quartz

[![DOI](https://zenodo.org/badge/464661620.svg)](https://zenodo.org/badge/latestdoi/464661620)

## Getting Started

### Hardware Requirements

We recommend running the artifact on an m6i.32xlarge AWS instance. Although it can also run on laptops with >= 256 GB memory, it will take a significantly longer time to run.

### Installation

We provide the following two approaches to install the artifact.

#### 1. Install from AMI

To facilitate the artifact evaluation of our submission, we provide an Amazon Machine Image (AMI) of Quartz with all dependencies pre-installed. Our AMI instance ID is ami-09ac48ad04d42cb72. To log in to the instance, the username and password are both `pldi22ae`.

#### 2. Install from source code

- Make sure you have CMake (https://cmake.org/) with version >= 3.16.

- Install the Z3 Theorem Prover (https://github.com/Z3Prover/z3):
  ```shell
  pip install z3-solver
  ```
  Our evaluation uses Z3 4.8.14.

- Run CMake:
  ```shell
  bash run_cmake.sh
  ```

Note that it is not necessary to install Quartz beforehand to run the artifact.

### Install External Packages
In order to run the experiments related to external packages, you need to install them:
- Qiskit (https://qiskit.org/):
  ```shell
  pip install qiskit
  ```
  Our evaluation uses Qiskit 0.34.2.

- pyvoqc (please follow the instructions on https://github.com/inQWIRE/pyvoqc).

## Table 2: Evaluating the Quartz Generator and Verifier

To reproduce the numbers in Table 2, run the following script:

```shell
bash run_table2.sh
```

In the output of the script, lines starting with `***` indicate the numbers used in Table 2. We expect the numbers to
differ a little from the numbers in the submission due to floating-point errors.

This script runs for several hours. To only reproduce the running time for the generator and verifier with all pruning
techniques in one hour, you can modify the third last argument for each invocation of `test_pruning` in `src/test/test_pruning.cpp`
from `true` to `false`, and then run `bash run_table2.sh`.

## Characteristics and the Number of Transformations for the Three Gate Sets

To reproduce the characteristics at the end of section 4 in the submission, run the following script:

```shell
bash gen_ecc_set.sh
```

In the output, `*** ch(...) = ...` denotes the characteristics for each gate set.

`*** Number of transformations of ... = ...` denotes the number of transformations for each gate set. We expect the
numbers of transformations to differ from the numbers in the submission due to floating-point errors.

The generated ECC Sets are stored in Json files with file name formatted like
this: `{Gate set name}_{number of gates}_{number_of qubits}_complete_ECC_set.json`.

## Table 3: Comparing Quartz with existing quantum circuit optimizers on Nam's gate set {𝑅𝑧(𝜆),𝑋,𝐻,𝐶𝑁𝑂𝑇}

### The results of Qiskit

To reproduce the results of Qiskit on Nam's gate set, run the following script:

``` shell
python Qiskit_nam.py
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of Qiskit for qcla_mod_7.qasm on Nam's gate set
884 gates after level 1 optimization after 0.063 seconds
884 gates after level 2 optimization after 0.135 seconds
853 gates after level 3 optimization after 0.330 seconds
```

As the above shows, for each circuit, we run Qiskit with optimization levels 1, 2, 3, respectively. We choose the minimum gate count among the 3 optimization levels as the final result.

It is worth noting that optimizations in Qiskit involves some non-determinism, which means that the results may vary among different runs of the optimizations.

### The results of Nam

We refer the results of Nam on Nam's gate set to the paper "A verified optimizer for Quantum circuits" (https://dl.acm.org/doi/10.1145/3434318). Specifically, the results can be found at Table 2, column "Nam(H)" in this paper.

### The results of VOQC

To reproduce the results of VOQC on Nam's gate set, run the following script:

``` shell
python VOQC_nam.py
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of VOQC for qcla_mod_7.qasm on Nam's gate set
723 gates after pass 'optimize_nam' after 0.048 seconds
```

### The results of Quartz

To reproduce the results of Quartz on Nam's gate set, run the following script:

``` shell
./run_nam.sh
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of Quartz for tof_3.qasm on Nam's gate set.
Gate count after optimization: 35, 7.818 seconds.
```

If you would like to run the experiments for different circuits separately, you can use the following script (assuming you are currently in the `build/` directory):

``` shell
./test_nam the/input/qasm/file/path --output the/output/qasm/file/(optional)
```


## Table 4: Comparing Quartz with existing circuit optimizers on the IBM gate set

### The results of Qiskit

To reproduce the results of Qiskit on IBMQ gate set, run the following script:

``` shell
python Qiskit_ibmq.py
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of Qiskit for qcla_mod_7.qasm on IBMQ gate set
884 gates after level 1 optimization after 0.064 seconds
818 gates after level 2 optimization after 0.311 seconds
795 gates after level 3 optimization after 0.389 seconds
```

As the above shows, for each circuit, we run Qiskit with optimization levels 1, 2, 3, respectively. We choose the minimum gate count among the 3 optimization levels as the final result.

It is worth noting that optimizations in Qiskit involves some non-determinism, which means that the results may vary among different runs of the optimizations.

### The results of t|ket⟩

We refer the results of t|ket⟩ on IBMQ gate set to the paper "A verified optimizer for Quantum circuits" (https://dl.acm.org/doi/10.1145/3434318). Specifically, the results can be found at Table 2, column "t|ket⟩" in this paper.

### The results of VOQC

To reproduce the results of VOQC on IBMQ gate set, run the following script:

``` shell
python VOQC_ibmq.py
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of VOQC for qcla_mod_7.qasm on IBMQ gate set
666 gates after pass 'optimize_nam' and pass 'optimize_ibm' after 0.048 seconds
```

### The results of Quartz

To reproduce the results of Quartz on IBMQ gate set, run the following script:

``` shell
./run_ibmq.sh
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of Quartz for mod5_4.qasm on IBMQ gate set.
Gate count after optimization: 52, 121.69 seconds.
```

If you would like to run the experiments for different circuits separately, you can use the following script (assuming you are currently in the `build/` directory):

``` shell
./test_ibmq the/input/qasm/file/path --output the/output/qasm/file/(optional)
```

## Table 5: Comparing Quartz with Quilc and t|ket⟩ on the Rigetti gate set (𝑅𝑥 (𝑘𝜋/2)(𝑘 ∈Z),𝑅𝑧(𝜆),𝐶𝑍)

### The results of Quilc

We use a docker image of Quilc (available at https://hub.docker.com/r/rigetti/quilc) for optimizing our quantum circuit benchmarks on the Quilc compiler. First, to get the latest stable version of Quilc, run `docker pull rigetti/quilc`. Second, start a Quilc server on a seperate process by running 
```shell
docker run --rm -it -p 5555:5555 rigetti/quilc -R
```
This spawn an RPCQ-mode Quilc server that Quilc's compiler can communication with over TCP. To reproduce the results of Quilc on Rigetti gate set, run the following script:

``` shell
python pyQuil_rigetti.py
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of pyQuil for qcla_mod_7.qasm on Rigetti gate set
3294 gates after 4.989 seconds
```

It is worth noting that optimizations in pyQuil involves some non-determinism, which means that the results may vary among different runs of the optimizations.

### The results of t|ket⟩

To reproduce the results of t|ket⟩ on Rigetti gate set, run the following script:

``` shell
python tket_rigetti.py
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of tket for qcla_mod_7.qasm on Rigetti gate set
3202 gates after 0.536 seconds
```

### The results of Quartz

To reproduce the results of Quartz on Rigetti gate set, run the following script:

``` shell
./run_rigetti.sh
```

The results will be shown in the console. Following shows part of the results as an example:

```
Optimization results of Quartz for barenco_tof_3.qasm on Rigetti gate set.
Gate count after optimization: 148, 12.682 seconds.
```

If you would like to run the experiments for different circuits separately, you can use the following script (assuming you are currently in the `build/` directory):

``` shell
./test_rigetti the/input/qasm/file/path --output the/output/qasm/file/(optional)
```
