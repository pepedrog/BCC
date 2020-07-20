/****************************************************************
    Nome: Pedro Gigeck Freire
    NUSP: 10737136

    Ao preencher esse cabeçalho com o meu nome e o meu número USP,
    declaro que todas as partes originais desse exercício programa (EP)
    foram desenvolvidas e implementadas por mim e que portanto não 
    constituem desonestidade acadêmica ou plágio.
    Declaro também que sou responsável por todas as cópias desse
    programa e que não distribui ou facilitei a sua distribuição.
    Estou ciente que os casos de plágio e desonestidade acadêmica
    serão tratados segundo os critérios divulgados na página da 
    disciplina.
    Entendo que EPs sem assinatura devem receber nota zero e, ainda
    assim, poderão ser punidos por desonestidade acadêmica.

    Abaixo descreva qualquer ajuda que você recebeu para fazer este
    EP.  Inclua qualquer ajuda recebida por pessoas (inclusive
    monitoras e colegas). Com exceção de material de MAC0323, caso
    você tenha utilizado alguma informação, trecho de código,...
    indique esse fato abaixo para que o seu programa não seja
    considerado plágio ou irregular.

    Exemplo:

        A monitora me explicou que eu devia utilizar a função xyz().

        O meu método xyz() foi baseada na descrição encontrada na 
        página https://www.ime.usp.br/~pf/algoritmos/aulas/enumeracao.html.

    Descrição de ajuda ou indicação de fonte:
		
		O tratamento de exceções foi feito conforme sugerido no paca
		
    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:
	
		Não consegui resolver meu delete nem o resize da tabela dinamica :(
		

****************************************************************/


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

#define capacidade_inicial 10


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


struct binarySearchST {
    int n, max;
	
	/* Vetores */
	void ** keys;
	void ** vals;
	
	size_t * nKeys;
	size_t * nVals;
	
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
	
	novaTabela->keys = emalloc(capacidade_inicial*sizeof(void*));
	novaTabela->vals = emalloc(capacidade_inicial*sizeof(void*));
	
	novaTabela->nKeys = emalloc(capacidade_inicial * sizeof(size_t));
	novaTabela->nVals = emalloc(capacidade_inicial * sizeof(size_t));
	
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
	
	free(st->nVals);
	free(st->nKeys);
	
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
	
	/* printf("inserindo %s em %d\n", key, i); */
	/* se a chave já está na tabela */
	if(i < st->n && st->compar(key, st->keys[i]) == 0){
		
		/*Atualizamos o valor*/
		st->nVals[i] = nVal;
		st->vals[i] = realloc(st->vals[i], nVal);
		memcpy(st->vals[i], val, nVal);
			
	}
	
	/* se a chave não está na tabela */
	else{
		
		/*Se a chave não cabe na tabela, resize */
		if(st->n >= st->max){
			/*printf("Aumentando a tabela\n");*/
			st->keys = realloc(st->keys, 2*st->max * sizeof(void*));
			st->nKeys = realloc(st->nKeys, 2*st->max * sizeof(size_t));
			st->vals = realloc(st->vals, 2*st->max * sizeof(void*));
			st->nVals = realloc(st->nVals, 2*st->max * sizeof(size_t));
			
			st->max *= 2;
		}
		
		/* Empurramos todo o vetor um para frente */
		for(j = st->n; j > i; j--){
			st->keys[j] = st->keys[j-1];
			st->nKeys[j] = st->nKeys[j-1];
			st->vals[j] = st->vals[j-1];
			st->nVals[j] = st->nVals[j-1];
		}
		
		/* cria a chave, cria o val*/ 
		st->vals[i] = malloc(nVal);
		st->nVals[i] = nVal;
		st->vals[i] = realloc(st->vals[i], nVal);
		memcpy(st->vals[i], val, nVal);
		
		st->keys[i] = malloc(nKey);
		st->nKeys[i] = nKey;
		st->keys[i] = realloc(st->keys[i], nKey);
		memcpy(st->keys[i], key, nKey);
		
		st->n++;
		
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
	/* Se a chave não está lá, retorna NULL */
	if(i >= st->n || st->compar(key, st->keys[i]) != 0){
		return NULL;
	}
	
	
	/* Se está, retorna um clone */
	clone = emalloc(st->nVals[i]);
	memcpy(clone, st->vals[i], st->nVals[i]);
	
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
	if(i == st->n || st->compar(key, st->keys[i]) != 0) return;
	
	/* Chave está na tabela */

	/* Liberamos a memória usada */
	free(st->keys[i]);
	free(st->vals[i]);
	
	/* Puxamos o vetor */
	for(j = i; j < st->n - 1; j++){
		
		st->keys[j] = st->keys[j+1];
		st->nKeys[j] = st->nKeys[j+1];
		st->vals[j] = st->vals[j+1];
		st->nVals[j] = st->nVals[j+1];
	}
	
	/* Se o n tá muito pequeno, resize */
	if(st->n < ((st->max)/4)){
		st->keys = realloc(st->keys, (st->max)/2 * sizeof(void*));	
		st->vals = realloc(st->vals, (st->max)/2 * sizeof(void*));
		st->nVals = realloc(st->nVals, (st->max)/2 * sizeof(size_t));
		st->nKeys = realloc(st->nKeys, (st->max)/2 * sizeof(size_t));
		
		st->max /= 2;
	}
	
	st->n--;
	
	
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
	
	clone = emalloc(st->nKeys[0]);
	memcpy(clone, st->keys[0], st->nKeys[0]);
	
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
	
	clone = emalloc(st->nKeys[st-> n - 1]);
	memcpy(clone, st->keys[st->n - 1], st->nKeys[st-> n - 1]);
	
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
	for(i = 0; i < st->n; i++) if(st->compar(key, st->keys[i]) <= 0) break;
	
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
	clone = emalloc(st->nVals[k]);
	memcpy(clone, st->vals[k], st->nVals[k]);
	
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
	delete(st, st->keys[0]);
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
	delete(st, st->keys[st->n -1]);
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
	clone = emalloc(st->nKeys[st->next]);
	memcpy(clone, st->keys[st->next], st->nKeys[st->next]);
	
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
	if(st == NULL) return EXIT_FAILURE;
	
	while(i < st->n && visit(st->keys[i], st->vals[i]) != 0) i++;
	
	if(i == st->n) return 1;
    return 0;

}
    

/*------------------------------------------------------------*/
/* 
 * Funções administrativas
 */

