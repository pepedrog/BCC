/*
 * MAC0323 Estruturas de Dados e Algoritmo II
 * 
 * Tabela de simbolos implementada atraves de uma BST rubro-negra
 *
 *     https://algs4.cs.princeton.edu/33balanced/RedBlackBST.java.html
 * 
 * As chaves e valores desta implementação são mais ou menos
 * genéricos
 */

/* interface para o uso da funcao deste módulo */
#include "redblackst.h"  

#include <stdlib.h>  /* free() */
#include <string.h>  /* memcpy() */
#include "util.h"    /* emalloc(), ecalloc() */

#undef DEBUG
#ifdef DEBUG
#include <stdio.h>   /* printf(): para debug */
#endif

/*
 * CONSTANTES 
 */
#define RED   TRUE
#define BLACK FALSE 

/*----------------------------------------------------------*/
/* 
 * Estrutura Básica da Tabela de Símbolos: 
 * 
 * implementação com árvore rubro-negra
 */
typedef struct node Node;

struct redBlackST {
    Node * raiz;
	int n;
	int h;
	
	/* Função de comparação */
	int (*compar)(const void *key1, const void *key2);
	
	int next;
};

/*----------------------------------------------------------*/
/* 
 * Estrutura de um nó da árvore
 *
 */
struct node {
	
    Bool color;
	
	void* key;
	void* val;
	
	size_t sizeKey;
	size_t sizeVal;
	
	int size; 
	
	Node * left;
	Node * right;
	
};

/*------------------------------------------------------------*/
/* 
 *  Protótipos de funções administrativas.
 * 
 *  Entre essa funções estão isRed(), rotateLeft(), rotateRight(),
 *  flipColors(), moveRedLeft(), moveRedRight() e balance().
 * 
 *  Não deixe de implmentar as funções chamadas pela função 
 *  check(): isBST(), isSizeConsistent(), isRankConsistent(),
 *  is23(), isBalanced().
 *
 */

/*---------------------------------------------------------------*/
static Bool 
isRed(Node* h);

/*---------------------------------------------------------------*/
static int 
sizeN(Node* r);

/*---------------------------------------------------------------*/
static void 
flipColors(Node *r);

/*---------------------------------------------------------------*/
static Node* 
rotateLeft(Node* r);

/*---------------------------------------------------------------*/
static Node* 
rotateRight(Node* r);

/*---------------------------------------------------------------*/
static Node* 
moveRedLeft(Node* h);

/*---------------------------------------------------------------*/
static Node* 
moveRedRight(Node* h);

/*---------------------------------------------------------------*/
static void*
selectRec(Node* h, int k);
/*---------------------------------------------------------------*/
static Bool
isBST(RedBlackST st);

/*---------------------------------------------------------------*/
static Bool
isSizeConsistent(RedBlackST st);

/*---------------------------------------------------------------*/
static Bool
isRankConsistent(RedBlackST st);

/*---------------------------------------------------------------*/
static Bool
is23(RedBlackST st);

/*---------------------------------------------------------------*/
static Bool
isBalanced(RedBlackST st);

/*-----------------------------------------------------------*/
/*
 *  initST(COMPAR)
 *
 *  RECEBE uma função COMPAR() para comparar chaves.
 *  RETORNA (referência/ponteiro para) uma tabela de símbolos vazia.
 *
 *  É esperado que COMPAR() tenha o seguinte comportamento:
 *
 *      COMPAR(key1, key2) retorna um inteiro < 0 se key1 <  key2
 *      COMPAR(key1, key2) retorna 0              se key1 == key2
 *      COMPAR(key1, key2) retorna um inteiro > 0 se key1 >  key2
 * 
 *  TODAS OS OPERAÇÕES da ST criada utilizam a COMPAR() para comparar
 *  chaves.
 * 
 */
 
RedBlackST
initST(int (*compar)(const void *key1, const void *key2))
{
	RedBlackST st;
	
	st = emalloc(sizeof(struct redBlackST));
	
	st->n = 0;
	
	st->raiz = NULL;
	st->compar = compar;
	
    return st;
}

/*-----------------------------------------------------------*/
/*
 *  freeST(ST)
 *
 *  RECEBE uma RedBlackST  ST e devolve ao sistema toda a memoria 
 *  utilizada por ST.
 *
 */
