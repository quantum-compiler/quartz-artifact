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

In the output of the script, lines starting with `***` indicate the numbers used in Table 2.
We expect the numbers to differ a little from the numbers in the submission because of floating-point errors.


## Characteristics and the Number of Transformations for the Three Gate Sets

Run the following script:
```shell
bash gen_ecc_set.sh
```

In the output, `*** ch(...) = ...` denotes the characteristics for each gate set.
`*** Number of transformations of ... = ...` denotes the number of transformations for each gate set.
