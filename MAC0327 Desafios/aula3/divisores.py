n = int(input())
lista = input()
lista = list(map(int, lista.split()))

lista = sorted(lista)
i = -1;
x = lista[-1]
print(x,'', end = '')
while i < 0:
	if(lista[i] == lista[i - 1] or x%lista[i] != 0):
		print(lista[i])
		break
	i -= 1
		

	