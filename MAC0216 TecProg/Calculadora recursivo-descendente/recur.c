#include <stdio.h>
#include <math.h>
#include "recur.h"

#define PI 4*atan(1.)

double k[NVARS] = {
  0.0,
};

static void Erro(char *msg)
{
  fprintf(stderr, "Erro de sintaxe: %s\n", msg);
}

double fator()
{
  int indice;
  double f1;
  
  switch (ilc) {
  case NUMERO:
	f1 = num;
	analex();
	break;
	
  case OPERADOR :
	if (ch == '-') {
	  analex();
	  f1 = -fator();          /* Note que assim vale "2+-(3*4)" */
	}
	else {
	  Erro("Erro de sintaxe: O unico operador valido aqui e' '-'");
	  analex(); f1 = fator();
	}
	break;
	
  case COSSENO:
	if (analex() != PAR_ESQ)
	  Erro("Faltando '(', inserindo");
	else analex();
	f1 = cos(expr()/180.*PI);
	if (ilc != PAR_DIR)
	  Erro("Assumindo a presenca de um ')'");
	else analex();
	break;

  case SENO:
	if (analex() != PAR_ESQ)
	  Erro("Faltando '(', inserindo");
	else analex();
	f1 = sin(expr()/180.*PI);
	if (ilc != PAR_DIR)
	  Erro("Assumindo a presenca de um ')'");
	else analex();
	break;
	
  case RAIZ:
	if (analex() != PAR_ESQ)
	  Erro("Faltando '(', inserindo");
	else analex();
	f1 = expr();
	if (f1 <0.) {
	  Erro("Tentativa de extrair a raiz de um número negativo, trocando o sinal");
	  f1 = -f1;
	}
	f1 = sqrt(f1);
	if (ilc != PAR_DIR)
	  Erro("Assumindo a presenca de um ')'");
	else analex();
	break;

  case PAR_ESQ :
	analex();
	f1 = expr();
	if (ilc != PAR_DIR)
	  Erro("Faltando ')', inserido");
	else analex();
	break;
    
  case VARIAVEL :
	if (analex() != COL_ESQ)
	  Erro("Faltando '[', inserindo");
	else analex();
	indice = (int) expr();
	if ((indice < 0) || (indice > NVARS)) {
	  Erro("Indice fora de faixa, assumindo 0");
	  indice = 0;
	}
	if (ilc != COL_DIR)
	  Erro("Assumindo a presenca de um ']'");
	else analex();
	if (ilc == ATRIBUI) {
	  analex();
	  k[indice] = expr();
	}
	f1 = k[indice];
	break;
    
  default:
	Erro("Fator inválido. Trocando por 1.0.");
	f1 = 1.0;
	analex();
	break;
  }
  return f1;
}

double termo()
{
  double t1, t2;
  char c;

  t1 = fator();
  while (ch == '*' || ch == '/') {
    c = ch; analex();
    switch (c) {
      case '*': 
        t1 *= fator();
        break;
        
      case '/':
        t2 = fator();
        if (t2 == 0.0) {
          Erro("Divisao por 0\n"
			   "Assumindo resultado == 1");
          t1 = 1.0;
        }
        else t1 /= t2;
        break;
    }
  }
  return t1;
}

double expr()
{
  double e1;
  char c;
  
  e1 = termo();
  while (ch == '+' || ch == '-') {
    c = ch;
    analex();
    switch (c) {
      case '+':
        e1 += termo();
        break;
      case '-':
        e1 -= termo();
        break;
    }
  }
  return e1;
}


