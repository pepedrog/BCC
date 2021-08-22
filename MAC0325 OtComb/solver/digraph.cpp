#include "digraph.h"

using std::vector;

digraph_t::digraph_t(int _n, int _m) : es(2), n(_n), m(_m + 2), adj(n), to(m) {}

vector<int> digraph_t::arc_vector() const { return vector<int>(m); }

arc_t digraph_t::add_arc(vertex_t i, vertex_t j) {
  to[es] = j;
  adj[i].push_back(es);
  return es++;
}

int digraph_t::size() const { return m; }

int digraph_t::order() const { return n; }

vector<arc_t> const &digraph_t::operator()(vertex_t i) const { return adj[i]; }

vector<arc_t> &digraph_t::operator()(vertex_t i) { return adj[i]; }

vertex_t digraph_t::head(arc_t e) const { return to[e]; }

std::vector<arc_t> digraph_t::arcs() const {
  std::vector<arc_t> ans(m - 2);
  for (arc_t a = 2; a < m; a++)
    ans[a - 2] = a;
  return ans;
}
