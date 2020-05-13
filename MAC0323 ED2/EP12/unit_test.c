/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * unit test para a ADT Bag
 *
 */
/* Bag */
#include "bag.h"  /* newBag(), freeBag(), add(), isEmpty(), size()*/

#include <stdio.h>   /* printf() */
#include <stdlib.h>  /* exit(), EXIT_SUCCESS */
#include "util.h"    /* emalloc(), Integer, String */
#include <assert.h>  /* assert() */


/*---------------------------------------------------------------*/
/* 
 *  M A I N 
 */
int 
main(int argc, char *argv[])
{
    Bag bagInteger = newBag(); /* bag de Integer */
    Bag bagString  = newBag(); /* bag de String */
    int i;
    Integer pInt = emalloc(sizeof *pInt); /* ponteiro para int */
    String  s;
    
    /* insira itens na bagInteger */
    assert(isEmpty(bagInteger) == TRUE);        
    for (i = 0; i < 10; i++) {
        *pInt = i;
        add(bagInteger, pInt, sizeof *pInt); 
    }
    free(pInt);
    assert(isEmpty(bagInteger) == FALSE);        
    assert(size(bagInteger) == 10);        

    for (pInt = itens(bagInteger, TRUE); pInt; pInt = itens(bagInteger, FALSE)) {
        printf("%d ", *pInt);
        free(pInt);
    }
    printf("\n");
    
    /* insira itens na bagString */
    assert(isEmpty(bagString) == TRUE);
    add(bagString, " MAC0323!", 10);
    add(bagString, " estudar", 9);
    add(bagString, " bom", 5);
    add(bagString, " é", 4);
    add(bagString, "Como", 5); 
    assert(isEmpty(bagString) == FALSE);        
    assert(size(bagString) == 5);        

    for (s = itens(bagString, TRUE); s; s = itens(bagString, FALSE)) {
        printf("%s", s);
        free(s);
    }
    printf("\n");
    
    /* teste os iteradores juntos */
    pInt = itens(bagInteger, TRUE);
    s = itens(bagString, TRUE);

    while (pInt != NULL || s != NULL) {
        if (pInt != NULL) {
            printf("%d  : ", *pInt);
            free(pInt);
        }
        else printf("NULL: ");
        if (s != NULL) {
            printf("'%s'\n", s);
            free(s);
        }
        else printf("NULL\n");
        pInt = itens(bagInteger, FALSE);
        s = itens(bagString, FALSE);
    } 
    
    /* libere área alocadas para as bags */
    freeBag(bagString);
    freeBag(bagInteger);
    return EXIT_SUCCESS;
}

