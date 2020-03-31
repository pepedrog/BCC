# flag para depuração
__DEBUG__ = True


# Variaveis globais (do módulo) que o mundo acessa para passar informações para a personagem.

global nFlechas
"""
Número de flechas que a personagem possui. Serve apenas para
consulta da personagem, pois o mundo mantém uma cópia "segura" dessa
informação (não tente inventar flechas...).
"""

global mundoCompartilhado
"""
Esse é um espaço onde a personagem tem acesso à representação do
mundo de uma outra personagem.  Essa informação pode ser usada como a
personagem quiser (por exemplo, transferindo o conteúdo para o seu
próprio "mundo", ou mantendo uma lista dos vários mundos
compartilhados com outras personagens).
"""


# Outras variáveis globais do módulo personagemNUSP

global salaLivre
"""
Lista com as coordenadas de salas nao visitadas. Essa lista
esta de acordo com a matriz mundo, ou seja, a coordenada [0,1] se 
relaciona com a linha 0 e coluna 1 de mundo.
"""

global outraPersonagem
"""
Flag acionada caso haja o encontro com outro personagem no mundo, o que
habilitara a troca de informaçoes sobre o mundo.
"""

global andando
"""
Flag acionada caso a personagem esteja andando, seja para chegar a um
Wumpus, seja para chegar a uma sala livre.
"""

global listaCaminho
"""
Contem lista com a sequencia de salas necessarias para se chegar a uma
determinada sala
"""

global contadorWumpus
"""
Armazena a contagem de Wumpus encontrados no mundo.
"""

global ref
"""
Ponteiro utilizado para os testes de caso da possiblidade de se chegar
a uma sala da lista de salas livres
"""

global contaG
"""
Contador usado para armazenar o numero de giros que ja se deu em uma 
sala, ou seja, se ele ja viu se alguma das suas adjacencias sao livres.
Quando excedido o numero limite, a personagem tem que achar um caminho
ate uma casa livre.
"""

global N
""" Dimensão do mundo.
"""

global mundo
"""
Representa o conhecimento da personagem em relação ao Mundo de
Wumpus. Essa é uma matriz de NxN onde a personagem toma notas de suas
percepções ao longo do caminho que percorre, indicando os muros, as
salas livres e as salas percorridas, bem como a proximidade de perigos
(poços e Wumpus). A geometria do mundo é a de um toro (aquela figura
que parece um donut!) onde existem sempre 4 salas vizinhas à posição
[i][j]: em sentido horário e a partir da (nossa) direita essas seriam:
[i][(j+1)%N], [(i+1)%N][j], [i][(j-1)%N] e [(i-1)%N][j]. Cada entrada
mundo[i][j] é uma lista de anotações/rótulos correspondentes às
informações encontradas ou deduzidas pela personagem sobre o conteúdo
da sala (i,j).
"""

global posicao
"""
Representa a posição relativa da personagem no mundo. Cada
personagem começa em uma posição aleatória (e desconhecida por ela,
pois não possui GPS ou equivalente) do Mundo "real" de Wumpus, e por
isso precisa usar um sistema de coordenadas pessoal para se orientar.
Por convenção, sua posição inicial é representada como [0,0] (canto
superior esquerdo) nesse sistema. Como o mundo não tem bordas, podemos
usar sempre os i=0,...,N-1 e j=0,...,N-1, que percorrem todas as salas
possíveis do Mundo de Wumpus, usando o operador módulo (%) para
corrigir a posição quando um passo nos levar a uma sala de índice <0
ou >=N.
"""

global orientacao
"""
Juntamente com a posição relativa, permite à personagem manter o
histórico das salas visitadas. Essa orientação é independente da
orientação "real" que o mundo usa para coordenar a ação de todas as
personagens. Por convenção, todas as personagens indicam sua orientação
inicial como "para baixo" ou "sul", correspondente à direção [1,0]
(direção do eixo vertical).
"""


