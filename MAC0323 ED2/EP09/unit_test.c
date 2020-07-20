/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * Contador de frequencia de palavras em um texto
 *
 *     http://www.ime.usp.br/~pf/mac0122-2003/aulas/symb-table.html
 * 
 * AVISO: Este programa quebra se o conjunto de caracters nao 
 *        for de 7-bits ASCII, ou seja, textos iso-latin 8859-1
 *        com acentos, cedilha, ... fazem o programa quebrar.
 *        UTF-8 nem pensar.
 */

#include <time.h>    /* clock_t, clock(), CLOCKS_PER_SECOND */
#include <stdio.h>   /* fprintf(), fgets(), printf() */
#include <stdlib.h>  /* exit(), EXIT_FAILURE */
#include <string.h>  /* strcmp() */
#include "util.h"    /* emalloc(), ecalloc(), strCmp(), getLine(), stringCopy(), 
                        ERRO(), AVISO(), getLine() */

/* tabela de símbolos */
#include "redblackst.h"  /* check(), initST(), freeST(), get(), put(), delete(), ... */

#define PROMPT      printf(">>> ");
#define SIZE_ST     "sizeST"
#define MIN_ST      "minST"
#define MAX_ST      "maxST"
#define DELMIN_ST   "delminST"
#define DELMAX_ST   "delmaxST"
#define KEYS_ST     "keysST"
#define GET_ST      "getST"
#define RANK_ST     "rankST"
#define DELETE_ST   "deleteST"
#define CHECK_ST    "checkST"
#define OPERACOES   "    " CHECK_ST  ", " SIZE_ST   ", " MIN_ST    ", " MAX_ST  ", "\
                           DELMIN_ST ", " DELMAX_ST ", " KEYS_ST "\n"\
                    "    " GET_ST " <key>, " RANK_ST " <key>, " DELETE_ST " <key>" "\n" 

/*---------------------------------------------------------------*/
/*
 *  P R O T Ó T I P O S
 */
static void 
mostreUso (char *nomePrograma);

RedBlackST
crieST(FILE *arqTexto);

void 
testeOperacoesST(RedBlackST st);

void 
testeOperacoes(RedBlackST st);

int
visit(const void *key, const void *val);

/*---------------------------------------------------------------*/
/* 
 *  M A I N 
 */
