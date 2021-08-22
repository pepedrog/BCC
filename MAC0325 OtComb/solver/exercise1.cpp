#include "digraph.h"
#include "flow_solver.h"
#include "shortest_walks.h"
#include <algorithm>
#include <iostream>
#include <vector>

using std::pair;
using std::vector;

template <typename T> struct injection {
  vector<T> x;

  injection(vector<T> &&_x) : x(_x) {
    std::sort(std::begin(x), std::end(x));
    x.erase(std::unique(std::begin(x), std::end(x)), std::end(x));
  }

  int operator()(T q) {
    return std::distance(std::begin(x),
                         std::lower_bound(std::begin(x), std::end(x), q));
  }

  T operator[](int i) { return x[i]; }
};

injection<char> read_vertices(int n) {
  vector<char> v(n);
  for (int i = 0; i < n; i++)
    std::cin >> v[i];
  return v;
}

int main() {
  int n;
  std::cin >> n;
  auto vertex = read_vertices(n);
  auto display = [&](std::vector<vertex_t> v) {
    for (vertex_t i : v)
      std::cout << vertex[i] << ' ';
    std::cout << '\n';
  };

  int m;
  std::cin >> m;

  digraph_t D(n, m);
  vector<int> u = D.arc_vector();

  for (int k = 0; k < m; k++) {
    char i, j;
    int capacity;
    std::cin >> std::ws >> i >> std::ws >> j >> capacity;
    u[D.add_arc(vertex(i), vertex(j))] = capacity;
  }

  flow_instance_t I = {D, u, vertex('r'), vertex('s')};
  solver_t s(I);
  {
    for (int i = 0; i < n; i++)
      std::sort(std::begin(s.D(i)), std::end(s.D(i)),
                [&](arc_t a, arc_t b) { return s.D.head(a) < s.D.head(b); });
  }
  std::vector<walk_t> log;
  auto [v, f, S] = solve(s, log);
  std::cout << "Value of the flow:\n" << v << '\n';

  std::cout << "List of paths:\n";
  for (walk_t w : log)
    display(w);

  std::cout << "Minimum cut:\n";
  display(S);

  std::cout << "Flow:\n";
  for (vertex_t i = 0; i < n; i++)
    for (arc_t a : D(i)) {
      vertex_t j = D.head(a);
      std::cout << vertex[i] << ' ';
      std::cout << vertex[j] << ": ";
      std::cout << f[a] << '\n';
    }
}