def inicializa(tamanho):
	""" Função de inicialização da personagem (recebe o tamanho do mundo).
		Usa as variáveis globais (do módulo) para representar seu
		conhecimento do mundo, sua posição e sua orientação relativas
		ao início da simulação. Você pode criar e inicializar outras
		variáveis aqui (por exemplo, a lista de salas livres e não
		visitadas).

	"""
	# declara as variáveis globais que serão acessadas
	global N, mundo, posicao, orientacao, salaLivre, outraPersonagem, andando, contadorWumpus, ref, contaG
	# guarda o tamanho do mundo
	N = tamanho
	# cria a matriz NxN com a representação do mundo conhecido
	mundo = []
	for i in range(N) : 
		linha = []
		for j in range(N) : 
			linha.append([]) # começa com listas vazias
		mundo.append(linha)

	# posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
	posicao = [0,0]
	orientacao = [1,0]
	salaLivre = [[0,0]]
	outraPersonagem = False
	andando = False
	contadorWumpus = 0
	ref = 0
	contaG = 0

def busca(ld, cd):
	"""
	funcao que percorre o mundo em busca de um determinado caminho
	n = dimensao do mundo; lp e cp = linha e coluna do personagem;
	ld e cd = linha e coluna do destino. Retorna uma lista com as 
	salas a serem percorridas para que se chega ao destino, e -1
	caso nao seja possivel calcular um caminho
	"""

	global posicao, N, listaCaminho

	#Sequencia de salas que definem o percurso a ser percorrido
	listaCaminho = [] 

	#pegando a atual posicao da personagem
	lp, cp = posicao[0], posicao[1]

	#Listas para auxiliar com salas ortogonais
	vl = [-1,0,1,0]
	vc = [0,1,0,-1]

	#Inicializando listas que representam o modo iterativo da funcao
	filaL = []
	filaC = []
	for i in range(N*N):
		filaL.append(0)
		filaC.append(0)

	#Inicializando uma matriz que vai servir de base para a mediçao dos caminhos
	caminho = []
	for i in range(N): 
		linha = []
		for j in range(N): 
			linha.append(0) 
		caminho.append(linha)

	#Atribuindo valores as listas iterativas e as variveis iniciais
	caminho[ld][cd] = 1;
	inicio = 0
	fim = 1
	filaL[1] = ld
	filaC[1] = cd
	l = ld
	c = cd

	#Equanto for possivel atribuir novos caminhos, ira executar o loop.
	#Este passo consiste em verificar se as quatro salas adjacentes a uma
	#outra sao "andaveis", isto e, nao representam perigo. Ao passo que, 
	#caso seja possivel andar por ela, sera atribuido um valor correspondente
	#ao numero de salas percorridas para se chegar a sala anterior, mais 1.
	while inicio < fim:
		inicio += 1
		l = filaL[inicio]
		c = filaC[inicio]
		num = caminho[l][c] + 1
		for i in range(4):
			lin = (l + vl[i])%N
			col = (c + vc[i])%N
			if caminho[lin][col] == 0 and ("V" in mundo[lin][col] or "L" in mundo[lin][col]):
				caminho[lin][col] = num;
				fim += 1
				filaL[fim] = lin 
				filaC[fim] = col

	l = lp
	c = cp
	num = caminho[l][c] - 1 

	#Neste loop, a matriz com o numero de casas que devem ser percorridas para se chegar a cada 
	#ponto ja foi definida. Este passo consiste em sair da sala atual da personagem, que apresenta
	#um valor de salas necessarias para se chegar la, e ir percorrendo as salas com valores 
	#decrementados, ate se chegar a sala de destino.
	while num > 1:
		k = 0
		achou = False
		while k < 4 and not achou:
			lin = (l + vl[k])%N
			col = (c + vc[k])%N
			if caminho[lin][col] == num:
				achou = True
				listaCaminho.append([lin,col])
				l = lin
				c = col 
			else:
				k += 1
		num -= 1

	#Checando se foi possivel calcular um caminho.
	if len(listaCaminho) == 0: 
		listaCaminho = -1
		
	else:
		listaCaminho.append([ld,cd])

