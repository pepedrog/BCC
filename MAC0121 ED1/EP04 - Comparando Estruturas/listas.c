#include <stdlib.h>
#include <stdio.h>
#include "string.h"

typedef struct Elemento{
	char* nome;
	int ocorrencia;
	struct Elemento* prox;
} elemento;

typedef elemento* apontador;

apontador criaElemento(apontador lista, char* pa){
	
	//Insere no inicio de lista
	
	//Cria o elemento
	apontador novo = malloc(sizeof(elemento));
	
	//Define o nome
	novo->nome = malloc(strlen(pa)*sizeof(char));
	for(int i = 0; i < strlen(pa); i++)
		novo->nome[i] = pa[i];	
	
	novo->ocorrencia = 1;
	
	//Coloca ele no inicio e retorna
	novo->prox = lista;

	return novo;
}

apontador insereLD(apontador lista, char* pa){
	
	//Percorre a lista para tentar encontrar a palavra
	apontador p = lista;
	int i = 0;
	while(p != NULL && strcmp(p->nome, pa)!=0){
		p = p->prox;
		i++;
	}
	
	//Se chegou no final sem encontrar, cria a nova palavra no inicio
	if(p == NULL) lista = criaElemento(lista, pa);
	//Se encontrou, apenas incrementa a ocorrencia
	else p->ocorrencia++;
	
	return lista;
}

apontador insereLO(apontador lista, char* pa){

	
	apontador p, ant, novo;
	
	//Percorre a lista ate encontrar alguem maior que pa
	p = lista; ant = NULL;
	while(p != NULL && strcmp(p->nome, pa) < 0){
		ant = p;
		p = p->prox;
	}
	
	//Se encontrei a palavra, apenas incrementa
	if(p != NULL && strcmp(p->nome, pa) == 0){
		p->ocorrencia++;
		return lista;
	}
	//Cria o novo elemento
	novo = criaElemento(p, pa);
	
	//Se a lista nao for vazia, insere no lugar certo
	if(ant != NULL) ant->prox = novo;
	//Se for, insere no inicio
	else lista = novo;
	
	return lista;
}

