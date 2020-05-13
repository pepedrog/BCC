// MAC0328 (2019) 
// Altere e modifique à vontade. Mas observe o meu bom layout (veja
// www.ime.usp.br/~pf/algoritmos/aulas/layout.html) e não use tabs
// (exceto no começo das linhas).

// Este arquivo: MYTOOLS.c (codificação UTF-8)
// Data: 2019-07-17
// Autor: Paulo Feofiloff
//
// Esta é a implementação de minha biblioteca particular de ferramentas 
// genéricas muito básicas.
////////////////////////////////////////////////////////////////////////


#include "MYTOOLS.h"
// contém a interface padrão stdlib.h

// Minha versão de malloc.
void *
mallocc( size_t n) {
   void *pointer = malloc( n);
   if (pointer == NULL) {
      fprintf( stderr, "\nmalloc devolveu NULL!\n"); 
      exit( EXIT_FAILURE);
   }
   return pointer;
}

// Função auxiliar usada por de quickSort(). Rearanja os elementos do
// vetor v[p..r] (com p <= r) e devolve j em p..r tal que
//         v[p..j-1] <= v[j] < v[j+1..r].
// (Veja www.ime.usp.br/~pf/algoritmos/aulas/quick.html.)
static int
separa( int v[], int p, int r) {
   int c = v[r]; // pivô
   int t, j = p;
   for (int k = p; k < r; ++k)
      if (v[k] <= c) {
         t = v[j], v[j] = v[k], v[k] = t;
         ++j; 
      } 
   t = v[j], v[j] = v[r], v[r] = t;
   return j; 
}

void 
quickSort( int v[], int p, int r) {
   while (p < r) {      
      int j = separa (v, p, r);    
      if (j - p < r - j) {     
         quickSort (v, p, j-1);
         p = j + 1;            
      } else {                 
         quickSort (v, j+1, r);
         r = j - 1;
      }
   }
}

int 
comp (const void *a, const void *b) {
    int x = *((int *) a);
    int y = *((int *) b);
    if (x < y) return -1;
    if (x > y) return  1;
    return 0;
}

