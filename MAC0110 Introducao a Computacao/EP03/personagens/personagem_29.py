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

global salas_livres
"""
Guarda as posições [m, n] das salas livres e não visitadas
"""

global tempo_esperado
"""
Guarda quanto tempo a personagem já esperou alguém aparecer para compartilhar
informações antes de correr riscos. Também serve para armazenar há quanto tempo
a personagem está disposta a correr riscos. Ela vai passar 10 rodadas esperando
e 10 rodadas correndo riscos, alternadamente.
"""

global outras_personagens
"""
Guarda informações de onde outras personagens foram encontradas. A cada vez
que uma personagem é encontrada de novo, sua posição é atualizada.
Convencion-se que essa variável é uma lista de listas de dois elementos:
o nome da personagem e a lista com as duas coordenadas da última posição
em que ela foi encontrada
"""

global atirei
"""
Variável booleana que permanece False todo o tempo, exceto na rodada em que
a personagem atira a flecha. É usada para determinar se o Wumpus morreu ou não
"""

global quantos_viram
"""
Essa variável guarda quantas personagens viram quais perigos. Se muita gente
observou um perigo, a chance dele ser real é maior. Ver menor_risco2()
"""

global revisitadas
"""
Variável que guarda algumas informações referentes a uma estratégia  de revsisitar
Ver função revisitar(). Trata-se de uma lista com as salas com 'V' já re-visitadas
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
    global N, mundo, posicao, orientacao, encontrou_muro, salas_livres, tempo_esperado, outras_personagens, atirei, quantos_viram, revisitadas
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
    salas_livres = []
    tempo_esperado = 0
    outras_personagens = []
    atirei = False
    revisitadas = []
    quantos_viram = []


    # Inicializa quantos_viram, que armazena quantas personagens viram cada letra
    # nessa representação do mundo. Cada elemento da matriz é da forma

    quantos_viram = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        quantos_viram.append(linha)

    for l in ['W?', 'W', 'P?', 'P']:
        for i in range(N): 
            for j in range(N) : 
                quantos_viram[i][j].append([l, []])



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
    global mundo, posicao, orientacao, salas_livres, revisitadas
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado).

    # ------------------------------------------------------------------- #

    if "I" in percepcao:
        mundo[posicao[0]][posicao[1]] = ["M"] # sobrescreve todo resto
        posicao = posicao_anterior(posicao)

    pos = posicao
    ori = orientacao

    # Adiciona e remove salas com L de todo o mundo da lista salas_livres
    atualiza_salas_livres()
    # se tivermos certeza da posição de um wumpus ou poço, queremos anotar:
    identificar_wumpus_ou_poco()
    # Adicionar informações de mundo compartilhado à minha representação
    incorpora_mundo_compartilhado(percepcao)
    # Adiciona personagens à lista outras_personangens
    conhece_personagem(percepcao)
    # Confere se eu matei um wumpus
    conferir_morte_de_wumpus(percepcao)
    # Confere se eu revisitando a função revisitar())
    if revisitadas != []:
        if pos in revisitadas[0]:
            revisitadas[1][revisitadas[0].index(pos)] = True


    # Adiciona "W?" ou "P?" às salas ao redor
    perigo = {"F":"W?", "B": "P?"}
    for indicio in perigo:
        if indicio in percepcao:
            adiciona_ao_mundo(pos, indicio)
            marcar_salas_adjacentes(pos, perigo[indicio], ["L", "V", "M", "W", "P"])

    # Se eu não estou sentindo fedor ou brisa ao redor, retira o perigo
    # correspondente ao redor
    for indicio in perigo:
        if indicio not in percepcao:
            remover_de_salas_adjacentes(pos, perigo[indicio])
            
    # Se não houver perigo, marcamos L
    # Note que se houvesse perigo, teríamos acabado de marcar 'W?'
    # ou 'P?' nos arredores, e portanto o parametro 'exceto' cumpre o
    # papel de não marcar L em salas perigosas
    marcar_salas_adjacentes(pos, "L", ["M", "V", "W?", "P?", "W", "P"])
        
    #Adiciona V a essa sala e retira os desnecessários
    adiciona_ao_mundo(pos, 'V')
    for letra in ['L', 'W?', 'W', 'P', 'P?']:
        remove_do_mundo(pos, letra)

    # De novo, pois pode ser necessário. Já temos novas informações
    atualiza_salas_livres()
    identificar_wumpus_ou_poco()
    incorpora_mundo_compartilhado(percepcao)

    # ------------------------------------------------------------------- #

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código

    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # elimine o teste abaixo quando tiver corrigido o bug de movimentação...
        if "I" in percepcao:
            print("Você bateu num muro e voltou para a posição anterior")
            # print("Você bateu num muro e talvez não esteja mais na sala em que pensa estar...")
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
                print("" ,end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

def agir(): 
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """

    global salas_livres, outras, personagens, nFlechas, posicao
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

    acao = ''
    pos = posicao

    # 0. Inicializa variáveis
    compartilhar = False
    matar_wumpus = False
    livres = False
    revisitando = False

    for el in outras_personagens:
        # se outra personagem estiver na minha posição, compartilhar
        if el[1] == pos:
            compartilhar = True
    pos_wumpus = achar_salas_com('W')

    a2 = None
    if len(pos_wumpus) > 0 and nFlechas > 0:
        a2 = acao_na_sala(pos_wumpus[0], 'T')
    a3 = None
    if salas_livres != []:
        a3 = ir_para(mais_perto(salas_livres))
    a4 = revisitar()
    
    ### 1. Compartilhar ###
    if compartilhar:
        acao = 'C'

    ### 2. Matar Wumpus ###
    elif a2 != None:
        #ir até onde wumpus está
        matar_wumpus = True
        acao = a2
        if acao == 'T':
            atirei == True

    ### 3. Ir para próxima sala livre ###
    elif a3 != None: 
        livres = True
        acao = a3

    ### 4. Revisita as salas (ficar dando voltas)

    elif a4 != None:
        revisitando = True
        acao = a4


    ### 5. Por último, corre riscos
    else:
        acao = correr_riscos()

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    if __DEBUG__:
        if compartilhar:
            print('Compartilhando informações: C')
        elif matar_wumpus:
            print('Atrás de um Wumpus!:', acao)
        elif livres:
            print('Indo para a sala livre mais perto:', acao)
        elif revis:
            print('Dando voltas por aí:', acao)
        else:
            print('indo para menor risco:', acao)

        print('Próxima acao sugerida:', acao)
        while True:
            a = input("Digite enter para a próxima ação sugerida ou digite a sua:\n")
            if a in ["A","D","E","T","C"]:
                acao = a
                break
            # elif a != '':
            #     try:
            #         exec(a)
            #     except Exception as error:
            #         print(str(error))
            else:
                break

        assert acao in ["A","D","E","T","C"]
        # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

    assert acao in ["A","D","E","T","C"]
    atualiza_pos_ori(acao)
    return acao

