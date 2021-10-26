all: main

main: main.cpp CubeModel/Cube.cpp Solver/IDDFSSolver.cpp Solver/CubeNode.cpp
	g++ -o main.exe main.cpp CubeModel/Cube.cpp Solver/IDDFSSolver.cpp Solver/CubeNode.cpp
	./main.exe

run:
	./main.exe

clean:
	rm -rf *.o *.exe