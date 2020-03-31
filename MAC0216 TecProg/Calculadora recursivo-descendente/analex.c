#include <stdio.h>
#include <ctype.h>
#include "analex.h"

double num;
TOKEN ilc;              /* item lexico corrente */
char  ch;

static TOKEN Erro()
{
  fputs("Item lexico inválido.\n", stderr);
  return INVALIDO;
}
    
TOKEN analex()
{
  while (isspace(ch = getc(stdin)));
  
  if ((ch == '.') || isdigit(ch)) {
    ungetc(ch, stdin);
    if(scanf("%lf", &num)!=1) {
      getchar();            /* Joga o ponto fora */
      Erro();
    }
    ch = 0;
    ilc = NUMERO;
  }
  else switch (ch) {
	case '+':     case '-':    case '*':     case '/':
      ilc = OPERADOR; break;
	case 'c': 
	  ilc = COSSENO; break;
	case 's': 
	  ilc = SENO; break;
	case 'r': 
	  ilc = RAIZ; break;
    case '(':
      ilc = PAR_ESQ; break;
    case ')':
      ilc = PAR_DIR; break;
    case '[':
      ilc = COL_ESQ; break;
    case ']':
      ilc = COL_DIR; break;
    case 'K': 
    case 'k':
      ilc = VARIAVEL; break;
    case ':':
      if ((ch = getc(stdin)) == '=')
        ilc = ATRIBUI;
      else return Erro(); break;
      
    case ';':
      ilc = PRINT; break;
      
    case EOF :
    case 'q' :
    case 'Q' :
    case 'f' :
    case 'F' :
      ilc = FIM; break;
      
    default : 
      return Erro();
  }
  return ilc;
}