###### FUNÇÕES AUXILIARES ##########################################






# ---- Funções relativas a agir ---------------------------------- #





def atualiza_pos_ori(acao):
    '''
    A partir da acao, determina as novas posicao e orientacao da personagem
    '''
    global posicao
    global orientacao
    global mundo

    pos = posicao
    ori = orientacao
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

def correr_riscos():
    '''
    Devolve a acao correspondente ao protocolo de correr riscos:
    Se não houver salas livres, queremos esperar 20 rodadas até alguém nos
    encontrar. Se até lá ninguém nos encontrar, vamos correr riscos durante
    5 rodadas.
    '''
    global tempo_esperado


    # 1. Espera para ver se algo chega a você
    if tempo_esperado >= 60:
        tempo_esperado = 0
    if tempo_esperado <= 50: 
        tempo_esperado += 1
        return 'E'
    else:
        # 2. Tenta dar voltas de novo
        ans = revisitar()
        if ans != None:
            return ans

        tempo_esperado += 1
        # 3. Arrisca as salas inseguras menos perigosas
        ans = ir_para(menor_risco())
        if ans != None and ans != []:
            return ans
        # 4. Se não há salas livres nem W? ou P?, vamos tentar
        #    ir na sala com o 'P' menos observado. Quem sabe
        #    alguma outra personagem não marcou isso por engano
        ans = ir_para(menor_risco2(achar_salas_com('P')))
        if ans != None and ans != []:
            return ans

        # 5. Se nada der certo, vamos direto ao assunto:
        return 'A'


