#ifndef IDDFSSOLVER_H
#define IDDFSSOLVER_H

#include "GroupNodes/CubeNode.h"
#include <stack>
#include <tuple> 
using namespace std;

#define MAXDEPTH 14

class IDDFSSolver
{
    protected:
        bool prune(Cube::MOVE move, Cube::MOVE lastMove) const;
        uint8_t minMove;
        uint8_t maxMove;

    public:
        IDDFSSolver(uint8_t minMove=0, uint8_t maxMove=18);

        stack<Cube::MOVE> findGoal(
            CubeNode& cube, 
            uint8_t maxDepth=MAXDEPTH+1
        );

        stack<Cube::MOVE> findLastGoal(
            CubeNode& cube,
            uint8_t maxDepth
        );

        void printSolution(stack<Cube::MOVE> solution, int maxMovesPerLine=16);
};


#endif