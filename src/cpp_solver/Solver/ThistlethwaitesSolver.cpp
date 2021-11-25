#include "ThistlethwaitesSolver.h"
#include <iostream>
using namespace std;

stack<Cube::MOVE> ThistlethwaitesSolver::solve(const Cube& cube)
{
    cout << "Solving G1" << " -> ";
    CubeNodeG1 cube_node_g1(cube);
    stack<Cube::MOVE> s1 = this->findGoal(cube_node_g1, 8);   // Should finish in <= 7 moves
    this->minMove += 4; // Prune U U' D D'

    cout << "Solving G2" << " -> ";
    CubeNodeG2 cube_node_g2((Cube)cube_node_g1);
    stack<Cube::MOVE> s2 = this->findGoal(cube_node_g2, 11);  // Should finish in <= 10 moves
    this->minMove += 4; // Prune F F' B B'

    cout << "Solving G3.1" << " -> ";
    CubeNodeG3_1 cube_node_g3_1((Cube)cube_node_g2);
    stack<Cube::MOVE> s3 = this->findGoal(cube_node_g3_1, 14);// Should finish in <= 13 moves

    cout << "Solving G3.2" << " -> ";
    CubeNodeG3_2 cube_node_g3_2((Cube)cube_node_g3_1);
    stack<Cube::MOVE> s4 = this->findGoal(cube_node_g3_2, 14);// Should finish in <= 13 moves
    this->minMove += 4; // Prune R R' L L'

    cout << "Solving G4" << " -> ";
    CubeNode cube_node_g4((Cube)cube_node_g3_2);
    stack<Cube::MOVE> s5 = this->findLastGoal(cube_node_g4, 16);  // Should finish in <= 15 moves
    
    // Print solutions
    this->printSolution(s1);
    this->printSolution(s2);
    this->printSolution(s3);
    this->printSolution(s4);
    this->printSolution(s5);

    return s5;
}
