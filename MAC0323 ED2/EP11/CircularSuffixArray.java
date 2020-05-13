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
	Uso o Quick3sort do algs4, indicado pelo coelho no paca
	Tbm uso a ideia da classe comparavel CircularSuffix, sugerido no checklist

    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:
	
	Minha ordenação não é examente n lg n :(
	Como colocado no paca, comparar strings pode custar bastante.. 
	porém, na média, em um texto em ingles regular, ele se da bem 

****************************************************************/

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.Quick3way;

import java.lang.IllegalArgumentException;

public class CircularSuffixArray {
	
	private String s; // string original
	private int n;
	private CircularSuffix array[];
	
	private class CircularSuffix implements Comparable<CircularSuffix>{
		
		//Index da string original onde esse sufixo começa
		int index;
		
		public CircularSuffix(int i){
			this.index = i;
		}
		
		public int compareTo(CircularSuffix x){
			
			int dif;
			//Chega no primeiro index diferente dos dois sufixos
			for(dif = 0; s.charAt((this.index + dif)%n) == s.charAt((x.index + dif)%n); dif++);
			
			return (s.charAt((index + dif)%n) - s.charAt((x.index + dif)%n));
		}
		
	}
	
    // circular suffix array of s
    public CircularSuffixArray(String s){
		if(s == null) throw new java.lang.IllegalArgumentException();
		this.s = s;
		this.n = s.length();
		this.array = new CircularSuffix[n];
		
		//"percorre a string" (artificialmente) pra fazer o vetor
		for(int i = 0; i < n; i++) array[i] = new CircularSuffix(i);
		
		//ordena
		Quick3way.sort(array);
		
	}

    // length of s
    public int length(){
		return this.n;
	}

    // returns index of ith sorted suffix
    public int index(int i){
		if(i < 0 || i >= n) throw new java.lang.IllegalArgumentException();
		return array[i].index;	
	}

    // unit testing (required)
    public static void main(String[] args){
		
		//Exemplo do abracadabra
		CircularSuffixArray a = new CircularSuffixArray("ABRACADABRA!");
		for(int i = 0; i < a.length(); i++) StdOut.println(a.index(i) + ": " + a.s.substring(a.index(i), a.length()) + a.s.substring(0, a.index(i)));
		
		//CircularSuffixArray b = new CircularSuffixArray(null);
	}
}