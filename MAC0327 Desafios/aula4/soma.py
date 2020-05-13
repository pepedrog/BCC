def S(n):
	soma = 0
	while(n >= 10):
		soma += n%(10)
		n = int(n/10)
	soma+=n
	return soma

n = input()
tamanho = len(n)
n = int(n)

a = 0
for i in range(tamanho - 1):
	a += 9*(10**i)
	
b = n - a

print(S(a) + S(b))