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

import math
import random
from collections import defaultdict
import util

# **********************************************************
# **            PART 01 Modeling BlackJack                **
# **********************************************************


class BlackjackMDP(util.MDP):
    """
    The BlackjackMDP class is a subclass of MDP that models the BlackJack game as a MDP
    """
    def __init__(self, valores_cartas, multiplicidade, limiar, custo_espiada):
        """
        valores_cartas: list of integers (face values for each card included in the deck)
        multiplicidade: single integer representing the number of cards with each face value
        limiar: maximum number of points (i.e. sum of card values in hand) before going bust
        custo_espiada: how much it costs to peek at the next card
        """
        self.valores_cartas = valores_cartas
        self.multiplicidade = multiplicidade
        self.limiar = limiar
        self.custo_espiada = custo_espiada

    def startState(self):
        """
         Return the start state.
         Each state is a tuple with 3 elements:
           -- The first element of the tuple is the sum of the cards in the player's hand.
           -- If the player's last action was to peek, the second element is the index
              (not the face value) of the next card that will be drawn; otherwise, the
              second element is None.
           -- The third element is a tuple giving counts for each of the cards remaining
              in the deck, or None if the deck is empty or the game is over (e.g. when
              the user quits or goes bust).
        """
        return (0, None, (self.multiplicidade,) * len(self.valores_cartas))

    def actions(self, state):
        """
        Return set of actions possible from |state|.
        You do not must to modify this function.
        """
        return ['Pegar', 'Espiar', 'Sair']

    def succAndProbReward(self, state, action):
        """
        Given a |state| and |action|, return a list of (newState, prob, reward) tuples
        corresponding to the states reachable from |state| when taking |action|.
        A few reminders:
         * Indicate a terminal state (after quitting, busting, or running out of cards)
           by setting the deck to None.
         * If |state| is an end state, you should return an empty list [].
         * When the probability is 0 for a transition to a particular new state,
           don't include that state in the list returned by succAndProbReward.
        """
        # BEGIN_YOUR_CODE
        new_states = []
        total = state[0]
        peek = state[1]
        deck = state[2]
        # end state
        if deck is None: return []
        # total of cards in the deck (to calculate probability)
        total_cards = 0
        for cards in deck: total_cards += cards
        # Process each possible action
        if action == 'Pegar':
            reward = 0
            if peek != None:
                # If I peeked, the action is deterministic 
                prob_card = 1
                total += self.valores_cartas[peek]
                if total > self.limiar: 
                    # BUST!
                    deck = None
                elif total_cards > 1:
                    deck = list(deck)
                    deck[peek] -= 1
                    deck = tuple(deck)
                else:
                    # Last card
                    reward = total
                    deck = None
                new_states = [((total, None, deck), prob_card, reward)]
            else:
                # Add a new state for each possible card
                for card in range(len(deck)):
                    new_total = total + self.valores_cartas[card]
                    prob_card = deck[card] / total_cards
                    if new_total > self.limiar: 
                        # BUST! or game over
                        new_deck = None
                    elif total_cards > 1:
                        new_deck = list(deck)
                        new_deck[card] -= 1
                        new_deck = tuple(new_deck)
                    else:
                        # Last card
                        reward = new_total
                        new_deck = None
                    if prob_card > 0:
                        new_states.append(((new_total, None, new_deck), prob_card, reward))
        
        elif action == 'Espiar':
            if peek is not None:
                # Forbidden double peeking
                return []
            reward = - self.custo_espiada
            # Add a new state for each possible card
            for card in range(len(deck)):
                prob_card = deck[card] / total_cards
                if prob_card > 0:
                    new_states.append(((total, card, deck), prob_card, reward))
        else:
            new_states = [((total, None, None), 1, total)]
            
        return new_states
        # END_YOUR_CODE

    def discount(self):
        """
        Return the descount  that is 1
        """
        return 1

# **********************************************************
# **                    PART 02 Value Iteration           **
# **********************************************************

class ValueIteration(util.MDPAlgorithm):
    """ Asynchronous Value iteration algorithm """
    def __init__(self):
        self.pi = {}
        self.V = {}

    def solve(self, mdp, epsilon=0.001):
        """
        Solve the MDP using value iteration.  Your solve() method must set
        - self.V to the dictionary mapping states to optimal values
        - self.pi to the dictionary mapping states to an optimal action
        Note: epsilon is the error tolerance: you should stop value iteration when
        all of the values change by less than epsilon.
        The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
        """
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) \
                            for action in mdp.actions(state))[1]
            return pi
        
        V = defaultdict(float)  # state -> value of state
        
        # Implement the main loop of Asynchronous Value Iteration Here:
        # BEGIN_YOUR_CODE
        for state in mdp.states:
            V[state] = 0
            
        gamma = mdp.discount()
        delta = float('inf')
        
        while delta > epsilon*((1-gamma)/gamma):
            partial_delta = 0
            for state in mdp.states:
                old_v = V[state]
                V[state] = max(computeQ(mdp, V, state, action) for action in mdp.actions(state))
                partial_delta = max(partial_delta, abs(old_v - V[state]))
            delta = min(partial_delta, delta)
        # END_YOUR_CODE

        # Extract the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        # print("ValueIteration: %d iterations" % numIters)
        self.pi = pi
        self.V = V

