from copy import deepcopy

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

def adjRoom(value):
    """Checa se o valor está em alguma das salas adjacentes, se sim, retorna
    as coordenadas de alguma das salas adj. com o valor, caso contrário, 
    retorna False
    """
    global mundo
    a1=[(posicao[0]+1)%N, (posicao[1]), mundo[(posicao[0]+1)%N][(posicao[1])]]
    a2=[(posicao[0]-1)%N, (posicao[1]), mundo[(posicao[0]-1)%N][(posicao[1])]]
    a3=[(posicao[0]), (posicao[1]+1)%N, mundo[(posicao[0])][(posicao[1]+1)%N]]
    a4=[(posicao[0]), (posicao[1]-1)%N, mundo[(posicao[0])][(posicao[1]-1)%N]]
    adj=[ a1,a2,a3,a4 ]
     
    for k in adj:
        if value in k[2]:
            return [True, [ k[0], k[1] ] ]
    
    return [False,[],[]]

def freeNeighborRoom():
    """Checa se existe uma casa livre e não visita nas adjacências e 
    retorna suas coordenadas se existir
    """
    global mundo, posicao
    a1=[(posicao[0]+1)%N, posicao[1], mundo[(posicao[0]+1)%N][(posicao[1])]]
    a2=[(posicao[0]-1)%N, posicao[1], mundo[(posicao[0]-1)%N][(posicao[1])]]
    a3=[posicao[0], (posicao[1]+1)%N, mundo[(posicao[0])][(posicao[1]+1)%N]]
    a4=[posicao[0], (posicao[1]-1)%N, mundo[(posicao[0])][(posicao[1]-1)%N]]
    adj=[ a1, a2, a3 ,a4 ]

    for k in adj:
        if ("L" in k[2]) and not ("V" in k[2]):
            return [True,[k[0],k[1]]]

    return [False,[],[]]

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mundo.append(linha)

    # Lista de salas livres e não visitadas
    global toExplore
    toExplore=[]

    # var. booleana p/ indicar se há jogadores na sala
    global playerInRoom
    playerInRoom=False

    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]

