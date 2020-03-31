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
    global salasLivres, haPersonagemNaSala, indoParaSalaLivre, salaLivreAtual
    global caminhoAteSalaLivre, matrizMarcada, deveArriscar
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
    # salas livres e não visitadas
    salasLivres = []
    # indicada a presença de outra personagem
    haPersonagemNaSala = False
    # indica se está indo para uma sala livre
    indoParaSalaLivre = False
    # sala livre sendo procurada no momento
    # inicializada com posição inicial
    salaLivreAtual = [0, 0]
    # caminho até a sala livre
    caminhoAteSalaLivre = []
    # matriz marcada com as distâncias de cada sala até uma sala livre
    # inicializada com -1 em todas as salas
    matrizMarcada = []
    for i in range(N):
        matrizMarcada.append([])
        for j in range(N):
            matrizMarcada[i].append(-1)
    # indica se deve arriscar ir numa sala desconhecida
    deveArriscar = False

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado
    global salasLivres, haPersonagemNaSala, deveArriscar
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código

    pos = posicao
    ori = orientacao

    # Se houver uma percepção diferente de F/B/I/U significa
    # que há uma personagem na sala.
    for p in percepcao:
        if p != "F" and p != "B" and p != "I" and p != "U":
            haPersonagemNaSala = True

    # Se houver salas livres e não visitadas, a personagem não deve se arriscar.
    if len(salasLivres) != 0:
        deveArriscar = False

    # Se houver um impacto, a personagem é "recolocada" (na verdade ela não
    # se moveu realmente, apenas na sua repesentação do mundo) na posição anterior.
    # Como houve impacto, a sala possui um muro e se esta estiver
    # na lista de salas livres e não visitadas, ela é removida.
    if "I" in percepcao:
        mundo[pos[0]][pos[1]] = ["M"]
        muro = [pos[0], pos[1]]
        if muro in salasLivres:
            salasLivres.remove(muro)
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)

    # Salas adjacentes
    baixo = mundo[(pos[0]+1)%N][pos[1]]
    cima = mundo[(pos[0]-1)%N][pos[1]]
    direita = mundo[pos[0]][(pos[1]+1)%N]
    esquerda = mundo[pos[0]][(pos[1]-1)%N]


    # Marca as salas adjacentes de acordo com a percepção.
    if not("B" in percepcao or "F" in percepcao or "I" in percepcao):
        if not("L" in baixo or "V" in baixo or "M" in baixo):
            mundo[(pos[0]+1)%N][pos[1]] = ["L"]
            salasLivres.append([(pos[0]+1)%N, pos[1]])
        if not("L" in cima or "V" in cima or "M" in cima):
            mundo[(pos[0]-1)%N][pos[1]] = ["L"]
            salasLivres.append([(pos[0]-1)%N, pos[1]])
        if not("L" in direita or "V" in direita or "M" in direita):
            mundo[pos[0]][(pos[1]+1)%N] = ["L"]
            salasLivres.append([pos[0], (pos[1]+1)%N])
        if not("L" in esquerda or "V" in esquerda or "M" in esquerda):
            mundo[pos[0]][(pos[1]-1)%N] = ["L"]
            salasLivres.append([pos[0], (pos[1]-1)%N])
    
    if "F" in percepcao:
        if not("W?" in baixo or "P" in baixo or "W" in baixo or "L" in baixo or "V" in baixo or "M" in baixo):
            baixo.append("W?")
        if not("W?" in cima or "P" in cima or "W" in cima or "L" in cima or "V" in cima or "M" in cima):
            cima.append("W?")
        if not("W?" in direita or "P" in direita or "W" in direita or "L" in direita or "V" in direita or "M" in direita):
            direita.append("W?")
        if not("W?" in esquerda or "P" in esquerda or "W" in esquerda or "L" in esquerda or "V" in esquerda or "M" in esquerda):
            esquerda.append("W?")

    if "B" in percepcao:
        if not("P?" in baixo or "P" in baixo or "W" in baixo or "L" in baixo or "V" in baixo or "M" in baixo):
            baixo.append("P?")
        if not("P?" in cima or "P" in cima or "W" in cima or  "L" in cima or "V" in cima or "M" in cima):
            cima.append("P?")
        if not("P?" in direita or "P" in direita or "W" in direita or "L" in direita or "V" in direita or "M" in direita):
            direita.append("P?")
        if not("P?" in esquerda or "P" in esquerda or "W" in esquerda or "L" in esquerda or "V" in esquerda or "M" in esquerda):
            esquerda.append("P?")

    # Se a sala atual não tiver sido visitada marca como visitada.
    # Se houver "W?" ou "P?" na sala, sobrescreve os valores com "V"
    # (pois não há uma ameaça de fato).
    if "V" not in mundo[pos[0]][pos[1]]:
        if "W?" in mundo[pos[0]][pos[1]] or "P?" in mundo[pos[0]][pos[1]]:
            mundo[pos[0]][pos[1]] = ["V"]
        else:
            mundo[pos[0]][pos[1]].append("V")

    # Verifica se há dados compartilhados.
    # Sempre confia na informação compartilhada.
    for i in range(len(mundoCompartilhado)):
        for j in range(len(mundoCompartilhado[0])):
            casaCompartilhada = mundoCompartilhado[i][j]
            casaMeuMundo = mundo[i][j]
            sala = [i, j]

            #Checa se a sala está livre e não foi visitada ainda.
            if (sala not in salasLivres and "L" in casaCompartilhada
                and "V" not in casaMeuMundo):
                mundo[i][j] = ["L"]
                salasLivres.append(sala)
            if "P" in casaCompartilhada:
                mundo[i][j] = ["P"]
            if "W" in casaCompartilhada:
                mundo[i][j] = ["W"]    
            if "M" in casaCompartilhada:
                mundo[i][j] = ["M"]

    # Caso a sala atual esteja na lista de salas livres e
    # não visitadas, ela é removida (pois acabou de ser visitada).
    salaAtual = [pos[0],pos[1]]
    if salaAtual in salasLivres:
        salasLivres.remove(salaAtual)
    print("Salas livres e não visitadas:", salasLivres)
    
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        pos = posicao
        ori = orientacao

        x = pos[0]
        y = pos[1]
        print("linha =", pos[0], ", coluna = ", pos[1])

        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada

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
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado
    global salasLivres, haPersonagemNaSala, indoParaSalaLivre, salaLivreAtual
    global caminhoAteSalaLivre, matrizMarcada, deveArriscar
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

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo é uma pseudo-implementação, pois recebe
    # a ação através de uma pergunta dirigida ao usuário.
    # No código a ser entregue, você deve programar algum tipo
    # de estratégia para 

    # ATENÇÃO: a atualizacao abaixo está errada!!!
    # Não checa se o movimento foi possível ou não... isso só dá para
    # saber quando chegar uma percepção nova (a percepção "I"
    # diz que o movimento anterior não foi possível).

    # ###########################################################
    # ###########################################################
    # ################### E S T R A T É G I A ###################
    # ###########################################################
    # ###########################################################
    # A personagem tenta acessar todas as salas livres e
    # não visitadas. A sala livre escolhida é sempre a primeira
    # da lista, não importando se está mais longe do que as outras.
    # Caso haja salas livres mas não seja possível acessá-las
    #(pois o caminho é desconhecido), a personagem apenas anda
    #(se houver um muro na frente, ela gira para a direita).
    # A personagem não atira nos Wumpus.
    # ###########################################################

    pos = posicao
    ori = orientacao

    # A prioridade é compartilhar informação
    if haPersonagemNaSala:
        haPersonagemNaSala = False
        return "C"
    else:
        if not indoParaSalaLivre and not deveArriscar:
            # Marca a matriz com 0s e -1s
            # 0: sala visitada
            # -1: sala desconhecida
            for i in range(N):
                for j in range(N):
                    casa = mundo[i][j]
                    if "V" in casa or "L" in casa:
                        matrizMarcada[i][j] = 0
                    else:
                        matrizMarcada[i][j] = -1
            
            if len(salasLivres) == 0:
                deveArriscar = True
                proxPos = [(pos[0]+ori[0])%len(mundo), (pos[1]+ori[1])%len(mundo)]
                if "M" in mundo[proxPos[0]][proxPos[1]]:
                    # Escolha arbitrária de rotação caso haja um muro
                    acao = "D"
                else:
                    acao = "A"
            else:
                sala = salasLivres[0]
                salaLivreAtual[0] = sala[0]
                salaLivreAtual[1] = sala[1]
                matrizMarcada = marcarMatriz(matrizMarcada, N, N, salaLivreAtual)
                caminhoAteSalaLivre = acharCaminho(matrizMarcada, N, N, salaLivreAtual, pos)

                # Contador para indicar quantas vezes a lista
                # foi empurrada. Se o número de empurrões for igual
                # ao tamanho da lista, significa que nenhuma sala livre
                # é acessível (a lista inteira ja foi "percorrida").
                cont = 0

                # Pega sempre a primeira sala livre não visitada.
                # Se não for possível ir até la, ela é empurrada
                # para o fim da lista e se puder ir, quando chegar lá,
                # ela é removida da lista (pois foi visitada).
                while len(caminhoAteSalaLivre) == 0:
                    salasLivres = empurrarElementos(salasLivres)
                    sala = salasLivres[0]
                    salaLivreAtual[0] = sala[0]
                    salaLivreAtual[1] = sala[1]
                    matrizMarcada = marcarMatriz(matrizMarcada, N, N, salaLivreAtual)
                    caminhoAteSalaLivre = acharCaminho(matrizMarcada, N, N, salaLivreAtual, pos)
                    cont += 1
                    if cont == len(salasLivres):
                        indoParaSalaLivre = False
                        deveArriscar = True
                        break

                if not deveArriscar: 
                    indoParaSalaLivre = True
                    caminho = caminhoAteSalaLivre[0]
                    acao = decidirAcao(pos, caminhoAteSalaLivre, N, ori, salaLivreAtual)

                    # Se o caminho seguinte for a sala livre procurada
                    # e a ação for andar, significa que a personagem chegou lá
                    if caminho == salaLivreAtual and acao == "A":
                        indoParaSalaLivre = False
                else:
                    proxPos = [(pos[0]+ori[0])%len(mundo), (pos[1]+ori[1])%len(mundo)]
                    if "M" in mundo[proxPos[0]][proxPos[1]]:
                        acao = "D"
                    else:
                        acao = "A"
                    
        # Indo para uma sala livre (não devo me arriscar)
        elif indoParaSalaLivre:
            caminho = caminhoAteSalaLivre[0]
            acao = decidirAcao(pos, caminhoAteSalaLivre, N, ori, salaLivreAtual)
            if caminho == salaLivreAtual  and acao == "A":
                indoParaSalaLivre = False

        # Sem salas livres, devo me arriscar
        else:
            proxPos = [(pos[0]+ori[0])%len(mundo), (pos[1]+ori[1])%len(mundo)]
            if "M" in mundo[proxPos[0]][proxPos[1]]:
                acao = "D"
            else:
                acao = "A"

        # Mexe na personagem de acordo com a ação.
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

