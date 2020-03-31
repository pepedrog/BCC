# flag para depuração
__DEBUG__ = True

# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global nFlechas
"""
Número de flechas que a personagem possui. Serve apenas para
consulta da personagem, pois o mundo mantém uma cópia "segura" dessa
informação (não tente inventar flechas...).
"""

global mundoCompartilhado
"""
Esse é um espaço onde a personagem tem acesso à representação do
mundo de uma outra personagem.  Essa informação pode ser usada como a
personagem quiser (por exemplo, transferindo o conteúdo para o seu
próprio "mundo", ou mantendo uma lista dos vários mundos
compartilhados com outras personagens).
"""

# Outras variáveis globais do módulo personagemNUSP

global N
""" Dimensão do mundo.
"""

global mundo
"""
Representa o conhecimento da personagem em relação ao Mundo de
Wumpus. Essa é uma matriz de NxN onde a personagem toma notas de suas
percepções ao longo do caminho que percorre, indicando os muros, as
salas livres e as salas percorridas, bem como a proximidade de perigos
(poços e Wumpus). A geometria do mundo é a de um toro (aquela figura
que parece um donut!) onde existem sempre 4 salas vizinhas à posição
[i][j]: em sentido horário e a partir da (nossa) direita essas seriam:
[i][(j+1)%N], [(i+1)%N][j], [i][(j-1)%N] e [(i-1)%N][j]. Cada entrada
mundo[i][j] é uma lista de anotações/rótulos correspondentes às
informações encontradas ou deduzidas pela personagem sobre o conteúdo
da sala (i,j).
"""

global posicao
"""
Representa a posição relativa da personagem no mundo. Cada
personagem começa em uma posição aleatória (e desconhecida por ela,
pois não possui GPS ou equivalente) do Mundo "real" de Wumpus, e por
isso precisa usar um sistema de coordenadas pessoal para se orientar.
Por convenção, sua posição inicial é representada como [0,0] (canto
superior esquerdo) nesse sistema. Como o mundo não tem bordas, podemos
usar sempre os i=0,...,N-1 e j=0,...,N-1, que percorrem todas as salas
possíveis do Mundo de Wumpus, usando o operador módulo (%) para
corrigir a posição quando um passo nos levar a uma sala de índice <0
ou >=N.
"""

global orientacao
"""
Juntamente com a posição relativa, permite à personagem manter o
histórico das salas visitadas. Essa orientação é independente da
orientação "real" que o mundo usa para coordenar a ação de todas as
personagens. Por convenção, todas as personagens indicam sua orientação
inicial como "para baixo" ou "sul", correspondente à direção [1,0]
(direção do eixo vertical).
"""

#VARIÁVEIS GLOBAIS CRIADAS PARA AUXILIAR A CONSTRUÇÃO E PARA POSTERIOR FUNCIONAMENTO DAS FUNÇÕES planejar(percepcao) E agir().

global percepcao_precedente
"""
O objetivo dessa variável é guardar a percepção recebida pela personagem em
uma rodada do jogo para tomar a próxima decisão, isto é, para escolher a próxima
sala a ser visitada de maneira segura ou para inferir a sala em que há algum perigo/
obstáculo (Wumpus ou poço/muro) e, consequentemente, alterar a representação do
mundo de modo a melhor representar o conhecimento mais atualizado da personagem
em cada rodada do jogo.
"""

global posicao_precedente
"""
O objetivo dessa variável é corrigir o erro do código original no caso em 
que a variável encontra o muro. Quando a personagem colide contra o muro,
a variável "posicao_precedente" armazena a posição da personagem imediatamente
anterior ao choque e atribui esta posição para a variável "posicao" após o
encontro com o muro.
"""

def inicializa(tamanho):

    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, percepcao_precedente, posicao_precedente

    #INICIALIZAÇÃO DAS SALAS QUE SERVIRÃO DE REFERÊNCIA À PERSONAGEM.
    posicao=[0,0]
    orientacao=[1,0]
    percepcao_precedente=[]
    posicao_precedente=[]

    # guarda o tamanho do mundo
    N = tamanho

    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mundo.append(linha)

