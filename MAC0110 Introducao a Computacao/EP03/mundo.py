""" O MUNDO DE WUMPUS

    Esta é uma versão adaptada do jogo criado por Gregory Yob em 1975.
    Nesta versão o mundo é um tabuleiro em forma de toro NxN em que cada
    sala pode estar livre, conter um muro, um poço sem fundo ou um
    terrível Wumpus. As personagens nesse mundo devem se unir para 
    eliminar todos os Wumpus e assim poderem voltar sãs e salvas para
    casa. Ao percorrerem as salas do mundo, as personagens recebem dados
    sensoriais que as ajudarão a compreender o que pode estar nas salas
    adjacentes, e assim evitar alguns destinos trágico, como cair em um
    poço sem fundo ou ser devoradas por um terrível Wumpus. Cada
    personagem possui uma flecha, que pode ser disparada uma única vez,
    preferencialmente quando a personagem tiver acumulado evidências
    suficientes de que existe um Wumpus à sua frente. Personagens também
    podem se encontrar, e trocar conhecimento sobre as partes do mundo
    que já exploraram.
"""

# use apenas para depuração
__DEBUG__ = True
    
# o mundo não deve ser importado como módulo
if __name__!="__main__":
    print("Por favor execute o Mundo de Wumpus com o comando\n",
          "    python3 mundo.py")
    exit()

# associa números/nomes aos 4 tipos de salas do mundo de Wumpus
LIVRE,MURO,POCO,WUMPUS = range(4)
salas = ["L","M","P","W"]

# associa números/nomes aos 5 tipos de ações possíveis
ANDAR,GIRARDIREITA,GIRARESQUERDA,ATIRAR,COMPARTILHAR = range(5)
acoes = ["A","D","E","T","C"]


