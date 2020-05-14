#include <stdio.h>
#include <stdlib.h>
#include "string.h"
int main(){
	/*
	int n, tam;
	char* palavra;
	scanf("%d", &n);
	for(int i = 0; i < n; i++){
		scanf("%s", palavra);
		tam = strlen(palavra);
		if(tam > 10) printf("%c%d%c\n", palavra[0], tam - 2, palavra[tam - 1]); 
		else printf("%s\n",palavra);
	}
	*/
	int n, tam;
	scanf("%d", &n);
	printf("%d", n);
	char** palavra = malloc(n*sizeof(char*));
	for(int i = 0; i < n; i++){
		scanf("%s", palavra[i]);
		printf("%s", palavra[i]);
	}
	printf("aa\n");
	for(int i = 0; i < n; i++){
		tam = strlen(palavra[i]);
		if(tam > 10) printf("%c%d%c\n", palavra[i][0], tam - 2, palavra[i][tam - 1]);
		else printf("%s\n",palavra[i]);
	}
	
}