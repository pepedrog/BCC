#include "listas.h"
#include "string.h"
#include <stdlib.h>

typedef struct cel{
	char* nome;
	int ocorrencia;
	struct cel *pai;
	struct cel *dir;
	struct cel *esq;
} celula;

typedef celula * galho;

galho insereAB(galho raiz, char* pa){
	
	galho p = raiz, anterior = NULL;
	int compara;
	
	//Vai descendo a arvore
	while(p != NULL){
		anterior = p;
		compara = strcmp(p->nome, pa);
		//Escolhe o lado para descer ou
		if(compara > 0) p = p->esq;
		else if(compara < 0) p = p->dir;
		
		else{
			//Se encontrei a palavra, apenas insere ela
			p->ocorrencia++;
			return raiz;
		}
	}
	
	//Cria nova folha
	p = malloc(sizeof(celula));
	
	p->nome = malloc(strlen(pa)*sizeof(char));
	for(int i = 0; i < strlen(pa); i++)
		p->nome[i] = pa[i];	
	
	p->ocorrencia = 1;
	p->pai = anterior;
	p->esq = p->dir = NULL;
	
	if(anterior == NULL) raiz = p;
	
	//Define qual filho (dir ou esq) sera a nova celula
	else if(strcmp(anterior->nome, pa) < 0) anterior->dir = p;
	else anterior->esq = p;
	
	return raiz;	
	
}

apontador ArvoreParaLista(galho raiz){
	
	apontador lista = NULL;
		
	if(raiz != NULL){
		
		//Coloca a raiz na lista 
		lista = criaElemento(lista, raiz->nome);
		lista->ocorrencia = raiz->ocorrencia;
		
		//Coloca a lista gerada pela arvore da direira
		lista->prox = ArvoreParaLista(raiz->dir);
		
		//Vai ate o final
		apontador p = lista;
		while(p->prox != NULL) p = p->prox;
		
		//E coloca a lista gerada pela esquerda
		p->prox = ArvoreParaLista(raiz->esq);
	}
	
	return lista;
	
}