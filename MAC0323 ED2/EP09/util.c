/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 *
 * As funcoes neste arquivo foram copias, com pequenas adaptacoes,
 * da biblioteca de Eric Roberts.
 * 
 * https://github.com/mblair/roberts_abstractions/tree/master/book_code
 *
 * Ver tambem 
 *
 *    http://www.ime.usp.br/~pf/algoritmos/
 *    http://www.ime.usp.br/~pf/mac0122-2003/aulas/symb-table.html
 * 
 */

#include "util.h"   /* interface para este modulo */

#include <ctype.h>  /* tolower(). isalpha() */
#include <stdlib.h> /* exit(), malloc(), EXIT_FAILURE */ 
#include <stdio.h>  /* fprinf(), stderr */
#include <string.h> /* strcpy(), strncpy() */

/*
 * Constants:
 * ----------
 * InitialBufferSize -- Initial buffer size for ReadLine
 */

#define INITIALBUFFERSIZE 128

/*
 *
 * File: simpio.c
 * Version: 1.0
 * Last modified on Fri Jul 15 14:10:41 1994 by eroberts
 * -----------------------------------------------------
 * This file implements the simpio.h interface.
 */
static String 
readLine(FILE *infile);
 
/*
 * Function: GetLine
 * -----------------
 * This function is a simple wrapper; all the work is done by
 * ReadLine.
 */

/* string GetLine(void) */
String 
getLine(FILE *infile) 
{
    return (readLine(infile)); /* ReadLine(stdin); */
}

/*
 * Function: ReadLine
 * ------------------
 * This function operates by reading characters from the file
 * into a dynamically allocated buffer.  If the buffer becomes
 * full before the end of the line is reached, a new buffer
 * twice the size of the previous one is allocated.
 */

/* string  ReadLine (FILE *infile) */
static String 
readLine(FILE *infile) 
{
    String line  = NULL; /* string */ 
    String nline = NULL;
    int n, ch, size;

    n = 0;
    size = INITIALBUFFERSIZE; /* Initialbuffersize; */
    line = emalloc((size+1)*sizeof(char)); /* GetBlock(size + 1);*/
    while ((ch = getc(infile)) != '\n' && ch != EOF) {
        if (n == size) {
            size *= 2;
            nline = emalloc((size+1)*sizeof(char)); /* GetBlock(size + 1);*/
            strncpy(nline, line, n);
            free(line); /* FreeBlock(line);*/
            line = nline;
        }
        line[n++] = ch;
    }
    if (n == 0 && ch == EOF) {
        free(line); /* FreeBlock(line); */
        return NULL;
    }
    line[n] = '\0';
    nline = emalloc((n+1)*sizeof(char)); /* (string) GetBlock(n + 1); */
    strcpy(nline, line);
    free(line); /* FreeBlock(line); */
    return nline;
}


/*-------------------------------------------------------------*/ 
/* emalloc 
 *
 * O parâmetro de emalloc é do tipo size_t.  
 * Em muitos computadores, size_t é equivalente a unsigned int.  
 * A função emalloc não está em nenhuma biblioteca e é desconhecida 
 * fora destas notas de aula. 
 * Ela é apenas uma abreviatura conveniente.
 * Fonte:  http://www.ime.usp.br/~pf/algoritmos/aulas/aloca.html
 *
 */
void *
emalloc(size_t nbytes)
{
    void *ptr;

    ptr = malloc(nbytes);
    if (ptr == NULL) 
    {
        ERROR(Socorro! malloc devolveu NULL!);
        exit(EXIT_FAILURE);
    }

    return ptr;
}

/*-------------------------------------------------------------*/ 
/* ecalloc 
 *
 * Os parâmetro de ecalloc são do tipo size_t.  
 * Em muitos computadores, size_t é equivalente a unsigned int.  
 * A função ecalloc não está em nenhuma biblioteca e é desconhecida 
 * fora destas notas de aula. 
 * Ela é apenas uma abreviatura conveniente.
 * Fonte:  http://www.ime.usp.br/~pf/algoritmos/aulas/aloca.html
 *
 */
void *
ecalloc(size_t nbytes, size_t size)
{
    void *ptr;

    ptr = calloc(nbytes, size);
    if (ptr == NULL) 
    {
        ERROR(Socorro! calloc devolveu NULL!);
        exit(EXIT_FAILURE);
    }

    return ptr;
}

