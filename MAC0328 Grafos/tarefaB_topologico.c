#include "GRAPHlists.h"

// Função que recebe um grafo e um permutação dos vértices
// e retorna true se a permutação é topológica e false caso contrário
bool tperm(Graph G, vertex vv[])
{
	bool * visitado = malloc(G->V * sizeof(bool));
	for (int i = 0; i < G->V; ++i) visitado[i] = false;
	for (int i = 0; i < G->V; ++i){
		vertex v = vv[i];
		visitado[v] = true;
		for (link a = G->adj[v]; a != NULL; a = a->next)
			if (visitado[a->w]) return false;
	}
	return true;
}

bool top(Graph G)
{
	// Pré processamento do grau de entrada
	int * inDegree = malloc(G->V * sizeof(int));
	for (int i = 0; i < G->V; ++i) inDegree[i] = 0;
	for (vertex v = 0; v < G->V; ++v)
		for (link a = G->adj[v]; a != NULL; a = a->next)
			inDegree[a->w]++;
	
	vertex font = 0;
	int V = G->V;
	int topnum = 1;
	while (font < G->V){
		if (inDegree[font] == 0){
			inDegree[font] = topnum++;
			for (link a = G->adj[font]; a != NULL; a = a->next)
				inDegree[a->w]--;
			font = 0;
			V--;
		}
		else font++;
	}
	
	if (V == 0) return true;
	return false;
}

int main(int n, char** arg){
	Graph G = GRAPHrand2(atoi(arg[1]), atoi(arg[2]));
	GRAPHshow(G);
	if(top(G)) printf("SIM\n");
	else printf("Não\n");
	free(G);
}