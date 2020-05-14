// MAC0328 (2019) Algoritmos em Grafos
// Aluno:      PEDRO GIGECK FREIRE
// Número USP: 10737136
// Tarefa:     C
// Data:       2019-08-29
//
// DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESTE PROGRAMA. TODAS
// AS PARTES DO PROGRAMA, EXCETO AS QUE FORAM FORNECIDAS PELO PROFESSOR
// OU COPIADAS DO LIVRO OU DAS BIBLIOTECAS DE SEDGEWICK OU ROBERTS,
// FORAM DESENVOLVIDAS POR MIM.  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR
// TODAS AS EVENTUAIS CÓPIAS DESTE PROGRAMA E QUE NÃO DISTRIBUI NEM
// FACILITEI A DISTRIBUIÇÃO DE CÓPIAS. 
//
////////////////////////////////////////////////////////////////////////

#include "bib/GRAPHlists.h"
#include "time.h"


// O programa gera um grafo aleatório e, através de 3 estratégias,
// verifica a presença de ciclos no Grafo, caso exista, o ciclo é
// printado, caso contrário, printa uma permutação topológica dos vértices

// Função auxiliar privada que recebe um vetor de vétices
// e os imprime na saída padrão na ordem reversa (direita -> esquerda)
void printVertexSeq( vertex *vertices, int n, char separador) {
   for (int i = n - 1; i > 0; --i)
      printf( "%d%c", vertices[i], separador);
   printf( "%d\n", vertices[0]);
}

bool CouT1( Graph G) {
   int *pre = mallocc( G->V * sizeof (int));
   int *post = mallocc( G->V * sizeof (int));
   int *pa = mallocc( G->V * sizeof (vertex));
   GRAPHdfs( G, pre, post, pa);
   // para não precisar alocar outros vetores, 
   // aproveitaremos o vetor da pre ordem
   int *ciclo = pre;
   int *top  = pre;
   for (vertex v = 0; v < G->V; ++v) {
      for (link a = G->adj[v]; a != NULL; a = a->next) {
         vertex w = a->w;
         if (post[v] < post[w]) { // v-w é de retorno
            int tamCiclo = 0;
	         for( vertex c = v; c != w; c = pa[c])
               ciclo[tamCiclo++] = c;
            ciclo[tamCiclo++] = w;
            ciclo[tamCiclo++] = v;
	         printVertexSeq(ciclo, tamCiclo, '-');
            free( pre);
            free( post);
            free( pa);
	         return true;
         }
      }
   }
   // post[v] > post[w] para todo arco v-w
   // portanto post é uma numeração anti-topológica
	for (vertex v = 0; v < G->V; ++v)
		top[post[v]] = v;
   printVertexSeq( top, G->V, ' ');
   free( pre);
   free( post);
   free( pa);
   return false;
}

// A função privada dfsRcycle() devolve true se encontra
// um ciclo ao fazer uma DFS em G a partir do vértice v e
// retorna os valores nos parâmetros passados
static bool dfsRcycle( Graph G, vertex v, int *pre, int *post, int *ciclo, int *cnt, int *cntt, int *tamCiclo, bool *fechouCiclo) { 
   pre[v] = (*cnt)++;
   for (link a = G->adj[v]; a != NULL; a = a->next) {
      vertex w = a->w;
      if (pre[w] == -1) {
         if (dfsRcycle( G, w, pre, post, ciclo, cnt, cntt, tamCiclo, fechouCiclo)) {
            if ( !(*fechouCiclo)) {
               ciclo[ (*tamCiclo)++] = w;
               if ( ciclo[0] == ciclo[*tamCiclo - 1])
                  *fechouCiclo = true;
               return true;
            }
         }
      } else {
         if (post[w] == -1) {
            ciclo[ (*tamCiclo)++] = w;
            return true; // base da recursão
         }
      }
   }
   post[v] = (*cntt)++;
   return false;
}

