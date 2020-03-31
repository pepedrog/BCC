class Warner:
    def oie(x):
        print("O que que há, velhinho?")


class Pacman(Warner) :
    def __init__(self, n="Mario"):
        self.nome = n
        self.boca = False
        self.orientação = 2
        self.posição = [0,0]
        self.vivo = True

    def anda(self, direção) :
        self.orientação = direção
        self.boca = not self.boca
        if self.orientação == 0 :
            self.posição[1] += 1
        elif self.orientação == 2 :
            self.posição[1] -= 1
        elif self.orientação == 1 :
            self.posição[0] += 1
        elif self.orientação == 3 :
            self.posição[0] -= 1


    def __str__(s) :
        return "Pacman "+s.nome

    def mostra(s):
        pb = "fechada"
        if s.boca :
            pb = "aberta"
        print("%s está em (%d,%d) com a boca %s\n"%(s.nome, s.posição[0], s.posição[1], pb))

    def oi(s) :
        print("Oi de ", s.nome)

    def tchau(self) :
        print(self.nome,  " foi embora")

class Fantasma :
    tot = 0
    def __init__(s):
        s.num = Fantasma.tot
        Fantasma.tot += 1
        print(s, s.num,"Encarnou..")

    def __str__(s) :
        return "Fantasma 👻"
        
    def oi(s) :
        print("Boo de ", s.num)


p1 = Pacman("Shigeru")
p2 = Pacman("Myamoto")
p3 = Pacman()

Nick      = Fantasma()
Gaspar    = Fantasma()
Penadinho = Fantasma()
Samara    = Fantasma()

def oi(x) :
    print("Achei um ", x)
    
p1.oie()
oi(p1)

Samara.oi()
p2.oi()
p1.tchau()

p2.anda(2)
p2.anda(1)
p2.anda(1)
p2.anda(3)
p2.mostra()
Nick.oi()

print("No total são {} fantasmas".format(Fantasma.tot))
