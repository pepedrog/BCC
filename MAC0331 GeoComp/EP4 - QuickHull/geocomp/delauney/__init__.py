# -*- coding: utf-8 -*-
"""Algoritmos para o problema da Triangulação de Delauney
"""
from . import incremental
from . import incremental_dag

children = [
	[ 'incremental', 'Incremental', 'Incremental' ],
    [ 'incremental_dag', 'Incremental', 'Incremental\nMostrando Busca' ]
]

__all__ = [a[0] for a in children]
