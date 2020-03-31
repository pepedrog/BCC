# ATENÇÃO: Você pode customizar o módulo alterando o valor abaixo.
INTERATIVIDADE = 0
# ATENÇÃO: Você pode customizar o módulo alterando o valor acima
"""
---------------------------------------------------------------------
Se INTERATIVIDADE = 0 (Não interativo), nenhum diálogo será exibido
na tela e você poderá acompanhar somente as mensagens exibidas pelo
mundo, como 'Você caiu em um Poço!' ou 'Você matou o Wumpus!'
---------------------------------------------------------------------
Se INTERATIVIDADE = 1, os diálogos acerca da representação do mundo
da personagem serão exibidos na tela, assim você poderá acompanhar
cada passo do protagonista. Além disso, você usará a tecla 'Enter'
para avançar para o próximo passo.
---------------------------------------------------------------------
Se INTERATIVIDADE = 2 (Interativo), os diálogos serão exibidos
normalmente e você poderá decidir as ações da personagem.
---------------------------------------------------------------------
Observação: Os diálogos acerca do mundo e do mundo compartilhado
estão dividios por um ponto (.)
---------------------------------------------------------------------
"""

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

global rotas
"""
Representa o conjunto de todas as possiveis rotas para posições livres
que a personagem pode tomar à fim de percorrer o mundo de Wumpus mantendo-se
viva. Cada vez que a personagem passa por uma localização com posições
adjacentes livres, é incluído na lista de rotas estas posições para que a
personagem possa explorá-las em um futuro breve.
"""

global rotaatual
"""
A 'rota atual' faz referência ao atual caminho definido pela personagem.
Em geral, esta é a primeira rota definida na variável rotas, que engendra
todas as posições que a personagem ainda pretende visitar.
"""

global comandos
"""
Esta variável representa a fila de comandos que a personagem precisa
tomar à fim de chegar ao ponto indicado. Para cada ponto previamente
adicionado na lista de rotas (e, portanto, para cada casa livre
conhecida), cria-se a lista de comandos que a personagem irá seguir
à fim de alcançar uma casa livre.
"""

