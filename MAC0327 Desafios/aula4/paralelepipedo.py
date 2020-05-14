from math import sqrt
entrada = input()
entrada = list(map(int, entrada.split()))
z = int(sqrt((entrada[2]*entrada[1])/entrada[0]))
x = int(entrada[1]/z)
y = int(entrada[0]/x)

total = 4*(x + y + z)
print(total)