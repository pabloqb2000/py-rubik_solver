PROGRAMS = CubeModel/Cube.cpp \
Solver/IDDFSSolver.cpp \
Solver/ThistlethwaitesSolver.cpp \
Solver/GroupNodes/CubeNode.cpp \
Solver/GroupNodes/CubeNodeG1.cpp \
Solver/GroupNodes/CubeNodeG2.cpp \
Solver/GroupNodes/CubeNodeG3_1.cpp \
Solver/GroupNodes/CubeNodeG3_2.cpp \
Solver/GroupNodes/SavePerms.cpp

all: main

main: main.cpp $(PROGRAMS)
	g++ -o main.exe main.cpp $(PROGRAMS)
	./main.exe

run:
	./main.exe

clean:
	rm -rf *.o *.exe