def planejar(percepcao):
	""" Nessa função a personagem deve atualizar seu conhecimento
		do mundo usando sua percepção da sala atual. Através desse
		parâmetro a personagem recebe (do mundo) todas as informações
		sensoriais associadas à sala atual, bem como o feedback de
		sua última ação.
		Essa percepção é uma lista de strings que podem valer:
			"F" = fedor do Wumpus em alguma sala adjacente,
			"B" = brisa de um poço em sala adjacente, 
			"I" para impacto com uma parede,
			"U" para o urro do Wumpus agonizante e
			"Nome" quando uma outra personagem é encontrada.
	"""
	# declara as variáveis globais que serão acessadas
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, N, salaLivre, outraPersonagem, contadorWumpus
	# Atualiza representação local do mundo (na visão da personagem).

	if 'I' in percepcao: #Caso a percepacao seja de impacto
		mundo[posicao[0]][posicao[1]] = ['M','I'] #marca aquela posicao como muro
		if 'L' in mundo[posicao[0]][posicao[1]]:
			mundo[posicao[0]][posicao[1]].remove('L')

		#caso a sala com muro esteja na lista de livres
		while posicao in salaLivre:
			#Remove a sala com muro da lista de livres
			salaLivre.remove(posicao) 
		posicao = [(posicao[0]-orientacao[0])%N, (posicao[1]-orientacao[1])%N] 
		#print("posicao depois muro:", posicao)
		#retorna a posicao que estava antes do impacto

	else: #caso nao tenha recebido impacto
		#definindo varival que ira contabilizar o total de casas com pessibilidade de P ou W
		possibilidades = 0
		#definindo uma lista que ira guardar as posiçoes dessas ocorrencias
		posiOcorrencia = []

		#criando uma lista como todas as salas adjacentes a atual, ou seja,
		#os indices dessas salas na matriz
		vizinhos = [ [(posicao[0]+1)%N, posicao[1]],
					 [(posicao[0]-1)%N, posicao[1]],
					 [posicao[0], (posicao[1]+1)%N],
					 [posicao[0], (posicao[1]-1)%N] ]
		
		#loop para percorrer todos os indices das salas vizinhas
		for v in vizinhos:
			#Ira realizar a marcaçao de incerteza de acordo com a percepcao recebida, levando em conta
			#que mais de uma incerteza pode ser atribuida a mesma sala. Caso nenhuma percepcao seja recebida
			#marca como livre, alem de adicionar esta sala a lista de salas livres. Ademais, ira estar 
			#realizando a contagem e a memorizacao do local das incertezas.
			if 'F' in percepcao and "L" not in mundo[v[0]][v[1]] and "V" not in mundo[v[0]][v[1]] \
			and "M" not in mundo[v[0]][v[1]] and "P" not in mundo[v[0]][v[1]] and "W" not in mundo[v[0]][v[1]]: 
				possibilidades += 1
				posiOcorrencia = v.copy()
				if "W?" not in mundo[v[0]][v[1]]:
					mundo[v[0]][v[1]].append("W?")

			if 'B' in percepcao and "L" not in mundo[v[0]][v[1]] and "V" not in mundo[v[0]][v[1]] \
			and "M" not in mundo[v[0]][v[1]] and "P" not in mundo[v[0]][v[1]] and "W" not in mundo[v[0]][v[1]]:
				possibilidades += 1
				posiOcorrencia = v.copy()
				if "P?" not in mundo[v[0]][v[1]]:	
					mundo[v[0]][v[1]].append("P?")
		
			if  len(percepcao) == 0 and len(mundo[v[0]][v[1]]) == 0:
				mundo[v[0]][v[1]].append('L')
				if v not in salaLivre:
					salaLivre.append(v.copy()) #Adiciona essa sala a lista de livres

		#Caso so tenha ocorrido a incerteza em apenas UMA sala, sera certo que tera um P ou W nela, portanto
		#iremos marca-la como tal, alem de incrementar o contador de Wumpus
		if possibilidades == 1:
			if "F" in percepcao:
				mundo[posiOcorrencia[0]][posiOcorrencia[1]].append('W')
				mundo[posiOcorrencia[0]][posiOcorrencia[1]].remove('W?')
				contadorWumpus += 1
			if "B" in percepcao:
				mundo[posiOcorrencia[0]][posiOcorrencia[1]].append('P')
				mundo[posiOcorrencia[0]][posiOcorrencia[1]].append('P?')

		#Marca a posicao atual como visitada
		if 'V' not in mundo[posicao[0]][posicao[1]]:
			mundo[posicao[0]][posicao[1]] = []
			mundo[posicao[0]][posicao[1]].append('V')

			if 'B' in percepcao: 
				mundo[posicao[0]][posicao[1]].append("B")

			if 'F' in percepcao: 
				mundo[posicao[0]][posicao[1]].append('F')

		#Remove incertezas
		if 'B?' in mundo[posicao[0]][posicao[1]]: 
			mundo[posicao[0]][posicao[1]].remove('B?')
		if 'F?' in mundo[posicao[0]][posicao[1]]: 
			mundo[posicao[0]][posicao[1]].remove('F?')

		#Remove esta sala da lista de salas livres, uma vez que ela acabou de ser visitada
		if posicao in salaLivre: 
			salaLivre.remove(posicao)

	#Aqui, ja foi realizado contato com outro jogador e o mundo foi compartilhado,
	#logo, sera realizado a atualizaçao da minha percepcao de acordo com os dados recebidos.
	if outraPersonagem is True: 
		for i in range(len(mundo)):
			for j in range(len(mundo[0])):
				if (len(mundoCompartilhado[i][j])) != 0 \
				and \
				(len(mundo[i][j]) == 0 or "W?" in mundo[i][j] or "P?" in mundo[i][j]) \
				and \
				(mundo[i][j] not in mundoCompartilhado[i][j]):
					mundo[i][j] = mundoCompartilhado[i][j].copy() #adiciona a minha percepcao de mundo

					if "L" in mundoCompartilhado[i][j] and [i,j] not in salaLivre:
						#adiciona salas livres a lista de livres
						salaLivre.append([i,j])

					#Icrementando o contador de Wumpus
					if 'W' in mundo[i][j]:
						contadorWumpus += 1
		outraPersonagem = False #desativa a flag 

	#Checa se alguma das percepcoes recebidas e uma personagem
	for p in percepcao:
		if p is not "B" and p is not "F" and p is not "I" and p is not "U":
			outraPersonagem = True #Ativa a flag

	# ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
	# O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
	
	if __DEBUG__:
		print("Percepção recebida pela personagem:")
		print(percepcao)
		#print(salaLivre)
		# mostra na tela (para o usuário) o mundo conhecido pela personagem
		# e o mundo compartilhado (quando disponível)
		print("Mundo conhecido pela personagem:")
		for i in range(len(mundo)):
			for j in range(len(mundo[0])):
				if posicao==[i,j]:
					if orientacao==[0,-1]:
						print("<",end="")
					print("X",end="")
					if orientacao==[0,1]:
						print(">",end="")
					if orientacao==[1,0]:
						print("v",end="")
					if orientacao==[-1,0]:
						print("^",end="")
				print("".join(mundo[i][j]),end="\t| ")
			print("\n"+"-"*(8*len(mundo)+1))
	# ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

