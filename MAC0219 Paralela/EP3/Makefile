CC=gcc
TARGET=monte_carlo
SOLUTION_TARGET=monte_carlo_solution
SRC=monte_carlo.c
SOLUTION_SRC=monte_carlo_solution.c
CFLAGS=-Wall
CLIBS=-lpthread -lm

all:
	$(CC) $(SRC) -o $(TARGET) $(CFLAGS) $(CLIBS)

debug:
	$(CC) $(SRC) -o $(TARGET) $(CFLAGS) $(CLIBS) -DDEBUG=1

verbose:
	$(CC) $(SRC) -o $(TARGET) $(CFLAGS) $(CLIBS) -DDEBUG=1 -DVERBOSE=1

solution:
	$(CC) $(SOLUTION_SRC) -o $(SOLUTION_TARGET) $(CFLAGS) $(CLIBS)

solution-debug:
	$(CC) $(SOLUTION_SRC) -o $(SOLUTION_TARGET) $(CFLAGS) $(CLIBS) -DDEBUG=1

clean:
	rm $(TARGET) $(SOLUTION_TARGET)
