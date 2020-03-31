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

global C 
""" 
armazena se na ultima percepção houve o encontro de outro personagem
"""
global caminho
'''
armazeda o caminho que sera feito pelo personagem
'''
global passo
'''
armazena o local do caminho que esta o proximo passo
'''
global seguro
'''
armazena se o caminhio sendo feito levará a uma casa segura
'''
global perigoso
'''
armazena se o caminhio sendo feito levará a uma casa perigosa
'''
global Wumpus
'''
armazena se o personagem esta em uma caçada
'''
global conferir
'''
armazena se há nessecidade de conferir os dados
'''

def inicializa(tamanho):
	""" Função de inicialização da personagem (recebe o tamanho do mundo).
		Usa as variáveis globais (do módulo) para representar seu
		conhecimento do mundo, sua posição e sua orientação relativas
		ao início da simulação. Você pode criar e inicializar outras
		variáveis aqui (por exemplo, a lista de salas livres e não
		visitadas).

	"""
	# declara as variáveis globais que serão acessadas
	global N, mundo, posicao, orientacao
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
	global nFlechas
	nFlechas = 1

	global C, caminho, passo, seguro, perigoso, Wumpus, conferir
	C = False
	caminho = []
	for i in range (N*N):
		caminho.append([0,0])
	passo = 0
	seguro = False
	perigoso = False
	Wumpus = [False,[]]
	conferir = False

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
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado
	# Atualiza representação local do mundo (na visão da personagem).
	# Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
	# Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
	# "B" para brisa, "F" para fedor, "L" para salas livres,
	# "M" para muros e "V" para salas visitadas.

	# Essa função ainda precisa ser implementada! São requisitos dessa
	# implementação a incorporação dos dados perceptuais à representação
	# do mundo, bem como a propagação do conhecimento adquirido para as
	# adjacências da sala atual (requisitos completos no enunciado).

	# ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
	# O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
	global C, passo, perigoso, Wumpus, conferir

	pos = posicao
	ori = orientacao
	# o personagem confer se há informacao para atualizar
	if conferir:
		for i in range(len(mundo)):
			for k in range(len(mundo[0])):
				if not('L' in mundo[i][k] or 'V' in mundo[i][k] or 'P' in mundo[i][k] or 'M' in mundo [i][k] or mundoCompartilhado[i][k]==[] or ('W' in mundo[i][k] and 'W' in mundoCompartilhado[i][k])):
					mundo[i][k]=mundoCompartilhado[i][k]
					if perigoso :
						perigoso = False
						passo = 0
		conferir=False
	mundo[pos[0]][pos[1]] = ["V"]

	adjacências = [[1,0],[0,-1],[-1,0],[0,1]]
	# o personagem confere se o Wumpus ainda está vivo,se está caçando
	if Wumpus[0]:
		for i in adjacências:
			aux = [(pos[0]+i[0])%len(mundo),(pos[1]+i[1])%len(mundo)]
			if Wumpus[1][0]==aux[0] and Wumpus[1][1]==aux[1]:
				if not('F' in percepcao):
					mundo[aux[0]][aux[1]] = L
					Wumpus[0] = False
					seguro = True


	#o personagem interpreta as informações adquiridas
	if "I" in percepcao:
		mundo [pos[0]][pos[1]] = ['M']
		pos[0] = (pos[0]-ori[0])%len(mundo)
		pos[1] = (pos[1]-ori[1])%len(mundo)
	else:
		for i in adjacências:
			aux = [(pos[0]+i[0])%len(mundo),(pos[1]+i[1])%len(mundo)]
			if not('V' in mundo[aux[0]][aux[1]] or 'M' in mundo[aux[0]][aux[1]]):
				if percepcao==[]:
					mundo[aux[0]][aux[1]] = ['L']
				if not('L' in mundo[aux[0]][aux[1]] or 'W' in mundo[aux[0]][aux[1]] or 'P' in mundo[aux[0]][aux[1]]):
					if "B" in percepcao:
						if not('P?' in mundo[aux[0]][aux[1]]):
							mundo[aux[0]][aux[1]].append('P?')
					if "F" in percepcao:
						if not('W?' in mundo[aux[0]][aux[1]]):
							mundo[aux[0]][aux[1]].append('W?')
	#o personagem ve se possui alguma certeza
	if ('B' in percepcao or 'F' in percepcao):
		cont = 0
		for i in adjacências:
			aux = [(pos[0]+i[0])%len(mundo),(pos[1]+i[1])%len(mundo)]
			if ('M' in mundo[aux[0]][aux[1]] or 'V' in mundo[aux[0]][aux[1]] or 'L' in mundo[aux[0]][aux[1]]):
				cont+=1
		if cont == 3:
			for i in adjacências:
				aux = [(pos[0]+i[0])%len(mundo),(pos[1]+i[1])%len(mundo)]
				if not('M' in mundo[aux[0]][aux[1]] or 'V' in mundo[aux[0]][aux[1]] or 'L' in mundo[aux[0]][aux[1]]):
					if 'B' in percepcao:
						mundo[aux[0]][aux[1]]=['P']
					elif 'F' in percepcao:
						mundo[aux[0]][aux[1]]=['W']
	#o personagem ve se encontrou outro personagem
	for i in percepcao:
		if (i!='B' and i!='F' and i!='I' and i!='U'):
			C = True
	if __DEBUG__:
		print("Percepção recebida pela personagem:")
		print(percepcao)
		# elimine o teste abaixo quando tiver corrigido o bug de movimentação...
		'''
		if "I" in percepcao:
			print("Você bateu num muro e talvez não esteja mais na sala em que pensa estar...")
		'''
		# essa atualização abaixo serve de ilustração/exemplo, e
		# apenas marca as salas como "Visitadas", mas está errada
		
		# mostra na tela (para o usuário) o mundo conhecido pela personagem
		# e o mundo compartilhado (quando disponível)
		print("Mundo conhecido pela personagem:")
		for i in range(len(mundo)):
			for j in range(len(mundo[0])):
				if pos==[i,j]:
					if ori==[0,-1]:
						print("<",end="")
					print("X",end="")
					if ori==[0,1]:
						print(">",end="")
					if ori==[1,0]:
						print("v",end="")
					if ori==[-1,0]:
						print("^",end="")
				print("".join(mundo[i][j]),end="\t| ")
				#print("".join(mundoCompartilhado[i][j]),end="\t| ")
			print("\n"+"-"*(8*len(mundo)+1))
	# ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####

