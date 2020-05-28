#include <stdio.h>
#include <stdlib.h>
#include <math.h>

using namespace std;

struct point { double x, y; };

struct point p[10000];
//double d = 10000;

int cmp (const void *a, const void *b) {
  struct point *p1 = (struct point *) a;
  struct point *p2 = (struct point *) b;
  if (p1->x < p2->x || (p1->x == p2->x && p1->y < p2->y)) return -1;
  return 1; 
}

#define DIST(p1, p2) (sqrt(((p1).x - (p2).x)*((p1).x - (p2).x) + ((p1).y - (p2).y)*((p1).y - (p2).y)))
#define min(a,b) (a < b ? a : b)

// Essa versão não é garantido O(nlgn)
// Mas como eu tiro toda a parte da ordenação pelo eixo y
// aparentemente fica, na prática, mais rápido
double dmin(long a, long b){
       long i, j, k;
       double d1, d2, d;
       double xp;
       if(a == b) return 10001+1.0;
       else if(b-a == 1) return DIST(p[b],p[a]);
       else {
            d1 = dmin(a,(a+b)/2);
            d2 = dmin((a+b)/2+1,b);
            d = min(d1,d2);
            j = (a+b)/2;
            xp = p[j].x;
            do{
               k = (a+b)/2 + 1;
               while(xp - p[k].x < d && k <= b){
                   d1 = DIST(p[k],p[j]);
                   d = min(d,d1);
                   k++;
               }
               j--;
            }while(xp - p[j].x < d && j >= a);
       return d;
       }
}

int main() {
  unsigned int n, m;
  scanf("%d", &n);
  double d;
  while (n) {
    m = n;
    while (n--) scanf("%lf %lf", &p[n].x, &p[n].y);

    qsort((void *) p, m, sizeof(struct point), cmp);
    d = dmin(0, m-1);
    
    if (d > 10000) printf("INFINITY\n");
    else printf("%.4lf\n", d);

    scanf("%d", &n);
  }
  return 0;
}