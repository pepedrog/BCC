%{
#include <stdio.h>
#include <ctype.h>
int yylex();
void yyerror();
%}

%token PN N  V INV F


/* Gramatica */
%%

line:
	| s line;

s: np vp F {puts(".");};

np: PN N {printf("búfalos de Buffalo");} 
  | np rc
;

rc: {printf(" que são trolados por ");} np V ;

vp: V  {printf(" trolam os ");} np;

%%

void yyerror(char *s) {
  fprintf(stderr,"%s\n",s);
}

int yylex() {
  int c;

  while (isspace(c=getchar()));

  switch (c) {
  case 'P':
  case 'p': return PN;

  case 'V':
  case 'v': return V;

  case 'n':
  case 'N': return N;

  case '.': return F;
  }
  return INV;
}

int main() {
  yyparse();
  return 0;
}
