# flag para depuração
__DEBUG__ = True

# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.
global nFlechas # númerod e flechas que a personagem possui
global mundoCompartilhado # da acesso a representação do mundo de outra personagem encontrada, matriz NxN

# Outras variáveis globais do módulo personagemNUSP
global N # dimensão do mundo
global mundo # representação do conhecimento próprio do mundo, cada sala (mundo[i][j]) quarda anotações 
global posicao # posição relativa no mundo, iniciada em [0,0]
global orientacao # junto com a posição, é usada para manter o conhecimento do mundo de forma correta
global acopanhando # booleano usado quando encontra-se outra personagem na mesma sala
global AA # guarda em uma lista as Ações Anteriores
#########################################################################################
######################################################################################### 
def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação.
    """
    global N, mundo, posicao, orientacao, AA
    N = tamanho # guarda o tamanho do mundo
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
    # inicia o histórico de ações anteriores
    AA = [0,0,0,0]
######################################################################################### 
######################################################################################### 
def planejar(percepcao):
    """ Função que recebe a percepção da sala atual e utiliza
        essa percepçao para atualizar o conhecimento de mundo.
        Possíveis percepções:
            "F" = fedor do Wumpus em alguma sala adjacente,
            "B" = brisa de um poço em sala adjacente, 
            "I" = impacto com um muro,
            "U" = urro do Wumpus morrendo e
            "Nome" = quando uma outra personagem é encontrada.
        Possíveis conhecimentos:
            "W/W?" = há ou pode haver um wumpus na sala,
            "P/P?" = há ou pode haver um poço na sala,
            "M" = há um muro na sala
            "L" = sala livre
            "V" = sala visitada
    """
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado
    global acompanhado, N
    # atualizando o conhecimento de mundo: "V" (visitado)
    mundo[posicao[0]][posicao[1]] = ["V"]
    # se sentimos um impacto ("I"), há um muro na sala
    if "I" in percepcao:
        mundo[(posicao[0])%N][(posicao[1])%N] = ["M"]
        # corrigindo a posição no mundo (se batemos em um muro, de fato, não nos movemos)
        posicao[0] = (posicao[0]-orientacao[0])%N
        posicao[1] = (posicao[1]-orientacao[1])%N
    # se sentimos uma brisa ("B"), as 4 salas adjacentes podem ter um poço ("P?")
    if "B" in percepcao:
        mundo[(posicao[0]+1)%N][posicao[1]] += ["P?"]
        mundo[(posicao[0]-1)%N][posicao[1]] += ["P?"]  
        mundo[posicao[0]][(posicao[1]-1)%N] += ["P?"]
        mundo[posicao[0]][(posicao[1]+1)%N] += ["P?"]
    # se sentimos um fedor ("F"), as 4 salas adjacentes podem ter um wumpus ("W?")
    if "F" in percepcao:
        mundo[(posicao[0]+1)%N][posicao[1]] += ["W?"]
        mundo[(posicao[0]-1)%N][posicao[1]] += ["W?"]  
        mundo[posicao[0]][(posicao[1]-1)%N] += ["W?"]
        mundo[posicao[0]][(posicao[1]+1)%N] += ["W?"]
    # se não percebemos brisa nem fedor, as 4 salas adjacentes estão livres
    if ("B" not in percepcao) and ("F" not in percepcao):
        mundo[(posicao[0]+1)%N][posicao[1]] += ["L"]
        mundo[(posicao[0]-1)%N][posicao[1]] += ["L"]  
        mundo[posicao[0]][(posicao[1]-1)%N] += ["L"]
        mundo[posicao[0]][(posicao[1]+1)%N] += ["L"]
    # se um wumpus foi morto, devemos considerar que qualquer sala
    # com o indicador "W" pode talvez não contenha mais o wumpus ("W?")
    if "U" in percepcao:
        mundo = morte_de_um_wumpus(mundo)   
    # confere se há outras personagens na sala, 
    # essa informação será usada na função agir()
    acompanhado = mais_personagens_na_sala(percepcao) 
    # atualizamos as informações de 'mundo' acrescentando
    # qualquer informação nova de 'mundoCompartilhado'
    mundo = mescla_mundos(mundo,mundoCompartilhado)
    # as funções acima podem ter colocado informações descartáveis
    # no conhecimento de mundo, vamos "limpar" essas informações
    mundo = limpa_mundo(mundo)
    #####################################################################################
    # DEBUG para imprimir a persepção e o conhecimento de mundo na tela
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        print("Mundo conhecido pela personagem:")
        for i in range(N):
            for j in range(len(mundo[0])):
                if posicao==[i,j]:
                    if orientacao==[0,-1]:
                        print("<",end="")
                    print("X",end="")
                    if orientacao==[0,1]:
                        print(">",end="")
                    if orientacao==[1,0]:
                        print("v",end="")
                    if orientacao==[-1,0]:
                        print("^",end="")
                print("".join(mundo[i][j]),end="\t| ")
            print("\n"+"-"*(8*N+1))
#########################################################################################
#########################################################################################
def mescla_mundos(mundo,mundoCompartilhado):
    """ adiciona as informações contidas no 'mundoCompartilhado' em 'mundo'
    """
    global N
    for linha in range(N):
        for coluna in range(N):
            mundo[linha][coluna] = mundo[linha][coluna] + mundoCompartilhado[linha][coluna]
    return mundo
#########################################################################################
#########################################################################################
def mais_personagens_na_sala(percep):
    """ confere se existem outras personagens na mesma sala
    """
    personagens = percep[:]
    if "B" in personagens: personagens.remove("B")
    if "F" in personagens: personagens.remove("F")
    if "I" in personagens: personagens.remove("I")
    if "U" in personagens: personagens.remove("U")
    if len(personagens) == 0:
        return False
    else:
        return True
#########################################################################################
#########################################################################################
def morte_de_um_wumpus(mundo):
    """ se um wumpus morreu devemos reconsiderar conclusões prévias (W -> W?)
    """
    global N
    for linha in range(N):
        for coluna in range(N):
            if "W" in mundo[linha][coluna]:
                mundo[linha][coluna].remove("W")
                mundo[linha][coluna].append("W?")
    return mundo
#########################################################################################
#########################################################################################
def limpa_mundo(mundo):
    """ chama a função limpa_sala() em todas as salas do mundo conhecido
    """
    global N
    for linha in range(N):
        for coluna in range(N):
            mundo[linha][coluna] = limpa_sala(mundo[linha][coluna])
    return mundo
#########################################################################################
#########################################################################################
def limpa_sala(sala):
    """ limpa a sala de informações erradas e/ou irrelevantes
    """
    sala_limpa = []
    # primeiro elina itens repetidos
    for item in sala:
        if item not in sala_limpa:
            sala_limpa.append(item)
    # agora remove itens determinados considerando uma hierarquia entre eles
    if "L" in sala_limpa and "M" in sala_limpa:
        sala_limpa.remove("L")
    if "M" in sala_limpa:
        sala_limpa = ["M"]
    if "V" in sala_limpa:
        sala_limpa = ["V"]
    if "P" in sala_limpa and "P?" in sala_limpa:
        sala_limpa.remove("P?")
    if "W" in sala_limpa and "W?" in sala_limpa:
        sala_limpa.remove("W?")
    if "L" in sala_limpa and "P?" in sala_limpa:
        sala_limpa.remove("P?")
    if "L" in sala_limpa and "P" in sala_limpa:
        sala_limpa.remove("P")
    if "L" in sala_limpa and "W?" in sala_limpa:
        sala_limpa.remove("W?")
    if "L" in sala_limpa and "W" in sala_limpa:
        sala_limpa.remove("W")
    return sala_limpa
#########################################################################################
#########################################################################################
def agir():
    """ Nessa função a personagem usa o seu conhecimento do mundo
        para decidir e executar (devolver) uma ação.
        As possíveis ações são:
        "A" = Andar, 
        "D" = girar à Direita, 
        "E" = girar à Esquerda,
        "T" = aTirar (no wumpus) e 
        "C" = Compartilhar (informações com outra personagem).
    """
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado
    global acompanhado, AA, N
    pos = posicao
    ori = orientacao
    frente = (pos[0]+ori[0])%N , (pos[1]+ori[1])%N # posição a frente da personagem
    #####################################################################################
    # 1) casos especiais: outra personagem na mesma sala ou wumpus em sala adjacente ####
    #####################################################################################
    # caso exista alguma personagem na sala, optar por compartilhar informações
    if acompanhado:
        return "C"
    # matar o wumpus caso ele esteja em uma sala adjacente
    if item_em_volta("W",mundo,posicao) and nFlechas > 0:
        if "W" in mundo[frente[0]][frente[1]]:  
            return "T"
        else:
            if ori[0]==0:
                ori[1] = -ori[1]
            ori[0],ori[1] = ori[1],ori[0]
            return "E"
    #####################################################################################
    # 2) casos de movimentação da personagem ############################################
    #####################################################################################
    # booleano que vai definir se a personagem tenta ações arriscadas 
    if num_salas_livres(mundo) == 0:
        arriscar = True # se não houver nenhuma sala livre conhecida
    else:
        arriscar = False # se houver alguma sala livre conhecida
    if item_em_volta("L",mundo,posicao):
        volta_L = True
    else:
        volta_L = False
    #####################################################################################
    if arriscar == False:
        # 1) passo para frente (se for seguro)
        if "L" in mundo[frente[0]][frente[1]]:
            acao = "A"
        # 2) se tiver salas livres em volta, girar até encontra-la
        elif volta_L and (AA[len(AA)-3] != "E" or AA[len(AA)-2] != "E" or AA[len(AA)-1] != "E"):
            acao = "E"
        # 3) passo para frente se for uma casa visitada
        elif "V" in mundo[frente[0]][frente[1]]:
            acao = "A"
        # 4) girar até achar uma sala visitada
        elif AA[len(AA)-5] != "E" or AA[len(AA)-6] != "E" or AA[len(AA)-7] != "E":
            acao = "E"
        # 5) evitar becos com muros por exemplo
        else:
            acao = "E"
    if arriscar == True:
        if not "P" in mundo[frente[0]][frente[1]] \
        and not "W" in mundo[frente[0]][frente[1]]:
            # 1) arriscar um possível poço se não há possibilidade de um wumpus
            if "P?" in mundo[frente[0]][frente[1]] \
            and not "W?" in mundo[frente[0]][frente[1]]:
                acao = "A"
            # 2) arriscar um possível wumpus se não há possibilidade de um poço
            elif "W?" in mundo[frente[0]][frente[1]] \
            and not "P?" in mundo[frente[0]][frente[1]]:
                acao = "A"
            # 3) arriscar um possível poço onde há chance de ter um wumpus também
            elif "P?" in mundo[frente[0]][frente[1]]:
                acao = "A"
            # 4) arriscar um possível wumpus onde há chance de ter um poço também
            elif "W?" in mundo[frente[0]][frente[1]]:
                acao = "A"
            # 5) se caiu em um beco
            elif "V" in mundo[frente[0]][frente[1]] and \
            ( (AA[len(AA)-4] != "E" or AA[len(AA)-3] != "E" or AA[len(AA)-2] != "E" or AA[len(AA)-1] != "E") ):
                acao = "A"
            # 6) girar            
            else:
                acao = "E"
        else:
            acao = "E"
    #####################################################################################
    # atualiza a posição no mundo
    if acao=="A":
        pos[0] = (pos[0]+ori[0])%N
        pos[1] = (pos[1]+ori[1])%N
    if acao=="E":
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
    if acao=="D":
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
    AA.append(acao) #registra as Ações Anteriores
    assert acao in ["A","D","E","T","C"]
    return acao
#########################################################################################
#########################################################################################
def item_em_volta(item,mundo,posicao):
    """ confere se o item está em uma sala adjacente
    """
    global N
    if item in mundo[(posicao[0]-1)%N][posicao[1]]:
        return True
    if item in mundo[(posicao[0]+1)%N][posicao[1]]:
        return True
    if item in mundo[posicao[0]][(posicao[1]-1)%N]:
        return True
    if item in mundo[posicao[0]][(posicao[1]+1)%N]:
        return True
    return False
#########################################################################################
#########################################################################################
def num_salas_livres(mundo_conhecido):
    """ conta o número de salas livres no mundo
    """
    global N
    numero_de_salas_livres = 0
    for linha in range(N):
        for coluna in range(N):
            if "L" in mundo_conhecido[linha][coluna]:
                numero_de_salas_livres +=1
    return numero_de_salas_livres
