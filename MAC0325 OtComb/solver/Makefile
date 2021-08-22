CXXFLAGS=-Wall -Wextra -std=c++17 -fsanitize=address -g
ARTIFACTS=digraph.o shortest_walks.o flow_solver.o

exercise1: exercise1.cpp $(ARTIFACTS)
		$(CXX) $(CXXFLAGS) $(ARTIFACTS) exercise1.cpp -o exercise1

clean:
		rm $(ARTIFACTS) exercise1
