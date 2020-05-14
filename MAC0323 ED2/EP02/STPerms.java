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

		Usei o algoritmo indicado pelo professor no PACA para gerar as permutações (mais explicações no final do arquivo)


    Se for o caso, descreva a seguir 'bugs' e limitações do seu programa:

		
****************************************************************/

/******************************************************************************
 *  Compilation:  javac-algs4 STPerms.java
 *  Execution:    java STPerms n s t opcao
 *  
 *  Enumera todas as (s,t)-permutações das n primeiras letras do alfabeto.
 *  As permutações devem ser exibidas em ordem lexicográfica.
 *  Sobre o papel da opcao, leia o enunciado do EP.
 *
 *  % java STPerms 4 2 2 0
 *  badc
 *  bdac
 *  cadb
 *  cdab
 *  % java STPerms 4 2 2 1
 *  4
 *  % java STPerms 4 2 2 2
 *  badc
 *  bdac
 *  cadb
 *  cdab
 *  4
 *   
 ******************************************************************************/

import edu.princeton.cs.algs4.StdOut;

public class STPerms {
	
	//Defini como atributos para não ficar passando os parâmetros tantas vezes (já que fiz recursivo)
	private static int count;
	private static int n;
	private static int s;
	private static int t;
	private static int opcao;
		
	//Função recursiva para gerar as permutações (muito pareida com a 'inspiração' fornecida)
	private static void permuta(String prefixo, String pos) {
        
		int n = pos.length();
        
		//base da recursão, quando chegamos a uma nova permutação
		if (n == 0){
			if(opcao != 1) StdOut.println(prefixo);
			count++;
		}
		
		else {
		
            for (int i = 0; i < n; i++)
				
				/*	Ideia desse if:
					se (todas as substrings de tamanho s+1 não forem crescentes && todas as substrings de tamanho t + 1 não forem decrescentes)
					
					Pensando de outro jeito:
					se (todas as substrings crescentes forem menores que s+1 && todas as substrings decrescentes fores menores que t + 1)
					
					Ou seja,
					Só vai chamar a recursão se o prefixo for (s, t), pois se o prefixo já quebrar, não precisamos permutar o resto
					Assim evito de comparar todas as permutações sem necessidade  */
				
				
				if(combinacao(prefixo +  pos.charAt(i), s + 1, true) && combinacao(prefixo + pos.charAt(i), t + 1, false))
					permuta(prefixo + pos.charAt(i), pos.substring(0, i) + pos.substring(i+1, n));
        }

    }
	
	//Função que confere se a substring será (s, t)
	public static boolean combinacao(String prefixo, int k, boolean crescente) {
		
		/*-------------------------------------------------------------
		
		IDEIA:         Se alguma substring de tamanho s + 1 for crescente, não é s
		
		Os parâmetros: prefixo = string a ser conferida
					   k = tamanho da substring (s + 1) ou (t + 1)
				       crescente = flag para mostrar se esamos procurando uma substring crescente ou decrescente
			
		FUNCIONAMENTO: Gera todas as combinações (aproveitando o código do ep1) da string, ou seja, todas as substrings de tamanho k
					   Conforme vai gerando as substrings, confere se ela satisfaz (s ou t)
					   Se alguma não satisfazer, retorna false
					   Se todas satgisfizerem retorna true
		
		------------------------------------------------------------------*/
		
		int n = prefixo.length() - 1;
		//Se nosso k for maior que a propria string, então todas as substrings vao ser menores que k
		if(k - 1 > n) return true;
		
		//Vamos gerar as combinações num vetor de ints, igual fiz no ep1
		//A substring representada pelo vetor será guardada na variavel parcial
		int[] vetor = new int[k];
		String parcial = new String();
		
		//inicializando o vetor com a primeira combinação, a sequencia 1, ..., k
		//inicializando a substring com a primeira combinação correspondente
		for(int i = 0; i < k; i++) vetor[i] = i;
		for(int i = 0; i < k; i++)	parcial += prefixo.charAt(vetor[i]);
		
		//Se essa primeira substring já quebra, retorna false
		if((crescente && crescente(parcial)) || (!crescente && decrescente(parcial))) return false;
		
		
		//Enquanto a primeira casa nao for a mais alta possivel (última combinação)
		while(vetor[0] != n-k+1){	
			
			//percorre o vetor de tras pra frente
			for(int i = k - 1; i >= 0; i--){
				
				//se for possivel incrementar essa casa sem estourar o valor de n na ultima casa
				if(vetor[i] < n - (k - 1 - i)){
					
					vetor[i]++;
					
					//vai percorrendo o vetor de volta só colocando a sequencia até o final
					for(int j = i + 1; j < k; j++) vetor[j] = vetor[j - 1] + 1;
					break;
				}
			}
			
			//Terminado de gerar a combinaçõa, vamos conferir a substring
			parcial = "";
			for(int i = 0; i < k; i++)	parcial += prefixo.charAt(vetor[i]);
			if((crescente && crescente(parcial)) || (!crescente && decrescente(parcial))) return false;
		}
		
		//Se conferimos todas sem achar nenhuma que quebra, maravilha!
		return true;
    }

