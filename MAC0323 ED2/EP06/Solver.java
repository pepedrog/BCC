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
		
		Meu programa algumas vezes mais que o que estava no enunciado do paca, mas parece estar de acordo com as otimizações,
		Talvez seja por causa do meu neighbors muito demorado, como explicado no arquivo Board.java
		

****************************************************************/


import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.Stack;
import edu.princeton.cs.algs4.MinPQ;

import java.lang.IllegalArgumentException;

public class Solver {
	
	private MinPQ<SearchNode> fila;
	private SearchNode ultimo;
	
	//Classe bem simples para fazer a fila priorizada
	private class SearchNode implements Comparable<SearchNode>{
		
		public SearchNode previous;
		public Board board;
		public int moves;
		
		public SearchNode(Board b, SearchNode previous, int moves){
			//Setando os atributos
			this.board = b;
			this.previous = previous;
			this.moves = moves;
		}
		
		public int priority(){
			return this.moves + this.board.manhattan();	
		}
		
		//Função de comparação das prioridades
		public int compareTo(SearchNode s){
			if(this.priority() > s.priority()) return 1;
			if(this.priority() < s.priority()) return -1;
			return 0;
		}
	}
	
    // find a solution to the initial board (using the A* algorithm)
    public Solver(Board initial){
		
		//Se não tiver solução
		if(!initial.isSolvable()) throw new IllegalArgumentException();
		
		//Iniciando a minPQ
		fila = new MinPQ<SearchNode>();
		SearchNode primeiro = new SearchNode(initial, null, 0);
		fila.insert(primeiro);
		
		SearchNode min;
		Iterable<Board> it;
		
		min = fila.delMin();
		
		//Enquanto não achamos uma solução
		while(!min.board.isGoal()){
			
			//Coloca os vizinhos na fila
			it = min.board.neighbors();
			for(Board vizinho: it)
				//Se o vizinho não for igual ao anterior, insere
				if(!vizinho.equals(min.previous)) fila.insert(new SearchNode(vizinho, min, min.moves + 1));
			
			//pega o próximo
			min = fila.delMin();	
			
		}
		
		//Guardar o ultimo para poder voltar e achar p caminho
		ultimo = min;
		
	}

    // min number of moves to solve initial board
    public int moves(){
		
		//Vai contando o numero de passos da solução
		int move = 0;
		
		SearchNode caminho = ultimo;
		while(caminho != null) {
			caminho = caminho.previous;
			move++;
		}
		
		return --move;
	}

    // sequence of boards in a shortest solution
    public Iterable<Board> solution(){
		
		//Vai percorrendo a solução e colocando na pilha, quando for desempilhada, veremos a ordem correta
		Stack<Board> pilha = new Stack<Board>(); 
		SearchNode caminho = ultimo;
		while(caminho != null){
			pilha.push(caminho.board);
			caminho = caminho.previous;
		}
		
		return pilha;
	}

    // test client (see below) 
    public static void main(String[] args){
		
		//Mesmo exemplo usado no teste do Board
		int[][] g = {{8,1,3},{4,0,2},{7,6,5}};
		Board b = new Board(g);
		Solver s = new Solver(b);
		
		StdOut.println(s.moves());
		Iterable<Board> is = s.solution();
		
		for(Board v : is){
			StdOut.println(v.toString());
		}
	}

}