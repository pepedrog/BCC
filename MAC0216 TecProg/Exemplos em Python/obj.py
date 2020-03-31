#!/usr/bin/env python3

class Ângulo :
    def __init__(self, g,m,s) :
        self.graus = g
        self.min   = m
        self.seg   = s

    def __repr__(self) :
        return "Ângulo(%4d,%2d,%2d)"%(self.graus, self.min, self.seg)

    def __str__(self) :
        return "%4dº %2d' %2d''"%(self.graus, self.min, self.seg)

    def __add__(self, outro) :
        sr = self.seg + outro.seg
        mr = self.min + outro.min  + sr//60
        sr %= 60
        gr = self.graus + outro.graus + mr // 60
        mr %= 60
        gr %= 360
        return Ângulo(gr,mr,sr)
    
class Astro:
    def __init__(self,n,a,d) :
        self.nome = n
        self.AR   = a
        self.Decl = d
        
    def imprime(self) :
        print("Nome: {}\n ({}, {})".format(\
            self.nome, self.AR.__repr__(), self.Decl.__repr__()))

class Estrela(Astro):
    def __init__(self, nome, a, d, tipo = 'G', temp=4000):
        super().__init__(nome,a,d)
        self.tipo = tipo
        self.temp = temp

    def imprime(self):
        super().imprime()
        print("Estrela do tipo {}\n          temp {}K\n".format(self.tipo,self.temp))
        
        
##################################################################################

# s = Estrela("Aldebaran", Ângulo(4, 0, 0), Ângulo( 12,12, 4),'K',  3910)
# e = Estrela("Sirius",    Ângulo(6,12, 4), Ângulo(-16,32,17), 'A', 9845) 
# l = Astro("Lua", Ângulo(4,25,5), Ângulo(2,12,31))
# s.imprime()
# e.imprime()
# l.imprime()

mapa = [Estrela("Alpha Crucis", Ângulo(12,4,4), Ângulo( -6,4,4)),
        Estrela("Antares",      Ângulo(16,4,4), Ângulo(-26,4,4)),
        Estrela("Betelgeuse",   Ângulo(20,4,4), Ângulo( 20,4,4)),
        Estrela("Rigel",        Ângulo(10,4,4), Ângulo( 10,4,4)),
        Astro("Lua", Ângulo(4,25,5), Ângulo(2,12,31))]

for ss in mapa :
    ss.imprime()
    
# a = Ângulo(30,4,15)
# print(a)
# b = a + Ângulo(10,8,50)            # vira a.__add__(outro)
# print(b)
# print(b+b)
