from geocomp.common.point import Point
from geocomp.common.abbb import Abbb
from geocomp.common.prim import left, area2
from geocomp.common import control

# Esse funciona em muitos casos,
# Algo acontece no exemplo seg1 que dá errado
# Eu descofio que é por causa que a árvore meche muito e daí
# a comparação assimétrica impede de achar as coisas
# (eu tentei consertar isso e não consertou 100%, ainda tem que debugar mais)

# pode ser que seja por conta de erro numérico
# pode ser por conta de pontos que intersectam mais de 2 segmentos
# ou pode ser por conta dos segmentos verticais
# Boa sorte pra quem quiser debugar isso

# Toda via, em casos com muitos segmentos (e muitas interseções) 
# eu recomendo usar o bom e velho força bruta, que é assintoticamente melhor nesses casos

# Precisão pro ponto flutuante
eps = 1e-7

class Node_Point:
    " Classe que será nosso nó na ABBB de pontos-eventos "  
    " guarda um ponto e os segmentos que ele pertence "
    def __init__ (self, ponto, ini, fim, inter):
        self.ponto = ponto
        self.ini = ini # lista dos segmentos que esse ponto é o ponto da esquerda
        self.fim = fim # lista dos segmentos que esse ponto é o ponto da direita
        self.inter = inter # lista dos segmentos que esse ponto é de um ponto de interseção
        
    def __eq__ (self, other):
        return other != None and self.ponto.approx_equals (other.ponto)
    
    # Ordem que usaremos na ABBB, da esquerda pra direita, de baixo pra cima    
    def __gt__ (self, other):
        return (self.ponto.x - other.ponto.x > eps or
                (abs(self.ponto.x - other.ponto.x) < eps and self.ponto.y - other.ponto.y > eps))
    
class Node_Seg:
    " Classe que será o nó na nossa ABBB da linha de varredura "
    " Guarda um segmento e seu ponto de referencia"
    def __init__(self, seg, ref):
        self.seg = seg
        self.ref = ref # Ponto de referência para percorrer a abbb
            
    def __eq__ (self, other):
        return other != None and self.seg == other.seg
    
    # Ordem que usaremos na linha de varredura    
    def __gt__ (self, other):
        ref = other.ref
        # Se o ponto de referencia é uma interseção, 
        if abs(area2 (self.seg.init, self.seg.to, ref)) < eps:
            # O ponto de referência vai ser o ponto da direita
            ref = other.seg.to
        
        # Self > other <=> other está a esquerda do self
        return left (self.seg.init, self.seg.to, ref)
    
    def __str__ (self):
        return str(self.seg) + " " + str (self.ref)

def eventos (segmentos):
    "Função que retorna uma ABBB de pontos-eventos, que são os extremos horizontais dos circulos"
    
    Q = Abbb () # Abbb dos pontos eventos
    
    for s in segmentos:
        
        if s.init.x > s.to.x:
            s.init, s.to = s.to, s.init
        
        no_seg = Node_Seg (s, s.init)
        
        p1 = Node_Point (s.init, ini = [no_seg], fim = [], inter = [])
        p2 = Node_Point (s.to, ini = [], fim = [no_seg], inter = [])
        
        no1 = Q.busca (p1)
        no2 = Q.busca (p2)
        
        # Se os pontos já estão inseridos, só atualiza, se não, insere
        if no1.elemento != None:  
            no1.elemento.ini.append (no_seg)
        else:
            Q.insere (p1)
            p1.ponto.plot (color = 'blue')
            
        if no2.elemento != None:
            no2.elemento.fim.append (no_seg)
        else:
            Q.insere (p2)
            p2.ponto.plot (color = 'blue')
        
    return Q

