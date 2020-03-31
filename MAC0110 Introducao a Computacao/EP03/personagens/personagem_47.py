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

global salaslivres
"""
Armazena todas as salas livres que ainda não foram visitadas pelo personagem,
de forma que ele possa voltar a elas caso esteja em uma casa onde qualquer passo
é arriscado.
"""
global info
"""
Detecta a presença de outro personagem na sala (na função planejar) e depois é
utilizada na função agir para que o personagem saiba que pode realizar a ação "Compartilhar".
"""
global flecha
"""
Verifica se o personagem atirou uma flecha em sua última ação, para que o personagem,
ao ouvir um urro, saiba que o Wumpus morto é o que está a sua frente.
"""

global Andar
"""
Verifica se o personagem realizou a ação "Andar".
"""

global GirarDireita
"""
Verifica se o personagem realizou a ação "Girar para a direita".
"""


global GirarEsquerda
"""
Verifica se o personagem realizou a ação "Girar para a esquerda".
"""





def encontrasalalivre(m, pos, ori, q):
    """Função que realiza o processo de direcionar o personagem a uma sala livre, caso
    ele se encontre em alguma situação em que qualquer passo é arriscado. Para isso, cria
    uma matriz numerada em que o valor de cada casa corresponde ao númerode passos necessários
    para alcançar a casa desejada (no caso, a sala livre).
    """

    """Cria uma matriz n que recebe a representação do mundo e indica casas livres ("livre")
    e casas possivelmente perigosas ou inacessíveis (-1)."""
    n=[]
    for i in range (len(m)):
        n.append([0]*len(m[0]))
    for i in range (len(m)):
        for j in range (len(m[0])):
            if m[i][j]==["L", "V"]:
                n[i][j]="livre"
            else:
                n[i][j]=-1

    salalivre=[q[0],q[1]]
    n[salalivre[0]][salalivre[1]]=1 #substitui o valor da casa que o personagem deseja visitar de "livre" para 1.
    matriz=True #garante que todas as casas marcadas como "livre" sejam numeradas.

    """Numera as casas de acordo com o número de passos necessários para atingir
    a sala livre."""
    while matriz:
        for i in range (len(m)):
            for j in range (len(m)):
                vizinhos = [[(i+1)%len(m),j],[(i-1)%len(m),j],[i,(j+1)%len(m)],[i,(j-1)%len(m)]]
                if type(n[i][j])==int and n[i][j]!=-1:
                    for k in vizinhos:
                        if n[k[0]][k[1]] == "livre" :
                            n[k[0]][k[1]]=n[i][j]+1

        """Verifica se todas as casas estão numeradas."""
        matriz = False
        for i in range (len(m)):
            for j in range (len(m)):
                if n[i][j]=="livre":
                    matriz=True

    """Define a posição do personagem e direciona seu movimento para uma casa que
    possua um "passo" a menos que a casa atual."""
    posicaoatual = [pos[0], pos[1]]
    if n[(pos[0]+ori[0])%len(m)][(pos[1]+ori[1])%len(m)]==n[pos[0]][pos[1]]-1:
        return "A"
    if n[(pos[0]+ori[1])%len(m)][(pos[1]-ori[0])%len(m)]==n[pos[0]][pos[1]]-1:
        return "D"
    if n[(pos[0]-ori[1])%len(m)][(pos[1]+ori[0])%len(m)]==n[pos[0]][pos[1]]-1:
        return "E"
    if n[(pos[0]-ori[0])%len(m)][(pos[1]-ori[1])%len(m)]==n[pos[0]][pos[1]]-1:
        return "D"
    

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, salaslivres, flecha, Andar, GirarDireita, GirarEsquerda
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
    salaslivres=[] #no início não há salas livres armazenadas...
    flecha = False #... e o personagem não disparou nenhuma flecha.
    Andar=False
    GirarDireita=False
    GirarEsquerda=False
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salaslivres, info, Andar, GirarDireita, GirarEsquerda
    
    pos = posicao
    ori = orientacao
    if Andar:
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
    if GirarEsquerda:
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
    if GirarDireita:
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]

    sl = salaslivres
    info = False
    countwumpus=0 #conta os W? adjacentes a uma casa para saber se há como definir W para uma delas.
    countpoco=0 #conta os P? adjacentes a uma casa para saber se há como definir P para uma delas.
    wumpusadj=False #Verifica se ja há pelo menos um W nas casas adjacentes.
    pocoadj=False #Verifica se ja há pelo menos um P nas casas adjacentes.


    """Detecta qualquer percepção que não seja F, B, U ou I, ou seja, detecta se há outro personagem na sala."""         
    for i in range (len(percepcao)):
        if percepcao[i]!="F" and percepcao[i]!="B" and percepcao[i]!="U" and percepcao[i]!="I":
            info = True

    """Quando o personagem ouvir um urro, se não sentir fedor na sua posição e tiver atirado, substitui a casa a
    sua frente de ["W"] para ["L"]. Caso ainda sinta fedor, ou não tenha disparado uma flecha, então transforma
    todos os W do mundo em W?"""
    if "U" in percepcao:
        if "F" not in percepcao and flecha==True:
            mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ["L"]
        else:
            for i in range (len(mundo)):
                for j in range(len(mundo)):
                    if mundo[i][j] == ["W"]:
                        mundo[i][j] = ["W?"]
    """Volta a posição do personagem caso ele tenha acertado um muro e remove a sala com o muro da lista de
    salas livres."""
    if "I" in percepcao:
        mundo[pos[0]][pos[1]]=["M"]
        if [pos[0],pos[1]] in salaslivres:
            salaslivres.remove([pos[0],pos[1]])
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)

    """Analisa as percepções recebidas marcando as casas adjacentes com W? (se sentir fedor), P? (se sentir
    uma brisa) ou L (caso não sinta nada), sem interferir nas casas que já possuam essas marcações, ou que
    tenham sido marcadas como L, V, M, W ou P."""   
    salasvizinhas = [ [(pos[0]+1)%len(mundo),pos[1]],[(pos[0]-1)%len(mundo),pos[1]],[pos[0],(pos[1]+1)%len(mundo)],[pos[0],(pos[1]-1)%len(mundo)] ]
    for sv in salasvizinhas:
        if "F" in percepcao:
            if mundo[sv[0]][sv[1]]!=["L", "V"] and mundo[sv[0]][sv[1]]!=["M"] and mundo[sv[0]][sv[1]]!=["L"] and mundo[sv[0]][sv[1]]!=["P"] and mundo[sv[0]][sv[1]]!=["W"] and "W?" not in mundo[sv[0]][sv[1]]:
                mundo[sv[0]][sv[1]].append("W?")
        if "B" in percepcao:
            if mundo[sv[0]][sv[1]]!=["L", "V"] and mundo[sv[0]][sv[1]]!=["M"] and mundo[sv[0]][sv[1]]!=["L"] and mundo[sv[0]][sv[1]]!=["P"] and mundo[sv[0]][sv[1]]!=["W"] and "P?" not in mundo[sv[0]][sv[1]]:
                mundo[sv[0]][sv[1]].append("P?")
        if percepcao==[]:
            if mundo[sv[0]][sv[1]]!=["L", "V"] and mundo[sv[0]][sv[1]]!=["M"]:
                if sv not in salaslivres:
                    salaslivres.append(sv)
                mundo[sv[0]][sv[1]]=["L"]

    """Analisa as casas adjacentes para saber se pode inferir com certeza a presença de
    um poço ou de um Wumpus, contando as marcações ao redor. Se houver apenas uma marcação
    P? (no caso de poços) ou W? (no caso de Wumpus), retira a "?". No entanto, se já houver
    P ou W ao redor não realiza nenhuma marcação, pois não é possível inferir nada."""
    for sv in salasvizinhas:
        if "F" in percepcao and "W?" in mundo[sv[0]][sv[1]]:
            countwumpus+=1
        if "B" in percepcao and "P?" in mundo[sv[0]][sv[1]]:
            countpoco+=1
        if "P" in mundo[sv[0]][sv[1]]:
            pocoadj=True
        if "W" in mundo[sv[0]][sv[1]]:
            wumpusadj=True
    for sv in salasvizinhas:
        if countwumpus==1 and wumpusadj==False:
            if "W?" in mundo[sv[0]][sv[1]]:
                mundo[sv[0]][sv[1]]=["W"]
        if countpoco==1 and pocoadj==False:
            if "P?" in mundo[sv[0]][sv[1]]:
                mundo[sv[0]][sv[1]]=["P"]

                
    mundo[pos[0]][pos[1]] = ["L", "V"] #marca a sala atual como livre e visitada.
    if [pos[0],pos[1]] in salaslivres: #retira a sala visitada da lista de salas livres, caso ela esteja nessa lista.
        salaslivres.remove([pos[0],pos[1]])


    for i in range(len(mundo)):
            for j in range(len(mundo[0])):

                """Caso o personagem já tenha definido o que há em uma casa, "ignora" o que lhe for passado."""               
                for k in range (len(mundo[i][j])):                                
                    if "?" not in mundo[i][j][k] and mundo[i][j]!=[]:
                        mundoCompartilhado[i][j] = []

                """Insere uma "?" depois dos valores recebidos por mundoCompartilhado, pois não trata
                as informações recebidas como certamente verdadeiras, poiso personagem que as compartilhou
                pode ter inferido algo errado (com exceção dos muros, pois é necessário colidir com eles
                para saber que estão ali). Em seguida, adiciona essas informações ao mundo (caso seja um
                muro, sobrescreve os valores daquela casa deixando apenas M)."""
                for l in range (len(mundoCompartilhado[i][j])):
                    if mundoCompartilhado[i][j][l]!="M" and "?" not in mundoCompartilhado[i][j][l]:
                        mundoCompartilhado[i][j][l]+="?"
                    if mundoCompartilhado[i][j][l] not in mundo[i][j]:
                        if mundoCompartilhado[i][j][l]=="M":
                            mundo[i][j]==["M"]
                        else:
                            mundo[i][j].append(mundoCompartilhado[i][j][l])
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
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
                if mundo[i][j]==["L", "V"]: #dá um print só de V quando o valor da casa for ["L", "V"]
                    print ("V", end="")
                else:
                    print("".join(mundo[i][j]),end="")
                print ("\t |", end="")
            print("\n"+"-"*(8*len(mundo)+1))


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salaslivres, info, flecha, Andar, GirarDireita, GirarEsquerda
    
    pos = posicao
    ori = orientacao
    sl = salaslivres
    flecha = False
    Andar = False
    GirarDireita = False
    GirarEsquerda = False
    
    if info: #se houver outro personagem na sala, utiliza a ação "Compartilhar".
        return "C"
    if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]==["L"]: #Anda para a sala a frente caso ela esteja livre.
        Andar=True
        return "A"
    if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]==["W"]: #se a casa a frente possuir um Wumpus e ainda houver flechas, realiza a ação "Atirar".
        if nFlechas!=0:
            flecha=True #Armazena que a flecha foi disparada.
            return "T"
    if mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]-ori[0])%len(mundo)]==["L"]: #Se a casa a direita estiver livre, vira à direita.
        GirarDireita=True
        return "D"
    if mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]+ori[0])%len(mundo)]==["L"]: #Se a casa à esquerda estiver livre, vira à esquerda.
        GirarEsquerda=True
        return "E"
    if salaslivres!=[]: #Se houver salas livres não visitadas, utiliza a função encontrasalalivre para alcançá-las.
        acao = encontrasalalivre(mundo, pos, ori, salaslivres[0])
        if acao=="A":
            Andar=True
        if acao=="E":
            GirarEsquerda=True
        if acao=="D":
            GirarDireita=True
        return acao

    """Se não houver salas livres não visitadas, procura por salas possivelmente livres (L?). Do contrário,
    anda pelas casas já visitadas para ver se há alguma sala possivelmente livre, ou para possivelmente encontrar
    algum personagem com quem compartilhar informações para descobrir novas informações."""
    if salaslivres==[]: 
        if "L?" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:
            Andar=True
            return "A"
        if "L?" in mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]-ori[0])%len(mundo)]:
            GirarDireita=True
            return "D"
        if "L?" in mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]+ori[0])%len(mundo)]:
            GirarEsquerda=True
            return "E"
        if mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]==["L","V"]:
            Andar=True
            return "A"
        if mundo[(pos[0]+ori[1])%len(mundo)][(pos[1]-ori[0])%len(mundo)]==["L","V"]:
            GirarDireita=True
            return "D"
        if mundo[(pos[0]-ori[1])%len(mundo)][(pos[1]+ori[0])%len(mundo)]==["L","V"]:
            GirarEsquerda=True
            return "E"
        if mundo[(pos[0]-ori[0])%len(mundo)][(pos[1]-ori[1])%len(mundo)]==["L","V"]:
            GirarDireita=True
            return "D"
