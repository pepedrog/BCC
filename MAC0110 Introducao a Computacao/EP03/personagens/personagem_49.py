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
# 1,0  == v
# -1,0 == ^
# 0,1  == >
# 0,-1 == <

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

###########################################

global personagemNaSala
"""
Valor booleano que indica se há ou não outro personagem na sala
"""

salasLivres = []
"""
Mantém uma lista das salas livres ainda não visitadas
"""

global matrizCaminhos
"""
Mantém uma matriz com um mapa 'alternativo' do mundo, o qual
indica apenas as distâncias até a próxima cada a ser visitada
"""


def resetaCaminhos() :
    """ Função que inicializa e limpa a matriz
    que armazena os valores numéricos
    """
    
    global matrizCaminhos

    matrizCaminhos = []
    for i in range(N) :
        linha = []
        for j in range(N) :
            linha.append(-1) # começa com listas de valores -1
        matrizCaminhos.append(linha)
    return

    

def fazCaminho(fim=[]):
    """ Implementa uma busca por largura no mundo, colocando como
    objetivo a primeira sala livre na lista e começando na posição
    atual do personagem. Armazena os valores numéricos em matrizCaminhos.
    """
    #limpa a matriz
    resetaCaminhos()

    global mundo,matrizCaminhos,posicao

    #marca o destino como 1 e adota como posição inicial
    matrizCaminhos[fim[0]][fim[1]] = 1
    pontas = [[fim[0],fim[1],1]]

    casa = [0,0] # força a entrada
    
    while len(pontas) != 0 and [casa[0],casa[1]] != posicao:

        casa = pontas[0]
        # confere as 4 casas ao redor da selecionada,
        # realizando os seguintes passos:
        # 1 - confere se ela é a posição atual, se sim, atribui o valor 0 e interrompe
        # 2 - confere se ela é válida, se não, pula
        # 3 - confere um valor de distância para ela em matrizCaminhos
        # 4 - adiciona ela a lista de pontas a serem checadas
        # após conferir as 4 casas, retira a selecionada da lista
        pos = [casa[0],(casa[1] + 1)%len(mundo)]
        if pos == posicao :
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 2
            break
        elif "V" in mundo[pos[0]][pos[1]] and \
        matrizCaminhos[pos[0]][pos[1]] == -1 :
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 1
            pontas.append([pos[0],pos[1],casa[2]+1])

        pos = [casa[0],(casa[1] - 1)%len(mundo)]
        if pos == posicao :
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 2
            break
        elif "V" in mundo[pos[0]][pos[1]] and \
        matrizCaminhos[pos[0]][pos[1]] == -1:
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 1
            pontas.append([pos[0],pos[1],casa[2]+1])

        pos = [(casa[0] + 1)%len(mundo),casa[1]]
        if pos == posicao :
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 2
            break
        elif "V" in mundo[pos[0]][pos[1]] and \
        matrizCaminhos[pos[0]][pos[1]] == -1:
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 1
            pontas.append([pos[0],pos[1],casa[2]+1])

        pos = [(casa[0] - 1)%len(mundo),casa[1]]
        if pos == posicao :
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 2
            break
        elif "V" in mundo[pos[0]][pos[1]] and \
        matrizCaminhos[pos[0]][pos[1]] == -1:
            matrizCaminhos[pos[0]][pos[1]] = casa[2] + 1
            pontas.append([pos[0],pos[1],casa[2]+1])

        pontas.remove(casa)

        

