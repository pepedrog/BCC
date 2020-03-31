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


# Outras variáveis globais do módulo personagem10723624

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

global companhia
"""
Variável booleana que indica se há personagens disponíveis para
compartilhar informação.
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
    for i in range(N):
        linha = []
        for j in range(N):
            linha.append([])  # começa com listas vazias
        mundo.append(linha)
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0, 0]
    orientacao = [1, 0]
    # define os companheiros de espaço como uma lista vazia


def verificador(i, j, condicao1, condicao2):
    """ Verifica as casas adjacentes de (i, j), checando pelas condições
        1 e 2, avaliando quantas vezes elas se repetem. Se o resultador for 1, o
        retorno da função é True e as coordenadas do único vizinho que segue
        as condições, indicando que não há casas vizinhas nas condições
        específicadas, caso contrário o retorno é False, com 0, 0 para coordenadas
    """
    # declara as variáveis globais que serão acessadas
    global N, mundo

    contador = 0
    # ranger de cima e baixo
    for m in range(-1, 2):
        if mundo[(i + m) % N][j] != []:
            # analisa as casas pulando a atual
            if m != 0:
                if condicao1 in mundo[(i + m) % N][j] or condicao2 in mundo[(i + m) % N][j]:
                    contador += 1
                    posX = j
                    posY = (i + m) % N
        else:
            # número arbitrário diferente de 0
            contador = 10
    # ranger de direita e esquerda
    for n in range(-1, 2):
        if mundo[i][(j + n) % N] != []:
            if n != 0:
                if condicao1 in mundo[i][(j + n) % N] or condicao2 in mundo[i][(j + n) % N]:
                    contador += 1
                    posX = (j + n) % N
                    posY = i
        else:
            # número arbitrário diferente de 0
            contador = 10
    # se o contador for 1, há apenas uma posição da qual pode satisfazer as condições,
    # assim há certeza da localização
    if contador == 1:
        return True, posX, posY
    else:
        return False, 0, 0


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
    global N, mundo, posicao, orientacao, nFlechas, mundoCompartilhado, companhia
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # tags vindas de "percepção" que não sejam geradas por outros jogadores
    naoJogadores = ["F", "B", "I", "U"]
    # tags de identidade definida, que afirmam com exatidão o paradeiro da casa em certo momento
    definitivos = ["M", "V", "W", "P", "L"]
    # tags de aviso sobre perigo, que guardam informação sobre
    # informação coletada pela personagem na casa
    warnings = ["F", "B"]
    pos = posicao
    ori = orientacao

    # cria uma lista da posição atual da personagem, seja com um impacto (muro)
    # ou com uma casa livre visitada
    if "I" in percepcao:
        mundo[pos[0]][pos[1]] = ["M"]
        # desloca a posição da personagem em -1 (oposto ao sentido da orientação)
        pos = [(pos[0] - ori[0]) % N, (pos[1] - ori[1]) % N]
    else:
        mundo[pos[0]][pos[1]] = ["V", "L"]
        companhia = False
        # vaculha todos os elementos de percepcao
        for i in range(len(percepcao)):
            # valor para não gerar erros quando os elementos de percepção forem retirados
            fix = 0
            # acrescenta as tags de fedor e brisa na lista da casa
            if percepcao[i - fix] in warnings:
                mundo[pos[0]][pos[1]].append(percepcao[i])
            # teste do iten i da lista de percepções para identificar se há algum nome de personagem
            elif percepcao[i - fix] not in naoJogadores:
                # remove tudos os itens de percepcao que não forem jogadores
                percepcao.remove(percepcao[i])
                fix += 1
                companhia = True

    # denota as casas com possível existência de Wumpus com "W?"
    if "F" in percepcao:
        # percorre as casas vizinhas em coluna (em cima e em baixo)
        for i in [-1, 1]:
            # seleciona lista vazia ou sem tag definida (lista definitivos)
            # ordem "[]" depois mundo[i][j][0] impede que procure um
            # termo inexistente em uma lista vazia
            if mundo[(pos[0] + i) % N][pos[1]] == [] or \
                    mundo[(pos[0] + i) % N][pos[1]][0] not in definitivos:
                # impede a existência de mais de uma tag "W?" por casa
                if "W?" not in mundo[(pos[0] + i) % N][pos[1]]:
                    mundo[(pos[0] + i) % N][pos[1]].append("W?")
        # percorre as casas vizinhas em linha (na direita e na esquerda)
        for j in [-1, 1]:
            if mundo[pos[0]][(pos[1] + j) % N] == [] or \
                    mundo[pos[0]][(pos[1] + j) % N][0] not in definitivos:
                if "W?" not in mundo[pos[0]][(pos[1] + j) % N]:
                    mundo[pos[0]][(pos[1] + j) % N].append("W?")

    # denota as casas com possível existência de poços com "P?" (modelo adaptado da função acima)
    if "B" in percepcao:
        for i in [-1, 1]:
            if mundo[(pos[0] + i) % N][pos[1]] == [] or \
                    mundo[(pos[0] + i) % N][pos[1]][0] not in definitivos:
                if "P?" not in mundo[(pos[0] + i) % N][pos[1]]:
                    mundo[(pos[0] + i) % N][pos[1]].append("P?")
        for j in [-1, 1]:
            if mundo[pos[0]][(pos[1] + j) % N] == [] or \
                    mundo[pos[0]][(pos[1] + j) % N][0] not in definitivos:
                if "P?" not in mundo[pos[0]][(pos[1] + j) % N]:
                    mundo[pos[0]][(pos[1] + j) % N].append("P?")

    # se a única percepção é um urro, quer dizer que algum Wumpus morreu, ou seja,
    #  as casas em volta da personagem estão livres
    if percepcao == [] or percepcao == ["U"]:
        # verificação em cima e em baixo
        for i in [-1, 1]:
            # checa se a casa checada ainda não foi visitada pelo jogador
            if "V" not in mundo[(pos[0] + i) % N][pos[1]]:
                # define a tag "L" para a casa quando está vazia ou quando não for muro,
                # pois, por a percepcao ter sido vazia
                if mundo[(pos[0] + i) % N][pos[1]] == [] or \
                        mundo[(pos[0] + i) % N][pos[1]] != ["M"]:
                    mundo[(pos[0] + i) % N][pos[1]] = ["L"]
        # verificação na esquerda e na direita
        for j in [-1, 1]:
            if "V" not in mundo[pos[0]][(pos[1] + j) % N]:
                if mundo[pos[0]][(pos[1] + j) % N] == [] or \
                        mundo[pos[0]][(pos[1] + j) % N] != ["M"]:
                    mundo[pos[0]][(pos[1] + j) % N] = ["L"]

    for i in range(N):
        for j in range(N):
            # analisa as casas ao redor de um fedor para verificar a certeza de Wumpus
            if "F" in mundo[i][j]:
                wumpus, x, y = verificador(i, j, "W?", "W")
                if wumpus:
                    mundo[y][x] = ["W"]
            # analisa as casas ao redor de uma brisa para verificar a certeza de poço
            if "B" in mundo[i][j]:
                poco, x, y = verificador(i, j, "P?", "P")
                if poco:
                    mundo[y][x] = ["P"]

            # certifica que a posição (i,j) no mundo não é fixa
            if len(mundo[i][j]) > 0:
                k = mundo[i][j][0]
            else:
                k = mundo[i][j]
            if k not in definitivos:
                # como não confiamos na informação dada por outra personagem,
                # pelo menos não por completo, escrevemos assim um muro como possível
                # casa livre, para este módulo conferir se essa informação é correta,
                # o mesmo se repete para casas visitadas e livres em mundoCompartilhado
                possiveisLivres = ["M", "L", "V"]
                for k in range(len(possiveisLivres)):
                    if possiveisLivres[k] in mundoCompartilhado[i][j]:
                        # evita repetições
                        if "L?" not in mundo[i][j]:
                            mundo[i][j].append("L?")
                if "W" in mundoCompartilhado[i][j] or "W?" in mundoCompartilhado[i][j]:
                    if "W?" not in mundo[i][j]:
                        mundo[i][j].append("W?")
                elif "P" in mundoCompartilhado[i][j] or "P?" in mundoCompartilhado[i][j]:
                    if "P?" not in mundo[i][j]:
                        mundo[i][j].append("P?")
                # propositalmente este código não utiliza as informações de
                # fedor e brisa dadas por outras personagens, isto pois, se uma
                # casa apresenta fedor ou brisa identificada por outra personagem,
                # quer dizer que ela também está marcada com visitada e,
                # consequantemente, livre


def mapeamento(path):
    """ Cria uma lista de listas mapeando o mundo com valores -1 ou k, sendo este
        último a distância mínima até o local desejado em "passos" de uma unidade.
    """
    # declara as variáveis globais que serão acessadas
    global N

    k = 0
    finalizador = False
    while not finalizador:
        k += 1
        contagem = 0
        # vasculha a lista inteira
        for i in range(N):
            for j in range(N):
                # para todos os itens da lista iguas a k
                if path[i][j] == k:
                    # casas vizinhas em cima e em baixo
                    for m in [-1, 1]:
                        # vizinho vazio
                        if path[(i + m) % N][j] == 0:
                            path[(i + m) % N][j] = k + 1
                            contagem += 1
                        # possível caminho menor
                        elif path[(i + m) % N][j] > k:
                            path[(i + m) % N][j] = k + 1
                            contagem += 1
                    for n in [-1, 1]:
                        # vizinho vazio
                        if path[i][(j + n) % N] == 0:
                            path[i][(j + n) % N] = k + 1
                            contagem += 1
                        # possível caminho menor
                        elif path[i][(j + n) % N] > k:
                            path[i][(j + n) % N] = k + 1
                            contagem += 1
        # se não foi somado nenhum k+1, a varredura pelo mapa está completa
        if contagem == 0:
            finalizador = True
    return path


def pathfinder(objeto, contra=0):
    """ Define o caminho mais curto até o ponto procurado, retornando
        se é possível chegar ao local desejado e o comando necessário
        para cada passo. Esta função também diferencia para caso o jogador
        esteja procurando um Wumpus, parando em frente ao monstro, preparado
        para atirar uma flecha.
    """
    # declara as variáveis globais que serão acessadas
    global N, mundo

    # cria uma matriz NxN
    path = []
    for i in range(N):
        linha = []
        for j in range(N):
            linha.append([])
        path.append(linha)
    for i in range(N):
        for j in range(N):
            # donota as coordenadas de path, com -1 para posições
            # não transitáveis e 0 para as transitaveis ("V")
            path[i][j] = mundo[i][j]
            if "V" not in path[i][j]:
                path[i][j] = -1
            else:
                path[i][j] = 0
    # caso o objeto seja um Wumpus, não queremos a personagem entrando na casa,
    # mas sim chegando o mais próximo possível dela, para poder matá-lo
    if objeto == "W":
        # procura na lista mundo inteira qualquer aparição de "M"
        for i in range(N):
            for j in range(N):
                if "W" in mundo[i][j]:
                    # vizinhos de cima e de baixo
                    for m in [-1, 1]:
                        if path[(i+m) % N][j] != -1:
                            # se não for uma casa perigosa, é marcada como destino possível
                            path[(i+m) % N][j] = 1
                    # vizinhos da esquerda e direita
                    for n in [-1, 1]:
                        if path[i][(j+n) % N] != -1:
                            # se não for uma casa perigosa, é marcada como destino possível
                            path[i][(j+n) % N] = 1
    else:
        # procura na lista inteira qualquer aparição de objeto
        for i in range(N):
            for j in range(N):
                # como o padrão de contra (caso nehuma especificação seja dada) é 0, ele
                # nunca aparecerá em mundo. As casas demarcadas com 1 serão as que não
                #  possuem o contra nelas e possuem objeto
                if objeto in mundo[i][j] and contra not in mundo[i][j]:
                    path[i][j] = 1
    path = mapeamento(path)
    return path


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, nFlechas, mundoCompartilhado, companhia
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

    if mundo[pos[0]][pos[1]] == ["M"]:
        pos[0] = (pos[0]-ori[0]) % N
        pos[1] = (pos[1]-ori[1]) % N

    if companhia:
        acao = "C"

    else:
        # procura as casas com "W" no mundo e marca as casas de path com a distancia até elas,
        # se não houver Wumpus no mapa todas as casas válidas para locomoção serão 0
        path = pathfinder("W")
        # minimo indica a posição com menor valor em path, ou seja, a posição entre os viznhos
        # mais próxima do ponto de interesse no momento
        minimo = path[pos[0]][pos[1]]
        # vizinhos de cima e de baixo
        for i in [-1, 1]:
            # testa se a casa é valida para andar e se possui valor menor que o minimo atual
            if path[(pos[0]+i) % N][pos[1]] != -1 and path[(pos[0]+i) % N][pos[1]] < minimo:
                minimo = path[(pos[0]+i) % N][pos[1]]
        for j in [-1, 1]:
            if path[pos[0]][(pos[1]+j) % N] != -1 and path[pos[0]][(pos[1]+j) % N] < minimo:
                minimo = path[pos[0]][(pos[1]+j) % N]

        if ori[0] == 0:
            es = -1
        else:
            es = 1
        TempOri = es*ori[1]

        # checa se a personagem está no local destinado
        if path[pos[0]][pos[1]] == 1 and nFlechas > 0:
            # confere se realmente há um fedor na região, afinal alguém pode ter matado
            # este Wumpus enquanto a personagem estava longe
            if "F" in mundo[pos[0]][pos[1]]:
                # última confirmação da posição do Wumpus antes de arriscar atirar
                if "W" in mundo[(pos[0] + ori[0]) % N][(pos[1] + ori[1]) % N]:
                    acao = "T"
                elif "W" in mundo[(pos[0] + TempOri) % N][(pos[1] + ori[0]) % N]:
                    acao = "E"
                else:
                    acao = "D"
        # se a posição for 0, não há caminho até o destino e não há necessidade
        # em ir atrás de um Wumpus se não há flechas sobrando
        elif path[pos[0]][pos[1]] != 0 and nFlechas > 0:
            # a personagem sempre se deslocará para casas de menor valor em path
            if minimo == path[(pos[0] + ori[0]) % N][(pos[1] + ori[1]) % N]:
                acao = "A"
            elif minimo == path[(pos[0] + TempOri) % N][(pos[1] + ori[0]) % N]:
                acao = "E"
            else:
                acao = "D"

        else:
            # mundo com as distâncias para as casas livres não visitadas
            path = pathfinder("L", "V")
            # existe caminho até a casa desejada
            minimo = path[pos[0]][pos[1]]
            # vizinhos de cima e de baixo
            for i in [-1, 1]:
                # testa se a casa é valida para andar e se possui valor menor que o minimo atual
                if path[(pos[0]+i) % N][pos[1]] != -1 and path[(pos[0]+i) % N][pos[1]] < minimo:
                    minimo = path[(pos[0]+i) % N][pos[1]]
            for j in [-1, 1]:
                if path[pos[0]][(pos[1]+j) % N] != -1 and path[pos[0]][(pos[1]+j) % N] < minimo:
                    minimo = path[pos[0]][(pos[1]+j) % N]

            if path[0][0] != 0:
                # a personagem sempre se deslocará para casas de menor valor em path
                if minimo == path[(pos[0] + ori[0]) % N][(pos[1] + ori[1]) % N]:
                    acao = "A"
                elif minimo == path[(pos[0] + TempOri) % N][(pos[1] + ori[0]) % N]:
                    acao = "E"
                else:
                    acao = "D"
            # não existe caminho até a casa desejada
            else:
                path = pathfinder("L?")
                minimo = path[pos[0]][pos[1]]
                # vizinhos de cima e de baixo
                for i in [-1, 1]:
                    # testa se a casa é valida para andar e se possui valor menor que o minimo atual
                    if path[(pos[0]+i) % N][pos[1]] != -1 and path[(pos[0]+i) % N][pos[1]] < minimo:
                        minimo = path[(pos[0]+i) % N][pos[1]]
                for j in [-1, 1]:
                    if path[pos[0]][(pos[1]+j) % N] != -1 and path[pos[0]][(pos[1]+j) % N] < minimo:
                        minimo = path[pos[0]][(pos[1]+j) % N]

                if path[0][0] != 0:
                    # a personagem sempre se deslocará para casas de menor valor em path
                    if minimo == path[(pos[0] + ori[0]) % N][(pos[1] + ori[1]) % N]:
                        acao = "A"
                    elif minimo == path[(pos[0] + TempOri) % N][(pos[1] + ori[0]) % N]:
                        acao = "E"
                    else:
                        acao = "D"
                # não existe caminho até a casa desejada
                else:
                    # quando não há casa descoberta que tenha a certeza de um wumpus presente,
                    # que a casa esteja, com certeza, livre (descoberta por este player),
                    # ou que há casa possivelmente livre (dada por outro player), este módulo
                    # irá girar em mesma posição até algum outro jogador chegar e passar mais
                    # informações sobre o mundo
                    acao = "D"

    if acao == "A":
        pos[0] = (pos[0]+ori[0]) % N
        pos[1] = (pos[1]+ori[1]) % N
    if acao == "E":
        if ori[0] == 0:
            ori[1] = -ori[1]
        ori[0], ori[1] = ori[1], ori[0]
    if acao == "D":
        if ori[1] == 0:
            ori[0] = -ori[0]
        ori[0], ori[1] = ori[1], ori[0]

    assert acao in ["A", "D", "E", "T", "C"]
    return acao
