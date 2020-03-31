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
Matriz que armazena valores em cada posição correspondentes à distância
dessa posição até uma casa livre (armazenada na lista "livres").
-1 significa que a posição não está livre/não foi visitada
Matriz inicializada com -1's e 0's.
"""

global compartilhar
"""
Variável booleana que determina se haverá compartilhamento de 
informações entre personagens.
"""

global compartilhado
"""
Variável booleana que informa a função planejar que na última rodada
a "agir" compartilhou.
"""

global livres
"""
Matriz de casas livres adjacentes.
"""

global andando
"""
Variável booleana que é verdadeira quando o personagem está executando
uma ação e falsa quando está planejando a próxima ação.
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
    global N, mundo, posicao, orientacao, livres, andando, caminho
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
    #matrizes inicializadas como listas vazias
    livres = []
    caminho = []
    andando = False #começando parado
    mundo[0][0].append("L") #inicializando tornando a casa inicial "livre"


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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, caminho, compartilhar, compartilhado, livres, andando
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.
    compartilhar = False #inicializando
    pos = posicao
    ori = orientacao
    percepcoes = ["F","B","I","U"] #lista de percepções comuns
    mundo[pos[0]][pos[1]] = ["V"] 
    if "I" in percepcao: #indica posições com muros e arruma a posição do personagem
                mundo[pos[0]][pos[1]] = ["M"]
                pos = [(pos[0]-ori[0])%N,(pos[1]-ori[1])%N]
                posicao = pos
    adjacentes = [ [(pos[0]+1)%N,pos[1]], #matriz que contém as posições adjacentes à posição analisada
                     [(pos[0]-1)%N,pos[1]],
                     [pos[0],(pos[1]+1)%N],
                     [pos[0],(pos[1]-1)%N] ]
    for i in percepcao: 
        if not (i=="F" or i=="B" or i=="U" or i=="I"): #significa que há uma personagem!
            compartilhar = True
    if "B" not in percepcao and "F" not in percepcao: #casa livre!
        for adj in adjacentes: #marcar como LIVRE os vizinhos e remover outras suposições
            if "L" not in mundo[adj[0]][adj[1]] and "M" not in mundo[adj[0]][adj[1]] and "V" not in mundo[adj[0]][adj[1]]:
                mundo[adj[0]][adj[1]].append("L")
                livres.append(adj)
                if "W?" in mundo[adj[0]][adj[1]]:
                   mundo[adj[0]][adj[1]].remove("W?")
                if "P?" in mundo[adj[0]][adj[1]]:
                   mundo[adj[0]][adj[1]].remove("P?")          
    else:        
        if "F" in percepcao:  #possíveis Wumpus indicados          
            for adj in adjacentes:
                if "W?" not in mundo[adj[0]][adj[1]] and "W" not in mundo[adj[0]][adj[1]] and "P" not in mundo[adj[0]][adj[1]] and "V" not in mundo[adj[0]][adj[1]] and "L" not in mundo[adj[0]][adj[1]] and "M" not in mundo[adj[0]][adj[1]]:
                    mundo[adj[0]][adj[1]].append("W?")
            if "F" not in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]].append("F")
        if "B" in percepcao:  #possíveis poços indicados           
            for adj in adjacentes:
                if "P?" not in mundo[adj[0]][adj[1]] and  "P" not in mundo[adj[0]][adj[1]] and "W" not in mundo[adj[0]][adj[1]] and "V" not in mundo[adj[0]][adj[1]] and "L" not in mundo[adj[0]][adj[1]] and "M" not in mundo[adj[0]][adj[1]]:
                   mundo[adj[0]][adj[1]].append("P?")
            if "B" not in mundo[pos[0]][pos[1]]:       
                mundo[pos[0]][pos[1]].append("B")                        
        if compartilhado: #quando encontra com outras personagens, compartilha e reitera seu mapa com as novas informações
            for i in range(len(mundo)):
                for j in range(len(mundo[i])):
                    for k in range(len(mundo[i][j])):
                        if "L" not in mundo[i][j] and "V" not in mundo[i][j]:
                            if "L" in mundoCompartilhado[i][j] or "V" in mundoCompartilhado[i][j]:
                                mundo[i][j] = ["L"]
                                livres.append([i,j])
                            if "W?" in mundoCompartilhado[i][j] and ("W?" not in mundo[i][j] or "W" not in mundo[i][j]):
                                mundo[i][j].append("W?")
                            if "W" in mundoCompartilhado[i][j] and "W" not in mundo[i][j]:
                                mundo[i][j] = ["W"]
                            if "P?" in mundoCompartilhado[i][j] and ("P?" not in mundo[i][j] or "P" not in mundo[i][j]):
                                mundo[i][j].append("P?")
                            if "P" in mundoCompartilhado[i][j] and "P" not in mundo[i][j]:
                                mundo[i][j] = ["P"]
                            if "M" in mundoCompartilhado[i][j] and "M" not in mundo[i][j]:
                                mundo[i][j] = ["M"] 

    #Traçando o caminho para preencher todas as casas livres:                                                    
    if len(livres) > 0 and not andando: 
        caminho = []   #reseta a matriz caminho         
        for i in range(N):
                caminho.append([-1]*N) #cronstrói a matriz caminho com -1's
        for i in range(N):
            for j in range(N):            
                if "L" in mundo[i][j] or "V" in mundo[i][j]: #preenche com 0 as casas livres
                    caminho[i][j] = 0
                
        caminho[livres[0][0]][livres[0][1]] = 1   #meu objetivo         
        lista = []   #lista de busca: guarda as salas que ainda precisamos preencher      
        lista.append(livres.pop(0))
        while lista != []: 
            distancia = lista.pop(0) #posição que queremos alcançar nesta jogada
            dist = caminho[distancia[0]][distancia[1]] #valor da posição que queremos alcançar nesta jogada 
            i = distancia[0]
            j = distancia[1]
            adjacentes = [ [(i+1)%N,j], #adjacentes à posição "distância" que está sendo analisada
                     [(i-1)%N,j],
                     [i,(j+1)%N],
                     [i,(j-1)%N] ]
            for adj in adjacentes:
                if caminho[adj[0]][adj[1]] == 0:
                    caminho[adj[0]][adj[1]] = dist + 1 #soma de modo que quanto mais perto da posição objetivo, menor o valor
                    lista.append([adj[0],adj[1]])
        andando = True            
                   
              
            
    if __DEBUG__: #matriz de percepções (mundo)
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # mostra na tela (para o usuário) o mundo conhecido pela personagem
        # e o mundo compartilhado (quando disponível)
        print("Mundo conhecido pela personagem:")
        for i in range(N):                
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
    


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, N, caminho, compartilhar, compartilhado, andando
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
    compartilhado = False
    pos = posicao
    ori = orientacao
    adjacentes = [ [(pos[0]+1)%N,pos[1]], #matriz que contém as posições adjacentes à posição analisada
                     [(pos[0]-1)%N,pos[1]],
                     [pos[0],(pos[1]+1)%N],
                     [pos[0],(pos[1]-1)%N] ] 
    if compartilhar: #compartilha informação (prioridade)
        acao = "C"
        compartilhado = True #para que na próxima leitura da planejar, as matrizes compartilhadas se fundam
    else:                                         
        for adj in adjacentes:
            if caminho[adj[0]][adj[1]] < caminho[pos[0]][pos[1]] and caminho[adj[0]][adj[1]] != -1: #se há uma posição ao redor com valor distância menor do que a posição atual
                if (pos[0] + ori[0])%N == adj[0] and (pos[1] + ori[1])%N == adj[1]: #se a posição livre está à frente, anda
                    acao = "A"
                    if caminho[adj[0]][adj[1]] == 1:
                        andando = False
                else:
                    acao = "E"   
                break
            elif "W" in mundo[adj[0]][adj[1]]: #se há um Wumpus nas casas adjacentes
                if (pos[0] + ori[0])%N == adj[0] and (pos[1] + ori[1])%N == adj[1] and nFlechas>0: #se essa casa está à frente, atira
                    acao = "T" #atira se há flechas      
            else:
                acao = "E" #fica girando até chegar outro personagem para compartilhar informações       
    #Traduz as ações para movimentos:            
    if acao=="A": 
        pos[0] = (pos[0]+ori[0])%N
        pos[1] = (pos[1]+ori[1])%N
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
