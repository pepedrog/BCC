CC      = gcc
CFLAGS  = -Wall -ansi -g -O0 -pedantic -Wno-unused-result -Wno-unused-function
RM      = rm
OBJS = util.o bag.o digraph.o unit_test.o
#------------------------------------------------

# chama o linker
unit_test:  $(OBJS)
	$(CC)  $(OBJS) -o unit_test -lm

# gera o objeto da unit_test
unit_test.o: unit_test.c util.o bag.o digraph.o 
	$(CC) $(CFLAGS) -c unit_test.c

# gera o objeto de DIGRAPH
digraph.o: digraph.c digraph.h bag.o
	$(CC) $(CFLAGS) -c digraph.c

# gera o objeto da BAG
bag.o: bag.c bag.h util.o 
	$(CC) $(CFLAGS) -c bag.c

# gera o objeto das funcoes de uso geral
util.o: util.c util.h
	$(CC) $(CFLAGS) -c util.c 

clean:
	$(RM) *.o *~ unit_test

