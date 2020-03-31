/* scanner para pseudo pascal */

%{
/* atof e' usado */
#include <math.h>
%}

DIGIT [0-9]
ID    [a-z][a-z0-9]+
INTEIRO [+-]?{DIGIT}+
%%

{INTEIRO}   {
	printf("Inteiro: %s (%d)\n", yytext, atoi(yytext));
	}

{DIGIT}+"."{DIGIT}*|{DIGIT}*"."{DIGIT}+	{
	printf("Float: %s (%g)\n", yytext, atof(yytext));
	}

if|then|"else"|begin|end|procedure|function	{
	printf("Palavra reservada: %s\n", yytext);
	}

{ID}	{
	printf("Identifdicador: %s\n", yytext);
	}

[-+*/><%] {
	printf("Operador: %s\n", yytext);
	}

"{"[^}]*"}"

[ \t\n]+

.	printf("Erro lexico: %s\n", yytext);

%%

int main(int ac, char **av)
{
	++av, --ac;
	if (ac) yyin = fopen(*av,"r");
	else yyin = stdin;
	yylex();
	return 0;
}