void  
freeST(RedBlackST st)
{
	while(st->n > 0) delete(st, st->raiz->key);
	free(st);
}


/*------------------------------------------------------------*/
/*
 * OPERAÇÕES USUAIS: put(), get(), contains(), delete(),
 * size() e isEmpty().
 */

/*-----------------------------------------------------------*/
/*
 *  put(ST, KEY, NKEY, VAL, NVAL)
 * 
 *  RECEBE a tabela de símbolos ST e um par KEY-VAL e procura a KEY na ST.
 *
 *     - se VAL é NULL, a entrada da chave KEY é removida da ST  
 *  
 *     - se KEY nao e' encontrada: o par KEY-VAL é inserido na ST
 *
 *     - se KEY e' encontra: o valor correspondente é atualizado
 *
 *  NKEY é o número de bytes de KEY e NVAL é o número de bytes de NVAL.
 *
 *  Para criar uma copia/clone de KEY é usado o seu número de bytes NKEY.
 *  Para criar uma copia/clode de VAL é usado o seu número de bytes NVAL.
 *
 */

void printRaiz(RedBlackST st){
	
	if(st->raiz == NULL) printf("raiz = NULL\n");
	else printf("raiz = %s\n", (char*) st->raiz->key);	
}

Node*
putRec(Node* r, RedBlackST st, const void *key, size_t sizeKey, const void *val, size_t sizeVal){
	
	Node* no;
	int cmp;
	
	/* se caimos fora da arvore, criamos o novo nó */
	if(r == NULL){
		no = malloc(sizeof(Node));
		no->key = malloc(sizeKey);
		no->val = malloc(sizeVal);
		
		memcpy(no->key, key, sizeKey);		
		memcpy(no->val, val, sizeVal);

		no->size = 1;
		
		no->sizeKey = sizeKey;
		no->sizeVal = sizeVal;
		
		no->color = RED;
		
		no->left = NULL;
		no->right = NULL;
		
		st->n++;

		return no;
	}
	
	cmp = st->compar(r->key, key);
	
	/* se key != r-> key, insere na subarvore*/
	if(cmp > 0) r->left = putRec(r->left, st, key, sizeKey, val, sizeVal);	
	else if(cmp < 0) r->right = putRec(r->right, st, key, sizeKey, val, sizeVal);
	
	/* apenas atualiza o valor */
	else{
		r->sizeVal = sizeVal;
		r->val = realloc(r->val, sizeVal);
		memcpy(r->val, val, sizeVal);
	}
	
	/* Apos inserir, ajeita a arvore */
	if (isRed(r->right) && !isRed(r->left))       r = rotateLeft(r);
    if (isRed(r->left)  &&  isRed(r->left->left)) r = rotateRight(r);
    if (isRed(r->left)  &&  isRed(r->right))      flipColors(r);
        r->size = sizeN(r->left) + sizeN(r->right) + 1;
		
	return r;
	
}

void  
put(RedBlackST st, const void *key, size_t sizeKey, const void *val, size_t sizeVal)
{	
	/* Exceções */
	if(st == NULL){
		ERROR("put(): argument st is NULL");
		return;
	}
	if(key == NULL){
		ERROR("put(): argument key is NULL");
		return;
	}
	
	if(val == NULL) delete(st, key);
	
	st->raiz = putRec(st->raiz, st, key, sizeKey, val, sizeVal);
	
}    


/*-----------------------------------------------------------*/
/*
 *  get(ST, KEY)
 *
 *  RECEBE uma tabela de símbolos ST e uma chave KEY.
 *
 *     - se KEY não está em ST, RETORNA NULL;
 *
 *     - se KEY está em ST, RETORNA uma cópia/clone do valor
 *       associado a KEY.
 * 
 */
void *
get(RedBlackST st, const void *key)
{
	
	Node * atual = st->raiz;
	void* clone;
	int cmp;
	
	while(atual != NULL){
		
		cmp = st->compar(atual->key, key);
		
		if(cmp > 0) atual = atual->left;
		else if(cmp < 0) atual = atual->right;
		else{
			clone = malloc(atual->sizeVal);
			memcpy(clone, atual->val, atual->sizeVal);
			return clone;
		}
	}
	
	return NULL;
}