def menor_risco():
    '''
    Determina, a partir das informações do mundo, qual é a sala não segura
    menos arriscosa. Seja o número de P?'s ou W?'s em volta de uma sala
    dado por p(sala). O critério aqui será escolher a sala não segura
    S em que a soma de p(sala) de todas as salas ao redor de S seja a maior
    Se não houver W? ou P?, devolve lista vazia
    '''


    # Vamos escolher a melhor, depois juntar todas do mesmo valor que ela
    # numa lista.
    ans = [[], []]
    letra = ['P?', 'W?']
    for i in range(2):
        lista = achar_salas_com(letra[i])
        if len(lista) > 0:
            ans[i] = lista[0]

        # guarda a sala com o maior 'criterio' (ver acima) em ans
        for p in lista:
            if criterio(p, letra[i]) >  criterio(ans[i], letra[i]):
                ans[i] = p[:]

    # Se não houver 'P?' ou 'W?' no mundo nem L, só nos restaria o suicídio...
    if ans[0] == [] and ans[1] == []:
        return suicidio()


    if criterio(ans[0], letra[0]) > criterio(ans[1], letra[1]):
        melhor =  ans[0]
        l = letra[0]
    else:
        melhor = ans[1]
        l = letra[1]

    # Junta todos os melhores na lista opcoes
    opcoes = []
    ans = [[], []]
    for i in range(2):
        lista = achar_salas_com(l)
        if len(lista) > 0:
            ans[i] = lista[0]

        # guarda as salas com o mr 'criterio' (ver acima) em ans
        for p in lista:
            if criterio(p, l) == criterio(melhor, l):
                opcoes.append(p)
    
    return menor_risco2(opcoes)
    
def menor_risco2(lista):
    '''
    Outro critério para menor risco também pode ser baseado em quantas pessoas
    observaram determinado perigo. Quanto mais gente observou um perigo, mais
    chance de ser real ele é.
    Essa função recebe uma lista de posições e, de acordo com esse critério,
    devolve uma daquelas com menor risco
    '''

    # Como só tem uma outra personagem em mundo.py da parte A do exercício,
    # não deu pra testar muito essa função, nem se ela funciona nem se
    # ela de fato ajuda

    global quantos_viram, mundo
    q = quantos_viram

    ans = lista[0]
    for p in lista:
        for i in range(4):
            if len(q[p[0]][p[1]][i]) > len(q[ans[0]][ans[1]][i]):
                ans = p

    return ans

def criterio(pos, letra):
    '''
    Devolve a soma dos números de salas ao redor das adjacências de pos
    que contem letra. Se receber lista vazia, devolve 0
    '''
    global mundo

    ans = 0

    if pos == []:
        return 0
    r = {'W?': 'F', 'P?': 'B'}
    adj = adjacentes(pos)
    for p in adj:
        if r[letra] in mundo[p[0]][p[1]]:
            ans += numero_de_salas_ao_redor_com(p, letra)
    return ans

def numero_de_salas_ao_redor_com(pos, letra):
    '''
    Devolve o número de salas ao redor de 'pos' que contem 'letra'
    '''
    global mundo

    adj = adjacentes(pos)
    ans = 0
    for p in adj:
        # Também conta se houver um 'P' e não só um 'P?'
        if letra in mundo[p[0]][p[1]] or letra[0] in mundo[p[0]][p[1]]:
            ans += 1
    return ans

