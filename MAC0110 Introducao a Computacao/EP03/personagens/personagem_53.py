# coding=utf-8
# flag para depuração
__DEBUG__ = True


# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

"""
    Número de flechas que a personagem possui. Serve apenas para
    consulta da personagem, pois o mundo mantém uma cópia "segura" dessa
    informação (não tente inventar flechas...).
"""
global nFlechas


"""
    Esse é um espaço onde a personagem tem acesso à representação do
    mundo de uma outra personagem.  Essa informação pode ser usada como a
    personagem quiser (por exemplo, transferindo o conteúdo para o seu
    próprio "mundo", ou mantendo uma lista dos vários mundos
    compartilhados com outras personagens).
"""
global mundoCompartilhado


# Outras variáveis globais do módulo personagem8910368

"""
    Dimensão do mundo.
"""
global N


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
global mundo


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
global posicao


"""
    Juntamente com a posição relativa, permite à personagem manter o
    histórico das salas visitadas. Essa orientação é independente da
    orientação "real" que o mundo usa para coordenar a ação de todas as
    personagens. Por convenção, todas as personagens indicam sua orientação
    inicial como "para baixo" ou "sul", correspondente à direção [1,0]
    (direção do eixo vertical).
"""
global orientacao


"""
    Lista contendo as percepções que a personagem recebe acerca
    do mundo em uma dada posição do tabuleiro
"""
global percepcoes


"""
    Armazena as salas ainda não visitadas pela personagem no mundo.
    Ela armazena as salas ainda vazias 
"""
global salasVazias


"""
    Uma flag que indica se a personagem atual acabou de compartilhar
    informações com alguma outra
"""
global recemCompartilhado


"""
    Função de inicialização da personagem (recebe o tamanho do mundo).
    Usa as variáveis globais (do módulo) para representar seu
    conhecimento do mundo, sua posição e sua orientação relativas
    ao início da simulação. Você pode criar e inicializar outras
    variáveis aqui (por exemplo, a lista de salas livres e não
    visitadas).
"""
def inicializa(tamanho):
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, salasVazias
    
    # guarda o tamanho do mundo
    N = tamanho

    # inicializa a flag de compartilhamento
    recemCompartilhado = False

    # inicialmente não há marcação de salas vazias
    salasVazias = []
    
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N):
        linha = []
        for j in range(N):
            linha.append([]) # começa com listas vazias
        mundo.append(linha)
    
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]


"""
    Descrição:
        Função que verifica se algum dos itens de lista1 está contido
        em lista2

    Parâmetros:
        lista1: uma lista de elementos a serem buscados
        lista2: uma lista em que os elementos de lista1 serão buscados

    Retorno:
        Um boolean que indica se algum item de lista1 está em lista2
"""
def lista_ja_contem(lista1, lista2):
    return any(elem in lista1 for elem in lista2)

"""
    Descrição:
        Atualiza o mundo conhecido pela personagem com as informações disponíveis nos
        marcadores passados.

    Parâmetros:
        marcadores: uma lista de string contendo os marcadores a serem atualizados no mundo
        mundo: uma lista de listas representando o mundo conhecido pela personagem.
        linha: um inteiro que indica a linha atual do personagem no mundo
        coluna: um inteiro que indica a coluna atual do personagem no mundo

    Retorno:
        Não há.
"""
def marcarVizinhos(marcadores, mundo, linha, coluna):
    vizinhos = [ [(linha - 1) % N, coluna],
                 [(linha + 1) % N, coluna],
                 [linha, (coluna - 1) % N],
                 [linha, (coluna + 1) % N] ]

    for v in range(len(vizinhos)):
        i = vizinhos[v][0]
        j = vizinhos[v][1]

        for k in range(len(marcadores)):

            # Verifica se a sala está vazia. Se estiver, só adiciona o marcador
            if mundo[i][j]:
                
                # Checa se esse marcador já está na sala, ou se a sala já possui
                # P/W caso tente inserir P?/W?. Também, somente deixa inserir se
                # não for sala já visitada, com muro ou livre
                possiveis_itens = ['V', 'L', 'M', marcadores[k], marcadores[k][:-1]]
                
                if not(lista_ja_contem(possiveis_itens, mundo[i][j])):
                    mundo.append(marcadores[k])
            else:
                mundo[i][j].append(marcadores[k])


