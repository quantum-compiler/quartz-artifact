#!/usr/bin/sh
cd build
make test_nam
mkdir -p ../circuit/nam-benchmarks/output_files/mod54
./test_nam ../circuit/nam-benchmarks/mod5_4.qasm --output ../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.33.nam --eqset ../Nam_3_3_complete_ECC_set.json &
./test_nam ../circuit/nam-benchmarks/mod5_4.qasm --output ../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.43.nam --eqset ../Nam_4_3_complete_ECC_set.json &
./test_nam ../circuit/nam-benchmarks/mod5_4.qasm --output ../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.53.nam --eqset ../Nam_5_3_complete_ECC_set.json &
./test_nam ../circuit/nam-benchmarks/mod5_4.qasm --output ../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.63.nam --eqset ../Nam_6_3_complete_ECC_set.json &
./test_nam ../circuit/nam-benchmarks/mod5_4.qasm --output ../circuit/nam-benchmarks/output_files/mod54/mod5_4.qasm.output.73.nam --eqset ../Nam_7_3_complete_ECC_set.json &
