
# Experimento de medição de tempo de 3 algoritmos de ordenação:
# ordenação por inserção (insertion sort), ordenação por intercalação
# (mergesort) e ordenação por contagem (counting sort).
# O objetivo é gerar saídas de texto com pares de números
# (tamanho do vetor, tempo de execução) para serem visualizados com
# o comando graph de plotutils. Para instalar o pacote plotutils
# em Linux basta rodar sudo apt install plotutils
# Para outros sistemas, veja a página
# https://www.gnu.org/software/plotutils/

from time import clock

from random import randint, seed

from conjunto import conjunto

from recursao_mergesort import mergesort as ms

# os elementos são inteiros entre 0 e M:
M = 10**3

# os tamanhos de vetor são os seguintes:
NNs = range(10,500,10)

def mergesort(vetor):
    ms(vetor,0,len(vetor))

def insertionsort(vetor):
    conj = conjunto(len(vetor)+1)
    conj.insere(vetor)

# vetor (estático) de contadores usados no counting sort.
contador = [ 0 ]*(M+1)
def countingsort(vetor):
    for vi in vetor:
        contador[vi] += 1
    k = 0
    for i in range(M+1):
        for j in range(contador[i]):
            vetor[k] = i
            k += 1
        contador[i] = 0

class Experimento:

    def criavetoraleatorio(self,N,M):
        self.vetor = []
        for i in range(N):
            self.vetor.append(randint(0,M))

    def ordenaecronometra(self,metodo):
        tantes = clock()
        metodo(self.vetor.copy())
        tdepois = clock()
        return tdepois-tantes

    def __init__(self,NNs,M):
        metodos = [ insertionsort, mergesort, countingsort ]
        # cria um dicionário de arquivos, que é como um vetor, mas indexado pelo método
        arquivo = {}
        for metodo in metodos:
            arquivo[metodo] = open("tempos-"+metodo.__name__+".txt","w")
        for N in NNs: # NNs contém todos os tamanhos de vetor
            for metodo in metodos:
                print("Executando",metodo.__name__,"para N="+str(N))
                # faz 100 repetições para cada N e cada método
                seed(0) # garante que todos os métodos usam os mesmos vetores
                tempo = 0 # usado para calcular o tempo médio
                for j in range(100):
                    self.criavetoraleatorio(N,M)
                    tempo += self.ordenaecronometra(metodo)/100
                # escreve no arquivo do método m o par "N tempo"
                arquivo[metodo].write(str(N)+"\t"+str(tempo)+"\n")
        for metodo in metodos:
            arquivo[metodo].close()

    
# roda o experimento completo, gerando os arquivos
# tempos-insertionsort.txt, tempos-mergesort.txt e tempos-countingsort.txt
# que podem ser visualizados separadamente com
# graph -T X tempos-metodo.txt
# ou conjuntamente com
# graph -T X tempos-insertionsort.txt tempos-mergesort.txt tempos-countingsort.txt
# A imagem pode ser guardada com
# graph -T svg tempos-insertionsort.txt tempos-mergesort.txt tempos-countingsort.txt > tempos.svg


e = Experimento(NNs,M)
