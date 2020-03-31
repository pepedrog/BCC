#include <stdio.h>
#include <ctype.h>
#include "analex.h"

double num = 0.;

static void Erro(char *errmsg)
{
     fprintf(stderr, "Erro léxico: %s\n",errmsg);
}

TOKEN analex()
{
  int c;
  TOKEN t; 

  while (isspace(c=getchar()));
 
  if ((c == EOF) || (c == 'f'))
	return FIM;

  if ((c == '.') || isdigit(c))  {
	ungetc(c, stdin);
	if (scanf("%lf", &num) != 1)
	  Erro("Ponto isolado! Será utilizado o último número colocado na entrada");
	return NUMERO;
  }

  switch (c) {
  case '+' : t=SOMA; break;    
  case '-' : t=SUB; break;    
  case 'x' :
  case '*' : t=MUL; break;    
  case '/' : t=DIV; break;    
  case 'c' : t=LIMPA; break;  
  case 'p' :
  case '=' : t=PRINT; break;  
  case 'l' : t=LISTA; break;
  default  :
	Erro ("Simbolo desconhecido");
	t = INV;
	break;
  }
  return t;
}
