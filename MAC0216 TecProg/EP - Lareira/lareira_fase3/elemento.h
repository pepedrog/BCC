#ifndef ELEMENTO_H
#define ELEMENTO_H
#include <stdio.h>
#include <stdlib.h>

typedef enum{
	False, True
} bool;

typedef char* string;

//union de atributo que pode se referir a um valor ou uma qualidade do objeto
typedef union{
	int val;
	string quali;
} atrib;

//lista de atributos do objeto
typedef struct{
	atrib* lista;
} Objeto;

//lista de salas adjacentes a uma sala
typedef struct{
	void* saidas[4];
} Lugar;

//union que determina se o elemento é objeto ou lugar
typedef union{
	Objeto objeto;
	Lugar lugar;
}detalhe;

//elo a ser usado em listas ligadas
typedef struct elo{
	void* val;
	char* nome;
	int tipo;
	struct elo* next;
} Elo;

//criação de uma lista ligada
typedef struct {
	Elo * cabec ;
} Lista ;

//criação de uma hash table
typedef struct TabSim{
	int size;
	Lista* listas;
} TabSim;

//definindo nosso elemento
typedef struct Elemento{
	string nome;
	string* artigos;
	string longa;
	string curta;
	bool ativo;
	bool visivel;
	bool conhecido;
	TabSim conteudo;
	int (**acoes)(struct Elemento*,struct Elemento*);
	void* animacao;
	detalhe def;
}Elemento;

#endif
