# flag para depuração
__DEBUG__ = False


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

global updated
""" Guarda quantas vezes uma certa posição do mundo foi atualizada (é uma matriz NxN)
"""

global livre
""" lista de salas livres
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

global lastaction
""" Guarda a ultima ação da personagem, para utilizar na sua próxima preperação
"""

global tempessoa
""" Para informar caso haja alguém na posição atual
"""

global actionqueue
""" Guarda a ordem de ações da função BFS
"""

global direcoes
""" Guarda de forma unificada cada direção
"""

global dist
""" Lista  da distância entre duas casas, gerada na função bfs
"""

global moves
""" Lista de movimentos de uma casa para as outras
"""

global vizinhoWumpus
""" Uma infeliz casa que está adjacente a um wumpus (lista que salva a posição x e y de um vizinho do Wumpus)
"""

def girapraca(inicial, final): #retorna a sequência de movimentos para girar para uma certa orientação
    global direcoes
    iniciali = direcoes.index(inicial)
    if(final == 3 and iniciali == 0): #todos os casos são baseados nos idexes das direções na lista global
        return ["D"]
    if(final == 0 and iniciali == 3):
        return ["E"]
    if(final > iniciali):
        return ["E"]*(final - iniciali)
    if(iniciali > final):
        return ["D"]*(iniciali - final)
    return []

def bfs(posicao, orientacao): #função para achar o menor caminho de uma posição "posicao" orientada "orientacao" até todas as outras casas que podem ser visitadas sem risco
    global direcoes, mundo, moves
    fila = [posicao] #fila que armazena qual a próxima posição a ser visitada
    orientacoes = [orientacao] #fila de orientações ao chegar nessas posições
    dist[posicao[0]][posicao[1]] = 0 #a distância da origem da função é 0
    while(len(fila) != 0): #enquanto tiverem casas possíveis para serem visitadas
        iterador = fila.pop(0) #retira o primeiro elemento da lista para iterar as casas vizinhas a ele
        oriatual = orientacoes.pop(0) #orientação atual da personagem
        for i in range(4): #itera pelas casas vizinhas
            nx = (iterador[0] + direcoes[i][0])%N #vizinho a ser estudado
            ny = (iterador[1] + direcoes[i][1])%N #"" "" ""
            if(dist[nx][ny] < float('Inf')): continue #se a distância a este vizinho já tiver sido determinada ignora
            if(not("V" in mundo[nx][ny] or "L" in mundo[nx][ny])): continue #se não for possível visitar a casa, ignora
            fila.append([nx, ny]) #como é possível visitar esta casa coloca ela na fila
            orientacoes.append(direcoes[i]) #coloca a orientação
            dist[nx][ny] = dist[iterador[0]][iterador[1]] + 1 #distância da casa, vai aumentando 1 em relação a casa do iterador
            moves[nx][ny] = moves[iterador[0]][iterador[1]].copy() #copia a lista de movimentos atuais (até o iterador)
            movimento = girapraca(oriatual, i) #movimento a ser feito para ir na casa, começa pela rotação necessária
            movimento.append("A") #coloca ação de andar
            for j in range(len(movimento)): #copia o movimento para a lista moves
                moves[nx][ny].append(movimento[j])
                
    return


def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, updated, lastaction, livre, direcoes, actionqueue, dist, temWumpus
    # guarda o tamanho do mundo
    N = tamanho
    lastaction = ""
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    updated = []
    livre = []
    dist = []
    actionqueue = []
    moves = []
    direcoes = [ [1,0], [0,1], [-1,0], [0,-1] ]
    vizinhoWumpus = []
    for i in range(N) : 
        linha = []
        linha2 = []
        linha3 = []
        linha4 = []
        linha5 = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
            linha2.append(0)
            linha3.append(False) #nenhuma casa começa livre (somente a origem, pois se não for não estaremos mais aqui para contar a historia)
            linha4.append(float('Inf')) #distâncias começam como infinitamente grandes, indicando que não se pode ir para a casa
            linha5.append([])
        mundo.append(linha)
        updated.append(linha2)
        livre.append(linha3)
        dist.append(linha4)
        moves.append(linha5)
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, updated, lastaction, livre, tempessoa, direcoes, temWumpus, vizinhoWumpus
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
    #
    
    vizinho = [] #lista de vizinhos. Útil para reduzir um pouco o tamanho das condicionais
    tempessoa = False #reseta a variável, e checa a cada iteração
    temPercepcao = False #variável para checar se tem alguma percepção sendo recebida
    vizinhoWumpus = [] #mesma lógica
    temWumpus = False #booleana para checar se tem um Wumpus. Útil para rodar a última varredura pela matriz
    
    for i in range(len(percepcao)):
        if(percepcao[i] != "F" and percepcao[i] != "B" and percepcao[i] != "I" and percepcao[i] != "U"):
            """ este check está aqui pelo fato de todas as personagens programadas sempre terem que compartilhar informações
                , logo ao jogar num mundo com vários jogadores é garantido que os dois vão estar na mesma casa depois de compartilhar informações
            """
            if(lastaction != "C"): #garante que não vai ficar compartilhando informações mais de uma vez, caso ainda tenha uma personagem na casa
                tempessoa = True
        else:
            temPercepcao = True
    if(lastaction == "C"): #atualiza as informações do mundo levando em consideração as informações recebidas por outra personagem. Confiança é chave! Ignora informações incertas, para averiguá-las pessoalmente
        for i in range(N): 
            for j in range(N):               
                if(len(mundoCompartilhado[i][j]) > 0): #checa se foi recebida alguma informação sobre a casa                    
                    if(not("V" in mundo[i][j])): #ignora informações de casas já visitadas
                        if("M" in mundoCompartilhado[i][j]):
                            mundo[i][j] = ["M"]
                            livre[i][j] = False
                        if("L" in mundoCompartilhado[i][j]):
                            mundo[i][j] = ["L"]
                            livre[i][j] = True
                        if("P" in mundoCompartilhado[i][j]):
                            mundo[i][j] = ["P"]
                            livre[i][j] = False    
                        if("W" in mundoCompartilhado[i][j]):
                            mundo[i][j] = ["W?"] #não há como saber se há ainda um wumpus lá
                            livre[i][j] = False
                        updated[i][j] += 1 #marca a casa como atualizada
                    mundoCompartilhado[i][j] = [] #reinicia o mundoCompartilhado para uso de outras personagens
    if "I" in percepcao: #primeiro checa se há algum muro, pois se tiver a posição estará errada
        mundo[posicao[0]][posicao[1]] = ["M"]
        livre[posicao[0]][posicao[1]] = False #seta para Falso caso a casa tenha sido marcada como livre antes
        posicao[0] = (posicao[0]- orientacao[0])%N #retorna para a posição de origem
        posicao[1] = (posicao[1] - orientacao[1])%N
    for i in range(4):
        vizinho.append(mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N]) #cria a lista de vizinhos
    if "U" in percepcao and not("F" in percepcao): #checa se morreu algum wumpus nas redondezas e não há mais seu fedor. Depois, remove todos os W e W? das casas ao seu redor
        for i in range(4):
            if("W" in vizinho[i]): 
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N].remove("W")
            elif("W?" in vizinho[i]):
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N].remove("W?")
    if "F" in percepcao: #checa se há fedor nas redondezas e atualiza as casas que não tenham sido atualizadas previamente
        for i in range(4):
            if(updated[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N] == 0):
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N].append("W?")
    elif(not("U" in percepcao)): #caso não tenha Fedor nem Urro na percepção, remove de todas as casas que estão em volta qualquer indicador de Wumpus
        for i in range(4):
            if("W" in vizinho[i]):
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N].remove("W")
            elif("W?" in vizinho[i]):
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N].remove("W?")
                if(vizinho[i] == []):
                        vizinho[i] = ["L"]
                        mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N] = ["L"]
    if "B" in percepcao: #mesma lógica do condicional para F
        for i in range(4):
            if(updated[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N] == 0):
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N].append("P?")
    else: #mesmo para o else do caso F
        for i in range(4):
            if("P?" in vizinho[i]):
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N].remove("P?")
            if(vizinho[i] == []): #como esse check obrigatoriamente vem depois do de F, se uma casa estiver vazia, ela será livre (pois implica que não há fedor nem Wumpus lá
                vizinho[i] = ["L"]
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N] = ["L"]
    if(not(temPercepcao)): #caso não haja percepção recebida marca todas as adjacentes como Livres
        for i in range(4):
            if(not("V" in vizinho[i]) and vizinho[i] != ["M"]): #ignora muros conhecidos ou casas já visitadas
                mundo[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N] = ["L"]
                livre[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N] = True 
    for i in range(4): #marca todas as casas em volta da que foi realizada a ação como atualizadas
        updated[(posicao[0] + direcoes[i][0])%N][(posicao[1] + direcoes[i][1])%N] += 1
        mundo[posicao[0]][posicao[1]] = ["V"] + percepcao #marca a casa atual como visitada
    updated[posicao[0]][posicao[1]] += 1 #marca como atualizada
    livre[posicao[0]][posicao[1]] = False #marca que ela não está mais livre
    for i in range(N): #vê se é possível fazer alguma inferência garantida sobre poços ou wumpus com as informações atuais
        for j in range(N):
            if("V" in mundo[i][j]): #checa somente o entorno de casas visitadas
                somaP = 0 #vai armazenar a quantidade de Ps (sejam garantidos ou não) em volta da casa. Se só houver um, é garantido que lá há um poço
                somaW = 0 #mesmo para os Wumpus
                indiceP = []
                indiceW = []
                for k in range(4):
                    if("P" in mundo[(i + direcoes[k][0])%N][(j + direcoes[k][1])%N] or "P?" in mundo[(i + direcoes[k][0])%N][(j + direcoes[k][1])%N]):
                        somaP += 1                        
                        indiceP.append([(i + direcoes[k][0])%N, (j + direcoes[k][1])%N])
                    if("W" in mundo[(i + direcoes[k][0])%N][(j + direcoes[k][1])%N] or "W?" in mundo[(i + direcoes[k][0])%N][(j + direcoes[k][1])%N]):
                        somaW += 1
                        indiceW.append([(i + direcoes[k][0])%N, (j + direcoes[k][1])%N])
                if(somaP == 1): #caso só haja um P, é garantido que é um poço
                    mundo[indiceP[0][0]][indiceP[0][1]] = ["P"]
                if(somaW == 1): #mesmo para Wumpus. Essas condições executam mesmo que já se saiba que lá há um Wumpus, assim sempre atualizando a variável temWumpus
                    mundo[indiceW[0][0]][indiceW[0][1]] = ["W"]
                    temWumpus = True
    if(temWumpus): #vai achar a posição de um Wumpus e salvar a posição um de seus vizinhos
        for i in range(N):
            for j in range(N):
                if(mundo[i][j] == ["W"]): #checa se há um wumpus. Se tiver, salva um de seus vizinhos já visitados (é garantido que existe um pois não se recebem certezas sobre Wumpus de compartilhamentos
                    for k in range(4):
                        if "V" in mundo[(i+direcoes[k][0])%N][(j+direcoes[k][1])%N]:
                            vizinhoWumpus = [(i+direcoes[k][0])%N, (j+direcoes[k][1])%N]

        
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
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
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, lastaction, tempessoa, actionqueue, moves, dist, vizinhoWumpus
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
    if(tempessoa): #se a percepção de pessoa for verdadeira, a ação obrigatoriamente e compartilhar
        actionqueue = ["C"] 
                
    if(actionqueue != []): #caso tenham movimentos na lista de ação executa o próximo
        acao = actionqueue.pop(0)
    elif(not(tempessoa)): #caso a ação não seja compartilhar
        dist = [] 
        moves = []
        for i in range(N): #reinicia moves e dist para o proximo loop (elas dependem da casa em que se está
            linha4 = []
            linha5 = []
            for j in range(N): 
                linha4.append(float('Inf'))
                linha5.append([])
            dist.append(linha4)
            moves.append(linha5)
        bfs(posicao, orientacao) #enche a lista de movimentos e distâncias
        minlen = float('Inf')
        mindist = float('Inf') #máximo para ser usado na função min
        maxdist = -float('Inf') #minimo para ser usado na função max
        ifinal = posicao[0] #váriaveis para armazenar o destino a ser ido, caso exista. Começa com pos pois não há movimentos para ir para a própria casa (lista moves[posicao[0]][posicao[1]] é vazia
        jfinal = posicao[1]
        imax = 0
        jmax = 0
        for i in range(N): #loops para iterar em todas as casas, vendo se é possível ir para ela. Pega a casa que está mais perto e com o menor número de movimentos necessários para ser o próximo destino
            for j in range(N):
                if(dist[i][j] <= mindist and livre[i][j]): #checa se tem alguma coisa livre mais perto
                    if(len(moves[i][j]) < minlen and len(moves[i][j]) != 0): #checa se é necessário menos movimentos para se chegar a esta casa e a lista de movimentos não é vazia (caso seja a casa na posicao ou uma livre inacessível)
                       minlen = len(moves[i][j]) #atualiza o número mínimo de movimentos
                       mindist = dist[i][j] #atualiza a distância mínima
                       ifinal = i #atualiza o que vai ser passado para a actionqueue
                       jfinal = j
                if(dist[i][j] > maxdist and dist[i][j] != float('Inf')): #guarda a distância maxima que se é possivel chegar (seja ela livre ou não, mas sem se arriscar). Aqui 
                    maxdist = dist[i][j]
                    imax = i
                    jmax = j
        actionqueue = moves[ifinal][jfinal] #pega como lista de ação a casa livre mais próxima
        if(actionqueue == []): #caso não tenham casas livres 
            if(vizinhoWumpus == []): #não tenham casas livres e Wumpus não tenha vizinhos
                actionqueue = moves[imax][jmax] #vai ir para a casa mais distante. Se não encontrar outro jogador, vai ficar neste loop infinitamente.
            elif(posicao != vizinhoWumpus and vizinhoWumpus != []): #caso ainda não esteja no vizinho de Wumpus e este exista
                actionqueue = [moves[vizinhoWumpus[0]][vizinhoWumpus[1]][0]] #desta forma, para a próxima iteração actionqueue estará vazia e checará se ainda há um Wumpus
            elif(posicao == vizinhoWumpus): #caso esteja no vizinho de Wumpus
                if("W" in mundo[(posicao[0]+orientacao[0])%N][(posicao[1]+orientacao[1])%N] and nFlechas > 0): actionqueue = ["T"] #caso tenha um Wumpus na sua frente e tenha flechas, atira
                elif(nFlechas > 0): actionqueue = ["D"] #caso tenha flechas, mas não está a frente do Wumpus
                else: actionqueue = moves[imax][jmax] #não tem mais flechas, então fica numa jornada para espalhar seu conhecimento pelo mundo. Mas sempre vai voltar para o Wumpus no fim, para caso tenha um jogador lá dar a garantia da posição certa do Wumpus
        acao = actionqueue.pop(0) #pega o primeiro movimento da fila de ação para executar
    lastaction = acao #armazena a ação, para passar para planejamento() (só relevente em caso de compartilhamento)
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
    
    assert acao in ["A","D","E","T","C"]
    return acao
