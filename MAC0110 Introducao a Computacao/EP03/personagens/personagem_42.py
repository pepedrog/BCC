# flag para depuração
__DEBUG__ = True


#variável global da percepcao
sensacao=[]

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


# Outras variáveis globais do módulo personagem10297647

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
    global N, mundo, posicao, orientacao
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo=[]
    for i in range(N) :
        linha = []
        for j in range(N) :
            linha.append("") # começa com strings vazias
        mundo.append(linha)
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado

    sensacao=percepcao
    casasLivres=[]
    pos = posicao
    ori = orientacao
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        if "I" in percepcao:
            mundo[pos[0]][pos[1]] = "M"
            pos[0] = (pos[0]-ori[0])%len(mundo)
            pos[1] = (pos[1]-ori[1])%len(mundo)


        mundo[pos[0]][pos[1]] = "V"
        if len(percepcao)==0 or percepcao==["Dummy"]:
                if mundo[(pos[0]+1)%N][pos[1]]!="M"and mundo[(pos[0]+1)%N][pos[1]]!="V":
                        mundo[(pos[0]+1)%N][pos[1]]="L"
                if mundo[(pos[0]-1)%N][pos[1]]!="M"and mundo[(pos[0]-1)%N][pos[1]]!="V":
                        mundo[(pos[0]-1)%N][pos[1]]="L"
                if mundo[pos[0]][(pos[1]+1)%N]!="M"and mundo[pos[0]][(pos[1]+1)%N]!="V":
                        mundo[pos[0]][(pos[1]+1)%N]="L"
                if mundo[pos[0]][(pos[1]-1)%N]!="M"and mundo[pos[0]][(pos[1]-1)%N]!="V":
                        mundo[pos[0]][(pos[1]-1)%N]="L"
        
                        
        if "B" in percepcao and "F" in percepcao:
            if mundo[(pos[0]+1)%N][pos[1]]=="":
                mundo[(pos[0]+1)%N][pos[1]]="WP?"
            if mundo[(pos[0]-1)%N][pos[1]]=="":
                mundo[(pos[0]-1)%N][pos[1]]="WP?"
            if mundo[pos[0]][(pos[1]+1)%N]=="":
                mundo[pos[0]][(pos[1]+1)%N]="WP?"
            if mundo[pos[0]][(pos[1]-1)%N]=="":
                mundo[pos[0]][(pos[1]-1)%N]="WP?"
            
        elif "B" in percepcao:
            if mundo[(pos[0]+1)%N][pos[1]]==""or mundo[(pos[0]+1)%N][pos[1]]=="WP?":
                mundo[(pos[0]+1)%N][pos[1]]="P?"
            if mundo[(pos[0]-1)%N][pos[1]]==""or mundo[(pos[0]-1)%N][pos[1]]=="WP?":
                mundo[(pos[0]-1)%N][pos[1]]="P?"
            if mundo[pos[0]][(pos[1]+1)%N]==""or mundo[pos[0]][(pos[1]+1)%N]=="WP?":
                mundo[pos[0]][(pos[1]+1)%N]="P?"
            if mundo[pos[0]][(pos[1]-1)%N]==""or mundo[pos[0]][(pos[1]-1)%N]=="WP?":
                mundo[pos[0]][(pos[1]-1)%N]="P?"

            if mundo[(pos[0]+1)%N][pos[1]]=="W?":mundo[(pos[0]+1)%N][pos[1]]="L"
            if mundo[(pos[0]-1)%N][pos[1]]=="W?":mundo[(pos[0]-1)%N][pos[1]]="L"
            if mundo[pos[0]][(pos[1]+1)%N]=="W?":mundo[pos[0]][(pos[1]+1)%N]="L"
            if mundo[pos[0]][(pos[1]-1)%N]=="W?":mundo[pos[0]][(pos[1]-1)%N]="L"
            
                
        elif "F" in percepcao:
            if mundo[(pos[0]+1)%N][pos[1]]==""or mundo[(pos[0]+1)%N][pos[1]]=="WP?":
                mundo[(pos[0]+1)%N][pos[1]]="W?"
            if mundo[(pos[0]-1)%N][pos[1]]==""or mundo[(pos[0]-1)%N][pos[1]]=="WP?":
                mundo[(pos[0]-1)%N][pos[1]]="W?"
            if mundo[pos[0]][(pos[1]+1)%N]==""or mundo[pos[0]][(pos[1]+1)%N]=="WP?":
                mundo[pos[0]][(pos[1]+1)%N]="W?"
            if mundo[pos[0]][(pos[1]-1)%N]==""or mundo[pos[0]][(pos[1]-1)%N]=="WP?":
                mundo[pos[0]][(pos[1]-1)%N]="W?"

            if mundo[(pos[0]+1)%N][pos[1]]=="P?":mundo[(pos[0]+1)%N][pos[1]]="L"
            if mundo[(pos[0]-1)%N][pos[1]]=="P?":mundo[(pos[0]-1)%N][pos[1]]="L"
            if mundo[pos[0]][(pos[1]+1)%N]=="P?":mundo[pos[0]][(pos[1]+1)%N]="L"
            if mundo[pos[0]][(pos[1]-1)%N]=="P?":mundo[pos[0]][(pos[1]-1)%N]="L"

        if "U" in percepcao:
            mundo[[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]]="L"

        # mostra na tela (para o usuário) o mundo conhecido pela personagem
        # e o mundo compartilhado (quando disponível)
        print("Mundo conhecido pela personagem:")
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
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="MM":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="VL":mundoCompartilhado[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="LL":mundoCompartilhado[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="LM":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="P?L":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="P?P":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="P?M":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="W?L":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="W?W":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="W?M":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="WP?W":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="WP?P":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="WP?L":mundo[i][j]=""
                if mundo[i][j]+"".join(mundoCompartilhado[i][j])=="WP?M":mundo[i][j]=""

                if mundo[i][j]=="L" or "".join(mundoCompartilhado[i][j])=="L":
                    casasLivres.append(str(i)+str(j) )
                
                print(mundo[i][j]+"".join(mundoCompartilhado[i][j]),end="\t |")
            print("\n"+"-"*(8*len(mundo)+1))
            

def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado,sensacao

    

    pos = posicao
    ori = orientacao
    if pos[0]==0 and pos[1]==0:
        acao="A"
    if pos[0]==1 and pos[1]==0 and ori==[1,0]:
        acao="D"
    if pos[0]==1 and pos[1]==0 and ori==[0,-1]:
        acao="A"
    if pos[0]==1 and pos[1]==N-1 and ori==[0,-1]:
        acao="E"
    if pos[0]==1 and pos[1]==N-1 and ori==[1,0]:
        acao="A"
    if pos[0]==2 and pos[1]==N-1 and ori==[1,0]:
        acao="T"
    
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


    return acao