def escolher():

	'''	Eu adotei uma estrategia a qual maximiza a chance
		de sobrevivencia do personagem.  Ela se baseia em
		se mover para casa livre mais longe para aumentar 
		as chances de encontrar outro personagem e trocar 
		informações, caso ja tenha percorido todas, matar
		o Wumpu mais longe do personagem e somente depois
		e caso nenhuma opção anterior seja possivel tenta
		a casa arriscada mais distante pelo mesmo motivo,
		Caso não haja mais casas fica andando para tentar
		achar outro personagem foi a decisão inplementada


		Pra essa parte fiz um codigo semelhante à disktra
		assim podendo localizar, precisamente, a casa que
		esta mais distante considerando as curvas, porque
		elas levam mais movimentos, porem  meu personagem
		segue pelo menor caminho à casa mais distante pra
		assim não ficar se movendo em circulos infinitos.
	'''

	global mundo, posicao, orientacao

	global caminho, passo, seguro, perigoso

	pos = posicao
	ori = orientacao

	disktra = []
	for x in range(len(mundo)):
		lista = []
		for y in range(len(mundo[0])):
			lista.append([])
		disktra.append(lista)
	fila = [pos]
	disktra[pos[0]][pos[1]]=[0,ori]
	segu = pos
	peri = pos
	wump = pos
	vaga = pos
	while len(fila)>0:
		atual = fila[0]
		for i in fila:
			if disktra[i[0]][i[1]][0]!=[] and disktra[i[0]][i[1]][0]<disktra[atual[0]][atual[1]][0]:
				atual = i
		if ('L' in mundo[atual[0]][atual[1]]):
			if disktra[atual[0]][atual[1]][0] > disktra[segu[0]][segu[1]][0]:
				segu = atual
		elif ('M' in mundo[atual[0]][atual[1]] or 'P' in mundo[atual[0]][atual[1]]):
			pass
		elif ('P?' in mundo[atual[0]][atual[1]] or 'W?' in mundo[atual[0]][atual[1]]):
			if disktra[atual[0]][atual[1]][0] > disktra[peri[0]][peri[1]][0]:
				peri = atual
		elif('W' in mundo[atual[0]][atual[1]]):
			if disktra[atual[0]][atual[1]][0] > disktra[wump[0]][wump[1]][0]:
				wump = atual

		elif ('V' in mundo[atual[0]][atual[1]]):
			if disktra[atual[0]][atual[1]][0] > disktra[vaga[0]][vaga[1]][0]:
				vaga = atual
			adj =[[1,0],[0,-1],[-1,0],[0,1]]
			dist = disktra[atual[0]][atual[1]][0]
			for i in disktra[atual[0]][atual[1]][1:]:
				prox = [(atual[0]+i[0])%len(mundo),(atual[1]+i[1])%len(mundo)]
				if disktra[prox[0]][prox[1]]==[]:
					disktra[prox[0]][prox[1]]=[dist+1,i]
					fila.append(prox)
				elif disktra[prox[0]][prox[1]][0] == dist+1:
					disktra[prox[0]][prox[1]].append(i)
				elif disktra[prox[0]][prox[1]][0] > dist+1:
					disktra[prox[0]][prox[1]]=[dist+1,i]
				adj.remove(i)

			if len(disktra[atual[0]][atual[1]])==2:
				i = disktra[atual[0]][atual[1]][1]
				i = [-i[0],-i[1]]
				prox = [(atual[0]+i[0])%len(mundo),(atual[1]+i[1])%len(mundo)]
				if disktra[prox[0]][prox[1]]==[]:
					disktra[prox[0]][prox[1]]=[dist+3,i]
					fila.append(prox)
				elif disktra[prox[0]][prox[1]][0] == dist+3:
					disktra[prox[0]][prox[1]].append(i)
				elif disktra[prox[0]][prox[1]][0] > dist+3:
					disktra[prox[0]][prox[1]]=[dist+3,i]
				adj.remove(i)
				
			for i in adj:
				prox = [(atual[0]+i[0])%len(mundo),(atual[1]+i[1])%len(mundo)]
				if disktra[prox[0]][prox[1]]==[]:
					disktra[prox[0]][prox[1]]=[dist+2,i]
					fila.append(prox)
				elif disktra[prox[0]][prox[1]][0] == dist+2:
					disktra[prox[0]][prox[1]].append(i)
				elif disktra[prox[0]][prox[1]][0] > dist+2:
					disktra[prox[0]][prox[1]]=[dist+2,i]
		fila.remove(atual)
	'''	constroi o caminho ate a casa localizada, priorisando
		caçar Wumpus, depois casas seguras e depois inseguras 
	'''
	
	if(segu != pos):
		atual = segu
		passo = 1
		while(atual!= pos):
			caminho[passo] = atual
			passo += 1
			i = disktra[atual[0]][atual[1]][1]
			i = [-i[0],-i[1]]
			atual = [(atual[0]+i[0])%len(mundo),(atual[1]+i[1])%len(mundo)]
		passo -= 1
		seguro = True
	elif(wump != pos and nFlechas>0):
		Wumpus[1] = wump
		atual = wump
		passo = 1
		while(atual!= pos):
			caminho[passo] = atual
			passo += 1
			i = disktra[atual[0]][atual[1]][1]
			i = [-i[0],-i[1]]
			atual = [(atual[0]+i[0])%len(mundo),(atual[1]+i[1])%len(mundo)]
		passo -= 1
		Wumpus[0] = True
	elif(peri != pos):
		atual = peri
		passo = 1
		while(atual!= pos):
			caminho[passo] = atual
			passo += 1
			i = disktra[atual[0]][atual[1]][1]
			i = [-i[0],-i[1]]
			atual = [(atual[0]+i[0])%len(mundo),(atual[1]+i[1])%len(mundo)]
		passo -= 1
		perigoso = True
	else :
		atual = vaga
		passo = 1
		while(atual!= pos):
			caminho[passo] = atual
			passo += 1
			i = disktra[atual[0]][atual[1]][1]
			i = [-i[0],-i[1]]
			atual = [(atual[0]+i[0])%len(mundo),(atual[1]+i[1])%len(mundo)]
		passo -= 1