def revisitar():
    '''
    Protocolo de espera ativa: ficar andando por onde já foi visitado para
    ver se encontra algo 
    '''
    global revisitadas, posicao
    pos = posicao

    #  Percorrer todas as salas com V de novo, para ver se algo de novo aparece
    #  (por exemplo, alguém cuja estratégia é ficar esperando)

    # Revisitadas uma lista que contém duas listas. Uma com todas as
    # salas já visitadas, outra com uma booleana indicando se essa
    # sala já foi revisitada ou não

    # criamos uma lista nova?
    if len(revisitadas) == 0 or revisitadas[0] != achar_salas_com('V'):
        revisitadas.append(achar_salas_com('V'))
        revisitadas.append([])
        for i in range(len(revisitadas[0])):
            revisitadas[1].append(False)

    opcoes = []
    for i in range(len(revisitadas[0])):
        if not revisitadas[1][i] and revisitadas[0][i] != pos:
            opcoes.append(revisitadas[0][i])
    
    if opcoes != []:
        return ir_para(mais_perto(opcoes))
    





# ---- Funções relativas ao planejamento ------------------------ #





def identificar_wumpus_ou_poco():
    ''' Procura, a partir das informações conhecidas do mundo, uma sala
    onde seja certa a presença de um wumpus ou poco e adiciona essa informação
    a mundo.
    '''
    global mundo
    global N

    ref = {'W':'F', 'P':'B'}

    # Se tiver um fedor e três salas livres ao redor, então a quarta deve ser um wumpus
    for l in ['W', 'P']:
        for i in range(N):
            for j in range(N):
                if ref[l] in mundo[i][j]:

                    contem = []
                    adj = adjacentes([i, j])
                    for sala in adj:
                        # Se já fez isso aqui antes, não precisa mais
                        if l in mundo[sala[0]][sala[1]]:
                            contem = []
                            break
                        if l + '?' in mundo[sala[0]][sala[1]]:
                            contem.append(sala)
                    if len(contem) == 1:
                        mundo[contem[0][0]][contem[0][1]].remove(l + '?')
                        mundo[contem[0][0]][contem[0][1]].append(l)

def conferir_morte_de_wumpus(percepcao):
    '''
    Se eu matei um wumpus, devo remover sua representação
    '''
    global posicao, orientacao, atirei, mundo
    pos = posicao
    ori = orientacao

    if not atirei or 'U' not in percepcao:
        return

    f = [pos[0] + ori[0] % N, pos[1] + ori[1] % N]
    if 'W' in mundo[f[0]][f[1]]:
        remove_do_mundo(f, 'W')
        remove_do_mundo(f, 'W?')

    atirei = False

def incorpora_mundo_compartilhado(percepcao):
    '''
    Incorpora à minha representação de mundo aquilo que foi compartilhado comigo
    (filosófico)
    '''
    global N
    global mundoCompartilhado

    nome = '4603521'
    for l in percepcao:
        if l not in ['F', 'B', 'I', 'U', 'W', 'W?', 'P', 'P?', 'M', 'V', 'L']:
            nome = l

    ref = {'B': 'P', 'F': 'W', 'B?': 'P?', 'F?': 'W?'}
    for i in range(N):
        for j in range(N):

            # Primeiro, os que entram substituindo outras letras:
            for l in ['L', 'M', 'V']:
                if l in mundoCompartilhado[i][j]:
                    adiciona_ao_mundo([i, j], l, ['L', 'M', 'V'], nome)
                    for r in ['W?', 'P?']:
                        remove_do_mundo([i, j], r)

            for l in ['W?', 'P?', 'B', 'P']:
                if l in mundoCompartilhado[i][j]:
                    adiciona_ao_mundo([i, j], l, ['L', 'V', 'M', l[0], l + '?'], nome)
                    # l[0] na exceção garante que não teremos algo como "W?W"

            # Eu só confio em mim mesmo para gastar minha flecha
            # O Wumpus pode ter morrido
            for l in ['F', 'W']:
                if l in mundoCompartilhado[i][j]:
                    adiciona_ao_mundo([i, j], l, ['L', 'V', 'M', l+'?'], nome)

            # Depois, conferimos se a outra personagem de fato marcou o que
            # se pode presumir com as informações dela
            for l in ref:
                if l in mundoCompartilhado:
                    for s in adjacentes([i, j]):
                        # Deve ir '?' de qualquer jeito
                        adiciona_ao_mundo(s, ref[s][0]+'?', ['L', 'M', 'V', ref[s], ref[s][0]], nome)
    atualiza_salas_livres()