/*-----------------------------------------------------------*/
/* 
 *  CONTAINS(ST, KEY)
 *
 *  RECEBE uma tabela de símbolos ST e uma chave KEY.
 * 
 *  RETORNA TRUE se KEY está na ST e FALSE em caso contrário.
 *
 */
Bool
contains(RedBlackST st, const void *key)
{
	void* clone = get(st, key);
	if(clone == NULL) return FALSE;
	free(clone);
	return TRUE;
}

/*-----------------------------------------------------------*/
/* 
 *  DELETE(ST, KEY)
 *
 *  RECEBE uma tabela de símbolos ST e uma chave KEY.
 * 
 *  Se KEY está em ST, remove a entrada correspondente a KEY.
 *  Se KEY não está em ST, faz nada.
 *
 */
Node* deleteRec(Node* h, RedBlackST st, const void* key){
	/*Se o no esta a esquerda */
	if (st->compar(key, h->key) < 0)  {
		/* se os dois filhos a esuqerda forem pretos */
        if (!isRed(h->left) && !isRed(h->left->left))
        	h = moveRedLeft(h);
    	h->left = deleteRec(h->left, st, key);
    }
    else {
		/*Se tem um no vermelho a esquerda, rodamos para "trocar"*/
        if (isRed(h->left))
           h = rotateRight(h);
		/* se achamos a key e é uma folha, apenas apagamos (pq nao vai ter mais nenhum no vermelho a esquerda)*/
        if (st->compar(key, h->key) == 0 && (h->right == NULL)){
			free(h->key);
			free(h->val);
			free(h);
            return NULL;
		}
		
        if (!isRed(h->right) && !isRed(h->right->left))
            h = moveRedRight(h);
		
		/* se achamos */
        if (st->compar(key, h->key) == 0) {
			Node * atual = h->right;
			
			/* buscando o menor da arvore direita */
			while(atual->left != NULL) atual = atual->left;
			
			h->key = realloc(h->key, atual->sizeKey);
			h->val = realloc(h->val, atual->sizeVal);
			
			h->sizeKey = atual->sizeKey;
			h->sizeVal = atual->sizeVal;
			
			/* coloca o menor no lugar do deletado e deleta ele la de baixo*/
			
			memcpy(h->key, atual->key, atual->sizeKey);
			memcpy(h->val, atual->val, atual->sizeVal);

            h->right = deleteRec(h->right, st, h->key);
        }
        else h->right = deleteRec(h->right, st, key);
	}
	
	/*balance*/
    if (isRed(h->right) && !isRed(h->left))       h = rotateLeft(h);
    if (isRed(h->left)  &&  isRed(h->left->left)) h = rotateRight(h);
    if (isRed(h->left)  &&  isRed(h->right))      flipColors(h);
        h->size = sizeN(h->left) + sizeN(h->right) + 1;
		
	return h;
}

void
delete(RedBlackST st, const void *key)
{
	if(contains(st, key)){
		st->raiz = deleteRec(st->raiz, st, key);
		st->n--;
	}
}


/*-----------------------------------------------------------*/
/* 
 *  SIZE(ST)
 *
 *  RECEBE uma tabela de símbolos ST.
 * 
 *  RETORNA o número de itens (= pares chave-valor) na ST.
 *
 */
int
size(RedBlackST st)
{
	if(st == NULL){
		ERROR("size(): argument st is NULL");
		return EXIT_FAILURE;
	}
	
    return sizeN(st->raiz);
}


/*-----------------------------------------------------------*/
/* 
 *  ISEMPTY(ST, KEY)
 *
 *  RECEBE uma tabela de símbolos ST.
 * 
 *  RETORNA TRUE se ST está vazia e FALSE em caso contrário.
 *
 */

Bool
isEmpty(RedBlackST st)
{	
	if(st == NULL){
		ERROR("isEmpty(): argument st is NULL");
		return EXIT_FAILURE;
	}
    return (sizeN(st->raiz) == 0);
}

/*------------------------------------------------------------*/
/*
 * OPERAÇÕES PARA TABELAS DE SÍMBOLOS ORDENADAS: 
 * min(), max(), rank(), select(), deleteMin() e deleteMax().
 */

