import heapq, collections, re, sys, time, os, random
import collections
import math

# Abstract interfaces for search problems and search algorithms.
# Builders and utilities for language models


class Node:
    """ Classe que abstrai as informacoes de um no' de busca

    A classe Node e' uma classe que abstrai o conceito de no' de busca
    estudado. Essa classe possui os seguintes atributos publicos:

    :var state: Armazena um estado do problema.
    :var cost: Armazena o custo acumulado do caminho do inicio ate o no' atual
    :var parent: Armazena um apontador para o no' pai caso exista, caso
        contrario armazena None por definicao.
    :var action: Armazena a acao realizada.
    """
    def __init__(self, state, cost, parent=None, action=None):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        if self.parent:
            self.height = self.parent.height + 1
        else:
            self.height = 0


    def __repr__(self):
        return "<Node {}>".format(self.state)



class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""
    def __init__(self, key, items=(),): 
        self.key = key
        self.items = []    # a heap of (score, counter, item) pairs
        self.count = 0
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queue."""
        m_tuple = (self.key(item),self.count, item)
        self.count += 1
        heapq.heappush(self.items, m_tuple)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[2]
    
    def top(self): return self.items[0][2]

    def __len__(self): return len(self.items)

def informed_search(problem, f):
    """Informed search using as a key of the Priority Queue f"""

    initialNode = Node(problem.initialState(), 0)
    frontier= PriorityQueue(f, [initialNode])
    reached = dict()
    reached[initialNode.state] = initialNode.cost
    while frontier:
        node = frontier.pop()
#        print(node.state)
#        print("{:.2f}".format(node.cost))
        if problem.isGoalState(node.state):
            return node
        for action in problem.actions(node.state):
            state = problem.nextState(node.state, action)
            cost = problem.stepCost(node.state, action) + node.cost
            if state not in reached or  cost < reached[state] :
                reached[state] = cost
                frontier.add(Node(state, cost, node, action))
    return None

def uniformCostSearch(problem):
    """ Implementa busca de custo uniforme no problema problem

        A funcao :func:'uniformCostSearch' recebe um problema problem e
        retorna None se o problema não contiver solucao, caso contrario
        retorna um no busca contendo um estado meta do problema.

        :param problem: Objeto da classe Problem descrita no enunciado
        :type problem: <class 'Problem'>
        :return solution: Um no de busca atualizado com a solucao ou None c.c.
        :rtype: <class 'Node'> or <class 'NoneType'>

        :Example:

        
        >>> goal = uniformCostSearch(problem)
        >>> goal.state
        (1,2,3,4,5,6,7,8,0)
        >>> goal.parent
        <__main__.node object at 0x7f29fbc301d0>
    """
    return informed_search(problem,lambda node: node.cost)



def aStar( problem, f):
    """ Implementa busca A* no problema problem

        A funcao :func:'aStar' recebe um problema problem e
        retorna None se o problema não contiver solucao, caso contrario
        retorna um no busca contendo um estado meta do problema.

        :param problem: Objeto da classe Problem descrita no enunciado
        :type problem: <class 'Problem'>
        :param f: função heuristica
        :return solution: Um no de busca atualizado com a solucao ou None c.c.
        :rtype: <class 'Node'> or <class 'NoneType'>

        :Example:

        
        >>> goal = aStar(problem, f)
        >>> goal.state
        (1,2,3,4,5,6,7,8,0)
        >>> goal.parent
        <__main__.node object at 0x7f29fbc301d0>
    """
    return informed_search(problem,f)

    
class Problem(object):
    """ Classe abstrata para representacao de um problema """
    def isState(self, state):
        """ Metodo abstrato que implementa verificacao de estado """
        raise NotImplementedError
    def initialState(self):
        """ Metodo abstrato que implementa retorno da posicao inicial """
        raise NotImplementedError
    def actions(self, state):
        """ Metodo abstrato que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        raise NotImplementedError
    def nextState(self, state, action):
        """ Metodo abstrato que implementa funcao de transicao """
        raise NotImplementedError
    def isGoalState(self, state):
        """ Metodo abstrato que implementa teste de meta """
        raise NotImplementedError
    def stepCost(self, state, action):
        """ Metodo abstrato que implementa funcao custo """
        raise NotImplementedError

