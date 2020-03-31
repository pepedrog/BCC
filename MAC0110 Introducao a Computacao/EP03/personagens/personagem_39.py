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

global ultimaAcao
"""
Guarda a ultima Ação da personagem, esta variável permite incorporar
informações compartilhadas se a ultima ação foi compartilhar e modificar
salas (W?) para (L) quando possivel.
"""

global salasLivres
"""
Lista que guarda coordenadas de salas livres
"""

global rotaAtual
"""
Matriz nxn onde cada entrada representa o numero de passos de distância
até a próxima casa livre em salasLivres.pop(), passando apenas por casas
visitadas. Se mundo[i][j] = "L", então rotaAtual[i][j] = 0 e casas adjacentes
a rotaAtual[i][j] recebem 1 se corresponderem a uma casa visitada.
Casas que não foram visitadas nem livres recebem marcação -1.
"""

global compartilhavel
"""
Variável booleana que serve para planejar um compartilhamento de informações
com outra personagem no mundo.
"""

global proximaCasa
"""
Guarda as coordenadas da proxima casa livre
"""

def anota(pos,H):
    """Vasculha entorno de uma posição no mundo marcando com H, as posições
    que não estejam livres, visitadas ou ja foram deduzidas como P,M ou W.
    """
    permanente = [["P"],["M"],["W"],["L"],["V"]]
    for i in range(-1,2):
        anotacaoA = mundo[(pos[0]+i)%len(mundo)][pos[1]]
        if H not in anotacaoA and anotacaoA not in permanente:
            mundo[(pos[0]+i)%len(mundo)][pos[1]].append(H)
        anotacaoB = mundo[pos[0]][(pos[1]+i)%len(mundo)]
        if H not in anotacaoB and anotacaoB not in permanente:
            mundo[pos[0]][(pos[1]+i)%len(mundo)].append(H)

def marcaAdjacente(i,j,k):
    """Marca casas adjacentes em uma posicao i,j em rotaAtual com k+1
    """
    # declara as variáveis globais que serão acessadas
    global N, rotaAtual

    if rotaAtual[(i+1)%N][j] == -2:
        rotaAtual[(i+1)%N][j] = k+1
    if rotaAtual[(i-1)%N][j] == -2:
        rotaAtual[(i-1)%N][j] = k+1
    if rotaAtual[i][(j+1)%N] == -2:
        rotaAtual[i][(j+1)%N] = k+1
    if rotaAtual[i][(j-1)%N] == -2:
        rotaAtual[i][(j-1)%N] = k+1
    

def atualizaRotaAtual():
    """Recebe uma matriz rota e uma lista coordenadas de tamanho 2.
    Retorna uma matriz onde cada entrada corresponde ao número de passos
    necessarios para chegar na próxima casa livre passando apenas por
    casas visitadas. 
    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, salasLivres, posicao, proximaCasa, rotaAtual
    posAtual = posicao
    if posAtual == proximaCasa and len(salasLivres) > 0:
        proximaCasa = salasLivres.pop()
        #(Re)Inicializa rotaNova
        rotaAtual = []
        for i in range(N):
            linha = []
            for j in range(N):
                linha.append(-1)
            rotaAtual.append(linha)

    for i in range(N):
        for j in range(N):
            if mundo[i][j] == ["V"]:
                rotaAtual[i][j] = -2 #-2 significa caminho possivel ainda não marcado

    i,j = proximaCasa

    #Posição da casa livre recebe marcacao 0 
    rotaAtual[i][j] = 0

    #Casas adjacentes a casa livre recebem marcacao 1, casas adjacentes a estas recebem
    #marcacao 2 e assim sucessivamente. 
    pos = [0,0]
    pos[0] = i
    pos[1] = j
    ultimaPosicao = j
    marcacao=0
    #Realiza a marcacao andando para a direita e depois para cima
    for i in range(N*N):
        marcaAdjacente(pos[0],pos[1],marcacao)
        marcacao = marcacao + 1
        pos[1] = (pos[1] + 1)%N
        if pos[1] == ultimaPosicao:
            pos[0] = (pos[0]+1)%N


def verificaCasasLivres():
    """Vasculha o mapa e atualiza lista de casas livres não visitadas
    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, salasLivres
    for i in range(N):
        for j in range(N):
            if mundo[i][j] == ["L"]:
                if [i,j] not in salasLivres:
                    salasLivres.append([i,j])
 
