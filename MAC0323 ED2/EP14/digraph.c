/****************************************************************
    Nome: Pedro Gigeck Freire
    NUSP: 10737136

    Ao preencher esse cabeçalho com o meu nome e o meu número USP,
    declaro que todas as partes originais desse exercício programa (EP)
    foram desenvolvidas e implementadas por mim e que portanto não 
    constituem desonestidade acadêmica ou plágio.
    Declaro também que sou responsável por todas as cópias desse
    programa e que não distribui ou facilitei a sua distribuição.
    Estou ciente que os casos de plágio e desonestidade acadêmica
    serão tratados segundo os critérios divulgados na página da 
    disciplina.
    Entendo que EPs sem assinatura devem receber nota zero e, ainda
    assim, poderão ser punidos por desonestidade acadêmica.

    Abaixo descreva qualquer ajuda que você recebeu para fazer este
    EP.  Inclua qualquer ajuda recebida por pessoas (inclusive
    monitoras e colegas). Com exceção de material de MAC0323, caso
    você tenha utilizado alguma informação, trecho de código,...
    indique esse fato abaixo para que o seu programa não seja
    considerado plágio ou irregular.

    Exemplo:

        A monitora me explicou que eu devia utilizar a função xyz().

        O meu método xyz() foi baseada na descrição encontrada na 
        página https://www.ime.usp.br/~pf/algoritmos/aulas/enumeracao.html.

    Descrição de ajuda ou indicação de fonte:
		
		Uma tradução bastante direta do Digraph do algs4

    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:
	
		Na função clone, fiz a versão que utiliza pilha para preservar a ordem das adjacencias
		Porém, a cada iteração é necessário esvaziar a pilha, o que faz a complexidade aumentar um pouco
		
		Embora seja igual ao do .java do algs4, lá ele não explicitamente faz o free, deixa o coletor de lixo do java
		Mas creio que o coletor faça algo muito semelhante do free, certo? :D

****************************************************************/


/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * ADT Digraph implementada atrevés de vetor de listas de adjacência.
 * As listas de adjacência são bag de ints que são mais restritos 
 * que as bags genéricas do EP12. Veja a api bag.h e simplifique 
 * o EP12 de acordo. 
 *  
 * Busque inspiração em: 
 *
 *    https://algs4.cs.princeton.edu/42digraph/ (Graph representation)
 *    https://algs4.cs.princeton.edu/42digraph/Digraph.java.html
 * 
 * DIGRAPH
 *
 * Digraph representa um grafo orientado de vértices inteiros de 0 a V-1. 
 * 
 * As principais operações são: add() que insere um arco no digrafo, e
 * adj() que itera sobre todos os vértices adjacentes a um dado vértice.
 * 
 * Arcos paralelos e laços são permitidos.
 * 
 * Esta implementação usa uma representação de _vetor de listas de adjacência_,
 * que  é uma vetor de objetos Bag indexado por vértices. 

 * ATENÇÃO: Por simplicidade esses Bag podem ser int's e não de Integer's.
 *
 * Todas as operações consomen no pior caso tempo constante, exceto
 * iterar sobre os vértices adjacentes a um determinado vértice, cujo 
 * consumo de tempo é proporcional ao número de tais vértices.
 * 
 * Para documentação adicional, ver 
 * https://algs4.cs.princeton.edu/42digraph, Seção 4.2 de
 * Algorithms, 4th Edition por Robert Sedgewick e Kevin Wayne.
 *
 */

/* interface para o uso da funcao deste módulo */
#include "digraph.h"


#include "bag.h"     /* add() e itens() */
#include <stdio.h>   /* fopen(), fclose(), fscanf(), ... */
#include <stdlib.h>  /* free() */
#include <string.h>  /* memcpy() */
#include "util.h"    /* emalloc(), ecalloc() */

#undef DEBUG
#ifdef DEBUG
#include <stdio.h>   /* printf(): para debuging */
#endif

/*----------------------------------------------------------*/
/* 
 * Estrutura básica de um Digraph
 * 
 * Implementação com vetor de listas de adjacência.
 */
struct digraph 
{
	/* Quantidade de vertices */
	int V;
	/* Quantidade de arestas/arcos */
	int E;
	/* Vetor de listas de adjacencias*/
	Bag * adj;
	/* Vetor para guardar a quantidade de arcos chegando em cada vertice */
	/* Poupando varrer todo o grafo para contar */
	int * indegree;
};

