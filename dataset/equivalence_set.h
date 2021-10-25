#pragma once

#include "../context/context.h"
#include "../dag/dag.h"

#include <functional>
#include <list>
#include <set>
#include <unordered_set>
#include <unordered_map>

class EquivalenceSet;

class EquivalenceClass {
 public:
  // Returns all DAGs in this equivalence class.
  [[nodiscard]] std::vector<DAG *> get_all_dags() const;

  void insert(std::unique_ptr<DAG> dag);

  [[nodiscard]] int size() const;
  void reserve(std::size_t new_cap);

  // Extract all DAGs in this equivalence class, and make this class empty.
  std::vector<std::unique_ptr<DAG>> extract();

  // Replace |dags_| with |dags|.
  void set_dags(std::vector<std::unique_ptr<DAG>> dags);

  // The first DAG is the representative.
  DAG *get_representative();

  // Returns if this equivalence class contains |dag|.
  [[nodiscard]] bool contains(const DAG &dag) const;

  // If this equivalence class contains |dag|, set |dag| as the representative
  // of the class and return true.
  // Otherwise, return false.
  [[nodiscard]] bool set_as_representative(const DAG &dag);

  // For each pair of circuits in this class, if they share
  // a common "first" gate or a common "last" gate, remove the latter one.
  // Here "first" means a quantum gate which does not topologically depend
  // on any other quantum gates, and "last" means a quantum gate which can
  // appear at last in some topological order of the DAG.
  // Return the number of circuits removed.
  int remove_common_first_or_last_gates(Context *ctx,
                                        std::unordered_set<DAGHashType> &hash_values_to_remove);

 private:
  std::vector<std::unique_ptr<DAG>> dags_;
};

// This class stores all equivalence classes.
class EquivalenceSet {
 public:
  // |new_representatives| is for Generator::generate().
  // It will be pushed back all representatives previously not in
  // the equivalence set.
  bool load_json(Context *ctx,
                 const std::string &file_name,
                 std::vector<DAG *> *new_representatives = nullptr);

  bool save_json(const std::string &file_name) const;

  // Normalize each clause of equivalent DAGs to have the minimum
  // (according to DAG::less_than) minimal representation.
  // Warning: see comments in DAG::minimal_representation().
  // TODO: adapt to the new equivalence set format
  void normalize_to_minimal_representations(Context *ctx);

  void clear();

  // A final pass of simplification before feeding the equivalences
  // to the optimizer.
  // Returns if the pass does some simplification or not.
  bool simplify(Context *ctx);

  // Remove equivalence classes with only one DAG.
  // Return the number of equivalent classes removed.
  int remove_singletons(Context *ctx);

  // Remove unused qubits and input parameters if they are unused in
  // each DAG of an equivalent class.
  // Return the number of equivalent classes removed
  // (and possibly inserted again).
  int remove_unused_qubits_and_input_params(Context *ctx);

  // For each pair of circuits in one equivalence class, if they share
  // a common "first" gate or a common "last" gate, remove the latter one.
  // Here "first" means a quantum gate which does not topologically depend
  // on any other quantum gates, and "last" means a quantum gate which can
  // appear at last in some topological order of the DAG.
  // Return the number of equivalent classes modified.
  int remove_common_first_or_last_gates(Context *ctx);

  // This function runs in O(1).
  [[nodiscard]] int num_equivalence_classes() const;

  // This function runs in O(|classes_|.size()).
  [[nodiscard]] int num_total_dags() const;

  // Returns the position in |classes_|, or -1 if not found.
  [[nodiscard]] int first_class_with_common_first_or_last_gates() const;

  [[nodiscard]] std::string get_class_id(int num_class) const;

  [[nodiscard]] std::vector<std::vector<DAG *>> get_all_equivalence_sets() const;

  [[nodiscard]] std::vector<EquivalenceClass *> get_possible_classes(const DAGHashType &hash_value) const;

  // A hacky function to insert a single class to the equivalence set.
  // There's no guarantee that the class inserted is different with any other
  // classes already in the set.
  void insert_class(Context *ctx,
                    std::unique_ptr<EquivalenceClass> equiv_class);

 private:
  void set_possible_class(const DAGHashType &hash_value,
                          EquivalenceClass *equiv_class);
  void remove_possible_class(const DAGHashType &hash_value,
                             EquivalenceClass *equiv_class);

  std::vector<std::unique_ptr<EquivalenceClass>> classes_;

  // A map from the hash value to all equivalence classes with at least one
  // DAG of the hash value.
  std::unordered_map<DAGHashType, std::set<EquivalenceClass *>>
      possible_classes_;
};
