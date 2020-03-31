"""
  AO PREENCHER ESSE CABEÇALHO COM O MEU NOME E O MEU NÚMERO USP, 
  DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESSE PROGRAMA. 
  TODAS AS PARTES ORIGINAIS DESSE EXERCÍCIO PROGRAMA (EP) FORAM 
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUÇÕES
  DESSE EP E QUE PORTANTO NÃO CONSTITUEM DESONESTIDADE ACADÊMICA
  OU PLÁGIO.  
  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR TODAS AS CÓPIAS
  DESSE PROGRAMA E QUE EU NÃO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUIÇÃO. ESTOU CIENTE QUE OS CASOS DE PLÁGIO E
  DESONESTIDADE ACADÊMICA SERÃO TRATADOS SEGUNDO OS CRITÉRIOS
  DIVULGADOS NA PÁGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NÃO SERÃO CORRIGIDOS E,
  AINDA ASSIM, PODERÃO SER PUNIDOS POR DESONESTIDADE ACADÊMICA.

  Nome : Pedro Gigeck Freire
  NUSP : 10737136
  Turma: 2018
  Prof.: Marcelo Gomes de Queiroz

"""
from random import randint 

# Função obrigatória
def distribuicao(N):
    """Devolve um inteiro dist onde cada dígito n=0,...N-1 representa
    um peso relativo em uma distribuição de probabilidade,
    verificando que dist esteja entre 0 e 10**N-1.
    """
    
    #Inicializando as variáveis que serão usadas na função
    dist = randint(0,9)     #Sorteia o primeiro número de dist
    casadecimal = 10        #Como o primeiro dígito já foi estabelecido, o próximo será multiplicado por 10
    M = N                   #Variável para manipular o valor de N sem prejudicar o assert
    
    #Laço que sorteará um valor para dist a cada unidade de M
    while M > 1:      
        
        #Define o dígito e multiplica pelo valor que encaixará-o na casa decimal correspondente
        proximodist = randint(0,9)      
        proximodist = proximodist * casadecimal
        dist = dist + proximodist
        
        #Aumenta uma casa decimal multiplicando por 10
        casadecimal = casadecimal * 10
        
        M -= 1;
    
    assert dist in range(10**N)
    return dist

# Função obrigatória
def jogada(N,jogador,lanceanterior):
    """Processa e devolve uma jogada do jogador ("humano" ou "computador"),
    que deve estar entre 0 e N-1 e não pode ser igual a lanceanterior.
    """
    #Conferência de qual o jogador da jogada, que contém um laço que só permite a continuidade
    #se o jogador der um lance diferente do anterior
    if jogador == "jogador":
        lance = int(input("É a sua vez de jogar:"))
        while lance == lanceanterior:
            print("A mesa já escolheu esse número.")
            lance = int(input("É a sua vez de jogar:"))
    else:
        print("É a vez da mesa jogar.")
        lance = randint(0,N-1)
        while lance == lanceanterior:           
            lance = randint(0,N-1);
        print("A mesa escolhe o número ",lance,".",sep="")    
    
    assert lance in range(N) and lance != lanceanterior
    return lance

# Função obrigatória
def sorteia(N,dist):
    """Devolve o resultado de um sorteio enviesado dentre os
    inteiros de 0 a N-1 de acordo com a distribuição dist.
    """
    #distm é uma variável que será manipulada no lugar de dist, que será usado mais a frente
    distm = dist
    #iniciando a soma, definindo o primeiro dígito
    S = distm % 10
    
    #Enquanto distm tiver mais que dois dígitos,
    #"Retira-se" o dígito que já foi somado e soma o próximo
    while distm > 9:
         distm = distm // 10 
         S += distm % 10
    
    #Sorteio do número relacionado aos pesos de cada valor de N
    sorteiopeso = randint(0,S-1)
    
    #Cálculo da somatoria Sparcial dos pesos P0 + P1 ... + Psorteio
    #tal que sorteio é o maior inteiro que faz Sparcial maior que sorteiopeso
    Sparcial = dist % 10
    sorteio = 0
    #Enquanto o Sparcial for maior que o sorteiopeso, o sorteio pode ser aumentado
    while sorteiopeso >= Sparcial:
        #Cálculo do Sparcial, que soma cada dígito de dist, como no cálculo de S
         dist = dist // 10
         Sparcial += dist % 10
         sorteio += 1
    
    assert sorteio in range(N)
    return sorteio

