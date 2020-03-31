from random import randint

# flag para depuração
__DEBUG__ = 0
__MAPA__ = 1


# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global listMovimentos

global ultimaOrientacao

global nComandos

global percepcao

global mundoPercepcao

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

global impacto


def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, listMovimentos, ultimaOrientacao, nComandos, mundoPercepcao
    
    listMovimentos = []
    
    ultimaOrientacao = []
    
    mundoPercepcao = []
    
    nComandos = 0
    
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N):
        mundoPercepcao.append([[]]*N)
        mundo.append([[]]*N) # começa com listas vazias
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]


def planejar(percep):
    """ Nessa função a personagem deve atualizar seu conhecimento
        do mundo usando sua percepção da sala atual. Através desse
        parâmetro a personagem recebe (do mundo) todas as informações
        sensoriais associadas à sala atual, bem como o feedback de
        sua última ação.
        Essa percepção é uma lista de strings que podem valer:
            "F" = fedor do Wumpus em alguma sala adjacente,
            "B" = brisa de um poço em sala adjacente, 
            "I" para impacto com uma parede,
            "U" para o urro do Wumpus agonizante e
            "Nome" quando uma outra personagem é encontrada.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, impacto, percepcao, mundoPercepcao
    percepcao = percep
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.
    direita = mundo[posicao[0]][(posicao[1]+1)%N]
    esquerda = mundo[posicao[0]][(posicao[1]-1)%N]
    abaixo = mundo[(posicao[0]+1)%N][posicao[1]]
    acima = mundo[(posicao[0]-1)%N][posicao[1]]
    impacto = 0
    if len(percep)==0:
        #Salas adjacentes estão livres
        if direita != "V" and direita != "M":
            mundo[posicao[0]][(posicao[1]+1)%N] = "L"
        if abaixo != "V" and abaixo != "M":
            mundo[(posicao[0]+1)%N][posicao[1]] = "L"
        if esquerda != "V" and esquerda != "M":
            mundo[posicao[0]][(posicao[1]-1)%N] = "L"
        if acima != "V" and acima != "M":
            mundo[(posicao[0]-1)%N][posicao[1]] = "L"
    elif percep[0] == "I":
        impacto=1
        mundo[(posicao[0])%len(mundo)][(posicao[1])%len(mundo)] = "M"
            
    elif percep[0]=="B":
        mundoPercepcao[posicao[0]][posicao[1]] = "B"
        if direita == "W?":
            mundo[posicao[0]][(posicao[1]+1)%N] = "W?P?"
        elif len(direita) == 0:
            mundo[posicao[0]][(posicao[1]+1)%N] = "P?"
        if abaixo == "W?":
            mundo[(posicao[0]+1)%N][posicao[1]] = "W?P?"
        elif len(abaixo) == 0:
            mundo[(posicao[0]+1)%N][posicao[1]] = "P?"
        if esquerda == "W?":
            mundo[posicao[0]][(posicao[1]-1)%N] = "W?P?"
        elif len(esquerda) == 0:
            mundo[posicao[0]][(posicao[1]-1)%N] = "P?"
        if acima == "W?":
            mundo[(posicao[0]-1)%N][posicao[1]] = "W?P?"
        elif len(acima) == 0:
            mundo[(posicao[0]-1)%N][posicao[1]] = "P?"
    
    elif percep[0]=="F":
        mundoPercepcao[posicao[0]][posicao[1]] = "F"
        if direita == "P?":
            mundo[posicao[0]][(posicao[1]+1)%N] = "W?P?"
        elif len(direita) == 0:
            mundo[posicao[0]][(posicao[1]+1)%N] = "W?"
        if abaixo == "P?":
            mundo[(posicao[0]+1)%N][posicao[1]] = "W?P?"
        elif len(abaixo) == 0:
            mundo[(posicao[0]+1)%N][posicao[1]] = "W?"
        if esquerda == "P?":
            mundo[posicao[0]][(posicao[1]-1)%N] = "W?P?"
        elif len(esquerda) == 0:
            mundo[posicao[0]][(posicao[1]-1)%N] = "W?"
        if acima == "P?":
            mundo[(posicao[0]-1)%N][posicao[1]] = "W?P?"
        elif len(acima) == 0:
            mundo[(posicao[0]-1)%N][posicao[1]] = "W?"
    
    if len(percep)>=2:
        if percep[0]=="B" and percep[1]=="F":
            mundoPercepcao[posicao[0]][posicao[1]] = "BF"
            if direita == "P?" or direita == "W?":
                mundo[posicao[0]][(posicao[1]+1)%N] = "W?P?"
            elif len(direita) == 0:
                mundo[posicao[0]][(posicao[1]+1)%N] = "W?P?"
            if abaixo == "P?" or abaixo == "W?":
                mundo[(posicao[0]+1)%N][posicao[1]] = "W?P?"
            elif len(abaixo) == 0:
                mundo[(posicao[0]+1)%N][posicao[1]] = "W?P?"
            if esquerda == "P?" or esquerda == "W?":
                mundo[posicao[0]][(posicao[1]-1)%N] = "W?P?"
            elif len(esquerda) == 0:
                mundo[posicao[0]][(posicao[1]-1)%N] = "W?P?"
            if acima == "P?" or acima == "W?":
                mundo[(posicao[0]-1)%N][posicao[1]] = "W?P?"
            elif len(acima) == 0:
                mundo[(posicao[0]-1)%N][posicao[1]] = "W?P?"
                
    
    if mundo[posicao[0]][posicao[1]]!="M":  
        mundo[posicao[0]][posicao[1]] = "V"
    
    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
    # 
    if __MAPA__:
        print("Percepção recebida pela personagem:")
        print(percep)
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        pos = posicao
        ori = orientacao
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
                print("", end="\t| ")
                #print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

def trajeto_a_casalivre(pos,posanterior,o):
    if __DEBUG__: 
        print("")
        print("DEBUGS A SEGUIR SÃO DA FUNCAO trajeto_a_casalivre:")
    global N, listMovimentos, nComandos
    ret=0
    proxcasa = [0,0]
    newo=[0,0]
    nComandosAux=0
    #verifica se ele mesmo é uma casa livre
    #Sul=[1,0],Norte=[-1,0],Direita=[0,1],Esquerda=[0,-1]
    if mundo[pos[0]][pos[1]] == "L":
        if __DEBUG__: print("mundo[pos[0]][pos[1]](posicao destino) == 'L'")
        if pos[0]==posanterior[0] and pos[1]==(posanterior[1]+1)%N:
            if o[0]==0 and o[1]==-1: 
                listMovimentos.append("D")
                listMovimentos.append("D")
            elif o[1]==0:
                if o[0]==1:
                    listMovimentos.append("E")
                elif o[0]==-1:
                        listMovimentos.append("D")
        elif pos[0]==(posanterior[0]-1)%N and pos[1]==posanterior[1]:
            if o[0]==1: 
                    listMovimentos.append("D")
                    listMovimentos.append("D")
            elif o[0]==0:
                if o[1]==1:
                    listMovimentos.append("E")
                elif o[1]==-1:
                    listMovimentos.append("D")
        elif pos[0]==posanterior[0] and pos[1]==(posanterior[1]-1)%N:
            if o[0]==0 and o[1]==1: 
                    listMovimentos.append("D")
                    listMovimentos.append("D")
            elif o[1]==0:
                if o[0]==1:
                    listMovimentos.append("D")
                elif o[0]==-1:
                    listMovimentos.append("E")
        elif pos[0]==(posanterior[0]+1)%N and pos[1]==posanterior[1]: 
            if o[0]==-1: 
                    listMovimentos.append("D")
                    listMovimentos.append("D")
            elif o[0]==0:
                if o[1]==1:
                    listMovimentos.append("D")
                elif o[1]==-1:
                    listMovimentos.append("E")
        listMovimentos.append("A")
        return 1
    
    else:     
        if __DEBUG__:print("i's do if mundo(proxcasa) == L")
        #i = um número de 0 a 3, com ordem aleatório, para evitar chamadas recursivas infinitas
        cont=0
        i_anteriores=[]
        while cont<4:
            i = randint(0,3)
            if i in i_anteriores:
                continue
            cont+=1
            i_anteriores.append(i)
            if i==0:
                #proxcasa -> casa à direita
                proxcasa[0],proxcasa[1] = pos[0],(pos[1]+1)%N
            elif i==1:
                #proxcasa -> casa acima
                proxcasa[0],proxcasa[1] = (pos[0]-1)%N,pos[1]
            elif i==2:
                #proxcasa -> casa à esquerda
                proxcasa[0],proxcasa[1] = pos[0],(pos[1]-1)%N
            elif i==3:
                #proxcasa -> casa abaixo
                proxcasa[0],proxcasa[1] = (pos[0]+1)%N,pos[1]
            if proxcasa[0]==posanterior[0] and proxcasa[1]==posanterior[1]:
                continue
            #Calcula, se precisar, quantas vezes o personagem deve girar
            if __DEBUG__:print("\ti ==", i)
            if mundo[proxcasa[0]][proxcasa[1]] == "L":
                if i==0:           
                    #Sul=[1,0],Norte=[-1,0],Direita=[0,1],Esquerda=[0,-1]
                    newo[0],newo[1] = 0,1 
                    if o[0]==0 and o[1]==-1: 
                        listMovimentos.append("D") 
                        nComandosAux+=1
                        listMovimentos.append("D")
                        nComandosAux+=1
                    elif o[1]==0:
                        if o[0]==1:
                            listMovimentos.append("E")
                            nComandosAux+=1
                        elif o[0]==-1:
                            listMovimentos.append("D")
                            nComandosAux+=1
                elif i==1:
                    newo[0],newo[1] = -1,0
                    if o[0]==1: 
                        listMovimentos.append("D")
                        nComandosAux+=1
                        listMovimentos.append("D")
                        nComandosAux+=1
                    elif o[0]==0:
                        if o[1]==1:
                            listMovimentos.append("E")
                            nComandosAux+=1
                        elif o[1]==-1:
                            listMovimentos.append("D") 
                            nComandosAux+=1
                elif i==2:
                    newo[0],newo[1] = 0,-1 
                    if o[0]==0 and o[1]==1: 
                        listMovimentos.append("D")
                        nComandosAux+=1
                        listMovimentos.append("D")
                        nComandosAux+=1
                    elif o[1]==0:
                        if o[0]==1:
                            listMovimentos.append("D")
                            nComandosAux+=1
                        elif o[0]==-1:
                            listMovimentos.append("E") 
                            nComandosAux+=1
                elif i==3:
                    newo[0],newo[1] = 1,0
                    if o[0]==-1: 
                        listMovimentos.append("D")
                        nComandosAux+=1
                        listMovimentos.append("D")
                        nComandosAux+=1
                    elif o[0]==0:
                        if o[1]==1:
                            listMovimentos.append("D")
                            nComandosAux+=1
                        elif o[1]==-1:
                            listMovimentos.append("E") 
                            nComandosAux+=1
                listMovimentos.append("A")
                nComandosAux+=1
                nComandos=nComandosAux
                return 1
    #caso não ache uma casa livre, procura uma V
    cont=0
    i_anteriores=[]
    while cont<4:
        i = randint(0,3)
        if i in i_anteriores:
            continue
        cont+=1
        i_anteriores.append(i)
        if __DEBUG__:print("i's do if mundo(proxcasa) == V")
        if i==0:
            #proxcasa -> casa à direita
            proxcasa[0],proxcasa[1] = pos[0],(pos[1]+1)%N
        elif i==1:
            #proxcasa -> casa acima
            proxcasa[0],proxcasa[1] = (pos[0]-1)%N,pos[1]
        elif i==2:
            #proxcasa -> casa à esquerda
            proxcasa[0],proxcasa[1] = pos[0],(pos[1]-1)%N
        elif i==3:
            #proxcasa -> casa abaixo
            proxcasa[0],proxcasa[1] = (pos[0]+1)%N,pos[1]
        if proxcasa[0]==posanterior[0] and proxcasa[1]==posanterior[1]:
            continue
        #Calcula, se precisar, quantas vezes o personagem deve girar
        if __DEBUG__:print("\ti ==", i)
        if  mundo[proxcasa[0]][proxcasa[1]] == "V":
            if i==0:
                newo[0],newo[1] = 0,1 
                if o[0]==0 and o[1]==-1: 
                    listMovimentos.append("D") 
                    nComandosAux+=1
                    listMovimentos.append("D")
                    nComandosAux+=1
                elif o[1]==0:
                    if o[0]==1:
                        listMovimentos.append("E")
                        nComandosAux+=1
                    elif o[0]==-1:
                        listMovimentos.append("D")
                        nComandosAux+=1
            elif i==1:
                newo[0],newo[1] = -1,0
                if o[0]==1: 
                    listMovimentos.append("D")
                    nComandosAux+=1
                    listMovimentos.append("D")
                    nComandosAux+=1
                elif o[0]==0:
                    if o[1]==1:
                        listMovimentos.append("E")
                        nComandosAux+=1
                    elif o[1]==-1:
                        listMovimentos.append("D") 
                        nComandosAux+=1
            elif i==2:
                newo[0],newo[1] = 0,-1 
                if o[0]==0 and o[1]==1: 
                    listMovimentos.append("D")
                    nComandosAux+=1
                    listMovimentos.append("D")
                    nComandosAux+=1
                elif o[1]==0:
                    if o[0]==1:
                        listMovimentos.append("D")
                        nComandosAux+=1
                    elif o[0]==-1:
                        listMovimentos.append("E") 
                        nComandosAux+=1
            elif i==3:
                newo[0],newo[1] = 1,0
                if o[0]==-1: 
                    listMovimentos.append("D")
                    nComandosAux+=1
                    listMovimentos.append("D")
                    nComandosAux+=1
                elif o[0]==0:
                    if o[1]==1:
                        listMovimentos.append("D")
                        nComandosAux+=1
                    elif o[1]==-1:
                        listMovimentos.append("E") 
                        nComandosAux+=1
            listMovimentos.append("A")
            nComandosAux+=1
            nComandos=nComandosAux
            if mundo[proxcasa[0]][proxcasa[1]] == "V":
                ret = trajeto_a_casalivre(proxcasa,pos,newo)
                if ret==-1:
                    for k in range(nComandos):
                        del listMovimentos[-1]#decrementa global
                elif ret==1:
                    return 1
    return -1
    



def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, impacto, listMovimentos, N, nComandos
    # Aplica uma certa estratégia para decidir a ação a ser
    # executada com base na representação local do mundo.
    # Devolve (para o mundo) o nome da ação pretendida.
    # Duas ações só são possíveis em condições específicas,
    # que devem ser testadas de antemão (sob risco da personagem
    # entrar em loop): atirar só é possível quando a personagem
    # dispõe de flechas, e compartilhar só é possível quando
    # existem outras personagens na mesma sala (percebidas
    # pela função planejar através de percepções diferentes de
    # "F", "B", "I" ou "U").
    #Adiciona à percepção de mundo as informações do mundoCompartilhado
    existe_livre=0
    ret=0
    prox_posicao=[0,0]
    o = [0,0]
    o[0],o[1] = orientacao[0],orientacao[1]
    #SE FOR DIFERENTE DE 0, TOMA AS ACOES PURAMENTE BASEADO EM LISTMOVIMENTOS
    if len(listMovimentos)==0:
        nComandos=0
        for i in range(N):
            for j in range(N):
                if mundo[i][j]=="L":
                    
                    existe_livre = 1 
        if existe_livre==1:
            if __DEBUG__: print("Existe casa Livre no mapa")
            i=0
            while ret!=1 and i<4:
                if i==0:#direita
                    prox_posicao[0],prox_posicao[1] = posicao[0],(posicao[1]+1)%N
                elif i==1:#acima
                    prox_posicao[0],prox_posicao[1] = (posicao[0]-1)%N,posicao[1]
                elif i==2:#esquerda
                    prox_posicao[0],prox_posicao[1] = posicao[0],(posicao[1]-1)%N
                elif i==3:#abaixo
                    prox_posicao[0],prox_posicao[1] = (posicao[0]+1)%N,posicao[1]
                if mundo[prox_posicao[0]][prox_posicao[1]] == "V" or mundo[prox_posicao[0]][prox_posicao[1]] == "L":
                    if __DEBUG__: print("mundo[",prox_posicao[0],"][",prox_posicao[1],"](prox_posicao) é == 'V' ou 'L'", sep="")
                    if __DEBUG__: print("Matriz mundo: ", mundo)
                    if __DEBUG__: print("Matriz mundoCompartilhado: ", mundoCompartilhado)
                    
                    
                    if mundo[prox_posicao[0]][prox_posicao[1]] == "V":
                        if __DEBUG__: print("mundo[",prox_posicao[0],"][",prox_posicao[1],"](prox_posicao) é == 'V'", ". i ==", i, sep="")
                        
                        if i==0:
                            #Sul=[1,0],Norte=[-1,0],Direita=[0,1],Esquerda=[0,-1]
                            if orientacao[0]==0 and orientacao[1]==-1:
                                listMovimentos.append("D")
                                listMovimentos.append("D")
                            elif orientacao[1]==0:
                                if orientacao[0]==1:
                                    listMovimentos.append("E")
                                elif orientacao[0]==-1:
                                    listMovimentos.append("D")
                            o[0],o[1] = 0,1
                        elif i==1:   
                            if orientacao[0]==1: 
                                    listMovimentos.append("D")
                                    listMovimentos.append("D")
                            elif orientacao[0]==0:
                                if orientacao[1]==1:
                                    listMovimentos.append("E")
                                elif orientacao[1]==-1:
                                    listMovimentos.append("D")
                            o[0],o[1] =-1,0
                        elif i==2:
                            if orientacao[0]==0 and orientacao[1]==1: 
                                    listMovimentos.append("D")
                                    listMovimentos.append("D")
                            elif orientacao[1]==0:
                                if orientacao[0]==1:
                                    listMovimentos.append("D")
                                elif orientacao[0]==-1:
                                    listMovimentos.append("E")
                            o[0],o[1] = 0,-1
                        elif i==3: 
                            if orientacao[0]==-1: 
                                    listMovimentos.append("D")
                                    listMovimentos.append("D")
                            elif orientacao[0]==0:
                                if orientacao[1]==1:
                                    listMovimentos.append("D")
                                elif orientacao[1]==-1:
                                    listMovimentos.append("E")
                            o[0],o[1] = 1,0
                        listMovimentos.append("A")
                    #Sul=[1,0],Norte=[-1,0],Direita=[0,1],Esquerda=[0,-1]
                    if __DEBUG__: print("Está enviando para funcao trajeto_a_casalivre (",prox_posicao,", ", posicao, ", ", o, ")",sep="")
                    ret = trajeto_a_casalivre(prox_posicao,posicao,o)
                i+=1
        else: 
            #Caso não haja mais casas livres no mapa
            listMovimentos.append("E")
    
    if __DEBUG__:print("LISTMOVIMENTOS",listMovimentos) 
    if "Dummy" in percepcao:
        acao = "C"
    else:
        acao = listMovimentos[0]
        del listMovimentos[0]
    
    
    for i in range(N):
        for j in range(N):
            if len(mundoCompartilhado[i][j])==1:
                if mundo[i][j]!="V" and (mundo[i][j]=="W?" or mundo[i][j]=="P?" or mundo[i][j]=="W?P?" or mundo[i][j]=="P?W?"):
                    if "L" in mundoCompartilhado[i][j]:
                        mundo[i][j]="L"
                    elif "W" in mundoCompartilhado[i][j]:
                        mundo[i][j]="W"
                    elif "P" in mundoCompartilhado[i][j]:
                        mundo[i][j]="P"
    
    """if __MAPA__:
        a = input("Aperte ENTER para continuar ou digite 'e' para interromper")
        if a=="e":
            exit()
    """
        
    pos = posicao
    ori = orientacao
    if impacto == 1:
            impacto=0
            for i in range(len(listMovimentos)):
                del listMovimentos[0]
            pos[0] = (pos[0]-ori[0])%len(mundo)
            pos[1] = (pos[1]-ori[1])%len(mundo)
    if acao=="A":
        if impacto != 1:
            pos[0] = (pos[0]+ori[0])%len(mundo)
            pos[1] = (pos[1]+ori[1])%len(mundo)
    elif acao=="E":
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
    elif acao=="D":
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####
   
    assert acao in ["A","D","E","T","C"]
    return acao
