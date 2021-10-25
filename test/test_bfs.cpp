#include "test_generator.h"

int main() {
  Context ctx
      ({GateType::x, GateType::y, GateType::rx, GateType::cx, GateType::add});
  Generator gen(&ctx);

  const int num_qubits = 3;
  const int num_input_parameters = 2;
  const int max_num_gates = 3;

  EquivalenceSet equiv_set;

  Dataset dataset1;
  auto start = std::chrono::steady_clock::now();
  gen.generate_dfs(num_qubits, num_input_parameters, max_num_gates,
                   dataset1, /*restrict_search_space=*/true);
  auto end = std::chrono::steady_clock::now();
  std::cout << std::dec << "DFS with search space restricted: "
            << dataset1.num_total_dags()
            << " circuits with " << dataset1.num_hash_values()
            << " different hash values are found in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;
  dataset1.save_json("dfs_restricted.json");

  start = std::chrono::steady_clock::now();
  equiv_set.clear();
  system(
      "python ../python/verify_equivalences.py dfs_restricted.json dfs_restricted_verified.json");
  equiv_set.load_json(&ctx, "dfs_restricted_verified.json");
  equiv_set.simplify(&ctx);
  equiv_set.save_json("dfs_restricted_simplified.json");
  end = std::chrono::steady_clock::now();
  std::cout << std::dec << "DFS with search space restricted: there are "
            << equiv_set.num_total_dags()
            << " circuits in " << equiv_set.num_equivalence_classes()
            << " equivalence classes after verification and simplification in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;

  ctx.clear_representatives();
  dataset1.clear();

  start = std::chrono::steady_clock::now();
  gen.generate_dfs(num_qubits, num_input_parameters, max_num_gates,
                   dataset1, /*restrict_search_space=*/false);
  end = std::chrono::steady_clock::now();
  std::cout << std::dec << "DFS for all DAGs: "
            << dataset1.num_total_dags()
            << " circuits with " << dataset1.num_hash_values()
            << " different hash values are found in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;
  dataset1.save_json("dfs_all.json");

  start = std::chrono::steady_clock::now();
  equiv_set.clear();
  system(
      "python ../python/verify_equivalences.py dfs_all.json dfs_all_verified.json");
  equiv_set.load_json(&ctx, "dfs_all_verified.json");
  equiv_set.simplify(&ctx);
  equiv_set.save_json("dfs_all_simplified.json");
  end = std::chrono::steady_clock::now();
  std::cout << std::dec << "DFS for all DAGs: there are "
            << equiv_set.num_total_dags()
            << " circuits in " << equiv_set.num_equivalence_classes()
            << " equivalence classes after verification and simplification in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;

  ctx.clear_representatives();

  Dataset dataset2;
  start = std::chrono::steady_clock::now();
  gen.generate(num_qubits,
               num_input_parameters,
               max_num_gates,
               &dataset2, /*verify_equivalences=*/
               false,
               nullptr, /*verbose=*/
               true);
  end = std::chrono::steady_clock::now();
  std::cout << std::dec << "BFS unverified: " << dataset2.num_total_dags()
            << " Circuits with " << dataset2.num_hash_values()
            << " different hash values are found in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;
  dataset2.save_json("bfs_unverified.json");

  start = std::chrono::steady_clock::now();
  equiv_set.clear();
  system(
      "python ../python/verify_equivalences.py bfs_unverified.json bfs_unverified_verified.json");
  equiv_set.load_json(&ctx, "bfs_unverified_verified.json");
  equiv_set.simplify(&ctx);
  equiv_set.save_json("bfs_unverified_simplified.json");
  end = std::chrono::steady_clock::now();
  std::cout << std::dec << "BFS unverified: there are "
            << equiv_set.num_total_dags()
            << " circuits in " << equiv_set.num_equivalence_classes()
            << " equivalence classes after verification and simplification in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;

  ctx.clear_representatives();

  Dataset dataset3;
  start = std::chrono::steady_clock::now();
  gen.generate(num_qubits,
               num_input_parameters,
               max_num_gates,
               &dataset3, /*verify_equivalences=*/
               true,
               &equiv_set, /*verbose=*/
               true);
  end = std::chrono::steady_clock::now();
  std::cout << std::dec << "BFS verified: " << dataset3.num_total_dags()
            << " circuits with " << dataset3.num_hash_values()
            << " different hash values are found in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;
  dataset3.save_json("tmp_before_verify.json");

  start = std::chrono::steady_clock::now();
  equiv_set.clear();
  system(
      "python ../python/verify_equivalences.py tmp_before_verify.json bfs_verified.json");
  equiv_set.load_json(&ctx, "bfs_verified.json");
  equiv_set.simplify(&ctx);
  equiv_set.save_json("bfs_verified_simplified.json");
  end = std::chrono::steady_clock::now();
  std::cout << std::dec << "BFS verified: there are "
            << equiv_set.num_total_dags()
            << " circuits in " << equiv_set.num_equivalence_classes()
            << " equivalence classes after verification and simplification in "
            << (double) std::chrono::duration_cast<std::chrono::milliseconds>(
                end - start).count() / 1000.0 << " seconds."
            << std::endl;

  auto result = equiv_set.first_class_with_common_first_or_last_gates();
  if (result == -1) {
    std::cout << "No common first or last gates." << std::endl;
  } else {
    std::cout << "Found common first or last gates in "
              << equiv_set.get_class_id(result) << std::endl;
  }
  return 0;
}
