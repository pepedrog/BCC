
typedef struct Elemento{
	char* nome;
	int ocorrencia;
	struct Elemento* prox;
} elemento;

typedef elemento* apontador;

apontador criaElemento(apontador, char*);
//Cria um elemento no inicio da lista passada

apontador insereLD(apontador, char*);
//Insere no inicio da lista

apontador insereLO(apontador, char*);
//Insere em ordem alfabetica