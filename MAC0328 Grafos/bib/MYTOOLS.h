// MAC0328 (2019) 
// Altere e modifique à vontade. Mas observe o meu bom layout (veja
// www.ime.usp.br/~pf/algoritmos/aulas/layout.html) e não use tabs
// (exceto no começo das linhas).

// Este arquivo: MYTOOLS.h (codificação UTF-8)
// Data: 2019-07-17     
// Autor: Paulo Feofiloff
//
// Esta é a interface de minha biblioteca particular que contém algumas 
// ferramentas genéricas muito básicas.
////////////////////////////////////////////////////////////////////////


#ifndef _MYTOOLS_h
#define _MYTOOLS_h

#include <stdlib.h> // malloc() e free()
#include <stdio.h> // printf()

// Muitas funções usam strings.
typedef char *string;

// Minha versão de malloc interrompe execução da função se malloc
// devolve NULL.
void *
mallocc( size_t n);

// Esta função rearranja o vetor v[p..r] em ordem crescente. (Veja
// www.ime.usp.br/~pf/algoritmos/aulas/quick.html.)
void 
quickSort( int v[], int p, int r);

// Em lugar de minha função quicksort(), é melhor usar a poderosa função
// qsort() da biblioteca padrão stdlib. Essa função é muito genérica e
// por isso exige que o cliente defina uma função de comparação comp().
//
// Exemplo: A função comp() compara inteiros apontados por elem1 e
// elem2. Devolve -1 se *elem1 é menor que *elem2, devolve +1 se *elem1
// é maior que *elem2, devolve 0 se *elem1 é igual a *elem2.
int 
comp( const void *elem1, const void *elem2);

#endif
