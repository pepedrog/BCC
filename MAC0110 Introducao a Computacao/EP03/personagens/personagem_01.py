#flag para depuração
global Start 

# flag para depuração
__DEBUG__ = False

global AlguemComigo  # booleano, se tem alguem na minha sala para compartilhar

# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global nFlechas
"""
Número de flechas que a personagem possui. Serve apenas para
consulta da personagem, pois o mundo mantém uma cópia "segura" dessa
informação (não tente inventar flechas...).
"""
global salasLivres  #lista de salas livres

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
global Path       #Path é um vetor de salas visitadas para um algoritmo que encontra caminhos(ou tenta)
global salaWumpus #Se sabemos a localização de um Wumpus queremos fazer pathing até a sua sala e atirar nele
global Instruction #Vetor de instruções retornadas pelo pathfinding
global infoCompartilhada #se temos informação compartilhada
global moving #booleano para indicar se estamos indo para uma sala (pathing)
global stuck #booleano, indica se estamos presos num ciclo

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, AlguemComigo, salasLivres, Start, Path, Instruction, moving, stuck, infoCompartilhada, salaWumpus
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mundo.append(linha)
    posicao = [0,0]
    orientacao = [1,0]
    AlguemComigo = False
    salasLivres = []     #guarda as salas livres
    Start = True         #flag para depuração
    Path = []
    Instruction = []
    moving = False
    stuck = False
    infoCompartilhada = False
    salaWumpus = []
    
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
    
    
    
    
    
    
    
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salasLivres, AlguemComigo, Start, infoCompartilhada
    pos = posicao
    ori = orientacao
    salaAlvo = []
    AlguemComigo = False
    if Start == True:
        vizinhos = []
        Start = False    



        
    if "I" in percepcao:
        mundo[pos[0]][pos[1]] = ["M"]
        if [pos[0], pos[1]] in salasLivres:      #volta uma sala com impacto
            salasLivres.remove([pos[0],pos[1]])
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)



    vizinhos = [ [(pos[0] + 1)%len(mundo),pos[1]],
                 [(pos[0] - 1)%len(mundo),pos[1]],
                 [pos[0],(pos[1] + 1)%len(mundo)],
                 [pos[0],(pos[1] - 1)%len(mundo)] ]
            
        
    if "B" not in percepcao and "F" not in percepcao and "I" not in percepcao:    #adiciona salas livres ao mapa e lista
        for viz in vizinhos:
            #print (viz)
            #print(mundo[viz[0]][viz[1]])
            if mundo[viz[0]][viz[1]] != ["W"] and mundo[viz[0]][viz[1]] != ["P"] and mundo[viz[0]][viz[1]] != ["V"] and mundo[viz[0]][viz[1]] != ["M"]:
                    mundo[viz[0]][viz[1]] = ["L"]
                    if [viz[0], viz[1]] not in salasLivres:
                        salasLivres.append([viz[0], viz[1]])     
                
    if "B" in percepcao:   #POÇO
        PocoAdjacenteConhecido = False
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] == ["P"]:
                PocoAdjacenteConhecido = True
        possivelpoco = 0
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] == [] or mundo[viz[0]][viz[1]] == ["P?"] or mundo[viz[0]][viz[1]] == ["W?"]:
                mundo[viz[0]][viz[1]] = ["P?"]
                flag0 = viz[0]
                flag1 = viz[1]
                possivelpoco = possivelpoco + 1
            
        if possivelpoco == 1 and not PocoAdjacenteConhecido:
            mundo[flag0][flag1] = ["P"]
            
    if "F" in percepcao:  #WUMPUS
        WumpusAdjacenteConhecido = False
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] == ["W"]:
                WumpusAdjacenteConhecido = True

        possivelWumpus = 0
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] == [] or mundo[viz[0]][viz[1]] == ["P?"] or mundo[viz[0]][viz[1]] == ["W?"]:
                mundo[viz[0]][viz[1]] = ["W?"]
                flag0 = viz[0]
                flag1 = viz[1]
                possivelWumpus = possivelWumpus + 1
            
        if possivelWumpus == 1 and not WumpusAdjacenteConhecido:
            mundo[flag0][flag1] = ["W"]
            salaWumpus.append([flag0 , flag1])
        
    if "U" in percepcao:  #reinicia os wumpus que sabemos onde estão, pra não atirar à toa
        for i in range(len(mundo)):
            for j in range(len(mundo[i])):
                if mundo[i][j] == ["W"]:
                    mundo[i][j] = ["W?"]
                    
    for i in percepcao:  #se isso for verdade tem alguem comigo
        if i != "U" and i != "F" and i != "B" and i != "I":
            AlguemComigo = True

        else:
            AlguemComigo = False
            
    if salasLivres != []:   
        salaAlvo = salasLivres[0]
    if salaWumpus != [] and nFlechas > 0:
        salaAlvo = salaWumpus[0]

    if pos == salaAlvo and salaAlvo != []:
        salasLivres.pop(0)  
        
    if salaAlvo != []:    
        FindPath(salaAlvo)  #encontramos uma sala livre/sala wumpus para onde queremos ir e abrimos o algoritmo de pathing

    
    if infoCompartilhada:   #usando informação compartilhada
        for i in range(len(mundoCompartilhado)):
            for j in range(len(mundoCompartilhado[i])):
                if (mundoCompartilhado[i][j] != []) and (mundo[i][j] != ["P"]) and (mundo[i][j] != ["W"]) or mundo[i][j] == []:
                    mundo[i][j] = mundoCompartilhado[i][j]
                    if mundo[i][j] == ["W"]:
                        salaWumpus.append([i,j])
                if mundo[i][j] == ["L"] and [i, j] not in salasLivres:
                    salasLivres.append([i, j])
        infoCompartilhada = False
    
    
    mundo[pos[0]][pos[1]] = ["V"] #visitamos uma sala
    
    #print("WUMPUS")
    #print(salaWumpus)
    #print("COMPARTIL.")
    #print(mundoCompartilhado)
    #print("MUNDO")
    #print(mundo)
    #print("SALASLIVRES")
    #print(salasLivres)
    #print("VIZINHOS")
    #print(vizinhos)

    if __DEBUG__:
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
                print("".join(mundo[i][j]),end="")
                print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####


