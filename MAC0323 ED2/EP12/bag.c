/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * ADT Bag implementada com lista ligada de itens. 
 *  
 *    https://algs4.cs.princeton.edu/13stacks/
 *    https://www.ime.usp.br/~pf/estruturas-de-dados/aulas/bag.html
 * 
 * Os itens desta implementação são genéricos: "shallow copy" dos itens dados.
 *
 *----------------------------------------------------------------------------
 * Object copying
 * https://en.wikipedia.org/wiki/Object_copying
 * 
 * Understanding Deep and Shallow Copy 
 * https://we-are.bookmyshow.com/understanding-deep-and-shallow-copy-in-javascript-13438bad941c
 *
 * Shallow copy is a bit-wise copy of an object. A new object is created that has an 
 * exact copy of the values in the original object. If any of the fields of the object 
 * are references to other objects, just the reference addresses are copied i.e., 
 * only the memory address is copied.
 
 * A deep copy copies all fields, and makes copies of dynamically allocated memory 
 * pointed to by the fields. A deep copy occurs when an object is copied along with the 
 * objects to which it refers.
 *
 */

/* interface para o uso da funcao deste módulo */
#include "bag.h"  

#include <stdlib.h>  /* free() */
#include <string.h>  /* memcpy() */
#include "util.h"    /* emalloc() */

#undef DEBUG
#ifdef DEBUG
#include <stdio.h>   /* printf(): para debuging */
#endif

/*----------------------------------------------------------*/
/* 
 * Estrutura Básica da Bag
 * 
 * Implementação com listas ligada dos itens.
 */

/* Estrutura dos nós da lista (itens do bag) */
struct node {
	
	void* val;
	size_t sizeVal;
	struct node * next;
};

typedef struct node* Node;

struct bag {
	
	/* Numero de elementos no bag */
	int n;		
	/* Primeiro da lista */
	Node first; 
	/* Próximo item do iterador */
	Node next;
};

/*-----------------------------------------------------------*/
/*
 *  newBag()
 *
 *  RETORNA (referência/ponteiro para) uma bag vazia.
 * 
 */
Bag
newBag()
{
	/* Alocando memória */
	Bag novo = emalloc(sizeof(struct bag));
	
	/* Setando atributos iniciais */
	novo->n = 0;
	novo->first = NULL;
	novo->next = NULL;
	
    return novo;
}

/*-----------------------------------------------------------*/
/*
 *  freeBag(BAG)
 *
 *  RECEBE uma Bag BAG e devolve ao sistema toda a memoria 
 *  utilizada.
 *
 */
void  
freeBag(Bag bag)
{
	/* Limpa os nós da lista */
	while(bag->first != NULL){
		Node prox = bag->first->next;
		
		free(bag->first->val);
		free(bag->first);
		bag->first = prox;	
	}
	/* Limpa o bag */
	free(bag);
}    

/*------------------------------------------------------------*/
/*
 * OPERAÇÕES USUAIS: add(), size(), isEmpty() e itens().
 */

/*-----------------------------------------------------------*/
/*
 *  add(BAG, ITEM, NITEM)
 * 
 *  RECEBE uma bag BAG e um ITEM e insere o ITEM na BAG.
 *  NITEM é o número de bytes de ITEM.
 *
 *  Para criar uma copia/clone de ITEM é usado o seu número de bytes NITEM.
 *
 */
void  
add(Bag bag, const void *item, size_t nItem)
{
	/* Cria o nó */
	Node novo;
	novo = emalloc(sizeof(struct node));
	
	/* Seta os atributos */
	novo->sizeVal = nItem;
	novo->val = emalloc(nItem);
	memcpy(novo->val, item, nItem);
	
	/* Insere no início da lista */
	novo->next = bag->first;
	bag->first = novo;
	
	bag->n++;
}    

/*-----------------------------------------------------------*/
/* 
 *  SIZE(BAG)
 *
 *  RECEBE uma bag BAG
 * 
 *  RETORNA o número de itens em BAG.
 */
int
size(Bag bag)
{
	return bag->n;
}

/*-----------------------------------------------------------*/
/* 
 *  ISEMPTY(BAG)
 *
 *  RECEBE uma bag BAG.
 * 
 *  RETORNA TRUE se BAG está vazia e FALSE em caso contrário.
 *
 */
Bool
isEmpty(Bag bag)
{
    return bag->n == 0;
}

/*-----------------------------------------------------------*/
/* 
 *  ITENS(BAG, INIT)
 * 
 *  RECEBE uma bag BAG e um Bool INIT.
 *
 *  Se INIT é TRUE,  ITENS() RETORNA uma cópia/clone do primeiro item na lista de itens na BAG.
 *  Se INIT é FALSE, ITENS() RETORNA uma cópia/clone do item sucessor do último item retornado.
 *  Se BAG está vazia ou não há sucessor do último item retornada, ITENS() RETORNA NULL.
 *
 *  Se entre duas chamadas de ITENS() a BAG é alterada, o comportamento é  indefinido. 
 *  
 */
void * 
itens(Bag bag, Bool init)
{
	void* copia;
	
	/* Se init, o próximo será o primeiro do bag */
	if(init) bag->next = bag->first;
		
	/* Se o bag não tem mais próximo, return NULL */
	if(bag->next == NULL) return NULL;
	
	/* Cria uma copia do proximo */
	copia = emalloc(bag->next->sizeVal);
	memcpy(copia, bag->next->val, bag->next->sizeVal);
	
	/* Atualiza o próximo */
	bag->next = bag->next->next;
	
    return copia;
}