/*-----------------------------------------------------------*/
/*
 *  MIN(ST)
 * 
 *  RECEBE uma tabela de símbolos ST e RETORNA uma cópia/clone
 *  da menor chave na tabela.
 *
 *  Se ST está vazia RETORNA NULL.
 *
 */

void *
min(RedBlackST st)
{
    return select(st, 0);
}


/*-----------------------------------------------------------*/
/*
 *  MAX(ST)
 * 
 *  RECEBE uma tabela de símbolos ST e RETORNA uma cópia/clone
 *  da maior chave na tabela.
 *
 *  Se ST está vazia RETORNA NULL.
 *
 */
void *
max(RedBlackST st)
{
    return select(st, st->n - 1);
}


/*-----------------------------------------------------------*/
/*
 *  RANK(ST, KEY)
 * 
 *  RECEBE uma tabela de símbolos ST e uma chave KEY.
 *  RETORNA o número de chaves em ST menores que KEY.
 *
 *  Se ST está vazia RETORNA NULL.
 *
 */

int
rankRec(Node* r, const void* key, int (*compar)(const void *key1, const void *key2), int i){
	
	/* se cairmos fora da árvore */
	if(r == NULL) return i;
	
	/* se a chave que estamos olhando for menor que a procurada*/
	if(compar(r->key, key) < 0){
		
		/* incrementa o i */
		i++;
		
		/* podemos procurar no filho direito */
		i += rankRec(r->right, key, compar, 0);
		
		/* adicionamos todo mundo do filho esquerdo */
		if(r->left != NULL) i += r->left->size;
	}
	
	/* procura na subarvore esquerda */
	else i += rankRec(r->left, key, compar, 0);
	
	return i;
}

int
rank(RedBlackST st, const void *key)
{	
	if(st == NULL){
		ERROR("rank(): argument st is NULL");
		return EXIT_FAILURE;
	}
    return rankRec(st->raiz, key, st->compar, 0);
} 

/*-----------------------------------------------------------*/
/*
 *  SELECT(ST, K)
 * 
 *  RECEBE uma tabela de símbolos ST e um inteiro K >= 0.
 *  RETORNA a (K+1)-ésima menor chave da tabela ST.
 *
 *  Se ST não tem K+1 elementos RETORNA NULL.
 *
 */

void *
select(RedBlackST st, int k)
{
	if(st == NULL){
		ERROR("select(): argument st is null");
		return NULL;
	}
	if(st->n < k) return NULL;
    return selectRec(st->raiz, k + 1);
}


/*-----------------------------------------------------------*/
/*
 *  deleteMIN(ST)
 * 
 *  RECEBE uma tabela de símbolos ST e remove a entrada correspondente
 *  à menor chave.
 *
 *  Se ST está vazia, faz nada.
 *
 */
void
deleteMin(RedBlackST st)
{
	delete(st, select(st, 0));
}


/*-----------------------------------------------------------*/
/*
 *  deleteMAX(ST)
 * 
 *  RECEBE uma tabela de símbolos ST e remove a entrada correspondente
 *  à maior chave.
 *
 *  Se ST está vazia, faz nada.
 *
 */
void
deleteMax(RedBlackST st)
{
	delete(st, select(st, st->n - 1));
}


/*-----------------------------------------------------------*/
/* 
 *  KEYS(ST, INIT)
 * 
 *  RECEBE uma tabela de símbolos ST e um Bool INIT.
 *
 *  Se INIT é TRUE, KEYS() RETORNA uma cópia/clone da menor chave na ST.
 *  Se INIT é FALSE, KEYS() RETORNA a chave sucessora da última chave retornada.
 *  Se ST está vazia ou não há sucessora da última chave retornada, KEYS() retorna NULL.
 *
 *  Se entre duas chamadas de KEYS() a ST é alterada, o comportamento é 
 *  indefinido. 
 *  
 */
void * 
keys(RedBlackST st, Bool init)
{
	if(init) st->next = 0;
	if(st->next >= st->n){
		
		return NULL;
	}
	
	return select(st, st->next++);
}



/*------------------------------------------------------------*/
/* 
 * Funções administrativas
 */

/***************************************************************************
 *  Utility functions.
 ***************************************************************************/

