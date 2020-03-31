# -*- coding: utf-8 -*-
"""
  AO PREENCHER ESSE CABEÇALHO COM O MEU NOME E O MEU NÚMERO USP, 
  DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESSE PROGRAMA. 
  TODAS AS PARTES ORIGINAIS DESSE EXERCÍCIO PROGRAMA (EP) FORAM 
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUÇÕES
  DESSE EP E QUE PORTANTO NÃO CONSTITUEM DESONESTIDADE ACADÊMICA
  OU PLÁGIO.  
  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR TODAS AS CÓPIAS
  DESSE PROGRAMA E QUE EU NÃO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUIÇÃO. ESTOU CIENTE QUE OS CASOS DE PLÁGIO E
  DESONESTIDADE ACADÊMICA SERÃO TRATADOS SEGUNDO OS CRITÉRIOS
  DIVULGADOS NA PÁGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NÃO SERÃO CORRIGIDOS E,
  AINDA ASSIM, PODERÃO SER PUNIDOS POR DESONESTIDADE ACADÊMICA.

  Nome : Pedro Gigeck Freire
  NUSP : 10737136
  Turma: t45
  Prof.: Marcelo Queiroz

  
"""
import sys
import pygame
import time
from random import randint
from math import floor, ceil
#from time import Timer

