
""" Módulo personagem10737136: define as funções básicas de gerenciamento
    da personagem10737136 no Mundo de Wumpus.
"""


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


# Outras variáveis globais do módulo personagem10737136

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

global salas_livres
"""
Lista das salas livres ainda não visitadas
"""

global tentou_andar
"""
Controle booleano para conferir se o movimento foi possível 
"""

global visita
"""
Controle booleano para conferir se a ação C é possível
"""

global caminho
"""

"""

global destino

global mapa_guiado

global salas_possivelmente_livres
"""
Controle booleano para quando ficar triste e querer tentar entregar sua vida a sorte
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
    global N,salas_possivelmente_livres, mundo, posicao, orientacao, salas_livres, tentou_andar, visita, caminho, mapa_guiado, destino, se_jogar_no_poco
    # guarda o tamanho do mundo
    N = tamanho
    salas_livres = []
    salas_possivelmente_livres = []
    tentou_andar = False
    visita = False
    caminho = []
    destino = [0,0]
    reseta_mapa_guiado()
    se_jogar_no_poco = False
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
    mundo[0][0] = ["V"]

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, visita, N, mapa_guiado, salas_possivelmente_livres
	
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).

    pos = posicao
    ori = orientacao
    
    #Tratamento do mundo Compartilhado:
    #Confiar em casas livres, muros e poços, pois economizam o trabalho de descobrí-los
    #Não registrar Wumpus porque eles podem não mais existir
    #Não registrar possíveis poços pois posso sentí-los eu mesmo e confiar na minha própria informação
    #Não registrar possíveis Wumpus pois posso sentí-los eu mesmo
    
    for a in range(N):
        for b in range(N):
            if ("L" in mundoCompartilhado[a][b] or "V" in mundoCompartilhado[a][b]) and ("V" not in mundo[a][b] and "P" not in mundo[a][b]):
                mundo[a][b] = ["L"]
                if [a,b] not in salas_livres:
                    salas_possivelmente_livres.append([a,b])
            else:
                if "P" in mundoCompartilhado[a][b]:
                    mundo[a][b] = ["P"]
                if "M" in mundoCompartilhado[a][b]:
                    if [a,b] in salas_livres:
                        salas_livres.remove([a,b])
                    mundo[a][b] = ["M"]
  
    if salas_possivelmente_livres != []:
        for sala in salas_possivelmente_livres:
            if sala not in salas_livres:
                vizinhas = [[sala[0],(sala[1] + 1)%N],
                         [sala[0],(sala[1] - 1)%N],
                         [(sala[0] + 1)%N,sala[1]],
                         [(sala[0] - 1)%N,sala[1]]] 
                #se é vizinha de alguma já vizitada então é visitável
                for sala2 in vizinhas:
                    if "V" in mundo[sala2[0]][sala2[1]] and "V" not in mundo[sala[0]][sala[1]] and "P" not in mundo[sala[0]][sala[1]]: 
                        salas_livres.append(sala)
    
    if tentou_andar:
        #Havendo ou não havendo muro, 
        #deve-se retirar a sala pretendida da lista das salas para visitar
        if [(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)] in salas_livres:
            salas_livres.remove([(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)])
        if [(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)] in salas_possivelmente_livres:
            salas_possivelmente_livres.remove([(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)])
        if "I" not in percepcao:    
            #Anda
            pos[0] = (pos[0]+ori[0])%len(mundo)
            pos[1] = (pos[1]+ori[1])%len(mundo)
            #Marca o "V"
            if "V" not in mundo[pos[0]][pos[1]]:   
                mundo[pos[0]][pos[1]].append("V")
                if "L" in mundo[pos[0]][pos[1]]:  
                    mundo[pos[0]][pos[1]].remove("L")
                
        #Se recebeu "I" então há um muro
        else:
            #Marca o muro
            mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ["M"]         
        
    
    #Posições das 4 salas vizinhas à atual
    posicoes_vizinhas = [[pos[0],(pos[1] + 1)%N],
                         [pos[0],(pos[1] - 1)%N],
                         [(pos[0] + 1)%N,pos[1]],
                         [(pos[0] - 1)%N,pos[1]]]
    
    visita = False
    for p in percepcao:
        if p == "F":
            marca_salas("W?",posicoes_vizinhas)
            if "F" not in mundo[pos[0]][pos[1]]:
                mundo[posicao[0]][posicao[1]].append("F")
     
        elif p == "B":
            marca_salas("P?",posicoes_vizinhas)
            if "B" not in mundo[pos[0]][pos[1]]:
                mundo[posicao[0]][posicao[1]].append("B")
        
        #Se a percepção não for F, B, I nem u então há um personagem
        elif p != "I" and p != "U":
            visita = True
        
    if "B" not in percepcao and "F" not in percepcao:
        marca_salas("L",posicoes_vizinhas)
        adiciona_livres(posicoes_vizinhas)
    
        
         
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)       
            
        
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        
        #mundo[pos[0]][pos[1]] = ["V"]
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
            print("\n"+"-"*(8*len(mundo)+1))
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

def marca_salas(conteudo, posicoes):
    """ Função que insere um conteúdo nas salas enviadas,
        o conteúdo deve estar de acordo com a percepção recebida.
        Salas já conhecidas não serão marcadas
    """
    global mundo
    for pos in posicoes:
        #Se a sala ainda não foi visitada, o conteúdo "L" deve sobrescrever qualquer outra marcação da sala
        if conteudo == "L":
            if "V" not in mundo[pos[0]][pos[1]] and "M" not in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]] = ["L"]
        #Se a sala já não for conhecida
        elif not(("V" in mundo[pos[0]][pos[1]]) 
              or ("L" in mundo[pos[0]][pos[1]]) 
              or ("M" in mundo[pos[0]][pos[1]]) 
              or ("P" in mundo[pos[0]][pos[1]])):
            #Se a sala ainda não tiver aquela marcação
            #para evitar coisas do tipo ["P?","P?","P?"]
            if conteudo not in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]].append(conteudo)
               
                
def adiciona_livres(posicoes):
    """ Recebe uma matriz 2xN com as posições das N salas livres descobertas 
        e adiciona as que ainda não foram exploradas na lista salas_livre
    """     
    global salas_livres      
    for pos in posicoes:
        #se a posicao já não estiver marcada e não for uma sala já visitada
        if not(pos in salas_livres) and not ("V" in mundo[pos[0]][pos[1]] or "M" in mundo[pos[0]][pos[1]]): 
            salas_livres.append(pos)
                
            
def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """    # declara as variáveis globais que serão acessadas
    global destino, caminho, mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salas_livres, tentou_andar, visita, se_jogar_no_poco
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
    
    #Se for possível o compartilhamento,
    #a ação será "C"
    if visita:
        tentou_andar = False
        return "C"
    
    #Confere se consigo chegar nas possíveis salas livres para não tentar chegar numa sala que eu não consigo achar o caminho
    
    #Se tem salas livres para visitar ainda
    if salas_livres != []:
        #Só calculará um novo caminho
        #se chegar no destino anterior
        #Para evitar que ele troque de destino no meio do caminho e entre num loop
        if mundo[destino[0]][destino[1]] != ["L"]:
            destino = acha_livre_perto()
            #Atualiza a variável caminho e o mapa que estava guiado pelo destino anterior
            reseta_mapa_guiado()
            define_caminho(destino, 0)
        
        #Se o caminho acabou   
        if len(caminho) == 0:
            #Podemos chegar ao destino
            acao = passo_pra_vizinha(destino)
            
        #Se ainda tem caminho e eu cheguei na próxima posição dele
        elif (caminho[0] == posicao):
            #Se tem outra posicao pra ir
            if len(caminho) != 1:    
                #Podemos ir para a próxima posição
                caminho = caminho[1:]
                acao = passo_pra_vizinha(caminho[0])     
            else:
                acao = passo_pra_vizinha(destino)    
        #Se ainda tem um caminho longo, podemos só realizar a ação tranquilamente  
        else:
            #Podemos chegar ao destino
            acao = passo_pra_vizinha(caminho[0])

    #se não há salas livres vai ficar rodando sempre pra direita até alguém aparecer
    else:
        acao = "D"
    #Especificações das ações
    ori = orientacao
    if acao=="A":
        tentou_andar = True
    else:
        tentou_andar = False
        if acao=="E":
            if ori[0]==0:
                ori[1] = -ori[1]
            ori[0],ori[1] = ori[1],ori[0]
        elif acao=="D":
            if ori[1]==0:
                ori[0] = -ori[0]
            ori[0],ori[1] = ori[1],ori[0]

    assert acao in ["A","D","E","T","C"]
    return acao

