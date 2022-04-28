# The Quartz Quantum Circuit Optimizer

[![DOI](https://zenodo.org/badge/464661620.svg)](https://zenodo.org/badge/latestdoi/464661620)


Quartz is a quantum circuit optimizer that automatically generates and verifies circuit transformations for an arbitrary quantum gate set. To optimize an input quantum circuit, Quartz uses these auto-generated circuit transformations to construct a search space of functionally equivalent quantum circuits.
Quartz uses a cost-based search algorithm to explore the space and discovers highly optimized quantum circuits.

Note: This README was written for the artifact evaluation and might not match everything in the latest version of the paper for now. We will update it very soon.

## Repository Organization

See [code structure](doc/CODE_STRUCTURE.md) for more information about the organization of the Quartz artifact code base.

## Getting Started

### Hardware Requirements

We recommend (and have only thoroughly tested) an m6i.32xlarge AWS instance with Ubuntu 20.04 to run our artifact. If other instances are used, we require at least 256 GB DRAM and disk space, and it may take longer than the reported times to run.

### Installation

We provide the following two approaches to install the artifact.

#### 1. Install from AMI

To facilitate the artifact evaluation of our submission, we provide an Amazon Machine Image (AMI) of Quartz with all dependencies pre-installed. Our AMI instance ID is ami-0fb5ae3c79d123cf1. To log in to the instance, the username and password are both `pldi22ae`.

#### 2. Install from source code

We have only tested all commands on Ubuntu 20.04, but they should also work on other operating systems such as Windows (see the "On Windows" paragraph below).

- Make sure you have CMake (https://cmake.org/) with version >= 3.16.

- Make sure `python` points to `python3`. If not, you can install `python-is-python3`:
  ```shell
  sudo apt-get install python-is-python3
  ```
  
- Install the Z3 Theorem Prover (https://github.com/Z3Prover/z3):
  ```shell
  pip install z3-solver==4.8.12
  ```
  **We require Z3 version 4.8.12.** Please do not use the latest version of Z3 as we have observed potential bugs.

- Install the Natsort Python package (https://pypi.org/project/natsort/)
  ```shell
  pip install natsort
  ```

- Run CMake:
  ```shell
  bash run_cmake.sh
  ```

Note that it is not necessary to install Quartz beforehand to run the artifact.

##### On Windows

Note that the experiment results may differ slightly on Windows.

- Make sure you have CMake (https://cmake.org/) with version >= 3.16.

- Make sure `python` points to `python3`.

- Make sure you have Visual Studio 2019. We have only tested version 16.11.5 of Visual Studio Community 2019.

- Run the following commands:
  ```batch
  mkdir build
  cd build
  cmake ..
  ```
  
- Open `build\Quartz.sln` in Visual Studio 2019, and click Build -> Build Solution.

### Install External Packages

Note that you do not need to install external packages if you install from AMI because we have already pre-installed them for you.

If you installed from source, in order to run the experiments related to external packages, you need to install them:

- Qiskit (https://qiskit.org/):
  ```shell
  pip install qiskit
  ```
  Our evaluation uses Qiskit 0.34.2.

- pyvoqc (please follow the instructions on https://github.com/inQWIRE/pyvoqc).

- t|ket⟩ (https://github.com/CQCL/tket):

  ``` shell
  pip install pytket
  ```
  Our evaluation uses pytket 0.16.0.

- pyQuil (https://github.com/rigetti/pyquil):

  ``` shell
  pip install pyquil
  ```
  Our evaluation uses pyquil 3.0.1.

## Table 5: Metrics for Quartz’s generator

**This script also generates ECC sets for following sections.**

To reproduce the numbers in Table 5 (and Table 8 in extended version) and to generate the ECC sets, run the following script:

```shell
bash gen_ecc_set.sh > eccset.log
python show_eccset_results.py
```

This script runs for about 13 hours. After about 4 hours, the script is generating the ECC sets for scalability analysis
(see the "Scalability Analysis on the Nam gate set" section of this README file).
If you do not want to run the scalability analysis and do not want to reproduce the data for the (7,3)-complete ECC set
for the Nam gate set, you can terminate the script after about 4 hours.

You can run the Python script while the shell script is running to see some intermediate results.
After running the shell script for about 1 minute, running the Python script should show the following result
(the running times may vary each time):
```
*** Number of transformations (|T|) of Rigetti_2_3 = 66
*** Number of transformations (|T|) of Rigetti_3_3 = 66
*** Size of resulting representative set (|Rn|) of Rigetti_2_3 = 361
*** Size of resulting representative set (|Rn|) of Rigetti_3_3 = 3143
*** Total Time (s) of Rigetti_2_3 = 1.773
*** Total Time (s) of Rigetti_3_3 = 5.955
*** Verification Time (s) of Rigetti_2_3 = 1.669
*** Verification Time (s) of Rigetti_3_3 = 5.156
*** ch(Rigetti,q=3) = 30
```

In the output, `*** ch(...) = ...` denotes the characteristics for each gate set.

The other rows correspond to cells in Table 5.

The generated ECC sets are stored in Json files with file name formatted like
this: `{Gate set name}_{number of gates}_{number_of qubits}_complete_ECC_set.json`.

On another Ubuntu machine with 12 CPU cores and 32 GB memory, we are able to generate
up to (6,3)-complete ECC sets for Nam gate set, up to (3,3)-complete ECC sets for IBM gate set,
and up to (6,3)-complete ECC sets for Rigetti gate set within 80 minutes in total.

##### On Windows

Run the following command:
```batch
build\Debug\gen_ecc_set.exe > eccset.log
python show_eccset_results.py
```

## Table 6: Evaluating the Quartz Generator and the Pruning Techniques

### Number of Possible Circuits

To reproduce the number of possible circuits in Table 6, run the following script (this script requires Python 3.8+):
```shell
python plot-scripts/table6_possible_circuits.py Nam
python plot-scripts/table6_possible_circuits.py IBM
python plot-scripts/table6_possible_circuits.py Rigetti
```

### Other Columns

To reproduce the other numbers in Table 6, run the following script:

```shell
bash run_table6.sh > table6.log
python show_table6_results.py
```

We present Table 6 in a different way in the camera-ready version than in the submission version of the paper.
We removed the "ECC Simplification" column and added some other columns. This script outputs the numbers
corresponding to the camera-ready version, but the column titles match the submission version for artifact evaluation.
We will modify the script to make the column titles match the camera-ready version when linking the artifact to the
camera-ready version of the paper.

We expect the numbers to differ from the numbers in the submission due to floating-point errors and bug fixes after the
paper submission.

You can run the Python script while the shell script is running to see some intermediate results (a part of the table).
You should be able to see the following intermediate results by running the Python script after running the shell script 1 minute:
```
- Nam Gate Set:
  - Row "n = 3":
    - Column "Original": 11404 (4179)
    - Algorithm 1 with only singleton removal (not shown in the submission): 1180 (566)
    - Column "Representative": 231 (99)
    - Column "Common Subcircuit": 164 (66)
    - Column "Overall Reduction": 98.56% (98.42%)
    - |Rn| (not shown in the submission): 4179
    - Verification time (s) (not shown in the submission): 2.575
    - Column "Running Time (s)": 3.721
  - Row "n = 4":
    - ...
```
The 5 rows with "`- Column`" correspond to 5 cells of the row "n = 3" of "Nam Gate Set" in Table 2.
- `Column "Original"` corresponds to the column `Original` in the submission, and column `Brute Force` in the camera-ready version.
- `Algorithm 1 with only singleton removal` corresponds to the column `RepGen` in the camera-ready version.
- `Column "Representative"` corresponds to the column `Representative` in the submission, and column `+ ECC Simplification` in the camera-ready version.
- `Column "Common Subcircuit"` corresponds to the column `Common Subcircuit` in the submission, and column `+ Common Subcircuit Pruning` in the camera-ready version.
- `Column "Overall Reduction"` corresponds to the column `Overall Reduction` in both versions.
- `|Rn|` corresponds to the column `|Rn|` in Table 3 of the camera-ready version.
- `Verification time (s)` corresponds to the column `Verification time (s)` in Table 3 of the camera-ready version.
- `Column "Running Time (s)"` corresponds to the column `Running Time (s)` in the submission, and column `Total Time (s)` in Table 3 of the camera-ready version.

This script runs for about 10 hours. To only reproduce the running time for the generator and verifier with all pruning
techniques faster (in 1.5 hours), you can modify the fourth last argument for each invocation of `test_pruning` in `src/test/test_pruning.cpp`
from `true` to `false` and comment out the invocations of `Nam_7_` and `IBM_5_`, and then run `bash run_table2.sh`.

##### On Windows

Run the following command:
```batch
build\Debug\test_pruning.exe > table2.log
python show_table2_results.py
```

## Table 3: Comparing Quartz with existing quantum circuit optimizers on Nam's gate set {𝑅𝑧(𝜆),𝑋,𝐻,𝐶𝑁𝑂𝑇}

This corresponds to Table 4 in the camera-ready version.

### The results of Qiskit

To reproduce the results of Qiskit on Nam's gate set, run the following script:

``` shell
python Qiskit_nam.py
```

This script runs for about 0.7 seconds.

The results will be shown in the console. The figure below shows part of the results as an example:

![](figures/Qiskit_nam_example.png)

As the figures shows, for each circuit, we run Qiskit with optimization levels 1, 2, 3, respectively. We choose the minimum gate count among the 3 optimization levels as the final result.

It is worth noting that optimizations in Qiskit involves some non-determinism, which means that the results may vary among different runs of the optimizations.

### The results of Nam

We refer the results of Nam on Nam's gate set to the paper "A verified optimizer for Quantum circuits" (https://dl.acm.org/doi/10.1145/3434318). Specifically, the results can be found at Table 2, column "Nam(H)" in this paper.

### The results of VOQC

To reproduce the results of VOQC on Nam's gate set, run the following script:

``` shell
python VOQC_nam.py
```

This script runs for about 0.5 seconds.

The results will be shown in the console. The figure below shows part of the results as an example:

![](figures/VOQC_nam_example.png)

### The results of Quartz Preprocessing

To reproduce the "Quartz Preprocess" column in the camera-ready version (not shown in the submission version),
run the following script:

```shell
bash run_nam_disable_search.sh > nam_disable_search.log
python extract_results.py nam_disable_search.log
```

This script runs for about 7 seconds.

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`:
```batch
cd build
Debug\test_nam.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --disable_search
```

### The results of Quartz

To reproduce the results of Quartz on Nam's gate set, run the following script:

``` shell
./run_nam.sh > nam.log
python extract_results.py nam.log
```

This script runs for 24 hours plus a few minutes.

You can run the Python script `python extract_results.py Nam_6_3` while the shell script is running to see some intermediate results.
Following shows an example excerpt of the output of the Python script:
```
barenco_tof_3   38
barenco_tof_4   68
barenco_tof_5   98
```

The figure below shows part of the results in `nam.log` as an example:

![](figures/quartz_nam_example.png)

If you would like to run the experiments for different circuits separately, you can use the following script (assuming you are currently in the `build/` directory):

``` shell
./test_nam the/input/qasm/file/path --output the/output/qasm/file/(optional)
```

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`
(assuming you are currently in the `build\` directory):
```batch
Debug\test_nam.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm
```

## Table 4: Comparing Quartz with existing circuit optimizers on the IBM gate set

This corresponds to Table 5 in the camera-ready version.

### The results of Qiskit

To reproduce the results of Qiskit on IBMQ gate set, run the following script:

``` shell
python Qiskit_ibmq.py
```

This script runs for about 0.9 seconds.

The results will be shown in the console. The figure below shows part of the results as an example:

![](figures/Qiskit_ibmq_example.png)

As the figures shows, for each circuit, we run Qiskit with optimization levels 1, 2, 3, respectively. We choose the minimum gate count among the 3 optimization levels as the final result.

It is worth noting that optimizations in Qiskit involves some non-determinism, which means that the results may vary among different runs of the optimizations.

### The results of t|ket⟩

We refer the results of t|ket⟩ on IBMQ gate set to the paper "A verified optimizer for Quantum circuits" (https://dl.acm.org/doi/10.1145/3434318). Specifically, the results can be found at Table 2, column "t|ket⟩" in this paper.

### The results of VOQC

To reproduce the results of VOQC on IBMQ gate set, run the following script:

``` shell
python VOQC_ibmq.py
```

This script runs for about 0.5 seconds.

The results will be shown in the console. The figure below shows part of the results as an example:

![](figures/VOQC_ibmq_example.png)

### The results of Quartz Preprocessing

To reproduce the "Quartz Preprocess" column in the camera-ready version (not shown in the submission version),
run the following script:

```shell
bash run_ibmq_disable_search.sh > ibm_disable_search.log
python extract_results.py ibm_disable_search.log
```

This script runs for about 10 seconds.

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`
(assuming you are currently in the `build\` directory):
```batch
Debug\test_ibmq.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --disable_search
```

### The results of Quartz

To reproduce the results of Quartz on IBMQ gate set, run the following script:

``` shell
./run_ibmq.sh > ibm.log
python extract_results.py ibm.log
```

This script runs for 24 hours plus a few minutes.

You can run the Python script `python extract_results.py IBM_4_3` while the shell script is running to see some intermediate results.
Following shows an example excerpt of the output of the Python script:
```
barenco_tof_3   36
barenco_tof_4   69
barenco_tof_5   102
```

The figure below shows part of the results in `ibm.log` as an example:

![](figures/quartz_ibmq_example.png)

If you would like to run the experiments for different circuits separately, you can use the following script (assuming you are currently in the `build/` directory):

``` shell
./test_ibmq the/input/qasm/file/path --output the/output/qasm/file/(optional)
```

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`
(assuming you are currently in the `build\` directory):
```batch
Debug\test_ibmq.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm
```

## Table 5: Comparing Quartz with Quilc and t|ket⟩ on the Rigetti gate set (𝑅𝑥 (𝑘𝜋/2)(𝑘 ∈Z),𝑅𝑧(𝜆),𝐶𝑍)

This corresponds to Table 6 in the camera-ready version.

### The results of Quilc

We use a docker image of Quilc (available at https://hub.docker.com/r/rigetti/quilc) for optimizing our quantum circuit benchmarks on the Quilc compiler. First, to get the latest stable version of Quilc, run `docker pull rigetti/quilc`. Second, start a Quilc server on a seperate process by running 
```shell
docker run --rm -it -p 5555:5555 rigetti/quilc -R
```
This spawn an RPCQ-mode Quilc server that Quilc's compiler can communication with over TCP. To reproduce the results of Quilc on Rigetti gate set, run the following script:

``` shell
python pyQuil_rigetti.py
```

This script runs for about 2 minutes.

The results will be shown in the console. The figure below shows part of the results as an example:

![](figures/pyquil_rigetti_example.png)

It is worth noting that optimizations in pyQuil involves some non-determinism, which means that the results may vary among different runs of the optimizations.

### The results of t|ket⟩

To reproduce the results of t|ket⟩ on Rigetti gate set, run the following script:

``` shell
python tket_rigetti.py
```

This script runs for about 8 seconds.

The results will be shown in the console. The figure below shows part of the results as an example:

![](figures/tket_rigetti_example.png)

### The results of Quartz Preprocessing

To reproduce the "Quartz Preprocess" column in the camera-ready version (not shown in the submission version),
run the following script:

```shell
bash run_rigetti_disable_search.sh > rigetti_disable_search.log
python extract_results.py rigetti_disable_search.log
```

This script runs for about 1 minute.

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`
(assuming you are currently in the `build\` directory):
```batch
Debug\test_rigetti.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --disable_search
```

### The results of Quartz

To reproduce the results of Quartz on Rigetti gate set, run the following script:

``` shell
./run_rigetti.sh > rigetti.log
python extract_results.py rigetti.log
```

This script runs for 24 hours plus a few minutes.

You can run the Python script `python extract_results.py Rigetti_6_3` while the shell script is running to see some intermediate results.
Following shows an example excerpt of the output of the Python script:
```
barenco_tof_3   148
barenco_tof_4   272
barenco_tof_5   388
```

The figure below shows part of the results in `rigetti.log` as an example:

![](figures/quartz_rigetti_example.png)

If you would like to run the experiments for different circuits separately, you can use the following script (assuming you are currently in the `build/` directory):

``` shell
./test_rigetti the/input/qasm/file/path --output the/output/qasm/file/(optional)
```

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`
(assuming you are currently in the `build\` directory):
```batch
Debug\test_rigetti.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm
```

## Scalability Analysis on the Nam gate set

This is not included in the paper submission, but we would like to include it for completeness because it appears in the camera-ready version (Figure 10).
To reproduce the scalability analysis results, run the following script after generating the ECC sets:

``` shell
bash run_scalability.sh
```

This script runs for about 100 hours (On machines with 512 threads, you can run all commands in the script in parallel, so it will only take 24 hours plus a few minutes.).
The results are stored in `scalability_{n}{q}.txt` where `n` ranges from 1 to 7, and `q` ranges from 1 to 4 (if `n` is 7, then the upper bound of `q` is 3).
You can run `python extract_results.py scalability_{n}{q}.txt` to see the final results,
or run `python extract_results.py Nam_{n}_{q}` to see the intermediate results.

##### On Windows

To run the experiments for different ECC sets and circuits separately, for example, to run the experiment for `barenco_tof_3` with a (3,2)-complete ECC set (`n=3, q=2`)
(assuming you are currently in the `build\` directory):
```batch
Debug\test_nam.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --eqset ..\Nam_3_2_complete_ECC_set.json
```

## Test other ECC sets

You can also test other ECC sets not shown above in this artifact.

For example, if you want to generate a (3,3)-complete ECC set with 4 input parameters
for the IBM gate set but without the U3 gate (to make the ECC set much smaller),
you can change the main function in `src/test/gen_ecc_set.cpp` to the following:

```c++
gen_ecc_set({GateType::u1, GateType::u2, GateType::cx, GateType::add},
            "IBM_without_U3_3_3_", true, 3, 4, 3);
return 0;
```

And then run the following commands:

```shell
./gen_ecc_set.sh
./run_ibmq.sh ../IBM_without_U3_3_3_complete_ECC_set.json > ibm_without_u3.txt
python extract_results.py ibm_without_u3.txt
```

The results should be slightly worse than the results in the paper, but it will run
much faster (in about 1 hour).

To generate a (4,3)-complete ECC set with 2 input parameters for the Rigetti gate set
but without the constraint that each input parameter is used at most once in a circuit,
you can change the main function in `src/test/gen_ecc_set.cpp` to the following:

```c++
gen_ecc_set({GateType::rx, GateType::rz, GateType::cz, GateType::add},
            "Rigetti_modified_4_3_", false, 3, 2, 4);
return 0;
```

And then run the following commands:

```shell
./gen_ecc_set.sh
./run_rigetti.sh ../Rigetti_modified_4_3_complete_ECC_set.json > rigetti_modified.txt
python extract_results.py rigetti_modified.txt
```
