import random

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

global temPersonagem
"""
Variável booleana para verificar se há um personagem no mesmo espaço
"""

global salasLivres
"""
Matriz que armazena as salas queainda estão livres
"""

global salasVisitadas
"""
Marca salas que já foram vizitadas, para que se possa usar para fazer o caminho que o personagem passara
"""

global boolSalas
"""
Matriz booleana para verificar onde ja se passou dentre as salas vizitadas
"""

global caminhos,caminho

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, temPersonagem, salasLivres, salasVisitadas, boolSalas, caminhos, caminho
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

    temPersonagem = False

    salasLivres = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        salasLivres.append(linha)

    salasVisitadas = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        salasVisitadas.append(linha)

    boolSalas = []
    for i in range(N):
        linha = []
        for j in range(N):
            linha.append([0])
        boolSalas.append(linha)

    caminhos = []
    caminho = []

def menorCaminho(x, y, salasVisitadas, salasLivres, boolSalas):
    global orientacao, caminho

    vizinhos = [ [(x+1)%len(mundo),y],
                     [(x-1)%len(mundo),y],
                     [x,(y+1)%len(mundo)],
                     [x,(y-1)%len(mundo)] ]

    if (salasLivres[x][y]):
        caminhos.append(caminho)
        return caminhos
    elif (not salasLivres[x][y]):

        for i in range(len(vizinhos)):
            if ((("V" in salasVisitadas[vizinhos[i][0]][vizinhos[i][1]]) and (1 in boolSalas[vizinhos[i][0]][vizinhos[i][1]])) or (("L" in salasLivres[vizinhos[i][0]][vizinhos[i][1]]))):
                if ("L" in salasLivres[vizinhos[i][0]][vizinhos[i][1]]):

                    l = vizinhos[i][0]
                    c = vizinhos[i][1]

                    caminho.append([l,c])
                    caminhos.append(caminho)

                    return caminho
                l = vizinhos[i][0]
                c = vizinhos[i][1]

                # Marca como casa ja visitada para naoentrar em um possivel loop infinito
                boolSalas[l][c] = [0]
                caminho.append([l,c])

                if (salasLivres[l][c]):
                    return caminho
                return menorCaminho(l, c, salasVisitadas, salasLivres, boolSalas)

        boolSalas[x][y] = [0]

        voltaCasa = caminho.pop()
        if (salasLivres[voltaCasa[0]][voltaCasa[1]]):
            return caminho

        if (not caminho):
            return []
        return menorCaminho(caminho[len(caminho)-1][0], caminho[len(caminho)-1][1], salasVisitadas, salasLivres, boolSalas)


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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,temPersonagem, salasLivres, salasVisitadas, boolSalas
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido psara as
    # adjacências da sala atual (requisitos completos no enunciado).
    
    per = percepcao[:]
    # Remove todos as pecepções F,B,I e U para deixar apenas o personagem, caso exista
    if ("F" in percepcao):
        per.remove("F")
    if ("B" in percepcao):
        per.remove("B")
    if ("I" in percepcao):
        per.remove("I")
    if ("U" in percepcao):
        per.remove("U")
    
    pos = posicao
    ori = orientacao
    if "I" in percepcao:
        if (not ("I" in mundo[pos[0]][pos[1]])):
            mundo[pos[0]][pos[1]].append("I")
        mundo[pos[0]][pos[1]] = ["M"]
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)
        boolSalas[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = [0]

    else :
        mundo[pos[0]][pos[1]] = ["V"]
        salasVisitadas[pos[0]][pos[1]] = ["V"]
        if ("L" in salasLivres[pos[0]][pos[1]]):
            salasLivres[pos[0]][pos[1]] = []

        boolSalas[pos[0]][pos[1]] = [1]
    # Verifica se há percepção de um jogador
    if (per):
        temPersonagem = True

    if (("B" in percepcao) or ("F") in percepcao):
        if (("B" in percepcao) and ("F") in percepcao):
            if ((not "F" in mundo[pos[0]][pos[1]]) and (not "B" in mundo[pos[0]][pos[1]])):
                mundo[pos[0]][pos[1]].append("F")
                mundo[pos[0]][pos[1]].append("B")
        elif ("B" in percepcao):
            if (not "B" in mundo[pos[0]][pos[1]]):
                mundo[pos[0]][pos[1]].append("B")
        elif ("F" in percepcao):
            if (not "F" in mundo[pos[0]][pos[1]]):
                mundo[pos[0]][pos[1]].append("F")
        i = -1
        while (i < 2):
            j = -1
            while (j < 2):  
                if ((i == 0 or j == 0) and (i != j)):
                    l = (pos[0]+i)%len(mundo)
                    c = (pos[1]+j)%len(mundo)
                    #salasEncostadas
                    if ((not mundo[l][c]) or ("P?/W?" in mundo[l][c])):
                        # Marca as casas que podem conter perigos
                        if (("B" in percepcao) and ("F" in percepcao)):
                            mundo[l][c] = ["P?/W?"]
                        elif ("B" in percepcao):
                            mundo[l][c] = ["P?"]
                        else :
                            mundo[l][c] = ["W?"]
                j = j + 1
            i = i + 1
    elif ("U" in percepcao): # Nao marcar esse como feito.... Ver depois
        mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ["L"]
        salasLivres[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ["L"]
    else : # Marca os locais livres
        i = -1
        while (i < 2):
            j = -1
            while (j < 2):  
                if ((i == 0 or j == 0)):
                    l = (pos[0]+i)%len(mundo)
                    c = (pos[1]+j)%len(mundo)
                    if (not mundo[l][c]):
                        mundo[l][c] = ["L"]
                        salasLivres[l][c] = ["L"]
                j = j + 1
            i = i + 1

    for i in range(len(mundo)):
        for j in range(len(mundo)):
            if (mundo[i][j] == mundoCompartilhado):
                mundo[i][j] = mundoCompartilhado
            if ("L" in mundoCompartilhado[i][j]):
                if (not("L" in mundo[i][j]) and not("V" in mundo[i][j])):
                    mundo[i][j] = ["L"]
                    #boolSalas[i][]
            elif ("P?" in mundoCompartilhado[i][j]):
                if (not("L" in mundo[i][j]) and not("V" in mundo[i][j])):
                    mundo[i][j] = ["P?"]
            elif ("W?" in mundoCompartilhado[i][j]):
                if (not("L" in mundo[i][j]) and not("V" in mundo[i][j])):
                    mundo[i][j] = ["W?"]
            elif ("P" in mundoCompartilhado[i][j]):
                if (not("L" in mundo[i][j]) and not("V" in mundo[i][j])):
                    mundo[i][j] = ["P"]
            elif ("W" in mundoCompartilhado[i][j]):
                if (not("L" in mundo[i][j]) and not("V" in mundo[i][j])):
                    mundo[i][j] = ["W"]
            elif ("M" in mundoCompartilhado[i][j]):
                mundo[i][j] = ["M"]

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
    # 
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)

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
                print("",end="\t| ")
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, temPersonagem, salasLivres, salasVisitadas, boolSalas, caminho
    # Aplica uma certa estratégia para decidir a ação a ser
    # executada com base na representação local do mundo.
    # Devolve (para o mundo) o nome da ação pretendida.
    # Duas ações só são possíveis em condições específicas,
    # que devem ser testadas de antemão (sob risco da personagem
    # entrar em loop): atirar só é possível quando a personagem
    # dispõe de flechas, e compartilhar só é possível quando
    # existem outras personagens na mesma sala (percebidas
    # pela função planejar através de percepções diferentes de
    #time.sleep(0.5)
    # "F", "B", "I" ou "U").
    pos = posicao
    ori = orientacao
    vizinhos = [ [(pos[0]+1)%len(mundo),pos[1]],
                     [(pos[0]-1)%len(mundo),pos[1]],
                     [pos[0],(pos[1]+1)%len(mundo)],
                     [pos[0],(pos[1]-1)%len(mundo)] ]

    if (temPersonagem):
        acao = "C"
        temPersonagem = False
        assert acao in ["A","D","E","T","C"]
        return acao
    else :


        # Gambiarra para caso o boneco chegue em um lucal sem saída, que no caso nao pode passar de 3
        contador = 0
        if (nFlechas > 0):
            for i in range(len(vizinhos)):
                if ("W" in mundo[vizinhos[i][0]][vizinhos[i][1]]):
                    if ("W" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]):
                        acao = "T"
                        assert acao in ["A","D","E","T","C"]
                        return acao
                    else:
                        acao = "E"
                        if ori[0]==0:
                            ori[1] = -ori[1]
                        ori[0],ori[1] = ori[1],ori[0]

                        caminho = []
                        assert acao in ["A","D","E","T","C"]
                        return acao


        for i in range(len(vizinhos)):
            if (("P?" or "W?" or "M") in mundo[vizinhos[i][0]][vizinhos[i][1]]):
                contador = contador + 1

        if ("L" in mundo[vizinhos[0][0]][vizinhos[0][1]] or "L" in mundo[vizinhos[1][0]][vizinhos[1][1]] or "L" in mundo[vizinhos[2][0]][vizinhos[2][1]] or "L" in mundo[vizinhos[3][0]][vizinhos[3][1]]):
            if ("L" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]):
                acao = "A"
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)

                caminho = []
                assert acao in ["A","D","E","T","C"]
                return acao
            else :
                acao = "E"
                if ori[0]==0:
                    ori[1] = -ori[1]
                ori[0],ori[1] = ori[1],ori[0]

                caminho = []
                assert acao in ["A","D","E","T","C"]
                return acao
        ### AQUI QUE FICAVA O BAGULHETE COM O CONTADOR >=3
        else :
            for i in range(len(mundo)):
                for j in range(len(mundo)):
                    if ("V" in mundo[i][j] or "L" in mundo[i][j]):
                        boolSalas[i][j] = [1]
                        if (i == pos[0] and j == pos[1]):
                            boolSalas[i][j] = [0]
            # Verificação se ainda ha salas livres
            if (not salasLivres):
                for i in range(len(vizinhos)):
                    if (("P?" or "W?") in mundo[pos[0]+ori[0]][pos[1]+ori[1]]):
                        acao = "A"
                        pos[0] = (pos[0]+ori[0])%len(mundo)
                        pos[1] = (pos[1]+ori[1])%len(mundo)
                        
                        assert acao in ["A","D","E","T","C"]
                        return acao
                    else: 
                        acao = "E"
                        if ori[0]==0:
                            ori[1] = -ori[1]
                        ori[0],ori[1] = ori[1],ori[0]
                        assert acao in ["A","D","E","T","C"]
                        return acao                        
            elif (salasLivres):

                if (not caminho):
                    caminho = menorCaminho(pos[0], pos[1], salasVisitadas, salasLivres, boolSalas)

                if (caminho):
                    proximaCasa = caminho[0]

                    if ((( (pos[0]+ori[0]) %len(mundo) == proximaCasa[0] )) and ((pos[1]+ori[1])%len(mundo) == proximaCasa[1])):

                        acao = "A"
                        pos[0] = (pos[0]+ori[0])%len(mundo)
                        pos[1] = (pos[1]+ori[1])%len(mundo)

                        caminho.remove(caminho[0])

                        assert acao in ["A","D","E","T","C"]
                        return acao
                    else :
                        acao = "E"
                        if ori[0]==0:
                            ori[1] = -ori[1]
                        ori[0],ori[1] = ori[1],ori[0]
                        assert acao in ["A","D","E","T","C"]
                        return acao
            elif (contador >= 3):
                if (not salasLivres):# Caso nao haja mais locais livres para esplorar se joga em um P? ou W?
                    if (("W?" or "P?") in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]):
                        acao = "A"
                        pos[0] = (pos[0]+ori[0])%len(mundo)
                        pos[1] = (pos[1]+ori[1])%len(mundo)
                        assert acao in ["A","D","E","T","C"]
                        return acao
    acao = "E"
    if ori[0]==0:
        ori[1] = -ori[1]
    ori[0],ori[1] = ori[1],ori[0]
    assert acao in ["A","D","E","T","C"]
    return acao
