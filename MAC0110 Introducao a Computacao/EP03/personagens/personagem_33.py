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
Lista que armazena as salas livres não visitadas que o personagem tem conhecimento
"""

global compartilhar
"""
Flag para compartilhamento quando outro personagem é encontrado
"""

global objetivo
"""
Lista que armazena a posição de uma dada sala na matriz "mundo"
"""

global caminho
"""
Lista de posições para obter o caminho até a posição objetivo
"""
global mapa
def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).
    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, salasLivres, compartilhar, caminho, objetivo
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N):
        mundo.append([]) # começa com listas vazias
        for j in range(N):
            mundo[i].append([])
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    # iniciailiza as variáveis como listas vazias e a flag compartilhar em False
    salasLivres = [] 
    caminho = []
    objetivo = []
    compartilhar = False

def encontraCaminho():
    """ Função que determina o menor caminho entre a posição relativa da
        personagem e um objetivo (uma sala livre da matriz "mundo")
    """
    global mundo, posicao, N, objetivo, caminho, salasLivres, mapa

    obj = objetivo
    # Se a sala já foi visitada descarta a posição e retorna caminho como
    # lista vazia
    if "V" in mundo[obj[0]][obj[1]]: 
        return []
    # Cria mapa de indicadores preenchendo salas acessíveis com 0's e o restante com
    # -1's para encontrar um caminho válido
    mapa = []
    for i in range(N):
        mapa.append([])
        for j in range(N):
            if "L" in mundo[i][j] or "V" in mundo[i][j]:
                mapa[i].append(0)
            else:
                mapa[i].append(-1)
    # Inicializa o objetivo com a menor "distância" e inicia uma lista com a sua posição
    mapa[obj[0]][obj[1]] = 1
    busca = [obj] 
    #Mapeia a matriz de indicadores até que não haja mais casas acessíveis (mapa[i][j]==0)
    while len(busca)!=0:
        pos = busca.pop(0)
        vizinhos = [[(pos[0]-1)%N,pos[1]], [pos[0],(pos[1]+1)%N], \
                    [(pos[0]+1)%N,pos[1]], [pos[0],(pos[1]-1)%N]]
        for sala in vizinhos:
            if mapa[sala[0]][sala[1]]==0:

                mapa[sala[0]][sala[1]] = mapa[pos[0]][pos[1]] + 1 
                busca.append([sala[0],sala[1]])
    # A partir da posição da personagem determina o menor caminho até o objetivo
    pos = posicao
    caminho = []
    contador = 0 # Contador para garantir que há um caminho acesssível
    while pos!=obj and contador<4:
        vizinhos = [[(pos[0]-1)%N,pos[1]], [pos[0],(pos[1]+1)%N], \
                    [(pos[0]+1)%N,pos[1]], [pos[0],(pos[1]-1)%N]]
        contador = 0
        for sala in vizinhos:
            if mapa[sala[0]][sala[1]]!=-1 and \
               mapa[sala[0]][sala[1]] < mapa[pos[0]][pos[1]]:
                pos = [sala[0],sala[1]]
                caminho.append(pos)
                break
            else:
                contador+=1
                continue
    # Se o contador é >= 4 indica que em algum momento da construção do caminho
    # não havia vizinhos acessíveis.
    if contador>=4:
        salasLivres.append(objetivo) # guarda a posição para tentativa posterior
        caminho=[]


def atualizaMundo():
    """ Função que incorpora os dados do mundo compartilhado com
        o "mundo" local
    """
    global mundoCompartilhado, mundo, salasLivres
    # Percorre o mundo compartilhado e insere as informações selecionadas no "mundo"
    # da personagem
    for i in range(len(mundoCompartilhado)):
        for j in range(len(mundoCompartilhado[0])):

            if mundo[i][j]==[] or "P?" in mundo[i][j] or "W?" in mundo[i][j]:
                if "P" in mundoCompartilhado[i][j]:
                    mundo[i][j]=["P"]
                if "W" in mundoCompartilhado[i][j]:
                    mundo[i][j]=["W"]
                    salasLivres.insert(0,[i,j])
                if "M" in mundoCompartilhado[i][j]:
                    mundo[i][j]=["M"]
                if "L" in mundoCompartilhado[i][j] and not("V" in mundo[i][j] or [i,j] in salasLivres):
                    mundo[i][j]=["L"]
                    salasLivres.append([i,j])

    
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, N, \
            salasLivres, compartilhar, caminho, objetivo, mapa
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Quando as informações de outra personagem foram compartilhadas
    # atualiza o "mundo" local 
    if compartilhar: 
        compartilhar = False
        atualizaMundo()
    
    ori = orientacao
    pos = posicao
    # Verifica se existe alguma personagem na posição atual e ativa 
    # a flag compartilhar caso verdadeiro
    if len(percepcao)>0:
        percepcoes = ["F", "B", "I", "U"]
        for item in percepcao:
            if not(item in percepcoes):
                compartilhar = True
                break
    # Corrige o posicionamento da personagem quando ocorre um impacto
    if "I" in percepcao:
        if ori == [0,1] or ori == [0,-1]:
            pos[1]=(pos[1]-ori[1])%N
            mundo[pos[0]][(pos[1]+ori[1])%N] = ["M"]
        else: 
            pos[0]=(pos[0]-ori[0])%N
            mundo[(pos[0]+ori[0])%N][pos[1]] = ["M"]
    # Caso não ocorra um impacto, atualiza a posição atual
    else:
        mundo[pos[0]][pos[1]] = ["V"]  
        #percepcoes = ["F","B"]
        #for item in percepcoes:
        #    if item in percepcao and not(item in mundo[pos[0]][pos[1]]):
        #        mundo[pos[0]][pos[1]].append(item)

    conhecidos = [["P"],["M"],["L"],["W"],["V"]]
    # Lista com as posições das salas vizinhas a posição atual
    vizinhos = [[(pos[0]+1)%N,pos[1]],[(pos[0]-1)%N,pos[1]],  \
                [pos[0],(pos[1]-1)%N],[pos[0],(pos[1]+1)%N]]
    # Incorpora a inferência sobre a percepcao nas salas adjacentes
    for sala in vizinhos:
    
        if not(mundo[sala[0]][sala[1]] in conhecidos):
            if "F" in percepcao and not("W?" in mundo[sala[0]][sala[1]]):
                mundo[sala[0]][sala[1]].append("W?")
            if "B" in percepcao and not("P?" in mundo[sala[0]][sala[1]]):
                mundo[sala[0]][sala[1]].append("P?")
            if "U" in percepcao and not("U?" in mundo[sala[0]][sala[1]]):
                mundo[sala[0]][sala[1]].append("U?")
            if [] == percepcao and not("L" in mundo[sala[0]][sala[1]]):
                mundo[sala[0]][sala[1]].append("L")
                salasLivres.append([sala[0],sala[1]])
    # Quando existem salas livres conhecidas e o personagem não encontra-se
    # em deslocamento tenta encontrar um caminho para alguma sala livre 
    if len(caminho)==0 and len(salasLivres)>0:
        objetivo = salasLivres.pop(0)
        encontraCaminho()
   
    
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        print("Salas livres:",salasLivres)
        print("Caminho:",caminho)

        ori = orientacao
        pos = posicao
        # Mostra na tela (para o usuário) o mundo conhecido pela personagem
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
                print("".join(mundo[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))

def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, N, caminho, compartilhar
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

    pos = posicao
    ori = orientacao
    # Declara a posição da sala a frente e a esquerda da personagem 
    # para facilitar a tomada de decisão 
    frente = [(pos[0]+ori[0])%N, (pos[1]+ori[1])%N]
    esquerda = [(pos[0]-ori[1])%N,(pos[1]+ori[0])%N]

    # Caso exista outro personagem na posição atual, compartilha informações 
    if compartilhar:
        return "C"
    # Se na posição a frente da personagem há um Wumpus, então o personagem atira
    # caso tenha flechas.
    elif "W" in mundo[frente[0]][frente[1]] and nFlechas>0:
        return "T"  
    # Se o personagem está em deslocamento avalia as posições adjacentes
    # e determina uma ação
    elif len(caminho)>0:   
        if frente == caminho[0]: #Se a posição a frente é a desejada avança.
            caminho.pop(0)
            acao = "A"
            pos[0] = (pos[0]+ori[0])%N
            pos[1] = (pos[1]+ori[1])%N
        elif esquerda == caminho[0]: # Se é a posição a esquerda, vira a esquerda.
            acao = "E"
            if ori[0]==0:
                ori[1] = -ori[1]
            ori[0],ori[1] = ori[1],ori[0]
        else: #Caso contrário, vira a direita.
            acao = "D"
            if ori[1]==0:
                ori[0] = -ori[0]
            ori[0],ori[1] = ori[1],ori[0]
    # Se nenhuma das condições acima são satisfeitas, o personagem gira até
    # até encontrar outra personagem
    else:
        acao = "D"
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]

    assert acao in ["A","D","E","T","C"]
    return acao