def conhece_personagem(percepcao):
    '''
    outras_personagens é uma lista cujos elementos são listas cujo primeiro
    elemento é o nome da outra personagem e o segundo elemento é a posição
    dela. Exemplo: [['Dummy', [3, 4]], ['4603521', [0, 0]]]
    '''
    global outras_personagens
    global posicao
    pos = posicao

    for el in percepcao:
        if el not in ['F', 'B', 'I', 'U', 'W', 'W?', 'P', 'P?', 'M', 'V', 'L']:
            personagem_conhecida = False
            for i in range(len(outras_personagens)):
                if el == outras_personagens[i][0]:
                    outras_personagens[i][1] = pos
                    personagem_conhecida = True
            if not personagem_conhecida:
                outras_personagens.append([el, pos])

    # Se estou aqui e a personagem não, retira ela da lista, pois ela não
    # está mais onde eu achava que estava.
    for p in outras_personagens:
        if p[1] == pos and p[0] not in percepcao:
            outras_personagens.remove(p)






# ---- Funções relativas ao deslocamento ------------------------ #





def acao_na_sala(sala, acao):
    ''' Recebe uma lista de dois elementos, contendo a posicao para
    onde fazer uma ação a uma sala.
    Devolve a próxima ação que deve ser tomada para tal ('E', ou 'D', ou a
    dada como parâmetro)'''
    global orientacao
    global posicao
    ori = orientacao
    pos = posicao

    if sala not in adjacentes(pos):
        return ir_para(sala)

    sala = orientacao_entre_salas(pos, sala)

    # As orientações em ref giram da esquerda para a direita
    ref = [[1, 0], [0, -1], [-1, 0], [0, 1]]
    assert sala in ref

    # já está na posição certa
    if sala == ori:
        return acao

    # se a próxima sala estiver à direita da orientação atual...
    elif sala == ref[(ref.index(ori) + 1)%4]:
        return 'D'
    else:
        # tanto se estiver à esquerda quanto se estiver atrás
        return 'E'

def ir_para(sala):
    '''recebe a posição de uma sala e devolve a próxima ação necessária
    para chegar lá passando só por sala livres ou visitadas. Se não houver,
    devolve None. Se receber um None ou [], também devolve None'''
    global posicao
    pos = posicao

    # vamos implementar sistema semelhante ao do exercício do rato
    # https://www.ime.usp.br/~macmulti/exercicios/extra/index.html

    if sala == [] or sala == None:
        return None

    d = tabela_de_distancias_caminhaveis(sala)

    # Se a posição atual não foi marcada,
    if d[pos[0]][pos[1]] == -1:
        # Então não há caminho seguro possível:
        return None


    adj = adjacentes(pos)
    for s in adj:
        if d[s[0]][s[1]] < d[pos[0]][pos[1]] and d[s[0]][s[1]] != -1 :
            return acao_na_sala(s, 'A')

def mais_perto(lista):
    ''' Recebe uma lista de posicoes e devolve a posição de uma das que
    estiver à menor distância caminhável da posição atual do jogador,
    onde caminhável significa que só passa por salas livres ou visitadas'''
    global posicao
    assert lista != []

    # inicializa variável 
    ans = lista[0][:]

    # Pega o melhor
    for el in lista:
        if distancia(ans, posicao) == None:
            ans = el
        elif distancia(el, posicao) != None:
            if distancia(el, posicao) < distancia(ans, posicao):
                ans = el[:]
    return ans

def posicao_anterior(pos):
    '''
    Devolve a posição e a orientacao anteriores baseado na posição atual e orientação.
    '''
    # Um dos parâmetros tem que ser igual, ou a orientação não faz sentido

    # A orientação anterior é a posição atual
    global orientacao 
    ori = orientacao
    pos_a = []
    for i in range(2):
        pos_a.append((pos[i] - ori[i]) % 5)

    return pos_a

