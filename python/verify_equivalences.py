import sys
import ast

sys.path.append("..")

from verifier.verifier import *

if __name__ == '__main__':
    # Usage example: python verify_equivalences.py input.json output.json True True True True
    # The third parameter is printing basic information or not
    # The fourth parameter is verbose or not
    # The fifth parameter is keeping equivalence classes with only 1 DAG or not
    # The sixth parameter is checking equivalences with different hash values or not
    find_equivalences(sys.argv[1], sys.argv[2],
                      print_basic_info=(True if len(sys.argv) <= 3 else ast.literal_eval(sys.argv[3])),
                      verbose=(False if len(sys.argv) <= 4 else ast.literal_eval(sys.argv[4])),
                      keep_classes_with_1_dag=(True if len(sys.argv) <= 5 else ast.literal_eval(sys.argv[5])),
                      check_equivalence_with_different_hash=(True if len(sys.argv) <= 6 else ast.literal_eval(sys.argv[6])))