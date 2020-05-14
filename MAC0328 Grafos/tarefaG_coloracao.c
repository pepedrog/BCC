// MAC0328 (2019) Algoritmos em Grafos
// Aluno:      PEDRO GIGECK FREIRE
// Número USP: 10737136
// Tarefa:     G
// Data:       2019-10-03
//
// DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESTE PROGRAMA. TODAS
// AS PARTES DO PROGRAMA, EXCETO AS QUE FORAM FORNECIDAS PELO PROFESSOR
// OU COPIADAS DO LIVRO OU DAS BIBLIOTECAS DE SEDGEWICK OU ROBERTS,
// FORAM DESENVOLVIDAS POR MIM.  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR
// TODAS AS EVENTUAIS CÓPIAS DESTE PROGRAMA E QUE NÃO DISTRIBUI NEM
// FACILITEI A DISTRIBUIÇÃO DE CÓPIAS. 
//
////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include "time.h"
#include "GRAPHlists.h"

bool coloracaoValida( UGraph G, int color[]) {
    for (vertex v = 0; v < G->V; v++)
        for (link a = G->adj[v]; a != NULL; a = a->next)
            if (color[a->w] == color[v])
                return false;
    return true;
}

// Versão aleatorizada da heurística de coloração sequencial
int UGRAPHrandSeqColoring( UGraph G, int color[]) { 
    int k = 0;
    for (vertex v = 0; v < G->V; ++v) color[v] = -1;
    bool *disponivel = mallocc( G->V * sizeof (int));
    for (int j = 0; j < G->V; ++j) {
        vertex v = rand() / (RAND_MAX + 1.0) * G->V;
        // sorteia um vértice e pega o próximo a partir dele sem cor
        while (color[v] != -1) v = (v + 1) % G->V;
        int i;
        for (i = 0; i < k; ++i) 
            disponivel[i] = true;
        for (link a = G->adj[v]; a != NULL; a = a->next) {
            i = color[a->w];
            if (i != -1) disponivel[i] = false;
        } // disponivel[0..k-1] dá as cores disponíveis para v
        for (i = 0; i < k; ++i) 
            if (disponivel[i]) break;
        if (i < k) color[v] = i;
        else color[v] = k++;
    }
    free( disponivel);
    return k;
}

// Versão da heuristica de coloração sequencial que colore os vértices
// por ordem decrescente de grau
int UGRAPHdegreeSeqColoring( UGraph G, int color[]) {
    // Cria a fila ordenada em ordem decrescente de grau
    PQinit( G->V);
    int *grau = malloc( G->V * sizeof( int));
    for (vertex v = 0; v < G->V; ++v) {
        grau[v] = G->V - GRAPHoutdeg( G, v);
        PQinsert( v, grau);
    }
    int k = 0;
    bool *disponivel = mallocc( G->V * sizeof (int));
    while (!PQempty()) {
        vertex v = PQdelmin( grau);
        int i;
        for (i = 0; i < k; ++i) 
            disponivel[i] = true;
        for (link a = G->adj[v]; a != NULL; a = a->next) {
            i = color[a->w];
            if (i != -1) disponivel[i] = false;
        } // disponivel[0..k-1] dá as cores disponíveis para v
        for (i = 0; i < k; ++i) 
        if (disponivel[i]) break;
        if (i < k) color[v] = i;
        else color[v] = k++;
    }
    free( disponivel);
    free( grau);
    PQfree();
    return k;
}

// Uma coloração sequecial com DFS
int dfsColor( Graph G, vertex v, int color[], int k) {
    bool *disponivel = malloc( k * sizeof( bool));
    int cor;
    for (cor = 0; cor < k; ++cor) disponivel[cor] = true;
    for (link a = G->adj[v]; a != NULL; a = a->next)
        if (color[a->w] != -1) disponivel[ color[a->w]] = false;
    for (cor = 0; cor < k; ++cor)
        if (disponivel[cor]) break;
    if (cor < k) color[v] = cor;
    else color[v] = k++;
    for (link a = G->adj[v]; a != NULL; a = a->next)
        if (color[a->w] == -1) {
            int c = dfsColor( G, a->w, color, k);
            if (c > k) k = c;
        }
    free( disponivel);
    return k;
}