/*
 * copyString
 * 
 * Recebe uma string S e faz uma cópia de S. O espaço para a
 * cópia é alocado por emalloc. Esta função foi inspirada na
 * CopyString da biblioteca strlib de Eric Roberts.
 *
 * Copiado de 
 *
 *    http://www.ime.usp.br/~pf/mac0122-2003/aulas/symb-table.html
 */

String 
copyString(String s) 
{
   String newstr;

   newstr = emalloc(strlen(s) + 1); /* +1 para o '\0' */
   strcpy(newstr, s);
   return newstr;
}


/*----------------------------------------------------------------------
 *   strCmp(const char *s1, const char *s2)
 *
 *   Comportamento identico ao da funcao strcmp da interface string.h
 *   da libC. A unica diferenca e que esta funcao desconsidera se as
 *   letras sao maiusculas ou mininusculas.
 *
 *   copiado da  gLibc
 *
 *   Ver http://fossies.org/dox/glibc-2.20/string_2strcmp_8c_source.html
 *   ou a copia nas notas de aula de MAC0323
 *     
 *   ------------------------------------------------------------------
 *   NAME
 *      strcmp - compare two strings
 *
 *   SYNOPSIS
 *      #include <string.h>
 *
 *      int strcmp(const char *s1, const char *s2);
 *
 *   DESCRIPTION
 *      The  strcmp() function compares the two strings s1 and s2.  
 *      It returns an integer less than, equal to, or greater than
 *      zero if s1 is found, respectively, to be less than, to match, 
 *      or be greater than s2.
 *
 */

int  
strCmp(const void *s1, const void *s2)
{
    const unsigned char *p1 = (const unsigned char *) s1;
    const unsigned char *p2 = (const unsigned char *) s2;
    unsigned char c1, c2;
 
    do
    {
        c1 = tolower((unsigned char) *p1++); /* tolower foi acrescentado */ 
        c2 = tolower((unsigned char) *p2++); /* tolower foi acrescentado */
        if (c1 == '\0')
            return c1 - c2;
    }
    while (c1 == c2);
 
    return c1 - c2;
}

/* 
 * Sobre a GLIBC:
 *
 * Copyright (C) 1991-2014 Free Software Foundation, Inc.
 * This file is part of the GNU C Library.
 *
 * The GNU C Library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * The GNU C Library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with the GNU C Library; if not, see
 * <http://www.gnu.org/licenses/>. 
 */


/*
 * getNextToken
 *
 * Recebe um string LINHA e retorna a proximo palavra da
 * LINHA.  Na primeira chamada LINHA deve um ponteiro para o
 * string do qual desejamos a palavra. Nas chamadas
 * seguintes, LINHA deve ser NULL para que a funcao retorne
 * uma a uma as palavras restante no string.
 * 
 * Observacao: o comportamento e semelhante a funcao strtok
 * da bibliotaca string do C. Da mesma maneira que a funcao
 * strtok, esta funcao tambem _altera_ a LINHA colocando
 * '\0' no imediatamente apos da palavra encontrada, exceto
 * quando a palavra termina junto com LINHA.
 * 
 * Ver tambem http://www.ime.usp.br/~pf/mac0122-2003/aulas/scanner.html
 *   
 */
String 
getNextToken(String linha) 
{
    static String strIni = NULL; /* inicio de onde devemos procurar a palavra */
    String strFim        = NULL;
    String str           = NULL;
    String palavra       = NULL;
    int len = 0;

    if (linha != NULL) strIni = linha;

    /* procure a primeira letra da proxima palavra */
    while (*strIni && !isalpha(*strIni)) strIni++;

    /* chegamos ao final da linha? */
    if (*strIni == '\0')  return NULL;

    /* ande sobre a palavra para encontrar o fim */
    str = strIni;
    while (*str && isalpha(*str)) str++;

    /* strFim sera strIni no inicio da proxima chamada */
    if (*str == '\0') strFim = str; /* chegamos ao final de LINHA */
    else strFim = str + 1;

    /* marque o final da palavra na LINHA */
    *str = '\0';

    /* crie uma copia da palavra encontrada */
    len = strlen(strIni) + 1; /* +1 para o '\0'*/
    palavra = emalloc(len*sizeof(char));
    strncpy(palavra, strIni, len); /* copia o '\0' junto */

    /* strIni sera a posicao a partir da qual procuraremos a 
       palavra na proxima chamada */
    strIni = strFim;

    return palavra;
}
