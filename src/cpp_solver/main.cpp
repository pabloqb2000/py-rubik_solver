#include "CubeModel/Cube.h"
#include "Solver/ThistlethwaitesSolver.h"
#include "Solver/GroupNodes/SavePerms.h"
#include <iostream>

int main() {
    Cube myCube;
    myCube.scramble(100);
    
    ThistlethwaitesSolver solver;
    solver.solve(myCube);

    return 0;
}