global pInformacao
"""
Está variável é um valor inteiro e só é ativada quando a personagem
detecta algum outro personagem na mesma posição. Nesta ocasião, esta
variável, 'Pedir Informação' é ativada, fazendo com que a personagem
compartilhe informações na próxima ação.
Quando pInformacao = 0, a personagem não percebe ninguem para
compartilhar; quando pInformacao = 1, a personagem percebeu alguém e
irá compartilhar na próxima ação; quando pInformacao = 2, a personagem
já compartilhou informação e agora irá atualizar seu mundo.
"""

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).
    """

    # Declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, rotas, rotaatual, comandos, pInformacao
    # Guarda o tamanho do mundo
    N = tamanho
    # Cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mundo.append(linha)
    # Posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    # As rotas e os comandos disponíveis no início são sempre nulos.
    rotas = []
    comandos = []
    # A personagem inicia o jogo sem rota predeterminada.
    rotaatual = [0,0]
    # A personagem também não pensa em solicitar informações.
    pInformacao = 0
    # Marca a posição inicial como Visitada e Livre. Podemos fazer isso mesmo
    # que esta posição seja, por exemplo, um poço; neste caso, a personagem
    # perde antes de começar a jogar. Só há jogo, portanto, quando a primeira
    # posição é livre.
    mundo[0][0] = ['L']


def marcar(evento):
    """ Esta função é utilizada para marcar algum evento, como 'L', 'P'
    ou 'W' nas casas adjacentes ao personagem. Não serão feitas marcações
    caso as posições já estejam rotuladas com 'L' ou 'M'.
    """
    
    # Declara as variáveis globais que serão acessadas.
    global N, mundo, posicao
    # Guarda a posição atual na variável 'pos'.
    pos = posicao
    # A variável i assume o valor, respectivamente, das posições ao norte,
    # ao sul, à oeste e à leste da atual posição da personagem.
    for i in [[(pos[0]-1)%N,pos[1]],[(pos[0]+1)%N,pos[1]],[pos[0],(pos[1]-1)%N],[pos[0],(pos[1]+1)%N]]:
        # Se a posição não estiver rotulada com 'L' ou 'M', marca-a com
        # o evento determinado.
        if not 'L' in mundo[i[0]][i[1]] and not 'M' in mundo[i[0]][i[1]] and not evento in mundo[i[0]][i[1]]:
            # Desmarca a possibilidade de Poço caso esteja sendo
            # marcado posição Livre.
            if evento == 'L' and 'P?' in mundo[i[0]][i[1]]:
                mundo[i[0]][i[1]].remove('P?')
            # Desmarca a possibilidade de Wumpus caso esteja sendo
            # marcado posição Livre.
            if evento == 'L' and 'W?' in mundo[i[0]][i[1]]:
                mundo[i[0]][i[1]].remove('W?')
            # Verifica, antes de marcar um evento, se já não existe uma
            # certeza de Poço ou Wumpus naquela região.
            if not (evento == 'P?' and 'P' in mundo[i[0]][i[1]]) and not (evento == 'W?' and 'W' in mundo[i[0]][i[1]]):
                # Marca na posição o evento determinado.
                mundo[i[0]][i[1]].append(evento)


def marcarduplo():
    """ Esta função é utilizada somente para marcar a possibilidade de
    existir simultaneamente um Poço e um Wumpus na região.
    """
    
    # Declara as variáveis globais que serão acessadas.
    global N, mundo, posicao
    # Guarda a posição atual na variável 'pos'.
    pos = posicao
    # Similar à função 'marcar', i assume o norte, o sul, o oeste e o leste.
    for i in [[(pos[0]-1)%N,pos[1]],[(pos[0]+1)%N,pos[1]],[pos[0],(pos[1]-1)%N],[pos[0],(pos[1]+1)%N]]:
        # Se a posição não estiver rotulada com nenhum valor já conhecido,
        # como 'L', 'M', 'P?', 'P', 'W? e 'W', podemos marcar a posição
        # com os valores simultâneos de Poço e Wumpus.
        if not 'L' in mundo[i[0]][i[1]] and not 'M' in mundo[i[0]][i[1]] and not 'P' in mundo[i[0]][i[1]] and not 'P?' in mundo[i[0]][i[1]] and not 'W' in mundo[i[0]][i[1]] and not 'W?' in mundo[i[0]][i[1]]:
            mundo[i[0]][i[1]].append('P?')
            mundo[i[0]][i[1]].append('W?')


def contagem():
    """ Esta função tem como objetivo contar o número de casas livres
    ou rotuladas com 'M' ao redor da posição atual da personagem. Se
    existir apenas uma única posição não-livre (ou 'M') adjacente, a
    função retorna esta posição; do contrário, esta função retorna o
    número de casas adjacentes livres.
    """

    # Declara as variáveis globais que serão acessadas.
    global N, mundo, posicao
    # Inicializa as variáveis especificas no tratamento da função.
    contador, perigo = 0, 0
    # Guarda a posição atual na variável 'pos'.
    pos = posicao
    # Similar à função 'marcar', i assume o norte, o sul, o oeste e o leste.
    for i in [[(pos[0]-1)%N,pos[1]],[(pos[0]+1)%N,pos[1]],[pos[0],(pos[1]-1)%N],[pos[0],(pos[1]+1)%N]]:
        # Verifica para cada uma das posições assimiladas se elas estão livres
        # (ou rotuladas com 'M'). 
        if 'L' in mundo[i[0]][i[1]] or 'M' in mundo[i[0]][i[1]]:
            contador += 1
        else:
            perigo = i
    # Se há 3 casas adjacentes livres, há uma única casa adjacente não-livre;
    # neste caso, a função retorna a posição desta casa. Se há um número
    # diferente de casas livres, a função retorna este valor.
    if contador == 3:
        return perigo
    else:
        return contador


def pathfinder(ponto):
    """ Esta função é responsável por encontrar um caminho seguro
    do ponto em que a personagem se encontra no momento até o
    ponto desejado (possivelmente uma casa livre e ainda não visitada)
    """

    # Declara as variáveis globais que serão acessadas.
    global N, mundo, posicao, orientacao, comandos

    # Limpa os comandos, caso ainda haja algum na fila.
    comandos = []

    # Declara as variáveis utilizadas nesta função.
    posatual = [posicao[0], posicao[1]] # Posição
    oriatual = [orientacao[0], orientacao[1]] # Orientação
    representacao = [] # Matriz de representação do mundo
    encontrei = True # Variável qualquer para laço
    k = 2 # Contador qualquer para laço

    # Cria uma matriz NxN (do tamanho do mundo) que representa este
    # universo a partir de valores inteiros.
    for i in range(N) : 
        representacao.append([])
        for j in range(N) : 
            representacao[i].append(0) # começa com listas nulas

    # Atribui o valor '-2' para todas as posições na matriz representação
    # que apresenta alguma ameaça (por exemplo: P, P?, W, W?) ou ainda é
    # desconhecida (não tem rótulo algum).
    for i in range(N):
        for j in range(N):
            if not 'L' in mundo[i][j]:
                representacao[i][j] = -2

    # Atribui o valor '1' para a posição em que dejesamos chegar.
    representacao[ponto[0]][ponto[1]] = 1

    # O seguinte laço realiza, para cada k, uma varredura completa da
    # matriz de representação e atribui o valor k para posições com
    # regiões adjacentes valendo k-1. Dessa forma, cada casa passa
    # a significar o número de passos necessários para se atingir a
    # posição pretendida.
    while encontrei:
        encontrei = False
        for i in range(N):
            for j in range(N):
                # verifica se o valor ainda não foi atribuido e se
                # as casas adjacentes valem k-1.
                if representacao[i][j] == 0 and (representacao[(i-1)%N][j] == k -1 or representacao[(i+1)%N][j] == k -1 or representacao[i][(j-1)%N] == k -1 or representacao[i][(j+1)%N] == k -1):
                    representacao[i][j] = k
                    encontrei = True
        k += 1

    # O seguinte laço executa as atribuições elaboradas no percurso
    # definido anteriormente e adiciona as futuras ações à lista
    # de comandos.
    kpersonagem = representacao[posatual[0]][posatual[1]]
    while kpersonagem > 1:
        # Calcula qual é a posição à frente da personagem
        frente = [(posatual[0] + oriatual[0])%N, (posatual[1] + oriatual[1])%N]
        # Verifica se a posição à frente da personagem é a casa correta
        # para realizar o movimento predefinido pela rota.
        if representacao[frente[0]][frente[1]] == kpersonagem -1:
            posatual[0], posatual[1] = frente[0], frente[1]
            comandos.append('A')
        else:
            # Calcula qual é a posição atrás da personagem
            atras = [(posatual[0] - oriatual[0])%N, (posatual[1] - oriatual[1])%N]
            # Verifica se a posição atrás da personagem é a casa correta
            # para realizar o movimento predefinido pela rota.
            if representacao[atras[0]][atras[1]] == kpersonagem -1:
                posatual[0], posatual[1] = atras[0], atras[1]
                oriatual[0], oriatual[1] = -oriatual[0], -oriatual[1]
                comandos += ['E','E','A']
            else:
                # Calcula qual é a posição à esquerda da personagem
                a, b = oriatual[0], oriatual[1]
                if a == 0:
                    b = -b
                a, b = b, a
                aesquerda = [(posatual[0] + a)%N, (posatual[1] + b)%N]
                # Verifica se a posição à esquerda da personagem é a casa correta
                # para realizar o movimento predefinido pela rota.
                if representacao[aesquerda[0]][aesquerda[1]] == kpersonagem -1:
                    posatual[0], posatual[1] = aesquerda[0], aesquerda[1]
                    oriatual[0], oriatual[1] = a, b
                    comandos += ['E', 'A']
                else:
                    # Calcula qual é a posição à direita da personagem
                    a, b = oriatual[0], oriatual[1]
                    if b == 0:
                        a = -a
                    a, b = b, a
                    adireita = [(posatual[0] + a)%N, (posatual[1] + b)%N]
                    # Verifica se a posição à direita da personagem é a casa correta
                    # para realizar o movimento predefinido pela rota.
                    if representacao[adireita[0]][adireita[1]] == kpersonagem -1:
                        posatual[0], posatual[1] = adireita[0], adireita[1]
                        oriatual[0], oriatual[1] = a, b
                        comandos += ['D', 'A']
                    else:
                        # Se nenhuma das quatro posições (à frente, atras,
                        # à direita e à esquerda) funcionou corretamente
                        # na execução deste código, há algo errado.
                        raise Exception('Erro na função Pathfinder!')
        # Realiza a subtração para manter a coerência do laço
        kpersonagem -= 1


def compartilhar():
    """
    Esta função tem por objetivo inserir as informações que foram
    compartilhadas com a personagem na sua representação do mundo.
    Para isso, percorremos todo o mundo compartilhado e comparamos
    com as informações que a nossa personagem possui.
    """

    # Declara as variáveis globais que serão acessadas.
    global N, mundo, mundoCompartilhado

    # O seguinte laço percorre todos os elementos do mundo e do
    # mundoCompartilhado, fazendo algumas comparações. Em geral,
    # vamos adicionar elementos à nossa representação se a posição
    # estiver vazia ou se há possibilidade de existir algum perigo
    for i in range(N):
        for j in range(N):
            if not 'V' in mundo[i][j]:
                # Adiciona-se local 'L' ao mundo.
                if mundoCompartilhado[i][j] == ['L']:
                    mundo[i][j] = ['L']
                # Adiciona-se 'P' ao mundo.
                if mundoCompartilhado[i][j] == ['P']:
                    mundo[i][j] = ['P']
                # Adiciona-se 'W' ao mundo.
                if mundoCompartilhado[i][j] == ['W']:
                    mundo[i][j] = ['W']

    # Aqui, é importante fazer uma varredura das posições para ver se é
    # possível encontrar novas casas livres a partir das informações que
    # a personagem recebeu.
    for i in range(N):
        for j in range(N):
            if not [i,j] == rotaatual and not [i,j] in rotas and mundo[i][j] == ['L']:
                rotas.append([i,j])


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

    # Declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, pInformacao

    # Define as variáveis de posição e orientação.
    pos, ori = posicao, orientacao

    # Define a variável 'tamanho da percepção', utilizada na
    # verificação de possíveis aliados.
    tampercepcao = len(percepcao)

    # Se a personagem recebeu um impacto, é necessário corrigir
    # a posição relativa e marcar a proxima posição com 'M'.
    # Isto deve ser feito antes de tudo para evitar que o código
    # seja rodado com a posição não corrigida!
    if 'I' in percepcao:
        tampercepcao -= 1 # Um item percebido é o 'I'
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)
        mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ['V', 'M']

    # Se a personagem acabou de compartilhar informações, é o momento certo
    # para ela adicionar estas novidades à sua representação do mundo.
    if pInformacao == 2:
        pInformacao = 0 # Zera a variável para permitir novos compartilhamentos.
        compartilhar()

    # Se a personagem está em uma posição rotulada como ameaça e
    # está jogando (ou seja, viva), podemos concluir que a casa
    # está livre.
    if 'P?' in mundo[pos[0]][pos[1]] or 'W?' in mundo[pos[0]][pos[1]]:
        mundo[pos[0]][pos[1]] = ['V', 'L']

    # Insere o rótulo 'V' (Visitado) na posição atual.
    if not 'V' in mundo[pos[0]][pos[1]]:
        mundo[pos[0]][pos[1]].insert(0, 'V')

    # Gerenciamento de ameaças.
    if not 'B' in percepcao and not 'F' in percepcao:
        # Se não há brisa nem fedor próximo, posso concluir que as
        # casas adjacentes estão livres.
        marcar('L')
    elif 'B' in percepcao and not 'F' in percepcao:
        tampercepcao -= 1 # Outro item percebido é a 'B'
        # Se a personagem esta sentindo uma brisa, é necessário marcar
        # a possibilidade de um poço nas casas adjacentes.
        i = contagem()
        # Se a contagem retornar um valor inteiro, significa que há
        # mais de uma casa adjacente não-livre; marcaremos, então, estas
        # posições. Se a contagem retornar uma posição, significa que
        # esta é a única casa não-livre adjacente ao personagem,
        # podemos concluir certamente que existe um poço ('P')
        # nesta região.
        if type(i) == int:
            marcar('P?')
        else:
            mundo[i[0]][i[1]] = ['P']
    elif not 'B' in percepcao and 'F' in percepcao:
        tampercepcao -= 1 # Outro item percebido é o 'F'
        # Se a personagem esta sentindo um fedor, é necessário marcar
        # a possibilidade de um Wumpus nas casas adjacentes!
        i = contagem()
        # Aqui, ocorre um tratamento similar ao dado para a marcação
        # das posições de Poço.
        if type(i) == int:
            marcar('W?')
        else:
            mundo[i[0]][i[1]] = ['W']
    else:
        tampercepcao -= 2 # Outros itens percebidos são a 'B' e o 'F'
        # Se a personagem está sentindo simultaneamente um fedor e uma
        # brisa, é necessário utilizar as duas marcações ao mesmo
        # tempo para não sobrescrever outras regiões.
        # Obs: Como sabemos que existem pelo menos dois perigos ao lado,
        # não é necessário realizar a contagem para averiguar certezas
        # de Poço ou Wumpus.
        marcarduplo()
        
    # Se a personagem ouvir um urro, significa que não há mais perigo
    # à frente, isto é, a posição pode ser marcada como 'L'
    if 'U' in percepcao:
        tampercepcao -= 1 # Outro item percebido é o 'U'
        mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ['L']

    # Se a personagem notar algo além de 'I','B','F' e 'U' na lista de
    # percepções, significa que há mais algum personagem. A variável é
    # ativada para que a nossa personagem compartilhe informações na
    # próxima ação.
    if tampercepcao > 0:
        pInformacao = 1

    # ################### I N T E R A T I V I D A D E #####################
    if INTERATIVIDADE == 1 or INTERATIVIDADE == 2:
        print("Percepção recebida pela personagem:", percepcao)
        
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
                print("".join(mundo[i][j]),end="\t.")
                print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(16*len(mundo)+1))
    # #####################################################################


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # Declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, rotas, rotaatual, comandos, pInformacao

    # Define as variáveis de posição e orientação.
    pos, ori = posicao, orientacao

    # Definição das posições adjacentes ao local atual da
    # personagem. Isto será utilizado para montar a estratégia.
    norte = [(pos[0]-1)%N,pos[1]]
    sul = [(pos[0]+1)%N,pos[1]]
    oeste = [pos[0],(pos[1]-1)%N]
    leste = [pos[0],(pos[1]+1)%N]

    # Aqui, adicionamos às rotas as casas livres (Obs: isso não inclui
    # casas livres e visitadas). Em outras palavras, marcamos todas as
    # casas livres para visitar em alguma ocasião futura.
    for i in [sul, norte, oeste, leste]:
        # Verificamos se a posição desejada esta rotulada como livre.
        if not i == rotaatual and not i in rotas and mundo[i[0]][i[1]] == ['L']:
            rotas.append(i)

    # Aqui, verificamos se o terrível Wumpus foi detectado em alguma posição
    # adjacente à personagem. Em teoria, a personagem deve eliminar o Wumpus
    # na maior parte dos jogos, já que, em algum momento, a personagem irá
    # traçar uma rota para uma posição vizinha (e ainda não visitada) do
    # Wumpus e, neste momento, detectá-lo.
    for i in [sul, norte, oeste, leste]:
        if mundo[i[0]][i[1]] == ['W']:
            # Neste momento, o Wumpus foi detectado. A partir daqui, pedimos
            # ajuda para a função pathfinder para traçar uma rota (basicamente
            # em se tratando das rotações da personagem) e trocamos a ultima
            # ação (ir em direção ao Wumpus) por atirar.
            rotaatual = i
            pathfinder(rotaatual)
            comandos.pop()
            if nFlechas > 0:
                comandos.append('T')
            
    # Este código é o cerne da estratégia tomada pelo computador durante
    # o jogo. Vamos sempre manter uma lista (rotas) atualizada com as
    # posições de todas as casas livres e ainda não visitadas. A partir
    # desta lista, vamos elaborar uma lista de comandos que permitirá
    # a personagem ir até as casas livres e ainda não visitadas.
    if pInformacao == 1:
        # Se a condição for verificada, a personagem deve imediatamente
        # compartilhar informações
        pInformacao = 2
        acao = 'C'
    elif len(comandos) == 0:
        while len(rotas) > 0:
            # Confirma se a primeira posição na lista de rotas
            # está marcada apenas como 'L'. É importante realizar
            # este procedimento porque a personagem pode visitar
            # esta posição durante alguma rota anterior.
            if mundo[rotas[0][0]][rotas[0][1]] == ['L']:
                # Caso a primeira rota seja adequada, chamamos a função
                # pathfinder para encontrar o melhor caminho da personagem
                # até o ponto desejado
                rotaatual = rotas.pop(0)
                pathfinder(rotaatual)
                break
            else:
                # Se a primeira rota não for adequada, vamos removê-la
                rotas.pop(0)
        if len(comandos) == 0:
            # Se não há rotas nem comandos disponíveis, a personagem
            # começa a girar esperando possivelmente encontrar alguem
            # para trocar informações.
            acao = 'E'
        else:
            acao = comandos.pop(0)
    else:
        acao = comandos.pop(0)


    # ################### I N T E R A T I V I D A D E #####################
    if INTERATIVIDADE == 1:
        dialog = input('Aperte Enter para continuar...')
    if INTERATIVIDADE == 2:
        acao = input("Digite a ação desejada (A/D/E/T/C): ")
    # #####################################################################


    # Atualiza as posições relativas à personagem com base na ação
    # decidida anteriormente. Caso a personagem sofra um impacto de
    # um muro, a posição será corrigida na função 'planejar'
    if acao == 'A':
        # Movimento para frente
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
    if acao == 'E':
        # Movimento para a esquerda
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
    if acao == 'D':
        # Movimento para a direita
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]

    # Verificação e retorno da ação.
    assert acao in ["A","D","E","T","C"]
    return acao
