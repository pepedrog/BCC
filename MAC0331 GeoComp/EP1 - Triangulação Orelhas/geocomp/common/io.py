#!/usr/bin/env python
"""Modulo para leitura de um arquivo de dados"""

from geocomp.common.point   import Point
from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment
from geocomp.common.disc    import Disc


def read(filename):
    """Reads any type of geometric primitive data structures (Point,
    Polygon, Segment) from a file and returns it as a list.

    This method reads geometric data from a file. Any empty line or
    any line started by '#' (considered  a commentary) is ignored.
    The input can be mixed, it can contains a set of Polygons, Points
    and Segments and not necessarily only one type of data.

    The following patterns are required during the input operation:

    Point: defined by two floating point coordinates, on a line,
           separated by whitespaces. For example:

               0 0
               0.5 1.5
               1.5 3

    Polygon: defined by a list of adjacent points, enclosed by '['
             at the beginning and ']' at the end, in the order that
             they appear in the polygon boundary, i.e., any pair of
             consecutive points defines an edge on the polygon
             boundary. For example, the following input defines a
             square:

             [
             0 0
             1 0
             1 1
             0 1
             ]

    Segment: defined by four floating point coordinates, on a line,
             separated by whitespaces. Each pair of consecutive
             coordinates defines a segment endpoint. For example,
             the following input defines a segment from (0, 0) to
             (0.5, 1.5):

             0 0 0.5 1.5

     Disc: Atualmente, ele espera que o arquivo contenha uma lista de
           discos, um disco por linha, as 3 coordenadas em cada linha
           (x, y, r). Exemplo:
    
            0 0 0
            0 1 2
            10 100 50

    :param filename: (str) The name of the file that will be read

    :return: (list) A list of geometric primitive data structures
             read from the file

    Raises:
        FileNotFoundError: if file could not be found

        TypeError: if 'filename' is None

        ValueError: if some input from the file does not follow the
                    required patterns

    """
    with open(filename) as file:
        i = 0
        vertices = []
        data = []
        expecting_polygon = False
        for line in file:
            i += 1
            line = line.split()
            if len(line) == 0 or line[0] == "#":
                continue
            if line[0] == "[":
                expecting_polygon = True
            elif line[0] == "]":
                expecting_polygon = False
                data.append(Polygon(vertices))
                vertices = []
            elif len(line) == 3:
                data.append(Disc(float(line[0]), float(line[1]), float(line[2])))
            elif len(line) == 4:
                data.append(
                    Segment(
                        Point(float(line[0]), float(line[1])),
                        Point(float(line[2]), float(line[3]))
                    )
                )
            elif len(line) == 2:
                if expecting_polygon:
                    vertices.append(Point(float(line[0]), float(line[1])))
                else:
                    data.append(Point(float(line[0]), float(line[1])))
            else:
                raise ValueError(
                    "Invalid input from file: {}: line: {}: {}".format(filename, i, line))
        return data

# if __name__ == '__main__':
#     import sys
#
#     for i in sys.argv[1:]:
#         print((i,':'))
#         lista = read_points (i)
#         print(('  ',repr(len(lista)), 'pontos:'))
#         for p in lista:
#             print(p)
