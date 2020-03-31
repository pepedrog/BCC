#include <stdio.h>
#include <stdlib.h>

typedef enum{
	False, True
}bool;

typedef char* string;

typedef union{
	int val;
	string quali;
}atrib;

typedef struct{
	atrib* lista;
}Objeto;

typedef struct{
	void* saidas;
}Lugar;

typedef union{
	Objeto objeto;
	Lugar lugar;
}detalhe;

typedef struct elo{
	void* val;
	char* nome;
	int tipo;
	void* value;
	struct elo* next;
}Elo;

typedef struct {
	Elo * cabec ;
}Lista;

typedef struct TabSim{
	int size;
	Lista* listas;
}TabSim;

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
