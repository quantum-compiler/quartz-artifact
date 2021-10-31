#pragma once

#include "../context/rule_parser.h"
#include "../parser/qasm_parser.h"
#include "../tasograph/tasograph.h"

void test_context_shift(const std::string &filename, Context *src_ctx,
                        Context *dst_ctx, RuleParser *rule_parser) {

  QASMParser qasm_parser(src_ctx);
  DAG *dag = nullptr;
  if (!qasm_parser.load_qasm(filename, dag)) {
	std::cout << "Parser failed" << std::endl;
	return;
  }

  TASOGraph::Graph graph(src_ctx, *dag);
  TASOGraph::Graph *graph_new_ctx =
      graph.context_shift(src_ctx, dst_ctx, rule_parser);
  for (auto it = graph_new_ctx->inEdges.begin();
       it != graph_new_ctx->inEdges.end(); ++it) {
	std::cout << gate_type_name(it->first.ptr->tp) << std::endl;
  }
  std::cout << graph_new_ctx->total_cost() << std::endl;
}