bool CouT2( Graph G) {
   int *pre = mallocc( G->V * sizeof (int));
   int *post = mallocc( G->V * sizeof (int));
   int *ciclo = mallocc( G->V * sizeof (vertex));
   int cnt = 0, cntt = 0, tamCiclo = 0;
   bool fechouCiclo = false;
   for (vertex v = 0; v < G->V; ++v)
      pre[v] = post[v] = -1;
   for (vertex v = 0; v < G->V; ++v)
      if (pre[v] == -1){
         if (dfsRcycle( G, v, pre, post, ciclo, &cnt, &cntt, &tamCiclo, &fechouCiclo)) {
            if (!fechouCiclo)
               ciclo[tamCiclo++] = v;
            printVertexSeq( ciclo, tamCiclo, '-');
            free( pre);
            free( post);
            free( ciclo);
            return true;
         }
      }
   // nao encontrou ciclo e post é anti-topológico
   int *top = ciclo;
   for (vertex v = 0; v < G->V; ++v)
	   top[ post[v]] = v;
   printVertexSeq( top, G->V, ' ');
   free( pre);
   free( post);
   free( ciclo);
   return false;
}

bool CouT3( Graph G) {
   int *indeg = mallocc( G->V * sizeof (int));
   int *topo = mallocc( G->V * sizeof (vertex));
   for (vertex v = 0; v < G->V; ++v) indeg[v] = 0;
   for (vertex v = 0; v < G->V; ++v) 
      for (link a = G->adj[v]; a != NULL; a = a->next)
         indeg[a->w] += 1;
   vertex *fila = mallocc( G->V * sizeof (vertex));
   int comeco = 0, fim = 0;
   for (vertex v = 0; v < G->V; ++v)
      if (indeg[v] == 0) 
         fila[fim++] = v;
   int k = 0;
   while (comeco < fim) { 
      // fila[comeco..fim-1] de fontes virtuais
      vertex v = fila[comeco++];
      topo[v] = k++;
      for (link a = G->adj[v]; a != NULL; a = a->next) {
         indeg[a->w] -= 1; // remoção virtual do arco v-w
         if (indeg[a->w] == 0) 
            fila[fim++] = a->w;
      }
   }
   if (k >= G->V) {
      for (int i = 0; i < G->V - 1; ++i)
         printf( "%d ", fila[i]);
      printf( "%d\n", fila[G->V - 1]);
      free( indeg); free( fila); free( topo);
      return true;
   }
   free( indeg); free( fila); free( topo);
   // Para não repetir o código de uma dfs que seria muito parecido
   return CouT2( G);
}

int main( int argc, char *argv[]) {
   if( argc < 4) {
      printf( "Erro: esperava pelo menos 3 argumentos\n");
      return 1;
   }
   int V = atoi( argv[1]);
   int A = atoi( argv[2]);
   srand( atoi( argv[3]));
   if( A > V * (V - 1)) {
      printf( "Erro: Número de arestas incoerente\n");
      return 2;
   }
   Graph G;
   if ( A < V * (V - 1) / 2) G = GRAPHrand1( V, A);
   else G = GRAPHrand2( V, A);
   // GRAPHshow( G); // para debug
   clock_t t = clock();
   bool c1 = CouT1( G);
   t = clock() - t;
   printf( "CouT1: %f seg\n", t / (float) CLOCKS_PER_SEC);
   t = clock();
   bool c2 = CouT2( G);
   t = clock() - t;
   printf( "CouT2: %f seg\n", t / (float) CLOCKS_PER_SEC);
   t = clock();
   bool c3 = CouT3( G);
   t = clock() - t;
   printf( "CouT3: %f seg\n", t / (float) CLOCKS_PER_SEC);
   if (!(c1 == c2 == c3)) printf( "Alerta: retornos booleanos diferentes!\n");
   return 0;
}