int UGRAPHdfsSeqColoring( UGraph G, int color[]) {
    int k = 0, c = 0;
    for (vertex v = 0; v < G->V; ++v)
        if (color[v] == -1) {
            c = dfsColor( G, v, color, 0); // nova etapa
            if (c > k) k = c;
        }
    return k;
}

// Heuristica de Brelaz
// Função auxiliar que calcula a quantas cores diferentes um vertice é adjacente
int coresAdj( UGraph G, int color[], vertex v, bool disponivel[]) {
    for (int i = 0; i < G->V; ++i) disponivel[i] = true;
    for (link a = G->adj[v]; a != NULL; a = a->next)
        if (color[a->w] != -1) disponivel[ color[a->w]] = false;
    int adj = 0;
    for (int i = 0; i < G->V; ++i) if (!disponivel[i]) adj++;
    return adj;
}

int UGRAPHbrelazSeqColoring( UGraph G, int color[], int k) {
    bool *disponivel = malloc( k * sizeof( int));
    // Escolhe o vértice adjacente a mais cores (desempatando pelo grau)
    vertex maior = 0;
    int adjMaior = -1;
    for (vertex v = 0; v < G->V; ++v) {
        if (color[v] == -1) {
            int adj = coresAdj( G, color, v, disponivel);
            if (adj > adjMaior || (adj == adjMaior
                && GRAPHoutdeg( G, maior) < GRAPHoutdeg( G, v))) {
                maior = v;
                adjMaior = adj;
            }
        }
    }
    int cor;
    if (color[maior] != -1) return k;
    for (cor = 0; cor < k; ++cor) disponivel[cor] = true;
    for (link a = G->adj[maior]; a != NULL; a = a->next)
        if (color[a->w] != -1) disponivel[ color[a->w]] = false;
    for (cor = 0; cor < k; ++cor)
        if (disponivel[cor]) break;
    if (cor < k) color[maior] = cor;
    else color[maior] = k++;
    /*
        int i;
    for (i = 0; i < k; ++i) 
        if (disponivel[i]) break;
    if (i < k) color[maior] = i;
    else color[maior] = k++;
    */
    free( disponivel);
    return UGRAPHbrelazSeqColoring( G, color, k);
}

// Funções para o algoritmo força bruta
// Função que retorna em color[] a próxima permutação de coloração
// do grafo e retorna false se já a permutação atual é a última
bool proxPermutation( int color[], int k, int n, int nori) {
    //base da recursão
    if (n == 1) {
        if (color[0] == k) {
            color[0] = 0;
            return false;
        }
        else {
            color[0]++;
            return true;
        }
    }
    // Permuta os outros n - 1 elementos
    if (proxPermutation( color, k, n - 1, nori)) return true;
    if (color[n - 1] == nori - n || color[n - 1] >= k) {
        color[n - 1] = 0;
        return false;
    }
    color[n - 1]++;
    return true;
}

// Função que testa todas as permutações possíveis para k cores
bool kcoloring( UGraph G, int color[], int k) {
    printf( "testando com %d cor(es)...\n", k + 1);
    for (int i = 0; i < G->V; ++i) color[i] = 0;
    if (coloracaoValida( G, color)) return true;
    while (proxPermutation( color, k, G->V, G->V)) {
        if (coloracaoValida( G, color)) return true;
    }
    return false;
}

// Função wrapper para o algoritmo ingênuo (ineficiente) de força bruta
int UGRAPHbruteColoring( UGraph G, int color[]) {
   int k = 0;
   while (!kcoloring( G, color, k)) k++;
   return k + 1;
}

