D [0-9]
L [a-zA-Z_]
H [a-zA-Z_0-9]
E [Ee][+-]?{D}+

%{
#include <math.h>
#include "calc.h"
#include "mcalc.tab.h"

%}


%%
	symrec *s;

{D}*[.]?{D}+{E}?	{ yylval.val = atof(yytext); return NUM; }

clear { return CLEAR;}

{L}{H}*			{
	s = getsym(yytext);
	if (s == 0) s = putsym(yytext, VAR);
	yylval.tptr = s;
	return s->type;
}

[ \t\n]+	/* pula espacos em branco */

#.*		/* comentarios simples */

;		{ return PRINT; }
=		{ return ASGN; }
[(]		{ return OPEN; }
[)]		{ return CLOSE; }
[+]		{ return ADD; }
[-]		{ return SUB; }
[*]		{ return MUL; }
[/]		{ return DIV; }
\^		{ return PWR; }
[*][*]	{ return PWR; }

.	{  fprintf(stderr, "Entrada ignorada\n-->%s\n", yytext); }

%%

/* Local Variables: */
/* mode: c */
/* End: */
