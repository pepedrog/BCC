// MAC0328 (2019) Algoritmos em Grafos
// Aluno:      PEDRO GIGECK FREIRE
// Número USP: 10737136
// Tarefa:     A
// Data:       2019-08-07
//
// Solução baseada em ... <se for o caso> ...
//
// DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESTE PROGRAMA. TODAS
// AS PARTES DO PROGRAMA, EXCETO AS QUE FORAM FORNECIDAS PELO PROFESSOR
// OU COPIADAS DO LIVRO OU DAS BIBLIOTECAS DE SEDGEWICK OU ROBERTS,
// FORAM DESENVOLVIDAS POR MIM.  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR
// TODAS AS EVENTUAIS CÓPIAS DESTE PROGRAMA E QUE NÃO DISTRIBUI NEM
// FACILITEI A DISTRIBUIÇÃO DE CÓPIAS. 
//
////////////////////////////////////////////////////////////////////////

#include <GRAPHlists.h>
#include <time.h> //clock()

// Função auxiliar para gerar e printar as tabelas,
// printando os 4 primeiros e os 4 ultimos ou até chegar em m
void printTable(int grau[], int V, int m){
	int g[8];
	for (int i = 0; i < 7; ++i) g[i] = 0;
	for (vertex v = 0; v < V; ++v){
		if (grau[v] < 4) g[grau[v]]++;
		else if (grau[v] >= m - 3) g[7 - m + grau[v]]++;
	}
	for (int i = 0; i < 4 && i <= m; ++i) printf("g=%d\t%d\n", i, g[i]);
	for (int i = 3; i >= 0; --i) if(m - i > 3) printf("g=%d\t%d\n", m - i, g[7 - i]);
}

// Percorre todos os arcos para preprocessar
// o grau de entrada e saida dos vértices
void processDegrees(Graph G){
	int * outdegree = malloc(G->V * sizeof(int));
	int * indegree = malloc(G->V * sizeof(int));
	for (vertex v = 0; v < G->V; ++v){
		outdegree[v] = 0;
		indegree[v] = 0;
	}
	int maxout = 0;
	int maxin = 0;
	for (vertex v = 0; v < G->V; ++v){
		for(link a = G->adj[v]; a != NULL; a = a->next){
			if(++outdegree[v] > maxout) maxout = outdegree[v];
			if(++indegree[a->w] > maxin) maxin = indegree[a->w];
		}
	}
	printf("Vértices por grau de saída:\n");
	printTable(outdegree, G->V, maxout);
	printf("Vértices por grau de entrada:\n");
	printTable(indegree, G->V, maxin);
}

// Função auxiliar para gerar o grafo aleatoriamente
// através da função recebida como argumento
void GRAPHrand(int V, int A, Graph (*f)(int, int)){
	clock_t t0 = clock();
	Graph G = f(V, A);
	double t = (clock() - t0) / (double) CLOCKS_PER_SEC;
	printf("V: %d\nA: %d\ntempo: %f s\n", G->V, G->A, t);
	processDegrees(G);
	if (G->V < 30){
		printf("Listas de adjacências:\n");
		GRAPHshow(G);
	}

}
	
int main(int argc, char* argv[]){
	if (argc == 3){
		int V, A;
		V = atoi(argv[1]);
		A = atoi(argv[2]);
		printf("GRAPHrand1():\n");
		GRAPHrand(V, A, GRAPHrand1);
		printf("------------------------------------------\n");
		printf("GRAPHrand2():\n");
		GRAPHrand(V, A, GRAPHrand2);
	}
}