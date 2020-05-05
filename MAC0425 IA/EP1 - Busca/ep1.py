"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Pedro Gigeck Freire
  NUSP : 10737136

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado
            Um estado desse problema será uma string da forma "XX_ abca bc bac"
            - XX é o índice da ultima letra da query que foi inserida no estado
            - abca bc bac são todas as letras até XX com alguns espaços intercalados
        """
        underIndex = 0   #indice do underscore
        while (underIndex < len(self.query) and state[underIndex] != '_'):
            underIndex += 1
        # Se encontrei o '_' então o estado é válido
        return underIndex < len(self.query)
         
    def lastInserted (self, state):
        """ Método que extrai o prefixo numérico do estado, que é a ultima letra da query inserida
            Retorna o número e o índice do '_', que é o tamanho do número 
        """
        underIndex = 0   #indice do underscore
        nextNumber = ""
        while (state[underIndex] != '_'):
            nextNumber += state[underIndex]
            underIndex += 1
        return int(nextNumber), underIndex
        
    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        # O estado inicial é aquele que nenhuma letra foi inserida ainda
        return "-1_"

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
            para um determinado estado
        """
        # Uma ação será adicionar uma palavra no estado
        # representaremos por um número, que é a quantidade de letras da palavra adicionada    
        nextLetter = (self.lastInserted(state)[0] + 1)
        # retorna uma lista de 1 ao máximo de letras
        return range(1, len (self.query) - nextLetter + 1)
    
    def wordAction (self, state, action):
        """ Função que recebe um estado e uma ação, e devolve a palavra que essa ação adiciona """
        ini = ini = self.lastInserted(state)[0] + 1
        end = ini + action
        return self.query[ini:end]

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        # Atualizamos o prefixo numérico e concatenamos a ação
        nextNumber, underIndex = self.lastInserted (state)
        newState = str(nextNumber + action) + state[underIndex:] + ' ' + self.wordAction (state, action)
        return newState

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        # Um estado é meta se já foram inseridas todas as letras
        lastInserted = self.lastInserted (state)[0]
        if (lastInserted == (len (self.query) - 1)):
            return True
        return False

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        # O custo de uma ação será o custo da palavra adicionada
        word = self.wordAction (state, action)
        cost = self.unigramCost (word)
        return cost
        
def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
    
    # BEGIN_YOUR_CODE 

    segProb = SegmentationProblem (query, unigramCost)
    solution = util.uniformCostSearch (segProb)
    solution = solution.state
    
    # tira o prefixo do estado
    prefix = 0
    while (solution[prefix] != "_"):
        prefix += 1
    solution = solution[prefix + 2:]
    
    return solution
    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
        
        # Faz uma matriz com os possible fills para facilitar o acesso
        self.pf = []
        for word in self.queryWords:
            possible = (list (possibleFills (word)))
            if possible == []:
                possible = [word]
            self.pf.append(possible)

    def isState(self, state):
        """ Metodo que implementa verificacao de estado
            Um estado desse problema será uma string da forma "XX_ abca bc bac"
            - XX é o índice da ultima palavra que foi inserida
            - abca bc bac são todas as palavras até XX de acordo com a possibilidade escolhida
        """
        underIndex = 0   #indice do underscore
        while (underIndex < len(self.queryWords) and state[underIndex] != '_'):
            underIndex += 1
        # Se encontrei o '_' então o estado é válido
        return underIndex < len(self.queryWords)

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        # O estado inicial é aquele que nenhuma palavra foi inserida
        return "-1_"
    
    def lastInserted (self, state):
        """ Método que extrai o prefixo numérico do estado, que é a ultima palavra da query inserida
            Retorna o número e o índice do primeiro '_', que é o tamanho do número 
        """
        underIndex = 0   #indice do underscore
        nextNumber = ""
        while (state[underIndex] != '_'):
            nextNumber += state[underIndex]
            underIndex += 1
        return int(nextNumber), underIndex

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
            para um determinado estado
        """
        # Uma ação será adicionar uma palavra no estado    
        nextWord = (self.lastInserted(state)[0] + 1)
        # retorna uma lista das possibilidades do possibleFills
        return range(len (self.pf[nextWord]))

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        # Atualiza o prefixo e concatena a palavra
        lastInserted, underIndex = self.lastInserted(state)
        lastInserted += 1
        return (str (lastInserted) + state[underIndex:] + ' ' + self.pf[lastInserted][action])

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        lastInserted = self.lastInserted(state)[0]
        return (lastInserted == len(self.pf) - 1)

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        lastInserted = self.lastInserted(state)[0]
        # Para a primeira palavra, retornarei 0, assim ele avaliara 
        # os primeiros bigramas sem enviesamento
        if (lastInserted == -1):
            return 0
        # Retorna o custo do bigrama da ultima dupla formada
        return self.bigramCost (state.split()[lastInserted + 1], self.pf[lastInserted + 1][action])

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    
    # não precisei usar o getSolution pela maneira que os estados foram modelados
    
    insVow = VowelInsertionProblem (queryWords, bigramCost, possibleFills)
    solution = util.uniformCostSearch (insVow)
    solution = solution.state
    
    # tira o prefixo do estado
    prefix = 0
    while (solution[prefix] != "_"):
        prefix += 1
    solution = solution[prefix + 2:]
    
    return solution
    
    # END_YOUR_CODE

############################################################

def getRealCosts(corpus='corpus.txt'):
    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    
    # Os testes aqui não necessariamente dão a resposta certa,
    # Mas acredito que dão as melhores respostas com base no corpus que temos
    
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)
    print("--")
    
    resulSegment = segmentWords('shouldistayorshouldigoifyousaythatyouaremine', unigramCost)
    print(resulSegment)
    resulSegment = segmentWords('iwillbehereuntiltheendoftimes', unigramCost)
    print(resulSegment)
    print("--")

    resulSegment = segmentWords('thisisthelawofthejungle', unigramCost)
    print(resulSegment)
    resulSegment = segmentWords('asoldandastrueasthesky', unigramCost)
    print(resulSegment)
    resulSegment = segmentWords('thewolfthatshallkeepitmay', unigramCost)
    print(resulSegment)
    resulSegment = segmentWords('butthewolfthatshallbreakitmustdie', unigramCost)
    print(resulSegment)
    print("--")
    
    resultInsert = insertVowels('w r th chmpns my frnd'.split(), bigramCost, possibleFills)
    print(resultInsert)
    resultInsert = insertVowels('nd w wll kp n fghtng ntl th nd'.split(), bigramCost, possibleFills)
    print(resultInsert)
    print("--")
    
    resultInsert = insertVowels('mgn thr s n hvn'.split(), bigramCost, possibleFills)
    print(resultInsert)
    resultInsert = insertVowels('mgn ll th ppl lvng lf n pc'.split(), bigramCost, possibleFills)
    print(resultInsert)
    print("--")

if __name__ == '__main__':
    main()