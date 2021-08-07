"""
--------------------------------------------------
MAC0427 - Otimização Não Linear
EP2 - Método do gradiente com condição de Armijo
  
Pedro Gigeck Freire - nUSP 10737136  
26/06/2021
--------------------------------------------------

A função principal deste EP é a metodo_gradiente
Os parâmetros são:

    x0       = ponto inicial
    sigma    = constante para condição de Armijo
    tau      = tolerância numérica
    max_iter = máximo de iterações para o método do gradiente
    f        = função objetivo para ser minimizada
    gradf    = função que devolve o vetor gradiente da f

A função metodo_gradiente retorna uma tupla (x, causa) onde
'x' é o ponto obtido pelo algoritmo e
'causa' é um texto indicando o motivo da parada do algoritmo   
 
Além disso, existem quatro variáveis globais que podem ser configuradas:

    passo_inicial = tamanho do passo (lambda) inicial na busca de Armijo
    reducao_passo = contante para o algoritmo da busca de Armijo,
                    determina a redução do passo em cada iteração
    log           = se True, a função principal printa o resultado final
    teste         = se True, executa uma função de teste pré defenida
    
A função de teste, junto com seu gradiente, se encontram no final do arquivo
"""

import numpy as np

passo_inicial = 1
reducao_passo = 0.8
log = False
teste = False

def metodo_gradiente (x0, sigma, tau, max_iter, f, gradf):
    k = 0
    x = x0
    while k <= max_iter and np.linalg.norm(gradf(x)) >= tau:
        d = - gradf(x)
        passo = busca_armijo (f, x, d, gradf, sigma)
        x = x + passo * d
        k = k + 1
    if k > max_iter:
    	causa = 'máximo de iterações atingido'
    else:
    	causa = 'tolerancia atingida'
    if log:
    	print('Ponto encontrado:\t', str(x))
    	print('Causa do encerramento: \t', causa)
    return (x, causa)

def busca_armijo (f, x, d, gradf, sigma):
    # Função auxiliar para definir o tamanho do passo 
    # de acordo com a condição de Armijo
    t = passo_inicial
    while f(x + t*d) > f(x) + sigma * t * np.dot(gradf(x),  d):
        t = t * reducao_passo
    return t


# ----------------------------------------------------
#   Função de teste
# ----------------------------------------------------

# f : R2 --> R
def f_teste(x):
    return x[0]**2 - 5*x[0]*x[1] + x[1]**4

# gradf : R2 --> R2
def gradf_teste(x):
    return np.array([2*x[0] - 5*x[1], -5*x[0] + 4*x[1]**3])

def executa_teste():
    x0 = np.array([1, 1])
    sigma = 0.5
    tau = 1e-7
    max_iter = 5000
    x = metodo_gradiente(x0, sigma, tau, max_iter, f_teste, gradf_teste)

# os três pontos de mínimo local da f_teste são 
# (0, 0)
# (4.42, 1.77)
# (-4.42, -1.77)

if teste:
    executa_teste()