def empurrarElementos(lista):
    """ Empurra os elementos da lista dada para a esquerda

    """
    
    L = []
    T = len(lista)
    for i in range(T):
        L.append(lista[(i+1)%T])

    return L

def decidirAcao(posAtual, caminho, N, ori, salaLivre):
    """ Decide a próxima ação baseado na orientação e na
        sala adjacente

    """
    global indoParaSalaLivre

    # Diferença entre as filas da sala atual e da sala adjacente.
    salaAdjacente = caminho[0]
    difL1 = (posAtual[0] - salaAdjacente[0])%N
    difL2 = (salaAdjacente[0] - posAtual[0])%N
    difLinha = min(difL1, difL2)

    difC1 = (posAtual[1] - salaAdjacente[1])%N
    difC2 = (salaAdjacente[1] - posAtual[1])%N
    difColuna = min(difC1, difC2)
    
    # Deixar as duas comparações abaixo é redundante, pois
    # so há diferença ou na coluna ou na linha (na teoria),
    # mas é melhor prevenir do que remediar.

    # As direções são relativas ao usuário e não à personagem.
    # Esquerda ou direita
    if difLinha == 0 and difColuna == 1:

        # Se há diferença nas colunas, checa se a sala
        # esta à esquerda ou à direita.
        # Se estiver à direita, ao somar 1 à coluna atual
        # deve resultar na coluna da direita (módulo N).
        # Mesma explicação para as outras direções.
        
        # Direita
        if (posAtual[1] + 1)%N == salaAdjacente[1]:
            # Virado para a sala
            if ori == [0, 1]:
                if (caminho[0] == salaLivre):
                    indoParaSalaLivre = False
                caminho.remove(caminho[0])
                return "A"

            # Virado para baixo
            elif ori == [1, 0]:
                return "E"

            # Virada para cima ou para a esquerda
            else:
                return "D"
            # A orientação para outras direções segue o mesmo racioncínio.

        # Esquerda
        else:
            if ori == [0, -1]:
                if (caminho[0] == salaLivre):
                    indoParaSalaLivre = False
                caminho.remove(caminho[0])
                return "A"
            elif ori == [1, 0]:
                return "D"
            else:
                return "E"
            
    # Cima ou baixo
    else:
        # Baixo
        if (posAtual[0] + 1)%N == salaAdjacente[0]:
            if ori == [1, 0]:
                if (caminho[0] == salaLivre):
                    indoParaSalaLivre = False
                caminho.remove(caminho[0])
                return "A"
            elif ori == [0, -1]:
                return "E"
            else:
                return "D"
        # Cima
        else:
            if ori == [-1, 0]:
                if (caminho[0] == salaLivre):
                    indoParaSalaLivre = False
                caminho.remove(caminho[0])
                return "A"
            elif ori == [0, -1]:
                return "D"
            else:
                return "E"

