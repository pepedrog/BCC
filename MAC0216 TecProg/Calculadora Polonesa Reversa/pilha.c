#include <stdio.h>
#include "pilha.h"

#define TAMPIL 100
typedef double Stack[TAMPIL];

static Stack pilha;
static int topo;

static void Erro(char *errmsg)
{
     fputs(errmsg,stderr);
	 fputc('\n', stderr);
}

void empilha(double x)
{
     if (topo < TAMPIL) pilha[topo++] = x;
     else Erro("Pilha cheia");
}

double desempilha()
{
     if (topo > 0) return pilha[--topo];
     else Erro ("Pilha vazia");
	 return 1.0;
}


void Limpa_Pilha()
{
     topo = 0;
}

void Lista_Pilha()
{
  int i;
  for (i = 0; i < topo; i++)
	printf("  [%3.3d]: %f\n", i, pilha[i]);
}