/*-----------------------------------------------------------*/
/*
 *  newDigraph(V)
 *
 *  RECEBE um inteiro V.
 *  RETORNA um digrafo com V vértices e 0 arcos.
 * 
 */
Digraph
newDigraph(int V)
{
	vertex i; /* index dos loops */
	
	Digraph novo = emalloc(sizeof(struct digraph));
	
	novo->adj = emalloc(V*sizeof(Bag));
	novo->indegree = emalloc(V*sizeof(vertex));
	
	for(i = 0; i < V; i++){
		novo->adj[i] = newBag();
		novo->indegree[i] = 0;
	}
	
	novo->V = V;
	novo->E = 0;
	
    return novo;
}

/*-----------------------------------------------------------*/
/*
 *  cloneDigraph(G)
 *
 *  RECEBE um digrafo G.
 *  RETORNA um clone de G.
 * 
 */
Digraph
cloneDigraph(Digraph G)
{
	vertex ori, dest;
	Bag pilha;
	Digraph clone;
	
	clone = newDigraph(G->V);
	clone->E = G->E;
	
	/* copia todos as adjacencias */
	for(ori = 0; ori < G->V; ori++){
		pilha = newBag();
		/* varre os vizinhos de i em G e vai adicionando numa pilha */
		/* depois adicionamos da pilha no clone, então a ordem permanece a mesma */
		for(dest = itens(G->adj[ori], TRUE); dest != -1; dest = itens(G->adj[ori], FALSE))
			add(pilha, dest);
		for(dest = itens(pilha, TRUE); dest != -1; dest = itens(pilha, FALSE))
			add(clone->adj[ori], dest);
		
		clone->indegree[ori] = G->indegree[ori];
		freeBag(pilha);
	}
	
	
    return clone;
}

/*-----------------------------------------------------------*/
/*
 *  reverseDigraph(G)
 *
 *  RECEBE um digrafo G.
 *  RETORNA o digrafo R que é o reverso de G: 
 *
 *      v-w é arco de G <=> w-v é arco de R.
 * 
 */
Digraph
reverseDigraph(Digraph G)
{
	/* igual ao clone, só troca quem adiciona em quem */
	
    vertex ori, dest;
	Digraph reverse = newDigraph(G->V);
	reverse->E = G->E;
	
	/* copia todos as adjacencias */
	for(ori = 0; ori < G->V; ori++){
		/* varre os vizinhos da origem em G e vai adicionando a origem neles*/
		for(dest = itens(G->adj[ori], TRUE); dest != -1; dest = itens(G->adj[ori], FALSE)) add(reverse->adj[dest], ori);
		
		reverse->indegree[ori] = size(G->adj[ori]);
	}
	
    return reverse;
}

/*-----------------------------------------------------------*/
/*
 *  readDigraph(NOMEARQ)
 *
 *  RECEBE uma stringa NOMEARQ.
 *  RETORNA o digrafo cuja representação está no arquivo de nome NOMEARQ.
 *  O arquivo contém o número de vértices V, seguido pelo número de arestas E,
 *  seguidos de E pares de vértices, com cada entrada separada por espaços.
 *
 *  Veja os arquivos  tinyDG.txt, mediumDG.txt e largeDG.txt na página do 
 *  EP e que foram copiados do algs4, 
 * 
 */
Digraph
readDigraph(String nomeArq)
{
	int V, i;
	/* Variaveis para ler os valores */
	vertex ori, dest;
	/* Grafo de retorno */
	Digraph G;
	
	FILE * arq = NULL;
	
    /* abra arquivo com texto */
    arq = fopen(nomeArq, "r");
	
	/* Trata excessão */
	if (arq == NULL) {
        printf("ERRO: arquivo '%s' nao pode ser aberto.\n", nomeArq);
        exit(EXIT_FAILURE);
    }
	
	/* Começa a ler o grafo */
	
	/* Le V e E*/
	fscanf(arq, "%d", &V);
	G = newDigraph(V);
	fscanf(arq, "%d", &(G->E));
	
	/* Le os pares e adiciona */
	for(i = 0; i < G->E; i++){
		fscanf(arq, "%d %d", &ori, &dest);
		add(G->adj[ori], dest);
	}
	
	fclose(arq);
	
    return G;
}


/*-----------------------------------------------------------*/
/*
 *  freeDigraph(G)
 *
 *  RECEBE um digrafo G e retorna ao sistema toda a memória 
 *  usada por G.
 *
 */
