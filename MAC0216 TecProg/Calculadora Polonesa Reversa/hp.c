#include <stdio.h>
#include "pilha.h"
#include "analex.h"

static void Erro(char *errmsg)
{
     fprintf(stderr, "ERRO: %s\n", errmsg);
     fputs("      Acao ignorada\n",stderr);
}

int main()
{
  TOKEN t;
  double op;
  Limpa_Pilha();
  
  while ((t=analex()) != FIM) {
	switch (t) {
	case NUMERO: 
	  empilha(num);
	  break;
	case SOMA: 
	  empilha(desempilha()+desempilha()); 
	  break;
	case SUB:
	  op = desempilha();
	  empilha(desempilha() - op); 
	  break;
	case MUL: 
	  empilha(desempilha()*desempilha()); 
	  break;
	case DIV: 
	  if (!(op = desempilha())) 
		Erro("Tentativa de divisao por 0");
	  else 
		empilha(desempilha()/op);
	  break;
	case LIMPA:
	  Limpa_Pilha();
	  break;
	case LISTA:
	  Lista_Pilha();
	  break;
	case PRINT:
	  op = desempilha();
	  printf("%12.5f\n", op);
	  empilha(op);
	  break;
	case NEG:
	  empilha(-desempilha()); 
	  break;
	default:
	  Erro("Isso não deveria acontecer!!");
	  break;
	}
  }
  return 0;
}
