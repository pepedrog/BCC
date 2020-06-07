from . import brute_force
from. import bent_ott_mod

children = [('brute_force', 'Brute_force', 'Força\nBruta'),
            ('bent_ott_mod', 'Bentley_Ottmann_Mod', 'Bentley e Ottmann\nModificado')]

__all__ = [a[0] for a in children]
