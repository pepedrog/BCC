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

global salasLivres
""" Cria uma matriz com o indice de todas as salas indicadas como livres
    e não visitadas até o momento.A próxima sala livre a ser visitada é 
    sempre a posição 0 dessa matriz, e quando a sala é visitada ela é
    removida dessa matriz. 
"""

global caminho
""" Uma lista com indices de salas que indica o menor caminho 
    para se chegar a próxima sala livre.
"""

global oriGiro
"""Variavel simples que indica se devo girar para a esquerda para direita.
   2 indica um giro para a direita e -2 um giro para esquerda.Ela em conjunto
   com a global girou fará o personagem andar em formato de zig-zag quando 
   ele não possui mais salas livres para visitar.
"""

global girou
"""Variavel booleana que indica se o personagem ja girou.Se False o personagem
    deve girar, caso False o personagem deve andar.
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
    global N, mundo, posicao, orientacao, salasLivres, caminho, oriGiro, girou
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
    salasLivres, caminho = [], []
    oriGiro, girou = 2, False

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salasLivres
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        pos = posicao
        ori = orientacao
        vizinhos = [ [(pos[0]+1)%N,pos[1]], [(pos[0]-1)%N,pos[1]], #código dos vizinhos do toro atual, muito importante para o manejo das percepções.
                    [pos[0],(pos[1]+1)%N], [pos[0],(pos[1]-1)%N] ]
        if("V" not in mundo[pos[0]][pos[1]]): #coloco o V caso o toro atual ainda não tem indicação de visitado.
            mundo[pos[0]][pos[1]] += ["V"]
        if ("I" in percepcao):
            if("M" not in mundo[pos[0]][pos[1]]): #adiciono a indicação de muro encontrado caso bata em um.
                mundo[pos[0]][pos[1]] += ["M"]
            for i in range(2):
                pos[i] -= ori[i] #volto a minha posição anterior
        for percep in percepcao: #verificação caso exista uma percepção diferente das padrões do jogo, logo um personagem.
            if(percep != 'B' and percep != 'F' and percep != 'I' and percep != 'B'):
                mundo[pos[0]][pos[1]] += ["C"] #adiciono a visão de mundo C de 'compartilhar' ou de 'char' 
        for vizinho in vizinhos:
            if(percepcao == [] and vizinho not in salasLivres and "V" not in mundo[vizinho[0]][vizinho[1]]):
               mundo[vizinho[0]][vizinho[1]] = ["L"]
               salasLivres.append(vizinho)
            if("L" not in mundo[vizinho[0]][vizinho[1]]):
                if('F' in percepcao and "W?" not in mundo[vizinho[0]][vizinho[1]]):
                    mundo[vizinho[0]][vizinho[1]] += ["W?"]
                if('B' in percepcao and "P?" not in mundo[vizinho[0]][vizinho[1]]):
                    mundo[vizinho[0]][vizinho[1]] += ["P?"]
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
                # if("L" in mundoCompartilhado[i][j] and "V" not in mundo[i][j] and len(salasLivres) <=2):
                #     salasLivres.append([i,j])
                # print("".join(mundo[i][j]),end="")
                # toroComp = "".join(mundoCompartilhado[i][j])
                # if(toroComp != '' and toroComp not in mundo[i][j]):
                #     print(toroComp,end='c')
                # print('',end="\t|")
                if(mundoCompartilhado[i][j] != []):
                    for infoComp in mundoCompartilhado[i][j]:
                        if(infoComp not in mundo[i][j] and "V" not in mundo[i][j]):
                            if(infoComp == "L"):
                                salasLivres.append([i,j])
                            mundo[i][j] += infoComp + 'c'
                print("".join(mundo[i][j]),end="\t|")
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salasLivres, caminho
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
    #acao = input("Digite a ação desejada (A/D/E/T/C): ")
    pos = posicao
    ori = orientacao
    print(salasLivres)
    if("C" in mundo[pos[0]][pos[1]]): #se a visão de mundo acusar um personagem na posição atual, devo compartilhar e receber informação.
        acao = "C" 
        mundo[pos[0]][pos[1]].remove("C")
    elif(len(salasLivres) > 0): #devo sempre tentar visitar as salas livres
        if(caminho == []):
            determinarCaminho(construirCaminho())
        if(caminho != []):
            print(caminho)
            acao = calcularMovimento(caminho[-1])
            if(acao == "A"):
                if(caminho[-1] == salasLivres[0]):
                    del salasLivres[0]
                del caminho[-1]
        else:
            acao = realizarZigZag()
    else:
        acao = realizarZigZag()
    corrigirOrientacao(acao)
    print(acao)
    assert acao in ["A","D","E","T","C"]
    return acao

def construirCaminho():
    """Essa função cria uma matriz com todos os possiveis caminhos entre as salas já visitadas, mostrando a distância entre a posição atual e as 
       possiveis casas.Essa matriz é então usada na função determinarCaminho para a obtenção do caminho mais curto. 
    """
    global mundo, posicao
    n = len(mundo)
    pos = posicao
    caminhos, contN = [], 0
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(0)
            if('V' not in mundo[i][j] and 'L' not in mundo[i][j] and 'Lc' not in mundo[i][j]):
                contN += 1
        caminhos.append(linha)
    caminhos[pos[0]][pos[1]] = 1
    m, i = [pos], 0
    while(len(m) > i):
        vizinhos = [ [(m[i][0]+1)%n,m[i][1]], [(m[i][0]-1)%n,m[i][1]],
                        [m[i][0],(m[i][1]+1)%n], [m[i][0],(m[i][1]-1)%n] ]
        for vizinho in vizinhos: 
            if(vizinho not in m and ("V" in mundo[vizinho[0]][vizinho[1]] or "L" in mundo[vizinho[0]][vizinho[1]] or "Lc" in mundo[vizinho[0]][vizinho[1]])):
                m.append(vizinho)
                caminhos[vizinho[0]][vizinho[1]] = caminhos[m[i][0]][m[i][1]] + 1
        i += 1
    return caminhos

def determinarCaminho(caminhos):

    """Essa função cria uma matriz que indica o menor caminho a ser percorrido entre a posição atual e a próxima casa livre.
    """
    global salasLivres, caminho
    n = len(caminhos)
    caminho, toro = [], [0,0]
    toro[0], toro[1] = salasLivres[0][0], salasLivres[0][1]
    while(caminhos[toro[0]][toro[1]] != 1):
        vizinhos = [ [(toro[0]+1)%n,toro[1]], [(toro[0]-1)%n,toro[1]],
                      [toro[0],(toro[1]+1)%n], [toro[0],(toro[1]-1)%n] ]
        for vizinho in vizinhos:
            if(caminhos[vizinho[0]][vizinho[1]] != 0 and caminhos[vizinho[0]][vizinho[1]] == caminhos[toro[0]][toro[1]] - 1):
                caminho.append([toro[0],toro[1]])
                toro[0], toro[1] = vizinho[0], vizinho[1]
            else:
                if(toro[0] == salasLivres[0] and toro[1] == salasLivres[1]):
                    return

def calcularMovimento(proxToro):
    global N, posicao, orientacao
    pos = posicao
    ori = orientacao
    if(pos[0] == (proxToro[0] - ori[0])%N and pos[1] == (proxToro[1] - ori[1])%N) :
        acao = "A"
    elif(pos[0] == (proxToro[0] - ori[1])%N and pos[1] == (proxToro[1] + ori[0])%N):
        acao = "D"
    elif(pos[0] == (proxToro[0] + ori[1])%N and pos[1] == (proxToro[1] - ori[0])%N):
        acao = "E"
    else:
        acao = "E"
    return acao

def realizarZigZag():
    global girou,oriGiro
    if(not girou):
        if(oriGiro == 2):
            acao = "D"
        elif(oriGiro == -2):
            acao = "E"
        oriGiro = -oriGiro
        girou = True
    else:
        acao = "A"
        girou = False
    return acao

def corrigirOrientacao(acao):
    global mundo, posicao, orientacao
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
