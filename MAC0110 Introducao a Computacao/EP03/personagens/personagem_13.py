# flag para depuração
__DEBUG__ = False


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

global vizinhas
"""
Matriz que permite iterar pelas salas vizinhas à sala em que está o 
personagem.
"""

global livres
"""
Lista que guarda as salas livres.
"""


global checaSala
"""
Variável usada para garantir que o personagem procurará por uma sala
livre dentre todas as adjacentes antes de tentar voltar pelo caminho que
fez.
"""

global indice
"""
Variável usada para determinar a sala seguinte quando o personagem estiver
fazendo o caminho de volta.
"""

global caminho
"""
Lista que guarda as salas visitadas pelo personagem, formando uma fila;
para que o personagem possa retroceder se encontrar um beco sem saídas
(ou escolhas ótimas).
"""

global compartilhar
"""
Variável que assume 3 valores (0, 1 e 2) para poder atuar em rodadas diferentes.
Quando a percepção de outro personagem é recebida ela assume o valor 1, que
será lido na função agir() para que a ação correspondente possa ser tomada e
assumirá o valor 2. Na rodada seguinte, quando compartilhar = 2 , a função
planejar() incorporará o mundo compartilhado ao mundo do personagem. 
"""

global marcador
"""
Como a checaSala, essa variável garante que, quando o personagem estiver fazendo
o caminho de volta, todas as salas adjacentes sejam checadas antes de passar para
a próxima sala na lista caminho.
"""

global salaanterior
"""
Variável usada para poder arrumar o mapa do personagem quando ele colide com um muro.
"""

