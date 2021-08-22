#pragma once
#include <vector>

using vertex_t = int;
using arc_t = int;

class digraph_t {
  int es;
  int n, m;
  std::vector<std::vector<arc_t>> adj;
  std::vector<vertex_t> to;

public:
  digraph_t(int n, int m);
  arc_t add_arc(vertex_t i, vertex_t j);
  int size() const;
  int order() const;
  std::vector<int> arc_vector() const;
  std::vector<arc_t> const &operator()(vertex_t) const;
  std::vector<arc_t> &operator()(vertex_t);
  vertex_t head(arc_t e) const;
  std::vector<arc_t> arcs() const;
};