def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, ultimaAcao, rotaAtual, salasLivres, compartilhavel, proximaCasa
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
    # Não há ultima ação no ínicio
    ultimaAcao = "X"
    #Cria uma lista vazia para armazenas posições de salas livres
    salasLivres = []
    #Inicializa a matriz da rota atual
    rotaAtual = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([-2]) # começa com listas vazias
        rotaAtual.append(linha)

    #Outras inicializações
    compartilhavel = False
    proximaCasa = [0,0]
        

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, ultimaAcao, salasLivres, compartilhavel, proximaCasa, rotaAtual
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).

    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        
    pos = posicao
    ori = orientacao
    mundo[pos[0]][pos[1]] = ["V"] #Marca a posição atual como visitado
    rotaAtual[pos[0]][pos[1]] = -2
    atualizaRotaAtual()
    
    #Lógica do compartilhamento de informações
    if ultimaAcao == "C":
        #Incorpora informações compartilhadas quando possivel, para isto
        #Assume que as informações (L), (M), (P) e (P?) são verdadeiras.
        #Se uma casa no mundoCompartilhado, mundoCompartilhado[i][j]
        #tiver sido marcada como W? ou W, marca com W? se não houver informação
        #disponivel em mundo[i][j]
        #Além disso, atualiza a variável compartilhavel para evitar loop de
        #acao = C
        listaDeCertezas = ["L","M","P"]
        for i in range(N):
            for j in range(N):
                    for k in range(len(mundoCompartilhado[i][j])):
                        anotacao = mundoCompartilhado[i][j][k]
                        if anotacao in listaDeCertezas:
                            mundo[i][j] = [mundoCompartilhado[i][j][k]]
                        elif anotacao == "V": #Casas visitadas por outra personagem estao livres
                            if mundo[i][j] != ["V"]:
                                mundo[i][j] = ["L"]
                                if [i,j] not in salasLivres: #Guarda as coordenadas da sala livre
                                    salasLivres.append([i,j])
                        elif anotacao == "P?" and "P?" not in mundo[i][j] and mundo[i][j] != ["P"] and mundo[i][j] != ["V"]:
                            mundo[i][j].append("P?")
                        elif "W?" not in mundo[i][j] and mundo[i][j] != ["W"] and mundo[i][j] != ["V"]:
                            mundo[i][j].append("W?") #Wumpus vistos anteriormente podem estar mortos agora
        compartilhavel = False

    #Processa as percepcoes:
    for p in percepcao:
    
        #Lógica do impacto
        if p == "I":
            #Ao sentir um impacto, marca um muro (M) na posição atualizada erroneamente
            #e corrige a posição
            rotaAtual[pos[0]][pos[1]] = -1
            mundo[pos[0]][pos[1]] = ["M"]
            pos[0] = (pos[0]-ori[0])%len(mundo)
            pos[1] = (pos[1]-ori[1])%len(mundo)
            #Atualiza salas livres
            if len(salasLivres) > 0:
                salasLivres.pop()
            if len(salasLivres) > 0:
                proximaCasa = salasLivres.pop()
            atualizaRotaAtual()

        #Lógica da brisa
        elif p == "B":
            #Ao sentir uma brisa, marca com P? as casas adjacentes que não
            #possuem marcacao
            anota(pos,"P?")
                    
        #Lógica do fedor    
        elif p == "F": 
            #Ao sentir fedor, marca com W? as casas adjacentes que não
            #possuem marcacao
            anota(pos,"W?")
                    
        #Lógica do disparo com sucesso    
        elif p == "U" and ultimaAcao == "T":
            #Se a ultima ação foi atirar e "U" está em percepcao,
            #então a casa a frente da personagem esta livre

            mundo[(pos[0]+ori[0])%len(mundo)[(pos[1]+ori[1])%len(mundo)]] = ["L"] #Substitui marcação
            salasLivres.append([i,j])

        else:
            #Se alguma percepção é diferente de "I", "B", "F" e "U", então
            #essa percepção representa o nome de uma personagem e a próxima
            #ação deve ser compartilhar as informações. 
            compartilhavel = True
        
    if "F" not in percepcao and "B" not in percepcao:
        #Se a personagem nao sente fedor (F) nem brisa (B),
        #então as casas adjacentes a ela não visitadas
        #que não são muros estão livres.
              
        for i in range(-1,2):
            linhaAdj = (pos[0]+i)%len(mundo)
            colunaAdj = (pos[1]+i)%len(mundo)
            verificacoes = [["M"],["W"],["P"],["V"]]

            if mundo[linhaAdj][pos[1]] not in verificacoes and mundo[linhaAdj][pos[1]] != ["V"]:
                mundo[linhaAdj][pos[1]] = ["L"]
                if [linhaAdj,pos[1]] not in salasLivres:
                    salasLivres.append([linhaAdj,pos[1]])
            if mundo[pos[0]][colunaAdj] not in verificacoes and mundo[linhaAdj][pos[1]] != ["V"]:
                mundo[pos[0]][colunaAdj] = ["L"]
                if [pos[0],colunaAdj] not in salasLivres:
                    salasLivres.append([pos[0],colunaAdj])
                
    verificaCasasLivres()

        
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
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, ultimaAcao, salasLivres, compartilhavel, rotaAtual
    # Aplica uma certa estratégia para decidir a ação a ser
    # executada com base na representação local do mundo.
    # Devolve (para o mundo) o nome da ação pretendida.

    #A lógica de ação funciona da seguinte maneira:
    #Se é possivel compartilhar, então acao = "C"
    #Se existem casas livres, então a personagem
    #busca seguir a rota até essa casa livre
    #Se não existem casas livres e a personagem
    #está diante de um W ou W?, então acao = "T"
    #Em ultimo caso, acao = D


    #Atualiza rota atual
    atualizaRotaAtual()
    
    pos = posicao
    ori = orientacao
    pos = posicao
    ori = orientacao

    #Ação padrão
    acao = "D"

    if compartilhavel:
        acao = "C"

    elif len(salasLivres) > 0:
        #Verifica se a rota permite andar para frente
        #Para isto, consulta a marcacao da casa atual e a marcacao da casa da frente
        #Na matriz rota atual.
        marcacaoAtual = rotaAtual[pos[0]][pos[1]]
        marcacaoAFrente = rotaAtual[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]
        if marcacaoAFrente < marcacaoAtual and marcacaoAFrente != -1:
            acao = "A"

    elif "W?" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] or "W" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:
        acao = "T"
        

    #Atualiza posicao e orientacao
    pos = posicao
    ori = orientacao
    if acao=="A":
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
    if acao=="D":
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]

    #Lembra da ultima posição
    ultimaAcao = acao

    

    assert acao in ["A","D","E","T","C"]
    return acao
