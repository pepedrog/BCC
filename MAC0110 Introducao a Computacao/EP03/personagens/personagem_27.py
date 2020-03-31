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

global acaoAnterior

global percepcaoAnterior


def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, acaoAnterior
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
    acaoAnterior = False


def nova_posicao(posicao, direcao):
    x = (posicao[0] + direcao[0]) % len(mundo)
    y = (posicao[1] + direcao[1]) % len(mundo)
    return [x, y]


def tem_intersecao(subconjunto, conjunto):
    """
    Returns:
        True caso `subconjunto` seja subconjunto de conjunto.
    """
    for item in subconjunto:
        if item in conjunto:
            return True

    return False


def valida_marcador(posicao, marcador):
    x, y = posicao
    if marcador.endswith('?'):
        if 'L' in mundo[x][y] or marcador[:-1] in mundo[x][y]:
            return False
    if marcador in mundo[x][y] or 'M' in mundo[x][y]:
        return False

    return True


def marcar_em_volta(posicao, marcador):
    global mundo

    em_volta = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    for item in em_volta:
        x, y = nova_posicao(posicao, item)

        if not valida_marcador([x, y], marcador):
            continue

        if (marcador == 'L' or marcador == 'V') and marcador not in mundo[x][y]:
            mundo[x][y].append(marcador)
        else:
            elegivel = not tem_intersecao(['L', 'V'], mundo[x][y])
            if elegivel and marcador not in mundo[x][y]:
                # se lugar ainda é desconhecido e não possui marcador
                mundo[x][y].append(marcador)


def marcar_em_cima(posicao, marcador):
    x, y = posicao

    if not valida_marcador(posicao, marcador):
        return

    if marcador == 'M':
        mundo[x][y] = ['M']
    elif marcador == 'L' or marcador == 'V':
        if 'M' not in mundo[x][y]:
            mundo[x][y] = ['V', 'L']
    elif marcador not in mundo[x][y]:
        mundo[x][y].append(marcador)


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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, acaoAnterior
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    percepcaoAnterior = percepcao

    if acaoAnterior == 'A':
        proxima_posicao = nova_posicao(posicao, orientacao)

    if 'I' in percepcao:
        # não anda e marca muro
        x, y = proxima_posicao
        marcar_em_cima(proxima_posicao, 'M')
    else:
        print(posicao)
        # executa a ação de andar
        if acaoAnterior == 'A':
            posicao = proxima_posicao
        marcar_em_cima(posicao, 'V')

        x, y = posicao

        if len(percepcao) == 0:
            marcar_em_volta(posicao, 'L')
        else:
            for percepcao_item in percepcao:
                indica_em_volta = ''
                if percepcao_item == 'F':
                    marcar_em_volta(posicao, 'W?')
                    marcar_em_cima(posicao, 'F')
                elif percepcao_item == 'B':
                    marcar_em_volta(posicao, 'P?')
                    marcar_em_cima(posicao, 'B')
                elif not tem_intersecao(['I', 'U'], percepcao):
                    pass  # é um jogador

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
        # mundo[pos[0]][pos[1]] = ["V"]
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, acaoAnterior
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
    acao = input("Digite a ação desejada (A/D/E/T/C): ")
    acao = acao.upper()
    # acao = 'A'

    # ATENÇÃO: a atualizacao abaixo está errada!!!
    # Não checa se o movimento foi possível ou não... isso só dá para
    # saber quando chegar uma percepção nova (a percepção "I"
    # diz que o movimento anterior não foi possível).
    pos = posicao
    ori = orientacao
    acaoAnterior = acao
    if acao=="E":
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
    elif acao=="D":
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
    elif acao == 'C':
        # verifica se podemos confiar no mapa
        # para isso, não deve haver discrepância entre info dada como certa
        for i in range(len(mundo)):
            for j in range(len(mundo[0])):
                info_compart = mundoCompartilhado[i][j]
                for item in info_compart:
                    import pdb; pdb.set_trace()
                    marcar_em_cima([i, j], item)

    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

    assert acao in ["A","D","E","T","C"]
    return acao
