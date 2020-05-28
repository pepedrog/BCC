#include <stdio.h>
#include <stdlib.h>

using namespace std;

struct point { int x, y; };

struct point p[1001];
//double d = 10000;

#define min(a,b) (a < b ? a : b)

bool inside (struct point q, int n) {
  int c = 0, m = n;
  int j;
  while (n--) {
    j = (m+n-1)%m;
    if (((p[n].y < q.y && p[j].y > q.y) || 
         (p[n].y > q.y && p[j].y < q.y)) &&
          p[n].x > q.x) c++;
  }
  if (c%2) return true;
  return false;
}

int main() {
  unsigned int n, m;
  struct point q;
  scanf("%d", &n);
  double d;
  while (n) {
    m = n;
    while (n--) scanf("%d %d", &p[n].x, &p[n].y);
    scanf("%d %d", &q.x, &q.y);
    if (inside (q, m)) printf ("T");
    else printf("F\n");
    scanf("%d", &n);
  }
  return 0;
}