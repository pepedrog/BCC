# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Par Mais Proximo:

Dado um conjunto de pontos S, determinar dois cuja distancia entre eles seja minima

Algoritmos disponveis:
- Forca bruta
"""
from . import brute
from . import shamos
from . import varredura

children = [
	[ 'brute', 'Brute', 'Forca Bruta' ],
    [ 'shamos', 'Shamos', 'Divisão e Conquista' ],
    [ 'varredura', 'Varre', 'Linha de Varredura' ]
]

__all__ = [a[0] for a in children]