int main( int argc, char* argv[]) {
    int V, E, s, k;
    int *color;
    clock_t t;
    if (argc < 4) {
        printf( "ERRO: argumetos incorretos\n");
        return 1;
    }
    V = atoi( argv[1]);
    E = atoi( argv[2]);
    s = atoi( argv[3]);
    if (E > V  * (V - 1) / 2){
        printf( "ERRO: Número de arestas muito grande\n");
        return 2;
    }
    color = malloc( V * sizeof( int));
    srand( s);
    printf( "Gerando o grafo...\n");
    t = clock();
    Graph G = UGRAPHrand1( V, E);
    t = clock() - t;
    printf( "Grafo gerado, tempo consumido = %f\n", (float) t / CLOCKS_PER_SEC);
    printf("-------------------------------------------------------\n");
    
    // Coloração sequencial
    for (vertex v = 0; v < G->V; ++v) color[v] = -1;
    t = clock();
    k = UGRAPHseqColoring( G, color);
    t = clock() - t;
    printf( "Coloração sequencial: %d cores\n%fs\n", k, (float) t / CLOCKS_PER_SEC);
    if (!coloracaoValida( G, color)) printf( "coloração inválida\n");
    printf("-------------------------------------------------------\n");

    // Coloração sequencial Aleatorizada
    for (vertex v = 0; v < G->V; ++v) color[v] = -1;
    t = clock();
    k = UGRAPHrandSeqColoring( G, color);
    t = clock() - t;
    printf( "Coloração sequencial aleatorizada: %d cores\n%fs\n", k, (float) t / CLOCKS_PER_SEC);
    if (!coloracaoValida( G, color)) printf( "coloração inválida\n");
    printf("-------------------------------------------------------\n");

    // Coloração sequencial por ordem decrescente de grau
    for (vertex v = 0; v < G->V; ++v) color[v] = -1;
    t = clock();
    k = UGRAPHdegreeSeqColoring( G, color);
    t = clock() - t;
    printf( "Coloração sequencial por ordem decrescente de grau: %d cores\n%fs\n", k, (float) t / CLOCKS_PER_SEC);
    if (!coloracaoValida( G, color)) printf( "coloração inválida\n");
    printf("-------------------------------------------------------\n");

    // Coloração sequencial com DFS
    for (vertex v = 0; v < G->V; ++v) color[v] = -1;
    t = clock();
    k = UGRAPHdfsSeqColoring( G, color);
    t = clock() - t;
    printf( "Coloração sequencial com DFS: %d cores\n%fs\n", k, (float) t / CLOCKS_PER_SEC);
    if (!coloracaoValida( G, color)) printf( "coloração inválida\n");
    printf("-------------------------------------------------------\n");

    // Heurística de Brelaz
    for (vertex v = 0; v < G->V; ++v) color[v] = -1;
    t = clock();
    k = UGRAPHbrelazSeqColoring( G, color, 0);
    t = clock() - t;
    printf( "Heurística de Brelaz: %d cores\n%fs\n", k, (float) t / CLOCKS_PER_SEC);
    if (!coloracaoValida( G, color)) printf( "coloração inválida\n");
    printf("-------------------------------------------------------\n");

    // Força bruta
    // Apenas se o grafo for pequeno
    if (V > 15) return 0;
    char resp;
    printf( "Deseja rodar o algoritmo força bruta ? (S/N)\n(Pode levar muito tempo)\n");
    scanf( "%c", &resp);
    if (resp == 'N') return 0;
    t = clock();
    k = UGRAPHbruteColoring( G, color);
    t = clock() - t;
    printf( "Algoritmo força bruta: %d cores\n%fs\n", k, (float) t / CLOCKS_PER_SEC);
    if (!coloracaoValida( G, color)) printf( "coloração inválida\n");
        
    return 0;
}

//////////////////////////////////////////////////////////////////////
//
// Relatório
// 
// A primeira constatação interessante que tive foi sobre
// a inviabilidade do algoritmo força bruta
// Para grafos com mais de 10 vértices e minimamente densos
// não consegui terminar mesmo após 1 dia inteiro de processamento!
//
// Depois, sobre as heurísticas gulosas, a que na grande maioria das
// vezes devolveu uma coloração com menos cores foi a heurístca de
// Brelaz, porém sempre levava muito mais tempo que as outras.
// Isso porque ela percorre mais vezes os vizinhos de cada vértice.
// Para vértices muito densos, ela pode deixar bastante a desejar.
// 
// A heurística ingênua de colorir durante a DFS se mostrou também
// bastante eficiente, fornecendo quase sempre menos cores que a
// coloração sequêncial pura.
//
// A heurística campeã, na minha perpepção com os testes, pela relação
// custo benefício (tempo vs cores) é a que colore os vértices pela
// ordem decrescente de grau !
//
//////////////////////////////////////////////////////////////////////