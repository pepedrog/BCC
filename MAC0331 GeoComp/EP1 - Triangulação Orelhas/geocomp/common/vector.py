import math

class Vector:
    """ Immutable vector structure. """

    __vector_type_exception = Exception('Values can be of type (int, float)')
    __vector_accepted_types = (int, float)

    __slots__ = ('values', '_norm', '_cached_norm')

    def __init__(self, args):
        if not hasattr(args, '__iter__'):
            raise Exception('Argument of vector must be iterable')
        self.values = tuple(args)
        self._norm = 0
        self._cached_norm = False
        assert all(type(item) in self.__vector_accepted_types for item in self.values), self.__vector_type_exception

    @classmethod
    def normalized(cls, args):
        if not hasattr(args, '__iter__'):
            raise Exception('Argument of vector.normalize must be iterable')
        assert all(type(item) in cls.__vector_accepted_types for item in args), cls.__vector_type_exception

        norm = cls.__get_norm(args)
        inverted_norm = 1.0 / norm
        v = cls(value * inverted_norm for value in args)
        v._norm = norm
        v._cached_norm = True
        return v

    @classmethod
    def from_angle(cls, angle):
        return cls((math.cos(angle), math.sin(angle)))

    @property
    def dimension(self):
        return len(self.values)

    @property
    def norm(self):
        if self._cached_norm:
            return self._norm
        norm = self.__get_norm(self.values)
        self._norm = norm
        self._cached_norm = True
        return norm

    def __len__(self):
        return len(self.values)
    
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise Exception('{} is not vector'.format(other))
        if self.dimension != other.dimension:
            raise Exception('{} has dimension != {}'.format(other, self.dimension))

        return Vector(i + j for i, j in zip(self, other))

    def __str__(self):
        return '<Vector dim={} values={}>'.format(self.dimension, self.values)

    def __mul__(self, x):
        if type(x) not in self.__vector_accepted_types:
            raise Exception('Cannot multiply {} with a Vector'.format(type(x)))
        
        return Vector(x * value for value in self.values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, key):
        return self.values[key]

    @classmethod
    def __get_norm(cls, values):
        return sum(i**2 for i in values)**0.5