class MundoDeWumpus:
    """ Classe principal: define um Mundo de Wumpus, cria personagens,
        faz a simulação e anuncia o final do jogo.
    """
    def __init__(self):
        """ Construtor: inicializa a representação do mundo,
            inclui as personagens NUSP e dummy e passa a simular o jogo.
        """
        # tamanho do mundo (que é um quadrado NxN dobrado na forma de um toro).
        self.N = 5
        # mundinho besta de teste...
        self.mundo = [ [ MURO  , LIVRE , MURO  , MURO  , LIVRE  ],
                       [ LIVRE , LIVRE , MURO  , LIVRE , LIVRE  ],
                       [ POCO  , LIVRE , LIVRE , LIVRE , POCO   ],
                       [ WUMPUS, LIVRE , LIVRE , LIVRE , LIVRE  ],
                       [ LIVRE , LIVRE , POCO  , LIVRE , MURO   ] ]
        #self.mundo = [ [ MURO  , LIVRE , MURO  , MURO  , LIVRE  ],
         #              [ LIVRE , LIVRE , MURO  , LIVRE , LIVRE  ],
          #             [ LIVRE  , LIVRE , LIVRE , LIVRE , LIVRE   ],
          #             [ WUMPUS, LIVRE , LIVRE , LIVRE , LIVRE  ],
         #            [ LIVRE , LIVRE , LIVRE  , LIVRE , MURO   ] ]
        
        # nesse mundo só há 1 Wumpus
        self.nWumpus = 1
        # cria personagemNUSP
        self.personagemNUSP = PersonagemNUSP(self.N)
        # cria uma segunda personagem, dummy, que apenas anda e mapeia o que vê.
        self.dummy = Dummy(self.N, self.mundo)
        # faz o processamento do jogo
        self.processaJogo()
        # anuncia o final do jogo
        self.finalizaJogo()
    
    def processaJogo(self):
        """ Método processaJogo: controla o laço principal, processando uma
            personagem por vez, enquanto o jogo não tiver acabado.
        """
        # inicializa flags que indicam a tentativa de andar em direção a uma
        # parede e a morte de um Wumpus.
        self.personagemNUSP.impacto = self.urro = False

        # Repete o laço principal enquanto existirem Wumpus e personagens vivos.
        while self.nWumpus>0 and self.personagemNUSP.estaviva:

            # código apenas para depuração: mostra o mundo a cada jogada
            if __DEBUG__:
                self.imprimeMundo()

            # coleta informações locais para produzir a percepção da personagemNUSP
            self.personagemNUSP.percepcao = self.montaPercepcao(self.personagemNUSP)

            # reinicializa flags (já foram usadas para as percepções das personagens)
            self.personagemNUSP.impacto = self.urro = False

            # chama o método de planejamento da personagemNUSP
            self.personagemNUSP.modulo.planejar(self.personagemNUSP.percepcao)

            # recebe ações da personagem até obter uma ação viável
            viavel = False
            while not viavel:
                # chama o método de ação da personagemNUSP
                acao = self.personagemNUSP.modulo.agir()
                # processa a ação (passando o próprio objeto MundoDeWumpus como argumento)
                viavel = self.personagemNUSP.processe[acoes.index(acao)](self)

            # processa personagem dummy
            self.dummy.percepcao = []
            self.dummy.planejar(self.dummy.percepcao)
            self.dummy.agir(self.personagemNUSP.posicao,self.mundo)

    def finalizaJogo(self):
        """ O jogo termina quando não há mais personagens vivas,
            ou quando todos os Wumpus foram mortos.
        """
        if __DEBUG__:
            self.imprimeMundo()
        nome = self.personagemNUSP.nome
        if self.nWumpus==0:
            print("Parabéns, "+nome+", você sobreviveu ao mundo de Wumpus!",sep="")
        x,y = self.personagemNUSP.posicao
        if self.mundo[x][y] == WUMPUS:
            print("Meus pêsames, "+nome+", você virou comida de Wumpus...",sep="")
        if self.mundo[x][y] == POCO:
            print("Meus pêsames, "+nome+", você caiu em um poço...",sep="")

    # outras funções auxiliares do processamento do mundo
    def imprimeMundo(self):
        pos = self.personagemNUSP.posicao
        dpos = self.dummy.posicao
        ori = self.personagemNUSP.orientacao
        print("Estado atual do mundo (nenhuma personagem enxerga isso!):")
        for i in range(self.N):
            for j in range(self.N):
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
                if dpos==[i,j]:
                    print("D",end="")
                print(salas[self.mundo[i][j]],end="\t| ")
            print("\n"+"-"*(8*self.N+1))

    def montaPercepcao(self,personagem):
        """ Vasculha as salas adjacentes à sala ocupada pela personagem,
            coletando as informações perceptíveis (fedor, brisa), além de
            agregar percepções decorrentes da última ação (impacto/urro),
            e de outras personagens presentes na posicao.
        """
        pos = personagem.posicao
        dpos = self.dummy.posicao
        percepcao = []
        vizinhos = [ [(pos[0]+1)%self.N,pos[1]],
                     [(pos[0]-1)%self.N,pos[1]],
                     [pos[0],(pos[1]+1)%self.N],
                     [pos[0],(pos[1]-1)%self.N] ]
        for viz in vizinhos:
            if self.mundo[viz[0]][viz[1]] == WUMPUS and "F" not in percepcao:
                percepcao.append("F") # fedor
            if self.mundo[viz[0]][viz[1]] == POCO and "B" not in percepcao:
                percepcao.append("B") # brisa
        if personagem.impacto:
            percepcao.append("I")
        if self.urro:
            percepcao.append("U")
        if pos == dpos:
            percepcao.append("Dummy")
        return percepcao