def acha_livre_perto():
    global posicao, mapa_guiado
    
    for sala in salas_livres:
        if "V" in mundo[sala[0]][sala[1]] or "P" in mundo[sala[0]][sala[1]] or "W" in mundo[sala[0]][sala[1]]:
            salas_livres.remove(sala)
    
    perto = salas_livres[-1]

    #Inicializa a distancia com a distância da última sala da lista
    #Calculando a distancia modular vertical + horizontal
    dist = mapa_guiado[perto[0]][perto[1]]
    #Verifica a distancia das outras salas
    for s in range(len(salas_livres) - 2):
        if mapa_guiado[perto[0]][perto[1]] < dist:
            dist = mapa_guiado[perto[0]][perto[1]]
            perto = salas_livres[s]
    return perto

def define_caminho(destino, i):
    """ Função que encontra um caminho da posição atual até o destino e numera as salas,
        atualizando o mapa_guiado
        como no problema do rato 
    """
    global N, mundo, posicao, caminho
    fim_recursao = False
    if i == 0:
        fim_recursao = True
    mapa_guiado[destino[0]][destino[1]] = i
    i += 1

    posicoes_vizinhas = [[destino[0],(destino[1] + 1)%N],
                         [destino[0],(destino[1] - 1)%N],
                         [(destino[0] + 1)%N,destino[1]],
                         [(destino[0] - 1)%N,destino[1]]] 
    #acessivel = False
    for vizinha in posicoes_vizinhas:
        #Se a sala for conhecidamente visitável e fizer parte de um caminho mais curto
        if "V" in mundo[vizinha[0]][vizinha[1]]:
            #acessivel = True
            if (mapa_guiado[vizinha[0]][vizinha[1]] > i or mapa_guiado[vizinha[0]][vizinha[1]]==-1):
                define_caminho(vizinha, i)
            
    #Se estou tentando acessar uma sala livre inacessivel (passada pelo Dummy)
    #Quando já tiver completado as recursões,
    #Ou seja, quando o mapa estiver completo, achará o caminho     
    if fim_recursao: 
        caminho = []     
        
        #print("mapa guiado")
        #for m in range(len(mundo)):
        #    for j in range(len(mundo[0])):
        #        print(mapa_guiado[m][j],end="\t| ")          
        #    print("\n"+"-"*(8*len(mundo)+1))
        
        caminho_mais_curto(posicao)
    #if not acessivel:
        #return "inacessivel"
    if vizinha == posicao:
        return #"acessivel"
    
    
