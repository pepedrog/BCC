/* Compilador da nossa linguagem pep */

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Funções que formatam operações para nossa linguagem do racket */
//Operadores aritmeticos
char *oper(char op, char *l, char *r) {
	char *res = malloc(strlen(l)+strlen(r)+6);
	sprintf(res, "(%c %s %s)", op, l, r);
	return res;
}
//Condicional
char *se(char *cond, char *entao, char *senao) {
	char *res = malloc(strlen(cond)+strlen(entao)+strlen(senao)+10);
	sprintf(res, "(if %s %s %s)", cond, entao, senao);
	return res;
}
//Seq
char *seq(char *exp1, char *exp2) {
	char *res = malloc(strlen(exp1)+strlen(exp2)+8);
	sprintf(res, "(seq %s %s)", exp1, exp2);
	return res;
}
//Chamando e criando Funções
char *call(char *nome, char *arg) {
	char *res = malloc(strlen(nome) + strlen(arg) + 8);
	sprintf(res, "(call %s %s)", nome, arg);
	return res;
}
char *func(char *nome, char *arg, char *corpo, char *faca) {
	char *res = malloc(2*strlen(nome) + strlen(arg) + strlen(corpo) + strlen(faca) + 40);
	sprintf(res, "(def %s 1 (seq (:= %s (func %s %s)) %s))", nome, nome, arg, corpo, faca);
	return res;
}
//Números e Símbolos
char *dup(char *orig) {
	char *res = malloc(strlen(orig)+1);
	strcpy(res,orig);
	return res;
}
//Atribuição de Variáveis
char *seja( char *simbolo, char *valor, char *faca) {
	char *res = malloc(strlen(simbolo) + strlen(valor) + strlen(faca) + 9);
	sprintf(res, "(def %s %s %s)", simbolo, valor, faca);
	return res;
}
char *atribui( char *simbolo, char *valor) {
	char *res = malloc(strlen(simbolo) + strlen(valor) + 6);
	sprintf(res, "(:= %s %s)", simbolo, valor);
	return res;
}
int yylex();
void yyerror(char *);
%}

%union {
	char *val;
}

%token	<val> NUM
%token  <val> FUNC
%token  ADD SUB MUL OPEN CLOSE SE ENTAO SENAO SEJA IGUAL FACA RECEBE E FUNCAO
%type	<val> exp
%type	<val> func

%left ADD SUB
%left MUL DIV
%left NEG
%left FUNC
/* Gramatica */
%%

input: 		
		| 		exp     { puts($1);}
		|		func	{ puts($1);}
		| 		error  	{ fprintf(stderr, "Entrada inválida\n"); }
;
// Expressões no geral -> Numeros, operadores, funções e condicional
exp: 				NUM 		{ $$ = dup($1); }
		| 		exp ADD exp					{ $$ = oper('+', $1, $3);}
		| 		exp SUB exp					{ $$ = oper('-', $1, $3);}
		| 		exp MUL exp					{ $$ = oper('*', $1, $3);}
		|		exp DIV exp 				{ $$ = oper('/', $1, $3);}
		| 		SUB exp %prec NEG 			{ $$ = oper('~', $2, "");}
		|		SE exp ENTAO exp 			{ $$ = se($2, $4, "");}
		|		SE exp ENTAO exp SENAO exp 	{ $$ = se($2, $4, $6);}
		| 		OPEN exp CLOSE 				{ $$ = dup($2);}
		|		SEJA func IGUAL exp FACA exp { $$ = seja($2, $4, $6); }
		|		func RECEBE exp 			{ $$ = atribui($1, $3); }
		|		OPEN exp E exp CLOSE		{ $$ = seq($2, $4);}
		|		SEJA func FUNCAO OPEN exp CLOSE exp FACA exp { $$ = func($2, $5, $7, $9); }
		|		func 						{ $$ = dup($1);}
;
// Chamada das funções (Nome e argumento)
func:				FUNC { $$ = dup($1);}
		|		func OPEN exp CLOSE { $$ = call($1, $3); }
;

%%

void yyerror(char *s) {
  fprintf(stderr,"%s\n",s);
}