def marcaAoRedor(tag = "L"):
    """ Marca as casas que não foram visitadas e não são muros com a tag,
    se uma tag for passada, se não marca as casas ao redor como livres.
    """

    global mundo,posicao,salasLivres

    # caso em que não há percepção
    # esse caso retira outras marcações
    if tag == "L":

        pos = [posicao[0],(posicao[1]-1 )% len(mundo)]
        if not ("V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]]):

            mundo[pos[0]][pos[1]] = ["L"]
            if not [pos[0],pos[1]] in salasLivres:
                salasLivres.append([pos[0],pos[1]])
            
        pos = [posicao[0],(posicao[1]+1)% len(mundo)]
        if not ("V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]]):

            mundo[pos[0]][pos[1]] = ["L"]
            if not [pos[0],pos[1]] in salasLivres:
                salasLivres.append([pos[0],pos[1]])

        pos = [(posicao[0]+1)% len(mundo),posicao[1]]
        if not ("V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]]):

            mundo[pos[0]][pos[1]] = ["L"]
            if not [pos[0],pos[1]] in salasLivres:
                salasLivres.append([pos[0],pos[1]])            

        pos = [(posicao[0]-1)% len(mundo),posicao[1]]
        if not ("V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]]):

            mundo[pos[0]][pos[1]] = ["L"]
            if not [pos[0],pos[1]] in salasLivres:
                salasLivres.append([pos[0],pos[1]])
        return

    # verifica se as casas ao redor devem ser marcadas e
    # realiza a marcação se sim
    pos = [posicao[0],(posicao[1]-1 )% len(mundo)]
    if not (tag in mundo[pos[0]][pos[1]] or \
            "V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]] or \
            "L" in mundo[pos[0]][pos[1]] or \
            "B" in mundo[pos[0]][pos[1]] or \
            "F" in mundo[pos[0]][pos[1]]):
        mundo[pos[0]][pos[1]].append(tag)

    
    pos = [posicao[0],(posicao[1]+1)% len(mundo)]
    if not (tag in mundo[pos[0]][pos[1]] or \
            "V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]] or \
            "L" in mundo[pos[0]][pos[1]] or \
            "B" in mundo[pos[0]][pos[1]] or \
            "F" in mundo[pos[0]][pos[1]]):
        mundo[pos[0]][pos[1]].append(tag)

    pos = [(posicao[0]+1)% len(mundo),posicao[1]]
    if not (tag in mundo[pos[0]][pos[1]] or \
            "V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]] or \
            "L" in mundo[pos[0]][pos[1]] or \
            "B" in mundo[pos[0]][pos[1]] or \
            "F" in mundo[pos[0]][pos[1]]):
        mundo[pos[0]][pos[1]].append(tag)

    pos = [(posicao[0]-1)% len(mundo),posicao[1]]
    if not (tag in mundo[pos[0]][pos[1]] or \
            "V" in mundo[pos[0]][pos[1]] or \
            "M" in mundo[pos[0]][pos[1]] or \
            "L" in mundo[pos[0]][pos[1]] or \
            "B" in mundo[pos[0]][pos[1]] or \
            "F" in mundo[pos[0]][pos[1]]):
        mundo[pos[0]][pos[1]].append(tag)

    return

def checaWumpus():
    """ Verifica se é razoável inferir que existe um Wumpus na
    posicao em frente ao personagem. Se sim marca um W no mundo.
    """
    
    global posicao,orientacao,mundo

    pos  = posicao
    ori = orientacao
    
    frente = [(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)]
    atras = [(pos[0]-ori[0])%len(mundo),(pos[1]-ori[1])%len(mundo)]
    esquerda = [(pos[0]+ori[1])%len(mundo),(pos[1]+ori[0])%len(mundo)]
    direita = [(pos[0]-ori[1])%len(mundo),(pos[1]-ori[0])%len(mundo)]
    
    if "W?" in mundo[frente[0]][frente[1]] and \
    not ("W?" in mundo[esquerda[0]][esquerda[1]] or \
    "W?" in mundo[direita[0]][direita[1]] or \
    "W?" in mundo[atras[0]][atras[1]]) :
        mundo[frente[0]][frente[1]] = ["W"]

    return

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,\
    personagemNaSala,pedeCaminho,Tiro
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).
    
    ori = orientacao
    personagemNaSala = False
    Tiro = False
    
    # correcao no caso de impacto
    if "I" in percepcao:
        if [posicao[0],posicao[1]] in salasLivres :
            salasLivres.remove([posicao[0],posicao[1]])
        mundo[posicao[0]][posicao[1]] = ["M"]
        posicao[0] = (posicao[0]-ori[0])%len(mundo)
        posicao[1] = (posicao[1]-ori[1])%len(mundo)
        resetaCaminhos()

    pos = posicao
    
    # marca as casas com as informações percebidas
    if percepcao == [] :
        marcaAoRedor()
    elif percepcao[-1] != "B" and percepcao[-1] != "F" and \
         percepcao[-1] != "I" and percepcao[-1] != "U":
        personagemNaSala = True
    else:
        if "B" in percepcao :
            marcaAoRedor('P?')
            if not "B" in mundo[pos[0]][pos[1]] :
                mundo[pos[0]][pos[1]].append("B")
        if "F" in percepcao :
            marcaAoRedor('W?')
            if not "F" in mundo[pos[0]][pos[1]] :
                mundo[pos[0]][pos[1]].append("F")
            Tiro = checaWumpus()
            

    #remove a sala recem visitada 
    if [pos[0],pos[1]] in salasLivres :
        salasLivres.remove([pos[0],pos[1]])

    #pede um novo caminho
    if len(salasLivres) != 0:
            fazCaminho(salasLivres[0])
    #marca a casa atual como visitada
    if not "V" in mundo[pos[0]][pos[1]] :
        mundo[pos[0]][pos[1]].append("V")
#    if "L" in mundo[pos[0]][pos[1]] :
#        if type(mundo[pos[0]][pos[1]]) == list :
#            mundo[pos[0]][pos[1]].remove("L")
#        else:
#            mundo[pos[0]][pos[1]] = mundo[pos[0]][pos[1]].replace("L","")
#    if "P?" in mundo[pos[0]][pos[1]] :
#        mundo[pos[0]][pos[1]] = mundo[pos[0]][pos[1]].replace("P?","")
#    if "W" in mundo[pos[0]][pos[1]] :
#        mundo[pos[0]][pos[1]] = mundo[pos[0]][pos[1]].replace("W?","")
    

    
        


    
    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
    # 
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # elimine o teste abaixo quando tiver corrigido o bug de movimentação...
        if "I" in percepcao:
            print("Você bateu num muro e talvez não esteja mais na sala em que pensa estar...")
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
#        pos = posicao
#        ori = orientacao
#        if mundo[pos[0]][pos[1]] in salasLivres :
#            salasLivres.remove(mundo[pos[0]][pos[1]])
#        mundo[pos[0]][pos[1]] = ["V"]
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
                print("".join(mundo[i][j]),end=" ")
                print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))

        print ("lista de salas Livres:")
        for i in range(len(salasLivres)):
            print(salasLivres[i][0],salasLivres[i][1])

        print("Matriz dos Caminhos:")
        for i in range(len(matrizCaminhos)):
            for j in range(len(matrizCaminhos[0])):
                print(matrizCaminhos[i][j],end="\t")
            print()

    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,\
    personagemNaSala,pedeCaminho,Tiro
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
    acao = "D" #ação padrão

    #define as posicoes ao redor do personagem
    frente = [(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)]
    atras = [(pos[0]-ori[0])%len(mundo),(pos[1]-ori[1])%len(mundo)]
    esquerda = [(pos[0]+ori[1])%len(mundo),(pos[1]+ori[0])%len(mundo)]
    direita = [(pos[0]-ori[1])%len(mundo),(pos[1]-ori[0])%len(mundo)]

    #se houver um outro personagem na sala
    if personagemNaSala:
        acao = "C"
    # suspeita forte de que existe um wumpus proximo
    elif "W" in mundo[frente[0]][frente[1]] or \
         "W" in mundoCompartilhado[frente[0]][frente[1]]:
        acao = "T"
    elif "W" in mundo[frente[0]][frente[1]] or \
         "W" in mundoCompartilhado[direita[0]][direita[1]] :
        acao = "D"
    elif "W" in mundo[frente[0]][frente[1]] or \
         "W" in mundoCompartilhado[esquerda[0]][esquerda[1]] :
        acao = "E"
    #compara todas as casas ao redor em função dos valore em
    # matrizCaminhos, verificando sempre se não se trata de um -1
    #com isso escolhe um movimento seguro para se fazer
    # indo em direção a uma casa livre não visitada
    elif matrizCaminhos[frente[0]][frente[1]] != -1 and \
    (matrizCaminhos[direita[0]][direita[1]] == -1 or\
    matrizCaminhos[frente[0]][frente[1]] <= matrizCaminhos[direita[0]][direita[1]]) and \
    (matrizCaminhos[esquerda[0]][esquerda[1]] == -1 or\
    matrizCaminhos[frente[0]][frente[1]] <= matrizCaminhos[esquerda[0]][esquerda[1]]) and \
    (matrizCaminhos[atras[0]][atras[1]] == -1 or\
    matrizCaminhos[frente[0]][frente[1]] <= matrizCaminhos[atras[0]][atras[1]]) :
        acao = "A"
    #trata dos casos direita e atras juntos
    elif (matrizCaminhos[direita[0]][direita[1]] != -1 and \
    matrizCaminhos[direita[0]][direita[1]] <= matrizCaminhos[frente[0]][frente[1]] and \
    (matrizCaminhos[esquerda[0]][esquerda[1]] == -1 or\
    matrizCaminhos[direita[0]][direita[1]] <= matrizCaminhos[esquerda[0]][esquerda[1]]) and \
    (matrizCaminhos[atras[0]][atras[1]] == -1 or\
    matrizCaminhos[direita[0]][direita[1]] <= matrizCaminhos[atras[0]][atras[1]]) ) \
    or \
    (  matrizCaminhos[atras[0]][atras[1]] != -1 and \
    (matrizCaminhos[atras[0]][atras[1]] == -1 or\
    matrizCaminhos[atras[0]][atras[1]] <= matrizCaminhos[frente[0]][frente[1]]) and \
    (matrizCaminhos[direita[0]][direita[1]] == -1 or\
    matrizCaminhos[atras[0]][atras[1]] <= matrizCaminhos[direita[0]][direita[1]]) and \
    (matrizCaminhos[esquerda[0]][esquerda[1]] == -1 or\
    matrizCaminhos[atras[0]][atras[1]] <= matrizCaminhos[esquerda[0]][esquerda[1]]) ):
        acao = "D"
    elif matrizCaminhos[esquerda[0]][esquerda[1]] != -1 and \
    matrizCaminhos[esquerda[0]][esquerda[1]] <= matrizCaminhos[frente[0]][frente[1]] and \
    (matrizCaminhos[direita[0]][direita[1]] == -1 or\
    matrizCaminhos[esquerda[0]][esquerda[1]] <= matrizCaminhos[direita[0]][direita[1]]) and \
    (matrizCaminhos[atras[0]][atras[1]] == -1 or\
    matrizCaminhos[esquerda[0]][esquerda[1]] <= matrizCaminhos[atras[0]][atras[1]]) :
        acao = "E"
        
    #todos as casas ao redor são ='s -1
    #não existe movimento seguro de acordo com as informações do personagem
    #todas as salas livres percebidas foram visitadas
    #utiliza a informação compartilhada
    elif len(salasLivres) == 0:
        if "L" in mundoCompartilhado[frente[0]][frente[1]]:
            acao = "A"
        elif "L" in mundoCompartilhado[direita[0]][direita[1]] or \
             "L" in mundoCompartilhado[atras[0]][atras[1]]:
            acao = "D"
        elif "L" in mundoCompartilhado[esquerda[0]][esquerda[1]] :
            acao = "E"
        #nenhuma sala livre conhecida, volta pelo caminho até encontrar
        #o Wumpus ou um personagem que compartilhe alguma informação relevante
        elif "V" in mundo[frente[0]][frente[1]] :
            acao = "A"                                     

        # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
        # O trecho abaixo é uma pseudo-implementação, pois recebe
        # a ação através de uma pergunta dirigida ao usuário.
        # No código a ser entregue, você deve programar algum tipo
        # de estratégia para 
#        acao = input("Digite a ação desejada (A/D/E/T/C): ")
  
        # ATENÇÃO: a atualizacao abaixo está errada!!!
        # Não checa se o movimento foi possível ou não... isso só dá para
        # saber quando chegar uma percepção nova (a percepção "I"
        # diz que o movimento anterior não foi possível).
        # [CORRIGIDO]
        
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
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

    assert acao in ["A","D","E","T","C"]
    return acao
