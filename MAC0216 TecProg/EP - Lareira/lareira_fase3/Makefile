LOADLIBES= -lfl -lreadline
CFLAGS=-Wall -g

all: jogo

%.c: %.y
	bison $<
	mv $*.tab.c $*.c

jogo: jogo.o jogol.o main.o traduzindo.o acoes.o salas.o hash.o lista.o elemento.o
	gcc -o $@ $^ $(LOADLIBES) -Wall

jogo.c : jogo.y

jogol.o: jogol.l jogo.c

%.o : %.c
	gcc -o $@ -c $< $(LOADLIBES)

clean:
	rm -f jogo *tab* *.o *~ jogo.c