class Personagem:
    """ Meta-classe para processar as ações de cada personagem:
        andar, girarDireita, girarEsquerda, atirar e compartilhar.
        Essas ações são métodos da personagem que recebem também
        o objeto MundoDeWumpus, pois potencialmente podem alterar
        o estado do mundo (por exemplo, ao se matar um Wumpus).
        Essas ações devolvem True/False indicando se foram realizadas.
        Cada personagem em particular além desses métodos também
        precisa definir as funções:
            def __init__(self,N):
            def planejar(self,percepcao):
            def agir(self):
    """
    def ande(self,MundoW):
        """ Função ande: verifica se é possível mover a personagem
            na direção indicada por sua orientação, e as consequências
            disso.
        """
        # posicao e orientacao atuais da personagem
        pos = self.posicao
        ori = self.orientacao
        # calcula a posição nova
        posnova = [(pos[0]+ori[0])%self.N,
                   (pos[1]+ori[1])%self.N]
        # se houver um muro, não dá para andar
        mundo = MundoW.mundo
        if mundo[posnova[0]][posnova[1]] == MURO:
            self.impacto = True
        else:
            pos[0],pos[1] = posnova[0],posnova[1]
            # se houver wumpus ou poço, é game over para a personagemNUSP
            if mundo[pos[0]][pos[1]] in [ WUMPUS, POCO ]:
                self.estaviva = False # NÃÃÃÃÃÃÃOOOOOOOOO!!!!!!!!!!!!
        # tentar andar é sempre realizável
        return True

    def gireDireita(self,MundoW):
        """ Corrige a orientação através de um giro no sentido horário.
        """
        ori = self.orientacao
        if ori[1]==0:
            ori[0] = -ori[0]
        ori[0],ori[1] = ori[1],ori[0]
        # girar é sempre realizável
        return True

    def gireEsquerda(self,MundoW):
        """ Corrige a orientação através de um giro no sentido anti-horário.
        """
        ori = self.orientacao
        if ori[0]==0:
            ori[1] = -ori[1]
        ori[0],ori[1] = ori[1],ori[0]
        # girar é sempre realizável
        return True

    def atire(self,MundoW):
        """ Atira uma flecha, se possível, na direção indicada pela
            orientação da personagemNUSP, e verifica se acertou um Wumpus.
        """
        # personagem só pode atirar se tiver flechas...
        if self.nFlechas==0:
            print("Lamento, "+self.nome+", você não tem mais flechas...", sep="")
            return False
        # processa o tiro
        self.nFlechas -= 1
        self.modulo.nFlechas = self.nFlechas
        # calcula destino do tiro
        pos = self.posicao
        ori = self.orientacao
        posnova = [(pos[0]+ori[0])%self.N,
                   (pos[1]+ori[1])%self.N]
        # verifica se acertou um Wumpus e atualiza o mundo
        mundo = MundoW.mundo
        if mundo[posnova[0]][posnova[1]] == WUMPUS:
            mundo[posnova[0]][posnova[1]] = LIVRE # atualiza a sala com Wumpus
            MundoW.nWumpus -= 1 # contabiliza a morte
            MundoW.urro = True # propaga o som da morte do Wumpus
        # informa que o tiro foi realizado
        return True

    def compartilhe(self,MundoW):
        """ Nesta 1a versão do jogo, o compartilhamento permite à personagemNUSP
            apenas enxergar o que a personagem dummy conhece do mundo, caso as
            duas estejam na mesma sala.
        """
        # testa se a personagemNUSP e dummy estão na mesma sala
        if self.posicao != MundoW.dummy.posicao:
            print("Não há outras personagens nessa sala para compartilharem informações...")
            return False
        # transfere o conhecimento acumulado pela personagem dummy,
        # fazendo a conversão entre os sistemas de coordenadas 
        for i in range(self.N):
            for j in range(self.N):
                # lembrando que a personagemNUSP começou na posição (2,2)
                # e olhando para a direita, mas pensava que estava na
                # posição (0,0) olhando para baixo...
                self.modulo.mundoCompartilhado[j-2][2-i] = MundoW.dummy.mundo[i][j]
        # compartilhamento bem-sucedido!
        return True