def agir():
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salasLivres, AlguemComigo, Path, Instruction, moving, stuck, infoCompartilhada
    pos = posicao
    ori = orientacao
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """


    vizinhos = [ [(pos[0] + 1)%len(mundo),pos[1]],
                 [(pos[0] - 1)%len(mundo),pos[1]],
                 [pos[0],(pos[1] + 1)%len(mundo)],
                 [pos[0],(pos[1] - 1)%len(mundo)] ]



    if AlguemComigo:
        infoCompartilhada = True
        stuck = False
        return ("C")

    if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["W"] and nFlechas > 0:  #bala nele
        return ("T")
    
            
    if salasLivres == []:  #se não ha salas livres, rode no lugar e espere que alguem nos encontre
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
        return("D")
        
    if stuck:      #se estamos presos, rode no lugar e espere que alguem nos desprenda
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
        return("D")   
        
    if Instruction != []:  #vetor que executa o movimento de pathfinding
        instrução = Instruction[0] 
        if instrução == "up":
            if (pos[0]+ori[0])%len(mundo) == (pos[0] - 1)%len(mundo) and (mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] ==["L"] or mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["V"]):
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                Instruction.pop(0)
                return ("A")
            else:
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return("D")
        if instrução == "dir":
            if(pos[1]+ori[1])%len(mundo) == (pos[1]+1)%len(mundo) and (mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] ==["L"] or mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["V"]):
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                Instruction.pop(0)
                return("A")
            else:
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return("D")
        if instrução == "down":
            if (pos[0]+ori[0])%len(mundo) == (pos[0]+1)%len(mundo) and (mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] ==["L"] or mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["V"]):
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                Instruction.pop(0)
                return("A")
            else:
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return("D")
        if instrução == "esq":
            if ((pos[1]+ori[1])%len(mundo) == (pos[1]-1)%len(mundo)) and (mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] ==["L"] or mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["V"]):
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                Instruction.pop(0)
                return("A")
            else:
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return("D")
            
    if (mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] ==["L"]) or (mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["V"]):
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
        return("A")  #se tudo o mais falhar, mas der pra andar pra frente, ande pra frente
        
    if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] != ["L"]:
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
        return("D")  #entra no modo girapião se exaurirmos nossas opções
        


def FindPath(TargetRoom):       #essa função tenta achar caminhos da nossa posição ate uma sala alvo. Está feio e não sei se foge do escopo do EP mas quis tentar fazer :D (também não sei se funciona direito)
    global posicao, mundo, Path, Instruction
    stuck = False
    pos = posicao
    posIni = posicao
    minDistance = len(mundo)**2 #limite máximo de movimento
    
    PathFound = False
    #Distance = GetDistance(pos, TargetRoom, mundo)
    Path = []  #Path armazena as salas que visitamos no caminho
    Instruction = [] #Instruction é um vetor de instruções que é usado no módulo agir
    i = 0 #Se encontrarmos uma situação em que entramos em loop e não está coberta no algoritmo, temos esse contador para limitar o loop
    if pos == TargetRoom:
        return
    while not PathFound and i < len(mundo)**2:  #i limita o pathfinding pra nao travar tudo se houver problemas
        minDistance = len(mundo)**2
        if pos not in Path:
            Path.append(pos)
        FreeRoom = False
        BlockedRooms = 0
        vizinhos = [ [(pos[0] + 1)%len(mundo),pos[1]],
                     [(pos[0] - 1)%len(mundo),pos[1]],
                     [pos[0],(pos[1] + 1)%len(mundo)],
                     [pos[0],(pos[1] - 1)%len(mundo)] ]
        #print("1.")
        #print(pos)
        #print(TargetRoom)
        #print(vizinhos)
        #print(Path)
        #print(Distance)
        #print(Instruction)
        
        for viz in vizinhos:
            if (mundo[viz[0]][viz[1]] != ["L"] and mundo[viz[0]][viz[1]] != ["V"]) or viz in Path:
                BlockedRooms = BlockedRooms + 1
        
        #print(str(BlockedRooms) + " blocked")
                
        if BlockedRooms == 4 and pos == posIni:
            stuck = True
        
        
        if stuck:
            return
        
        if BlockedRooms == 4 and not stuck:
            if pos not in Path:
                Path.append(pos)
                pos = Path[len(Path - 2)]        
            if pos in Path:
                pos = Path[Path.index(pos) - 1]  #se chegamos num dead-end queremos voltar
            
            
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] == ["L"]:  #não é um dead-end
                FreeRoom = True
        
        if not FreeRoom:
            for viz in vizinhos:
                if mundo[viz[0]][viz[1]] == ["V"] and [viz[0],viz[1]] not in Path:
                            #print("REPORT" +str(viz), str(TargetRoom), str(mundo))
                            newDistance = GetDistance(viz, TargetRoom, mundo)
                            if newDistance < minDistance:
                                minDistance = newDistance
                                
            for viz in vizinhos:
                if mundo[viz[0]][viz[1]] == ["V"]:
                    if GetDistance(viz, TargetRoom, mundo) == minDistance and viz not in Path:
                       # print("viz " + str(viz))
                        Path.append(viz)
                        
                        if [(pos[0]-1)%len(mundo),pos[1]] == viz:  #vizinho acima
                            Instruction.append("up")
                            
                        elif [(pos[0]+1)%len(mundo),pos[1]]== viz:   #vizinho abaixo
                            Instruction.append("down")
                            
                        elif [pos[0],(pos[1]+1)%len(mundo)]== viz:   #vizinho à direita
                            Instruction.append("dir")
                            
                        elif[pos[0],(pos[1]-1)%len(mundo)]== viz:    #vizinho à esquerda
                            Instruction.append("esq")
                            
                        pos = viz
                        minDistance = 0
        if FreeRoom:       
            for viz in vizinhos:
                if mundo[viz[0]][viz[1]] == ["L"] and [viz[0],viz[1]] not in Path:
                            newDistance = GetDistance(viz, TargetRoom, mundo)
                            if newDistance < minDistance:
                                minDistance = newDistance
                                
            for viz in vizinhos:
                if mundo[viz[0]][viz[1]] == ["L"]:
                    if GetDistance(viz, TargetRoom, mundo) == minDistance and viz not in Path:
                       # print("viz " + str(viz))
                       
                        Path.append(viz)
                        
                        if [(pos[0]-1)%len(mundo),pos[1]] == viz:  #vizinho acima
                            Instruction.append("up")
                            
                        elif [(pos[0]+1)%len(mundo),pos[1]]== viz:   #vizinho abaixo
                            Instruction.append("down")
                            
                        elif [pos[0],(pos[1]+1)%len(mundo)]== viz:   #vizinho à direita
                            Instruction.append("dir")
                            
                        elif[pos[0],(pos[1]-1)%len(mundo)]== viz:    #vizinho à esquerda
                            Instruction.append("esq")
                            
                        pos = viz
                        minDistance = 0
                                    
        if pos == TargetRoom:
            PathFound = True
            Path = []
        #print("2.")
        #print(pos)
        #print(TargetRoom)
        #print(vizinhos)
        #print(Path)
        #print(Distance)
        #print(Instruction)
        i = i + 1
    return(Instruction)
        

            

    
    
def GetDistance(ThisRoom, TargetRoom, mundo):  #calcula distancias

    
    iDistance = min((TargetRoom[0] - ThisRoom[0])%len(mundo), (ThisRoom[0] - TargetRoom[0])%len(mundo))
    jDistance = min((TargetRoom[1] - ThisRoom[1])%len(mundo), (ThisRoom[1] - TargetRoom[1])%len(mundo))
    
    Distance = iDistance + jDistance
    
    return(Distance)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


