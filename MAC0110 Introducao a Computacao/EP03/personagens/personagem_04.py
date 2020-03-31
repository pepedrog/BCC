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

global salasLivres # Lista de salas livres e não visitadas
global acao # Última ação realizada
global sensacao # Última percepção recebida
global semWumpus # Lista de salas que não têm Wumpus
global pos # Posição atual do personagem
global ori # Orientação atual do personagem
global direcao # Auxilia na determinação da próxima ação quando a string de percepção é vazia

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, salasLivres, acao, sensacao, semWumpus, direcao
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

    salasLivres = []
    acao = ""
    sensacao = []
    semWumpus = []
    direcao = 1

""" Identifica as salas livres/visitadas
"""
def planejar_livre2(lin, col):
    global salasLivres, mundo

    if "V" in mundo[lin][col]:
        if [lin, col] in salasLivres:
            salasLivres.remove([lin, col])
    else:
        mundo[lin][col] = ["L"]
        if [lin, col] not in salasLivres:
            salasLivres.append([lin, col])

""" Determina as salas que serão verificadas em planejar_livre2() """
def planejar_livre():
    global mundo, pos

    planejar_livre2(pos[0], (pos[1]-1)%len(mundo))
    planejar_livre2(pos[0], (pos[1]+1)%len(mundo))
    planejar_livre2((pos[0]+1)%len(mundo), pos[1])
    planejar_livre2((pos[0]-1)%len(mundo), pos[1])

""" Identifica as salas muradas """
def planejar_I():
    global mundo, pos, ori

    lin = -1
    col = -1

    if ori==[0,-1]:
        mundo[pos[0]][(pos[1]-1)%len(mundo)] = ["M", "V"]
        lin = pos[0]
        col = (pos[1]-1)%len(mundo)
    elif ori==[0,1]:
        mundo[pos[0]][(pos[1]+1)%len(mundo)] = ["M", "V"]
        lin = pos[0]
        col = (pos[1]+1)%len(mundo)
    elif ori==[1,0]:
        mundo[(pos[0]+1)%len(mundo)][pos[1]] = ["M", "V"]
        lin = (pos[0]+1)%len(mundo)
        col = pos[1]
    elif ori==[-1,0]:
        mundo[(pos[0]-1)%len(mundo)][pos[1]] = ["M", "V"]
        lin = (pos[0]-1)%len(mundo)
        col = pos[1]
    planejar_livre2(lin, col)

""" Identifica as salas com possíveis Wumpus """
def planejar_F2(lin, col):
    global mundo, semWumpus

    sala = mundo[lin][col]
    if "L" not in sala and "V" not in sala and "W?" not in sala and \
        [lin, col] not in semWumpus:
        mundo[lin][col].append("W?")

""" Determina as salas que serão verificadas em planejar_F2() """
def planejar_F():
    global mundo, pos

    planejar_F2(pos[0], (pos[1]-1)%len(mundo))
    planejar_F2(pos[0], (pos[1]+1)%len(mundo))
    planejar_F2((pos[0]+1)%len(mundo), pos[1])
    planejar_F2((pos[0]-1)%len(mundo), pos[1])

""" Identifica as salas com possíveis poços """
def planejar_B2(lin, col):
    global mundo

    sala = mundo[lin][col]
    if "L" not in sala and "V" not in sala and "P?" not in sala:
        mundo[lin][col].append("P?")

""" Determina as salas que serão verificadas em planejar_B2() """
def planejar_B():
    global mundo, pos

    planejar_B2(pos[0], (pos[1]-1)%len(mundo))
    planejar_B2(pos[0], (pos[1]+1)%len(mundo))
    planejar_B2((pos[0]+1)%len(mundo), pos[1])
    planejar_B2((pos[0]-1)%len(mundo), pos[1])

""" Incorpora mundos ao mundo de personagem8515986 """
def incorporar_mundo_compartilhado():
    global mundo, mundoCompartilhado, semWumpus

    for i in range (len(mundo)):
        for j in range (len(mundo[0])):
            for k in mundoCompartilhado[i][j]:
                sala = mundo[i][j]
                if k+"?" not in sala and "L" not in sala and "V" not in sala:
                    if k+"?" == "W?" and [i, j] in semWumpus:
                        continue
                    mundo[i][j].append(k+"?")

