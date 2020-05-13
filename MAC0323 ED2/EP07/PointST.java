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


import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.RectHV;
import edu.princeton.cs.algs4.RedBlackBST;
import edu.princeton.cs.algs4.StdOut;

public class PointST<Value> {
	
	//Nosso plano (conjunto de pontos) será representado por essa árvore
	//Inclusive, os métodos requisitados são muito parecidos com os métodos já implementados na classe RedBlackBST
	private RedBlackBST<Point2D, Value> raiz;
	
    //Construtor
    public PointST(){
		//Constroi a árvore vazia
		raiz = new RedBlackBST<Point2D, Value>();		
	}

	/*  -------------------------------------------------------------------------------------
				Métodos praticamente herdados da implementação da RedBlackBST  
		-------------------------------------------------------------------------------------   */
	
    public boolean isEmpty(){					return raiz.isEmpty();		}

    public int size(){							return raiz.size();			}	

    public void put(Point2D p, Value val){		raiz.put(p, val);  			}

    public Value get(Point2D p){				return raiz.get(p);			}

    public boolean contains(Point2D p){ 		return raiz.contains(p);	}

    public Iterable<Point2D> points(){			return raiz.keys();			}
	
	/*  ------------------------------------------------------------------------------------- */

    //Retorna um iterável com todos os pontos dentro do retângulo rect
    public Iterable<Point2D> range(RectHV rect){
		
		//Vamos iterar por todos os pontos da árvore e verificar quais estão dentro dos limites
		Iterable<Point2D> it = this.points();
		
		//Aproiveitando que já estamos usando a classe das RedBlackBST, vamos contruir o iterável com ela 
		//para não precisar construir uma nova estrutura de lista, por exemplo
		RedBlackBST<Point2D, Integer> ret = new RedBlackBST<Point2D, Integer>();
		
		for(Point2D p : it)
			//Se o ponto está dentro do retângulo, adicionamos
			if(rect.contains(p)) ret.put(p, 0);
		
		return ret.keys();
	}
		

    //O elemento (ou um dos) mais próximo de p 
    public Point2D nearest(Point2D p){
		
		if(this.isEmpty()) return null;
		
		//Vamos basicamente percorrer todos os pontos, procurando o com menor distância
		Point2D nearest = raiz.min();
		Iterable<Point2D> it = this.points();
		for(Point2D candidato : it) if(candidato.distanceTo(p) < nearest.distanceTo(p)) nearest = candidato;
		return nearest;
	}

    // unit testing (required)
    public static void main(String[] args){
	
		PointST<Integer> plano = new PointST<Integer>();
		
		plano.put(new Point2D(0,0), 5);
		plano.put(new Point2D(1,0), 6);
		plano.put(new Point2D(1,1), 3);
		plano.put(new Point2D(0,2), 2);
		plano.put(new Point2D(0,5), 2);
		plano.put(new Point2D(2,1), 3);
		
		StdOut.println("Todos os pontos colocados");
		
		Iterable<Point2D> it = plano.points();
		for( Point2D p : it) StdOut.println(p.toString() + "\n");
		
		
		StdOut.println("Pontos dentro do retangulo");
		Iterable<Point2D> it2 = plano.range(new RectHV(0.5, -1, 3, 3));
		
		for( Point2D p : it2) StdOut.println(p.toString() + "\n");
		
		StdOut.println("Ponto mais perto de (3, 3)");
		StdOut.println(plano.nearest(new Point2D(3,3)).toString());
		
		
		
	}

}
