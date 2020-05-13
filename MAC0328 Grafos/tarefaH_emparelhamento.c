// MAC0328 (2019) Algoritmos em Grafos
// Aluno:      PEDRO GIGECK FREIRE
// Número USP: 10737136
// Tarefa:     H
// Data:       2019-10-30
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
#include "QUEUE.h"

// Função auxiliar que retorna o maior de dois inteiros
int max (int a, int b) {
    if (a > b) return a;
    return b;
}

////////////////////////////////////////////////////////////////////////
//          Exercício 1 - Altura de uma árvore radicada               //
////////////////////////////////////////////////////////////////////////

// Função auxiliar recursiva que faz uma DFS na árvore
// retornando a maior profundidade de um vértice (altura)
int alturaRec (Graph T, bool *visitado, vertex v, int prof)
{
    visitado[v] = true;
    int altura = prof;
    for (link a = T->adj[v]; a != NULL; a = a->next)
        if (!visitado[a->w])
            altura = max (altura, alturaRec (T, visitado, a->w, prof + 1));
    return altura;
}

// Função que recebe uma árvore radicada T com raiz r
int altura (Graph T, vertex r)
{
    int altura = 0;
    bool *visitado = malloc (T->V * sizeof (bool));
    for (vertex v = 0; v < T->V; ++v) visitado[v] = false;
    altura = alturaRec (T, visitado, r, 0);
    return altura;
}

////////////////////////////////////////////////////////////////////////
//                Exercício 2 - Emparelhamento Maximal                //
////////////////////////////////////////////////////////////////////////

// Função que recebe um grafo não-dirigido G, guarda em match[]
// um emparelhamento maximal e devolve o tamanho desse emparelhamento
int emparelhamento (UGraph G, vertex match[]) {
    int tam = 0;
    for (vertex v = 0; v < G->V; v++) match[v] = -1;
    bool *visitado = malloc (G->V * sizeof (bool));
    // Busca em largura para montar o emparelhamento
    QUEUEinit (G->V);
    for (vertex u = 0; u < G->V; u++) {
        if (!visitado[u]) {
            QUEUEput (u);
            while (!QUEUEempty()) {
                vertex v = QUEUEget();
                visitado[v] = true;
                for (link a = G->adj[v]; a != NULL; a = a->next) {
                    vertex w = a->w;
                    if (match[v] == -1 && match[w] == -1) {
                        match[v] = w;
                        match[w] = v;
                        tam++;
                    }
                    if (!visitado[w]) QUEUEput (w);
                }
            }
        }
    }
    return tam;
}

////////////////////////////////////////////////////////////////////////
//               Exercício 3 - Fim do Algoritmo Húngaro               //
////////////////////////////////////////////////////////////////////////

// - É possível que o conjunto X seja vazio ?
// 
// Sim.
// O conjunto X é o conjunto dos vétices visitados pelo algoritmo.
// A primeira tarefa do algoritmo que encontra os caminhos aumentadores
// é marcar como visitado todos os vértices solteiros de cor 0.
//
// Se o conjunto X ficar vazio, então todos os vértices de cor 0 estão casados!
// Isso significa que todo vértice de cor 1 ou está casado ou não tem vizinhos.
// (pois se fosse solteiro haveria um caminho aumentador) 
//
// Além disso, sabemos que (X - C0) U (C0 - X) é uma cobertura, 
// portanto C0 será uma cobertura do grafo!
//
// - É possível que X seja o conjunto de todos os vértices ?
// Sim.
// Como X não é vazio, então existe pelo menos um vértice de cor 0 solteiro.
// Esse vértice vai visitar todos seus vizinhos e seus matchs (sabemos que os 
// vizinhos estão casados pois não há caminhos aumentadores).
// Então todo vértice de cor 1 que está conectado a algum outro vértice, está
// casado.
//
// Com o mesmo raciocínio da cobertura, vemos que nesse caso C1 é uma cobertura
// do mesmo tamanho do emparelhamento.
