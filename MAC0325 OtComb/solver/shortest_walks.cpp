#include "shortest_walks.h"

using std::pair;

walks_t::walks_t(int n, vertex_t _r) : r(_r), A(n, {-1, -1}) {}

bool walks_t::reach(vertex_t i) const { return A[i].first != -1; }

pair<vertex_t, arc_t> walks_t::operator()(vertex_t i) const { return A[i]; }

pair<vertex_t, arc_t> &walks_t::operator()(vertex_t i) { return A[i]; }

walk_t walks_t::walk(vertex_t i) const {
  walk_t ans;
  if (reach(i)) walk_impl(ans, i);
  return ans;
}

void walks_t::walk_impl(walk_t& w, vertex_t i) const {
  if (r != i) {
    const vertex_t j = A[i].first;
    walk_impl(w, j);
  }
  w.push_back(i);
}

walks_t shortest_walks(digraph_t const &D,
                       std::function<bool(arc_t)> subdigraph, vertex_t r) {
  walks_t walks(D.order(), r);
  std::queue<vertex_t> q;

  walks(r) = {r, -1};
  q.push(r);
  while (not q.empty()) {
    int i = q.front();
    q.pop();

    for (arc_t a : D(i)) {
      int j = D.head(a);
      if (subdigraph(a) and (not walks.reach(j))) {
        walks(j) = {i, a};
        q.push(j);
      }
    }
  }

  return walks;
}
