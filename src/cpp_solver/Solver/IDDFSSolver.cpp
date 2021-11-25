#include "IDDFSSolver.h"
#include <iostream>

IDDFSSolver::IDDFSSolver(uint8_t minMove, uint8_t maxMove)
{
    this->minMove = minMove;
    this->maxMove = maxMove;
}

/**
* Check if the next move should be skipped.
* @param move The index of a twist move, not yet applied.
* @param lastMove The last move index.
*/
bool IDDFSSolver::prune(Cube::MOVE move, Cube::MOVE lastMove) const
{
    typedef Cube::MOVE M;

    // Two twists of the same face.
    if ((move == M::R || move == M::RP || move == M::R2) &&
        (lastMove == M::R || lastMove == M::RP || lastMove == M::R2))
        return true;

    if ((move == M::L || move == M::LP || move == M::L2) &&
        (lastMove == M::L || lastMove == M::LP || lastMove == M::L2))
        return true;

    if ((move == M::F || move == M::FP || move == M::F2) &&
        (lastMove == M::F || lastMove == M::FP || lastMove == M::F2))
        return true;

    if ((move == M::B || move == M::BP || move == M::B2) &&
        (lastMove == M::B || lastMove == M::BP || lastMove == M::B2))
        return true;

    if ((move == M::U || move == M::UP || move == M::U2) &&
        (lastMove == M::U || lastMove == M::UP || lastMove == M::U2))
        return true;

    if ((move == M::D || move == M::DP || move == M::D2) &&
        (lastMove == M::D || lastMove == M::DP || lastMove == M::D2))
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
    typedef Cube::MOVE M;

    stack<M> move_stack;
    stack<uint8_t> depth_stack;
    uint8_t d;
    int8_t last_depth=0;
    M actual_move;
    for(uint8_t i = this->minMove; i < this->maxMove; i++) cout << move_names[i] << " ";
    cout << endl;

    for(uint8_t depth = 0; depth < maxDepth; depth++) {
        move_stack.push(M::NONE);
        depth_stack.push(0);
        if (depth != 0) cout << "\033[F";
        cout << "Depth: " << unsigned(depth) << endl;

        while(!depth_stack.empty()) {
            actual_move = move_stack.top();
            d = depth_stack.top();
            move_stack.pop();
            depth_stack.pop();

            for(int8_t i = -1; i < last_depth - d; i++)
                cube.invert();
            cube.move(actual_move);

            if(d < depth) {
                d++;
                for(uint8_t i = this->minMove; i < this->maxMove; i++) {
                    if(!this->prune(actual_move, (M)i)) {
                        move_stack.push((M)i);
                        depth_stack.push(d);
                    }
                }
                d--;
            } else {
                if (cube.isGoal()) {
                    cout << "FOUND GOAL" << endl << endl;
                    return cube.getStack();
                }
            }

            last_depth = d;
        }
    }

    stack<M> emptyStack;
    return emptyStack;
}

/**
* Use IDDFS to find a path from the given node
* to a goal node
* @param cube Initial scrambled cube
**/
stack<Cube::MOVE> IDDFSSolver::findLastGoal(CubeNode& cube, uint8_t maxDepth) {
    typedef Cube::MOVE M;

    stack<M> move_stack;
    stack<uint8_t> depth_stack;
    uint8_t d;
    int8_t last_depth=0;
    M actual_move;
    M new_move;
    for(uint8_t i = this->minMove; i < this->maxMove; i++) cout << move_names[i] << " ";
    cout << endl;

    for(uint8_t depth = 0; depth < maxDepth; depth++) {
        move_stack.push(M::NONE);
        depth_stack.push(0);
        if (depth != 0) cout << "\033[F";
        cout << "Depth: " << unsigned(depth) << endl;

        while(!depth_stack.empty()) {
            actual_move = move_stack.top();
            d = depth_stack.top();
            move_stack.pop();
            depth_stack.pop();

            for(int8_t i = -1; i < last_depth - d; i++)
                cube.invert();
            cube.move(actual_move);

            if(d < depth) {
                d++;
                for(uint8_t i = this->minMove; i < this->maxMove; i++) {
                    new_move = (M)i;
                    if(actual_move != new_move && !(
                        (new_move == M::F2 && actual_move == M::B2) ||
                        (new_move == M::L2 && actual_move == M::R2) ||
                        (new_move == M::U2 && actual_move == M::D2)
                    )) {
                        move_stack.push(new_move);
                        depth_stack.push(d);
                    }
                }
                d--;
            } else {
                if (cube.isSolved()) {
                    cout << "FOUND GOAL" << endl << endl;
                    return cube.getStack();
                }
            }

            last_depth = d;
        }
    }

    stack<M> emptyStack;
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
