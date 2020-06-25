"""
    Implementação de uma DCEL (Double Connected Edge List)
    Uma lista de arestas duplamente ligadas para representar grafos planares
    
    A estrutura guarda, para cada vértice, uma meia aresta que tem ele como origem e para cada face,
    uma meia aresta da sua fronteira.
    
    Cada meia aresta guarda um ponteiro para a próxima e anterior, seus vértices,
    um ponteiro para sua aresta gêmea (ou outra meia aresta) e o índice da sua face
"""

from geocomp.common.prim import left, right
from geocomp.common.point import Point
from geocomp.common.control import plot_delete
from math import pi

#debug
from geocomp.common.control import sleep

class half_edge:
    " Classe da meia aresta "
    def __init__ (self, init, to, f, prox, prev, twin):
        self.init = init
        self.to = to
        self.f = f       # (face index)
        self.prox = prox
        self.prev = prev
        self.twin = twin 
        self.draw_id = None
    
    def __eq__ (self, other):
        return other != None and self.init == other.init and self.to == other.to
    
    def draw (self, color = "green"):
        self.hide()
        self.draw_id = self.init.lineto (self.to, color)
        self.twin.draw_id = self.draw_id

    def hide (self):
        if self.draw_id != None:
            plot_delete (self.draw_id)
            self.draw_id = self.twin.draw_id = None

    def close_circuit (self):
        " Indica se a aresta e faz parte de um circuito fechado (um polígono)"
        aux = self.prox
        while aux != self:
            if aux == self.twin:
                return False
            aux = aux.prox
        return True
    
    def __str__ (self):
        " String para testes "
        return str(self.init) + "->" + str(self.to)