class Personagem:
    """ Classes que serão o molde de cada personagem, 
        como se cada instância dessa classe fosse um corpo que algum módulo comandará
    """
    def __init__(self, modulo, nome, N):
        """ Construtor da classe Personagem
        """
        # inicializa a personagemNUSP
        self.estaviva = True # bem-vinda ao Mundo de Wumpus, personagem!
        self.N = N #copia a dimensão do mundo, pra facilitar
        self.impacto = False
        #Sorteia uma imagem de algum personagem para a personagem (para os personagem não terem imagens iguais)
        self.numerodaimagem = randint(5,10)
        #sorteia a posição e orientação iniciais
        self.posicao = [randint(0, N -1),randint(0, N -1)] 
        self.orientacao = randint(1, 4)
        if self.orientacao == 1:
            self.orientacao = [0,1]
        elif self.orientacao == 2:
            self.orientacao = [0,-1]          
        elif self.orientacao == 3:
            self.orientacao = [1,0]
        else:
            self.orientacao = [-1,0]
            
        
        self.nFlechas = 1 #valor default do numero de flechas de cada personagem
        
        self.modulo = modulo
        self.nome = nome
        
        self.modulo.inicializa(N) # chama a inicialização do módulo
        # define os valores que a personagemNUSP conhece
        self.modulo.nFlechas = self.nFlechas # copia nFlechas para o módulo
        
        self.modulo.mundoCompartilhado = [] # cria matriz NxN de listas vazias
        for i in range(N):
            self.modulo.mundoCompartilhado.append([[]]*N)
        
    def ande(self,MundoW):
        """ Função ande: verifica se é possível mover a personagem
            na direção indicada por sua orientação, e as consequências
            disso.
        """
        # calcula a posição nova
        posnova = [(self.posicao[0]+self.orientacao[0])%self.N,
                   (self.posicao[1]+self.orientacao[1])%self.N]
        # se houver um muro, não dá para andar
        mundo = MundoW.mundo
        if "M" in mundo[posnova[0]][posnova[1]]:
            self.impacto = True
        else:
            #Se remove da sala que estava
            MundoW.mundo[self.posicao[0]][self.posicao[1]].remove(self)
            #Atualiza a posição
            self.posicao[0],self.posicao[1] = posnova[0],posnova[1]
            #Se coloca na sala atual
            MundoW.mundo[self.posicao[0]][self.posicao[1]].append(self)
            #Se houver wumpus ou poço, é game over para a personagemNUSP
            if mundo[self.posicao[0]][self.posicao[1]] in [ "W", "P" ]:
                self.estaviva = False # NÃÃÃÃÃÃÃOOOOOOOOO!!!!!!!!!!!!
                self.morrer()
        # tentar andar é sempre realizável
        return True

    def gireDireita(self):
        """ Corrige a orientação através de um giro no sentido horário.
        """
        if self.orientacao[1]==0:
            self.orientacao[0] = -self.orientacao[0]
        self.orientacao[0],self.orientacao[1] = self.orientacao[1],self.orientacao[0]
        # girar é sempre realizável
        return True

    def gireEsquerda(self):
        """ Corrige a orientação através de um giro no sentido anti-horário.
        """
        if self.orientacao[0]==0:
            self.orientacao[1] = -self.orientacao[1]
        self.orientacao[0],self.orientacao[1] = self.orientacao[1],self.orientacao[0]
        # girar é sempre realizável
        return True

    def atire(self,MundoW):
        """ Atira uma flecha, se possível, na direção indicada pela
            orientação da personagem, e verifica se acertou um Wumpus.
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
        if "W" in MundoW.mundo[posnova[0]][posnova[1]]:
            MundoW.mundo[posnova[0]][posnova[1]].append("L") # atualiza a sala com Wumpus
            MundoW.nWumpus -= 1 # contabiliza a morte
            MundoW.urro = True # propaga o som da morte do Wumpus
        # informa que o tiro foi realizado
        return True

    def compartilhe(self, mundoDosOutros, mundo):
        """ Recebe um mundo adaptado 
        """
        sala_atual = mundo[self.posicao[0]][self.posicao[1]]
        tem_alguem = False
        for elemento in sala_atual:
            if elemento != "L" and elemento != self:
                tem_alguem = True
                
            if tem_alguem:
                break
            
        if not tem_alguem:
            print("Atenção," + self.nome + "\nNão há outras personagens nessa sala para compartilharem informações...")
            return False
        # transfere o conhecimento acumulado pela personagem dummy,
        # fazendo a conversão entre os sistemas de coordenadas 
        for i in range(self.N):
            for j in range(self.N):
                #Poe as coisas do MundoDosOutros no mundoCompartilhado se o mundoCompartilhado já não conhecer essa coisa
                for coisa in mundoDosOutros[i][j]:
                    if coisa not in self.modulo.mundoCompartilhado[i][j]:
                        self.modulo.mundoCompartilhado[i][j].append(coisa)
        # compartilhamento bem-sucedido!
        return True

    def planejar(self,percepcao):
        """ Método planejar (implementado pelo módulo)
        """
        self.modulo.planejar(percepcao)

    def agir(self):
        """ Método agir (implementado pelo módulo)
        """
        return self.modulo.agir()
        
    def morrer(self, MundoW):
        self.estaviva = False
        #se remove do mundo 
        self.MundoW.mundo[self.posicao[0]][self.posicao[1]].remove(self)
        
class ListaDePersonagens:
    """ Classe que sincroniza as ações e planejamentos de todas as personagens
    """
    def __init__(self, plista, N):
        self.lista = []
        for personagem in plista:
            #Cria a lista já instanciando os personagens (importando da lista de nomes dos módulos recebida sem o '.py')
            self.lista.append(Personagem(__import__(personagem[:-3]), personagem[:-3], N))
            
    def processaPercepcoes(self, mundo, personagem, urro):
        """Método que interpreta o mundo ao redor de algum personagem e retorna para este alguma percepção
        """
        N = len(mundo)
        percepcoes = []
         
        #Se tiver alguma coisa na casa em que o personagem está (Que não pode ser W ou P senão não poderia ter ninguém lá)
        for outrapessoa in mundo[personagem.posicao[0]][personagem.posicao[1]]:
            #Se essa coisa não for o próprio personagem, então podemos adicionar esse outro personagem às percepções
            if outrapessoa != "L" and outrapessoa.nome != personagem.nome:
                percepcoes.append(outrapessoa.nome)
        
        salas_vizinhas = [mundo[(personagem.posicao[0] + 1)%N][personagem.posicao[1]],
                          mundo[(personagem.posicao[0] - 1)%N][personagem.posicao[1]],
                          mundo[personagem.posicao[0]][(personagem.posicao[1] + 1)%N],
                          mundo[personagem.posicao[0]][(personagem.posicao[1] - 1)%N]]
            
        #Adicionando F e B às percepções caso Wumpus ou Poço nas salas vizinhas
        for vizinha in salas_vizinhas:
            if "W" in vizinha and "F" not in percepcoes:
                percepcoes.append("F")             
            if "P" in vizinha and "B" not in percepcoes:
                percepcoes.append("B")
        
        if personagem.impacto:
            percepcoes.append("I")
            personagem.impacto = False
        if urro:
            percepcoes.append("U")
        return percepcoes
           
        
    def processaPlanejamentos(self, mWumpus):
        
        for personagem in self.lista:
             personagem.planejar(self.processaPercepcoes(mWumpus.mundo, personagem, mWumpus.urro))
        
    def processaCompartilhamentos(self, personagem, mundo):
        
        personagens_aqui = []
        for pessoa in mundo[personagem.posicao[0]][personagem.posicao[1]]:
            if pessoa != "L" and pessoa != personagem:
                personagens_aqui.append(pessoa)
        
        #Criando um mundo provisório com o tamanho correto
        mundoDosOutros = []
        N = len(mundo)
        for i in range(N):
            linha= []
            for j in range(N):
                linha.append([])
            mundoDosOutros.append(linha)
        for p in personagens_aqui:                       
                            
            orimod = personagem.modulo.orientacao
            orireal = personagem.orientacao
            
            porimod = p.modulo.orientacao
            porireal = p.orientacao
            #rotaciona o mundo do personagem pra ficar com a mesma orientacao do mundo real
            comando = "nenhum"
            if (orimod == [0, 1] and orireal == [1, 0]) or (orimod == [1, 0] and orireal == [0, -1]) or (orimod == [0, -1] and orireal == [-1, 0]) or (orimod == [-1, 0] and orireal == [0, 1]):
                comando = "tem que virar pra direita"               
            elif (orimod == [0, 1] and orireal == [-1, 0]) or (orimod == [1, 0] and orireal == [0, 1]) or (orimod == [0, -1] and orireal == [1, 0]) or (orimod == [-1, 0] and orireal == [0, -1]):
                comando = "tem que virar pra esquerda"               
            #elif (orimod == [0, 1] and orireal == [0, -1]) or (orimod == [1, 0] and orireal == [-1, 0]) or (orimod == [0, -1] and orireal == [0, 1]) or (orimod == [-1, 0] and orireal == [1, 0]):
            else: 
                comando = "tem que virar de cabeça pra baixo"
                
            #rotaciona o mundo do p pra ficar com a mesma orientacao do mundo real
            if (porimod == [0, 1] and porireal == [1, 0]) or (porimod == [1, 0] and porireal == [0, -1]) or (porimod == [0, -1] and porireal == [-1, 0]) or (porimod == [-1, 0] and porireal == [0, 1]):
                comandop = "tem que virar pra direita"
                
            elif (porimod == [0, 1] and porireal == [-1, 0]) or (porimod == [1, 0] and porireal == [0, 1]) or (porimod == [0, -1] and porireal == [1, 0]) or (porimod == [-1, 0] and porireal == [0, -1]):
                comandop = "tem que virar pra esquerda"
                
            #elif (porimod == [0, 1] and porireal == [0, -1]) or (porimod == [1, 0] and porireal == [-1, 0]) or (porimod == [0, -1] and porireal == [0, 1]) or (porimod == [-1, 0] and porireal == [1, 0]):
            else:
                comandop = "tem que virar de cabeça pra baixo"
                
            #Se as duas orientações são iguais, não precisa mexer na orientação dos mundos
            if comando != comandop:
                if comando == "nenhum":
                    if comandop == "tem que virar pra direita":
                        mundop = self.giraMundo(p.modulo.mundo, "direita")
                    elif comandop == "tem que virar pra esquerda":
                        mundop = self.giraMundo(p.modulo.mundo, "esquerda")
                    elif comandop == "tem que de cabeça pra baixo":
                        mundop = self.giraMundo(p.modulo.mundo, "baixo")
                        
                elif comando == "tem que virar pra direita":
                    if comandop == "nenhum":
                        mundop = self.giraMundo(p.modulo.mundo, "esquerda")
                    elif comandop == "tem que virar pra esquerda":
                        mundop = self.giraMundo(p.modulo.mundo, "baixo")
                    elif comandop == "tem que virar de cabeça pra baixo":
                        mundop = self.giraMundo(p.modulo.mundo, "direita")
                        
                elif comando == "tem que virar pra esquerda":
                    if comandop == "tem que virar pra direita":
                        mundop = self.giraMundo(p.modulo.mundo, "baixo")
                    elif comandop == "nenhum":
                        mundop = self.giraMundo(p.modulo.mundo, "direita")
                    elif comandop == "tem que virar de cabeça pra baixo":
                        mundop = self.giraMundo(p.modulo.mundo, "direita")
                        
                elif comando == "tem que virar de cabeça pra baixo":
                    if comandop == "tem que virar pra direita":
                        mundop = self.giraMundo(p.modulo.mundo, "esquerda")
                    elif comandop == "nenhum":
                        mundop = self.giraMundo(p.modulo.mundo, "baixo")
                    elif comandop == "tem que virar pra esquerda":
                        mundop = self.giraMundo(p.modulo.mundo, "direita")
                        
            #Aqui o mundop está com a orientação do mundo da personagem
            
            #vamos agora colocar as casas nas posições corretas
            deltai = p.modulo.posicao[0] - personagem.modulo.posicao[0]
            deltaj = p.modulo.posicao[1] - personagem.modulo.posicao[1]
            
            mundop = self.transladaMundo(mundo, deltai, deltaj)
            print(len(mundop), len(mundop[0]), len(mundo))
            for i in range(len(mundo)):   
                for j in range(len(mundo)):
                    for coisa in mundop[i][j]:
                        if coisa == "V":
                            coisa = "L"
                        if coisa not in mundoDosOutros:
                            mundoDosOutros.append(coisa)
                            
            print("Mundo dos outros:")
            for i in range(len(mundo)):
                for j in range(len(mundo)):
                   print("".join(mundoDosOutros[i][j]),end="\t| ")        
                print("\n"+"-"*(8*len(mundo)+1))
        
        return personagem.compartilhe(mundoDosOutros, mundo)
    
    def giraMundo(self, mundo, direcao):
        
        print("Mundop sem ta rotacionado:")
        for i in range(len(mundo)):
            for j in range(len(mundo)):
               print("".join(mundo[i][j]),end="\t| ")        
            print("\n"+"-"*(8*len(mundo)+1))           
        
        N = len(mundo)
        #Só criando um mundo no tamanho certo
        mundo_girado = []
        for i in range(N):
            linha = []
            for j in range(N):
                linha.append([])
            mundo_girado.append(linha)
            
        for i in range(N):
            for j in range(N):
                if direcao == "direita":
                    #As colunas viram linhas (j vira i e o que tava em baixo vai pro começo da linha) 
                    #mundo_girado[j][N-1-i] = mundo[i][j]
                    mundo_girado[i][j].append(mundo[abs(j - (N-1))][i])
                    
                elif direcao == "esquerda":
                    #As colunas viram linhas (mas agora o que tava em baixo vai pro final da linha)
                    #mundo_girado[N-1-j][i] = mundo[i][j]
                    mundo_girado[i][j].append(mundo[j][abs(i - (N-1))])
                    
                elif direcao == "baixo":
                    #Só inverte as linhas
                    mundo_girado[N-1-i][N-1-j].append(mundo[i][j])
                    #mundo_girado[i][j] = mundo[j][abs(i - (N-1))]
        
        print("Mundo_girado rotacionado para:", direcao)
        for i in range(N):
            for j in range(N):
                print("".join(str(mundo_girado[i][j])),end="\t| ")
            print("\n"+"-"*(8*len(mundo)+1))
        return mundo_girado
    
    def transladaMundo(self, mundo, diferencai, diferencaj):
        N = len(mundo)
        #Só criando um mundo no tamanho certo
        N = len(mundo)
        #Só criando um mundo no tamanho certo
        mundo_transladado = []
        for i in range(N):
            linha = []
            for j in range(N):
                linha.append([])
            mundo_transladado.append(linha)
        for i in range(N):
            for j in range(N):
                mundo_transladado[(i - diferencai)%N][(j - diferencaj)%N] = mundo[i][j]
                
        return mundo_transladado
        
            
            
        
        
        
    def processaAcoes(self, MundoW):      
        
        #lista dos personagem que andarão, pois serão os últimos a realizar suas ações
        nomades = []
        
        for personagem in self.lista:
            
            #Preferi fazer do jeito menos ousado (sem aquele vetor de funções todo sofisticado)
            viavel = False
            while not viavel:
                acao = personagem.agir()
                if acao == "A":
                    nomades.append(personagem)
                    viavel = True
                elif acao == "T":
                    viavel = personagem.atire(MundoW)
                elif acao == "C":
                    viavel = self.processaCompartilhamentos(personagem, MundoW.mundo) 
                elif acao == "E":
                    personagem.gireEsquerda()
                    viavel = True
                elif acao == "D":
                    personagem.gireDireita()
                    viavel = True
        
        for personagem in nomades:
            personagem.ande(MundoW)
        
class Interface:
    """Classe que comandará a parte visual do mundo
    """
    
    def __init__(self,mundo, M, S):
        
        #Inicializando os atributos com valores default
        self.N = len(mundo)
        self.M = M
        self.S = S
        self.I0 = 0
        self.J0 = 0
        self.deltaT = -1 
        self.mundo = mundo
        #Cálculo do tamanho de cada imagem para que a tela toda fique preenchida com SxS imagens 
        self.tamanho_imagens = floor(self.M/self.S)
        
        self.imagens = []
        #Método para definir as imagens pelo tamanho
        self.redimensionaImagens(self.tamanho_imagens)
        
        #Inicia o módulo pygame
        pygame.init()
        

        #Carrega o logo do jogo
        logo = pygame.image.load("anel.jpg")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Mundo de Wumpus")
        
        self.atualizaTela(mundo)
        

    def atualizaTela(self, mundo):
        """ Método que projeta na tela o mundo, de acordo com a resolução,
            "zoom" e qual sala estará em [0,0] da instância atual.
        """
        #Constroi a tela de tamanho MxM
        self.tela = pygame.display.set_mode((self.M,self.M))
        
        #Coordenadas em pixels da tela
        coordenadas = [0,0]
        #Coordenadas em salas do mundo
        I = 0
        J = 0
        #Percorre as linhas da tela
        while coordenadas[1] < self.M :
            #Percorre as colunas da tela
            while coordenadas[0] < self.M:
                #Encontra quais serão os índices do mundo de acordo com a sala em 0,0
                inovo = (I + self.I0)%self.N
                jnovo = (J + self.J0)%self.N
                #Preenche a tela de acordo com o conteúdo do mundo
                
                for coisas in mundo[inovo][jnovo]:
                    #Se for um Wumpus
                    if coisas == "W":
                        self.tela.blit(self.imagens[1],(coordenadas[0],coordenadas[1]))
                        self.tela.blit(self.imagens[4],(coordenadas[0],coordenadas[1]))
                    #se não for um wumpus, já põe a grama
                    else:
                        self.tela.blit(self.imagens[0],(coordenadas[0],coordenadas[1]))
                    #Se for um muro
                        if coisas == "M":
                            self.tela.blit(self.imagens[2],(coordenadas[0],coordenadas[1]))
                    #Se for um poço   
                        elif coisas == "P":
                            self.tela.blit(self.imagens[3],(coordenadas[0],coordenadas[1]))
                    #Se for um personagem
                        elif coisas != "L": #se for um personagem
                            i = coisas.numerodaimagem
                            #Coloca a imagem do personagem girando ele de acordo com a orientação
                            if coisas.orientacao == [-1,0]:
                                self.tela.blit(self.imagens[i],(coordenadas[0],coordenadas[1]))
                            elif coisas.orientacao == [0,1]:
                                self.tela.blit(pygame.transform.rotate(self.imagens[i],270),(coordenadas[0],coordenadas[1]))
                            elif coisas.orientacao == [1,0]:
                                self.tela.blit(pygame.transform.rotate(self.imagens[i],180),(coordenadas[0],coordenadas[1]))
                            else:
                                self.tela.blit(pygame.transform.rotate(self.imagens[i],90),(coordenadas[0],coordenadas[1]))

                #Troca o índice do mundo e o ponto da tela para inserir a próxima imagem
                coordenadas[0] += self.tamanho_imagens
                J += 1
            coordenadas[1] += self.tamanho_imagens
            I += 1
            J = 0
            coordenadas[0] = 0
        #Atualiza tela
        pygame.display.flip()
    
    def processaComando(self, comando):
        """ Método para interpretar o comando recebido do teclado
        """
        if comando == pygame.K_LEFT:
            self.J0 -= 1
             
        elif comando == pygame.K_RIGHT:
            self.J0 += 1
      
        elif comando == pygame.K_UP:
            self.I0 -= 1
            
        elif comando == pygame.K_DOWN:
            self.I0 += 1
            
        elif comando == pygame.K_COMMA:
            self.deltaT /= 1.5
            
        elif comando == pygame.K_PERIOD:
            self.deltaT *= 1.5
        
        elif comando == pygame.K_SPACE:
            self.deltaT *= -1
        
        else:
            if comando == pygame.K_KP_MINUS or comando == pygame.K_MINUS:
                self.S += 0.5
        
            elif comando == pygame.K_EQUALS or comando == pygame.K_KP_EQUALS:
                #O menor valor de S permitido é 1
                if self.S > 1.5:
                    self.S -= 0.5
                else:
                    self.S = 1
            
            self.redimensionaImagens(floor(self.M/self.S))
                
        self.atualizaTela(self.mundo) 
        
    def redimensionaImagens(self,novoTamanho):
        """ Método que recarrega as imagens de acordo com um novo tamanho
        """  
        self.tamanho_imagens = novoTamanho        
        nome_imagens = ["grama.jpg", "gramaorc.jpg","muro.png","poco.png","orc.png","personagem1.png","personagem2.png","personagem3.png","personagem4.png","personagem5.png","personagem6.png"]        
        self.imagens = []
        for i in range(len(nome_imagens)):
            #recarrega as imagens, ao invés de só redimensionar,
            #para não perder resolução após muitos zooms
            self.imagens.append(pygame.image.load(nome_imagens[i]))
            self.imagens[i] = pygame.transform.scale(self.imagens[i],(novoTamanho,novoTamanho))
        
        #De modo que
        #imagens[0] = Grama de fundo (Sala Livre)
        #imagens[1] = Grama escura (Fundo da sala de um Wumpus)
        #imagens[2] = Muro
        #imagens[3] = Poço
        #imagens[4] = Orc (Wumpus)
        #imagens[5] = Frodo (Personagem)
        #imagens[6] = Boromir (Personagem)
        #imagens[7] = Gandalf (Personagem)
        #imagens[8] = Gimli (Personagem)
        #imagens[9] = Aragorn (Personagem)
        #imagens[10] = Legolas (Personagem)
        
class MundoDeWumpus:
    
    def __init__(self):
        
        self.urro = False
        
        #Primeiro pega os nomes dos arquivos dos personagens só para saber quantos são
        from glob import glob
        self.personagens = glob("personagem*.py")
        
        #Calcula algumas variáveis da especificação de acordo com o número de personagens (valor default)
        self.P = len(self.personagens)
        M = 800
        S = 5
        α = 0.2
        β = 0.2
        γ = 0.9
        δ = 0.5

        parametros = [M, S, α, β, γ, δ]
        i = 0
        for arg in sys.argv:
            parametros[i] = arg
            i+=1
            
        self.N = ceil((γ*self.P/(1-α-β-δ))**0.5)
        
        nMuros = floor(self.N*α)
        nPocos = floor(self.N*β)
        self.nWumpus = floor(self.P*γ)
        
        #Redefine a lista dos personagens com os objetos da classe Personagem, agora que já sabemos o N
        self.personagens = ListaDePersonagens(self.personagens, self.N)
        #Neste momento, cada personagem já tem sua posição, sprteada na instanciação
        
        #Criando o mundo
        self.mundo = []
        for i in range(self.N):
            linha = []
            for j in range(self.N):
                linha.append([])
            self.mundo.append(linha)
            
        #vamos preencher o mundo com os personagens:
        for p in self.personagens.lista:
            if "L" not in self.mundo[p.posicao[0]][p.posicao[1]]:
                self.mundo[p.posicao[0]][p.posicao[1]].append("L")
            self.mundo[p.posicao[0]][p.posicao[1]].append(p)
        
        #Preenche a quantidade de sala dos muros, poços e wumpus
        #em salas aleatórias e vazias do mundo
        for muro in range(nMuros):
            #sorteia uma posição vazia pro muro 
            i,j = randint(0,self.N - 1),randint(0,self.N - 1)
            while self.mundo[i][j] != []:
                i,j = randint(0,self.N - 1),randint(0,self.N - 1)
            self.mundo[i][j].append("M")
                    
        for poco in range(nPocos):
            #sorteia uma posição vazia pro poço 
            i,j = randint(0,self.N - 1),randint(0,self.N - 1)
            while self.mundo[i][j] != []:
                i,j = randint(0,self.N - 1),randint(0,self.N - 1)
            self.mundo[i][j].append("P")
            
        for wumpus in range(self.nWumpus):
            #sorteia uma posição vazia pro Wumpus 
            i,j = randint(0,self.N - 1),randint(0,self.N - 1)
            while self.mundo[i][j] != []:
                i,j = randint(0,self.N - 1),randint(0,self.N - 1)
            self.mundo[i][j].append("W")
            
        #Preenche as casas restantes como livres 
        for i in range(self.N):
            for j in range(self.N):
                if self.mundo[i][j] == []:
                    self.mundo[i][j].append("L")
                #print(self.mundo[i][j],end="\t| ")
            #print("\n"+"-"*(8*self.N+1))
            
        #Com o mundo todo preenchido, podemos gerar a interface!
        self.interface = Interface(self.mundo, M, S)
        
        self.processaJogo()
                
        self.finalizaJogo()
        
    def processaJogo(self):
        
        a = time.clock()
        running = True
        #Parte feita baseada nos tutoriais sugeridos
        while running and self.nWumpus > 0 and self.P > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Sai do loop principal
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.interface.processaComando(event.key)
            
            b = time.clock()
            #Sempre já tiver passado deltaT de tempo e o jogo não estiver pausado
            if self.interface.deltaT > 0 and b - a > self.interface.deltaT: 
                a = b
                #Faz o turno
                self.Turno()
            
    def Turno(self):
        
        print("\n novo turno\n")
        self.personagens.processaPlanejamentos(self)
        self.personagens.processaAcoes(self)
        for i in range(self.P):    
            print(self.personagens.lista[i].nome,"posicao",self.personagens.lista[i].posicao,"orientacao",self.personagens.lista[i].orientacao)
        self.interface.atualizaTela(self.mundo)
        
               
        
    def finalizaJogo(self):
        if self.nWumpus == 0:
            print("Parabéns Jogadores!")
        else:
            print("Parabéns Wumpus!")

m = MundoDeWumpus()