def planejar(percepcao):
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, toExplore, playerInRoom


    def setPThreat(threat):
        """Associa possíveis ameaças nas casas adjacentes
        Caso casa não possua "L", "V", "M" e percepção de 
        ameaça na casa atual """
        
        global mundo, posicao, orientacao
        
        if threat=="F":
            threat2="W?"

        if threat=="B":
            threat2="P?"

        if not (threat in mundo[posicao[0]][posicao[1]]):
            mundo[posicao[0]][posicao[1]].append(threat)

        if not any(i in ["L","V","M","W?","P?","W","P"] for i in mundo[(posicao[0]+1)%N][posicao[1]]):
            mundo[(posicao[0]+1)%N][posicao[1]].append(threat2)
            mundo[(posicao[0]+1)%N][posicao[1]].sort()

        if not any(i in ["L","V","M","W?","P?","W","P"] for i in mundo[(posicao[0]-1)%N][posicao[1]]):
            mundo[(posicao[0]-1)%N][posicao[1]].append(threat2)
            mundo[(posicao[0]-1)%N][posicao[1]].sort()

        if not any(i in ["L","V","M","W?","P?","W","P"] for i in mundo[posicao[0]][(posicao[1]+1)%N]):
            mundo[posicao[0]][(posicao[1]+1)%N].append(threat2)
            mundo[posicao[0]][(posicao[1]+1)%N].sort()

        if not any(i in ["L","V","M","W?","P?","W","P"] for i in mundo[posicao[0]][(posicao[1]-1)%N]):
            mundo[posicao[0]][(posicao[1]-1)%N].append(threat2)
            mundo[posicao[0]][(posicao[1]-1)%N].sort()
    
    def setFree():
        """Marca como livres as salas adjacentes a salas
          s/ indicadores de ameaças """
        
        global mundo, posicao, orientacao, toExplore

        if not any(i in ["L","M"] for i in mundo[(posicao[0]+1)%N][posicao[1]]):
            mundo[(posicao[0]+1)%N][posicao[1]].append("L")
            if [(posicao[0]+1)%N,(posicao[1])] not in toExplore:
                toExplore.append([(posicao[0]+1)%N,(posicao[1])])

        if not any(i in ["L","M"] for i in mundo[(posicao[0]-1)%N][posicao[1]]):
            mundo[(posicao[0]-1)%N][posicao[1]].append("L")
            if [(posicao[0]-1)%N,(posicao[1])] not in toExplore:
                toExplore.append([(posicao[0]-1)%N,(posicao[1])])

        if not any(i in ["L","M"] for i in mundo[posicao[0]][(posicao[1]+1)%N]):
            mundo[posicao[0]][(posicao[1]+1)%N].append("L")
            if [(posicao[0])%N,(posicao[1]+1)%N] not in toExplore:
                toExplore.append([(posicao[0])%N,(posicao[1]+1)%N])

        if not any(i in ["L","M"] for i in mundo[posicao[0]][(posicao[1]-1)%N]):
            mundo[posicao[0]][(posicao[1]-1)%N].append("L")
            if [(posicao[0])%N,(posicao[1]-1)%N] not in toExplore:
                toExplore.append([(posicao[0])%N,(posicao[1]-1)%N])

    def remove2(item,lista):
        """ Remove item da lista, se existir"""
        if item in lista:
            lista.remove(item)

        return lista
    
    def intelUpdate():
        """Realiza junção de informações do mundo com mundoCompartilhado
        """
        global mundo, mundoCompartilhado, toExplore
        for i in range(len(mundo)):
            for j in range(len(mundo[0])):
                if (mundoCompartilhado[i][j] == "L") and ("V" not in mundo[i][j]):
                    mundo[i][j] = mundoCompartilhado[i][j]
                    toExplore.append([i,j])
                if any(i in ["P","W"] for i in mundoCompartilhado[i][j]) and not any( i in ["V","L"] for i in mundo[i][j]):
                    mundo[i][j] = mundoCompartilhado[i][j]
                if mundoCompartilhado[i][j] == "M":
                    mundo[i][j] = mundoCompartilhado[i][j]

    def checkPlayer(percepcao):
        # checa a existência de um jogador na mesma sala
        global playerInRoom
        from copy import deepcopy
        x=deepcopy(percepcao)
        x=remove2("F",x)
        x=remove2("B",x)
        x=remove2("I",x)
        x=remove2("U",x)
        if x==[]:
            playerInRoom=False
        else:
            playerInRoom=True
        
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.
    intelUpdate()
    checkPlayer(percepcao)

    # Verifica se houve impacto e realize as compensações e anotações pertinentes
    if "I" in percepcao:
        mundo[posicao[0]][posicao[1]] = ["M"]
        toExplore = remove2([posicao[0],posicao[1]],toExplore)
        posicao = [ (posicao[0]-orientacao[0])%N , (posicao[1]-orientacao[1])%N ]
    # Se a movimentação foi bem-sucedida
    else:
        # Se não há F nem B, as casas adjacentes podem ser livres
        if not any(i in ["F","B"] for i in percepcao):
            setFree()
        else:
            # Se há F ou B, F e B associado à posição e W?/P? nas adjacências
            # pertinentes
            if "F" in percepcao:
                setPThreat("F")
            if "B" in percepcao:
                setPThreat("B")
        
        # Se U em percepção, a casa à frente está livre
        if "U" in percepcao:
            mundo[(posicao[0] + orientacao[0])%N][(posicao[1] + orientacao[1])%N]="L"
            toExplore.append([(posicao[0]+orientacao[0])%N,(posicao[1]+orientacao[1])%N])

        # Marca casas como vistadas e remove da lista de casas livres e não-visitadas
        if "V" not in mundo[posicao[0]][posicao[1]]:
            mundo[posicao[0]][posicao[1]].append("V")

            if [posicao[0],posicao[1]] in toExplore:
                toExplore.remove([posicao[0],posicao[1]])
        
        # Remove indicadores de ameaça da posição, pois se ela foi visitada
        # com sucesso, então não houve ameaça
        for i in ["W","W?","P","P?","M"]:
            mundo[posicao[0]][posicao[1]]=remove2(i,mundo[posicao[0]][posicao[1]])

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código

    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)


        pos = posicao
        ori = orientacao

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
                print("".join(mundo[i][j]),end="\t| ")
                
            print("\n"+"-"*(8*len(mundo)+1))
        print(toExplore)
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
        """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, playerInRoom
    pos = posicao
    ori = orientacao
    # Cria as orientações p/ esq e direita
    oriesq=deepcopy(ori)
    oridir=deepcopy(ori)
    if oriesq[0]==0:
        oriesq[1]=-oriesq[1]
    oriesq[0],oriesq[1] = oriesq[1],oriesq[0]
    if oridir[1]==0:
        oridir[0] = -oridir[0]
    oridir[0],oridir[1] = oridir[1],oridir[0]

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

    # Se houver jogador na sala, compartilha
    if playerInRoom==True:
        print("C")
        return "C"
    else:
        # Se houver um Wumpus nas adjacências, tenta matar ele
        if adjRoom("W")[0] and (nFlechas>0):
            if [(pos[0]+ori[0])%N,(pos[1]+ori[1])%N]==adjRoom("W")[1]:
                print("T")
                nFlechas=nFlechas-1
                return "T"

            elif [(pos[0]+oridir[0])%N,(pos[1]+oridir[1])%N]==adjRoom("W")[1]: 
                print("D")
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return "D"

            elif [(pos[0]+oriesq[0])%N,(pos[1]+oriesq[1])%N]==adjRoom("W")[1]: 
                print("E")
                if ori[0]==0:
                    ori[1] = -ori[1]
                ori[0],ori[1] = ori[1],ori[0]
                return "E"
            
            else:
                print("D")
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return "D"

        # Procura casas livres não visitadas
        elif freeNeighborRoom()[0]==True:
            if [(pos[0]+ori[0])%N,(pos[1]+ori[1])%N] == freeNeighborRoom()[1]:
                print("A")
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                return "A"
            elif [(pos[0]+oridir[0])%N,(pos[1]+oridir[1])%N] == freeNeighborRoom()[1]:
                print("D")
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return "D"

            elif [(pos[0]+oriesq[0])%N,(pos[1]+oriesq[1])%N] == freeNeighborRoom()[1]:
                print("E")
                if ori[0]==0:
                    ori[1] = -ori[1]
                ori[0],ori[1] = ori[1],ori[0]
                return "E"

            else:
                print("D")
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return "D"


        # Procura casas seguras para ir
        elif (adjRoom("V")[0]==True):
            if [(pos[0]+ori[0])%N,(pos[1]+ori[1])%N] == adjRoom("V")[1]:
                print("A")
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                return "A"
            elif [(pos[0]+oridir[0])%N,(pos[1]+oridir[1])%N] == adjRoom("V")[1]:
                print("D")
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return "D"
            
            elif [(pos[0]+oriesq[0])%N,(pos[1]+oriesq[1])%N] == adjRoom("V")[1]:
                print("E")
                if ori[0]==0:
                    ori[1] = -ori[1]
                ori[0],ori[1] = ori[1],ori[0]
                return "E"
        
            else:
                print("D")
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return "D"

        # Realiza um passo arriscado, o qual não é certamente mortal
        elif (toExplore==[]) and not (any(k in ["W","P","M"] for k in mundo[(pos[0]+ori[0])%N][(pos[1]+ori[1])%N])):
            print("A")
            pos[0] = (pos[0]+ori[0])%len(mundo)
            pos[1] = (pos[1]+ori[1])%len(mundo)
            return "A"

        else:
            print("D")
            if ori[1]==0:
                ori[0] = -ori[0]
            ori[0],ori[1] = ori[1],ori[0]
            return "D"

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo é uma pseudo-implementação, pois recebe
    # a ação através de uma pergunta dirigida ao usuário.
    # No código a ser entregue, você deve programar algum tipo
    # de estratégia para 
    acao = input("Digite a ação desejada (A/D/E/T/C): ")

    pos = posicao
    ori = orientacao
    if acao=="A":
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
    if acao=="E":
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
    if acao=="D":
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####
    
    assert acao in ["A","D","E","T","C"]
    return acao

# ♥
# iL
# oma
# et
# ue
