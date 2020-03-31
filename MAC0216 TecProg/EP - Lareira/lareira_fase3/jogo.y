%{
#include <stdio.h>
//#include "lista.h"
//#include "salas.h"
#include "acoes.h"
//#include "elemento.h"

int yylex();
int yyerror(char *);

%}


/* Declaracoes */
%union {
  void *tptr;
  char *str;
  int  direc;
}

%token <tptr> VERBO OBJ LUGAR

/* DESC representa uma palavra desconhecida */
%token <str> DESC
%token  NORTE SUL LESTE OESTE VAPARA EOL FIM INVENT

%type <direc> dir
%type <tptr> obj

%defines

%%
/* Gramatica */


input: EOL		{ printf("Zzzz...\n"); }
    | cmd
	| VAPARA  {}
			  dir {
			      } eol
     | dir {} eol

	| INVENT {
			 /* listagem do inventário */
			 if (imprimeConteudo(personagem, 4, 'Q'))
                puts("Você está sem nada no momento...");
			 else {
                puts("Você tem:");
                imprimeConteudo(personagem, 4, 'I');
             }

		 } eol
	| FIM  { return 0;}
	| DESC { puts("Nada do que você diz está fazendo sentido.");}
	| error eol;
;

cmd: VERBO {
          //puts("reconheci");
			    /* Intransitivo */
          //Busca o verbo na lista e realiza a acao;
  	 	    fptr acao = (fptr) LBuscaGlobal(sym_table, $1, 'P');
          //puts("encontrei");
          acao(NULL, NULL);
		   } eol
   | VERBO obj {
			   /* Transitivo direto */
         //Busca o verbo e o objeto
         //puts("verbo obj");
         //printf("%s\n", (char*)$1);
			     fptr acao = (fptr) LBuscaGlobal(sym_table, $1, 'P');
           //puts("reconheci acao");
           Elemento *e = (Elemento*) LBuscaGlobal(sym_table, $2, 'P');
           //printf("peguei o %s\n", e->nome);
           acao(e, NULL);
			 } eol
   | VERBO obj obj {
          /* Bitransitivo */
          //Busca o verbo e os dois objetos
			    fptr acao = (fptr) LBuscaGlobal(sym_table, $1, 'P');
          Elemento *e = (Elemento*) LBuscaGlobal(sym_table, $2, 'P');
          Elemento *e2 = (Elemento*) LBuscaGlobal(sym_table, $3, 'P');
          acao(e, e2);
			   } eol
   | VERBO DESC {
			     printf("%s??\n", $2);
			 } eol
   | VERBO obj DESC {
			   printf("não sei o que é isso: %s\n",  $3);
			   } eol
   | VERBO DESC DESC {
			     printf("Pare de jogar e vá descansar um pouco\n"
						"Fazer isso com %s e %s, que coisa\n", $2,$3
						);
			   } eol
;

obj: OBJ    { $$ = $1;}
   | LUGAR  { $$ = $1;}

dir: NORTE	  { Mover(atual, 0); }
	 | SUL	  { Mover(atual, 1); }
	 | LESTE  { Mover(atual, 2); }
	 | OESTE  { Mover(atual, 3); }
	 | DESC   { puts("... (onde é isso?)"); $$=-1;}
;

eol: EOL {return 1;}
%%

int yyerror(char *s) {
  puts("Não entendi...");
  return 0;
}
