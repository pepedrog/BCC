import random
""" Módulo personagemNUSP: define as funções básicas de gerenciamento
    da personagemNUSP no Mundo de Wumpus.
"""


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

global perc
'''
Esta variável lê a lista percepção na função planejar. Depois, esta variável
é usada na função agir.
'''

global explor
'''
Na função planejar, quando a função está "mapeando" o mapa, esta variável
booleana "explor" fica False se ainda houver "" ou "L" no mapa e True caso
contrário. Esta variável booleana é usada na função agir para "permitir" 
que o bot atire a flecha numa sala onde o Wumpus possa estar.
'''

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, \
    perc, explor
    
    
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
        perc = percepcao
        # Corrige o "bug" de movimentação quando o bot bate numa parede
        if "I" in percepcao:
            print("Você bateu num muro")
            if "M" not in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]].append("M")
            pos[0] = (pos[0]-ori[0])%len(mundo)
            pos[1] = (pos[1]-ori[1])%len(mundo)

        # Lê brisa ("B") e marca "P?" nas salas vizinhas que não sejam "V"
        # nem "M"        
        mundo[pos[0]][pos[1]] = ["V"]
        if "B" in percepcao:
            if "V" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                if "M" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                    if "P?" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                        mundo[(pos[0]+1)%len(mundo)][pos[1]].append("P?")
            if "V" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                if "M" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                    if "P?" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                        mundo[(pos[0]-1)%len(mundo)][pos[1]].append("P?")
            if "V" not in mundo[pos[0]][(pos[1]+1)%len(mundo[0])]:
                if "M" not in mundo[pos[0]][(pos[1]+1)%len(mundo[0])]:
                    if "P?" not in mundo[pos[0]][(pos[1]+1)%len(mundo[0])]:
                        mundo[pos[0]][(pos[1]+1)%len(mundo[0])].append("P?")
            if "V" not in mundo[pos[0]][(pos[1]-1)%len(mundo[0])]:
                if "M" not in mundo[pos[0]][(pos[1]-1)%len(mundo[0])]:
                    if "P?" not in mundo[pos[0]][(pos[1]-1)%len(mundo[0])]:
                        mundo[pos[0]][(pos[1]-1)%len(mundo[0])].append("P?")
        
        # Lê fedor ("F") e marca "W?" nas salas vizinhas que não sejam "V"
        # nem "M"
        if "F" in percepcao:
            mundo[pos[0]][pos[1]].append("F")
            if "V" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                if "M" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                    if "W?" not in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                        mundo[(pos[0]+1)%len(mundo)][pos[1]].append("W?")
            if "V" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                if "M" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                    if "W?" not in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                        mundo[(pos[0]-1)%len(mundo)][pos[1]].append("W?")
            if "V" not in mundo[pos[0]][(pos[1]+1)%len(mundo)]:
                if "M" not in mundo[pos[0]][(pos[1]+1)%len(mundo)]:
                    if "W?" not in mundo[pos[0]][(pos[1]+1)%len(mundo)]:
                        mundo[pos[0]][(pos[1]+1)%len(mundo)].append("W?")
            if "V" not in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
                if "M" not in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
                    if "W?" not in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
                        mundo[pos[0]][(pos[1]-1)%len(mundo)].append("W?")
                        
        
        # Mostra na tela (para o usuário) o mundo conhecido pela personagem
        print("Mundo conhecido pela personagem:")
        explor = True   #Se True, permite que o bot atire a flecha para tentar
                        #o Wumpus
        for i in range(len(mundo)):
            for j in range(len(mundo[0])):
                if pos==[i,j]:
                    print("X",end="")
                    if ori==[0,-1]:
                        print("<",end="")                    
                    if ori==[0,1]:
                        print(">",end="")
                    if ori==[1,0]:
                        print("v",end="")
                    if ori==[-1,0]:
                        print("^",end="")
                if "V" in mundo[i][j]:
                    if "F" in mundo[i][j]:
                        mundo[i][j] = ["V","F"] # Eu não sei se é permitido 
                                                # marcar o mapa com "F", mas
                                                # isto ajuda muito na hora 
                                                # de julgar se atira a flecha
                                                # para matar o Wumpus
                    else:
                        mundo[i][j] = ["V"]
                elif "M" in mundo[i][j] or "M" in mundoCompartilhado[i][j]:
                    mundo[i][j] =["M"]
                elif "L" in mundoCompartilhado[i][j]:
                    mundo[i][j] = ["L"]
                elif "P?" in mundoCompartilhado[i][j] and "V" not in mundo\
                [i][j]:
                    mundo[i][j] = ["P?"]
                elif "W?" in mundoCompartilhado[i][j] and "V" not in mundo\
                [i][j]:
                    mundo[i][j] = ["W?"]
                if mundo[i][j] == [] or "L" in mundo[i][j]:
                    explor = False  # Se False, proíbe o bot de caçar o Wumpus
                                    # e, dessa forma, explora o mapa apenas
                
                print("".join(mundo[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))



def agir():
    """ Nessa função, o bot usa seu conhecimento do mundo para decidir
        e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, \
    perc, explor
    pos = posicao
    ori = orientacao
    trigger = 0  # Esta variável serve para verificar se um "W?" (possível
                 # Wumpus) é realmente um Wumpus ou um falso positivo
    
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
    
   # Abaixo é o programa para encontrar um possível Wumpus e verificar se
   # é um alvo bom o suficiente para utilizar uma flecha 
    if explor == True: 
        if "W?" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
                         (mundo[0])]:
            if "F" in mundo[(pos[0]+ori[0]+1)%len(mundo)][(pos[1]+ori[1])%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]+ori[0]-1)%len(mundo)][(pos[1]+ori[1])%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1]+1)%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1]-1)%len\
                            (mundo[0])]:
                trigger+=1
            if trigger >=2:  # Esta linha avalia se o possível Wumpus é real ou
                             # não. Se for, o bot atira uma flecha
                acao = "T"
                trigger = 0
            else:
                acao = random.choice("D""E")
                trigger = 0
        # Abaixo, verifica se há um possível Wumpus ("W?") ao lado. Se há, vira
        # em direção a ele se ouver Fedor ("F") o suficiente ao redor
        elif "W?" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]-ori[0])%len\
                           (mundo[0])]:
            if "F" in mundo[(pos[0]-ori[1]+1)%len(mundo)][(pos[1]-ori[0])%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]-ori[1]-1)%len(mundo)][(pos[1]-ori[0])%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]-ori[0]+1)%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]-ori[0]-1)%len\
                            (mundo[0])]:
                trigger+=1
            if trigger >= 2:
                if ori[0]!=0:
                    acao = "D"
                    trigger = 0
                else:
                    acao = "E"
                    trigger = 0
            else:
                acao = "A"
                trigger = 0
        # Abaixo, mesma lógica do programa acima, mas oposto
        elif "W?" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]+ori[0])%len\
                           (mundo[0])]:
            if "F" in mundo[(pos[0]+ori[1]+1)%len(mundo)][(pos[1]+ori[0])%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]+ori[1]-1)%len(mundo)][(pos[1]+ori[0])%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]+ori[0]+1)%len\
                            (mundo[0])]:
                trigger+=1
            if "F" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]+ori[0]-1)%len\
                            (mundo[0])]:
                trigger+=1
            if trigger >= 2:                
                if ori[0]!=0:
                    acao = "E"
                    trigger = 0
                else:
                    acao = "D"
                    trigger = 0
            else:
                acao = "A"
                trigger = 0
        # Abaixo, serve para andar para frente quando a sala for Livre ("L")
        # ou inexplorada([])
        elif mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo[0])]\
        == [] or "L" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
           (mundo[0])]:
            acao = "A"
        # Abaixo, se estiver em frente a uma sala Vista ("V"), verifica se há
        # salas inexploradas ou Livres aos lados. Se sim, vira em direção a 
        # ela. Se não, segue em frente
        elif "V" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
                          (mundo[0])]:
            if ori[0]!=0:
                if "L" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]-ori[0])%\
                                len(mundo[0])] or mundo[(pos[0]-ori[1])%len\
                                   (mundo)][(pos[1]-ori[0])%len(mundo[0])]==\
                                []:
                    acao = "D"
                elif "L" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]+ori[0])\
                                  %len(mundo[0])] or mundo[(pos[0]+ori[1])%\
                                      len(mundo)][(pos[1]+ori[0])%len(mundo\
                                         [0])]==[]:
                    acao = "E"
                else:
                    acao = "A"
            else:
                if "L" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]+ori[0])\
                                %len(mundo[0])] or mundo[(pos[0]+ori[1])%len\
                                    (mundo)][(pos[1]+ori[0])%len(mundo[0])]\
                                ==[]:
                    acao = "D"
                elif "L" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]-ori[0])\
                                  %len(mundo[0])] or mundo[(pos[0]-ori[1])%\
                                      len(mundo)][(pos[1]-ori[0])%len(mundo\
                                         [0])]==[]:
                    acao = "E"
                else:
                    acao = "A"
        # Abaixo, se, em frente, houver um "obstáculo" como possível poço
        # ("P?") ou um muro ("M"), virar para a direita ou esquerda num 
        # sorteio
        elif "P?" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
                           (mundo[0])] and "W?" not in mundo[(pos[0]+ori[0])\
                           %len(mundo)][(pos[1]+ori[1])%len(mundo[0])] or "M"\
                           in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1]\
                                    )%len(mundo[0])]:
            acao = random.choice("D""E")
        elif "W" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
                          (mundo[0])]:
            acao = "T"
        # Abaixo, só para ter certeza de não ocorrer erro de declaração de 
        # variáveis
        else:
            acao = random.choice("D""E")
    # Abaixo, é para quando o mapa NÃO está completamente explorado, portanto,
    # o bot não tem permissão de caçar o Wumpus
    else:
        # A prioridade é o de trocar informações com os outros personagens
        if "Dummy" in perc:
            acao = "C"
        # Abaixo, serve para andar para frente quando a sala for Livre ("L")
        # ou inexplorada([])
        elif mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo[0])]\
        == [] or "L" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
           (mundo[0])]:
            acao = "A"
        # Abaixo, se estiver em frente a uma sala Vista ("V"), verifica se há
        # salas inexploradas ou Livres aos lados. Se sim, vira em direção a 
        # ela. Se não, segue em frente
        elif "V" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
                          (mundo[0])]:
            if ori[0]!=0:
                if "L" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]-ori[0])%\
                                len(mundo[0])] or mundo[(pos[0]-ori[1])%len\
                                   (mundo)][(pos[1]-ori[0])%len(mundo[0])]==[]:
                    acao = "D"
                elif "L" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]+ori[0])%\
                                  len(mundo[0])] or mundo[(pos[0]+ori[1])%len\
                                     (mundo)][(pos[1]+ori[0])%len(mundo[0])]\
                                  ==[]:
                    acao = "E"
                else:
                    acao = "A"
            else:
                if "L" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]+ori[0])%\
                                len(mundo[0])] or mundo[(pos[0]+ori[1])%len\
                                   (mundo)][(pos[1]+ori[0])%len(mundo[0])]==[]:
                    acao = "D"
                elif "L" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]-ori[0])\
                                  %len(mundo[0])] or mundo[(pos[0]-ori[1])%len\
                                      (mundo)][(pos[1]-ori[0])%len(mundo[0])]\
                                  ==[]:
                    acao = "E"
                else:
                    acao = random.choice("A""D""E")
        # Abaixo, se, em frente, houver um "obstáculo" como possível poço
        # ("P?"), um possível Wumpus ("W?") ou um muro ("M"), virar para a 
        #direita ou esquerda num sorteio
        elif "P?" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
                           (mundo[0])] or "W?" in mundo[(pos[0]+ori[0])%\
                           len(mundo)][(pos[1]+ori[1])%len(mundo[0])] or "M"\
                           in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1]\
                                    )%len(mundo[0])]:
            acao = random.choice("D""E")
        elif "W" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len\
                          (mundo[0])]:
            acao = "T"
        # Abaixo, só para ter certeza de não ocorrer erro de declaração de 
        # variáveis
        else:
            acao = random.choice("D""E")
    
    # Abaixo, comando o que cada ação faz
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
    # Garante que só ações permitidas sejam utilizadas
    assert acao in ["A","D","E","T","C"]
    return acao
