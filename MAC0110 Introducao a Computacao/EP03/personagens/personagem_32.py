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

global atirou_flecha
"""
Para marcar se a persongem atirou uma flecha e na próxima ação
poder verificar se matou um Wumpus
"""

global acao_compartilhar
"""

"""

global caminho_livre
"""
Lista de coordenadas de um caminho seguro até uma casa livre.
"""

global contador
"""
Conta quantas ações tivemos. A personagem aguardará um certo número de ações 
depois de não ter caminhos seguros, antes de tomar caminhos arriscados
enquanto isso, esperará por um resgate.
"""
global conta_passos
"""
Na busca por um caminho livre, conta quantos passos numa mesma diração
foram dados, para tentar mudar a estratégia.
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
    global N, mundo, posicao, orientacao, acao_anterior, acao_compartilhar, caminho_livre, contador, conta_passos
    acao_compartilhar = False
    acao_anterior = ""
    caminho_livre = []
    contador = 0
    conta_passos = 0
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, acao_anterior, acao_compartilhar, caminho_livre, conta_passos
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    #"L" para salas livres,
    #  e "V" para salas visitadas.
    pos = posicao
    ori = orientacao
    sala_f = mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]
    
    sala = []
    
    #atualiza a sala com "W" se a minha personagem matar um Wumpus
    if "W" in sala_f and "F" not in percepcao:
        sala_f.remove("W")
        
    # PERCEPÇÃO "I" (MURO)
    if "I" in percepcao:
        sala = mundo[pos[0]][pos[1]]
        if "M" not in sala:
            sala.append("M")
            if "L" in sala:
                sala.remove("L")
            if "P?" in sala:
                sala.remove("P?")
            if "W?" in sala:
                sala.remove("W?")
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)
        
    # PERCEPÇÃO - outro personagem
    for item in percepcao:
       if item not in ["F","B","I","U"]:
            acao_compartilhar = True

    # NÃO HÁ PERCEPÇÃO - MARCAR SALAS LIVRES
    if "F" not in percepcao and "B" not in percepcao:
        sala = mundo[(pos[0])%len(mundo)][(pos[1]-1)%len(mundo)]
        if "V" not in sala and "L" not in sala and "M" not in sala:
            sala.append("L")
            if "W?" in sala:
                sala.remove("W?")
            if "P?" in sala:
                sala.remove("P?")
        sala = mundo[(pos[0])%len(mundo)][(pos[1]+1)%len(mundo)]
        if "V" not in sala and "L" not in sala and "M" not in sala:
            sala.append("L")
            if "W?" in sala:
                sala.remove("W?")
            if "P?" in sala:
                sala.remove("P?")
        sala = mundo[(pos[0]-1)%len(mundo)][(pos[1])%len(mundo)]
        if "V" not in sala and "L" not in sala and "M" not in sala:
            sala.append("L")
            if "W?" in sala:
                sala.remove("W?")
            if "P?" in sala:
                sala.remove("P?")
        sala = mundo[(pos[0]+1)%len(mundo)][(pos[1])%len(mundo)]
        if "V" not in sala and "L" not in sala and "M" not in sala:
            sala.append("L")
            if "W?" in sala:
                sala.remove("W?")
            if "P?" in sala:
                sala.remove("P?")
    
    # PERCEPÇÃO "B" (POÇO)
    if "B" in percepcao:
        sala = mundo[pos[0]][pos[1]]
        if "B" not in sala:
            sala.append("B")
        sala = mundo[(pos[0])%len(mundo)][(pos[1]-1)%len(mundo)]
        if "V" not in sala and "L" not in sala and "P?" not in sala and "M" not in sala:
            sala.append("P?")
        sala = mundo[(pos[0])%len(mundo)][(pos[1]+1)%len(mundo)]
        if "V" not in sala  and "L" not in sala and "P?" not in sala and "M" not in sala:
            sala.append("P?")
        sala = mundo[(pos[0]-1)%len(mundo)][(pos[1])%len(mundo)]
        if "V" not in sala  and "L" not in sala and "P?" not in sala and "M" not in sala:
            sala.append("P?")
        sala = mundo[(pos[0]+1)%len(mundo)][(pos[1])%len(mundo)]
        if "V" not in sala  and "L" not in sala and "P?" not in sala and "M" not in sala:
            sala.append("P?")
    
    # PERCEPÇÃO "F" (WUMPUS)
    if "F" in percepcao:
        sala = mundo[pos[0]][pos[1]]
        if "F" not in sala:
            sala.append("F")
        sala1 = mundo[(pos[0])%len(mundo)][(pos[1]-1)%len(mundo)]
        sala2 = mundo[(pos[0])%len(mundo)][(pos[1]+1)%len(mundo)]
        sala3 = mundo[(pos[0]-1)%len(mundo)][(pos[1])%len(mundo)]
        sala4 = mundo[(pos[0]+1)%len(mundo)][(pos[1])%len(mundo)]
        if "V" not in sala1  and "L" not in sala1 and "W?" not in sala1 and "M" not in sala1 and "W" not in sala1:
            sala1.append("W?")
        if "V" not in sala2  and "L" not in sala2 and "W?" not in sala2 and "M" not in sala2 and "W" not in sala2:
            sala2.append("W?")        
        if "V" not in sala3  and "L" not in sala3 and "W?" not in sala3 and "M" not in sala3 and "W" not in sala3:
            sala3.append("W?")        
        if "V" not in sala4  and "L" not in sala4 and "W?" not in sala4 and "M" not in sala4 and "W" not in sala4:
            sala4.append("W?")
        contaW = ("W?" in sala1 or "W" in sala1) + ("W?" in sala2 or "W" in sala2) + ("W?" in sala3 or "W" in sala3) + ("W?" in sala4 or "W" in sala4)
        contaVL = (sala1 != []) + (sala2 != []) + (sala3 != []) + (sala4 != [])
        if contaW == 1 and contaVL == 4:
            if "W?" in sala1 and "W" not in sala1: ##confirmar que é um Wumpus (TEM QUE CONTAR NÃO VAZIAS, PODE SER MURO, OU POCO, MAS NÃO PODE SER VAZIA)
                sala1.remove("W?")
                sala1.append("W")
            if "W?" in sala2 and "W" not in sala2: 
                sala2.remove("W?")
                sala2.append("W")
            if "W?" in sala3 and "W" not in sala3: 
                sala3.remove("W?")
                sala3.append("W")
            if "W?" in sala4 and "W" not in sala4: 
                sala4.remove("W?")
                sala4.append("W")

    ## Confimar WUMPUS (W? -> W)
    ## verifica se nas salas diagonais e adjacentes (pulando 1 casa) se há W?
    for i in range(N):
        for j in range(N):
            if "W?" in mundo[i][j]:
                #diagonais
                sala1 = mundo[(i-1)%len(mundo)][(j-1)%len(mundo)]
                sala2 = mundo[(i-1)%len(mundo)][(j+1)%len(mundo)]
                sala3 = mundo[(i+1)%len(mundo)][(j-1)%len(mundo)]
                sala4 = mundo[(i+1)%len(mundo)][(j+1)%len(mundo)]
                #salas adjacentes (pulando 1 casa)
                sala5 = mundo[(i)%len(mundo)][(j-2)%len(mundo)]
                sala6 = mundo[(i)%len(mundo)][(j+2)%len(mundo)]
                sala7 = mundo[(i-2)%len(mundo)][(j)%len(mundo)]
                sala8 = mundo[(i+2)%len(mundo)][(j)%len(mundo)]
                if ("V" in sala1 or "L" in sala1) and ("V" in sala2 or "L" in sala2) and ("V" in sala3 or "L" in sala3) and ("V" in sala4 or "L" in sala4) and ("V" in sala5 or "L" in sala5) and ("V" in sala6 or "L" in sala6) and ("V" in sala7 or "L" in sala7) and ("V" in sala8 or "L" in sala8):
                        mundo[i][j].remove("W?")
                        if "W" not in mundo[i][j]:
                            mundo[i][j].append("W")
    
    # CAMINHO LIVRE
    # Procura um caminho segura até uma CASA LIVRE NÃO VISITADA
    # dado que todas as casa adjacente já são conhecidas
    # legenda (usando referências absolutas):
    # c -> cima
    # d -> direita
    # e -> esquerda
    # b -> baixo
    # procura um caminho em até N**2 casas
    caminho_livre = []
    pos2 = [pos[0],pos[1]]
    ultimo_passo = ""
    encontrouL = False
    i = 1
    while i <= N**2 and not encontrouL:
        i += 1
        # procura em mundo
        procura_c = mundo[(pos2[0]-1)%len(mundo)][(pos2[1])%len(mundo)]
        procura_d = mundo[(pos2[0])%len(mundo)][(pos2[1]+1)%len(mundo)]
        procura_e = mundo[(pos2[0])%len(mundo)][(pos2[1]-1)%len(mundo)]
        procura_b = mundo[(pos2[0]+1)%len(mundo)][(pos2[1])%len(mundo)]
        # procura em mundoCompartilhado
        procura2_c = mundoCompartilhado[(pos2[0]-1)%len(mundo)][(pos2[1])%len(mundo)]
        procura2_d = mundoCompartilhado[(pos2[0])%len(mundo)][(pos2[1]+1)%len(mundo)]
        procura2_e = mundoCompartilhado[(pos2[0])%len(mundo)][(pos2[1]-1)%len(mundo)]
        procura2_b = mundoCompartilhado[(pos2[0]+1)%len(mundo)][(pos2[1])%len(mundo)]
        # procura L nas redondezas
        if "L" in procura_c and ultimo_passo!="b":
            caminho_livre.append("c")
            pos2 = [pos2[0]-1,pos2[1]]
            if "L" in procura_c:
                encontrouL = True
        elif "L" in procura_d and ultimo_passo!="e":
            caminho_livre.append("d")
            pos2 = [pos2[0],pos2[1]+1]
            if "L" in procura_d:
                encontrouL = True
        elif "L" in procura_e and ultimo_passo!="d":
            caminho_livre.append("e")
            pos2 = [pos2[0]-1,pos2[1]]
            if "L" in procura_e:
                encontrouL = True
        elif "L" in procura_b and ultimo_passo!="c":
            caminho_livre.append("b")
            pos2 = [pos2[0]+1,pos2[1]]
            if "L" in procura_b:
                encontrouL = True
        # não encontrou L nas redondezas, procurar V
        elif "V" in procura_c and ultimo_passo!="b":
            caminho_livre.append("c")
            pos2 = [pos2[0]-1,pos2[1]]
            conta_passos += 1
        elif "V" in procura_d and ultimo_passo!="e":
            caminho_livre.append("d")
            pos2 = [pos2[0],pos2[1]+1]
            conta_passos += 1
        elif "V" in procura_e and ultimo_passo!="d":
            caminho_livre.append("e")
            pos2 = [pos2[0]-1,pos2[1]]
            conta_passos += 1
        elif "V" in procura_b and ultimo_passo!="c":
            caminho_livre.append("b")
            pos2 = [pos2[0]+1,pos2[1]]
            conta_passos += 1
        # utilizar informação compartilhada
                
        """
        elif conta_passos > N+1:
            caminho_livre.append(-1)
        #procura L em mundoComparilhado
        elif "L" in procura2_c and ultimo_passo!="b":
            caminho_livre.append("c")
            pos2 = [pos2[0]-1,pos2[1]]
            if "L" in procura_c:
                encontrouL = True
        elif "L" in procura2_d and ultimo_passo!="e":
            caminho_livre.append("d")
            pos2 = [pos2[0],pos2[1]+1]
            if "L" in procura2_d:
                encontrouL = True
        elif "L" in procura2_e and ultimo_passo!="d":
            caminho_livre.append("e")
            pos2 = [pos2[0]-1,pos2[1]]
            if "L" in procura2_e:
                encontrouL = True
        elif "L" in procura2_b and ultimo_passo!="c":
            caminho_livre.append("b")
            pos2 = [pos2[0]+1,pos2[1]]
            if "L" in procura2_b:
                encontrouL = True
        #procura V em mundoCompartilhado
        elif "V" in procura2_c and ultimo_passo!="b":
            caminho_livre.append("c")
            pos2 = [pos2[0]-1,pos2[1]]
        elif "V" in procura2_d and ultimo_passo!="e":
            caminho_livre.append("d")
            pos2 = [pos2[0],pos2[1]+1]
        elif "V" in procura2_e and ultimo_passo!="d":
            caminho_livre.append("e")
            pos2 = [pos2[0]-1,pos2[1]]
        elif "V" in procura2_b and ultimo_passo!="c":
            caminho_livre.append("b")
            pos2 = [pos2[0]+1,pos2[1]]
        # procura caminhos não seguros em mundo (Wumpus), se contador > 100
        else:
            contador += 1
            if contador > 100:
                if "W?" in procura_c and ultimo_passo!="b":
                    caminho_livre.append("c")
                    pos2 = [pos2[0]-1,pos2[1]]
                elif "W?" in procura_d and ultimo_passo!="e":
                    caminho_livre.append("d")
                    pos2 = [pos2[0],pos2[1]+1]
                elif "W?" in procura_e and ultimo_passo!="d":
                    caminho_livre.append("e")
                    pos2 = [pos2[0]-1,pos2[1]]
                elif "W?" in procura_b and ultimo_passo!="c":
                    caminho_livre.append("b")
                    pos2 = [pos2[0]+1,pos2[1]]
            # procura caminhos não seguros em mundo (Poço), se contador > 100
                if "P?" in procura_c and ultimo_passo!="b":
                    caminho_livre.append("c")
                    pos2 = [pos2[0]-1,pos2[1]]
                elif "P?" in procura_d and ultimo_passo!="e":
                    caminho_livre.append("d")
                    pos2 = [pos2[0],pos2[1]+1]
                elif "P?" in procura_e and ultimo_passo!="d":
                    caminho_livre.append("e")
                    pos2 = [pos2[0]-1,pos2[1]]
                elif "P?" in procura_b and ultimo_passo!="c":
                    caminho_livre.append("b")
                    pos2 = [pos2[0]+1,pos2[1]]
                    """
        ultimo_passo = caminho_livre[-1]
        
    print("caminho_livre",caminho_livre)
    if "V" not in mundo[pos[0]][pos[1]]:
        mundo[pos[0]][pos[1]].append("V")
        if "L" in mundo[pos[0]][pos[1]]:
            mundo[pos[0]][pos[1]].remove("L")

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
    # 
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
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


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, acao_compartilhar, caminho_livre, contador, conta_passos
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
    
    # acao_definida: verifica se uma ação já foi definida para não
    # verificar as outras condições
    acao_definida = False
    
    ##
    acao_anterior = ""
    
    pos = posicao
    ori = orientacao
    
    if acao_compartilhar:
        acao = "C"
        acao_definida = True
        acao_compartilhar = False

    # Definimos:
    #   sala_f: sala à frente da personagem
    #   sala_a: sala atrás da personagem
    #   sala_d: sala à direita da personagem
    #   sala_e: sala à esquerda da personagem
    sala_f = mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]
    sala_a = mundo[(pos[0]-ori[0])%len(mundo)][(pos[1]-ori[1])%len(mundo)]
    ori2 = [ori[0],ori[1]]
    if ori[0]==0:
        ori2[1] = -ori[1]
    sala_e = mundo[(pos[0]+ori2[1])%len(mundo)][(pos[1]+ori2[0])%len(mundo)]        
    ori2 = [ori[0],ori[1]]
    if ori[1]==0:
        ori2[0] = -ori[0]
    sala_d = mundo[(pos[0]+ori2[1])%len(mundo)][(pos[1]+ori2[0])%len(mundo)]
    
    if __DEBUG__:
        espera = input()    #para DEBUG pessoal - apertar enter para a próxima ação
        
    # Procura um Wumpus confirmado nas salas adjacentes
    # Neste caso, temos certeza de sua localização e atiraremos uma flecha
    if not acao_definida and nFlechas > 0:
        if "W" in sala_f:
            acao = "T"
            acao_definida = True
            acao_anterior = "T"
        elif "W" in sala_e:
            acao = "E"
            acao_definida = True
        elif "W" in sala_d:
            acao = "D"
            acao_definida = True
    
    # Procura SALAS LIVRES não visitadas na vizinhança (salas adjacentes)
    if not acao_definida:
        if "L" in sala_f:
            acao = "A"
            acao_definida = True
        elif "L" in sala_e:
            acao = "E"
            acao_definida = True
        elif "L" in sala_d:
            acao = "D"
            acao_definida = True
        
    #se não houver salas livres na vizinhança, percorrer a lista caminho_livre
    if not acao_definida:
        if caminho_livre[0] == "c":
            if ori == [-1,0]:
                acao = "A"
            if ori == [0,1]:
                acao = "E"
            if ori == [0,-1]:
                acao = "D"
            if ori == [1,0]:
                acao = "D"####
            acao_definida = True
        elif caminho_livre[0] == "d":
            if ori == [-1,0]:
                acao = "D"
            if ori == [0,1]:
                acao = "A"
            if ori == [0,-1]:
                acao = "D"###
            if ori == [1,0]:
                acao = "E"
            acao_definida = True
        elif caminho_livre[0] == "e":
            if ori == [-1,0]:
                acao = "E"
            if ori == [0,1]:
                acao = "D"###
            if ori == [0,-1]:
                acao == "A"
            if ori == [1,0]:
                acao = "D"
            acao_definida = True
        elif caminho_livre[0] == "b":
            if ori == [-1,0]:
                acao = "D"###
            if ori == [0,1]:
                acao = "D"
            if ori == [0,-1]:
                acao = "E"
            if ori == [1,0]:
                acao = "A"
            acao_definida = True

                
    # se não houver alternativa, girar
    if not acao_definida:
        acao = "D"
    
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
    assert acao in ["A","D","E","T","C"]
    return acao