class Dcel:
    def __init__ (self):
        self.v = dict()
        self.f = [None]
        # Alguma informação adicional vinculada a cada face
        # (Por exemplo o nó do DAG na triangulação de Delauney)
        self.extra_info = [None]
    
    def add_vertex (self, p):
        " Cria um novo vértice sem arestas na DCEL "
        self.v[p] = None
    
    def add_edge (self, v1, v2, f = None):
        " Adiciona uma meia-aresta v1-v2 e outra v2-v1 f é a face em que elas entrarão "
        # se a f é conhecida, consumo tempo proporcional a quantidade de vértices nessa face"
        # se f == None, consumo tempo proporcional ao grau de v1 + grau de v2 "

        # Cria as meias arestas
        e1 = half_edge (v1, v2, 0, None, None, None)
        e2 = half_edge (v2, v1, 0, None, None, e1)
        e1.twin = e2
        
        # Ajeita os ponteiros de prox e prev
        prox1 = self.__prox_edge (v1, v2, f)
        prox2 = self.__prox_edge (v2, v1, f)
        if prox1 == None:
            prox1 = e2
            prev2 = e1
        else:
            prev2 = prox1.prev
        if prox2 == None:
            prox2 = e1
            prev1 = e2
        else:
            prev1 = prox2.prev
        e1.prox = prox1
        e1.prev = prev1
        e2.prox = prox2
        e2.prev = prev2
        e1.prox.prev = e1
        e1.prev.prox = e1
        e2.prox.prev = e2
        e2.prev.prox = e2
        
        e1.f = e1.prox.f
        e2.f = e2.prox.f
        
        # Confere se criou uma nova face
        cc1 = e1.close_circuit()
        cc2 = e2.close_circuit()
        if cc1 and not cc2:
            self.f[e2.f] = e2
            self.__create_face (e1)
        if cc2:
            self.f[e1.f] = e1
            self.__create_face (e2)
            
        self.v[v1] = e1
        self.v[v2] = e2
        
        # Primeira Aresta adicionada
        if self.f[0] is None: self.f[0] = e1
            
        return e1

    def remove_edge (self, e):
        " Remove a meia aresta 'e' e sua gêmea "
        e.hide()
        # Remove = tira todas as referencias a ela
        e.prev.prox = e.twin.prox
        e.prox.prev = e.twin.prev
        e.twin.prox.prev = e.prev
        e.twin.prev.prox = e.prox 

        if self.v[e.init] == e: self.v[e.init] = e.prev.twin
        if self.v[e.to] == e.twin: self.v[e.to] = e.twin.prev.twin
        if self.f[e.f] == e: self.f[e.f] = e.prox
        if self.f[e.twin.f] == e.twin: self.f[e.twin.f] = e.twin.prox
        
        # Se continuei igual, então essa era a única aresta do vértice
        if self.v[e.init] == e: self.v[e.init] = None
        if self.v[e.to] == e.twin: self.v[e.to] = None
        
        # Confere se não extingui uma face
        if e.f != e.twin.f:
            self.__remove_face (e.f, e.twin.f)
    
    def __create_face (self, e):
        " Cria uma face após inserir uma aresta que a delimitou"
        new = len (self.f)
        e.f = new
        self.f.append (e)
        self.extra_info.append (None)
        aux = e.prox
        while aux != e:
            aux.f = new
            aux = aux.prox

    def __remove_face (self, removed, substitute):
        " Após remover uma aresta que uniu duas faces, "
        " faço todos da primeira face apontarem para segunda "
        if removed < substitute:
            removed, substitute = substitute, removed
        aux = self.f[removed].prox
        while aux != self.f[removed]:
            aux.f = substitute
            aux = aux.prox
        aux.f = substitute
        # Tira a face da lista de faces colocando a ultima no lugar dela
        if removed == len(self.f) - 1: 
            self.f.pop()
            self.extra_info.pop()
        else: 
            self.f[removed] = self.f.pop()
            aux = self.f[removed].prox
            while aux != self.f[removed]:
                aux.f = removed
                aux = aux.prox
            aux.f = removed
            self.extra_info[removed] = self.extra_info.pop()

    def __prox_edge (self, v1, v2, f):
        " Encontra a meia aresta que sai de v2 que deixa v1 a sua esquerda "
        # Se v2 não tem arestas
        if self.v[v2] is None:
            return None
        
        # Se conheço a face, busco nela
        if f != None:
            prox = self.f[f]
            while prox.init != v2:
                prox = prox.prox
            return prox
        
        # Se não conheço a face, busco nos vértices
        def angulo (v3):
            " Devolve algo proporcional ao angulo em v2 de v1-v2-v3 "
            # Vou achar, na verdade, o cosseno do angulo com a lei do cosseno
            a2 = (v3.x - v1.x)**2 + (v3.y - v1.y)**2
            b2 = (v3.x - v2.x)**2 + (v3.y - v2.y)**2
            c2 = (v1.x - v2.x)**2 + (v1.y - v2.y)**2
            ang = ((b2 + c2 - a2)/(2*((b2*c2)**0.5)))
            if right(v1, v2, v3):
                ang = - ang - 1000
            return -ang
    
        # Vou percorrer todas as arestas de v2 e achar a que forma angulo menor com v1-v2
        prox = self.v[v2]
        min_ang = angulo(prox.to)
        aux = prox.prev.twin
        while aux != self.v[v2]:
            ang_aux = angulo(aux.to)
            if ang_aux < min_ang:
                prox = aux
                min_ang = ang_aux
            aux = aux.prev.twin
            
        return prox
    
    def initPolygon (self, P):
        " Transforma o self numa dcel para o polígono P "
        v = P.vertices()
        self.add_vertex (v[0])
        for i in range (1, len(v)):
            self.add_vertex (v[i])
            self.add_edge (v[i - 1], v[i])
        self.add_edge (v[-1], v[0])
    
    def __str__ (self):
        " Representação em string para testes e debug "
        s = "Vértices\n"
        for p in self.v:
            s += str(p) + ":" + str(self.v[p]) + "\n"
        s += "\nFaces:\n"
        for i in range(len(self.f)):
            s += str(i) + ":" + str(self.f[i]) + "\n"
        return s
        