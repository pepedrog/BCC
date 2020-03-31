#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "elemento.h"
//int main(){printf("Lista funcionando \n");}

int stringsIguais(char* s1, char* s2)
{
	int i;
	for(i = 0; s1[i] != '\0' && s2[i] != '\0' && s1[i] == s2[i]; i++);
	if(s1[i] == '\0' && s2[i] == '\0') return 1;
	return 0;
}

Lista Lcria(void){
	//Instanciando uma lista e alocando o primeiro endereço (cabec)
	Lista s;
	s.cabec = malloc(sizeof(Elo));
	//Definindo o próximo elo vazio (fim da lista)
	s.cabec->next = NULL;
	s.cabec->val = NULL;
	return s;
}

int LBuscaTipoGlobal(Lista* sym_table, char * procurado){
	Elo* crawler = sym_table->cabec;
	while(crawler != NULL && crawler->val != NULL){
		if(stringsIguais(crawler->nome, procurado)){
			return crawler->tipo;
		}
		crawler = crawler->next;
	}
	return -1;
}

void *LBuscaGlobal(Lista* sym_table, char * procurado, char GRR){
	Elo* crawler = sym_table->cabec;
	while(crawler != NULL & crawler->val != NULL){
		//printf("procurado %s e atual %s\n", procurado, crawler->nome);
		if(stringsIguais(crawler->nome, procurado)){
			if(GRR == 'P') return crawler->val;
			else return crawler->nome;
		}
		crawler = crawler->next;
	}
	return NULL;

}

Lista *LinsereGlobal (Lista *sym_table, char *sym_name, int sym_type, void *val)
{

  Elo* novo =  malloc(sizeof(Elo));

	novo->nome = (char *) malloc (strlen (sym_name) + 1);
	strcpy(novo->nome,sym_name);

	novo->tipo = sym_type;
	novo->val = val;
	if(sym_table != NULL) novo->next = sym_table->cabec;
	else novo->next == NULL;
	/*
  Elo* crawler = novo;
  int i = 0;
	while(crawler != NULL){
		crawler = crawler->next;
		printf("%s - ", crawler->nome);
		i++;
	}
	*/
	Lista* nova = malloc(sizeof(Lista));
	nova->cabec = novo;
	//Elo* crawler = novo;
	/*while(crawler != NULL){
		printf("%s -  ",crawler->nome);
		crawler = crawler->next;
	}*/
  return nova;
}


void Ldestroi(Lista lista1){
	//Endereço de elo que percorrerá a lista
	Elo* crawler = lista1.cabec;
	//Enquanto não chegar no final da lista
	while(crawler != NULL){
		//Salva o endereço do atual
		Elo* aux = crawler;
		//Avança o crawler (para desalocar o próximo)
		crawler = crawler->next;
		//Limpa o atual
		//if(aux->val != NULL) printf("Estamos livrando o %s\n",aux->val->nome);
		aux->val = NULL;
		free(aux);
	}
	return;
}

Elo* Linsere(Lista lista1, Elemento* val){
	//Percorre a lista até chegar no final (crawler == NULL) ou chegar em alguma posição vazia (crawler->val == NULL)
	Elo* crawler = lista1.cabec;
	while(crawler != NULL && crawler->val != NULL){
		//Achando o último elemento da lista e inserindo mais um
		if(crawler->next == NULL)
		{
			Elo* proximo = malloc(sizeof(Elo));
			proximo->val = val;
			proximo->next = NULL;
			crawler->next = proximo;
			return (crawler->next);

		}
		crawler = crawler->next;
	}

	//Se achou uma posição sem valor, podemos apenas inserir
	if(crawler != NULL) crawler->val = val;
	return crawler;
}

Elemento* Lbusca(Lista lista1, char* n){
	//Mesma estrutura do insere, percorre a lista até achar ou chegar no final
	Elo* crawler = lista1.cabec;
	Elemento* e = (Elemento*) crawler->val;
	while(crawler != NULL){
		e = (Elemento*) crawler->val;
		if(crawler->val != NULL && stringsIguais(e->nome, n)){
			return crawler->val;
		}
		crawler = crawler->next;
	}
	return NULL;
}

Elemento* Lretira(Lista lista1, Elemento* val){
	//Percorre a lista até encontrar o elemento
	Elo* crawler = lista1.cabec;
	Elemento* e;
	while(crawler != NULL){
		if(crawler->val == val){
			e = (Elemento *) crawler->val;
			//Apaga o antigo valor e anula o ponteiro
			free(e->nome);
			free(crawler->val);
			crawler->val = NULL;
			return val;
		}
		crawler = crawler->next;
	}
	return NULL;
}
