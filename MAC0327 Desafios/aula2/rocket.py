entrada = input();
entrada = entrada.split();
n = int(entrada[0])
k = int(entrada[-1])
s = input()

s = sorted(s)
ant = 0
r = 0
for letra in s :
	if(ord(letra) - ant > 1):
		r += (ord(letra) - 96)
		ant = ord(letra)
		k -= 1
		if(k == 0):
			break
		

	

if(k == 0):
	print(r)
else:
	print(-1)
