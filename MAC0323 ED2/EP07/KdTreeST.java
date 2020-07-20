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
	A principio não tive certeza se podiamos usar estruturas prontas, então tinha implementado minha própria fila (comentado no fim do código)

****************************************************************/

import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.RectHV;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.Queue;
import edu.princeton.cs.algs4.Stack;

import java.util.Iterator;

public class KdTreeST<Value> {
	
	//Constantes para facilitar leitura
	private static final boolean horizontal = true;
	private static final boolean vertical = false;
	
	//Nó da árvore
	private class Node {
   		private Point2D p;      // Ponto
   		private Value val;      // Valor
  		private RectHV rect;    // Retângulo correspondente a esse nó (facilitando a busca)
   		private Node lb;        // Filho esquerdo
    	private Node rt;        // Filho direito
		
		//Construtor
		public Node(Point2D p, Value val, RectHV rect){
			this.p = p;
			this.val = val;
			this.rect = rect;
			this.lb = null;
			this.rt = null;
		}
	}
	
	//A Árvore
	private Node raiz;
	private int n;
	
    //Cnstroi a árvore vazia
    public KdTreeST(){
		this.raiz = null;	
		this.n = 0;
	}

    //Está vazia ?
    public boolean isEmpty(){ 
		return n == 0; 
	}

    //Numero de pontos
    public int size(){ 
		return this.n; 
	}

    //Assoccia o valor val ao ponto p
    public void put(Point2D p, Value val){
		
		if (p == null) throw new java.lang.NullPointerException();
		
		//Apenas chamamos a recursão para a raiz, onde
		//o nó pai é nulo e a orientação é vertical
		raiz = put(null, raiz, p, val, vertical);
		
	}
	
	//put recursivo
	private Node put(Node pai, Node no, Point2D p, Value val, boolean orientacao){
		
		//Base da recursão
		if(no == null){
			
			//Construindo o retangulo
			RectHV ret;
			if(pai == null)
				//Se o pai é nulo, estamo na raiz
				//o retângulo é todo o R²
				ret = new RectHV(Double.NEGATIVE_INFINITY, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY, Double.POSITIVE_INFINITY);
			else
				//Se não, construímos o retangulo 
				ret = novoRet(pai.rect, !orientacao, pai.p, p);
			
			//Criamos o nó
			Node retorno = new Node(p, val, ret);
			n++;
			return retorno;
		}
		
		
		//Passo da recursão
		
		//Vamos decidir se vamos para a direita ou esquerda, com base na orientação
		double cmp;
		if(orientacao == vertical) cmp = p.x() - no.p.x();
		else cmp = p.y() - no.p.y();
		
		//Confere se o que queremos inserir é o nó que estamos olhando primeiro, pois cmp == 0 não implica igualdade nesse caso
		if(p.equals(no.p)) no.val = val;
		//Decide aon de colocar (lb ou rt)
		else if(cmp >= 0) no.rt = put(no, no.rt, p, val, !orientacao);
		else no.lb = put(no, no.lb, p, val, !orientacao);
		
		return no;
	}
	
	//Função para gerar o retângulo do filho, com base no do pai
	private RectHV novoRet(RectHV retanguloPai, boolean orientacaoPai, Point2D pai, Point2D p){
		//Basicamente copiamos o retangulo do pai e apenas mexemos e uma das barreiras
		//Abaixo segue os 4 casos
		
		RectHV ret;
		
		if(orientacaoPai == vertical) {
			if(pai.x() > p.x())ret = new RectHV(retanguloPai.xmin(),retanguloPai.ymin(), pai.x(),retanguloPai.ymax());	
			else ret = new RectHV(pai.x(),retanguloPai.ymin(), retanguloPai.xmax(),retanguloPai.ymax());
		}
		else{
			if(pai.y() > p.y())ret = new RectHV(retanguloPai.xmin(),retanguloPai.ymin(), retanguloPai.xmax(),pai.y());	
			else ret = new RectHV(retanguloPai.xmin(),pai.y(), retanguloPai.xmax(),retanguloPai.ymax());		
		}
		
		return ret;
	}
	