""" Imprime o mundo de personagem8515986 """
def imprime(percepcao):
    global mundo, salasLivres, semWumpus, pos, ori

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
            print("",end="\t| ")
        print("\n"+"-"*(8*len(mundo)+1))
    print(salasLivres)
    print(semWumpus)

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, acao, sencacao, semWumpus, pos, ori
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
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        pos = posicao
        ori = orientacao
        if "I" not in percepcao:
            mundo[pos[0]][pos[1]] = ["V"]
            if acao == "A":
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                mundo[pos[0]][pos[1]] = ["V"]
        else:
            if ori==[0,-1]:
                mundo[pos[0]][(pos[1]-1)%len(mundo)] = ["M"]
            elif ori==[0,1]:
                mundo[pos[0]][(pos[1]+1)%len(mundo)] = ["M"]
            elif ori==[1,0]:
                mundo[(pos[0]+1)%len(mundo)][pos[1]] = ["M"]
            elif ori==[-1,0]:
                mundo[(pos[0]-1)%len(mundo)][pos[1]] = ["M"]

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
    else:
        pos = posicao
        ori = orientacao
        atualizar_sensacao(percepcao)

        if "I" in percepcao:
            planejar_I()
        else:
            mundo[pos[0]][pos[1]] = ["V"]
            planejar_livre2(pos[0], pos[1])
            if acao == "A":
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                mundo[pos[0]][pos[1]] = ["V"]
                planejar_livre2(pos[0], pos[1])
            elif acao == "T":
                lin = (pos[0]+ori[0])%len(mundo)
                col = (pos[1]+ori[1])%len(mundo)
                if "U" in percepcao:
                    planejar_livre2(lin, col)
                elif "W?" in mundo[lin][col]:
                    mundo[lin][col].remove("W?")
                    semWumpus.append([lin, col])
            elif acao == "C":
                incorporar_mundo_compartilhado()

            if "F" in percepcao:
                planejar_F()
            if "B" in percepcao:
                planejar_B()
            if "F" not in percepcao and "B" not in percepcao:
                planejar_livre()

    #UTILIZADO APENAS NA DEPURAÇÃO:
    #imprime(percepcao)
    #resp = str(input("Parada: "))

""" Atualiza a variável global que armazena a última percepção recebida """
def atualizar_sensacao(percepcao):
    global sensacao
    sensacao = percepcao

""" Vira o personagem à direita """
def virar_direita():
    global ori

    if ori[1]==0:
        ori[0] = -ori[0]
    ori[0],ori[1] = ori[1],ori[0]
    return "D"

""" Vira o personagem à esquerda """
def virar_esquerda():
    global ori

    if ori[0]==0:
        ori[1] = -ori[1]
    ori[0],ori[1] = ori[1],ori[0]
    return "E"

""" Quando as salas ao redor não têm perigo, decide se o
    personagem visitará outra casa ou mudará de direção """
def escolher_direcao():
    global direcao

    if direcao == 1 or direcao == 3 or direcao == 5:
        direcao += 1
        return "A"
    if direcao == 2 or direcao == 4:
        direcao += 1
        return virar_direita()
    else:
        direcao = 1
        return virar_esquerda()

""" Verifica se há, ao redor, salas livres e não visitadas """
def verifica_sala_ao_redor(acima, abaixo, frente, atras):
    global salasLivres

    count = 0
    if frente in salasLivres:
        count += 1
    if atras in salasLivres:
        count += 1
    if acima in salasLivres:
        count += 1
    if abaixo in salasLivres:
        count += 1
    return count

