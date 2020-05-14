/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * NAO EDITE OU MODIFIQUE NADA QUE ESTA ESCRITO NESTE ARQUIVO
 *
 * Interface levemente modificada para a tabela de simbolos 
 * implementada atraves de uma BST rubro-negra (RedBlackST)
 * descrita em 
 *  
 *   https://algs4.cs.princeton.edu/33balanced/
 */


/* 
 * REDBLACKST
 *
 * Representa uma tabela de símbolos (ST) ordenada "genérica".
 *
 * Permite as operações usuais: put(), get(), contains(), delete(), size() 
 * e isEmpty().
 *
 * Fornece algumas operações para tabelas de símbolos ordenadas: min(), 
 * max(), rank(), select(), deleteMin() e deleteMax().
 *
 * Também fornece a operação keys() para iterar todas as chaves.
 *
 * Uma tabela de símbolos implementa a abstração "array associativo":
 * ao associar um valor a uma chave que já está na tabela de símbolos,
 * a convenção é substituir o valor antigo pelo novo valor.
 *
 * Ao contrário de java.util.Map, essa implementação usa a convenção de que
 * os valores não podem ser NULL - associar o valor de uma chave para NULL
 * é equivalente a excluir a chave da tabela de símbolos.
 * 
 * Esta implementação usa uma árvore rubro-negra.
 * Requer que uma função compar() seja argumento do construtor.
 *
 * As operações put(), get(), delete(), deleteMin(), deleteMax(), 
 * contains(), select(), rank(), min(), max() consomem  tempo 
 * logarítmico.
 * As operações size(), isEmpty() consomem tempo constante.
 *
 * Para documentação adicional, veja 
 * https://algs4.cs.princeton.edu/33balanced, Seção 3.3
 * Algorithms, 4th Edition, por Robert Sedgewick e Kevin Wayne.
 */

#ifndef _REDBLACKST_H
#define _REDBLACKST_H

#include <stddef.h> /* size_t */
#include "util.h"   /* Bool */

typedef struct redBlackST *RedBlackST;

/*-----------------------------------------------------------*/
/*  prototipos das funcoes que manipulam a tabela de simbolos */

/*-----------------------------------------------------------*/
/* 
 *  Construtor e "destrutor"
 */
/* 
 *  INIT(COMPAR)
 *
 *  cria uma ST vazia 
 *  compar() é ponteiro para uma função que retorna um inteiro tal que
 *
 *      compar(key1, key2) retorna um inteiro < 0 se key1 <  key2
 *      compar(key1, key2) retorna um 0           se key1 == key2
 *      compar(key1, key2) retorna um inteiro > 0 se key1 >  key2
 */
RedBlackST
initST(int (*compar)(const void *this, const void *that));

/* libera todo o espaço usado pela ST */
void  
freeST(RedBlackST st);

/*------------------------------------------------------------*/
/*
 * Permite as operações usuais: put(), get(), contains(), delete(),
 * size() e isEmpty().
 */

/* coloca um par KEY-VAL na ST */
void  
put(RedBlackST st, const void *key, size_t nKey, const void *val, size_t nVal);

/* retorna o valor associado a KEY */
void * 
get(RedBlackST st, const void *key);

/* retorna TRUE se KEY esta na ST e FALSE em caso contrário */
Bool
contains(RedBlackST st, const void *key);

/* remove da ST a chave KEY */
void
delete(RedBlackST st, const void *key);

/* retorna o numero de itens na ST */
int
size(RedBlackST st);

void printRaiz(RedBlackST st);

/* retorna TRUE se ST esta vazia e FALSE em caso contrário */
Bool
isEmpty(RedBlackST st);

/*------------------------------------------------------------*/
/*
 * Fornece algumas operações para tabelas de símbolos ordenadas: 
 * min(), max(), rank(), select(), deleteMin() e deleteMax().
 */

/* menor chave na ST */
void *
min(RedBlackST st);

/* maior chave na ST */
void *
max(RedBlackST st);

/* numero de chaves menores que key */
int
rank(RedBlackST st, const void *key);

/* remove menor chave */
void
deleteMin(RedBlackST st);
int height(RedBlackST st);

/* remove menor chave */
void
deleteMax(RedBlackST st);

/* a k-ésima chave da ST */
void *
select(RedBlackST st, int k);

/*------------------------------------------------------------*/
/*
 * Também fornece a operação keys() para iterar todas as chaves.
 */

/* all of the keys, as an Iterable */
void *
keys(RedBlackST st, Bool init);

/***************************************************************************
 *  Check integrity of red-black tree data structure.
 ***************************************************************************/
Bool 
check(RedBlackST st);

#endif /* _REDBLACKST_H */
