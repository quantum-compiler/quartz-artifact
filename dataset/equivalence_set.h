#pragma once

#include "../context/context.h"
#include "../dag/dag.h"

#include <list>
#include <unordered_set>
#include <unordered_map>

class EquivalenceSet {
 public:
  bool load_json(Context *ctx, const std::string &file_name);

  // Normalize each clause of equivalent DAGs to have the minimum
  // (according to DAG::less_than) minimal representation.
  void normalize_to_minimal_representations();

  // We cannot use std::vector here because that would need
  // std::unordered_set<std::unique_ptr<DAG>> to be copy-constructable.
  //
  // Each std::unordered_set represents a clause of equivalent DAGs.
  std::unordered_map<DAGHashType,
                     std::list<std::unordered_set<std::unique_ptr<DAG>>>>
      dataset;
};
