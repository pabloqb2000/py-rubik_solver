#include "IDDFSSolver.h"
#include <iostream>

/**
* Check if the next move should be skipped.
* @param move The index of a twist move, not yet applied.
* @param lastMove The last move index.
*/
bool IDDFSSolver::prune(Cube::MOVE move, Cube::MOVE lastMove) const
{
    typedef Cube::MOVE M;

    // Two twists of the same face.
    if ((move == M::L || move == M::LP || move == M::L2) &&
        (lastMove == M::L || lastMove == M::LP || lastMove == M::L2))
        return true;

    if ((move == M::R || move == M::RP || move == M::R2) &&
        (lastMove == M::R || lastMove == M::RP || lastMove == M::R2))
        return true;

    if ((move == M::U || move == M::UP || move == M::U2) &&
        (lastMove == M::U || lastMove == M::UP || lastMove == M::U2))
        return true;

    if ((move == M::D || move == M::DP || move == M::D2) &&
        (lastMove == M::D || lastMove == M::DP || lastMove == M::D2))
        return true;

    if ((move == M::F || move == M::FP || move == M::F2) &&
        (lastMove == M::F || lastMove == M::FP || lastMove == M::F2))
        return true;

    if ((move == M::B || move == M::BP || move == M::B2) &&
        (lastMove == M::B || lastMove == M::BP || lastMove == M::B2))
        return true;
    // Commutative moves.
    if ((move == M::F || move == M::FP || move == M::F2) &&
        (lastMove == M::B || lastMove == M::BP || lastMove == M::B2))
        return true;

    if ((move == M::L || move == M::LP || move == M::L2) &&
        (lastMove == M::R || lastMove == M::RP || lastMove == M::R2))
        return true;

    if ((move == M::U || move == M::UP || move == M::U2) &&
        (lastMove == M::D || lastMove == M::DP || lastMove == M::D2))
        return true;

    return false;
}

/**
* Use IDDFS to find a path from the given node
* to a goal node
* @param cube Initial scrambled cube
**/
stack<Cube::MOVE> IDDFSSolver::findGoal(CubeNode& cube, uint8_t maxDepth) {
    stack<tuple<Cube::MOVE, uint8_t>> dfs_stack;
    tuple<Cube::MOVE, uint8_t> actual_node;
    uint8_t d;
    int8_t last_depth=0;
    Cube::MOVE actual_move;

    for(uint8_t depth = 0; depth < maxDepth; depth++) {
        dfs_stack.push(make_tuple(Cube::MOVE::NONE, 0));
        cout << "Depth: " << unsigned(depth) << endl;

        while(!dfs_stack.empty()) {

            actual_node = dfs_stack.top();
            actual_move = get<0>(actual_node);
            d = get<1>(actual_node);
            dfs_stack.pop();

            for(int8_t i = 0; i < last_depth - d + 1; i++)
                cube.invert();
            cube.move(actual_move);

            if(d < depth) {
                for(uint8_t i = 0; i < 18; i++) {
                    if(!this->prune(actual_move, (Cube::MOVE)i)) {
                        dfs_stack.push(make_tuple((Cube::MOVE)i, d+1));
                    }
                }
            } else{
                if (cube.isGoal()) {
                    return cube.getStack();
                }
            }

            last_depth = d;
        }
    }

    stack<Cube::MOVE> emptyStack;
    return emptyStack;
}


/**
* Print solution on stdoutput
**/
void IDDFSSolver::printSolution(stack<Cube::MOVE> solution, int maxMovesPerLine) {
    stack<Cube::MOVE> reverseSolution;
    uint8_t i = 0;

    while(!solution.empty()) {
        reverseSolution.push(solution.top());
        solution.pop();
    }

    reverseSolution.pop(); // Delete the NONE move
    while(!reverseSolution.empty()) {
        cout << move_names[(uint8_t)reverseSolution.top()] << ", ";
        if(i > maxMovesPerLine) {
            i = 0;
            cout << endl;
        }
        i++;
        reverseSolution.pop();
    }
    cout << endl;
}
