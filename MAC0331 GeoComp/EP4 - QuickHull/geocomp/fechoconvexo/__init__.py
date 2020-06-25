# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Fecho Convexo 2D:

Algoritmos disponveis:
- QuickHull
"""
from . import quickhull

children = [
	[ 'quickhull', 'quickhull', 'QuickHull' ]
]

__all__ = [a[0] for a in children]
