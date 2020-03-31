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
   
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mundo.append(linha)
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    orientacao = [1,0]
    
def LifeFindsAWay(Mapa):#Cria o caminho indicando a distancia até um 'L' 
            #Faz como no exercicio do rato mas o Queijo são todos os 'L' restantes
            global n, mundo, orientacao, posicao            
            ThePlaceIWannaBe=0 #valor que o 'V' tem no Mapa
            DoIKnoDaWae=False 
            while DoIKnoDaWae == False:                
                ThePlaceIWannaBe+=1#Valor que o "L' tem no mapa na primeira execução do loop. No caso 'L' = 1
                ShitsDoneYo=0                
                for r in range(N):
                    for k in range(N):                     
                       if Mapa[r][k]== ThePlaceIWannaBe:
                           Hood=[Mapa[(r+1)%N][k], Mapa[(r-1)%N][k], Mapa[r][(k+1)%N], Mapa[r][(k-1)%N]]#cha os adjacentes...                           
                           for l in range(4):#...e corrige o valor adicionando +1 em relação a casa adjacnete
                               if Hood[l]== 0:
                                   Hood[l]= ThePlaceIWannaBe+1
                                   ShitsDoneYo+=1 
                               elif Hood[l]>ThePlaceIWannaBe :                                   
                                   Hood[l]=ThePlaceIWannaBe+1
                                   ShitsDoneYo+=1 
                           Mapa[(r+1)%N][k], Mapa[(r-1)%N][k], Mapa[r][(k+1)%N], Mapa[r][(k-1)%N]=Hood[0],Hood[1],Hood[2],Hood[3]                                    
                if ShitsDoneYo==0:#se não fizer nenhuma busca, para o laco.
                    DoIKnoDaWae=True
            return Mapa
        
def Map():#Cria uma versão do mundo trocando os valores de 'V','L','M','W','W?','P' e 'P?'
        global mundoCompartilhado
        Mapa=[]
        for i in range(N):
            linha =[]
            for j in range(N):
                linha.append([])
            Mapa.append(linha)         
        for r in range(N):
            for k in range(N):
                if mundo[r][k]==['V']: 
                    Mapa[r][k]=0 
                if mundo[r][k]==['L']:
                    Mapa[r][k]= 1                      
                if mundo[r][k]!=['V'] and mundo[r][k]!=['L']:
                    Mapa[r][k]=-1
                    if mundo[r][k]==['W']:
                        Mapa[r][k]=-2 
       
        return Mapa 
    
def Move(Mapa):#Compara os valores vizinhos e direciona o personagem na direção do menor valor...
     pos = posicao
     ori = orientacao   
     vizinhos=[Mapa[(pos[0]+1)%N][pos[1]],Mapa[pos[0]][(pos[1]+1)%N],Mapa[(pos[0]-1)][pos[1]],Mapa[pos[0]][(pos[1]-1)%N]]
     minimo = Mapa[pos[0]][pos[1]]
     for i in range(len(vizinhos)):
        if vizinhos[i] > 0 and vizinhos[i] < minimo:
                minimo = vizinhos[i]       
     if Mapa[(pos[0]+ori[0])%len(Mapa)][(pos[1]+ori[1])%len(Mapa)] != minimo:
         acao='E'     
     if Mapa[(pos[0]+ori[0])%len(Mapa)][(pos[1]+ori[1])%len(Mapa)] == minimo:
         acao='A'             
     #...além de tentar matar o Wumpus se a casa da frente for a do Wumpus enquanto ele gira e tiver flechas.
     if Mapa[(pos[0]+ori[0])%len(Mapa)][(pos[1]+ori[1])%len(Mapa)] == -2 and nFlechas>0:
         acao='T'
     return acao       
