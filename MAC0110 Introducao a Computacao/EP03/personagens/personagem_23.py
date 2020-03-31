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

global numero_colisoes_com_muro
numero_colisoes_com_muro = 0


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
def percorre_mapa(mundo) : 
    """
        Função que percorre todo o mundo e atualiza as salas não visitadas quando o jogador
        recebe informação de outro jogador
    """
    nao_visitados = []
    for i in range(N) : 
        for j in range(N) : 
            if 'L' in mundo[i][j] : 
                nao_visitados.append([i, j])

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, visitados, nao_visitados, bifurcacao, proxima, backtracking, contador_giro_backtracking, confiança
    # guarda o tamanho do mundo
    confiança = False
    proxima = [[],[]]
    N = tamanho
    visitados = []
    nao_visitados = []
    bifurcacao = []
    acao = 'Inicializa'

    backtracking = False
    contador_giro_backtracking = 0

    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N):
        linha = []
        for j in range(N) : 
            linha.append([])
        mundo.append(linha) 
        # começa com listas vazias
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]


def varredura(string_alvo, mundo, pos, nao_visitados, percepcao, modo) :
    """
        Função que recebe uma str e a insere nos arredores do personagem em mundo
        Ademais, se a posição a ser varrida estiver marcada como "L" ou "V", não
        preenche. A função tambem anota no mundo quais casas não foram visitadas ao redor
        O modo determina como a função se comporta : se vai escrever algo nas anotações, ler, ou
        contar a frequencia.
    """
    contador = 0
    i = -1
    while i <= 1 : 
        j = -1
        while j <= 1 :
            coordenada_i = (pos[0] + i)%N
            coordenada_j = (pos[1] + j)%N
            posicao_verificada = mundo[coordenada_i][coordenada_j]
            if abs(i) != abs(j) : 
                if posicao_verificada == string_alvo : 
                    contador += 1
                if modo == "Leitura" : 
                    if posicao_verificada == string_alvo : 
                        return coordenada_i, coordenada_j
                if modo == "Escrita" : 
                    if posicao_verificada == [] or ('W?' in percepcao and 'P?' in percepcao) : 
                        posicao_verificada.append(string_alvo)
                    if posicao_verificada == ['L'] and [coordenada_i,coordenada_j] not in nao_visitados :
                        nao_visitados.append( [  coordenada_i,  coordenada_j   ]   )
            j += 1
        i += 1    
    if modo == "Contador" : 
        return contador





def find_only(string_alvo, mundo, pos) : 
    """
        Função que recebe uma string alvo e verifica se ela ocorre apenas uma vez ao redor. Se ocorrer apenas uma vez,
        a função marca aquela posição como string_alvo (por exemplo, a função percebe que, se w? ocorre apenas uma vez)
        ao redor, então essa duvida é o wumpus).
    """
    if confiança == False : #so tenta advinhar se nao tiver ajuda
        contador_unico = 0
        alvo = string_alvo + '?'
        i = -1
        while i <= 1 : 
            j = -1
            while j <= 1 :
                if abs(i) != abs(j) : 
                    if mundo[(pos[0] + i)%N][(pos[1] + j)%N] == [alvo] :
                        contador_unico += 1
                        if contador_unico == 1 :
                            referencia_linha = i
                            referencia_coluna = j
                    else :
                        if '?' in mundo[(pos[0] + i)%N][(pos[1] + j)%N] : #Cobre o caso que, se string_alvo = W, tenho adjacente um P?. O contario vale
                            return
                j += 1
            i += 1
        if contador_unico == 1 : 
            mundo[(pos[0] + referencia_linha)%N][(pos[1] + referencia_coluna)%N] = string_alvo

             
                





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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, numero_colisoes_com_muro, copia_percepcao, backtracking, contador_giro_backtracking, confiança
    copia_percepcao = percepcao[:]
    pos = posicao
    ori = orientacao

    percorre_mapa(mundo)
    

    if [ pos[0], pos[1]] in nao_visitados : 
        nao_visitados.remove([ pos[0], pos[1]])

    if  len(percepcao) == 0 or (len(percepcao) == 1 and 'Dummy' in percepcao) : 
        varredura('L', mundo, pos, nao_visitados, percepcao, 'Escrita')


    if "I" in percepcao:
        numero_colisoes_com_muro += 1
        if numero_colisoes_com_muro == 1 : 
            mundo[pos[0]][pos[1]] = 'M'
            pos[0] = (pos[0]-ori[0])%len(mundo)
            pos[1] = (pos[1]-ori[1])%len(mundo)
    else :
        numero_colisoes_com_muro = 0
        

    if "F" in percepcao : 
        varredura('W?', mundo,pos, nao_visitados, percepcao, 'Escrita')
        find_only('W', mundo, pos)

    
    if "B" in percepcao :
        varredura('P?', mundo, pos, nao_visitados, percepcao, 'Escrita')
        find_only('P', mundo, pos)
    
    visitado = pos[:]
    if visitado not in visitados : 
        mundo[pos[0]][pos[1]] = ['V'] 
        visitados.append(visitado)


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
            print("",end="\t| ") 
        print("\n"+"-"*(8*len(mundo)+1))

    for i in range(N) : 
        for j in range(N) : 
            if len(mundoCompartilhado[i][j]) > 0 and mundo[i][j] != 'M' and mundo[i][j] != ['V']: 
                mundo[i][j] = mundoCompartilhado[i][j]

    # confiança = False



def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, numero_colisoes_com_muro, backtracking, contador_giro_backtracking
    pos = posicao
    clone_pos = pos[:] #evita erro de referencia
    ori = orientacao
    proxima[0] = (pos[0]+ori[0])%len(mundo)
    proxima[1] = (pos[1]+ori[1])%len(mundo)
    if backtracking == False : 
        cont = varredura (['L'], mundo, pos, nao_visitados, copia_percepcao, 'Contador')
        if cont <=1 and clone_pos in bifurcacao : 
            bifurcacao.pop()
        if cont >= 1 :
            
            if clone_pos not in bifurcacao :
                bifurcacao.append(clone_pos)
            pos_verificada = varredura (['L'], mundo, pos, nao_visitados, copia_percepcao, 'Leitura')
            if mundo[ proxima[0] ][ proxima[1] ] == ['L'] : 
                acao = "A"
            else : 
                acao = "D"
        else :  #caso no qual tenho nenhuma casa livre ao redor. Ou seja, cheguei num beco sem saida
            if len(nao_visitados) == 0 : #aqui,  o personagem arrisca
                acao = "A"
            else :
                backtracking = True
  
        tamanho_percepcao = len(copia_percepcao)
        for i in range(tamanho_percepcao) : 
            if len(copia_percepcao[i]) > 1 : #com certeza é um personagem
                acao = "C"
                confiança = True
                pass
    if backtracking == True :
        if proxima not in bifurcacao : #faz o personagem girar duas vezes. Como temos uma busca semelhante a DFS, isso o obriga a refazer seu caminho
            acao = 'D'
            contador_giro_backtracking += 1
        else : 
            acao = 'A'
            contador_giro_backtracking = 0
        if clone_pos in bifurcacao : 
            backtracking = False #pare de voltar, voce atingiu uma bifurcacao!
        

    if ('F' in copia_percepcao and len(nao_visitados) == 0 or 'W' in mundo[ proxima[0] ][ proxima[1] ]) and nFlechas > 0 : 
        acao = 'T'


            
    if acao=="A" and numero_colisoes_com_muro == 0:
        
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