/*
 * HEIGHT(ST)
 * 
 * RECEBE uma RedBlackST e RETORNA a sua altura. 
 * Uma BST com apenas um nó tem altura zero.
 * 
 */

int
heightRec(Node* r, int h){

	int hDir, hEsq, maior;
	if(r == NULL) return h;
	
	hDir = heightRec(r->right, h);
	hEsq = heightRec(r->left, h);
	
	if(hDir > hEsq) maior = hDir;
	else maior = hEsq;
	
	/* altura da maior subarvore + 1*/
	return (maior + 1);
}
int
height(RedBlackST st){

	if(st == NULL){
		ERROR("height(): argument st is NULL");
		return EXIT_FAILURE;
	}

	return heightRec(st->raiz, -1);
}



/***************************************************************************
 *  Check integrity of red-black tree data structure.
 ***************************************************************************/

/*
 * CHECK(ST)
 *
 * RECEBE uma RedBlackST ST e RETORNA TRUE se não encontrar algum
 * problema de ordem ou estrutural. Em caso contrário RETORNA 
 * FALSE.
 * 
 */
Bool
check(RedBlackST st)
{
    if (!isBST(st))            ERROR("check(): not in symmetric order");
    if (!isSizeConsistent(st)) ERROR("check(): subtree counts not consistent");
    if (!isRankConsistent(st)) ERROR("check(): ranks not consistent");
    if (!is23(st))             ERROR("check(): not a 2-3 tree");
    if (!isBalanced(st))       ERROR("check(): not balanced");
    return isBST(st) && isSizeConsistent(st) && isRankConsistent(st) && is23(st) && isBalanced(st);
}


/* 
 * ISBST(ST)
 * 
 * RECEBE uma RedBlackST ST.
 * RETORNA TRUE se a árvore é uma BST.
 * 
 */

static Bool isBSTRec(Node* h, RedBlackST st, void* min, void* max);

static Bool
isBST(RedBlackST st)
{	
    return isBSTRec(st->raiz, st, NULL, NULL);
}


/* 
 *  ISSIZECONSISTENT(ST) 
 *
 *  RECEBE uma RedBlackST ST e RETORNA TRUE se para cada nó h
 *  vale que size(h) = 1 + size(h->left) + size(h->right) e 
 *  FALSE em caso contrário.
 */

static Bool isSizeConsistentRec(Node* h);
					 
static Bool
isSizeConsistent(RedBlackST st)
{
    return isSizeConsistentRec(st->raiz);
}

/* 
 *  ISRANKCONSISTENT(ST)
 *
 *  RECEBE uma RedBlackST ST e RETORNA TRUE se seus rank() e
 *  select() são consistentes.
 */  
/* check that ranks are consistent */

static Bool
isRankConsistent(RedBlackST st)
{
	void* atual;
	int i;
	for (i = 0; i < size(st); i++)
            if (i != rank(st, select(st, i))) return FALSE;
	
	atual = keys(st, TRUE);
	
    while (atual != NULL){
        if (st->compar(atual, (select(st, rank(st, atual)))) != 0) return FALSE;
		atual = keys(st, FALSE);
	}
    return TRUE;
}

/* 
 *  IS23(ST)
 *
 *  RECEBE uma RedBlackST ST e RETORNA FALSE se há algum link RED
 *  para a direta ou se ha dois links para esquerda seguidos RED 
 *  Em caso contrário RETORNA TRUE (= a ST representa uma árvore 2-3). 
 */

static Bool is23Rec(Node* h);

static Bool
is23(RedBlackST st)
{
    return is23Rec(st->raiz);
}

/* 
 *  ISBALANCED(ST) 
 * 
 *  RECEBE uma RedBlackST ST e RETORNA TRUE se st satisfaz
 *  balanceamento negro perfeiro.
 */
			
static int isBalancedRec(Node* h, int blackLinks);

static Bool
isBalanced(RedBlackST st)
{
	if(st->n == 1) return TRUE;
    return (isBalancedRec(st->raiz, 0) != 0);
}

/*--------------------------------------------------------------*/
/*   F U N Ç Õ E S    A U X I L I A R E S    D O    C H E C K   */
/*--------------------------------------------------------------*/

