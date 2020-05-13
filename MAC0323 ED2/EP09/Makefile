CC      = gcc
CFLAGS  = -Wall -ansi -g -O0 -pedantic -Wno-unused-result -Wno-unused-function
RM      = rm
OBJS = util.o redblackst.o unit_test.o
#------------------------------------------------

# chama o linker
unit_test:  $(OBJS)
	$(CC)  $(OBJS) -o unit_test -lm

# gera o objeto da unit_test
unit_test.o: unit_test.c util.h redblackst.h 
	$(CC) $(CFLAGS) -c unit_test.c

# gera o objeto da ST
redblackst.o: redblackst.c redblackst.h util.h 
	$(CC) $(CFLAGS) -c redblackst.c

# gera o objeto das funcoes de uso geral
util.o: util.c util.h
	$(CC) $(CFLAGS) -c util.c 

clean:
	$(RM) *.o *~ unit_test

