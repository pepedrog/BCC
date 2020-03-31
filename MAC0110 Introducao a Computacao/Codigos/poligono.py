
# usamos um pouco de trigonometria para relacionar ângulos e lados de polígonos
from math import sin, pi

class poligono:
    """ Classe poligono: coleção de objetos associados a polígonos
        regulares no plano. Cada uma destas figuras é definida pelos
        atributos nlados (número de lados), raio (da circunferência
        onde a figura se inscreve, que é também a distância entre o
        centro do polígono e qualquer um de seus vértices) e nome
        (normalmente um número em Grego mais o sufixo -gono=ângulo,
        como "pentágono", "dodecágono", "icoságono" ou
        "diacosipentacontaheptágono").  Outros valores que são
        característicos dos polígonos regulares, tais como ângulo
        interno, lado ou perímetro, são computados a partir dos
        atributos básicos.
    """
    
    def __init__(self,nlados,raio,nome):
        """ Construtor da classe poligono: recebe os atributos essenciais
            que definem essas figuras.
        """
        self.nlados = nlados
        self.raio = raio
        self.nome = nome

    def __str__(self):
        """ Conversão implícita para string: define a maneira de apresentar
            o objeto quando chamamos print(objeto).
        """
        return  "Olá, eu sou um objeto da classe polígono! "+\
                "Meu nome é "+self.nome+ \
                ", eu sou um polígono de "+\
                str(self.nlados)+ \
                " lados de comprimento "+ \
                str(self.lado())+", com ângulos internos de " \
                +str(self.angulo())+" graus "+\
                "e perímetro de "+str(self.perimetro())+\
                ", inscrito em uma circunferência de raio "+ \
                str(self.raio)+".\n"
                
    def angulo(self):
        """ método ângulo: ângulo interno a cada vértice.
        """
        return 180-360/self.nlados

    def lado(self):
        """ método lado: medida de cada lado do polígono.
        """
        return 2*self.raio*sin(pi/self.nlados)

    def perimetro(self):
        """ método perímetro: soma de todos os lados.
        """
        return self.nlados*self.lado()

# cria alguns objetos poligonais
t = poligono(3,1,"triângulo")
print(t)
q = poligono(4,1,"quadrado")
print(q)
p = poligono(5,1,"pentágono")
print(p)
d = poligono(12,1,"dodecágono")
print(d)
i = poligono(20,1,"icoságono")
print(i)
dph = poligono(257,1,"diacosipentacontaheptágono")
print(dph)
print("Observe:")
print("\tcomo o perímetro se aproxima da circunferência;")
print("\tcomo o ângulo interno se aproxima de 180 graus; e")
print("\tcomo o lado tende a 0.")

