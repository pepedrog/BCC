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






def inicializa(tamanho):
	""" Função de inicialização da personagem (recebe o tamanho do mundo).
		Usa as variáveis globais (do módulo) para representar seu
		conhecimento do mundo, sua posição e sua orientação relativas
		ao início da simulação. Você pode criar e inicializar outras
		variáveis aqui (por exemplo, a lista de salas livres e não
		visitadas).

	"""
	# declara as variáveis globais que serão acessadas
	global N, mundo, posicao, orientacao, lista, comant,modo,share
	global voltar #auxilia a rodar 180 graus
	# guarda o tamanho do mundo
	N = tamanho
	share = 0#flag de compartilhamento
	comant = "A"#comando anterior
	voltar = 0
	modo = 0#estrategia de jogo 
	# cria a matriz NxN com a representação do mundo conhecido
	mundo = []
	for i in range(N) : 
		linha = []
		for j in range(N) : 
			linha.append([]) # começa com listas vazias
		mundo.append(linha)
	lista = []#lista que contém as areas livres
	for i in range(N) : 
		linha2 = []
		for j in range(N) : 
			linha2.append([])
		lista.append(linha2)
	for i in range(N):
		for j in range(N):
			lista[i][j] = 0#0 = nao é livre, 1 = é livre
	# posição e orientação iniciais da personagem (sempre serão [0,0] e [1,0]).
	posicao = [0,0]
	orientacao = [1,0]

def verificalista(lista):#verifica se existe area livre conhecida no mapa e retorna 1 se há
	for i in range(N):
		for j in range(N):
			if(lista[i][j] == 1):
				return 1
	return 0			
				
