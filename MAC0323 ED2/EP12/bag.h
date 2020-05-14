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
 */

/* 
 * BAG
 *
 * Um saco (= bag) é um ADT que consiste em uma coleção de coisas ou itens munida 
 * basicamente de duas operações:  
 *
 *     - add(), que insere um item na coleção; e 
 *     - itens(), que é usada para percorre os itens da coleção.
 *  
 * A ordem em que itens() percorre as coisas da coleção não é especificada e está 
 * fora do controle do cliente.
 *
 * Esta implementação usa listas ligada de itens.
 *
 * As operações add() e itens(), além de isEmpty() e size() consomem tempo constante.
 *
 * Para documentação adicional, veja 
 * https://algs4.cs.princeton.edu/13stacks/Bag.java.html
 * Algorithms, 4th Edition, por Robert Sedgewick e Kevin Wayne.
 */

#ifndef _BAG_H
#define _BAG_H

#include <stddef.h> /* size_t */
#include "util.h"   /* Bool */

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
add(Bag bag, const void *item, size_t nItem);

/* retorna o numero de itens na Bag */
int
size(Bag bag);

/* retorna TRUE se Bag está vazia e FALSE em caso contrário */
Bool
isEmpty(Bag bag);

/* all of the items, as an Iterable */
void *
itens(Bag bag, Bool init);

#endif /* _BAG_H */
