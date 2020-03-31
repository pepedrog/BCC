__DEBUG__ = False

global compartilhar
"""
Informa se existe outra personagem na mesma sala que a nossa personagem.
"""

global nFlechas
global mundoCompartilhado
global N
global mundo
global posicao
global orientacao


def inicializa(tamanho):
    global N, mundo, posicao, orientacao
    N = tamanho
    mundo = []
    for i in range(N):
        mundo.append([[]]*N)
    posicao = [0,0]
    orientacao = [1,0]


def planejar(percepcao):
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, compartilhar

    # atualiza a percepção de mundo da personagem usando informações compartilhadas.
    for i in range(len(mundo)):
        for j in range(len(mundo)):
            # se as informações compartilhadas não conterem interrogação, iremos atualizar a nossa percepção de mundo.
            if mundo[i][j] in [[],["P?"],["W?"],["P?","W?"]] and not mundoCompartilhado[i][j] in [[],["P?"],["W?"],["P?","W?"]]:
                if mundoCompartilhado[i][j] == ["L","V"]: mundo[i][j] = ["L"]
                else: mundo[i][j] = mundoCompartilhado[i][j]
            # se existir na nossa representação de mundo alguma sala com a marcação 'P?W?' e a
            # informação compartilhada conter apenas 'P?' ou 'W?' iremos atualizar a percepção.
            if mundo[i][j] == ["P?","W?"] and mundoCompartilhado[i][j] in [["P?"],["W?"]]:
                mundo[i][j] = mundoCompartilhado[i][j]
            # atualiza as casas que contém muros.
            if mundo[i][j] == ["L"] and mundoCompartilhado[i][j] == ["M"]:
                mundo[i][j] = mundoCompartilhado[i][j]

    pos = posicao
    ori = orientacao
    vizinhos = [ [(pos[0]+1)%len(mundo),pos[1]],
                 [(pos[0]-1)%len(mundo),pos[1]],
                 [pos[0],(pos[1]+1)%len(mundo)],
                 [pos[0],(pos[1]-1)%len(mundo)] ]
    
    # marca a sala atual como visitada.   
    mundo[pos[0]][pos[1]] = ["L","V"]

    # se houver alguma percepção diferente das habituais, podemos concluir que há outra
    # personagem na mesma sala e portanto iremos compartilhar informações imediatamente.
    compartilhar = False
    for elemento in percepcao:
        if not elemento in ["B","F","I","U"]: compartilhar = True

    # as variáveis abaixo contam quantas marcações do tipo "W?" e do tipo "P?" existem nas adjacências da sala
    # atual. Se existir apenas uma marcação, e houver a devida percepção, então podemos concluir com certeza que
    # "W?" = "W" e "P?" = "P".
    contador_w_interrogação = 0    
    contador_p_interrogação = 0
    
    for viz in vizinhos:
        # marca as salas adjacentes à sala atual com ["P?","W?"] caso "B" e "F" estejam na percepcao
        # e somente se as casas adjacentes não possuírem nenhuma outra informação armazenada.
        if "B" in percepcao and "F" in percepcao:
            if mundo[viz[0]][viz[1]] in [[],["P?"],["W?"],["P?","W?"]]: mundo[viz[0]][viz[1]] = ["P?","W?"]
            if mundo[viz[0]][viz[1]] in [["W?"],["P?","W?"]]: contador_w_interrogação += 1            
            if mundo[viz[0]][viz[1]] in [["P?"],["P?","W?"]]: contador_p_interrogação += 1
            
        # marca as salas adjacentes à sala atual com 'W?' caso "F" esteja na percepcao, e somente
        # se as casas adjacentes não possuírem nenhuma outra informação armazenada.            
        if "F" in percepcao and not "B" in percepcao:
            if mundo[viz[0]][viz[1]] in [[],["P"],["P?"],["W?"],["P?","W?"]]: mundo[viz[0]][viz[1]] = ["W?"]
            if mundo[viz[0]][viz[1]] in [["W?"],["P?","W?"]]: contador_w_interrogação += 1
            
        # marca as salas adjacentes à sala atual com 'P?' caso "B" esteja na percepcao, e somente
        # se as casas adjacentes não possuírem nenhuma outra informação armazenada.
        if "B" in percepcao and not "F" in percepcao:
            if mundo[viz[0]][viz[1]] in [[],["W"],["P?"],["W?"],["P?","W?"]]: mundo[viz[0]][viz[1]] = ["P?"]
            if mundo[viz[0]][viz[1]] in [["P?"],["P?","W?"]]: contador_p_interrogação += 1            
            
        # se não há nenhuma percepção do tipo 'B', 'F' ou 'I' na sala atual, podemos concluir
        # que as salas adjacentes são livres ou são muros. Será marcada com 'L', pois se for
        # de fato um muro, posteriormente essa marcação sera alterada para 'M', quando a nossa
        # personagem tentar entrar nessa sala.
        if not "B" in percepcao and not "F" in percepcao and not "I" in percepcao:
            if mundo[viz[0]][viz[1]] in [[],["P"],["W"],["P?"],["W?"],["P?","W?"]]: mundo[viz[0]][viz[1]] = ["L"]

    # o trecho abaixo faz a substituição das marcações, quando já possuirmos a certeza do que há nas salas.
    if contador_w_interrogação == 1:
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] in [["W?"],["P?","W?"]]: mundo[viz[0]][viz[1]] == ["W"]
    if contador_p_interrogação == 1:
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] in [["P?"],["P?","W?"]]: mundo[viz[0]][viz[1]] == ["P"]        
            
    # marca a sala à frente com 'M' caso seja percebido um impacto 'I', e retorna o personagem
    # para a posição em que ele estava antes de tentar andar em direção ao muro.
    if "I" in percepcao:
        mundo[pos[0]][pos[1]] = ["M"]
        pos[0],pos[1] = (pos[0]-ori[0])%len(mundo),(pos[1]-ori[1])%len(mundo)
    
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, compartilhar
    pos,ori = posicao,orientacao
    vizinhos = [ [(pos[0]+1)%len(mundo),pos[1]],
                 [(pos[0]-1)%len(mundo),pos[1]],
                 [pos[0],(pos[1]+1)%len(mundo)],
                 [pos[0],(pos[1]-1)%len(mundo)] ]

    # quando for possível compartilhar informações, isso será feito imediatamente.
    if compartilhar:
        return "C"

    # se ainda houverem flechas, checa se existe algum Wumpus nas adjacências da casa atual, e prepara o ataque.
    if nFlechas > 0:
        for viz in vizinhos:
            if mundo[viz[0]][viz[1]] == ["W"]:
                while mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] != ["W"]:
                    # a personagem irá virar-se para a direita até que a casa imediatamente à frente
                    # contenha um Wumpus. Quando isso acontecer, a flecha será disparada.
                    if ori[1]==0:
                        ori[0] = -ori[0]
                    ori[0],ori[1] = ori[1],ori[0]
                    return "D"
                return "T"

    # procura por salas livres que ainda não foram visitadas, e entra nelas. (não pense obscenidades!)
    for viz in vizinhos:
        if mundo[viz[0]][viz[1]] == ["L"]:
            # se existir alguma sala livre nas adjacências da sala atual, vamos nos dirigir para lá.
            while mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] != ["L"]:
                # vamos virar para a direita até que a sala livre esteja na nossa frente.
                # quando isso acontecer, andamos em direção a ela.
                if ori[1]==0:
                    ori[0] = -ori[0]
                ori[0],ori[1] = ori[1],ori[0]
                return "D"
            # passo em direção à sala livre.
            pos[0] = (pos[0]+ori[0])%len(mundo)
            pos[1] = (pos[1]+ori[1])%len(mundo)            
            return "A"     

    # Se não existirem salas livres nas adjacências da sala atual, nossa personagem irá voltar a casas já visitadas
    # a procura de novas salas livres. Caso não haja nenhuma, a personagem irá andar apenas nas casas já conhecidas,
    # até que outra personagem compartilhe informações. Caso a casa imetiatamente à frente da nossa personagem estiver
    # marcada com 'V', ela irá se dirigir para lá.
    if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["L","V"]:
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
        return "A"

    # caso não esteja, ela irá se virar para a direita, até que seja possível andar.
    else:
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
        return "D"
