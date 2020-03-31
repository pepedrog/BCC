/* Calculadora infixa */

%{
#include <stdio.h>
#include "symrec.h"
#include "coisas.h"
  
int yylex();
int yyerror(char *);

/* Macro para simplificar a escrita das chamadas de função */
#define F(x) (*(Fptr)(x->value))

/* Identifica qual a versão correta do verbo chamado */
symrec * AcertaF(symrec *f, symrec *o1) {
  symrec *s;

  /* Verifica se existe uma versão especial no local atual (Posic) */
  if ((s = getsym(Posic->cont, f->name)))
	return s;

  /* Verifica se o primeiro objeto tem uma versão especial */
  if (o1) {
	Elemento *o = o1->value;
	if ((s = getsym(o->cont, f->name)))
	  return s;
  }
  return f;	
}
%}

/* Declaracoes */
%union {
  symrec *tptr;
  char *str;
  int  direc;
}

%token <tptr> VERBO OBJ LUGAR

/* DESC representa uma palavra desconhecida */
%token <str> DESC
%token  NORTE SUL LESTE OESTE CIMA BAIXO VAPARA EOL FIM INVENT

%type <direc> dir
%type <tptr> obj

%defines

%%
/* Gramatica */


input: EOL		{ printf("Zzzz...\n"); }
    | cmd
	| VAPARA  {
	  		   /* movimentação */
	  		   printf("Seguindo para ");
	  		  }
			  dir {
					if ($3 >= 0 && Posic->Det.lug.Saidas[$3]) {
					  Posic = Posic->Det.lug.Saidas[$3];
					  Examinar(NULL,NULL);
					}
					else puts("Não há passagem....");
			      } eol
	 | dir {
			 /* movimentação  */
             if ($1 >= 0 && Posic->Det.lug.Saidas[$1]) {
			   Posic = Posic->Det.lug.Saidas[$1];
			   printf("Você foi para %s\n", Posic->nome);
			   Examinar(Posic,NULL);
			 }
			 else puts("Não há passagem....");
											} eol

	| INVENT {
			 /* listagem do inventário */
			 if (inventario) {
			   puts("Você tem:");
			   printsym(inventario);
			 }
			 else puts("Você está sem nada no momento...");
												
		 } eol
	| FIM  { return 0;}
	| DESC { puts("Não tem registro, Will Robinson.");}
	| error eol;
;

cmd: VERBO {
			 /* Intransitivo */
  	 	     F(AcertaF($1,NULL))(NULL,NULL);
		   } eol
   | VERBO obj {
			   /* Transitivo direto */
			   F(AcertaF($1,$2))($2->value,NULL);
			 } eol 
   | VERBO obj obj {
                 /* Bitransitivo */
			     F(AcertaF($1,$2))($2->value,$3->value);
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

dir: NORTE	  { puts("norte"); $$=0;}
	 | SUL	  { puts("sul");   $$=1;}
	 | LESTE  { puts("leste"); $$=2;}
	 | OESTE  { puts("oeste"); $$=3;}
	 | CIMA	  { puts("cima");  $$=4;}
	 | BAIXO  { puts("baixo"); $$=5;}
	 | DESC   { puts("... (onde é isso?)"); $$=-1;}
;

eol: EOL {return 1;}
%%

int yyerror(char *s) {
  puts("Não entendi...");
  return 0;
}
