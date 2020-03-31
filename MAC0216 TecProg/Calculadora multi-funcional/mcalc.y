/* Calculadora infixa */

%{
#include <stdio.h>
#include <math.h>
#include "calc.h"
%}

/* Declaracoes */
%union {
  double val;
  symrec *tptr;
} 

%token <val>  NUM
%token <tptr> VAR FNCT
%token  ADD SUB MUL DIV PWR ASGN PRINT OPEN CLOSE CLEAR
%type  <val>  exp 

%right ASGN
%left ADD SUB
%left MUL DIV
%left NEG
%right PWR

/* Gramatica */
%%
input:				/* vazio */
     | input line
;

line: PRINT
    | exp PRINT		{ printf("\t%.10g\n", $1); }
	| CLEAR     { system("clear");}
	| error  	{ fprintf(stderr, "Incluindo um ';'\n"); 
					}
;

exp: NUM 		{ $$ = $1;}
   | VAR		{ $$ = $1->value.var;}
   | VAR ASGN exp	{ $$ = $3; $1->value.var = $3; }
   | FNCT OPEN exp CLOSE	{ $$ = (*($1->value.fnctptr))($3); } 
   | exp ADD exp	{ $$ = $1 + $3 ;}
   | exp SUB exp	{ $$ = $1 - $3 ;}
   | exp MUL exp	{ $$ = $1 * $3; }
   | exp DIV exp	{ $$ = $1 / $3; }
   | SUB exp %prec NEG  { $$ = - $2;} 
   | exp PWR exp	{ $$ = pow($1, $3); }
   | OPEN exp CLOSE	{ $$ = $2;}
;

%%

yyerror(char *s) {
  fprintf(stderr,"%s\n",s);
}
