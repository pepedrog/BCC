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

public class CircularSuffixArray {
	
	private String s; // string original
	private n;
	private int array[];
	
	private class Node implements Comparable<Node>{
		
		char c;
		int index;
		
		public Node(char c, int i){
			this.c = c;
			this.index = i;
		}
		
		public int comparTo(Node x){
			return (int) (this.c - x.c);
		}
		
	}
	
    // circular suffix array of s
    public CircularSuffixArray(String s){
		
		this.s = s;
		this.n = s.lenght;
		this.array = new int[n];
		
		Node nodes[] = new Node[n];
		
		//percorre a string pra fazer um vetor de nós
		for(int i = 0; i < n; i++) nodes[i] = new Node(s.charAt(i), i);
		
	}

    // length of s
    public int length(){
		return this.n;
	}

    // returns index of ith sorted suffix
    public int index(int i){
		return array[i];	
	}

    // unit testing (required)
    public static void main(String[] args){
		
		CircularSuffixArray a = new CircularSuffixArray(new String("ABRACADABRA!"));
		
	}
}