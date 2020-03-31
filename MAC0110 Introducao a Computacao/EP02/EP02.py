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

def main():
    """
    Programa principal, que le as listas de palavras, pergunta se o poema deve ou ˆ
    nao usar rimas e qual o número de versos desejados, e gera o poema.
    """
    
    numsub = int(input("Quantos substantivos você deseja utilizar?"))
    subs = [[]]*numsub
    print("Digite um substantivo (com artigo) por linha:")
    for i in range(numsub):
        subs[i] = input()
    
    numver = int(input("Quantos verbos você deseja utilizar?"))
    verbos = [[]]*numver
    print("Digite um verbo (com preposição) por linha:")
    for i in range(numver):
        verbos[i] = input()
        
    rima = input("Você deseja uma poesia com rima? Responda sim ou não:")
    if rima == "sim":
        rima = True
    else:
        rima = False
        
    versos = int(input("Quantos versos você deseja que a poesia tenha?"))
    
    poema = produzVersos(subs, verbos, versos, rima)
    #Acrescentando o ponto final no final
    if poema[len(poema) - 1][len(poema[len(poema) - 1]) - 1] != ".":
        poema[len(poema) - 1] += "."
    for i in poema:
        print(i)
    
def produzVersos(substantivos, verbos, numeroDeVersos, rima):
    """
    Gera (na tela) um poema, usando as listas de substantivos e verbos 
    e com o numero de versos desejado, com ou sem rima, dependendo do 
    valor do parametro booleano rima.
    """
    M = len(substantivos + verbos)
         
    #Vetores booleanos para controle de repetições das palavras
    boolVerbos = [True]*(len(verbos) - 1)
    boolSubs = [True]*(len(substantivos) - 1)
    verso = [""]*numeroDeVersos
    
    for n in range(numeroDeVersos): #Iteração para gerar os versos
          
        #Sorteio da ordem de palavras
        #Se = 0 -> sujeito + verbo + objeto
        #Se = 1 -> sujeito + objeto + verbo
        #Se = 2 -> verbo + objeto + sujeito
        ordem = randint(0,2)
        
        if rima and n + 1 % 2 == 0: #Se precisar rimar e o verso for par
     
            if ordem == 0: #Então só o objeto precisa rimar
                rimaS = ""
                rimaV = ""
                rimaO = verso[n-1][-2:]             
           
            elif ordem == 1: #Então só o verbo precisa rimar
                rimaS = ""
                rimaV = verso[n-1][-2:]
                rimaO = ""
            
            elif ordem == 2: #Então só o sujeito precisa rimar
                rimaS = verso[n-1][-2:]
                rimaV = ""
                rimaO = ""
        else:
            rimaS = rimaV = rimaO = ""
               
        #Sorteia Verbo
        iVerbo = sorteiaIndiceVerbo(boolVerbos, verbos, M, rimaV)
        verbo = verbos[iVerbo]
        boolVerbos[iVerbo] = False #Simboliza que o verbo já foi usado
         
        #Sorteia Sujeito
        iSuj = sorteiaIndiceSubs(boolSubs, substantivos, M, rimaS) 
        sujeito = substantivos[iSuj]  #Define o sujeito do verso     
        boolSubs[iSuj] = False #Simboliza que o substantivo já foi usado
           
        #Sorteia Objeto
        iObj = sorteiaIndiceSubs(boolSubs, substantivos, M, rimaO) 
        objeto = substantivos[iObj]
        boolSubs[iObj] = False #Simboliza que o substantivo já foi usado
           
        verso[n] = geraVerso(verbo, sujeito, objeto, ordem)
          
        if verso[n][0] == " " :
            verso[n] = verso[n][1:]
        
        if (n + 1) % 2 == 0: #se for um verso par
            verso[n] += "."
            if (n + 1) % 4 == 0:
                verso[n] += "\n"
        else: #se for impar
            #Deixando a primeira letra maiuscula
            listverso = list(verso[n])
            listverso[0] = listverso[0].upper()
            verso[n] = "".join(listverso)
        
    return verso
            
def sorteiaIndiceVerbo(boolVerbos, verbos, M, rima):
    #Tenta sortear um verbo M vezes
    for i in range(M):
        
        if len(boolVerbos) > 1:
            indiceVerbo = randint(0, len(boolVerbos) - 1)
        else:
            indiceVerbo = 0
        if boolVerbos[indiceVerbo]: #Se o verbo no indice ainda não tiver sido usado
            
            #Tirando a preposição do verbo para conferir a rima
            i = -1
            while verbos[indiceVerbo][i] != " ": #Separando a preposição
                i -= 1 
            verboP = verbos[:i] #tira a preposicao
            
            if rima == "" or verboP[-2:] == rima: #Se não tiver rima ou a palavra rimar
                return indiceVerbo
     
    #Se após M repetições não for sorteado um verbo 'novo', retorna o último sorteado
    return indiceVerbo
        
def sorteiaIndiceSubs(boolSubs, subs, M, rima) :
    #Tenta sortear um substantivo M vezes
    for i in range(M):
        
        if len(boolSubs) > 1:
            indiceSubs = randint(0, len(boolSubs) - 1)
        else:
            indiceSubs = 0
        if boolSubs[indiceSubs]: #Se o substantivo no indice ainda não tiver sido usado
            if rima == "" or subs[indiceSubs][-2:] == rima: #Se não tiver rima ou a palavra rimar
                return indiceSubs
     
    #Se após M repetições não for sorteado um substantivo 'novo', retorna o último sorteado
    return indiceSubs

def geraVerso(verbo, sujeito, objeto, ordem):
    
    #Sorteio do uso de conjunções
    if randint(0,2) == 0:   
        conjuncoes = ["como", "e", "enquanto", "mesmo quando", "porque", "quando", "se", "toda vez que"]
        conjuncao = conjuncoes[randint(0, len(conjuncoes) - 1)]
        
    else:
        conjuncao = ""
        
    verbo, objeto = adequaPreposicao(verbo, objeto)
      
    verso = conjuncao + " "
    if ordem == 0:
        verso += sujeito + " " + verbo + " " + objeto
    elif ordem == 1:
        verso += sujeito + " " + objeto + " " + verbo
    elif ordem == 2:
        verso += verbo + " " + objeto + " " + sujeito
        
    return verso


def adequaPreposicao(verbo, objeto):
    
    i = -1
    while verbo[i] != " ": #Separando a preposição
        i -= 1 
        
    preposicao = verbo[i + 1:]
    
    artigo = objeto[:1]
        
    if preposicao != "com" and preposicao != "para":
        verbo = verbo[:i] #tira a preposicao
        objeto = objeto[1:] #tira o artigo
    
        if preposicao == "a":
            if artigo == "a":
                objeto = "à" + objeto
            elif artigo == "o":
                objeto = "ao" + objeto
        
        elif preposicao == "de":
            if artigo == "o":
                objeto = "do" + objeto
            elif artigo == "a":
                objeto = "da" + objeto
    
        elif preposicao == "em":
            if artigo == "o":
                objeto = "no" + objeto
            elif artigo == "a":
                objeto = "na" + objeto
             
        elif preposicao == "por":
            if artigo == "o":
                objeto = "pelo" + objeto
            elif artigo == "a":
                objeto = "pela" + objeto
                   
        elif preposicao == "-":
            objeto = artigo + objeto
    else:
        verbo = verbo[:i] #tira a preposicao
        objeto = preposicao + " " + objeto
    return verbo, objeto
       
main()