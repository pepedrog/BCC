// MAC0328 (2019) 
// Altere e modifique à vontade. Mas observe o meu bom layout (veja
// www.ime.usp.br/~pf/algoritmos/aulas/layout.html) e não use tabs
// (exceto no começo das linhas).

// Este arquivo: UF.c (codificação UTF-8)
// Data: 2019-07-17
// Autor: Paulo Feofiloff
//
// Esta é uma implementação de uma estrutura Union-Find especializada
// para vértices de grafos (veja GRAPHlists.h e GRAPHlists.c). O código
// inclui os truques "path compression" e "union-by-rank".
//
// O código é uma adaptação dos programas do livro "Algorithms",
// 3rd.ed., part 1, de Sedgewick.
////////////////////////////////////////////////////////////////////////


#include "UF.h"
// inclui MYTOOLS.h e a definição de vértice (#define vertex int)

// Estrutura de dados privada.
static vertex *chefe;
static int *size;

void 
UFinit( int V) {
   chefe = mallocc( V * sizeof (vertex)); 
   size = mallocc( V * sizeof (int)); 
   for (vertex v = 0; v < V; ++v) { 
      chefe[v] = v; 
      size[v] = 1; 
   }
}

vertex 
UFfind( vertex v) { 
   vertex v0 = v; 
   while (v0 != chefe[v0]) 
      v0 = chefe[v0]; // path compression
   return v0; 
}

void
UFunion( vertex v0, vertex w0) { 
   if (size[v0] < size[w0]) { // union-by-rank
      chefe[v0] = w0; 
      size[w0] += size[v0]; 
   }
   else { 
      chefe[w0] = v0; 
      size[v0] += size[w0]; 
   }
}

void 
UFfree( void) { 
   free( chefe);
   free( size);
}

