#include <stdio.h>
#include <stdlib.h>
#include "string.h"
#include "ctype.h"

#include "vetores.h"
#include "arvore.h"

typedef char* string;

int main(int argc, char** argv){

	FILE* texto = fopen(argv[1],"r");
	
	string estrutura = argv[2];
	
	//variaveis para armazenar o conteudo lido
	char letra;
	string pa = malloc(0);

	int tam_pa = 0;
	
	//Apenas inicializando cada estrutura
	vetor v;
	apontador lista = NULL;
	galho ab = NULL;
	
	
	// Vetores
	if(estrutura[0] == 'V')
	{		
		//Um vetor de funcoes apenas para nao precisar repetir o codigo para cada funcao
		void (**funcoes)() = malloc(2*sizeof(void*));
		funcoes[0] = insereVD;
		funcoes[1] = insereVO;

		//inicializando o vetor
		v.palavras = malloc(50*sizeof(palavra));
		v.final = 0;
		v.max = 50;
		
		//Definindo qual funcao usaremos (insere desordenado ou ordenado)
		int func;
		if(estrutura[1] == 'D') func = 0;
		else func = 1;
		
		//Lendo o arquivo
		while ((letra = fgetc(texto)) != EOF){
			//Enquando a sequencia for alfanumerica
			if(isalnum(letra)){
				//Transforma em minusculo
				letra = tolower(letra);
				//Concatena na palavra
				pa = (string) realloc(pa, tam_pa + 1);
				pa[tam_pa] = letra;
				pa[tam_pa + 1] = '\0';
				tam_pa++;
			}
			//Quando acabar a sequencia
			else{
				//Se tiver uma palavra, insere no vetor
				if(tam_pa > 0) funcoes[func](&v, pa);
				tam_pa = 0;
			}
		}		
	}
	
	//Listas
	else if(estrutura[0] == 'L')
	{		
		//Vetor de funcoes apenas para nao reescrever o codigo pras duas funcoes
		apontador (**funcoes)() = malloc(2*sizeof(void*));
		funcoes[0] = insereLD;
		funcoes[1] = insereLO;
		
		//Definindo se ira inserir na lista desordenada ou ordenada
		int func;
		if(estrutura[1] == 'D') func = 0;
		else func = 1;
	
		//Mesma coisa que dos vetores
		while (fscanf(texto, "%c", &letra) != EOF)
			if(isalnum(letra)){
				letra = tolower(letra);
				pa = (string) realloc(pa, tam_pa + 1);
				pa[tam_pa] = letra;
				pa[tam_pa + 1] = '\0';
				tam_pa++;
			}
			else{
				if(tam_pa > 0) lista = funcoes[func](lista, pa);
				tam_pa = 0;
			}
		
		//Se inseri numa lista ordenada, e quero imprimir com a ordem alfabetica, posso apenas imprimir a lista
		if(func && argv[3][0] == 'A'){
			while(lista != NULL){
				printf("%s %d\n", lista->nome, lista->ocorrencia);
				lista = lista->prox;
			}
			return 0;
		}
	}

	else 
	{		
		//Mesma leitura do texto
		while (fscanf(texto, "%c", &letra) != EOF)
			if(isalnum(letra)){
				letra = tolower(letra);
				pa = (string) realloc(pa, tam_pa + 1);
				pa[tam_pa] = letra;
				pa[tam_pa + 1] = '\0';
				tam_pa++;
			}
			else{
				if(tam_pa > 0) ab = insereAB(ab, pa);
				tam_pa = 0;
			}
		
		//Transforma a arvore em lista, para transformar num vetor para imprimir
		lista = ArvoreParaLista(ab);				
	}
	
	//Limpa a palavra
	if(pa != NULL) free(pa);
	
	//Vamos colocar a lista ou a arvore que temos em um vetor, para entao ordenar e imprimir
	if(estrutura[0] != 'V'){
		
		//inicializa o vetor
		v.palavras = malloc(50*sizeof(palavra));
		v.final = 0;
		v.max = 50;
	
		//Percorre a lista inserindo no vetor
		while(lista != NULL){
			//Se acabar o vetor, realloca
			if(v.max == v.final){
				v.palavras = (palavra*) realloc(v.palavras, 2*v.max*(sizeof(palavra)));
				v.max *= 2;
			}
			
			v.palavras[v.final].nome = lista->nome;
			v.palavras[v.final].ocorrencia = lista->ocorrencia;
			lista = lista->prox;	
			v.final++;
		}
	}
	
	//Ordena o vetro de acordo com o esperado
	if(argv[3][0] == 'O') ordenaVetorOcorrencia(&v, 0, v.final);
	else ordenaVetorPalavra(&v, 0, v.final);
	
	//Imprime o vetor!
	for(int i = 0; i < v.final; i++) printf("%s %d\n",v.palavras[i].nome, v.palavras[i].ocorrencia);
	
}