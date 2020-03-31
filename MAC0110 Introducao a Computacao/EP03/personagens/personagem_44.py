# flag para depuração
__DEBUG__ = True

# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global nFlechas #numero de flechas
global mundoCompartilhado #representacao do mundo de outra personagem

#Outras variaveis globais do modulo personagemNUSP

global N #dimensão do mundo NxN
global mundo #matriz do conhecimento da personagem. Na forma mundo[i][j], cada entrada é uma lista
global posicao #posicao relativa. Padrao: (0,0) canto superior esquerdo
global orientacao #orientacao da movimentacao da personagem. Padrao: (1,0), direcao do eixo vertical

def inicializa(tamanho):
    """ Função de inicialização da personagem (recebe o tamanho do mundo).
        Usa as variáveis globais (do módulo) para representar seu
        conhecimento do mundo, sua posição e sua orientação relativas
        ao início da simulação. Você pode criar e inicializar outras
        variáveis aqui (por exemplo, a lista de salas livres e não
        visitadas).

    """
    # declara as variáveis globais que serão acessadas
    global N, mundo, posicao, orientacao, salasLivres, amigo, acao
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N):
        linha=[]
        for i in range(N):
            linha.append([]) #comeca com listas vazias
        mundo.append(linha)
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    salasLivres = []#armazena a posicao das salas livres que ainda nao foram visitadas
    amigo=False #indicará a presenca de outra personagem na mesma sala
    acao=""

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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, N, salasLivres, amigo, acao
    i, j = posicao[0], posicao[1]
    
    #direcoes na nossa visao, nao da personagem
    dirE = mundo[i][(j-1)%N]
    dirD =  mundo[i][(j+1)%N]
    dirT = mundo[(i+1)%N][j]
    dirB = mundo[(i-1)%N][j]
    
    if not "I" in percepcao: mundo[i][j]=["V","L"] #marca sala visitada
    if [i,j] in salasLivres: salasLivres.remove([i,j]) #remove sala atual das livres que faltavam ser visitadas
    if percepcao==[]: #marca salas ao redor como livres caso ja nao visitadas ou com muro
        if not ("V" in dirT or "L" in dirT or dirT==["M"]): mundo[(i+1)%N][j]=["L"]; salasLivres+=[[(i+1)%N,j]]
        if not ("V" in dirB or "L" in dirB or dirB==["M"]): mundo[(i-1)%N][j]=["L"]; salasLivres+=[[(i-1)%N,j]]
        if not ("V" in dirD or "L" in dirD or dirD==["M"]): mundo[i][(j+1)%N]=["L"]; salasLivres+=[[i,(j+1)%N]]
        if not ("V" in dirE or "L" in dirE or dirE==["M"]): mundo[i][(j-1)%N]=["L"]; salasLivres+=[[i,(j-1)%N]]
    else:
        for t in percepcao:
            if t == "I": #caso tenha impacto, havia um muro, entao volta pra posicao anterior
                mundo[posicao[0]][posicao[1]]=["M"] #e marca o muro no mundo
                posicao[0]=(i-orientacao[0])%N
                posicao[1]=(j-orientacao[1])%N
                dirE, dirD, dirT, dirB = mundo[i][(j-1)%N], mundo[i][(j+1)%N], mundo[(i+1)%N][j], mundo[(i-1)%N][j]
            elif t== "U":
                mundo[i][j] #nenhuma acao especifica
            elif t == "F" or t==  "B":
                if t=="F": sente="W?"
                if t=="B": sente="P?"
                #proximas linhas marcam a percepcao no mapa caso ja nao haja
                if not (sente in dirT or "V" in dirT or  "L" in dirT or dirT==["M"] or dirT==["P"] or dirT==["W"]): mundo[(i+1)%N][j]+= [sente]
                if not (sente in dirB or "V" in dirB or  "L" in dirB or dirB==["M"] or dirB==["P"] or dirB==["W"]): mundo[(i-1)%N][j]+= [sente]
                if not (sente in dirD or "V" in dirD or  "L" in dirD or dirD==["M"] or dirD==["P"] or dirD==["W"]): mundo[i][(j+1)%N]+= [sente]
                if not (sente in dirE or "V" in dirE or  "L" in dirE or dirE==["M"] or dirE==["P"] or dirE==["W"]): mundo[i][(j-1)%N]+= [sente]
            else: #percepcao diferente de F, B, I, U, entao é outro personagem na sala
                amigo=True

    for i in range(N):
        for j in range(N):
            inc=[0, []]
            for a in (-1, 0,1):
                for b in range(-1, 0, 1):
                    if "W?" in mundo[(a+i)%N][(b+j)%N]:
                        inc[0]+=1
                        inc[1]=[(a+i)%N,(b+j)%N]
            if inc[0]==1 and inc[1]==[i,j]:
                mundo[i][j]=["W"]
                print("atualizado")
                input()
            if mundoCompartilhado[i][j]!=[] and (mundo[i][j]==[] or (not mundoCompartilhado[i][j] in mundo[i][j] and mundo[i][j]!=["M"] and mundo[i][j]!=["V","L"])):
                #agrega informacoes compartilhadas somente quando a sala nao tem percepcoes ou novas percepcoes pra salas nao visitadas
                mundo[i][j]=mundoCompartilhado[i][j]
                #adiciona salas livres nao visitadas na lista caso ja nao esteja
                if mundoCompartilhado[i][j]==["L"] and not [i,j] in salasLivres: salasLivres+=[[i,j]]

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
                    print("X",end="")
                    if ori==[0,1]:
                        print(">",end="")
                    if ori==[1,0]:
                        print("v",end="")
                    if ori==[-1,0]:
                        print("^",end="")
                print("".join(mundo[i][j]),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
    # ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####


def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, N, amigo, acao
    i, j = posicao[0], posicao[1]
    ori = orientacao
    prox=mundo[(i+ori[0])%N][(j+ori[1])%N]
    avante= not ("M" in prox or "P?" in prox or "W?" in prox or "P" in prox or "W" in prox)
    
    if amigo==True: #tem outra personagem na sala
        acao="C"
        amigo=False
    else:
        #visita sala livre e nao explorada a frente
        if prox==["L"]: acao="A"
        #atira no Wumpus se for certeza que ele esta la
        elif prox==["W"] and nFlechas!=0: acao="T"
        else:
            
            if salasLivres!=[]: #ainda ha o que explorar
                distancia=2*N
                
                for salas in salasLivres:
                    #busca a sala mais proxima dentro da lista de salas livres e nao visitadas
                    if distancia >= (salas[0]-i)%N+(salas[1]-j)%N:
                        distancia=(salas[0]-i)%N+(salas[1]-j)%N
                        melhorSala=salas
                    if distancia >= (i-salas[0])%N+(j-salas[1])%N:
                        distancia=(i-salas[0])%N+(j-salas[1])%N
                        melhorSala=salas
                        
                if melhorSala[0]==i: #sala mais proxima esta na mesma linha
                    acao="E"
                    if (j-melhorSala[1])%N <=(melhorSala[1]-j)%N: #esquerda melhor
                        livre, col=True, j
                        while (col-1)%N >melhorSala[1] and livre==True:
                            if mundo[i][(col-1)%N]!=["V","L"] and mundo[i][(col-1)%N]!=["L"]:
                                livre=False
                            else: col=col-1
                        if livre and ori==[0,1] and avante: acao="A"#se esta livre e na direcao certa
                        
                    if ((j-melhorSala[1])%N >(melhorSala[1]-j)%N) or livre==False: #direita melhor
                        livre, col=True, j
                        while (col+1)%N < melhorSala[1] and livre==True:
                            if mundo[i][(col+1)%N]!=["V", "L"] and mundo[i][(col+1)%N]!=["L"]:
                                livre=False
                            else: col=col+1
                        if livre and ori==[0,-1] and avante: acao="A" #se esta livre e na direcao certa
                        if livre and ori==[0,1] and avante: acao="A" #livre e orientacao errada 
                        else:
                            if (ori==[-1,0] or ori==[1,0]) and avante: acao="A" #muda de linha
                            elif avante and ori!=[-1,0] and ori!=[1,0]: acao="A"

                elif melhorSala[1]==j: #mesma coluna
                    acao="D"
                    if (i-melhorSala[0])%N <=(melhorSala[0]-i)%N: #acima melhor	
                        livre, lin=True, i
                        while (lin-1)%N > melhorSala[0] and livre==True: #checa se o caminho esta livre
                            if mundo[(lin-1)%N][j]!=["V", "L"] and mundo[(lin-1)%N][j]!=["L"]:
                                livre=False
                            else: lin=lin-1
                        if livre and ori==[-1,0] and avante: acao="A"
                        elif livre and ori==[0,-1] and avante: acao="D"
                        
                    if ((i-melhorSala[0])%N >(melhorSala[0]-i)%N) or livre==False: #abaixo melhor ou caminho por cima nao livre
                        livre, lin=True, i
                        while ((lin+1)%N <melhorSala[0]) and (livre==True): #checa se o caminho está livre (a coluna)
                            if mundo[(lin+1)%N][j]!=["V","L"] and mundo[(lin+1)%N][j]!=["L"]:
                                livre=False
                            else: lin=lin+1
                        if livre and ori==[1,0] and avante: acao="A" #esta na direcao certa e caminho livre
                        if livre and ori==[0,-1]: acao="E" #livre mas personagem virado para a esquerda
                        if livre and ori==[0,1]: acao="D" #livre mas personagem virado para a direita
                        elif not livre: #caminho nao esta livre 
                            if ori==([0,1] or [0,-1]) and avante: acao="A"
                            elif avante and ori!=[-1,0] and ori!=[1,0]: acao="A"

                else: #esta desalinhado
                    if mundo[(i-1)%N][j]==["V","L"] or mundo[(i-1)%N][j]==["L"]:
                        if ori==[-1,0]: acao="A"
                        else: acao="D"
                    elif mundo[i][(j+1)%N]==["V","L"] or mundo[i][(j+1)%N]==["L"]:
                        if ori==[0,1]: acao="A"
                        else: acao="D"
                    elif mundo[(i+1)%N][j]==["V","L"] or mundo[(i+1)%N][j]==["L"]:
                        if ori==[1,0]: acao="A"
                        else: acao="D"
                    elif avante: acao="A"
                    else: acao="D"
                    
            elif not ("P" in prox or "W" in prox or "M" in prox): #arrisca-se caso nao teha certeza do perigo
                acao="A"
            else: #certeza de coisa ruim na frente
                acao="D"
                
    if acao=="A":
            posicao[0] = (i+ori[0])%N
            posicao[1] = (j+ori[1])%N
    elif acao=="E":
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
    elif acao=="D":
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
    assert acao in ["A","D","E","T","C"]
    return acao
