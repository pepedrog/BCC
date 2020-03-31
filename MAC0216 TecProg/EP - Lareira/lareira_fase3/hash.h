#ifndef HASH_H
#define HASH_H
#include "lista.h"



/*
typedef struct TabSim{
	int size;
	Lista* listas;
}TabSim;*/

int hash(char*, int);
	//Definindo como será o hash das palavras


TabSim Tcria(int);
	//Criando uma tabela com tam listas

void Tdestroi(TabSim);
	//Percorre a tabela destruindo as listas dela

int Tinsere(TabSim, Elemento*);
	//Calcula o hash do elemento, que é em qual lista ele será inserido

Elemento* Tbusca(TabSim, char*);
	//Busca um elemento na tabela

int Tretira(TabSim, char*);
	//Busca um elemento na tabela para retirá-lo
#endif
