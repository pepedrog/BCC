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
"""
Lista contendo as posiçõe das salas livres ainda não visitadas
"""

global amigoProximo
"""
Variável que determina a existência de algum outro personagem sendo sentido na
percepção
"""

global percurso
"""
Lista que contém o caminho a ser percorrido para chegar à uma determinada sala
livre.
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
    global N, mundo, posicao, orientacao, salasLivres, percurso
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N) :
        linha = []
        for j in range(N) :
            linha.append([]) # começa com listas vazias
        mundo.append(linha)
    salasLivres = []
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    percurso = []

def MarcaAoRedor(percepcao):
    """ Esta função marca a percepção sentida pela personagem nos locais ao seu
        redor, dependendo do tipo de percepção a marcação terá condições para
        ocorrer.
        Existe uma condicional para cada percepçção, para assim determinar seus
        casos um a um, pois existem casos nos quais uma percepção pode ser
        sentida, mas isto não faz com que ela seja válida. Como exemplo, quando
        é sentido uma brisa e fedor, porém sua personagem já havia descoberto
        em outro local que naquele lugar só poderia haver um wumpus.
        Disso decorreu a necessidade de cirar diversas condicionais, para que
        elas se anulem
    """
    # declara as variáveis globais que serão acessadas
    global posicao, orientacao, salasLivres
    pos = posicao
    ori = orientacao

    # Percepção acionada quando a personagem bate num muro, após a batida elas
    # marca a sala com um "M" indicando que lá existe um muro e logo em seguida
    # retorna a personagem para a posição na qual deveria estar (e está, sem
    # esta mudança ela apenas teria pensado que havia se movido).
    if "I" in percepcao:
        mundo[pos[0]][pos[1]] = ["M"]
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)

    # Percepção acionada quando a personagem sente uma brisa, o sinal "P?" só
    # será colocado em lugares nos quais uma sala ainda não foi explorada, é
    # livre, tem um muro ou possivelmente tem um Wumpus (pois se aquela sala
    # teve somente a percepção de um Wumpus em outro momento, ela não tem um
    # poço).
    if "B" in percepcao:
        if not("B" in mundo[pos[0]][pos[1]]):
            mundo[pos[0]][pos[1]] += ["B"]
        # Frente
        if not("V" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or \
               "M" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or \
               "L" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or \
               "P?" in mundo[(pos[0]+1)%len(mundo)][pos[1]]):
            mundo[(pos[0]+1)%len(mundo)][pos[1]] += ["P?"]
        # Trás
        if not("V" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or \
               "M" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or \
               "L" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or \
               "P?" in mundo[(pos[0]-1)%len(mundo)][pos[1]]):
            mundo[(pos[0]-1)%len(mundo)][pos[1]] += ["P?"]
        # Esquerda
        if not("V" in mundo[pos[0]][(pos[1]-1)%len(mundo)] or \
               "M" in mundo[pos[0]][(pos[1]-1)%len(mundo)] or \
               "L" in mundo[pos[0]][(pos[1]-1)%len(mundo)] or \
               "P?" in mundo[pos[0]][(pos[1]-1)%len(mundo)]):
            mundo[pos[0]][(pos[1]-1)%len(mundo)] += ["P?"]
        # Direita
        if not("V" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or \
               "M" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or \
               "L" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or \
               "P?" in mundo[pos[0]][(pos[1]+1)%len(mundo)]):
            mundo[pos[0]][(pos[1]+1)%len(mundo)] += ["P?"]

    # Percepção acionada quando a personagem sente uma fedor medonho, o sinal
    # "W?" só será colocado em lugares nos quais uma sala ainda não foi
    # explorada, é livre, tem um muro ou possivelmente tem um Wumpus (pois se
    # aquela sala teve somente a percepção de um Wumpus em outro momento, ela
    # não tem um poço).
    if "F" in percepcao:
        if not("F" in mundo[pos[0]][pos[1]]):
            mundo[pos[0]][pos[1]] += ["F"]
        # Frente
        if not("V" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or \
               "M" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or \
               "L" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or \
               "W?" in mundo[(pos[0]+1)%len(mundo)][pos[1]]):
            mundo[(pos[0]+1)%len(mundo)][pos[1]] += ["W?"]
        # Trás
        if not("V" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or \
               "M" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or \
               "L" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or \
               "W?" in mundo[(pos[0]-1)%len(mundo)][pos[1]]):
            mundo[(pos[0]-1)%len(mundo)][pos[1]] += ["W?"]
        # Esquerda
        if not("V" in mundo[pos[0]][(pos[1]-1)%len(mundo)] or \
               "M" in mundo[pos[0]][(pos[1]-1)%len(mundo)] or \
               "L" in mundo[pos[0]][(pos[1]-1)%len(mundo)] or \
               "W?" in mundo[pos[0]][(pos[1]-1)%len(mundo)]):
            mundo[pos[0]][(pos[1]-1)%len(mundo)] += ["W?"]
        # Direita
        if not("V" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or \
               "M" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or \
               "L" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or \
               "W?" in mundo[pos[0]][(pos[1]+1)%len(mundo)]):
            mundo[pos[0]][(pos[1]+1)%len(mundo)] += ["W?"]

    # Esta parte marca as salas próximas quando livres, isto ocorre quando não
    # são sentidas percepções do tipo "B" ou "F", pois assim as salas ao lado
    # são livres ou visitadas (ou um Wumpus foi morto ao lado).
    # Esta parte do código também é muito importante, pois ela cria uma lista
    # para guardar o conjunto de salas livres, para que, futuramente,
    # a personagem as visite.
    if not("B" in percepcao or "F" in percepcao):
        # Frente
        if not("V" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or \
               "M" in mundo[(pos[0]+1)%len(mundo)][pos[1]]):
            mundo[(pos[0]+1)%len(mundo)][pos[1]] = ["L"]
            if not([(pos[0]+1)%len(mundo),pos[1]] in salasLivres):
                salasLivres.extend([[(pos[0]+1)%len(mundo),pos[1]]])
        # Trás
        if not("V" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or \
               "M" in mundo[(pos[0]-1)%len(mundo)][pos[1]]):
            mundo[(pos[0]-1)%len(mundo)][pos[1]] = ["L"]
            if not([(pos[0]-1)%len(mundo),pos[1]] in salasLivres):
                salasLivres.extend([[(pos[0]-1)%len(mundo),pos[1]]])
        # Esquerda
        if not("V" in mundo[pos[0]][(pos[1]-1)%len(mundo)] or \
               "M" in mundo[pos[0]][(pos[1]-1)%len(mundo)]):
            mundo[pos[0]][(pos[1]-1)%len(mundo)] = ["L"]
            if not([pos[0],(pos[1]-1)%len(mundo)] in salasLivres):
                salasLivres.extend([[pos[0],(pos[1]-1)%len(mundo)]])
        # Direita
        if not("V" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or \
               "M" in mundo[pos[0]][(pos[1]+1)%len(mundo)]):
            mundo[pos[0]][(pos[1]+1)%len(mundo)] = ["L"]
            if not([pos[0],(pos[1]+1)%len(mundo)] in salasLivres):
                salasLivres.extend([[pos[0],(pos[1]+1)%len(mundo)]])

def verifica(i,j):
    """
        Verifica se a sala livre passada pela "mundoCompartilhado" é válida, ou
        seja, se ao lado dela existe alguma sala de "mundo" já visitada.
    """
    global mundo

    valorBool = False
    if ("V" in mundo[(i-1)%len(mundo)][j]):
        valorBool = True
    elif ("V" in mundo[(i+1)%len(mundo)][j]):
        valorBool = True
    elif ("V" in mundo[i][(j-1)%len(mundo)]):
        valorBool = True
    elif ("V" in mundo[i][(j+1)%len(mundo)]):
        valorBool = True

    return valorBool

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,salasLivres, amigoProximo
    # Atualiza representação local do mundo (na visão da personagem).
    pos = posicao
    ori = orientacao
    amigoProximo = False

    # Essa atualização abaixo serve para marcar as salas visitadas e em seguida
    # ocorre uma condicional que irá retirar as salas marcadas como livres, da
    # listas de salas vazias. Tal condicional foi implementada antes da função
    # MarcaAoRedor, pois caso fosse implementadaantes a posição da personagem
    # teria sido corrigida antes da sala ser atual ser excluída da lista
    # de salas livres (caso esta fosse uma sala antes catalogada como livre).
    if not(("B" in mundo[pos[0]][pos[1]]) or ("F" in mundo[pos[0]][pos[1]])):
        mundo[pos[0]][pos[1]] = ["V"]
    if [pos[0],pos[1]] in salasLivres:
        salasLivres.remove([pos[0],pos[1]])
    MarcaAoRedor(percepcao)
    print(salasLivres)

    # Nesta parte do código são incorporados à lista "mundo" os conhecimentos
    # compartilhados por outras personagens. O conhecimento compartilhado por
    # outras personagens só irá ser coletado quando estes forem do tipo "L",
    # para que minha prórpia personagem descubra os outros conhecimentos e apenas
    # acredite no de salas livres. Esta implementação foi feita pensando no fato
    # de que parar as personagens chegarem até as outras, estas passaram por
    # caminhos livres, de modo que suas salas visitadas e as que não exploraram
    # estarão de alguma maneira interligadas (caso não tenha havido algum erro
    # na marcação de salas livres) fazendo assim com que a minha personagem
    # possa ela mesma coletar as percepções que a outra também recebeu (por isso
    # não são coletadas as outras percepções que a).
    if percepcao != []:
        if not(percepcao[-1] == "I" or percepcao[-1] == "U" or \
               percepcao[-1] == "B" or percepcao[-1] == "F"):
               for i in range(len(mundo)):
                   for j in range(len(mundo[0])):
                       if ((mundo[i][j] == []) or ("W?" in mundo[i][j]) or \
                        ("P?" in mundo[i][j])) and ("L" in mundoCompartilhado[i][j]):
                               valorBool = verifica(i,j)
                               if valorBool:
                                   mundo[i][j] = ["L"]
                                   salasLivres.extend([[i,j]])

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
                print(end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))

    if percepcao:
        for i in range(len(percepcao)):
            if not((percepcao[i] == "B") or (percepcao[i] == "F") or \
                   (percepcao[i] == "U") or (percepcao[i] == "I")):
                amigoProximo = True

def converteNo(elemento,mundoAndavel):
    """
        Transforma listas em grafos para usar na Busca Em Largura
    """
    global mundo
    m = elemento[0] 
    n = elemento[1]
    no = []
    if ([(m+1)%len(mundo),n] in mundoAndavel):
        no.extend([(m+1)%len(mundo),n])
    if ([(m-1)%len(mundo),n] in mundoAndavel):
        no.extend([(m-1)%len(mundo),n])
    if ([m,(n+1)%len(mundo)] in mundoAndavel):
        no.extend([m,(n+1)%len(mundo)])
    if ([m,(n-1)%len(mundo)] in mundoAndavel):
        no.extend([m,(n-1)%len(mundo)])

    return no

def BuscaEmLargura(mundoAndavel,inicio,fim):
    """
        Cria uma lista vazia e a preenche com as "coordenadas" de salas vazias
        e livres, para que assim seja montado um caminho até a sala livre destinada.
    """
    explorado = []
    caminhos = [[inicio]]
    while caminhos:
        # Tira o primeiro item de caminho e coloca em caminho
        caminho = caminhos.pop(0)
        # get the last node from the path
        no = caminho[-1]
        if no not in explorado:
            vizinhos = converteNo(no,mundoAndavel)
            # Percorre todos os nós vizinhos e constrói um novo caminho
            for vizinho in vizinhos:
                percurso = list(caminho)
                percurso.append(vizinho)
                if vizinho == fim:
                    return percurso
            explorado.append(no)
    return percurso

def caminha():
    """
        #Nessa função será criado o caminho que a personagem irá usar para
        #chegar até às salas livres. Para que a função funcione de maneira correta
        #a informação recebida pelas outras personagens deve estar correta (a única
        #informação que é recebida é a das salas livres), ou a personagem tentará
        #percorrer caminhos impossíveis.
    """
    global mundo, salasLivres, percurso, posicao, orientacao, N
    pos = posicao
    ori = orientacao

    if [pos[0],pos[1]] in percurso:
        percurso.remove([pos[0],pos[1]])
    # Caso a lista percurso não seja vazia a condicional é acionada e caso a
    # posição na frente da personagem seja a próxima sala a ser visitada, ação
    # retornada é "A"; caso não seja o personagem gira pra esquerda até ficar
    # na frente dessa posição.
    if percurso:
        if((pos[0]+ori[0])%len(mundo) == percurso[0][0]) and ((pos[1]+ori[1])%len(mundo) == percurso[0][1]):
            acao = "A"
        else:
            acao = "E"
    # Caso a lista percurso esteja vazia, a função busca irá criar um percurso
    # do local atual até a casa livre com as coordenadas em salasLivres[0]
    if not percurso:
        # cria a lista para representar o mundo no qual a personagem pode
        # andar sem tomar passos arriscados.
        mundoAndavel = []
        # Cria uma matriz que consiste apenas nos caminhos "seguros" dos quais a
        # personagem poderá utilizar para chegar até a sala livre na posição
        # salasLivres[0].
        for i in range(N):
            for j in range(N):
                if ("V" in mundo[i][j]):
                    mundoAndavel.append([i,j])
        percurso = BuscaEmLargura(mundoAndavel,pos,salasLivres)

    assert acao in ["A","D","E","T","C"]
    return acao


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"= Andar, "D"= Girar Direita, "E"= Girar Esquerda,
        "T"= ATirar e "C"= Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,amigoProximo, salasLivres
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

    pos = posicao
    ori = orientacao

    # Toda vez que uma personagem estiver disponível para compartilhar informação
    # com a minha personagem, ela irá fazê-lo.
    if amigoProximo:
           acao = "C"
    # Caso as salas livres tenham acabado, a personagem irá girar para esquerda
    # até falar com outra personagem para obter mais informações sobre outras
    # salas livres (caso existam).
    elif not salasLivres:
            acao = "E"
    else:
        acao = caminha(mundo,salasLivres)

    # Possível resultado das ações resultantes dos laços acima
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
