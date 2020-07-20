/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * ADT Bag implementada com lista ligada de itens. 
 *  
 *    https://algs4.cs.princeton.edu/13stacks/
 *    https://www.ime.usp.br/~pf/estruturas-de-dados/aulas/bag.html
 * 
 * ATENÇÃO: por simplicidade Bag contém apenas inteiros (int) não 
 * negativos (>=0) que são 'nomes' de vértices (vertex) de um 
 * digrafo.
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
struct node {	
	int val;
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


/*------------------------------------------------------------*/
/* 
 * Protótipos de funções administrativas: tem modificador 'static'
 * 
 */

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
add(Bag bag, vertex item)
{
	
	/* Cria o nó */
	Node novo;
	novo = emalloc(sizeof(struct node));
	
	/* Seta os atributos */
	novo->val = item;
	
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
 *  Se BAG está vazia ou não há sucessor do último item retornado, ITENS() RETORNA -1.
 *
 *  Se entre duas chamadas de ITENS() a BAG é alterada, o comportamento é  indefinido. 
 *  
 */
vertex 
itens(Bag bag, Bool init)
{
	vertex ret;
	
	/* Se init, o próximo será o primeiro do bag */
	if(init) bag->next = bag->first;
		
	/* Se o bag não tem mais próximo, return NULL */
	if(bag->next == NULL) return -1;
	
	/* Cria uma copia do proximo */
	ret = bag->next->val;
	/* Atualiza o próximo */
	bag->next = bag->next->next;
	
    return ret;
}

/*------------------------------------------------------------*/
/* 
 * Implementaçao de funções administrativas
 */