	//Obtem o valor associado ao ponto p
	public Value get(Point2D p){
		if (p == null) throw new java.lang.NullPointerException();
		//Chamamos nossa versão recursiva
		return get(raiz, p, horizontal);
	}
	
    //get recursivo
    private Value get(Node no, Point2D p, boolean orientacao) {
		
		//base onde não p não pertence a árvore
  		if(no == null) return null;
		
		//Decidindo para que lado vamos olhar, com base na orientação do ponto
		//percebi depois que poderia usar também os retangulos dos pontos para essa decisão, mas não vi muita diferença
		double cmp;
		if(orientacao == horizontal) cmp = p.x() - no.p.x();
		else cmp = p.y() - no.p.y();
		
		//Encontra o nó ou chama recurivo
		if(p.equals(no.p)) return no.val;
		else if(cmp >= 0) return get(no.rt, p, !orientacao);
		else return get(no.lb, p, !orientacao);
	}

    //A árvore contém p? 
    public boolean contains(Point2D p){
		if (p == null) throw new java.lang.NullPointerException();
		if(get(p) != null) return true;
		return false;	
	}

    //Iteravel com todos os pontos por ordem de nível
    public Iterable<Point2D> points(){
		
		Queue<Node> fila = new Queue<Node>();
		Queue<Point2D> retorno = new Queue<Point2D>();
		fila.enqueue(raiz);
		Node atual;
		for(int m = 0; m < n; m++){
			atual = fila.dequeue();
			retorno.enqueue(atual.p);
			if(atual.lb != null) fila.enqueue(atual.lb);
			if(atual.rt != null) fila.enqueue(atual.rt);
		}
			
		return retorno;
		
		//Na fila implementada caseiramente:
		//return new FilaIteravel(); //no fim do código
	}

	
	
    //Pontos dentro do retângulo 
    public Iterable<Point2D> range(RectHV rect){
		
		//Apenas chamamos o recursivo, que guardará os pontos nessa fila externa
		
		Queue<Point2D> fila = new Queue<Point2D>();
		
		range(raiz, rect, fila);
		
		return fila;
			
	}

	//Range recursivo
	private void range(Node r, RectHV rect, Queue<Point2D> fila){
		
		if(r != null){
			//Confere o atual
			if(rect.contains(r.p)) fila.enqueue(r.p);
			//Chama recursivo, se há interseção
			if(r.lb != null && rect.intersects(r.lb.rect)) range(r.lb, rect, fila);			
			if(r.rt != null && rect.intersects(r.rt.rect)) range(r.rt, rect, fila);
		}
	}
	
	
    //Encontra o ponto mais perto 
    public Point2D nearest(Point2D p){
		
		if (p == null) throw new java.lang.NullPointerException();
		if(raiz == null) return null;
		
		//Com nosso método adicional, podemos apenas chamar essa função, dispensando a função comentada abaixo
        return nearest(p, 1).iterator().next();
		
		//return nearest(raiz, p, raiz.p);
	}
	
	/*
	Versão antes da implementação do iterable
	
	private Point2D nearest(Node r, Point2D p, Point2D near){
		
		if (p == null) throw new java.lang.NullPointerException();
		
		
		if(r.p.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = r.p;
		
		//Se o lado esquerdo contem o ponto, faço ele primeiro
		if(r.lb != null && r.lb.rect.contains(p)){
			if(r.lb != null && r.lb.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.lb, p, near);	
			if(r.rt != null && r.rt.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.rt, p, near);
		}
		//Se o lado direito contem, faço ele primeiro
		else{
			if(r.rt != null && r.rt.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.rt, p, near);
			if(r.lb != null && r.lb.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.lb, p, near);	
		}
		
		return near;
			
	}
	*/
	
	
	//Retorna os k pontos mais perto de p	
	public Iterable<Point2D> nearest(Point2D p, int k){
			
		if(k >= n) return this.points();
		
		//Guardaremos os pontos nessa pilha enquanto entramos nas recursões
		Stack<Point2D> pilha = new Stack<Point2D>();
		
		//Chama a primeira
		nearest(raiz, p, raiz.p, pilha);
		
		//Adequa a pilha ao tamanho k
		Stack<Point2D> pilhak = new Stack<Point2D>();
		Iterator<Point2D> it = pilha.iterator();
		
		//Apenas uma conferência para não bugar
		if(k > pilha.size()) k = pilha.size();
		
		//Agora sim, coloca os k primeiros na pilha certa
		for(; k > 0; k--){
			pilhak.push(it.next());
		}
		
		return pilha;		
		
	}
	
