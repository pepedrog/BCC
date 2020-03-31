#include "listas.h"

typedef struct cel{
	char* nome;
	int ocorrencia;
	struct cel *pai;
	struct cel *dir;
	struct cel *esq;
} celula;

typedef celula * galho;

galho insereAB(galho, char*);
//Insere na arvore, conforme defenido em sala

apontador ArvoreParaLista(galho);
//Transforma a arvore em lista recursivamente para conseguir ordenar depois