# Makefile para MAC0328 (2019).
# CodificaÃ§Ã£o: UTF-8.
# Modifique Ã  vontade!
########################################################################


# STD = -ansi
STD = -std=c99

OP1  = -Wall -Wextra -Wpedantic -Wshadow

OP2 = -Wno-unused-result -Wno-unused-function

## optimization
OPTM = -O0
# OPTM = -O2

# GDB = -g

# onde compilador deve procurar GRAPHlists.h, QUEUE.h, etc.
INC = -I./bib

LM = 
# LM = -lm
##  in case you use sqrt, sin, cos, etc.

# serÃ£o compilados junto com programa-cliente
BIB = \
bib/GRAPHlists.c \
bib/QUEUE.c \
bib/PQ.c \
bib/UF.c \
bib/MYTOOLS.c

VERBOSE = -v

.FORCE :

default : 
	@echo "Para compilar prog.c diga make prog"
	@echo ""

% : %.c .FORCE
	@echo "-------"
	gcc $(STD) $(OP1) $(OP2) $(OPTM) $(INC) $< $(BIB) -o $@ $(LM)
	@echo "-------"
	@echo ""


