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
Representação relativa a procura de salas livres
"""
global plano
"""
Refere-se aos planos de ação a serem enviado da função planejar para
a função agir.São eles:
    
    -plano==0, Plano de busca sonar, padrão sala livre
    -plano==1, Compartilha mundo
    -plano==2, Mudança no padrão de procura, busca específica de sala livre
    -plano==3, Plano busca e ataque caso houver flechas
    
"""

global contador
"""
contador para mudança de comportamento de giro de personagem, 
horário/antihorário, tem como objetivo evitar loops.
"""

global contadorv2
"""
contador para mudança de comportamento de plano de busca de sala livre
"""
global ultimo_olfato
"""
Garante o ultimo olfato antes do disparo de flechas
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
    global N, mundo, posicao, orientacao, plano, salas_livres, contador,\
    contadorv2
    # guarda o tamanho do mundo
    N = tamanho
    # cria a matriz NxN com a representação do mundo conhecido
    mundo = []
    for i in range(N) :
        linha = []
        for j in range(N) :
            linha.append([]) # começa com listas vazias
        mundo.append(linha)  
    # cria a matriz NxN com a representação das salas desconhecidas ou livres 
    # não exploradas     
    salas_livres = []
    for i in range(N) :
        linhaL = []
        for j in range(N) :
            linhaL.append([-1]) # começa com listas vazias
        salas_livres.append(linhaL)  
    salas_livres[0][0]=[-1] 
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    # Inicializa o plano inicial
    plano=0
    # Inicializa um contador
    contador=0
    # Inicializa um contador que inicializa outro padrão de movimento
    contadorv2=0
    #
    
   

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
    global N, mundo, posicao, orientacao, nFlechas, mundoCompartilhado,\
    salas_livres , plano, contador, contadorv2, ultimo_olfato
    #
    pos = posicao
    ori = orientacao
    ###########################################
    #plano==0, Plano de busca sonar, padrão sala livre:
    #   Busca salas livres na proximidade, como um efeito de "sonar", ou seja
    #   circular e expansível, numerando as casa mais próximas com valores
    #   altos, as distantes com valores mais baixos, e as livres como 0
    #plano==1, Compartilha mundo
    #   Compartilha mundo com outras personagens, contudo por segurança só
    #   coleta informaçoes relativas a salas livres, marcando-as com 0
    #plano==2, Mudança no padrão de procura, busca específica:
    #   depois de explorar o mundo por N*20 rodadas, a personagem alterna
    #   o padrão de busca para um mais específico, isto é, escolhe uma sala
    #   marcada por livre e a procura. O plano 0 e 2 se alternam afim de 
    #   diminuir a probabilidade de looping de comportamento
    #plano==3, Plano busca e ataque caso houver flechas:
    #   Enumera um alvo Wumpus com -2, depois de eliminações de erros. Se 
    #   dirige a ele e dispara a flecha
    ###########################################
    # inicializa o planos
    #
    # Como o nome do personagem pode ser diverso, a condicional garante que 
    # o plano1 de conversa seja sempre acionado caso haver personagem
    plano=0
    if percepcao!=[] and percepcao!=["B"] and percepcao!=["F"] and \
    percepcao!=["I"] and percepcao!=['B', 'F']:
        plano=1
    if contadorv2>=(N*20):
        plano=2
    #
    # Recebe a percepcão do ultimo olfato
    ultimo_olfato=percepcao
    # Confirma localização do Wumpus por eliminação
    for i in range(N):
        for j in range(N):
            if "W?" in mundo[i][j]:
                n=0
                alvo_i,alvo_j=i,j
                for k in range(-1,2):
                    for r in range (-1,2):
                        if "W?" in mundo[(alvo_i+k)% N][(alvo_j+r)% N] or\
                        mundo[(alvo_i+k)% N][(alvo_j+r)%N]==[]:
                            n+=1
                if n==1:
                    mundo[alvo_i][alvo_j]=["W"]
    #                
    # Confirma localização do poço por eliminação
    for i in range(N):
        for j in range(N):
            if "P?" in mundo[i][j]:
                n=0
                alvo_i,alvo_j=i,j
                for k in range(-1,2):
                    for r in range (-1,2):
                        if "P?" in mundo[(alvo_i+k)% N][(alvo_j+r)% N] or\
                        mundo[(alvo_i+k)% N][(alvo_j+r)%N]==[]:
                            n+=1
                if n==1:
                    mundo[alvo_i][alvo_j]=["P"] 
    #
    # Em caso de certeza da localização de Wumpus inicializa o plano de ataque
    # caso somente houver flechas
    achouWumpus=False
    for sublista in mundo:
        for i in range(N):
            if "W" in sublista[i]:
                achouWumpus=True
    if achouWumpus==True and nFlechas>0:
        plano=3        
    #
    # Garante que o personagem não perca a noção depois de bater em um muro!   
    if "I" in percepcao:
        mundo[pos[0]][pos[1]]=["M"]
        salas_livres[pos[0]][pos[1]]=[-1]
        pos[0]=(pos[0]-ori[0])%N
        pos[1]=(pos[1]-ori[1])%N 
    #                 
    # Marca possibilidade de Wumpus em casas vazias ou outras suspeitas   
    if "F" in percepcao:
        mundo[pos[0]][pos[1]] = ["V","F"]
        if mundo[pos[0]][(pos[1]+1)% N]==[] or mundo[pos[0]][(pos[1]+1)% N]==["P?"]:
             mundo[pos[0]][(pos[1]+1)% N]=["W?"]
        if mundo[(pos[0]+1)% N][pos[1]]==[] or mundo[pos[0]][(pos[1]+1)% N]==["P?"]:
             mundo[(pos[0]+1)% N][pos[1]]=["W?"]
        if mundo[pos[0]][(pos[1]-1)% N]==[] or mundo[pos[0]][(pos[1]+1)% N]==["P?"]:
             mundo[pos[0]][(pos[1]-1)% N]=["W?"]
        if mundo[(pos[0]-1)% N][pos[1]]==[] or mundo[pos[0]][(pos[1]+1)% N]==["P?"]:
             mundo[(pos[0]-1)% N][pos[1]]=["W?"] 
    #
    # Marca possibilidade de poços em casas vazias ou outras suspeitas, essa parte
    # vem depois da percepção de wumpus, a fim de priorizar a marcação de poço, dimi
    # -indo a possibilidade de erro e disperdício de flecha.
    if 'B' in percepcao: 
        mundo[pos[0]][pos[1]] = ["V","B"]
        if mundo[pos[0]][(pos[1]+1)% N]==[] or mundo[pos[0]][(pos[1]+1)% N]==["W?"]:
             mundo[pos[0]][(pos[1]+1)% N]=["P?"]
        if mundo[(pos[0]+1)% N][pos[1]]==[] or mundo[pos[0]][(pos[1]+1)% N]==["W?"]:
             mundo[(pos[0]+1)% N][pos[1]]=["P?"]
        if mundo[pos[0]][(pos[1]-1)% N]==[] or mundo[pos[0]][(pos[1]+1)% N]==["W?"]:
             mundo[pos[0]][(pos[1]-1)% N]=["P?"]
        if mundo[(pos[0]-1)% N][pos[1]]==[] or mundo[pos[0]][(pos[1]+1)% N]==["W?"]:
             mundo[(pos[0]-1)% N][pos[1]]=["P?"]
    #
    # Enumeras casas como livres se não houver percepção de perigo
    if percepcao==[] or ('B' not in percepcao and 'F' not in percepcao and\
    'I' not in percepcao):
        mundo[pos[0]][pos[1]] = ["V"]
        
        if mundo[pos[0]][(pos[1]+1)% N]==[] or mundo[pos[0]][(pos[1]+1)% N]==["P?"]\
        or mundo[pos[0]][(pos[1]+1)% N]==["W?"]:
             mundo[pos[0]][(pos[1]+1)% N]=["L"]
             salas_livres[pos[0]][(pos[1]+1)% N]=[0]
             
        if mundo[(pos[0]+1)% N][pos[1]]==[] or mundo[(pos[0]+1)% N][pos[1]]==["P?"]\
        or mundo[(pos[0]+1)% N][pos[1]]==["W?"]:
             mundo[(pos[0]+1)% N][pos[1]]=["L"]
             salas_livres[(pos[0]+1)% N][pos[1]]=[0]
             
        if mundo[pos[0]][(pos[1]-1)% N]==[] or mundo[pos[0]][(pos[1]-1)% N]==["P?"]\
        or mundo[pos[0]][(pos[1]-1)% N]==["W?"]:
             mundo[pos[0]][(pos[1]-1)% N]=["L"]
             salas_livres[pos[0]][(pos[1]-1)% N]=[0]
             
        if mundo[(pos[0]-1)%N][pos[1]]==[] or mundo[(pos[0]-1)% N][pos[1]]==["P?"]\
        or mundo[(pos[0]-1)% N][pos[1]]==["W?"]:
             mundo[(pos[0]-1)% N][pos[1]]=["L"]
             salas_livres[(pos[0]-1)% N][pos[1]]=[0]
    #
    # Faz a enumeração das salas visitadas de acordo com a busca sonar,
    # o centro parte sempre da atual posição do personagem (decrescente)
    if plano==0 and contadorv2<(N*20): 
        contadorv2+=1
        for r in range(0,(N//2)+(N%2)):
            for k in range(0,(N//2)+(N%2)):
                if "V" in mundo[(pos[0]+k)% N][(pos[1]+r)% N]:                
                    salas_livres[(pos[0]+k)% N][(pos[1]+r)% N]=[N-(r+k)]
                if "V" in mundo[(pos[0]+k)% N][(pos[1]-r)% N]:
                    salas_livres[(pos[0]+k)% N][(pos[1]-r)% N]=[N-(r+k)]
                if "V" in mundo[(pos[0]-r)% N][(pos[1]+k)% N]:
                    salas_livres[(pos[0]-r)% N][(pos[1]+k)% N]=[N-(r+k)]
                if "V" in mundo[(pos[0]-r)% N][(pos[1]-k)% N]: 
                    salas_livres[(pos[0]-r)% N][(pos[1]-k)% N]=[N-(r+k)]  
    #
    # Recebe o compartilhamento de salas livres de outra personagem    
    if plano==1:
        for i in range(N):
            for j in range(N):
                if ("L" in mundoCompartilhado[i][j]) and ("V" not in mundo[i][j])\
                and ("P" not in mundo[i][j]) and ("W" not in mundo[i][j]):
                    mundo[i][j]=["L"]
                    salas_livres[i][j]=[0]
    #
    # Faz a enumeração das salas visitadas de acordo com a busca específica
    # o centro parte de uma das salas livres (crescente)       
    if plano==2: 
        contadorv2+=1
        e=False
        for i in range(N):
            for j in range(N):
                if "L" in mundo[i][j]:
                    e=True
                    alvo_i,alvo_j=i,j
        if e==False:
            plano=0
        for r in range(0,(N//2)+(N%2)):
            for k in range(0,(N//2)+(N%2)):
                if "V" in mundo[(alvo_i+k)% N][(alvo_j+r)% N]:                
                    salas_livres[(alvo_i+k)% N][(alvo_j+r)% N]=[r+k]
                if "V" in  mundo[(alvo_i+k)% N][(alvo_j-r)% N]:
                    salas_livres[(alvo_i+k)% N][(alvo_j-r)% N]=[r+k]
                if "V" in  mundo[(alvo_i-r)% N][(alvo_j+k)% N]:
                    salas_livres[(alvo_i-r)% N][(alvo_j+k)% N]=[r+k]
                if "V" in  mundo[(alvo_i-r)% N][(alvo_j-k)% N]: 
                    salas_livres[(alvo_i-r)% N][(alvo_j-k)% N]=[r+k]        
        if contadorv2>=(N*30):
            contadorv2=0
    #
    # Plano de ataque, marca um Wumpus certo ("W") como -2 e o procura a fim
    # de aniquila-lo.Como o plano 3 só é ativado caso houver flechas, não há
    # essa preocupação abaixo.
    if plano==3: 
        for i in range(N):
            for j in range(N):
                if "W" in mundo[i][j]:
                    salas_livres[i][j]=[-2]
                    alvo_i,alvo_j=i,j
        for r in range(0,(N//2)+(N%2)):
            for k in range(0,(N//2)+(N%2)):
                if "V"in mundo[(alvo_i+k)% N][(alvo_j+r)% N]:                
                    salas_livres[(alvo_i+k)% N][(alvo_j+r)% N]=[r+k]
                if "V"in mundo[(alvo_i+k)% N][(alvo_j-r)% N]:
                    salas_livres[(alvo_i+k)% N][(alvo_j-r)% N]=[r+k]
                if "V"in mundo[(alvo_i-r)% N][(alvo_j+k)% N]:
                    salas_livres[(alvo_i-r)% N][(alvo_j+k)% N]=[r+k]
                if "V"in mundo[(alvo_i-r)% N][(alvo_j-k)% N]: 
                    salas_livres[(alvo_i-r)% N][(alvo_j-k)% N]=[r+k]   
                    
                    
     
    # ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
    # O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
    # 
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)
        # elimine o teste abaixo quando tiver corrigido o bug de movimentação...
        if "I" in percepcao:
            print("Você bateu num muro e talvez não esteja mais na sala em que pensa estar...")
        # essa atualização abaixo serve de ilustração/exemplo, e
        # apenas marca as salas como "Visitadas", mas está errada
        pos = posicao
        ori = orientacao
        mundo[pos[0]][pos[1]] = ["V"]
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
    global N, mundo, posicao, orientacao, nFlechas, mundoCompartilhado,\
    salas_livres, plano, contador,contadorv2, ultimo_olfato
    #
    # Aplica a orientação e posição global  
    pos = posicao
    ori = orientacao
    #   
    # Caso plano 1 escolhe a acão "C"
    if plano==1:
        acao="C"   
    #     
    #   A função abaixo verefica os valores das casas ao redor do personagem
    # a fim de sempre escolher a mais proxima ou igual a 0 (ou -2,no caso do
    # Wumpus). 
    #   Os if`s abaixo de cada uma garantem que as casas -1, no sejam 
    # escolhidas na procura atribuindo valores acima de qualquer possibilidade
    # N+1.
    Dir=salas_livres[pos[0]][(pos[1]+1)%N]
    Direita=Dir[0]
    if Direita<0:
        Direita=N+1
        
    Bai=salas_livres[(pos[0]+1)%N][pos[1]]
    Baixo=Bai[0]
    if Baixo<0:
        Baixo=N+1
 
    Esq=salas_livres[pos[0]][(pos[1]-1)%N]
    Esquerda=Esq[0]
    if Esquerda<0:
        Esquerda=N+1

    Cim=salas_livres[(pos[0]-1)%N][pos[1]]
    Cima=Cim[0]
    if Cima<0:
        Cima=N+1
    # Escolhe um valor mínimo de busca
    n_direcao_objetivo=min(Direita,Baixo,Esquerda,Cima)
    #
    # Inicializa o processo de mobilização, certificando as prioridades de acao.
    if plano==0 or plano==2 or plano==3:
        pos_visao=[0,0]
   
        pos_visao[0] = (pos[0]+ori[0])%N
        pos_visao[1] = (pos[1]+ori[1])%N
     
        if salas_livres[pos_visao[0]][pos_visao[1]]==[n_direcao_objetivo] or\
        salas_livres[pos_visao[0]][pos_visao[1]]==[-2]:
            if salas_livres[pos_visao[0]][pos_visao[1]]==[-2] and plano==3 and\
            ("F" in ultimo_olfato):
                acao="T"
                plano=1
            else:
                acao="A"
        else:
            #Esses contadores alternam a o giro em horário/anti-horário.
            if contador>4:
                if contador>8:
                    contador=0
                acao="E"
            else:
                acao="D"
            contador+=1

      
    #
    # Adequa a posição de acordo com as ações.
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
        
    assert acao in ["A","D","E","T","C"]
    return acao
