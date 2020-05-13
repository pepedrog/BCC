s = input()
s = list(s)
uns = 0
for n in s:
	if(n == '1'):
		uns += 1
aindanao = 1
for a in s:
	if(a == '2' and aindanao):
		aindanao = 0
		for i in range(uns):
			print('1', end = '')
	if(a != '1'):
		print(a, end = '');
if(aindanao):
		aindanao = 0
		for i in range(uns):
			print('1', end = '')
print()
