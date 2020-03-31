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


def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, livres, andando, mBFS
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N):
       linha = []
       for j in range(N):
           linha.append([]) #começa com listas vazias
       mundo.append(linha)

    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    livres = []
    andando = False
    mBFS = []



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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, comp , livres, mBFS, andando
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
    pos = posicao
    #lista de casas adjacentes
    adj = [ [(pos[0]+1)%N,pos[1]],
            [(pos[0]-1)%N,pos[1]],
            [pos[0],(pos[1]+1)%N],
            [pos[0],(pos[1]-1)%N] ]
    #variavel que será usada para definir o uso ou não da ação 'C'
    comp = False
    # atualiza o lugar onde houve impacto para muro e arruma a posição para o lugar certo
    if 'I' in percepcao:
        mundo[pos[0]][pos[1]] = ['M']
        posicao = [(pos[0] - ori[0])%N,(pos[1] - ori[1])%N]

    # arruma a posição para visitada caso ela não seja um muro
    if 'I' not in percepcao:
        mundo[posicao[0]][posicao[1]] = ['V']

    #se não houver nem brisa e nem poço, as casas adjacentes que não sao muros estão livres
    if 'B' not in percepcao and 'F' not in percepcao:

        for a in range(4):
            if 'M' not in mundo[adj[a][0]][adj[a][1]] and 'V' not in mundo[adj[a][0]][adj[a][1]]:
                mundo[adj[a][0]][adj[a][1]] = ['L']
                livres.append([adj[a][0],adj[a][1]])


    itens_perc = len(percepcao)
    possibilidades = 0
    # loop que passa por cada item da percepção
    for k in range(itens_perc):

        #se a percepcao tiver fedor:
        if percepcao[k] == 'F':

           #conta quantos wumpus determinados existem nas casas adjacentes
            wumpus_det = 0
            for f in range(4):
                if mundo[adj[f][0]][adj[f][1]] == ['W']:
                    wumpus_det = wumpus_det + 1
            
            #conta em quantas casas adjacentes ainda existe a possibilidade de ter wumpus
            for i in range(4):
                if mundo[adj[i][0]][adj[i][1]] == [] or 'P?' in mundo[adj[i][0]][adj[i][1]] or 'W?' in mundo[adj[i][0]][adj[i][1]] :
                    possibilidades = possibilidades + 1
                else:
                    possibilidades = possibilidades + 0


            for j in range(4):

                #se só houver um lugar possivel de ter wumpus, não houver nenhum wumpus marcado ainda e a casa adjacente for P?,W?,P?W? ou W?P?:
                if possibilidades == 1 and wumpus_det == 0 and ('P?' in mundo[adj[j][0]][adj[j][1]] or 'W?' in  mundo[adj[j][0]][adj[j][1]] or mundo[adj[j][0]][adj[j][1]] == []):
                    mundo[adj[j][0]][adj[j][1]] = ['W']

                #se houver mais de um lugar possivel de ter wumpus ou houver só um lugar possiver mas ja houver pelo menos um wumpus já marcado e a casa adj estiver vazia:
                if (possibilidades > 1 or (possibilidades == 1 and wumpus_det >= 1)) and mundo[adj[j][0]][adj[j][1]] == [] :
                    mundo[adj[j][0]][adj[j][1]] = ['W?']

                #se houver mais de um lugar possivel de ter wumpus ou houver só um lugar possiver mas ja houver pelo menos um wumpus já marcado e a casa adj for P?
                if (possibilidades > 1 or (possibilidades == 1 and wumpus_det >= 1)) and ('P?' in mundo[adj[j][0]][adj[j][1]]):
                    mundo[adj[j][0]][adj[j][1]].append('W?')

        #se a percepcao tiver brisa
        elif percepcao[k] =='B':

            #conta quantos poços determinados existem nas casas adjacentes
            poço_det = 0
            for f in range(4):
                if mundo[adj[f][0]][adj[f][1]] == ['P']:
                    poço_det = poço_det + 1

            #conta em quantas casas adjacentes ainda existe a possibilidade de ter poço
            for i in range(4):
                if mundo[adj[i][0]][adj[i][1]] == [] or 'W?' in mundo[adj[i][0]][adj[i][1]] or  'P?' in mundo[adj[i][0]][adj[i][1]]:
                    possibilidades = possibilidades + 1
                else:
                    possibilidades = possibilidades + 0

            for j in range(4):

                #se só houver um lugar possivel de ter poço, não houver nenhum poço marcado ainda e a casa adjacente for P?,W?,P?W? ou W?P?:
                if possibilidades == 1 and poço_det == 0 and ('P?' in mundo[adj[j][0]][adj[j][1]]  or 'W?' in mundo[adj[j][0]][adj[j][1]] or mundo[adj[j][0]][adj[j][1]] == [] ):
                    mundo[adj[j][0]][adj[j][1]] = ['P']

                #se houver mais de um lugar possivel de ter poço ou houver só um lugar possiver mas ja houver pelo menos um poço já marcado e a casa adj estiver vazia:
                if (possibilidades > 1 or (possibilidades == 1 and poço_det >= 1)) and mundo[adj[j][0]][adj[j][1]] ==[]:
                    mundo[adj[j][0]][adj[j][1]] = ['P?']

                #se houver mais de um lugar possivel de ter poço ou houver só um lugar possiver mas ja houver pelo menos um wumpus já marcado e a casa adj for W?,P?W? ou W?P?:
                if (possibilidades > 1 or (possibilidades == 1 and poço_det >= 1)) and ('W?' in  mundo[adj[j][0]][adj[j][1]]):
                    mundo[adj[j][0]][adj[j][1]].append('P?')


        # se a percepcao tiver o nome de alguem
        elif percepcao[k] != 'U' and percepcao[k] != 'I':
            #se percepcao tem um nome, o compartilhamento tem q acontecer em agir
            comp = True
            for i in range(N):
                for j in range(N):
                    #se a casa no meu mundo nao tiver nada e o que tiver no da pessoa não for livre:
                    if mundo[i][j] == [] and  mundoCompartilhado[i][j] != ['L']:
                        #se no mundo da outra pessoa tiver um V, entra no meu como L
                        if mundoCompartilhado[i][j] == ['V']:
                            mundo[i][j] = ['L']
                            livres.append([i,j])
                        # de resto, só copia
                        else:
                            mundo[i][j] = mundoCompartilhado[i][j]

                    # se no meu mundo for um P? e no da pessoa for qualquer coisa que não vazio ou L:
                    if mundo[i][j] == ['P?'] and mundoCompartilhado[i][j] != [] and mundoCompartilhado[i][j] != ['L']:
                        #se no mundo da pessoa tiver um W?, no meu vira um P?W?
                        if mundoCompartilhado[i][j] == ['W?']:
                            mundo[i][j].append('W?')
                        #se no mundo da pessoa tiver um V, no meu vira um L
                        elif mundoCompartilhado[i][j] == ['V']:
                             mundo[i][j] = ['L']
                        
                             livres.append([i,j])
                        #de resto, só copia
                        else:
                            mundo[i][j] = mundoCompartilhado[i][j]

                    #se no meu mundo tiver um W? e o da pessoa não for vazio nem livre :
                    if mundo[i][j] == ['W?'] and mundoCompartilhado[i][j] != [] and mundoCompartilhado[i][j] != ['L']:
                        #se no mundo dela for um P?, entra no meu como W?P?
                        if mundoCompartilhado[i][j] == ['P?']:
                            mundo[i][j].append('P?')
                        #se no mundo dela for V, entra no meu como L
                        elif mundoCompartilhado[i][j] == ['V']:
                            mundo[i][j] = ['L']
                    
                            livres.append([i,j])
                        # de resto, só copia
                        else:
                            mundo[i][j] = mundoCompartilhado[i][j]

                    # se no meu mundo for W?P? ou P?W? e o na pessoa não for nem P? nem W? nem vazio nem L:
                    if ( 'W?' in mundo[i][j] and 'P?' in mundo[i][j] ) and (mundoCompartilhado[i][j] == ['P'] or mundoCompartilhado[i][j] == ['W'] and mundoCompartilhado[i][j] == ['L'] or mundoCompartilhado[i][j] == ['V'] or mundoCompartilhado[i][j] == ['M']) :
                        ##se no mundo dela for V, entra no meu como L
                        if mundoCompartilhado[i][j] == ['V']:
                            mundo[i][j] = ['L']
                            
                            livres.append([i,j])
                        # de resto, só copia
                        else:
                            mundo[i][j] = mundoCompartilhado[i][j]

    
    if not andando and len(livres) > 0:
        mBFS = bfs(N,mundo,livres)
        andando = True

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
    #
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # elimine o teste abaixo quando tiver corrigido o bug de movimentação...
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        pos = posicao
        ori = orientacao
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
                print("".join(mundo[i][j]),end="\t| ")
                # print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####
