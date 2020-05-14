// MAC0328 (2019) Algoritmos em Grafos
// Aluno:      PEDRO GIGECK FREIRE
// Número USP: 10737136
// Tarefa:     I
// Data:       2019-11-20
//
// DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESTE PROGRAMA. TODAS
// AS PARTES DO PROGRAMA, EXCETO AS QUE FORAM FORNECIDAS PELO PROFESSOR
// OU COPIADAS DO LIVRO OU DAS BIBLIOTECAS DE SEDGEWICK, FORAM
// DESENVOLVIDAS POR MIM. DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR TODAS
// AS EVENTUAIS CÓPIAS DESTE PROGRAMA E QUE NÃO DISTRIBUI NEM FACILITEI
// A DISTRIBUIÇÃO DE CÓPIAS. 
//
////////////////////////////////////////////////////////////////////////

#include "GRAPHlists.h"
#include <stdlib.h>

#define min( A, B) (A < B ? A : B)

////////////////////////////////////////////////////////////////////////
//
// EXERCÍCIO A - MACARRONADA
//
// Algoritmo em português:
// macarronada (G, f, s, t)
//    cria um fluxo auxiliar igual a f 
//    enquanto existirem caminhos
//       encontra um caminho
//       printa o caminho e o fluxo que ele conduz
//       retira o fluxo desse caminho do auxiliar
//
////////////////////////////////////////////////////////////////////////

typedef int** fluxo;

// Função auxiliar que recebe um fluxo f, dois vértices s e t
// e encontra um caminho simples de s a t que conduza um fluxo > 0.
// Retorna o fluxo que tal caminho conduz, ou 0 se não há caminho
int encontraCaminho( Graph G, fluxo f, vertex caminho[], vertex s, vertex t) {
    int qfluxo = INT_MAX;
    int i = 0;
    link a;
    while (s != t) {
        for (a = G->adj[s]; a != NULL; a = a->next) {
            vertex w = a->w;
            if (f[s][w] > 0) {
                caminho[i++] = s;
                qfluxo = min( qfluxo, f[s][w]);
                s = w;
                break;
            }
        }
        if (a == NULL) return 0;
    }
    caminho[i] = t;
    return qfluxo;
}

// Função que printa o fluxo f como uma "macarronada" (uma coleção de
// caminhos simples de s a t, onde cada caminho conduz alguma quantidade
// de fluxo)
void macarronada( Graph G, fluxo f, vertex s, vertex t) {
    fluxo aux = malloc( G->V * sizeof *aux);
    for (vertex v = 0; v < G->V; v++) {
        aux[v] = malloc( G->V * sizeof( int));
        for (vertex w = 0; w < G->V; w++) aux[v][w] = f[v][w];
    }
    vertex *caminho = malloc( G->V * sizeof( vertex));
    int f_caminho;
    while ((f_caminho = encontraCaminho( G, aux, caminho, s, t))) {
        for (int i = 0; caminho[i] != t; i++) {
            printf( "%d-", caminho[i]);
            aux[caminho[i]][caminho[i + 1]] -= f_caminho;
        }
        printf( "%d\t fluxo: %d\n", t, f_caminho);
    }
}

////////////////////////////////////////////////////////////////////////
//
// EXERCÍCIO B - FLUXO EM QUASE-ÁRVORE
//
// Algoritmo em português:
// (Bastante simples, onde pilha de recursão cuida do trabalho pesado)
// Fazemos uma DFS na árvore, buscando o vértice t,
// em cada caminho da busca guardamos a quantidade de fluxo máxima
// que tal caminho comporta (a capacidade residual). 
// A quantidade de fluxo de um vértice v será a soma das quantidades
// máximas de cada filho w de v, limitado a capacidade do arco v-w.
//
////////////////////////////////////////////////////////////////////////

// Função que recebe uma "quase-árvore" radicada G com raiz em s 
// e retorna a intensidade de um fluxo máximo de s a t
int fluxoMax( Graph G, vertex s, vertex t) {
    if (s == t) return INT_MAX;
    int qfluxo = 0;
    for (link a = G->adj[s]; a != NULL; a = a->next) 
        qfluxo += min( a->cap, fluxoMax( G, a->w, t));
    return qfluxo;
}