def posicao_posterior(mundo, mundoCompartilhado, posicao):
    """
       Esta função deve, acima de tudo, garantir a sobrevivência da personagem
       ao devolver somente posições livres de armadilhas (poços e Wumpus) ou
       a posição certeira do Wumpus.
       Logo, ela procura salas adjacentes livres ou visitadas para garantir que a
       personagem não caia em um poço ou morra devorada por um WUmpus. Além disso,
       a função retorna a posição correta do Wumpus para que a personagem não
       use a sua flecha desnecessariamente.
    """

    #VARIÁVEL QUE REPRESENTA O TAMANHO DA MATRIZ EM QUE A PERSONAGEM ESTÁ INSERIDA.
    N=len(mundo)

     #VERIFICA SE A SALA É LIVRE E, PORTANTO, PASSÍVEL DE SER VISITADA PELA PERSONAGEM.
    if ("V" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "L" in mundoCompartilhado[(posicao[0]-1)%N][posicao[1]%N]) or ("V" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "L" in mundo[(posicao[0]-1)%N][posicao[1]%N]):
        return [(posicao[0]-1)%N, posicao[1]%N]

    if ("V" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "L" in mundoCompartilhado[posicao[0]%N][(posicao[1]-1)%N]) or ("V" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "L" in mundo[posicao[0]%N][(posicao[1]-1)%N]):
        return [posicao[0]%N, (posicao[1]-1)%N]

    if ("V" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "L" in mundoCompartilhado[(posicao[0]+1)%N][posicao[1]%N]) or ("V" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "L" in mundo[(posicao[0]+1)%N][posicao[1]%N]):
        return [(posicao[0]+1)%N, posicao[1]%N]

    if ("V" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "L" in mundoCompartilhado[posicao[0]%N][(posicao[1]+1)%N]) or ("V" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "L" in mundo[posicao[0]%N][(posicao[1]+1)%N]):
        return [posicao[0]%N, (posicao[1]+1)%N]

   #RETORNA A POSIÇÃO DO WUMPUS QUE SE ENCONTRA NAS SALAS ADJACENTES À SALA DA PERSONAGEM PARA QUE ESSE SEJA MORTO.
    if "W" in mundoCompartilhado[(posicao[0]-1)%N][posicao[1]%N] or "W" in mundo[(posicao[0]-1)%N][posicao[1]%N]:
        return [(posicao[0]-1)%N, posicao[1]%N]

    if "W" in mundoCompartilhado[posicao[0]%N][(posicao[1]-1)%N] or "W" in mundo[posicao[0]%N][(posicao[1]-1)%N]:
        return [posicao[0]%N, (posicao[1]-1)%N]

    if "W" in mundoCompartilhado[(posicao[0]+1)%N][posicao[1]%N] or "W" in mundo[(posicao[0]+1)%N][posicao[1]%N]:
        return [(posicao[0]+1)%N, posicao[1]%N]

    if "W" in mundoCompartilhado[posicao[0]%N][(posicao[1]+1)%N] or "W" in mundo[posicao[0]%N][(posicao[1]+1)%N]:
        return [posicao[0]%N, (posicao[1]+1)%N]

    #RETORNA UMA CASA QUE JÁ TENHA SIDO VISITADA E, PORTANTO, É SEGURA.
    if "V" in mundo[(posicao[0]-1)%N][posicao[1]%N]:
        return [(posicao[0]-1)%N, posicao[1]%N]    

    if "V" in mundo[posicao[0]%N][(posicao[1]-1)%N]:
        return [posicao[0]%N, (posicao[1]-1)%N]

    if "V" in mundo[(posicao[0]+1)%N][posicao[1]%N]:
        return [(posicao[0]+1)%N, posicao[1]%N]

    if "V" in mundo[posicao[0]%N][(posicao[1]+1)%N]:
        return [posicao[0]%N, (posicao[1]+1)%N]

