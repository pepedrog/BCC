/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * unit test para a ADT Digraph
 *
 */
/* tabela de símbolos */
#include "digraph.h"  /* newDigraph(), cloneDigraph(), reverseDigraph(), 
                         freeDigraph(), addEdge(), vDigraph(), eDigraph() */
#include "util.h"    /* String, emalloc(), Integer, String, ERRO(), AVISO() */

#include <stdio.h>   /* printf() */
#include <stdlib.h>  /* exit(), EXIT_SUCCESS */
#include <assert.h>  /* assert() */


/*---------------------------------------------------------------*/
/* 
 *  M A I N 
 */
int 
main(int argc, char *argv[])
{
    Digraph K1 = newDigraph(1);
    Digraph K2 = newDigraph(2);
    Digraph cloneK2   = NULL;
    Digraph reverseK2 = NULL;
    Digraph tinyDG    = NULL;
    Digraph mediumDG  = NULL;
    Digraph largeDG   = NULL;
    String s1 = NULL;
    String s2 = NULL;
    String s  = NULL;
    vertex v;
    vertex w;
    int V = -1;
    int E = -1;

    /*---------------------------------------*/
    printf("-----\nteste toString()\n");
    s1 = toString(K1); /* toString() */
    s2 = toString(K2); /* toString() */
    printf("%s", s1);
    printf("%s", s2);
    free(s1);
    free(s2);

    /*---------------------------------------*/
    printf("-----\nteste addEdge()\n");
    addEdge(K2, 0, 1); /* addEdge() */
    addEdge(K2, 0, 1); /* addEdge() */
    addEdge(K2, 0, 1); /* addEdge() */
    addEdge(K2, 1, 0); /* addEdge() */
    s1 = toString(K1); 
    s2 = toString(K2);
    printf("%s", s1);
    printf("%s", s2);
    free(s1);
    free(s2);
    s1 = s2 = NULL;

    /*---------------------------------------*/
    printf("-----\nteste clone()\n");
    cloneK2   = cloneDigraph(K2);
    
    /* libere área alocadas para digrafos */
    freeDigraph(K1); /* freeDigraph() */
    freeDigraph(K2); /* freeDigraph() */
    K1 = K2 = NULL;
    
    s = toString(cloneK2);
    printf("clone K2: %s", s);
    V = vDigraph(cloneK2);
    E = eDigraph(cloneK2);

    /*---------------------------------------*/
    printf("-----\nteste iterador adj()\n");
    printf("clone K2: %d vertices, %d edges\n", V, E);
    for (v = 0; v < V; v++) {
        printf("%d: ", v);
        for (w = adj(cloneK2, v, TRUE); w >= 0; w = adj(cloneK2, v, FALSE)) {
            printf("%d ", w);
        }
        printf("\n");
    }
    free(s);

    /*---------------------------------------*/
    printf("-----\nteste reverseDigraph()\n");
    reverseK2 = reverseDigraph(cloneK2);
    freeDigraph(cloneK2);
    s = toString(reverseK2);
    V = vDigraph(reverseK2);
    E = eDigraph(reverseK2);
    printf("reverse K2 (%d vertices, %d edges): %s", V, E, s);
    free(s);
    freeDigraph(reverseK2);

    /*---------------------------------------*/
    printf("-----\nteste readDigraph()\n");
    tinyDG   = readDigraph("tinyDG.txt");
    s = toString(tinyDG);
    printf("tinyDG: %s", s);
    free(s);
    freeDigraph(tinyDG);
    
    mediumDG = readDigraph("mediumDG.txt");
    printf("mediusDG: %d vertices, %d edges\n", vDigraph(mediumDG), eDigraph(mediumDG));
    freeDigraph(mediumDG);
    
    largeDG  = readDigraph("largeDG.txt");
    printf("largeDG: %d vertices, %d edges\n", vDigraph(largeDG), eDigraph(largeDG));
    freeDigraph(largeDG);
    
    return EXIT_SUCCESS;
}
