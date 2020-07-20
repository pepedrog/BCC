/*
 * MAC0323 Estruturas de Dados e Algoritmo II
 * 
 * Tabela de simbolos implementada atraves de vetores ordenados 
 * redeminsionaveis 
 *
 *     https://algs4.cs.princeton.edu/31elementary/BinarySearchST.java.html
 * 
 * As chaves e valores desta implementação são mais ou menos
 * genéricos
 */

/* interface para o uso da funcao deste módulo */
#include "binarysearchst.h"  

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

#define capacidade_inicial 8


/*------------------------------------------------------------*/
/* 
 * Funções administrativas
 */

/*----------------------------------------------------------*/
/* 
 * Estrutura Básica da Tabela de Símbolos: 
 * 
 * implementação com vetores ordenados
 */

struct node { 
	void * item;
	size_t size;
};

typedef struct node *Node;

struct binarySearchST {
    int n, max;
	
	/* Vetores */
	Node * keys;
	Node * vals;
	
	/* Tamanho (bytes) da chave e valor */
	size_t nKey;
	size_t nVal;
	
	int (*compar)(const void *key1, const void *key2);
	
	/* pŕoxima chave que será retornada pela função keys*/
	int next;
};

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
BinarySearchST
initST(int (*compar)(const void *key1, const void *key2))
{
	BinarySearchST novaTabela = malloc(sizeof(struct binarySearchST));
	
	novaTabela->keys = malloc(capacidade_inicial*sizeof(Node));
	novaTabela->vals = malloc(capacidade_inicial*sizeof(Node));
	
	novaTabela->n = 0;
	novaTabela->max = capacidade_inicial;
	
	novaTabela->compar = compar;
	
    return novaTabela;
}

/*-----------------------------------------------------------*/
/*
 *  freeST(ST)
 *
 *  RECEBE uma BinarySearchST  ST e devolve ao sistema toda a memoria 
 *  utilizada por ST.
 *
 */
void  
freeST(BinarySearchST st)
{
	int i;
	
	/* Exceção */
	if(st == NULL) return;
	for(i = 0; i < st->n; i++){
		free(st->keys[i]);
		free(st->vals[i]);
	}
	
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
void  
put(BinarySearchST st, const void *key, size_t nKey, const void *val, size_t nVal)
{
	
	int i, j;
	
	printf("inserindo %s\n", key);
	
	/* Se val == null, deletamos o elementos (key-val) */
	if(val == NULL){
		delete(st, key);
		return;
	}
	
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("put(): argument ST is null");
        return;
    }
	
    if (key == NULL) {
        ERROR("put(): argument KEY is null");
        return;
    }
	
	/*Indice onde teoricamente inseriremos a chave */
	i = rank(st, key);
	
	/* se a chave já está na tabela */
	if(i < st->n && st->compar(key, st->keys[i]->item) == 0){
		
		/*Atualizamos o valor*/
		st->vals[i]->size = nVal;
		st->vals[i]->item = realloc(st->vals[i]->item, nVal);
		memcpy(st->vals[i]->item, val, nVal);
			
	}
	
	/* se a chave não está na tabela */
	else{
		
		/*Se a chave não cabe na tabela, resize */
		if(st->n >= st->max){
			st->keys = realloc(st->keys, 2*st->max * sizeof(Node));
			st->vals = realloc(st->vals, 2*st->max * sizeof(Node));
			st->max *= 2;
		}
		
		/* Empurramos todo o vetor um para frente */
		for(j = st->n; j < i; j--){
			st->keys[j] = st->keys[j-1];
			st->vals[j] = st->vals[j-1];
		}
		
		/* cria a chave, cria o val*/ 
		/*st->vals[i] = malloc(sizeof(struct node));*/
		st->vals[i]->size = nVal;
		st->vals[i]->item = realloc(st->vals[i]->item, nVal);
		memcpy(st->vals[i]->item, val, nVal);
		
		/*st->keys[i] = malloc(sizeof(struct node));*/
		st->keys[i]->size = nVal;
		st->keys[i]->item = realloc(st->vals[i]->item, nKey);
		memcpy(st->vals[i]->item, key, nKey);
		
		st->n++;
		
		printf("A vizinhança 0 1 2 :\n");
		printf(" %s ", st->keys[0]);
		if(st->n > 1) printf(" %s ", st->keys[1]->item);
		if(st->n > 2) printf(" %s ", st->keys[2]->item);
	}
	
}    

