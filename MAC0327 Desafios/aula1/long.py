n = input()
for i in range(int(n)):
	s = input()
	tam = len(s)
	if tam > 10: 
		print(s[0], tam - 2, s[-1], sep = '')
	else:
		print(s)