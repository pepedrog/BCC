#include <stdio.h>
#include <stdlib.h>
#include "string.h"

typedef struct {
	char* nome;
	int ocorrencia;
} palavra;

typedef struct{
	palavra* palavras;
	int final;
	int max;
} vetor;

void criaPalavra(palavra* nova, char* pa)
{
	//Inicializa ocorrencia e nome
	nova->ocorrencia = 1;
	if(nova->nome != NULL) free(nova->nome);
	
	//Insere o nome
	nova->nome = malloc(strlen(pa)*sizeof(char));
	int i = 0;
	while(pa[i] != '\0'){
		nova->nome[i] = pa[i];
		i++;
	}
	nova->nome[i] = pa[i]; //coloca '\0' no final
}

void insereVD(vetor* v, char* pa)
{
	//Percorre o vetor para encontrar a palavra
	int posicao;
	for(posicao = 0; posicao < v->final && strcmp(v->palavras[posicao].nome, pa) != 0; posicao++);

	//Se nao encontrou a palavra, insere no final
	if(posicao == v->final){
		//Se o tamanho estorou, realoca
		if(v->max == v->final){
			v->palavras = (palavra*) realloc(v->palavras, 2*v->max*(sizeof(palavra)));
			v->max *= 2;
		}
		criaPalavra(&(v->palavras[v->final]), pa);
		v->final++;
	}
	
	//Se encontrou a palavra, incrementa a ocorrencia dela
	else
		v->palavras[posicao].ocorrencia++;
	
}

void insereVO(vetor* v, char* pa)
{        
    //Encontra a posicao com Busca Binaria
	int posicao = 0;
	int compara;
    int inicio = 0;
    int fim = v->final;

	//Busca binaria iterativa
    while (inicio < fim)
    {	
		posicao = (inicio + fim) / 2;
        compara = strcmp(v->palavras[posicao].nome, pa);
		//Se encontrei a palavra, apenas aumenta a ocorrencia
        if (compara == 0){
			v->palavras[posicao].ocorrencia++;
			return;
		}
        else if (compara > 0) fim = posicao;     
        else inicio = posicao + 1;
    }
	
	posicao = (inicio + fim) / 2;
	
	//Nao encontrei a palavra
	
	//Se estorou o tamanho, realloca
	if(v->max == v->final){
		v->palavras = (palavra*) realloc(v->palavras, 2*v->max*(sizeof(palavra)));
		v->max *= 2;
	}
	
	//Empurra todos os elementos para a direita
	for(int i = v->final; i > posicao; i--){
		criaPalavra(&(v->palavras[i]), v->palavras[i - 1].nome);
		v->palavras[i].ocorrencia = v->palavras[i - 1].ocorrencia;
	}
	
	//Insere na posicao
	criaPalavra(&(v->palavras[posicao]), pa);
	
	v->final++;
}


//Troca duas palavras do vetor
void troca(vetor* v, int i, int j)
{
	palavra aux = v->palavras[i];
	v->palavras[i] = v->palavras[j];
	v->palavras[j] = aux;	
}

/*Separa do Sedgewick visto em aula*/
//Um para cada ordenacao
int separaPalavra(vetor* v, int ini, int fim)
{
	int i = ini - 1;
	palavra pivo = v->palavras[fim - 1];
	for(int j = ini; j < fim; j++)
		if(strcmp(v->palavras[j].nome,pivo.nome) <= 0){
			i++;
			troca(v, i, j);
		}
	
	return i;
}

int separaOcorrencia(vetor* v, int ini, int fim)
{
	palavra pivo = v->palavras[fim - 1];
	int i = ini - 1;
	for(int j = ini; j < fim; j++)
		if(v->palavras[j].ocorrencia > pivo.ocorrencia || (v->palavras[j].ocorrencia == pivo.ocorrencia && strcmp(v->palavras[j].nome,pivo.nome) <= 0)){
			i++;
			troca(v, i, j);
		 }
	
	return i;
}

/*  Quicksort visto em aula*/
void ordenaVetorPalavra(vetor* v, int ini, int fim){
	int pivo;
	if(fim - ini >= 2){
		pivo = separaPalavra(v, ini, fim);
		ordenaVetorPalavra(v, pivo, fim);
		ordenaVetorPalavra(v, ini, pivo);
	}
}

void ordenaVetorOcorrencia(vetor* v, int ini, int fim){
	int pivo;
	if(fim - ini >= 2){
		pivo = separaOcorrencia(v, ini, fim);
		ordenaVetorOcorrencia(v, pivo, fim);
		ordenaVetorOcorrencia(v, ini, pivo);
	}
}
