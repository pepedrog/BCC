/* -*- mode:c -*- */
/* Conversor para dólar */

%{
#include <math.h>
#include <locale.h>
#include <monetary.h>

double taxa = 1.;

void converte(double d) {
  char b[2048];
  strfmon(b,2048,"%!n", d/taxa);
  printf("US$%s", b);
}
%}

MILHAR	 [[:digit:]]{3}
VAL		 -?[[:digit:]][[:digit:]]?[[:digit:]]?
CENT	 [[:digit:]]{2}

SEP [[:space:]]*

	  double valor=0.;
%s VALOR  MEIO

%%

R[$]{SEP} BEGIN(VALOR);

<VALOR>{VAL} {
			 valor = atof(yytext); 
			 BEGIN(MEIO);
			 }
<MEIO>[.]{MILHAR} {
			     valor *=1000;
				 valor += atof(++yytext);
			   }
<MEIO,VALOR>[,]{CENT} {
			   valor += atof(++yytext)/100;
			   converte(valor);
			   valor = 0.;
			   BEGIN(0);
		     }

<VALOR,MEIO>(.|\n) {
		     converte(valor);
			 valor = 0.;
			 ECHO;
			 BEGIN(0);
		   }


. ECHO;

%%
 
int main(int ac, char **av)
{
  ac--, av++;
  if (ac) {
	taxa = atof(*av);
	ac--, av++;
  }
  if (!taxa) {
	fprintf(stderr,"Taxa inaceitável\n");
	exit(1);
  }

  setlocale(LC_ALL,"pt_BR");

  if (ac) yyin = fopen(*av,"r");
  yylex();
}
