tudo: pep linguagem
pep: pep.tab.o lex.yy.o main.o 
	gcc -o $@ $^  -lfl

pep.tab.o: pep.y
	bison -d pep.y
	gcc -c pep.tab.c

lex.yy.o: pep.l
	flex pep.l
	gcc -c lex.yy.c

linguagem: linguagem.rkt
	raco exe $<

clean:
	rm -f *.o lex.yy.c mcalc.tab.c mcalc.tab.h linguagem *~
