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

global percep
"""
Salva a percepcao do personagem para uso em funcoes que nao recebem esse valor do mundo
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, percep
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.
    
    # Guarda a informação recebida pela percepção para o uso na próxima função
    percep = "ERROR"
    percep = percepcao
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)       
        pos = posicao
        ori = orientacao
        # poupando espaço e tempo 
        y = pos[0]
        x = pos[1]
        # verifica se o movimento foi possível e marca V. Caso contrário, volta para a casa de origem e marca M
        if "I" not in percepcao:
            mundo[y][x] = ["V"]
        else:
            pos[0] = (pos[0]-ori[0])%len(mundo)
            pos[1] = (pos[1]-ori[1])%len(mundo)
            mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ["M"]
        # O if funciona para estabelecer uma identação, uma vez que o programa não estava rodando sem uma. Pode ter sido um bug.
        # define as casas ao arredor da casa atual baseado na percepcao.
        if mundo[y][x] == mundo[y][x]:
            if "B" in percepcao:
                if mundo[((y+1)%len(mundo))][x] == []:
                    mundo[((y+1)%len(mundo))][x] += ["P?"]
                if mundo[((y-1)%len(mundo))][x] == []:
                    mundo[((y-1)%len(mundo))][x] += ["P?"]
                if mundo[y][((x+1)%len(mundo))] == []:
                    mundo[y][((x+1)%len(mundo))] += ["P?"]
                if mundo[y][((x-1)%len(mundo))] == []:
                    mundo[y][((x-1)%len(mundo))] += ["P?"]                                        
            if "F" in percepcao:
                if mundo[((y+1)%len(mundo))][x] == []:
                    mundo[((y+1)%len(mundo))][x] += ["W?"]
                if mundo[((y-1)%len(mundo))][x] == []:
                    mundo[((y-1)%len(mundo))][x] += ["W?"]
                if mundo[y][((x+1)%len(mundo))] == []:
                    mundo[y][((x+1)%len(mundo))] += ["W?"]
                if mundo[y][((x-1)%len(mundo))] == []:
                    mundo[y][((x-1)%len(mundo))] += ["W?"]
            elif "I" not in percepcao and "B" not in percepcao and "F" not in percepcao:
                if "V" not in mundo[((y+1)%len(mundo))][x] and "M" not in mundo[((y+1)%len(mundo))][x]:
                    mundo[((y+1)%len(mundo))][x] = ["L"]
                if "V" not in mundo[((y-1)%len(mundo))][x] and "M" not in mundo[((y-1)%len(mundo))][x]:
                    mundo[((y-1)%len(mundo))][x] = ["L"]
                if "V" not in mundo[y][((x+1)%len(mundo))] and "M" not in mundo[y][((x+1)%len(mundo))]:
                    mundo[y][((x+1)%len(mundo))] = ["L"]
                if "V" not in mundo[y][((x-1)%len(mundo))] and "M" not in mundo[y][((x-1)%len(mundo))]:
                    mundo[y][((x-1)%len(mundo))] = ["L"]
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
                #retira a repetição de letras, inclusive quando uma informação é recebida
                if "V" in mundo[i][j]:
                    mundo[i][j] = ["V"]
                elif "M" in mundo[i][j] or "M" in mundoCompartilhado[i][j]: 
                    mundo[i][j] = ["M"]
                elif "L" in mundoCompartilhado[i][j]:
                    mundo[i][j] = ["L"]
                elif "P" in mundoCompartilhado[i][j]:
                    mundo[i][j] = ["P"]
                elif "W" in mundoCompartilhado[i][j]:
                    mundo[i][j] = ["W"]
                elif "P?" in mundoCompartilhado[i][j]:
                    if "V" not in mundo[i][j]:
                        mundo[i][j] = ["P?"]
                elif "W?" in mundoCompartilhado[i][j]:
                    if "V" not in mundo[i][j]:
                        mundo[i][j] = ["W?"]
                print("",end="")
                print(" (".join(mundo[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    return percep


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, percep
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
    # Variáveis para economizar espaço e deixar o código mais limpo 
    y = pos[0]   
    x = pos[1]
    baixo = (y+1)%len(mundo)
    cima = (y-1)%len(mundo)
    esq = (x-1)%len(mundo)
    dire = (x+1)%len(mundo)
    # esse trecho é o "raciocínio" do personagem.
    if pos == posicao:
    ##### trecho comentado abaixo é apenas válido em mundos com o personagem "Dummy". Seja esse o caso, sempre é alcançada a vitória
    #   if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["W"]:
    #       acao = "T"
    #    elif ("W" in mundo[baixo][x] or "W" in mundo[cima][x] or "W" in mundo[y][esq] or "W" in mundo[y][dire]) and  mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] != ["W"]:
    #       acao =  "D"
        if "Dummy" in percep:
            acao = "C"            
        elif "I" in percep:
            acao = "E"
        elif mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["L"] or mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == []:
            acao = "A"
        elif ("L" in mundo[baixo][x] or "L" in mundo[cima][x] or "L" in mundo[y][esq] or "L" in mundo[y][dire]) and  mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] != ["L"]:
            acao =  "D"
        elif "L" not in mundo[baixo][x] and "L" not in mundo[cima][x] and "L" not in mundo[y][esq] and "L" not in mundo[y][dire]:
            if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["V"]:
                acao = "A"
            else:
                acao = "D"
        elif mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] == ["P?"]:
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