/*-----------------------------------------------------------*/
/*
 *  get(ST, KEY)
 *
 *  RECEBE uma tabela de símbolos ST e uma chave KEY.
 *
 *     - se KEY está em ST, RETORNA NULL;
 *
 *     - se KEY não está em ST, RETORNA uma cópia/clone do valor
 *       associado a KEY.
 * 
 */
void *
get(BinarySearchST st, const void *key)
{
	int i;
	void* clone;
		
	printf("Vamos buscar %s\n", key);
	
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("get(): argument ST is null");
        return NULL;
    }
    if (key == NULL) {
        ERROR("get(): argument KEY is null");
        return NULL;
    }
	
	/* Como estamos trabalhando com vetores ordenados, a função get é basicamente a função rank */
	
	
	/* Achamos o indice onde a chave deveria estar */
	i = rank(st, key); 
	
	printf("Estaria na posição %d\n", i);
	
	/* Se a chave não está lá, retorna NULL */
	if(i >= st->n || st->compar(key, st->keys[i]->item) != 0){
		printf("Não está na tabela\n");
		return NULL;
	}
	
	printf("A chave está na tabela! pois n = %d \n", st->n);
	
	/* Se está, retorna um clone */
	clone = emalloc(st->vals[i]->size);
	memcpy(clone, st->vals[i]->item, st->vals[i]->size);
	
	return clone;
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
contains(BinarySearchST st, const void *key)
{
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("contains(): argument ST is null");
        return FALSE;
    }
    if (key == NULL) {
        ERROR("contains(): argument KEY is null");
        return FALSE;
    }
	
	/* Se a função get retornar NULL, então a chave não está na tabela */
	if(get(st, key) == NULL) return FALSE;
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
void
delete(BinarySearchST st, const void *key)
{
	int i, j;
	
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("delete(): argument ST is null");
        return;
    }
    if (key == NULL) {
		/* Não considerarei um erro, apenas seguiremos em diante, como se a chave null não estivesse na tabrla*/
        return;
    }
	
	i = rank(st, key);
	
	/*Se a chave não está na tabela*/
	if(i == st->n || st->compar(key, st->keys[i]->item) != 0) return;
	
	/* Chave está na tabela */
	
	/* Liberamos a memória usada */
	free(st->keys[i]->item);
	free(st->vals[i]->item);
	
	/* Puxamos o vetor */
	for(j = i; j < st->n; st++){
		st->keys[j] = st->keys[j+1];
		st->vals[j] = st->vals[j+1];
	}
	
	/* Se o n tá muito pequeno, resize */
	if(st->n < ((st->max)/4)){
		st->keys = realloc(st->keys, (st->max)/4 * sizeof(Node));	
		st->vals = realloc(st->keys, (st->max)/4 * sizeof(Node));
		
		st->max /= 4;
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
size(BinarySearchST st)
{
	/* Tratamento de exceções */
	if (st == NULL) {
        ERROR("size(): argument ST is null");
        return EXIT_FAILURE;
    }
	
	return st->n;
    return 0;
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
isEmpty(BinarySearchST st)
{
	/* Tratamento de exceção */
	if (st == NULL) {
		/* Vamos considerar que se o ponteiro é nulo, a aŕvore está vazia */
        ERROR("isEmpty(): argument ST is null, returning TRUE");
        return TRUE;
    }
	
	return st->n == 0;
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
min(BinarySearchST st)
{
	void * clone;
	
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("min(): argument ST is null");
        return NULL;
    }
	
	if(isEmpty(st)) return NULL;
	
	clone = emalloc(st->vals[0]->size);
	memcpy(clone, st->vals[0]->item, st->vals[0]->size);
	
	return clone;
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
max(BinarySearchST st)
{
	void* clone;
	
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("max(): argument ST is null");
        return NULL;
    }
	
	if(isEmpty(st)) return NULL;
	
	clone = emalloc(st->vals[st-> n - 1]->size);
	memcpy(clone, st->vals[st->n - 1]->item, st->vals[st-> n - 1]->size);
	
	return clone;
}

/*-----------------------------------------------------------*/
/*
 *  RANK(ST, KEY)
 * 
 *  RECEBE uma tabela de símbolos ST e uma chave KEY.
 *  RETORNA o número de chaves em ST menores que KEY.
 *
 *  Se ST está vazia RETORNA EXIT_FAILURE.
 *
 */
int
rank(BinarySearchST st, const void *key)
{
	int i;
	
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("rank(): argument ST is null");
        return EXIT_FAILURE;
    }
    if (key == NULL) {
        ERROR("rank(): argument KEY is null");
        return EXIT_FAILURE;
    }
	
	if(st == NULL) return EXIT_FAILURE;
	
	/* percorre e conta as chaves até achar uma maior */
	for(i = 0; i < st->n; i++) if(st->compar(key, st->keys[i]->item) >= 0) break;
	
    return i;
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
select(BinarySearchST st, int k)
{
	void* clone;
	
	/* Tratamento de exceção */
	if (st == NULL) {
        ERROR("select(): argument ST is null");
        return NULL;
    }
	
	/* Se a tabela não tem k + 1 elementos */
    if(k >= st->n) return NULL;
	
	/* Clonamos o k-ésimo elemento */
	clone = emalloc(st->vals[k]->size);
	memcpy(clone, st->vals[k]->item, st->vals[k]->size);
	
	return clone;
	
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
deleteMin(BinarySearchST st)
{	
	if(st == NULL) return;
	delete(st, st->keys[0]->item);
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
deleteMax(BinarySearchST st)
{
	if(st == NULL) return;
	delete(st, st->keys[st->n -1]->item);
}

/*-----------------------------------------------------------*/
/* 
 *  KEYS(ST, INIT)
 * 
 *  RECEBE uma tabela de símbolos ST e um Bool INIT.
 *
 *  Se INIT é TRUE, KEYS() RETORNA uma cópia/clone da menor chave na ST.
 *  Se INIT é FALSE, KEYS() RETORNA a chave sucessora da última chave retornada.
 *  Se ST está vazia ou não há sucessora da última chave retornada, KEYS() RETORNA NULL.
 *
 *  Se entre duas chamadas de KEYS() a ST é alterada, o comportamento é 
 *  indefinido. 
 *  
 */
void * 
keys(BinarySearchST st, Bool init)
{
	void* clone;
	
	if(st == NULL) return NULL;
	
	if(init) st->next = 0;
	
	/* se já chegamos no último */
	if(st->next >= st->n) return NULL;
	
	/* clonamos o próximo e retornamos */
	clone = emalloc(st->vals[st->next]->size);
	memcpy(clone, st->vals[st->next]->item, st->vals[st->next]->size);
	
	st->next++;
	
	return clone;
}

/*-----------------------------------------------------------*/
/*
  Visit each entry on the ST.

  The VISIT function is called, in-order, with each pair key-value in the ST.
  If the VISIT function returns zero, then the iteration stops.

  visitST returns zero if the iteration was stopped by the visit function,
  nonzero otherwise.
*/
int
visitST(BinarySearchST st, int (*visit)(const void *key, const void *val))
{
	int i = 0;
	while(i < st->n && visit(st->keys[i]->item, st->vals[i]->item) != 0) i--;
	
	if(i == st->n) return 1;
    return 0;

}
    

/*------------------------------------------------------------*/
/* 
 * Funções administrativas
 */

