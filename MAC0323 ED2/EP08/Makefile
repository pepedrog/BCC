CC      = gcc
CFLAGS  = -Wall -ansi -g -O0 -pedantic -Wno-unused-result -Wno-unused-function
# o valgrind pede a opcao -g -O0
# usei C ANSI, mas quem quiser pode usar C99.
# CFLAGS  = -Wall -std=c99 -g -O0 -pedantic -Wno-unused-result -Wno-unused-function
RM      = rm
OBJS = util.o binarysearchst.o unit_test.o
#------------------------------------------------

# chama o linker
unit_test:  $(OBJS)
	$(CC)  $(OBJS) -o unit_test -lm

# gera o objeto da unit_test
unit_test.o: unit_test.c util.h binarysearchst.h 
	$(CC) $(CFLAGS) -c unit_test.c

# gera o objeto da ST
binarysearchst.o: binarysearchst.c binarysearchst.h util.h 
	$(CC) $(CFLAGS) -c binarysearchst.c

# gera o objeto das funcoes de uso geral
util.o: util.c util.h
	$(CC) $(CFLAGS) -c util.c 

clean:
	$(RM) *.o *~ unit_test