static Bool isBSTRec(Node* h, RedBlackST st, void* min, void* max){
	if(h == NULL) return TRUE;
	if(min != NULL && st->compar(h->key, min) <= 0) return FALSE;
	if(max != NULL && st->compar(h->key, max) >= 0) return FALSE;
	return isBSTRec(h->left, st, min, h->key) && isBSTRec(h->right, st, h->key, max);
}
					 
/* retorna 0 se não está balanceado, outro inteiro se está*/
static int isBalancedRec(Node* h, int blackLinks){
	
	int blackLeft, blackRight;
	
	/*Tiramos um pois chamamos sempre com mais um, e nao faz sentidp adicionar 1 para um no nulo*/
	if(h == NULL) return (blackLinks);
	
	if(!isRed(h)) blackLinks++;
	
	blackLeft = isBalancedRec(h->left, blackLinks);
	blackRight = isBalancedRec(h->right, blackLinks);
	
	/* Temos que ver se blackDireita == blackEsquerda */
	/* Vamos definir que se for diferente, retornemos 0 */
	if(blackLeft != blackRight) return 0;
	
	/* se forem iguais, retorno qualquer uma das duas */
	return blackLeft;
	
	/* ideia : se todos os nos estiverem balanceados, 
	blackEsquerda sera sempre igual a blackDireita e um numero != 0 se propagará até a primeira chamada da recursão */
}

static Bool is23Rec(Node* h){
	
	if(h == NULL) return TRUE;
	return is23Rec(h->left) && is23Rec(h->right) && (!isRed(h->right) && !(isRed(h->left) && isRed(h->left->left))) ;
}

static Bool isSizeConsistentRec(Node* h){
	if(h == NULL) return TRUE;
	/*retorna se subarvore esquerda de h é consistente && subarvore direita de h é consistente  &&	h é consistente	*/
	return 			(isSizeConsistentRec(h->left) 	   &&     isSizeConsistentRec(h->right) 	&&  (h->size == 1 + sizeN(h->left) + sizeN(h->right)));
}



/*---------------------------------------------------*/
/*       F U N Ç Õ E S     A U X I L I A R E S       */
/*---------------------------------------------------*/


static Bool isRed(Node* h){
	if(h == NULL) return FALSE;
	return (h->color == RED);
}

static int sizeN(Node* r){
	if(r == NULL) return 0;
	return r->size;
}

static void flipColors(Node *r){
	
	r->color = !r->color;
	if(r->left != NULL) r->left->color = !r->left->color;
	if(r->right != NULL) r->right->color = !r->right->color;
	
}

static Node* rotateLeft(Node* r){
	
	Node * x = r->right;
	
	r->right = x->left;
	x->left = r;
	
	x->color = r->color;
	r->color = RED;
	x->size = r->size;
	r->size = sizeN(r->left) + sizeN(r->right) + 1;
	
	return x;
}

static Node* rotateRight(Node* r){
	
	Node * x = r->left;
	
	r->left = x->right;
	x->right = r;
	
	x->color = r->color;
	r->color = RED;
	x->size = r->size;
	r->size = sizeN(r->left) + sizeN(r->right) + 1;
	
	return x;
}

static Node* moveRedLeft(Node* h){
	
	flipColors(h);
    if (isRed(h->right->left)) { 
        h->right = rotateRight(h->right);
        h = rotateLeft(h);
        flipColors(h);
    }
    return h;
}

static Node* moveRedRight(Node* h){
	
	flipColors(h);
    if (isRed(h->left->left)) { 
        h = rotateRight(h);
        flipColors(h);
    }
    return h;	
}

static void* selectRec(Node* r, int k){
	
	Node* atual = r;
	void * clone;
	int quantMenores = sizeN(r->left);
	
	/*printf("buscando o %d menor na arvore %s\n", k, (char*) r->key);
	printf("%s tem %d menores\n", (char*) r->key, quantMenores);*/
	
	
	/* pega o menor */
	if(k - 1 > quantMenores) return selectRec(r->right, k - (quantMenores + 1));
	else if (k - 1 < quantMenores) return selectRec(r->left, k);
	
	clone = malloc(atual->sizeKey);
	memcpy(clone, atual->key, atual->sizeKey);
	return clone;

}
