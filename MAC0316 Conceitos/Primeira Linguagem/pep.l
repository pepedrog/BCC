D [0-9]
E [Ee][+-]?{D}+ 
F [a-zA-Z][a-zA-Z0-9]*
%{
#include <math.h>
#include "pep.tab.h"

%}


%%
{D}*[.]?{D}+{E}?	{ yylval.val = yytext; return NUM; }

[ \t\n]+	/* pula espacos em branco */

#.*		/* comentarios simples */

[(]		{ return OPEN; }
[)]		{ return CLOSE; }
[+]		{ return ADD; }
[-]		{ return SUB; }
[*]		{ return MUL; }
[/]		{ return DIV; }
se      	{ return SE;  }
entao   	{ return ENTAO; }
senao   	{ return SENAO; }
{F}     	{ yylval.val = yytext; return FUNC; } /* nome alfanumérico de função */

%%

/* Local Variables: */
/* mode: c */
/* End: */