def planejar(percepcao):

    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, posicao_precedente, percepcao_precedente

    N=len(mundo)
  
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)

    #CORREÇÃO DO ERRO DO CÓDIGO ORIGINAL NO CASO EM QUE A PERSONAGEM COLIDE CONTRA O MURO.
    percepcao_precedente=percepcao

    if "I" in percepcao:

        if "M" not in mundo[(posicao[0]-1)%N][posicao[1]%N]:
            mundo[posicao[0]][posicao[1]].append("M")
            posicao=posicao_precedente

        if "M" not in mundo[posicao[0]%N][(posicao[1]-1)%N]:
            mundo[posicao[0]][posicao[1]].append("M")
            posicao=posicao_precedente

        if "M" not in mundo[(posicao[0]+1)%N][posicao[1]%N]:
            mundo[posicao[0]][posicao[1]].append("M")
            posicao=posicao_precedente

        if "M" not in mundo[posicao[0]%N][(posicao[1]+1)%N]:
            mundo[posicao[0]][posicao[1]].append("M")
            posicao=posicao_precedente

    #SE A PERSONAGEM RECEBE A PERCEPÇÃO "F" EM SUA LISTA DE PERCEPÇÕES, ENTÃO HÁ UM WUMPUS EM ALGUMA SALA ADJACENTE. LOGO, ELA MARCA AS SALAS ADJACENTES COM "W?"
    #CONTANTO QUE A SALA NÃO TENHA SIDO VISITADA NEM SEJA LIVRE NEM TENHA UM MURO. 
    if "F" in percepcao:

        if "V" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "L" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "W?" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]-1)%N][posicao[1]%N]:
            mundo[(posicao[0]-1)%N][posicao[1]%N].append("W?")

        if "V" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "L" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "W?" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]-1)%N]:
            mundo[posicao[0]%N][(posicao[1]-1)%N].append("W?")

        if "V" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "L" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "W?" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]+1)%N][posicao[1]%N]:
            mundo[(posicao[0]+1)%N][posicao[1]%N].append("W?")

        if "V" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "L" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "W?" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]+1)%N]:
            mundo[posicao[0]%N][(posicao[1]+1)%N].append("W?")

    #SE A PERSONAGEM RECEBE A PERCEPÇÃO "B" EM SUA LISTA DE PERCEPÇÕES, ENTÃO HÁ UM POÇO EM ALGUMA SALA ADJACENTE. LOGO, ELA MARCA AS SALAS ADJACENTES COM "P?"
    #CONTANTO QUE A SALA NÃO TENHA SIDO VISITADA NEM SEJA LIVRE NEM TENHA UM MURO.
    if "B" in percepcao:

        if "V" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "L" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "P?" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]-1)%N][posicao[1]%N]:
            mundo[(posicao[0]-1)%N][posicao[1]%N].append("P?")

        if "V" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "L" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "P?" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]-1)%N]:
            mundo[posicao[0]%N][(posicao[1]-1)%N].append("P?")

        if "V" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "L" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "P?" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]+1)%N][posicao[1]%N]:
            mundo[(posicao[0]+1)%N][posicao[1]%N].append("P?")

        if "V" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "L" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "P?" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]+1)%N]:
            mundo[posicao[0]%N][(posicao[1]+1)%N].append("P?")
   
    #SE A LISTA DE PERCEPÇÕES DA PERSONAGEM ESTÁ VAZIA, ENTÃO ELA ESTÁ EM UMA SALA CUJAS SALAS ADJACENTES NÃO POSSUEM OBSTÁCULOS NEM ARMADILHAS. LOGO, ELA MARCA AS
    #SALAS ADJACENTES COM "L" CONTANTO QUE A SALA NÃO TENHA SIDO VISITADA NEM SEJA LIVRE. 
    if percepcao==[]:

        if "V" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "L" not in mundo[(posicao[0]-1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]-1)%N][posicao[1]%N]:
            mundo[(posicao[0]-1)%N][posicao[1]%N].append("L")

        if "V" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "L" not in mundo[posicao[0]%N][(posicao[1]-1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]-1)%N]:
            mundo[posicao[0]%N][(posicao[1]-1)%N].append("L")

        if "V" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "L" not in mundo[(posicao[0]+1)%N][posicao[1]%N] and "M" not in mundo[(posicao[0]+1)%N][posicao[1]%N]:
            mundo[(posicao[0]+1)%N][posicao[1]%N].append("L")

        if "V" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "L" not in mundo[posicao[0]%N][(posicao[1]+1)%N] and "M" not in mundo[posicao[0]%N][(posicao[1]+1)%N]:
            mundo[posicao[0]%N][(posicao[1]+1)%N].append("L")

    pos=posicao
    ori=orientacao
    mundo[pos[0]][pos[1]]=["V"]

    if __DEBUG__:

        # mostra na tela (para o usuário) o mundo conhecido pela personagem
        # e o mundo compartilhado (quando disponível)
        print("Mundo conhecido pela personagem:")
        for i in range(len(mundo)):
            for j in range(len(mundo[0])):
                if pos==[i,j]:
                    if ori==[0,-1]:
                        print("<",end="")
                    print("X",end="")
                    if ori==[0,1]:
                        print(">",end="")
                    if ori==[1,0]:
                        print("v",end="")
                    if ori==[-1,0]:
                        print("^",end="")
                print("".join(mundo[i][j]),end="")
                print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))

def agir():

    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, posicao_precedente, percepcao_precedente

    N=len(mundo)
    posicao_atualizada=posicao_posterior(mundo, mundoCompartilhado, posicao)

    if (posicao[0]+orientacao[0])%N==(posicao_atualizada[0]%N) and (posicao[1]+orientacao[1])%N==(posicao_atualizada[1]%N):
        if "W" in mundoCompartilhado[(posicao[0]+orientacao[0])%N][(posicao[1]+orientacao[1])%N] or "W" in mundo[(posicao[0]+orientacao[0])%N][(posicao[1]+orientacao[1])%N]:
            acao="T"    
        else:
            acao="A"
    else:
        acao="D"

    if "Dummy" in percepcao_precedente:
        acao="C"

    if acao=="A":
        posicao_precedente=[posicao[0], posicao[1]]
        posicao[0]=(posicao[0]+orientacao[0])%N
        posicao[1]=(posicao[1]+orientacao[1])%N

    if acao=="E":
        if orientacao[0]==0:
            orientacao[1]=-orientacao[1]
        orientacao[0],orientacao[1]=orientacao[1],orientacao[0]

    if acao=="D":
        if orientacao[1]==0:
            orientacao[0]=-orientacao[0]
        orientacao[0],orientacao[1]=orientacao[1],orientacao[0]

    if __DEBUG__:
        print("acao:", acao)
        print("========================Fim da instrução===============================")
    assert acao in ["A","D","E","T","C"]
    return acao