void  
freeDigraph(Digraph G)
{
	int i;
	for(i = 0; i < G->V; i++) freeBag(G->adj[i]);
	free(G->adj);
	free(G->indegree);
	free(G);
}    

/*------------------------------------------------------------*/
/*
 * OPERAÇÕES USUAIS: 
 *
 *     - vDigraph(), eDigraph(): número de vértices e arcos
 *     - addEdge(): insere um arco
 *     - adj(): itera sobre os vizinhos de um dado vértice
 *     - outDegree(), inDegree(): grau de saída e de entrada
 *     - toString(): usada para exibir o digrafo 
 */

/*-----------------------------------------------------------*/
/* 
 *  VDIGRAPH(G)
 *
 *  RECEBE um digrafo G e RETORNA seu número de vertices.
 *
 */
int
vDigraph(Digraph G)
{
    return G->V;
    
}

/*-----------------------------------------------------------*/
/* 
 *  EDIGRAPH(G)
 *
 *  RECEBE um digrafo G e RETORNA seu número de arcos (edges).
 *
 */
int
eDigraph(Digraph G)
{
    return G->E;
}

/*-----------------------------------------------------------*/
/*
 *  addEdge(G, V, W)
 * 
 *  RECEBE um digrafo G e vértice V e W e INSERE o arco V-W  
 *  em G.
 *
 */
void  
addEdge(Digraph G, vertex v, vertex w)
{
	add(G->adj[v], w);
	G->indegree[w]++;
	G->E++;
}    


/*-----------------------------------------------------------*/
/* 
 *  ADJ(G, V, INIT)
 * 
 *  RECEBE um digrafo G, um vértice v de G e um Bool INIT.
 *
 *  Se INIT é TRUE,  ADJ() RETORNA o primeiro vértice na lista de adjacência de V.
 *  Se INIT é FALSE, ADJ() RETORNA o sucessor na lista de adjacência de V do 
 *                   último vértice retornado.
 *  Se a lista de adjacência de V é vazia ou não há sucessor do último vértice 
 *  retornada, ADJ() RETORNA -1.
 *
 *  Se entre duas chamadas de ADJ() a lista de adjacência de V é alterada, 
 *  o comportamento é  indefinido. 
 *  
 */
int 
adj(Digraph G, vertex v, Bool init)
{	
    return itens(G->adj[v], init);
}

/*-----------------------------------------------------------*/
/*
 *  outDegree(G, V)
 * 
 *  RECEBE um digrafo G e vértice V.
 *  RETORNA o número de arcos saindo de V.
 *
 */
int
outDegree(Digraph G, vertex v)
{
    return size(G->adj[v]);
}

/*-----------------------------------------------------------*/
/*
 *  inDegree(G, V)
 * 
 *  RECEBE um digrafo G e vértice V.
 *  RETORNA o número de arcos entrando em V.
 *
 */
int
inDegree(Digraph G, vertex v)
{
    return G->indegree[v];
}


/*-----------------------------------------------------------*/
/*
 *  toString(G)
 * 
 *  RECEBE um digrafo G.
 *  RETORNA uma string que representa G. Essa string será usada
 *  para exibir o digrafo: printf("%s", toString(G)); 
 *    
 *  Sigestão: para fazer esta função inspire-se no método 
 *  toString() da classe Digraph do algs4.
 */

String
toString(Digraph G)
{
	
	vertex i, j;
	String s;
	
	/*considerando que V e E tem até 6 dígitos (que é isso que cabe num int)*/
	String v = emalloc(7*sizeof(char));
	String e = emalloc(14*sizeof(char));;
	
	/* Aloca a string com um tamanho da primeira frase + as listas */
	s = emalloc((30 + 10*(G->E)) * sizeof(char));
	
	sprintf(s, "%d vertices, %d edges\n", vDigraph(G), eDigraph(G));
	
	/* Percorre o vetor de listas  */
	for(i = 0; i < G->V; i++){
		sprintf(v, "%d: ", i);
		strcat(s, v);
		/* percorre as listas */
		for(j = itens(G->adj[i], TRUE); j != -1; j = itens(G->adj[i], FALSE)){
			sprintf(e, "%d ", j);
			strcat(s, e);
		}
		strcat(s, "\n");
	}
	
	free(v);
	free(e);
	
	
    return s;
}

/*------------------------------------------------------------*/
/* 
 * Implementaçao de funções administrativas: têm o modificador 
 * static.
 */