def orientacao_entre_salas(partida, chegada):
    '''Devolve a orientação [lista de coordenadas] de uma sala em relação à outra
    exemplos:
    ([0, 0], [0, 1]) -> [0, 1].
    ([3, 3], [2, 3]) -> [-1, 0]
    ([0, 2], [4, 2]) -> [-1, 0]  (para N = 5)
    '''
    global N

    assert partida in adjacentes(chegada)

    ans = [[], []]
    ans[0] = chegada[0] - partida[0]
    ans[1] = chegada[1] - partida[1]

    for i in range(2):
        if ans[i] == N - 1:
            ans[i] = -1
        elif ans[i] == 1 - N:
            ans[i] = 1
             
    return ans

def distancia(a, b):
    '''Devolve a distância caminhável (ou seja, que só passa por salas livres
    ou visitadas) entre dois pontos. Se não houver, devolve None.
    Esse distância CONTA quantas vezes a personagem vai ter que virar para
    chegar ao destino
    '''

    # b é sempre a personagem
    d = tabela_de_distancias_caminhaveis(b)
    if d[a[0]][a[1]] != -1:
        return d[a[0]][a[1]] + curvas_no_caminho(d, a)

def curvas_no_caminho(d, a):
    '''
    No trajeto de a até o alvo de d (ver documentação da função
    tabela_de_distancias_caminháveis), devolve quantas curvas terão
    de ser feitas,
    '''

    global orientacao, posicao, N

    # o ponto no mapa onde há 1 é o personagem.
    assert d[posicao[0]][posicao[1]] == 1

    # Vamos supor que se trata de alguém indo de a até
    # b (na verdade é o contrário)

    # define a primeira orientacao para o lado da próxima casa no caminho
    # e a posicao inicial, que é igual a 'a'
    p = menor_adjacente(d, a)[:]
    prox_p = menor_adjacente(d, p)[:]
    o = orientacao_entre_salas(a, p)[:]
    prox_o = orientacao_entre_salas(p, prox_p)[:]
    # As orientações em ref giram da esquerda para a direita
    ref = [[1, 0], [0, -1], [-1, 0], [0, 1]]

    soma = 0
    cond = True
    while p != posicao:
        m = ref.index(o)
        n = ref.index(prox_o)
        # soma quantas vezes precisa girar para chegar em menor_adjacente
        soma += min((m-n) % 4, (n-m) % 4)

        p = prox_p[:]
        prox_p = menor_adjacente(d, p)
        o = prox_o
        prox_o = orientacao_entre_salas(p, prox_p)
        
    # depois tem que somar os giros de orientacao em relação a 'o'
    # por que ainda não consideramos como a orientacao da personagem
    # se relaciona com esse caminho

    m = ref.index(o)
    n = (ref.index(orientacao) + 2) % 4
    soma += min((m - n) % 4, (n - m) % 4)

    return soma

def menor_adjacente(d, pos):
    '''
    devolve a posicao da sala adjacente a pos que tem o menor valor em d
    '''

    assert pos != None
    adj = adjacentes(pos)

    # Tem que inicializar em uma variável cujo valor em d não seja -1
    menor = adj[0]
    # Percorre adj até achar alguém com valor != -1
    while d[menor[0]][menor[1]] == -1 and adj.index(menor) < 4:
        menor = adj[adj.index(menor) + 1] 

    # Se der esse erro, tá chegando informação errada
    assert d[menor[0]][menor[1]] != -1

    for s in adj[1:]:
        if d[s[0]][s[1]] != -1 and d[s[0]][s[1]] < d[menor[0]][menor[1]]:
            menor = s
    return menor

def tabela_de_distancias_caminhaveis(alvo):
    '''
    Devolve matriz em que a todas as salas caminháveis (visitadas ou livres)
    corresponde um número que indica a distância caminhável dessa sala
    até o alvo
    '''


    # vamos implementar sistema semelhante ao do exercício do rato
    # https://www.ime.usp.br/~macmulti/exercicios/extra/index.html

    # Inicializar uma matriz do tamanho do mundo cheia de -1 (que representa
    # salas não livres ou não visitadas)
    d = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append(-1) # começa com listas vazias
        d.append(linha)

    # Função recursiva para marcar as distâncias em d
    marcar_tabela_de_distancias(d, alvo, 1)

    return d

