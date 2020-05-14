// MAC0328 (2019) 
// Altere e modifique à vontade. Mas observe o meu bom layout (veja
// www.ime.usp.br/~pf/algoritmos/aulas/layout.html) e não use tabs
// (exceto no começo das linhas).

// Este arquivo: PQ.c (codificação UTF-8)
// Data: 2019-07-17
// Autor: Paulo Feofiloff
//
// Esta é uma implementação clássica de uma fila priorizada "crescente"
// (= min-oriented priority queue) de vértices de um grafo (veja
// GRAPHlists.h e GRAPHlists.c). Ela usa um heap pq[1..n] organizado de
// modo que pq[1] tenha prioridade mínima. 
//
// O código é uma adaptação do programa 9.12, p.391, do livro
// "Algorithms", 3rd.ed., part 1, de Sedgewick.
////////////////////////////////////////////////////////////////////////


#include "PQ.h"
// inclui MYTOOLS.h (que contém mallocc())

// A fila priorizada é armazenada no vetor pq[1..n] de vértices. Esse
// vetor é organizado como um heap.
static vertex *pq; 
static int n;

// As prioridades são dadas em um vetor prty[] indexado por vértices:
// o vértice na posição k de pq tem prioridade prty[pq[k]]. (O vetor
// prty[] é fornecido pelo cliente.) O heap pq[1..n] é caracterizado
// pela propriedade prty[pq[k/2]] <= prty[pq[k]] para k = 2, ..., n.
// Portanto, o vértice pq[1] tem prioridade prty[pq[1]] mínima.

#define greater( i, j) (prty[pq[i]] > prty[pq[j]] ? 1 : 0)

// O vetor qp[0..n-1] é o "inverso" de pq: para cada vértice v, qp[v] é
// o único índice tal que pq[qp[v]] == v. É claro que qp[pq[i]] == i
// para todo i.
static int *qp; 

static void 
exch( int i, int j) {
   vertex t = pq[i]; pq[i] = pq[j]; pq[j] = t;
   qp[pq[i]] = i;
   qp[pq[j]] = j;
}

static void 
fixUp( int k, int prty[]) {
   while (k > 1 && greater( k/2, k)) {
      exch( k/2, k);
      k = k/2;
   }
}

static void 
fixDown( int k, int prty[]) { 
   while (2*k <= n) { 
      int j = 2*k;
      if (j < n && greater( j, j+1)) j++;
      if (!greater( k, j)) break;
      exch( k, j); 
      k = j;
   }
}

// Supõe-se que teremos sempre n <= V.
void 
PQinit( int V) { 
   pq = mallocc( (V+1) * sizeof (vertex));
   qp = mallocc(  V * sizeof (int));
   n = 0; 
} 

int 
PQempty( void) { 
   return n == 0; 
}

void 
PQinsert( vertex v, int prty[]) {
   qp[v] = ++n; 
   pq[n] = v; 
   fixUp( n, prty); 
}

vertex 
PQdelmin( int prty[]) { 
   exch( 1, n); 
   --n; 
   fixDown( 1, prty); 
   return pq[n+1]; 
}

void 
PQdec( vertex w, int prty[]) { 
   fixUp( qp[w], prty); 
}

void 
PQfree( ) { 
   free( pq);
   free( qp);
}