""" Verifica se há, ao redor, alguma sala possivelmente segura """
def verifica_sala_ao_redor2(acima, abaixo, frente, atras):
    global mundos

    count = 0
    if ("V" in mundo[acima[0]][acima[1]] or "L?" in mundo[acima[0]][acima[1]]) and \
        "M" not in mundo[acima[0]][acima[1]]:
        count += 1
    if ("V" in mundo[abaixo[0]][abaixo[1]] or "L?" in mundo[abaixo[0]][abaixo[1]]) and \
        "M" not in mundo[abaixo[0]][abaixo[1]]:
        count += 1
    if ("V" in mundo[frente[0]][frente[1]] or "L?" in mundo[frente[0]][frente[1]]) and \
        "M" not in mundo[frente[0]][frente[1]]:
        count += 1
    if ("V" in mundo[atras[0]][atras[1]] or "L?" in mundo[atras[0]][atras[1]]) and \
        "M" not in mundo[atras[0]][atras[1]]:
        count += 1
    return count

""" Verifica as salas ao redor com as funções verifica_sala_ao_redor() e
    verifica_sala_ao_redor2()
"""
def verificar_redor(aponta, acima, abaixo, frente, atras):
    global mundo, salasLivres

    if verifica_sala_ao_redor(acima, abaixo, frente, atras) > 0:
        if aponta in salasLivres:
            return "A"
        return virar_direita()

    if verifica_sala_ao_redor2(acima, abaixo, frente, atras) > 0:
        if ("V" in mundo[aponta[0]][aponta[1]] or "L?" in mundo[aponta[0]][aponta[1]]) and \
            "M" not in mundo[aponta[0]][aponta[1]]:
            return "A"
        return virar_direita()

""" Determina a próxima ação quando uma das percepções é F """
def agir_F(aponta, acima, abaixo, frente, atras):
    global mundo, salasLivres, nFlechas

    if nFlechas > 0:
        if "W?" in mundo[aponta[0]][aponta[1]]:
            return "T"
        return virar_direita()
    return verificar_redor(aponta, acima, abaixo, frente, atras)

""" Determina a próxima ação quando uma das percepções é B """
def agir_B(aponta, acima, abaixo, frente, atras):
    global mundo, salasLivres
    return verificar_redor(aponta, acima, abaixo, frente, atras)

""" Determina a próxima ação quando não há percepção """
def agir_Livre(aponta, acima, abaixo, frente, atras):
    global salasLivres

    if verifica_sala_ao_redor(acima, abaixo, frente, atras) > 0:
        if aponta in salasLivres:
            return "A"
        return virar_direita()
    return escolher_direcao()

""" Determina a próxima ação quando uma das percepções é um outro personagem """
def agir_C():
    for i in sensacao:
        if i != "F" and i != "B" and i != "I" and i != "U":
            return "C"
    return ""

def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, acao, sensacao, salaWumpus, pos, ori
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
    if __DEBUG__:
        acao = input("Digite a ação desejada (A/D/E/T/C): ")

        # ATENÇÃO: a atualizacao abaixo está errada!!!
        # Não checa se o movimento foi possível ou não... isso só dá para
        # saber quando chegar uma percepção nova (a percepção "I"
        # diz que o movimento anterior não foi possível).
        pos = posicao
        ori = orientacao
        if acao=="E":
            if ori[0]==0:
                ori[1] = -ori[1]
            ori[0],ori[1] = ori[1],ori[0]
        if acao=="D":
            if ori[1]==0:
                ori[0] = -ori[0]
            ori[0],ori[1] = ori[1],ori[0]
        # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

    else:
        acao = agir_C()
        if acao != "C":
            pos = posicao
            ori = orientacao
            sala = mundo[pos[0]][pos[1]]

            aponta = [(pos[0]+ori[0])%len(mundo), (pos[1]+ori[1])%len(mundo)]
            frente = [pos[0], (pos[1]+1)%len(mundo)]
            atras = [pos[0], (pos[1]-1)%len(mundo)]
            acima = [(pos[0]-1)%len(mundo), pos[1]]
            abaixo = [(pos[0]+1)%len(mundo), pos[1]]

            if len(sensacao) == 0:
                acao = agir_Livre(aponta, acima, abaixo, frente, atras)
            elif "F" in sensacao:
                acao = agir_F(aponta, acima, abaixo, frente, atras)
            elif "B" in sensacao:
                acao = agir_B(aponta, acima, abaixo, frente, atras)
            elif "I" in sensacao:
                acao = virar_direita()
            elif "U" in sensacao:
                acao = "A"

    assert acao in ["A","D","E","T","C"]
    return acao
