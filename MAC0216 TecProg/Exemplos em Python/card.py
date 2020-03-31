class Carta:
    """
    Classe auxiliar para definição de uma carta
    """
    def __init__(self, n,v) :
        """n é o naipe e v é o valor"""
        self.naipe, self.valor  = n, v
    def __str__(self):
        return self.valor + " de " + self.naipe

