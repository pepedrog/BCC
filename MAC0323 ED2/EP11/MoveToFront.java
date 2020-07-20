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
	
	No encode() tem arquivos que ele considera o EOF como um caracter, outros não..
	Fiz com base na codificação do abra.txt do diretório textfiles (do jeito que dava certo para este)

****************************************************************/

import edu.princeton.cs.algs4.BinaryStdIn;
import edu.princeton.cs.algs4.BinaryStdOut;
import edu.princeton.cs.algs4.StdOut;

import java.lang.IllegalArgumentException;

public class MoveToFront {
	
	//Constantes
	private static final int R = 255; //Tamanho do alfabeto ASCII extendido
	
	private static class Node{
		
		char c;
		int freq;
		Node next;
		
		public Node(char c, Node next){
			this.next = next;
			this.c = c;
		}
	}
	
    // apply move-to-front encoding, reading from standard input and writing to standard output
    public static void encode(){
		
		//Montando a lista, adicionando de tras pra frente, como se fosse uma pilha
		Node lista = new Node((char) R, null);
		for(int i = R - 1; i >= 0; i--) lista = new Node((char) i, lista);
		
		char c;
		char index;
		Node atual, ant;
		
		//Comecando a leitura do texto
		//Enquanto existe texto, ou equivalentemente, while(c != EOF)
		while(!BinaryStdIn.isEmpty()){
			
			c = BinaryStdIn.readChar();
			//inicializando as variaveis para a busca
			index = (char) 0;
			ant = lista;
			atual = lista;

			//buscando c na lista
			while(atual.c != c){
			    index++;
			    ant = atual;
			    atual = atual.next;
			}

			//Escreve o index
			BinaryStdOut.write(index);

			//Move to Front
			ant.next = atual.next;
			Node aux = lista;
			lista = atual;
			lista.next = aux;

		}
		
		BinaryStdOut.close();
	}

    // apply move-to-front decoding, reading from standard input and writing to standard output
    public static void decode(){
		
		//Montando a lista, adicionando de tras pra frente, como se fosse uma pilha
		Node lista = new Node((char) R, null);
		for(int i = R - 1; i >= 0; i--) lista = new Node((char) i, lista);
		
		char c;
		char index;
		Node atual, ant;
		
		//Comecando a leitura do texto
		while(!BinaryStdIn.isEmpty()){
			
			//Leio o index que irei chegar
			index = BinaryStdIn.readChar();
			//Inicializando a busca
			atual = lista;
			ant = lista;
			
			//Percorre a lista até a index-ésima posição
			while(index > (char) 0){
				index--;
			    ant = atual;
			    atual = atual.next;
			}

			//Escreve o char do index
			BinaryStdOut.write(atual.c);

			//Move to Front
			ant.next = atual.next;
			Node aux = lista;
			lista = atual;
			lista.next = aux;	
			
		}
		
		BinaryStdOut.close();
	}

    // if args[0] is "-", apply move-to-front encoding
    // if args[0] is "+", apply move-to-front decoding
    public static void main(String[] args){
		
		if(args.length < 1)	throw new IllegalArgumentException("MoveToFront: Missing command line argument");
        else if (args[0].equals("-")) encode();
        else if (args[0].equals("+")) decode();
        else throw new IllegalArgumentException("MoveToFront: Illegal command line argument");
	}

}