#Iniciando o jogo
N = int(input("Bem vind@ à roleta maluca!\nPor favor digite a quantidade de elementos da roleta (entre 2 e 100):"))

#Verificação se o jogador inseriu um N válido
while not(N >= 2 and N<=100):
    N = int(input("Por favor digite um inteiro entre 2 e 100:"))

print("A roleta possui os números 0...", N-1,sep="")
print("Aguarde enquanto envieso a roleta...")

#Enviesando a roleta
dist = distribuicao(N)

#Iniciando a primeira rodada, com as pontuações zeradas
continua = "S"
rodada = 1
pontuacaojogador = 0

#Enquanto o jogador quiser continuar jogando:
while continua == "S":
    print("\nRodada", rodada)
    print("Escolhendo jogador inicial...")
    
    #Sorteio da ordem das jogadas
    if randint(0,1) == 0:
        #Mesa joga primeiro, ou
        jmesa = jogada(N,"mesa",-1)
        jjogador = jogada(N,"jogador",jmesa)
    else:
        #Jogador joga primeiro
        jjogador = jogada(N,"jogador",-1)
        jmesa = jogada(N,"mesa", jjogador)
 
    #Sorteando um valor de 0 a N -1
    sorteio = sorteia(N, dist)
    print("Sorteio =", sorteio)
    
    #Verificação de qual jogada se aproximou mais do sorteio
    #Considerando a distância radial, conforme descrito no enunciado
    #Desempatando a favor do jogador (quando a distancia jogador == distancia mesa)
    if(min(jjogador - sorteio, sorteio - jjogador) >= min(jmesa - sorteio, sorteio - jmesa)):
        print("Você ganhou!")
        #Verificação se foi um acerto preciso ou aproximado
        if sorteio == jjogador:
            pontuacaojogador += 100
        else:
            pontuacaojogador += 10
    else:
        print("A mesa ganhou")
        if sorteio == jmesa:
            pontuacaojogador -= 100
        else:
            pontuacaojogador -= 10
            
    #As pontuações são baseadas no fato de que a pontuação da mesa é oposta ao do jogador
    
    #Finalizando a rodada
    print("Pontuação: Jogador = ", pontuacaojogador, ", Mesa = ", -pontuacaojogador, sep="")
    continua = input("Deseja continuar jogando (S/N):")
    rodada += 1

#Finalizando o jogo
#Função opcional
def desmontaroleta(N,dist):
    """Explicita a estrutura da roleta maluca, enviesada pela
    distribuição dist: para cada inteiro entre 0 e N-1 mostra
    o peso correspondente (entre 0 e 9), a probabilidade
    teórica associada, e a frequência relativa deste dígito
    em uma repetição de 1000 sorteios com essa distribuição.
    """
    
    print("Essa é a estrutura da roleta maluca:")
    print("x\tPeso\tProb(x)\tFreq(x)")
    
    #Variável para poder manipular N e dist sem comprometer os outros processos
    M = N
    distm = dist
    distn = dist 
    #Cálculo da soma de todos os pesos, para poder calcular a probabilidade
    Sprob = distm % 10
    #Enquanto distm tiver mais que dois dígitos,
    #"Retira-se" o dígito que já foi somado e soma o próximo
    while distm > 9:
        distm = distm // 10 
        Sprob += distm % 10 
    
    #Laço que calcula a probabilidade e a frequência para cada valor de M-1 a 0
    while M > 0:
        x = N - M     
        
        #Cálculo do peso
        Peso = distn % 10
        distn = distn // 10     
        Prob = Peso / Sprob
        
        Sfreq = 0
        contador = 0
        
        #Verificação da frequência de x em 1000 sorteios
        while contador < 1000:
            if sorteia(N, dist) == x:
                Sfreq += 1
            
            contador += 1
        
        Freq = Sfreq / 1000
        print(x,Peso,"{0:2.3f}".format(Prob),"{0:2.3f}".format(Freq), sep="\t")
        
        M -= 1

#Checagem da função bônus
if continua == "Abra o jogo!":
  desmontaroleta(N, dist)

#Se o jogador venceu ou o jogo empatou
if pontuacaojogador >= -pontuacaojogador:
    print("\nVocê deve receber", pontuacaojogador, "da mesa!")
else:
#Se o jogador perdeu
    print("\nVocê deve pagar", pontuacaojogador, "para a mesa!")
    
print("Obrigado por jogar a roleta maluca!")
         