	//Função que confere se uma string é crescente
	private static boolean crescente(String s){
		int n = s.length();
		for(int i = 0; i < n - 1; i++)
			if(s.charAt(i) > s.charAt(i + 1)) return false;
		
		return true;
	}
	
	//Função que confere se uma string é decrescente
	private static boolean decrescente(String s){
		int n = s.length();
		for(int i = 0; i < n - 1; i++)
			if(s.charAt(i) < s.charAt(i + 1)) return false;
		
		return true;
	}
	
    public static void main(String[] args) {
		
        n = Integer.parseInt(args[0]);
        s = Integer.parseInt(args[1]);
		t = Integer.parseInt(args[2]);
		opcao = Integer.parseInt(args[3]);
       
		char[] alfabeto = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
	
		count = 0;
		
		String perm = new String();
		for (int i = 0; i < n; i++)
            perm += alfabeto[i];
		
		permuta("", perm);
		if(opcao != 0) StdOut.println(count);
    }
}

/*----------------------------------------------------------------------------------------------------------------------------
	
	Função que eu fiz por conta própria para gerar as permutações, depois de muitas tentativas,
	Mas por causa da função inverte ficou com uma complexidade muito grande,
	Então usei algo parecido com o do professor mesmo :/
	
	A ideia era fazer recursivo, de modo que ia printando em ordem..
	Porem, na hora de voltar para a primeira recursão, a permutação estava invertida,
	Então eu precisaria ou usar mais espaço, salvando a permutação inicial para não ficar modificando ela ao longo das recursões
	Ou inverte-la no final da recursão (Aumentando a complexidade)
	
	Como o professor recomendou que usassemos espaço O(n)
	Prefiri fazer essa inversão, mas aí o algoritmo ficava quadrático pra cada permutação, então abandonei
	
	public static void permuta(char[] perm, int n, int comeco, int s, int t){
		
		if(comeco == n - 1){
			printaPermutacao(perm, n);
			return;
		}
		
		for(int i = comeco; i < n; i++){
			
			troca(perm, comeco, i);
			permuta(perm, n, comeco + 1, s, t);
			if(i < n - 1) inverte(perm, comeco + 1, n);
			
		}		
	}
	
	private static void inverte(char[] perm, int comeco, int n){
	
		for(int i = 0; i < (n-comeco)/2; i++) troca(perm, comeco + i, n - 1 - i);
	}
	
	private static void printaPermutacao(char[] perm, int n){
		for (int i = 0; i < n; i++)
			StdOut.print(perm[i]);
		StdOut.println();	
	}
	
	private static void troca(char[] perm, int i, int j){
		char c = perm[i]; 
		perm[i] = perm[j]; 
		perm[j] = c;
	}
	--------------------------------------------------------------------------------------------------------------------------------*/
