# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:41:11 2018

@author: gigec
"""
global mundo, posicao, N, mapa_guiado

def inicializa():
    global mundo, posicao, N, mapa_guiado
    mundo = []
    N = 5
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mundo.append(linha)
        
    mapa_guiado = []
    for i in range(N) : 
        linha = []
        for j in range(N) : 
            linha.append([]) # começa com listas vazias
        mapa_guiado.append(linha)
    # posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
    posicao = [0,0]
    mundo[0][0] = ["V"]
    
    mundo[1][0] = mundo[2][0] = mundo[2][1] = mundo[3][1] = mundo[3][2] = mundo[4][2] = "V"

def numera_mapa(destino, i):
    global N, mundo, mapa_guiado, posicao
    
    mapa_guiado[destino[0]][destino[1]] = i
 
    
    posicoes_vizinhas = [[destino[0],(destino[1] + 1)%N],
                         [destino[0],(destino[1] - 1)%N],
                         [(destino[0] + 1)%N,destino[1]],
                         [(destino[0] - 1)%N,destino[1]]]
    
     
    print("Mundo conhecido pela personagem:")
    for m in range(len(mundo)):
        for j in range(len(mundo[0])):
            print(mapa_guiado[m][j],end="\t| ")          
        print("\n"+"-"*(8*len(mundo)+1))
    
    
    for vizinha in posicoes_vizinhas:
        if mundo[vizinha[0]][vizinha[1]] == "V" and type(mapa_guiado[vizinha[0]][vizinha[1]]) == list:# and mapa_guiado[vizinha[0]][vizinha[1] > i:
            i += 1
            numera_mapa(vizinha, i)
            print(vizinha, i)
    if vizinha == posicao:
        return
    
inicializa()
numera_mapa([4,3], 0)

                
    print("mapa guiado")
    for m in range(len(mundo)):
        for j in range(len(mundo[0])):
            print(mapa_guiado[m][j],end="\t| ")          
        print("\n"+"-"*(8*len(mundo)+1))
        
        
                          
    print("mapa do dummy")
    for m in range(len(mundo)):
        for j in range(len(mundo[0])):
            print(mundoCompartilhado[m][j],end="\t| ")          
        print("\n"+"-"*(8*len(mundo)+1))
        
    print("mapa guiado")
    for m in range(len(mundo)):
        for j in range(len(mundo[0])):
            print(mapa_guiado[m][j],end="\t| ")          
        print("\n"+"-"*(8*len(mundo)+1))
    
def define_caminho(destino, i):
    """ Função que encontra um caminho da posição atual até o destino e numera as salas,
        atualizando o mapa_guiado
        como no problema do rato 
    """
    global N, mundo, posicao, caminho
    fim_recursao = False
    if i == 0:
        fim_recursao = True
    mapa_guiado[destino[0]][destino[1]] = i
    i += 1

    posicoes_vizinhas = [[destino[0],(destino[1] + 1)%N],
                         [destino[0],(destino[1] - 1)%N],
                         [(destino[0] + 1)%N,destino[1]],
                         [(destino[0] - 1)%N,destino[1]]] 
    acessivel = False
    for vizinha in posicoes_vizinhas:
        #Se a sala for conhecidamente visitável e fizer parte de um caminho mais curto
        if "V" in mundo[vizinha[0]][vizinha[1]]:
            acessivel = True
            if (mapa_guiado[vizinha[0]][vizinha[1]] > i or mapa_guiado[vizinha[0]][vizinha[1]]==-1):
                define_caminho(vizinha, i)
            
    #Se estou tentando acessar uma sala livre inacessivel (passada pelo Dummy)
    #Quando já tiver completado as recursões,
    #Ou seja, quando o mapa estiver completo, achará o caminho     
    if fim_recursao: 
        caminho = []     
        
        print("mapa guiado")
        for m in range(len(mundo)):
            for j in range(len(mundo[0])):
                print(mapa_guiado[m][j],end="\t| ")          
            print("\n"+"-"*(8*len(mundo)+1))
        
        caminho_mais_curto(posicao)
    if not acessivel:
        return "inacessivel"
    if vizinha == posicao:
        return "acessivel"        
        
         self.mundo = [ [ MURO  , LIVRE , MURO  , MURO  , LIVRE  ],
                       [ LIVRE , LIVRE , MURO  , LIVRE , LIVRE  ],
                       [ LIVRE  , LIVRE , LIVRE , LIVRE , LIVRE   ],
                       [ WUMPUS, LIVRE , LIVRE , LIVRE , LIVRE  ],
                       [ LIVRE , LIVRE , LIVRE  , LIVRE , MURO   ] ]