"""
    Descrição:
        Atualiza os marcadores em uma dada posição no mundo. Diferencia-se da função
        marcarVizinhos pois atualiza apenas uma posição

    Parâmetros:
        marcadores: uma lista de string contendo os marcadores a serem atualizados no mundo
        mundo: uma lista de listas representando o mundo conhecido pela personagem
        linha: um inteiro que indica a linha atual do personagem no mundo
        coluna: um inteiro que indica a coluna atual do personagem no mundo

    Retorno:
        Não há.
"""
def marcarAtual(marcadores, mundo, linha, coluna):
    for k in range(len(marcadores)):
        if marcadores[k] not in mundo[linha][coluna]:
            mundo[linha][coluna].append(marcadores[k])


"""
    Descrição:
        Função que cruza os dados do mundo que a personagem coletou com dados
        compartilhados por outras personagens, de modo a tentar inferir algo
        que ajude a sobreviver ou a matar o Wumpus. Note que limpamos a matriz
        de mundo compartilhado após usá-la, de modo a evitar que dados desatualizados
        sejam incorporados à matriz do mundo

    Parâmetros:
        mundo: uma lista de listas contendo o mundo conhecido pela personagem
        mundoCompartilhado: uma lista de listas contendo dados do mundo coletados
                            por outra personagem

    Retorno:
        Não há.
"""
def cruzarDadosCompartilhados(mundo, mundoCompartilhado):
    for i in range(N):
        for j in range(N):
            # Somente acrescenta marcadores se já não tivermos ido à sala
            # ou se não soubermos que ela está livre. Nesse caso, simplesmente
            # adiciona o que à outra personagem sabe ao nosso mundo, se a lista
            # de conhecimentos dela não for fazia
            if (mundoCompartilhado[i][j]) and ('L' not in mundo[i][j]) and ('V' not in mundo[i][j]):
                mundo[i][j] = mundoCompartilhado[i][j]
                mundoCompartilhado[i][j] = []
          

"""
    Descrição:
        Função que busca por novas salas não visitadas e as coloca em uma lista
        que age como uma pilha, da qual só é possível retirar itens do início,
        nunca do fim

    Parâmetros:
        mundo: uma lista de listas representando o mundo conhecido pela personagem
        posicao: uma lista com dois inteiros indicando a sala-destino da
                 personagem no formato (linha, coluna)
        salasVazias: uma lista contendo as salas vazias ainda não visitadas

    Retorno:
        Não há.
"""
def atualizarSalasVazias(mundo, posicao, salasVazias):
    linha = posicao[0]
    coluna = posicao[1]

    vizinhos = [ [(linha - 1) % N, coluna],
                 [(linha + 1) % N, coluna],
                 [linha, (coluna - 1) % N],
                 [linha, (coluna + 1) % N] ]

    for v in vizinhos:
        sala = mundo[v[0]][v[1]]

        # Se for uma sala vazia, ainda não-visitada e que não tem um
        # muro, então ela deve ser incluída na lista
        if ('L' in sala) and (v not in salasVazias) and not(lista_ja_contem(['M', 'V'], sala)):
            salasVazias.insert(0, v)


