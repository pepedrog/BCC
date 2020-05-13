/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 *
 * NAO EDITE OU MODIFIQUE NADA QUE ESTA ESCRITO NESTE ARQUIVO
 *
 * Aqui esta o prototipo das funções emalloc(), ecalloc(),
 * getLine(), getNextToken() além das definições de
 * Bool, String, Integer e algumas macros de uso geral.
 */

#ifndef _UTIL_H
#define _UTIL_H

#include <stdio.h>  /* size_t */

#define MAX(a,b)     ((a) > (b) ? (a): (b))

/*---------------------------------------------------------------*/
/* Bool */
enum bool 
{
    FALSE,
    TRUE
};
typedef enum bool Bool;

/*---------------------------------------------------------------*/
/* String */
typedef char * String;

/*---------------------------------------------------------------*/
/* Integer */
typedef int * Integer;

/*-------------------------------------------------------------*/ 
/* alguma macros/abreviaturas uteis */
#define ERROR(msg)   fprintf(stderr,"ERROR: %s\n", #msg)
#define WARNING(msg) fprintf(stdout,"WARNING: %s\n", #msg)

/*---------------------------------------------------------------*/
/* prototipo de funcoes */
void *
emalloc(size_t nbytes);

void *
ecalloc(size_t nbytes, size_t size);

String 
getLine(FILE *infile);

String 
copyString(String s); 

int  
strCmp(const void *s1, const void *s2);

String 
getNextToken(String line);

#endif /* _UTIL_H */
