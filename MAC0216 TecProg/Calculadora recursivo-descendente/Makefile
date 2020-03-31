OPT= --pedantic --ansi -Wall

calc : recur.o analex.o calc.o
	gcc $(OPT) -o calc recur.o analex.o calc.o -lm

recur.o : recur.c analex.h recur.h
	gcc $(OPT) -c recur.c

analex.o : analex.c analex.h
	gcc $(OPT) -c analex.c

calc.o : calc.c recur.h analex.h
	gcc $(OPT) -c calc.c

clean: 
	rm -f *.o *~ calc