def marcar_tabela_de_distancias(d, sala, marca):
    '''
    Marca salas na representação d (distancias) do mundo. Cada sala é
    marcada com 'marca' e marca suas adjacentes seguras com 'marca - 1'
    '''
    global mundo


    # se o valor atual dessa sala for -1, então o novo valor é marca
    # se essa sala já tiver um valor, queremos que fique o menor deles

    if d[sala[0]][sala[1]] < 0 or d[sala[0]][sala[1]] > marca:
        d[sala[0]][sala[1]] = marca
    else:
        # se não, não fazemos nada, para evitar loop infinito
        return None

    adj = adjacentes(sala)
    for s in adj:
        if 'V' in mundo[s[0]][s[1]] or 'L' in mundo[s[0]][s[1]]:
            marcar_tabela_de_distancias(d, s, marca+1)




# ---- Funções relativas ao mundo ------------------------------- #




def marcar_salas_adjacentes(pos, string, exceto=[]):
    '''
    Marca as salas adjacentes à 'pos' com a 'string', a não ser que algum
    elemento da lista 'exceto' já seja elemento dessa posição. 
    '''
    for p in adjacentes(pos):
        adiciona_ao_mundo(p, string, exceto)

def remover_de_salas_adjacentes(pos, string, exceto=[]):
    '''
    Remove das salas adjacentes à 'pos' a 'string', a não ser que algum
    elemento da lista 'exceto' já seja elemento dessa posição. 
    '''
    for p in adjacentes(pos):
        remove_do_mundo(p, string, exceto)

def atualiza_salas_livres():
    '''
    Atualiza a lista sala_livre. Adiciona novas e remove as que não o são mais
    '''
    global N
    global mundo
    global salas_livres

    for i in range(N):
        for j in range(N):
            if 'L' in mundo[i][j] and [i, j] not in salas_livres:
                salas_livres.append([i, j])
            if 'L' not in mundo[i][j] and [i, j] in salas_livres:
                salas_livres.remove([i, j])

def adjacentes(pos):
    '''
    Devolve a posicao (lista de quatro listas de dois elementos,
    ex: [[0, 1], [1, 0], [-1, 0], [0, -1]])das salas adjacentes
    '''
    global N
    ans = []
    for p in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
        ans.append([(pos[0] + p[0]) % N, (pos[1] + p[1]) % N])
    return ans

def adiciona_ao_mundo(pos, letra, exceto=[], quem='4603521'):
    '''
    Adiciona letra ao mundo em 'pos', se já não houver essa letra
    lá e se nenhum elemento de exceto estiver lá
    '''
    global mundo, quantos_viram
    q = quantos_viram

    i, j = pos[0], pos[1]
    pode = True

    if letra in mundo[i][j]:
        pode = False

    for e in exceto:
        if e in mundo[i][j]:
            pode = False

    if pode:
        mundo[i][j].append(letra)

    for l in ['W?', 'W', 'P', 'P?']:
        for el in q[i][j]:
            if letra == l and el[0] == l and quem not in el[1]:
                el[1].append(quem)

def remove_do_mundo(pos, letra, exceto=[]):
    '''
    Remove letra do mundo em 'pos' se houver essa letra lá'
    e se nenhum elemento de exceto estiver lá
    '''
    global mundo, quantos_viram
    q = quantos_viram

    i, j = pos[0], pos[1]
    pode = True

    if letra not in mundo[i][j]:
        pode = False

    for e in exceto:
        if e in mundo[i][j]:
            pode = False

    if pode:
        mundo[i][j].remove(letra)

    for l in ['W?', 'W', 'P', 'P?']:
        for el in q[i][j]:
            if letra == l and el[0] == l:
                el[1] = []

def achar_salas_com(s):
    '''
    Recebe uma string e devolve uma lista com a posição de todas
    as salas no mundo que a contêm. Se não achar, devolve lista vazia
    '''
    global mundo
    global N

    ans = []
    for i in range(N):
        for j in range(N):
            if s in mundo[i][j] and [i, j] not in ans:
                ans.append([i, j])
    return ans



#debug:
def impr(a):
    for i in range(N):
        for j in range(N):
            print(a[i][j], end='\t')
        print()
    print()