"""
    Descrição:
        Planeja as atitudes da personagem, atualizando incluindo na sua
        representação do mundo as percepções que lhe são enviadas

    Parâmetros:
        percepcao: lista de strings com as percepções sentidas pela personagem

    Retorno:
        Não há.
"""
def planejar(percepcao):

    # Declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, percepcoes
    global salasVazias, nFlechas, mundoCompartilhado
    
    # Cria uma lista de marcações para colocar nas posições
    # vizinhas, baseando-se nas percepções obtidas na posição
    # atual; e uma para a posição atual
    marcadoresVizinhos = []
    marcadoresAtuais = []

    # Se não tem percepção, então os vizinhos estão livres
    if not percepcao:
        marcadoresVizinhos.append('L')
    else:
        if 'F' in percepcao:
            marcadoresAtuais.append('F')
            marcadoresVizinhos.append('W?')
        
        if 'B' in percepcao:
            marcadoresAtuais.append('B')
            marcadoresVizinhos.append('P?')      
        
        # Bateu em um muro, então não houve alteração na posição
        # da personagem no mundo, ie, ela ainda está no mesmo lugar.
        # Marca o muro apenas na casa à frente da personagem.  
        if 'I' in percepcao:

            # Note que a atualização de marcadores é feita aqui dentro
            # pois resetamos a posição da personagem, assim que um muro
            # é detectado
            marcarAtual(['M', 'V'], mundo, posicao[0], posicao[1])

            # Retorna a posição em uma casa, indicando que não houve
            # movimento
            posicao[0] += orientacao[0] * -1
            posicao[1] += orientacao[1] * -1
        
    # Ao fim marca como V todas as salas em que houve tentativa
    # de movimento, não importa se com sucesso ou não
    if 'V' not in mundo[posicao[0]][posicao[1]]:
        marcadoresAtuais.append('V')

    # Atualiza os marcadores na posição atual e nas posições adjacentes
    marcarVizinhos(marcadoresVizinhos, mundo, posicao[0], posicao[1])
    marcarAtual(marcadoresAtuais, mundo, posicao[0], posicao[1])

    # Tenta cruzar o conhecimento atual do mundo com eventuais dados
    # compartilhados por outros personagens
    cruzarDadosCompartilhados(mundo, mundoCompartilhado)

    # Após marcar as novas salas
    atualizarSalasVazias(mundo, posicao, salasVazias)

    # Torna percepção global, de modo que se consiga ter acesso a
    # ela na função agir()
    percepcoes = percepcao

    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)

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
                    print("* ",end="")
                    if ori==[0,1]:
                        print(">",end="")
                    if ori==[1,0]:
                        print("v",end="")
                    if ori==[-1,0]:
                        print("^",end="")
                print(",".join(mundo[i][j]),end="")
                print("",end="\t\t| ")
                # print(",".join(mundoCompartilhado[i][j]),end="\t\t| ")
            print("\n"+"-"*(16*len(mundo)+1))
    

"""
    Descrição:
        Função que determina qual deve ser a ação tomada pelo personagem
        para que com suas posição e orientação atuais ele chegue ao seu
        destino. Observe que essa função parte do pressuposto que só é
        possível ir a alguma das casas vizinhas na horizontal e diagonal

    Parâmetros:
        origem: uma lista com dois inteiros indicando a posicao atual da
                personagem no formato (linha, coluna)
        destino: uma lista com dois inteiros indicando a sala-destino da
                personagem no formato (linha, coluna)
        orientacao: uma lista com dois inteiros indicando a orientacao
                atual da personagem no formato (orient_horiz, orient_vert)

    Retorno:
        Uma string contendo o caracter que indica a ação a ser tomada,
        podendo ser A, T, D, E
"""
def determinarAcao(origem, destino, orientacao):
    lin_inicio = origem[0]
    col_inicio = origem[1]

    lin_destino = destino[0]
    col_destino = destino[1]

    next_lin = origem[0] + orientacao[0]
    next_col = origem[1] + orientacao[1]

    # Destino está no mesmo nível (à frente ou atrás)
    if next_lin == lin_destino:
        if next_col == col_destino:
            return 'A'
        else:
            return 'D'

    # Destino está abaixo da linha para a qual nos encaminhamos
    elif next_lin < lin_destino:

        # Está se movimentando na vertical, se não mudar de coluna
        if next_col == col_destino:
            return 'A'

        elif next_col > col_destino:
            return 'D' if (next_lin - lin_inicio == 0) else 'E'
        else:
            return 'E' if (next_lin - lin_inicio == 0) else 'D'

    # Destino está acima da linha para a qual nos encaminhamos
    else: 

        # Está se movimentando na vertical, se não mudar de coluna
        if next_col == col_destino:
            return 'A'

        elif (next_col > col_destino):
            return 'E' if (next_lin - lin_inicio == 0) else 'D'
        else:
            return 'D' if (next_lin - lin_inicio == 0) else 'E'


