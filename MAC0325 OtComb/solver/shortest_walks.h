#pragma once
#include "digraph.h"
#include <functional>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>

using walk_t = std::vector<vertex_t>;

class walks_t {
  int r;
  std::vector<std::pair<vertex_t, arc_t>> A;

  void walk_impl(walk_t&, vertex_t) const;

public:
  walks_t(int, vertex_t);
  std::pair<vertex_t, arc_t> operator()(vertex_t) const;
  std::pair<vertex_t, arc_t> &operator()(vertex_t);
  bool reach(vertex_t i) const;
  walk_t walk(vertex_t i) const;
};

walks_t shortest_walks(digraph_t const &D,
                       std::function<bool(arc_t)> subdigraph, vertex_t r);