	//Função que faz o serviço	
	private Point2D nearest(Node r, Point2D p, Point2D near, Stack<Point2D> pilha){
		
		
		//Confere se o atual não é o mais perto
		if(r.p.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = r.p;
		
		//Se o lado esquerdo contem o ponto, faço ele primeiro
		if(r.lb != null && r.lb.rect.contains(p)){
			if(r.lb != null && r.lb.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.lb, p, near, pilha);	
			if(r.rt != null && r.rt.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.rt, p, near, pilha);
		}
		//Se o lado direito contem, faço ele primeiro
		else{
			if(r.rt != null && r.rt.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.rt, p, near, pilha);
			if(r.lb != null && r.lb.rect.distanceSquaredTo(p) < near.distanceSquaredTo(p)) near = nearest(r.lb, p, near, pilha);	
		}
		
		//Empilha e retorna
		pilha.push(near);
		return near;
			
	}


    // unit testing (required)
    public static void main(String[] args){
	
		KdTreeST<Integer> plano = new KdTreeST<Integer>();
		
		StdOut.println("Contruindo os pontos do enunciado");
		
		plano.put(new Point2D(0.7, 0.2), 5);
		plano.put(new Point2D(0.5, 0.4), 6);
		plano.put(new Point2D(0.2, 0.3), 3);
		plano.put(new Point2D(0.4, 0.7), 2);
		plano.put(new Point2D(0.9, 0.6), 2);
		
		//plano.put(new Point2D(0.6, 1), 5);
		//plano.put(new Point2D(0.6, 0.5), 5);
		
		StdOut.println("Todos os pontos colocados por ordem de nível");
		
		Iterable<Point2D> it = plano.points();
		for( Point2D p : it) StdOut.println(p.toString());
		
		StdOut.println("Ponto mais perto de (0,0)");
		StdOut.println(plano.nearest(new Point2D(0,0)).toString());
		
		
		StdOut.println("Ponto mais perto de (1,1)");
		StdOut.println(plano.nearest(new Point2D(1,1)).toString());
		
		StdOut.println("Todos os pontos dentro do retangulo [0.45, +inf] x [0.3, 1]");
		
		Iterable<Point2D> it2 = plano.range(new RectHV(0.45, 0.3, Double.POSITIVE_INFINITY, 1));
		for( Point2D p : it2) StdOut.println(p.toString());
		
	}
}

/* --------------------- FILA ITERÁVEL -----------------------------*/
/*
	//Fila para iterar os nós em ordem de nível
	private class FilaIteravel implements Iterable<Point2D>{

		public Iterator<Point2D> iterator(){
			//Função iterador que faz o trabalho
			return new Iterador(raiz);
		}
		
		private class Iterador implements Iterator<Point2D>{
	
			//Nó da fila
			private class NodeF{
				Node item;
				NodeF next;
				public NodeF(Node p){
					this.item = p;
					this.next = null;
				}
			}
		
			private NodeF atual, ultimo;
			private int n;
		
			//Constrói a fila com a raiz;
			public Iterador(Node raiz){
				this.atual = this.ultimo = new NodeF(raiz);
			}
			
			public Point2D next(){
			
				//Coloca os dois filhos no fim da fila (se existem)
				if(atual.item.lb != null){
					ultimo.next = new NodeF(atual.item.lb);
					ultimo = ultimo.next;
				}
				if(atual.item.rt != null){
					ultimo.next = new NodeF(atual.item.rt);
					ultimo = ultimo.next;
				}
				//Retorna e atualiza o atual
				Point2D next = atual.item.p;
				atual = atual.next;
				return next;
			}			
			public boolean hasNext(){
        	   	return atual != null;
    		}
			public void remove() {
				//Não usaremos
            	//throw new UnsupportedOperationException();
        	}		
		}
	}	
*/