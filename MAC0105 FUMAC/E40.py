# -*- coding: utf-8 -*-
"""
Created on Wed May 16 20:00:12 2018

@author: gigec
"""
def main():
    fracao = input("Digite uma fração da forma m/n:")
    numerador = int(fracao.rpartition("/")[0])
    denominador = int(fracao.rpartition("/")[2])
    print(fracaoEgipcia(numerador, denominador))

def fracaoEgipcia(m,n):
    denominadores = []
    q = achaDenominadorEgipcio(m, n)
    denominadores.append(q)
    soma = "1/" + str(q)
    
    #Construção iterativa das frações
    while m != 1:
        m,n = subtraiFracao([m,n],q)  #acha o novo m/n = m/n - 1/q
        q = achaDenominadorEgipcio(m,n) #recalcula o q
        denominadores.append(q)
    
    for d in denominadores[1:]:
        soma += " + 1/" + str(d)
    
    return soma
        
def achaDenominadorEgipcio(m, n):

    if(m == 1):
        return n
    else:
        q = teto(n/m)
        return q

def teto(x):
    if int(x) == x:
        return x
    else:
        return int(x) + 1

def simplificaFracao(num, den):
    
    for i in range(int(min(num,den) + 2)):
        if num % (i + 2) == 0 and den % (i + 2) == 0:
            num = num / (i + 2)
            den = den / (i + 2)
            denovo = simplificaFracao(num,den)
            if [int(num), int(den)] != denovo:
                num,den = denovo[0],denovo[1]
    
    return [int(num), int(den)]

def subtraiFracao(fracao, q):
    """
    Sendo fracao1 = m/n
    Realiza uma operação do tipo m/n - 1/q com m,n,q inteiros
    """
    # m/n - 1/q = (mq - n)/nq sendo m/n > 1/q
    m = fracao[0]
    n = fracao[1]
    return simplificaFracao(m*q - n, n*q)
    
main()