def marca_intersec (no1, no2, pontos, x = None):
    "Testa se há interseção entre o nó1 e o nó2 e adiciona em pontos, se houver"
    "E só marca as interseções que ocorrem do x pra direita"
    
    # Despinta de verde e pinta de amarelo
    no1.seg.hide()
    no2.seg.hide()
    no1.seg.plot ("yellow")
    no2.seg.plot ("yellow")
    control.sleep()
    # despinta de amarelo e pinta de verde denovo
    no1.seg.hide()
    no2.seg.hide()
    no1.seg.plot ("green")
    no2.seg.plot ("green")
    
    p = no1.seg.intersection (no2.seg)
    # Só marco se o o ponto esta pra frente do x especificado
    if (p != None and (x == None or p.x > x)):
        # Crio o nó
        p_no = Node_Point (p, ini = [], fim = [], inter = [no1, no2])
            
        # insere o ponto na arvore, ou só atualiza se ele já existir
        p_no_abb = pontos.busca (p_no)
        if p_no_abb.elemento == None:
            pontos.insere (p_no)
            p_no.ponto.plot('blue') 
        else:
            if no1 not in p_no_abb.elemento.inter:
                p_no_abb.elemento.inter.append (no1)
            if no2 not in p_no_abb.elemento.inter:
                p_no_abb.elemento.inter.append (no2)
                    
    control.sleep()
    
def insere_na_linha (L, no, pontos, x = None, trocados = []):
    "Insere o nó na linha de varredura L e testa as interseções com consecutivos "
    "Mas só marca as interseções que ocorrem do x pra frente e que não se repetem nos trocados"
    
    L.insere (no)
    
    pred = L.predecessor (no)
    suc = L.sucessor (no)
    
    if pred != None and (trocados == [] or pred not in trocados):
        marca_intersec (no, pred, pontos, x)
    if suc != None and (trocados == [] or suc not in trocados):
        marca_intersec (no, suc, pontos, x)
    
def deleta_da_linha (L, no, pontos, x = None):
    "Deleta o nó da linha de varredura L e testa a interseção entre os que ficaram consecutivos"
    "Mas só marca as interseções que ocorrem do x pra frente"
    
    pred = L.predecessor (no)
    suc = L.sucessor (no)
    L.deleta (no)
    no.seg.hide()
    control.sleep()
    
    if pred != None and suc != None and pred != suc:
        marca_intersec (pred, suc, pontos, x)

def Bentley_Ottmann (l):
    
    L = Abbb () # Linha de varredura
    resp = [] # Os nós com os pontos de interseção que retornaremos
    
    # Pré-processamento - Transforma cada circulo em pontos-eventos
    # pontos é a ABBB de pontos eventos
    pontos = eventos (l)
    control.sleep()
    
    while not pontos.vazia():
        p = pontos.deleta_min()
        # desenha a linha
        id_linha = control.plot_vert_line (p.ponto.x)
        id_evento = p.ponto.hilight()
        control.sleep()
        
        "------------------------- Pontos da esquerda --------------------------------"
        for seg in p.ini:
            seg.seg.plot ("green")
            control.sleep()
            insere_na_linha (L, seg, pontos, p.ponto.x)
         
        "------------------------- Pontos de interseção ------------------------------"
        if len (p.inter) > 0 or (len (p.ini) + len (p.fim) > 1):
            p.ponto.hilight('yellow')
            resp.append (p)
            
        # Troca a ordem dos segmentos (do p.inter[])
        trocados = []
        # Remove todos
        for seg in p.inter:
            seg.ref = Point (p.ponto.x - 10*eps, ((seg.seg.to.x*seg.seg.init.y) -
                                                 (seg.seg.init.x*seg.seg.to.y) -
                                                 (p.ponto.x - 10*eps)*(seg.seg.init.y - seg.seg.to.y)) / 
                                                 (seg.seg.to.x - seg.seg.init.x))
            trocados.append (seg)
            L.deleta (seg)
        # Insere denovo com o novo ponto de referencia
        for seg in trocados:
            seg.ref = p.ponto
            #print("reinserindo " + str(seg))
            insere_na_linha (L, seg, pontos, p.ponto.x, trocados)
        
        "------------------------- Pontos da direita --------------------------------"
        for seg in p.fim:
            deleta_da_linha (L, seg, pontos, p.ponto.x)
            
        # apaga a linha
        control.plot_delete (id_linha)    
        control.plot_delete (id_evento)
        p.ponto.unplot()

    return resp