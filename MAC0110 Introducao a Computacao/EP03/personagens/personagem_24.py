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

global percepcao2
"""
Representa a variavel local percepcao, mas se tornando uma variavel global
para que possa ser usada em outras funções além de usar na função planejar.
"""

global mundoLivre
"""
Uma matriz NxN com a representação das casas Livres no mundo, para que a
personagem possa usá-la para explorar lugares novos.
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, percepcao2, mundoLivre
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
    percepcao2 = percepcao
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # essa atualização abaixo serve de ilustração/exemplo, e
        pos = posicao
        ori = orientacao
        # une o mundoCompartilhado com o mundo da personagem
        for i in range(len(mundo)):
            for j in range(len(mundo[0])):
                if "L" in mundoCompartilhado[i][j] and "V" not in mundo[i][j]:
                    if "W?" in mundo[i][j]:
                        mundo[i][j].remove("W?")
                    if "P?" in mundo[i][j]:
                        mundo[i][j].remove("P?")
                    if "L" in mundo[i][j]:
                        mundo[i][j].remove("L")
                    mundo[i][j].append("L")
                elif "M" in mundoCompartilhado[i][j]:
                    if "M" in mundo[i][j]:
                        mundo[i][j].remove("M")
                    if "W?" in mundo[i][j]:
                        mundo[i][j].remove("W?")
                    if "P?" in mundo[i][j]:
                        mundo[i][j].remove("P?")
                    if "L" in mundo[i][j]:
                        mundo[i][j].remove("L")
                    mundo[i][j].append("M")
                elif "V" in mundoCompartilhado[i][j]:
                    if "V" in mundo[i][j]:
                        mundo[i][j].remove("V")
                    if "W?" in mundo[i][j]:
                        mundo[i][j].remove("W?")
                    if "P?" in mundo[i][j]:
                        mundo[i][j].remove("P?")
                    if "L" in mundo[i][j]:
                        mundo[i][j].remove("L")
                    mundo[i][j].append("V")
                elif "P?" in mundoCompartilhado[i][j]:
                    if "W?" in mundo[i][j] or "" in mundo[i][j]:
                        mundo[i][j].append("P?")
                elif "W?" in mundoCompartilhado[i][j]:
                    if "P?" in mundo[i][j] or "" in mundo[i][j]:
                        mundo[i][j].append("W?")
        #  troca de variável para deixar o código mais claro na função
        baixo = mundo[(pos[0]+1)%len(mundo)][pos[1]]
        direita = mundo[pos[0]][(pos[1]+1)%len(mundo)]
        cima = mundo[(pos[0]-1)%len(mundo)][pos[1]]
        esquerda = mundo[pos[0]][(pos[1]-1)%len(mundo)]
        # marca as salas como "Visitadas" e troca V por L, caso haja L
        if "V" not in mundo[pos[0]][pos[1]]:
            if "L" in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]].remove("L")
            mundo[pos[0]][pos[1]].append("V")
        # quando a personagem bate em um muro, ela marca a casa como visitada e
        # marca a posição que tentou acessar como Muro também.
        if "I" in percepcao:
            if "M" not in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]].append("M")
            pos[0] = (pos[0]-ori[0])%len(mundo)
            pos[1] = (pos[1]-ori[1])%len(mundo)
        # marca com F quando está perto do monstro malígno e as possíveis casas
        # adjacentes onde um Wumpus pode estar está com W?
        elif "F" in percepcao:
            if "F" not in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]].append("F")
            if "W?" not in baixo and "L" not in baixo and "V" not in baixo and "M" not in baixo:
                mundo[(pos[0]+1)%len(mundo)][pos[1]].append("W?")
            if "W?" not in direita and "L" not in direita and "V" not in direita and "M" not in direita:
                mundo[pos[0]][(pos[1]+1)%len(mundo)].append("W?")
            if "W?" not in cima and "L" not in cima and "V" not in cima and "M" not in cima:
                mundo[(pos[0]-1)%len(mundo)][pos[1]].append("W?")
            if "W?" not in esquerda and "L" not in esquerda and "V" not in esquerda and "M" not in esquerda:
                mundo[pos[0]][(pos[1]-1)%len(mundo)].append("W?")
        # marca com B quando sentir um brisa por perto e as possíveis casas
        # adjacentes onde um poço pode estar com P?
        elif "B" in percepcao:
            if "B" not in mundo[pos[0]][pos[1]]:
                mundo[pos[0]][pos[1]].append("B")
            if "P?" not in baixo and "L" not in baixo and "V" not in baixo and "M" not in baixo:
                mundo[(pos[0]+1)%len(mundo)][pos[1]].append("P?")
            if "P?" not in direita and "L" not in direita and "V" not in direita and "M" not in direita:
                mundo[pos[0]][(pos[1]+1)%len(mundo)].append("P?")
            if "P?" not in cima and "L" not in cima and "V" not in cima and "M" not in cima:
                mundo[(pos[0]-1)%len(mundo)][pos[1]].append("P?")
            if "P?" not in esquerda and "L" not in esquerda and "V" not in esquerda and "M" not in esquerda:
                mundo[pos[0]][(pos[1]-1)%len(mundo)].append("P?")
        # marca com L quando não estiver em uma casa com B ou F (o caso com M
        # está contemplado acima)
        else:
            if "W?" not in baixo and "P?" not in baixo and "L" not in baixo and "V" not in baixo and "M" not in baixo:
                mundo[(pos[0]+1)%len(mundo)][pos[1]].append("L")
            if "W?" not in direita and "P?" not in direita and "L" not in direita and "V" not in direita and "M" not in direita:
                mundo[pos[0]][(pos[1]+1)%len(mundo)].append("L")
            if "W?" not in cima and "P?" not in cima and "L" not in cima and "V" not in cima and "M" not in cima:
                mundo[(pos[0]-1)%len(mundo)][pos[1]].append("L")
            if "W?" not in esquerda and "P?" not in esquerda and "L" not in esquerda and "V" not in esquerda and "M" not in esquerda:
                mundo[pos[0]][(pos[1]-1)%len(mundo)].append("L")
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
                #print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))  
        # cria a matriz NxN com a representação das casas Livres no mundo
        mundoLivre = []
        for i in range(len(mundo)): 
            linha = []
            for j in range(len(mundo)): 
                if "L" in mundo[i][j] or "L" in mundoCompartilhado[i][j]:
                    linha.append(["L"])
                else:
                    linha.append([])
            mundoLivre.append(linha)
        # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, percepcao2, mundoLivre
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
    
    # procura se tem algum personagem para compartilhar informação, caso tenha
    # é ativado a ação "C"
    print("percepcao2: ",percepcao2)
    for item in range(len(percepcao2)):  
        if percepcao2[item] != "" and percepcao2[item] != "F" and percepcao2[item] != "B" and percepcao2[item] != "I" and percepcao2[item] != "U":
            acao = "C"
            return acao
    # ATENÇÃO: a atualizacao abaixo está errada!!!
    # Não checa se o movimento foi possível ou não... isso só dá para
    # saber quando chegar uma percepção nova (a percepção "I"
    # diz que o movimento anterior não foi possível).
    pos = posicao
    ori = orientacao
    # Anda para frente se a casa da frente está livre
    if "L" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:
        acao = "A"
    # vira para direita, se a casa da direta está livre e vira para
    # esquerda, se a casa da esquerda está livre    
    elif "L" in mundo[(pos[0]+1)%len(mundo)][pos[1]] or "L" in mundo[(pos[0]-1)%len(mundo)][pos[1]] or "L" in mundo[pos[0]][(pos[1]+1)%len(mundo)] or "L" in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
        if ori[0] == 1 and ori[1] == 0:
            if "L" in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
                acao = "D"
            elif "L" in mundo[pos[0]][(pos[1]+1)%len(mundo)]:
                acao = "E"
        if ori[0] == 0 and ori[1] == -1:
            if "L" in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                acao = "D"
            elif "L" in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                acao = "E"
        if ori[0] == -1 and ori[1] == 0:
            if "L" in mundo[pos[0]][(pos[1]+1)%len(mundo)]:
                acao = "D"
            elif "L" in mundo[pos[0]][(pos[1]-1)%len(mundo)]:
                acao = "E"
        if ori[0] == 0 and ori[1] == 1:
            if "L" in mundo[(pos[0]+1)%len(mundo)][pos[1]]:
                acao = "D"
            elif "L" in mundo[(pos[0]-1)%len(mundo)][pos[1]]:
                acao = "E"
    else:
        # volta para uma casa já visitada
        if "V" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:
            acao = "A"
        else:
            acao = "D"
    #acao = input("Digite a ação desejada (A/D/E/T/C): ")
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