def verificaitem(x):#verifica se x é um caminho que se deve evitar
	if x == ['P?']:
		return 0
	elif x == ['P']:
		return 0
	elif x == ['W?']:
		return 0
	elif x == ['V']:
		return 0
	elif x == ['M']:
		return 0
	return 1

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
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, voltar, lista,comant,share
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
	# 

	pos = posicao
	ori = orientacao
	print("Percepção recebida pela personagem:")
	print(percepcao)

	if "I" in percepcao:#retorna a posicao original quando bate no muro e marca o muro
		mundo[pos[0]][pos[1]] = ["M"]
		pos[0] = pos[0] - ori[0]
		pos[1] = pos[1] - ori[1]

	mundo[pos[0]][pos[1]] = ["V"]#atualiza o local  atual como visitado
	if lista[pos[0]][pos[1]] == 1:#uma area livre torna-se visitada e se atualiza a lista
		lista[pos[0]][pos[1]] = 0
		modo = 0#modo onde se evita ir a lugares ja visitados

	if "Dummy" in percepcao:#detecta a presenca do dummy e comanda a compartilhar
		share += 1

	if "B" in percepcao:#atualiza o mapa quando detecta brisa
		if mundo[pos[0]][(pos[1]+1)%N] == []:
			mundo[pos[0]][(pos[1]+1)%N] = ["P?"]

		if mundo[pos[0]][(pos[1]-1)%N] == []:
			mundo[pos[0]][(pos[1]-1)%N] = ["P?"]

		if mundo[(pos[0]+1)%N][pos[1]] == []:
			mundo[(pos[0]+1)%N][pos[1]] = ["P?"]

		if mundo[(pos[0]-1)%N][pos[1]] == []:
			mundo[(pos[0]-1)%N][pos[1]] = ["P?"]

	elif "F" in percepcao:#atualiza o mapa quando detecta fedor
		if mundo[pos[0]][(pos[1]+1)%N] == []:
			mundo[pos[0]][(pos[1]+1)%N] = ["W?"]

		if mundo[pos[0]][(pos[1]-1)%N] == []:
			mundo[pos[0]][(pos[1]-1)%N] = ["W?"]

		if mundo[(pos[0]+1)%N][pos[1]] == []:
			mundo[(pos[0]+1)%N][pos[1]] = ["W?"]

		if mundo[(pos[0]-1)%N][pos[1]] == []:
			mundo[(pos[0]-1)%N][pos[1]] = ["W?"]

	else:#atualiza o mapa quando nao há nenhuma percepcao
		if mundo[pos[0]][(pos[1]+1)%N] != ["V"] and mundo[pos[0]][(pos[1]+1)%N] != ["M"]:
			mundo[pos[0]][(pos[1]+1)%N] = ["L"]
			lista[pos[0]][(pos[1]+1)%N] = 1

		if mundo[pos[0]][(pos[1]-1)%N] != ["V"] and mundo[pos[0]][(pos[1]-1)%N] != ["M"]:
			mundo[pos[0]][(pos[1]-1)%N] = ["L"]
			lista[pos[0]][(pos[1]-1)%N] = 1

		if mundo[(pos[0]+1)%N][pos[1]] != ["V"] and mundo[(pos[0]+1)%N][pos[1]] != ["M"]:
			mundo[(pos[0]+1)%N][pos[1]] = ["L"]
			lista[(pos[0]+1)%N][pos[1]] = 1

		if mundo[(pos[0]-1)%N][pos[1]] != ["V"] and mundo[(pos[0]-1)%N][pos[1]] != ["M"]:
			mundo[(pos[0]-1)%N][pos[1]] = ["L"]
			lista[(pos[0]-1)%N][pos[1]] = 1

	if comant == "C":#atualiza o mundo do personagem com as informacoes compartilhadas
		for i in range(N):
			for j in range(N):
				if(mundoCompartilhado[i][j] == ["L"]):
					if(mundo[i][j] != ["V"]):
						mundo[i][j] = ["L"]

				elif(mundoCompartilhado[i][j] != []):
					mundo[i][j] = mundoCompartilhado[i][j]

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
			print("".join(mundo[i][j]),end="")#tirei o print do mundo compartilhado pois ficava confuso
			print(end="\t| ")
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
	global mundo, posicao, orientacao, nFlechas, mundoCompartilhado, voltar, comant, share, lista, modo
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
	pos = posicao
	ori = orientacao
	frente = mundo[(pos[0]+ori[0])%N][(pos[1]+ori[1])%N]
	tras = 	mundo[(pos[0]-ori[0])%N][(pos[1]-ori[1])%N]
	if ori[0] == 0:
		esq = mundo[(pos[0]-ori[1])%N][(pos[1]+ori[0])%N]
		dire = mundo[(pos[0]+ori[0])%N][(pos[1]-ori[1])%N]

	else:
		esq = mundo[(pos[0]+ori[1])%N][(pos[1]+ori[0])%N]
		dire = mundo[(pos[0]+ori[0])%N][(pos[1]+ori[1])%N] 

	if (share >= 1): #compartilha sempre que possivel
		acao = "C"
		share -= 1

	elif voltar:#da meia volta em acompanhamento ao movimento anterior
		acao = "E"
		voltar -= 1

	elif modo == 1:#modo em que nao se evita usar caminhos ja visitados
		if frente == ["W"]:
			acao = "T"#atira no wumpus

		elif dire == ["W"]:
			acao = "D"

		elif esq == ["W"] or tras == ["W"]:
			acao = "E"

		elif frente == ["L"]:
			acao = "A"

		elif dire == ["L"]:
			acao = "D"

		elif esq == ["L"] or tras == ["L"]:
			acao = "E"

		elif verificaitem(frente) or frente == ["V"]:
			acao = "A"

		elif verificaitem(dire) or dire == ["V"]:
			acao = "D"

		elif verificaitem(dire) or esq == ["V"]:
			acao = "E"

		else:
			acao =  "E"
			voltar = 1

	else:
		if verificaitem(frente):
			acao = "A"

		elif verificaitem(dire):
			acao = "D"

		elif verificaitem(esq):
			acao = "E"

		elif verificalista:
			acao = "E"
			modo = 1

		else:#so faz moviemntos arriscados quando nao tem mais salas livres para explorar
			if frente == ["P?"] or frente == ["W?"]:
				acao = "A"

			elif dire == ["P?"] or dire == ["W?"]:
				acao = "D"

			elif esq == ["P?"] or esq == ["W?"]:
				acao = "E"

			else:
				acao = "E"
				modo = 1
	
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
	comant = acao#salva o comando 
	assert acao in ["A","D","E","T","C"]
	return acao
