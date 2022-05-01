# The Quartz Quantum Circuit Optimizer

[![DOI](https://zenodo.org/badge/464661620.svg)](https://zenodo.org/badge/latestdoi/464661620)

Quartz is a quantum circuit optimizer that automatically generates and verifies circuit transformations for an arbitrary quantum gate set. To optimize an input quantum circuit, Quartz uses these auto-generated circuit transformations to construct a search space of functionally equivalent quantum circuits.
Quartz uses a cost-based search algorithm to explore the space and discovers highly optimized quantum circuits.

See more details in the PLDI paper ([DOI](https://doi.org/10.1145/3519939.3523433)) or the extended version ([arXiv](https://arxiv.org/abs/2204.09033)).

## Repository Organization

See [code structure](doc/CODE_STRUCTURE.md) for more information about the organization of the Quartz artifact code base.

## Getting Started

### Hardware Requirements

We recommend (and have only thoroughly tested) an m6i.32xlarge AWS instance with Ubuntu 20.04 to run our artifact. If other instances are used, we require at least 256 GB DRAM and disk space, and it may take longer than the reported times to run.

### Installation

We have only tested all commands on Ubuntu 20.04, but they should also work on other operating systems such as Windows (see the "On Windows" paragraph below).

- Make sure you have CMake (https://cmake.org/) with version >= 3.16 and pip3. If not, you can install them:
  ```shell
  sudo apt install python3-pip
  sudo apt install cmake
  ```

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
  ./run_cmake.sh
  ```
    - If you see `-bash: ./run_cmake.sh: Permission denied`, please run `chmod +x *.sh`.

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

In order to run the experiments related to external packages, you need to install the following external packages:

- Qiskit (https://qiskit.org/):
  ```shell
  pip install qiskit
  ```
  Our evaluation uses Qiskit 0.34.2.

- pyvoqc (for details, please refer to the instructions on https://github.com/inQWIRE/pyvoqc).

    To install `pyvoqc`, you should first install [opam](https://opam.ocaml.org/doc/Install.html).

    After `opam` is installed, you can use the following scripts to install the OCaml version of `VOQC` which is a prerequisite of `pyvoqc`.

    ```
    # environment setup
    opam init
    eval $(opam env)

    # install the OCaml version of VOQC
    opam pin voqc https://github.com/inQWIRE/mlvoqc.git#mapping
    ```

    Then, you can clone the [pyvoqc](https://github.com/inQWIRE/pyvoqc#installation) repo and build the `VOQC` library and install it to python with the following script:

    ```
    git clone https://github.com/inQWIRE/pyvoqc.git
    cd pyvoqc
    ./install.sh # sudo may required
    ```

    To check that installation worked, open a Python shell and try `from pyvoqc.voqc import VOQCCircuit`.


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

**This script also generates ECC sets for following sections.** You can also download the ECC sets from [Zenodo](https://zenodo.org/record/6508992).

To reproduce the numbers in Table 5 (and Table 8 in extended version) and to generate the ECC sets, run the following script:

```shell
./gen_ecc_set.sh > eccset.log
python show_eccset_results.py
```

This script runs for about 13 hours. The script generates the ECC sets for the Rigetti gate set first, then the Nam gate set, then the IBM gate set, in about 4 hours.
After these ~4 hours, the script is generating the ECC sets for scalability analysis
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

##### On Windows

The script is the same on Windows.

### Other Columns

To reproduce the other numbers in Table 6, run the following script:

```shell
./run_table6.sh > table6.log
python show_table6_results.py
```

You can run the Python script while the shell script is running to see some intermediate results (a part of the table).
You should be able to see the following intermediate results by running the Python script after running the shell script 1 minute:
```
- Nam Gate Set:
  - Row "n = 2":
    - Column "RepGen": 400
    - Column "+ ECC Simplification": 50
    - Column "+ Common Subcircuit": 50
...
```
The 3 rows with "`- Column`" correspond to 3 cells of the row "n = 2" of "Nam Gate Set" in Table 6.

The numbers inside the parentheses in Table 6 can be computed by dividing the number of possible circuits by the numbers here.

This script runs for about 7 hours.

##### On Windows

Run the following command:
```batch
build\Debug\test_pruning.exe > table6.log
python show_table6_results.py
```

## Table 2: Comparing Quartz with existing quantum circuit optimizers on the Nam gate set {𝑅𝑧(𝜆),𝑋,𝐻,𝐶𝑁𝑂𝑇}

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

To reproduce the "Quartz Preprocess" column in Table 2, run the following script:

```shell
./run_nam_disable_search.sh > nam_disable_search.log
```

This script runs for about 7 seconds. After that, use the following command to show the results:

```shell
python extract_results.py nam_disable_search.log
```

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`:
```batch
cd build
Debug\test_nam.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --disable_search
```

### The results of Quartz

To reproduce the results of Quartz on Nam's gate set, run the following script (after generating `Nam_6_3_complete_ECC_set.json` using `./gen_ecc_set.sh`):

```shell
./run_nam.sh > nam.log
```

This script runs in background for 24 hours plus a few minutes, using 26 cores.
After that, use the following command to show the results:

```shell
python extract_results.py nam.log
```

You can run the Python script `python extract_results.py Nam_6_3` while the shell script is running to see the most up-to-date intermediate results.
For the results of the first `{t}` seconds, you can run `python extract_results.py Nam_6_3 {t}`.
Following shows an example excerpt of the output of the Python script:
```
adder_8         732 (at 0.0040 seconds)
barenco_tof_3   44 (at 32.4400 seconds)
barenco_tof_4   86 (at 0.0000 seconds)
barenco_tof_5   126 (at 0.0000 seconds)
barenco_tof_10  326 (at 0.0010 seconds)
```

You can also run the Python script `python extract_results.py Nam_6_3` after the script `run_nam.sh` finished to see detailed results.

The log files are also available on [Zenodo](https://zenodo.org/record/6508992).

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

## Table 3: Comparing Quartz with existing circuit optimizers on the IBM gate set

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

To reproduce the "Quartz Preprocess" column in Table 3, run the following script:

```shell
./run_ibmq_disable_search.sh > ibm_disable_search.log
```

This script runs for about 10 seconds. After that, use the following command to show the results:

```shell
python extract_results.py ibm_disable_search.log
```

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`
(assuming you are currently in the `build\` directory):
```batch
Debug\test_ibmq.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --disable_search
```

### The results of Quartz

To reproduce the results of Quartz on IBMQ gate set, run the following script (after generating `IBM_4_3_complete_ECC_set.json` using `./gen_ecc_set.sh`):

```shell
./run_ibmq.sh > ibm.log
```

This script runs in background for 24 hours plus a few minutes, using 26 cores.
After that, use the following command to show the results:

```shell
python extract_results.py ibm.log
```

You can run the Python script `python extract_results.py IBM_4_3` while the shell script is running to see the most up-to-date intermediate results.
For the results of the first `{t}` seconds, you can run `python extract_results.py IBM_4_3 {t}`.
Following shows an example excerpt of the output of the Python script:
```
adder_8         736 (at 0.0020 seconds)
barenco_tof_3   36 (at 59.6340 seconds)
barenco_tof_4   69 (at 58.9980 seconds)
barenco_tof_5   109 (at 56.2830 seconds)
barenco_tof_10  324 (at 54.0790 seconds)
```

You can also run the Python script `python extract_results.py IBM_4_3` after the script `run_ibmq.sh` finished to see detailed results.

The log files are also available on [Zenodo](https://zenodo.org/record/6508992).

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

## Table 4: Comparing Quartz with Quilc and t|ket⟩ on the Rigetti gate set

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

To reproduce the "Quartz Preprocess" column in Table 4, run the following script:

```shell
./run_rigetti_disable_search.sh > rigetti_disable_search.log
```

This script runs in background for about 1 minute. After that, use the following command to show the results:

```shell
python extract_results.py rigetti_disable_search.log
```

##### On Windows

To run the experiments for different circuits separately, for example, to run the experiment for `barenco_tof_3`
(assuming you are currently in the `build\` directory):
```batch
Debug\test_rigetti.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --disable_search
```

### The results of Quartz

To reproduce the results of Quartz on Rigetti gate set, run the following script (after generating `Rigetti_6_3_complete_ECC_set.json` using `./gen_ecc_set.sh`):

```shell
./run_rigetti.sh > rigetti.log
```

This script runs in background for 24 hours plus a few minutes, using 26 cores.
After that, use the following command to show the results:

```shell
python extract_results.py rigetti.log
```

You can run the Python script `python extract_results.py Rigetti_3_3` while the shell script is running to see the most up-to-date intermediate results.
For the results of the first `{t}` seconds, you can run `python extract_results.py Rigetti_3_3 {t}`.
Following shows an example excerpt of the output of the Python script:
```
adder_8         2788 (at 0.0100 seconds)
barenco_tof_3   148 (at 59.9830 seconds)
barenco_tof_4   272 (at 59.5070 seconds)
barenco_tof_5   410 (at 59.5290 seconds)
barenco_tof_10  1058 (at 46.4950 seconds)
```

You can also run the Python script `python extract_results.py Rigetti_3_3` after the script `run_rigetti.sh` finished to see detailed results.

The log files are also available on [Zenodo](https://zenodo.org/record/6508992).

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

## Section 7.5: Analyzing Quartz’s Circuit Optimizer

To reproduce the results in Section 7.5 of the paper, run the following script after generating the ECC sets:

```shell
./run_scalability.sh
```

This script runs for about 100 hours (On machines with 512 threads, you can run all commands in the script in parallel, so it will only take 24 hours plus a few minutes.).
The results are stored in `scalability_{n}{q}.txt` where `n` ranges from 1 to 7, and `q` ranges from 1 to 4 (if `n` is 7, then the upper bound of `q` is 3).
You can run `python extract_results.py scalability_{n}{q}.txt` to see the final results,
or run `python extract_results.py Nam_{n}_{q}` to see the intermediate results.

The log files are also available on [Zenodo](https://zenodo.org/record/6508992).

You can run `python plot-scripts/scalability_plot.py` to plot Figure 7 in the paper and Figure 9-34 (left) in the extended version.
You can also copy the corresponding part of the output of `python extract_results.py Nam_{n}_{q}` for each `n` and `q`
into line 13-60 of `plot-scripts/scalability_plot.py`
and then run `python plot-scripts/scalability_plot.py` to plot the results.

You can run `python plot-scripts/time_plot.py` to plot Figure 8 in the paper and Figure 9-34 (right) in the extended version.
You can also copy the corresponding part of the output of `python extract_results.py Nam_{n}_3` for each `n`
into line 13-18 of `plot-scripts/time_plot.py`
and then run `python plot-scripts/time_plot.py` to plot the results.

##### On Windows

To run the experiments for different ECC sets and circuits separately, for example, to run the experiment for `barenco_tof_3` with a (3,2)-complete ECC set (`n=3, q=2`)
(assuming you are currently in the `build\` directory):
```batch
Debug\test_nam.exe ..\circuit\nam-benchmarks\barenco_tof_3.qasm --eqset ..\Nam_3_2_complete_ECC_set.json
```

## For `mod5_4`

We provide an optimization result example of 25 gates at `circuit/example-circuits/mod5_4_optimized_result.qasm`.

To use different random seeds to run the circuit `mod5_4`, please make the following changes in the code:
- At line 64-66 of `src/quartz/tasograph/substitution.h`, change
  ```c++
    /*if (lc == rc) {
      return lhs->random_value_ < rhs->random_value_;
    }*/
  ```
  to
  ```c++
    if (lc == rc) {
      return lhs->random_value_ < rhs->random_value_;
    }
  ```
- At line 246 of `src/quartz/tasograph/tasograph.h`, change
  ```c++
  // int random_value_;
  ```
  to
  ```c++
  int random_value_;
  ```
- At line 30 of `src/quartz/tasograph/tasograph.cpp`, change
  ```c++
  /*, random_value_(rand())*/
  ```
  to
  ```c++
  , random_value_(rand())
  ```
- At line 32 of `src/quartz/tasograph/tasograph.cpp`, change
  ```c++
  /*, random_value_(rand())*/
  ```
  to
  ```c++
  , random_value_(rand())
  ```
- At line 119 of `src/quartz/tasograph/tasograph.cpp`, change
  ```c++
  /*: random_value_(rand())*/
  ```
  to
  ```c++
  : random_value_(rand())
  ```
- At line 1109 of `src/quartz/tasograph/tasograph.cpp`, change
  ```c++
  // srand(0);
  ```
  to
  ```c++
  srand({seed});
  ```
  where `{seed}` is the random seed you want to run
- At line 1113 of `src/quartz/tasograph/tasograph.cpp`, change
  ```c++
  ".log";
  ```
  to
  ```c++
  "_rand{seed}.log";
  ```
  where `{seed}` is the random seed you want to run
- At line 1117 of `src/quartz/tasograph/tasograph.cpp`, change
  ```c++
  ".err";
  ```
  to
  ```c++
  "_rand{seed}.err";
  ```
  where `{seed}` is the random seed you want to run

After all these changes, run the following script:
```shell
./run_nam_mod5_4.sh
```

This script runs for 24 hours plus a few minutes. You can use the following commands to see the results
(before 24 hours, they will show intermediate results):
```shell
python extract_results.py Nam_3_3_mod5_4_rand
python extract_results.py Nam_4_3_mod5_4_rand
python extract_results.py Nam_5_3_mod5_4_rand
python extract_results.py Nam_6_3_mod5_4_rand
python extract_results.py Nam_7_3_mod5_4_rand
```

You can change the `{seed}` above multiple times and then run `run_nam_mod5_4.sh` and `extract_results.py`
to show the results of multiple runs together.

The log files for 6 different random seeds and one run not using `srand` (so 7 runs in total for each `n`)
are also available on [Zenodo](https://zenodo.org/record/6508992).

You can run `python plot-scripts/mod54_plot.py` to plot Figure 35 in the extended version of the paper.
You can also copy the corresponding part of the output of `python extract_results.py Nam_{n}_3_mod5_4_rand` for each `n`
into line 14-18 and line 22-26 of `plot-scripts/mod54_plot.py`
and then run `python plot-scripts/mod54_plot.py` to plot the results.

##### On Windows
Instead of running `./run_nam_mod5_4.sh`, you can follow these steps:
- Open `build\Quartz.sln` in Visual Studio 2019, and click Build -> Build Solution.
- Run the following commands (assuming you are currently in the `build\` directory):
  ```batch
  mkdir "../circuit/nam-benchmarks/output_files/mod54"
  Debug\test_nam.exe "../circuit/nam-benchmarks/mod5_4.qasm" --output "../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.33.nam" --eqset "../Nam_3_3_complete_ECC_set.json"
  Debug\test_nam.exe "../circuit/nam-benchmarks/mod5_4.qasm" --output "../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.43.nam" --eqset "../Nam_4_3_complete_ECC_set.json"
  Debug\test_nam.exe "../circuit/nam-benchmarks/mod5_4.qasm" --output "../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.53.nam" --eqset "../Nam_5_3_complete_ECC_set.json"
  Debug\test_nam.exe "../circuit/nam-benchmarks/mod5_4.qasm" --output "../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.63.nam" --eqset "../Nam_6_3_complete_ECC_set.json"
  Debug\test_nam.exe "../circuit/nam-benchmarks/mod5_4.qasm" --output "../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.73.nam" --eqset "../Nam_7_3_complete_ECC_set.json"
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
```

The results should be slightly worse than the results in the paper, but it will run
much faster (in about 1 hour). After that, you can use the following command to see the results:

```shell
python extract_results.py ibm_without_u3.txt
```

To generate a (4,3)-complete ECC set with 2 input parameters for a gate set similar to Rigetti gate set
but allowing any `Rx` gates (instead of only allowing `Rx(k * pi / 2)` where `k` is an integer) and
without the constraint that each input parameter is used at most once in a circuit,
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
```

This script may run for 24 hours plus a few minutes.
After that, you can use the following command to see the results:

```shell
python extract_results.py rigetti_modified.txt
```