def pensar():
	''' esta função serve para 'pensar' o que fazer
		quando personagem tem as coordenada da casa
		a qual ele esta e da casa adjacente que ele
		quer ir e decide a acao qual ele deve tomar
	'''
	global posicao, orientacao
	global nFlechas
	global caminho, passo, seguro, perigoso, Wumpus

	pos = posicao
	ori = orientacao

	adj = [[1,0],[0,-1],[-1,0],[0,1]]

	i=0
	while (adj[i][0] != ori[0]) or (adj[i][1] != ori[1]):
		i+=1

	acao = ''

	frente = [(pos[0]+ori[0])%len(mundo),(pos[1]+ori[1])%len(mundo)]
	esquer = [(pos[0]+adj[i-1][0])%len(mundo),(pos[1]+adj[i-1][1])%len(mundo)]
	if caminho[passo][0] == frente[0] and caminho[passo][1] == frente[1] :
		if Wumpus[0] == True and ('W' in mundo[frente[0]][frente[1]]):
			acao = 'T'
			nFlechas -= 1
			Wumpus[0] = False
			seguro = True
		else:
			acao = 'A'
			passo -= 1
	elif caminho[passo][0] == esquer[0] and caminho[passo][1] == esquer[1]:
		acao = 'E'
	else:
		acao = 'D'

	if passo == 0:
		seguro = False
		perigoso = False
	return acao

