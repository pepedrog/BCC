# flag para depuração
__DEBUG__ = True


# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global nFlechas ########
"""
Número de flechas que a personagem possui. Serve apenas para
consulta da personagem, pois o mundo mantém uma cópia "segura" dessa
informação (não tente inventar flechas...).
"""

global mundoCompartilhado ############
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


def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, salasLivres, salasNvisitadas, percepcao2, compartilhe
    # guarda o tamanho do mundo
    N = tamanho
    #TODAS AS SALAS LIVRES E SALAS NAO VISITADAS
    salasLivres = [] ###
    salasNvisitadas = [] ###
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    ## variável criada para ter uma lista de percepcao em agir()
    percepcao2 = []
    for i in range(N) : 
        linha = []
        linha1 = []
        linha2 = []
        linha3 = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
            linha1.append(False)
            linha2.append(True) # todas as casas sao nao-visitadas no começo
            linha3.append([])
        mundo.append(linha)
        percepcao2.append(linha3)
        salasLivres.append(linha1) # TRUE SE A SALA EM QUESTAO ESTA LIVRE
        salasNvisitadas.append(linha2) #TRUE SE A SALA EM QUESTAO NAO FOI VISITADA 
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    compartilhe = False

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, salasLivres, salasNvisitadas, percepcao2, compartilhe
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.

    # Essa função ainda precisa ser implementada! São requisitos dessa
    # implementação a incorporação dos dados perceptuais à representação
    # do mundo, bem como a propagação do conhecimento adquirido para as
    # adjacências da sala atual (requisitos completos no enunciado). 
    
    compartilhe = False
    
    for nome in percepcao:
        if percepcao!=[] and nome!="I" and nome!="B" and nome!="F" and nome!="U" and nome!="V" and nome!="L":
            compartilhe = True
        
