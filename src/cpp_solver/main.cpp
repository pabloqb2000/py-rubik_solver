#include "CubeModel/Cube.h"
#include "Solver/IDDFSSolver.h"
#include <iostream>

int main() {
    Cube myCube = Cube("RRRUUUUUULLLLLUUFFFFFFFFRRDDDRRRBBBBBBBBDDDDLLLD");
    myCube.scramble(3);
    cout << myCube.toString() << endl;
    CubeNode node(myCube);

    IDDFSSolver solver;
    solver.printSolution(
        solver.findGoal(node)
    );

    return 0;
}
