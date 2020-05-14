// MAC0328 (2019) Algoritmos em Grafos
// Aluno:      PEDRO GIGECK FREIRE
// Número USP: 10737136
// Tarefa:     E
// Data:       2019-09-12
//
// DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESTE PROGRAMA. TODAS
// AS PARTES DO PROGRAMA, EXCETO AS QUE FORAM FORNECIDAS PELO PROFESSOR
// OU COPIADAS DO LIVRO OU DAS BIBLIOTECAS DE SEDGEWICK OU ROBERTS,
// FORAM DESENVOLVIDAS POR MIM.  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR
// TODAS AS EVENTUAIS CÓPIAS DESTE PROGRAMA E QUE NÃO DISTRIBUI NEM
// FACILITEI A DISTRIBUIÇÃO DE CÓPIAS.
//
////////////////////////////////////////////////////////////////////////

#include "GRAPHlists.h"

// Função que recebe um Grafo não dirigido G e retorna
// true se G é aresta-biconexo e false caso contrário
bool UGRAPHisEdgeBiconnected( UGraph G) {
    if( !UGRAPHisConnected( G)) return false;
    for (vertex v = 0; v < G->V; ++v)
        for (link a = G->adj[v]; a != NULL; a = a->next) {
            vertex w = a->w;
            UGRAPHremoveEdge( G, v, w);
            if( !GRAPHreach( G, v, w)) return false;
            UGRAPHinsertEdge( G, v, w);
        }
    return true;
}
