# flag para depuração
__DEBUG__ = False


# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global nFlechas
global mundoCompartilhado
global N
global mundo
global posicao
global orientacao

global alguemNaSala
global girouE
global andou
andou = False
girouE = False
girouD = False


global caminho
caminho = []
global target
target = []
global closetarget
closetarget = []
global alternativas
alternativas = []
global huntTheWumpus
huntTheWumpus = False


def adjacencias(pos):
    adjacentes = [ [(pos[0]+1)%N,pos[1]],
                [(pos[0]-1)%N,pos[1]],
                [pos[0],(pos[1]+1)%N],
                [pos[0],(pos[1]-1)%N] ]
    return adjacentes

def montaCaminho(target):
    matrizObjetivo = []
    instrucoes = []
    for g in range(N):
        matrizObjetivo.append([]*N)
    #matrizObjetivo[target]=1

    return instrucoes

def executaCaminho():
    return caminho.pop(0)

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
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]


def planejar(percepcao):

    percepcoes = ["F", "B", "I", "U"]
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, alguemNaSala, girouE, andou
    alguemNaSala = False #reseta
    backup = []


    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # elimine o teste abaixo quando tiver corrigido o bug de movimentação...
        if "I" in percepcao:
            print("Você bateu num muro e talvez não esteja mais na sala em que pensa estar...")
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        pos = posicao
        ori = orientacao
        mundo[pos[0]][pos[1]] = ["V"]
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

    # Atualiza posição
    pos = posicao
    ori = orientacao
    if andou:
        backup.append(pos[0]) 
        backup.append(pos[1])
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
        andou = False
    if girouE:
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
        girouE = False

    adjacentes = adjacencias(posicao) #calcula indices das casas adjacentes
    
    if "V" not in mundo[pos[0]][pos[1]]:
        mundo[pos[0]][pos[1]].append("V")
    if "L" not in mundo[pos[0]][pos[1]]:
        mundo[pos[0]][pos[1]].append("L") #se estou vivo, então essa sala está livre
 
    if not percepcao:
        for y in range(4):
            if "V" in mundo[adjacentes[y][0]][adjacentes[y][1]]:
                mundo[adjacentes[y][0]][adjacentes[y][1]] = ["V","L"]
            else:
                mundo[adjacentes[y][0]][adjacentes[y][1]] = ["L"]
    else:
        for a in percepcao:
            if a not in percepcoes:
                alguemNaSala = True
        
            if a == "I":
                mundo[posicao[0]][posicao[1]].append("M","V")  
                posicao[0],posicao[1] = backup[0],backup[1]

            if a == "B":
                mundo[pos[0]][pos[1]].append("B")
                for b in range(4):
                    if "P" and "P?" and "L" not in mundo[adjacentes[b][0]][adjacentes[b][1]]:
                        mundo[adjacentes[b][0]][adjacentes[b][1]].append("P?")
                    #A partir daqui verifica-se se, com essa nova informação, é possível concluir a localização de algum poço
                    adjacenteDoAdjacente = adjacencias(adjacentes[b])
                    contador = 0
                    for c in range(4):
                        if "B" in mundo[adjacenteDoAdjacente[c][0]][adjacenteDoAdjacente[c][1]]:
                            contador += 1

                    if contador == 4:
                        mundo[adjacentes[b][0]][adjacentes[b][1]].remove("P?")
                        mundo[adjacentes[b][0]][adjacentes[b][1]].append("P")


            if a == "F":
                mundo[pos[0]][pos[1]].append("F")
                for b in range(4):
                    if "W" and "W?" and "L" not in mundo[adjacentes[b][0]][adjacentes[b][1]]:
                        mundo[adjacentes[b][0]][adjacentes[b][1]].append("W?")
                    #A partir daqui verifica-se se, com essa nova informação, é possível concluir a localização de algum Wumpus
                    adjacenteDoAdjacente = adjacencias(adjacentes[b])
                    contador = 0
                    for c in range(4):
                        if "F" in mundo[adjacenteDoAdjacente[c][0]][adjacenteDoAdjacente[c][1]]:
                            contador += 1

                    if contador == 4:
                        mundo[adjacentes[b][0]][adjacentes[b][1]].remove("W?")
                        mundo[adjacentes[b][0]][adjacentes[b][1]].append("W")

            if a == "U":
                mundo[(posicao[0]+orientacao[0])%len(mundo)][(posicao[1]+orientacao[1])%len(mundo)].remove("W").append("L")


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """

    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, alguemNaSala, target, closetarget, girouE, andou, N

    acao = ""
    vizinhosIndex = adjacencias(posicao)
    vizinhos = [[],[],[],[]]
    frente = [(posicao[0]+orientacao[0])%len(mundo),(posicao[1]+orientacao[1])%len(mundo)]

    for j in range(4):
        vizinhos[j] = mundo[vizinhosIndex[j][0]][vizinhosIndex[j][1]]
    




    if alguemNaSala == True: #prioridade número um é obter mais informações
        acao = "C"

    elif mundo[frente[0]][frente[1]] == "W":
        acao = "T" #se houver certeza de Wumpus à frente, atirar

    elif caminho: #já estou seguindo um caminho
        #acao = executaCaminho()
        #return caminho.pop(0)
        z = 1

    
    else:
        if not closetarget:
            for d in range(4):
                #verifica as casas livres adjacentes e fica com a última delas. As outras são salvas numa lista para checar depois
                casa = vizinhos[d]
                #if "V" and "M" not in casa and "L" in casa:
                if "M" not in casa and "L" in casa:
                        if closetarget and closetarget not in alternativas:
                            alternativas.append(closetarget)
                        closetarget = vizinhosIndex[d]
        if closetarget: #destino potencial nas adjacências imediatas
            
             
            if closetarget != frente:
                acao = "E"
                girouE = True
            else:
                acao = "A"
                andou = True
                closetarget = []

        

        else: #nenhum destino em potencial localizado nas adjacências...
            if alternativas: #...porem ainda há pontos seguros inexplorados
                target = alternativas[0]


            else:
                #esgotadas as alternativas, consultar o mundo compartilhado
                for f in range(N):
                    for g in range(N):
                        if not mundo[f][g]:
                            mundo[f][g] = mundoCompartilhado[f][g]


    assert acao in ["A","D","E","T","C"]
    return acao
