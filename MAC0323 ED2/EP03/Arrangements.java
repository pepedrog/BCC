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
		
		Modelo de iterador similar ao mostrado em aula (https://www.ime.usp.br/~coelho/mac0323-2019/aulas/aula01/03-BagIterable/)


    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:

****************************************************************/

// excessões pedidas
import java.lang.IllegalArgumentException;
import java.lang.UnsupportedOperationException;
import java.util.NoSuchElementException;

// pode ser útil
import java.util.Arrays; // Arrays.sort(), Arrays.copyOf(), ...

import java.util.Iterator; // passo 0 para criarmos um iterador

import edu.princeton.cs.algs4.StdOut;

public class Arrangements implements Iterable<String> {
	
	//Implementação será feit usando char[] ao invés de String
	private char[] first;
	private int n;
		
	public Arrangements(String s){
		
		//se a string for nula
		if(s == null) throw new IllegalArgumentException();
		
		//Coloca como primeiro arranjo a ordenação normal da string
		first = s.toCharArray();
		Arrays.sort(first);
		
		n = s.length();
	}
	
	public Iterator<String> iterator() {
        return new ArrIterator();
    }
    
    // Classe que implementa o Iterator    
    private class ArrIterator implements Iterator<String> {
		
		//Iniciando a variavel que percorrerá os arranjos
		private char[] atual = Arrays.copyOf(first, n);
		boolean acabou = false;
		
		//vetor que indicará qual parte tem que ser permutavel (separando o prefixo)
        private char[] incrementavel = new char[n];
		
        public boolean hasNext(){
            return !acabou;
        }
		
		public String next() {
		
			/* OBS: Fiz o EP2 recursivo, por gastar um pouco menos espaço, então o método de permutar está diferente entra o EP2 e o EP */
			
			//Guardando o atual pra imprimir depois
			String retorno = String.valueOf(atual);
			
			//Buscando a pŕoxima permutação
			//Vamos achar qual é o primeiro dígito que pode ser incrementado (de tras pra frente) 
			for(int i = n -1; i >= 0; i--){
			
				//Vai guardando qual é a parte que tera que ser incrementada (permutada)
				incrementavel[n - 1 - i] = atual[i];
				
				if(consigoIncrementar(atual, i)){
					
					incrementa(atual, i);
					return retorno;
				}
			
			}
			
			//Se acabou o for, quer dizer que chegamos na última permutação, nenhum digito pode ser incrementado
			
			if(!acabou){
				
				acabou = true;
				return retorno;
			}
			
			//Se ja tinha acabado, erro!
			throw new NoSuchElementException();
        
		}
		
		private boolean consigoIncrementar(char[] atual, int i){
			
			//percorre o vetor dos incrementaveis, e confere se há algum dígito maior que o que eu quero incrementar
			for(int j = 0; j < n - 1 - i; j++)
				if(incrementavel[j]	> atual[i]) return true;
			
			return false;
		}
		
		private void incrementa(char[] atual, int i) {
			
			//Ordena os que tem que incrementar
			char[] comecoIncrementavel = Arrays.copyOfRange(incrementavel, 0, n - i);
			Arrays.sort(comecoIncrementavel);
			
			/*  Decidi fazer essa ordenação por causa da complexidade:
				Se não a fizesse, teria que percorrer o vetor dos incrementaveis achando cada termo que iria em cada posição = O(n^2)
				Com ele ordenado, posso apenas ir colocando os digitos em sequencia, ou seja, ordenação O(n logn) + colocar os digitos O(n) = O(nlogn)
			*/
			
			//incrementa a posicao i, colocando o menor elemento maior que atual[i]
			int j;
			for(j = 0; j < n - i; j++){
				if(comecoIncrementavel[j] > atual[i]){
					atual[i] = comecoIncrementavel[j];
					break;
				}
			}
			//Tirando esse elemento que já foi usado do vetor (jogando todo o resto pra frente)
			for(int l = j; l < n - i - 1; l++)
				comecoIncrementavel[l] = comecoIncrementavel[l + 1];

			//Colocando os outros digitos, que já estao em ordem crescente
			for(int k = i + 1; k < n; k++)
				atual[k] = comecoIncrementavel[k - i - 1];
			
		}
		
        public void remove() {
            throw new UnsupportedOperationException();
        }
    }
	
	
    // Unit test
    public static void main(String[] args) {
        String s = args[0];
        Arrangements arr = new Arrangements(s);
        
        StdOut.println("Teste 1: imprime no máximo os 10 primeiros arranjos");
        Iterator<String> it = arr.iterator();
        for (int i = 0; it.hasNext() && i < 10; i++) {
            StdOut.println(i + " : " + it.next());
        }
        
        StdOut.println("Teste 2: imprime todos os arranjos");
        int i = 0;
        for (String arranjo: arr) {
            StdOut.println(i + " : " + arranjo);
            i++;
        }
    }
}
