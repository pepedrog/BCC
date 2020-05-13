/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * NAO EDITE OU MODIFIQUE NADA QUE ESTA ESCRITO NESTE ARQUIVO
 *
 * Interface levemente modificada para uma ADT bag implementada 
 * através de lista ligadas de itens como descrita em 
 *  
 *    https://algs4.cs.princeton.edu/13stacks/
 *    https://www.ime.usp.br/~pf/estruturas-de-dados/aulas/bag.html
 * 
 * ATENÇÃO: por simplicidade Bag contém apenas inteiros (int) não 
 * negativos (>=0) que são 'nomes' de vértices (vertex = int) de 
 * um digrafo.
 */

#ifndef _BAG_H
#define _BAG_H

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

typedef struct bag *Bag;

/*-----------------------------------------------------------*/
/*  prototipos das funcoes que manipulam uma bag             */

/*-----------------------------------------------------------*/
/* 
 *  Construtor e "destrutor"
 */
/* 
 *  newBag()
 *
 *  cria uma bag vazia 
 
 */
Bag
newBag();

/* libera todo o espaço usado pela Bag */
void  
freeBag(Bag bag);

/*------------------------------------------------------------*/
/*
 * Permite as operações usuais: add(), isEmpty(), size() e itens().
 */

/* coloca um item na Bag */
void  
add(Bag bag, vertex item);

/* retorna o numero de itens na Bag */
int
size(Bag bag);

/* retorna TRUE se Bag está vazia e FALSE em caso contrário */
Bool
isEmpty(Bag bag);

/* all of the items, as an Iterable */
vertex
itens(Bag bag, Bool init);

#endif /* _BAG_H */
