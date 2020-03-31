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

global caminho
"""
Matriz que armazena o caminho percorrido, distância até os locais livres 
"""

global x
"""
atribui número dependendo de sua posição em relação ao caminho feito
"""

global livre
"""
lista de casas livres ainda não visitadas
"""

global checaWumpus
"""
True se sentir fedor
"""

global compartilhar
"""
variável que devolve true caso haja algum personagem para trocar informações
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
    global N, mundo, posicao, orientacao,livre,x,caminho,Atirar
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    livre = []
    for i in range(N) :
        linha = []
        for j in range(N) :
            linha.append([]) # começa com listas vazias
        mundo.append(linha)# começa com listas vazias
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    #cria matriz que armazena a distância até os lugares livres 
    caminho = []
    for i in range(N) :
        linha = []
        for j in range(N) :
            linha.append([]) # começa com listas vazias
        caminho.append(linha)
    x=0    
    Atirar=False

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,livre,x,caminho,checaWumpus,compartilhar
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado)
    print("Percepção recebida pela personagem:")
    print(percepcao)
    pos = posicao
    ori = orientacao
    checaWumpus = False
    compartilhar = False
    #marca lugares visitadods com V
    mundo[pos[0]][pos[1]] = ["V"]
    vizinhos = [ [(pos[0]+1)%N,pos[1]],
    [(pos[0]-1)%N,pos[1]],
    [pos[0],(pos[1]+1)%N],
    [pos[0],(pos[1]-1)%N] ]
    #marca os muros
    if "I" in percepcao:
        mundo[pos[0]][pos[1]].append(["M"])
        caminho[pos[0]][pos[1]] = "m"
        pos[0] = pos[0]-ori[0]
        pos[1] = pos [1]-ori[1]
    #marca onde pode haver poço    
    elif "B" in percepcao:
        for viz in vizinhos:
            if "M" not in mundo[viz[0]][viz[1]] and "V" not in mundo[viz[0]][viz[1]] and "L" not in mundo[viz[0]][viz[1]]:
                mundo[viz[0]][viz[1]].append(["P?"])
                caminho[viz[0]][viz[1]]="P"+str(p)                    
    #marca onde pode haver Wumpus
    elif "F" in percepcao:
        for viz in vizinhos:
            if "M" or "V" not in mundo[viz[0]][viz[1]]:
                mundo[viz[0]][viz[1]].append(["W?"])
                caminho[viz[0]][viz[1]]="W"+str(w)
                checaWumpus = True
    elif "B" not in percepcao and "I" not in percepcao and "V" not in percepcao:
        compartilhar == True         

    #marca os locais livres            
    if percepcao == []:             
        for viz in vizinhos:
            if "M" not in mundo[viz[0]][viz[1]] and "V" not in mundo[viz[0]][viz[1]] and "L" not in mundo[viz[0]][viz[1]]:
                mundo[viz[0]][viz[1]] = ["L"]
                livre.append([viz[0]])
                caminho[viz[0]][viz[1]] = x+1
            if livre != [] and mundo[pos[0]][pos[1]] in livre:
                livre.remove([mundo[pos[0]][pos[1]]])
                caminho[pos[0]][pos[1]]=x             
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
            if mundo[i][j] == []:
                mundo [i][j] = mundoCompartilhado[i][j]        
            print("".join(mundo[i][j]),end="\t| ")
        print("\n"+"-"*(8*len(mundo)+1))   
    #checa o mapa inteiro para saber se tem um de cada tipo de poço e wumpus


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,checaWumpus,compartilhar,Atirar
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
    checaWumpus = False
    ori = orientacao
    pos = posicao
    acao=""
    vizinhos = [ [(pos[0]+1)%N,pos[1]],
    [(pos[0]-1)%N,pos[1]],
    [pos[0],(pos[1]+1)%N],
    [pos[0],(pos[1]-1)%N] ]
    #prioridade é compartilhar informações:
    if compartilhar == True:
        acao="C"   

    #elif checaWumpus==True:
    if checaWumpus==True:
        for viz in vizinhos:
            if "W" in mundo[viz[0]][viz[1]] and "W?" not in mundo[viz[0]][viz[1]]:
                Atirar = True

    else:    
        d=[[1,0],[-1,0],[0,1],[0,-1]]
        frente0 = (pos[0]+ori[0])%len(mundo)
        frente1 = (pos[1]+ori[1])%len(mundo)
        if Atirar==True:
            if mundo[frente0][frente1]=="W" and nFlechas>0:
                acao="T"
                Atirar = False
            else:
                acao = "D"
        elif mundo[frente0][frente1]=="L":
            acao = "A"
        else:
            acao = "D"                    

    if acao=="A":
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
        x +=1 
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