def acharCaminho(M, linhas, colunas, posLivre, posPersonagem):
    """ Acha o menor caminho até a posição livre

    """
    
    aP = posPersonagem[0]
    bP = posPersonagem[1]
    aL = posLivre[0]
    bL = posLivre[1]

    # Se a posição da personagem estiver marcada com 0
    # (após a marcação das distâncias), significa que
    # é impossível acessar a sala livre partindo dessa posição.
    if M[aP][bP] == 0:
        return []

    caminho = []
    casaAtual = [aP, bP]
    casaLivre = [aL, bL]
    while casaAtual != casaLivre:
        x = casaAtual[0]
        y = casaAtual[1]
        
        posBaixo = [(x+1)%linhas, y]
        posCima = [(x-1)%linhas, y]
        posDireita = [x, (y+1)%colunas]
        posEsquerda = [x, (y-1)%colunas]

        # Pega os valores das casas adjacentes
        # e compara para verificar qual está mais
        # perto da posição livre.
        # Se a casa adjacente tiver valor -1,
        # ela recebe o número de casas da matriz
        # pois o maior caminho é aquele em que se
        # percorre a matriz inteira e portanto
        # qualquer outro caminho diferente é menor que este.
        casaBaixo = M[posBaixo[0]][posBaixo[1]]
        if casaBaixo == -1:
            casaBaixo = len(M)*len(M[0])    

        casaCima = M[posCima[0]][posCima[1]]
        if casaCima == -1:
            casaCima = len(M)*len(M[0])

        casaDireita = M[posDireita[0]][posDireita[1]]
        if casaDireita == -1:
            casaDireita = len(M)*len(M[0])
            
        casaEsquerda = M[posEsquerda[0]][posEsquerda[1]]
        if casaEsquerda == -1:
            casaEsquerda = len(M)*len(M[0])

        menor = min(casaBaixo, casaCima, casaDireita, casaEsquerda)

        # Se duas ou mais casas adjacentes possuirem o
        # mesmo valor, a escolhida é aquela em que estiver no desvio
        # verificado antes.
        if menor == casaBaixo:
            casaAtual = posBaixo
            caminho.append(posBaixo)
        elif menor == casaCima:
            casaAtual = posCima
            caminho.append(posCima)
        elif menor == casaDireita:
            casaAtual = posDireita
            caminho.append(posDireita)
        else:
            casaAtual = posEsquerda
            caminho.append(posEsquerda)

    return caminho

