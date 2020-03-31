# flag para depuração
__DEBUG__ = True


# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global nFlechas
"""
Número de flechas que a personagem possui. Serve apenas para
consulta da personagem, pois o mundo mantém uma cópia "segura" dessa
informação (não tente inventar flechas...).
"""

# CHAMADA DE UMA PERCEPÇÃO A SER UTILIZADA NA ATUALIZAÇÃO DO MAPA
global percepcaoG

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
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N):
        linha = []
        for j in range(N):
            linha.append([])  # começa com listas vazias
        mundo.append(linha)
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0, 0]
    orientacao = [1, 0]


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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, percepcaoG
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).

    percepcaoG = percepcao

    pos = posicao
    ori = orientacao
    mapainterno = []
    for i in range(N):
        largura = []
        for j in range(N):
            largura.append([])
        mapainterno.append(largura)
    # CRIAÇÃO DE UM MAPA INTERNO PARA DECIDIR QUAL PROXIMO MOVIMENTO É MAIS ADEQUADO A SITUAÇÃO
    for m in range(0, N):
        for n in range(0, N):
            if "L" and "W?" and "M" and "V" not in mundo[m][n]:
                mapainterno[m][n] = -2
            if "L" in mundo[m][n]:
                mapainterno[m][n] = 4
            if "W?" in mundo[m][n]:
                mapainterno[m][n] = 1
            if "P?" in mundo[m][n]:
                mapainterno[m][n] = 1
            if "M" in mundo[m][n]:
                mapainterno[m][n] = -3
            if "V" in mundo[m][n]:
                mapainterno[m][n] = 3
            if "V" in mundo[(pos[0]-ori[0]) % len(mundo)][(pos[1]-ori[1]) % len(mundo)]:
                mapainterno[(pos[0]-ori[0]) % len(mundo)
                            ][(pos[1]-ori[1]) % len(mundo)] = 2

    # TODOS OS ALERTAS ABAIXO FORAM IMPLEMENTADOS NAS POSIÇÕES MANUALMENTE, POR ISSO ELE FICOU TÃO EXTENSO(PODERIA TER SIDO EVITADO AO COLOCAR ALGUMAS FUNÇÕES QUE SE REPETEM COMO UMA VARIAVEL UNICA:/)
    # PERCEPÇÃO DE MUROS
    if "I" in percepcao:
        if ori == [1, 0]:  # SUL v
            pos[0] = (pos[0]-1) % len(mundo)
            mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) %
                   len(mundo)] = ["M"]
        if ori == [-1, 0]:  # NORTE ^
            pos[0] = (pos[0]+1) % len(mundo)
            mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) %
                   len(mundo)] = ["M"]
        if ori == [0, 1]:  # LESTE ->
            pos[1] = (pos[1]-1) % len(mundo)
            mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) %
                   len(mundo)] = ["M"]
        if ori == [0, -1]:  # OESSSSSSSSSSSSSSSSSSSSSTE <-
            pos[1] = (pos[1]+1) % len(mundo)
            mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) %
                   len(mundo)] = ["M"]

    # POSSIBILIDADE DE UM POÇO PROXIMO, ALERTANDO AS LATERAIS IMEDIATAS
    if "B" in percepcao and "F" not in percepcao:

        if ori == [1, 0] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # SUL v
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][(pos[1])]:
                mundo[(pos[0]+1) % len(mundo)][(pos[1])] = ["P?"]
            if "L" and "V" and "M" not in mundo[(pos[0])][(pos[1]+1) % len(mundo)]:
                mundo[(pos[0])][(pos[1]+1) % len(mundo)] = ["P?"]
            if "L" and "V" and "M" not in mundo[(pos[0])][(pos[1]-1) % len(mundo)]:
                mundo[(pos[0])][(pos[1]-1) % len(mundo)] = ["P?"]
        if ori == [0, 1] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # LESTE ->
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][pos[1]]:
                mundo[(pos[0]+1) % len(mundo)][pos[1]] = ["P?"]
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["P?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]+1) % len(mundo)]:
                mundo[pos[0]][(pos[1]+1) % len(mundo)] = ["P?"]
        if ori == [-1, 0] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # NORTE ^
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["P?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]+1) % len(mundo)]:
                mundo[pos[0]][(pos[1]+1) % len(mundo)] = ["P?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]-1) % len(mundo)]:
                mundo[pos[0]][(pos[1]-1) % len(mundo)] = ["P?"]
        if ori == [0, -1] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # OESSSSSSSSSSSSSSSSSSSSSTE <-
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["P?"]
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][pos[1]]:
                mundo[(pos[0]+1) % len(mundo)][pos[1]] = ["P?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]-1) % len(mundo)]:
                mundo[pos[0]][(pos[1]-1) % len(mundo)] = ["P?"]

    # POSSIBILIDADE DE UM WUMPUS PROXIMO, ALERTANDO AS LATERAIS IMEDIATAS
    if "F" in percepcao and "B" not in percepcao:

        if ori == [1, 0] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # SUL v
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][(pos[1])]:
                mundo[(pos[0]+1) % len(mundo)][(pos[1])] = ["W?"]
            if "L" and "V" and "M" not in mundo[(pos[0])][(pos[1]+1) % len(mundo)]:
                mundo[(pos[0])][(pos[1]+1) % len(mundo)] = ["W?"]
            if "L" and "V" and "M" not in mundo[(pos[0])][(pos[1]-1) % len(mundo)]:
                mundo[(pos[0])][(pos[1]-1) % len(mundo)] = ["W?"]
        if ori == [0, 1] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # LESTE ->
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][pos[1]]:
                mundo[(pos[0]+1) % len(mundo)][pos[1]] = ["W?"]
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]+1) % len(mundo)]:
                mundo[pos[0]][(pos[1]+1) % len(mundo)] = ["W?"]
        if ori == [-1, 0] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # NORTE ^
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]+1) % len(mundo)]:
                mundo[pos[0]][(pos[1]+1) % len(mundo)] = ["W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]-1) % len(mundo)]:
                mundo[pos[0]][(pos[1]-1) % len(mundo)] = ["W?"]
        if ori == [0, -1] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # OESSSSSSSSSSSSSSSSSSSSSTE <-
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["W?"]
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][pos[1]]:
                mundo[(pos[0]+1) % len(mundo)][pos[1]] = ["W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]-1) % len(mundo)]:
                mundo[pos[0]][(pos[1]-1) % len(mundo)] = ["W?"]

    # POSSIVEL MONSTRO/POÇO(RECEBER AS DUAS OPÇÕES AO MESMO TEMPO)
    if "F" in percepcao and "B" in percepcao:

        if ori == [1, 0] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # SUL v
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][(pos[1])]:
                mundo[(pos[0]+1) % len(mundo)][(pos[1])] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[(pos[0])][(pos[1]+1) % len(mundo)]:
                mundo[(pos[0])][(pos[1]+1) % len(mundo)] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[(pos[0])][(pos[1]-1) % len(mundo)]:
                mundo[(pos[0])][(pos[1]-1) % len(mundo)] = ["P?/W?"]
        if ori == [0, 1] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # LESTE ->
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][pos[1]]:
                mundo[(pos[0]+1) % len(mundo)][pos[1]] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]+1) % len(mundo)]:
                mundo[pos[0]][(pos[1]+1) % len(mundo)] = ["P?/W?"]
        if ori == [-1, 0] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # NORTE ^
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]+1) % len(mundo)]:
                mundo[pos[0]][(pos[1]+1) % len(mundo)] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]-1) % len(mundo)]:
                mundo[pos[0]][(pos[1]-1) % len(mundo)] = ["P?/W?"]
        if ori == [0, -1] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["M"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["W?"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["L"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["V"] and mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] != ["P?/W?"]:  # OESSSSSSSSSSSSSSSSSSSSSTE <-
            if "L" and "V" and "M" not in mundo[(pos[0]-1) % len(mundo)][pos[1]]:
                mundo[(pos[0]-1) % len(mundo)][pos[1]] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[(pos[0]+1) % len(mundo)][pos[1]]:
                mundo[(pos[0]+1) % len(mundo)][pos[1]] = ["P?/W?"]
            if "L" and "V" and "M" not in mundo[pos[0]][(pos[1]-1) % len(mundo)]:
                mundo[pos[0]][(pos[1]-1) % len(mundo)] = ["P?/W?"]

    # AREAS LIVRES
    if "F" not in percepcao and "B" not in percepcao and "I" not in percepcao :
        if "V" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
            if  "M" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                mundo[(pos[0]+1)%len(mundo)][pos[1]] = ["L"]
        if "V" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
            if  "M" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                mundo[(pos[0]-1)%len(mundo)][pos[1]] = ["L"]
        if "V" not in mundo[pos[0]][(pos[1]+1)%len(mundo)]:
            if  "M" not in mundo[pos[0]][(pos[1]+1)%len(mundo)]:
                mundo[pos[0]][(pos[1]+1)%len(mundo)] = ["L"]
        if "V" not in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
            if  "M" not in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
                mundo[pos[0]][(pos[1]-1)%len(mundo)] = ["L"]

         

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
    #
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
                if pos == [i, j]:
                    if ori == [0, -1]:
                        print("<", end="")
                    print("X", end="")
                    if ori == [0, 1]:
                        print(">", end="")
                    if ori == [1, 0]:
                        print("v", end="")
                    if ori == [-1, 0]:
                        print("^", end="")
                print("".join(mundo[i][j]), end="")
                print("".join(mundoCompartilhado[i][j]), end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=atirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, percepcaoG
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
    mapainterno = []
    for i in range(N):
        largura = []
        for j in range(N):
            largura.append([])
        mapainterno.append(largura)
    # CRIAÇÃO DE UM MAPA INTERNO PARA DECIDIR QUAL PROXIMO MOVIMENTO É MAIS ADEQUADO A SITUAÇÃO
    for m in range(0, N):
        for n in range(0, N):
            if "L" and "W?" and "M" and "V" not in mundo[m][n]:
                mapainterno[m][n] = -2
            if "L" in mundo[m][n]:
                mapainterno[m][n] = 4
            if "W?" in mundo[m][n]:
                mapainterno[m][n] = 1
            if "P?" in mundo[m][n]:
                mapainterno[m][n] = 1
            if "M" in mundo[m][n]:
                mapainterno[m][n] = -3
            if "V" in mundo[m][n]:
                mapainterno[m][n] = 3
            if "V" in mundo[(pos[0]-ori[0]) % len(mundo)][(pos[1]-ori[1]) % len(mundo)]:
                mapainterno[(pos[0]-ori[0]) % len(mundo)
                            ][(pos[1]-ori[1]) % len(mundo)] = 2

    # CONDIÇÕES DE MOVIMENTO
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]+1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]-1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]) % len(mundo)][(pos[1]+1) % len(mundo)]:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]+1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]-1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]) % len(mundo)][(pos[1]-1) % len(mundo)]:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]+1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]) % len(mundo)][(pos[1]+1) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]) % len(mundo)][(pos[1]-1) % len(mundo)]:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]-1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]) % len(mundo)][(pos[1]+1) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > mapainterno[(pos[0]) % len(mundo)][(pos[1]-1) % len(mundo)]:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]+1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]-1) % len(mundo)][(pos[1]) % len(mundo)] or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]+1) % len(mundo)] and mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]-1) % len(mundo)]:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]+1) % len(mundo)][(pos[1]) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]-1) % len(mundo)][(pos[1]) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]+1) % len(mundo)] > 1:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]+1) % len(mundo)][(pos[1]) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]-1) % len(mundo)][(pos[1]) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]-1) % len(mundo)] > 1:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]+1) % len(mundo)][(pos[1]) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]+1) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]-1) % len(mundo)] > 1:
        acao = "A"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]-1) % len(mundo)][(pos[1]) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]+1) % len(mundo)] > 1 or mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]) % len(mundo)][(pos[1]-1) % len(mundo)] > 1:
        acao = "A"

    # PROCURANDO LOCAIS NA QUAL É SEGURO ANDAR
    if "V" and "L" not in mundo[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)]:
        if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] < mapainterno[(pos[0]+1) % len(mundo)][pos[1]]:
            acao = "E"
        if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] < mapainterno[(pos[0]-1) % len(mundo)][pos[1]]:
            acao = "E"
        if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] < mapainterno[pos[0]][(pos[1]+1) % len(mundo)]:
            acao = "E"
        if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] < mapainterno[pos[0]][(pos[1]-1) % len(mundo)]:
            acao = "E"
    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == -1:
        acao = "T"

    # COMPARTILHAMENTO
    percepcoespossiveis = [["I"], ["F"], ["B"], ['B', 'F'], ['B', 'I'], ['F', 'I']]
    if percepcaoG not in percepcoespossiveis and percepcaoG != []:
        acao = "C"

    # ATUALIZAÇÃO DO MAPA INTERNO COM O COMPARTILHADO
    for u in range(0, N):
        for f in range(0, N):
            if 'L' in mundoCompartilhado[u][f]:
                if "V" not in mundo[u][f]:
                    mapainterno[u][f] = 4
            if 'W' in mundoCompartilhado[u][f]:
                mapainterno[u][f] = -1
            if 'P' in mundoCompartilhado[u][f]:
                mapainterno[u][f] = 1
            if 'M' in mundoCompartilhado[u][f]:
                mapainterno[u][f] = -3
            if 'V' in mundoCompartilhado[u][f]:
                mapainterno[u][f] = 3
    for k in range(0, N):
        for h in range(0, N):
            if mapainterno[k][h] == 4:
                mundo[k][h] = ["L"]


    # CALCULO DE DISTANCIAS ENTRE COORDENADAS
    contador_sul = N
    contador_norte = N
    contador_leste = N
    contador_oeste = N
    distancia_norte = 0
    distancia_sul = 0
    distancia_leste = 0
    distancia_oeste = 0
    while contador_sul != 0:
        if mapainterno[(pos[0]+contador_sul) % len(mundo)][pos[1]] != 1:
            distancia_sul = distancia_sul+1
        if mapainterno[(pos[0]+contador_sul) % len(mundo)][pos[1]] == 1:
            break
        if mapainterno[(pos[0]+contador_sul) % len(mundo)][pos[1]] == -2:
            break
        if mapainterno[(pos[0]+contador_sul) % len(mundo)][pos[1]] == -3:
            break
        contador_sul = contador_sul - 1
    while contador_norte != 0:
        if mapainterno[(pos[0]-contador_norte) % len(mundo)][pos[1]] != 1:
            distancia_norte = distancia_norte+1
        if mapainterno[(pos[0]-contador_norte) % len(mundo)][pos[1]] == 1:
            break
        if mapainterno[(pos[0]-contador_norte) % len(mundo)][pos[1]] == -2:
            break
        if mapainterno[(pos[0]-contador_norte) % len(mundo)][pos[1]] == -3:
            break
        contador_norte = contador_norte - 1
    while contador_leste != 0:
        if mapainterno[pos[0]][(pos[1] + contador_leste) % len(mundo)] != 1:
            distancia_leste = distancia_leste+1
        if mapainterno[pos[0]][(pos[1] + contador_leste) % len(mundo)] == 1:
            break
        if mapainterno[pos[0]][(pos[1] + contador_leste) % len(mundo)] == -2:
            break
        if mapainterno[pos[0]][(pos[1] + contador_leste) % len(mundo)] == -3:
            break
        contador_leste = contador_leste - 1
    while contador_oeste != 0:
        if mapainterno[pos[0]][(pos[1] + contador_oeste) % len(mundo)] != 1:
            distancia_oeste = distancia_oeste+1
        if mapainterno[pos[0]][(pos[1] + contador_oeste) % len(mundo)] == 1:
            break
        if mapainterno[pos[0]][(pos[1] + contador_oeste) % len(mundo)] == -2:
            break
        if mapainterno[pos[0]][(pos[1] + contador_oeste) % len(mundo)] == -3:
            break
        contador_oeste = contador_oeste - 1

    if mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] == mapainterno[(pos[0]-ori[0]) % len(mundo)][(pos[1]-ori[1]) % len(mundo)] and mapainterno[(pos[0]+ori[0]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 1:
        if distancia_norte > distancia_sul and distancia_norte > distancia_leste and distancia_norte > distancia_oeste and ori == [-1, 0] and distancia_norte != 0:
            acao = "A"
        if distancia_norte > distancia_sul and distancia_norte > distancia_leste and distancia_norte > distancia_oeste and ori == [0, 1]and distancia_norte != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "E"
        if distancia_norte > distancia_sul and distancia_norte > distancia_leste and distancia_norte > distancia_oeste and ori == [0, -1]and distancia_norte != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "D"
        if distancia_norte > distancia_sul and distancia_norte > distancia_leste and distancia_norte > distancia_oeste and ori == [1, 0]and distancia_norte != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "E"

        if distancia_sul > distancia_norte and distancia_sul > distancia_leste and distancia_sul > distancia_oeste and ori == [1, 0]and distancia_sul != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "A"
        if distancia_sul > distancia_norte and distancia_sul > distancia_leste and distancia_sul > distancia_oeste and ori == [0, 1]and distancia_sul != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "D"
        if distancia_sul > distancia_norte and distancia_sul > distancia_leste and distancia_sul > distancia_oeste and ori == [0, -1]and distancia_sul != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "E"
        if distancia_sul > distancia_norte and distancia_sul > distancia_leste and distancia_sul > distancia_oeste and ori == [-1, 0]and distancia_sul != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "E"

        if distancia_leste > distancia_norte and distancia_sul < distancia_leste and distancia_leste > distancia_oeste and ori == [1, 0]and distancia_leste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "E"
        if distancia_leste > distancia_norte and distancia_sul < distancia_leste and distancia_leste > distancia_oeste and ori == [0, 1]and distancia_leste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "A"
        if distancia_leste > distancia_norte and distancia_sul < distancia_leste and distancia_leste > distancia_oeste and ori == [0, -1]and distancia_leste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "D"
        if distancia_leste > distancia_norte and distancia_sul < distancia_leste and distancia_leste > distancia_oeste and ori == [-1, 0]and distancia_leste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "E"

        if distancia_oeste > distancia_norte and distancia_oeste > distancia_leste and distancia_sul < distancia_oeste and ori == [1, 0]and distancia_oeste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao = "D"
        if distancia_oeste > distancia_norte and distancia_oeste > distancia_leste and distancia_sul < distancia_oeste and ori == [0, 1]and distancia_oeste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao= "E"
        if distancia_oeste > distancia_norte and distancia_oeste > distancia_leste and distancia_sul < distancia_oeste and ori == [0, -1]and distancia_oeste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao= "A"
        if distancia_oeste > distancia_norte and distancia_oeste > distancia_leste and distancia_sul < distancia_oeste and ori == [-1, 0]and distancia_oeste != 0 and mapainterno[(pos[0]+ori[1]) % len(mundo)][(pos[1]+ori[1]) % len(mundo)] > 0:
            acao= "E"

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo é uma pseudo-implementação, pois recebe
    # a ação através de uma pergunta dirigida ao usuário.
    # No código a ser entregue, você deve programar algum tipo
    # de estratégia para

    # ATENÇÃO: a atualizacao abaixo está errada!!!
    # Não checa se o movimento foi possível ou não... isso só dá para
    # saber quando chegar uma percepção nova (a percepção "I"
    # diz que o movimento anterior não foi possível).

    if acao == "A":
        pos[0]= (pos[0]+ori[0]) % len(mundo)
        pos[1]= (pos[1]+ori[1]) % len(mundo)
    if acao == "E":
        if ori[0] == 0:
            ori[1]= -ori[1]
        ori[0], ori[1]= ori[1], ori[0]
    if acao == "D":
        if ori[1] == 0:
            ori[0]= -ori[0]
        ori[0], ori[1]= ori[1], ori[0]
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

    assert acao in ["A", "D", "E", "T", "C"]
    return acao
