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
	
	Leitura do input igual sugerido no fórum do paca


    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:

****************************************************************/

import edu.princeton.cs.algs4.BinaryStdIn;
import edu.princeton.cs.algs4.BinaryStdOut;
import edu.princeton.cs.algs4.StdOut;

import edu.princeton.cs.algs4.Quick3way;

public class BurrowsWheeler {

    // apply Burrows-Wheeler transform,
    // reading from standard input and writing to standard output 
    public static void transform(){
		
		// read the input
        String s = BinaryStdIn.readString(); // <<<<<<<<<<<
		
		int n = s.length();
		
		//Constroi o array
		CircularSuffixArray array = new CircularSuffixArray(s);
		
		//Percorre o array para encontrar o first
		for(int i = 0; i < n; i++) if(array.index(i) == 0){ BinaryStdOut.write(i); break; }
		
		//Percorre no array escrevendo na saída
		for(int i = 0; i < n; i++)
			//Escreve a ultima (primeira - 1) letra do i-ésimo sufixo
 			if(array.index(i) != 0) BinaryStdOut.write(s.charAt(array.index(i) - 1));
			else BinaryStdOut.write(s.charAt(n - 1));
				
		BinaryStdOut.close();
	}

	
    // apply Burrows-Wheeler inverse transform,
    // reading from standard input and writing to standard output
    public static void inverseTransform(){
		
		int first = BinaryStdIn.readInt();
		
		String s = BinaryStdIn.readString();
		int n = s.length();
		char lastColumn[] =  s.toCharArray();
		

		
		//Primeira coluna, que é a ordenação do input
		//Fazendo um vetor de Character, porque char não é Comparable :(
		Character firstColumn[] = new Character[n];
		for(int i = 0; i < n; i++) firstColumn[i] = lastColumn[i];
		Quick3way.sort(firstColumn);
		
		int next[] = new int[n];
		
		//inicializa next com valores nulos
		for(int i = 0; i < n; i++) next[i] = n;
		
		//Pra cada valor da first column, descobre o next
		for(int i = 0; i < n; i++){
			//acha o char da firstcolomn na lastColumn
			int j = 0;
			while(firstColumn[i] != lastColumn[j]) j++;
			next[i] = j++;
			
			//Vai preenchendo até mudar o caracter
			//Ja que os caracteres repetidos tem o next correspondente em ordem crescente
			while(i < n-1 && firstColumn[i] == firstColumn[i+1]){
				//acha o próximo j a partir do j anterior
				i++;
				while(firstColumn[i] != lastColumn[j]) j++;
				next[i] = j++;
			}
		}
		
		//Vai percorrendo a corrente de next até o final
		int atual = first;
		for(int i = 0; i < n; i++){
			BinaryStdOut.write(firstColumn[atual]);
			atual = next[atual];
		}
		
		BinaryStdOut.close();
		
	}

    // if args[0] is "-", apply Burrows-Wheeler transform
    // if args[0] is "+", apply Burrows-Wheeler inverse transform
    public static void main(String[] args){
		
		if(args.length < 1)	throw new IllegalArgumentException("MoveToFront: Missing command line argument");
        else if (args[0].equals("-")) transform();
        else if (args[0].equals("+")) inverseTransform();
        else throw new IllegalArgumentException("MoveToFront: Illegal command line argument");
		
	}

}