def getSolution(node, problem):
    """ Checa  a validade de uma solucao para o problema e retorna a sequencia
        de acoes se houver solucao.
    """
    steps = []
    if not problem.isGoalState(node.state):
        return (False, steps)
    while node.parent is not None:
        new_n = node.parent
        if node.state != problem.nextState(new_n.state, node.action):
            return (False, steps)
        steps.append(node.action)
        node = new_n
    if node is not None and node.action is not None :
        steps.append(node.action)
    return (True,  ' '.join(list(reversed(steps))))

SENTENCE_BEGIN = '-BEGIN-'

def sliding(xs, windowSize):
    for i in range(1, len(xs) + 1):
        yield xs[max(0, i - windowSize):i]

def removeAll(s, chars):
    return ''.join(filter(lambda c: c not in chars, s))

def alphaOnly(s):
    s = s.replace('-', ' ')
    return filter(lambda c: c.isalpha() or c == ' ', s)

def cleanLine(l):
    return alphaOnly(l.strip().lower())

def words(l):
    l = "".join(l)
    return l.split()

# Make an n-gram model of words in text from a corpus.

def makeLanguageModels(path):
    unigramCounts = collections.Counter()
    totalCounts = 0
    bigramCounts = collections.Counter()
    bitotalCounts = collections.Counter()
    VOCAB_SIZE = 600000
    LONG_WORD_THRESHOLD = 5
    LENGTH_DISCOUNT = 0.15

    def bigramWindow(win):
        assert len(win) in [1, 2]
        if len(win) == 1:
            return (SENTENCE_BEGIN, win[0])
        else:
            return tuple(win)

    with open(path, 'r') as f:
        for l in f:
            ws = words(cleanLine(l))
            unigrams = [x[0] for x in sliding(ws, 1)]
            bigrams = [bigramWindow(x) for x in sliding(ws, 2)]
            totalCounts += len(unigrams)
            unigramCounts.update(unigrams)
            bigramCounts.update(bigrams)
            bitotalCounts.update([x[0] for x in bigrams])

    def unigramCost(x):
        if x not in unigramCounts:
            length = max(LONG_WORD_THRESHOLD, len(x))
            return -(length * math.log(LENGTH_DISCOUNT) + math.log(1.0) - math.log(VOCAB_SIZE))
        else:
            return math.log(totalCounts) - math.log(unigramCounts[x])

    def bigramModel(a, b):
        return math.log(bitotalCounts[a] + VOCAB_SIZE) - math.log(bigramCounts[(a, b)] + 1)

    return unigramCost, bigramModel

def logSumExp(x, y):
    lo = min(x, y)
    hi = max(x, y)
    return math.log(1.0 + math.exp(lo - hi)) + hi;

def smoothUnigramAndBigram(unigramCost, bigramModel, a):
    '''Coefficient `a` is Bernoulli weight favoring unigram'''
    # Want: -log( a * exp(-u) + (1-a) * exp(-b) )
    #     = -log( exp(log(a) - u) + exp(log(1-a) - b) )
    #     = -logSumExp( log(a) - u, log(1-a) - b )

    def smoothModel(w1, w2):
        u = unigramCost(w2)
        b = bigramModel(w1, w2)
        return -logSumExp(math.log(a) - u, math.log(1-a) - b)

    return smoothModel

# Make a map for inverse lookup of words without vowels -> possible
# full words

def makeInverseRemovalDictionary(path, removeChars):
    wordsRemovedToFull = collections.defaultdict(set)

    with open(path, 'r') as f:
        for l in f:
            for w in words(cleanLine(l)):
                wordsRemovedToFull[removeAll(w, removeChars)].add(w)

    wordsRemovedToFull = dict(wordsRemovedToFull)

    def possibleFills(short):
        return wordsRemovedToFull.get(short, set())

    return possibleFills