class PersonagemNUSP(Personagem):
    """ Classe PersonagemNUSP: implementa um personagem definido através de um modulo.
        Essa classe tem um método construtor (__init__) que traz as definições do módulo,
        e implementa os métodos planejar e agir a partir das funções homônimas do módulo.
    """
    def __init__(self,N):
        """ Construtor da classe PersonagemNUSP
        """
        # localiza o código da personagem
        from glob import glob
        lista = glob("personagem*.py")
        self.modulo = __import__(lista[0][:-3]) # importa tirando o .py do nome
        self.nome = lista[0][10:-3]

        # inicializa a personagemNUSP
        self.estaviva = True # bem-vinda ao Mundo de Wumpus, personagemNUSP!
        self.N = N # copia a dimensão do mundo, pra facilitar
        self.posicao = [2,2] # coloca a personagemNUSP no centro do tabuleiro real...
        self.orientacao = [0,1] # ... e olhando para a direita
        self.nFlechas = 1 # primeiro chá de bebê da personagemNUSP
        self.modulo.inicializa(N) # chama a inicialização do módulo
        # define os valores que a personagemNUSP conhece
        self.modulo.nFlechas = self.nFlechas # copia nFlechas para o módulo
        self.modulo.mundoCompartilhado = [] # cria matriz NxN de listas vazias
        for i in range(N):
            self.modulo.mundoCompartilhado.append([[]]*N)

        # Usa um vetor com as funções acima para facilitar o processamento das ações.
        # Os índices correspondem aos valores atribuídos aos símbolos respectivos
        # ("A"<->0, "D"<->1, etc.)
        self.processe = [ self.ande, self.gireDireita, self.gireEsquerda, self.atire, self.compartilhe ]

    def planejar(self,percepcao):
        """ Método planejar (implementado pelo módulo)
        """
        self.modulo.planejar(percepcao)

    def agir(self):
        """ Método agir (implementado pelo módulo)
        """
        self.modulo.agir()


class Dummy(Personagem):
    """ Classe Dummy: implementa a personagem Dummy, que fica perambulando pelo mundo
        coletando informações, a fim de compartilhá-las com a personagemNUSP. Essa
        personagem só faz parte da parte A do EP3 (não existirá na parte B).    
    """
    from random import randint

    # direções de movimento para a personagem dummy:
    direcoes = [ [1,0], [0,1], [-1,0], [0,-1] ]

    def __init__(self,N,mundo):
        """ Construtor da classe Dummy.
        """
        self.N = N
        self.posicao = [0, 0]
        self.mundo = [ [ [], [], [], [], [] ],
                       [ [], [], [], [], [] ],
                       [ [], [], [], [], [] ],
                       [ [], [], [], [], [] ],
                       [ [], [], [], [], [] ] ]
        self.mundo[0][0] = [salas[mundo[0][0]]]


    def planejar(self,percepcao):
        """ A personagem Dummy não faz nenhum planejamento...
        """
        return

    def agir(self,pos,mundo):
        """ Move a personagem Dummy, sorteando uma das 4 direções;
            Essa personagem não tem raciocínio, e pode passar ilesa
            por muros, poços, Wumpus e etc. Mas ela gosta de se
            encontrar com a personagemNUSP que está na posicao pos.
        """
        # verifica se a personagemNUSP está na adjacência, e se move para lá
        if abs(pos[0]-self.posicao[0])+abs(pos[1]-self.posicao[1])==1:
            self.posicao[0], self.posicao[1] = pos[0], pos[1]
        else:
            # do contrário, sorteia uma direção qualquer para andar
            d = self.direcoes[self.randint(0,3)]
            self.posicao[0],self.posicao[1] = (self.posicao[0]+d[0])%self.N,(self.posicao[1]+d[1])%self.N
            self.mundo[self.posicao[0]][self.posicao[1]] = [salas[mundo[self.posicao[0]][self.posicao[1]]]]


# Chamada principal... é aqui que toda a mágica acontece!

m = MundoDeWumpus()

