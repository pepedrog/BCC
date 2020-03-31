mcalc: mcalc.tab.o lex.yy.o main.o symrec.o
	gcc -o $@ $^ -lm -lfl

mcalc.tab.o: mcalc.y
	bison -d mcalc.y
	gcc -c mcalc.tab.c

lex.yy.o: mcalc.l
	flex mcalc.l
	gcc -c lex.yy.c

symrec.o: symrec.c calc.h
	gcc -c symrec.c

clean:
	rm -f *.o lex.yy.c mcalc.tab.c mcalc.tab.h *~
