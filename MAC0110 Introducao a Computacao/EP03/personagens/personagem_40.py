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

global usacompartilhado
"""
Permite que a personagem adquira informações do mundo compartilhado
somente após o uso de C, para evitar duplicações de informação
"""

global compartilhou
"""
Determina se o personagem já compartilhou nessa sala. Essa
variável evita que a personagem fique compartilhando
indefinidamente.
"""

global tempersonagem
"""
Determina se há personagem na sala ou não.
"""

global instrucoes
"""
Lista que receberá o caminho que o personagem decide seguir.
"""

global salaslivres
global salaspotencialmentelivres
global listadewumpus
global possiveiswumpus
"""
Listas que receberão as coordenadas das células contendo salas livres ("L"),
salas potencialmente livres ("L?"), wumpuses ("W") e possíveis wumpuses ("W?").
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
    global N, mundo, posicao, orientacao, usacompartilhado, compartilhou, instrucoes
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
    # Define que as informações do mundo compartilhado não serão agregadas ao mundo
    # real até a utilização de "C" após encontrar uma personagem.
    usacompartilhado = False
    # Define valor inicial da variável para correto funcionamento do mecanismo.
    # Caso a personagem fique presa no inicio, não podendo dar passo sem risco,
    # ela rotacionará até que outra personagem ache ela.
    compartilhou = False
    # Define que inicialmente a personagem não deve seguir nenhuma instrução
    instrucoes = []


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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, \
        usacompartilhado, instrucoes, salaslivres, salaspotencialmentelivres, \
        listadewumpus, possiveiswumpus, tempersonagem
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
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        pos = posicao
        ori = orientacao
        # mostra na tela (para o usuário) o mundo conhecido pela personagem
        # e o mundo compartilhado (quando disponível)
        print("Mundo conhecido pela personagem:")
        for i in range(len(mundo)):
            for j in range(len(mundo[0])):
                if pos == [i, j]:
                    if ori == [0, -1]:
                        print("<", end="")
                    print("X", end="")
                    if ori == [0, 1]:
                        print(">", end="")
                    if ori == [1, 0]:
                        print("v", end="")
                    if ori == [-1, 0]:
                        print("^", end="")
                print("".join(mundo[i][j]), end="")
                print(end="\t| ")
            print("\n" + "-" * (8 * len(mundo) + 1))
        # Permite acompanhar o jogo passo a passo.
        input()
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

    # Atribui variável de contador para o correto funcionamento do laço.
    contapercepcao = 0
    # Verifica se há outra personagem na mesma célula.
    # Itera pelos valores adquiridos pela percepção
    for item in percepcao:
        # Se existe valor, aumenta o contador em um.
        # Esse mecanismo é utilizado ao invés de simples atribuição à
        # tempersonagem para evitar que, na próxima iteração,
        # o valor retorne para False.
        if item != "F" and item != "B" and item != "I" and item != "U":
            contapercepcao += 1
    # Se foi constatado que há personagem, coloca variável como True.
    # Caso contrário, coloca variável como False.
    if contapercepcao > 0:
        tempersonagem = True
    else:
        tempersonagem = False

    # Se houve impacto com muro, muda a posição do personagem
    # para o valor correto. Caso contrário, a personagem
    # consideraria estar na célula do muro.
    if "I" in percepcao:
        mundo[posicao[0]][posicao[1]] = ["M"]
        posicao = [(posicao[0] - orientacao[0]) % N,
                   (posicao[1] - orientacao[1]) % N]

    # Realiza as marcações conforme o personagem anda,
    # e somente se a sala atual não foi visitada.
    if "V" not in mundo[posicao[0]][posicao[1]]:
        # Se há percepção de fedor e a sala já não foi marcada,
        # marca a sala com "F" e chama a função manipulaEntorno(mundo)
        # para marcar as células vizinhas com "W?", indicando
        # possibilidade de haver Wumpus.
        # Também remove as marcações de "L?".
        if ("F" in percepcao) and ("F" not in mundo[posicao[0]][posicao[1]]):
            mundo[posicao[0]][posicao[1]].append("F")
            manipulaEntorno(mundo, posicao[0], posicao[1], ["W?"])
            manipulaEntorno(mundo, posicao[0], posicao[1], ["L?"], "r")
        # Se há percepção de brisa e a sala já não foi marcada,
        # marca a sala com "B" e chama a função manipulaEntorno(mundo)
        # para marcar as células vizinhas com "P?", indicando
        # possibilidade de haver poço.
        # Também remove as marcações de "L?".
        if ("B" in percepcao) and ("B" not in mundo[posicao[0]][posicao[1]]):
            mundo[posicao[0]][posicao[1]].append("B")
            manipulaEntorno(mundo, posicao[0], posicao[1], ["P?"])
            manipulaEntorno(mundo, posicao[0], posicao[1], ["L?"], "r")
        # Se não há percepção de brisa nem de fedor, chama a função
        # manipulaEntorno(mundo) para marcar células vizinhas com "L",
        # indicando que a sala está livre (ainda há chance de haver
        # um muro em uma das salas). E chama a função manipulaEntorno
        # em modo "r" para remover "W?"s, "P?"s e "L?s" vizinhos.
        if ("B" not in percepcao) and ("F" not in percepcao):
            manipulaEntorno(mundo, posicao[0], posicao[1], ["L"])
            manipulaEntorno(mundo, posicao[0], posicao[1], [
                            "W?"], "r")
            manipulaEntorno(mundo, posicao[0], posicao[1], [
                            "P?"], "r")
            manipulaEntorno(mundo, posicao[0], posicao[1], [
                            "L?"], "r")

        # Marca sala atual como visitada ("V"). A marcação foi feita
        # no index 0 de forma a facilitar a depuração.
        # Essa marcação é a última que deve ser feita nessa indentação
        # de forma a garantir o correto funcionamento da função
        # manipulaEntorno(mundo).
        mundo[posicao[0]][posicao[1]].insert(0, "V")
        # Remove "L", "L?, "W?", "P?" caso existam, dado que agora a sala
        # já foi visitada.
        if "L" in mundo[posicao[0]][posicao[1]]:
            mundo[posicao[0]][posicao[1]].remove("L")
        if "L?" in mundo[posicao[0]][posicao[1]]:
            mundo[posicao[0]][posicao[1]].remove("L?")
        if "W?" in mundo[posicao[0]][posicao[1]]:
            mundo[posicao[0]][posicao[1]].remove("W?")
        if "P?" in mundo[posicao[0]][posicao[1]]:
            mundo[posicao[0]][posicao[1]].remove("P?")

    # Define valor inicial às listas, necessário para o correto funcionamento do laço.
    salaslivres = []
    salaspotencialmentelivres = []
    listadewumpus = []
    possiveiswumpus = []
    # Escaneia por todas as células do mundo, realizando
    # marcações.
    for i in range(N):
        for j in range(N):
            """
            Deduz onde estão os Wumpus e poços. A dedução funciona
            chamando a função manipulaEntorno em modo contador nas células
            com "F" e "B", para contar o número de aparições de "W?", "P?"
            "W" e "P" nas células vizinhas. Caso exista somente um "W?"
            ou somente um "P?" vizinhos, e caso não exista "W" ou "P" vizinhos
            já determinados, essas células são marcadas como "W" ou "P"
            pelo uso de manipulaEntorno em modo substituição.
            """
            if ("F" in mundo[i][j]) and (manipulaEntorno(mundo, i, j, ["W?"], "c") == 1)\
                    and (manipulaEntorno(mundo, i, j, ["W"], "c") == 0):
                manipulaEntorno(mundo, i, j, ["W?"],
                                "s", "W", "P?")
                # Deduz existência de Wumpus em células do entorno que contém tanto
                # "P?" quanto "W?" se ela for a única célula do entorno,
                # ou seja, o único lugar possível para o Wumpus existir.
                if manipulaEntorno(mundo, i, j, ["W?", "P?"], "c") == 1:
                    manipulaEntorno(
                        mundo, i, j, ["W?", "P?"], "s", "W")
            if ("B" in mundo[i][j]) and (manipulaEntorno(mundo, i, j, ["P?"], "c") == 1)\
                    and (manipulaEntorno(mundo, i, j, ["P"], "c") == 0):
                manipulaEntorno(mundo, i, j, ["P?"],
                                "s", "P", "W?")
                # Deduz existência do poço em células do entorno que contém tanto
                # "P?" quanto "W?", se ela for a única célula do entorno,
                # ou seja, o único lugar possível para o poço existir.
                if manipulaEntorno(mundo, i, j, ["W?", "P?"], "c") == 1:
                    manipulaEntorno(
                        mundo, i, j, ["W?", "P?"], "s", "P")

            # Adiciona coordenadas da célula à lista de salas livres se ela for uma sala
            # livre.
            if "L" in mundo[i][j]:
                salaslivres.append([i, j])
            # Adiciona coordenadas da célula à lista de salas potencialmente livres se ela
            # estiver marcada como potencialmente livre e se houver uma sala visitada
            # vizinha.
            if "L?" in mundo[i][j] and manipulaEntorno(mundo, i, j, "V", "c"):
                salaspotencialmentelivres.append([i, j])
            # Adiciona coordenadas da célula à lista de casas com Wumpus se ela estiver
            # marcada com Wumpus.
            if "W" in mundo[i][j]:
                listadewumpus.append([i, j])
            # Adiciona coordenadas da célula à lista de casas com possíveis Wumpuses
            # se ela estiver marcada com possibilidade de Wumpus
            # e não estiver marcada com possível poço.
            # Essa lista será utilizada com uma estratégia específica.
            if "W?" in mundo[i][j] and "P?" not in mundo[i][j]:
                possiveiswumpus.append([i, j])

            # Adiciona informações do mundo compartilhado ao mundo somente
            # se a ação C foi utilizada na rodada anterior.
            if usacompartilhado == 1:
                # Quando a célula do mundo está vazia ou contém possibilidade de poço ou Wumpus,
                # e já não possui "L?",
                # limpa célula e adiciona as marcações "V" e "L" como marcações "L?" para
                # que o personagem explore por conta própria. O intuito é de abrir
                # possibilidades de caminhos não explorados.
                if ((mundo[i][j] == []) or ("W?" in mundo[i][j]) or ("P?" in mundo[i][j]))\
                        and (("V" in mundoCompartilhado[i][j]) or ("L" in mundoCompartilhado[i][j]))\
                        and ("L?" not in mundo[i][j]):
                    mundo[i][j].clear()
                    mundo[i][j].append("L?")

    # Se o mapa foi atualizado, retorna a checagem de compartilhamento
    # ao valor inicial
    if usacompartilhado == 1:
        usacompartilhado = 0


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, \
        usacompartilhado, compartilhou, instrucoes, salaslivres, \
        salaspotencialmentelivres, listadewumpus, possiveiswumpus, tempersonagem
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
    # acao = input("Digite a ação desejada (A/D/E/T/C): ")

    # ATENÇÃO: a atualizacao abaixo está errada!!!
    # Não checa se o movimento foi possível ou não... isso só dá para
    # saber quando chegar uma percepção nova (a percepção "I"
    # diz que o movimento anterior não foi possível).
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

    """
    Aplica estratégias de jogo, seguindo uma versão desse diagrama simplificado:
    * Tem personagem para compartilhar com: compartilha com a personagem
    * Não tem personagem para compartilhar com:
        * Passos ja foram definidos por uma estratégia: segue a estratégia
        * Passos não foram definidos por uma estratégia: define uma estratégia e à segue
            * Não tem flecha:
                * Se tem livre: acha caminho até primeiro livre da lista
                * Se não ou não foi possível, mas tem L?: acha caminho até ele
                * Se não ou não foi possível: estratégia de rotação, resetando a variável de compartilhamento.
            * Tem flecha:
                * Se tem wumpus: acha caminho até ele, substitui último comando por atira
                * Se não ou não foi possível, mas tem livre: acha caminho até o primeiro da lista possível
                * Se não ou não foi possível, mas tem L?: acha caminho até ele se possível
                * Se não ou não foi possível, mas tem W? e não tem P?: acha caminho até ele, substitui último comando por atira.
                * Se não ou não foi possível: estratégia de rotação, resetando a variável de compartilhamento.
    Estratégia de achar caminho: anda até a célula de forma segura.
    Estratégia de rotação: na impossibilidade de garantir um movimento seguro, rotaciona no mesmo lugar,
    na esperança de que outro jogador achará a personagem para que seja possível compartilhar informações.
    """
    # Compartilha informação se há outro personagem na sala e ainda
    # não se compartilhou informação nessa sala.
    # O motivo dessa condição é evitar ficar preso no mesmo local.
    if (tempersonagem) and (compartilhou == False):
        acao = "C"
        # Coloca valor em usacompartilhado para que o mundo seja
        # atualizado no próximo uso da função percepção.
        usacompartilhado = True
        # Muda valor da variável para True, de modo que a personagem não
        # compartilhe enquanto estiver na mesma sala.
        compartilhou = True
    else:
        # Se não existem instruções a serem seguidas pela personagem,
        # tenta definí-las.
        if instrucoes == []:
            # Se possui flecha e há algum Wumpus definido, chama a estratégia de
            # matar Wumpus.
            if (nFlechas > 0) and (len(listadewumpus) > 0):
                instrucoes = mataWumpus(listadewumpus)
            # Se um caminho não foi achado e há salas livres, chama a estratégia
            # de andar até uma sala livre.
            if (instrucoes == []) and len(salaslivres) > 0:
                instrucoes = andaParaCelula(salaslivres)
            # Se um caminho não foi achado e há salas potencialmente livres,
            # chama a estratégia de andar até uma sala potencialmente livre.
            if (instrucoes == []) and len(salaspotencialmentelivres) > 0:
                instrucoes = andaParaCelula(salaspotencialmentelivres)
            # Se um caminho não foi achado, possui flecha e há um possível Wumpus,
            # chama a estratégia de matar possível Wumpus.
            if (instrucoes == []) and (nFlechas > 0) and (len(possiveiswumpus) > 0):
                instrucoes = mataWumpus(possiveiswumpus)
            # Se nenhuma possibilidade foi satisfeita, a
            # personagem rotaciona no lugar.
            if (instrucoes == []):
                acao = "E"
                # Permite que o personagem compartilhe após utilizar a estratégia
                # de rotacao.
                compartilhou = False
        # Se existem instruções a serem seguidas pela personagem,
        # executa a próxima instrução da lista e à remove, de forma que
        # no próximo turno a próxima instrução seja executada.
        # A condição é "if" para a executar instruções definidas nesse turno
        # ou em turno anteriores.
        if instrucoes != []:
            acao = instrucoes[0]
            del instrucoes[0]

    # Verifica se a ação existe
    assert acao in ["A", "D", "E", "T", "C"]
    # Atualiza posicao e orietnação do personagem de acordo com a ação.
    if acao == "A":
        posicao[0] = (posicao[0] + orientacao[0]) % N
        posicao[1] = (posicao[1] + orientacao[1]) % N
        # Reseta variável, dado que a personagem saiu da célula em que
        # compartilhou a informação.
        compartilhou = False
    if acao == "E":
        if orientacao[0] == 0:
            orientacao[1] = -orientacao[1]
        orientacao[0], orientacao[1] = orientacao[1], orientacao[0]
    if acao == "D":
        if orientacao[1] == 0:
            orientacao[0] = -orientacao[0]
        orientacao[0], orientacao[1] = orientacao[1], orientacao[0]
    return acao


def manipulaEntorno(matriz, i, j, conteudo, modo="a", conteudonovo='Erro', excecao=-1):
    """
    Atualiza a representação da matriz para as quatro casas vizinhas,
    realizando a operação de acordo com o parâmetro modo:
        "a" - modo adição: adiciona conteúdo às 4 casas vizinhas. Se o parâmetro
        excecao assumir valor True, adiciona valor somente às casas que não contenham
        algum valor.
        "r" - modo remoção: remove conteúdo das 4 casas vizinhas.
        "c" - modo contador: conta o número de casas vizinhas com o conteúdo e
        sem o conteúdo do parâmetro excecao, e retorna o valor.
        Considera somente os casos em que todos os elementos estão presentes.
        "s" - modo substituição: substitui todas as marcações das casas vizinhas
        que possuírem o conteúdo pelo conteúdo novo. Considera somente os casos
        em que todos os elementos estão presentes.
        "l" - modo listar: retorna uma lista de coordenadas das casas vizinhas
        que possuem o conteúdo.
    Se nenhum parâmetro modo for dado, utiliza-se "a" como padrão.
    O parâmetro conteudo deve ser uma lista. A operação é feita para cada item da lista.
    Se conteudonovo não for especificado para a operação de substituição,
    utiliza-se "Erro" como padrão.
    Se nenhum parâmetro excecao for dado, utiliza-se -1 como padrão.
    """
    # Verifica se o valor de modo é "a", "r", "c" ou "s".
    assert (modo == "a") or (modo == "r") or (
        modo == "c") or (modo == "s") or (modo == "l")
    # Define uma lista em que cada elemento é uma coordenada da casa vizinha,
    # para uso pelo modo "l"
    coordvizinhas = [[(i + 1) % N, j],
                     [(i - 1) % N, j],
                     [i, (j + 1) % N],
                     [i, (j - 1) % N]]
    # Define uma lista em que cada elemento é uma casa vizinha
    vizinhas = [matriz[(i + 1) % N][j],
                matriz[(i - 1) % N][j],
                matriz[i][(j + 1) % N],
                matriz[i][(j - 1) % N]]
    # Define um valor inicial para a lista de casas
    listadecasas = []
    # Define valor inicial do contador para correto funcionamento do laço.
    contador = 0
    # Itera pelas casas vizinhas, manipulando seu conteúdo.
    for k in vizinhas:
        # Define/reseta valor inicial de contador de item
        contadordeitem = 0
        for item in conteudo:
            # Adiciona conteúdo às casas vizinhas somente se
            # a casa atual não foi visitada, se o conteúdo já não está presente
            # nas casas vizinhas e se as casas vizinhas não possuem
            # alguma marcação definitiva tal como L, V, W, P, M, F, B.
            # Caso excecao possua valor True e a casa possua conteúdo,
            # não adiciona o valor a ela (PS: expressão representada por outra
            # equivalente).
            if modo == "a":
                if ("V" not in matriz[i][j])\
                        and (item not in k) and ("L" not in k)\
                        and ("V" not in k) and ("W" not in k) and ("P" not in k)\
                        and ("M" not in k) and ("F" not in k) and ("B" not in k):
                    k.append(item)
            # Remove conteúdo de casas vizinhas se o modo for "r", realizando
            # a verificação da existência de conteúdo antes de remover.
            elif (modo == "r"):
                if (item in k):
                    k.remove(item)
            # Incrementa o contador se a célula vizinha possui o conteúdo e
            # não possui a exceção. Considera-se implicitamente que o modo é "c".
            elif (item in k):
                if (excecao not in k):
                    contadordeitem += 1
            if contadordeitem == len(conteudo):
                # Incrementa o contador de conteúdo.
                contador += 1
                # Se o modo for "s", o conteúdo existir na célula vizinha, a
                # exceção não existir e a condição for verdadeira,
                # remove todas as marcações da célula
                # e adiciona o conteúdo novo.
                if (modo == "s") and (excecao not in k):
                    k.clear()
                    k.append(conteudonovo)
                # Se o modo for "l" e o conteúdo existir na célula vizinha,
                # adiciona as coordenadas da célula vizinha à lista de casas.
                elif modo == "l":
                    listadecasas.append(coordvizinhas[vizinhas.index(k)])

    # Retorna contador se a função está em modo c.
    if (modo == "c"):
        return contador
    # Retorna lista de casas se a função está em modo l.
    elif (modo == "l"):
        return listadecasas


def marcaCaminho(i, j):
    """
    Marca matriz com distâncias de cada célula marcada à célula de coordenadas i, j,
    e retorna a matriz.
    A matriz é equivalente à matriz mundo.
    O propósito dessa função é ser usada pela função achaCaminho().
    """
    global mundo
    # Cria matriz equivalente à matriz mundo
    matriz = []
    for k in range(N):
        linha = []
        for l in range(N):
            linha.append([0])
        matriz.append(linha)
    # Coloca valor 1 na célula que se quer obter distâncias de.
    matriz[i][j] = [1]
    # Itera por todas as células da matriz
    for k in range(N):
        for l in range(N):
            # Marca com -1 as células da matriz cuja célula correspondente no mundo
            # não sejam um caminho viável (ou seja, não estejam marcadas com "V").
            if "V" not in mundo[k][l] and matriz[k][l] != [1]:
                matriz[k][l] = [-1]
    # Define valor inicial de contador para o correto funcionamento do laço.
    # A função do contador é fazer com que esse processo de marcação
    # seja realizado somente ao redor de células que contenham o seu número.
    # Ele também determina quantas vezes o laço será repetido.
    contador = 1
    # O laço só terminará quando todos os incrementos foram feitos. Para isso,
    # utiliza-se o contador, dado que um caminho pode ter no máximo N * N células, e da mesma
    # forma, são realizados no máximo N * N marcações ao redor das célula.
    while contador != N * N:
        # Itera por todas as células da matriz
        for k in range(N):
            for l in range(N):
                # Para as células que são caminhos viáveis, adiciona distância às casas
                # vizinhas que já não contenham um valor, utilizando a função manipulaEntorno
                # em modo adição. A distância adicionada é equivalente ao valor contido na célula + 1.
                if matriz[k][l] != [-1]:
                    # Verifica se o processo deve ser realizado ao redor da célula ou não.
                    if matriz[k][l][0] == contador:
                        manipulaEntorno(
                            matriz, k, l, [0], "s", matriz[k][l][0] + 1, excecao=-1)
        # Incrementa contador
        contador += 1
    return matriz


def achaCaminho(a, b, orientacaoinicial, i, j, orientacaofinal=None):
    """
    Acha caminho da célula (a,b) para a célula de coordenadas (i, j) no mundo, considerando
    orientação inicial, e retorna lista contendo o caminho. Orientacao final é considerada
    se houver.
    Utiliza-se a matriz gerada pela função marcaCaminho.
    """
    global N
    matriz = marcaCaminho(i, j)
    # Define a lista de passos para o correto funcionamento do laço.
    # Essa lista receberá provisoriamente os passos
    # 0, 1, 2, 3, indicando respectivamente os movimentos dentro da matriz de
    # cima, baixo, esquerda e direita.
    listadepassos = []
    # Cria lista de bifurcacoes. Um primeiro elemento é definido para evitar
    # erros na operações.
    # Cada elemento da lista segue o formato [a, b, lista de caminhos, numero de passos dados desde
    # a última bifurcação]
    listadebifurcacoes = [[-1, -1, [[-1]], -1]]
    # Cria lista que será utilizada para armazenar as instruções finais da personagem.
    listadeinstrucoes = []

    # Continua no laço enquanto não for achado caminho
    while matriz[a][b] != [1]:
        # Define lista de caminhos
        caminhos = manipulaEntorno(matriz, a, b, [matriz[a][b][0] - 1], "l")
        # Se não há caminhos para serem seguidos (caminho sem saída),
        # retorna à última bifurcação, realizando as operações necessárias.
        if len(caminhos) == 0:
            # Remove as coordenadas do caminho seguido da lista de caminhos da última bifurcação
            del listadebifurcacoes[-1][2][0]
            # Remove da lista de passos os caracteres correspondentes aos passos
            # dados desde a última bifurcação.
            listadepassos = listadepassos[0:len(
                listadepassos) - listadebifurcacoes[-1][3]]
            # Reseta o número de passos dados desde a última bifurcação para 0
            listadebifurcacoes[-1][3] = 0
            # Remove última bifurcação da lista de bifurcações se todos seus caminhos já foram explorados
            if len(listadebifurcacoes[-1][2]) == 0:
                del listadebifurcacoes[-1]
            # Retorna string vazia se não existem mais bifurcações, ou seja, se todos os caminhos
            # foram explorados e não se chegou à célula de coordenadas (i, j)
            if len(listadebifurcacoes) <= 1:
                return []
            # Retorna à bifurcação anterior
            a, b = listadebifurcacoes[-1][0], listadebifurcacoes[-1][1]

        # Se há caminhos para serem seguidos, segue pelo primeiro da lista, realizando
        # as operações necessárias.
        else:
            # Se há mais de um caminho, adiciona a bifurcação à lista de bifurcações.
            if len(caminhos) > 1:
                listadebifurcacoes.append([a, b, caminhos, 0])

            # Incrementa o número de passos dados desde a última bifurcação
            listadebifurcacoes[-1][3] += 1

            # Adiciona o passo dado à lista de passos de acordo com as condicionais:
            # Checa se o passo dado é na direção 0 (para cima)
            if (caminhos[0][0] - a) % 5 == 4:
                listadepassos.append(0)
            # Checa se o passo dado é na direção 1 (para direita)
            elif (caminhos[0][1] - b) % 5 == 1:
                listadepassos.append(1)
            # Checa se o passo dado é na direção 2 (para baixo)
            elif (caminhos[0][0] - a) % 5 == 1:
                listadepassos.append(2)
            # O passo dado será na direção 3 (para esquerda)
            else:
                listadepassos.append(3)

            # Muda a posição atual para a célula do caminho, que corresponde aos valores de a e b.
            a, b = caminhos[0][0], caminhos[0][1]

            # Deleta o caminho seguido
            del caminhos[0]

    # Terminado o laço, o caminho foi encontrado.
    # Processa a lista de passos, convertendo-a para instruções do jogo.
    # Itera pela lista de passos, formada pelos comandos 0, 1, 2, 3.
    for k in range(1, len(listadepassos)):
        # Obtém valor que determinará qual é a instrução de jogo correspondente.
        # 0 corresponde a A
        # 1 corresponde a D
        # 2 corresponderia a voltar para a casa anterior, o que não ocorrerá.
        # 3 corresponde a E
        valor = (listadepassos[k] - listadepassos[k - 1]) % 4
        # Marca instruções de acordo com a variável valor
        # "A" será adicionado em todos os três casos possíveis.
        if valor != 0:
            listadeinstrucoes = listadeinstrucoes + interpretaRotacao(valor)
        listadeinstrucoes = listadeinstrucoes + ["A"]
    # Converte a orientação inicial da personagem para o sistema 0, 1, 2, 3
    orientacaoinicial = converteOrientacao(orientacaoinicial)
    # Define variável que será usadas para determinar quais instruções a personagem
    # deve realizar de forma a ajustar suas orientações inicial.
    inicial = (listadepassos[0] - orientacaoinicial) % 4
    # Adiciona instruções para a correção da orientação inicial da personagem
    # E adiciona a instrução andar correspondente ao primeiro passo
    listadeinstrucoes = (interpretaRotacao(inicial)) + \
        ["A"] + listadeinstrucoes

    # Se orientacaofinal foi definida, adiciona instruções de forma a corrigir a
    # orientação final.
    if orientacaofinal is not None:
        # Converte a orientação final da personagem para o sistema 0, 1, 2, 3
        orientacaofinal = converteOrientacao(orientacaofinal)
        # Define variável que será usadas para determinar quais instruções a personagem
        # deve realizar de forma a ajustar suas orientações final.
        final = (orientacaofinal - listadepassos[-1]) % 4
        # Adiciona instruções para a correção da orientação final da personagem
        listadeinstrucoes = listadeinstrucoes + interpretaRotacao(final)

    # Retorna as instruções.
    # Prefere-se retorná-las à modificar a variável global instruções, por motivos
    # de implementação.
    return listadeinstrucoes


def converteOrientacao(orientacao):
    """
    Converte coordenadas de orientação para o sistema 0, 1, 2, 3.
    0 <=> cima
    1 <=> direita
    2 <=> baixo
    3 <=> esquerda

    """
    # Realiza a conversão
    if orientacao[0] == -1:
        orientacao = 0
    elif orientacao[1] == 1:
        orientacao = 1
    elif orientacao[0] == 1:
        orientacao = 2
    else:
        orientacao = 3
    # Retorna o valor
    return orientacao


def interpretaRotacao(valor):
    """
    Interpreta valor que corresponde à mudança de orientação, retornando uma lista com sua
    as instruções correspondentes.
    0 diz que não é preciso realizar a rotação, e não retornará nada.
    1 corresponde a D
    2 corresponde a uma rotação para o lado oposto. É retornado ["D", "D"].
    3 corresponde a E
    """
    if valor == 0:
        return []
    elif valor == 1:
        return ["D"]
    elif valor == 2:
        return ["D", "D"]
    elif valor == 3:
        return ["E"]


def andaParaCelula(lista):
    """
    Procura um caminho para célula na lista.
    """
    # Variáveis utilizadas pela função
    global posicao, orientacao
    # Itera por cada célula da lista, procurando um caminho até ela pela
    # chamada da função achaCaminho, que retorna [] se o caminho não for encontrado.
    # Retorna o caminho, quer ele tenha sido encontrado ou não
    for celula in lista:
        caminho = achaCaminho(
            posicao[0], posicao[1], orientacao, celula[0], celula[1])
        if caminho != []:
            return caminho
    return []


def mataWumpus(listadewumpus):
    """
    Cria lista de instruções correspondentes à
    andar até célula vizinha ao wumpus ou possível wumpus e atira em sua direção.
    """
    # Procura caminho até o wumpus ou possível wumpus
    caminho = andaParaCelula(listadewumpus)
    # Remove última instrução de andar, o personagem estará olhando
    # na direção do Wumpus.
    del caminho[-1]
    # Adiciona instrução de atirar.
    caminho.append("T")
    # Adiciona instrução de andar, para que o personagem ocupe a posição após o tiro.
    caminho.append("A")
    return caminho
