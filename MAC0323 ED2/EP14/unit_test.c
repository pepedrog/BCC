/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * unit test para a ADT Topological
 *
 */
/* representação topológica */
#include "topological.h" /* isDag(), hasCycle(), 
                          * pre(), post(), rank(), 
                          * preorder(), postorder(), order(), 
                          * cycle() 
                          */
#include "digraph.h"  /* newDigraph(), reverseDigraph(), freeDigraph(), vDigraph() */
#include "util.h"     /* String */

#include <stdio.h>   /* printf() */
#include <stdlib.h>  /* EXIT_SUCCESS */


/* protótipo de função para testar a ADT */
void
teste(Digraph G, Topological ts, String nome);

/* protótipo de função auxiliar */
void
pause();

/* constantes */
/* numero de testes */
#define N      5  

#define ENTER '\n'

/*---------------------------------------------------------------*/
/* 
 *  M A I N 
 */
int 
main(int argc, char *argv[])
{
    Digraph P2       = readDigraph("p2.txt");
    Topological tsP2 = newTopological(P2);
    
    Digraph RP2       = reverseDigraph(P2);
    Topological tsRP2 = newTopological(RP2);
        
    Digraph K4        = readDigraph("k4.txt");
    Topological tsK4  = newTopological(K4);
    
    Digraph RK4       = reverseDigraph(K4);
    Topological tsRK4 = newTopological(RK4);

    Digraph        C5 = readDigraph("c5.txt");
    Topological tsC5  = newTopological(C5);

    Digraph       AK5 = readDigraph("ak5.txt");
    Topological tsAK5 = newTopological(AK5);

    Digraph       HK5 = readDigraph("hk5.txt");
    Topological tsHK5 = newTopological(HK5);

    Digraph         G = readDigraph("g.txt");
    Topological   tsG = newTopological(G);
    
    Digraph       tinyDG = readDigraph("tinyDG.txt");
    Topological tsTinyDG = newTopological(tinyDG);

    Digraph       mediumDG = readDigraph("mediumDG.txt");
    Topological tsMediumDG = newTopological(mediumDG);
    /*
    Digraph       largeDG = readDigraph("largeDG.txt");
    Topological tsLargeDG = newTopological(largeDG);
    */
    
    teste(P2,   tsP2,   "P2");
    teste(RP2, tsRP2,  "RP2");
    teste(K4,   tsK4,   "K4");
    teste(RK4, tsRK4,  "RK4");
    teste(C5,   tsC5,   "C5");
    teste(AK5, tsAK5,  "AK5");
    teste(HK5, tsHK5,  "HK5");
    teste(  G,   tsG,    "G");
    teste(tinyDG, tsTinyDG,  "tinyDG");
    teste(mediumDG, tsMediumDG,  "mediumDG"); 
    /* teste(largeDG,   tsLargeDG,  "largeDG"); */

    
    /* liberando memoria digrafos */
    freeDigraph(P2);
    freeDigraph(RP2);
    freeDigraph(K4);
    freeDigraph(RK4);
    freeDigraph(C5);
    freeDigraph(AK5);
    freeDigraph(HK5);
    freeDigraph(G);
    freeDigraph(tinyDG);
    freeDigraph(mediumDG);
    /* freeDigraph(largeDG); */

    /* liberando memoria representacoes topologicas */
    freeTopological(tsP2);
    freeTopological(tsRP2);
    freeTopological(tsK4);
    freeTopological(tsRK4);
    freeTopological(tsC5);
    freeTopological(tsAK5);
    freeTopological(tsHK5);
    freeTopological(tsG);
    freeTopological(tsTinyDG);
    freeTopological(tsMediumDG);
    /* freeTopological(tsLargeDG); */
    
    return EXIT_SUCCESS;
}

/*------------------------------------------------*/
/*
 * TESTE(G, NOME)
 * 
 * RECEBE um digrafo G, uma representacao topologica TS de G e o NOME do digrafo.
 * TESSTA as funções da ADT da representacao topologica TS.
 */
void
teste(Digraph G, Topological ts, String nome)
{
    String s;
    vertex v;
    printf("\n========================================\n");
    printf("Iniciando testes com o digrafo %s:\n", nome);
    
    /* mostre o digrafo */
    s = toString(G);
    printf("digrafo %s:\n%s", nome, s);
    free(s);

    /* mostre se o digrafo é acíclico */
    printf("\n--------------\n");
    printf("   isDag(): %d\n", isDag(ts));
    printf("hasCycle(): %d\n", hasCycle(ts));
    
    /*------------------------------------------*/
    /* mostre os resultados da funcoes que atribuem posições aos vértices */
    printf("\n--------------\n");
    printf("   v   : "); 
    for (v = 0; v < vDigraph(G); v++) {
        printf("%2d ", v);
    }
    printf("\n");

    /*-----------------------------*/
    printf(" pre(v): "); 
    for (v = 0; v < vDigraph(G); v++) {
        printf("%2d ", pre(ts, v));
    }
    printf("\n");

    /*-----------------------------*/
    printf("post(v): "); 
    for (v = 0; v < vDigraph(G); v++) {
        printf("%2d ", post(ts, v));
    }
    printf("\n");

    /*-----------------------------*/
    printf("rank(v): "); 
    for (v = 0; v < vDigraph(G); v++) {
        printf("%2d ", rank(ts, v));
    }
    printf("\n");
    
    /*------------------------------------------*/
    /* mostre os resultados da funcoes ordenam os vértices */
    printf("\n--------------");
    
    /*-----------------------------*/
    printf("\n preorder(): ");
    for (v = preorder(ts, TRUE); v >= 0; v = preorder(ts, FALSE)) {
        printf("%2d ", v);
    }

    /*-----------------------------*/
    printf("\npostorder(): ");
    for (v = postorder(ts, TRUE); v >= 0; v = postorder(ts, FALSE)) {
        printf("%2d ", v);
    }

    /*-----------------------------*/
    printf("\n    order(): ");
    for (v = order(ts, TRUE); v >= 0; v = order(ts, FALSE)) {
        printf("%2d ", v);
    }

    /*-----------------------------*/
    printf("\ncycle: ");
    for (v = cycle(ts, TRUE); v >= 0; v = cycle(ts, FALSE)) {
        printf("%2d ", v);
    }
    printf("\n");
        
    printf("Testes encerrados \n");
    pause();
}

/*------------------------------------------------*/
void
pause()
{
    char ch;
    printf("Tecle ENTER para continuar ");
    do {
        scanf("%c", &ch);
    } while (ch != ENTER);
}
