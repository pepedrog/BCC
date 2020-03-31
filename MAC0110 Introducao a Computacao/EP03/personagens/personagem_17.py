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

global posAnt
"""
Guara a informação da posicao anterior, para que seja possível
voltar a posição quando há impacto
"""


global percep
"""
Guarda a percepcao sentida
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
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mundo.append(linha)
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]


def contem(lista, elemento):
    """
    verifica se o elemento está na lista
    """
    for i in range(len(lista)):
        if (lista[i] == elemento):
            return True
    return False


def pegaVizinhos(mundo):
    """
    Função pega o conteúdo dos vizinhos acima, abaixo,
    a direita e a esquerda
    """
    # declara as variáveis globais que serão acessadas
    global posicao
    
    # coordenadas de linha e coluna
    linha = posicao[0]
    coluna = posicao[1]

    # todos os vizinhos
    vizinhos = []

    # vizinho acima 'vizinhos[0]'
    vizinhos.append(mundo[(linha-1)%N][coluna])

    # vizinho abaixo 'vizinhos[1]'
    vizinhos.append(mundo[(linha+1)%N][coluna])

    # vizinho direita 'vizinhos[2]'
    vizinhos.append(mundo[linha][(coluna+1)%N])

    # vizinho esquerda 'vizinhos[3]'
    vizinhos.append(mundo[linha][(coluna-1)%N])

    return vizinhos




def intrepretaPercepcao(percepcao):
    """
    Esta função mapeia os possíveis conteúdos das casas
    vizinhas de acordo com a percepeção recebida
    """
    global mundo


    vizinhos = pegaVizinhos(mundo)

    if "B" in percepcao:
        sensacao = "P?"
    elif "F" in percepcao:
        sensacao = "W?"
    else:
        sensacao = "L"
    for i in range(4):
        if vizinhos[i] != ["V"] and not contem(vizinhos[i], sensacao) and not contem(vizinhos[i], "M"):            
            vizinhos[i].append(sensacao)


def giraPersonagem(vizinhos):
    """
    Esta função faz a personagem girar até a casa desejada e executa
    o movimento de andar
    """
    if vizinhos == 0:
        if orientacao == [-1, 0]:
            return "A"
        elif orientacao[1] == 0:
            return "E"
        elif orientacao[1] == -1:
            return "D"
        else:
            return "E"
    if vizinhos == 1:
        if orientacao == [1, 0]:
            return "A"
        elif orientacao[1] == 0:
            return "E"
        elif orientacao[1] == -1:
            return "E"
        else:
            return "D"
    if vizinhos == 2:
        if orientacao == [0, 1]:
            return "A"
        elif orientacao[0] == 0:
            return "E"
        elif orientacao[0] == -1:
            return "D"
        else:
            return "E"
    if vizinhos == 3:
        if orientacao == [0, -1]:
            return "A"
        elif orientacao[0] == 0:
            return "D"
        elif orientacao[0] == -1:
            return "E"
        else:
            return "D"



def defineComando(percepcao):
    """
    Esta função define o melhor comando a ser executado
    de acordo com as circunstâncias que a percepção apresenta
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, mundoCompartilhado

    # olho o conteúdo dos 4 vizinhos
    vizinhos = pegaVizinhos(mundo)
    vizinhosDummy = pegaVizinhos(mundoCompartilhado)

    # se "Dummy" está na percepção, escolh-se sempre
    # compartilhar informações, para conhecer melhor o mundo 
    if "Dummy" in percepcao:
        return "C"


    # MATA
    # a sequencia de preferência do movimento ficou arbritariamente
    # ordenada assim: pra cima, pra baixo, lado esquerdo, lado direito
    if contem(vizinhos[0], "W?") and contem(vizinhosDummy[0], "W"):
        if giraPersonagem(0) == "A":
            return "T"
        else:
            return giraPersonagem(0)
    if contem(vizinhos[1], "W?") and contem(vizinhosDummy[1], "W"):
        if giraPersonagem(1) == "A":
            return "T"
        else:
            return giraPersonagem(1)
    if contem(vizinhos[2], "W?") and contem(vizinhosDummy[2], "W"):
        if giraPersonagem(2) == "A":
            return "T"
        else:
            return giraPersonagem(2)
    if contem(vizinhos[3], "W?") and contem(vizinhosDummy[3], "W"):
        if giraPersonagem(3) == "A":
            return "T"
        else:
            return giraPersonagem(3)

    # A ideia é caminhar para os locais que sabemos ser Livres("L")
    # Dando preferencia por seguir em frente, e caso
    # isto não seja possível, verica-se esta possibilidade
    # girando num sentido horário, até acharmos um local Livre.
    if orientacao == [-1, 0]:
        if contem(vizinhos[0], "L") or (contem(vizinhosDummy[0], "L") and not contem(vizinhos[0], "V")):
            return giraPersonagem(0)
        if contem(vizinhos[2], "L") or (contem(vizinhosDummy[2], "L") and not contem(vizinhos[2], "V")):
            return giraPersonagem(2)
        if contem(vizinhos[1], "L") or (contem(vizinhosDummy[1], "L") and not contem(vizinhos[1], "V")):
            return giraPersonagem(1)
        if contem(vizinhos[3], "L") or (contem(vizinhosDummy[3], "L") and not contem(vizinhos[3], "V")):
            return giraPersonagem(3)
    elif orientacao == [0, 1]:
        if contem(vizinhos[2], "L") or (contem(vizinhosDummy[2], "L") and not contem(vizinhos[2], "V")):
            return giraPersonagem(2)
        if contem(vizinhos[1], "L") or (contem(vizinhosDummy[1], "L") and not contem(vizinhos[1], "V")):
            return giraPersonagem(1)
        if contem(vizinhos[3], "L") or (contem(vizinhosDummy[3], "L") and not contem(vizinhos[3], "V")):
            return giraPersonagem(3)
        if contem(vizinhos[0], "L") or (contem(vizinhosDummy[0], "L") and not contem(vizinhos[0], "V")):
            return giraPersonagem(0)    
    elif orientacao == [1, 0]:
        if contem(vizinhos[1], "L") or (contem(vizinhosDummy[1], "L") and not contem(vizinhos[1], "V")):
            return giraPersonagem(1)
        if contem(vizinhos[3], "L") or (contem(vizinhosDummy[3], "L") and not contem(vizinhos[3], "V")):
            return giraPersonagem(3)
        if contem(vizinhos[0], "L") or (contem(vizinhosDummy[0], "L") and not contem(vizinhos[0], "V")):
            return giraPersonagem(0)
        if contem(vizinhos[2], "L") or (contem(vizinhosDummy[2], "L") and not contem(vizinhos[2], "V")):
            return giraPersonagem(2)
    else:
        if contem(vizinhos[3], "L") or (contem(vizinhosDummy[3], "L") and not contem(vizinhos[3], "V")):
            return giraPersonagem(3)
        if contem(vizinhos[0], "L") or (contem(vizinhosDummy[0], "L") and not contem(vizinhos[0], "V")):
            return giraPersonagem(0)
        if contem(vizinhos[2], "L") or (contem(vizinhosDummy[2], "L") and not contem(vizinhos[2], "V")):
            return giraPersonagem(2)
        if contem(vizinhos[1], "L") or (contem(vizinhosDummy[1], "L") and not contem(vizinhos[1], "V")):
            return giraPersonagem(1)



    

    # Caso não se tenha nenhuma vizinha livre
    # volta para uma casa ja visitada.
    # Dando preferencia por seguir em frente, e caso
    # isto não seja possível, verica-se esta possibilidade
    # girando num sentido horário.
    if orientacao == [-1, 0]:
        if contem(vizinhos[0], "V"):	
            return giraPersonagem(0)
        if contem(vizinhos[2], "V"):
            return giraPersonagem(2)
        if contem(vizinhos[1], "V"):
            return giraPersonagem(1)
        if contem(vizinhos[3], "V"):
            return giraPersonagem(3)                                
            
    if orientacao == [0, 1]:
        if contem(vizinhos[2], "V"):	
            return giraPersonagem(2)
        if contem(vizinhos[1], "V"):
            return giraPersonagem(1)
        if contem(vizinhos[3], "V"):
            return giraPersonagem(3)
        if contem(vizinhos[0], "V"):
            return giraPersonagem(0)

    if orientacao == [1,0]:
        if contem(vizinhos[1], "V"):	
            return giraPersonagem(1)
        if contem(vizinhos[3], "V"):
            return giraPersonagem(3)
        if contem(vizinhos[0], "V"):
            return giraPersonagem(0)
        if contem(vizinhos[2], "V"):
            return giraPersonagem(2)

    if orientacao == [0, -1]:
        if contem(vizinhos[3], "V"):	
            return giraPersonagem(3)
        if contem(vizinhos[0], "V"):
            return giraPersonagem(0)
        if contem(vizinhos[2], "V"):
            return giraPersonagem(2)
        if contem(vizinhos[1], "V"):
            return giraPersonagem(1)
        
	
	
    

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,  posAnt, percep
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).

    percep = percepcao.copy()
    print("Percepção recebida pela personagem:")
    print(percepcao)
    # "I" nos diz que a movimentação não foi possível, então a posição não se altera
    # recebendo uma cópia da posição anterior...
    if "I" in percepcao:
        mundo[posicao[0]][posicao[1]] = ["M"]
        posicao = posAnt.copy()        
    intrepretaPercepcao(percepcao)            
    print(posicao)        
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


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, posAnt, percep
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

    # aqui é recebida a ação a ser executada com base na percepção obtida
    acao = defineComando(percep)
  
    # guarda-se a posição anterior para o caso de a ação gerar impacto
    # para que seja possível manter a coordenada 
    posAnt = posicao.copy()
    ori = orientacao
    if acao=="A":
        posicao[0] = (posicao[0]+ori[0])%len(mundo)
        posicao[1] = (posicao[1]+ori[1])%len(mundo)
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