"""
    Descrição:
        Função que verifica se há um Wumpus na vizinhança. Se localizar
        algum, determina a ação que deve ser tomada

    Parâmetros:
        mundo:      uma lista de listas representando o mundo conhecido pela personagem
        posicao:    uma lista com dois inteiros indicando a sala-destino da
                    personagem no formato (linha, coluna)
        orientacao: uma lista com dois inteiros indicando a orientacao
                    atual da personagem no formato (orient_horiz, orient_vert)

    Retorno:
        Uma string que indica qual atitude deve ser tomada para
        se aproximar do Wumpus, podendo ser T, D ou E, caso haja
        um Wumpus por perto, ou -1, se não houver Wumpus na vizinhança
"""
def wumpusProximo(mundo, posicao, orientacao):
    linha = posicao[0]
    coluna = posicao[1]

    vizinhos = [ [(linha - 1) % N, coluna],  # acima
                 [(linha + 1) % N, coluna],  # embaixo
                 [linha, (coluna - 1) % N],  # à esquerda
                 [linha, (coluna + 1) % N] ] # à direita
    
    for v in vizinhos:
        if mundo[v[0]][v[1]] == 'W':
            # Se a direcao do movimento é para frente, detém-no
            # por segurança e envia o comando para atirar
            acao = determinarAcao(posicao, v, orientacao)
            return 'T' if acao == 'A' else acao
    
    return '-1'


"""
    Descrição:
        Verifica se há outra personagem na mesma sala que a personagem atual,
        olhando se nas percepções da personagem há algo diferente de F, B, I e U

    Parâmetros:
        percepcoes: lista de strings com as percepções sentidas pela personagem

    Retorno:
        True, caso haja outra personagem na sala em questão, ou False, caso
        não haja personagem 
"""
def sentiuNovaPersonagem(percepcoes):
    for i in range(len(percepcoes)):
        if percepcoes[i] not in ['F', 'B', 'I', 'U']:
            return True
    return False


"""
    Descrição:
        Função que decide qual deve ser o próximo movimento. Note
        que ele só retira da a sala-destino da pilha de salas livres
        quando de fato estiver diante dela

    Parâmetros:
        salasVazias: uma lista de posicoes (linha, coluna) que indica
                     quais salas ainda não foram visitadas
        posicao:    uma lista com dois inteiros indicando a sala-destino da
                    personagem no formato (linha, coluna)
        orientacao: uma lista com dois inteiros indicando a orientacao
                    atual da personagem no formato (orient_horiz, orient_vert)

    Retorno:
        Uma string contendo uma ação, podendo ser E, D ou A
"""
def decidirProximoMovimento(salasVazias, posicao, orientacao):
    proximaSalaLivre = salasVazias[0]

    # Somente muda a ação caso esteja de fato se movendo
    acao = determinarAcao(posicao, proximaSalaLivre, orientacao)
    if acao == 'A':
        salasVazias.pop(0)

    return acao


"""
    Descrição:
        Função que atualiza os parâmetros posição e orientação com
        base na ação a ser tratada

    Parâmetros:
        acao: uma string contendo uma ação, podendo ser E, D, A

    Retorno:
        Não há
"""
def atualizarPosicao(acao):

    global posicao, orientacao, N

    if acao == "A":
        posicao[0] = (posicao[0] + orientacao[0]) % N
        posicao[1] = (posicao[1] + orientacao[1]) % N
    if acao == "E":
        if orientacao[0] == 0:
            orientacao[1] = -orientacao[1]
        orientacao[0], orientacao[1] = orientacao[1], orientacao[0]
    if acao == "D":
        if orientacao[1] == 0:
            orientacao[0] = -orientacao[0]
        orientacao[0], orientacao[1] = orientacao[1], orientacao[0]


"""
    Nessa função a personagem deve usar seu conhecimento
    do mundo para decidir e tentar executar (devolver) uma ação.
    Possíveis ações (valores de retorno da função) são
    "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
    "T"=aTirar e "C"=Compartilhar.
"""
def agir():

    # declara as variáveis globais que serão acessadas
    global mundo, posicao, percepcoes, orientacao
    global salasVazias, nFlechas, mundoCompartilhado
    global recemCompartilhado

    # Se existe um Wumpus à frente, deve simplesmente atirar
    acao = wumpusProximo(mundo, posicao, orientacao)
    if acao != '-1':
        return acao

    # Se achou uma nova personagem na sala, imediatamente
    # solicita o compartilhamento de informações
    if sentiuNovaPersonagem(percepcoes) and not(recemCompartilhado):
        recemCompartilhado = True
        return 'C'

    # Decide um novo movimento a ser realizado com base na atual
    # lista de salas vazias, retornando-o ao mundo
    acao = decidirProximoMovimento(salasVazias, posicao, orientacao)
    atualizarPosicao(acao)

    # Atualiza a flag de compartilhamento pra dizer que essa não
    # foi uma ação com compartilhamento
    recemCompartilhado = False

    return acao
