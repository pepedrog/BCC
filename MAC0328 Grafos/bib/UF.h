// MAC0328 (2019) 
// Altere e modifique à vontade. Mas observe o meu bom layout (veja
// www.ime.usp.br/~pf/algoritmos/aulas/layout.html) e não use tabs
// (exceto no começo das linhas).

// Este arquivo: UF.h (codificação UTF-8)
// Data: 2019-07-17
// Autor: Paulo Feofiloff
//
// Esta é a interface de uma implementação da estrutura Union-Find
// especializada para vértices de grafos (veja GRAPHlists.h e
// GRAPHlists.c).
//
// O código é uma adaptação dos programas do livro "Algorithms",
// 3rd.ed., part 1, de Sedgewick.
////////////////////////////////////////////////////////////////////////


#ifndef _UF_h
#define _UF_h

#include "MYTOOLS.h" // mallocc()

// Vértices (de grafos) são números inteiros não-negativos (veja
// GRAPHlists.h).
#define vertex int

// UFinit() inicializa a estutura de chefes fazendo com que cada vértice
// seja o seu próprio chefe.
void 
UFinit( int V);

// A função UFfind() devolve o chefe de v (ou seja, o chefe da
// componente conexa a floresta geradora mst[0..k-1] que contém v).
vertex 
UFfind( vertex v);

// A função UFunion() recebe dois chefes distintos v0 e w0 e faz a união
// das correspondentes componentes conexas. Devolve 1 se v0 for o chefe
// da fusão das componentes e 2 se w0 for o chefe da fusão das
// componentes.
void
UFunion( vertex v0, vertex w0);

// Encerra a estrutura Union-Find e libera o espaço auxiliar que foi
// alocado pela estrutura.
void 
UFfree( void);

#endif
