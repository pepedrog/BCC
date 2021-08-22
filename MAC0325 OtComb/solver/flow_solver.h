#pragma once
#include "digraph.h"
#include "shortest_walks.h"
#include <climits>
#include <iostream>
#include <vector>

using flow_t = std::vector<int>;
using cut_t = std::vector<vertex_t>;

struct flow_solution_t {
  int value;
  flow_t f;
  cut_t S;
};

struct flow_instance_t {
  digraph_t D;
  flow_t u;
  vertex_t r, s;
};

struct solver_t {
  int n;
  digraph_t D;
  flow_t u;
  vertex_t r, s;
  std::vector<arc_t> original_arc;

  solver_t(flow_instance_t);
  friend flow_solution_t solve(solver_t, std::vector<walk_t>&);

private:
  int maxflow(flow_t &f, std::vector<walk_t>&) const;
  arc_t reverse(arc_t) const;
  bool forward_arc(arc_t) const;
  int path_capacity(flow_t const &f, walks_t const &walks, vertex_t i) const;
  void update_flow(flow_t &f, walks_t const &walks, int nf, vertex_t i) const;
};
