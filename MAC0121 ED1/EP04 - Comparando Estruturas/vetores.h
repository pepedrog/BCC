
typedef struct {
	char* nome;
	int ocorrencia;
} palavra;

typedef struct{
	palavra* palavras;
	int final;
	int max;
} vetor;

//Um vetor de structs palavra

void criaPalavra(palavra*, char*);
//Cria a palavra na posicao passada

void insereVD(vetor*, char*);
//Insere no final do vetor

void insereVO(vetor*, char*);
//Busca a posicao e insere

//Parte para o quicksort

void troca(vetor*, int, int);
//Troca as duas posicoes

int separaPalavra(vetor*, int, int);
int separaOcorrencia(vetor*, int, int);
//Separa do Sedgewick, visto em aula, para as duas ordenacoes

void ordenaVetorPalavra(vetor*, int, int);
void ordenaVetorOcorrencia(vetor*, int, int);
//Quicksort como visto em aula para as duas ordenacoes
