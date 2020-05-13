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

****************************************************************/

import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.Stopwatch;

public class PercolationStats {

	//Atributos da classe
	private int n, t;
	private Percolation p;
	
	//Onde guardaremos os números de 'sites' abertos
	private int testes[];
	
    //Construtor, que fará os t testes no grid n por n
    public PercolationStats(int n, int trials){
		
		//Setando atributos
		this.n = n;
		this.t = trials;
		this.testes = new int[t];
		
		//Fazendo os testes
		for(int i = 0; i < t; i++){
			
			//'Zera' o grid, criando um novo todo bloqueado
			p = new Percolation(n);
			
			//Enquanto não 'percola', vai abrindo novos sites aleatoriamente
			while(!p.percolates()) p.open(StdRandom.uniform(n), StdRandom.uniform(n));
			
			//Guarda quantod sites foram abertos
			testes[i] = p.numberOfOpenSites();
			
			/* PS: Preferi guardar os inteiros e apenas fazer a divisão por n² depois, por questão de precisão (quanto menos divisões, mais preciso) */

		}
	}

    //Media simples usando a biblioteca sugerida StdStats
    public double mean(){
		
		//Faz a media dos openSites e divide pelo total por ultimo
		return (StdStats.mean(testes)/(n*n));	
	}

    //Desvio Padrão usando a biblioteca sugerida StdStats
    public double stddev(){
		return (StdStats.stddev(testes)/(n*n));
	}

    //Limite inferior do intervalo de confiança de 95%
    public double confidenceLow(){
		return(this.mean() - 1.96*this.stddev()/(Math.sqrt(t)));
	}

    //Limite superior do intervalo de confiança de 95%
    public double confidenceHigh(){
		return(this.mean() + 1.96*this.stddev()/(Math.sqrt(t)));
	}

    //Unit test
	public static void main(String[] args){
	
		Stopwatch sw = new Stopwatch();
		
		PercolationStats ps = new PercolationStats(Integer.parseInt(args[0]), Integer.parseInt(args[1]));
		
		StdOut.printf("%-20s = %1.6f \n", "mean()", ps.mean());
		StdOut.printf("%-20s = %1.6f \n", "stddev()", ps.stddev());
		StdOut.printf("%-20s = %1.6f \n", "confidenceLow()", ps.confidenceLow());
		StdOut.printf("%-20s = %1.6f \n", "confidenceHigh()", ps.confidenceHigh());
		StdOut.printf("%-20s = %1.6f \n", "elapsed time", sw.elapsedTime());
	}

}