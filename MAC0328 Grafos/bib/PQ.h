// MAC0328 (2019) 
// Altere e modifique à vontade. Mas observe o meu bom layout (veja
// www.ime.usp.br/~pf/algoritmos/aulas/layout.html) e não use tabs
// (exceto no começo das linhas).

// Este arquivo: PQ.h (codificação UTF-8)
// Data: 2019-07-17
// Autor: Paulo Feofiloff
//
// Esta é a interface da implementação de uma fila priorizada
// "crescente" (= min-oriented priority queue) de vértices de um grafo
// (veja GRAPHlists.h e GRAPHlists.c).
//
// O código é uma adaptação do programa 9.11, p.390, do livro
// "Algorithms", 3rd.ed., part 1, de Sedgewick.
////////////////////////////////////////////////////////////////////////


#ifndef _PQ_h
#define _PQ_h

#include "MYTOOLS.h" // mallocc()

// Os vértices (de grafos) são inteirosnão-negativos (veja
// GRAPHlists.h).
#define vertex int

// As prioridades da fila são dadas em um vetor prty[] indexado por
// vértices. O vértice v com prty[v] mínima tem prioridade máxima.

void 
PQinit( int V);
// Supõe-se que a fila tem no máximo V vértices.

int 
PQempty( void);

void 
PQinsert( vertex v, int prty[]);

vertex 
PQdelmin( int prty[]);

void 
PQdec( vertex w, int prty[]);

void 
PQfree( );

#endif