DEBUG = False

# First MDP
MDP1 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)
# Second MDP
MDP2 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=15, custo_espiada=1)

if DEBUG:
    solver = ValueIteration()
    solver.solve(MDP2)
    for state in MDP1.states:
        if state[2] is not None:
            print("Tenho " + str(state[0]) + ", Espiei " + str(state[1]) + 
                  ", Devo " + str(solver.pi[state]))
    print("---------------------")

def geraMDPxereta():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action for at least 10% of the states.
    """
    # BEGIN_YOUR_CODE
    return BlackjackMDP(valores_cartas=[5, 20], multiplicidade=4, limiar=20, custo_espiada=1)
    # END_YOUR_CODE
"""
    vi = ValueIteration()
    vi.solve(teste)
    espiadas = 0
    for state in teste.states:
        if state[2] is not None:
            print("Tenho " + str(state[0]) + ", Espiei " + str(state[1]) + 
                  ", Devo " + str(vi.pi[state]))
        if vi.pi[state] == 'Espiar':
            espiadas += 1
    print("total = " + str(espiadas/len(teste.states)))
    print("---------------------")"""

# **********************************************************
# **                    PART 03 Q-Learning                **
# **********************************************************

class QLearningAlgorithm(util.RLAlgorithm):
    """
    Performs Q-learning.  Read util.RLAlgorithm for more information.
    actions: a function that takes a state and returns a list of actions.
    discount: a number between 0 and 1, which determines the discount factor
    featureExtractor: a function that takes a state and action and returns a
    list of (feature name, feature value) pairs.
    explorationProb: the epsilon value indicating how frequently the policy
    returns a random action
    """
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def getQ(self, state, action):
        """
         Return the Q function associated with the weights and features
        """
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    def getAction(self, state):
        """
        Produce an action given a state, using the epsilon-greedy algorithm: with probability
        |explorationProb|, take a random action.
        """
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    def getStepSize(self):
        """
        Return the step size to update the weights.
        """
        return 1.0 / math.sqrt(self.numIters)

    def incorporateFeedback(self, state, action, reward, newState):
        """
         We will call this function with (s, a, r, s'), which you should use to update |weights|.
         You should update the weights using self.getStepSize(); use
         self.getQ() to compute the current estimate of the parameters.

         HINT: Remember to check if s is a terminal state and s' None.
        """
        # BEGIN_YOUR_CODE
        alpha = self.getStepSize()
        q = self.getQ(state, action)
        if newState is None:
            V = q
        else:
            V = max(self.getQ(newState, a) for a in self.actions(newState))
        # calculate each weight based on the actual weights
        weights_update = defaultdict(float)
        for f, v in self.featureExtractor(state, action):
            weights_update[f] = self.weights[f] + alpha*(reward + self.discount*V - q)*v
        # after calculating the new values, update syncronsynchronously
        for f, _ in self.featureExtractor(state, action):
            self.weights[f] = weights_update[f]
        #print("recebi " + str(state) + str(action) + str(reward) + str(newState))
        #print(self.weights)
        # END_YOUR_CODE

def identityFeatureExtractor(state, action):
    """
    Return a single-element list containing a binary (indicator) feature
    for the existence of the (state, action) pair.  Provides no generalization.
    """
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

# Large test case
largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3, limiar=40, custo_espiada=1)

# **********************************************************
# **        PART 03-01 Features for Q-Learning             **
# **********************************************************

def blackjackFeatureExtractor(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE
    # Feature 1, 2 = Cards Left, Cards in Hand (extimate)
    # Feature 1 = estimative of points in the deck
    cards_left = 0
    cards_hand = 0
    max_cards = 0
    if state[2] is not None:
        for c in state[2]:
            max_cards = max(max_cards, c)
            cards_left += c
        cards_hand = max_cards*len(state[2]) - cards_left
    return [((state[0], action), 1)]
    
    # END_YOUR_CODE

def blackjackFeatureExtractor3(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE
    # Feature 1, 2 = Cards Left, Cards in Hand (extimate)
    # Feature 1 = estimative of points in the deck
    cards_left = 0
    cards_hand = 0
    max_cards = 0
    if state[2] is not None:
        for c in state[2]:
            max_cards = max(max_cards, c)
            cards_left += c
        cards_hand = max_cards*len(state[2]) - cards_left
    return [("cards_left", cards_left), ("cands_hand", cards_hand), ((state[0], action), 1)]
    
    # END_YOUR_CODE
def blackjackFeatureExtractor2(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE
    # Feature 1, 2 = Cards Left, Cards in Hand (extimate)
    cards_left = 0
    cards_hand = 0
    max_cards = 0
    if state[2] is not None:
        for c in state[2]:
            max_cards = max(max_cards, c)
            cards_left += c
        cards_hand = max_cards*len(state[2]) - cards_left
    f1 = ("cards_left", cards_left)
    f2 = ("cards_hand", cards_hand)
    # Feature 3 = action identifiers
    f3 = (action, 1)
    # Feature 4 = my total
    f4 = ("total", state[0])
    return [f1, f2, f3, f4]
    # END_YOUR_CODE
# **********************************************************
# **                     SIMULATIONS                      **
# **********************************************************

# Funtion to simulate the ValueIteraction Algorithm
def simulateVI(mdp, vi, numTrials=10, maxIterations=1000):
    """
     Perform |numTrials| of the following:
     On each trial, take the MDP |mdp| and an RLAlgorithm |rl| and simulates the
     RL algorithm according to the dynamics of the MDP.
     Each trial will run for at most |maxIterations|.
     Return the list of rewards that we get for each trial.
    """
    def sample(probs):
        """Return i in [0, ..., len(probs)-1] with probability probs[i]."""
        target = random.random()
        accum = 0
        for i, prob in enumerate(probs):
            accum += prob
            if accum >= target: return i
        raise Exception("Invalid probs: %s" % probs)

    totalRewards = []  # The rewards we get on each trial
    for trial in range(numTrials):
        state = mdp.startState()
        sequence = [state]
        totalDiscount = 1
        totalReward = 0
        for _ in range(maxIterations):
            action = vi.pi[state]
            transitions = mdp.succAndProbReward(state, action)
            if len(transitions) == 0:
                break

            # Choose a random transition
            i = sample([prob for newState, prob, reward in transitions])
            newState, prob, reward = transitions[i]

            totalReward += totalDiscount * reward
            totalDiscount *= mdp.discount()
            state = newState
        totalRewards.append(totalReward)
    return totalRewards

def print_algorithms_compare(mdp, ql, episodes):
    vi = ValueIteration()
    vi.solve(mdp)
    rewards_vi = sum(simulateVI(mdp, vi, episodes))
    rewards_ql = sum(util.simulate(mdp, ql, episodes))
    print("VI | %.4f" % (rewards_vi/episodes))
    print("QL | %.4f" % (rewards_ql/episodes))



print("Average Reward")
print("Training with MDP1 and identityFeatureExtractor")
ql = QLearningAlgorithm(MDP1.actions, MDP1.discount(), identityFeatureExtractor)
util.simulate(MDP1, ql, 30000)
ql.explorationProb = 0

print("-----------\nMDP1")
print_algorithms_compare (MDP1, ql, 30000)
print("-----------\nMDP2")
print_algorithms_compare (MDP2, ql, 30000)
print("-----------\nlargeMDP")
print_algorithms_compare (largeMDP, ql, 30000)

print("\nTraining with MDP1 and blackjackFeatureExtractor")
ql = QLearningAlgorithm(MDP1.actions, MDP1.discount(), blackjackFeatureExtractor)
util.simulate(MDP1, ql, 30000)
print(ql.weights)
ql.explorationProb = 0

print("-----------\nMDP1")
print_algorithms_compare (MDP1, ql, 30000)
print("-----------\nMDP2")
print_algorithms_compare (MDP2, ql, 30000)
print("-----------\nlargeMDP")
print_algorithms_compare (largeMDP, ql, 30000)

print("\nTraining with largeMDP and blackjackFeatureExtractor")
ql = QLearningAlgorithm(largeMDP.actions, largeMDP.discount(), blackjackFeatureExtractor)
util.simulate(largeMDP, ql, 30000, verbose=False)
print(ql.weights)
ql.explorationProb = 0

print("-----------\nMDP1")
print_algorithms_compare (MDP1, ql, 30000)
print("-----------\nMDP2")
print_algorithms_compare (MDP2, ql, 30000)
print("-----------\nlargeMDP")
print_algorithms_compare (largeMDP, ql, 30000)