def agir():
	""" Nessa função a personagem deve usar seu conhecimento
		do mundo para decidir e tentar executar (devolver) uma ação.
		Possíveis ações (valores de retorno da função) são
		"A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
		"T"=aTirar e "C"=Compartilhar.
	"""
	# declara as variáveis globais que serão acessadas
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado
	# Aplica uma certa estratégia para decidir a ação a ser
	# executada com base na representação local do mundo.
	# Devolve (para o mundo) o nome da ação pretendida.
	# Duas ações só são possíveis em condições específicas,
	# que devem ser testadas de antemão (sob risco da personagem
	# entrar em loop): atirar só é possível quando a personagem
	# dispõe de flechas, e compartilhar só é possível quando
	# existem outras personagens na mesma sala (percebidas
	# pela função planejar através de percepções diferentes de
	# "F", "B", "I" ou "U").

	# ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
	# O trecho abaixo é uma pseudo-implementação, pois recebe
	# a ação através de uma pergunta dirigida ao usuário.
	# No código a ser entregue, você deve programar algum tipo
	# de estratégia para 
	global C, caminho, passo, seguro, perigoso, conferir
	pos = posicao
	ori = orientacao
	acao = ""
	adjacências = [[1,0],[0,-1],[-1,0],[0,1]]
	
	''' no caso de nao haver nenhum cainho definido
		chama a função que escolhe uma casa destino
		e monta um caminho seguro o qual guia a ela
	'''
	if passo == 0:
		escolher()
	'''	o personagem tenta troca informaçoes sempre	
	'''
	if C:
		acao = 'C'
		C = False
		conferir=True
	elif passo > 0:
		acao = pensar()
	else:
		acao = input("Digite a ação desejada (A/D/E/T): ")

	# ATENÇÃO: a atualizacao abaixo está errada!!!
	# Não checa se o movimento foi possível ou não... isso só dá para
	# saber quando chegar uma percepção nova (a percepção "I"
	# diz que o movimento anterior não foi possível).
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
	# ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####
	#input()
	assert acao in ["A","D","E","T","C"]
	return acao