def marcarMatriz(M, linhas, colunas, posLivre):
    """ Marca toda a matriz M com as respectivas distâncias de cada
        casa visitada até a posição livre

    """
    
    a = posLivre[0]
    b = posLivre[1]
    M[a][b] = 1
    
    casasMarcadas = []
    casasMarcadas.append([a, b])
    estaAtualizando = True
    while estaAtualizando:
        # Para cada varredura na matriz deve haver
        # pelo menos uma casa marcada (ou atualizada).
        # Se não houver, significa que não há mais casas
        # para marcar.
        estaAtualizando = False
        for x in range(linhas):
            for y in range(colunas):
                # 0 representa uma casa visitada.
                # -1 representa uma casa não visitada..

                # Só tenta marcar as casas adjacentes
                # se a casa central ja tiver sido marcada
                # (seu valor é diferente de zero) e
                # se ela já tiver sido visitada (diferente de -1).
                if M[x][y] > 0:
                    posBaixo = [(x+1)%linhas, y]
                    posCima = [(x-1)%linhas, y]
                    posDireita = [x, (y+1)%colunas]
                    posEsquerda = [x, (y-1)%colunas]

                    # Checa se uma casa adjacente já foi marcada,
                    # caso esteja marcada verifica ainda
                    # se há uma distância menor para marcar.
                    if posBaixo not in casasMarcadas:
                            if M[posBaixo[0]][posBaixo[1]] == 0:
                                M[posBaixo[0]][posBaixo[1]] = M[x][y] + 1
                                casasMarcadas.append(posBaixo)
                                estaAtualizando = True
                    else:
                        if M[posBaixo[0]][posBaixo[1]] > M[x][y] + 1:
                            M[posBaixo[0]][posBaixo[1]] = M[x][y] + 1
                            estaAtualizando = True

                    if posCima not in casasMarcadas:
                            if M[posCima[0]][posCima[1]] == 0:
                                M[posCima[0]][posCima[1]] = M[x][y] + 1
                                casasMarcadas.append(posCima)
                                estaAtualizando = True
                    else:
                        if M[posCima[0]][posCima[1]] > M[x][y] + 1:
                            M[posCima[0]][posCima[1]] = M[x][y] + 1
                            estaAtualizando = True

                    if posDireita not in casasMarcadas:
                            if M[posDireita[0]][posDireita[1]] == 0:
                                M[posDireita[0]][posDireita[1]] = M[x][y] + 1
                                casasMarcadas.append(posDireita)
                                estaAtualizando = True
                    else:
                        if M[posDireita[0]][posDireita[1]] > M[x][y] + 1:
                            M[posDireita[0]][posDireita[1]] = M[x][y] + 1
                            estaAtualizando = True

                    if posEsquerda not in casasMarcadas:
                            if M[posEsquerda[0]][posEsquerda[1]] == 0:
                                M[posEsquerda[0]][posEsquerda[1]] = M[x][y] + 1
                                casasMarcadas.append(posEsquerda)
                                estaAtualizando = True
                    else:
                        if M[posEsquerda[0]][posEsquerda[1]] > M[x][y] + 1:
                            M[posEsquerda[0]][posEsquerda[1]] = M[x][y] + 1
                            estaAtualizando = True

    return M

