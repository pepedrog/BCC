/**********************
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

**********************/

// excessões pedidas
import java.lang.IllegalArgumentException;
import java.lang.UnsupportedOperationException;
import java.util.NoSuchElementException;

// pode ser útil
//import java.util.Arrays; // Arrays.sort(), Arrays.copyOf(), ...

import java.util.Iterator; // passo 0 para criarmos um iterador

import edu.princeton.cs.algs4.StdOut;

public class Deque<Item> implements Iterable<Item> {


      private int n;
      private Node first;
      private Node last;

      private class Node{

        Item item;
        Node prox;
	      Node ant;

        public Node(Item item){
          this.item = item;
          this.prox = this;
          this.ant = this;
        }

    }

    // is the deque empty?
    public boolean isEmpty(){
	     return n == 0;
    }

    // return the number of items on the deque
    public int size(){
	     return n;
    }

    // add the item to the front
    public void addFirst(Item item){

	     Node novo = new Node(item);
       if(first == null) first = novo;
	     else{
         Node last = first.ant;
         first.ant = novo;
         novo.prox = first;
         novo.ant = last;
         first = novo;
       }
       n++;
    }

    // add the item to the back
    public void addLast(Item item){
      Node novo = new Node(item);
      novo.prox = first;
	    if(first != null){
	       novo.ant = first.ant;

         first.ant.prox = novo;
	       first.ant = novo;
         n++;
	    }
      else this.addFirst(item);
    }

    // remove and return the item from the front
    public Item removeFirst(){

      if(this.isEmpty()) return null;

      Node aux = first;

      if(n == 1) first = null;
      else{

        first = aux.prox;
        first.ant = aux.ant;
      }

	    n--;

      return aux.item;

    }

    // remove and return the item from the back
    public Item removeLast(){

      if(this.isEmpty()) return null;


      Node aux = first.ant;

      if(n == 1) first = null;


      else{
        first.ant = first.ant.ant;
	       first.ant.prox = first;
      }
      n--;
      return aux.item;

    }

    // return an iterator over items in order from front to back
    public Iterator<Item> iterator(){

      return new DequeIterator();
    }
    private class DequeIterator implements Iterator<Item> {

    private int passo;
    private Node atual;
    public DequeIterator(){
      atual = first;
      passo = 0;
    }
		//Iniciando a variavel que percorrerá os arranjos
    public boolean hasNext(){
            return passo < n;
    }

		public Item next() {
      Node retorno = atual;
      if(hasNext() && retorno != null){
        atual = retorno.prox;
        passo++;
        return retorno.item;
      }

      throw new NoSuchElementException();


		}
        public void remove() {
            throw new UnsupportedOperationException();
        }
    }

    // unit testing (required)
    public static void main(String[] args){
      Integer[] v = {new Integer(100), new Integer(200), new Integer(123), new Integer(345) };
      Integer[] f = {new Integer(9), new Integer(99), new Integer(999), new Integer(3499995) };

	  Deque<Integer> d = new Deque<Integer>();
StdOut.println("Vamos fazer um Deque de inteiros\nInserindo inteiros, no inicio e no fim");
      for(int i = 0; i<4; i++){
        d.addLast(new Integer(4));
        d.addFirst(v[i]);
        d.addLast(f[i]);
	  }

/*
      int a = d.size();
      for(int i = 0; i < a; i++) StdOut.println(d.removeFirst());
	   //StdOut.println(d.removeLast());

     for(int i = 0; i<4; i++){
       d.addLast(new Integer(5));
       d.addFirst(v[i]);
       d.addLast(f[i]);
    }

     for(int i = 0; i < a; i++) StdOut.println(d.removeLast());
//
Iterator<Integer> it = d.iterator();
        for (int i = 0; it.hasNext() && i < 10; i++) {            StdOut.println(i + " : " + it.next());   StdOut.println("entrei");
      }*/
		StdOut.println("Vamos iterar por essa lista");
	int i = 0;
	for (Integer itt: d) {
       StdOut.println(i + " : " + itt);
       i++;
   }
		
		StdOut.println("Vamos removendo do começo");
		int a = d.size();
      for(int j = 0; j < a; j++) StdOut.println(d.removeFirst());
		
	if(d.size() == 0) StdOut.println("Nosso deque está vazio!");
		
		
    }

}