FalarComAmiguinho="N"  
    
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
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, FalarComAmiguinho
    # Atualiza representação local do mundo (na visão da personagem).
    # Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
    # Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
    # "B" para brisa, "F" para fedor, "L" para salas livres,
    # "M" para muros e "V" para salas visitadas.
    
    
    pos = posicao
    ori = orientacao
    mundo[pos[0]][pos[1]] = ["V"]                             
    adjacentes=[mundo[(pos[0]+1)%N][pos[1]],mundo[pos[0]][(pos[1]+1)%N],mundo[(pos[0]-1)][pos[1]],mundo[pos[0]][(pos[1]-1)%N]]                         
   
    if 'I' in percepcao:#ajusta a posição após o impacto e re-define as salas vizinhas para a posição correta
        pos[0] = (pos[0]-ori[0])%len(mundo)
        pos[1] = (pos[1]-ori[1])%len(mundo)  
        adjacentes=[mundo[(pos[0]+1)%N][pos[1]],mundo[pos[0]][(pos[1]+1)%N],mundo[(pos[0]-1)][pos[1]],mundo[pos[0]][(pos[1]-1)%N]]                                                                                       
   
    if percepcao==[]: #ve se tem alguma coisa em volta e marca 'L' quando não tiver                              
        for q in range(4):
           if adjacentes[q] != ['L'] and adjacentes[q] != ['V'] and adjacentes[q] != ['M'] and adjacentes[q] != ['W'] and adjacentes[q] != ['B']:
               adjacentes[q]=['L'] 
              
    if 'F' in percepcao:
        Wfinder=0# conta quantas casas diferentes de W? tem em volta...          
        for q in range(4):
            if adjacentes[q]==['L'] or adjacentes[q] == ['V'] or adjacentes[q] == ['M'] or adjacentes[q] == ['B']:
                Wfinder+=1
            if adjacentes[q] != ['L'] and adjacentes[q] != ['V'] and adjacentes[q] != ['M'] and adjacentes[q] != ['W'] and adjacentes[q] != ['B']:
                adjacentes[q]=['W?']               
        if Wfinder==3: #...e se tiver 3, marca a casa W? como o Wumpus.                 
            for w in range(4):
                if adjacentes[w]==['W?']:
                    adjacentes[w]=['W']
                    break 
                
    if 'B' in percepcao:        
         Pfinder=0# conta quantas casas diferentes de P? tem em volta...         
         for q in range(4):  
             if adjacentes[q]==['L'] or adjacentes[q] == ['V'] or adjacentes[q] == ['M'] or adjacentes[q] == ['B']:
                Pfinder+=1
             if adjacentes[q] != ['L'] and adjacentes[q] != ['V'] and adjacentes[q] != ['M'] and adjacentes[q] != ['W'] and adjacentes[q] != ['B']:
                adjacentes[q]=['P?']         
         if Pfinder==3:#...e se tiver 3, marca a casa P? como o poço.            
            for w in range(4):
                if adjacentes[w]==['P?']:
                    adjacentes[w]=['P']

        
    #if 'U' in percepcao:
       # Yay i guess :D =True 
        
    #Este bloco realoca os valores para as salas adjacentes em relação ao mundo.                         
    mundo[(pos[0]+1)%N][pos[1]]=adjacentes[0]
    mundo[pos[0]][(pos[1]+1)%N]=adjacentes[1]
    mundo[(pos[0]-1)][pos[1]]=adjacentes[2]
    mundo[pos[0]][(pos[1]-1)%N]=adjacentes[3]
  
    if 'I' in percepcao:#coloca o Muro depois de se resolverem as outras percepções. 
        mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)] = ['M']
 
    if __DEBUG__:
        print("Percepção recebida pela personagem:")
        print(percepcao)                           
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
    
    #Estabelce a condição de Compartilhamento vendo se existe um item com len()>2, ou seja qualquer que seja o nome da personagem     
    for k in range(len(percepcao)):                  
           if len(percepcao[k])>2:
               FalarComAmiguinho='C'               
               break
           if len(percepcao[k])<2:
               FalarComAmiguinho='N'
    if percepcao==[]:
        FalarComAmiguinho='N'
               
def agir():
    """ Nessa função a personagem deve usar seu conhecimento
        do mundo para decidir e tentar executar (devolver) uma ação.
        Possíveis ações (valores de retorno da função) são
        "A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
        "T"=aTirar e "C"=Compartilhar.
    """
    # declara as variáveis globais que serão acessadas
    global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, FalarComAmiguinho
    pos = posicao
    ori = orientacao 
    Mapa=LifeFindsAWay(Map()) 
    print(Mapa)
    print(FalarComAmiguinho)
    #acao=input('Qual ação: ')      
    acao=Move(Mapa)
    if FalarComAmiguinho == 'C' :
        acao='C' 
    else:
        FalarComAmiguinho='N'
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