def caminho_mais_curto(pos):
    """ Função que definirá uma lista das salas que compõem o caminho mais curto ao destino,
        (sem incluir as extremidades)
        de acordo com o mapa_guiado atual, colocando na variável global caminho
    """
    global caminho, mapa_guiado
    posicoes_vizinhas = [[pos[0],(pos[1] + 1)%N],
                         [pos[0],(pos[1] - 1)%N],
                         [(pos[0] + 1)%N,pos[1]],
                         [(pos[0] - 1)%N,pos[1]]] 
    distancia = -1
    for vizinha in posicoes_vizinhas:
        #Se a vizinha faz parte de algum caminho
        if mapa_guiado[vizinha[0]][vizinha[1]] != -1:
            #se a distancia ainda não tiver sido alterada
            if distancia == -1:
                #'inicializa' a sala mais proxima
                distancia = mapa_guiado[vizinha[0]][vizinha[1]]
                proxima_sala = vizinha
            #se a vizinha for mais perto que a vizinha atualmente escolhida, reescolhe
            elif mapa_guiado[vizinha[0]][vizinha[1]] < distancia:
                proxima_sala = vizinha

    
    #Adiciona a próxima sala ao caminho print(proxima_sala, proxima_sala != destino, destino, caminho)
    if proxima_sala != destino:
        caminho.append(proxima_sala)
        caminho_mais_curto(proxima_sala)

    
    
def passo_pra_vizinha(vizinha):
    """ Função que retorna um próximo passo (ação) necessário para
        locomover a personagem para alguma sala vizinha especificada
    """
    global posicao, orientacao, caminho, N
    if [(posicao[0] + orientacao[0])%N,(posicao[1] + orientacao[1])%N] != vizinha:
        #O intuito é girar em sentido horário até achar a direção certa
        return "D"
    
    #Quando a orientação estiver correta, andar        
    return "A"

    
def reseta_mapa_guiado():
    global mapa_guiado
    mapa_guiado = []
    for m in range(N) : 
        linha = [-1]
        for j in range(N) : 
            linha.append(-1) # começa com listas de -1
        mapa_guiado.append(linha)