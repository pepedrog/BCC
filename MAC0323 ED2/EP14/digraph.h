/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * NAO EDITE OU MODIFIQUE NADA QUE ESTA ESCRITO NESTE ARQUIVO
 *
 * Interface de uma ADT digraph adaptada para C
 *  
 *   https://algs4.cs.princeton.edu/42digraph/
 *   https://algs4.cs.princeton.edu/42digraph/Digraph.java.html
 * 
 * DIGRAPH
 *
 * Digraph representa um grafo orientado de vértices inteiros de 0 a V-1. 
 * 
 * As principais operações são: add() que insere um arco no digrafo, e
 * adj() que itera sobre todos os vértices adjacentes a um dado vértice.
 * 
 * Arcos paralelos e laços são permitidos.
 * 
 * Está implementação usa uma representação de _vetor de listas de adjacência_,
 * que  é uma vetor de objetos Bag indexado por vértices. Por simplicidade 
 * esses Bag são de objetos int e não de Integer.
 *
 * Todas as operações consomen no pior caso tempo constante, exceto
 * iterar sobre os vértices adjacentes a um determinado vértice, cujo consumo
 * de tempo é proporcional ao número de tais vértices.
 * 
 * Para documentação adicional, ver 
 * https://algs4.cs.princeton.edu/42digraph, Seção 4.2 de
 * Algorithms, 4th Edition por Robert Sedgewick e Kevin Wayne.
 *
 */
#ifndef _DIGRAPH_H
#define _DIGRAPH_H

#include <stddef.h> /* size_t */
#include "util.h"   /* Bool */

/* vértices de digrafos são inteiros */
/* o 'v' minúsculo tem dois motivos: 
 *   - ser compatível com as notas de aula de 
 *     Algoritmos em Grafos de Paulo Feofiloff
 *     https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/graphdatastructs.html
 *   - indicar que, como int, uma variável do tipo vertex __não__ é um 
 *     ponteiro (não corresponde a uma variável de referência).
 */
#ifndef vertex
#define vertex int
#endif

/* Digraph é um ponteiro para a estrutura que representa um digrafo */
typedef struct digraph *Digraph;

/*-----------------------------------------------------------*/
/*  prototipos das funcoes que manipulam um digraph          */

/*-----------------------------------------------------------*/
/* 
 *  Construtores e "destrutor"
 */

/* 
 *  retorna um digrafo com V vértices sem arcos 
 */
Digraph
newDigraph(int V);

/* retorna um clone de G */
Digraph
cloneDigraph(Digraph G);

/* retorna o digrafo reverso de G */
Digraph
reverseDigraph(Digraph G);

/* retorna a representação do digrafo lido de um arquivo */
Digraph
readDigraph(String nomeArq);

/* libera todo o espaço usado pelo digrafo */
void  
freeDigraph(Digraph G);

/*------------------------------------------------------------*/
/*
 * Permite as operações usuais: 
 *
 *     - vDigraph(), eDigraph(): número de vértices e arcos
 *     - addEdge(): insere um arco
 *     - adj(): itera sobre os vizinhos de um dado vértice
 *     - outDegree(), inDegree(): grau de saída e de entrada
 *     - toString(): usada para exibir o digrafo 
 */

/* retorna o número de vértices do digrafo */
int
vDigraph(Digraph G);

/* retorna o número de arcos do digrafo */
int
eDigraph(Digraph G);

/* insere o arco v→w no dgrafo */
void
addEdge(Digraph G, vertex v, vertex w);

/* retorna os vértices adjacentes a partir de v */
int
adj(Digraph G, vertex v, Bool init);

/* retorna o número de arcos saindo de v */
int
outDegree(Digraph G, vertex v);

/* retorna o número de arcos entrando em v */
int
inDegree(Digraph G, vertex v);

/* retorna uma string usada para exibir o digrafo */
String
toString(Digraph G);

#endif /* _DIGRAPH_H */