global zeraCaminho
"""
Responsável por zerar o caminho apenas uma vez por Wumpus (quando o Wumpus é morto, a
variável é resetada).
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
	global N, mundo, posicao, orientacao, vizinhas, livres, checaSala, indice, caminho, compartilhar, marcador, zeraCaminho
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
	livres = []
	caminho = [[0, 0]]
	checaSala, indice, compartilhar, marcador = 0, 1, 0, 0
	zeraCaminho = True

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
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, vizinhas
	global proxpos, indice, checaSala, salaanterior, compartilhar, caminho, zeraCaminho
	# Atualiza representação local do mundo (na visão da personagem).
	# Devem ser usados os símbolos "W"/"W?" para Wumpus ou possível
	# Wumpus e "P"/"P?" para poço ou possível poço, além dos indicadores
	# "B" para brisa, "F" para fedor, "L" para salas livres,
	# "M" para muros e "V" para salas visitadas.

	# Essa função ainda precisa ser implementada! São requisitos dessa
	# implementação a incorporação dos dados perceptuais à representação
	# do mundo, bem como a propagação do conhecimento adquirido para as
	# adjacências da sala atual (requisitos completos no enunciado).

	pos = posicao
	ori = orientacao

	# Indexação das casas vizinhas, na ordem Norte(0), Sul(1), Oeste(2) e Leste(3).
	vizinhas = [ [(pos[0]-1)%N, pos[1]],
				 [(pos[0]+1)%N, pos[1]],
				 [pos[0], (pos[1]-1)%N],
				 [pos[0], (pos[1]+1)%N] ]
	vazio = []
	dummy = ["Dummy"]
	checador = 0

	if "V" not in mundo[pos[0]][pos[1]]:
		mundo[pos[0]][pos[1]] = ["V"]

	if compartilhar == 2:
		compartilhar = 0
		for i in range(len(mundo)):
			for j in range(len(mundo[0])):
				if "M" in mundoCompartilhado[i][j]:
					if [mundo[i], mundo[j]] in livres:  #Tira da lista das salas livres um muro, marcado falsamente como livre.
						ind = livres.index([mundo[i], mundo[j]])
						livres.remove(ind)
					mundo[i][j] = ["M"]
				if "P" in mundoCompartilhado[i][j]:
					if (mundo[i][j] == vazio or "W?" in mundo[i][j]) and "P?" not in mundo[i][j]:
						mundo[i][j].append("P?")
				if "W" in mundoCompartilhado[i][j]:
					if (mundo[i][j] == vazio or "P?" in mundo[i][j]) and "W?" not in mundo[i][j]:
						mundo[i][j].append("W?")
				if "L" in mundoCompartilhado[i][j]:
					if "M" and "L" not in mundo[i][j]:
						mundo[i][j] = ["L"]
						livres.append([i, j])  #Coloca na lista de salas livres a nova integrante.

	for viz in vizinhas:
		if (percepcao == vazio or percepcao == dummy) and "M" not in mundo[viz[0]][viz[1]]:  #Verifica quando a sala está livre.
			if "V" not in mundo[viz[0]][viz[1]] or "L" not in mundo[viz[0]][viz[1]]:  #Uma sala já visitada não precisa ser marcada.
				mundo[viz[0]][viz[1]] = ["L"]
			coordviz = [viz[0], viz[1]]
			if coordviz not in livres and "M" not in mundo[viz[0]][viz[1]]:  #Coloca as novas salas livres em sua lista.
				livres.append(coordviz)

		#Sinaliza as salas vizinhas apenas se elas já não possuírem "L", "V", "M" ou o próprio sinal.
		if "B" in percepcao:
			if "L" not in mundo[viz[0]][viz[1]] and "V" not in mundo[viz[0]][viz[1]] and "M" not in mundo[viz[0]][viz[1]] and "P?" not in mundo[viz[0]][viz[1]] and "P" not in mundo[viz[0]][viz[1]]:
				mundo[viz[0]][viz[1]].append("P?")

		if "F" in percepcao: 
			if "L" not in mundo[viz[0]][viz[1]] and "V" not in mundo[viz[0]][viz[1]] and "M" not in mundo[viz[0]][viz[1]] and "W?" not in mundo[viz[0]][viz[1]]:
				mundo[viz[0]][viz[1]].append("W?")

	if "I" in percepcao:
		#Desfaz a movimentação da jogada anterior e coloca "M" na sala em frente.
		pos[0] = salaanterior[0]
		pos[1] = salaanterior[1]
		if "M" not in mundo[(pos[0]+ori[0])%N][(pos[1]+ori[1])%N]:
			mundo[(pos[0]+ori[0])%N][(pos[1]+ori[1])%N] = ["M"]
		caminho.pop()  #Remove a sala murada da fila.

	if "Dummy" in percepcao:
		compartilhar = 1

	if "U" in percepcao:  #Com o Wumpus morto, sua morada fica livre.
		mundo[(pos[0]+ori[0])%N][(pos[1]+ori[1])%N] = ["L"]
		livres.append(mundo[(pos[0]+ori[0])%N][(pos[1]+ori[1])%N])
		zeraCaminho = True  #Se outro alguém matar o Wumpus, o jogador deve voltar a explorar.

	"""
	Abaixo é verificado se é possível marcar certeza no conteúdo
	de uma sala marcada com "P?" ou "W?". O checador é incrementado se:
		1. A casa vizinha à atual estiver vazia (não tiver nenhuma
		informação);
		2. A casa vizinha contiver a mesma percepção da casa atual.
	Nos casos em que o checador somar 1 (ou seja, só existe uma casa
	vizinha com "P?" ou "W?" e nenhuma das casas vizinhas não possui 
	informação), a casa é marcada com certeza ("P" ou "W").
	"""
	if "B" in percepcao:
		for viz in vizinhas:
			if "P?" in mundo[viz[0]][viz[1]]:
				checador += 1
			if mundo[viz[0]][viz[1]] == vazio:
				checador += 1
		if checador == 1:
			for viz in vizinhas:
				if "P?" in  mundo[viz[0]][viz[1]]:
					mundo[viz[0]][viz[1]] = ["P"]
	if "F" in percepcao:
		for viz in vizinhas:
			if "W?" in mundo[viz[0]][viz[1]]:
				checador += 1
			if mundo[viz[0]][viz[1]] == vazio:
				checador += 1
		if checador == 1:
			for viz in vizinhas:
				if "W?" in  mundo[viz[0]][viz[1]]:
					mundo[viz[0]][viz[1]] = ["W"]


	# ############ T R E C H O   D E   I L U S T R A Ç Ã O ##############
	# O trecho abaixo serve apenas para lhe ajudar a depurar o seu código
	# 


	if __DEBUG__:
		print("Percepção recebida pela personagem:")
		print(percepcao)
		# elimine o teste abaixo quando tiver corrigido o bug de movimentação...

		if "I" in percepcao:
			print("Você bateu num muro e talvez não esteja mais na sala em que pensa estar...")
		# essa atualização abaixo serve de ilustração/exemplo, e
		# apenas marca as salas como "Visitadas", mas está errada

		#mundo[pos[0]][pos[1]] = ["V"]
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
				print("".join(mundo[i][j]),end="")
				print("",end="\t| ")
			print("\n"+"-"*(8*len(mundo)+1))
		#print(orientacao)
		#print(livres)
		#f = input()
		print("caminho:", caminho)
		#print("checaSala:", checaSala)
		print("posicao:", [pos[0], pos[1]])
		#print("mundoCompartilhado")
		#print(mundo[viz[0]][viz[1]])
		#print(mundo)
	# ##### F I M   D O   T R E C H O   D E   I L U S T R A Ç Ã O #####



def agir():
	""" Nessa função a personagem deve usar seu conhecimento
		do mundo para decidir e tentar executar (devolver) uma ação.
		Possíveis ações (valores de retorno da função) são
		"A"=Andar, "D"=girarDireita, "E"=girarEsquerda,
		"T"=aTirar e "C"=Compartilhar.
	"""
	# declara as variáveis globais que serão acessadas
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, checaSala
	global salaanterior, caminho, compartilhar, indice, marcador, zeraCaminho
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
	pos = posicao
	ori = orientacao
	proxpos = [(pos[0]+ori[0])%len(mundo), (pos[1]+ori[1])%len(mundo)]  #Próxima posição.

	for i in range(len(mundo)):
		for j in range(len(mundo[0])):
			"""
			Checa em toda a matriz se apareceu a certeza de um Wumpus. Caso sim, a personagem
			deve voltar a explorar (reiniciar seus caminhos) até encontrar o Wumpus e matá-lo.
			"""
			if "W" in mundo[i][j] and zeraCaminho:
				zeraCaminho = False
				caminho = [pos[0], pos[1]]
				indice = 1
	if "W" in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:  #Se o Wumpus estiver em frente...
		if nFlechas > 0:  #... e a personagem possuir flechas...
			zeraCaminho = True
			return "T"  #... ela o mata! E zera seu caminho, para voltar a explorar.

	if compartilhar == 1:
		compartilhar = 2
		return "C"

	if (proxpos in livres and proxpos not in caminho) and "M" not in mundo[(pos[0]+ori[0])%len(mundo)][(pos[1]+ori[1])%len(mundo)]:
		#Se a próxima sala estiver marcada como livre mas ainda não fizer parte
		#do caminho (nem for um muro), a personagem irá para lá.
		salaanterior = [pos[0], pos[1]]
		indice = 1
		pos[0] = (pos[0]+ori[0])%len(mundo)
		pos[1] = (pos[1]+ori[1])%len(mundo)
		caminho.append([pos[0], pos[1]])  #Coloca a sala que a personagem acabou de passar na lista caminho.
		checaSala = 0  #Reinicia o ciclo de procurar por salas livres na próxima sala.
		return "A"

	elif checaSala < 4:  #Checará se as 4 salas adjacentes estão livres, para seguir para lá.
		checaSala += 1
		if ori[0]==0:
			ori[1] = -ori[1]
		ori[0],ori[1] = ori[1],ori[0]        
		return "E"  #Se não estiver livre, gira 90º e tenta de novo!

	else:
		"""
		Se nenhuma das salas adjacentes forem livres, a personagem procurará
		pela sala de onde veio, e retornará para ela. De lá, irá verificar se
		existe outra sala livre pela qual ainda não passou (não está no caminho),
		e assim sucessivamente.
		"""
		if proxpos == caminho[-indice]:
			salaanterior = [pos[0], pos[1]]
			checaSala = 0
			pos[0] = (pos[0]+ori[0])%len(mundo)
			pos[1] = (pos[1]+ori[1])%len(mundo)
			return "A"
		if ori[0]==0:
			ori[1] = -ori[1]
		ori[0],ori[1] = ori[1],ori[0]
		marcador += 1
		if marcador == 4:
			marcador = 0
			indice = (indice + 1)%(len(caminho))

		return "E"
