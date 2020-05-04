#!/usr/bin/env python
"""Algoritmo de Divisão e Conquista (Shamos e Hoey)"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.prim import *
import math

# distancia global para manter atualizada
d = float("inf")

def dist (par):
    " Retorna a comprimento ao quadrado do segmento par"
    " Se o segmento for um único ponto, retorna infinito, para consistencia"
    d2 = dist2 (par.init, par.to)
    if d2 > 0:
        return  d2
    return float("inf")

def minPar (a, b):
    " Recebe dois segmentos e retorna aquele com menor distancia "
    if (dist (a) < dist (b)):
        return a
    return b

def candidatos (l, i, j, meio):
    " Retorna uma lista dos pontos dentro da faixa [-d, +d] do ponto do leio da lista l[i:j] "
    global d
    cand = []
    for p in l[i:j]:
        if abs(p.x - meio.x) < d:
            cand.append (p)
    
    return cand

def menorInter (l, i, j, meio, par_min):
    " Retorna o par de pontos mais proximo dentro da faixa dada pelo ponto meio da lista "
    " e a distancia do min_par "
    global d
    
    blue = meio.hilight("blue")
    
    # desenha a faixa que eu estou procurando
    v1 = control.plot_vert_line (meio.x - d, "blue")
    v2 = control.plot_vert_line (meio.x + d, "blue")
    control.sleep()
    
    par_inter = None
    cand = candidatos (l, i, j, meio)
    
    for k in range(len(cand)):
        cyan = cand[k].hilight("cyan")
        for l in range(k + 1, len(cand)):
            
            # Se os pontos já estão distantes, posso parar de olhar
            if (cand[l].y - cand[k].y > d):
                break
            
            cand_inter = Segment (cand[k], cand[l])
            cand_inter.plot("cyan")
            control.sleep()
            cand_inter.hide()
            
            dcand = math.sqrt (dist2 (cand[k], cand[l]))
            # Se achei um novo par, apaga o outro e pinta esse
            if (dcand < d):
                d = dcand
                if par_inter != None:
                    par_inter.hide()
                par_inter = cand_inter
                par_inter.plot("blue")
                control.sleep()
            
        cand[k].unhilight(id = cyan)
    
    control.plot_delete (v1)
    control.plot_delete (v2)
    meio.unhilight(id = blue)
    control.sleep()
    
    return par_inter                

def intercalaY (l, i, j):
    " Função que recebe uma lista l[i:j] dividida em metades ordenadas e intercala "
    " as duas metades, é o intercala do mergeSort "
    meio = (i + j) // 2
    ini1 = i
    ini2 = meio
    
    aux = []
    while (ini1 < meio and ini2 < j):
        if l[ini1].y < l[ini2].y:
            aux.append(l[ini1])
            ini1 += 1
        else:
            aux.append(l[ini2])
            ini2 += 1
            
    # Copia a metade que falta no vetor
    while ini1 < meio:
        aux.append(l[ini1])
        ini1 += 1
    while ini2 < j:
        aux.append(l[ini2])
        ini2 += 1
    
    l[i:j] = aux[:]            

def ShamosRec (l, i, j):
    " Função que faz o serviço recursivo " 
    " recebe uma lista de pontos l[i:j] ordenados pela coordenada x "
    # Base da recursão, 2 ou 1 ponto
    if j - i < 3:
        # registra o par mais proximo
        par_min = Segment(l[i], l[j - 1])
        # Ordena pelo eixo y
        if (l[i].y > l[j - 1].y):
            l[i], l[j - 1] = l[j - 1], l[i]
    else:
        q = (i + j) // 2
        meio = l[q]
        
        vert_id = control.plot_vert_line(meio.x)
        verde = meio.hilight()
        control.sleep()
        
        # Calcula o menor das duas metades
        par_esq = ShamosRec (l, i, q)
        par_dir = ShamosRec (l, q, j)
        
        par_min = minPar (par_esq, par_dir)
        
        # Intercala do mergeSort escondido
        intercalaY (l, i, j)
        
        control.plot_delete (vert_id)
        meio.unhilight(id = verde)
        
        # Calcula o menor entre as duas metade
        par_inter = menorInter (l, i, j, meio, par_min)
        if par_inter != None:
            par_min = minPar (par_inter, par_min)
            par_inter.hide()
            
        par_esq.unhilight()
        par_dir.unhilight()
    
    global d
    dnovo = math.sqrt (dist (par_min))
    d = min (d, dnovo)
    
    par_min.hilight("red")
    control.sleep()
    return par_min

def pontosRepetidos (l):
    " Verifica se há pontos coincidentes em l "
    for i in range (1, len (l)):
        l[i].hilight('green')
        control.sleep()
        if l[i] == l[i - 1]:
            l[i].hilight('red')
            return True
        l[i].unhilight()
    return False

def Shamos (l):
    "Algoritmo de divisão e conquista para encontrar o par de pontos mais proximo"
    "Recebe uma lista de pontos l"         

    if len (l) < 2: return None
    
    global d
    d = float("inf")
    
    l = sorted(l, key = lambda x:x.x)
    
    if not pontosRepetidos(l):
        ShamosRec (l, 0, len(l))