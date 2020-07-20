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

    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:
	
	ATENÇÃÃO !!!!
	Meu programa não funciona!!!!
	Ele compila mas entra num loop infinito, favor não tentar executá-lo!!!!
	Não tive tempo de debugar :(
	Estou entregando de coração aberto para uma possível avaliação da lógica do código
	
	Abraços :D

****************************************************************/

/*
 * MAC0323 Algoritmos e Estruturas de Dados II
 * 
 * ADT Topological é uma "representação topológica" de digrafo.
 * Esta implementação usa ADT Digraph do EP13.
 *  
 * Busque inspiração em: 
 *
 *   https://algs4.cs.princeton.edu/42digraph/
 *   https://algs4.cs.princeton.edu/42digraph/DepthFirstOrder.java
 *   https://algs4.cs.princeton.edu/42digraph/Topological.java
 *   https://algs4.cs.princeton.edu/42digraph/DirectedCycle.java
 * 
 * TOPOLOGICAL
 *
 * Topological é uma ¨representação topológica" de um dado digrafo.
 * 
 * As principais operações são: 
 *
 *      - hasCycle(): indica se o digrafo tem um ciclo (DirectedCycle.java)
 *      - isDag(): indica se o digrafo é acyclico (Topological.java)
 *
 *      - pre(): retorna a numeração pré-ordem de um vértice em relação a uma dfs 
 *               (DepthFirstOrder.java)
 *      - pos(): retorna a numareção pós-ordem de um vértice em relação a uma dfs
 *               (DepthFirstOrder.java)
 *      - rank(): retorna a numeração topológica de um vértice (Topological.java)
 * 
 *      - preorder(): itera sobre todos os vértices do digrafo em pré-ordem
 *                    (em relação a uma dfs, DepthFirstOrder.java)
 *      - postorder(): itera sobre todos os vértices do digrafo em pós-ordem
 *                    (em relação a uma dfs, ordenação topologica reversa, 
 *                     DepthFirstOrder.java)
 *      - order(): itera sobre todos os vértices do digrafo em ordem  
 *                 topologica (Topological.java)
 *      - cycle(): itera sobre os vértices de um ciclo (DirectedCycle.java)
 *
 * O construtor e "destrutor" da classe consomem tempo linear..
 *
 * Cada chama das demais operações consome tempo constante.
 *
 * O espaço gasto por esta ADT é proporcional ao número de vértices V do digrafo.
 * 
 * Para documentação adicional, ver 
 * https://algs4.cs.princeton.edu/42digraph, Seção 4.2 de
 * Algorithms, 4th Edition por Robert Sedgewick e Kevin Wayne.
 *
 */

/* interface para o uso da funcao deste módulo */
#include "topological.h"

#include "digraph.h" /* Digraph, vDigraph(), eDigraph(), adj(), ... */
#include "bag.h"     /* add() e itens() */
#include "util.h"    /* emalloc(), ecalloc(), ERRO(), AVISO() */

#include <stdlib.h>  /* free() */

#undef DEBUG
#ifdef DEBUG
#include <stdio.h>   /* printf(): para debugging */
#endif
 

/*----------------------------------------------------------*/

/* 	
 * Estruturas auxiliares 
 *
 */

struct node
{
	vertex v;
	struct node * prox;
	struct node * ant;
};

typedef struct node * Node;

struct queue
{
	Node first;
	Node last;
	Node next;
	int n;
};	

typedef struct queue * Queue;

/* 
 * Estrutura básica de um Topological
 * 
 */
struct topological 
{
	Bool * marked;
	Bool * onStack;
	
	vertex * edgeTo;
	vertex * pre;
	vertex * pos;
	vertex * rank;
	
	Bag cycle;
	
	Queue preOrdem;
	Queue posOrdem;
	
	int preCounter;
	int posCounter;
};



/*------------------------------------------------------------*/
/* 
 * Protótipos de funções administrativas: tem modificador 'static'
 * 
 */
 
static Node newNode(vertex v, Node prox, Node ant);

static Queue newQueue();

static void enqueue(Queue q, vertex v);

static void freeQueue(Queue q);

static void dfs(Digraph G, vertex v, Topological t);

/*-----------------------------------------------------------*/
/*
 *  newTopological(G)
 *
 *  RECEBE um digrafo G.
 *  RETORNA uma representação topológica de G.
 * 
 */
Topological 
newTopological(Digraph G)
{
	Topological novo; vertex v; vertex i;
	int V;
	
	novo = emalloc(sizeof(struct topological));
	V = vDigraph(G);
	
	/* Alocando e setando os atributos */
	
	novo->preCounter = 0;
	novo->posCounter = 0;
	
	novo->marked = emalloc(V*sizeof(Bool));
	novo->onStack = emalloc(V*sizeof(Bool));
	novo->edgeTo = emalloc(V*sizeof(vertex));
	novo->pre = emalloc(V*sizeof(vertex));
	novo->pos = emalloc(V*sizeof(vertex));
	novo->rank = emalloc(V*sizeof(vertex));
	
	novo->cycle = newBag();
	
	novo->preOrdem = newQueue(V);
	novo->posOrdem = newQueue(V);
	
	for(v = 0; v < V; v++){
		novo->marked[v] = FALSE;
		novo->onStack[v] = FALSE;
	}
	
	/* Fazendo as dfs */
	for(v = 0; v < V; v++){
		if(!novo->marked[v]) dfs(G, v, novo);	
	}
	
	i = V - 1;
	
	for(v = postorder(novo, TRUE); v != -1; v = postorder(novo, FALSE))
		novo->rank[v] = i--;
	
    return novo;
}

/*-----------------------------------------------------------*/
/*
 *  freeTopological(TS)
 *
 *  RECEBE uma representação topologica TS.
 *  DEVOLVE ao sistema toda a memória usada por TS.
 *
 */
void  
freeTopological(Topological ts)
{
	/* Um free adequado pra cada atributo */
	free(ts->marked);
	free(ts->onStack);
	
	free(ts->edgeTo);
	free(ts->pre);
	free(ts->pos);
	
	freeBag(ts->cycle);
	freeQueue(ts->preOrdem);
	freeQueue(ts->posOrdem);
	
	free(ts);
}    

/*------------------------------------------------------------*/
/*
 *  OPERAÇÕES: 
 *
 */

/*-----------------------------------------------------------*/
/* 
 *  HASCYCLE(TS)
 *
 *  RECEBE uma representação topológica TS de um digrafo;
 *  RETORNA TRUE se o digrafo possui um ciclo e FALSE em caso 
 *  contrário.
 *
 */
Bool
hasCycle(Topological ts)
{
    if(ts == NULL) ERROR();
    return isEmpty(ts->cycle);
}

/*-----------------------------------------------------------*/
/* 
 *  ISDAG(TS)
 *
 *  RECEBE um representação topológica TS de um digrafo.
 *  RETORNA TRUE se o digrafo for um DAG e FALSE em caso 
 *  contrário.
 *
 */
Bool
isDag(Topological ts)
{
    /* ts é DAG <=> ts não tem ciclo */
    return !hasCycle(ts);
}

/*-----------------------------------------------------------*/
/* 
 *  PRE(TS, V)
 *
 *  RECEBE uma representação topológica TS de um digrafo e um 
 *  vértice V.
 *  RETORNA a numeração pré-ordem de V em TS.
 *
 */
int
pre(Topological ts, vertex v)
{
	return ts->pre[v];
    return -1;
}

/*-----------------------------------------------------------*/
/* 
 *  POST(TS, V)
 *
 *  RECEBE uma representação topológica TS de um digrafo e um 
 *  vértice V.
 *  RETORNA a numeração pós-ordem de V em TS.
 *
 */
int
post(Topological ts, vertex v)
{
	return ts->pos[v];
    return -1;
}

/*-----------------------------------------------------------*/
/* 
 *  RANK(TS, V)
 *
 *  RECEBE uma representação topológica TS de um digrafo e um 
 *  vértice V.
 *  RETORNA a posição de V na ordenação topológica em TS;
 *  retorna -1 se o digrafo não for um DAG.
 *
 */
int
rank(Topological ts, vertex v)
{
    if(!isDag(ts)) return -1;
	return ts->rank[v];
    
}

/*-----------------------------------------------------------*/
/* 
 *  PREORDER(TS, INIT)
 * 
 *  RECEBE uma representação topológica TS de um digrafo e um 
 *  Bool INIT.
 *
 *  Se INIT é TRUE,  PREORDER() RETORNA o primeiro vértice na ordenação pré-ordem de TS.
 *  Se INIT é FALSE, PREORDER() RETORNA o vértice sucessor do último vértice retornado
 *                   na ordenação pré-ordem de TS; se todos os vértices já foram retornados, 
 *                   a função retorna -1.
 */
vertex
preorder(Topological ts, Bool init)
{
	Node aux;
    if(init) ts->preOrdem->next = ts->preOrdem->first;
	
	if(ts->preOrdem->next == NULL) return -1;
	
	aux = ts->preOrdem->next;
	ts->preOrdem->next = ts->preOrdem->next->prox;
	return aux->v;
}

/*-----------------------------------------------------------*/
/* 
 *  POSTORDER(TS, INIT)
 * 
 *  RECEBE uma representação topológica TS de um digrafo e um 
 *  Bool INIT.
 *
 *  Se INIT é TRUE,  POSTORDER() RETORNA o primeiro vértice na ordenação pós-ordem de TS.
 *  Se INIT é FALSE, POSTORDER() RETORNA o vértice sucessor do último vértice retornado
 *                   na ordenação pós-ordem de TS; se todos os vértices já foram retornados, 
 *                   a função retorna -1.
 */
vertex
postorder(Topological ts, Bool init)
{
	Node aux;
    if(init) ts->posOrdem->next = ts->posOrdem->first;
	
	if(ts->posOrdem->next == NULL) return -1;
	
	aux = ts->posOrdem->next;
	ts->posOrdem->next = ts->posOrdem->next->prox;
	return aux->v;
}

/*-----------------------------------------------------------*/
/* 
 *  ORDER(TS, INIT)
 * 
 *  RECEBE uma representação topológica TS de um digrafo e um Bool INIT.
 *
 *  Se INIT é TRUE,  ORDER() RETORNA o primeiro vértice na ordenação topológica 
 *                   de TS.
 *  Se INIT é FALSE, ORDER() RETORNA o vértice sucessor do último vértice retornado
 *                   na ordenação topológica de TS; se todos os vértices já foram 
 *                   retornados, a função retorna -1.
 *
 *  Se o digrafo _não_ é um DAG, ORDER() RETORNA -1.
 */
vertex
order(Topological ts, Bool init)
{
	Node aux;
	if(init) ts->posOrdem->next = ts->posOrdem->last;
	
	if(ts->posOrdem->next == NULL) return -1;
	
	aux = ts->posOrdem->next;
	ts->posOrdem->next = ts->posOrdem->next->ant;
	return aux->v;
}

/*-----------------------------------------------------------*/
/* 
 *  CYCLE(TS, INIT)
 * 
 *  RECEBE uma representação topológica TS de um digrafo e um Bool INIT.
 *
 *  Se INIT é TRUE,  CYCLE() RETORNA um vértice em um ciclo do digrafo.
 *  Se INIT é FALSE, CYCLE() RETORNA o vértice  no ciclo que é sucessor do 
 *                   último vértice retornado; se todos os vértices no ciclo já 
 *                   foram retornados, a função retorna -1.
 *
 *  Se o digrafo é um DAG, CYCLE() RETORNA -1.
 *
 */
vertex
cycle(Topological ts, Bool init)
{
    if(isDag(ts)) return -1;
	return itens(ts->cycle, init);
	
}


/*------------------------------------------------------------*/
/* 
 * Implementaçao de funções administrativas: têm o modificador 
 * static.
 */

static Node newNode(vertex v, Node prox, Node ant){
	
	Node novo = emalloc(sizeof(struct node));
	novo->v = v;
	novo->prox = prox;
	novo->ant = ant;
	
	return novo;
	
}

static Queue newQueue(int n){
	
	Queue novo;
	novo = emalloc(n * sizeof(struct queue));
	novo->first = NULL;
	novo->last = NULL;
	novo->n = 0;
	
	return novo;
}

static void enqueue(Queue q, vertex v){
	
	if(q->n == 0){
		q->first = newNode(v, NULL, NULL);
		q->last = q->first;
		return;
	}
	
	q->last = newNode(v, q->last, NULL);
	q->next = q->last;
}

static void freeQueue(Queue q){
		
	Node aux;
	while(q->n > 0){
		
		aux = q->first->prox;
		free(q->first);
		
		q->first = aux;
		q->n--;
		
	}
	
	free(q);
		
}

static void dfs(Digraph G, vertex v, Topological t){
	
	vertex w, x;
	
	/* Marca todos os vetores */
	t->marked[v] = TRUE; 		  /* v foi visitado */
	t->onStack[v] = TRUE;         /* v está na pilha */
	
	
	/* antes de entrar nas recursões, coloca o v na pre ordem */
	enqueue(t->preOrdem, v);
	t->pre[v] = t->preCounter++;
	
	/* pra cada vizinho w de v, marca o caminho e chama a dfs */
	for(w = adj(G, v, TRUE); w != -1; w = adj(G, v, TRUE)){
		if(!t->marked[w]){
			t->edgeTo[w] = v;
        	dfs(G, w, t);
		}
	
		/* Se w está na pilha, então há um ciclo */
		/* se já tem um ciclo em t->cycle, não precisamos colocar outro */
		if(t->onStack[v] && isEmpty(t->cycle)){
			t->cycle = newBag();
            for (x = v; x != w; x = t->edgeTo[x]) {
                add(t->cycle, x);
            }
            add(t->cycle, w);
            add(t->cycle, v);
		}
	}
	
	
	/* apos sair das recursões, coloca o v na pos ordem e tira da pilha */
	t->onStack[v] = FALSE;
	
	enqueue(t->posOrdem, v);
    t->pos[v] = t->posCounter++;
}