##SE TIVER INFO. QUE FOI COMPARTILHADA, ATUALIZA A LISTA Bool DE SALAS LIVRES E QUAISQUER PROBLEMAS DE SOBRESCRIÇAO
    if compartilhe:
        for linhas in range(N):
            for colunas in range(N):
                if "L" in mundoCompartilhado[linhas][colunas]:
                    if salasLivres[linhas][colunas]==False:
                        salasLivres[linhas][colunas] = True
                    if "V" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["V"] #CASO HAJA SOBREPOSICAO 'VL'
                    elif "M" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["M"] #CASO HAJA SOBREPOSIÇAO 'ML'
                    elif "P?" in mundo[linhas][colunas] or "W?" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["L"] #CASO HAJA 'W?L' ou 'P?L'
                    else:
                        mundo[linhas][colunas] = ["L"] #CASO HAJA SOBREPOSICAO 'LL'
                elif "M" in mundoCompartilhado[linhas][colunas]:
                    if salasLivres[linhas][colunas]==True:
                        salasLivres[linhas][colunas] = False
                    if "V" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["V"]
                    elif "W?" in mundo[linhas][colunas] or "P?" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["M"]
                    else:
                        mundo[linhas][colunas] = ["M"]
                elif "W?" in mundoCompartilhado[linhas][colunas]:
                    if salasLivres[linhas][colunas]==True:
                        salasLivres[linhas][colunas] = False
                    if "V" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["V"]
                    elif "M" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["M"]
                    elif "P?" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["P?","W?"]
                    else:
                        mundo[linhas][colunas] = ["W?"]
                elif "P?" in mundoCompartilhado[linhas][colunas]:
                    if salasLivres[linhas][colunas]==True:
                        salasLivres[linhas][colunas] = False
                    if "V" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["V"]
                    elif "M" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["M"]
                    elif "W?" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["P?","W?"]
                    else:
                        mundo[linhas][colunas] = ["P?"]
                elif "W" in mundoCompartilhado[linhas][colunas]:
                    if salasLivres[linhas][colunas]==True:
                        salasLivres[linhas][colunas] = False
                    if "V" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["V"]
                    elif "M" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["M"]
                    elif "P?" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["P?","W?"]
                    else:
                        mundo[linhas][colunas] = ["W?"]
                elif "P" in mundoCompartilhado[linhas][colunas]:
                    if salasLivres[linhas][colunas]==True:
                        salasLivres[linhas][colunas] = False
                    if "V" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["V"]
                    elif "M" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["M"]
                    elif "W?" in mundo[linhas][colunas]:
                        mundo[linhas][colunas] = ["P?","W?"]
                    else:
                        mundo[linhas][colunas] = ["P?"]
                    
    
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        pos = posicao
        ori = orientacao
       
        vizinhanca=[ [(pos[0]+1)%N,pos[1]],    #EM CIMA
                     [(pos[0]-1)%N,pos[1]],    #EM BAIXO
                     [pos[0],(pos[1]+1)%N],    #DIREITA
                     [pos[0],(pos[1]-1)%N] ]   #ESQUERDA

        ##COLOCA M AO COLODIR E FICA NO MSM LUGAR
        if "I" in percepcao: ##N COLOCA I EM percepcao2
            mundo[pos[0]][pos[1]] = ["M"]
            percepcao2[pos[0]][pos[1]] = ["M"]
            posnovaPersonagem = [(pos[0]-ori[0])%N,
                                 (pos[1]-ori[1])%N]
            pos[0],pos[1] = posnovaPersonagem[0],posnovaPersonagem[1]
            vizinhanca=[ [(pos[0]+1)%N,pos[1]],    #EM CIMA
                         [(pos[0]-1)%N,pos[1]],    #EM BAIXO
                         [pos[0],(pos[1]+1)%N],    #DIREITA
                         [pos[0],(pos[1]-1)%N] ]   #ESQUERDA
            
        ##COLOCA L EM TODOS AO REDOR SE NAO HOUVER PERCEPÇAO
        if "B" not in percepcao and "F" not in percepcao:
            for lado in vizinhanca:
                if "M" not in mundo[lado[0]][lado[1]] and "V" not in mundo[lado[0]][lado[1]] and "L" not in mundo[lado[0]][lado[1]]:
                    mundo[lado[0]][lado[1]] = ["L"]
                    if "M" not in percepcao2[lado[0]][lado[1]]:
                        percepcao2[lado[0]][lado[1]] = ["L"]
                    salasLivres[lado[0]][lado[1]] = True
                    
        ##COLOCA 'P?' SE SENTIR 'B'
        if "B" in percepcao:
            if "B" not in percepcao2[pos[0]][pos[1]]:
                percepcao2[pos[0]][pos[1]].append("B")
            for lado in vizinhanca:
                if "V" not in mundo[lado[0]][lado[1]] and "M" not in mundo[lado[0]][lado[1]] and "P?" not in mundo[lado[0]][lado[1]] and "L" not in mundo[lado[0]][lado[1]]:
                    mundo[lado[0]][lado[1]].append("P?")
                    
        ##COLOCA 'W?' SE SENTIR 'F'
        if "F" in percepcao:
            if "F" not in percepcao2[pos[0]][pos[1]]:
                percepcao2[pos[0]][pos[1]].append("F")
            for lado in vizinhanca:
                if "V" not in mundo[lado[0]][lado[1]] and "M" not in mundo[lado[0]][lado[1]] and "W?" not in mundo[lado[0]][lado[1]] and "L" not in mundo[lado[0]][lado[1]]:
                    mundo[lado[0]][lado[1]].append("W?")
 
       
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        mundo[pos[0]][pos[1]] = ["V"]
        salasNvisitadas[pos[0]][pos[1]] = False
        salasLivres[pos[0]][pos[1]] = True
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
                print("".join(mundo[i][j]),end="\t| ")
              #  print("".join(mundoCompartilhado[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    