int 
main(int argc, char *argv[])
{
    FILE *         arqTexto = NULL;
    RedBlackST st       = NULL;

    if (argc < 2) mostreUso(argv[0]);

    /* abra arquivo com texto */
    arqTexto = fopen(argv[1], "r");
    if (arqTexto == NULL) {
        printf("ERRO: arquivo '%s' nao pode ser aberto.\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    /* crie a tabela de símbolos */
    st = crieST(arqTexto);
    
    /* teste operacoes */
    testeOperacoes(st);

    /* libere a memória ocupada pela ST */
    freeST(st);

    return EXIT_SUCCESS;
}


/*-------------------------------------------------------*/
/* 
 *  CRIEST(ARQTEXTO) 
 *
 *  RECEBE um arquivo ARQTEXTO e RETORNA uma tabela de 
 *  símbolos em que as chaves são as palavras do arquivo. 
 *  O valor correspondente a cada palavra é o seu número 
 *  de ocorrências.
 *
 *  As chaves da tabela de símbolo são do tipo String
 *  e os respectivos valores do tipo Integer.
 *
 *  String e Integer estão definidos em util.h.
 */
RedBlackST
crieST(FILE *arqTexto)
{
    RedBlackST st = NULL;
    String linha      = NULL;
    /* usadas para medir tempo de processamento */
    clock_t start, end; 
    double elapsed = 0;
   
    /* comece a cronometrar */
    start = clock(); 
    
    /* crie a ST vazia */
    printf("criando ST vazia...\n");
    st = initST(strCmp); 
    printf("tabela criada\n");

    /* leia cada linha do arquivoo */
    printf("colocando pares key-val na ST...\n");
    while ((linha = getLine(arqTexto))) {
        /* coloque cada palavra na linha na ST */
        String palavra = getNextToken(linha); /* 1a. palavra */
        while (palavra) {
            /* pegue o número de ocorrência da palavra até o momento */
            Integer frequencia = get(st, palavra);
            
            /* atualize a frequencia */
            if (frequencia == NULL) {
                frequencia = emalloc(sizeof(Integer));
                *frequencia = 0;
            }
            (*frequencia)++;
            
            /* atualize o para palavra-frequencia na ST */
            /* +1 devido ao '\0'            VVV */
            put(st, palavra, strlen(palavra) + 1, frequencia, sizeof(Integer));
            /* devolva os bytes do par palavra-frequencia */ 
            free(palavra); 
            free(frequencia);
            /* pegue próxima palavra */
            palavra = getNextToken(NULL); /* proxima palavra */
        }
        /* devolva os bytes da linha */
        free(linha);
    }
    /* trave o cronometro */  
    end = clock();

    /* calcule o tempo */
    elapsed = ((double) (end - start)) / CLOCKS_PER_SEC;
    fclose(arqTexto);
    printf("arquivo lido e ST construida em %g segundos\n", elapsed);
    printf("ST possui %d pares key-val\n\n", size(st));
    printf("ST tem altura %d\n\n", height(st));

    return st;
}


/*-------------------------------------------------------*/
/* 
 *  TESTEOPEARCOES(ST) 
 *
 *  RECEBE uma tabela de símbols ST e testa várias operações
 *  interativamente.
 *
 *  A função supõe que as chaves são do tipo String e os
 *  valores são do tipo Integer (ver util.h).
 */
void 
testeOperacoes(RedBlackST st)
{
    String linha    = NULL;
    
    /* mostre uso */
    printf("Possiveis operacoes do teste interativo:\n");
    printf(OPERACOES);
    printf("CRTL-D para encerrar.\n");
    PROMPT;
    while ((linha = getLine(stdin))) {
        /* pegue operacao a ser testada */
        String operacao = getNextToken(linha);
        if (operacao == NULL) {
             ERROR(operacao esperada);
        }
        /*---------------------------------*/
        else if (!strcmp(operacao, CHECK_ST)) {
            if (check(st)) {
                printf("RedBlackST passou no teste de integridade\n");
            }
            else {
                ERROR("RedBlackST nao passou no teste de integridade\n");
            }
        }
        /*---------------------------------*/
        else if (!strcmp(operacao, SIZE_ST)) {
            printf("%d\n", size(st));
        }
        /*---------------------------------*/
        else if (!strcmp(operacao, MIN_ST)) {
            String key = min(st);
            if (key == NULL) {
                printf("ST vazia\n");
            } else {
                printf("%s\n", key);
                free(key);
            }
        }
        /*---------------------------------*/
        else if (!strcmp(operacao, MAX_ST)) {
            String key = max(st);
            if (key == NULL) {
                printf("ST vazia\n");
            } else {
                printf("%s\n", key);
                free(key);
            }
        }
        /*---------------------------------*/
        else if (!strcmp(operacao, DELMIN_ST)) {
            deleteMin(st);
        }
        /*---------------------------------*/
        else if (!strcmp(operacao, DELMAX_ST)) {
            deleteMax(st);
        }
        /*---------------------------------*/
        else if (!strcmp(operacao, KEYS_ST)) {
            String key = NULL;
            for (key = keys(st, TRUE); key; key = keys(st,FALSE)) {
                Integer frequencia = NULL;
                frequencia = get(st, key); /* consulte a ST */
                /* mostre o resultado da consulta */
                if (frequencia == NULL) {
                    printf("'%s': 0\n", key);
                } else {
                    printf("'%s': %d\n", key, *frequencia);
                    free(frequencia); 
                }
                free(key);
            }
        }
        /*---------------------------------*/
        else {
            /* operação necessita de argumento key */
            String key = getNextToken(NULL);
            if (key == NULL) {
                ERROR(operacao necessita uma palavra);
            } else {
                /*---------------------------------*/
                if (!strcmp(operacao, GET_ST)) {
                    Integer frequencia = NULL;
                    frequencia = get(st, key); /* consulte a ST */
                    /* mostre o resultado da consulta */
                    if (frequencia == NULL) {
                        printf("'%s': 0\n", key);
                    } else {
                        printf("'%s': %d\n", key, *frequencia);
                        free(frequencia); 
                    }
                }
                /*---------------------------------*/
                else if (!strcmp(operacao, RANK_ST)) {
                    int r = rank(st, key);
                    printf("%d\n",r);
                }
                /*---------------------------------*/
                else if (!strcmp(operacao, DELETE_ST)) {
                    delete(st, key);
                }
                else {
                    ERROR(operacao nao reconhecida);
                }
                free(key);
            }
        }
		
        if (operacao != NULL) free(operacao);
        free(linha);
        PROMPT;
    }
    printf("\n");
}


/*---------------------------------------------------------------*/
/* 
 *  I M P L E M E N T A Ç Ã O   D A S   F U N Ç Õ E S   DA  
 *                     A U X I L I A R E S 
 */
static void 
mostreUso (char *nomePrograma)
{
    fprintf(stderr,"%s: Uso \n"
	    "prompt> %s nome-arquivo\n"
	    "    nome-arquivo = nome do arquivo com o texto\n"
	    ,nomePrograma, nomePrograma);
    exit(EXIT_FAILURE);
}