def agir():
	""" Nessa função a personagem deve usar seu conhecimento
		do mundo para decidir e tentar executar (devolver) uma ação.
		Possíveis ações (valores de retorno da função) são
		"A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
		"T"=aTirar e "C"=Compartilhar.
	"""
	# declara as variáveis globais que serão acessadas
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, outraPersonagem, andando, ref, listaCaminho, contaG
	# Estrategia e de tentar sempre andar a uma casa livre, caso nao seja possivel
	# chegar a nenhuma, personagem fica rodando, esperando por um contato :( 

	acao = ""

	# Varivel com a previa do destino, caso a personagem ande da sua posiçao atual
	# e seguindo sua orientacao
	previaDest = [(posicao[0]+orientacao[0])%N, (posicao[1]+orientacao[1])%N]

	# Executa caso ainda haja salas livres e que ainda nao se sabe se podem ser visitadas
	if len(salaLivre) > 0 and ref in range(len(salaLivre)):

		# Caso tenha haja a percepcao de contato com outra personagem, ira realizar o 
		# compartilhamento de informacoes, alem de 'resetar' todas as atitudes que a
		# personagem estava tomando, ou seja, faz com que ela repense suas acoes de 
		# acordo com as novas informacoes recebidas.
		if outraPersonagem is True:
			ref = 0
			contaG = 0
			andando = False
			return "C"
		
		# Caso a personagem nao esteja esteja se direcionando a uma determinada sala 
		# livre, ira verificar se alguma das quatro casas adjacentes a ela ainda nao 
		# foi visitada, caso isso se confirme, ela se move ate ela. Caso nenhuma de
		# suas casas visinhas seja livre, ira determinar um caminho a se percorer, de
		# tal modo que se chegue a uma casa livre. A casa livre e determinada por uma 
		# lista que contem todas as casas livres ainda nao visitadas. Quando nao ha
		# maneiras de se chegar a uma casa, essa funcao sera chamada novamente, com o
		# ponteiro 'ref' indicando, se possivel, uma nova sala para se tentar chegar.
		if andando is False :
			if previaDest.copy() in salaLivre.copy():
				acao = 'A'
				contaG = 0

			elif acao != 'A' and contaG < 5:
				acao = 'E'
				contaG += 1

			if acao not in ["A","D","E","T","C"] or contaG == 5:				
				if ref in range(len(salaLivre)):
					busca(salaLivre[ref][0], salaLivre[ref][1])
				andando = True
				ref = 0

		# Caso a personagem esteja se direcionando a uma determinada sala. Ira percorrer
		# a lista com as salas necessarias para se chegar ao destino, usando o mesmo 
		# sistema do caso anterior, de checar as 4 casas adjacentes em busca de 
		# correspondencia. Caso nao seja possivel se locomover a uma determinada sala,
		# ira realizar uma forma de recursao, fazendo com que seja tentado encontrar
		# um caminho para a proxima sala da lista de salas livres.
		if andando is True:
			if listaCaminho is not -1:			
				if len(listaCaminho) > 0:
					if previaDest.copy() == listaCaminho[0].copy():
						acao = 'A'
						contaG = 0
						listaCaminho.remove(listaCaminho[0])

					elif len(listaCaminho) == 1 and 'M' in mundo[previaDest[0]][previaDest[1]]:
						andando = False
						ref = 0
						acao = "E"

					else:
						acao = 'E'

				elif len(listaCaminho) == 0:
					andando = False
					ref = 0
					acao = "E"

			elif listaCaminho is -1:
				if ref in range(len(salaLivre)):
					ref += 1
					acao = "E"
					andando = False	

	# Caso nao seja mais possivel se locomover a uma casa livre, ficara girando em
	# busca de alguma iteracao/companhia.
	else:
		acao = 'E'

	# Atualizacao da percepcao de localizacao da personagem
	pos = posicao
	ori = orientacao

	if acao=="A":
		pos[0] = (pos[0]+ori[0])%len(mundo)
		pos[1] = (pos[1]+ori[1])%len(mundo)
	if acao=="E":
		if ori[0]==0:
			ori[1] = -ori[1]
		ori[0],ori[1] = ori[1],ori[0]
	if acao=="D":
		if ori[1]==0:
			ori[0] = -ori[0]
		ori[0],ori[1] = ori[1],ori[0]

	assert acao in ["A","D","E","T","C"]
	return acao
