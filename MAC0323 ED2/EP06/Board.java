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
		
		O método equals() foi extraido (fortemente inspirado) do exemplo Date.java sugerido na página do Checklist


    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:
		
		No método neighbors, tive muita dificuldade com as cópias do vetor, não consegui achar ajuda eficiente na internet
		Sempre que eu modificava a cópia, o original também era modificado,
		Entao criei minha própria cópia, que aumentou (e muito) a complexidade do método, que era pra ser linear virou quadrático,
		Mas como a performance aceitada era até n² eu deixei dessa forma.

****************************************************************/


import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.Stack;

import java.lang.IllegalArgumentException;

public class Board {

	private int[][] board;
	private int n;
	private int i0, j0;
	private int hamming, manhattan;
	
    //Construtor
    public Board(int[][] tiles){
		
		//inicializando as variáveis de instância	
		n = tiles.length;
		board = new int[n][n];
		hamming = manhattan = 0;
		
		//Percorrendo o board para calcular manhattan e hamming		
		for(int i = 0; i < n; i++)
			for(int j = 0; j < n; j++){
				board[i][j] = tiles[i][j];
				if(tiles[i][j] != 0){
					//Calcula baseado nas posições que os números deveriam estar
					if(tiles[i][j] != i*n + j + 1) hamming++;
					manhattan += abs((tiles[i][j]-1)%n - j);
					manhattan += abs((tiles[i][j]-1)/n - i);
				}
				else{
					//Salvaremos a posição do zero para facilitar no cálculo dos vizinhos
					i0 = i; j0 = j;	
				}
			}
	}

                 
    //Representação String do board
    public String toString(){
		String s = new String();
		s += this.n + "\n";
		
		//percorre o board
		for(int i = 0; i < n; i++){
			for(int j = 0; j < n; j++){
				//formatação da especificação
				s += String.format("%2d ", tileAt(i, j));
;	
			}
			if(i < n - 1) s+="\n";
		}
		return s;	
	}

    //tile at (row, col) or 0 if blank
    public int tileAt(int row, int col){
		if(row < 0 || col < 0 || row >= n || row >= n) throw new IllegalArgumentException();
		return board[row][col];	
	}

    // board size n
    public int size(){
		return this.n;	
	}

    // number of tiles out of place
    public int hamming(){
		return this.hamming;
	}

    // sum of Manhattan distances between tiles and goal
    public int manhattan(){
		return this.manhattan;	
	}

    // is this board the goal board?
    public boolean isGoal(){
		return hamming == 0;	
	}

    // does this board equal y?
    public boolean equals(Object y){
		
		//Modelo copiado do Exemplo de Data.java (sugerido na página do checklist)
		if (y == this) return true;
        if (y == null) return false;
        if (y.getClass() != this.getClass()) return false;
        Board b_y = (Board) y;
        return (this.n == b_y.size() && this.toString().equals(b_y.toString()));
    }

    //Iteravel com todos os vizinhos
    public Iterable<Board> neighbors(){
		
		//Vamos guardá-los numa pilha
		Stack<Board> vizinhos = new Stack<Board>();
		int[][] copia = new int[n][n];
		
		//vizinho de cima
		if(i0 > 0){
			//reseta o board
			copy(copia);
			//faz a troca
			troca(copia, i0, j0, i0 - 1, j0);
			//empilha
			vizinhos.push(new Board(copia));
		}
		//vizinho de baixo
		if(i0 < n - 1){
			copy(copia);
			troca(copia, i0, j0, i0 + 1, j0);
			vizinhos.push(new Board(copia));
		}
		//vizinho da esquerda
		if(j0 > 0){
			copy(copia);
			troca(copia, i0, j0, i0, j0 - 1);
			vizinhos.push(new Board(copia));
		}
		//vizinho da direita
		if(j0 < n - 1){
			copy(copia);
			troca(copia, i0, j0, i0, j0 + 1);
			vizinhos.push(new Board(copia));
		}
		
		return vizinhos;
		
	}

    // is this board solvable?
    public boolean isSolvable(){
		
		int inversions = 0;
		
		//Percorre o board
		for(int i = 0; i < n; i++)
			for(int j = 0; j < n; j++)
				//Pra cada posição, percorre todos que tem a frente procurando um  número menor
				for(int k = i*n + j; k < n*n; k++)
					if(board[k/n][k%n] != 0 && board[k/n][k%n] < board[i][j]) inversions += 1;
		//Critérios estabelecidos no enunciado
		if(n%2 == 0) return (((inversions + i0)%2)==1);
		return inversions%2 == 0;
	}

    // unit testing
    public static void main(String[] args){
		int[][] g = {{8,1,3},{4,0,2},{7,6,5}};
		Board b = new Board(g);

		StdOut.println(b.toString());
		StdOut.println("Hamming = " + b.hamming());
		StdOut.println("Manhattan = " + b.manhattan());
		StdOut.println("Neighbors:");
		Iterable<Board> ib = b.neighbors();
		for(Board v : ib){
			StdOut.println(v.toString());
		}
		
		if(b.isSolvable()) StdOut.println("soluvel");
		else StdOut.println("insoluvel");
	}
	
	//troca as posicoes j e i de um board
	private static void troca(int[][] b, int i, int j, int novoi, int novoj){
		int a = b[i][j];
		b[i][j] = b[novoi][novoj];
		b[novoi][novoj] = a;
	}
		
	//Só um absolute para calcular o manhattan
	private static int abs(int x){
		if(x > 0) return x;
		return -x;
	}
	
	//Copia o board (e não as referencias)
	private void copy(int[][] copia){
		for(int i = 0; i < n; i++)
			for(int j = 0; j < n; j++)
				copia[i][j] = board[i][j];
	}

}