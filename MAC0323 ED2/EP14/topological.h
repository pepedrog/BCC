/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * NAO EDITE OU MODIFIQUE NADA QUE ESTA ESCRITO NESTE ARQUIVO
 *
 * Interface de uma ADT dfs adaptação para para C de partes das classes
 * 
 * 
 * TOPOLOGICAL
 *
 * Recebe um digrafo e constroi um tipo abstrato de dados (ADT) que basicamente 
 * determina, 
 * 
 *      - uma ordenação topológica dos vértices (se o digrafo for um DAG);
 *      - um ciclo (se houver algum).
 *   
 * Diremos que este ADT é uma "representação topológica" do digrafo.
 * 
 * As principais operações são: 
 *
 *      - hasCycle(): indica se o digrafo tem um ciclo (DirectedCycle.java)
 *      - isDag(): indica se o digrafo é acyclico (Topological.java)
 *
 *      - pre(): retorna a numeração pré-ordem de um vértice em relação a uma dfs 
 *               (DepthFirstOrder.java)
 *      - pos(): retorna a numareção pós-ordem de um vértice em relação a uma dfs
 *               (DepthFirstOrder.java)
 *      - rank(): retorna a numeração topológica de um vértice (Topological.java)
 * 
 *      - preorder(): itera sobre todos os vértices do digrafo em pré-ordem
 *                    (em relação a uma dfs, DepthFirstOrder.java)
 *      - postorder(): itera sobre todos os vértices do digrafo em pós-ordem
 *                    (em relação a uma dfs, ordenação topologica reversa, 
 *                     DepthFirstOrder.java)
 *      - order(): itera sobre todos os vértices do digrafo em ordem  
 *                 topologica (Topological.java)
 *      - cycle(): itera sobre os vértices de um ciclo (DirectedCycle.java)
 *      
 * Para documentação adicional, ver 
 * https://algs4.cs.princeton.edu/42digraph, Seção 4.2 de
 * Algorithms, 4th Edition por Robert Sedgewick e Kevin Wayne.
 *
 */
#ifndef _TOPOLOGICAL_H
#define _TOPOLOGICAL_H

#include "util.h"   /* Bool */
#include "digraph.h" /* Digraph, newDigraph(), adj(), vertex, ... */

/* Topological é um ponteiro para a estrutura que representa esta ADT */
typedef struct topological *Topological;

/*-----------------------------------------------------------*/
/*  prototipos das funcoes que manipulam um topological      */

/*-----------------------------------------------------------*/
/* 
 *  Construtor e "destrutor"
 */

/* 
 *  retorna uma representação topológica do digrafo G
 */
Topological
newTopological(Digraph G);

/* libera todo o espaço usado pela representação topologica */
void  
freeTopological(Topological ts);

/*------------------------------------------------------------*/
/*
 * Operações
 *
 */
/* retorna TRUE se o digrafo representado por TS possui um ciclo */
Bool
hasCycle(Topological ts);

/* retorna TRUE se o digrafo representado por TS é um DAG */
Bool
isDag(Topological ts);

/* retorna a numeração pré-ordemdo do vértice V */
int
pre(Topological ts, vertex v);

/* retorna a numeração pos-ordemdo do vértice V */
int
post(Topological ts, vertex v);

/* retorna a numeração topológica do vértice V */
int
rank(Topological ts, vertex v);

/* retorna os vértices em pré-ordem */
vertex
preorder(Topological ts, Bool init);

/* retorna os vértices em pós-ordem */
vertex
postorder(Topological ts, Bool init);

/* retorna os vértices em ordem topológica */
vertex
order(Topological ts, Bool init);

/* retorna os vértices em um ciclo do digrafo representado por TS */
vertex
cycle(Topological ts, Bool init);

#endif /* _TOPOLOGICAL_H */
