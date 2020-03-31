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

global pos_anterior
"""
Guarda a posição anterior do jogador, pois caso bata em algum muro
ele deve voltar para onde estava.
"""

global percepcao_atual
"""
Armazena a percepção recebida pelo jogador para que seja possivel
usar tanto no momento de planejar como no momento de agir
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
    global N, mundo, posicao, orientacao, pos_anterior, percepcao_atual
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
    pos_anterior = [-1, -1]
    orientacao = [1,0]
    percepcao_atual = []


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
    global mundo,N, posicao, orientacao, nFlechas, mundoCompartilhado, pos_anterior, percepcao_atual
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

    percepcao_atual = percepcao[:]

    if "I" in percepcao:
        mundo[posicao[0]][posicao[1]] = ["M"]
        posicao = pos_anterior
    
    if percepcao == []:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j):
                    cordenadaX = (posicao[0] + i) % N
                    cordenadaY = (posicao[1] + j) % N
                    if "L" not in mundo[cordenadaX][cordenadaY]\
                        and "M" not in mundo[cordenadaX][cordenadaY]\
                        and "V" not in mundo[cordenadaX][cordenadaY]:

                        mundo[cordenadaX][cordenadaY].append("L")
    
    if "B" in percepcao:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j):
                    cordenadaX = (posicao[0] + i) % N
                    cordenadaY = (posicao[1] + j) % N
                    if "B?" not in mundo[cordenadaX][cordenadaY] \
                        and "V" not in mundo[cordenadaX][cordenadaY] \
                        and "L" not in mundo[cordenadaX][cordenadaY]:

                        mundo[cordenadaX][cordenadaY].append("B?")

    if "F" in percepcao:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j):
                    cordenadaX = (posicao[0] + i) % N
                    cordenadaY = (posicao[1] + j) % N
                    if "F?" not in mundo[cordenadaX][cordenadaY] \
                        and "V" not in mundo[cordenadaX][cordenadaY] \
                        and "L" not in mundo[cordenadaX][cordenadaY]:

                        mundo[cordenadaX][cordenadaY].append("F?")
    
    if "W" in percepcao:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j):
                    cordenadaX = (posicao[0] + i) % N
                    cordenadaY = (posicao[1] + j) % N
                    if "W?" not in mundo[cordenadaX][cordenadaY] \
                        and "V" not in mundo[cordenadaX][cordenadaY] \
                        and "L" not in mundo[cordenadaX][cordenadaY]:
                        mundo[cordenadaX][cordenadaY].append("W?")


    # essa atualização abaixo serve de ilustração/exemplo, e
    # apenas marca as salas como "Visitadas", mas está errada
    pos = posicao
    ori = orientacao
    mundo[pos[0]][pos[1]] = ["V"]

    if __DEBUG__:
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, pos_anterior, percepcao_atual
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

    nova_posicao = obterNovaPosicao(mundo, mundoCompartilhado, pos)
    if __DEBUG__:
        print("Posição atual:", pos)
        print("Nova posição encontrada:", nova_posicao)
        print("O que há na nova posição no nosso mundo:", mundo[nova_posicao[0] % N][nova_posicao[1] % N])
        print("O que há na nova posição no mundo compartilhado:", mundoCompartilhado[nova_posicao[0] % N][nova_posicao[1] % N])

    if (pos[0] + ori[0]) % N == nova_posicao[0] % N and (pos[1] + ori[1]) % N == nova_posicao[1] % N:
        posicaoWumpusInferida = infereWumpus(mundo, mundoCompartilhado, pos)
        if "W" in mundo[(pos[0] + ori[0]) % N][(pos[1] + ori[1]) % N] \
            or "W" in mundoCompartilhado[(pos[0] + ori[0]) % N][(pos[1] + ori[1]) % N] \
            or posicaoWumpusInferida is not None:
            acao = "T"    
        else:
            acao = "A"
    else:
        acao = "D"

    if "Dummy" in percepcao_atual:
        acao = "C"

    if acao=="A":
        pos_anterior = [pos[0], pos[1]]
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
    
    if __DEBUG__:
        print("acao:", acao)
        print("========================Fim da instrução===============================")
    assert acao in ["A","D","E","T","C"]
    return acao

def obterNovaPosicao(mundo, mundoCompartilhado, pos):
    N = len(mundo)

    #Caso tenha um Wumpus na redondeza, retorna essa posição para que seja morto
    posicaoDoWumpus = encontraWumpus(mundo, mundoCompartilhado, pos)
    if posicaoDoWumpus is not None:
        return posicaoDoWumpus

    #Caso seja possivel inferir onde esta o Wumpus, enviar tal cordenada
    posicaoInferidaDoWumpus = infereWumpus(mundo, mundoCompartilhado, pos)
    if posicaoInferidaDoWumpus is not None:
        if __DEBUG__:
            print("Inferi uma posição para o Wumpus.")
        return posicaoInferidaDoWumpus
    
    # Verifica se alguma casa ao redor esta livre e não foi visitada
    casaLivre = encontraCasaLivreENaoVisitada(mundo, mundoCompartilhado, pos)
    if casaLivre is not None:
        return casaLivre

    ## Retorna para alguma posição visitada em segurança
    casaVisitada = encontraPosicaoVisitada(mundo, mundoCompartilhado, pos)
    if casaVisitada is not None:
        return casaVisitada
    
    #Vamos andar para um lugar que tenha brisa, mas até onde
    #sabemos não há um bueiro, e tambem não ir se sabemos que há muro
    pocoParaArriscar = encontraPocoParaArriscar(mundo, mundoCompartilhado, pos)
    if pocoParaArriscar is not None:
        return pocoParaArriscar

def infereWumpus(mundo, mundoCompartilhado, pos):
    N = len(mundo)
    if ("L" in mundo[(pos[0] - 1) % N][(pos[1] + 0) % N] \
            or "L" in mundoCompartilhado[(pos[0] - 1) % N][(pos[1] + 0) % N]) \
        and ("M" in mundo[(pos[0] + 0) % N][(pos[1] - 1) % N] \
            or "M" in mundoCompartilhado[(pos[0] + 0) % N][(pos[1] - 1) % N]) \
        and ("P" in mundo[(pos[0] + 0) % N][(pos[1] + 1) % N] \
            or "P" in mundoCompartilhado[(pos[0] + 0) % N][(pos[1] + 1) % N]):
        return [(pos[0] + 1) % N, (pos[1] + 0) % N]
    else:
        return None

def encontraCasaLivreENaoVisitada(mundo, mundoCompartilhado, pos):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                cordenadaX = (pos[0] + i) % N
                cordenadaY = (pos[1] + j) % N
                if ("L" in mundo[cordenadaX][cordenadaY] \
                    or "L" in mundoCompartilhado[cordenadaX][cordenadaY]) \
                    and "M" not in mundo[cordenadaX][cordenadaY] \
                    and "V" not in mundo[cordenadaX][cordenadaY]:
                    return [cordenadaX, cordenadaY]
    return None

def encontraPosicaoVisitada(mundo, mundoCompartilhado, pos):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                cordenadaX = (pos[0] + i) % N
                cordenadaY = (pos[1] + j) % N
                if "V" in mundo[cordenadaX][cordenadaY]:
                    return [cordenadaX, cordenadaY]
    return None

def encontraPocoParaArriscar(mundo, mundoCompartilhado, pos):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                cordenadaX = (pos[0] + i) % N
                cordenadaY = (pos[1] + j) % N
                if "B?" in mundo[cordenadaX][cordenadaY] \
                    and "M" not in mundo[cordenadaX][cordenadaY] \
                    and "P" not in mundo[cordenadaX][cordenadaY]:
                    return [cordenadaX, cordenadaY]
    return None

def encontraWumpus(mundo, mundoCompartilhado, pos):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                cordenadaX = (pos[0] + i) % N
                cordenadaY = (pos[1] + j) % N
                if "W" in mundo[cordenadaX][cordenadaY] \
                    or "W" in mundoCompartilhado[cordenadaX][cordenadaY]:
                    return [cordenadaX, cordenadaY]
    return None
