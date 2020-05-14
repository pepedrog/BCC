// MAC0328 (2019) 
// Altere e modifique à vontade. Mas observe o meu bom layout (veja
// www.ime.usp.br/~pf/algoritmos/aulas/layout.html) e não use tabs
// (exceto no começo das linhas).

// Este arquivo: QUEUE.c (codificação UTF-8)
// Data: 2019-07-17
// Autor: Paulo Feofiloff
//
// Esta é uma implementação de uma fila de vértices de um grafo (veja
// GRAPHlists.h e GRAPHlists.c).
//
// O código é uma adaptação dos programas 4.10 e 4.11, p.156-157, do
// livro "Algorithms", 3rd.ed., part 1, de Sedgewick.
////////////////////////////////////////////////////////////////////////


#include "QUEUE.h"
// inclui MYTOOLS.h (que contém a definição de mallocc())

// A fila reside no segmento queue[begin..end-1] de um vetor
// queue[0..N-1]. A fila está vazia se begin == end. Vamos supor que
// temos sempre 0 <= begin <= end <= N.

static vertex *queue; 
static int begin, end;

void 
QUEUEinit( int N) { 
   queue = mallocc( N * sizeof (vertex));
   begin = end = 0; 
}

int 
QUEUEempty( void) { 
   return begin == end; 
}

void 
QUEUEput( vertex v) {
   queue[end++] = v;
}

vertex 
QUEUEget( void) { 
   return queue[begin++];
}

void 
QUEUEfree( void) {
   free( queue);
}