def bfs(N,matriz,livres):


    #cria uma matriz de busca
    mbusca = []
    for i in range(N):
       linha = []
       for j in range(N):
           linha.append(0)
       mbusca.append(linha)

    #cria uma lista de busca e numera a matriz de busca com 0 e -1
    for i in range(N):
        for j in range(N):
            if 'V' in matriz[i][j] or 'L' in  matriz[i][j]:
                mbusca[i][j] = 0
            else:
                mbusca[i][j] = -1
    #vou tirar meu objetivo da lista de livres
    objetivo = livres.pop(0)
    #vou colocar 1 nessa posicao na matriz de busca
    mbusca[objetivo[0]][objetivo[1]] = 1
    #vou colocar meu objetivo na lista de busca
    lbusca = []
    lbusca.append([objetivo[0],objetivo[1]])


    #lista dos adjacentes a casa livre
    # adj = [[(lbusca[0][0]+1)%N,lbusca[0][1]],
    #        [(lbusca[0][0]-1)%N,lbusca[0][1]],
    #        [lbusca[0][0],(lbusca[0][1]+1)%N],
    #        [lbusca[0][0],(lbusca[0][1]-1)%N]]

    mbusca[lbusca[0][0]][lbusca[0][1]] = 1

    #vou começar o laço
    while len(lbusca) > 0:
        sala = lbusca.pop(0)
        adj = [[(sala[0]+1)%N,sala[1]],
               [(sala[0]-1)%N,sala[1]],
               [sala[0],(sala[1]+1)%N],
               [sala[0],(sala[1]-1)%N]]
        valor= mbusca[sala[0]][sala[1]]

        
        for i in range(4):
            
            if mbusca[adj[i][0]][adj[i][1]] == 0:
                mbusca[adj[i][0]][adj[i][1]] = valor + 1
                lbusca.append([adj[i][0],adj[i][1]])

    
    return mbusca


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, comp, livres, mBFS, andando
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
    acao = 'D'
    ori = orientacao
    pos = posicao
    #lista de casas adjacentes
    adj = [ [(pos[0]+1)%N,pos[1]],
            [(pos[0]-1)%N,pos[1]],
            [pos[0],(pos[1]+1)%N],
            [pos[0],(pos[1]-1)%N] ]



    v_adj = 0 #numero de casas visitadas nas adjacencias
    w_adj = 0 #numero de casas com wumpus nas adjacencias
    per_adj = 0 #numero de casas perigosas nas adjacencias
    for k in range(4):
        if mundo[adj[k][0]][adj[k][1]] == ['W']:
            w_adj = w_adj + 1
        if mundo[adj[k][0]][adj[k][1]] != ['L'] and mundo[adj[k][0]][adj[k][1]] != ['W'] and mundo[adj[k][0]][adj[k][1]] != ['M'] and mundo[adj[k][0]][adj[k][1]] != ['V'] :
            per_adj =  per_adj + 1
        if mundo[adj[k][0]][adj[k][1]] == ['V']:
            v_adj =  v_adj + 1



    # se tiver aparecido um nome em percepcao e, portanto, comp tiver mudado de False para True deverá
    #ocorrer compartilhamento
    if comp == True:
        acao = 'C'

    #se tem wumpus na adj
    elif w_adj >= 1:
        i = 0
        while i <= 3:
            if mundo[[adj[i][0]][adj[i][1]]] == ['W']:
                if mundo[(pos[0] + ori[0])%N][(pos[1] + ori[1])%N] == mundo[adj[i][0]][adj[i][1]] and nFlechas > 0:
                    acao = 'T'
                    mundo[adj[i][0]][adj[i][1]] = ['L'] #atualiza a casa para livre agora que ela não tem mais o wumpus
                    nFlechas = nFlechas - 1 #atualiza o numero de flechas depois do tiro

                else:
                    acao = 'D'

                break
            i = i + 1


    elif len(livres) == 0 :
        acao = 'D'


    # se  tem livres no mundo e você nao esta enurralado por 4 casas perigosas
    else:
        
        
        for i in range(4):
            
            if  (mBFS[adj[i][0]][adj[i][1]] < mBFS[pos[0]][pos[1]] and mBFS[adj[i][0]][adj[i][1]] != -1) :
                
                
                if (pos[0] + ori[0])%N == adj[i][0] and (pos[1] + ori[1])%N == adj[i][1]:
                    
                    acao = 'A'
                    if mBFS[adj[i][0]][adj[i][1]] == 1:
                        
                        andando = False

                else:
                    acao = 'D'
                break





    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo é uma pseudo-implementação, pois recebe
    # a ação através de uma pergunta dirigida ao usuário.
    # No código a ser entregue, você deve programar algum tipo
    # de estratégia para
    

    # ATENÇÃO: a atualizacao abaixo está errada!!!
    # Não checa se o movimento foi possível ou não... isso só dá para
    # saber quando chegar uma percepção nova (a percepção "I"
    # diz que o movimento anterior não foi possível).
    pos = posicao
    ori = orientacao
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
