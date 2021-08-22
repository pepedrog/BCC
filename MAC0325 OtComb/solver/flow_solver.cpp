#include "flow_solver.h"

using std::pair;
using std::vector;

solver_t::solver_t(flow_instance_t I)
    : n(I.D.order()), D(n, 2 * I.D.size()), u(D.arc_vector()), r(I.r), s(I.s),
      original_arc(D.size()) {
  for (vertex_t i = 0; i < n; i++)
    for (arc_t a : I.D(i)) {
      const vertex_t j = I.D.head(a);

      arc_t b = D.add_arc(i, j);
      u[b] = I.u[a];
      original_arc[b] = a;

      arc_t c = D.add_arc(j, i);
      u[c] = 0;
      original_arc[c] = a;
    }
}

flow_solution_t solve(solver_t solver, vector<walk_t>& log) {
  const int n = solver.D.order();
  flow_t residual_f = solver.D.arc_vector();
  const int value = solver.maxflow(residual_f, log);

  flow_t f(solver.D.size() / 2);
  for (arc_t a : solver.D.arcs())
    if (solver.forward_arc(a))
      f[solver.original_arc[a]] = residual_f[a];

  auto residual = [&](arc_t a) { return residual_f[a] < solver.u[a]; };
  auto walks = shortest_walks(solver.D, residual, solver.r);

  cut_t S;
  for (vertex_t i = 0; i < n; i++)
    if (walks.reach(i))
      S.push_back(i);

  return {value, f, S};
}

int solver_t::maxflow(vector<int> &f, vector<walk_t>& log) const {
  auto residual = [&](arc_t a) { return f[a] < u[a]; };
  auto walks = shortest_walks(D, residual, r);

  if (not walks.reach(s))
    return 0;

  int nf = path_capacity(f, walks, s);
  update_flow(f, walks, nf, s);

  log.push_back(walks.walk(s));

  return nf + maxflow(f, log);
}

arc_t solver_t::reverse(arc_t a) const { return (a ^ 1); }

bool solver_t::forward_arc(arc_t a) const { return !(a & 1); }

int solver_t::path_capacity(vector<int> const &f, walks_t const &walks,
                            vertex_t i) const {
  if (r == i)
    return INT_MAX;
  const auto [j, a] = walks(i);
  return std::min(u[a] - f[a], path_capacity(f, walks, j));
}

void solver_t::update_flow(vector<int> &f, walks_t const &walks, int nf,
                           vertex_t i) const {
  if (r == i)
    return;
  const auto [j, a] = walks(i);
  f[a] += nf;
  f[reverse(a)] -= nf;
  update_flow(f, walks, nf, j);
}
