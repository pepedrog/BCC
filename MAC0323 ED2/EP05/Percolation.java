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
		
		Segui muito de perto o especificado no enunciado e na página do checklist, inclusive, foi de lá a ideia de fazer o virtual_top, virtual_bottom


    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:
	
	Como não houve problemas com a API, não resolvi o erro que foi chamado de BackWash (se percolates, todos os conjuntos conectados a ultima linha ficam full)

****************************************************************/



import edu.princeton.cs.algs4.WeightedQuickUnionUF;
import edu.princeton.cs.algs4.StdOut;

public class Percolation {

	//Atributos da classe
	private WeightedQuickUnionUF grid;
    private int n, n_open;
	
	//grid auxiliar para controlar quais sites estao abertos 
    private boolean[] grid_open;
	
	//Posicoes ficticias auxiliares
    private int virtual_top, virtual_bottom, virtual_perc;
	
    //Construtor: inicia todos os atributos
    public Percolation(int n){
		
      	int sz = n*n;
		
	    virtual_top = sz;
      	virtual_bottom = sz + 1;
	  	virtual_perc = sz + 2;
		
      	grid = new WeightedQuickUnionUF(sz + 3);
      	this.n = n;
     
      	grid_open = new boolean[sz];
      	n_open = 0;

    }

    //Abre o site na posicao row,col
    public void open(int row, int col){
		
	  	//Validando posicao recebida
      	if(!isValid(row, col)) throw new IllegalArgumentException();
		
	  	//convertendo as coordenadas 2d (grid) para 1d (Union Find)
      	int pos = index(row, col);
		
	  	//Vetor apenas para facilitar a conferencia dos 4 vizinhos
      	int directions[][] = {{row + 1, col}, {row - 1, col}, {row, col + 1}, {row, col - 1}};

	  	//Se a posicao já não esta aberta
      	if(!grid_open[pos]){
		  
			//abre
        	n_open++;
        	grid_open[pos] = true;
		  
			//Se estiver na primeira linha, marcamos que é full (conectado com o virtual_top)
			if(pos < n) grid.union(pos, virtual_top);
		  
			//Se estiver na ultima linha, masrcamos que está conectado com o virtual_bottom (apenas para verificar se percolated)
			else if(pos >= n*(n - 1)) grid.union(pos, virtual_bottom);
		  
			//Para cada um dos 4 vizinhos
        	for(int i = 0; i < 4; i++){
			 
				//Se for uma casa válida e estiver aberta, conectamos os 2.
           		if(isValid(directions[i][0], directions[i][1]) && isOpen(directions[i][0], directions[i][1])){
					grid.union(pos, index(directions[i][0], directions[i][1]));
		   		}
			}
    	}
    }

    public boolean isOpen(int row, int col){
		
		//Valida os parametros
      	if(!isValid(row, col)) throw new IllegalArgumentException();
		//Apenas confere no grid
      	return grid_open[index(row, col)];
    }
	
	public boolean isFull(int row, int col){
      	//Valida os parametros
		if(!isValid(row, col)) throw new IllegalArgumentException();
	  	//Se está conectado com o virtual_top, então é full
      	return grid.connected(index(row, col), virtual_top);
    }

    public int numberOfOpenSites(){
      	return n_open;
    }

    public boolean percolates(){
		//Se o virtual_top está conectado com o virtal_bottom, então existe um caminho, logo, true	
      	return(grid.connected(virtual_top, virtual_bottom));
    }
		
	
    // unit testing (required)
    public static void main(String[] args){
		
		//Os melhores exemplos podem ser visualizados com o PercolationVisualizer, mas vamos fazer um teste 'improvisado'

    	StdOut.println("Vamos fazer um teste com n = 5");
		Percolation p = new Percolation(5);
		StdOut.println("Criamos o grid bloqueado");
		p.printGrid();
		
		StdOut.println("Adicionando alguns pontos");
		p.open(1,1);
		p.open(3,3);
		p.open(2,3);
		p.open(1,3);
		p.open(0,3);
		p.open(2,2);
		
		p.open(4,4);
		
		p.printGrid();
		StdOut.println("perculates? " + p.percolates());
		
		StdOut.println("Agora Vamos adicionar o ponto 3,4");
		
		p.open(3,4);
		p.printGrid();
		StdOut.println("perculates? " + p.percolates());
		
    }

	//Converte coordenadas 2D em 1D
    private int index(int row, int col){
		//Fazemos do jeito mais natural, "enfileirando" as linhas
      	return (row*n + col);
    }

	//Validador das posicoes
    private boolean isValid(int row, int col){
      	return (row < n && col < n && row >=0 && col >= 0);
    }

	//Funçãozinha quebra-galho para os testes
	private void printGrid(){
	
		for(int i = 0; i < n; i++){
			StdOut.println();
			for(int j = 0; j < n; j++){
				if(isFull(i,j)) StdOut.print(" F ");
				else if(isOpen(i,j)) StdOut.print(" O ");
				else StdOut.print(" - ");
			}
		}
		
		StdOut.println();
		StdOut.println();
		
	}
}