def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, percepcao2, N, compartilhe,salasLivres
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
    
    ##OBSERVAÇAO: FRENTE DO INDIVÍDUO É mundo[(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)]
    pos = posicao
    ori = orientacao
    vizinhanca=[ [(pos[0]+1)%N,pos[1]],    #EM CIMA
                 [(pos[0]-1)%N,pos[1]],    #EM BAIXO
                 [pos[0],(pos[1]+1)%N],    #DIREITA
                 [pos[0],(pos[1]-1)%N] ]   #ESQUERDA
    
    print("salasLivres:",salasLivres)
    
    ##PRIORIDADE À COMPARTILHAMENTO DE info.
    if compartilhe:
        acao = "C"
        return acao
    
    ##SE TIVER ESPAÇO LIVRE NA FRENTE
    if "L" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] and "M" not in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]: #ANDA PRA FRENTE
        acao="A"
        pos[0] = (pos[0]+ori[0])%len(mundo)
        pos[1] = (pos[1]+ori[1])%len(mundo)
        return acao
    ##PROCURA AOS REDORES
    else:
        for casa in vizinhanca: #PEGA A PRIMEIRA CASA ADJACENTE LIVRE
            if "L" in mundo[casa[0]][casa[1]] and "M" not in mundo[casa[0]][casa[1]]: #"M not in casa" serve apenas para caso algo de errado
                if ori[0]==0 and ori[0] == -ori[1] and ori[1] == -ori[0]:#SE SÓ PRECISAR VIRAR À ESQUERDA e ori[0]==0
                    acao = "E"
                    ori[1] = -ori[1]
                    ori[0],ori[1] = ori[1],ori[0]
                    return acao
                elif ori[0]!=0 and ori[0] == ori[1] and ori[1] == ori[0]: #SE SÓ PRECISAR VIRAR À ESQUERDA e ori[0]!=0 
                    acao = "E"
                    ori[0],ori[1] = ori[1],ori[0]
                    return acao
                elif ori[1]==0 and ori[0] == -ori[1] and ori[1] == -ori[0]: #SE SÓ PRECISAR VIRAR À DIREITA e ori[1]==0
                    acao = "D"
                    ori[0] = -ori[0]
                    ori[0],ori[1] = ori[1],ori[0]
                    return acao
                elif ori[1]!=0 and ori[0] == ori[1] and ori[1] == ori[0]: #SE SÓ PRECISAR VIRAR À DIREITA e ori[1]!=0
                    acao = "D"
                    ori[0],ori[1] = ori[1],ori[0]
                    return acao
                else: #SE TIVER DO LADO OPOSTO
                    acao = "E" #VIRA PRA UM LADO QUALQUER
                    if ori[0]==0:
                        ori[1] = -ori[1]
                    ori[0],ori[1] = ori[1],ori[0]
                    return acao                
    ##SE NAO HOUVEREM CASA LIVRES AOS ARREDORES, ENTAO DEVE TER M,P? ou W?
    ##CASO EM QUE HÁ P? ou W?

    vizinhanca=[ [(pos[0]+1)%N,pos[1]],    #EM CIMA
                 [(pos[0]-1)%N,pos[1]],    #EM BAIXO
                 [pos[0],(pos[1]+1)%N],    #DIREITA
                 [pos[0],(pos[1]-1)%N] ]   #ESQUERDA
    

    TudoVisitado = True
    NaoHaSaida = True
    JaAndei = False #INDICA SE JA PASSOU EM ALGUM LUGAR
    IrPara = [0,0]
    for linha in range(N) : 
        for coluna in range(N) :  #DIMENSOES DO MAPA
            if "L" in mundo[linha][coluna] and salasNvisitadas[linha][coluna] == True: #SE TEM UMA SALA
                TudoVisitado = False                                                   #LIVRE NAO VISITADA
            if TudoVisitado == False: #SE TEVE LUGAR QUE NAO VISITOU, VAI ATÉ LA
                VisitarLocal = mundo[linha][coluna] #pega a última casa da lista que nao visitou
            if "V" in mundo[linha][coluna]:
                JaAndei = True
                bloco = [  [(linha+1)%N,coluna],    #EM CIMA
                           [(linha-1)%N,coluna],    #EM BAIXO
                           [linha,(coluna+1)%N],    #DIREITA
                           [linha,(coluna-1)%N] ]   #ESQUERDA
                for k in bloco:
                    if "L" in mundo[k[0]][k[1]]:
                        NaoHaSaida = False
                        IrPara = [k[0],k[1]]
    
    print("IrPara:",IrPara)
    print("NaoHaSaida:",NaoHaSaida)
    if JaAndei==False:
        NaoHaSaida = True
    QuantosW = 0
    if "F" in percepcao2[pos[0]][pos[1]]:
        QuantosW += 1
    if "B" in percepcao2[pos[0]][pos[1]] or "F" in percepcao2[pos[0]][pos[1]]:
        if TudoVisitado or NaoHaSaida: #SE TODAS AS CASAS LIVRES JA FORAM VISITADAS     
            if "P?" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] or "W?" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]: #SE TIVER NA FRENTE
               if "F" in percepcao2[pos[0]][pos[1]] and QuantosW == 1 and nFlechas>=1: #SE SÓ TIVER 1 'W?' AO REDOR E NA FRENTE
                   acao="T"
                   return acao
               else: #QUALQUER UM DOS DOIS, ARRISCA AVANÇAR
                   acao="A"
                   pos[0] = (pos[0]+ori[0])%len(mundo)
                   pos[1] = (pos[1]+ori[1])%len(mundo)
                   return acao
            else:
                if ori[0]==0: #SE SÓ PRECISAR VIRAR À ESQUERDA e ori[0]==0
                    acao = "E"
                    ori[1] = -ori[1]
                    ori[0],ori[1] = ori[1],ori[0]
                    return acao
                elif ori[0]!=0: #SE SÓ PRECISAR VIRAR À ESQUERDA e ori[0]!=0
                    acao = "E"
                    ori[0],ori[1] = ori[1],ori[0]
                    return acao
                                            
        else: #Se TudoVisitado == False, DEVE VOLTAR PRO LOCAL ONDE TEM 'L', o 'VisitarLocal'
            if "V" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:  #SE 'V' TIVER NA FRENTE
                acao="A"
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                return acao
            else:
                acao = "E" #VIRA PRA UM LADO QUALQUER PRA DAR MEIA-VOLTA
                if ori[0]==0:
                    ori[1] = -ori[1]
                ori[0],ori[1] = ori[1],ori[0]
                return acao   
                
    else: #SE NAO SENTIR "B" ou "F" ########
        if TudoVisitado or NaoHaSaida: #SE TODAS AS CASAS LIVRES JA FORAM VISITADAS 
            if "V" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]: #SE 'V' TIVER NA FRENTE
                acao="A"
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                return acao
            else:
                acao = "E" #VIRA PRA UM LADO QUALQUER PRA DAR MEIA-VOLTA
                if ori[0]==0:
                    ori[1] = -ori[1]
                ori[0],ori[1] = ori[1],ori[0]
                return acao
        
        else: #precisa ir pro lugar com L ##IrPara
            if salasLivres[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:
                acao = "A"
                pos[0] = (pos[0]+ori[0])%len(mundo)
                pos[1] = (pos[1]+ori[1])%len(mundo)
                return acao
            else:
                acao = "E" #VIRA PRA UM LADO QUALQUER PRA DAR MEIA-VOLTA
                if ori[0]==0:
                    ori[1] = -ori[1]
                ori[0],ori[1] = ori[1],ori[0]
                return acao
            

    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo é uma pseudo-implementação, pois recebe
    # a ação através de uma pergunta dirigida ao usuário.
    # No código a ser entregue, você deve programar algum tipo
    # de estratégia para 
##    acao = input("Digite a ação desejada (A/D/E/T/C): ")

    # ATENÇÃO: a atualizacao abaixo está errada!!!
    # Não checa se o movimento foi possível ou não... isso só dá para
    # saber quando chegar uma percepção nova (a percepção "I"
    # diz que o movimento anterior não foi possível).
##    if acao=="A":
##        pos[0] = (pos[0]+ori[0])%len(mundo)
##        pos[1] = (pos[1]+ori[1])%len(mundo)
##    if acao=="E":
##        if ori[0]==0:
##            ori[1] = -ori[1]
##        ori[0],ori[1] = ori[1],ori[0]
##    if acao=="D":
##        if ori[1]==0:
##            ori[0] = -ori[0]
##        ori[0],ori[1] = ori[1],ori[0]
##    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####
##
#    assert acao in ["A","D","E","T","C"]
#    return acao

#####OBSERVACOES: DA PRA JUNTAR OS CASOS DE VIRAR PRA DIREITA/ESQUERDA COMO LAÇOS if DE FORA
#####             E COLOCAR DENTRO OS CASOS EM QUE HÁ "L" ou "W?"/"P?"
